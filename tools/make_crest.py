"""Cut the family coat of arms out of its background and export the site's marks.

The whole achievement is used everywhere: header, footer, and the favicons. The
favicons are just the same artwork centred on a square canvas.

An earlier version extracted the shield alone for the icons, on the theory that it
reads better at 16 px. It did, marginally — but finding the shield meant segmenting
the blue field, masking to its silhouette so the helm above it would not bleed in,
reconstructing the top edge the helm covers, and redrawing the border. Four rounds
of image processing, each one repairing the last, in exchange for slightly crisper
detail at a size where no favicon shows detail anyway. Not worth it. Deleted.

The one bit of processing that is genuinely needed is the background: the source
sits on a dark radial glow, which would read as a dark box behind the crest on the
light theme. Keying it out by colour does not work — the artwork's own outlines are
as dark as the glow. So the mask is built from what the artwork *is* instead
(bright), then closed to bridge the outlines, then its small enclosed holes are
filled. Large enclosed pockets stay transparent: those are the gaps between the
mantling scrolls, and they are background.

Dev-only. Run with ~/miniconda3/envs/py4dstem/bin/python.

The source PNG is gitignored — it is 2.5 MB and never served, while everything it
produces is committed. Put it back at assets/crest-source.png before running. Do
not "optimise" it to a palette first: the mask is built from brightness thresholds,
and quantising shifts the edge pixels enough to change the crop.
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'crest-source.png')
OUT = os.path.join(ROOT, 'assets')


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


# ---- cut the artwork out of the glow ----

src = Image.open(SRC).convert('RGB')
rgb = np.asarray(src).astype(np.float32) / 255.0
bright = rgb.max(axis=2) > 0.55

# Closing with an element wider than an outline bridges across outlines -- which are
# flanked by fills on both sides -- without bridging across the background.
mask = ndimage.binary_closing(bright, structure=disk(14))

# Keep the achievement itself, dropping speckle the glow left behind.
labels, n = ndimage.label(mask)
if n > 1:
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    mask = labels == (int(np.argmax(sizes)) + 1)

# Fill the interiors the outlines enclose, but only the small ones.
holes = ndimage.binary_fill_holes(mask) & ~mask
hl, hn = ndimage.label(holes)
if hn:
    limit = 0.004 * mask.size
    for i, area in enumerate(ndimage.sum(holes, hl, range(1, hn + 1)), start=1):
        if area < limit:
            mask |= hl == i

# Feather by a pixel so the edge is not a staircase at small sizes.
alpha = ndimage.gaussian_filter(mask.astype(np.float32), 0.8)
alpha = np.clip((alpha - 0.35) / 0.4, 0, 1)

crest = Image.fromarray(
    np.dstack([np.asarray(src), (alpha * 255).astype(np.uint8)]), mode='RGBA')
crest = crest.crop(crest.getbbox())
print(f'source {src.size} -> artwork {crest.size}')


def write(img, name, colors=64):
    """Heraldic artwork is a handful of flat colours, so a palette is free."""
    img.quantize(colors=colors, method=Image.FASTOCTREE).save(
        f'{OUT}/{name}', optimize=True)
    print(f'  {name}: {os.path.getsize(f"{OUT}/{name}") / 1e3:.0f} kB')


# ---- the header and footer mark ----

write(crest.resize((256, round(crest.height * 256 / crest.width)), Image.LANCZOS),
      'crest.png')

# ---- favicons: the same artwork, centred on a square ----

side = round(max(crest.size) * 1.04)
square = Image.new('RGBA', (side, side), (0, 0, 0, 0))
square.paste(crest, ((side - crest.width) // 2, (side - crest.height) // 2), crest)

# Only the sizes the pages link. A 32 covers the tab at 1x and 2x and browsers
# downscale it cleanly, so there is no separate 16.
for size in (32, 512):
    write(square.resize((size, size), Image.LANCZOS), f'favicon-{size}.png')
write(square.resize((180, 180), Image.LANCZOS), 'apple-touch-icon.png')
