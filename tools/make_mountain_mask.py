"""Make the 'sky mask' for the mountain range: opaque everywhere ABOVE the mountain ridge, clear below.
Used with Clip Children so a giant Daven only shows above the mountains (he rises from behind them).

Usage: python tools/make_mountain_mask.py sprites
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

BG = Path(sys.argv[1]) / "environment" / "background"
EXTRA = 1600  # how much sky above the picture the mask covers

a = np.asarray(Image.open(BG / "mountain_range.png").convert("RGBA"))[..., 3] > 60
h, w = a.shape
ridge = np.full(w, h, float)
for x in range(w):
    ys = np.nonzero(a[:, x])[0]
    if len(ys):
        ridge[x] = ys.min() + 6  # a little inside the line, so the line itself covers the edge
ridge = ndimage.grey_closing(ridge, size=9)  # ignore tiny gaps in the marker line
mask = np.zeros((h + EXTRA, w), np.uint8)
yy = np.arange(h + EXTRA)[:, None]
mask[yy < (ridge[None, :] + EXTRA)] = 255
img = Image.fromarray(np.dstack([np.full_like(mask, 255)] * 3 + [mask]), "RGBA")
img.save(BG / "mountain_range_sky_mask.png", optimize=True)
print("mask", img.size, "offset y", -EXTRA / 2)
