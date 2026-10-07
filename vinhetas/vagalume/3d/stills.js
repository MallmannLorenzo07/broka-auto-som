// renders 3D "limpos" (sem textos) em momentos escolhidos: node stills.js pagina.html t1,t2,...
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [,,html,ts]=process.argv;
(async()=>{
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1.2});
 await p.goto('file://'+html,{waitUntil:'networkidle'}); await p.waitForFunction(()=>window.__ready);
 await p.addStyleTag({content:'.cena,#cap,#marca,#grao,#flash{display:none!important}#preto{opacity:0!important}'});
 for(const t of ts.split(',').map(Number)){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:require('path').dirname(html)+`/still_${t}.png`});}
 await b.close();
})();
