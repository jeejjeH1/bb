// node render-hero.cjs  -> ../assets/hero-loop.mp4 + .webm (seamless 6s loop)
const { chromium } = require('/opt/node-tools/node_modules/playwright');
const { spawnSync } = require('child_process');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.resolve(__dirname, 'hero-frames'); fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 634 } });
  await p.goto('file://' + path.resolve(__dirname, 'hero-loop.html'));
  await p.evaluate(() => window.ready);
  const FPS = 30, N = 180;
  for (let f = 0; f < N; f++) {
    const d = await p.evaluate(t => { window.render(t); return document.getElementById('c').toDataURL('image/jpeg', .94).split(',')[1]; }, f / FPS);
    fs.writeFileSync(`${dir}/${String(f).padStart(3, '0')}.jpg`, Buffer.from(d, 'base64'));
  }
  await b.close();
  const out = path.resolve(__dirname, '../assets/hero-loop');
  spawnSync('ffmpeg', ['-y', '-v', 'error', '-framerate', '30', '-i', `${dir}/%03d.jpg`, '-c:v', 'libx264', '-preset', 'slow', '-crf', '24', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out + '.mp4'], { stdio: 'inherit' });
  spawnSync('ffmpeg', ['-y', '-v', 'error', '-framerate', '30', '-i', `${dir}/%03d.jpg`, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '36', '-row-mt', '1', out + '.webm'], { stdio: 'inherit' });
  spawnSync('cp', [`${dir}/000.jpg`, path.resolve(__dirname, '../assets/hero-poster.jpg')]);
  fs.rmSync(dir, { recursive: true, force: true });
})();
