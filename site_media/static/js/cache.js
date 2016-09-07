// Store those elements in vars, so we don't have to look for them over and over 
var CANVAS_DIV = $('#canvas');

var e_form = $('#gridder');
var e_width = $('#id_width');
var e_width_unit = $('#id_width_unit');
var e_height = $('#id_height');
var e_height_unit = $('#id_height_unit');
var e_columns = $('#id_columns');
var e_columns_gutter = $('#id_columns_gutter');
var e_columns_gutter_unit = $('#id_columns_gutter_unit');
var e_columns_width = $('#id_cols_width');
var e_columns_unit = $('#id_cols_width_unit');

var e_baseline = $('#id_baseline');
var e_baseline_unit = $('#id_baseline_unit');

var e_margin_left = $('#id_margin_left');
var e_margin_left_unit = $('#id_margin_left_unit');
var e_margin_right = $('#id_margin_right');
var e_margin_right_unit = $('#id_margin_right_unit');
var e_margin_top = $('#id_margin_top');
var e_margin_top_unit = $('#id_margin_top_unit');
var e_margin_bottom = $('#id_margin_bottom');
var e_margin_bottom_unit = $('#id_margin_bottom_unit');

var e_cols_width_unit = $('#id_cols_width_unit');

var e_cols_color = $('#id_columns_color');
var e_baseline_color = $('#id_baseline_color');

/* shortcuts */
var e_values_units = [
    [e_width,e_width_unit],
    [e_height,e_height_unit],
    [e_columns_width,e_columns_unit],
    [e_columns_gutter,e_columns_gutter_unit],
    [e_baseline,e_baseline_unit],
    [e_margin_left,e_margin_left_unit],
    [e_margin_right,e_margin_right_unit],
    [e_margin_top,e_margin_top_unit],
    [e_margin_bottom,e_margin_bottom_unit]
];
