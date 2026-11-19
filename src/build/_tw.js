const {chromium}=require('playwright');const fs=require('fs');(async()=>{
const b=await chromium.launch({args:['--use-gl=swiftshader','--enable-webgl','--ignore-gpu-blocklist']});
for (const [pg,w,out,wait] of [['index.html',1440,'/tmp/t_idx.png',5000],['03_collection_plan.html',1440,'/tmp/t_03p.png',5000],['08_midterm_review.html',1440,'/tmp/t_08p.png',5000],['12_visualization.html',390,'/tmp/t_12m.png',5000]]){
const p=await b.newPage({viewport:{width:w,height:900}});
p.on('pageerror',e=>console.log('ERR',pg,e.message));
await p.route(/fonts\.g/,r=>r.abort());
await p.route(/cdn\.jsdelivr\.net\/npm\/three@[^/]+\/(.*)$/,r=>{const m=r.request().url().match(/three@[^/]+\/(.*)$/);
 r.fulfill({status:200,contentType:'application/javascript',body:fs.readFileSync('/tmp/t3/node_modules/three/'+m[1])})});
await p.goto('file:///home/claude/fintech_data_analysis/'+pg);
if(w<700){await p.click('.tw-go3d');}
await p.waitForTimeout(wait);
await (await p.$('#tower')).screenshot({path:out});await p.close()}
await b.close()})()
