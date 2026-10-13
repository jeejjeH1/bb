// Usage: node render.cjs            -> renders assets/master-intro-video.mp4 (silent)
//        node render.cjs 2.4 5.6    -> writes preview PNGs for those times
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  p.on('console', m => console.log('console:', m.text()));
  await p.goto('file://' + path.resolve(__dirname, 'scene.html'));
  await p.evaluate(() => window.ready);
  const grab = t => p.evaluate(t => { window.render(t); return document.getElementById('out').toDataURL('image/jpeg', .93).split(',')[1]; }, t);
  const times = process.argv.slice(2).map(Number);
  if (times.length) {
    fs.mkdirSync(path.resolve(__dirname, 'preview'), { recursive: true });
    for (const t of times) fs.writeFileSync(path.resolve(__dirname, `preview/${t}.jpg`), Buffer.from(await grab(t), 'base64'));
    await b.close(); return;
  }
  const { FPS, DUR } = await p.evaluate(() => ({ FPS: window.FPS, DUR: window.DUR }));
  const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-preset', 'medium',
    path.resolve(__dirname, 'video-silent.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let f = 0; f < FPS * DUR; f++) {
    const buf = Buffer.from(await grab(f / FPS), 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 60 === 0) console.log('frame', f);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await b.close();
})();
