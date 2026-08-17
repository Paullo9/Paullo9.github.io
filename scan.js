/* The lab scan: hotspots and named camera positions.
 *
 * The scan is the page's table of contents rather than an ornament — every marker
 * writes into the panel beside it, and the camera hotspot hands the reader on to
 * the dataset in section 02, which that camera is what recorded.
 *
 * Camera positions are absolute (target + orbit), not framing percentages, so they
 * stay put if the model is ever re-cropped to a different bounding box.
 */
(() => {
  const mv = document.getElementById('scan');
  if (!mv) return;

  const eyebrow = document.getElementById('scan-eyebrow');
  const title = document.getElementById('scan-title');
  const body = document.getElementById('scan-body');
  const views = document.getElementById('scan-views');

  /* Every line here is Paul's own description of the room. An earlier draft was
     written from the group's public equipment page plus guesswork and got three of
     five objects wrong — the high tension tank was called a nitrogen dewar, the
     holder cabinet a preparation bench, and the loading bench a control desk.
     Don't infer what a thing is from its shape in the scan. Ask. */

  const HOME = {
    eyebrow: 'The lab',
    title: 'Where I work',
    body: `<p>The lab I work in at the University of Siegen, scanned with the LiDAR
           sensor on my phone. Tap a marker.</p>`,
  };

  const INFO = {
    column: {
      eyebrow: 'Microscope',
      title: 'The column',
      body: `<p>An FEI Talos — the group's transmission electron microscope. Most of what
             I do happens at this thing.</p>`,
    },
    camera: {
      eyebrow: 'Camera',
      title: 'Where the data comes off',
      body: `<p>A camera sits under the column. In a 4D-STEM run it records a whole
             diffraction pattern at every point the beam stops at, which is where the
             dataset further down came from.</p>`,
      jump: { href: '#data', label: 'That dataset →' },
    },
    tank: {
      eyebrow: 'High tension',
      title: 'The high tension tank',
      body: `<p>The accelerating voltage for the microscope is generated in here, not in
             the column itself.</p>`,
    },
    cabinet: {
      eyebrow: 'Storage',
      title: 'The holder cabinet',
      body: `<p>A drying cabinet. The specimen holders live in here between sessions.</p>`,
    },
    plasma: {
      eyebrow: 'Cleaning',
      title: 'The plasma cleaner',
      body: `<p>Specimens and holders go in here first. A low-pressure plasma takes off the
             hydrocarbons that would otherwise crack into a carbon layer under the beam.</p>`,
    },
    desk: {
      eyebrow: 'Loading',
      title: 'The loading bench',
      body: `<p>Where the specimen goes into the holder, under a light microscope, before
             it goes anywhere near the column.</p>`,
    },
  };

  const buttons = [...mv.querySelectorAll('.hotspot')];

  function show(key) {
    const info = key ? INFO[key] : HOME;
    if (!info) return;

    eyebrow.textContent = info.eyebrow;
    title.textContent = info.title;
    body.innerHTML = info.body + (info.jump
      ? `<p><a class="btn" href="${info.jump.href}">${info.jump.label}</a></p>`
      : '');

    for (const b of buttons) {
      b.setAttribute('aria-pressed', String(b.dataset.hotspot === key));
    }
  }

  // ---- named camera positions ----

  // Only room / column / camera / tank have buttons under the scan; the other two
  // are reached by their marker. goTo() clears the button row when there is no
  // button for the view it flew to.
  const VIEWS = {
    room:    { target: '-0.55m 0.25m 0.1m',  orbit: '14deg 79deg 6.4m',  fov: '42deg' },
    column:  { target: '0.28m 0.35m 0.4m',   orbit: '0deg 80deg 3.2m',   fov: '42deg', info: 'column' },
    camera:  { target: '0.05m -0.85m 0.45m', orbit: '0deg 78deg 2.6m',   fov: '42deg', info: 'camera' },
    tank:    { target: '-1.3m -0.15m -1.3m', orbit: '22deg 80deg 2.8m',  fov: '44deg', info: 'tank' },
    cabinet: { target: '-1.6m -0.3m -0.2m',  orbit: '30deg 80deg 2.0m',  fov: '42deg', info: 'cabinet' },
    plasma:  { target: '1.45m -0.33m 0.6m',  orbit: '-72deg 78deg 1.5m', fov: '42deg', info: 'plasma' },
    desk:    { target: '1.35m -0.3m 1.1m',   orbit: '-78deg 74deg 4.4m', fov: '45deg', info: 'desk' },
  };

  function goTo(name) {
    const v = VIEWS[name];
    if (!v) return;
    mv.cameraTarget = v.target;
    mv.cameraOrbit = v.orbit;
    mv.fieldOfView = v.fov;
    for (const b of views.querySelectorAll('[data-view]')) {
      b.setAttribute('aria-pressed', String(b.dataset.view === name));
    }
    show(v.info || null);
  }

  views.addEventListener('click', (e) => {
    const b = e.target.closest('button[data-view]');
    if (b) goTo(b.dataset.view);
  });

  // A marker opens its panel and, where one exists, flies the camera to match.
  // Pressing the active marker again returns to the overview.
  for (const b of buttons) {
    b.addEventListener('click', () => {
      if (b.getAttribute('aria-pressed') === 'true') {
        goTo('room');          // has no `info`, so this also clears the panel
        return;
      }
      const key = b.dataset.hotspot;
      const name = Object.keys(VIEWS).find((k) => VIEWS[k].info === key);
      if (name) {
        goTo(name);
      } else {
        // No matching camera position — clear the preset row rather than leave a
        // view highlighted next to a panel it does not describe.
        for (const v of views.querySelectorAll('[data-view]')) v.setAttribute('aria-pressed', 'false');
        show(key);
      }
    });
  }

  // Dragging the model by hand invalidates whichever preset was highlighted.
  mv.addEventListener('camera-change', (e) => {
    if (e.detail.source !== 'user-interaction') return;
    for (const b of views.querySelectorAll('[data-view]')) b.setAttribute('aria-pressed', 'false');
  });
})();
