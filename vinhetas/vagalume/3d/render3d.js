// uso: node render.js motion.html saida.mp4 audio.m4a [fps]   |   node render.js motion.html amostras  t1,t2,...
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process'); const fs=require('fs');
const [,,html,out,arg,fpsArg]=process.argv;
(async()=>{
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']}); const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1.2});
 const errs=[];p.on('pageerror',e=>errs.push(e.message));
 await p.goto('file://'+html,{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready); await p.waitForFunction(()=>window.__ready);
 const dur=await p.evaluate(()=>window.__dur);
 if(out==='amostras'){fs.mkdirSync(require('path').dirname(html)+'/amostras',{recursive:true});
   for(const t of arg.split(',').map(Number)){await p.evaluate(t=>window.__seek(t),t);await p.screenshot({path:require('path').dirname(html)+`/amostras/t_${String(t).padStart(6,'0')}.jpg`,type:'jpeg',quality:80});}
   console.log('erros',JSON.stringify(errs),'dur',dur);await b.close();return;}
 const fps=+(fpsArg||30), N=Math.ceil(dur*fps);
 const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-i','-','-i',arg,'-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-vf','scale=1920:1080:flags=lanczos','-c:a','copy','-shortest','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
 const t0=Date.now();
 for(let i=0;i<N;i++){
   await p.evaluate(t=>window.__seek(t),i/fps);
   const buf=await p.screenshot({type:'jpeg',quality:93});
   if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
   if(i%300===0)console.log(`quadro ${i}/${N} · ${((Date.now()-t0)/1000).toFixed(0)}s`);
 }
 ff.stdin.end(); await new Promise(r=>ff.on('close',r));
 console.log('pronto',out,'erros',JSON.stringify(errs)); await b.close();
})();
