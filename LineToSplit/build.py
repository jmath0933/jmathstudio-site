import json,html,shutil
from pathlib import Path
R=Path(__file__).parent; D=R/'dist'; C=json.loads((R/'src/config.json').read_text()); enabled=[l for l in C['languages'] if l['enabled']]; base=C['baseUrl']; E=html.escape

def page(lang,root=False):
 t=json.loads((R/f'src/locales/{lang}.json').read_text());u=t['ui']; prefix='' if root else '../'; url=base if root else base+lang+'/'; canonical=base+lang+'/'
 privacy_href = prefix + ('privacy-ko.html' if lang == 'ko' else 'privacy.html')
 privacy_label = '개인정보처리방침' if lang == 'ko' else 'Privacy Policy'
 def asset(n):return prefix+'assets/'+n
 def img(n,cls='screen',caption='',eager=False):
  return f'<figure class="{cls}"><img src="{asset(f"screen-{n:02}.webp")}" width="1536" height="2048" alt="{E(t["imageAlts"][n-1])}" '+('fetchpriority="high"' if eager else 'loading="lazy" decoding="async"')+'>'+ (f'<figcaption>{E(caption)}</figcaption>' if caption else '')+'</figure>'
 def stores():return f'<div class="stores"><a class="store" href="{E(C["appStore"])}"><small>{E(u["appStore"])}</small><strong>App Store</strong></a><a class="store" href="{E(C["googlePlay"])}"><small>{E(u["googlePlay"])}</small><strong>Google Play</strong></a></div>'
 def heading(key,intro=None):return f'<div class="section-head"><h2>{E(t[key])}</h2>'+ (f'<p>{E(t[intro])}</p>' if intro else '')+'</div>'
 def section(content,id=''):return f'<section class="section"'+(f' id="{id}"' if id else '')+'>'+content+'</section>'
 alts=''.join(f'<link rel="alternate" hreflang="{l["code"]}" href="{base}{l["code"]}/">' for l in enabled)+f'<link rel="alternate" hreflang="x-default" href="{base}">'
 schema={'@context':'https://schema.org','@type':'SoftwareApplication','name':'Line To Split','url':canonical,'applicationCategory':'GameApplication','operatingSystem':'iOS, Android','description':t['metaDescription'],'offers':{'@type':'Offer','price':'0','priceCurrency':'USD'},'author':{'@type':'Organization','name':'Jmath Studio','url':'https://jmathstudio.com/'},'downloadUrl':[C['appStore'],C['googlePlay']]}
 runtime={'languages':enabled,'current':lang,'root':root,'prefix':prefix}
 language_links=''.join(
  f'<li><a href="{prefix}{l["code"]}/" data-language="{l["code"]}" '
  f'lang="{l["code"]}" hreflang="{l["code"]}"'
  + (' aria-current="page"' if l['code']==lang else '')
  + f'>{E(l["label"])}</a></li>'
  for l in enabled
 )
 current_label=next((l['label'] for l in enabled if l['code']==lang),lang)
 out=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(t['metaTitle'])}</title><meta name="description" content="{E(t['metaDescription'])}"><meta name="theme-color" content="#f4f8fc"><link rel="canonical" href="{canonical}">{alts}<meta property="og:type" content="website"><meta property="og:site_name" content="Jmath Studio"><meta property="og:title" content="{E(t['metaTitle'])}"><meta property="og:description" content="{E(t['metaDescription'])}"><meta property="og:url" content="{canonical}"><meta name="twitter:card" content="summary"><meta name="twitter:title" content="{E(t['metaTitle'])}"><meta name="twitter:description" content="{E(t['metaDescription'])}"><link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='7' fill='%23175ca5'/%3E%3Cpath d='M19 2L13 30' stroke='white' stroke-width='3'/%3E%3C/svg%3E"><link rel="stylesheet" href="{prefix}style.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script></head><body><a class="skip" href="#main">{E(u['skip'])}</a><div class="blueprint"><header class="header wrap"><a class="brand" href="https://jmathstudio.com/">Jmath Studio</a><nav aria-label="Page navigation"><a href="#how-to-play">{E(t['nav'][0])}</a><a href="#screenshots">{E(t['nav'][1])}</a><a href="#download">{E(t['nav'][2])}</a></nav><button class="language-menu" type="button" id="language-button" data-open-language aria-haspopup="dialog">{E(current_label)}</button></header><main id="main"><div class="wrap">'''
 out+=f'<section class="hero"><div><p class="eyebrow">{E(t["eyebrow"])}</p><h1>Line To Split</h1><p class="tagline">{E(t["tagline"][0])}<br><span>{E(t["tagline"][1])}</span></p><p class="intro">{E(t["intro"])}</p>{stores()}<p class="fine">{E(t["downloadNote"])}</p></div>{img(3,caption=t["galleryLabels"][2],eager=True)}</section>'
 out+=section(heading('howHeading')+'<div class="steps">'+''.join(f'<article><div><span class="number">0{i+1}</span><h3>{E(a)}</h3><p>{E(b)}</p></div>{img(n)}</article>' for i,(a,b,n) in enumerate(t['how']))+'</div>','how-to-play')
 out+=section(f'<p class="eyebrow">{E(t["normalLabel"])}</p>'+heading('normalHeading','normalIntro')+'<div class="stages">'+''.join(f'<article><span class="number">{E(u["stage"])} {i+1}</span><h3 class="ratio">{E(a)}</h3><p>{E(b)}</p>'+img([4,3,8][i])+(f'<aside class="tip"><strong>{E(u["tip"])}</strong><p>{E(t["tip"])}</p></aside>' if i==2 else '')+'</article>' for i,(a,b) in enumerate(t['normalStages']))+'</div>','normal-mode')
 out+=section(heading('feedbackHeading')+'<div class="feedback">'+''.join(f'<article><img src="{asset(n+".png")}" width="512" height="512" loading="lazy" alt="{E(a)} archery feedback"><h3>{E(a)}</h3><p>{E(b)}</p></article>' for a,b,n in t['feedback'])+f'</div><div class="star-result"><h3>{E(t["stars"])}</h3>{img(9)}</div>')
 out+='</div><section class="bridge"><div class="wrap"><h2>'+E(t['unlockHeading'][0])+'<br><span>'+E(t['unlockHeading'][1])+f'</span></h2></div></section></div><div class="dark"><div class="wrap">'
 out+=f'<section class="challenge" id="challenge-mode"><div><p class="eyebrow">{E(t["challengeLabel"])}</p><h2>{E(t["challengeHeading"])}</h2><p class="intro">{E(t["challengeIntro"])}</p><ol>'+''.join(f'<li><span class="number">{E(u["stage"])} {i+1}</span><h3>{E(a)}</h3><p>{E(b)}</p></li>' for i,(a,b) in enumerate(t['challengeStages']))+'</ol><p class="closing">'+'<br>'.join(map(E,t['challengeClosing']))+f'</p><div class="mood"><h3>{E(t["moodHeading"])}</h3><p>{E(t["moodText"])}</p></div></div>{img(10)}</section>'
 out+='</div></div><div class="blueprint post-challenge"><div class="wrap">'
 gallery=f'<div class="gallery-heading">{heading("galleryHeading","galleryIntro")}<div class="controls"><button id="prev" aria-label="{E(u["previous"])}" aria-controls="gallery">←</button><button id="next" aria-label="{E(u["next"])}" aria-controls="gallery">→</button></div></div><div class="gallery" id="gallery" tabindex="0" role="region" aria-label="Game screenshots">'
 for i,label in enumerate(t['galleryLabels'],1):gallery+=f'<figure><a href="{asset(f"screen-{i:02}.webp")}" aria-label="{E(u["view"]+": "+label)}"><img src="{asset(f"screen-{i:02}.webp")}" width="1536" height="2048" loading="lazy" alt="{E(t["imageAlts"][i-1])}"></a><figcaption>{i:02} — {E(label)}</figcaption></figure>'
 out+=section(gallery+f'</div><p class="gallery-help">{E(u["galleryHelp"])}</p>','screenshots')
 out+=section(heading('featuresHeading')+'<div class="features">'+''.join(f'<article><h3>{E(a)}</h3><p>{E(b)}</p></article>' for a,b in t['features'])+'</div>')
 out+=section(heading('faqHeading')+'<div class="faq">'+''.join(f'<details><summary>{E(a)}</summary><p>{E(b)}</p></details>' for a,b in t['faq'])+'</div>')
 out+='</div></div><div class="dark finale"><div class="wrap">'
 out+=f'''<section class="cta" id="download"><img src="{asset("main.png")}" width="1024" height="501" loading="lazy" alt="{E(u["promoAlt"])}"><div><h2>{E(t["downloadHeading"])}</h2><p>{E(t["downloadCopy"])}</p>{stores()}<p class="fine">{E(t["downloadNote"])}</p></div></section></div></main><footer class="footer wrap"><p>{E(u["footer"])}</p><div class="footer-links"><a href="{privacy_href}">{privacy_label}</a><a href="https://jmathstudio.com/">Jmath Studio</a></div></footer></div><dialog class="viewer" id="viewer" aria-labelledby="viewer-title" aria-describedby="viewer-caption"><div class="viewer-head"><h2 id="viewer-title">{E(u["screenshot"])}</h2><button id="close" autofocus>{E(u["close"])}</button></div><img id="viewer-image" alt=""><p id="viewer-caption"></p></dialog>
<dialog class="viewer language-dialog"
        id="language-dialog"
        aria-labelledby="language-heading">
  <div class="viewer-head">
    <h2 id="language-heading">{E(u["language"])}</h2>
    <button type="button" id="language-close">{E(u["close"])}</button>
  </div>
  <ul class="language-options">{language_links}</ul>
</dialog>
<script id="site-config" type="application/json">{json.dumps(runtime,ensure_ascii=False)}</script><script src="{prefix}app.js" defer></script></body></html>'''
 # Keep DOM nesting valid: the light/dark surface wrappers both belong inside main.
 out=out.replace('<div class="blueprint"><header','<main id="main"><div class="blueprint"><header').replace('</header><main id="main">','</header>').replace('</div></main><footer','</div><footer').replace('</footer></div><dialog','</footer></div></main><dialog')
 return out
D.mkdir(exist_ok=True)
for f in ['style.css','app.js']:shutil.copy2(R/'src'/f,D/f)

assets_src = R / 'assets'
assets_dst = D / 'assets'

if assets_dst.exists():
    shutil.rmtree(assets_dst)

shutil.copytree(assets_src, assets_dst)

(D/'index.html').write_text(page('en',True))
for l in enabled:
 p=D/l['code'];p.mkdir(exist_ok=True);(p/'index.html').write_text(page(l['code']))
(D/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{base}{l["code"]}/</loc></url>' for l in enabled)+'</urlset>')
# Publish the generated site to the LineToSplit root for GitHub Pages.
publish_items = [
    'index.html',
    'style.css',
    'app.js',
    'sitemap.xml',
    'assets',
    *[l['code'] for l in enabled],
]

for name in publish_items:
    src = D / name
    dst = R / name

    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()

    if src.is_dir():
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)

print('Built English root and /en/; inactive translations are not published or advertised in hreflang.')
