TitleView = GenericView.extend({
    tagName: 'h2',
    events: {
        "keyup": "setValue"
    },
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.param = options.parameter;

        this.model.bind('change:'+this.param, this.getValue, this);
        this.parentView.bind('change:model', this.getValue, this);
        this.setValue();
    },
    setValue: function() {
        params = {};
        if (this.$('input')) {
            this.value = $(this.$('input')).val();
        } else {
            this.value = $(this.el).text();
        }
        params[this.param] = this.value;
        this.model.set(params);
    },
    getValue: function() {
        if (this.$('input')) {
            $(this.$('input')).val(this.model.get(this.param));
        } else {
            $(this.el).text(this.model.get(this.param));
        }
    }
});