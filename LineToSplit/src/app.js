(()=>{
'use strict';
const config=JSON.parse(document.getElementById('site-config').textContent);
const codes=config.languages.map(x=>x.code),key='jmath.linetosplit.language';
function resolveLanguage(preferences,available=codes){
 for(const raw of preferences){const l=String(raw).toLowerCase();let candidate;
 if(/^zh($|-)/.test(l))candidate=/hant|tw|hk|mo/.test(l)?'zh-TW':'zh-CN';
 else if(/^pt($|-)/.test(l))candidate='pt-BR';
 else candidate=l.split('-')[0];
 if(available.includes(candidate))return candidate;
 }return 'en';
}
// Export pure matching logic for future locale QA without enabling unfinished translations.
window.LineToSplit={resolveLanguage};
let saved;try{saved=localStorage.getItem(key)}catch{}
const rootURL=new URL(config.prefix||'./',location.href);
if(config.root){const chosen=codes.includes(saved)?saved:resolveLanguage(navigator.languages||[navigator.language]);if(chosen!=='en')location.replace(new URL(chosen+'/',rootURL).href+location.hash)}
const languageDialog = document.getElementById('language-dialog');
const languageButton = document.getElementById('language-button');
const languageClose = document.getElementById('language-close');

let languageOverflow = '';

if (
  languageDialog &&
  languageButton &&
  typeof languageDialog.showModal === 'function'
) {
  languageButton.addEventListener('click', () => {
    languageOverflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    languageDialog.showModal();
  });

  languageClose.addEventListener('click', () => {
    languageDialog.close();
  });

  languageDialog.addEventListener('close', () => {
    document.body.style.overflow = languageOverflow;
    languageButton.focus();
  });

  languageDialog.addEventListener('click', event => {
    const rect = languageDialog.getBoundingClientRect();

    if (
      event.target === languageDialog &&
      (
        event.clientX < rect.left ||
        event.clientX > rect.right ||
        event.clientY < rect.top ||
        event.clientY > rect.bottom
      )
    ) {
      languageDialog.close();
    }
  });
}

document.querySelectorAll('[data-language]').forEach(link => {
  link.addEventListener('click', event => {
    const selected = link.dataset.language;

    if (!codes.includes(selected)) {
      event.preventDefault();
      return;
    }

    try {
      localStorage.setItem(key, selected);
    } catch {}

    if (selected === config.current) {
      event.preventDefault();
      languageDialog?.close();
    }
  });
});
const gallery=document.getElementById('gallery'),prev=document.getElementById('prev'),next=document.getElementById('next');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
function move(direction){gallery.scrollBy({left:direction*(gallery.firstElementChild.getBoundingClientRect().width+parseFloat(getComputedStyle(gallery).gap)),behavior:reduced.matches?'instant':'smooth'})}
function update(){prev.disabled=gallery.scrollLeft<2;next.disabled=gallery.scrollLeft+gallery.clientWidth>=gallery.scrollWidth-2}
prev.addEventListener('click',()=>move(-1));next.addEventListener('click',()=>move(1));gallery.addEventListener('scroll',update,{passive:true});new ResizeObserver(update).observe(gallery);update();
gallery.addEventListener('keydown',e=>{if(e.target!==gallery)return;if(e.key==='ArrowRight'||e.key==='ArrowLeft'){e.preventDefault();move(e.key==='ArrowRight'?1:-1)}});
const dialog=document.getElementById('viewer'),image=document.getElementById('viewer-image');let trigger,oldOverflow;
if(typeof dialog.showModal==='function')document.querySelectorAll('.gallery a').forEach(a=>{a.setAttribute('aria-haspopup','dialog');a.addEventListener('click',e=>{if(e.ctrlKey||e.metaKey||e.altKey||e.shiftKey)return;e.preventDefault();trigger=a;image.src=a.href;image.alt=a.querySelector('img').alt;document.getElementById('viewer-caption').textContent=a.parentElement.querySelector('figcaption').textContent;oldOverflow=document.body.style.overflow;document.body.style.overflow='hidden';dialog.showModal()})});
document.getElementById('close').addEventListener('click',()=>dialog.close());dialog.addEventListener('close',()=>{document.body.style.overflow=oldOverflow;trigger?.focus();image.removeAttribute('src')});dialog.addEventListener('click',e=>{const r=dialog.getBoundingClientRect();if(e.target===dialog&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))dialog.close()});
})();
