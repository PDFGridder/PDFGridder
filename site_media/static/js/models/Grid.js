var Grid = Backbone.Model.extend({
    defaults: {
        'name': 'Untitled',
        'width': 210,
        'width_unit': 'mm',

        'height': 297,
        'height_unit': 'mm',

        'margin_top': 5,
        'margin_top_unit': 'mm',
        'margin_bottom': 5,
        'margin_bottom_unit': 'mm',
        'margin_left': 5,
        'margin_left_unit': 'mm',
        'margin_right': 5,
        'margin_right_unit': 'mm',

        'columns': 7,
        'columns_color': '#eeeeee',
        'columns_opacity': 1.0,
        'columns_width': 26,
        'columns_width_unit': 'mm',
        'columns_gutter': 3,
        'columns_gutter_unit': 'mm',

        'baseline': 15,
        'baseline_unit': 'pt',
        'baseline_color': "#c0c0c0",
        'baseline_opacity': 1.0
    },
    validators: {
        'width': 'isPositiveNumber',
        'height': 'isPositiveNumber',

        'margin_top': 'isPositiveNumber',
        'margin_bottom': 'isPositiveNumber',
        'margin_left': 'isPositiveNumber',
        'margin_right': 'isPositiveNumber',

        'columns': 'isInteger',
        'columns_color': 'isColor',
        'columns_opacity': 'isAlpha',
        'columns_width': 'isPositiveNumber',
        'columns_gutter': 'isPositiveNumber',

        'baseline': 'isPositiveNumber',
        'baseline_color': 'isColor',
        'baseline_opacity': 'isAlpha',

        'summary': 'isString',
        'created': 'isDate'
    },
    unitAttributes: [
        'width_unit',
        'height_unit',
        'margin_top_unit',
        'margin_bottom_unit',
        'margin_left_unit',
        'margin_right_unit',
        'columns_gutter_unit',
        'columns_width_unit',
        'baseline_unit'
    ],
    widthAttributes: [
        'width',
        'margin_left',
        'margin_right',
        'columns',
        'columns_gutter'
    ],
    initialize: function() {
        this.collection = new GridCollection();
        if (!this.id) {
            this.set(this.defaults, {silent: true});
        }
        this.setColumnsWidthForInnerArea();

        _.each(this.widthAttributes, function(k) {
            this.bind('change:'+k, this.setColumnsWidthForInnerArea, this);
        }, this);

        this.bind('change:columns_width', this.setGutterWidthForInnerArea);

        this.bind('change:columns', this.updateSummary, this);
        this.bind('change:columns_gutter', this.updateSummary, this);
        this.bind('change:columns_gutter_unit', this.updateSummary, this);
        this.bind('change:baseline', this.updateSummary, this);
        this.bind('change:baseline_unit', this.updateSummary, this);
        this.bind('change:is_spread', this.updateSummary, this);

        _.each(this.unitAttributes, function(k) {
            this.bind('change:'+k, this.updateValue, this);
        }, this);
    },
    innerAreaWidth: function() {
        page_width = this.normalize('width');
        margin_left = this.normalize('margin_left');
        margin_right = this.normalize('margin_right');
        inner_width = page_width-margin_left-margin_right;

        return inner_width;
    },
    columnsWidthForInnerArea: function() {
        settings = {
            'gutter': this.normalize('columns_gutter'),
            'colsN': this.get('columns'),
            'areaWidth': this.innerAreaWidth()
        };

        width = (settings.areaWidth-(settings.gutter*(settings.colsN-1)))/settings.colsN;
        return this.convertValueToUnit(width, this.get('columns_width_unit'));
    },
    gutterWidthForInnerArea: function() {
        settings = {
            'columnsWidth': this.normalize('columns_width'),
            'colsN': this.get('columns'),
            'areaWidth': this.innerAreaWidth()
        };

        gutter = (settings.areaWidth - (settings.columnsWidth*settings.colsN)) / (settings.colsN-1);
        return this.convertValueToUnit(gutter, this.get('columns_gutter_unit'));
    },
    setGutterWidthForInnerArea: function() {
        this.set({'columns_gutter': this.gutterWidthForInnerArea()});
    },
    setColumnsWidthForInnerArea: function() {
        if (this.get('columns_gutter')) {
            this.set({'columns_width': this.columnsWidthForInnerArea()});
        }
    },
    normalizeFromUnit: function(param, unit) {
        val = this.get(param);
        return val*UNITS[unit];
    },
    normalize: function(param) {
        unit = this.get(param+'_unit');
        return this.normalizeFromUnit(param, unit);
    },
    convertValueToUnit: function(val, unit) {
        return val/UNITS[unit];
    },
    convertToUnit: function(param, unit) {
        val = this.get(param);
        return this.convertValueToUnit(val, unit);
    },
    convert: function(param) {
        unit = this.get(param+'_unit');
        return this.convertToUnit(param, unit);
    },
    switchUnits: function(newUnit) {
        var unit = newUnit;
        _.each(this.unitAttributes, function(k) {
            this.set(k, 'px');
        }, this);
    },
    getAbsolute: function(k, v) {
        unit = this.get(k+'_unit');
        value = this.convertValueToUnit(v, unit);
        return value;
    },
    noopValidator: function(value) {
        return true;
    },
    isPositiveNumber: function(value) {
        if (_.isNaN(value) || !_.isNumber(value) || value < 0) {
            return "This value should be a positive Number.";
        }
        return true;
    },
    isInteger: function(value) {
        isPositiveNumber = this.isPositiveNumber(value);
        if (isPositiveNumber === true ) {
            if (value % 1 !== 0) {
                return "This value must be an Integer.";
            }
        }
        return isPositiveNumber;
    },
    isDate: function(value) {
        if (_.isString(value)) {
            value = new Date(value);
        }
        if (!_.isDate(value)) {
            return "This value must be a valid date.";
        }
        return true;
    },
    isAlpha: function(value) {
        if (_.isString(value)) {
            value = parseFloat(value);
        }
        isPositiveNumber = this.isPositiveNumber(value);

        if (isPositiveNumber === true ) {
            if (value < 0 || value > 1) {
                return "This value must be between 0 and 1.";
            }
        }
        return isPositiveNumber;
    },
    isColor: function(value) {
        if (value.match(/#[0-9,a-f,A-F]{3,6}/) === null) {
            return ("This value must be a valid hex color");
        }
        return true;
    },
    isString: function(value) {
        if (!_.isString(value)) {
            return "This value must be a string.";
        }
        return true;
    },
    validateValue: function(validatorName, value) {
        return this[validatorName](value);
    },
    validate: function(attrs) {
        errors = {};
        ctx = {
            model: this,
            errors: errors
        };
        _.each(attrs, function(value, key, attrs) {
            validator = this.model.validators[key];
            if (validator) {
                validatorResult = this.model.validateValue(validator, value);
                if (validatorResult !== true) {
                    if (_.isUndefined(this.errors[key])) {
                        this.errors[key] = [];
                    }
                    this.errors[key].push(validatorResult);
                }
            }
        }, ctx);
        if (!_.isEmpty(errors)) {
            return errors;
        }
    },
    buildSummary: function() {
        if (this.get('is_spread')) {
            summary = 'Spread, ';
        } else {
            summary = '';
        }
        summary += this.get('columns')+' cols, gutter '+this.get('columns_gutter').toFixed(1)+this.get('columns_gutter_unit')+', baseline '+this.get('baseline').toFixed(1)+this.get('baseline_unit');

        return summary;
    },
    updateValue: function() {
        _.each(this.changedAttributes(), function(v, k) {
            if (_.include(this.unitAttributes, k)) {
                param = k.split('_').slice(0, -1).join('_');
                newValue = this.normalizeFromUnit(param, this.previous(k))/UNITS[this.get(k)];
                params = {};
                params[param] = newValue;
                this.set(params);
            }
        }, this);
    },
    updateSummary: function() {
        this.set({summary: this.buildSummary()});
    }
});
