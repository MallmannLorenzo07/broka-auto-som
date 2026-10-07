// node render_parte.js pagina.html saida.mp4 quadro_inicial [quadro_final] — renderiza só um trecho (sem áudio), para retomar renders interrompidos
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const { spawn } = require('child_process');
const [,,html,out,ini,fimArg]=process.argv;
(async()=>{
 const b=await chromium.launch({args:['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
 const p=await b.newPage({viewport:{width:1600,height:900},deviceScaleFactor:1.2});
 await p.goto('file://'+html,{waitUntil:'networkidle'}); await p.evaluate(()=>document.fonts.ready); await p.waitForFunction(()=>window.__ready);
 const dur=await p.evaluate(()=>window.__dur), fps=30, N=fimArg?+fimArg:Math.ceil(dur*fps);
 const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate','30','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-vf','scale=1920:1080:flags=lanczos','-movflags','+faststart',out],{stdio:['pipe','inherit','inherit']});
 for(let i=+ini;i<N;i++){await p.evaluate(t=>window.__seek(t),i/fps); const buf=await p.screenshot({type:'jpeg',quality:93}); if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r)); if(i%60===0)console.log('quadro',i,'/',N);}
 ff.stdin.end(); await new Promise(r=>ff.on('close',r)); console.log('pronto',out); await b.close();
})();
