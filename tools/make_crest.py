"""Cut the family coat of arms out of its background, and derive the site's marks.

Two outputs. The full achievement goes in the header and the footer. The shield
alone becomes the favicon set, because at 16 px the full achievement — mantling,
helm, crown, three flowers — collapses into a smudge, while a gold lion on a blue
field still reads. Both were rendered and compared before choosing.


The source (`media/paul/Wappen_GPT.png`) sits on a dark radial glow rather than on
transparency, which would look like a mistake on the light theme. Keying it out by
colour does not work: the artwork's own outlines are as dark as the background.

So the mask is built from what the artwork *is* instead — saturated colour or high
value — which catches every filled region but misses the black outlines between
them. Closing the mask and filling holes then recovers the outlines, because an
outline is always enclosed by the regions it separates.

Dev-only. Run with ~/miniconda3/envs/py4dstem/bin/python.

The source PNG is gitignored — it is 2.5 MB and never served, while everything it
produces is committed. Put it back at media/paul/Wappen_GPT.png before running.
Do not "optimise" it to a palette first: the mask is built from brightness
thresholds, and quantising shifts the edge pixels enough to change the crop.
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'media', 'paul', 'Wappen_GPT.png')
OUT = os.path.join(ROOT, 'media', 'paul')

src = Image.open(SRC).convert('RGB')
rgb = np.asarray(src).astype(np.float32) / 255.0

mx = rgb.max(axis=2)

# The background glow is dark; every filled area of the artwork is bright. The
# black outlines are dark too, so they are missed here and recovered below.
# Colour is useless as a discriminator: the glow is strongly tinted.
core = mx > 0.55

def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r

# Closing with an element wider than an outline bridges across outlines — which
# are flanked by fills on both sides — without bridging across the background.
mask = ndimage.binary_closing(core, structure=disk(14))

# Keep only the achievement itself, dropping speckle the glow left behind.
labels, n = ndimage.label(mask)
if n > 1:
    sizes = ndimage.sum(mask, labels, range(1, n + 1))
    mask = labels == (int(np.argmax(sizes)) + 1)

# Fill the interiors the outlines enclose, but only the small ones: the large
# enclosed pockets between the mantling scrolls are background and must stay
# transparent, or they come back as dark blotches.
holes = ndimage.binary_fill_holes(mask) & ~mask
hl, hn = ndimage.label(holes)
if hn:
    limit = 0.004 * mask.size
    for i, area in enumerate(ndimage.sum(holes, hl, range(1, hn + 1)), start=1):
        if area < limit:
            mask |= hl == i

# Feather by one pixel so the edge is not a staircase at small sizes.
alpha = ndimage.gaussian_filter(mask.astype(np.float32), 0.8)
alpha = np.clip((alpha - 0.35) / 0.4, 0, 1)

out = np.dstack([np.asarray(src), (alpha * 255).astype(np.uint8)])
crest = Image.fromarray(out, mode='RGBA')

# Trim to the artwork, then keep a little breathing room.
bbox = crest.getbbox()
crest = crest.crop(bbox)
print(f'source {src.size} -> cropped {crest.size}')

# Heraldic artwork is a handful of flat colours, so a palette costs nothing
# visible and roughly quarters the file. 64 entries is well clear of what the
# resampled edges need.
width = 256
height = round(crest.height * width / crest.width)
small = crest.resize((width, height), Image.LANCZOS)
small.quantize(colors=64, method=Image.FASTOCTREE).save(f'{OUT}/crest-{width}.png', optimize=True)
print(f'  crest-{width}.png: {os.path.getsize(f"{OUT}/crest-{width}.png") / 1e3:.0f} kB')


# ---- the shield alone, squared, for favicons ----

ICONS = os.path.join(ROOT, 'media', 'index')
os.makedirs(ICONS, exist_ok=True)

W, H = crest.size
shield = crest.crop((round(W * 0.24), round(H * 0.55), round(W * 0.76), H))
side = max(shield.size)
square = Image.new('RGBA', (side, side), (0, 0, 0, 0))
square.paste(shield, ((side - shield.width) // 2, (side - shield.height) // 2), shield)

def icon(size, path):
    """Palette-quantised so a 512 px icon is ~20 kB rather than ~250."""
    img = square.resize((size, size), Image.LANCZOS)
    img.quantize(colors=64, method=Image.FASTOCTREE).save(path, optimize=True)
    print(f'  {os.path.basename(path)}: {os.path.getsize(path) / 1e3:.0f} kB')


# Only the sizes the pages actually link. Anything else is dead weight.
for size in (16, 32, 512):
    icon(size, f'{ICONS}/favicon-{size}.png')
icon(180, f'{ICONS}/apple-touch-icon.png')
