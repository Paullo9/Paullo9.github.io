"""Generate the social card for paullobpreis.com.

The card puts the real mean diffraction pattern of the NiCu cube behind the
wordmark, so it is made of the same data the page is. Tinted to the magma accent,
which is the site's default palette.

The favicons and the header/footer mark are not made here — they come off the
family arms in tools/make_crest.py.

Dev-only. Run with ~/miniconda3/envs/py4dstem/bin/python.
"""
import json
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICONS = os.path.join(ROOT, 'media', 'index')
DEMO = os.path.join(ROOT, 'media', 'demo')

INK = (18, 19, 22)
ASH = (231, 233, 231)
ACCENT = (251, 144, 98)          # magma, dark-ground end — matches --accent
MUTED = (154, 160, 166)

MONO = '/System/Library/Fonts/Menlo.ttc'
SANS = '/System/Library/Fonts/HelveticaNeue.ttc'


def mean_pattern():
    """Mean diffraction pattern of the cube, decoded back to linear units."""
    with open(f'{DEMO}/manifest.json') as f:
        m = json.load(f)
    Rx, Ry = m['scan']['x'], m['scan']['y']
    Qx, Qy = m['detector']['x'], m['detector']['y']
    c = m['compand']

    atlas = np.asarray(Image.open(f'{DEMO}/atlas.png').convert('L'))
    cube = atlas.reshape(Ry, Qy, Rx, Qx).transpose(0, 2, 1, 3)
    lut = c['knee'] * np.expm1(np.arange(256) / 255.0 * c['denom'])
    return lut[cube].mean(axis=(0, 1))


pat = np.log1p(mean_pattern())
pat = (pat - pat.min()) / (np.ptp(pat) or 1)

# Tint the pattern from ink to accent so it sits inside the palette rather than
# on top of it, and keep it dim -- it is a texture, not a subject.
tint = np.stack([INK[i] + (ACCENT[i] - INK[i]) * pat * 0.62 for i in range(3)], axis=-1)
disc = Image.fromarray(tint.astype(np.uint8)).resize((900, 900), Image.LANCZOS)

card = Image.new('RGB', (1200, 630), INK)
card.paste(disc, (560, -135))

# Fade the pattern out towards the text so the wordmark never fights it. The ramp
# spans most of the card on purpose: a short one leaves a visible vertical seam.
grad = Image.new('L', (1200, 630))
gd = ImageDraw.Draw(grad)
for x in range(1200):
    gd.line([(x, 0), (x, 630)], fill=round(max(0.0, min(1.0, (1180 - x) / 700)) * 255))
card = Image.composite(Image.new('RGB', (1200, 630), INK), card, grad)

d = ImageDraw.Draw(card)
d.rectangle([0, 0, 1199, 6], fill=ACCENT)

name = ImageFont.truetype(SANS, 82, index=1)      # Bold
sub = ImageFont.truetype(SANS, 34)
tag = ImageFont.truetype(MONO, 24)

d.text((80, 232), 'Paul Lobpreis', font=name, fill=ASH)
d.text((80, 342), 'Materials scientist in Siegen', font=sub, fill=MUTED)
d.text((80, 452), 'PAULLOBPREIS.COM', font=tag, fill=ACCENT)

card.save(f'{ICONS}/og.jpg', quality=88, optimize=True, progressive=True)
print(f'og.jpg: {os.path.getsize(f"{ICONS}/og.jpg") / 1e3:.0f} kB')
