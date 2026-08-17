"""Cut the family coat of arms out of its background, and derive the site's marks.

Two outputs. The full achievement goes in the header and the footer. The shield
alone becomes the favicon set, because at 16 px the full achievement — mantling,
helm, crown, three flowers — collapses into a smudge, while a gold lion on a blue
field still reads. Both were rendered and compared before choosing.


The source (`assets/crest-source.png`) sits on a dark radial glow rather than on
transparency, which would look like a mistake on the light theme. Keying it out by
colour does not work: the artwork's own outlines are as dark as the background.

So the mask is built from what the artwork *is* instead — saturated colour or high
value — which catches every filled region but misses the black outlines between
them. Closing the mask and filling holes then recovers the outlines, because an
outline is always enclosed by the regions it separates.

Dev-only. Run with ~/miniconda3/envs/py4dstem/bin/python.

The source PNG is gitignored — it is 2.5 MB and never served, while everything it
produces is committed. Put it back at assets/crest-source.png before running.
Do not "optimise" it to a palette first: the mask is built from brightness
thresholds, and quantising shifts the edge pixels enough to change the crop.
"""
import os

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'crest-source.png')
OUT = os.path.join(ROOT, 'assets')

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
small.quantize(colors=64, method=Image.FASTOCTREE).save(f'{OUT}/crest.png', optimize=True)
print(f'  crest.png: {os.path.getsize(f"{OUT}/crest.png") / 1e3:.0f} kB')


# ---- the shield alone, squared, for favicons ----

ICONS = os.path.join(ROOT, 'assets')
os.makedirs(ICONS, exist_ok=True)

# Find the shield rather than guessing a crop box. Fixed fractions of the image
# sliced through the helm at the top and clipped the shield's shoulders at the
# sides. The shield is the one large solid-blue area, so: take every strongly
# blue pixel, keep the largest connected blob, and use its bounding box.
arr = np.asarray(crest).astype(np.int16)
r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]
blue = (a > 128) & (b > 110) & (b - r > 45) & (b - g > 15)

labels, n = ndimage.label(blue)
assert n, 'no blue region found — has the artwork changed?'
sizes = ndimage.sum(blue, labels, range(1, n + 1))
field = labels == (int(np.argmax(sizes)) + 1)

# The shield's own black outline cannot be harvested from the artwork: the helm and
# the mantling touch the shield along its top edge, so any dilation wide enough to
# pick up the outline also picks up pieces of them, which is what left dark stubs
# in the top corners of the icon.
#
# So keep only what is unambiguously the shield — the blue field with its holes
# filled, which restores the lion and the star — and draw the border instead of
# copying it. A ring just outside the silhouette, painted the same near-black the
# artwork uses.
inner = ndimage.binary_fill_holes(field)

# The helm rests on the shield and hides part of its top edge, so the blue field
# genuinely stops short there and the silhouette comes out with a notch in the
# middle of the top. Close it by filling each column up to the shield's highest
# row — but only where the gap is small, so a corner that is really rounded stays
# rounded instead of being squared off.
art = np.asarray(crest)
shield_arr = np.zeros_like(art)
shield_arr[inner] = art[inner]

# This shield has a straight top edge, so every column can be filled up to the
# highest row the field reaches. A per-column threshold was tried first and left a
# notch wherever the helm covered more than the threshold allowed.
#
# The reconstructed strip cannot copy the artwork — the helm is exactly what was
# covering it. Extending each column's topmost surviving pixel upwards instead of
# painting a single flat blue keeps the field's shading continuous; a flat median
# left a visible seam at 512 px.
ys, xs = np.where(inner)
top, left, right = ys.min(), xs.min(), xs.max()

# One flat blue, taken from the field's own pixels in the upper fifth of the shield
# so it matches the local tone. Extending each column's nearest surviving pixel was
# tried instead and picked up whatever happened to sit at the boundary — antialiased
# edges became bright streaks, the lion's outline became a black bar.
band = field.copy()
band[top + round(0.2 * (ys.max() - top)):, :] = False
FIELD = np.median(art[band][:, :3], axis=0).astype(np.uint8)

for c in range(left, right + 1):
    column = inner[:, c]
    if not column.any():
        continue
    first = int(np.argmax(column))
    if first > top:
        shield_arr[top:first, c] = (*FIELD, 255)
        inner[top:first, c] = True

ring = ndimage.binary_dilation(inner, structure=disk(10)) & ~inner
shield_arr[ring] = (16, 18, 20, 255)

shield_full = Image.fromarray(shield_arr, mode='RGBA')
shield = shield_full.crop(shield_full.getbbox())
print(f'shield rebuilt, outline redrawn, {shield.size}')

# Square canvas, slightly larger than the shield so it does not touch the edges.
side = round(max(shield.size) * 1.08)
square = Image.new('RGBA', (side, side), (0, 0, 0, 0))
square.paste(shield, ((side - shield.width) // 2, (side - shield.height) // 2), shield)

def icon(size, path):
    """Palette-quantised so a 512 px icon is ~20 kB rather than ~250."""
    img = square.resize((size, size), Image.LANCZOS)
    img.quantize(colors=64, method=Image.FASTOCTREE).save(path, optimize=True)
    print(f'  {os.path.basename(path)}: {os.path.getsize(path) / 1e3:.0f} kB')


# Only the sizes the pages actually link. A 32 covers the tab at 1x and 2x and
# browsers downscale it cleanly, so there is no separate 16.
for size in (32, 512):
    icon(size, f'{ICONS}/favicon-{size}.png')
icon(180, f'{ICONS}/apple-touch-icon.png')
