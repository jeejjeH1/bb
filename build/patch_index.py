"""One-off patch: turns index.html into build/index.template.html with the new features."""
import re
s = open('/home/user/portfolio/build/index.backup.html').read()
def rep(a, b, cnt=1):
    global s
    assert a in s, 'MISSING: ' + a[:80]
    s = s.replace(a, b, cnt)

# ---------------- CSS ----------------
rep("@media(prefers-reduced-motion:reduce){\n  *{animation:none", r'''/* ===== v3: gate, scroll stage, posters, cinema player, order form ===== */
#pre .gate{position:relative;z-index:4;display:flex;flex-direction:column;align-items:center;gap:14px;margin-top:26px;opacity:0;transform:translateY(20px);transition:opacity .4s,transform .4s;pointer-events:none}
#pre.can .gate{opacity:1;transform:none;pointer-events:auto}
#pre.can .cnt{opacity:0}
.enter{font-family:var(--f-display);font-size:clamp(30px,5vw,54px);letter-spacing:.06em;text-transform:uppercase;background:var(--gold);color:var(--ink);border:0;padding:16px 46px;cursor:pointer;clip-path:polygon(14px 0,100% 0,calc(100% - 14px) 100%,0 100%);animation:beat 1s ease-in-out infinite}
.enter:hover{background:var(--gold-hi)}
@keyframes beat{0%,100%{transform:scale(1)}12%{transform:scale(1.07)}24%{transform:scale(1)}}
.mute{background:none;border:0;color:var(--mute);font-family:var(--f-mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;cursor:pointer;text-decoration:underline;text-underline-offset:4px}
.sndbtn{background:transparent;border:2px solid #3a3522;color:var(--paper);font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;padding:8px 10px;cursor:pointer;text-transform:uppercase}
.sndbtn[aria-pressed="true"]{border-color:var(--gold);color:var(--gold)}

.stage{position:relative;height:250vh}
.stage .sticky{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;isolation:isolate}
.stage .hero{height:100%;min-height:0;max-height:none;aspect-ratio:auto;will-change:transform}
video.hero-art{width:100%;height:100%;object-fit:cover;object-position:right center;background:var(--ink);animation:none;transform-origin:var(--fx,80%) var(--fy,70%)}
.behind{position:absolute;inset:0;z-index:-5;background:var(--gold);display:grid;place-items:center;overflow:hidden;color:var(--ink)}
.behind::before{content:"";position:absolute;inset:-50%;background:repeating-conic-gradient(from 0deg at 50% 50%,transparent 0 5deg,rgba(11,10,7,.12) 5deg 6deg);animation:spin 50s linear infinite}
.behind::after{content:"";position:absolute;inset:0;background:radial-gradient(circle,rgba(11,10,7,.22) 1.6px,transparent 1.9px) 0 0/16px 16px}
.behind .bt{position:relative;z-index:1;text-align:center;transform:skewX(-8deg)}
.behind h2{font-family:var(--f-display);font-weight:400;font-size:clamp(70px,16vw,240px);line-height:.85;margin:0;text-transform:uppercase;text-shadow:6px 6px 0 var(--paper)}
.behind p{margin:18px 0 0}
#shatter{position:absolute;inset:0;width:100%;height:100%;z-index:6;pointer-events:none}
.scrollhint{position:absolute;left:50%;bottom:22px;transform:translateX(-50%);z-index:5;color:var(--gold);display:flex;flex-direction:column;align-items:center;gap:6px;animation:bob 1.6s ease-in-out infinite}
@keyframes bob{50%{transform:translate(-50%,8px)}}
@media(max-width:700px){
  .stage{height:210vh}
  video.hero-art{position:absolute;inset:0 0 auto 0;height:68%;object-position:78% center}
  .scrollhint{display:none}
}

.card .frame img,.card .frame video{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.card .frame video{opacity:0;transition:opacity .3s}
.card.playing .frame video{opacity:1}
.card .frame img{filter:saturate(.75) brightness(.85);transition:filter .35s,transform .6s}
.card:hover .frame img{filter:none;transform:scale(1.05)}
.card .sum{margin:2px 0 0;color:var(--mute);font-size:14px;line-height:1.45;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}

/* cinema player */
.wipe{position:fixed;inset:0;z-index:150;pointer-events:none}
.wipe i{position:absolute;left:-20%;width:140%;height:52%;transform:translateX(-120%) skewX(-18deg)}
.wipe i:nth-child(1){top:0;background:var(--gold)}
.wipe i:nth-child(2){bottom:0;background:var(--ink);border-top:6px solid var(--gold)}
.wipe.in i{animation:wIn .32s cubic-bezier(.7,0,.2,1) forwards}
.wipe.in i:nth-child(2){animation-delay:.05s}
.wipe.out i{transform:translateX(0) skewX(-18deg);animation:wOut .45s cubic-bezier(.7,0,.2,1) forwards}
.wipe.out i:nth-child(2){animation-delay:.06s}
@keyframes wIn{to{transform:translateX(0) skewX(-18deg)}}
@keyframes wOut{to{transform:translateX(120%) skewX(-18deg)}}
dialog#dlg{width:min(1180px,calc(100% - 24px))}
.dlg .bar{align-items:flex-start}
.dlg .info{min-width:0;flex:1 1 320px}
.dlg .brand{color:var(--gold);margin-bottom:6px}
.dlg .dsum{margin:8px 0 0;color:#e6dfc9;font-size:15px;max-width:70ch}
.dlg .nav2{display:flex;gap:8px}
.dlg .nav2 button{font-family:var(--f-display);font-size:22px;width:48px;height:44px;background:transparent;color:var(--gold);border:2px solid var(--gold);cursor:pointer}
.dlg .nav2 button:hover{background:var(--gold);color:var(--ink)}
.dlg .count{color:var(--mute);align-self:center}

/* order form */
.order{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.2fr);gap:clamp(28px,5vw,70px);align-items:start;margin-top:40px}
.order .pitch p{color:#e6dfc9;font-size:18px;max-width:42ch;margin:0 0 18px}
.order .pitch ol{margin:0;padding:0;list-style:none;display:grid;gap:12px;counter-reset:s}
.order .pitch li{display:flex;gap:14px;align-items:baseline;color:var(--paper)}
.order .pitch li::before{counter-increment:s;content:counter(s,decimal-leading-zero);font-family:var(--f-display);color:var(--gold);font-size:26px}
form.brief{background:var(--ink-2);border:2px solid var(--line);padding:clamp(18px,3vw,30px);display:grid;gap:18px;box-shadow:10px 10px 0 var(--gold)}
.fld{display:grid;gap:8px;min-width:0}
.fld>label,.fld>legend{font-family:var(--f-mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);padding:0}
fieldset.fld{border:0;margin:0;padding:0}
.fld input,.fld textarea{font:inherit;color:var(--paper);background:var(--ink);border:2px solid #3a3522;padding:12px 14px;width:100%;transition:border-color .2s}
.fld input:focus,.fld textarea:focus{outline:none;border-color:var(--gold)}
.fld textarea{min-height:110px;resize:vertical}
.opts{display:flex;flex-wrap:wrap;gap:8px}
.opts input{position:absolute;opacity:0;pointer-events:none}
.opts label{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;text-transform:uppercase;border:2px solid #3a3522;padding:9px 12px;cursor:pointer;transition:.2s}
.opts input:checked+label{background:var(--gold);border-color:var(--gold);color:var(--ink)}
.opts input:focus-visible+label{outline:3px solid var(--gold);outline-offset:2px}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.err{color:#ff6b6b;font-size:14px;min-height:1em;margin:0}
.preview{font-family:var(--f-mono);font-size:12px;white-space:pre-wrap;background:var(--ink);border:2px dashed #3a3522;padding:12px;color:var(--mute);max-height:180px;overflow:auto}
.sendrow{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
.toast{position:fixed;left:50%;bottom:calc(24px + env(safe-area-inset-bottom,0px));transform:translate(-50%,140%);z-index:160;background:var(--gold);color:var(--ink);font-weight:800;padding:14px 20px;max-width:calc(100% - 32px);transition:transform .35s cubic-bezier(.2,.9,.2,1);box-shadow:6px 6px 0 #000}
.toast.on{transform:translate(-50%,0)}
@media(max-width:800px){.order{grid-template-columns:1fr}.row2{grid-template-columns:1fr}}

@media(prefers-reduced-motion:reduce){
  .stage{height:auto}.stage .sticky{position:relative;height:auto;min-height:620px}
  *{animation:none''')

# ---------------- HTML ----------------
rep('<div class="mid"><h2>Master</h2><div class="cnt" id="cnt">0</div></div>',
    '<div class="mid"><h2>Master</h2><div class="cnt" id="cnt">0</div>\n    <div class="gate"><button class="enter" id="enter" type="button">Enter</button><button class="mute" id="enterQuiet" type="button">Enter without sound</button></div></div>')
rep('<div id="pre" aria-hidden="true">', '<div id="pre">')
rep('<noscript>', '<noscript>') if '<noscript>' in s else None
rep('<body>\n', '<body>\n<noscript><style>#pre{display:none}</style></noscript>\n')
rep('''      <a class="btn" href="https://x.com/0xMASTER82" target="_blank" rel="noopener">Follow on X</a>
    </div>''', '''      <a href="#order">Hire me</a>
      <button class="sndbtn" id="snd" type="button" aria-pressed="false">Sound off</button>
      <a class="btn" href="https://x.com/0xMASTER82" target="_blank" rel="noopener">Follow on X</a>
    </div>''')
rep('''<header class="hero" id="top">
  <div class="hero-art"></div>''', '''<section class="stage" id="top">
<div class="sticky">
<div class="behind" aria-hidden="true"><div class="bt"><h2>All my<br>works</h2><p class="mono">25 motion pieces · keep scrolling</p></div></div>
<header class="hero" id="hero">
  <video class="hero-art" autoplay muted loop playsinline preload="auto" poster="assets/hero-poster.jpg" aria-hidden="true">
    <source src="assets/hero-loop.webm" type="video/webm">
    <source src="assets/hero-loop.mp4" type="video/mp4">
  </video>''')
rep('''    <div class="stats" id="stats"></div>
  </div>
</header>''', '''    <div class="stats" id="stats"></div>
  </div>
  <div class="scrollhint mono" aria-hidden="true">Scroll<span>↓</span></div>
</header>
<canvas id="shatter" aria-hidden="true"></canvas>
</div>
</section>''')
rep('''    <h2 class="disp">Let's <em>build.</em></h2>
    <div class="handle">
      <span class="at">@0xMASTER82</span>
      <a class="btn" href="https://x.com/0xMASTER82" target="_blank" rel="noopener">Message me on X</a>
      <a class="btn ghost" href="https://github.com/jeejjeH1" target="_blank" rel="noopener">GitHub</a>
    </div>
  </div>''', '''    <h2 class="disp">Let's <em>build.</em></h2>
    <div class="order" id="order">
      <div class="pitch">
        <p>Tell me about your project in under a minute. The form turns your answers into a message for my X DMs.</p>
        <ol>
          <li>Fill in the brief</li>
          <li>Tap “Send on X”: the message is copied and my X profile opens</li>
          <li>Tap Message on my profile and paste</li>
        </ol>
        <div class="handle" style="margin-top:28px">
          <span class="at">@0xMASTER82</span>
          <a class="btn ghost" href="https://github.com/jeejjeH1" target="_blank" rel="noopener">GitHub</a>
        </div>
      </div>
      <form class="brief" id="brief" novalidate>
        <div class="row2">
          <div class="fld"><label for="f-name">Your name or @handle</label><input id="f-name" name="name" autocomplete="nickname" placeholder="@yourproject"></div>
          <div class="fld"><label for="f-proj">Project / brand</label><input id="f-proj" name="proj" placeholder="e.g. GenLayer"></div>
        </div>
        <fieldset class="fld"><legend>What do you need?</legend><div class="opts" id="o-type"></div></fieldset>
        <div class="fld"><label for="f-about">What's the project about?</label><textarea id="f-about" name="about" placeholder="The post or launch this video is for, key message, any links"></textarea></div>
        <fieldset class="fld"><legend>Budget</legend><div class="opts" id="o-budget"></div></fieldset>
        <fieldset class="fld"><legend>Timeline</legend><div class="opts" id="o-time"></div></fieldset>
        <p class="err" id="f-err" role="alert"></p>
        <div class="preview" id="f-prev" aria-live="polite"></div>
        <div class="sendrow">
          <button class="btn" type="submit" id="f-send">Send on X</button>
          <button class="btn ghost" type="button" id="f-post">Post it publicly</button>
        </div>
      </form>
    </div>
  </div>''')
rep('''    <video id="dv" controls playsinline></video>
    <div class="bar">
      <h3 id="dt"></h3>
      <div class="acts">
        <a class="btn ghost" id="dsrc" href="#" target="_blank" rel="noopener">Source code</a>
        <button class="btn" id="dx" type="button">Close</button>
      </div>
    </div>''', '''    <video id="dv" controls playsinline></video>
    <div class="bar">
      <div class="info"><div class="brand mono" id="db"></div><h3 id="dt"></h3><p class="dsum" id="ds"></p></div>
      <div class="acts">
        <div class="nav2"><button type="button" id="dp" aria-label="Previous work">←</button><span class="count mono" id="dc"></span><button type="button" id="dn" aria-label="Next work">→</button></div>
        <a class="btn" id="dpage" href="#">Project page</a>
        <a class="btn ghost" id="dsrc" href="#" target="_blank" rel="noopener">Source</a>
        <button class="btn ghost" id="dx" type="button">Close</button>
      </div>
    </div>''')
rep('<footer>', '<div class="wipe" id="wipe" aria-hidden="true"><i></i><i></i></div>\n<div class="toast" id="toast" role="status"></div>\n<footer>')

# ---------------- JS ----------------
s = re.sub(r'const W = \(title.*?\n\];\n', 'const WORKS = /*@WORKS@*/[];\n', s, flags=re.S)
rep("/* ===== YOUR WORKS. Each video plays straight from its GitHub repo. ===== */",
    "/* ===== WORKS: generated by build/build.py from build/works.json. Full videos stream from GitHub. ===== */")
rep('''    <div class="frame">
      <video muted loop playsinline preload="none" data-src="${esc(url(w))}"></video>''', '''    <div class="frame">
      <img src="assets/works/${w.slug}.jpg" alt="" loading="lazy" decoding="async" width="640" height="360">
      <video muted loop playsinline preload="none" data-src="assets/works/${w.slug}.mp4"></video>''')
rep('''      <h3>${esc(w.title)}</h3>
      <div class="meta mono"><span>${esc(w.brand)}</span><span>${w.mb} MB</span></div>''', '''      <h3>${esc(w.title)}</h3>
      <p class="sum">${esc(w.sum)}</p>
      <div class="meta mono"><span>${esc(w.brand)}</span><span>${w.len}</span></div>''')
rep('''// lazy first-frame thumbnails: only load videos near the viewport
const vio = 'IntersectionObserver' in window ? new IntersectionObserver(es=>es.forEach(e=>{
  if(!e.isIntersecting) return;
  const v = e.target; v.preload = 'metadata'; v.src = v.dataset.src + '#t=1.5'; vio.unobserve(v);
}),{rootMargin:'300px'}) : null;
document.querySelectorAll('video[data-src]').forEach(v=>{ if(vio) vio.observe(v); });

// hover preview
document.querySelectorAll('.card, .reel:not(.intro)').forEach(c=>{
  const v = c.querySelector('video');
  c.addEventListener('pointerenter', e=>{ if(e.pointerType==='mouse' && v.src){ v.play().catch(()=>{}); } });
  c.addEventListener('pointerleave', ()=>{ v.pause(); });
});''', '''// light 3s previews: on hover with a mouse, or when a card sits in the middle of a phone screen
function preview(card, on){
  const v = card.querySelector('video'); if(!v) return;
  if(on){ if(!v.src) v.src = v.dataset.src; v.play().then(()=>card.classList.add('playing')).catch(()=>{}); }
  else { v.pause(); card.classList.remove('playing'); }
}
grid.querySelectorAll('.card').forEach(c=>{
  c.addEventListener('pointerenter', e=>{ if(e.pointerType==='mouse') preview(c,true); });
  c.addEventListener('pointerleave', e=>{ if(e.pointerType==='mouse') preview(c,false); });
});
if(!matchMedia('(pointer:fine)').matches && 'IntersectionObserver' in window){
  const pio = new IntersectionObserver(es=>es.forEach(e=>preview(e.target, e.isIntersecting)),{rootMargin:'-35% 0px -35% 0px'});
  grid.querySelectorAll('.card').forEach(c=>pio.observe(c));
}''')
rep('''// modal player
const dlg = $('#dlg'), dv = $('#dv');
function open(w){
  $('#dt').textContent = w.title;
  $('#dsrc').href = repoUrl(w);
  dv.src = url(w);
  if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open','');
  dv.play().catch(()=>{});
}
function close(){ dv.pause(); dv.removeAttribute('src'); dv.load(); if(dlg.close) dlg.close(); else dlg.removeAttribute('open'); }
grid.addEventListener('click', e=>{ const c=e.target.closest('.card'); if(c) open(WORKS[+c.dataset.i]); });''', '''// cinema player: a slanted wipe covers the page, the player opens behind it, the wipe leaves
const dlg = $('#dlg'), dv = $('#dv'), wipe = $('#wipe');
let cur = -1;
const visibleIdx = () => [...grid.querySelectorAll('.card:not(.hide)')].map(c=>+c.dataset.i);
function fill_(w, i){
  $('#dt').textContent = w.title; $('#db').textContent = w.brand + (w.len ? ' · ' + w.len : '');
  $('#ds').textContent = w.sum || ''; $('#dsrc').href = repoUrl(w);
  const page = $('#dpage'); page.hidden = !w.slug; if(w.slug) page.href = 'work/' + w.slug + '/';
  const nav = dlg.querySelector('.nav2'); nav.hidden = i < 0;
  if(i >= 0){ const vi = visibleIdx(); $('#dc').textContent = `${vi.indexOf(i)+1} / ${vi.length}`; }
  dv.poster = w.slug ? 'assets/works/' + w.slug + '.jpg' : 'assets/hero-poster.jpg';
  dv.src = url(w); dv.play().catch(()=>{});
}
function runWipe(mid){
  if(RM_){ mid(); return; }
  wipe.className = 'wipe in'; sfx.whoosh();
  setTimeout(()=>{ mid(); wipe.className = 'wipe out'; setTimeout(()=>{ wipe.className = 'wipe'; }, 520); }, 340);
}
const RM_ = matchMedia('(prefers-reduced-motion:reduce)').matches;
function open(w, i=-1){
  cur = i;
  runWipe(()=>{ fill_(w, i); if(!dlg.open){ if(dlg.showModal) dlg.showModal(); else dlg.setAttribute('open',''); } });
}
function step(d){
  if(cur < 0) return; const vi = visibleIdx(); const k = (vi.indexOf(cur) + d + vi.length) % vi.length;
  cur = vi[k]; runWipe(()=>fill_(WORKS[cur], cur));
}
function close(){ dv.pause(); dv.removeAttribute('src'); dv.load(); if(dlg.close) dlg.close(); else dlg.removeAttribute('open'); }
grid.addEventListener('click', e=>{ const c=e.target.closest('.card'); if(c) open(WORKS[+c.dataset.i], +c.dataset.i); });
$('#dp').addEventListener('click', ()=>step(-1));
$('#dn').addEventListener('click', ()=>step(1));
dlg.addEventListener('keydown', e=>{ if(e.key==='ArrowRight'){ e.preventDefault(); step(1); } if(e.key==='ArrowLeft'){ e.preventDefault(); step(-1); } });
(function(){ let x0=null,y0=0; dlg.addEventListener('touchstart',e=>{x0=e.touches[0].clientX;y0=e.touches[0].clientY;},{passive:true});
  dlg.addEventListener('touchend',e=>{ if(x0===null) return; const dx=e.changedTouches[0].clientX-x0, dy=e.changedTouches[0].clientY-y0; if(Math.abs(dx)>70 && Math.abs(dx)>Math.abs(dy)*1.5) step(dx<0?1:-1); x0=null; }); })();''')

# preloader becomes a gate with sound
rep('''  const go = () => { document.body.classList.add('ready'); document.body.classList.remove('lock'); pre.classList.add('done'); setTimeout(()=>pre.remove(),1300); scramble(document.querySelector('.hero .tag b')); };''',
'''  const go = (withSound) => { if(withSound){ setSound(true); sfx.impact(); } document.body.classList.add('ready'); document.body.classList.remove('lock'); pre.classList.add('done'); flash(); setTimeout(()=>pre.remove(),1300); scramble(document.querySelector('.hero .tag b')); };
  const gate = () => { pre.classList.add('can'); setTimeout(()=>$('#enter').focus({preventScroll:true}),50); };
  $('#enter').addEventListener('click', ()=>go(true));
  $('#enterQuiet').addEventListener('click', ()=>go(false));''')
rep('''    if(p<1) requestAnimationFrame(tick); else if(!fin){ fin=true; go(); }
  })(t0);
  setTimeout(()=>{ if(!fin){ fin=true; go(); } }, 3500); // fail-safe''', '''    if(p<1) requestAnimationFrame(tick); else if(!fin){ fin=true; gate(); }
  })(t0);
  setTimeout(()=>{ if(!fin){ fin=true; gate(); } }, 3000); // fail-safe''')

rep("  if(scrollY<innerHeight) art.style.transform = `translateY(${scrollY*.15}px)`;\n", '')
# sound engine + scroll stage + order form appended before the closing script
EXTRA = open('/home/user/portfolio/build/extra.js').read()
i = s.rfind('</script>')
s = s[:i] + EXTRA + '\n' + s[i:]
open('/home/user/portfolio/build/index.template.html', 'w').write(s)
print('ok')
