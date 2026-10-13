// usage: node render.cjs <outdir> [fps] [comma-separated preview times]
const {chromium}=require('/opt/node-tools/node_modules/playwright');const fs=require('fs');
(async()=>{const out=process.argv[2],fps=+(process.argv[3]||60),times=process.argv[4];
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1920,height:1080}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+__dirname+'/scene.html');await p.waitForFunction(()=>window.READY);
fs.mkdirSync(out,{recursive:true});
const T=times?times.split(',').map(Number):[...Array(Math.round(10*fps)).keys()].map(i=>i/fps);
for(let i=0;i<T.length;i++){await p.evaluate(t=>render(t),T[i]);await p.screenshot({path:out+'/f'+String(i).padStart(4,'0')+'.png'});}
await b.close()})();
