const root = document.documentElement;
const saved = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

function applyTheme(theme){
  root.setAttribute('data-theme', theme);
  const meta = document.getElementById('theme-color');
  meta.content = theme === 'dark' || (theme === '' && prefersDark) ? '#0b0f16' : '#ffffff';

  const darkIcon = document.querySelector('link[rel="icon"][media*="dark"]');
  const lightIcon = document.querySelector('link[rel="icon"][media*="light"]');
  if(darkIcon && lightIcon){
    if(theme === 'dark'){ darkIcon.media=''; lightIcon.media='not all'; }
    else if(theme === 'light'){ lightIcon.media=''; darkIcon.media='not all'; }
    else { darkIcon.media='(prefers-color-scheme: dark)'; lightIcon.media='(prefers-color-scheme: light)'; }
  }
}

// Initialize
applyTheme(saved ?? '');

document.addEventListener('DOMContentLoaded', () => {
  const btn = document.getElementById('theme-toggle');
  const current = root.getAttribute('data-theme');
  btn.textContent = current ? `Theme: ${current}` : 'Theme: auto';

  btn.addEventListener('click', () => {
    const cur = root.getAttribute('data-theme');
    const next = cur === '' ? 'dark' : cur === 'dark' ? 'light' : '';
    applyTheme(next);
    if(next === '') localStorage.removeItem('theme'); else localStorage.setItem('theme', next);
    btn.textContent = next ? `Theme: ${next}` : 'Theme: auto';
  });
});
