# paullobpreis.com

Personal site of Paul Lobpreis — materials scientist, electron microscopy and 4D-STEM
at the University of Siegen. Served by GitHub Pages from `main`, at
[paullobpreis.com](https://paullobpreis.com) and `paullo9.github.io`.

Plain HTML, CSS and vanilla JavaScript. No build step, no dependencies fetched at
runtime, no web fonts, no analytics, no cookies, no third-party requests.

| Path | What |
|---|---|
| `index.html` | The landing page: links, the lab scan, the 4D-STEM demo. |
| `cv.html` | The full CV. |
| `style.css` | All styling for both pages. |
| `theme.js` | Light/dark toggle and the accent palette picker. |
| `scan.js` | Hotspots and camera positions for the 3D lab scan. |
| `demo.js` | The interactive 4D-STEM demo. |
| `vendor/` | `<model-viewer>`, vendored rather than loaded from a CDN. |
| `assets/` | The LiDAR scan of the lab, raw and cropped. |
| `assets/` | The family arms and the CV PDF. |
| `assets/` | Sprite atlas and manifest for the demo. |
| `tools/` | Dev-only generators for everything in `assets/`. Nothing at runtime uses them. |

Everything under `assets/` and `assets/` is derived and regenerable. If
something there looks wrong, fix the generator in `tools/`, not the artefact.

Local preview:

```bash
python3 -m http.server 4185
```
