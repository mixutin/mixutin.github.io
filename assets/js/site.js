(() => {
  'use strict';
  const root = document.documentElement;
  root.classList.add('js');
  const menu = document.querySelector('.menu');
  const nav = document.querySelector('#navigation');
  if (menu && nav) {
    const close = () => {
      nav.classList.remove('open');
      menu.setAttribute('aria-expanded', 'false');
    };
    menu.addEventListener('click', () => {
      const open = menu.getAttribute('aria-expanded') !== 'true';
      nav.classList.toggle('open', open);
      menu.setAttribute('aria-expanded', String(open));
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
        close();
        menu.focus();
      }
    });
    document.addEventListener('click', event => {
      if (!nav.contains(event.target) && !menu.contains(event.target)) close();
    });
    nav.addEventListener('click', event => { if (event.target.closest('a')) close(); });
    matchMedia('(min-width: 821px)').addEventListener('change', close);
  }

  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let paused = reduced.matches;
  try { paused = reduced.matches || sessionStorage.getItem('portfolio-motion') === 'paused'; } catch {}
  const motionButtons = [...document.querySelectorAll('[data-motion-toggle]')];
  const applyMotion = () => {
    root.dataset.motion = paused ? 'paused' : 'running';
    motionButtons.forEach(button => {
      button.setAttribute('aria-pressed', String(paused));
      button.textContent = paused ? button.dataset.resume : button.dataset.pause;
    });
    document.dispatchEvent(new CustomEvent('portfolio:motion', { detail: { paused } }));
  };
  motionButtons.forEach(button => button.addEventListener('click', () => {
    paused = !paused;
    try { sessionStorage.setItem('portfolio-motion', paused ? 'paused' : 'running'); } catch {}
    applyMotion();
  }));
  reduced.addEventListener('change', event => { paused = event.matches; applyMotion(); });
  applyMotion();

  document.querySelectorAll('[data-project-browser]').forEach(browser => {
    const controls = browser.querySelector('[data-filter-controls]');
    const search = browser.querySelector('[data-project-search]');
    const buttons = [...browser.querySelectorAll('[data-filter]')];
    const cards = [...browser.querySelectorAll('[data-project]')];
    const count = browser.querySelector('[data-result-count]');
    const empty = browser.querySelector('[data-empty]');
    if (!controls || !search || !count || !empty) return;
    let category = 'all';
    const filter = () => {
      const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
      let visible = 0;
      cards.forEach(card => {
        const haystack = card.dataset.search.toLocaleLowerCase();
        card.hidden = !(category === 'all' || card.dataset.category === category) || !words.every(word => haystack.includes(word));
        if (!card.hidden) visible++;
      });
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
      count.textContent = `${visible} ${count.dataset.label}`;
      empty.hidden = visible > 0;
    };
    buttons.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filter(); }));
    search.addEventListener('input', filter);
    browser.querySelector('[data-reset]')?.addEventListener('click', () => {
      category = 'all'; search.value = ''; filter(); search.focus();
    });
    controls.hidden = false;
    filter();
  });

  if (['/', '/index.html', '/fi/', '/fi/index.html'].includes(location.pathname) && ['#workstation', '#ai-security'].includes(location.hash)) {
    location.replace(`${root.lang === 'fi' ? '/fi' : ''}/about/${location.hash}`);
  }
})();
