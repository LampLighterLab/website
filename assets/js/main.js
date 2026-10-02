(() => {
  const button = document.querySelector('.nav-toggle');
  const navigation = document.getElementById('site-nav');
  if (!button || !navigation) return;

  const setOpen = (open) => {
    navigation.classList.toggle('is-open', open);
    button.setAttribute('aria-expanded', String(open));
  };

  document.documentElement.classList.add('js');
  button.hidden = false;
  button.addEventListener('click', () => {
    setOpen(button.getAttribute('aria-expanded') !== 'true');
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
      setOpen(false);
      button.focus();
    }
  });
})();
