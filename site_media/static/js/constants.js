// costants
var SYSTEMS = {
    'metric': 'mm',
    'imperial': 'in',
    'pixels': 'px'
};
var UNITS = {
    'px': 1.0,
    'pt': 1.0,
    'in': 72.0,
    'mm': 0.0393700787*72
};
var PAPER_SIZE = { // in mm
    'A5': [148*UNITS['mm'],210*UNITS['mm']],
    'A4': [210*UNITS['mm'],297*UNITS['mm']],
    'A3': [297*UNITS['mm'],420*UNITS['mm']],
    'LETTER': [216*UNITS['mm'],279*UNITS['mm']], // according to wikipedia
    'TABLOID': [432*UNITS['mm'],279*UNITS['mm']] // according to wikipedia
};
var MAX_CANVAS_WIDTH = 850;
