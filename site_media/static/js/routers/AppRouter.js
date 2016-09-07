AppRouter = Backbone.Router.extend({
    routes: {
        "": "new_grid",
        "_=_": "redirectToRoot",
        "grids/:grid_id/": "grid_detail"
    },
    initialize: function(options) {
        this.root = options.root;
    },
    absoluteNavigate: function(url, trigger) {
        var fragment = url.replace(this.root, '');
        return this.navigate(fragment, trigger);
    },
    startApp: function(model) {
        if (!window.app) {
            window.app = new AppView({model:model, collection: window.collection});
        } else {
            window.app.changeModel(model);
        }
    },
    redirectToRoot: function() {
        return this.navigate('/', {trigger: true});
    },
    new_grid: function() {
        model = new Grid({'user_id': window.user_id});
        this.startApp(model);
    },
    grid_detail: function(grid_id) {
        model = window.collection.detect(function(grid) {
            return grid.get('id') == window.object_id;
        });
        if (!model) {
            model = new Grid({id: window.object_id});
        }
        model.fetch({success: this.startApp});
    }
});
