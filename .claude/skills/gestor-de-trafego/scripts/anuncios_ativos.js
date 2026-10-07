// Captura anúncios ativos públicos: Biblioteca de Anúncios do Meta + Central de Transparência do Google.
// Uso: node anuncios_ativos.js --meta "Marcelo Munhoz" --dominio marcelomunhoz.com.br --saida ./saida
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const META_Q = arg('--meta');
const DOMINIO = arg('--dominio');
const SAIDA = arg('--saida', './saida');
fs.mkdirSync(SAIDA, { recursive: true });

async function rolar(page, vezes = 12) {
  for (let i = 0; i < vezes; i++) {
    await page.mouse.wheel(0, 4000);
    await page.waitForTimeout(1200);
  }
}

async function aceitarCookies(page) {
  for (const txt of ['Permitir todos os cookies', 'Allow all cookies', 'Aceitar tudo', 'Accept all']) {
    const b = page.getByRole('button', { name: txt });
    if (await b.count()) { await b.first().click().catch(() => {}); await page.waitForTimeout(800); return; }
  }
}

async function meta(browser) {
  const page = await browser.newPage({ locale: 'pt-BR', viewport: { width: 1400, height: 1000 } });
  const url = 'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=BR'
    + '&media_type=all&search_type=keyword_unordered&q=' + encodeURIComponent(META_Q);
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await aceitarCookies(page);
  await page.waitForTimeout(5000);
  await rolar(page);
  await page.screenshot({ path: path.join(SAIDA, 'meta.png'), fullPage: true });
  const texto = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync(path.join(SAIDA, 'meta.txt'), url + '\n\n' + texto);
  console.log('Meta: ok →', path.join(SAIDA, 'meta.txt'));
}

async function google(browser) {
  const page = await browser.newPage({ locale: 'pt-BR', viewport: { width: 1400, height: 1000 } });
  const url = `https://adstransparency.google.com/?region=BR&domain=${DOMINIO}`;
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await aceitarCookies(page);
  await page.waitForTimeout(4000);
  await rolar(page, 6);
  await page.screenshot({ path: path.join(SAIDA, 'google.png'), fullPage: true });
  const texto = await page.evaluate(() => document.body.innerText);
  let links = await page.$$eval('a[href*="/creative/"]', as => [...new Set(as.map(a => a.href))]);
  // a busca por domínio mostra só uma prévia: abre a página de cada anunciante para pegar todos os criativos
  const anunciantes = [...new Set(links.map(l => (l.match(/advertiser\/(AR\d+)/) || [])[1]).filter(Boolean))];
  for (const ar of anunciantes) {
    await page.goto(`https://adstransparency.google.com/advertiser/${ar}?region=BR`, { waitUntil: 'load', timeout: 90000 });
    await page.waitForTimeout(6000);
    await rolar(page, 10);
    links = [...new Set([...links, ...await page.$$eval('a[href*="/creative/"]', as => as.map(a => a.href))])];
  }
  fs.writeFileSync(path.join(SAIDA, 'google.txt'), url + '\n\n' + texto + '\n\nCRIATIVOS:\n' + links.join('\n'));
  // abre os primeiros criativos para capturar texto/formato de cada um
  for (const [i, l] of links.slice(0, 40).entries()) {
    const p = await browser.newPage({ locale: 'pt-BR', viewport: { width: 1200, height: 900 } });
    await p.goto(l, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => {});
    await p.waitForTimeout(3000);
    await p.screenshot({ path: path.join(SAIDA, `google_criativo_${i + 1}.png`), fullPage: true });
    fs.appendFileSync(path.join(SAIDA, 'google.txt'), `\n\n=== ${l}\n` + await p.evaluate(() => document.body.innerText));
    await p.close();
  }
  console.log('Google: ok →', path.join(SAIDA, 'google.txt'), `(${links.length} criativos)`);
}

(async () => {
  const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  try {
    if (META_Q) await meta(browser).catch(e => console.error('Meta falhou:', e.message));
    if (DOMINIO) await google(browser).catch(e => console.error('Google falhou:', e.message));
  } finally { await browser.close(); }
})();
