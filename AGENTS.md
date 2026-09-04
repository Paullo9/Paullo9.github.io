# AGENTS.md — paullobpreis.com

Context for the `Paullo9/Paullo9.github.io` repo. Last updated 2026-08-17.

## What this is

Paul Lobpreis's personal site. Live at **https://paullobpreis.com** (apex, via
Cloudflare DNS in the same account as `mac4dstem.com` — the grey-cloud/DNS-only
pattern documented in that repo's AGENTS.md applies here identically).

Structurally a **sibling of mac4dstem.com**: same neutral greys, same mono
uppercase label idiom, same hairline rules. The accent is not fixed — see
Palettes below.

**This is not a work-context site.** Paul said so explicitly on 2026-08-17, after
a first version built the whole landing page as a narrative funnel into 4D-STEM.
Microscopy and mac4DSTEM are a small part of what he does, and subpages on other
topics (sport, travel, a photo feed, a delayed diary) are planned. Two rules fall
out of that, and both were learned the hard way:

- **Keep the copy short and unproduced.** Lines like "This is the room everything
  on this page comes out of" and "real geometry, real mess, no modelling" were
  called out as pretentious and obviously generated. No scene-setting, no filler,
  no gap-filling. If a sentence is not carrying a fact, delete it.
- **The instruments are not his.** They belong to the chair and to the university.
  An earlier draft read like a private gear list — brand names, spec tables, "our
  TEM lab". Never write it that way again.

## Ground rules

- **Plain HTML + CSS + vanilla JS. No build step, no framework.** Push to `main`
  and Pages publishes in about a minute.
- **No web fonts.** System stack only — embedding Google Fonts is a GDPR problem
  in Germany.
- **No third-party requests at runtime.** `<model-viewer>` is vendored into
  `vendor/`, not pulled from unpkg. The footer states this as fact; adding any
  external fetch makes that a lie.
- **No Git LFS.** Pages serves the pointer file, not the content.

## Page structure

`index.html` is one scrolling page, chosen from three mockups on 2026-08-17:

> **Welcome line** → **Elsewhere** (the links) → **4D-STEM** (the demo) →
> **Projects** (mac4DSTEM) → **The lab** (the scan)

The links stay first. The demo led the page for one iteration and was moved back
down: opening on 4D-STEM makes the site read as a work page, which is the one
thing it is not supposed to be.

The hero is deliberately almost empty: the name at reading size and one line
saying the site is under construction. A tagline and an introductory paragraph
were both there and were both cut — the name is already in the header and the
description read as generated filler. **Don't put a bio back.**

Links come before the microscopy on purpose — they are what most visitors want,
and it keeps the work from leading. There are no section numbers; they made the
page look more produced than it should.

### The nav holds pages, never sections

`Home · CV` today, growing to `Home · Projects · Travel · … · CV`. An earlier
version mixed in-page anchors (Links, Lab, Projects) with a real page (CV), and
Paul found it unsatisfying without being able to say why — that was the reason.
Anchors and pages behave differently and must not sit in one row. Adding a topic
means one new file and one new entry; sections inside a page are just scrolled to.

"Projects" is a section on Home for now. It becomes its own page when there is a
second project — not before. Do **not** make Projects a catch-all for the planned
travel/training/gallery pages; those are content, not projects, and burying them
one level down is worse than a longer nav.

The scan (`#lab`) is `loading="lazy"`, so its 4.1 MB GLB is only fetched when a
visitor scrolls near it. Verified: at a 700 px viewport height the first load is
3.4 MB instead of 7.5 MB.

`cv.html` is the full CV as HTML, with the PDF as a download rather than an
`<iframe>`. It carries a print stylesheet. **The CV does not appear on the
landing page** — an excerpt was there and was confusing.

## Palettes

Two independent axes on `<html>`, both set by `theme.js` before paint and both
stored in localStorage:

| Attribute | Values |
|---|---|
| `data-theme` | `light`, `dark`, or absent (follow the OS) |
| `data-palette` | `magma` (default), `viridis`, `mono` |

The theme moves the greys; the palette moves only `--accent`. The page stays the
same quiet grey either way — the colour is meant to be about as loud as the old
teal was, no louder.

Accent values are read off the matplotlib maps the demo already uses, so "magma"
in the header and "magma" in the demo mean the same thing. Light grounds need the
dark end of each map and dark grounds the light end, so all nine combinations are
written out in `style.css`. A `var()` indirection there would break the
`prefers-color-scheme` fallback — don't refactor it into one.

`theme.js` fires a `palettechange` event; `demo.js` listens and switches its
colour map to match, **until the visitor picks a map by hand**, after which it
stops following (`mapPinned`).

## The lab scan

`assets/lab-raw.glb` is the raw capture, taken with the LiDAR sensor on
Paul's iPhone (the filename predates knowing that). It carries a large sheet
of floor/wall bleeding several metres past the west wall, which hangs off the
model like a torn flag. `tools/crop_glb.py` cuts it out by triangle centroid:

```bash
python3 tools/crop_glb.py --x-min -2.9 --out assets/lab.glb
```

That drops 8% of the triangles and nothing that belongs to the room — the door
wall survives; it was checked side by side. **The page loads `assets/lab.glb`.**
Keep the raw file: it is the source the cropper needs.

Hotspot `data-position` / `data-normal` values in `index.html` were picked off
the live model with `positionAndNormalFromPoint`. They are absolute model-space
coordinates, so they survive re-cropping. Camera positions in `scan.js` are
absolute target + orbit for the same reason — not framing percentages.

`min-camera-orbit` / `max-camera-orbit` in `index.html` keep the viewer inside
the room; without them you can orbit under the floor.

### What the six markers are

Every description comes from Paul directly (2026-08-17). An earlier version was
written from the group's public equipment page plus guesswork and **got three of
five wrong**:

| Marker | Is | Was wrongly called |
|---|---|---|
| `column` | the group's FEI Talos | — |
| `camera` | the camera under the column | — |
| `tank` | the **high tension tank** — where the accelerating voltage is generated | "liquid nitrogen dewar" |
| `cabinet` | a **drying cabinet** holding the TEM specimen holders | "preparation bench" |
| `plasma` | the **plasma cleaner** — the blue and white box | (was missing) |
| `desk` | where the specimen is loaded into the holder under a light microscope | "where the microscope is driven from" |

**Do not infer what an object is from its shape in the scan.** A white cylinder is
not a dewar. Ask.

The copy lives in the `INFO` object in `scan.js`; positions and `data-normal`
values are in `index.html`. Only room / column / camera / tank have buttons under
the scan — the rest are reached by their marker, and `goTo()` clears the button
row when it flies somewhere no button represents.

## The 4D-STEM demo

Real space and diffraction space side by side, each carrying a mask that produces
the other. **This is intentionally the same interaction as mac4dstem.com** — Paul
asked for it explicitly on 2026-08-17, after a first version that split the idea
into separate "probe" and "detector" modes. **That earlier version is gone, not
archived** — nothing had been committed when it was replaced. If the raw
single-position pattern view is ever wanted back, it has to be rewritten.

Panel order is **diffraction-left, real-space-right**, mirroring the app and the
mac4DSTEM site. Keep all three in step.

Copy in this section must not say "left" and "right": the panels stack on a phone.

### Data

Source cube is the same NiCu file as the mac4DSTEM site
(`mac4DSTEM_Organization/website/datacube/*.h5`, ~156 MB, gitignored there).
`tools/export_atlas.py` writes `assets/demo-atlas.png` + `manifest.json`.

Three things not to "optimise":

**The atlas is PNG and lossless on purpose.** Lossy WebP bleeds across tile
edges — neighbouring tiles are unrelated patterns — and lossless WebP measured
*larger* than optimized PNG here (2.64 vs 2.49 MB). There is nothing to trade.

**Intensities are companded, not raw.** 8 bits cannot hold the linear range
between the direct beam and dark-field signal. The page rebuilds a 256-entry
Float32 LUT from the manifest and sums `lut[byte]`. Summing raw bytes would look
plausible and be physically wrong. Round-trip error on ADF sums is 0.10% median.

**The scan is binned 3×, not 2×.** mac4dstem.com bins 2× and ships 5.4 MB; this
page already carries a 4.1 MB room scan, so it bins to 66×66 and 2.5 MB. Scan
step is therefore 9 nm, not 3.

Auto-loads on approach via IntersectionObserver (600 px `rootMargin`), skipped on
`saveData` or 2g. Canvases use `touch-action: pan-y` so a vertical swipe still
scrolls past the demo on a phone.

## The family arms

`assets/crest-source.png` is the source, on a dark radial glow rather than
transparency. `tools/make_crest.py` keys it out and writes `assets/crest.png`.

Keying by colour does not work — the glow is strongly tinted and the artwork's own
outlines are as dark as the background. The mask is built from brightness instead
(`val > 0.55`, which catches every fill and misses the outlines), then closed with
a disk wider than an outline to bridge across them. Only *small* enclosed holes are
filled: the large pockets between the mantling scrolls are background and must stay
transparent. The artwork touches the source frame, so "background = connected to the
border" is not available.

The full achievement is the header logo and the footer mark. **The favicons are
the shield alone** — at 16 px the mantling, helm, crown and flowers collapse into
a smudge, while a gold lion on a blue field still reads. Both were rendered side
by side at 16 and 32 px before choosing.

The old "PL" monogram is gone; `tools/make_brand.py` now only builds the social
card. `assets/logo.png` and the unused favicon sizes were deleted with it.

## The research group link

The group's site moved. Both links — the Elsewhere tile on Home and the current
position on the CV — point at **https://www.uni-siegen.de/en/nt/lmn**, which is the
page Paul built. The old `lmn.mb.uni-siegen.de` is stale; do not restore it. The
JSON-LD `affiliation` names the group and uses the same URL.

## Open items

1. **The CV PDF exposes a private address and mobile number.** `assets/cv.pdf`
   is public and contains Donnerscheidtstr. 12 and a phone number. It needs
   regenerating from the LaTeX source with the university address instead. It is
   also 9.7 MB, which is a photo that was never downsampled.
2. **Demo data publishability — unconfirmed.** Same open question as the
   mac4DSTEM site: the NiCu atlas is real thesis data. Confirm it is cleared.
3. **No personal Instagram.** Only the group account `@lmn_unisiegen` is linked;
   Paul's own was asked for and not supplied.
4. **Paul is not on the group's staff page.** Worth asking to be added — the site
   links there.
5. **No Impressum.** A purely private, non-commercial site generally falls
   outside § 5 DDG, but a site that markets professional work is a grey area.
   Paul's call.
6. **Nothing is committed yet.** Everything sits in the working tree on `main`.
7. **No postal address anywhere.** Paul asked for the footer to carry only the
   email and the arms. The address he gave ("Adolf-Reichweinstr. 28") could not be
   confirmed — the group's contact page still says Paul-Bonatz-Str. 9–11 and the
   AR campus is officially Adolf-Reichwein-Str. 2 — so nothing is published.
8. **The "Other" CV section was removed.** It said handball at TSG Siegen, which
   is no longer current. Paul intends to put a different hobby there.
8. **Subpages wanted.** Ideas raised: a guestbook, chess, a personal photo feed,
   an Anki-style quiz, a this-or-that game with a results table, personal stats,
   a training log (possibly auto-updating from Strava), a diary on a year's
   delay. Nothing decided.

## Preview

`.Codex/launch.json` runs `python3 -m http.server 4185`. Note that the in-app
browser pane only captures screenshots reliably at `scrollY === 0` — to inspect a
section, hide the other `main > .wrap` blocks with JS rather than scrolling.
