#!/usr/bin/env python
import cairo
from .utils import hex_to_rgba, parse_unit


def parse_size(size):
    """take a size as str (es: 14px), return its value in px/pt as int
    """
    if hasattr(size, 'isdigit'):
        if size.isdigit():
            return int(size)
        return parse_unit(size[:-2], size[-2:])
    return size


def parse_size_shorthand(shorthand):
    tokens = shorthand.split()

    l = len(tokens)
    if l == 1:
        return {'top': parse_size(tokens[0]), 'right': parse_size(tokens[0]), 'bottom': parse_size(tokens[0]), 'left': parse_size(tokens[0])}
    if l == 2:
        return {'top': parse_size(tokens[0]), 'right': parse_size(tokens[1]), 'bottom': parse_size(tokens[0]), 'left': parse_size(tokens[1])}

    return {'top': parse_size(tokens[0]), 'right': parse_size(tokens[1]), 'bottom': parse_size(tokens[2]), 'left': parse_size(tokens[3])}


def hex_to_cairo(value, alpha=1.0):
    value = hex_to_rgba(value, alpha)
    rgb = [v / 255.0 for v in value[:3]]
    rgb.append(value[-1])
    return tuple(rgb)


class PDFGridder(object):
    def __init__(self, grid):
        self.grid = grid
        self.paper = {
            'width': str(grid.width) + grid.width_unit,
            'height': str(grid.height) + grid.height_unit,
        }
        self.columns = {
            'count': grid.columns,
            'color': grid.columns_color,
            'opacity': grid.columns_opacity,
            'gutter': grid.columns_gutter_str()
        }
        self.baseline = {
            'distance': str(grid.baseline) + grid.baseline_unit,
            'color': grid.baseline_color,
            'opacity': grid.baseline_opacity,
        }
        self.margin = grid.margins()
        self.margin_size = parse_size_shorthand(self.margin)
        self.is_spread = grid.is_spread

        self.rows = {
            'count': 0,
            'gutter': 0,
            'color': '#ccc',
            'opacity': 0.5
        }

    def draw_cols(self, bottom, w):
        cols = self.columns['count']
        if cols > 0:
            cols_gutter_size = parse_size(self.columns['gutter'])
            cols_width = (w / cols) - cols_gutter_size + (cols_gutter_size / cols) - (self.margin_size['left'] / cols) - (self.margin_size['right'] / cols)
            cols_offset = cols_width + cols_gutter_size
            cols_color = hex_to_cairo(self.columns['color'], self.columns['opacity'])

            for i in xrange(cols):
                self.ctx.rectangle(i * cols_offset + self.margin_size['left'], 0, cols_width, bottom)
            self.ctx.set_source_rgba(*cols_color)  # Solid color
            self.ctx.fill()

    def draw_rows(self, rows, h):
        #rows
        rows_count = rows['count']
        if rows_count:
            rows_gutter_size = parse_size(rows['gutter'])
            rows_color = hex_to_cairo(rows['color'], rows['opacity'])
            rows_height = (h / rows_count) - rows_gutter_size + (rows_gutter_size / rows_count) - (self.margin_size['top'] / rows_count) - (self.margin_size['bottom'] / rows_count)
            rows_offset = rows_height + rows_gutter_size
            for i in xrange(rows_count):
                self.ctx.rectangle(
                    self.margin_size['left'],
                    i * rows_offset,
                    rows_height,
                    self.margin_size['right']
                )
            self.ctx.set_source_rgba(*rows_color)  # Solid color
            self.ctx.fill()

    def draw_baselines(self, distance, w, bottom, lines_color):
        base_offset = distance
        while base_offset < bottom:
            self.ctx.move_to(self.margin_size['left'], base_offset)
            self.ctx.line_to(w - self.margin_size['right'], base_offset)
            base_offset = base_offset + distance
        self.ctx.set_source_rgba(*lines_color)  # Solid color
        self.ctx.set_line_width(0.25)
        self.ctx.stroke()

    def build_page(self, surface, h_flip=False):
        w, h = parse_size(self.paper['width']), parse_size(self.paper['height'])

        if h_flip:
            self.margin_size['left'], self.margin_size['right'] = self.margin_size['right'], self.margin_size['left']

        self.ctx = cairo.Context(surface)

        #ctx.scale (w/1.0, h/1.0) # Normalizing the canvas
        self.ctx.translate(0, self.margin_size['top'])
        bottom = h - self.margin_size['bottom'] - self.margin_size['top']

        self.draw_cols(bottom, w)
        self.draw_rows(self.rows, h)

        #baseline
        try:
            lines_color = hex_to_cairo(self.baseline['color'], self.baseline['opacity'])
        except ValueError:
            lines_color = None

        distance = parse_size(self.baseline['distance'])
        if distance > 0 and lines_color is not None:
            self.draw_baselines(distance, w, bottom, lines_color)

        return self.ctx

    def build(self, output='output.pdf'):
        w, h = parse_size(self.paper['width']), parse_size(self.paper['height'])

        surface = cairo.PDFSurface(output, w, h)
        self.build_page(surface=surface)
        surface.show_page()
        if self.is_spread:
            self.build_page(surface=surface, h_flip=True)
            surface.show_page()

        surface.finish()

        return output
