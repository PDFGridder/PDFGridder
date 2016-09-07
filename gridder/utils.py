INCH = 72.0
MM = 0.0393700787 * INCH
PX = 1.0
PT = PX

UNITS = {
    'px': PX,
    'pt': PT,
    'in': INCH,
    'mm': MM,
}


def parse_unit(value, unit):
    """Convert in px
Valid units are: mm, in, pt, px.
"""

    return float(value) * UNITS[unit]


def hex_to_rgba(value, alpha=1.0):
    """Convert from HEX to RGB tuple
see: http://stackoverflow.com/questions/214359/converting-hex-to-rgb-and-vice-versa/214657#214657
    """
    value = value.lstrip('#')
    if len(value) == 3:
        value = ''.join([c + c for c in value])
    lv = len(value)
    rgba = [int(value[i:i + lv / 3], 16) for i in range(0, lv, lv / 3)]
    rgba.append(alpha)
    return tuple(rgba)
