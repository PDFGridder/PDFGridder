var ControlsView = GenericView.extend({
    events: {
        'click #units button': 'switchSystem',
        'change #paper_size': 'changePageFormat',
        'click #id_save_as': 'openSaveAs',
        'click #id_save_as_confirm': 'saveAs',
        'click #options_colors': 'toggleColors',
        'click #id_submit': 'downloadPDF',
        'click #id_downloadINX': 'downloadINX',
        'click #id_downloadIDML': 'downloadIDML',
        'click #id_downloadCSS': 'downloadCSS',
        'click #id_save': 'save',
        'click #toggleDownloadOptions': 'toggleDownloadOptions'
    },
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        _.bindAll(this, 'prepareAdd', 'saveError', 'downloadError', 'downloadGridPDF', 'downloadGridINX', 'downloadGridIDML', 'downloadGridCSS', 'saveAs', 'redirect');

        this.measureViews = _.map(this.$('.measure'), function(elem) {
            v = new MeasureView({
                parentView: this,
                parameter: $(elem).attr('id'),
                el: elem,
                model: this.model
            });
            return v;
        }, this);

        this.marginViews = _.map(this.$('.margin'), function(elem) {
            v = new MarginView({
                parentView: this,
                parameter: $(elem).attr('id'),
                el: elem,
                model: this.model
            });
            return v;
        }, this);

        this.increaseViews = _.map(this.$('.increase'), function(elem) {
            v = new IncreaseView({
                parentView: this,
                parameter: $(elem).attr('id'),
                model: this.model,
                el: elem
            });
            return v;
        }, this);

        this.columnsColorPicker = new ColorPickerView({
            el: this.$('#columns_color_opacity_picker'),
            param_group: 'columns',
            parentView: this,
            model: this.model
        }).render();

        this.baselineColorPicker = new ColorPickerView({
            el: this.$('#baseline_color_opacity_picker'),
            param_group: 'baseline',
            parentView: this,
            model: this.model
        }).render();

        this.spreadOption = new OptionView({
            el: this.$('#is_spread'),
            parameter: 'is_spread',
            model: this.model,
            parentView: this
        });

        this.units = {
            'width_unit': e_cols_width_unit.val(),
            'gutter_unit': e_columns_gutter_unit.val()
        };

        this.model.trigger('change');
        this.colorsPanel = this.$('#colors');
    },
    changePageFormat: function(e) {
        val = $(e.currentTarget).val();
        size = PAPER_SIZE[val];

        w = this.model.getAbsolute('width', size[0]);
        h = this.model.getAbsolute('height', size[1]);

        this.model.set({
            'width': w,
            'height': h
        });
    },
    toggleColors: function(e) {
        e.preventDefault();
        if (this.colorsPanel.css('display') == 'block') {
            this.$('#options_colors .ui-icon',this).removeClass('ui-icon-triangle-1-s');
            this.$('#options_colors .ui-icon',this).addClass('ui-icon-triangle-1-e');
            this.colorsPanel.slideUp();
        } else {
            this.$('#options_colors .ui-icon',this).removeClass('ui-icon-triangle-1-e');
            this.$('#options_colors .ui-icon',this).addClass('ui-icon-triangle-1-s');
            this.colorsPanel.slideDown();
        }
    },
    switchSystem: function(e) {
        e.preventDefault();
        var elem = e.target;

        var unit = SYSTEMS[$(elem).val()];
        this.model.switchUnits(unit);
    },
    openSaveAs: function(e) {
        e.preventDefault();
        if (this.$('#save').css('display') == 'block') {
            $(e.target).removeClass('open');
            this.$('#save').slideUp();
        } else {
            $(e.target).addClass('open');
            this.$('#save').slideDown();
        }
    },
    prepareAdd: function(model, attrs) {
        model.fetch({success: this.redirect});
        this.parentView.collection.add(model);
    },

    showError: function(button, model, xhr) {
        if (xhr.responseText) {
            var data = JSON.parse(xhr.responseText);
            var content;
            var popoverOptions = {'content': content, placement: 'top', delay: 450};

            if (xhr.status == 401) {
                var tmpl = _.template('<p><%= error %></p><a href="/plans/pricing/" class="btn btn-primary btn-block"><span class="glyphicon glyphicon-credit-card"></span> Upgrade Plan</a>');
                popoverOptions.content = tmpl(data);
                popoverOptions.html = true;
                button.one('mouseout', function(e) {
                    $(this).prop('disabled', true);
                });
            } else {
                popoverOptions.content = data['error'];
            }
            button.popover('destroy');
            button.popover(popoverOptions);
            button.popover('show');
        }
    },
    saveError: function(model, xhr) {
        this.showError(this.$('#id_save'), model, xhr);
    },
    downloadError: function(model, xhr) {
        this.showError(this.$('#toggleDownloadOptions'), model, xhr);
    },
    save: function(e) {
        e.preventDefault();
        created = null;
        if (this.model.isNew()) {
            created = new Date().toISOString();
        }
        this.model.set({
            'created': created,
            'grid': null,
            'hash': null,
            'name': this.$('#id_name').val(),
            'description': this.$('#id_description').val(),
            'summary': this.model.buildSummary()
        });
        this.model.save({}, {success: this.prepareAdd, error: this.saveError});
    },
    saveAs: function(e) {
        e.preventDefault();
        newModel = this.model.clone();
        newModel.set({
            'resource_uri': null,
            'id': null,
            'created': new Date().toISOString(),
            'edit_url': null,
            'grid': null,
            'hash': null,
            'name': this.$('#id_name').val(),
            'description': this.$('#id_description').val(),
            'summary': newModel.buildSummary()
        }, {silent:true});
        this.parentView.changeModel(newModel);
        this.model.save({}, {success: this.prepareAdd, error: this.saveError});
    },
    redirect: function(model, reponse) {
        if (!this.parentView.collection.get(model.cid)) {
            this.parentView.collection.add(model);
        }
        window.router.absoluteNavigate(model.get('edit_url'));
    },
    toggleDownloadOptions: function(e) {
        e.preventDefault();
        this.$('#downloadOptions').toggle();
    },
    downloadPDF: function(e) {
        e.preventDefault();
        this.model.save({'summary': this.model.buildSummary()}, {success: this.downloadGridPDF, error: this.downloadError});
    },
    downloadGridPDF: function(model, response) {
        this.model.fetch({success: function(model, response) {
            this.$('#toggleDownloadOptions').click();
            window.location = model.get('grid');
        }});
    },
    downloadINX: function(e) {
        if (window.user_id) {
            e.preventDefault();
            this.model.save({'summary': this.model.buildSummary()}, {success: this.downloadGridINX, error: this.downloadError});
        }
    },
    downloadGridINX: function(model, response) {
        this.model.fetch({success: function(model, response) {
            this.$('#toggleDownloadOptions').click();
            window.location = model.get('edit_url')+'inx/';
        }});
    },
    downloadIDML: function(e) {
        e.preventDefault();
        this.model.save({'summary': this.model.buildSummary()}, {success: this.downloadGridIDML, error: this.downloadError});
    },
    downloadGridIDML: function(model, response) {
        this.model.fetch({success: function(model, response) {
            this.$('#toggleDownloadOptions').click();
            window.location = model.get('edit_url')+'idml/';
        }});
    },
    downloadCSS: function(e) {
        e.preventDefault();
        this.model.save({'summary': this.model.buildSummary()}, {success: this.downloadGridCSS, error: this.downloadError});
    },
    downloadGridCSS: function(model, response) {
        this.model.fetch({success: function(model, response) {
            this.$('#toggleDownloadOptions').click();
            window.location = model.get('edit_url')+'css/';
        }});
    }
});
