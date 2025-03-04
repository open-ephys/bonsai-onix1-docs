// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

function addCodeTag(remarks) {
  return remarks
    .replace('<td class=\"term\"> True </td>', '<td class=\"term\"><code> True </code></td>')
    .replace('<td class=\"term\"> False </td>', '<td class=\"term\"><code> False </code></td>');
}

function extractEnumData(model) {
  return model.children
    .filter(child => child.type === 'field')
    .map(child => ({
      'field&value': child.syntax.content[0].value,
      'description': [child.summary, child.remarks].join(''),
      'id': child.uid.replaceAll('.', '_'),
    }));
}

function sortPropertiesData(properties) {
  return properties.sort((a, b) => (
    a.name.match(/\D+|\d+$/g)[0] === b.name.match(/\D+|\d+$/g)[0] ?
      Number(a.name.match(/\D+|\d+$/g)[1]) - Number(b.name.match(/\D+|\d+$/g)[1]) :
      0
  ));
}

function processChildProperty(child, sharedModel) {
  const enumFields = sharedModel[`~/api/${child.syntax.return.type.uid}.yml`]?.type === 'enum' ?
    extractEnumData(sharedModel[`~/api/${child.syntax.return.type.uid}.yml`]) :
    [];
    const acquisition = child?.attributes.some(attribute => attribute.type === 'System.ComponentModel.CategoryAttribute' && attribute?.arguments[0].value === 'Acquisition');
    const configuration = child?.attributes.some(attribute => attribute.type === 'System.ComponentModel.CategoryAttribute' && attribute?.arguments[0].value === 'Configuration');
  return {
    'name': child.name[0].value,
    'type': child.syntax.return.type.specName[0].value,
    'propertyDescription': 
    {
      'text': addCodeTag([child.summary, child.remarks].join('')),
      'hasEnum': enumFields.length > 0,
      'enum': enumFields,
    },
    'configuration': configuration,
    'acquisition': acquisition,
    'id': child.uid.replaceAll('.', '_'),
  }
}

const filterProperties = propertyCandidate => propertyCandidate.type === 'property' && !propertyCandidate?.attributes.some(attribute => 
  attribute.type === 'System.ComponentModel.BrowsableAttribute' && attribute.arguments[0].value === false);

function extractPropertiesData(model, sharedModel) {
  return model?.children
    .filter(filterProperties)
    .map(child => processChildProperty(child, sharedModel));
}

function extractPropertiesFromInheritedMembersData(model, sharedModel) {
  return model.inheritedMembers
    .filter(filterProperties)
    .map(inheritedMember => 
    (
      processChildProperty
      (
        sharedModel[`~/api/${inheritedMember.parent}.yml`].children.find(inheritedMemberChild => inheritedMemberChild.uid === inheritedMember.uid),
        sharedModel
      )
    )
  );
}

function extractConstituentOperatorsData(model) {
  return model?.children
    .filter(child => child.type === 'property' && model.__global._shared?.[`~/api/${child.syntax.return.type.uid}.yml`].type === 'class')
    .map(child => 
      {
      const deviceModel = model.__global._shared?.[`~/api/${child.syntax.return.type.uid}.yml`];
      const properties = sortPropertiesData(extractPropertiesData(deviceModel, model.__global._shared));
      return {
        'object': child.name[0].value,
        'type': child.syntax.return.type.specName[0].value,
        'constituentOperator': true,
        'hasProperties': properties === undefined || properties.length === 0 ? false : true,
        'properties': properties,
        'id': child.uid.replaceAll('.', '_'),
      };
    }
  );
}

function extractOperatorData(model) {
  const checkForCategory = (category) => model.syntax?.content[0].value.includes(`[WorkflowElementCategory(ElementCategory.${category})]`);
  const checkInheritance = (inheritance) => model.inheritance?.some(inherited => inherited.uid.includes(inheritance));
  source = checkForCategory('Source') || checkInheritance('Bonsai.Source');
  sink = checkForCategory('Sink') || checkInheritance('Bonsai.Sink');
  combinator = checkForCategory('Combinator') || checkInheritance('Bonsai.Combinator');
  transform = checkForCategory('Transform') || checkInheritance('Bonsai.Transform');
  hub = checkInheritance('OpenEphys.Onix1.MultiDeviceFactory');
  configureDevice = checkInheritance('OpenEphys.Onix1.SingleDeviceFactory');
  type = model.uid.includes('DeviceFactory') ? false : sink ? 'sink' : combinator ? 'combinator' : source ? 'source' : transform ? 'transform' : false;
  if (hub) {model = model.__global._shared['~/api/OpenEphys.Onix1.MultiDeviceFactory.yml'];}
  overloads = model.children
    .filter(child => child.name[0].value.includes('Process') || child.name[0].value.includes('Generate'))
    .map(child => ({
      'overloadsDescription': [child.summary, child.remarks].join(''),
      'input': [child.syntax?.parameters[0].description, child.syntax?.parameters[0].remarks].join(''),
      'output': [child.syntax.return.description, child.syntax.return.remarks].join(''),
    }));
  return {
    'type': type,
    'hub': hub,
    'configureDevice': configureDevice,
    'workflow': type.length > 0,
    'overloads': overloads,
  }
}

/**
 * This method will be called at the start of exports.transform in ManagedReference.html.primary.js
 */
exports.preTransform = function (model) {
  if (model.type === 'class' || model.type === 'struct') {
    operator = extractOperatorData(model);
    if (operator.hub) {
      properties = extractConstituentOperatorsData(model);
      properties.unshift({
        'object': model.name[0].value.replace('Configure', ''),
        'constituentOperator': false,
        'hasProperties': true,
        'properties': sortPropertiesData([
          ...extractPropertiesData(model, model.__global._shared),
          ...extractPropertiesFromInheritedMembersData(model, model.__global._shared),
        ]).filter(modelProperty => !properties.map(property => property.object).includes(modelProperty?.name))
      });
    }
    else {
      properties = sortPropertiesData([
        ...extractPropertiesData(model, model.__global._shared),
        ...extractPropertiesFromInheritedMembersData(model, model.__global._shared),
      ]);
    }
    model.oe = {
      'name': model.name[0].value,
      'uid': model.uid,
      'description': [model.summary, model.remarks].join(''),
      'operator': operator,
      'properties': properties
    };
  }
  else if (model.type === 'enum') {
    model.oe = {
      'name': model.name[0].value,
      'uid': model.uid,
      'description': [model.summary, model.remarks].join(''),
      'enum': extractEnumData(model),
    };
  }

  return model;
}

/**
 * This method will be called at the end of exports.transform in ManagedReference.html.primary.js
 */
exports.postTransform = function (model) {
  return model;
}
