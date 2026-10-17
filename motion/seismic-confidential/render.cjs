// Usage: node render.cjs            -> renders video-silent.mp4 + cues.json
//        node render.cjs 2.4 5.6    -> writes preview/<t>.jpg for those times
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const out = f => path.resolve(__dirname, f);
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  p.on('console', m => console.log('console:', m.text()));
  await p.goto('file://' + out('scene.html') + '?r=1');
  await p.evaluate(() => window.ready);
  const grab = async t => { await p.evaluate(t => window.render(t), t); return p.screenshot({ type: 'jpeg', quality: 92 }); };
  const times = process.argv.slice(2).map(Number);
  if (times.length) {
    fs.mkdirSync(out('preview'), { recursive: true });
    for (const t of times) fs.writeFileSync(out(`preview/${t}.jpg`), await grab(t));
    await b.close(); return;
  }
  const { FPS, DUR, CUES } = await p.evaluate(() => ({ FPS: window.FPS, DUR: window.DUR, CUES: window.CUES }));
  fs.writeFileSync(out('cues.json'), JSON.stringify({ DUR, ...CUES }));
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'medium', out('video-silent.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const N = Math.round(FPS * DUR), t0 = Date.now();
  for (let f = 0; f < N; f++) {
    const buf = await grab(f / FPS);
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 300 === 0) console.log('frame', f, '/', N, ((Date.now() - t0) / 1000).toFixed(0) + 's');
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
