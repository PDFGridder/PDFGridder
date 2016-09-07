UnitView = GenericView.extend({
    events: {
        "change": "setValue"
    },
    tagName: 'select',
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.param = options.parameter;

        this.unitElement = $(this.el);
        this.setValue();
        _.bindAll(this, 'getValue', 'showErrors');
        this.model.bind('change:'+this.param, this.getValue);
        this.getValue();
    },
    setValue: function() {
        this.value = this.unitElement.val();
        if (this.model.get(this.param) != this.value) {
            params = {};
            params[this.param] = this.value;
            this.clearErrors();
            this.model.set(params, {'error': this.showErrors });
        }
    },
    getValue: function() {
        if (this.model.get(this.param) != this.value) {
            value = this.model.get(this.param);
            this.unitElement.val(value);
            this.value = value;
        }
    },
    showErrors: function(model, errors) {
        return this.parentView.showErrors(model, errors);
    },
    clearErrors: function() {
        return this.parentView.clearErrors();
    }
});