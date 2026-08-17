/* Appearance: theme (light/dark ground) and palette (which accent).
 *
 * Two independent axes, both stored and both applied to <html> before paint —
 * this file is loaded without `defer` in <head> — so there is no flash of the
 * wrong colours.
 *
 * Theme "auto" is the absence of data-theme, which lets the prefers-color-scheme
 * block in style.css do the work. The palette always has a value; magma is the
 * default and is written out rather than left implicit, so the picker can show
 * which one is active on first load.
 */
(() => {
  const THEMES = ['', 'dark', 'light'];
  const LABEL = { '': 'auto', dark: 'dark', light: 'light' };
  const PALETTES = ['magma', 'viridis', 'mono'];
  const root = document.documentElement;

  const read = (key, fallback) => {
    try {
      return localStorage.getItem(key) ?? fallback;
    } catch {
      return fallback;   // Safari private mode throws; the default is fine
    }
  };

  const write = (key, value) => {
    try {
      if (value) localStorage.setItem(key, value);
      else localStorage.removeItem(key);
    } catch { /* nothing to do if storage is unavailable */ }
  };

  let theme = read('theme', '') || '';
  if (!THEMES.includes(theme)) theme = '';

  let palette = read('palette', 'magma');
  if (!PALETTES.includes(palette)) palette = 'magma';

  function applyTheme() {
    if (theme) root.setAttribute('data-theme', theme);
    else root.removeAttribute('data-theme');

    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      const dark = theme === 'dark'
        || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches);
      meta.content = dark ? '#121316' : '#E4E6E4';
    }
  }

  function applyPalette() {
    root.setAttribute('data-palette', palette);
    // The demo listens for this so its colour map follows the page.
    document.dispatchEvent(new CustomEvent('palettechange', { detail: { palette } }));
  }

  applyTheme();
  applyPalette();

  // In auto mode the OS can change under us; follow it so theme-color stays right.
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (!theme) applyTheme();
  });

  document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('theme-toggle');
    if (btn) {
      const paint = () => {
        btn.textContent = LABEL[theme];
        btn.setAttribute('aria-label', `Appearance: ${LABEL[theme]}. Click to change.`);
      };
      paint();
      btn.addEventListener('click', () => {
        theme = THEMES[(THEMES.indexOf(theme) + 1) % THEMES.length];
        applyTheme();
        write('theme', theme);
        paint();
      });
    }

    const picker = document.getElementById('palette');
    if (!picker) return;

    const mark = () => {
      for (const b of picker.querySelectorAll('[data-palette]')) {
        b.setAttribute('aria-pressed', String(b.dataset.palette === palette));
      }
    };
    mark();

    picker.addEventListener('click', (e) => {
      const b = e.target.closest('button[data-palette]');
      if (!b || !PALETTES.includes(b.dataset.palette)) return;
      palette = b.dataset.palette;
      applyPalette();
      write('palette', palette);
      mark();
    });
  });
})();
