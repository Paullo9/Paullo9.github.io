"""Export the 4D-STEM datacube to a sprite atlas for the demo on paullobpreis.com.

Same idea as the mac4DSTEM site's exporter, but tuned for a page that already
carries a 4 MB room scan: the scan is binned harder (3x rather than 2x) and the
atlas ships as lossless WebP, which lands around 1.5 MB instead of 5.4.

Layout: scan positions tile one image, each tile a full diffraction pattern.
Intensities are log-companded to uint8; the page rebuilds a 256-entry LUT from
the manifest and sums lut[byte], so integrals stay linear in recorded units.

Dev-only. Nothing at runtime uses this. Run it with an environment that has
h5py, numpy and pillow -- ~/miniconda3/envs/py4dstem does.
"""
import glob
import json
import math
import os

import h5py
import numpy as np
from PIL import Image

SRC = glob.glob('/Users/paullobpreis/GitHub/mac4DSTEM_Organization/website/datacube/*.h5')[0]
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media', 'demo')

SCAN_BIN = 3     # 200 -> 66 (198 used, 2 rows/cols dropped). Atlas 2112x2112.

os.makedirs(OUT, exist_ok=True)

with h5py.File(SRC, 'r') as h:
    data = h['/dm_dataset_root/dm_dataset/data'][()]          # (Ry, Rx, Qy, Qx) float32
    cal = h['/dm_dataset_root/metadatabundle/calibration']
    q_size = float(cal['Q_pixel_size'][()])
    r_size = float(cal['R_pixel_size'][()])
    q_units = cal['Q_pixel_units'][()]
    r_units = cal['R_pixel_units'][()]

q_units = q_units.decode() if isinstance(q_units, bytes) else q_units
r_units = r_units.decode() if isinstance(r_units, bytes) else r_units

Ry, Rx, Qy, Qx = data.shape
print(f'source  {data.shape} {data.dtype}  step {r_size} {r_units}  q {q_size} {q_units}')

# ---- bin the scan (crop the remainder rather than pad) ----
ry, rx = (Ry // SCAN_BIN) * SCAN_BIN, (Rx // SCAN_BIN) * SCAN_BIN
data = data[:ry, :rx]
data = data.reshape(ry // SCAN_BIN, SCAN_BIN, rx // SCAN_BIN, SCAN_BIN, Qy, Qx)
data = data.sum(axis=(1, 3))
Ry, Rx = data.shape[:2]
print(f'binned  {data.shape}  (scan step {r_size * SCAN_BIN:.3g} {r_units})')

# ---- clip and compand ----
np.clip(data, 0, None, out=data)
vmax = float(np.percentile(data, 99.999))          # ignore a few hot pixels
np.clip(data, 0, vmax, out=data)

knee = max(vmax / 5000.0, 1e-6)                    # sets how much low-signal detail survives
denom = math.log1p(vmax / knee)
companded = np.rint(255.0 * np.log1p(data / knee) / denom).astype(np.uint8)

# ---- lay out the atlas: tile (ry, rx) at pixel (rx*Qx, ry*Qy) ----
atlas = companded.transpose(0, 2, 1, 3).reshape(Ry * Qy, Rx * Qx)
print(f'atlas   {atlas.shape[1]}x{atlas.shape[0]} px')

# PNG, not WebP. Lossy WebP bleeds across tile edges -- neighbouring tiles are
# unrelated patterns -- and lossless WebP measured *larger* here than optimized
# PNG (2.64 vs 2.49 MB), so there is nothing to trade.
img = Image.fromarray(atlas, mode='L')
img.save(f'{OUT}/atlas.png', optimize=True)
print(f'  atlas.png: {os.path.getsize(f"{OUT}/atlas.png") / 1e6:.2f} MB')

manifest = {
    'scan':     {'x': Rx, 'y': Ry},
    'detector': {'x': Qx, 'y': Qy},
    'calibration': {
        'q_pixel_size': q_size, 'q_pixel_units': q_units,
        'r_pixel_size': r_size * SCAN_BIN, 'r_pixel_units': r_units,
    },
    'compand': {'knee': knee, 'vmax': vmax, 'denom': denom},
    'sample': 'Ni65Cu35 alloy',
}
with open(f'{OUT}/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

# ---- sanity check: the round trip must not move an ADF sum ----
lut = knee * np.expm1(np.arange(256) / 255.0 * denom)
decoded = lut[companded]
yy, xx = np.mgrid[0:Qy, 0:Qx]
r = np.hypot(yy - (Qy - 1) / 2, xx - (Qx - 1) / 2)
for label, mask in (('BF', r < 4), ('ADF', (r >= 6) & (r < 15))):
    ref = (data * mask).sum(axis=(2, 3))
    got = (decoded * mask).sum(axis=(2, 3))
    err = np.abs(got - ref) / np.maximum(ref, 1e-12)
    print(f'  {label:3s} sum error: median {np.median(err) * 100:.2f}%  max {err.max() * 100:.2f}%')
