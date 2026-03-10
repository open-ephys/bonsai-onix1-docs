// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

/**
 * This method will be called at the start of exports.transform in toc.html.js and toc.json.js
 */
exports.preTransform = function (model) {
  if (model.items[0].name === 'OpenEphys.Onix1'){
    if (model.items[0].items){
      itemsItemsLength = model.items[0].items.length;
      let items = [
        {
          'name': 'Core Operators',
          'href' : 'core.html',
          'topicHref': 'core.html',
          'topicUid': 'core',
          'items': []
        }, 
        {
          'name': 'Configuration Operators',
          'href' : 'configure.html',
          'topicHref': 'configure.html',
          'topicUid': 'configure',
          'items': []
        }, 
        {
          'name': 'Data I/O Operators',
          'href' : 'dataio.html',
          'topicHref': 'dataio.html',
          'topicUid': 'dataio',
          'items': []
        }, 
        {
          'name': 'Data Elements',
          'href' : 'data-elements.html',
          'topicHref': 'data-elements.html',
          'topicUid': 'data-elements',
          'items': []
        }, 
        {
          'name': 'Other',
          'topicUid': 'other',
          'items': 
          [
            {
              'name': 'Device Configuration Operators',
              'href' : 'device-configure.html',
              'topicHref': 'device-configure.html',
              'topicUid': 'device-configure',
              'items': []
            },
            {
              'name': 'Constants',
              'href' : 'constants.html',
              'topicHref': 'constants.html',
              'topicUid': 'constants',
              'items': []
            }
          ]
        }
      ];
      for (let i = 0; i < itemsItemsLength; i++) 
      {
        globalYml = '~/api/' + model.items[0].items[i].topicUid + '.yml';
        globalModel = model.__global._shared[globalYml];
        if (globalModel?.type === 'class' || globalModel?.type === 'struct')
        {
          if (model.items[0].items[i].name.includes('CreateContext') || model.items[0].items[i].name.includes('StartAcquisition'))
          {
            items[0].items.push(model.items[0].items[i]);
          }
          else if (globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.MultiDeviceFactory'))
          {
            items[1].items.push(model.items[0].items[i]);
          }
          else if (globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.SingleDeviceFactory'))
          {
            items[4].items[0].items.push(model.items[0].items[i]);
          }
          else if ((globalModel.syntax?.content[0].value.includes('ElementCategory.Source') || 
          globalModel.syntax?.content[0].value.includes('ElementCategory.Sink') ||
          globalModel?.inheritance.some(inherited => inherited.uid.includes('Bonsai.Source')) ||
          globalModel?.inheritance.some(inherited => inherited.uid.includes('Bonsai.Sink'))) &&
          !globalModel.syntax?.content[0].value.includes('abstract'))
          {
            items[2].items.push(model.items[0].items[i]);
          }
          else if (model.items[0].items[i].name.includes('ContextTask') || 
          model.items[0].items[i].name.includes('OutputClockParameters') ||
          model.items[0].items[i].name.includes('DataFrame') ||
          globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.DataFrame' || inherited.uid === 'OpenEphys.Onix1.BufferedDataFrame'))
          {
            items[3].items.push(model.items[0].items[i]);
          }
        }
        else if (globalModel && globalModel.type === 'enum') 
        {
          items[4].items[1].items.push(model.items[0].items[i]);
        }
      }
      model.items[0].items = items;
    }
  }
  return model;
}

/**
 * This method will be called at the end of exports.transform in toc.html.js and toc.json.js
 */
exports.postTransform = function (model) {
  return model;
}
