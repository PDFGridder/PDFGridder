GridRowView = GenericView.extend({
    tagName: 'li',
    className: "hentry",
    events: {
        'click .star': "toggleStar",
        'click .delete': 'deleteGrid'
    },
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        _.bindAll(this, 'updateStar', 'deleteRow');
        this.model.bind('change', this.updateChanged, this);
        this.model.bind('save', this.resetChanged, this);
        this.model.bind('change:star', this.updateStar);
        this.model.bind('change:name', this.updateTitle, this);
        this.model.bind('change:summary', this.updateSummary, this);
        this.render();
    },
    render: function() {
        grid = this.model;
        created = Date.parse(grid.get('created').split('.')[0]);
        created_human = created.toString('MMM, d')+created.getOrdinal()+created.toString(' yyyy');

        newItem = '<div class="tools"><a rel="'+grid.get('id')+
        '" class="star" href="#" title="favorite"></a><a class="download" href="'+grid.get('grid')+'" title="download">&darr;</a><a class="delete" href="#" rel="'+grid.get('id')+'" title="delete" title="delete">&times;</a></div><div class="details"><h5 class="entry-title"><a href="'+grid.get('edit_url')+'" title="edit this grid">'+grid.get('name')+'</a></h5><p class="entry-summary">'+grid.get('summary')+'</p><p class="published">created on '+created_human+'.</p></div>';
        $(this.el).html(newItem);
        this.updateStar();

        return this;
    },
    toggleStar: function(e) {
        e.preventDefault();
        this.model.set({star: !this.model.get('star')});
        this.model.save();
    },
    deleteGrid: function(e) {
        e.preventDefault();
        this.model.destroy({success: this.deleteRow});
    },
    deleteRow: function(model, response) {
        $(this.el).addClass('deleting');
        var parentView = this.parentView;
        $(this.el).slideUp(function() {
            parentView.removeSubView(this);
        });
    },
    updateChanged: function(e) {
        changedAttributes = this.model.changedAttributes();
        delete changedAttributes['hash'];
        delete changedAttributes['grid'];
        if (!_.isEmpty(changedAttributes)) {
            $(this.el).addClass('modified');
        }
    },
    resetChanged: function(e) {
        $(this.el).removeClass('modified');
    },
    updateStar: function() {
        star = this.$('.star[rel='+this.model.get('id')+']');
        if (this.model.get('star') === true) {
            star.html('★');
            star.parents('.hentry').addClass('starred');
        } else {
            star.html('☆');
            star.parents('.hentry').removeClass('starred');
        }
    },
    updateTitle: function() {
        this.$('.entry-title a').text(this.model.get('name'));
    },
    updateSummary: function() {
        this.$('.entry-summary').text(this.model.get('summary'));
    },
    show: function() {
        $(this.el).slideDown();
    },
    hide: function() {
        $(this.el).slideUp();
    },
    setActiveGrid: function() {
        $(this.el).addClass('active');
    },
    unsetActiveGrid: function() {
        $(this.el).removeClass('active');
    }
});