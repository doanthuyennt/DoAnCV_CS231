from PIL import Image
import numpy as np
from PIL import Image, ImageChops


def fill(size, color):
    assert len(size) == 2
    assert len(color) in [3, 4]

    if len(color) == 4:
        color[3] = int(round(color[3] * 255))  # alpha

    uniqued = list(set(color))
    cmap = {c: Image.new('L', size, c) for c in uniqued}

    if len(color) == 3:
        r, g, b = color
        return Image.merge('RGB', (cmap[r], cmap[g], cmap[b]))
    else:
        r, g, b, a = color
        return Image.merge('RGBA', (cmap[r], cmap[g], cmap[b], cmap[a]))