
    (() => {
      const dialog = document.getElementById('image-viewer');
      if (!dialog || typeof dialog.showModal !== 'function') return;
      const image = document.getElementById('viewer-image');
      const caption = document.getElementById('viewer-caption');
      let trigger = null;
      let previousOverflow = '';
      document.querySelectorAll('.gallery a').forEach(link => {
        link.setAttribute('aria-haspopup', 'dialog');
        link.addEventListener('click', event => {
          if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
          event.preventDefault();
          trigger = link;
          image.src = link.href;
          image.alt = link.querySelector('img').alt;
          caption.textContent = link.closest('figure').querySelector('figcaption').textContent;
          previousOverflow = document.body.style.overflow;
          dialog.showModal();
          document.body.style.overflow = 'hidden';
        });
      });
      document.getElementById('viewer-close').addEventListener('click', () => dialog.close());
      dialog.addEventListener('click', event => {
        const box = dialog.getBoundingClientRect();
        if (event.target === dialog && (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom)) dialog.close();
      });
      // Native modal dialog supports Escape and confines keyboard focus.
      dialog.addEventListener('close', () => {
        document.body.style.overflow = previousOverflow;
        if (trigger) trigger.focus();
        image.removeAttribute('src');
      });
    })();
  