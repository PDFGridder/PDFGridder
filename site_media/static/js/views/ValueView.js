ValueView = GenericView.extend({
    events: {
        "change": "highlightInteger"
    },
    tagName: 'input',
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.param = options.parameter;

        this.valueElement = $(this.el);

        _.bindAll(this, 'getValue', 'showErrors', 'highlightInteger');
        this.setValue();
        this.model.bind('change:'+this.param, this.getValue);
        this.getValue();
        this.valueElement.trigger('change');
    },
    setValue: function() {
        params = {};
        this.value = this.fixComma(this.valueElement.val());
        if (!isNaN(this.value) && this.value >= 0) {
            params[this.param] = this.value;
            this.clearErrors();
            this.model.set(params, {'error': this.showErrors });
        }
    },
    fixComma: function(value) {
        // fixes comma/dot decimal separator
        parsed = parseFloat(value.replace(',','.'));
        if (_.isNumber(parsed)) return parsed;
        return NaN;
    },
    prettyPrint: function(value) {
        if (_.isNumber(value)) return value.toFixed(2);
        return NaN;
    },
    highlightInteger: function() {
        this.setValue();
        value = this.fixComma(this.valueElement.val());
        if ((value.toFixed(2) % 1) === 0) {
            this.valueElement.parent().addClass('success');
        } else {
            this.valueElement.parent().removeClass('success');
        }
    },
    getValue: function() {
        value = this.model.get(this.param);
        if (value != this.value) {
            this.value = value;
            this.valueElement.val(this.prettyPrint(this.value));
        }

    },
    showErrors: function(model, errors) {
        return this.parentView.showErrors(model, errors);
    },
    clearErrors: function() {
        return this.parentView.clearErrors();
    }
});