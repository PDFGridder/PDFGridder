jQuery.fn.increase_widget = function(options) {
    tpl = '<div class="increase_widget"><span class="state"><a class="increase ui-icon ui-icon-triangle-1-n" href="#">+</a></span><span class="state"><a class="decrease ui-icon ui-icon-triangle-1-s" href="#">-</a></span></div>';
    
    var settings = jQuery.extend({
         min: 0,
         max: false
    }, options);
    
    this.each(function() {
        var input = this;
        var w = jQuery(tpl).insertAfter(this);
        
        jQuery('.increase', w).click(function(e) {
            e.preventDefault();
            value = jQuery(input).val();
            if (settings.max === false || value < settings.max) {
                value++;
                jQuery(input).val(value);
                jQuery(input).trigger('change');
            };
        });
        jQuery('.decrease', w).click(function(e) {
            e.preventDefault();
            value = jQuery(input).val();
            if (settings.min === false || value > settings.min) {
                value--;
                jQuery(input).val(value);
                jQuery(input).trigger('change');
            };
        });
        jQuery('a', w).hover(function() {
            jQuery(this).parent('.state').addClass('ui-state-highlight');
        }, function() {
            jQuery(this).parent('.state').removeClass('ui-state-highlight');
        });
    });
};
