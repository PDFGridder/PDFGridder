var GridView = GenericView.extend({
    initialize: function(options) {
        GenericView.prototype.initialize.apply(this, arguments);

        this.page = options.page;
        this.model.bind('change', this.render, this);
        this.model.bind('change:is_spread', this.setupCanvas, this);
        this.bind('change:model', this.setupCanvas, this);
        this.setupCanvas();
    },
    getRatio: function() {
        canvas_width = MAX_CANVAS_WIDTH;
        if (this.model.get('is_spread')) {
            canvas_width = (canvas_width/2)-4;
        }
        ratio = canvas_width/this.model.normalize('width');
        return ratio;
    },
    convert_to_unit: function(value, unit) {
        return value/UNITS[unit];
    },
    setupCanvas: function() {
        page_width = this.model.normalize('width');
        page_height = this.model.normalize('height');

        ratio = this.getRatio();
        canvas_width = page_width*ratio;
        canvas_height = page_height*ratio;

        $(this.el).css({width: canvas_width});
        if (this.model.get('is_spread')) {
            $(this.el).addClass('spread');
        } else {
            $(this.el).removeClass('spread');
        }
        $(this.el).html('');
        this.canvas = Raphael($(this.el).attr('id'), canvas_width, canvas_height);
        this.render();
    },
    render: function() {

        page_width = this.model.normalize('width');
        page_height = this.model.normalize('height');

        margin_top = this.model.normalize('margin_top');
        margin_bottom = this.model.normalize('margin_bottom');
        margin_left = this.model.normalize('margin_left');
        margin_right = this.model.normalize('margin_right');

        if (this.page == 'left') {
            temp = margin_left;
            margin_left = margin_right;
            margin_right = temp;
        }

        baseline = this.model.normalize('baseline');
        baseline_color = this.model.get('baseline_color');
        baseline_opacity = this.model.get('baseline_opacity');

        columns_count = this.model.get('columns');
        columns_width = this.model.normalize('columns_width');

        gutter = this.model.normalize('columns_gutter');

        ratio = this.getRatio();
        canvas = this.canvas;

        canvas.clear();

        page_scaled = {
            'width': page_width*ratio,
            'height': page_height*ratio,
            'margin_top': margin_top*ratio,
            'margin_bottom': margin_bottom*ratio,
            'margin_left': margin_left*ratio,
            'margin_right': margin_right*ratio
        };
        columns_scaled = {
            'count': columns_count,
            'width': columns_width*ratio,
            'width_unit': this.parentView.controlsView.units['width_unit'],
            'gutter': gutter*ratio,
            'gutter_unit': this.parentView.controlsView.units['gutter_unit'],
            'color': this.model.get('columns_color'),
            'opacity': this.model.get('columns_opacity')
        };
        baseline_scaled = {
            'size': baseline*ratio,
            'color': baseline_color,
            'opacity': baseline_opacity
        };

        this.draw_columns(this.canvas, page_scaled, columns_scaled);
        this.draw_baseline(this.canvas, page_scaled, baseline_scaled);
        this.draw_quotes(this.canvas, page_scaled, columns_scaled, baseline_scaled);
    },
    draw_columns: function(canvas, page, columns) {
        col_height = page['height']-page['margin_top']-page['margin_bottom'];

        col_rects = canvas.set();
        col_gutters = canvas.set();

        for (i=0;i<columns['count'];i++) {
            x = page['margin_left'] + (i*(columns['width']+columns['gutter']));
            col = canvas.rect(x, page['margin_top'], columns['width'], col_height);
            $(col.node).css('opacity', columns['opacity']);
            col_rects.push(col);

            if (i<columns['count']-1) {
                gut = canvas.rect(x+columns['width'], page['margin_top'], columns['width'], col_height);
                col_gutters.push(gut);
            }
        }

        col_gutters.attr('fill','white');
        col_gutters.attr('stroke','none');
        col_rects.attr('fill', columns['color']);
        col_rects.attr('stroke','none');
    },
    draw_quotes: function(canvas, page, columns, baseline) {
        columns['width_unit'] = this.model.get('width_unit');
        col_padding = 5;

        quotes = canvas.set();
        lines = canvas.set();

        if (baseline['size'] > 6) {
            step = baseline['size']*2;
        } else {
            step = 24;
        }

        x0 = page['margin_left'];
        y0 = page['margin_top'];
        for (i=1;i<=columns['count'];i++) {
            w = (columns['width']*i)+(columns['gutter']*(i-1));
            x1 = x0+w;
            y0 += step;
            line = canvas.path("M"+x0+" "+y0+"L"+x1+" "+y0);
            open = canvas.path("M"+x0+" "+(y0-2)+"L"+x0+" "+(y0+2));
            close = canvas.path("M"+x1+" "+(y0-2)+"L"+x1+" "+(y0+2));
            lines.push(line);
            lines.push(open);
            lines.push(close);

            y0 += -10;

            quote = canvas.text(x0+(w/2), y0, i+': '+ this.convert_to_unit((w/ratio),columns['width_unit']).toFixed(2)+columns['width_unit']);
            quotes.push(quote);
            y0 += 10;
        }
        quotes.attr('text-anchor', 'middle');
        quotes.attr('fill', 'purple');
        quotes.attr('background', 'white');
        lines.attr('stroke','purple');

    },

    draw_rows: function(canvas, page, rows,ratio) {
        row_padding = 5;

        row_width = page['width']-page['margin_left']-page['margin_right'];

        row_rects = canvas.set();
        row_quotes = canvas.set();
        row_gutters = canvas.set();
        row_gut_quotes = canvas.set();

        for (i=0;i<rows['count'];i++) {
            x = page['margin_left'] + (i*(rows['width']+rows['gutter']));
            row = canvas.rect(x, page['margin_left'], rows['height'], row_width);
            $(row.node).hover(function() {
                row_quotes.show();
            }, function() {
                row_quotes.hide();
            });
            row_rects.push(row);

            if (i<rows['count']-1) {
                gut = canvas.rect(x+rows['height'], page['margin_left'], rows['height'], row_width);
                $(gut.node).hover(function() {
                    row_gut_quotes.show();
                }, function() {
                    row_gut_quotes.hide();
                });
                row_gutters.push(gut);
            }
        }
        for (i=0;i<rows['count'];i++) {
            x = page['margin_top'] + (i*(rows['height']+rows['gutter']));
            row_quote = canvas.text(x+row_padding, page['margin_left']+5+row_padding, this.convert_to_unit((rows['height']/ratio),rows['height_unit']).toFixed(2)+rows['height_unit']);
            row_quotes.push(row_quote);

            if (i<row['count']-1) {
                gut_quote = canvas.text(x+row['height'], page['margin_left']+5+row_padding, this.convert_to_unit((rows['gutter']/ratio),rows['gutter_unit']).toFixed(2)+rows['gutter_unit']);
                row_gut_quotes.push(gut_quote);
            }
        }

        row_gutters.attr('fill','white');
        row_gutters.attr('stroke','none');
        row_rects.attr('fill',rows['color']);
        row_rects.attr('stroke','none');
        row_quotes.hide();
        row_quotes.attr('text-anchor', 'start');
        row_quotes.attr('fill', 'purple');
        row_gut_quotes.hide();
        row_gut_quotes.attr('text-anchor', 'start');
        row_gut_quotes.attr('fill', 'green');
    },
    draw_baseline: function(canvas, page, baseline) {
        if (baseline['size'] > 0) {
            baselines = canvas.set();

            baseline_x2 = page['width']-page['margin_right'];
            baseline_y2 = page['height']-page['margin_bottom'];

            y = page['margin_top']+baseline['size'];
            while (y < baseline_y2) {
                line = canvas.path("M"+page['margin_left']+" "+y+"L"+baseline_x2+" "+y);
                y += baseline['size'];
                $(line.node).css('opacity', baseline['opacity']);
                baselines.push(line);
            }
            baselines.attr('stroke',baseline['color']);
        }
    }
});
