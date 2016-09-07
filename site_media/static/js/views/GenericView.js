var GenericView = Backbone.View.extend({
    initialize: function(options) {
        this.parentView = options.parentView;
        if (this.parentView.model) {
            this.parentView.bind('change:model', this.changeModel, this);
        }
    },
    changeModel: function() {
        this.model = this.parentView.model;
        this.trigger('change:model');
    }
});