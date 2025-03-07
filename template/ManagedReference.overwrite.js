var common = require('./ManagedReference.common.js');

exports.getOptions = function (model) {
    var ignoreChildrenBookmarks = model._splitReference && model.type && common.getCategory(model.type) === 'ns';
    
    return {
        isShared: true,
        bookmarks: common.getBookmarks(model, ignoreChildrenBookmarks)
    };
}