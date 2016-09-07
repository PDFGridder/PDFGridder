ColorPickerView = GenericView.extend({
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);
        this.param_group = options.param_group;

        this.colorView = new ColorView({
            el: this.$('.color_picker'),
            parentView: this,
            parameter: this.param_group+'_color',
            colorElement: this.$('#id_'+this.param_group+'_color'),
            model: this.model
        });

        this.opacityView = new OpacityView({
            el: this.$('.opacity_slider'),
            parentView: this,
            parameter: this.param_group+'_opacity',
            opacityElement: this.$('#id_'+this.param_group+'_opacity'),
            model: this.model
        });
    },
    render: function() {
        this.colorView.render();
        this.opacityView.render();
        return this;
    }
});