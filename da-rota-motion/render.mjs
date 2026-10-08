// Renderiza o motion quadro a quadro com Chromium (Playwright) e monta o MP4 com ffmpeg.
// Uso:
//   node render.mjs                       -> da-rota-motion.mp4 (30 fps, com trilha)
//   node render.mjs --stills 1,3,4.5 out/ -> PNGs dos instantes indicados (conferência)
import { createRequire } from 'node:module';
import { spawn, execSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';
import path from 'node:path';
import fs from 'node:fs';

const require = createRequire(import.meta.url);
let playwright;
try { playwright = require('playwright'); }
catch { playwright = require(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }

const dir = path.dirname(fileURLToPath(import.meta.url));
const FPS = 30, W = 1080, H = 1920;
const args = process.argv.slice(2);

const browser = await playwright.chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
await page.goto(pathToFileURL(path.join(dir, 'index.html')).href + '?render=1');
await page.evaluate(() => window.ready);
const DUR = await page.evaluate(() => window.__DUR);

if (args[0] === '--stills') {
  const out = args[2] || path.join(dir, 'stills');
  fs.mkdirSync(out, { recursive: true });
  for (const t of args[1].split(',').map(Number)) {
    await page.evaluate(t => window.seek(t), t);
    await page.screenshot({ path: path.join(out, `t${t.toFixed(2).padStart(5, '0')}.png`) });
  }
} else {
  const outFile = path.join(dir, 'da-rota-motion.mp4');
  const audio = ['mix.wav', 'trilha.wav', 'mix.mp3', 'trilha.mp3'].map(f => path.join(dir, 'assets', f)).find(f => fs.existsSync(f)) || '';
  const ff = spawn('ffmpeg', [
    '-y', '-loglevel', 'error',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    ...(fs.existsSync(audio) ? ['-i', audio] : []),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS),
    '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', outFile,
  ], { stdio: ['pipe', 'inherit', 'inherit'] });
  const total = Math.round(DUR * FPS);
  for (let f = 0; f < total; f++) {
    await page.evaluate(t => window.seek(t), f / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 60 === 0) process.stdout.write(`quadro ${f}/${total}\n`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('ok ->', outFile);
}
await browser.close();
