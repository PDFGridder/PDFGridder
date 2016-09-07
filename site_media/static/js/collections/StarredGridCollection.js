StarredGridCollection = Backbone.Collection.extend({
    url: '/api/v1/grids/?star=True',
    model: Grid
});