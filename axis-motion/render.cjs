const {chromium}=require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:1920,height:1080}});
await p.goto('file://'+__dirname+'/scene.html');await p.waitForTimeout(500);
const fs=require('fs');fs.mkdirSync('/tmp/fr',{recursive:true});
const N=300;for(let i=0;i<N;i++){await p.evaluate(t=>render(t),i/30);await p.screenshot({path:`/tmp/fr/f${String(i).padStart(4,'0')}.png`});}
await b.close()})();
