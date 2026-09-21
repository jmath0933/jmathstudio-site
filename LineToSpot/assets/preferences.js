(() => {
  const supported = ['en','ko','ja','zh-Hans','zh-Hant','es','fr','de','pt-BR','ru','id'];
  const key = 'jmath.lineToSpot.language.v1';
  function match(tag) {
    const t = String(tag || '').toLowerCase().replace(/_/g, '-');
    if (t === 'zh' || t.startsWith('zh-')) {
      if (t.includes('-hant')) return 'zh-Hant';
      if (t.includes('-hans')) return 'zh-Hans';
      return /(^|-)(tw|hk|mo)(-|$)/.test(t) ? 'zh-Hant' : 'zh-Hans';
    }
    const base = t.split('-')[0];
    if (base === 'pt') return 'pt-BR';
    return supported.includes(base) ? base : null;
  }
  function choose(saved, languages) {
    if (supported.includes(saved)) return saved;
    for (const tag of languages || []) { const code = match(tag); if (code) return code; }
    return 'en';
  }
  function saved() { try { return localStorage.getItem(key); } catch (_) { return null; } }
  function remember(code) { if (supported.includes(code)) { try { localStorage.setItem(key, code); } catch (_) {} } }
  function detect() { return choose(saved(), navigator.languages || [navigator.language]); }
  window.LineToSpotLanguage = { supported, match, choose, saved, remember, detect };
})();
