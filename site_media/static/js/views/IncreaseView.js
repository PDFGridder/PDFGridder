IncreaseView = GenericView.extend({
    events: {
        "change input.value": "setValue"
    },
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.param = options.parameter;

        this.valueElement = this.$('input.value');
        this.valueElement.increase_widget({min: 1});

        _.bindAll(this, 'getValue', 'showErrors');
        this.setValue();
        this.model.bind('change:'+this.param, this.getValue);
    },
    setValue: function() {
        params = {};
        this.value = parseInt(this.valueElement.val(), 10);
        params[this.param] = this.value;
        this.clearErrors();
        this.model.set(params, {'error': this.showErrors});
    },
    getValue: function() {
        value = this.model.get(this.param);
        if (value != this.value) {
            this.value = value;
            this.valueElement.val(this.value);
        }
    },
    clearErrors: function() {
        $(this.el).removeClass('error');
        $(this.el).siblings('.errorMessage').slideUp(function() {
            $(this).remove();
        });
    },
    showErrors: function(model, errors) {
        if (this.valueElement.val() !== '') {
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