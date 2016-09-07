OpacityView = GenericView.extend({
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        _.bindAll(this, 'setOpacity', 'setValue', 'showErrors');
        this.param = options.parameter;
        this.opacityElement = options.opacityElement;
        $(this.opacityElement).bind('change', this.setValue);
        this.setValue();
    },
    render: function() {
        this.opacitySlider = $('<div class="opacity_slider"></div>');

        this.opacitySlider.slider({
            min:0, max: 1, step: 0.01, value: 1, orientation: 'vertical',
            slide: this.setOpacity
        });
        $(this.el).append(this.opacitySlider);
        return this;
    },
    setOpacity: function(e, ui) {
        $('.farbtastic', $(this.el).parent()).css('opacity', ui.value);
        $(this.opacityElement).val(ui.value);
        $(this.opacityElement).trigger('change');
        return true;
    },
    setValue: function() {
        params = {};
        opacity = $(this.opacityElement).val();
        this.value = parseFloat(opacity);
        params[this.param] = this.value;
        this.clearErrors();
        this.model.set(params, {'error': this.showErrors });
    },
    clearErrors: function() {
        $(this.el).removeClass('error');
        $(this.el).siblings('.errorMessage').slideUp(function() {
            $(this).remove();
        });
    },
    showErrors: function(model, errors) {
        if (this.opacityElement.val() !== '') {
            $(this.el).addClass('error');
            errorList = errors[this.param];
            _.each(errorList, function(error) {
                errorSpan = $('<p class="errorMessage">'+error+'</p>');
                $(this.el).before(errorSpan);
                errorSpan.slideDown();
            }, this);
        }
    }
});