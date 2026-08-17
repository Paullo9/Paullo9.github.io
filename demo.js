/* A 4D-STEM dataset you can poke at, running entirely in the page.
 *
 * Same interaction as the demo on mac4dstem.com, on purpose: real space and
 * diffraction space side by side, each carrying a mask that produces the other.
 * The detector mask integrates to the virtual image; the scan region integrates
 * to the diffraction pattern. Panel order is diffraction-left, real-space-right,
 * which mirrors the app — keep the two in step if that layout ever changes.
 *
 * Data is a sprite atlas of real diffraction patterns (tools/export_atlas.py).
 * Intensities are log-companded to uint8 there and decompanded through a
 * 256-entry lookup table before any summing, so the sums stay linear in the
 * units the microscope recorded. Summing the raw bytes would look plausible and
 * be physically wrong.
 */
(() => {
  const root = document.getElementById('demo');
  if (!root) return;

  const ATLAS = 'assets/demo-atlas.png';
  const MANIFEST = 'assets/demo-manifest.json';

  const el = (id) => document.getElementById(id);
  const loadBtn = el('demo-load');
  const stage = el('demo-stage');
  const status = el('demo-status');
  const rCanvas = el('demo-real');
  const qCanvas = el('demo-diff');
  const rRead = el('demo-real-read');
  const qRead = el('demo-diff-read');
  const presetRow = el('demo-presets');

  let cube = null;                 // Uint8Array, ((ry*Rx + rx)*Qy + qy)*Qx + qx
  let lut = null;                  // Float32Array(256) — companded byte -> intensity
  let Rx, Ry, Qx, Qy, cal;

  // Masks, in pixel units of their own space.
  const det  = { cx: 0, cy: 0, rin: 0, rout: 4 };   // detector: annulus (rin = 0 -> disc)
  const scan = { cx: 0, cy: 0, r: 0, all: true };   // scan region

  /* ---------- colour maps ----------
   * 32 control points sampled from matplotlib, expanded to 256 entries by linear
   * interpolation. Both are perceptually uniform, which matters here: the eye
   * should read intensity differences, not the map's own contrast artefacts. */
  const MAP_POINTS = {
    viridis: '440154470d6048186a482374472e7c4538824241863e4a893a548c365d8d32658e2e6d8e2b758e287d8e25848e228c8d1f948c1e9c8920a38625ab822eb37c3aba7648c16e58c7656ccd5a7fd34e93d741a8db34c0df25d5e21aeae51afde725',
    magma:   '0000040303120a0822130d341e11492a115c38106c45107754137d6018806d1d81792282882781942c80a1307eae347bbd3977ca3e72d6456ce24d66ec5860f3655cf8745cfb835ffd9467fea36ffeb27afec185fed194fde0a1fceeb0fcfdbf',
  };

  function buildRamp(hex) {
    const n = hex.length / 6;
    const pts = [];
    for (let i = 0; i < n; i++) {
      const h = hex.slice(i * 6, i * 6 + 6);
      pts.push([parseInt(h.slice(0, 2), 16), parseInt(h.slice(2, 4), 16), parseInt(h.slice(4, 6), 16)]);
    }
    const ramp = new Uint8Array(256 * 3);
    for (let i = 0; i < 256; i++) {
      const t = (i / 255) * (n - 1);
      const a = Math.floor(t), b = Math.min(n - 1, a + 1), f = t - a;
      for (let c = 0; c < 3; c++) ramp[i * 3 + c] = Math.round(pts[a][c] + (pts[b][c] - pts[a][c]) * f);
    }
    return ramp;
  }

  const RAMPS = { grey: null };
  for (const k in MAP_POINTS) RAMPS[k] = buildRamp(MAP_POINTS[k]);

  // The demo starts on whichever map the page's accent came from, so picking
  // "magma" in the header and "magma" here mean the same thing. Once the visitor
  // chooses a map explicitly the demo stops following the header.
  const FROM_PALETTE = { magma: 'magma', viridis: 'viridis', mono: 'grey' };
  let mapName = FROM_PALETTE[document.documentElement.dataset.palette] || 'grey';
  let mapPinned = false;
  let ramp = RAMPS[mapName];       // null = greyscale

  function markMaps() {
    const row = el('demo-maps');
    if (!row) return;
    for (const b of row.querySelectorAll('button[data-map]')) {
      b.setAttribute('aria-pressed', String(b.dataset.map === mapName));
    }
  }

  document.addEventListener('palettechange', (e) => {
    if (mapPinned) return;
    mapName = FROM_PALETTE[e.detail.palette] || 'grey';
    ramp = RAMPS[mapName];
    markMaps();
    if (cube) recomputeBoth();
  });

  /* ---------- loading ---------- */

  async function load() {
    loadBtn.disabled = true;
    loadBtn.textContent = 'Loading…';

    try {
      const [manifest, img] = await Promise.all([
        fetch(MANIFEST).then((r) => {
          if (!r.ok) throw new Error(`manifest ${r.status}`);
          return r.json();
        }),
        new Promise((resolve, reject) => {
          const i = new Image();
          i.onload = () => resolve(i);
          i.onerror = () => reject(new Error('atlas failed to load'));
          i.src = ATLAS;
        }),
      ]);

      Rx = manifest.scan.x;     Ry = manifest.scan.y;
      Qx = manifest.detector.x; Qy = manifest.detector.y;
      cal = manifest.calibration;

      // Decode the atlas once, repack into per-position order, then let it go.
      const off = document.createElement('canvas');
      off.width = Rx * Qx;
      off.height = Ry * Qy;
      const octx = off.getContext('2d', { willReadFrequently: true });
      octx.drawImage(img, 0, 0);
      const rgba = octx.getImageData(0, 0, off.width, off.height).data;

      cube = new Uint8Array(Rx * Ry * Qx * Qy);
      for (let ry = 0; ry < Ry; ry++) {
        for (let qy = 0; qy < Qy; qy++) {
          const row = (ry * Qy + qy) * off.width;
          for (let rx = 0; rx < Rx; rx++) {
            const src = (row + rx * Qx) * 4;
            const dst = ((ry * Rx + rx) * Qy + qy) * Qx;
            for (let qx = 0; qx < Qx; qx++) cube[dst + qx] = rgba[src + qx * 4];
          }
        }
      }
      off.width = off.height = 0;

      const { knee, denom } = manifest.compand;
      lut = new Float32Array(256);
      for (let i = 0; i < 256; i++) lut[i] = knee * Math.expm1((i / 255) * denom);

      det.cx = (Qx - 1) / 2;  det.cy = (Qy - 1) / 2;
      scan.cx = (Rx - 1) / 2; scan.cy = (Ry - 1) / 2; scan.r = Math.min(Rx, Ry) / 4;

      stage.hidden = false;
      loadBtn.hidden = true;
      status.textContent = `${Rx}×${Ry} scan · ${Qx}×${Qy} detector · ${manifest.sample}`;
      markMaps();
      sizeCanvases();
      recomputeBoth();
    } catch (err) {
      loadBtn.disabled = false;
      loadBtn.textContent = 'Retry';
      status.textContent = `Could not load the dataset — ${err.message}`;
    }
  }

  /* ---------- computation ---------- */

  // Detector mask -> virtual image over the whole scan.
  function virtualImage() {
    const out = new Float32Array(Rx * Ry);
    const idx = [];
    for (let qy = 0; qy < Qy; qy++) {
      for (let qx = 0; qx < Qx; qx++) {
        const d = Math.hypot(qx - det.cx, qy - det.cy);
        if (d >= det.rin && d < det.rout) idx.push(qy * Qx + qx);
      }
    }
    const n = idx.length;
    for (let p = 0; p < Rx * Ry; p++) {
      const base = p * Qx * Qy;
      let acc = 0;
      for (let k = 0; k < n; k++) acc += lut[cube[base + idx[k]]];
      out[p] = acc;
    }
    return out;
  }

  // Scan region -> summed diffraction pattern.
  function diffractionPattern() {
    const out = new Float32Array(Qx * Qy);
    const npx = Qx * Qy;
    let count = 0;
    for (let ry = 0; ry < Ry; ry++) {
      for (let rx = 0; rx < Rx; rx++) {
        if (!scan.all && Math.hypot(rx - scan.cx, ry - scan.cy) >= scan.r) continue;
        const base = (ry * Rx + rx) * npx;
        for (let i = 0; i < npx; i++) out[i] += lut[cube[base + i]];
        count++;
      }
    }
    if (count) for (let i = 0; i < npx; i++) out[i] /= count;
    return out;
  }

  /* ---------- rendering ---------- */

  function percentiles(arr, lo, hi) {
    const s = Float32Array.from(arr).sort();
    const at = (f) => s[Math.min(s.length - 1, Math.max(0, Math.round(f * (s.length - 1))))];
    return [at(lo), at(hi)];
  }

  function paint(canvas, values, w, h, logScale) {
    const disp = logScale ? Float32Array.from(values, (v) => Math.log1p(Math.max(v, 0))) : values;
    const [lo, hi] = percentiles(disp, 0.02, 0.995);
    const span = hi - lo || 1;

    const buf = document.createElement('canvas');
    buf.width = w; buf.height = h;
    const bctx = buf.getContext('2d');
    const img = bctx.createImageData(w, h);
    for (let i = 0; i < w * h; i++) {
      const v = Math.max(0, Math.min(1, (disp[i] - lo) / span));
      const g = Math.round(v * 255);
      if (ramp) {
        img.data[i * 4]     = ramp[g * 3];
        img.data[i * 4 + 1] = ramp[g * 3 + 1];
        img.data[i * 4 + 2] = ramp[g * 3 + 2];
      } else {
        img.data[i * 4] = img.data[i * 4 + 1] = img.data[i * 4 + 2] = g;
      }
      img.data[i * 4 + 3] = 255;
    }
    bctx.putImageData(img, 0, 0);

    const ctx = canvas.getContext('2d');
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.imageSmoothingEnabled = false;
    const side = canvas.width / dpr;
    ctx.clearRect(0, 0, side, side);
    ctx.drawImage(buf, 0, 0, side, side);
    return side;
  }

  // Masks are stroked twice — a dark halo, then a light dash on top — so they stay
  // legible over any colour map, including the bright end of viridis and magma.
  function overlay(canvas, draw) {
    const ctx = canvas.getContext('2d');
    ctx.save();
    ctx.lineWidth = 3.5;
    ctx.setLineDash([]);
    ctx.strokeStyle = 'rgba(0,0,0,0.6)';
    draw(ctx);
    ctx.lineWidth = 1.5;
    ctx.setLineDash([5, 3]);
    ctx.strokeStyle = '#ffffff';
    draw(ctx);
    ctx.restore();
  }

  function drawReal() {
    const side = paint(rCanvas, virtualImage(), Rx, Ry, false);
    const s = side / Rx;
    if (!scan.all) {
      overlay(rCanvas, (ctx) => {
        ctx.beginPath();
        ctx.arc((scan.cx + 0.5) * s, (scan.cy + 0.5) * s, scan.r * s, 0, Math.PI * 2);
        ctx.stroke();
      });
    }
    const nm = cal.r_pixel_size;
    rRead.textContent = scan.all
      ? `whole scan · ${(Rx * nm / 1000).toFixed(2)} × ${(Ry * nm / 1000).toFixed(2)} µm`
      : `region r = ${(scan.r * nm).toFixed(0)} nm`;
  }

  function drawDiff() {
    const side = paint(qCanvas, diffractionPattern(), Qx, Qy, true);
    const s = side / Qx;
    overlay(qCanvas, (ctx) => {
      ctx.beginPath();
      ctx.arc((det.cx + 0.5) * s, (det.cy + 0.5) * s, det.rout * s, 0, Math.PI * 2);
      ctx.stroke();
      if (det.rin > 0) {
        ctx.beginPath();
        ctx.arc((det.cx + 0.5) * s, (det.cy + 0.5) * s, det.rin * s, 0, Math.PI * 2);
        ctx.stroke();
      }
    });
    const q = cal.q_pixel_size;
    qRead.textContent = det.rin > 0
      ? `annular · ${(det.rin * q).toFixed(2)}–${(det.rout * q).toFixed(2)} Å⁻¹`
      : `disc · r = ${(det.rout * q).toFixed(2)} Å⁻¹`;
  }

  function recomputeBoth() { drawDiff(); drawReal(); }

  /* ---------- interaction ---------- */

  function sizeCanvases() {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    for (const c of [rCanvas, qCanvas]) {
      const rect = c.getBoundingClientRect();
      if (!rect.width) continue;
      c.width = Math.round(rect.width * dpr);
      c.height = Math.round(rect.width * dpr);
    }
  }

  function pointerPos(canvas, e, n) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: ((e.clientX - rect.left) / rect.width) * n - 0.5,
      y: ((e.clientY - rect.top) / rect.height) * n - 0.5,
    };
  }

  function bindDrag(canvas, n, onMove) {
    let active = false;
    canvas.addEventListener('pointerdown', (e) => {
      active = true;
      canvas.setPointerCapture(e.pointerId);
      onMove(pointerPos(canvas, e, n));
    });
    canvas.addEventListener('pointermove', (e) => {
      if (active) onMove(pointerPos(canvas, e, n));
    });
    canvas.addEventListener('pointerup', () => { active = false; });
    canvas.addEventListener('pointercancel', () => { active = false; });
  }

  function wireInteractions() {
    bindDrag(qCanvas, Qx, (p) => {
      det.cx = Math.max(0, Math.min(Qx - 1, p.x));
      det.cy = Math.max(0, Math.min(Qy - 1, p.y));
      recomputeBoth();
    });

    qCanvas.addEventListener('wheel', (e) => {
      e.preventDefault();
      const step = e.deltaY > 0 ? 0.6 : -0.6;
      if (e.shiftKey) det.rin = Math.max(0, Math.min(det.rout - 1, det.rin + step));
      else det.rout = Math.max(det.rin + 1, Math.min(Qx / 2, det.rout + step));
      recomputeBoth();
    }, { passive: false });

    bindDrag(rCanvas, Rx, (p) => {
      scan.all = false;
      scan.cx = Math.max(0, Math.min(Rx - 1, p.x));
      scan.cy = Math.max(0, Math.min(Ry - 1, p.y));
      recomputeBoth();
    });

    rCanvas.addEventListener('wheel', (e) => {
      if (scan.all) return;
      e.preventDefault();
      scan.r = Math.max(2, Math.min(Rx / 2, scan.r + (e.deltaY > 0 ? 1.5 : -1.5)));
      recomputeBoth();
    }, { passive: false });

    presetRow.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-preset]');
      if (!b) return;
      const p = b.dataset.preset;
      det.cx = (Qx - 1) / 2; det.cy = (Qy - 1) / 2;
      if (p === 'bf')    { det.rin = 0;  det.rout = 4; }
      if (p === 'adf')   { det.rin = 6;  det.rout = 12; }
      if (p === 'haadf') { det.rin = 12; det.rout = 16; }
      if (p === 'all')   { scan.all = true; }
      for (const x of presetRow.querySelectorAll('button[data-preset]')) {
        x.setAttribute('aria-pressed', String(x === b && p !== 'all'));
      }
      recomputeBoth();
    });

    el('demo-maps').addEventListener('click', (e) => {
      const b = e.target.closest('button[data-map]');
      if (!b) return;
      mapName = b.dataset.map;
      mapPinned = true;
      ramp = RAMPS[mapName] || null;
      markMaps();
      recomputeBoth();
    });

    window.addEventListener('resize', () => {
      if (!cube) return;
      sizeCanvases();
      recomputeBoth();
    });
  }

  async function start() {
    await load();
    if (cube) wireInteractions();
  }

  loadBtn.addEventListener('click', start);

  // Load on approach so the demo is simply there when you scroll to it — but never
  // on a metered or slow connection, where 2.5 MB is the visitor's problem, not ours.
  const conn = navigator.connection;
  const frugal = conn && (conn.saveData || /^(slow-)?2g$/.test(conn.effectiveType || ''));
  if (frugal) {
    status.textContent = 'Not loaded — 2.5 MB, tap to load.';
  } else {
    const io = new IntersectionObserver((entries) => {
      for (const e of entries) {
        if (e.isIntersecting && !cube) { io.disconnect(); start(); }
      }
    }, { rootMargin: '600px' });
    io.observe(root);
  }
})();
