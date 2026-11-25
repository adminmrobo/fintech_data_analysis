
/* 동적 대시보드: 회차마다 한 화면(조절기 · 숫자 카드 4개 · 그림 2개 · 해석), 목차에서는 탭으로 13개 */
var DASHES={};
function niceTicks(lo,hi,n){var span=hi-lo||1,step=Math.pow(10,Math.floor(Math.log10(span/n))),e=span/n/step;step*=e>=5?10:e>=2?5:e>=1?2:1;var t=[],s=Math.ceil(lo/step)*step;for(var v=s;v<=hi+step*1e-6;v+=step)t.push(+v.toFixed(10));return t}
function dChart(c,spec,H){var W=fit(c,H),ctx=c.getContext('2d');ctx.clearRect(0,0,W,H);
  var L=52,R=14,T=30,B=40,pw=W-L-R,ph=H-T-B;txt(ctx,spec.title,L,18,COL.text,13,'left',true);
  if(spec.t==='bar'){var n=spec.vals.length,mx=spec.ymax||Math.max.apply(null,spec.vals.concat([1e-9]))*1.18,bw=pw/n;ctx.strokeStyle=COL.rule;ctx.beginPath();ctx.moveTo(L,T+ph+.5);ctx.lineTo(L+pw,T+ph+.5);ctx.stroke();
    if(spec.hline!=null){var hy=T+ph-spec.hline/mx*ph;ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.a;ctx.beginPath();ctx.moveTo(L,hy);ctx.lineTo(L+pw,hy);ctx.stroke();ctx.restore();txt(ctx,spec.hlabel||'',L+2,hy-5,COL.a,11,'left',true)}
    spec.vals.forEach(function(v,i){var bh=Math.max(0,v)/mx*ph,x=L+i*bw+bw*.2;ctx.fillStyle=(spec.cols&&spec.cols[i])||COL.s;ctx.fillRect(x,T+ph-bh,bw*.6,bh);txt(ctx,(spec.fy||String)(v),x+bw*.3,T+ph-bh-6,COL.text,bw<44?10:12,'center',true);txt(ctx,spec.labels[i],x+(spec.pair?bw*.8:bw*.3),T+ph+16,COL.muted,11,'center')});return}
  if(spec.t==='hist'){var bins=spec.bins||30,cnt=new Array(bins).fill(0),lo=spec.lo,hi=spec.hi;spec.vals.forEach(function(v){var k=Math.floor((v-lo)/(hi-lo)*bins);if(k>=0&&k<bins)cnt[k]++});var m=Math.max.apply(null,cnt)||1;
    ctx.fillStyle=spec.c||'rgba(63,95,168,.55)';cnt.forEach(function(k,i){var bh=k/m*ph;ctx.fillRect(L+i*pw/bins+1,T+ph-bh,pw/bins-2,bh)});
    ctx.strokeStyle=COL.rule;ctx.beginPath();ctx.moveTo(L,T+ph+.5);ctx.lineTo(L+pw,T+ph+.5);ctx.stroke();niceTicks(lo,hi,5).forEach(function(t){var x=L+(t-lo)/(hi-lo)*pw;txt(ctx,(spec.fx||String)(t),x,T+ph+16,COL.muted,11,'center')});
    (spec.marks||[]).forEach(function(mk,i){var x=L+(mk.x-lo)/(hi-lo)*pw;if(x<L||x>L+pw)return;ctx.save();ctx.strokeStyle=mk.c||COL.r;ctx.setLineDash([4,3]);ctx.beginPath();ctx.moveTo(x,T);ctx.lineTo(x,T+ph);ctx.stroke();ctx.restore();txt(ctx,mk.l,x+(i%2?-4:4),T+10+(i%3)*13,mk.c||COL.r,11,i%2?'right':'left',true)});
    if(spec.xl)txt(ctx,spec.xl,L+pw,H-6,COL.muted,11,'right');return}
  /* line */
  var xs=spec.xs,x0=xs[0],x1=xs[xs.length-1],ylo=spec.ymin,yhi=spec.ymax;if(ylo==null||yhi==null){var all=[];spec.ys.forEach(function(s){s.d.forEach(function(v){if(isFinite(v))all.push(v)})});if(ylo==null)ylo=Math.min.apply(null,all);if(yhi==null)yhi=Math.max.apply(null,all);if(yhi===ylo)yhi=ylo+1;var pad=(yhi-ylo)*.08;if(spec.ymin==null)ylo-=pad;if(spec.ymax==null)yhi+=pad}
  function X(v){return spec.logx?L+(Math.log(v)-Math.log(x0))/(Math.log(x1)-Math.log(x0))*pw:L+(v-x0)/(x1-x0)*pw}function Y(v){return T+ph-(v-ylo)/(yhi-ylo)*ph}
  ctx.strokeStyle=COL.rule;ctx.lineWidth=1;niceTicks(ylo,yhi,4).forEach(function(t){var y=Y(t);ctx.beginPath();ctx.moveTo(L,y+.5);ctx.lineTo(L+pw,y+.5);ctx.stroke();txt(ctx,(spec.fy||String)(t),L-6,y+4,COL.muted,11,'right')});
  var xt=spec.logx?[1,3,10,30,100,300,1000,3000,10000,30000,100000].filter(function(v){return v>=x0&&v<=x1}):niceTicks(x0,x1,5);xt.forEach(function(t){txt(ctx,(spec.fx||String)(t),X(t),T+ph+16,COL.muted,11,'center')});
  if(spec.band){ctx.fillStyle='rgba(19,138,82,.08)';var b=spec.band,b0=clamp(X(b[0]),L,L+pw),b1=clamp(X(b[1]),L,L+pw);if(b1>b0)ctx.fillRect(b0,T,b1-b0,ph)}
  if(spec.hline!=null){ctx.save();ctx.setLineDash([5,4]);ctx.strokeStyle=COL.a;ctx.beginPath();ctx.moveTo(L,Y(spec.hline));ctx.lineTo(L+pw,Y(spec.hline));ctx.stroke();ctx.restore();txt(ctx,spec.hlabel||'',L+pw-2,Y(spec.hline)<T+16?Y(spec.hline)+14:Y(spec.hline)-5,COL.a,11,'right',true)}
  var lx=L+pw;spec.ys.forEach(function(s,si){ctx.save();ctx.strokeStyle=s.c;ctx.lineWidth=s.w||2.2;if(s.dash)ctx.setLineDash(s.dash);ctx.beginPath();var st=false;s.d.forEach(function(v,i){if(!isFinite(v)){st=false;return}var px=X(xs[i]),py=Y(clamp(v,ylo,yhi));if(!st){ctx.moveTo(px,py);st=true}else ctx.lineTo(px,py)});ctx.stroke();if(s.fill){ctx.lineTo(X(x1),Y(ylo));ctx.lineTo(X(x0),Y(ylo));ctx.closePath();ctx.globalAlpha=.12;ctx.fillStyle=s.c;ctx.fill()}ctx.restore();
    if(s.n&&spec.ys.length>1){ctx.save();ctx.font='700 11px "IBM Plex Sans KR",system-ui,sans-serif';var tw=ctx.measureText('● '+s.n).width;ctx.restore();lx-=tw+12;txt(ctx,'● '+s.n,lx+12,18,s.c,11,'left',true)}});
  if(spec.mark&&X(spec.mark.x)>=L-1&&X(spec.mark.x)<=L+pw+1){var mx_=X(spec.mark.x);ctx.save();ctx.strokeStyle=COL.r;ctx.setLineDash([4,3]);ctx.beginPath();ctx.moveTo(mx_,T);ctx.lineTo(mx_,T+ph);ctx.stroke();ctx.restore();if(spec.mark.y!=null){ctx.fillStyle=COL.r;ctx.beginPath();ctx.arc(mx_,Y(clamp(spec.mark.y,ylo,yhi)),5,0,7);ctx.fill()}if(spec.mark.l)txt(ctx,spec.mark.l,mx_+(mx_>L+pw*.7?-6:6),T+ph-8,COL.r,11,mx_>L+pw*.7?'right':'left',true)}
  if(spec.xl)txt(ctx,spec.xl,L+pw,H-4,COL.muted,11,'right');if(spec.yl)txt(ctx,spec.yl,4,T-10+0,COL.muted,11,'left')}

function Dash(el,key){var D=DASHES[key];if(!D){el.innerHTML='';return}el.innerHTML='';var p={},seed=1,ctl={},playing=false;
  var head=h('div',{class:'dhead'});head.innerHTML='<div><span class="eyebrow">동적 대시보드 · '+esc(D.tag||'')+'</span><h3>'+D.title+'</h3><p class="muted" style="font-size:14px">'+(D.sub||'')+'</p></div>';var hb=h('div',{class:'dbtns'});head.appendChild(hb);el.appendChild(head);
  var row=ctrlRow(el);var K=kpis(el,4);var g=h('div',{class:'dgrid'});el.appendChild(g);var c1=mkCanvas(g,240,D.title+' 그림 1'),c2=mkCanvas(g,240,D.title+' 그림 2');var I=insight(el);
  D.params.forEach(function(q){p[q[0]]=q[5];ctl[q[0]]=slider(row,q[1],q[2],q[3],q[4],q[5],q[6],function(v){p[q[0]]=v;draw()})});
  var pb=action(hb,'▶ 재생: '+(D.playLabel||'천천히 바꿔 보기'),function(){if(playing){playing=false;return}var q=D.params.filter(function(x){return x[0]===D.play})[0];if(!q)return;if(reduce){ctl[q[0]].set(q[3]);return}playing=true;pb.textContent='■ 멈춤';var t0=null,from=q[2],to=q[3];function step(ts){if(!playing){pb.textContent='▶ 재생: '+(D.playLabel||'천천히 바꿔 보기');return}if(!t0)t0=ts;var u=Math.min(1,(ts-t0)/4500),v=from+(to-from)*(D.playLog?(Math.pow(to/from,u)*from-from)/(to-from):u);v=Math.round(v/q[4])*q[4];ctl[q[0]].set(+v.toFixed(6));if(u<1)requestAnimationFrame(step);else{playing=false;pb.textContent='▶ 재생: '+(D.playLabel||'천천히 바꿔 보기')}}requestAnimationFrame(step)},true);
  if(D.random)action(hb,'↻ 다시 뽑기',function(){seed++;draw()});
  action(hb,'처음 값',function(){playing=false;D.params.forEach(function(q){ctl[q[0]].set(q[5])})});
  function draw(){var o=D.f(p,rng(seed*7919+13));K(o.k);dChart(c1,o.c[0],240);dChart(c2,o.c[1],240);I(o.note);c1._spec=o.c[0];c2._spec=o.c[1]}
  addMod(c1,function(dt){if(!dt&&c1._spec){dChart(c1,c1._spec,240);dChart(c2,c2._spec,240)}});draw();return {stop:function(){playing=false}}}
function initDash(){var el=$('.dash[data-dash]');if(el)Dash(el,el.dataset.dash);var tabs=$('.dtabs');if(tabs){var box=$('#dashbox'),cur=null;$$('button',tabs).forEach(function(b){b.addEventListener('click',function(){$$('button',tabs).forEach(function(x){x.setAttribute('aria-pressed','false')});b.setAttribute('aria-pressed','true');if(cur)cur.stop();cur=Dash(box,b.dataset.k);var a=$('#dashlink');if(a){a.href=b.dataset.f+'#dash';a.textContent=(+b.dataset.k)+'회차 해설 페이지에서 자세히 보기 →'}})});var f=$('button',tabs);if(f)f.click()}}

function rng0(){return 0}
function seqv(a,b,n){var o=[];for(var i=0;i<n;i++)o.push(a+(b-a)*i/(n-1));return o}
function logseq(a,b,n){var o=[];for(var i=0;i<n;i++)o.push(a*Math.pow(b/a,i/(n-1)));return o}
function lgam(x){var c=[76.18009172947146,-86.50532032941677,24.01409824083091,-1.231739572450155,.1208650973866179e-2,-.5395239384953e-5],y=x,t=x+5.5;t-=(x+.5)*Math.log(t);var s=1.000000000190015;for(var j=0;j<6;j++)s+=c[j]/++y;return -t+Math.log(2.5066282746310005*s/x)}
function betaPdf(x,a,b){if(x<=0||x>=1)return 0;return Math.exp((a-1)*Math.log(x)+(b-1)*Math.log(1-x)+lgam(a+b)-lgam(a)-lgam(b))}
function normCdf(z){var t=1/(1+.2316419*Math.abs(z)),d=.3989423*Math.exp(-z*z/2),p=d*t*(.3193815+t*(-.3565638+t*(1.781478+t*(-1.821256+t*1.330274))));return z>0?1-p:p}
function P1(v){return (v*100).toFixed(1)+'%'}function P0(v){return Math.round(v*100)+'%'}
function won(v){return Math.abs(v)>=1e8?(v/1e8).toFixed(1)+'억':Math.abs(v)>=1e4?nf(Math.round(v/1e4))+'만':nf(Math.round(v))}

/* 핀테크 데이터 분석 — 회차별 동적 대시보드 (FD = 실제 데이터 표본·계산 결과) */
function staleErr(P,gap){var s=0,n=0;for(var i=gap;i<P.length;i++){var j=Math.floor(i/gap)*gap-1;if(j<0)j=0;s+=Math.abs(P[i]-P[j])/P[i];n++}return s/n}
var KS=[1,3,5,7,9,11,15,21,31,51],AS=['AMZN','NFLX','BTC'],ANM={AMZN:'아마존',NFLX:'넷플릭스',BTC:'비트코인',DPZ:'도미노'};

DASHES['01']={tag:'1회차',title:'은행 고객 데이터 한눈에',sub:'거래 횟수 하나로 이탈 고객이 얼마나 갈리는지 (실제 은행 고객 표본 400명)',play:'cut',playLabel:'기준을 20회→120회로',
  params:[['cut','거래 횟수 기준',20,120,5,55,function(v){return v+'회'}]],
  f:function(q){var S=FD.knn_s,lo=[0,0],hi=[0,0];S.x.forEach(function(x,i){var g=x<q.cut?lo:hi;g[0]++;g[1]+=S.t[i]});var rl=lo[1]/(lo[0]||1),rh=hi[1]/(hi[0]||1),cuts=seqv(20,120,21);
    return {k:[[P1(rl),q.cut+'회 미만 고객의 이탈률','r'],[P1(rh),q.cut+'회 이상 고객의 이탈률','g'],[(rl/(rh||.001)).toFixed(1)+'배','두 무리의 차이','a'],[P1(FD.bank.rate),'전체 이탈률 (10,127명)','i']],
      c:[{t:'bar',title:'기준 아래·위 이탈률',labels:[q.cut+'회 미만 ('+lo[0]+'명)',q.cut+'회 이상 ('+hi[0]+'명)'],vals:[rl*100,rh*100],cols:[COL.r,COL.g],fy:function(v){return v.toFixed(1)+'%'},hline:FD.bank.rate*100,hlabel:'전체'},
        {t:'line',title:'기준을 옮길 때 두 무리의 이탈률',xs:cuts,ys:[{n:'기준 미만',c:COL.r,d:cuts.map(function(c){var a=0,b=0;S.x.forEach(function(x,i){if(x<c){a++;b+=S.t[i]}});return b/(a||1)*100})},{n:'기준 이상',c:COL.g,d:cuts.map(function(c){var a=0,b=0;S.x.forEach(function(x,i){if(x>=c){a++;b+=S.t[i]}});return b/(a||1)*100})}],ymin:0,fy:function(v){return v+'%'},mark:{x:q.cut},xl:'거래 횟수 기준'}],
      note:[['g','거래가 적은 고객일수록 떠날 가능성이 커요. 핀테크가 "행동 데이터"를 중시하는 이유입니다.'],['a','표본 400명의 결과예요. 전체 데이터로 계산한 대결 결과(1회차 대결)와 함께 보세요.']]}}};

DASHES['02']={tag:'2회차',title:'공개할 열과 다시 알아보기 위험',sub:'보험 고객 1,338명 — 열을 줄일수록 유일한 사람이 줄어든다',play:'lv',playLabel:'공개 열을 5개→3개로',
  params:[['lv','공개 열 단계',0,2,1,0,function(v){return FD.ins.uniq[v][0]}]],
  f:function(q){var U=FD.ins.uniq,u=U[q.lv];return {k:[[nf(u[1])+'명','유일한 조합을 가진 사람','r'],[P1(u[1]/FD.ins.n),'전체 중','a'],[nf(u[3]),'서로 다른 조합','i'],[String(u[2]),'가장 작은 묶음(k)','g']],
    c:[{t:'bar',title:'공개 열별 유일한 사람 수',labels:U.map(function(x){return x[0].replace(/·/g,'\n').split('\n').length+'열'}),vals:U.map(function(x){return x[1]}),cols:U.map(function(x,i){return i===q.lv?COL.r:'rgba(63,95,168,.55)'}),fy:nf},
      {t:'bar',title:'지금 단계의 사람 나눔',labels:['유일한 사람','나머지'],vals:[u[1],FD.ins.n-u[1]],cols:[COL.r,COL.g],fy:nf}],
    note:[['g','이름을 지운 것만으로는 익명이 아니에요. 남은 열의 조합이 사람을 가리킵니다.'],['a','법에서는 이름 등을 지우고 추가 정보 없이는 알아볼 수 없게 한 것을 가명정보, 어떤 방법으로도 알아볼 수 없게 한 것을 익명정보라 해요.']]}}};

DASHES['03']={tag:'3회차',title:'수집 주기와 정보의 신선도',sub:'가장 최근에 모은 값으로 오늘 가격을 어림할 때의 오차 (실제 주가 2013~2019)',play:'gap',playLabel:'주기를 1일→63일로',
  params:[['gap','수집 주기',1,63,1,21,function(v){return v+'거래일'}]],
  f:function(q){var gs=[1,2,5,10,21,42,63];return {k:AS.concat(['DPZ']).map(function(a,i){return [P1(staleErr(FD.port[a],q.gap)),ANM[a]+' 평균 오차',['i','r','a','g'][i]]}),
    c:[{t:'bar',title:'지금 주기의 종목별 오차',labels:AS.concat(['DPZ']).map(function(a){return ANM[a]}),vals:AS.concat(['DPZ']).map(function(a){return staleErr(FD.port[a],q.gap)*100}),fy:function(v){return v.toFixed(1)+'%'}},
      {t:'line',title:'수집 주기별 오차',xs:gs,ys:AS.map(function(a,i){return {n:ANM[a],c:[COL.s,COL.r,COL.a][i],d:gs.map(function(g){return staleErr(FD.port[a],g)*100})}}),ymin:0,fy:function(v){return v+'%'},mark:{x:q.gap},xl:'수집 주기(거래일)'}],
    note:[['g','변동이 큰 자산(비트코인)일수록 자주 모아야 해요. 한 달에 한 번 모으면 평균 13% 넘게 빗나갑니다.'],['a','자주 모을수록 비용(서버·API 호출·저장)이 늘어요. 수집 계획은 "얼마나 신선해야 하나"와 비용 사이의 선택입니다.']]}}};

DASHES['04']={tag:'4회차',title:'학습 점수와 시험 점수',sub:'KNN의 이웃 수 k에 따른 정확도 (은행 고객 10,127명, 표준화)',play:'ki',playLabel:'k를 1→51로',
  params:[['ki','이웃 수 k',0,9,1,0,function(v){return 'k = '+KS[v]}]],
  f:function(q){var A=FD.knn.std,a=A[KS[q.ki]];return {k:[[P1(a[0]),'학습 정확도','r'],[P1(a[1]),'시험 정확도','g'],[P1(a[0]-a[1])+'p','차이','a'],[P1(FD.knn.base),'"모두 남는다" 기준선','i']],
    c:[{t:'line',title:'k에 따른 학습·시험 정확도',xs:KS,logx:true,ys:[{n:'학습',c:COL.r,d:KS.map(function(k){return A[k][0]*100})},{n:'시험',c:COL.g,d:KS.map(function(k){return A[k][1]*100})}],ymin:85,ymax:100,fy:function(v){return v+'%'},fx:String,mark:{x:KS[q.ki]},xl:'k (로그 눈금)'},
      {t:'bar',title:'지금 k에서',labels:['학습','시험','기준선'],vals:[a[0]*100,a[1]*100,FD.knn.base*100],cols:[COL.r,COL.g,COL.muted],fy:function(v){return v.toFixed(1)+'%'},ymax:100}],
    note:[['g','학습과 시험 점수가 벌어지면 과대적합, 둘 다 낮으면 과소적합이에요.'],['a','최종 점수는 학습에 한 번도 쓰지 않은 시험 데이터로만 보고해야 합니다.']]}}};

DASHES['05']={tag:'5회차',title:'이상치 울타리 대시보드',sub:'연간 거래 금액의 IQR 울타리 (실제 은행 고객 표본 1,500명)',play:'k',playLabel:'배수를 1→4로',
  params:[['k','울타리 배수',1,4,.25,1.5,function(v){return '× '+v.toFixed(2)}]],
  f:function(q){var v=FD.amt,up=FD.out.q3+q.k*(FD.out.q3-FD.out.q1),n=v.filter(function(x){return x>up}).length,ks=seqv(1,4,13);
    return {k:[[nf(Math.round(up)),'위쪽 울타리($)','r'],[nf(n)+'명','울타리 밖 (표본)','a'],[P1(n/v.length),'비율','i'],[nf(FD.out.iqr),'IQR = Q3 − Q1','g']],
      c:[{t:'hist',title:'거래 금액 분포와 울타리',vals:v,lo:0,hi:19000,bins:38,fx:function(x){return nf(x/1000)+'천'},marks:[{x:FD.out.q1,l:'Q1',c:COL.g},{x:FD.out.q3,l:'Q3',c:COL.g},{x:up,l:'울타리',c:COL.r}]},
        {t:'line',title:'배수에 따른 울타리 밖 비율',xs:ks,ys:[{n:'울타리 밖',c:COL.r,d:ks.map(function(k){var u=FD.out.q3+k*FD.out.iqr;return v.filter(function(x){return x>u}).length/v.length*100})}],ymin:0,fy:function(x){return x.toFixed(0)+'%'},mark:{x:q.k},xl:'울타리 배수'}],
      note:[['g','배수를 4까지 올려도 오른쪽 봉우리는 남아요. 오류가 아니라 실제로 거래를 많이 하는 고객 무리이기 때문입니다.'],['a','"1.5배"는 관례일 뿐 법칙이 아니에요. 이상치 후보를 찾는 도구로 쓰고, 지울지는 업무 의미로 정합니다.']]}}};

DASHES['06']={tag:'6회차',title:'표준화와 이웃 수',sub:'같은 KNN이라도 거리 재는 법에 따라 (은행 고객 10,127명)',play:'ki',playLabel:'k를 1→51로',
  params:[['ki','이웃 수 k',0,9,1,2,function(v){return 'k = '+KS[v]}]],
  f:function(q){var k=KS[q.ki],R=FD.knn.raw[k],S=FD.knn.std[k];return {k:[[P1(R[1]),'그대로 · 시험 정확도','a'],[P1(S[1]),'표준화 · 시험 정확도','g'],[P1(S[1]-R[1])+'p','표준화 효과','i'],[P1(FD.knn.svm_raw)+' → '+P1(FD.knn.svm_rbf),'SVM: 그대로 → 표준화','r']],
    c:[{t:'line',title:'k에 따른 시험 정확도',xs:KS,logx:true,ys:[{n:'그대로',c:COL.a,d:KS.map(function(x){return FD.knn.raw[x][1]*100})},{n:'표준화',c:COL.g,d:KS.map(function(x){return FD.knn.std[x][1]*100})}],ymin:86,ymax:92,fy:function(v){return v+'%'},fx:String,mark:{x:k},xl:'k (로그 눈금)'},
      {t:'bar',title:'SVM(RBF)은 표준화가 더 중요',labels:['SVM 그대로','SVM 표준화','기준선'],vals:[FD.knn.svm_raw*100,FD.knn.svm_rbf*100,FD.knn.base*100],cols:[COL.a,COL.g,COL.muted],fy:function(v){return v.toFixed(1)+'%'},ymax:100}],
    note:[['g','KNN에서는 표준화 효과가 1%p 안팎이지만, SVM은 표준화하지 않으면 "모두 남는다"로 찍는 모델이 됐어요.'],['a','표준화 기준(평균·표준편차)은 학습 데이터에서만 구해 시험 데이터에 그대로 써야 합니다.']]}}};

DASHES['07']={tag:'7회차',title:'임계값 대시보드',sub:'여행자 보험 청구 예측 (시험 15,832건, 실제 청구 232건)',play:'ti',playLabel:'임계값을 0.5%→50%로',
  params:[['ti','임계값',0,12,1,3,function(v){return P1(FD.travel.cms[v].th)}]],
  f:function(q){var T=FD.travel.cms,m=T[q.ti],s=cmCalc(m),th=T.map(function(x){return x.th*100});
    return {k:[[P1(s.acc),'정확도','i'],[P1(s.pre),'정밀도','a'],[P1(s.rec),'재현율','r'],[nf(m.fp),'괜히 의심한 고객(FP)','m']],
      c:[{t:'bar',title:'혼동행렬 네 구역',labels:['TP','FN','FP','TN'],vals:[m.tp,m.fn,m.fp,m.tn],cols:[COL.g,COL.r,COL.a,COL.s],fy:nf},
        {t:'line',title:'임계값에 따른 지표',xs:th,logx:true,ys:[{n:'정확도',c:COL.s,d:T.map(function(x){return cmCalc(x).acc*100})},{n:'재현율',c:COL.r,d:T.map(function(x){return cmCalc(x).rec*100})},{n:'정밀도',c:COL.a,d:T.map(function(x){return cmCalc(x).pre*100})}],ymin:0,ymax:100,fy:function(v){return v+'%'},fx:function(v){return v+'%'},mark:{x:m.th*100},xl:'임계값(로그)'}],
      note:[['g','정확도는 거의 늘 높고, 재현율과 정밀도가 서로 맞바꿔져요.'],['a','어느 지표를 볼지는 모델이 아니라 업무가 정합니다. 놓친 청구 한 건과 괜한 조사 한 건의 비용을 비교하세요.']]}}};

DASHES['09']={tag:'9회차',title:'KNN 회귀의 이웃 수',sub:'연봉으로 소비액 예측 (DirectMarketing 표본 300명, 4명 중 1명은 시험용)',play:'k',playLabel:'k를 1→50으로',
  params:[['k','이웃 수 k',1,50,1,5,function(v){return 'k = '+v}]],
  f:function(q){var S=FD.dm_s,tr=[],te=[];S.x.forEach(function(x,i){(i%4?tr:te).push([x,S.y[i]])});function kp(x,k){return mean(tr.map(function(p){return [Math.abs(p[0]-x),p[1]]}).sort(function(a,b){return a[0]-b[0]}).slice(0,k).map(function(z){return z[1]}))}
    function mae(set,k){return mean(set.map(function(p){return Math.abs(p[1]-kp(p[0],k))}))}var ks=[1,2,3,5,8,12,20,30,50],a=FD.dm.lin_coef,b0=FD.dm.lin_b0,lin=mean(te.map(function(p){return Math.abs(p[1]-(a*p[0]+b0))})),xs=seqv(10,170,40);
    return {k:[['$'+nf(mae(tr,q.k)),'학습 MAE','r'],['$'+nf(mae(te,q.k)),'시험 MAE','g'],['$'+nf(lin),'선형 회귀 시험 MAE','i'],[q.k+'명','평균 내는 이웃','a']],
      c:[{t:'line',title:'예측 곡선 (KNN과 직선)',xs:xs,ys:[{n:'KNN k='+q.k,c:COL.r,d:xs.map(function(x){return kp(x,q.k)})},{n:'선형',c:COL.g,d:xs.map(function(x){return a*x+b0})}],ymin:0,fy:nf,fx:String,xl:'연봉(천 달러)'},
        {t:'line',title:'k에 따른 학습·시험 MAE',xs:ks,logx:true,ys:[{n:'학습',c:COL.r,d:ks.map(function(k){return mae(tr,k)})},{n:'시험',c:COL.g,d:ks.map(function(k){return mae(te,k)})}],fy:function(v){return '$'+nf(v)},fx:String,mark:{x:q.k},xl:'k'}],
      note:[['g','k = 1이면 학습 오차는 0이지만 시험 오차가 커요. k를 키우면 곡선이 매끈해지며 직선에 가까워집니다.'],['a','표본 300명 기준이라 전체 데이터 결과(시험 R² KNN '+FD.dm.knn_r2+', 선형 '+FD.dm.lin_r2+')와 조금 다를 수 있어요.']]}}};

DASHES['10']={tag:'10회차',title:'나무의 깊이와 과대적합',sub:'거래 횟수·회전 잔액으로 이탈 예측 (은행 고객 10,127명)',play:'di',playLabel:'깊이를 1→끝까지',
  params:[['di','최대 깊이',0,9,1,3,function(v){return ['1','2','3','4','5','6','8','10','15','제한 없음'][v]}]],
  f:function(q){var ds=['1','2','3','4','5','6','8','10','15','None'],D=FD.tree.depth,a=D[ds[q.di]],xs=[1,2,3,4,5,6,8,10,15,20];
    return {k:[[P1(a[0]),'학습 정확도','r'],[P1(a[1]),'시험 정확도','g'],[nf(a[2])+'개','잎 수','i'],[P1(a[0]-a[1])+'p','차이','a']],
      c:[{t:'line',title:'깊이에 따른 정확도',xs:xs,ys:[{n:'학습',c:COL.r,d:ds.map(function(d){return D[d][0]*100})},{n:'시험',c:COL.g,d:ds.map(function(d){return D[d][1]*100})}],ymin:83,ymax:96,fy:function(v){return v+'%'},fx:function(v){return v===20?'끝':String(v)},mark:{x:xs[q.di]},xl:'최대 깊이'},
        {t:'bar',title:'깊이별 잎 수 (규칙의 개수)',labels:['1','2','3','4','6','10','끝'],vals:['1','2','3','4','6','10','None'].map(function(d){return D[d][2]}),cols:['1','2','3','4','6','10','None'].map(function(d){return d===ds[q.di]?COL.r:'rgba(63,95,168,.55)'}),fy:nf}],
      note:[['g','깊이 4~6에서 시험 정확도가 가장 높아요. 그 뒤로는 학습 데이터의 우연까지 외웁니다.'],['a','잎이 707개인 나무는 규칙이 707개라는 뜻이에요. 대출 거절 이유를 설명해야 하는 금융에서는 얕은 나무가 더 쓸모 있을 수 있습니다.']]}}};

DASHES['11']={tag:'11회차',title:'AR 모델과 "어제 그대로"',sub:'마지막 120거래일 종가 예측 (실제 주가)',play:'li',playLabel:'과거 1일→20일',
  params:[['ai','종목',0,2,1,1,function(v){return ANM[AS[v]]}],['li','과거 며칠(lags)',0,4,1,2,function(v){return [1,2,5,10,20][v]+'일'}]],
  f:function(q){var a=AS[q.ai],lg=[1,2,5,10,20][q.li],R=FD.ar[a][lg],P=FD.port[a].slice(-120),xs=seqv(1,120,120);
    return {k:[['$'+nf(R.mae,1),'AR('+lg+') MAE','r'],['$'+nf(R.naive_mae,1),'어제 그대로 MAE','g'],[P1(R.mape),'AR MAPE','a'],[P0(FD.ar_dir[a][0]),'방향 적중(수익률 AR5)','i']],
      c:[{t:'line',title:ANM[a]+' 실제와 예측',xs:xs,ys:[{n:'실제',c:COL.s,d:P},{n:'AR('+lg+')',c:COL.r,d:R.pred,w:1.5}],fy:nf,fx:function(v){return v+'일'},xl:'시험 기간'},
        {t:'bar',title:'lags별 MAE (점선 = 어제 그대로)',labels:['1','2','5','10','20'],vals:[1,2,5,10,20].map(function(l){return FD.ar[a][l].mae}),cols:[1,2,5,10,20].map(function(l){return l===lg?COL.r:'rgba(63,95,168,.55)'}),fy:function(v){return nf(v,1)},hline:R.naive_mae,hlabel:'어제 그대로'}],
      note:[['g','과거를 길게 봐도 오차가 줄지 않아요. 가격은 어제 값에서 크게 벗어나지 않는 "임의보행"에 가깝기 때문입니다.'],['a','교육용 예시이며 투자 자문이 아닙니다.']]}}};

DASHES['12']={tag:'12회차',title:'꼬리를 자르면 대표값은?',sub:'보험료 상위 일부를 뺄 때 평균과 중앙값의 변화 (보험 1,338명)',play:'trim',playLabel:'0%→20% 빼기',
  params:[['trim','상위 몇 %를 빼면',0,20,1,0,function(v){return v+'%'}]],
  f:function(q){var v=FD.ins.ch.slice().sort(function(a,b){return a-b}),n=Math.round(v.length*(1-q.trim/100)),u=v.slice(0,n),ts=seqv(0,20,21);function tm(t){var w=v.slice(0,Math.round(v.length*(1-t/100)));return [mean(w),median(w)]}
    var m=tm(q.trim);return {k:[['$'+nf(m[0]),'평균','r'],['$'+nf(m[1]),'중앙값','g'],['$'+nf(m[0]-m[1]),'평균 − 중앙값','a'],[nf(v.length-n)+'명','뺀 고객','i']],
      c:[{t:'hist',title:'남은 고객의 보험료 분포',vals:u,lo:0,hi:65000,bins:40,fx:function(x){return nf(x/1000)+'천'},marks:[{x:m[0],l:'평균',c:COL.r},{x:m[1],l:'중앙값',c:COL.g}]},
        {t:'line',title:'뺀 비율에 따른 평균·중앙값',xs:ts,ys:[{n:'평균',c:COL.r,d:ts.map(function(t){return tm(t)[0]})},{n:'중앙값',c:COL.g,d:ts.map(function(t){return tm(t)[1]})}],fy:function(x){return '$'+nf(x)},fx:function(x){return x+'%'},mark:{x:q.trim},xl:'상위 몇 % 제거'}],
      note:[['g','꼬리를 자르면 평균은 크게 움직이고 중앙값은 조금만 움직여요. 중앙값이 극단값에 강한(로버스트) 대표값입니다.'],['a','그렇다고 꼬리를 지우면 안 돼요. 흡연·비만 고객의 높은 보험료는 보험사에 가장 중요한 정보입니다.']]}}};

DASHES['13']={tag:'13회차',title:'이동평균 교차 전략 비교',sub:'네 종목에 같은 규칙을 적용 (2013~2019, 거래 비용 0.1%)',play:'s',playLabel:'짧은 평균 5일→50일',
  params:[['s','짧은 이동평균',5,50,5,20,function(v){return v+'일'}],['l','긴 이동평균',30,200,10,60,function(v){return v+'일'}]],
  f:function(q){var l=Math.max(q.l,q.s+10),AA=['AMZN','NFLX','DPZ','BTC'],R=AA.map(function(a){return maBT(FD.port[a],q.s,l,.001)}),r0=R[0],xs=seqv(0,r0.eq.length-1,r0.eq.length);
    return {k:AA.map(function(a,i){return [nf(R[i].ret+1,1)+' / '+nf(R[i].bhr+1,1)+'배',ANM[a]+' 전략 / 보유',['i','r','a','g'][i]]}),
      c:[{t:'line',title:'아마존: 전략과 보유의 자산(배)',xs:xs,ys:[{n:'보유',c:COL.muted,d:r0.bh},{n:'교차 '+q.s+'/'+l,c:COL.g,d:r0.eq}],fy:function(v){return nf(v,1)},fx:function(i){var d=FD.port.dates[Math.round(i)];return d?d.slice(0,4):''}},
        {t:'bar',title:'최대 낙폭 (초록 = 전략, 회색 = 보유)',labels:AA.map(function(a){return ANM[a]}).reduce(function(o,x){return o.concat([x,''])},[]),pair:true,vals:R.reduce(function(o,r){return o.concat([-r.mdd*100,-r.bmdd*100])},[]),cols:R.reduce(function(o){return o.concat([COL.g,COL.muted])},[]),fy:function(v){return '−'+v.toFixed(0)+'%'}}],
      note:[['g','교차 전략은 대체로 최대 낙폭을 줄이지만, 꾸준히 오른 종목에서는 수익도 줄어요.'],['a','같은 기간 데이터로 규칙을 고르고 같은 기간에 평가하면 결과가 부풀려져요(과최적화). 교육용이며 투자 자문이 아닙니다.']]}}};

DASHES['14']={tag:'14회차',title:'비식별 조치의 균형',sub:'보험 고객 1,338명 — 나이 폭·지역·자녀 수 공개 여부에 따른 k',play:'wi',playLabel:'나이 폭 1살→20살',
  params:[['wi','나이 묶는 폭',0,3,1,0,function(v){return [1,5,10,20][v]+'살'}],['reg','지역 (0 삭제 · 1 공개)',0,1,1,1,function(v){return v?'공개':'삭제'}],['ch','자녀 수 (0 삭제 · 1 공개)',0,1,1,1,function(v){return v?'공개':'삭제'}]],
  f:function(q){var w=[1,5,10,20][q.wi],o=FD.kanon.filter(function(k){return k.w===w&&k.reg===q.reg&&k.ch===q.ch})[0],ws=[1,5,10,20];
    return {k:[['k = '+o.k,'가장 작은 묶음','g'],[nf(o.groups),'묶음 수','i'],[nf(o.rows_small)+'명','5명 미만 묶음 속 사람','r'],[nf(o.small),'5명 미만 묶음 수','a']],
      c:[{t:'bar',title:'나이 폭별 위험한 사람 수 (지금 지역·자녀 설정)',labels:ws.map(function(x){return x+'살'}),vals:ws.map(function(x){return FD.kanon.filter(function(k){return k.w===x&&k.reg===q.reg&&k.ch===q.ch})[0].rows_small}),cols:ws.map(function(x){return x===w?COL.r:'rgba(63,95,168,.55)'}),fy:nf},
        {t:'bar',title:'나이 폭별 묶음 수 (정보의 양)',labels:ws.map(function(x){return x+'살'}),vals:ws.map(function(x){return FD.kanon.filter(function(k){return k.w===x&&k.reg===q.reg&&k.ch===q.ch})[0].groups}),cols:ws.map(function(x){return x===w?COL.g:'rgba(19,138,82,.4)'}),fy:nf}],
      note:[['g','위험(왼쪽)과 정보(오른쪽)는 함께 줄어요. 비식별은 둘 사이의 균형을 고르는 일입니다.'],['a','지역 하나만 지워도 k가 1에서 11~13으로 뛰는 경우가 있어요. 어떤 열이 사람을 가리키는지 먼저 찾는 것이 핵심입니다.']]}}};
