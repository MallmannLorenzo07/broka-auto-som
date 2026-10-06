const { chromium } = require('playwright');const fs=require('fs');
const AD=process.argv[2];const TL=JSON.parse(fs.readFileSync(AD+'/timeline.json'));
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+AD+'/anuncio.html?rec=1');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(1000);
for(let i=0;i<TL.length;i++){await p.evaluate(t=>render(t),TL[i]);await p.screenshot({path:`${AD}/frames2/f${String(i).padStart(4,'0')}.jpg`,type:'jpeg',quality:95})}
console.log('frames',TL.length);await b.close()})();
