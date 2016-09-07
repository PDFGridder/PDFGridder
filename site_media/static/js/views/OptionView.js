OptionView = GenericView.extend({
    events: {
        "change": "setValue"
    },
    tagName: 'p',
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.param = options.parameter;

        this.checkboxElement = this.$('input');

        _.bindAll(this, 'getValue', 'setValue');
        this.setValue();
        this.model.bind('change:'+this.param, this.getValue);
        this.getValue();
    },
    setValue: function() {
        params = {};
        this.value = this.$('input').is(':checked');
        params[this.param] = this.value;
        this.model.set(params);
    },
    getValue: function() {
        value = this.model.get(this.param);
        if (value != this.value) {
            this.value = value;
        }
    }
});