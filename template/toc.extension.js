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
    let items = [
      {
        'name': 'Core Operators',
        'href' : `core${suffix}.html`,
        'topicHref': `core${suffix}.html`,
        'topicUid': `core${suffix}`,
        'items': []
      },
      {
        'name': 'Configuration Operators',
        'href' : `configure${suffix}.html`,
        'topicHref': `configure${suffix}.html`,
        'topicUid': `configure${suffix}`,
        'items': []
      },
      {
        'name': 'Data I/O Operators',
        'href' : `dataio${suffix}.html`,
        'topicHref': `dataio${suffix}.html`,
        'topicUid': `dataio${suffix}`,
        'items': []
      },
      {
        'name': 'Data Elements',
        'href' : `data-elements${suffix}.html`,
        'topicHref': `data-elements${suffix}.html`,
        'topicUid': `data-elements${suffix}`,
        'items': []
      },
      {
        'name': 'Other',
        'topicUid': `other${suffix}`,
        'items':
        [
          {
            'name': 'Device Configuration Operators',
            'href' : `device-configure${suffix}.html`,
            'topicHref': `device-configure${suffix}.html`,
            'topicUid': `device-configure${suffix}`,
            'items': []
          },
          {
            'name': 'Constants',
            'href' : `constants${suffix}.html`,
            'topicHref': `constants${suffix}.html`,
            'topicUid': `constants${suffix}`,
            'items': []
          }
        ]
      }
    ];
    for (const child of namespace.items)
    {
      if (child.name.endsWith('Attribute')) continue;
      globalYml = '~/api/' + child.topicUid + '.yml';
      globalModel = model.__global._shared[globalYml];
      if (globalModel?.type === 'class' || globalModel?.type === 'struct')
      {
        if (child.name.includes('CreateContext') || child.name.includes('StartAcquisition'))
        {
          items[0].items.push(child);
        }
        else if (globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.MultiDeviceFactory'))
        {
          items[1].items.push(child);
        }
        else if (globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.SingleDeviceFactory'))
        {
          items[4].items[0].items.push(child);
        }
        else if ((globalModel.syntax?.content[0].value.includes('ElementCategory.Source') ||
        globalModel.syntax?.content[0].value.includes('ElementCategory.Sink') ||
        globalModel?.inheritance.some(inherited => inherited.uid.includes('Bonsai.Source')) ||
        globalModel?.inheritance.some(inherited => inherited.uid.includes('Bonsai.Sink'))) &&
        !globalModel.syntax?.content[0].value.includes('abstract'))
        {
          items[2].items.push(child);
        }
        else if (child.name.includes('ContextTask') ||
        child.name.includes('OutputClockParameters') ||
        child.name.includes('DataFrame') ||
        globalModel?.inheritance.some(inherited => inherited.uid === 'OpenEphys.Onix1.DataFrame' || inherited.uid === 'OpenEphys.Onix1.BufferedDataFrame'))
        {
          items[3].items.push(child);
        }
      }
      else if (globalModel && globalModel.type === 'enum')
      {
        items[4].items[1].items.push(child);
      }
    }
    items[4].items = items[4].items.filter(sub => sub.items.length > 0);
    namespace.items = items.filter(bucket => bucket.items.length > 0);
  }
  return model;
}

/**
 * This method will be called at the end of exports.transform in toc.html.js and toc.json.js
 */
exports.postTransform = function (model) {
  return model;
}
