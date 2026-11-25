# -*- coding: utf-8 -*-
"""핀데이터 그룹 본사 타워 — 3D 첫 화면(건물 안내)

목차(index)는 건물 전체를, 회차 쪽은 그 회차가 들어 있는 층을 3D로 보여 주고
층 평면(방 = 이 쪽의 열)과 둘러보는 순서를 안내한다.

- build.py / build_extra.py 가 nav 바로 뒤, 표지 그림 앞에 tower_html(key)를 넣는다.
- 이미 빌드된 HTML에는 add_tower.py 로 같은 블록을 넣거나 갈아 끼운다(표식 <!--tower:start--> … <!--tower:end-->).
- three.js 는 CDN(jsdelivr)에서 불러온다. 불러오지 못하면 오른쪽 안내판만으로 쓸 수 있다.
"""
import os, json, html

B = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(B, 'tower.css'), encoding='utf-8').read()
JS = open(os.path.join(B, 'tower.js'), encoding='utf-8').read()
THREE_VER = '0.170.0'

COMPANY = dict(ko='핀데이터 그룹', en='FinData Group', hq='여의도 본사 타워',
               motto='고객 데이터로 금융 서비스를 설계하는 핀테크 회사',
               note='가상의 핀테크 기업입니다. 층마다 한 부서가 있고, 부서마다 그 회차의 데이터 분석 도구로 일합니다.')

CLOCKS = [('서울', 'Asia/Seoul'), ('런던', 'Europe/London'), ('뉴욕', 'America/New_York'), ('싱가포르', 'Asia/Singapore')]

PAL = ['#3f5fa8', '#138a52', '#d23f2c', '#2563c9', '#a8329f', '#b77800', '#14899a', '#7a45d6']

def LES(a, b, c, sa, sb, sc):
    return [('three', '안내 데스크', '3줄 요약'), ('cast', '팀 라운지', '연구실 식구'), ('lv1', a, '단계 ① ' + sa), ('lv2', b, '단계 ② ' + sb), ('lv3', c, '단계 ③ ' + sc),
            ('dash', '상황실', '한눈에 보는 대시보드'), ('duel', '대결 홀', '초파리 대 주판봇 대결'), ('sum', '정리 데스크', '정리'), ('kg', '자료실', '지식 색인 · 꾸러미')]

REV = [('three', '안내 데스크', '3줄 요약'), ('cast', '팀 라운지', '연구실 식구'), ('summary', '요약 갤러리', '1부 요약'), ('orig', '교안 문제 시험장', '2부 교안 문제'),
       ('calc', '업무 계산실', '3부 업무 계산'), ('score', '점수판', '회차별 점수'), ('kg', '자료실', '지식 색인 · 꾸러미')]

IDX = [('three', '안내 데스크', '3줄 요약'), ('map', '층별 안내판', '회차 지도'), ('keys', '한 줄 핵심 게시판', '한 줄 핵심 모음'), ('dash', '종합 상황실', '종합 대시보드'),
       ('path', '개념 계단', '개념 흐름'), ('data', '데이터 창고', '실습 데이터'), ('how', '식구 라운지', '식구 · 사용법'), ('about', '자료 보관실', '자료와 원칙')]

def F(key, label, file, dept, en, branch, title, ep, biz, rooms):
    return dict(key=key, label=label, file=file, dept=dept, en=en, branch=branch, title=title, ep=ep, biz=biz, rooms=rooms)

# 아래에서 위로: 로비 → 1~7층 → 8층 중간 점검 라운지 → 9~14층 → 15층 전망대(기말 점검)
FLOORS = [
 F('00', 'L', 'index.html', '로비 · 안내 데스크', 'Lobby & Directory', '여의도 본사', '목차 — 핀테크 데이터 분석 기초', '목차',
   '본사 타워의 로비입니다. 층별 안내판에서 부서(회차)를 고르면 그 층으로 올라갑니다.', IDX),
 F('01', '1F', '01_fintech_industry.html', '핀테크 전략기획실', 'Fintech Strategy', '협업 지사 서울', '핀테크 산업의 이해와 핀테크 데이터', '01회차',
   '기존 금융과 핀테크가 무엇이 다른지, 인터넷은행·간편결제·로보어드바이저가 어떤 데이터로 돈을 버는지 정리하는 부서예요.',
   LES('은행 비교 회의실', '결제 흐름 상황판', '고객 데이터 열람실', '핀테크란', '비즈니스 모델', '핀테크 데이터')),
 F('02', '2F', '02_data_collection.html', '데이터 수집팀', 'Data Acquisition', '협업 지사 싱가포르', '핀테크 데이터 수집 기술', '02회차',
   '설문·Open API·공공데이터·웹 스크래핑으로 데이터를 모으고, 개인정보 보호를 점검하는 부서예요.',
   LES('데이터 지도실', '수집 방법 실험실', '개인정보 점검실', '데이터 특징', '수집 기술', '수집 시 고려사항')),
 F('03', '3F', '03_collection_plan.html', '데이터 기획실', 'Data Planning', '협업 지사 런던', '데이터 분석을 위한 준비 — 수집 계획', '03회차',
   '분석 목표를 먼저 정하고, 무엇을 얼마나 자주 어디서 모을지 계획서를 쓰는 부서예요.',
   LES('계획 수립실', '플랫폼 분석실', '데이터 사전 서고', '수집 계획', '서비스와 플랫폼', '세부 계획')),
 F('04', '4F', '04_analysis_concepts.html', '분석 도구 지원실', 'Analytics Enablement', '협업 지사 뉴욕', '데이터 분석 개념의 이해', '04회차',
   '엑셀부터 파이썬까지 도구를 고르고, 인공지능 모델을 어떻게 만들고 검증하는지 표준을 정하는 부서예요.',
   LES('도구 상담실', '모델 분류 보드', '검증 실험실', '분석 도구', 'AI 모델의 종류', '개발·검증 과정')),
 F('05', '5F', '05_preprocessing.html', '데이터 전처리 센터', 'Data Preparation', '협업 지사 서울', '분류모형(1) — Colab과 데이터 전처리', '05회차',
   '분석 환경을 만들고, 데이터를 입력하고, 결측값·이상치·라벨을 손보는 "부엌" 같은 부서예요.',
   LES('Colab 작업실', '이상치 점검실', '라벨링 작업대', '환경과 자료 구조', '결측값·이상치', '라벨과 데이터 세팅')),
 F('06', '6F', '06_knn_svm.html', '고객 이탈 분석팀', 'Churn Analytics', '협업 지사 토론토', '데이터 분석 실습 — KNN·SVM·분할·표준화', '06회차',
   '어떤 고객이 떠날지 가까운 이웃(KNN)과 경계선(SVM)으로 가려내는 부서예요.',
   LES('이웃 투표실', '경계선 설계실', '저울 맞추는 방', 'KNN', 'SVM', '분할과 표준화')),
 F('07', '7F', '07_model_evaluation.html', '모델 검증실', 'Model Validation', '협업 지사 프랑크푸르트', '데이터 분석 모델의 평가', '07회차',
   '모델이 정말 쓸 만한지 혼동행렬·ROC·교차검증으로 따지고, 출시 전에 통과 도장을 찍는 부서예요.',
   LES('혼동행렬 심사실', 'ROC 전망실', '교차검증 실험실', '혼동행렬과 지표', 'ROC와 AUC', '최적화')),
 F('08', '8F', '08_midterm_review.html', '중간 점검 라운지', 'Sky Bridge Lounge', '서관·동관을 잇는 스카이브리지', '중간 요약정리 및 퀴즈 — 1~7회차', '1~7회차 점검',
   '서관 1~7층을 돌아본 직원들이 동관으로 건너가기 전에 쉬어 가며 요약을 보고, 교안 문제와 업무 계산으로 점검하는 스카이브리지 라운지예요.', REV),
 F('09', '9F', '09_regression.html', '보험 가격 산정팀', 'Insurance Pricing', '협업 지사 취리히', '데이터 분석 모형: 회귀모형(1)', '09회차',
   '보험료·소비 금액처럼 "얼마"를 맞히는 회귀 모델을 만들고, 오차를 MSE·RMSE·R²로 재는 부서예요.',
   LES('KNN 회귀실', '곡선 맞춤 공방', '오차 계측실', '회귀와 KNN 회귀', '선형·비선형', '성능 지표')),
 F('10', '10F', '10_logistic_tree.html', '신용 리스크 모델링실', 'Credit Risk Modeling', '협업 지사 런던', '데이터 분석 모형: 회귀모형(2) — 로지스틱·결정나무·특성공학', '10회차',
   '확률을 내놓는 로지스틱 회귀, 설명하기 쉬운 결정나무, 좋은 특성을 만드는 특성공학을 다루는 부서예요.',
   LES('확률 곡선실', '의사결정나무 정원', '특성 공방', '로지스틱 회귀', '결정나무', '특성공학')),
 F('11', '11F', '11_deep_learning_timeseries.html', '시장 데이터 랩', 'Market Data Lab', '협업 지사 뉴욕', '딥러닝 모델과 시계열 데이터 분석', '11회차',
   '신경망의 원리를 익히고, 주가 같은 시계열을 정상성·AR·ARIMA로 다루는 랩이에요. (교육용 · 투자 자문 아님)',
   LES('뉴런 실험실', '시계열 관측소', '예측 시뮬레이터', '신경망', '시계열과 정상성', 'AR 모델')),
 F('12', '12F', '12_visualization.html', '데이터 시각화 스튜디오', 'Visualization Studio', '협업 지사 파리', '핀테크 데이터 시각화', '12회차',
   '대표값·흩어짐·상관을 그림으로 보여 주고, 목적에 맞는 차트를 골라 보고서를 만드는 스튜디오예요.',
   LES('분포 갤러리', '상관 히트맵실', '차트 고르는 방', '대표값과 치우침', '상관과 인과', '차트 고르기')),
 F('13', '13F', '13_robo_advisor.html', '로보어드바이저 사업부', 'Robo-Advisory', '협업 지사 싱가포르', '데이터 기반의 핀테크 서비스 기획 — 로보어드바이저', '13회차',
   '고객의 투자성향을 데이터로 받아 자산을 나누고, 규칙 기반 매매와 성과를 평가하는 서비스 부서예요. (교육용 · 투자 자문 아님)',
   LES('투자성향 상담실', '수수료 비교실', '매매 규칙 연구실', '데이터 기반 서비스', '서비스 기획', '알고리즘과 성과')),
 F('14', '14F', '14_security_quality.html', '정보보호·데이터 거버넌스 센터', 'Security & Data Governance', '여의도 본사 직할', '데이터 보안 및 품질 관리', '14회차',
   '보안 3요소와 법규를 지키고, 비식별 조치와 품질 점검으로 데이터를 믿을 수 있게 관리하는 센터예요.',
   LES('보안 관제실', '비식별 처리실', '품질 진단실', '보안과 거버넌스', '비식별과 프라이버시', '품질과 표준화')),
 F('15', '15F', '15_final_review.html', '전망대 · 기말 점검', 'Observatory & Final Review', '모든 지사 공용 공간', '기말 요약정리 및 퀴즈 — 9~14회차', '9~14회차 점검',
   '9~14층을 돌아본 뒤 맨 위층 전망대에서 건물 전체를 내려다보며 요약하고 퀴즈로 마무리하는 곳이에요.', REV),
]
for i, f in enumerate(FLOORS):
    f['color'] = '#5d6278' if f['key'] in ('00',) else ('#138a52' if f['key'] in ('08', '15') else PAL[(i - 1) % len(PAL)])
KEYS = [f['key'] for f in FLOORS]
BYKEY = {f['key']: f for f in FLOORS}

e = lambda s: html.escape(str(s), quote=True)

def floor_name(f):
    return f'{f["label"]} {f["dept"]}'

def _data(cur):
    fl = [dict(key=f['key'], label=f['label'], dept=f['dept'], en=f['en'], branch=f['branch'], title=f['title'], ep=f['ep'], file=f['file'],
               biz=f['biz'], color=f['color'], rooms=[dict(id=a, name=b, sec=c) for a, b, c in f['rooms']]) for f in FLOORS]
    return dict(cur=cur, company=COMPANY, floors=fl)

def _route_items(f):
    o = []
    for i, (a, b, c) in enumerate(f['rooms']):
        tag = 'EV' if i == 0 else str(i)
        o.append(f'<li data-i="{i}"><a href="#{a}"><i>{tag}</i><b>{e(b)}</b><span>{e(c)}</span></a></li>')
    return ''.join(o)

def _panel_floor(f):
    i = KEYS.index(f['key'])
    dn = FLOORS[i - 1] if i > 1 else None          # 1F의 아래는 로비(목차)
    up = FLOORS[i + 1] if i + 1 < len(FLOORS) else None
    el = []
    el.append(f'<a class="dn" href="{dn["file"]}" title="{e(dn["title"])}">▼ {e(floor_name(dn))}</a>' if dn else '<span class="dn off">▼ 아래층 없음</span>')
    el.append('<a class="lob" href="index.html">로비 · 목차</a>')
    el.append(f'<a class="up" href="{up["file"]}" title="{e(up["title"])}">▲ {e(floor_name(up))}</a>' if up else '<span class="up off">▲ 전망대가 맨 위층</span>')
    first = '엘리베이터에서 내리면 안내 데스크(3줄 요약)부터 들러요. 걷는 사람 표시가 둘러보는 순서를 따라 움직입니다.'
    return f'''<aside class="tw-panel" aria-label="{e(f["label"])} 층 안내">
<p class="tw-co"><b>{e(COMPANY["ko"])}</b> {e(COMPANY["hq"])} · <span>{e(COMPANY["en"])}</span></p>
<div class="tw-fl"><span class="tw-badge" style="--c:{f["color"]}">{e(f["label"])}</span><div><h2>{e(f["dept"])}</h2><p class="tw-en">{e(f["en"])} · {e(f["branch"])}</p></div></div>
<p class="tw-ep"><b>{e(f["ep"])}</b> {e(f["title"])}</p>
<p class="tw-biz">{e(f["biz"])}</p>
<h3>이 층 둘러보는 순서</h3>
<p class="tw-tip">{first}</p>
<ol class="tw-route">{_route_items(f)}</ol>
<nav class="tw-elev" aria-label="엘리베이터 — 층 이동">{"".join(el)}</nav>
</aside>'''

def _panel_index(f):
    rows = []
    for g in reversed(FLOORS[1:]):
        rows.append(f'<li data-k="{g["key"]}"><a href="{g["file"]}"><span class="tw-badge" style="--c:{g["color"]}">{e(g["label"])}</span><b>{e(g["dept"])}</b><span>{e(g["ep"])} · {e(g["title"])}</span></a></li>')
    rows.append(f'<li data-k="00" class="here"><a href="#three"><span class="tw-badge" style="--c:{f["color"]}">L</span><b>로비 · 안내 데스크</b><span>지금 계신 곳 · 이 목차 쪽</span></a></li>')
    clocks = ''.join(f'<span data-tz="{tz}"><b>{c}</b><i>--:--</i></span>' for c, tz in CLOCKS)
    return f'''<aside class="tw-panel" aria-label="층별 안내판">
<p class="tw-co"><b>{e(COMPANY["ko"])}</b> {e(COMPANY["hq"])} · <span>{e(COMPANY["en"])}</span></p>
<h2>층별 안내판</h2>
<p class="tw-biz">{e(COMPANY["motto"])}. 쌍둥이 타워 중 서관에 1~7층, 동관 고층부에 9~14층 부서가 있고, 두 동을 잇는 8층 스카이브리지 라운지와 동관 15층 전망대에서 요약정리와 퀴즈를 봅니다. 건물의 층을 누르거나 아래 안내판에서 골라 올라가세요.</p>
<div class="tw-clock" aria-label="세계 지사 시각">{clocks}</div>
<ol class="tw-dir">{"".join(rows)}</ol>
<p class="tw-note">{e(COMPANY["note"])}</p>
</aside>'''

def tower_html(key):
    f = BYKEY[key]
    idx = key == '00'
    panel = _panel_index(f) if idx else _panel_floor(f)
    tools = ('<button type="button" data-v="b" class="on">건물 전체</button><button type="button" data-v="spin" aria-pressed="true">자동 회전</button>' if idx else
             '<button type="button" data-v="b">건물 전체</button><button type="button" data-v="p" class="on">이 층 평면</button>')
    hint = '드래그로 돌려 보고 층을 누르면 안내 카드가 열려요' if idx else '방을 누르면 그 자리로 내려갑니다 · 드래그로 돌려 보기'
    cap = (f'{COMPANY["ko"]} 본사 타워 3D 모형: 로비부터 15층 전망대까지 16개 층, 층마다 한 부서(회차)' if idx else
           f'{COMPANY["ko"]} 본사 타워 3D 모형에서 {f["label"]} {f["dept"]}을(를) 건물 밖으로 꺼내 보여 주는 층 평면')
    data = json.dumps(_data(key), ensure_ascii=False).replace('</', '<\\/')
    imap = json.dumps({'imports': {'three': f'https://cdn.jsdelivr.net/npm/three@{THREE_VER}/build/three.module.js',
                                   'three/addons/': f'https://cdn.jsdelivr.net/npm/three@{THREE_VER}/examples/jsm/'}})
    return f'''<!--tower:start-->
<style>
{CSS}
</style>
<section class="tower{' tw-idx' if idx else ''}" id="tower" data-floor="{key}" aria-label="{e(COMPANY['ko'])} 본사 타워 — 건물 안내">
<div class="tw-stage" role="img" aria-label="{e(cap)}">
<div class="tw-cv" aria-hidden="true"></div><div class="tw-labels" aria-hidden="true"></div>
<div class="tw-tools">{tools}</div>
<p class="tw-hint">{hint}</p>
<div class="tw-card" hidden></div>
<div class="tw-err" hidden>3D 건물을 불러오지 못했습니다(인터넷 연결 · WebGL 확인). 오른쪽 안내판으로 그대로 이동할 수 있어요.</div>
<div class="tw-load">건물을 짓는 중…</div>
</div>
{panel}
</section>
<script type="application/json" id="towerData">{data}</script>
<script type="importmap">{imap}</script>
<script type="module">
{JS}
</script>
<!--tower:end-->
'''

NAV_LINK = '<a href="#tower">건물 안내</a>'
