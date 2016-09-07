GridListView = GenericView.extend({
    events: {
        'click .category a[rel=hentry]': 'filterAll',
        'click .category a[rel=starred]': "filterStarred"
    },
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.rowViews = [];

        _.bindAll(this, 'addNewGrid', 'refreshGrids', 'filterAll', 'filterStarred');
        this.collection.bind('add', this.addNewGrid, this);
        this.collection.bind('reset', this.refreshGrids, this);
        if (this.parentView.model !== undefined) {
            this.parentView.bind('change:model', this.setActiveRowView, this);
        }
        this.refreshGrids(this.collection);
    },
    refreshGrids: function(collection, resp) {
        this.$('.grids').html('');
        collection.each(function(grid) {
            gw = this.addGridView(grid);
            inserted = $(gw.el).appendTo(this.$('.grids'));
        }, this);
        this.setActiveRowView();
    },
    addGridView: function(grid) {
        gridRowView = new GridRowView({
            parentView: this,
            model: grid,
            id: "row-grid-"+grid.get('id')
        });
        this.rowViews.push(gridRowView);
        return gridRowView;
    },
    addNewGrid: function(grid) {
        gw = this.addGridView(grid);
        $(gridRowView.el).addClass('just_added');
        inserted = $(gw.el).prependTo(this.$('.grids'));

        $(inserted).slideDown('slow',function() {
            $(this).animate({'backgroundColor':'#fafafa'},'slow', function() {
                $(this).removeClass('just_added');
            });
        });
        this.setActiveRowView();
    },
    removeSubView: function(view) {
        $(view.el).remove();
        this.rowViews = _.without(this.rowViews, view);
    },
    selectFilter: function(filterEl) {
        $(filterEl).addClass('selected').siblings().removeClass('selected');
    },
    filterAll: function(e) {
        e.preventDefault();
        this.selectFilter($(e.currentTarget).parent());
        _.each(this.rowViews, function(view) {
            view.show();
        });
    },
    setActiveRowView: function() {
        if (this.parentView.model) {
            grid = this.parentView.model;
            _.map(this.rowViews, function(rowView) {
                if (rowView.model == this) {
                    rowView.setActiveGrid();
                } else {
                    rowView.unsetActiveGrid();
                }
            }, grid);
    }
    },
    filterStarred: function(e) {
        e.preventDefault();
        this.selectFilter($(e.currentTarget).parent());
        _.each(this.rowViews, function(view) {
            if (!$(view.el).hasClass('starred')) {
                view.hide();
            }
        });
    }
});