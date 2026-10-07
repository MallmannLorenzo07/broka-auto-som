// node fotografa.js fotos.html saida_dir [0,1,2...]
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const [,,html,out,lista]=process.argv; const fs=require('fs'); fs.mkdirSync(out,{recursive:true});
(async()=>{
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const p=await b.newPage({viewport:{width:1920,height:2000}});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
 await p.goto('file://'+html,{waitUntil:'networkidle'}); await p.waitForFunction(()=>window.__ready);
 const n=lista?lista.split(',').map(Number):[0,1,2,3,4,5,6,7];
 for(const i of n){const nome=await p.evaluate(i=>FOTO(i),i); const el=await p.$('#foto'); await el.screenshot({path:`${out}/${nome}.png`}); console.log('ok',nome);}
 console.log('erros',JSON.stringify(errs)); await b.close();
})();
