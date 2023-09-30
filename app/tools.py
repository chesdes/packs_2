# Imports
from PIL import Image

# hex to rgb / rgb to hex
def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hex):
    return tuple(int(hex.split("#")[1][i:i+2], 16) for i in (0, 2, 4))

