AppView = Backbone.View.extend({
    initialize: function() {
        _.bindAll(this, 'changeModel');
        this.collection.on('reset', this.setupGridList, this);
        this.collection.fetch();
        grid_data = {};
        this.setup();
    },
    setup: function(model) {

        this.titleView = new TitleView({
            el: $('h2.pageTitle'),
            model: this.model,
            parentView: this,
            parameter: 'name'
        });
        this.controlsView = new ControlsView({
            el: $("#gridder"),
            model: this.model,
            parentView: this
        });

        this.rightGridView = new GridView({
            el: $("#right_page"),
            model: this.model,
            parentView: this,
            page: 'right'
        });

        this.leftGridView = new GridView({
            el: $("#left_page"),
            model: this.model,
            parentView: this,
            page: 'left'
        });
    },
    setupGridList: function(collection) {
        this.gridListView = new GridListView({
            el: $('#recents'),
            parentView: this,
            collection: this.collection
        });
    },
    changeModel: function(model) {
        this.model = model;
        this.trigger('change:model');
    }
});