var MeasureView = GenericView.extend({
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.param = options.parameter;

        this.valueView = new ValueView({
            parentView: this,
            el: this.$('input.value'),
            model: this.model,
            parameter: this.param
        });
        this.unitView = new UnitView({
            parentView: this,
            el: this.$('.units'),
            model: this.model,
            parameter: this.param+'_unit'
        });
        this.label = this.$('label');
        _.bindAll(this, 'showErrors');
    },
    clearErrors: function() {
        $(this.el).removeClass('error');
        $(this.el).siblings('.errorMessage').slideUp(function() {
            $(this).remove();
        });
    },
    showErrors: function(model, errors) {
        if (this.valueView && this.valueView.valueElement.val() !== '') {
            $(this.el).removeClass('success').addClass('error');
            errorList = errors[this.param];
            _.each(errorList, function(error) {
                errorSpan = $('<p class="errorMessage">'+error+'</p>');
                $(this.el).before(errorSpan);
                errorSpan.slideDown();
            }, this);
        }
    }
});