/* ── PAXINDEX — NAVIGATION ── */

const NAV_PAGES = {
  'index.html':    'nav-classement',
  'carte.html':    'nav-carte',
  'tendances.html':'nav-tendances',
  'alertes.html':  'nav-alertes',
  'config.html':   'nav-config',
};

const TAB_PAGES = {
  'index.html':    'tab-global',
  'conflits.html': 'tab-conflits',
  'commerce.html': 'tab-commerce',
  'tendances.html':'tab-evolution',
  'stats.html':    'tab-stats',
};

document.addEventListener('DOMContentLoaded', () => {
  const page = location.pathname.split('/').pop() || 'index.html';

  /* Active bottom nav */
  const activeNav = NAV_PAGES[page];
  if (activeNav) {
    const el = document.getElementById(activeNav);
    if (el) el.classList.add('active');
  }

  /* Active header tab */
  const activeTab = TAB_PAGES[page];
  if (activeTab) {
    const el = document.getElementById(activeTab);
    if (el) el.classList.add('active');
  }

  /* Tab click → navigation */
  document.querySelectorAll('[data-href]').forEach(el => {
    el.addEventListener('click', () => {
      window.location.href = el.dataset.href;
    });
  });
});
