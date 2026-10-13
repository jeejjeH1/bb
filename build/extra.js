
/* ================= sound (Web Audio, only after the visitor opts in) ================= */
let SOUND = false, AC = null;
const sndBtn = $('#snd');
function setSound(on){
  SOUND = on;
  if(on && !AC){ try{ AC = new (window.AudioContext || window.webkitAudioContext)(); }catch(e){ SOUND = false; } }
  if(AC && AC.state === 'suspended') AC.resume();
  sndBtn.setAttribute('aria-pressed', SOUND); sndBtn.textContent = SOUND ? 'Sound on' : 'Sound off';
}
sndBtn.addEventListener('click', ()=>{ setSound(!SOUND); if(SOUND) sfx.tick(); });
function noiseBuf(d){ const b = AC.createBuffer(1, Math.floor(AC.sampleRate*d), AC.sampleRate), c = b.getChannelData(0); for(let i=0;i<c.length;i++) c[i] = Math.random()*2-1; return b; }
function out(v){ const g = AC.createGain(); g.gain.value = v; g.connect(AC.destination); return g; }
const sfx = {
  impact(){
    if(!SOUND || !AC) return; const t = AC.currentTime, m = out(.9);
    const o = AC.createOscillator(), g = AC.createGain();
    o.frequency.setValueAtTime(150, t); o.frequency.exponentialRampToValueAtTime(34, t+.5);
    g.gain.setValueAtTime(1, t); g.gain.exponentialRampToValueAtTime(.001, t+1.6); o.connect(g).connect(m); o.start(t); o.stop(t+1.7);
    const n = AC.createBufferSource(); n.buffer = noiseBuf(1.2);
    const f = AC.createBiquadFilter(); f.type = 'lowpass'; f.frequency.setValueAtTime(7000, t); f.frequency.exponentialRampToValueAtTime(200, t+.8);
    const ng = AC.createGain(); ng.gain.setValueAtTime(.6, t); ng.gain.exponentialRampToValueAtTime(.001, t+1); n.connect(f).connect(ng).connect(m); n.start(t);
    [174.6, 207.7, 261.6, 349.2].forEach(fr=>{
      const s = AC.createOscillator(), sg = AC.createGain(), lp = AC.createBiquadFilter();
      s.type = 'sawtooth'; s.frequency.value = fr; lp.type = 'lowpass';
      lp.frequency.setValueAtTime(3200, t); lp.frequency.exponentialRampToValueAtTime(300, t+.9);
      sg.gain.setValueAtTime(.07, t); sg.gain.exponentialRampToValueAtTime(.001, t+1.3); s.connect(lp).connect(sg).connect(m); s.start(t); s.stop(t+1.4);
    });
  },
  whoosh(){
    if(!SOUND || !AC) return; const t = AC.currentTime, m = out(.5);
    const n = AC.createBufferSource(); n.buffer = noiseBuf(.5);
    const f = AC.createBiquadFilter(); f.type = 'bandpass'; f.Q.value = 1.4;
    f.frequency.setValueAtTime(300, t); f.frequency.exponentialRampToValueAtTime(3200, t+.22); f.frequency.exponentialRampToValueAtTime(500, t+.45);
    const g = AC.createGain(); g.gain.setValueAtTime(.001, t); g.gain.exponentialRampToValueAtTime(1, t+.2); g.gain.exponentialRampToValueAtTime(.001, t+.48);
    n.connect(f).connect(g).connect(m); n.start(t);
  },
  crack(){
    if(!SOUND || !AC) return; const t = AC.currentTime, m = out(.6);
    for(let i=0;i<5;i++){ const n = AC.createBufferSource(); n.buffer = noiseBuf(.06); const f = AC.createBiquadFilter(); f.type='highpass'; f.frequency.value = 2500 + i*600;
      const g = AC.createGain(); const st = t + i*.035; g.gain.setValueAtTime(.8, st); g.gain.exponentialRampToValueAtTime(.001, st+.05); n.connect(f).connect(g).connect(m); n.start(st); }
  },
  glass(){
    if(!SOUND || !AC) return; const t = AC.currentTime, m = out(.45);
    for(let i=0;i<26;i++){ const o = AC.createOscillator(), g = AC.createGain(); o.type = 'triangle'; o.frequency.value = 2200 + Math.random()*5200;
      const st = t + Math.random()*.7; g.gain.setValueAtTime(.12, st); g.gain.exponentialRampToValueAtTime(.001, st+.12+Math.random()*.25); o.connect(g).connect(m); o.start(st); o.stop(st+.5); }
    const n = AC.createBufferSource(); n.buffer = noiseBuf(.9); const f = AC.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 3000;
    const g = AC.createGain(); g.gain.setValueAtTime(.5, t); g.gain.exponentialRampToValueAtTime(.001, t+.9); n.connect(f).connect(g).connect(m); n.start(t);
  },
  tick(){
    if(!SOUND || !AC) return; const t = AC.currentTime, o = AC.createOscillator(), g = AC.createGain();
    o.frequency.value = 2400; g.gain.setValueAtTime(.12, t); g.gain.exponentialRampToValueAtTime(.001, t+.06); o.connect(g).connect(out(1)); o.start(t); o.stop(t+.08);
  }
};

/* ================= scroll stage: zoom into the fist, crack, shatter, reveal ================= */
(function(){
  if(matchMedia('(prefers-reduced-motion:reduce)').matches) return;
  const stage = $('#top'), hero = $('#hero'), vid = hero.querySelector('video'), copy = hero.querySelector('.wrap'), hint = hero.querySelector('.scrollhint');
  const cv = $('#shatter'), g = cv.getContext('2d');
  const snap = document.createElement('canvas'), sg = snap.getContext('2d');
  const poster = new Image(); poster.src = 'assets/hero-poster.jpg';
  const ART_W = 1920, ART_H = 634, FIST_X = .795, FIST_Y = .70, ZOOM = 1.7;
  const C = (v,a=0,b=1)=>Math.min(b,Math.max(a,v)), sg_ = (p,a,b)=>C((p-a)/(b-a));
  const eio = t=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2, eo = t=>1-Math.pow(1-t,3);
  let Wd, Hd, dpr, fx, fy, box, shards = [], rings = [], state = 0, ticking = false;

  function layout(){
    dpr = Math.min(2, devicePixelRatio || 1); Wd = cv.clientWidth; Hd = cv.clientHeight;
    cv.width = snap.width = Math.round(Wd*dpr); cv.height = snap.height = Math.round(Hd*dpr);
    const bw = vid.offsetWidth, bh = vid.offsetHeight, s = Math.max(bw/ART_W, bh/ART_H), dw = ART_W*s, dh = ART_H*s;
    const posX = innerWidth <= 700 ? .78 : 1, ox = (bw-dw)*posX, oy = (bh-dh)*.5;
    box = {x: vid.offsetLeft + ox, y: vid.offsetTop + oy, w: dw, h: dh};
    fx = C(box.x + FIST_X*dw, Wd*.15, Wd*.85); fy = C(box.y + FIST_Y*dh, Hd*.2, Hd*.85);
    vid.style.setProperty('--fx', (fx - vid.offsetLeft) + 'px'); vid.style.setProperty('--fy', (fy - vid.offsetTop) + 'px');
    build();
  }
  function build(){
    let seed = 9; const r = ()=>((seed = (seed*1664525 + 1013904223) >>> 0) / 4294967296);
    const D = Math.hypot(Wd, Hd), R = [0, .035, .09, .17, .28, .42, .6, .85, 1.25].map(f=>f*D), n = 15;
    rings = R.map((rad,k)=>[...Array(n)].map((_,j)=>{ const a = (j + (k ? (r()-.5)*.6 : 0))/n*Math.PI*2, rr = k ? rad*(1+(r()-.5)*.25) : 0; return [fx + Math.cos(a)*rr, fy + Math.sin(a)*rr]; }));
    shards = [];
    for(let k=0;k<R.length-1;k++) for(let j=0;j<n;j++){
      const pts = [rings[k][j], rings[k+1][j], rings[k+1][(j+1)%n], rings[k][(j+1)%n]];
      const cx = pts.reduce((s,p)=>s+p[0],0)/4, cy = pts.reduce((s,p)=>s+p[1],0)/4, dx = cx-fx, dy = cy-fy, L = Math.hypot(dx,dy)||1;
      shards.push({pts, cx, cy, ux: dx/L, uy: dy/L, sp: (.35 + r()*.75)*D*(1 - k*.05), rot: (r()-.5)*2.6, del: k*.035 + r()*.04, lift: (r()-.3)*.3*D});
    }
  }
  function drawSnap(){
    const src = vid.readyState >= 2 ? vid : (poster.complete ? poster : null);
    sg.setTransform(dpr,0,0,dpr,0,0); sg.fillStyle = '#0b0a07'; sg.fillRect(0,0,Wd,Hd);
    if(src){ sg.save(); sg.translate(fx,fy); sg.scale(ZOOM,ZOOM); sg.translate(-fx,-fy); sg.drawImage(src, box.x, box.y, box.w, box.h); sg.restore(); }
    const gr = sg.createLinearGradient(0,0,Wd,0); gr.addColorStop(0,'rgba(11,10,7,.85)'); gr.addColorStop(.5,'rgba(11,10,7,.2)'); gr.addColorStop(1,'rgba(11,10,7,0)'); sg.fillStyle = gr; sg.fillRect(0,0,Wd,Hd);
  }
  function cracks(k){
    g.save(); g.lineJoin = 'round'; g.lineCap = 'round';
    g.shadowColor = '#ffc61a'; g.shadowBlur = 14; g.strokeStyle = 'rgba(255,252,235,.95)'; g.lineWidth = 2.2;
    const reach = k*Math.hypot(Wd,Hd)*.75;
    g.beginPath();
    for(let j=0;j<rings[0].length;j++){
      for(let q=0;q<rings.length-1;q++){
        const a = rings[q][j], b = rings[q+1][j], da = Math.hypot(a[0]-fx,a[1]-fy), db = Math.hypot(b[0]-fx,b[1]-fy);
        if(da > reach) break; const t = C((reach-da)/(db-da||1));
        g.moveTo(a[0],a[1]); g.lineTo(a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t);
      }
    }
    for(let q=1;q<rings.length-1;q++){
      const rad = Math.hypot(rings[q][0][0]-fx, rings[q][0][1]-fy); if(rad > reach*.8) break;
      for(let j=0;j<rings[q].length;j++){ const a = rings[q][j], b = rings[q][(j+1)%rings[q].length]; if((j*7+q)%3===0) continue; g.moveTo(a[0],a[1]); g.lineTo(b[0],b[1]); }
    }
    g.stroke();
    const glow = g.createRadialGradient(fx,fy,0,fx,fy,120+k*220); glow.addColorStop(0,`rgba(255,240,150,${.55*k})`); glow.addColorStop(1,'rgba(255,240,150,0)');
    g.shadowBlur = 0; g.fillStyle = glow; g.fillRect(0,0,Wd,Hd);
    g.restore();
  }
  function shatter(s){
    drawSnap();
    for(const sh of shards){
      const e = eo(sg_(s, sh.del, 1)), a = 1 - sg_(s, .5 + sh.del*.5, 1);
      if(a <= 0) continue;
      const tx = sh.ux*sh.sp*e, ty = sh.uy*sh.sp*e + (e*e)*.35*Hd - sh.lift*e;
      g.save(); g.globalAlpha = a;
      g.translate(sh.cx + tx, sh.cy + ty); g.rotate(sh.rot*e); const sc = 1 - .3*e; g.scale(sc, sc); g.translate(-sh.cx, -sh.cy);
      g.beginPath(); sh.pts.forEach((p,i)=>i?g.lineTo(p[0],p[1]):g.moveTo(p[0],p[1])); g.closePath();
      g.save(); g.clip(); g.drawImage(snap, 0, 0, Wd, Hd); g.restore();
      g.strokeStyle = 'rgba(255,214,90,.9)'; g.lineWidth = 2; g.stroke();
      g.restore();
    }
  }
  function frame(){
    ticking = false;
    const span = stage.offsetHeight - innerHeight, p = C(-stage.getBoundingClientRect().top / (span || 1));
    const z = eio(sg_(p, 0, .36));
    vid.style.transform = `scale(${1 + z*(ZOOM-1)})`;
    copy.style.transform = `translateX(${-z*80}vw) skewX(${-z*12}deg)`; copy.style.opacity = 1 - z*1.3;
    hint.style.opacity = 1 - z*4;
    g.setTransform(dpr,0,0,dpr,0,0); g.clearRect(0,0,Wd,Hd);
    const ck = sg_(p, .34, .46);
    if(p < .46){
      hero.style.visibility = '';
      if(ck > 0){ cracks(ck); const j = ck*7; hero.style.translate = `${(Math.random()-.5)*j}px ${(Math.random()-.5)*j}px`; } else hero.style.translate = '';
      if(ck > 0 && state < 1){ state = 1; sfx.crack(); }
      if(ck === 0) state = 0;
    } else {
      hero.style.visibility = 'hidden'; hero.style.translate = '';
      if(state < 2){ state = 2; flash(); sfx.impact(); sfx.glass(); }
      shatter(sg_(p, .46, .97));
    }
  }
  const req = ()=>{ if(!ticking){ ticking = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', req, {passive:true});
  addEventListener('resize', ()=>{ layout(); req(); });
  vid.addEventListener('loadeddata', ()=>{ layout(); req(); });
  layout(); req();
})();

/* ================= order form -> X ================= */
(function(){
  const opts = {
    'o-type': ['Explainer', 'Launch / promo', 'Announcement', 'Event recap', 'Something else'],
    'o-budget': ['Under $300', '$300–700', '$700–1,500', '$1,500+', "Let's talk"],
    'o-time': ['This week', '1–2 weeks', '2–4 weeks', 'Flexible']
  };
  Object.entries(opts).forEach(([id, list])=>{
    $('#'+id).innerHTML = list.map((v,i)=>`<input type="radio" name="${id}" id="${id}-${i}" value="${esc(v)}"><label for="${id}-${i}">${esc(v)}</label>`).join('');
  });
  const form = $('#brief'), prev = $('#f-prev'), err = $('#f-err');
  const pick = n => { const el = form.querySelector(`[name="${n}"]:checked`); return el ? el.value : ''; };
  const f = k => form.elements[k].value.trim();
  const msg = () => ['Hey Master! Project brief from your site:', '',
    `From: ${f('name') || '-'}`, `Project: ${f('proj') || '-'}`, `Need: ${pick('o-type') || '-'}`,
    `Budget: ${pick('o-budget') || '-'}`, `Timeline: ${pick('o-time') || '-'}`, '', f('about') || '-'].join('\n');
  const upd = () => { prev.textContent = msg(); };
  form.addEventListener('input', upd); form.addEventListener('change', ()=>{ upd(); sfx.tick(); }); upd();
  function toast(t){ const el = $('#toast'); el.textContent = t; el.classList.add('on'); clearTimeout(el._t); el._t = setTimeout(()=>el.classList.remove('on'), 5000); }
  function check(){
    if(!pick('o-type') || !f('about')){ err.textContent = 'Pick what you need and write a line about the project, then send.'; return false; }
    err.textContent = ''; return true;
  }
  form.addEventListener('submit', e=>{
    e.preventDefault(); if(!check()) return;
    const m = msg();
    const copied = navigator.clipboard ? navigator.clipboard.writeText(m) : Promise.reject();
    copied.then(()=>toast('Brief copied. On my X profile, tap Message and paste it.'))
      .catch(()=>{ const r = document.createRange(); r.selectNodeContents(prev); const s = getSelection(); s.removeAllRanges(); s.addRange(r);
        toast('Copy the highlighted brief, then tap Message on my X profile.'); });
    window.open('https://x.com/0xMASTER82', '_blank', 'noopener');
    sfx.tick();
  });
  $('#f-post').addEventListener('click', ()=>{
    if(!check()) return;
    const t = `@0xMASTER82 I'd like a motion graphic: ${pick('o-type')}, budget ${pick('o-budget') || 'TBD'}, timeline ${pick('o-time') || 'flexible'}. ${f('about')}`.slice(0, 275);
    window.open('https://x.com/intent/post?text=' + encodeURIComponent(t), '_blank', 'noopener');
  });
})();
