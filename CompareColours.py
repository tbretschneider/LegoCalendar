# Compare colours

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000


def colorcompare(color1, color2):
    delta_e = delta_e_cie2000(color1_lab, color2_lab)
    print("difference between colours is", delta_e)
