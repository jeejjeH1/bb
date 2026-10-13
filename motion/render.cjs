const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const FPS = 30, DUR = 10;
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1280, height: 720 } });
  p.on('pageerror', e => console.error('PAGEERR', e.message));
  await p.goto('file://' + path.resolve(__dirname, 'scene.html'));
  await p.evaluate(() => window.ready);
  const ff = spawn('ffmpeg', ['-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'medium', '-movflags', '+faststart',
    path.resolve(__dirname, '../assets/master-intro.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
  const el = await p.$('#c');
  for (let f = 0; f < FPS * DUR; f++) {
    await p.evaluate(t => window.draw(t), f / FPS);
    const buf = await el.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await p.evaluate(() => window.draw(1.8)); await el.screenshot({ path: path.resolve(__dirname, 's1.png') });
  for (const [n, t] of [['s2', 2.4], ['s3', 4.4], ['s4', 6.0], ['s5', 8.8]]) { await p.evaluate(t => window.draw(t), t); await el.screenshot({ path: path.resolve(__dirname, n + '.png') }); }
  await b.close();
})();
