// 섹션별 스크린샷: node shots.js file.html out_prefix sel1 sel2 ...
const {chromium}=require('playwright');
(async()=>{const [f,pre,...sels]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:1100,height:900}});
await p.route(/fonts\.googleapis|fonts\.gstatic|jsdelivr/,r=>r.abort());await p.goto('file://'+f);await p.waitForTimeout(500);
for(const s of sels){const el=await p.$(s);if(!el){console.log('missing',s);continue}await el.scrollIntoViewIfNeeded();await p.waitForTimeout(250);await el.screenshot({path:pre+'_'+s.replace(/[^a-z0-9]/gi,'')+'.png'});console.log('shot',s)}
await b.close()})();
