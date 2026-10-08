// vertical 1080x1920: node rv.js pagina.html?c=c1 saida.mp4   |   node rv.js pagina.html?c=c1 amostras t1,t2
const { chromium } = require('/opt/node22/lib/node_modules/playwright'); const { spawn } = require('child_process');
const [,,url,out,arg]=process.argv;
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+url,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForFunction(()=>window.__ready);
 const dur=await p.evaluate(()=>window.__dur);
 if(out==='amostras'){for(const t of arg.split(',').map(Number)){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:`/tmp/rv_${t}.jpg`,type:'jpeg',quality:80})}console.log('erros',JSON.stringify(errs));await b.close();return}
 const N=Math.round(dur*30), ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-r','30',out],{stdio:['pipe','inherit','inherit']});
 for(let i=0;i<N;i++){await p.evaluate(t=>window.__seek(t),i/30);const buf=await p.screenshot({type:'jpeg',quality:94});if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r))}
 ff.stdin.end();await new Promise(r=>ff.on('close',r));console.log('pronto',out,N,'quadros',JSON.stringify(errs));await b.close()})();
