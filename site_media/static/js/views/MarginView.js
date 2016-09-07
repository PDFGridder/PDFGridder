MarginView = MeasureView.extend({
    initialize: function(options) {
        MeasureView.prototype.initialize.call(this, options);

        this.model.bind('change:is_spread', this.changeLabel, this);
        this.changeLabel();
    },
    changeLabel: function() {
        if (this.param == 'margin_left') {
            if (this.model.get('is_spread')) {
                this.label.text('Inside');
            } else {
                this.label.text('Left');
            }
        } else if (this.param == 'margin_right') {
            if (this.model.get('is_spread')) {
                this.label.text('Outside');
            } else {
                this.label.text('Right');
            }
        }
    }
});
