ColorView = GenericView.extend({
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);
        _.bindAll(this, 'setColor', 'setValue');
        this.param = options.parameter;
        this.colorElement = options.colorElement;
        $(this.colorElement).change(this.setValue);
        this.setValue();
    },
    render: function() {
        this.colorPicker = $('<div class="color_picker"></div>');
        this.colorPicker.farbtastic(this.setColor);
        $(this.el).append(this.colorPicker);
        return this;
    },
    setColor: function(color) {
        field = $(this.colorElement);
        $(field).css({backgroundColor: color});
        $(field).val(color);
        $(field).trigger('change');
    },
    setValue: function() {
        params = {};
        color = $(this.colorElement).val();
        this.value = color;
        params[this.param] = this.value;
        this.model.set(params);
    }
});