(() => {
  const preference = window.LineToSpotLanguage;
  const dialog = document.getElementById('language-dialog');
  let opener = null;
  let overflow = '';
  if (dialog && typeof dialog.showModal === 'function') {
    document.querySelectorAll('[data-open-language]').forEach(link => {
      link.setAttribute('aria-haspopup', 'dialog');
      link.addEventListener('click', event => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault(); opener = link; overflow = document.body.style.overflow;
        dialog.showModal(); document.body.style.overflow = 'hidden';
      });
    });
    document.getElementById('language-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => { document.body.style.overflow = overflow; if (opener) opener.focus(); });
  }
  document.querySelectorAll('[data-language]').forEach(link => {
    link.addEventListener('click', event => {
      const code = link.dataset.language;
      if (!preference.supported.includes(code)) return;
      preference.remember(code);
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      if (document.documentElement.dataset.preview === 'true' && window.parent !== window) {
        event.preventDefault(); window.parent.postMessage({type:'linetospot-language', code}, '*'); return;
      }
      // Relative HTML files can also be reviewed without a web server.
      if (location.protocol === 'file:') { event.preventDefault(); location.href = new URL('index.html', link.href).href; }
    });
  });
})();
