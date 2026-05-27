// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

/**
 * This method will be called at the start of exports.transform in toc.html.js and toc.json.js
 */
exports.preTransform = function (model) {
  for (const namespace of model.items) {
    if (!namespace.name.startsWith('OpenEphys.Onix1')) continue;
    if (namespace.name.includes('Design')) continue;
    if (!namespace.items) continue;
    const suffix = namespace.name === 'OpenEphys.Onix1' ? '' : '-' + namespace.name.split('.').pop().toLowerCase();
    let items = {
      core: {
        'name': 'Core Operators',
        'href' : `core${suffix}.html`,
        'topicHref': `core${suffix}.html`,
        'topicUid': `core${suffix}`,
        'items': []
      },
      configure: {
        'name': 'Configuration Operators',
        'href' : `configure${suffix}.html`,
        'topicHref': `configure${suffix}.html`,
        'topicUid': `configure${suffix}`,
        'items': []
      },
      dataSource: {
        'name': 'Data Source Operators',
        'href' : `datasource${suffix}.html`,
        'topicHref': `datasource${suffix}.html`,
        'topicUid': `datasource${suffix}`,
        'items': []
      },
      dataSink: {
        'name': 'Data Sink Operators',
        'href' : `datasink${suffix}.html`,
        'topicHref': `datasink${suffix}.html`,
        'topicUid': `datasink${suffix}`,
        'items': []
      },
      dataElements: {
        'name': 'Data Elements',
        'href' : `data-elements${suffix}.html`,
        'topicHref': `data-elements${suffix}.html`,
        'topicUid': `data-elements${suffix}`,
        'items': []
      },
      other: {
        'name': 'Other',
        'topicUid': `other${suffix}`,
        'items': {
          deviceConfigure: {
            'name': 'Device Configuration Operators',
            'href' : `device-configure${suffix}.html`,
            'topicHref': `device-configure${suffix}.html`,
            'topicUid': `device-configure${suffix}`,
            'items': []
          },
          constants: {
            'name': 'Constants',
            'href' : `constants${suffix}.html`,
            'topicHref': `constants${suffix}.html`,
            'topicUid': `constants${suffix}`,
            'items': []
          }
        }
      }
    };
    for (const child of namespace.items)
    {
      if (child.name.endsWith('Attribute')) continue;
      globalYml = '~/api/' + child.topicUid + '.yml';
      globalModel = model.__global._shared[globalYml];
      if (globalModel?.type === 'class' || globalModel?.type === 'struct')
      {
        if (child.name.includes('CreateContext') || child.name.includes('StartAcquisition'))
        {
          items.core.items.push(child);
        }
        else if (globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.MultiDeviceFactory'))
        {
          items.configure.items.push(child);
        }
        else if (globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.SingleDeviceFactory'))
        {
          items.other.items.deviceConfigure.items.push(child);
        }
        else if ((globalModel.syntax?.content[0].value.includes('ElementCategory.Source') ||
        globalModel?.inheritance.some(inherited => inherited.uid.includes('Bonsai.Source'))) &&
        !globalModel.syntax?.content[0].value.includes('abstract'))
        {
          items.dataSource.items.push(child);
        }
        else if ((globalModel.syntax?.content[0].value.includes('ElementCategory.Sink') ||
        globalModel?.inheritance.some(inherited => inherited.uid.includes('Bonsai.Sink'))) &&
        !globalModel.syntax?.content[0].value.includes('abstract'))
        {
          items.dataSink.items.push(child);
        }
        else if (child.name.includes('ContextTask') ||
        child.name.includes('OutputClockParameters') ||
        child.name.includes('DataFrame') ||
        globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.DataFrame' || inherited.uid === 'OpenEphys.Onix1.BufferedDataFrame'))
        {
          items.dataElements.items.push(child);
        }
      }
      else if (globalModel && globalModel.type === 'enum')
      {
        items.other.items.constants.items.push(child);
      }
    }
    items.other.items = Object.values(items.other.items).filter(sub => sub.items.length > 0);
    namespace.items = Object.values(items).filter(bucket => bucket.items.length > 0);
  }
  return model;
}

/**
 * This method will be called at the end of exports.transform in toc.html.js and toc.json.js
 */
exports.postTransform = function (model) {
  return model;
}
