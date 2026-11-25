/* 핀테크 데이터 분석 실험 모듈 — 실제 데이터(fintech-data 표본, FD)와 예시값 모형 */
function S0(el,cfg,hgt,label){return mkCanvas(el,hgt,label,cfg.wide)}
function mean(a){return a.reduce(function(s,v){return s+v},0)/a.length}
function sd(a){var m=mean(a);return Math.sqrt(a.reduce(function(s,v){return s+(v-m)*(v-m)},0)/a.length)}
function quant(a,q){var s=a.slice().sort(function(x,y){return x-y});var k=(s.length-1)*q,f=Math.floor(k);return s[f]+(s[Math.min(s.length-1,f+1)]-s[f])*(k-f)}
function median(a){return quant(a,.5)}
function frame(ctx,W,H,o){/* o: xlo,xhi,ylo,yhi,fx,fy,xl,yl,L,B */var L=o.L||56,R=14,T=o.T||28,B=o.B||34,pw=W-L-R,ph=H-T-B;
  function X(v){return L+(v-o.xlo)/(o.xhi-o.xlo)*pw}function Y(v){return T+ph-(v-o.ylo)/(o.yhi-o.ylo)*ph}
  ctx.save();ctx.strokeStyle=COL.rule;ctx.lineWidth=1;niceTicks(o.ylo,o.yhi,4).forEach(function(t){var y=Y(t);ctx.beginPath();ctx.moveTo(L,y+.5);ctx.lineTo(L+pw,y+.5);ctx.stroke();txt(ctx,(o.fy||String)(t),L-6,y+4,COL.muted,10,'right')});
  niceTicks(o.xlo,o.xhi,5).forEach(function(t){txt(ctx,(o.fx||String)(t),X(t),T+ph+15,COL.muted,10,'center')});ctx.restore();
  if(o.xl)txt(ctx,o.xl,L+pw,H-3,COL.muted,11,'right');if(o.yl)txt(ctx,o.yl,6,14,COL.muted,11,'left');
  return {X:X,Y:Y,L:L,T:T,pw:pw,ph:ph,inv:function(px,py){return [o.xlo+(px-L)/pw*(o.xhi-o.xlo),o.ylo+(T+ph-py)/ph*(o.yhi-o.ylo)]}}}
function dot(ctx,x,y,r,fill,stroke){ctx.beginPath();ctx.arc(x,y,r,0,7);if(fill){ctx.fillStyle=fill;ctx.fill()}if(stroke){ctx.strokeStyle=stroke;ctx.lineWidth=1.5;ctx.stroke()}}
function tbl(el,before){var tw=h('div',{class:'tw'});el.insertBefore(tw,before||null);return tw}
function seg(n){return Array.apply(null,Array(n)).map(function(_,i){return i})}
var REAL='실제 데이터',EX='예시값';
var C0='rgba(63,95,168,.55)',C1='rgba(210,63,44,.85)';

/* ── 공용: 분류해 보기(카드를 상자에 넣기) ── */
SIMS.sorter=function(el,cfg){var tw=tbl(el),row=ctrlRow(el),K=kpis(el,3),I=insight(el),pick={},cur=0;
  function draw(){var it=cfg.items[cur];tw.innerHTML='<div class="sortcard"><span class="muted">'+(cur+1)+' / '+cfg.items.length+'</span><p><b>'+it[0]+'</b></p></div>';
    var g=h('div',{class:'group'});cfg.cats.forEach(function(c,ci){var b=h('button',{class:'bt',type:'button','aria-pressed':String(pick[cur]===ci)},c);b.addEventListener('click',function(){pick[cur]=ci;draw()});g.appendChild(b)});tw.appendChild(g);
    var done=Object.keys(pick).length,ok=Object.keys(pick).filter(function(k){return pick[k]===cfg.items[k][1]}).length;
    K([[done+'/'+cfg.items.length,'고른 카드','i'],[ok+'개','맞힌 카드','g'],[done?pct(ok/done,0):'—','정답률','a']]);
    I(pick[cur]==null?[['a','위 버튼에서 알맞은 상자를 골라 보세요. '+(cfg.hint||'')]]:[[pick[cur]===it[1]?'g':'r',(pick[cur]===it[1]?'맞아요. ':'정답은 <b>'+cfg.cats[it[1]]+'</b>예요. ')+it[2]]])}
  action(row,'← 이전',function(){cur=(cur+cfg.items.length-1)%cfg.items.length;draw()});action(row,'다음 →',function(){cur=(cur+1)%cfg.items.length;draw()},true);action(row,'처음부터',function(){pick={};cur=0;draw()});draw()};

/* ── 공용: 순서 맞히기 ── */
SIMS.order=function(el,cfg){var tw=tbl(el),row=ctrlRow(el),I=insight(el),r=rng(cfg.seed||5),pool=cfg.steps.map(function(s,i){return i}),got=[];
  pool.sort(function(){return r()-.5});
  function draw(){tw.innerHTML='';var a=h('div',{class:'group'});a.appendChild(h('span',{class:'glabel'},'남은 단계'));pool.filter(function(i){return got.indexOf(i)<0}).forEach(function(i){var b=h('button',{class:'bt',type:'button'},cfg.steps[i][0]);b.addEventListener('click',function(){got.push(i);draw()});a.appendChild(b)});tw.appendChild(a);
    var ol=h('ol',{class:'orderlist'});got.forEach(function(i,k){var ok=i===k;ol.appendChild(h('li',{class:ok?'ok':'no'},(ok?'✓ ':'✗ ')+cfg.steps[i][0]+' <span class="muted">— '+cfg.steps[i][1]+'</span>'))});tw.appendChild(ol);
    var okn=got.filter(function(i,k){return i===k}).length;
    I(got.length<cfg.steps.length?[['a','첫 단계부터 차례로 눌러 보세요. 지금까지 '+got.length+'단계 중 '+okn+'단계가 제자리예요.']]:[[okn===cfg.steps.length?'g':'r',okn===cfg.steps.length?'모두 제자리예요. '+cfg.done:'제자리는 '+okn+'단계예요. 정답 순서: '+cfg.steps.map(function(s){return s[0]}).join(' → ')]])}
  action(row,'한 단계 되돌리기',function(){got.pop();draw()});action(row,'처음부터',function(){got=[];draw()});draw()};

/* ── 1-① 지점 vs 앱: 고객 1인당 운영비 (예시값) ── */
SIMS.branchcost=function(el,cfg){var c=S0(el,cfg,240,'지점 수에 따른 고객 1인당 운영비 막대'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),br=cfg.br0,cu=cfg.cu0;
  slider(row,'지점 수',0,800,10,br,function(v){return nf(v)+'곳'},function(v){br=v;draw()});slider(row,'고객 수',100,2000,50,cu,function(v){return nf(v)+'만 명'},function(v){cu=v;draw()});
  function draw(){var W=fit(c,240),ctx=c.getContext('2d');ctx.clearRect(0,0,W,240);grid(ctx,W,240);
    var fix=cfg.app,brc=br*cfg.perBr,tot=fix+brc,per=tot/(cu*1e4)*1e8,app=fix/(cu*1e4)*1e8,mx=Math.max(per,cfg.app/(100*1e4)*1e8+cfg.perBr*800/(100*1e4)*1e8)*0.6;
    var items=[['지점 은행',per,COL.s],['앱 전용 은행',app,COL.g]],L=110,pw=W-L-90;
    items.forEach(function(it,i){var y=60+i*80,w=clamp(it[1]/Math.max(per,1)*pw,2,pw);ctx.fillStyle=it[2];ctx.fillRect(L,y,w,34);txt(ctx,it[0],L-8,y+22,COL.text,12,'right',true);txt(ctx,nf(it[1])+'원',L+w+6,y+22,COL.text,12,'left',true)});
    stamp(ctx,W,EX);var gap=per-app;
    K([[nf(per)+'원','지점 은행 고객 1인당 연 운영비','i'],[nf(app)+'원','앱 전용 은행','g'],[nf(gap)+'원','차이 (금리·수수료 여력)','a'],[cu>0?(gap/ (cfg.dep*1e4)*100).toFixed(2)+'%p':'—','예금 '+nf(cfg.dep)+'만 원 기준 금리 여력','m']]);
    E('1인당 운영비 = (공통 운영비 <b>'+nf(cfg.app)+'억</b> + 지점 <em>'+nf(br)+'곳</em> × '+cfg.perBr+'억) ÷ 고객 '+nf(cu)+'만 명 = <i>'+nf(per)+'원</i>');
    I([['g','지점을 0곳으로 줄이면 비용 막대가 앱 전용 은행과 같아져요. 인터넷전문은행이 예금 금리를 더 주거나 수수료를 낮출 수 있는 이유예요.'],['a','숫자는 구조를 보여 주기 위한 예시값이에요. 실제 은행의 비용 구조는 인건비·전산·마케팅 등으로 훨씬 복잡합니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 1-② 결제 1만 원의 수수료 나눔 (예시값) ── */
SIMS.payflow=function(el,cfg){var c=S0(el,cfg,230,'결제 금액이 가맹점·카드사·VAN/PG·간편결제사로 나뉘는 띠'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),ch='off',amt=10000;
  buttons(row,'결제 길',[['off','오프라인 카드 (VAN)'],['on','온라인 카드 (PG)'],['easy','간편결제']],ch,function(v){ch=v;draw()});
  slider(row,'결제 금액',1000,100000,1000,amt,function(v){return nf(v)+'원'},function(v){amt=v;draw()});
  function draw(){var P=cfg[ch],W=fit(c,230),ctx=c.getContext('2d');ctx.clearRect(0,0,W,230);grid(ctx,W,230);var x0=20,w=W-40,tot=0;
    var parts=P.parts.map(function(p){var v=Math.round(amt*p[1]/100);tot+=v;return [p[0],v,p[2]]});
    txt(ctx,'결제 '+nf(amt)+'원 전체',x0,26,COL.text,12,'left',true);var mw=(amt-tot)/amt*w;ctx.fillStyle='#5d6278';ctx.fillRect(x0,34,mw,30);ctx.fillStyle=COL.r;ctx.fillRect(x0+mw,34,w-mw,30);txt(ctx,'가맹점 '+pct((amt-tot)/amt,1),x0+8,54,'#fff',12,'left',true);txt(ctx,'수수료 →',x0+mw-6,54,'#fff',11,'right',true);
    txt(ctx,'수수료 '+nf(tot)+'원만 크게 펼쳐 보기',x0,104,COL.text,12,'left',true);var x=x0;
    parts.forEach(function(p,i){var pw=p[1]/(tot||1)*w;ctx.fillStyle=p[2];ctx.fillRect(x,112,Math.max(pw-2,1),46);if(pw>60){txt(ctx,p[0],x+pw/2,132,'#fff',12,'center',true);txt(ctx,nf(p[1])+'원',x+pw/2,150,'#fff',12,'center',true)}else txt(ctx,p[0]+' '+nf(p[1])+'원',x+pw/2,176+(i%2)*14,p[2],11,'center',true);x+=pw});
    stamp(ctx,W,EX);
    K([[nf(amt-tot)+'원','가맹점이 받는 돈','g'],[nf(tot)+'원','수수료 합계','r'],[pct(tot/amt,2),'수수료율 합계','a'],[P.parts.length+'곳','돈이 거쳐 가는 회사','i']]);
    E('수수료 = 결제 금액 × 수수료율 → '+P.parts.map(function(p){return p[0]+' '+p[1]+'%'}).join(' + ')+' = <i>'+pct(tot/amt,2)+'</i>');
    I([['g',P.note],['a','수수료율은 구조를 보여 주는 예시값이에요. 실제 수수료는 가맹점 규모·업종·계약에 따라 다르고, 우대 수수료 제도가 있습니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 1-③ 실제 은행 고객 데이터 열 둘러보기 ── */
SIMS.columns=function(el,cfg){var cols=FD.bankcols,c=S0(el,cfg,260,'고른 열의 구간별 이탈률 막대'),row=ctrlRow(el),K=kpis(el,4),I=insight(el),cur=cfg.start||0;
  var sel=h('select',{class:'sel','aria-label':'열 고르기'});cols.forEach(function(o,i){var op=h('option',{value:i},o.ko+' ('+o.c+')');if(i===cur)op.selected=true;sel.appendChild(op)});var g=h('div',{class:'group'});g.appendChild(h('span',{class:'glabel'},'열 고르기'));g.appendChild(sel);row.appendChild(g);
  sel.addEventListener('change',function(){cur=+sel.value;draw()});
  function draw(){var o=cols[cur],W=fit(c,260),ctx=c.getContext('2d');ctx.clearRect(0,0,W,260);grid(ctx,W,260);var it=o.rate,mx=Math.max.apply(null,it.map(function(x){return x[1]}).concat([.2]))*1.15;
    var L=50,pw=W-L-14,bw=pw/it.length,base=FD.bank.rate;
    ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.a;var yb=230-base/mx*190;ctx.beginPath();ctx.moveTo(L,yb);ctx.lineTo(L+pw,yb);ctx.stroke();ctx.restore();txt(ctx,'점선: 전체 이탈률 '+pct(base,1),L+pw,18,COL.a,11,'right',true);
    it.forEach(function(x,i){var bh=x[1]/mx*190,bx=L+i*bw+bw*.18;ctx.fillStyle=x[1]>base*1.3?COL.r:C0;ctx.fillRect(bx,230-bh,bw*.64,bh);txt(ctx,pct(x[1],1),bx+bw*.32,226-bh,COL.text,11,'center',true);txt(ctx,String(x[0]).replace('Less than ','~').replace(' - ','~').slice(0,14),bx+bw*.32,246,COL.muted,10,'center')});
    txt(ctx,o.ko+' — 구간(또는 범주)별 이탈률',L,18,COL.text,12,'left',true);
    var spread=Math.max.apply(null,it.map(function(x){return x[1]}))-Math.min.apply(null,it.map(function(x){return x[1]}));
    K([[o.kind==='num'?'숫자형':'범주형','데이터 유형','i'],[o.kind==='num'?nf(o.mean,1):String(o.top[0][0]),o.kind==='num'?'평균':'가장 많은 값','g'],[pct(spread,1)+'p','구간별 이탈률 차이','r'],[o.group,'데이터 묶음','a']]);
    I([[spread>.15?'r':'g',spread>.15?'구간에 따라 이탈률이 크게 달라요. 이 열은 이탈을 예측하는 데 쓸모가 큰 후보입니다.':'구간별 이탈률이 전체(점선)와 비슷해요. 이 열만으로는 이탈을 가르기 어렵습니다.'],['a',o.note]])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 2-② 수집 방법 고르기 (예시 점수) ── */
SIMS.collect=function(el,cfg){var c=S0(el,cfg,250,'수집 방법별 가중 점수 막대'),row=ctrlRow(el),K=kpis(el,3),I=insight(el),wt=cfg.crit.map(function(x){return x[1]});
  cfg.crit.forEach(function(cr,i){slider(row,cr[0]+' 중요도',0,5,1,wt[i],function(v){return v},function(v){wt[i]=v;draw()})});
  function draw(){var W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);var sw=wt.reduce(function(a,b){return a+b},0)||1;
    var sc=cfg.methods.map(function(m){return [m[0],m[1].reduce(function(s,v,i){return s+v*wt[i]},0)/sw,m[2]]}),best=sc.slice().sort(function(a,b){return b[1]-a[1]})[0];
    var L=130,pw=W-L-60;sc.forEach(function(s,i){var y=24+i*54;ctx.fillStyle=s===best?COL.g:C0;ctx.fillRect(L,y,s[1]/5*pw,30);txt(ctx,s[0],L-8,y+20,COL.text,12,'right',true);txt(ctx,s[1].toFixed(2)+' / 5',L+s[1]/5*pw+6,y+20,COL.text,12,'left',true)});stamp(ctx,W,EX);
    K([[best[0],'지금 가중치에서 1등','g'],[best[1].toFixed(2),'가중 점수(5점 만점)','i'],[sw,'가중치 합','a']]);
    I([['g',best[2]],['a','점수는 교안의 체크포인트(비용·적시성·신뢰성·확장성)를 비교하려고 정한 예시값이에요. 프로젝트마다 다시 매겨야 합니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 2-③ 준식별자 조합과 다시 알아보기(재식별) 위험 — 보험 데이터 1,338명 ── */
SIMS.pseudo=function(el,cfg){var tw=tbl(el),row=ctrlRow(el),K=kpis(el,4),I=insight(el),lv=0;var U=FD.ins.uniq;
  buttons(row,'공개할 열',U.map(function(u,i){return [i,u[0]]}),0,function(v){lv=v;draw()});
  function draw(){var u=U[lv];tw.innerHTML='<table class="tb"><tr><th>단계</th><th>하는 일</th><th>법적 구분</th></tr>'+cfg.rows.map(function(r){return '<tr><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+r[2]+'</td></tr>'}).join('')+'</table>';
    K([[nf(u[1])+'명','세상에 한 명뿐인 조합','r'],[pct(u[1]/FD.ins.n,1),'전체 '+nf(FD.ins.n)+'명 중','a'],[nf(u[3]),'서로 다른 조합 수','i'],[u[2]+'명','가장 작은 묶음 크기 (k)','g']]);
    I([[u[1]>100?'r':'a','이름을 지워도 <b>'+u[0]+'</b>를 그대로 두면 '+nf(u[1])+'명은 그 조합이 유일해요. 이 사람의 이웃·동료가 이 열들을 알면 누구인지 알아볼 수 있습니다(재식별).'],['g','열을 줄일수록 유일한 사람이 줄어요. 이름만 지운 데이터는 "가명정보"이지 "익명정보"가 아닙니다. 14회차에서 k-익명성으로 더 자세히 봐요.']])}
  draw()};

/* ── 3-② 서비스 vs 플랫폼 (예시값) ── */
SIMS.network=function(el,cfg){var c=S0(el,cfg,250,'사용자 수에 따른 연결 수와 데이터 열 수'),row=ctrlRow(el),K=kpis(el,4),I=insight(el),n=20,s=3;
  slider(row,'사용자 수',2,60,1,n,function(v){return v+'명'},function(v){n=v;draw()});slider(row,'연결된 서비스 수',1,8,1,s,function(v){return v+'개'},function(v){s=v;draw()});
  function draw(){var W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);var r=rng(3),cx=W*.3,cy=130,R=95,pts=seg(n).map(function(i){var a=i/n*Math.PI*2;return [cx+R*Math.cos(a),cy+R*Math.sin(a)]});
    ctx.strokeStyle='rgba(63,95,168,.12)';ctx.lineWidth=1;if(n<=40)pts.forEach(function(p,i){for(var j=i+1;j<n;j++){ctx.beginPath();ctx.moveTo(p[0],p[1]);ctx.lineTo(pts[j][0],pts[j][1]);ctx.stroke()}});
    pts.forEach(function(p){dot(ctx,p[0],p[1],4,COL.s)});txt(ctx,'플랫폼: 사용자끼리 연결',cx,22,COL.text,12,'center',true);
    var x0=W*.62,links=n*(n-1)/2,cells=n*s*cfg.per;txt(ctx,'서비스 1개: 회사 ↔ 사용자',x0+W*.18,22,COL.text,12,'center',true);
    var bx=x0,bw=W-x0-20;[['서비스 연결 수',n,COL.muted],['플랫폼 연결 수',links,COL.s],['쌓이는 데이터 열',cells,COL.g]].forEach(function(b,i){var mx=Math.max(links,cells,n);var w=b[1]/mx*bw;ctx.fillStyle=b[2];ctx.fillRect(bx,60+i*55,Math.max(w,2),26);txt(ctx,b[0]+' '+nf(b[1]),bx,54+i*55,COL.text,11,'left',true)});stamp(ctx,W,EX);
    K([[nf(n),'서비스형: 회사와의 연결','i'],[nf(links),'플랫폼형: 사용자끼리 연결 n(n−1)/2','g'],[nf(cells),'통합 데이터 열 (사용자×서비스×'+cfg.per+')','a'],[(links/n).toFixed(1)+'배','연결 수 차이','r']]);
    I([['g','사용자가 늘면 플랫폼의 연결 수는 제곱에 가깝게 늘어요(네트워크 효과). 송금·결제·보험이 한 앱에 붙으면 한 사람의 데이터가 여러 서비스에 걸쳐 통합됩니다.'],['a','"데이터가 많다"가 "쓸모 있다"는 뜻은 아니에요. 통합된 만큼 개인정보 보호와 품질 관리 부담도 커집니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 3-③ 대출 데이터 사전(80열)에서 목표에 필요한 열 고르기 ── */
SIMS.dict=function(el,cfg){var tw=tbl(el),row=ctrlRow(el),K=kpis(el,4),I=insight(el),goal=0,q='';
  buttons(row,'분석 목표',cfg.goals.map(function(g,i){return [i,g[0]]}),0,function(v){goal=v;draw()});
  var inp=h('input',{class:'search',type:'search',placeholder:'열 이름·설명 검색 (예: annual, 연체)','aria-label':'데이터 사전 검색'});row.appendChild(inp);inp.addEventListener('input',function(){q=inp.value.toLowerCase();draw()});
  function draw(){var G=cfg.goals[goal],need=G[1],D=FD.loan_dict;var rows=D.filter(function(d){return !q||d[0].toLowerCase().indexOf(q)>=0||d[1].toLowerCase().indexOf(q)>=0});
    tw.innerHTML='<table class="tb"><tr><th>열 이름</th><th>설명(원문)</th><th>이 목표에</th></tr>'+rows.slice(0,14).map(function(d){var on=need.indexOf(d[0])>=0;return '<tr'+(on?' class="hit"':'')+'><td><code>'+esc(d[0])+'</code></td><td>'+esc(d[1])+'</td><td>'+(on?'<b style="color:var(--g)">필요</b>':'<span class="muted">—</span>')+'</td></tr>'}).join('')+'</table>'+(rows.length>14?'<p class="muted">… 검색 결과 '+rows.length+'열 중 14열만 보여요.</p>':'');
    K([[D.length+'열','데이터 사전 전체','i'],[need.length+'열','이 목표에 필요한 열(예시 선택)','g'],[pct(need.length/D.length,0),'전체 중 필요한 비율','a'],[rows.length+'열','검색 결과','m']]);
    I([['g',G[2]],['a','원본 대출 데이터(loan.csv)는 용량이 커서 이 저장소에 넣지 못했고, 열 설명서(loan_data_description.csv)만 들어 있어요. 필요한 열 고르기는 설명용 예시예요.']])}
  draw()};

/* ── 4-① 분석 도구 고르기 (예시 규칙) ── */
SIMS.toolpick=function(el,cfg){var c=S0(el,cfg,240,'도구별 적합도 막대'),row=ctrlRow(el),K=kpis(el,3),I=insight(el),v={size:2,repeat:2,budget:2,code:1,share:2};
  [['size','데이터 크기',['수천 행','수만 행','수백만 행']],['repeat','반복 분석',['한 번','가끔','매일 자동']],['budget','예산',['0원','조금','넉넉']],['code','코딩 경험',['없음','조금','능숙']],['share','결과 공유',['파일','보고서','대시보드']]].forEach(function(o){buttons(row,o[1],o[2].map(function(t,i){return [i+1,t]}),v[o[0]],function(x){v[o[0]]=x;draw()})});
  function draw(){var W=fit(c,240),ctx=c.getContext('2d');ctx.clearRect(0,0,W,240);grid(ctx,W,240);
    var S=cfg.tools.map(function(t){var s=0;for(var k in t[1])s+=t[1][k][v[k]-1];return [t[0],s,t[2]]}),mx=Math.max.apply(null,S.map(function(s){return s[1]})),best=S.filter(function(s){return s[1]===mx})[0];
    var L=130,pw=W-L-50;S.forEach(function(s,i){var y=24+i*52;var w=clamp((s[1]+10)/30*pw,4,pw);ctx.fillStyle=s===best?COL.g:C0;ctx.fillRect(L,y,w,30);txt(ctx,s[0],L-8,y+20,COL.text,12,'right',true);txt(ctx,String(s[1]),L+w+6,y+20,COL.text,12,'left',true)});stamp(ctx,W,EX);
    K([[best[0],'지금 조건에서 1등','g'],[String(mx),'적합 점수','i'],[S.length+'종','비교한 도구 묶음','a']]);I([['g',best[2]],['a','점수 규칙은 교안의 도구 비교표를 바탕으로 정한 예시예요. 실제로는 회사가 이미 쓰는 도구와 보안 규정이 가장 큰 조건입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 4-③ / 공용: KNN k에 따른 학습·시험 정확도 (실제 데이터) ── */
SIMS.fitcurve=function(el,cfg){var c=S0(el,cfg,250,'k에 따른 학습 정확도와 시험 정확도 선'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),ks=[1,3,5,7,9,11,15,21,31,51],ki=0;
  slider(row,'이웃 수 k',0,ks.length-1,1,ki,function(i){return 'k = '+ks[i]},function(i){ki=i;draw()});
  function draw(){var A=FD.knn.std,W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);var F=frame(ctx,W,250,{xlo:0,xhi:ks.length-1,ylo:.85,yhi:1,fy:function(v){return pct(v,0)},fx:function(i){return ks[Math.round(i)]||''},xl:'이웃 수 k'});
    [[0,COL.r,'학습 정확도'],[1,COL.g,'시험 정확도']].forEach(function(s,si){ctx.strokeStyle=s[1];ctx.lineWidth=2.4;ctx.beginPath();ks.forEach(function(k,i){var y=F.Y(A[k][s[0]]);i?ctx.lineTo(F.X(i),y):ctx.moveTo(F.X(i),y)});ctx.stroke();txt(ctx,'● '+s[2],F.L+8+si*110,18,s[1],12,'left',true)});
    ctx.save();ctx.setLineDash([4,3]);ctx.strokeStyle=COL.muted;ctx.beginPath();ctx.moveTo(F.X(ki),F.T);ctx.lineTo(F.X(ki),F.T+F.ph);ctx.stroke();ctx.restore();stamp(ctx,W,REAL);
    var a=A[ks[ki]],gap=a[0]-a[1];K([[pct(a[0],1),'학습 정확도','r'],[pct(a[1],1),'시험 정확도','g'],[pct(gap,1)+'p','둘의 차이','a'],[pct(FD.knn.base,1),'"모두 남는다"로 찍을 때','i']]);
    E('정확도 = 맞힌 고객 수 ÷ 전체 고객 수 · 학습 '+nf(FD.knn.ntr)+'명, 시험 '+nf(FD.knn.nte)+'명 (은행 고객 10,127명을 75:25로 나눔)');
    I([[gap>.05?'r':'g',gap>.05?'k가 작으면 학습 데이터는 거의 다 맞히지만 시험 데이터에서는 떨어져요. 시험 범위를 외운 학생처럼 새 고객에 약한 <b>과대적합</b>입니다.':'k를 키우면 두 정확도가 가까워져요. 새 고객에게도 비슷하게 통하는 상태예요.'],['a','"모두 남는다"고만 찍어도 '+pct(FD.knn.base,1)+'가 나와요. 정확도는 이 기준선과 비교해서 읽어야 합니다(7회차).']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 5-① 같은 고객을 여러 자료 구조로 ── */
SIMS.structs=function(el,cfg){var tw=tbl(el),row=ctrlRow(el),I=insight(el),m='list';var R=cfg.rows;
  buttons(row,'자료 구조',[['list','List'],['tuple','Tuple'],['dict','Dictionary'],['df','DataFrame']],m,function(v){m=v;draw()});
  function draw(){var s='';if(m==='list')s='<pre class="out">trans_ct = ['+R.map(function(r){return r[1]}).join(', ')+']\ntrans_amt = ['+R.map(function(r){return r[2]}).join(', ')+']\nlabel = ['+R.map(function(r){return r[3]}).join(', ')+']\n\ntrans_ct.append(80)   # 바꿀 수 있어요</pre>';
    if(m==='tuple')s='<pre class="out">customer = ('+R[0].join(', ')+')\n\ncustomer[1] = 50   # 오류! 튜플은 바꿀 수 없어요</pre>';
    if(m==='dict')s='<pre class="out">customer = {\n  "고객번호": '+R[0][0]+',\n  "거래횟수": '+R[0][1]+',\n  "거래금액": '+R[0][2]+',\n  "이탈": '+R[0][3]+'\n}\ncustomer["거래횟수"]   # 이름(키)으로 꺼냄 → '+R[0][1]+'</pre>';
    if(m==='df')s='<table class="tb"><tr><th></th><th>고객번호</th><th>거래횟수</th><th>거래금액</th><th>이탈</th></tr>'+R.map(function(r,i){return '<tr><td class="muted">'+i+'</td><td>'+r[0]+'</td><td>'+r[1]+'</td><td>'+nf(r[2])+'</td><td>'+r[3]+'</td></tr>'}).join('')+'</table>';
    tw.innerHTML=s;I([['g',{list:'List는 순서가 있고 바꿀 수 있어요. 교안의 bream_length처럼 같은 종류의 값을 한 줄로 모을 때 씁니다.',tuple:'Tuple은 List와 같지만 바꿀 수 없어요. 고정된 기록(예: 거래 한 건)을 실수로 고치지 않게 할 때 씁니다.',dict:'Dictionary는 "이름: 값" 쌍이에요. 고객 한 명의 여러 항목을 이름으로 꺼낼 때 편합니다.',df:'DataFrame(pandas)은 엑셀 표처럼 행과 열이 있어요. 실제 분석은 대부분 여기서 합니다. 값은 실제 은행 고객 5명이에요.'}[m]]])}
  draw()};

/* ── 5-② 이상치: 거래 금액 상자그림과 IQR 울타리 (실제 데이터) ── */
SIMS.outlier=function(el,cfg){var c=S0(el,cfg,250,'거래 금액 히스토그램과 이상치 울타리'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),k=1.5,v=FD.amt;
  slider(row,'울타리 배수',1,4,.5,k,function(x){return '× '+x.toFixed(1)},function(x){k=x;draw()});
  function draw(){var W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);var q1=FD.out.q1,q3=FD.out.q3,iq=q3-q1,up=q3+k*iq;
    var F=frame(ctx,W,250,{xlo:0,xhi:19000,ylo:0,yhi:1,fx:function(x){return nf(x/1000)+'천'},fy:function(){return ''},xl:'연간 거래 금액(달러)',L:20});
    var bins=38,cnt=new Array(bins).fill(0);v.forEach(function(x){cnt[Math.min(bins-1,Math.floor(x/19000*bins))]++});var mx=Math.max.apply(null,cnt);
    cnt.forEach(function(n,i){var x0=F.X(i*19000/bins),x1=F.X((i+1)*19000/bins),hh=n/mx*(F.ph-20);ctx.fillStyle=(i+.5)*19000/bins>up?C1:C0;ctx.fillRect(x0+1,F.T+F.ph-hh,x1-x0-2,hh)});
    ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.r;ctx.beginPath();ctx.moveTo(F.X(up),F.T);ctx.lineTo(F.X(up),F.T+F.ph);ctx.stroke();ctx.restore();txt(ctx,'울타리 '+nf(up),F.X(up)+4,F.T+12,COL.r,11,'left',true);stamp(ctx,W,REAL);
    var n=v.filter(function(x){return x>up}).length,N=v.length;K([[nf(Math.round(up)),'위쪽 울타리(달러)','r'],[nf(Math.round(n/N*FD.bank.n)),'울타리 밖 고객(전체 기준 추정)','a'],[pct(n/N,1),'비율','i'],[pct(FD.out.attr_rate_out,1),'1.5배 울타리 밖 고객의 이탈률','g']]);
    E('위쪽 울타리 = Q3 + <b>'+k.toFixed(1)+'</b> × IQR = '+nf(q3)+' + '+k.toFixed(1)+' × '+nf(iq)+' = <i>'+nf(Math.round(up))+'</i> (IQR = Q3 − Q1)');
    I([['a','오른쪽에 따로 떨어진 봉우리가 보여요. 입력 오류가 아니라 거래를 아주 많이 하는 "우량 고객" 무리입니다.'],['g','이상치는 무조건 지우는 게 아니에요. 이 고객들의 이탈률은 '+pct(FD.out.attr_rate_out,1)+'로 전체('+pct(FD.bank.rate,1)+')보다 낮아, 지우면 중요한 정보를 잃습니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 5-③ 라벨 만들기와 순서쌍 ── */
SIMS.labeling=function(el,cfg){var c=S0(el,cfg,200,'기존 고객과 이탈 고객 수 막대'),tw=tbl(el),row=ctrlRow(el),K=kpis(el,3),I=insight(el),step=0;
  buttons(row,'단계',[[0,'① 원래 값'],[1,'② 1/0 라벨'],[2,'③ [길이, 무게]처럼 순서쌍']],0,function(v){step=v;draw()});
  function draw(){var W=fit(c,200),ctx=c.getContext('2d');ctx.clearRect(0,0,W,200);grid(ctx,W,200);var a=FD.bank.n-FD.bank.attr,b=FD.bank.attr;
    [[step?'0 (기존 고객)':'Existing Customer',a,C0],[step?'1 (이탈 고객)':'Attrited Customer',b,C1]].forEach(function(x,i){var w=x[1]/FD.bank.n*(W-200);ctx.fillStyle=x[2];ctx.fillRect(170,40+i*64,w,36);txt(ctx,x[0],162,63+i*64,COL.text,12,'right',true);txt(ctx,nf(x[1])+'명',176+w,63+i*64,COL.text,12,'left',true)});stamp(ctx,W,REAL);
    var R=FD.rows5;tw.innerHTML=step<2?'<pre class="out">'+(step===0?'Attrition_Flag: '+R.map(function(r){return r[3]?'"Attrited Customer"':'"Existing Customer"'}).join(', '):'target = [0]*'+nf(a)+' + [1]*'+nf(b)+'   # 교안의 [1]*35 + [0]*14와 같은 방법\n# 실제로는 순서대로가 아니라 고객마다: (df.Attrition_Flag == "Attrited Customer").astype(int)')+'</pre>':'<pre class="out">data = [[c, a] for c, a in zip(trans_ct, trans_amt)]\n'+R.map(function(r){return '['+r[1]+', '+r[2]+'] → '+r[3]}).join('\n')+'</pre>';
    K([[nf(FD.bank.n),'전체 고객','i'],[pct(b/FD.bank.n,1),'이탈 고객 비율','r'],[(a/b).toFixed(1)+' : 1','기존 : 이탈','a']]);
    I([['g',['문자 라벨은 모델이 계산할 수 없어요. 숫자로 바꿔야 합니다.','관심 있는 쪽(이탈)을 1로 두는 것이 관례예요. 정밀도·재현율이 "1을 얼마나 잘 잡나"로 계산되기 때문입니다.','zip은 두 리스트를 지퍼처럼 하나씩 짝지어요. 고객마다 [거래횟수, 거래금액] 한 쌍이 입력, 0/1이 정답이 됩니다.'][step]],['a','이탈 고객이 16%뿐이라 "모두 남는다"고 찍어도 84%가 맞아요. 이 불균형은 6·7회차 내내 따라다닙니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 6-① KNN: 새 고객의 이웃 투표 (실제 표본 400명) ── */
function knnPlot(el,cfg,mode){var c=S0(el,cfg,300,'거래 횟수·거래 금액 산점도와 새 고객의 이웃'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),k=5,std=mode==='scale'?0:1,nx=cfg.nx||50,ny=cfg.ny||2500;
  var S=FD.knn_s,mu=FD.knn.mu,sg=FD.knn.sd;
  if(mode!=='scale')slider(row,'이웃 수 k',1,25,2,k,function(v){return 'k = '+v},function(v){k=v;draw()});
  if(mode==='scale')buttons(row,'거리 재는 법',[[0,'그대로 (달러가 지배)'],[1,'표준화 후']],0,function(v){std=v;draw()});
  function dist(i){var dx=S.x[i]-nx,dy=S.y[i]-ny;if(std){dx/=sg[0];dy/=sg[1]}return Math.sqrt(dx*dx+dy*dy)}
  function draw(){var W=fit(c,300),ctx=c.getContext('2d');ctx.clearRect(0,0,W,300);grid(ctx,W,300);var F=frame(ctx,W,300,{xlo:0,xhi:145,ylo:0,yhi:19000,fx:String,fy:function(v){return nf(v/1000)+'천'},xl:'연간 거래 횟수',yl:'거래 금액($)'});c._F=F;
    var idx=seg(S.x.length).sort(function(a,b){return dist(a)-dist(b)}).slice(0,k),vote=idx.filter(function(i){return S.t[i]}).length;
    S.x.forEach(function(x,i){dot(ctx,F.X(x),F.Y(S.y[i]),3,S.t[i]?C1:C0)});
    idx.forEach(function(i){ctx.strokeStyle=COL.a;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(F.X(nx),F.Y(ny));ctx.lineTo(F.X(S.x[i]),F.Y(S.y[i]));ctx.stroke();dot(ctx,F.X(S.x[i]),F.Y(S.y[i]),6,null,COL.a)});
    ctx.fillStyle=COL.text;ctx.beginPath();var px=F.X(nx),py=F.Y(ny);ctx.moveTo(px,py-9);ctx.lineTo(px+8,py+6);ctx.lineTo(px-8,py+6);ctx.closePath();ctx.fill();
    txt(ctx,'● 기존 고객  ',F.L+6,F.T+4,COL.s,11,'left',true);txt(ctx,'● 이탈 고객',F.L+90,F.T+4,COL.r,11,'left',true);stamp(ctx,W,REAL+' 400명');
    var pred=vote*2>k?1:0,dx=(std?'표준화':'그대로');
    K([[vote+' / '+k,'이웃 중 이탈 고객','r'],[pred?'이탈':'유지','다수결 예측','g'],[nf(nx)+'회 · $'+nf(ny),'새 고객 (그림을 눌러 옮기기)','i'],[mode==='scale'?dx:pct(FD.knn.std[k]?FD.knn.std[k][1]:FD.knn.std[5][1],1),mode==='scale'?'거리 재는 법':'k='+(FD.knn.std[k]?k:5)+' 시험 정확도(전체 데이터)','a']]);
    E(mode==='scale'?'거리 = √( (거래횟수 차이'+(std?' ÷ '+sg[0].toFixed(1):'')+')² + (거래금액 차이'+(std?' ÷ '+nf(sg[1]):'')+')² )':'예측 = 가장 가까운 <b>k</b>명 중 많은 쪽 → 이탈 '+vote+'명 vs 유지 '+(k-vote)+'명 → <i>'+(pred?'이탈':'유지')+'</i>');
    I(mode==='scale'?(std?[['g','표준화하면 두 축이 같은 무게가 돼요. 이웃이 거래 횟수가 비슷한 고객들로 바뀝니다.'],['a','교안의 생선(길이 cm · 무게 g) 예와 같은 현상이에요. 단위가 큰 쪽이 거리를 독차지합니다.']]:[['r','지금은 거래 금액(수천 달러) 차이가 거래 횟수(수십 회) 차이를 압도해요. 이웃이 거의 "금액이 비슷한 사람"으로만 뽑힙니다. 위 산점도에서 이웃들이 가로로 길게 퍼진 것을 보세요.'],['a','그림의 축 눈금 때문에 가까워 보여도, 계산에서는 금액 1,000달러 차이가 횟수 1,000번 차이와 같게 취급돼요.']]):[['g','k가 작으면 바로 옆 몇 명에 휘둘리고, 크면 멀리 있는 고객까지 투표해요. 실제 데이터에서는 k = 21 근처가 시험 정확도가 가장 높았습니다.'],['a','KNN은 "학습"이라 할 게 거의 없어요. 고객을 모두 기억해 두었다가 물어볼 때마다 거리를 다 잽니다. 그래서 고객이 많으면 느려요.']])}
  c.addEventListener('click',function(e){var F=c._F;if(!F)return;var r=c.getBoundingClientRect(),v=F.inv(e.clientX-r.left,e.clientY-r.top);nx=clamp(Math.round(v[0]),10,140);ny=clamp(Math.round(v[1]/50)*50,500,18500);draw()});
  addMod(c,function(dt){if(!dt)draw()});draw()}
SIMS.knn=function(el,cfg){knnPlot(el,cfg,'knn')};
SIMS.scale=function(el,cfg){knnPlot(el,cfg,'scale')};

/* ── 6-② 선형 SVM: 경계와 여백 (표준화된 실제 표본, 브라우저에서 학습) ── */
SIMS.svm=function(el,cfg){var c=S0(el,cfg,300,'표준화한 산점도와 SVM 경계선·여백'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),lam=0.01,bal=1;
  var S=FD.knn_s,mu=FD.knn.mu,sg=FD.knn.sd,X=S.x.map(function(x,i){return [(x-mu[0])/sg[0],(S.y[i]-mu[1])/sg[1]]}),Y=S.t.map(function(t){return t?1:-1});
  slider(row,'여백 넓히기 λ (클수록 C 작음)',-4,0,.5,-2,function(v){return 'λ = 10^'+v},function(v){lam=Math.pow(10,v);draw()});
  buttons(row,'이탈 고객 가중',[[0,'같게'],[1,'더 무겁게 (balanced)']],bal,function(v){bal=v;draw()});
  function train(){var w=[0,0],b=0,r=rng(9),n=X.length,np=Y.filter(function(y){return y>0}).length,wp=bal?n/(2*np):1,wn=bal?n/(2*(n-np)):1;
    for(var t=1;t<=6000;t++){var i=Math.floor(r()*n),eta=1/(lam*t+50),m=Y[i]*(w[0]*X[i][0]+w[1]*X[i][1]+b),cw=Y[i]>0?wp:wn;w[0]*=(1-eta*lam);w[1]*=(1-eta*lam);if(m<1){w[0]+=eta*cw*Y[i]*X[i][0];w[1]+=eta*cw*Y[i]*X[i][1];b+=eta*cw*Y[i]*.5}}return [w,b]}
  function draw(){var M=train(),w=M[0],b=M[1],W=fit(c,300),ctx=c.getContext('2d');ctx.clearRect(0,0,W,300);grid(ctx,W,300);var F=frame(ctx,W,300,{xlo:-2.6,xhi:3.2,ylo:-1.3,yhi:4.2,fx:function(v){return v.toFixed(0)},fy:function(v){return v.toFixed(0)},xl:'거래 횟수 (표준화)',yl:'거래 금액 (표준화)'});
    var tp=0,fp=0,fn=0,tn=0,sv=0;X.forEach(function(p,i){var s=w[0]*p[0]+w[1]*p[1]+b,pr=s>0?1:-1;if(Math.abs(s)<1)sv++;if(pr>0&&Y[i]>0)tp++;else if(pr>0)fp++;else if(Y[i]>0)fn++;else tn++;dot(ctx,F.X(p[0]),F.Y(p[1]),Math.abs(s)<1?4.5:3,Y[i]>0?C1:C0,Math.abs(s)<1?COL.text:null)});
    function ln(off,col,dash){if(Math.abs(w[1])<1e-6)return;ctx.save();ctx.strokeStyle=col;ctx.lineWidth=dash?1.2:2.6;if(dash)ctx.setLineDash([5,4]);ctx.beginPath();var x0=-2.6,x1=3.2;ctx.moveTo(F.X(x0),F.Y((off-b-w[0]*x0)/w[1]));ctx.lineTo(F.X(x1),F.Y((off-b-w[0]*x1)/w[1]));ctx.stroke();ctx.restore()}
    ctx.save();ctx.beginPath();ctx.rect(F.L,F.T,F.pw,F.ph);ctx.clip();ln(0,COL.text,0);ln(1,COL.muted,1);ln(-1,COL.muted,1);ctx.restore();stamp(ctx,W,REAL+' 400명');
    var n=X.length,acc=(tp+tn)/n,rec=tp/(tp+fn||1),marg=2/Math.sqrt(w[0]*w[0]+w[1]*w[1]);
    K([[pct(acc,1),'정확도(이 표본)','g'],[pct(rec,1),'이탈 고객을 잡은 비율(재현율)','r'],[marg.toFixed(2),'여백 폭 (2/|w|)','i'],[sv+'명','여백 안·경계 위 고객(굵은 점)','a']]);
    E('경계: '+w[0].toFixed(2)+' × 거래횟수 + '+w[1].toFixed(2)+' × 거래금액 + ('+b.toFixed(2)+') = 0 · 점선 = 여백(±1)');
    I([[bal?'g':'r',bal?'이탈 고객에 무게를 더 주면 경계가 기존 고객 쪽으로 밀려, 이탈 고객을 더 많이 잡아요. 대신 기존 고객 일부를 이탈로 잘못 부릅니다.':'가중을 같게 두면 수가 많은 기존 고객 쪽으로 기울어, 이탈 고객을 거의 놓칠 수 있어요. 실제 데이터 전체에서 선형 SVM은 정확도 '+pct(FD.knn.svm_lin,1)+'로 "모두 남는다"와 똑같았습니다.'],['a','λ를 키우면(=C를 줄이면) 몇 명이 틀려도 여백을 넓게 잡아요. 좁은 여백은 학습 데이터에 딱 맞추지만 새 고객에 약할 수 있습니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 7-① 혼동행렬과 임계값 (여행자 보험 청구, 실제 데이터) ── */
function cmCalc(m){var n=m.tp+m.fp+m.fn+m.tn,acc=(m.tp+m.tn)/n,pre=m.tp/(m.tp+m.fp||1),rec=m.tp/(m.tp+m.fn||1),f1=pre+rec?2*pre*rec/(pre+rec):0;return {acc:acc,pre:pre,rec:rec,f1:f1,fpr:m.fp/(m.fp+m.tn||1)}}
SIMS.cm=function(el,cfg){var tw=tbl(el),c=S0(el,cfg,200,'정확도·정밀도·재현율·F1 막대'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),ti=3,T=FD.travel.cms;
  slider(row,'"청구한다"로 부를 기준(임계값)',0,T.length-1,1,ti,function(i){return pct(T[i].th,1)},function(i){ti=i;draw()});
  function draw(){var m=T[ti],s=cmCalc(m);tw.innerHTML='<table class="tb cm"><tr><th></th><th>예측: 청구</th><th>예측: 청구 안 함</th></tr><tr><th>실제: 청구</th><td class="g">TP '+nf(m.tp)+'</td><td class="r">FN '+nf(m.fn)+'</td></tr><tr><th>실제: 청구 안 함</th><td class="a">FP '+nf(m.fp)+'</td><td class="g">TN '+nf(m.tn)+'</td></tr></table>';
    var W=fit(c,200),ctx=c.getContext('2d');ctx.clearRect(0,0,W,200);grid(ctx,W,200);var it=[['정확도',s.acc,COL.s],['정밀도',s.pre,COL.a],['재현율',s.rec,COL.r],['F1',s.f1,COL.g]],L=70,pw=W-L-60;
    it.forEach(function(x,i){var y=18+i*44;ctx.fillStyle=x[2];ctx.fillRect(L,y,x[1]*pw,28);txt(ctx,x[0],L-8,y+19,COL.text,12,'right',true);txt(ctx,pct(x[1],1),L+x[1]*pw+6,y+19,COL.text,12,'left',true)});stamp(ctx,W,REAL);
    K([[pct(s.acc,1),'정확도','i'],[pct(s.pre,1),'정밀도 TP÷(TP+FP)','a'],[pct(s.rec,1),'재현율 TP÷(TP+FN)','r'],[pct(s.f1,1),'F1','g']]);
    E('재현율 = TP ÷ (TP + FN) = '+m.tp+' ÷ ('+m.tp+' + '+m.fn+') = <i>'+pct(s.rec,1)+'</i> · 시험 데이터 '+nf(FD.travel.nte)+'건 중 실제 청구 '+FD.travel.pos_te+'건');
    I([[s.rec<.2?'r':'g',s.rec<.2?'기준을 높이면 거의 아무도 "청구"로 부르지 않아요. 정확도는 98%대로 높지만 실제 청구를 거의 다 놓칩니다(FN).':'기준을 낮추면 청구를 많이 잡지만(재현율↑), 청구하지 않을 사람까지 의심하게 돼요(FP↑, 정밀도↓).'],['a','청구 비율이 '+pct(FD.travel.rate,1)+'뿐이라 정확도만 보면 속기 쉬워요. 보험사가 FN(놓친 청구)과 FP(괜한 조사) 중 무엇이 더 비싼지 정해야 기준을 고를 수 있습니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 7-② ROC 곡선 ── */
SIMS.roc=function(el,cfg){var c=S0(el,cfg,300,'ROC 곡선과 지금 임계값의 점'),row=ctrlRow(el),K=kpis(el,3),E=eqline(el),I=insight(el),ti=3,T=FD.travel.cms;
  slider(row,'임계값',0,T.length-1,1,ti,function(i){return pct(T[i].th,1)},function(i){ti=i;draw()});
  function draw(){var W=fit(c,300),ctx=c.getContext('2d');ctx.clearRect(0,0,W,300);grid(ctx,W,300);var S=Math.min(W-80,260),F=frame(ctx,S+70,300,{xlo:0,xhi:1,ylo:0,yhi:1,fx:function(v){return pct(v,0)},fy:function(v){return pct(v,0)},xl:'FPR (괜히 의심한 비율)',yl:'TPR (재현율)'});
    ctx.fillStyle='rgba(19,138,82,.10)';ctx.beginPath();ctx.moveTo(F.X(0),F.Y(0));FD.travel.roc.forEach(function(p){ctx.lineTo(F.X(p[0]),F.Y(p[1]))});ctx.lineTo(F.X(1),F.Y(0));ctx.closePath();ctx.fill();
    ctx.strokeStyle=COL.g;ctx.lineWidth=2.4;ctx.beginPath();FD.travel.roc.forEach(function(p,i){i?ctx.lineTo(F.X(p[0]),F.Y(p[1])):ctx.moveTo(F.X(p[0]),F.Y(p[1]))});ctx.stroke();
    ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.muted;ctx.beginPath();ctx.moveTo(F.X(0),F.Y(0));ctx.lineTo(F.X(1),F.Y(1));ctx.stroke();ctx.restore();
    var s=cmCalc(T[ti]);dot(ctx,F.X(s.fpr),F.Y(s.rec),7,COL.r,'#fff');txt(ctx,'AUC = '+FD.travel.auc.toFixed(3),F.X(.55),F.Y(.25),COL.g,13,'left',true);txt(ctx,'찍기(대각선)',F.X(.62),F.Y(.58),COL.muted,11,'left');stamp(ctx,W,REAL);
    K([[FD.travel.auc.toFixed(3),'AUC (곡선 아래 넓이)','g'],[pct(s.rec,1),'지금 점의 TPR','r'],[pct(s.fpr,1),'지금 점의 FPR','a']]);
    E('AUC = 무작위로 고른 "청구 고객"의 점수가 "비청구 고객"보다 높을 확률 ≈ <i>'+pct(FD.travel.auc,1)+'</i>');
    I([['g','임계값을 바꾸면 빨간 점이 곡선 위를 움직여요. 곡선 하나에 모든 임계값의 성적이 다 들어 있습니다.'],['a','대각선은 동전 던지기 수준(AUC 0.5)이에요. AUC는 임계값을 고르기 전의 "모델 자체의 가려내는 힘"을 비교할 때 씁니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 7-③ 교차검증과 앙상블 ── */
SIMS.cv=function(el,cfg){var c=S0(el,cfg,250,'한 번 나눈 시험 20번의 정확도 점과 5겹 교차검증'),row=ctrlRow(el),K=kpis(el,4),I=insight(el),show=20;
  slider(row,'한 번 나눠 본 횟수',1,20,1,show,function(v){return v+'번'},function(v){show=v;draw()});
  function draw(){var W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);var S=FD.cv.singles.slice(0,show),F=frame(ctx,W,250,{xlo:0,xhi:21,ylo:.88,yhi:.97,fy:function(v){return pct(v,0)},fx:function(v){return v>0&&v<21?String(v):''},xl:'몇 번째 무작위 분할'});
    S.forEach(function(v,i){dot(ctx,F.X(i+1),F.Y(v),5,C0)});ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.g;ctx.beginPath();ctx.moveTo(F.L,F.Y(FD.cv.cv_mean));ctx.lineTo(F.L+F.pw,F.Y(FD.cv.cv_mean));ctx.stroke();ctx.restore();
    txt(ctx,'5겹 교차검증 평균 '+pct(FD.cv.cv_mean,1),F.L+6,F.Y(FD.cv.cv_mean)-6,COL.g,11,'left',true);
    [[FD.cv.tree,'결정나무 1그루',COL.a],[FD.cv.forest,'랜덤 포레스트 200그루',COL.m]].forEach(function(x){ctx.save();ctx.strokeStyle=x[2];ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(F.L,F.Y(x[0]));ctx.lineTo(F.L+F.pw,F.Y(x[0]));ctx.stroke();ctx.restore();txt(ctx,x[1]+' '+pct(x[0],1)+' (14개 특성)',F.L+F.pw-4,F.Y(x[0])-6,x[2],11,'right',true)});stamp(ctx,W,REAL);
    var lo=Math.min.apply(null,S),hi=Math.max.apply(null,S);
    K([[pct(lo,1)+'~'+pct(hi,1),'한 번 나눌 때 나온 범위 (KNN)','a'],[pct(FD.cv.cv_mean,1)+' ± '+pct(FD.cv.cv_sd,1),'5겹 교차검증 평균 ± 표준편차','g'],[pct(FD.cv.tree,1),'결정나무 1그루','i'],[pct(FD.cv.forest,1),'랜덤 포레스트(앙상블)','m']]);
    I([['g','같은 모델인데도 어떻게 나누느냐에 따라 정확도가 '+pct(hi-lo,1)+'p 오르내려요. 교차검증은 다섯 번 돌아가며 시험을 봐서 그 평균으로 판단합니다.'],['a','여러 나무의 다수결(랜덤 포레스트)이 한 그루보다 '+pct(FD.cv.forest-FD.cv.tree,1)+'p 높았어요. 앙상블은 개별 모델의 실수를 서로 상쇄합니다. 대신 왜 그렇게 판단했는지 설명하기는 더 어려워져요.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 9-① KNN 회귀 vs 선형 회귀: 연봉 → 소비액 (DirectMarketing) ── */
SIMS.knnreg=function(el,cfg){var c=S0(el,cfg,290,'연봉과 소비액 산점도, KNN 회귀 곡선과 직선'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),k=5,qx=150;var S=FD.dm_s;
  slider(row,'이웃 수 k',1,40,1,k,function(v){return 'k = '+v},function(v){k=v;draw()});slider(row,'예측할 연봉',10,200,5,qx,function(v){return nf(v)+'천 달러'},function(v){qx=v;draw()});
  function kp(x){var d=S.x.map(function(v,i){return [Math.abs(v-x),S.y[i]]}).sort(function(a,b){return a[0]-b[0]}).slice(0,k);return mean(d.map(function(z){return z[1]}))}
  function draw(){var W=fit(c,290),ctx=c.getContext('2d');ctx.clearRect(0,0,W,290);grid(ctx,W,290);var F=frame(ctx,W,290,{xlo:0,xhi:200,ylo:0,yhi:6500,fx:String,fy:function(v){return nf(v)},xl:'연봉(천 달러)',yl:'연간 소비액($)'});
    ctx.fillStyle='rgba(183,120,0,.07)';ctx.fillRect(F.X(170),F.T,F.X(200)-F.X(170),F.ph);txt(ctx,'데이터 밖',F.X(185),F.T+14,COL.a,11,'center',true);
    S.x.forEach(function(x,i){dot(ctx,F.X(x),F.Y(S.y[i]),2.6,C0)});
    ctx.strokeStyle=COL.r;ctx.lineWidth=2.2;ctx.beginPath();for(var x=10;x<=200;x+=2){var y=kp(x);x===10?ctx.moveTo(F.X(x),F.Y(y)):ctx.lineTo(F.X(x),F.Y(y))}ctx.stroke();
    var a=FD.dm.lin_coef,b0=FD.dm.lin_b0;ctx.strokeStyle=COL.g;ctx.beginPath();ctx.moveTo(F.X(0),F.Y(b0));ctx.lineTo(F.X(200),F.Y(b0+a*200));ctx.stroke();
    var pk=kp(qx),pl=b0+a*qx;dot(ctx,F.X(qx),F.Y(pk),6,COL.r,'#fff');dot(ctx,F.X(qx),F.Y(pl),6,COL.g,'#fff');
    txt(ctx,'— KNN 회귀',F.L+8,F.T+4,COL.r,11,'left',true);txt(ctx,'— 선형 회귀',F.L+100,F.T+4,COL.g,11,'left',true);stamp(ctx,W,REAL+' 300명');
    K([['$'+nf(pk),'KNN 예측 (연봉 '+qx+'천)','r'],['$'+nf(pl),'선형 회귀 예측','g'],[FD.dm.knn_r2.toFixed(2)+' / '+FD.dm.lin_r2.toFixed(2),'시험 R² (KNN k=5 / 선형)','i'],['$'+nf(FD.dm.lin_coef,1),'연봉 1천 달러당 소비 증가','a']]);
    E('선형 회귀: 소비액 = <b>'+FD.dm.lin_coef.toFixed(1)+'</b> × 연봉(천 달러) + ('+FD.dm.lin_b0.toFixed(0)+') → '+qx+'천 달러면 <i>$'+nf(pl)+'</i>');
    I([[qx>170?'r':'g',qx>170?'데이터 밖(연봉 170천 달러 이상)에서 KNN 곡선은 평평해져요. 이웃이 모두 "지금까지 본 가장 높은 연봉" 고객들이라, 그 이상으로 예측하지 못합니다.':'데이터가 많은 구간에서는 KNN과 직선이 비슷하게 따라가요. KNN은 이웃의 평균을, 선형 회귀는 직선 하나를 씁니다.'],['a','k를 1로 줄이면 KNN 곡선이 들쭉날쭉해져요. 학습 R²는 높아지지만 새 고객에게는 약해지는 과대적합입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 9-② 직선 vs 곡선: 나이 → 보험료 (다항 회귀, 브라우저에서 최소제곱) ── */
function lsq(X,y){/* 정규방정식, 작은 차수 */var p=X[0].length,A=seg(p).map(function(){return new Array(p).fill(0)}),b=new Array(p).fill(0);X.forEach(function(r,i){for(var a=0;a<p;a++){b[a]+=r[a]*y[i];for(var c=0;c<p;c++)A[a][c]+=r[a]*r[c]}});
  for(var i=0;i<p;i++){var mx=i;for(var j=i+1;j<p;j++)if(Math.abs(A[j][i])>Math.abs(A[mx][i]))mx=j;var t=A[i];A[i]=A[mx];A[mx]=t;var tb=b[i];b[i]=b[mx];b[mx]=tb;for(j=i+1;j<p;j++){var f=A[j][i]/A[i][i];for(var c=i;c<p;c++)A[j][c]-=f*A[i][c];b[j]-=f*b[i]}}
  var x=new Array(p).fill(0);for(i=p-1;i>=0;i--){var s=b[i];for(j=i+1;j<p;j++)s-=A[i][j]*x[j];x[i]=s/A[i][i]}return x}
SIMS.polyfit=function(el,cfg){var c=S0(el,cfg,290,'나이와 보험료 산점도에 직선·곡선 맞추기'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),deg=1,grp='all';var S=FD.ins_s;
  buttons(row,'차수',[[1,'1차 (직선)'],[2,'2차'],[3,'3차'],[8,'8차']],deg,function(v){deg=v;draw()});buttons(row,'고객',[['all','전체'],['no','비흡연자만']],grp,function(v){grp=v;draw()});
  function draw(){var idx=seg(S.age.length).filter(function(i){return grp==='all'||!S.sm[i]}),tr=idx.filter(function(i,k){return k%4}),te=idx.filter(function(i,k){return !(k%4)});
    function row_(a){var z=(a-40)/15,r=[1];for(var d=1;d<=deg;d++)r.push(Math.pow(z,d));return r}
    var w=lsq(tr.map(function(i){return row_(S.age[i])}),tr.map(function(i){return S.ch[i]})),P=function(a){return row_(a).reduce(function(s,v,j){return s+v*w[j]},0)};
    function r2(I_){var y=I_.map(function(i){return S.ch[i]}),m=mean(y),ss=0,se=0;I_.forEach(function(i){ss+=(S.ch[i]-m)*(S.ch[i]-m);se+=(S.ch[i]-P(S.age[i]))*(S.ch[i]-P(S.age[i]))});return 1-se/ss}
    var W=fit(c,290),ctx=c.getContext('2d');ctx.clearRect(0,0,W,290);grid(ctx,W,290);var F=frame(ctx,W,290,{xlo:17,xhi:65,ylo:0,yhi:65000,fx:String,fy:function(v){return nf(v/1000)+'천'},xl:'나이',yl:'연간 보험료($)'});
    idx.forEach(function(i){dot(ctx,F.X(S.age[i]),F.Y(S.ch[i]),2.8,S.sm[i]?C1:C0)});
    ctx.save();ctx.beginPath();ctx.rect(F.L,F.T,F.pw,F.ph);ctx.clip();ctx.strokeStyle=COL.g;ctx.lineWidth=2.6;ctx.beginPath();for(var a=18;a<=64;a+=.5){a===18?ctx.moveTo(F.X(a),F.Y(P(a))):ctx.lineTo(F.X(a),F.Y(P(a)))}ctx.stroke();ctx.restore();
    txt(ctx,'● 비흡연',F.L+8,F.T+4,COL.s,11,'left',true);txt(ctx,'● 흡연',F.L+70,F.T+4,COL.r,11,'left',true);stamp(ctx,W,REAL+' 400명');
    var a=r2(tr),b=r2(te);K([[a.toFixed(3),'학습 R²','r'],[b.toFixed(3),'시험 R²','g'],[deg+'차',deg===1?'직선':'곡선','i'],[nf(idx.length)+'명','쓴 고객','a']]);
    E(deg===1?'보험료 = a × 나이 + b':'보험료 = b + a₁·나이 + a₂·나이² '+(deg>2?'+ … + a'+deg+'·나이^'+deg:''));
    I([[grp==='all'?'r':'g',grp==='all'?'전체 고객은 보험료가 세 띠로 갈라져 있어요(흡연·비만). 나이만으로는 차수를 올려도 R²가 크게 오르지 않습니다. 빠진 특성(흡연)이 문제예요 → 10회차 특성공학.':'비흡연자만 보면 나이가 들수록 보험료가 살짝 휘어 오르며 늘어요. 2차 곡선이 직선보다 잘 맞습니다.'],[deg>=8?'r':'a',deg>=8?'8차 곡선은 학습 데이터 끝부분에서 크게 휘어요. 학습 R²에 비해 시험 R²가 따라오지 않으면 과대적합이에요.':'차수를 올리면 학습 R²는 늘 오르거나 같아요. 시험 R²가 함께 오를 때만 의미가 있습니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 9-③ 오차 지표: 내가 그은 직선의 MSE·RMSE·MAE·R² ── */
SIMS.metrics=function(el,cfg){var c=S0(el,cfg,290,'내가 그은 직선과 잔차'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),a=15,b=200,outl=0,p=1;var S0_=FD.dm_s;
  slider(row,'기울기 a',0,40,1,a,function(v){return v},function(v){a=v;draw()});slider(row,'절편 b',-800,1200,50,b,function(v){return nf(v)},function(v){b=v;draw()});
  buttons(row,'이상치',[[0,'없음'],[1,'소비 $30,000 고객 1명 추가']],0,function(v){outl=v;draw()});slider(row,'넣은 특성 수 p (수정 R²용)',1,20,1,p,function(v){return v+'개'},function(v){p=v;draw()});
  function draw(){var X=S0_.x.slice(0,120),Y=S0_.y.slice(0,120);if(outl){X=X.concat([60]);Y=Y.concat([30000])}var n=X.length;
    var e=X.map(function(x,i){return Y[i]-(a*x+b)}),mse=mean(e.map(function(v){return v*v})),mae=mean(e.map(Math.abs)),m=mean(Y),sst=mean(Y.map(function(v){return (v-m)*(v-m)})),r2=1-mse/sst,adj=1-(1-r2)*(n-1)/(n-p-1);
    var W=fit(c,290),ctx=c.getContext('2d');ctx.clearRect(0,0,W,290);grid(ctx,W,290);var F=frame(ctx,W,290,{xlo:0,xhi:140,ylo:0,yhi:5000,fx:String,fy:nf,xl:'연봉(천 달러)',yl:'소비액($)'});
    ctx.save();ctx.beginPath();ctx.rect(F.L,F.T,F.pw,F.ph);ctx.clip();X.forEach(function(x,i){ctx.strokeStyle='rgba(210,63,44,.35)';ctx.beginPath();ctx.moveTo(F.X(x),F.Y(Y[i]));ctx.lineTo(F.X(x),F.Y(a*x+b));ctx.stroke();dot(ctx,F.X(x),F.Y(Y[i]),3,C0)});
    ctx.strokeStyle=COL.g;ctx.lineWidth=2.6;ctx.beginPath();ctx.moveTo(F.X(0),F.Y(b));ctx.lineTo(F.X(140),F.Y(a*140+b));ctx.stroke();ctx.restore();if(outl)txt(ctx,'↑ $30,000 고객(그림 밖)',F.X(60),F.T+12,COL.r,11,'center',true);stamp(ctx,W,REAL+' 120명');
    K([[nf(Math.round(mse)),'MSE (오차² 평균)','r'],['$'+nf(Math.round(Math.sqrt(mse))),'RMSE (√MSE)','a'],['$'+nf(Math.round(mae)),'MAE (|오차| 평균)','i'],[r2.toFixed(3)+' / '+adj.toFixed(3),'R² / 수정 R²','g']]);
    E('R² = 1 − SSE ÷ SST = 1 − '+nf(Math.round(mse*n))+' ÷ '+nf(Math.round(sst*n))+' = <i>'+r2.toFixed(3)+'</i> · 수정 R² = 1 − (1 − R²)(n − 1)/(n − p − 1)');
    I([[outl?'r':'g',outl?'고객 1명을 더했을 뿐인데 RMSE가 크게 뛰어요. 오차를 제곱하는 MSE·RMSE는 큰 오차 하나에 민감하고, MAE는 덜 민감합니다.':'기울기와 절편을 움직여 빨간 잔차의 합이 줄어드는 곳을 찾아보세요. 컴퓨터는 이 MSE가 가장 작은 직선을 계산으로 바로 찾습니다(최소제곱).'],['a','특성 수 p를 늘리면 수정 R²가 R²보다 낮아져요. 쓸모없는 특성을 많이 넣어 R²를 부풀리는 것을 벌주는 지표입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 10-① 로지스틱: 거래 횟수 → 이탈 확률 ── */
SIMS.logit=function(el,cfg){var c=S0(el,cfg,270,'거래 횟수 구간별 실제 이탈률과 로지스틱 곡선'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),x=45,th=.5;var L=FD.logit;
  slider(row,'거래 횟수',10,140,1,x,function(v){return v+'회'},function(v){x=v;draw()});slider(row,'"이탈"로 부를 기준',.1,.9,.05,th,function(v){return pct(v,0)},function(v){th=v;draw()});
  function p(v){return 1/(1+Math.exp(-(L.w*v+L.b0)))}
  function draw(){var W=fit(c,270),ctx=c.getContext('2d');ctx.clearRect(0,0,W,270);grid(ctx,W,270);var F=frame(ctx,W,270,{xlo:10,xhi:140,ylo:0,yhi:1,fx:String,fy:function(v){return pct(v,0)},xl:'연간 거래 횟수',yl:'이탈 확률'});
    L.bins.forEach(function(b_){var x0=F.X(b_[0]),x1=F.X(b_[1]);ctx.fillStyle='rgba(210,63,44,.18)';ctx.fillRect(x0+1,F.Y(b_[2]),x1-x0-2,F.Y(0)-F.Y(b_[2]))});
    ctx.strokeStyle=COL.s;ctx.lineWidth=2.6;ctx.beginPath();for(var v=10;v<=140;v++){v===10?ctx.moveTo(F.X(v),F.Y(p(v))):ctx.lineTo(F.X(v),F.Y(p(v)))}ctx.stroke();
    ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.a;ctx.beginPath();ctx.moveTo(F.L,F.Y(th));ctx.lineTo(F.L+F.pw,F.Y(th));ctx.stroke();ctx.restore();
    var cut=(Math.log(th/(1-th))-L.b0)/L.w;dot(ctx,F.X(x),F.Y(p(x)),7,COL.r,'#fff');txt(ctx,'■ 실제 이탈률(구간)',F.L+8,F.T+4,COL.r,11,'left',true);txt(ctx,'— 로지스틱 곡선',F.L+130,F.T+4,COL.s,11,'left',true);stamp(ctx,W,REAL+' 10,127명');
    var z=L.w*x+L.b0;K([[pct(p(x),1),'예측 이탈 확률','r'],[p(x)>=th?'이탈':'유지','기준 '+pct(th,0)+'에서 판정','g'],[z.toFixed(2),'z (직선 부분)','i'],[cut>10?Math.round(cut)+'회 미만':'—','이 기준에서 "이탈"이 되는 거래 횟수','a']]);
    E('z = '+L.w.toFixed(4)+' × '+x+' + '+L.b0.toFixed(3)+' = '+z.toFixed(2)+' → 확률 = 1 ÷ (1 + e<sup>−z</sup>) = <i>'+pct(p(x),1)+'</i>');
    I([['g','직선(z)을 시그모이드에 넣으면 0~1 사이 확률이 돼요. 그래서 이름은 "회귀"지만 분류에 씁니다.'],['a','실제 이탈률(빨간 막대)은 40~50회 구간에서 오히려 솟아요. 특성 하나짜리 매끈한 S자 곡선은 이 굴곡을 못 따라갑니다. 결정나무(단계 ②)는 구간을 잘라 이런 굴곡을 잡아요.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 10-② 결정나무: 깊이별 잎 (실제 데이터에서 sklearn으로 학습한 결과) ── */
SIMS.tree=function(el,cfg){var c=S0(el,cfg,300,'거래 횟수·회전 잔액 평면을 나무가 자른 구역'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),d=1;var T=FD.tree,S=T.sample;
  buttons(row,'깊이',[[1,'1'],[2,'2'],[3,'3'],[4,'4']],d,function(v){d=v;draw()});
  function draw(){var W=fit(c,300),ctx=c.getContext('2d');ctx.clearRect(0,0,W,300);grid(ctx,W,300);var F=frame(ctx,W,300,{xlo:10,xhi:140,ylo:0,yhi:2600,fx:String,fy:nf,xl:'연간 거래 횟수',yl:'회전 잔액($)'});
    T.leaves[d].forEach(function(l){var x0=F.X(Math.max(10,l[0])),x1=F.X(Math.min(140,l[2])),y0=F.Y(Math.min(2600,l[3])),y1=F.Y(Math.max(0,l[1]));ctx.fillStyle=l[4]>.5?'rgba(210,63,44,'+(.10+.3*l[4])+')':'rgba(63,95,168,'+(.06+.2*(1-l[4]))+')';ctx.fillRect(x0,y0,x1-x0,y1-y0);ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.strokeRect(x0,y0,x1-x0,y1-y0);if(x1-x0>38&&y1-y0>18)txt(ctx,pct(l[4],0),(x0+x1)/2,(y0+y1)/2+4,COL.text,11,'center',true)});
    S.x.forEach(function(x,i){dot(ctx,F.X(x),F.Y(S.y[i]),2.4,S.t[i]?C1:C0)});stamp(ctx,W,REAL);
    var A=T.depth[d],R=T.root;K([[pct(A[0],1),'학습 정확도','r'],[pct(A[1],1),'시험 정확도','g'],[A[2]+'개','잎(마지막 구역) 수','i'],[pct(T.depth['None'][1],1),'끝까지 자란 나무의 시험 정확도','a']]);
    E('첫 질문: 거래 횟수 ≤ '+R.th+'회? → 예: '+nf(R.nl)+'명(이탈 '+pct(R.left_rate,0)+', 지니 '+R.left_gini+') / 아니오: '+nf(R.nr)+'명(이탈 '+pct(R.right_rate,0)+', 지니 '+R.right_gini+') · 처음 지니 '+R.gini);
    I([['g','나무는 "어디서 자르면 양쪽이 가장 깨끗해질까(지니 불순도↓)"를 묻는 질문을 반복해요. 구역 숫자는 그 구역의 이탈 고객 비율입니다.'],[d>=4?'a':'g',d>=4?'깊이를 더 키우면 학습 정확도는 오르지만 시험 정확도는 '+pct(T.depth['6'][1],1)+' 근처에서 멈췄다가, 끝까지 자라면 '+pct(T.depth['None'][1],1)+'로 떨어져요(과대적합). 그래서 max_depth로 가지치기를 합니다.':'깊이 2만으로 "거래가 적고 잔액도 적은 고객" 구역이 따로 생겨요. 로지스틱 곡선이 못 잡던 굴곡입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 10-③ 특성공학: 보험료 예측에 특성 더하기 (실제 결과) ── */
SIMS.features=function(el,cfg){var c=S0(el,cfg,250,'특성 조합별 시험 R² 막대'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),k=2;var FE=FD.fe,names=Object.keys(FE);
  slider(row,'특성 조합',0,names.length-1,1,k,function(i){return names[i]},function(i){k=i;draw()});
  function draw(){var W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);var L=120,pw=W-L-60;
    names.forEach(function(nm,i){var y=12+i*32,v=FE[nm].r2;ctx.fillStyle=i===k?COL.g:(i<k?C0:'rgba(93,98,120,.18)');ctx.fillRect(L,y,v*pw,22);txt(ctx,nm,L-8,y+16,COL.text,11,'right',i===k);txt(ctx,v.toFixed(3),L+v*pw+6,y+16,COL.text,11,'left',true)});stamp(ctx,W,REAL+' 보험 1,338명');
    var f=FE[names[k]],co=f.coef;K([[f.r2.toFixed(3),'시험 R²','g'],['$'+nf(f.rmse),'RMSE','r'],[Object.keys(co).length+'개','특성 수','i'],[f.adj.toFixed(3),'수정 R²','a']]);
    var lab={age:'나이',age2:'나이²',bmi:'BMI',sm:'흡연',sm_obese:'흡연×비만',sm_bmi:'흡연×BMI',children:'자녀',male:'남성'};
    E('보험료 = '+Object.keys(co).map(function(x,i){var v=co[x];return (i?(v<0?' − ':' + '):(v<0?'−':''))+nf(Math.abs(v),0)+'·'+lab[x]}).join('')+(f.b0<0?' − ':' + ')+nf(Math.abs(f.b0),0));
    I([[k>=4?'g':'a',k>=4?'"흡연이면서 비만(BMI ≥ 30)"이라는 새 특성 하나로 R²가 0.76에서 0.86으로 뛰어요. 흡연자의 보험료는 비만일 때만 크게 오르는데, 두 특성을 따로 넣으면 이 "함께 있을 때" 효과를 표현하지 못하기 때문입니다.':'흡연 여부를 넣는 순간 R²가 0.13에서 0.76으로 크게 뛰어요. 좋은 특성 하나가 모델을 바꿉니다.'],['a','나이² 하나 더한 것은 거의 효과가 없었어요. 특성을 많이 넣는 것보다 데이터를 보고 "이유 있는" 특성을 만드는 것이 특성공학입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 11-① 인공 뉴런 하나 (예시값) ── */
SIMS.neuron=function(el,cfg){var c=S0(el,cfg,240,'입력 두 개, 가중치, 활성화 함수를 거친 출력'),row=ctrlRow(el),K=kpis(el,3),E=eqline(el),I=insight(el),x1=.6,x2=.3,w1=1.5,w2=-2,b=-.2,act='sig';
  slider(row,'입력 x₁ (최근 연체 횟수, 표준화)',-2,2,.1,x1,function(v){return v.toFixed(1)},function(v){x1=v;draw()});slider(row,'입력 x₂ (소득, 표준화)',-2,2,.1,x2,function(v){return v.toFixed(1)},function(v){x2=v;draw()});
  slider(row,'가중치 w₁',-3,3,.1,w1,function(v){return v.toFixed(1)},function(v){w1=v;draw()});slider(row,'가중치 w₂',-3,3,.1,w2,function(v){return v.toFixed(1)},function(v){w2=v;draw()});
  buttons(row,'활성화',[['step','계단'],['sig','시그모이드'],['relu','ReLU']],act,function(v){act=v;draw()});
  function f(z){return act==='step'?(z>0?1:0):act==='sig'?1/(1+Math.exp(-z)):Math.max(0,z)}
  function draw(){var z=w1*x1+w2*x2+b,y=f(z),W=fit(c,240),ctx=c.getContext('2d');ctx.clearRect(0,0,W,240);grid(ctx,W,240);var cx=W*.5;
    [[x1,70,'x₁'],[x2,170,'x₂']].forEach(function(p,i){dot(ctx,70,p[1],22,'#eef1f8',COL.s);txt(ctx,p[2]+'='+p[0].toFixed(1),70,p[1]+4,COL.text,11,'center',true);var w=i?w2:w1;ctx.strokeStyle=w>0?COL.g:COL.r;ctx.lineWidth=1+Math.abs(w)*2;ctx.beginPath();ctx.moveTo(92,p[1]);ctx.lineTo(cx-30,120);ctx.stroke();txt(ctx,'w='+w.toFixed(1),(92+cx-30)/2,p[1]<120?p[1]+18:p[1]-12,w>0?COL.g:COL.r,11,'center',true)});
    dot(ctx,cx,120,30,'#f3edff',COL.doc);txt(ctx,'Σ → '+(act==='sig'?'σ':act==='step'?'계단':'ReLU'),cx,124,COL.doc,12,'center',true);
    ctx.strokeStyle=COL.text;ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(cx+30,120);ctx.lineTo(W-110,120);ctx.stroke();dot(ctx,W-80,120,26,y>.5?'#fde8e6':'#e8f5ee',y>.5?COL.r:COL.g);txt(ctx,y.toFixed(2),W-80,124,COL.text,13,'center',true);stamp(ctx,W,EX);
    K([[z.toFixed(2),'z = w₁x₁ + w₂x₂ + b','i'],[y.toFixed(3),'출력 (활성화 후)','g'],[act==='sig'?(y>.5?'위험':'안전'):(y>0?'신호 전달':'멈춤'),'해석','a']]);
    E('z = '+w1.toFixed(1)+'×'+x1.toFixed(1)+' + ('+w2.toFixed(1)+')×'+x2.toFixed(1)+' + ('+b+') = '+z.toFixed(2)+' → 출력 <i>'+y.toFixed(3)+'</i>');
    I([['g','뉴런 하나는 "입력 × 가중치를 더하고, 기준을 넘으면 신호를 보낸다"가 전부예요. 시그모이드 뉴런 하나는 10회차의 로지스틱 회귀와 같은 식입니다.'],['a','딥러닝은 이런 뉴런을 여러 층으로 쌓고, 가중치를 데이터에서 스스로 찾아요(역전파). 여기 가중치는 손으로 정한 예시값입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 11-② 가격과 수익률: 정상성 (실제 주가) ── */
SIMS.station=function(el,cfg){var c=S0(el,cfg,270,'가격 또는 일간 수익률 선과 네 구간의 평균'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),a='AMZN',m='price';
  buttons(row,'종목',[['AMZN','아마존'],['BTC','비트코인']],a,function(v){a=v;draw()});buttons(row,'보는 값',[['price','가격'],['ret','일간 수익률(차분)']],m,function(v){m=v;draw()});
  function draw(){var P=FD.port[a],y=m==='price'?P:P.slice(1).map(function(v,i){return (Math.log(v)-Math.log(P[i]))*100}),n=y.length,W=fit(c,270),ctx=c.getContext('2d');ctx.clearRect(0,0,W,270);grid(ctx,W,270);
    var lo=Math.min.apply(null,y),hi=Math.max.apply(null,y);if(m==='ret'){lo=Math.max(lo,-15);hi=Math.min(hi,15)}var F=frame(ctx,W,270,{xlo:0,xhi:n,ylo:lo,yhi:hi,fx:function(i){var d=FD.port.dates[Math.min(n-1,Math.round(i))];return d?d.slice(0,4):''},fy:function(v){return m==='price'?nf(v):v.toFixed(0)+'%'}});
    ctx.strokeStyle=m==='price'?COL.s:'rgba(63,95,168,.6)';ctx.lineWidth=m==='price'?1.8:1;ctx.beginPath();y.forEach(function(v,i){var Y=F.Y(clamp(v,lo,hi));i?ctx.lineTo(F.X(i),Y):ctx.moveTo(F.X(i),Y)});ctx.stroke();
    var q=Math.floor(n/4),st=[];for(var k=0;k<4;k++){var s=y.slice(k*q,(k+1)*q),mu=mean(s),sg=sd(s);st.push([mu,sg]);ctx.strokeStyle=COL.r;ctx.lineWidth=2.4;ctx.beginPath();ctx.moveTo(F.X(k*q),F.Y(clamp(mu,lo,hi)));ctx.lineTo(F.X((k+1)*q),F.Y(clamp(mu,lo,hi)));ctx.stroke()}stamp(ctx,W,REAL+' '+FD.port.start.slice(0,4)+'~'+FD.port.end.slice(0,4));
    var fm=function(v){return m==='price'?nf(v):v.toFixed(2)+'%'};K(st.map(function(s,i){return [fm(s[0]),(i+1)+'구간 평균 (σ '+fm(s[1])+')',['i','g','a','r'][i]]}));
    E(m==='price'?'가격 그대로: 구간마다 평균이 '+fm(st[0][0])+' → '+fm(st[3][0])+'로 크게 바뀜':'수익률 = ln(오늘 가격) − ln(어제 가격) · 구간 평균이 모두 0 근처');
    I(m==='price'?[['r','가격은 시간에 따라 평균이 계속 올라가요(추세). 평균과 흩어짐이 시간에 따라 변하는 <b>비정상 시계열</b>입니다.'],['a','비정상 시계열에 그대로 회귀를 돌리면 "함께 오른 두 가격"이 상관이 있는 것처럼 보이는 함정(가짜 회귀)에 빠지기 쉬워요.']]:[['g','하루 변화(차분)로 바꾸면 평균이 0 근처에서 머물러요. 이렇게 평균이 일정한 <b>정상 시계열</b>로 만든 뒤 AR·MA·ARMA를 씁니다(ARIMA의 I = 차분).'],['a','흩어짐(σ)은 구간마다 아직 달라요. 금융 수익률은 출렁임이 몰려 다니는 성질이 있어 완전한 정상 시계열은 아닙니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 11-③ AR 모델: 과거 p일로 내일 가격 (실제 결과) ── */
SIMS.ar=function(el,cfg){var c=S0(el,cfg,270,'시험 기간 120일 실제 가격과 AR 예측 선'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),a='NFLX',lg=5;
  buttons(row,'종목',[['AMZN','아마존'],['NFLX','넷플릭스'],['BTC','비트코인']],a,function(v){a=v;draw()});buttons(row,'과거 며칠 (lags)',[[1,'1'],[2,'2'],[5,'5'],[10,'10'],[20,'20']],lg,function(v){lg=v;draw()});
  function draw(){var R=FD.ar[a][lg],P=FD.port[a],act=P.slice(-120),pr=R.pred,W=fit(c,270),ctx=c.getContext('2d');ctx.clearRect(0,0,W,270);grid(ctx,W,270);
    var lo=Math.min.apply(null,act.concat(pr))*.98,hi=Math.max.apply(null,act.concat(pr))*1.02,F=frame(ctx,W,270,{xlo:0,xhi:119,ylo:lo,yhi:hi,fx:function(i){return i%30?'':(i+1)+'일'},fy:nf,xl:'시험 기간(마지막 120거래일)'});
    [[act,COL.s,2,'실제'],[pr,COL.r,1.6,'AR('+lg+') 예측']].forEach(function(s,si){ctx.strokeStyle=s[1];ctx.lineWidth=s[2];ctx.beginPath();s[0].forEach(function(v,i){i?ctx.lineTo(F.X(i),F.Y(v)):ctx.moveTo(F.X(i),F.Y(v))});ctx.stroke();txt(ctx,'— '+s[3],F.L+8+si*80,F.T+4,s[1],11,'left',true)});stamp(ctx,W,REAL);
    K([[nf(R.mae,1),'AR('+lg+') MAE','r'],[nf(R.naive_mae,1),'"어제 가격 그대로" MAE','g'],[pct(R.mape,2),'AR MAPE','a'],[R.mae<R.naive_mae?'AR':'어제 그대로','더 작은 오차','i']]);
    E('AR('+lg+'): 오늘 가격 = c + φ₁·어제 + φ₂·그제 + … + φ'+lg+'·'+lg+'일 전 (학습: 시험 전 '+nf(P.length-120-lg)+'일)');
    I([[R.mae<R.naive_mae?'g':'r','예측선(빨강)이 실제선(파랑)을 하루 늦게 따라가는 모습이 보여요. 가격의 AR 모델은 결국 "어제 가격 근처"를 말하고, 어제 가격 그대로와 오차가 거의 같습니다.'],['a','방향(오를지 내릴지)을 맞힌 비율은 수익률 AR(5)로도 '+pct(FD.ar_dir[a][0],0)+'였어요. 주가 예측이 어려운 이유이고, 교육용 예시이며 투자 자문이 아닙니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 12-① 대표값과 치우침: 보험료 분포 ── */
SIMS.center=function(el,cfg){var c=S0(el,cfg,260,'보험료 히스토그램과 평균·중앙값'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),lg=0,v=FD.ins.ch;
  buttons(row,'가로축',[[0,'그대로 ($)'],[1,'로그 눈금']],0,function(x){lg=x;draw()});
  function draw(){var y=lg?v.map(Math.log10):v,lo=lg?3:0,hi=lg?4.85:65000,W=fit(c,260),ctx=c.getContext('2d');ctx.clearRect(0,0,W,260);grid(ctx,W,260);
    var F=frame(ctx,W,260,{xlo:lo,xhi:hi,ylo:0,yhi:1,fx:function(x){return lg?'$'+nf(Math.pow(10,x)):nf(x/1000)+'천'},fy:function(){return ''},L:20}),bins=40,cnt=new Array(bins).fill(0);y.forEach(function(x){cnt[clamp(Math.floor((x-lo)/(hi-lo)*bins),0,bins-1)]++});var mx=Math.max.apply(null,cnt);
    cnt.forEach(function(n,i){var x0=F.X(lo+i*(hi-lo)/bins),x1=F.X(lo+(i+1)*(hi-lo)/bins),hh=n/mx*(F.ph-24);ctx.fillStyle=C0;ctx.fillRect(x0+1,F.T+F.ph-hh,x1-x0-2,hh)});
    var mu=mean(v),md=median(v);[[mu,'평균',COL.r],[md,'중앙값',COL.g]].forEach(function(m,i){var X=F.X(lg?Math.log10(m[0]):m[0]);ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=m[2];ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(X,F.T);ctx.lineTo(X,F.T+F.ph);ctx.stroke();ctx.restore();txt(ctx,m[1]+' $'+nf(m[0]),X+(i?-4:4),F.T+12+i*14,m[2],11,i?'right':'left',true)});stamp(ctx,W,REAL+' 1,338명');
    K([['$'+nf(mu),'평균','r'],['$'+nf(md),'중앙값','g'],[FD.ins.skew.toFixed(2),'왜도 (0이면 좌우 대칭)','a'],['$'+nf(sd(v)),'표준편차','i']]);
    E('왜도 '+FD.ins.skew.toFixed(2)+' &gt; 0 → 오른쪽 꼬리가 긴 분포 → 평균($'+nf(mu)+') &gt; 중앙값($'+nf(md)+')');
    I([['g','소수의 아주 큰 보험료(흡연·비만 고객)가 평균을 오른쪽으로 끌어당겨요. "보통 고객"을 말할 때는 중앙값이 더 대표적입니다.'],['a',lg?'로그 눈금으로 보면 꼬리가 접혀 봉우리가 여럿(비흡연·흡연·흡연+비만)인 것이 더 잘 보여요.':'로그 눈금 버튼을 눌러 보세요. 오른쪽으로 길게 늘어진 분포는 로그로 보면 모양이 더 잘 보입니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 12-② 상관관계 히트맵 (실제 수익률) ── */
SIMS.corr=function(el,cfg){var c=S0(el,cfg,300,'수익률 상관계수 히트맵'),row=ctrlRow(el),K=kpis(el,3),E=eqline(el),I=insight(el),set='us';
  buttons(row,'자산 묶음',[['us','미국 주식·비트코인 (2013~2019)'],['intl','국제 지표 (2020)']],set,function(v){set=v;draw()});
  function draw(){var M=set==='us'?FD.port.corr:FD.intl.corr,N=set==='us'?['아마존','도미노','비트코인','넷플릭스']:FD.intl.names,n=N.length,W=fit(c,300),ctx=c.getContext('2d');ctx.clearRect(0,0,W,300);
    var S=Math.min((W-110)/n,(270-20)/n),x0=90,y0=24;for(var i=0;i<n;i++){txt(ctx,N[i],x0-6,y0+i*S+S/2+4,COL.text,11,'right',true);txt(ctx,N[i],x0+i*S+S/2,y0-6,COL.text,10,'center',true);for(var j=0;j<n;j++){var v=M[i][j];ctx.fillStyle=v>=0?'rgba(210,63,44,'+Math.abs(v)*.85+')':'rgba(37,99,201,'+Math.abs(v)*.85+')';ctx.fillRect(x0+j*S+1,y0+i*S+1,S-2,S-2);txt(ctx,v.toFixed(2),x0+j*S+S/2,y0+i*S+S/2+4,Math.abs(v)>.55?'#fff':COL.text,11,'center',true)}}stamp(ctx,W,REAL);
    var pr=[];for(i=0;i<n;i++)for(j=i+1;j<n;j++)pr.push([M[i][j],N[i]+'–'+N[j]]);pr.sort(function(a,b){return b[0]-a[0]});
    K([[pr[0][1]+' '+pr[0][0].toFixed(2),'가장 강한 양의 상관','r'],[pr[pr.length-1][1]+' '+pr[pr.length-1][0].toFixed(2),'가장 강한 음의 상관','i'],[n+'개','자산 수','a']]);
    E('상관계수 r = 공분산 ÷ (σ<sub>X</sub> × σ<sub>Y</sub>), −1 ≤ r ≤ 1 · 일간 수익률로 계산');
    I(set==='us'?[['g','미국 주식끼리도 일간 수익률 상관은 0.2~0.4 정도예요. 비트코인은 주식과 거의 따로 움직였습니다(0 근처).'],['a','가격 자체로 상관을 재면 함께 오른 추세 때문에 0.9 가까이 나와요(11회차 비정상 시계열). 상관은 수익률로 재야 합니다.']]:[['g','다우지수와 VIX(공포지수)는 강한 음의 상관이에요. 주가가 떨어질 때 불안이 커지는 관계입니다.'],['r','상관은 인과가 아니에요. 원인을 말하려면 실험(A/B 테스트)이나 시간 순서·다른 요인 통제가 필요합니다. 원자료에는 결측이 많아(DOW '+FD.intl.missing.DOW+'행) 결측을 뺀 '+FD.intl.n+'일로 계산했어요.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 12-③ 목적에 맞는 차트 고르기 (실제 데이터) ── */
SIMS.chartpick=function(el,cfg){var c=S0(el,cfg,270,'고른 목적에 맞춰 그린 차트'),row=ctrlRow(el),K=kpis(el,2),I=insight(el),p='trend';
  buttons(row,'보여 주고 싶은 것',[['trend','시간에 따른 변화'],['comp','항목 비교'],['part','구성 비율'],['dist','분포·흩어짐'],['rel','두 변수의 관계']],p,function(v){p=v;draw()});
  function draw(){var W=fit(c,270),ctx=c.getContext('2d');ctx.clearRect(0,0,W,270);grid(ctx,W,270);var A=['AMZN','DPZ','NFLX'],cols=[COL.s,COL.a,COL.r],nm={AMZN:'아마존',DPZ:'도미노',NFLX:'넷플릭스'};
    if(p==='trend'){var F=frame(ctx,W,270,{xlo:0,xhi:FD.port.AMZN.length,ylo:0,yhi:14,fx:function(i){var d=FD.port.dates[Math.round(i)];return d?d.slice(0,4):''},fy:function(v){return v+'배'}});A.forEach(function(a,k){var P=FD.port[a];ctx.strokeStyle=cols[k];ctx.lineWidth=2;ctx.beginPath();P.forEach(function(v,i){i?ctx.lineTo(F.X(i),F.Y(v/P[0])):ctx.moveTo(F.X(i),F.Y(v/P[0]))});ctx.stroke();txt(ctx,'— '+nm[a],F.L+8+k*70,F.T+4,cols[k],11,'left',true)})}
    if(p==='comp'){var mu=A.map(function(a){return FD.port.mu[a]}),L=90,pw=W-L-60;A.forEach(function(a,k){var y=40+k*64;ctx.fillStyle=cols[k];ctx.fillRect(L,y,mu[k]/.6*pw,36);txt(ctx,nm[a],L-8,y+23,COL.text,12,'right',true);txt(ctx,pct(mu[k],0),L+mu[k]/.6*pw+6,y+23,COL.text,12,'left',true)});txt(ctx,'연평균 수익률(단순 평균×252)',L,20,COL.muted,11,'left')}
    if(p==='part'){var w=[.4,.3,.3],a0=-Math.PI/2,cx=W/2,cy=140,R=100;w.forEach(function(x,k){ctx.fillStyle=cols[k];ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,R,a0,a0+x*Math.PI*2);ctx.closePath();ctx.fill();var m=a0+x*Math.PI;txt(ctx,nm[A[k]]+' '+pct(x,0),cx+Math.cos(m)*(R+30),cy+Math.sin(m)*(R+18)+4,COL.text,12,'center',true);a0+=x*Math.PI*2});txt(ctx,'예시 포트폴리오 비중',12,20,COL.muted,11,'left')}
    if(p==='dist'){var L2=90,pw2=W-L2-30,X=function(v){return L2+(v+.08)/.16*pw2};A.forEach(function(a,k){var P=FD.port[a],r=P.slice(1).map(function(v,i){return v/P[i]-1}),q=[.05,.25,.5,.75,.95].map(function(z){return quant(r,z)}),y=50+k*70;ctx.strokeStyle=cols[k];ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(X(q[0]),y);ctx.lineTo(X(q[4]),y);ctx.stroke();ctx.fillStyle='rgba(255,255,255,.9)';ctx.fillRect(X(q[1]),y-16,X(q[3])-X(q[1]),32);ctx.strokeRect(X(q[1]),y-16,X(q[3])-X(q[1]),32);ctx.beginPath();ctx.moveTo(X(q[2]),y-16);ctx.lineTo(X(q[2]),y+16);ctx.stroke();txt(ctx,nm[a],L2-8,y+4,COL.text,12,'right',true)});[-.08,-.04,0,.04,.08].forEach(function(t){txt(ctx,pct(t,0),X(t),250,COL.muted,10,'center')});txt(ctx,'일간 수익률 상자그림 (5%~95% 수염)',L2,20,COL.muted,11,'left')}
    if(p==='rel'){var Pa=FD.port.AMZN,Pn=FD.port.NFLX,ra=Pa.slice(1).map(function(v,i){return v/Pa[i]-1}),rn=Pn.slice(1).map(function(v,i){return v/Pn[i]-1}),F2=frame(ctx,W,270,{xlo:-.1,xhi:.1,ylo:-.1,yhi:.1,fx:function(v){return pct(v,0)},fy:function(v){return pct(v,0)},xl:'아마존 일간 수익률',yl:'넷플릭스'});ra.forEach(function(v,i){if(Math.abs(v)<.1&&Math.abs(rn[i])<.1)dot(ctx,F2.X(v),F2.Y(rn[i]),2,'rgba(63,95,168,.35)')})}
    stamp(ctx,W,p==='part'?EX:REAL);var M={trend:['꺾은선','시간 순서가 있는 값은 선으로 이어야 오르내림이 보여요. 처음 가격을 1로 맞춰(정규화) 세 종목을 한 축에 놓았습니다.'],comp:['막대','항목끼리 크기를 비교할 때는 막대가 가장 정확히 읽혀요. 길이로 비교하니까요.'],part:['원(파이)','전체 중 몫을 보여 줄 때만 원을 써요. 조각이 많거나 비슷하면 막대가 더 낫습니다.'],dist:['상자그림','가운데(중앙값)·몸통(50%)·수염으로 흩어짐과 치우침을 한눈에 비교해요. 넷플릭스의 상자가 가장 넓어요.'],rel:['산점도','두 숫자 변수의 관계는 점으로 찍어요. 오른쪽 위로 기운 구름이 약한 양의 상관을 보여 줍니다.']}[p];
    K([[M[0],'고른 차트','g'],[p==='part'?'예시값':'fintech-data 포트폴리오','데이터','a']]);I([['g',M[1]],['a','교안의 캔들스틱·OHLC 차트는 시가·고가·저가·종가가 있어야 그려요. 이 데이터는 종가만 있어 꺾은선으로 대신했습니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 13-① 투자성향 설문 → 자산 배분 ── */
SIMS.profile=function(el,cfg){var tw=tbl(el),c=S0(el,cfg,220,'주식 비중별 기대 수익률·변동성·최대 낙폭'),row=ctrlRow(el),K=kpis(el,4),I=insight(el),ans=cfg.qs.map(function(){return 1});
  function draw(){tw.innerHTML='';cfg.qs.forEach(function(q,qi){var g=h('div',{class:'group'});g.appendChild(h('span',{class:'glabel'},q[0]));q[1].forEach(function(o,oi){var b=h('button',{class:'bt',type:'button','aria-pressed':String(ans[qi]===oi)},o);b.addEventListener('click',function(){ans[qi]=oi;draw()});g.appendChild(b)});tw.appendChild(g)});
    var sc=ans.reduce(function(a,b){return a+b},0),mx=cfg.qs.reduce(function(a,q){return a+q[1].length-1},0),wi=Math.round(sc/mx*5),A=FD.alloc[wi],types=['안정형','안정추구형','위험중립형','적극투자형','공격투자형','공격투자형'];
    var W=fit(c,220),ctx=c.getContext('2d');ctx.clearRect(0,0,W,220);grid(ctx,W,220);var F=frame(ctx,W,220,{xlo:0,xhi:5,ylo:-.35,yhi:.45,fx:function(i){return pct(FD.alloc[Math.round(i)]?FD.alloc[Math.round(i)].w:0,0)},fy:function(v){return pct(v,0)},xl:'주식 비중'});
    [['mu',COL.g,'연 기대 수익률'],['vol',COL.a,'연 변동성'],['mdd',COL.r,'최대 낙폭']].forEach(function(s,si){ctx.strokeStyle=s[1];ctx.lineWidth=2.2;ctx.beginPath();FD.alloc.forEach(function(a,i){i?ctx.lineTo(F.X(i),F.Y(a[s[0]])):ctx.moveTo(F.X(i),F.Y(a[s[0]]))});ctx.stroke();txt(ctx,'— '+s[2],F.L+8+si*100,F.T+4,s[1],11,'left',true)});ctx.save();ctx.setLineDash([4,3]);ctx.strokeStyle=COL.text;ctx.beginPath();ctx.moveTo(F.X(wi),F.T);ctx.lineTo(F.X(wi),F.T+F.ph);ctx.stroke();ctx.restore();stamp(ctx,W,REAL+' 2013~2019');
    K([[types[wi],'투자성향 (점수 '+sc+'/'+mx+')','i'],[pct(A.w,0),'추천 주식 비중','g'],[pct(A.mu,1),'과거 연 수익률(이 기간)','a'],[pct(A.mdd,1),'과거 최대 낙폭','r']]);
    I([['g','설문 점수가 높을수록 주식 비중을 늘리는 단순 규칙이에요. 로보어드바이저는 이 "투자자 정보 확인서"를 데이터로 받아 배분을 정합니다.'],['a','수익률은 미국 주식 세 종목이 크게 오른 2013~2019년의 과거 기록이에요. 미래를 보장하지 않으며, 교육용 예시이고 투자 자문이 아닙니다.']])}
  draw()};

/* ── 13-② 수수료의 복리 효과 (예시값) ── */
SIMS.fee=function(el,cfg){var c=S0(el,cfg,250,'수수료별 자산 성장 선'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),yr=20,r=.05,f1=.3,f2=1.5;
  slider(row,'기간',1,40,1,yr,function(v){return v+'년'},function(v){yr=v;draw()});slider(row,'연 수익률(수수료 전)',0,10,.5,r*100,function(v){return v+'%'},function(v){r=v/100;draw()});slider(row,'로보 수수료',0,1,.05,f1,function(v){return v.toFixed(2)+'%'},function(v){f1=v;draw()});slider(row,'사람 자문 수수료',.5,3,.1,f2,function(v){return v.toFixed(1)+'%'},function(v){f2=v;draw()});
  function draw(){var P=1000,a=seg(yr+1).map(function(t){return P*Math.pow(1+r-f1/100,t)}),b=seg(yr+1).map(function(t){return P*Math.pow(1+r-f2/100,t)}),W=fit(c,250),ctx=c.getContext('2d');ctx.clearRect(0,0,W,250);grid(ctx,W,250);
    var F=frame(ctx,W,250,{xlo:0,xhi:yr,ylo:0,yhi:Math.max(a[yr],1100)*1.05,fx:function(v){return v+'년'},fy:function(v){return nf(v)+'만'}});[[a,COL.g,'로보 '+f1.toFixed(2)+'%'],[b,COL.r,'사람 자문 '+f2.toFixed(1)+'%']].forEach(function(s,si){ctx.strokeStyle=s[1];ctx.lineWidth=2.4;ctx.beginPath();s[0].forEach(function(v,i){i?ctx.lineTo(F.X(i),F.Y(v)):ctx.moveTo(F.X(i),F.Y(v))});ctx.stroke();txt(ctx,'— '+s[2],F.L+8+si*110,F.T+4,s[1],11,'left',true)});stamp(ctx,W,EX);
    K([[nf(a[yr])+'만 원','로보 ('+yr+'년 뒤)','g'],[nf(b[yr])+'만 원','사람 자문','r'],[nf(a[yr]-b[yr])+'만 원','차이','a'],[pct((a[yr]-b[yr])/a[yr],0),'차이 비율','i']]);
    E('자산 = 1,000만 원 × (1 + 수익률 − 수수료)<sup>년</sup> = 1,000 × (1 + '+r.toFixed(3)+' − '+(f1/100).toFixed(4)+')<sup>'+yr+'</sup> = <i>'+nf(a[yr])+'만 원</i>');
    I([['g','수수료 1%p 차이는 작아 보여도 복리로 쌓이면 20년 뒤 수백만 원이 돼요. 낮은 비용이 로보어드바이저의 핵심 강점입니다.'],['a','수수료율·수익률은 예시값이에요. 실제 서비스는 최소 가입 금액·성과 보수·세금 구조가 모두 다르고, 투자 자문이 아닙니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 13-③ 시스템 트레이딩: 이동평균 교차 (실제 가격, 브라우저 계산) ── */
function maBT(P,s,l,fee){var n=P.length,ms=[],ml=[],eq=[1],bh=[1],pos=0,tr=0,peak=1,mdd=0,inm=0;for(var i=0;i<n;i++){ms.push(i>=s-1?mean(P.slice(i-s+1,i+1)):NaN);ml.push(i>=l-1?mean(P.slice(i-l+1,i+1)):NaN)}
  for(i=1;i<n;i++){var r=P[i]/P[i-1]-1,e=eq[i-1]*(1+pos*r);var sig=ms[i]>ml[i]?1:0;if(sig!==pos){e*=(1-fee);tr++}pos=sig;inm+=pos;eq.push(e);bh.push(bh[i-1]*(1+r));peak=Math.max(peak,e);mdd=Math.min(mdd,e/peak-1)}
  var pk=1,bm=0;bh.forEach(function(v){pk=Math.max(pk,v);bm=Math.min(bm,v/pk-1)});return {eq:eq,bh:bh,ms:ms,ml:ml,ret:eq[n-1]-1,bhr:bh[n-1]-1,mdd:mdd,bmdd:bm,tr:tr,inm:inm/n}}
SIMS.ma=function(el,cfg){var c=S0(el,cfg,280,'가격과 두 이동평균, 전략과 보유의 자산 곡선'),row=ctrlRow(el),K=kpis(el,4),E=eqline(el),I=insight(el),a='AMZN',s=20,l=60,fee=.1;
  buttons(row,'종목',[['AMZN','아마존'],['NFLX','넷플릭스'],['DPZ','도미노'],['BTC','비트코인']],a,function(v){a=v;draw()});slider(row,'짧은 이동평균',5,50,5,s,function(v){return v+'일'},function(v){s=v;draw()});slider(row,'긴 이동평균',20,200,10,l,function(v){return v+'일'},function(v){l=v;draw()});slider(row,'거래 비용',0,.5,.05,fee,function(v){return v.toFixed(2)+'%'},function(v){fee=v;draw()});
  function draw(){if(l<=s)l=s+10;var P=FD.port[a],R=maBT(P,s,l,fee/100),W=fit(c,280),ctx=c.getContext('2d');ctx.clearRect(0,0,W,280);grid(ctx,W,280);
    var lo=Math.log10(Math.min.apply(null,R.eq.concat(R.bh))),hi=Math.log10(Math.max.apply(null,R.eq.concat(R.bh))),F=frame(ctx,W,280,{xlo:0,xhi:P.length,ylo:lo,yhi:hi,fx:function(i){var d=FD.port.dates[Math.round(i)];return d?d.slice(0,4):''},fy:function(v){return nf(Math.pow(10,v),1)+'배'},yl:'자산(로그)'});
    [[R.bh,COL.muted,'사서 보유'],[R.eq,COL.g,'이동평균 교차 '+s+'/'+l]].forEach(function(z,zi){ctx.strokeStyle=z[1];ctx.lineWidth=2;ctx.beginPath();z[0].forEach(function(v,i){i?ctx.lineTo(F.X(i),F.Y(Math.log10(v))):ctx.moveTo(F.X(i),F.Y(Math.log10(v)))});ctx.stroke();txt(ctx,'— '+z[2],F.L+8+zi*90,F.T+4,z[1],11,'left',true)});stamp(ctx,W,REAL+' 2013~2019');
    K([[nf(R.ret+1,2)+'배','전략 최종 자산','g'],[nf(R.bhr+1,2)+'배','사서 보유','i'],[pct(R.mdd,0)+' / '+pct(R.bmdd,0),'최대 낙폭 (전략 / 보유)','r'],[R.tr+'번 · '+pct(R.inm,0),'매매 횟수 · 주식 보유 기간','a']]);
    E('규칙: 짧은 평균('+s+'일) &gt; 긴 평균('+l+'일) 이면 다음 날 보유, 아니면 현금 · 매매마다 비용 '+fee.toFixed(2)+'%');
    I([[R.ret>R.bhr?'g':'r',R.ret>R.bhr?'이 종목·기간에서는 교차 전략이 보유보다 나았어요. 크게 떨어지는 구간을 피했기 때문입니다.':'이 종목·기간에서는 그냥 보유가 더 나았어요. 꾸준히 오른 종목에서는 신호가 늦어 오르는 날을 놓칩니다.'],['a','과거에 맞춘 규칙을 그대로 미래에 쓰면 틀리기 쉬워요(과최적화). 교육용 예시이며 투자 자문이 아닙니다.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 14-② k-익명성: 일반화와 정보 손실 (보험 1,338명) ── */
SIMS.kanon=function(el,cfg){var c=S0(el,cfg,230,'묶음 크기별 사람 수와 k'),row=ctrlRow(el),K=kpis(el,4),I=insight(el),w=1,reg=1,ch=1;
  buttons(row,'나이 묶는 폭',[[1,'1살(그대로)'],[5,'5살'],[10,'10살'],[20,'20살']],w,function(v){w=v;draw()});buttons(row,'지역',[[1,'공개'],[0,'삭제']],reg,function(v){reg=v;draw()});buttons(row,'자녀 수',[[1,'공개'],[0,'삭제']],ch,function(v){ch=v;draw()});
  function draw(){var o=FD.kanon.filter(function(k){return k.w===w&&k.reg===reg&&k.ch===ch})[0],W=fit(c,230),ctx=c.getContext('2d');ctx.clearRect(0,0,W,230);grid(ctx,W,230);
    var safe=FD.ins.n-o.rows_small,L=150,pw=W-L-80;[['5명 미만 묶음 속 사람',o.rows_small,COL.r],['5명 이상 묶음 속 사람',safe,COL.g]].forEach(function(x,i){var bw=x[1]/FD.ins.n*pw;ctx.fillStyle=x[2];ctx.fillRect(L,40+i*70,Math.max(bw,2),38);txt(ctx,x[0],L-8,64+i*70,COL.text,12,'right',true);txt(ctx,nf(x[1])+'명',L+bw+6,64+i*70,COL.text,12,'left',true)});stamp(ctx,W,REAL+' 1,338명');
    K([['k = '+o.k,'가장 작은 묶음 크기','g'],[nf(o.groups),'묶음 수 (많을수록 정보 많음)','i'],[nf(o.rows_small)+'명','5명 미만 묶음 속 사람','r'],['나이 '+(w>1?w+'살 단위':'그대로')+(reg?' · 지역':'')+(ch?' · 자녀':''),'남긴 준식별자 (+성별)','a']]);
    I([[o.k>=5?'g':'r',o.k>=5?'모든 묶음이 '+o.k+'명 이상이에요. 같은 조합을 가진 사람이 최소 '+o.k+'명이라, 이 열들만으로는 한 사람을 집어낼 수 없어요(k-익명성).':'아직 한 명뿐인 묶음이 있어요(k = 1). 나이 폭을 넓히거나 열을 지워 보세요.'],['a','열을 지우고 폭을 넓힐수록 안전해지지만 분석에 쓸 정보도 줄어요. 지역·자녀 수를 지우면 그 열에 대한 분석은 할 수 없습니다. 같은 묶음 안의 민감정보가 모두 같으면 여전히 알 수 있어(l-다양성) 함께 점검해야 해요.']])}
  addMod(c,function(dt){if(!dt)draw()});draw()};

/* ── 14-③ 데이터 품질 진단: fintech-data 원자료에서 실제로 찾은 문제 ── */
SIMS.dq=function(el,cfg){var tw=tbl(el),row=ctrlRow(el),K=kpis(el,3),I=insight(el),dim='all';var Q=FD.quality;
  var items=[['완전성','여행자 보험의 성별(Gender) 결측',Q.travel_gender_missing,Q.travel_rows,'결측이 71%라 그대로는 쓸 수 없어요. 열을 빼거나 "모름" 범주로 둡니다.'],
    ['완전성','은행 고객의 학력 "Unknown"',Q.bank_unknown.Education_Level,Q.bank_n,'빈 값 대신 "Unknown"이라는 글자로 들어 있어 isna()로는 안 잡혀요. 숨은 결측입니다.'],
    ['완전성','마케팅 데이터의 구매 이력(History) 결측',Q.dm_hist_missing,Q.dm_rows,'이력이 없는 신규 고객일 수 있어요. 결측 자체가 정보일 수 있으니 이유를 먼저 확인합니다.'],
    ['유효성','여행 기간(Duration)이 음수',Q.travel_dur_neg,Q.travel_rows,'기간이 0보다 작을 수는 없어요. 입력 오류로 보고 고치거나 뺍니다.'],
    ['유효성','나이 100세 초과(118세)',Q.travel_age_118,Q.travel_rows,'같은 값 118이 수백 건 반복돼요. "모름"을 118로 적은 기본값일 가능성이 큽니다.'],
    ['유효성','순매출(Net Sales)이 음수',Q.travel_sales_neg,Q.travel_rows,'환불일 수 있어 오류라고 단정할 수 없어요. 업무 규칙(환불 기록 방식)을 확인해야 합니다.'],
    ['일관성','국제 지표의 다우·VIX 결측(한국 휴일과 미국 휴일 차이)',Q.intl_missing.DOW,Q.intl_rows,'나라마다 거래일이 달라 생긴 빈 값이에요. 날짜 기준을 맞추는 표준화가 필요합니다.'],
    ['일관성','감성 문장: 같은 문장에 다른 감성 라벨',Q.sent_conflict,Q.sent_rows,'같은 문장이 긍정·중립으로 따로 붙어 있어요. 라벨링 기준이 일관되지 않은 것입니다.'],
    ['유일성','감성 문장 중복',Q.sent_dup,Q.sent_rows,'중복 문장이 학습·시험에 나뉘어 들어가면 성능이 부풀려져요.'],
    ['정확성','Revolution4의 두 파일이 같은 내용 + 머리글 없음',1,2,'bank_customers.csv와 direct_marketimg.csv가 바이트까지 같고 열 이름 줄이 빠져 있어요. 파일 이름과 내용이 다른 메타데이터 오류입니다.']];
  buttons(row,'품질 차원',[['all','전체'],['완전성','완전성'],['유효성','유효성'],['일관성','일관성'],['유일성','유일성'],['정확성','정확성']],dim,function(v){dim=v;draw()});
  function draw(){var S=items.filter(function(x){return dim==='all'||x[0]===dim});tw.innerHTML='<table class="tb"><tr><th>차원</th><th>찾은 문제</th><th>건수</th><th>어떻게 할까</th></tr>'+S.map(function(x){return '<tr><td><b>'+x[0]+'</b></td><td>'+x[1]+'</td><td>'+nf(x[2])+(x[3]>2?' / '+nf(x[3])+' ('+pct(x[2]/x[3],1)+')':'')+'</td><td>'+x[4]+'</td></tr>'}).join('')+'</table>';
    K([[S.length+'건','이 차원에서 찾은 문제','r'],['6개','살펴본 원자료 파일','i'],['자동 점검','이 표를 만든 방법 (src/analysis)','g']]);
    I([['g','이 문제들은 모두 이 강의가 쓰는 fintech-data 원자료에서 코드로 실제로 찾은 것이에요. 공개 데이터라도 바로 쓰지 말고 품질부터 점검해야 합니다.'],['a','품질 문제를 찾았다고 바로 지우면 안 돼요. "왜 생겼나"를 확인하고, 고친 내용을 기록(메타데이터)으로 남겨야 다음 사람이 같은 실수를 하지 않습니다.']])}
  draw()};

/* ───────── 대결 ───────── */
DUELS.beh_vs_demo=function(){var A=FD.d.duel01;return {fly:A.beh.auc,robo:A.demo.auc,say:'시험 고객 2,532명에서 이탈 고객을 가려내는 힘(AUC)은 초파리 쪽(거래 횟수 1열) '+A.beh.auc.toFixed(3)+', 주판봇 쪽(나이·성별·학력·소득·결혼 → 가변수 '+A.n_demo_cols+'열) '+A.demo.auc.toFixed(3)+'이에요. 0.5가 찍기 수준입니다.'}};
DUELS.phish_quality=function(){var P=FD.d.phish;return {fly:P.clean_rec,robo:P.biased_rec,say:'시험 사이트 406개 중 실제 피싱을 잡아낸 비율(재현율)은 초파리 쪽(점검한 600건) '+pct(P.clean_rec,1)+', 주판봇 쪽(점검 없이 모은 '+P.noisy_n+'건, 피싱 '+P.flip2+'건이 "정상"으로 잘못 적힘) '+pct(P.biased_rec,1)+'예요.'}};
DUELS.collect_cycle=function(){var D=FD.d.duel03;return {fly:D.AMZN.monthly*100,robo:D.AMZN.daily*100,say:'아마존 주가를 "가장 최근에 모은 값"으로 어림했을 때 평균 오차는 초파리 쪽(한 달에 한 번 수집) '+pct(D.AMZN.monthly,1)+', 주판봇 쪽(매일 수집) '+pct(D.AMZN.daily,1)+'예요. 비트코인은 '+pct(D.BTC.monthly,1)+' 대 '+pct(D.BTC.daily,1)+'로 차이가 더 커요.'}};
DUELS.train_vs_test=function(){var D=FD.d.duel04;return {fly:D.k15_test*100,robo:D.test_acc*100,say:'새 고객 2,532명 정확도는 초파리 쪽(시험 세트 점수로 고른 k=15 모델) '+pct(D.k15_test,1)+', 주판봇 쪽(학습 데이터 점수 '+pct(D.train_acc,1)+'로 고른 k=1 모델) '+pct(D.test_acc,1)+'예요. 주판봇이 본 99.8%는 이미 본 고객을 다시 맞힌 점수였어요.'}};
DUELS.unknown_drop=function(){var D=FD.d.duel05;return {fly:D.keep_acc,robo:D.drop_acc,say:'같은 시험 고객 2,532명 정확도는 초파리 쪽(Unknown을 하나의 값으로 두고 '+nf(D.keep_train)+'명으로 학습) '+pct(D.keep_acc,2)+', 주판봇 쪽(Unknown 행을 지우고 '+nf(D.drop_train)+'명으로 학습) '+pct(D.drop_acc,2)+'예요. 지운 쪽은 학습 고객 '+pct(1-D.drop_train/D.keep_train,0)+'를 버렸습니다.'}};
DUELS.svm_scale=function(){var D=FD.d.duel06;return {fly:D.std_rec*100,robo:D.raw_rec*100,say:'시험 고객 2,532명 중 실제 이탈 고객 '+FD.knn.pos_te+'명을 잡은 비율(재현율)은 초파리 쪽(표준화 후 SVM) '+pct(D.std_rec,1)+', 주판봇 쪽(그대로 SVM) '+pct(D.raw_rec,1)+'예요. 그대로 쓴 SVM은 정확도 '+pct(D.raw,1)+'로 "모두 남는다"와 똑같이 찍었습니다.'}};
DUELS.acc_vs_recall=function(){var D=FD.d.duel07;var A={fly:D.lr.acc*100,robo:D.all0.acc*100,label:'기준 A: 정확도(%)'},B={fly:D.lr.caught,robo:0,label:'기준 B: 실제 청구 232건 중 잡아낸 건수'};return {fly:A.fly,robo:A.robo,cond:true,condA:A,condB:B,say:'정확도로 재면 주판봇 쪽("모두 청구 없음") '+pct(D.all0.acc,1)+', 초파리 쪽(로지스틱, 기준 2%) '+pct(D.lr.acc,1)+'예요. 잡아낸 청구로 재면 '+D.lr.caught+'건 대 0건입니다.'}};
DUELS.extrapolate=function(){var D=FD.d.duel09;return {fly:D.lin_mae,robo:D.knn_mae,say:'연봉 상위 10% 고객 '+D.n_hi+'명(학습 때 본 적 없는 높은 연봉)의 소비액 평균 오차(MAE)는 초파리 쪽(선형 회귀) $'+nf(D.lin_mae)+', 주판봇 쪽(KNN 회귀) $'+nf(D.knn_mae)+'예요. KNN은 아무리 높은 연봉에도 $'+nf(D.knn_max)+' 이상을 말하지 못했어요.'}};
DUELS.more_features=function(){var F=FD.d.fe;return {fly:F['나이+BMI+흡연'].r2,robo:F['+흡연×BMI'].r2,say:'시험 고객 335명 보험료의 R²는 초파리 쪽(나이·BMI·흡연 3개) '+F['나이+BMI+흡연'].r2.toFixed(3)+', 주판봇 쪽(나이²·흡연×비만·흡연×BMI를 더한 6개) '+F['+흡연×BMI'].r2.toFixed(3)+'이에요. RMSE는 $'+nf(F['나이+BMI+흡연'].rmse)+' 대 $'+nf(F['+흡연×BMI'].rmse)+'.'}};
DUELS.naive_vs_ar=function(){var D=FD.d.duel11;return {fly:D.naive,robo:D.ar,say:'넷플릭스 마지막 120거래일 종가의 평균 오차(MAE)는 초파리 쪽("내일 = 오늘 가격") $'+D.naive.toFixed(2)+', 주판봇 쪽(과거 10일 AR 모델) $'+D.ar.toFixed(2)+'예요. 비트코인에서도 $'+nf(D.naive_btc)+' 대 $'+nf(D.ar_btc)+'로 같은 결과였어요.'}};
DUELS.mean_vs_median=function(){var D=FD.d.duel12;var A={fly:D.mae_med,robo:D.mae_mean,label:'기준 A: 평균 절대 오차 MAE ($, 낮을수록 좋음)'},B={fly:D.rmse_med,robo:D.rmse_mean,label:'기준 B: RMSE ($, 낮을수록 좋음)'};return {fly:A.fly,robo:A.robo,cond:true,condA:A,condB:B,say:'새 고객 '+D.n_test+'명의 보험료를 숫자 하나로 맞힐 때, MAE는 초파리 쪽(중앙값 $'+nf(D.median)+') $'+nf(D.mae_med)+', 주판봇 쪽(평균 $'+nf(D.mean)+') $'+nf(D.mae_mean)+'이고, RMSE는 $'+nf(D.rmse_med)+' 대 $'+nf(D.rmse_mean)+'예요.'}};
DUELS.ma_vs_hold=function(){var D=FD.d.duel13;var A={fly:(D.AMZN.bh+1),robo:(D.AMZN.ret+1),label:'가정 A: 아마존 (2013~2019, 최종 자산 배수)'},B={fly:(D.BTC.bh+1),robo:(D.BTC.ret+1),label:'가정 B: 비트코인 (같은 기간, 최종 자산 배수)'};return {fly:A.fly,robo:A.robo,cond:true,condA:A,condB:B,say:'최종 자산은 아마존에서 초파리 쪽(사서 보유) '+nf(A.fly,1)+'배, 주판봇 쪽(20/60일 교차) '+nf(A.robo,1)+'배이고, 비트코인에서는 '+nf(B.fly,0)+'배 대 '+nf(B.robo,0)+'배예요. 최대 낙폭은 비트코인 보유 '+pct(D.BTC.bh_mdd,0)+', 교차 전략 '+pct(D.BTC.mdd,0)+'였어요.'}};
DUELS.kanon_duel=function(){var D=FD.d.duel14;return {fly:D.fly.rows_small,robo:D.robo.rows_small,say:'5명 미만 묶음에 속해 다시 알아볼 위험이 큰 사람은 초파리 쪽(나이 5살 단위 + 자녀 수 공개) '+D.fly.rows_small+'명(k='+D.fly.k+'), 주판봇 쪽(나이 20살 단위, 지역·자녀 삭제) '+D.robo.rows_small+'명(k='+D.robo.k+')이에요. 보험료 예측 R²는 '+D.fly.r2.toFixed(3)+' 대 '+D.robo.r2.toFixed(3)+'로 거의 같았어요.'}};
