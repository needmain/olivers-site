document.addEventListener('DOMContentLoaded', () => {
  const menu = document.querySelector('.nav-menu');
  if (!menu) return;
  const links = menu.querySelectorAll('a[href]');
  const path = location.pathname.split('/').pop() || 'index.html';
  links.forEach(a => {
    const href = a.getAttribute('href');
    if (href === path) {
      a.classList.add('nav-active');
    }
  });

  const toggle = document.querySelector('.nav-toggle');
  if (toggle) {
    toggle.setAttribute('aria-expanded', 'false');
    toggle.addEventListener('click', () => {
      const expanded = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!expanded));
      menu.classList.toggle('active');
    });
  }
});
