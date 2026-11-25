#!/usr/bin/env python3
"""핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01 — 연구실 해설(비전공자판) 빌드.

사용:  cd src && python3 hands_on/h01_build.py ..      → 저장소 루트에 hands_on_01.html
- 숫자는 hands_on/01/*/data 의 실제 파일에서 다시 계산한다(대출 장부 441MB만 노트북 실행 결과를 상수로 쓰고 assert로 대조 가능).
- 캐릭터 그림은 src/build/sprites.json(저장소에 넣지 않음, README 참고)에서 가져온다.
"""
import os, sys, json, re, html, math
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.dirname(HERE); ROOT = os.path.dirname(SRC)
sys.argv = [sys.argv[0]] + (sys.argv[1:] or [ROOT])
OUTDIR = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.join(SRC, 'build')); sys.path.insert(0, os.path.join(SRC, 'pages'))
import build as B
from _mk import Q, G
e = html.escape
D = os.path.join(ROOT, 'hands_on', '01')
FILE = 'hands_on_01.html'
GH = 'https://github.com/adminmrobo/fintech_data_analysis/tree/main/hands_on/01/'
COLAB = 'https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/'
nf = lambda x, d=0: f'{x:,.{d}f}'

# ───────────────────────── 1. 실제 데이터로 숫자 계산 ─────────────────────────
def rd(folder, f, **kw): return pd.read_csv(os.path.join(D, folder, 'data', f), low_memory=False, **kw)
A = 'A_customer_data_tour'; Bf = 'B_fraud_phishing_check'; C = 'C_portfolio_price_diary'; Df = 'D_loan_ledger_check'; E = 'E_dictionary_and_bankruptcy'; F = 'F_text_and_ratings'
bank = rd(A, 'Bank_customers_data.csv'); dm = rd(A, 'DirectMarketing.csv'); ins = rd(A, 'insurance.csv'); tr = rd(A, 'travel insurance.csv')
N = {}
N['bank_shape'] = bank.shape; ac = bank.Attrition_Flag.value_counts(); N['bank_exist'], N['bank_left'] = int(ac['Existing Customer']), int(ac['Attrited Customer'])
N['bank_left_pct'] = N['bank_left'] / len(bank) * 100
tc = bank.groupby('Attrition_Flag').Total_Trans_Ct.mean(); N['ct_left'], N['ct_exist'] = tc['Attrited Customer'], tc['Existing Customer']
N['dm_shape'] = dm.shape; N['dm_hist_na'] = int(dm.History.isna().sum())
N['ins_shape'] = ins.shape; sm = ins.groupby('smoker').charges.mean(); N['ins_no'], N['ins_yes'] = sm['no'], sm['yes']; N['ins_ratio'] = N['ins_yes'] / N['ins_no']
N['tr_shape'] = tr.shape; N['tr_claim'] = int((tr.Claim == 'Yes').sum()); N['tr_gender_na'] = int(tr.Gender.isna().sum()); N['tr_age118'] = int((tr.Age >= 118).sum()); N['tr_dur_neg'] = int((tr.Duration < 0).sum())
ph = rd(Bf, 'Website Phishing.csv'); cl = rd(Bf, 'insurance_claims.csv')
pv = ph.Result.value_counts(); N['ph_shape'] = ph.shape; N['ph_bad'], N['ph_sus'], N['ph_ok'] = int(pv[-1]), int(pv[0]), int(pv[1])
N['cl_shape'] = cl.shape; N['cl_y'] = int((cl.fraud_reported == 'Y').sum()); N['cl_nan'] = int(cl.authorities_contacted.isna().sum())
N['cl_q'] = {c: int((cl[c] == '?').sum()) for c in cl.columns if (cl[c] == '?').any()}
sev = (cl.fraud_reported == 'Y').groupby(cl.incident_severity).mean(); N['sev'] = sev.to_dict()
pf = rd(C, 'portfolio_data.csv'); px = pf.set_index(pd.to_datetime(pf.Date))[['AMZN', 'DPZ', 'BTC', 'NFLX']]
N['pf_shape'] = pf.shape; N['pf_first'] = px.iloc[0].to_dict(); N['pf_last'] = px.iloc[-1].to_dict(); N['pf_x'] = (px.iloc[-1] / px.iloc[0]).to_dict(); N['pf_vol'] = (px.pct_change().std() * 100).to_dict()
it = rd(C, 'international_portfolio_data.csv', index_col=0); N['it_shape'] = it.shape; N['it_obj'] = [c for c in ['kospi', 'gold', 'dol', 'VIX1'] if it[c].dtype == object or str(it[c].dtype) == 'str']
N['it_kospi_na'] = int(it.kospi.isna().sum()); wd = pd.to_datetime(it.real_date).dt.dayofweek; N['it_wkend_na'] = it.kospi.isna().groupby(wd >= 5).mean().to_dict()
npf = rd(C, 'new_portfolio_data.csv'); N['npf_shape'] = npf.shape
b4 = rd(Df, 'bank_customers.csv', header=None); d4 = rd(Df, 'direct_marketimg.csv', header=None); N['r4_same'] = bool(b4.equals(d4)); N['r4_rows'] = len(b4)
# 대출 장부(441MB): D_loan_ledger_check.ipynb 실행 결과 (887,379 × 74)
LOAN = dict(shape=(887379, 74), charged=45248, current=601779, paid=207723, default=1219,
            rate={'A': 7.24, 'B': 10.83, 'C': 13.98, 'D': 17.18, 'E': 19.90, 'F': 23.58, 'G': 25.63}, null90=17, joint_na=0.999)
desc = rd(E, 'loan_data_description.csv'); N['desc_rows'] = len(desc)
bk = rd(E, 'company_bankruptcy.csv'); N['bk_shape'] = bk.shape; N['bk_1'] = int(bk['Bankrupt?'].sum()); N['bk_pct'] = N['bk_1'] / len(bk) * 100
N['bk_space'] = sum(1 for c in bk.columns if c != c.strip())
bk.columns = bk.columns.str.strip(); dr = bk.groupby('Bankrupt?')['Debt ratio %'].mean(); N['bk_debt'] = dr.to_dict()
se = rd(F, 'Financial_Sentiment_Analysis.csv', index_col=0); sv = se.Sentiment.value_counts(); N['se_shape'] = se.shape; N['se'] = sv.to_dict(); N['se_dup'] = int(se.Sentence.duplicated().sum())
fk = rd(F, 'News_Fake_and_Real_Fake.csv.gz'); tu = rd(F, 'News_Fake_and_Real_True.csv.gz'); N['fake'], N['true'] = len(fk), len(tu)
N['fake_subj'] = sorted(fk.subject.unique()); N['true_subj'] = sorted(tu.subject.unique()); N['subj_overlap'] = len(set(fk.subject) & set(tu.subject))
tn = rd(F, 'text_similarity_train.csv', index_col=0); tt = rd(F, 'text_similarity_test.csv', index_col=0); N['sim_tr'], N['sim_te'] = len(tn), len(tt); N['sim_true'] = int(tn.same_security.sum())
ra = rd(F, 'ratings_small.csv'); N['ra_n'] = len(ra); N['ra_u'] = ra.userId.nunique(); N['ra_m'] = ra.movieId.nunique(); N['ra_density'] = N['ra_n'] / (N['ra_u'] * N['ra_m']) * 100
N['ra_dist'] = ra.rating.value_counts().sort_index().to_dict(); N['ra_mean'] = ra.rating.mean()
nfx = rd(F, 'netflix_list.csv.gz'); N['nf_shape'] = nfx.shape
# 손계산 검산
assert round(N['bank_left_pct'], 1) == 16.1 and N['bank_left'] == 1627
assert round(N['pf_last']['AMZN'] / N['pf_first']['AMZN'] * 100) == 741
assert round(N['ra_density'], 2) == 1.64 and N['ra_u'] * N['ra_m'] == 6083286
assert round(N['bk_pct'], 1) == 3.2 and N['bk_1'] == 220 and N['bk_shape'] == (6819, 96)
bmax = px.BTC.max(); bmin = px.BTC[px.BTC.idxmax():].min(); assert round((1 - bmin / bmax) * 100) == 83
assert N['r4_same'] and N['subj_overlap'] == 0 and N['cl_y'] == 247
print({k: v for k, v in N.items() if not isinstance(v, (dict, list))})

import glob
NFILES = len([f for f in glob.glob(os.path.join(D, '*', 'data', '*')) if not re.search(r'part[12]$', f)])
assert NFILES == 26, NFILES

# ───────────────────────── 2. 그림 (외부 라이브러리 없는 SVG) ─────────────────────────
BLUE, ORANGE, RED, TEAL, GRAY, GREEN = '#3f5fa8', '#d9822b', '#cc3434', '#14899a', '#8a90a0', '#138a52'
def svg_bars(items, title, unit='', w=520, dec=0, note=''):
    """items: [(라벨, 값, 색)] 세로 막대."""
    n = len(items); h = 250; top, bot, left = 36, 46, 12; bw = (w - left * 2) / n
    mx = max(v for _, v, _ in items) * 1.15
    o = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}"><text x="{w/2}" y="20" text-anchor="middle" class="ct">{e(title)}</text>']
    for i, (lab, v, c) in enumerate(items):
        bh = (h - top - bot) * v / mx; x = left + i * bw + bw * 0.18; y = h - bot - bh
        o.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw*0.64:.1f}" height="{bh:.1f}" rx="4" fill="{c}"/>')
        o.append(f'<text x="{x+bw*0.32:.1f}" y="{y-6:.1f}" text-anchor="middle" class="cv">{nf(v, dec)}{unit}</text>')
        o.append(f'<text x="{x+bw*0.32:.1f}" y="{h-bot+18}" text-anchor="middle" class="cl">{e(lab)}</text>')
    o.append(f'<line x1="{left}" y1="{h-bot}" x2="{w-left}" y2="{h-bot}" stroke="#c9ced9"/>')
    if note: o.append(f'<text x="{w/2}" y="{h-6}" text-anchor="middle" class="cn">{e(note)}</text>')
    return ''.join(o) + '</svg>'

def svg_hbars(items, title, unit='%', w=520, dec=1):
    h = 44 + 38 * len(items); left = 130; mx = max(v for _, v, _ in items) * 1.18
    o = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}"><text x="{w/2}" y="20" text-anchor="middle" class="ct">{e(title)}</text>']
    for i, (lab, v, c) in enumerate(items):
        y = 36 + i * 38; bw = (w - left - 20) * v / mx
        o.append(f'<text x="{left-8}" y="{y+18}" text-anchor="end" class="cl">{e(lab)}</text><rect x="{left}" y="{y+4}" width="{bw:.1f}" height="22" rx="4" fill="{c}"/><text x="{left+bw+6:.1f}" y="{y+20}" class="cv">{nf(v, dec)}{unit}</text>')
    return ''.join(o) + '</svg>'

def svg_lines(df, title, log=False, w=620, h=300, colors=None, ylab=''):
    colors = colors or [BLUE, ORANGE, RED, TEAL]
    d = df.iloc[::5]; left, right, top, bot = 56, 92, 34, 34
    vals = d.values.flatten(); lo, hi = (math.log10(vals.min()), math.log10(vals.max())) if log else (0, vals.max())
    Y = lambda v: top + (h - top - bot) * (1 - ((math.log10(v) if log else v) - lo) / (hi - lo))
    X = lambda i: left + (w - left - right) * i / (len(d) - 1)
    o = [f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="{e(title)}"><text x="{w/2}" y="20" text-anchor="middle" class="ct">{e(title)}</text>']
    ticks = [10, 100, 1000, 10000] if log else [0, 2000, 4000, 6000, 8000]
    for t in ticks:
        if (math.log10(t) if log else t) < lo - 1e-9 or (math.log10(t) if log else t) > hi + 1e-9: continue
        o.append(f'<line x1="{left}" y1="{Y(t):.1f}" x2="{w-right}" y2="{Y(t):.1f}" stroke="#e3e6ee"/><text x="{left-6}" y="{Y(t)+4:.1f}" text-anchor="end" class="cl">{nf(t)}</text>')
    yrs = {}
    for i, dt in enumerate(d.index):
        if dt.year not in yrs and dt.month == 1: yrs[dt.year] = i
    for yv, i in yrs.items(): o.append(f'<text x="{X(i):.1f}" y="{h-12}" text-anchor="middle" class="cl">{yv}</text>')
    for k, col in enumerate(d.columns):
        pts = ' '.join(f'{X(i):.1f},{Y(v):.1f}' for i, v in enumerate(d[col].values))
        o.append(f'<polyline points="{pts}" fill="none" stroke="{colors[k]}" stroke-width="2"/>')
        o.append(f'<text x="{w-right+6}" y="{Y(d[col].values[-1])+4:.1f}" class="cv" fill="{colors[k]}">{col}</text>')
    if ylab: o.append(f'<text x="14" y="{top-8}" class="cl">{e(ylab)}</text>')
    return ''.join(o) + '</svg>'

def svg_dots(k, n, title, w=520):
    """100개 점 중 k개 빨강 (불균형·희소 보여 주기)."""
    o = [f'<svg class="chart" viewBox="0 0 {w} 230" role="img" aria-label="{e(title)}"><text x="{w/2}" y="20" text-anchor="middle" class="ct">{e(title)}</text>']
    for i in range(100):
        r, c = divmod(i, 20); o.append(f'<rect x="{60+c*20}" y="{36+r*34}" width="16" height="26" rx="3" fill="{RED if i < k else "#d6dbe6"}"/>')
    o.append(f'<text x="{w/2}" y="222" text-anchor="middle" class="cn">빨간 상자 {k}개 = 100곳 중 부도 기업 약 {k}곳</text>')
    return ''.join(o) + '</svg>'

CH = {}
CH['A1'] = svg_bars([('남은 고객', N['bank_exist'], BLUE), ('떠난 고객', N['bank_left'], ORANGE)], '은행 고객 10,127명 — 남은 고객과 떠난 고객', '명')
CH['A2'] = svg_bars([('비흡연', N['ins_no'], BLUE), ('흡연', N['ins_yes'], ORANGE)], '흡연 여부별 평균 의료비($) — 1,338명', '', note=f'흡연자가 약 {N["ins_ratio"]:.1f}배')
sevk = [('Major Damage', '큰 파손'), ('Total Loss', '전손(못 고침)'), ('Minor Damage', '작은 파손'), ('Trivial Damage', '아주 작은 흠')]
CH['B1'] = svg_hbars([(ko, N['sev'][k] * 100, RED if k == 'Major Damage' else GRAY) for k, ko in sevk], '사고 손상 정도별 허위 청구 비율')
CH['C_robo'] = svg_lines(px, '주판봇 팀 차트 — 원래 가격 그대로 (달러)', log=False, ylab='가격($)')
CH['C_fly'] = svg_lines(px / px.iloc[0] * 100, '초파리 팀 차트 — 첫날을 100으로 맞추고 로그 눈금', log=True, ylab='첫날=100')
CH['D1'] = svg_bars([(g, v, BLUE if g in 'AB' else (ORANGE if g in 'CDE' else RED)) for g, v in LOAN['rate'].items()], '신용등급별 평균 대출 금리(%) — 887,379건', '%', dec=1, note='A가 가장 믿을 만한 등급, G가 가장 위험한 등급')
CH['E1'] = svg_dots(round(N['bk_pct']), 100, '기업 6,819곳 중 부도 220곳 (3.2%)')
CH['F1'] = svg_bars([('중립', N['se']['neutral'], GRAY), ('긍정', N['se']['positive'], GREEN), ('부정', N['se']['negative'], RED)], '금융 문장 5,842개의 감성 꼬리표', '개')
CH['F2'] = svg_bars([(f'{k:g}', v, ORANGE if k >= 4 else BLUE) for k, v in N['ra_dist'].items()], '영화 평점 100,004개의 분포 (0.5~5점)', '', w=620, note=f'평균 {N["ra_mean"]:.2f}점 — 높은 점수에 몰려 있어요')

# ───────────────────────── 3. 페이지 내용 ─────────────────────────
TEAM = {'fly': ('초파리 팀', ['fly', 'sia', 'asst', 'x2']), 'robo': ('주판봇 팀', ['robo', 'moa', 'x1', 'x3'])}
B.NAMES.update({'sia': '시아(인턴1)', 'moa': '모아(인턴2)', 'asst': '하루(조수)', 'x1': 'X1', 'x2': 'X2', 'x3': 'X3'})
ROLE = {'fly': '초파리 팀 조장', 'robo': '주판봇 팀 조장', 'sia': '초파리 팀', 'asst': '초파리 팀', 'x2': '초파리 팀', 'moa': '주판봇 팀', 'x1': '주판봇 팀', 'x3': '주판봇 팀', 'doc': '심판'}

def T(who, mood, text):
    return (who, mood, text)

# 라운드(=코드) 6개. 각 라운드: 형식·발표자·장면 대화·코드 설명·데이터 요약·실행 결과·함정·왜/수식·코드·심판·퀴즈
R = []
R.append(dict(
 id='rA', work='업무에서는: 떠난 고객 비율(16.1%)을 매달 같은 방식으로 세면, 이탈이 늘었는지 줄었는지 바로 보여요. 이탈 방지 캠페인의 출발점이에요.', code='A', name='고객 데이터 4종 둘러보기', folder=A, orig='Revolution', fmt='조별 발표', team='fly', presenters='초파리 팀 (시아 · 하루 · X2)',
 lead='표 네 권(은행 고객, 쇼핑몰 마케팅, 건강보험료, 여행자보험)을 차례로 펼쳐 첫 장만 훑어보는 코드예요. 초파리 팀이 조별 발표를 맡았어요.',
 key='표를 열면 맨 먼저 "몇 줄, 몇 열, 빈 값은 어디?" 세 가지를 확인한다.',
 scene=[T('doc', 'front', '첫 발표는 초파리 팀이에요. 여러분 회사에 고객 명부 파일 네 개가 메일로 왔다고 생각해 보세요. 제일 먼저 뭘 확인할까요?'),
        T('sia', 'explain', '저희 팀은 "펼치기 → 세기 → 빈 곳 찾기" 순서로 했어요. 은행 고객은 10,127명, 항목은 21개예요.'),
        T('asst', 'report', f'떠난 고객이 {nf(N["bank_left"])}명, 전체의 {N["bank_left_pct"]:.1f}%예요. 떠난 고객은 1년 거래 횟수가 평균 {N["ct_left"]:.1f}번으로, 남은 고객({N["ct_exist"]:.1f}번)보다 적었어요.'),
        T('x2', 'think', f'저는 빈 값을 맡았어요. 여행자보험 장부는 성별이 {nf(N["tr_gender_na"])}줄이나 비어 있어요. 전체의 {N["tr_gender_na"]/N["tr_shape"][0]*100:.0f}%예요.'),
        T('robo', 'wow', '흡연자 보험료가 3.8배라니! 담배가 보험료를 3.8배로 만드는 거네요!'),
        T('fly', 'clip', '잠깐, 그건 "함께 나타난다"까지만 말할 수 있어. 나이·체질량지수도 같이 봐야 원인이라고 할 수 있지.')],
 what=['판다스(pandas)라는 표 다루는 도구를 불러와요.', '인터넷 주소에 있는 표(CSV 파일) 네 개를 하나씩 읽어 이름표를 붙여요: bank_customers, direct_marketing, insurance, travel_insurance.', '이름만 적어 실행하면 표의 앞뒤 몇 줄이 화면에 나와요. 원본 코드는 여기까지예요.', '실행판 노트북은 여기에 "몇 줄·몇 열", "빈 값 세기", "그룹별 평균"을 더했어요.'],
 analogy='새 학기에 반 명부 네 권을 받은 담임 선생님이 "몇 명이지? 어떤 항목이 적혀 있지? 빈 곳은?"부터 확인하는 일과 같아요.',
 data=[('은행 고객 명부', 'Bank_customers_data.csv', N['bank_shape'], '고객 한 명이 한 줄. 떠났는지(Attrition_Flag), 나이, 카드 등급, 1년 거래액 등', '빈 값 0 (단, "Unknown"이라는 글자로 숨은 빈 값이 교육수준 1,519줄)'),
       ('쇼핑몰 마케팅 명부', 'DirectMarketing.csv', N['dm_shape'], '고객 한 명이 한 줄. 연봉, 자녀 수, 1년 이용액(AmountSpent)', f'가입 기간(History) 빈 값 {N["dm_hist_na"]}줄'),
       ('건강보험료 표', 'insurance.csv', N['ins_shape'], '가입자 한 명이 한 줄. 나이, 체질량지수(BMI), 흡연, 의료비(charges)', '빈 값 0'),
       ('여행자보험 판매 장부', 'travel insurance.csv', N['tr_shape'], '판매 한 건이 한 줄. 판매처, 상품, 여행지, 보험금 청구 여부(Claim)', f'성별 빈 값 {nf(N["tr_gender_na"])}줄')],
 result=[f'은행 고객 {nf(N["bank_shape"][0])}명 중 떠난 고객 {nf(N["bank_left"])}명({N["bank_left_pct"]:.1f}%).',
         f'흡연자 평균 의료비 ${nf(N["ins_yes"])}, 비흡연자 ${nf(N["ins_no"])} — 약 {N["ins_ratio"]:.1f}배.',
         f'여행자보험 {nf(N["tr_shape"][0])}건 중 보험금 청구는 {nf(N["tr_claim"])}건({N["tr_claim"]/N["tr_shape"][0]*100:.1f}%)뿐.',
         f'이상한 값: 나이 118세가 {nf(N["tr_age118"])}건, 보험기간이 음수인 건 {N["tr_dur_neg"]}건.'],
 charts=['A1', 'A2'],
 trap=('AI 판단 코너 — 118세 여행자가 984명?', f'AI에게 "여행자보험 고객 나이를 요약해 줘"라고 하면 "최고령 118세"라고 그대로 말할 수 있어요. 118세 고객이 {nf(N["tr_age118"])}명이나 있는 건 이상하죠. 나이를 모를 때 넣어 둔 "임시 숫자"일 가능성이 커요. 숫자가 그럴듯한지 먼저 물어보세요.'),
 why=dict(problem='떠난 고객 1,627명 — 많은 걸까요, 적은 걸까요? 숫자 하나만 보면 판단이 안 돼요.', limit='개수(명)는 전체 크기가 다른 표끼리 비교할 수 없어요.', solve='전체로 나눠 백분율(%)로 바꾸면 크기가 다른 표도 비교할 수 있어요.', easy='"반에서 3명 지각"보다 "반의 10%가 지각"이 비교하기 쉬워요.'),
 math=dict(q='비율이요? 퍼센트 말하는 거죠? 그런데 무엇으로 나눠야 해요?', school='초등 비와 비율 — 비율 = 비교하는 양 ÷ 기준량', fx='이탈률(%) = 떠난 고객 수 ÷ 전체 고객 수 × 100', parts=[('떠난 고객 수', '떠났다고 적힌 줄의 개수 (1,627)'), ('전체 고객 수', '표의 줄 수 (10,127)'), ('× 100', '소수를 퍼센트로 바꾸기')],
           try_=['1,627 ÷ 10,127 = 0.1607', '0.1607 × 100 = 16.1%', '→ 고객 100명 중 약 16명이 떠났어요'], comment='기준량(전체)을 먼저 정하면 되는군요! 다음 표랑 비교할 수 있겠어요.'),
 snip=[("import pandas as pd", "표를 다루는 도구 판다스를 pd라는 짧은 이름으로 불러와요"), ("bank_customers = pd.read_csv('…/Bank_customers_data.csv')", "인터넷의 CSV 파일을 읽어 bank_customers라는 이름의 표로 만들어요"), ("bank_customers", "이름만 쓰면 표의 앞뒤 일부가 보여요"), ("bank_customers.shape", "(줄 수, 열 수) — (10127, 21)"), ("df['열'].value_counts()", "그 열에 어떤 값이 몇 번 나왔는지 세요")],
 judge=dict(score=(5, 4, 4), line='숫자 확인은 정확했어요. 흡연과 보험료는 "함께 나타난다"까지만 말한 점, 118세를 짚은 점이 좋았어요. 다만 "Unknown"이라는 글자로 숨은 빈 값은 놓쳤어요.'),
 quiz=[Q('표를 처음 열었을 때 가장 먼저 확인할 세 가지로 알맞은 것은?', ['평균·최댓값·최솟값', '줄 수·열 수·빈 값', '차트·색깔·제목'], 1, '크기(몇 줄·몇 열)와 빈 값을 먼저 알아야 다음 계산이 믿을 만해요.', '라운드 A의 "가져갈 한 가지"', '개념'),
       Q(f'여행자보험 장부에 118세 고객이 {nf(N["tr_age118"])}명 있어요. 가장 알맞은 해석은?', ['118세 여행자가 정말 많다', '나이를 모를 때 넣어 둔 임시 숫자일 수 있어 확인이 필요하다', '평균 나이를 올려 주니 그대로 둔다'], 1, '한 값에 수백 명이 몰려 있고 현실적이지 않으면 입력 규칙을 의심해요.', 'AI 판단 코너', 'AI 판단')]))
R.append(dict(
 id='rB', work='업무에서는: 조사팀은 손상이 큰 사고(Major Damage) 청구부터 먼저 확인해요. 허위 비율이 다른 청구의 5~9배라서 같은 시간에 더 많이 찾아요.', code='B', name='보험사기·피싱 탐지 데이터 점검', folder=Bf, orig='Revolution2', fmt='개인 발표', team='robo', presenters='X1 (주판봇 팀)',
 lead='가짜 웹사이트(피싱)와 허위 보험금 청구를 가려낼 때 쓰는 표를 불러와, 열마다 빈 값과 자료형을 세는 "건강검진"을 하는 코드예요. 주판봇 팀의 X1이 혼자 발표했어요.',
 key='빈 값은 NaN으로만 숨지 않는다. "?" 같은 글자로도 숨는다.',
 scene=[T('doc', 'front', '두 번째는 X1의 개인 발표예요. 보험회사 조사팀에서 "수상한 청구서 1,000장"을 받았다면, 무엇부터 셀까요?'),
        T('x1', 'think', f'저는 허위 청구부터 셌어요. 1,000건 중 허위가 {N["cl_y"]}건, 약 4건 중 1건이에요.'),
        T('x1', 'proud', '열마다 빈 값을 세 주는 명령으로는 경찰 연락기관 91줄뿐이라고 나와요. 그런데 표를 직접 보니 "?"가 잔뜩 있었어요!'),
        T('robo', 'happy', '역시 우리 팀! 빈 값이 91개라고 AI가 말했어도 X1은 속지 않았지.'),
        T('fly', 'point', '하나 더. 원본 코드는 여행자보험 표를 insurance_claim이라는 이름에 다시 담아서 앞의 청구 표를 덮어써. 이름표가 같으면 앞 표가 사라져.'),
        T('asst', 'shock', '어, 정말이에요. 실행판 노트북에서는 travel_insurance로 이름을 바꿨어요.')],
 what=['피싱 사이트 표를 읽고, 결과(Result) 열에서 정상·의심·피싱이 몇 개인지 세요.', '열 목록 확인 명령(info)으로 열마다 "비어 있지 않은 값의 수"와 자료형(숫자·글자)을 봐요.', '자동차 보험 청구 표(1,000건 × 39열)를 읽어 허위 청구(fraud_reported) 수를 세요.', '실행판은 "?"로 숨은 빈 값을 세고, 사고 손상 정도별 허위 청구 비율을 구해요.'],
 analogy='건강검진표에서 "기록 없음"이라고 적힌 곳만 세면 안 되고, 물음표로 대충 적어 둔 곳도 찾아야 하는 것과 같아요.',
 data=[('피싱 사이트', 'Website Phishing.csv', N['ph_shape'], '웹사이트 한 곳이 한 줄. 주소 길이·팝업·보안 인증 상태를 −1/0/1로 표시', '빈 값 0'),
       ('자동차 보험 청구', 'insurance_claims.csv', N['cl_shape'], '청구 한 건이 한 줄. 사고 종류·손상 정도·청구액·허위 여부(Y/N)', f'NaN {N["cl_nan"]}줄 + "?" {sum(N["cl_q"].values())}개'),
       ('건강보험료', 'insurance.csv', N['ins_shape'], '라운드 A와 같은 파일', '빈 값 0'),
       ('여행자보험', 'travel insurance.csv', N['tr_shape'], '라운드 A와 같은 파일', '성별 빈 값 다수')],
 result=[f'피싱 사이트 표: 피싱 {N["ph_bad"]}곳, 정상 {N["ph_ok"]}곳, 의심 {N["ph_sus"]}곳.',
         f'보험 청구 1,000건 중 허위 {N["cl_y"]}건(24.7%).',
         '"?" 빈 값: 충돌 유형 ' + str(N['cl_q']['collision_type']) + '개, 재산 피해 여부 ' + str(N['cl_q']['property_damage']) + '개, 경찰 보고서 여부 ' + str(N['cl_q']['police_report_available']) + '개.',
         f'손상이 큰 사고(Major Damage)의 허위 비율 {N["sev"]["Major Damage"]*100:.1f}% — 다른 정도(6.7~12.9%)보다 훨씬 높아요.'],
 charts=['B1'],
 trap=('AI 판단 코너 — "빈 값은 91개뿐입니다"', '빈 값 세기 명령이나 AI 요약은 NaN(컴퓨터가 아는 빈 값 표시)만 셉니다. 이 표에는 "?"가 881개 더 있어요. "빈 값이 없다"는 말을 들으면 "글자로 숨은 빈 값은?"이라고 되물어 보세요.'),
 why=dict(problem='허위 청구 247건이 어디에 몰려 있는지 알고 싶어요.', limit='전체 비율(24.7%) 하나로는 어느 사고에서 허위가 많은지 안 보여요.', solve='손상 정도별로 묶어서(그룹) 각각 비율을 구하면 몰린 곳이 보여요.', easy='전교 평균 점수 대신 반별 평균을 보면 어느 반이 다른지 보이는 것과 같아요.'),
 math=None,
 snip=[("website_phishing.info()", "열마다 비어 있지 않은 값의 수와 자료형을 보여 줘요"), ("insurance_claim = pd.read_csv('…insurance_claims.csv')", "보험 청구 표를 insurance_claim이라는 이름으로 읽어요"), ("insurance_claim = pd.read_csv('…travel%20insurance.csv')", "원본 코드: 같은 이름에 여행자보험 표를 다시 담아 앞 표를 덮어써요(실행판에서 고침)"), ("(df[c] == '?').sum()", "실행판: 그 열에 \"?\"가 몇 개인지 세요")],
 judge=dict(score=(4, 4, 5), line='"?"로 숨은 빈 값을 찾아낸 건 이번 발표회 최고의 발견 중 하나예요. 다만 손상 정도별 비율은 숫자만 말하고 "그래서 조사팀은 큰 파손 청구를 먼저 본다"는 업무 해석이 빠졌어요.'),
 quiz=[Q('info()가 "빈 값 91개"라고 보여 줬어요. 그런데 표에 "?"가 881개 있다면?', ['빈 값은 91개가 맞다', '"?"도 사실상 빈 값이라 따로 세고 처리해야 한다', '"?"는 정답을 뜻한다'], 1, 'NaN이 아닌 글자로 적힌 빈 값은 info()가 세지 않아요.', 'AI 판단 코너', 'AI 판단'),
       Q('같은 이름(insurance_claim)에 다른 표를 다시 담으면 어떻게 될까요?', ['두 표가 합쳐진다', '앞의 표는 사라지고 새 표만 남는다', '오류가 나서 멈춘다'], 1, '이름표는 하나의 표만 가리켜요. 다시 담으면 앞 표는 더 이상 쓸 수 없어요.', '초파리의 지적', '코드 읽기')]))
R.append(dict(
 id='rC', work='업무에서는: 고객에게 여러 상품의 성과를 보여 줄 때 첫날=100 차트를 쓰고, 흔들림(표준편차)을 꼭 함께 적어요.', code='C', name='주가 일기장 — 포트폴리오 시계열 읽기', folder=C, orig='Revolution3', fmt='데이터 시각화 조별 발표 (두 팀 대결)', team='both', presenters='초파리 팀 vs 주판봇 팀',
 lead='날짜마다 종가(그날 마지막 가격)를 적은 주가 일기장을 읽는 코드예요. 같은 데이터로 두 팀이 각자 차트를 그려 시각화 대결을 했어요.',
 key='출발점이 다른 숫자를 비교할 때는 "첫날 = 100"으로 맞춘 뒤 그린다.',
 scene=[T('doc', 'judge', '세 번째는 시각화 대결이에요. 같은 주가 일기장(2013~2019, 4종목)으로 각 팀이 차트 한 장을 냅니다. 투자 설명회에서 고객에게 보여 줄 차트라고 생각하세요.'),
        T('robo', 'chart', '주판봇 팀은 원래 가격을 그대로 그렸어요! 비트코인이 하늘로 솟았죠. 비트코인이 최고!'),
        T('moa', 'sweat', '그런데 조장님… 아마존·넷플릭스·도미노피자 선이 바닥에 딱 붙어서 하나도 안 보여요.'),
        T('fly', 'point', '초파리 팀은 네 종목 모두 첫날을 100으로 맞췄어. 그리고 눈금을 10 → 100 → 1000처럼 "몇 배씩"으로 늘려서 그렸지(로그 눈금).'),
        T('asst', 'report', f'그러면 아마존 {N["pf_x"]["AMZN"]:.1f}배, 넷플릭스 {N["pf_x"]["NFLX"]:.1f}배, 도미노피자 {N["pf_x"]["DPZ"]:.1f}배, 비트코인 {N["pf_x"]["BTC"]:.0f}배가 한 화면에 다 보여요.'),
        T('x2', 'think', f'대신 비트코인은 하루 평균 {N["pf_vol"]["BTC"]:.1f}%씩 출렁였어요. 아마존은 {N["pf_vol"]["AMZN"]:.1f}%. 많이 오른 만큼 많이 흔들렸어요.')],
 what=['미국 4종목(아마존·도미노피자·비트코인·넷플릭스) 일기장 1,520일 치를 읽어요.', '한·미 지표(다우존스·코스피·금·달러·비트코인·이더리움) 일기장 2,070일 치를 읽고 열 목록 확인 명령(info)으로 자료형을 봐요.', '실행판은 "처음 대비 몇 배", "하루 변동 크기(표준편차)", 첫날=100 차트를 더했어요.', '원본이 열지 않았던 세 번째 일기장(2012~2021, 구글 포함)도 열어 봐요.'],
 analogy='키 150cm 형과 100cm 동생 중 누가 더 많이 컸는지 보려면 키 그대로가 아니라 "작년 키 대비 몇 %"로 봐야 하는 것과 같아요.',
 data=[('미국 4종목 일기장', 'portfolio_data.csv', N['pf_shape'], '하루가 한 줄. 날짜와 네 종목의 종가', '빈 값 0'),
       ('한·미 국제 지표', 'international_portfolio_data.csv', N['it_shape'], '하루가 한 줄. 지수 종가와 하루 수익률(이름 끝 1), 코로나 시기 표시', f'코스피 빈 값 {N["it_kospi_na"]}줄 (주말·휴장일)'),
       ('새 포트폴리오', 'new_portfolio_data.csv', N['npf_shape'], '2012-01-03 ~ 2021-10-21, 아마존·도미노피자·구글·넷플릭스', '빈 값 0 (원본 코드는 읽지 않음)')],
 result=[f'기간: 2013-05-01 ~ 2019-05-14, {nf(N["pf_shape"][0])}일.',
         '처음 대비 마지막 값: ' + ', '.join(f'{k} {v:.1f}배' for k, v in N['pf_x'].items()) + '.',
         '하루 수익률의 표준편차(흔들림): ' + ', '.join(f'{k} {v:.2f}%' for k, v in N['pf_vol'].items()) + '.',
         f'국제 지표 표에서 코스피·금·달러가 숫자가 아닌 글자로 읽혔어요("2,326.17"처럼 쉼표가 들어 있음). 토·일요일은 코스피 값이 100% 비어 있어요.'],
 charts=['C_robo', 'C_fly'],
 trap=('AI 판단 코너 — "비트코인이 최고의 투자였습니다"', 'AI가 차트를 보고 이렇게 결론 내릴 수 있어요. 그러나 ① 이 기간(2013~2019)에만 해당하고, ② 하루 흔들림이 아마존의 약 5.5배였고, ③ 2017-12-18 최고점(약 18,972달러)에서 2018-12-14(약 3,235달러)까지 83% 떨어진 적도 있어요. 기간과 위험을 함께 묻지 않은 결론은 반쪽이에요. 이 페이지는 투자 권유가 아니에요.'),
 why=dict(problem='네 종목의 출발 가격이 30달러~250달러로 다 달라요. 그대로 그리면 큰 숫자 하나에 나머지가 묻혀요.', limit='원래 가격 차트는 "누가 비싼가"만 보여 주고 "누가 많이 올랐나"는 안 보여 줘요.', solve='모두 첫날을 100으로 맞추고(정규화), 몇 배씩 늘어나는 눈금(로그 눈금)을 쓰면 오른 비율을 공평하게 비교해요.', easy='출발선이 다른 달리기 선수들을 같은 출발선에 세우는 일이에요.'),
 math=dict(q='첫날을 100으로 맞춘다는 게 무슨 계산이에요? 숫자를 바꿔도 돼요?', school='중학교 비례식, 고등학교 로그함수 (log₁₀ 100 = 2, log₁₀ 1000 = 3)', fx='오늘의 지수 = 오늘 가격 ÷ 첫날 가격 × 100', parts=[('오늘 가격', '그날 종가 (예: 2019-05-14 아마존 1,840.1달러)'), ('첫날 가격', '2013-05-01 종가 (아마존 248.2달러)'), ('× 100', '첫날이 100이 되게 맞추기'), ('로그 눈금', '10→100→1000처럼 같은 간격이 "10배"를 뜻함')],
           try_=['아마존: 1,840.1 ÷ 248.2 × 100 = 741', '→ 첫날 100이 741이 됐어요 = 7.4배', '비트코인: 8,183.8 ÷ 106.2 × 100 = 7,700 → 77배'], comment='가격은 그대로 두고 "보는 기준"만 바꾸는 거군요. 그래서 모양은 같고 비교만 공평해져요!'),
 snip=[("portfolio_data = pd.read_csv('…/portfolio_data.csv')", "미국 4종목 일기장을 읽어요"), ("portfolio_data.info()", "1,520줄, 5열, 모두 비어 있지 않음"), ("pd.read_csv(…, index_col=0)", "파일 맨 앞 열(번호)을 줄 이름으로 써요"), ("prices / prices.iloc[0] * 100", "실행판: 모든 날을 첫날로 나눠 100을 곱해요 (첫날=100)"), ("str.replace(',', '')", "실행판: 쉼표를 지워 글자를 숫자로 바꿀 준비를 해요")],
 judge=dict(score=None, line='이번 대결은 초파리 팀 승이에요. 고객이 "누가 많이 올랐나"를 비교하려면 첫날=100 차트가 맞아요. 주판봇 팀도 "가장 비싼 건 무엇인가"를 묻는 자리라면 원래 가격 차트가 맞을 수 있어요. 차트는 질문이 정해요.'),
 duel=dict(fly=14, robo=11),
 quiz=[Q('출발 가격이 다른 네 종목의 상승률을 한 차트로 비교하려면?', ['원래 가격을 그대로 그린다', '모두 첫날을 100으로 맞춰 그린다', '가장 비싼 종목만 그린다'], 1, '같은 출발선(100)에 세우면 오른 비율을 공평하게 비교할 수 있어요.', '왜 이 방법을 쓰나 상자', '개념'),
       Q('어떤 종목이 첫날 50달러, 마지막 날 150달러였어요. 첫날=100 지수로 마지막 날 값은?', ['150', '300', '200'], 1, '150 ÷ 50 × 100 = 300. 3배가 됐어요.', '오늘 가격 ÷ 첫날 가격 × 100', '계산')]))
R.append(dict(
 id='rD', work='업무에서는: 데이터를 넘겨받으면 파일 이름 대신 열 이름·첫 3줄·줄 수를 확인하고 메모로 남겨요. 같은 실수를 팀 전체가 피해요.', code='D', name='대출 장부와 고객 명부 크기 재기', folder=Df, orig='Revolution4', fmt='상담 (모아 → 박사)', team='robo', presenters='모아 (주판봇 팀) 상담 신청',
 lead='미국 P2P 대출회사의 대출 장부(88만 건 × 74열)를 불러와 크기(몇 줄·몇 열)와 열 목록을 확인하는 코드예요. 모아가 실행하다 막혀 박사에게 상담을 신청했어요.',
 key='파일 이름을 믿지 말고 내용을 확인한다. 두 파일이 똑같을 수도, 첫 줄(열 이름)이 없을 수도 있다.',
 scene=[T('moa', 'sweat', '박사님, 상담 좀 해 주세요. 대출 장부를 열었더니 컴퓨터가 한참 멈췄어요. 그리고 이상한 게 있어요.'),
        T('doc', 'explain', '천천히 얘기해 봐요. 여기서 오래 걸리는 건 다들 겪는 일이에요. 파일이 441MB, 엑셀로 치면 88만 줄이라 몇십 초 걸리는 게 정상이에요.'),
        T('moa', 'think', '폴더에 bank_customers.csv랑 direct_marketimg.csv가 있는데요, 마케팅 파일을 열었더니 은행 고객 명부가 나와요. 그리고 열 이름이 "768805383", "Existing Customer"예요.'),
        T('doc', 'judge', f'좋은 발견이에요. 두 파일을 비교해 보면 내용이 완전히 똑같아요({N["r4_rows"]:,}줄). 그리고 첫 줄에 열 이름이 없어서, 판다스가 첫 고객의 값을 열 이름으로 착각한 거예요. "첫 줄도 데이터예요"라고 알려 주는 설정을 넣고, 열 이름을 따로 붙이면 돼요(코드는 접기 상자에).'),
        T('x3', 'shock', '파일 이름만 믿었으면 "마케팅 데이터"를 분석한다고 보고서를 쓸 뻔했네요!'),
        T('fly', 'magnify', '원본 노트북은 이 파일 대신 코드 A 저장소의 파일을 읽어서 문제가 안 보였던 거야. 폴더 안 파일도 한 번은 직접 열어 봐야 해.')],
 what=['대출 장부 loan.csv를 읽고 앞 5줄(head)을 봐요.', '크기 확인 명령(shape)으로 88만 줄 × 74열, 열 목록 확인 명령(info)으로 74개 열의 이름·빈 값·자료형을 봐요.', '은행 고객 명부와 다이렉트 마케팅 명부를 읽어 각각 크기를 재요.', '실행판은 대출 상태별 건수, 등급별 금리, 90% 넘게 빈 열, 두 파일이 같은지 확인을 더했어요.'],
 analogy='이사 온 집의 상자에 "부엌"이라고 적혀 있어도 열어 보니 책이 들어 있을 수 있어요. 이름표가 아니라 내용을 봐야 해요.',
 data=[('대출 장부', 'loan.csv (gzip 3조각)', LOAN['shape'], '대출 한 건이 한 줄. 금액·금리·등급·상태(정상 상환/연체/부실) 등 74열', f'90% 넘게 빈 열 {LOAN["null90"]}개 (공동 대출 관련 등)'),
       ('은행 고객 명부(복사본)', 'bank_customers.csv', (N['r4_rows'], 21), '코드 A의 은행 고객 명부와 같은 내용', '첫 줄(열 이름) 없음'),
       ('"다이렉트 마케팅"', 'direct_marketimg.csv', (N['r4_rows'], 21), '이름과 달리 은행 고객 명부와 완전히 같은 파일', '첫 줄(열 이름) 없음'),
       ('변수 설명', 'loan_data_description.csv', (N['desc_rows'], 3), '대출 장부 열 이름과 영어 뜻풀이', '—')],
 result=[f'대출 장부 {nf(LOAN["shape"][0])}건 × {LOAN["shape"][1]}열.',
         f'상태: 상환 중 {nf(LOAN["current"])}건, 다 갚음 {nf(LOAN["paid"])}건, 부실 처리(Charged Off) {nf(LOAN["charged"])}건({LOAN["charged"]/LOAN["shape"][0]*100:.1f}%).',
         f'등급별 평균 금리: A {LOAN["rate"]["A"]}% → G {LOAN["rate"]["G"]}% — 위험할수록 금리가 높아요.',
         f'두 파일이 똑같은가? {N["r4_same"]} (예). 그냥 읽으면 첫 고객이 열 이름이 되어 10,126줄로 하나 줄어요.'],
 charts=['D1'],
 trap=('AI 판단 코너 — "마케팅 데이터 분석 결과입니다"', '파일 이름이 direct_marketimg.csv라서 AI가 "다이렉트 마케팅 데이터 요약"이라고 제목을 붙일 수 있어요. 열 이름과 첫 줄을 보면 은행 고객 명부예요. AI에게 파일을 줄 때는 "열 이름과 첫 3줄을 먼저 보여 줘"라고 요청하세요.'),
 why=None, math=None,
 snip=[("loan = pd.read_csv('…/loan.csv')", "대출 장부(441MB)를 읽어요. 몇십 초 걸릴 수 있어요"), ("loan.shape", "(887379, 74)"), ("loan.info()", "74개 열의 이름, 비어 있지 않은 수, 자료형"), ("pd.read_csv(f, header=None)", "실행판: 첫 줄을 열 이름으로 쓰지 말라는 뜻"), ("a.equals(b)", "실행판: 두 표가 완전히 같은지 True/False로 알려 줘요")],
 judge=dict(score=(4, 4, 4), line='상담도 점수에 넣었어요. 모아가 "이상하다"는 느낌을 그냥 넘기지 않고 가져온 게 핵심이에요. 질문이 구체적이었고(파일 이름·열 이름), 덕분에 팀 전체가 같은 실수를 피했어요.'),
 quiz=[Q('CSV 파일을 읽었더니 열 이름이 "768805383", "Existing Customer"처럼 나왔어요. 가장 그럴듯한 원인은?', ['파일이 고장 났다', '첫 줄에 열 이름이 없어서 첫 데이터가 열 이름이 됐다', '판다스 버전이 낮다'], 1, 'header=None으로 읽고 열 이름을 따로 붙이면 돼요.', '상담 장면', '코드 읽기'),
       Q('이름이 다른 두 파일의 크기가 똑같이 1,244,210바이트예요. 먼저 할 일은?', ['둘 다 분석에 쓴다', '내용이 같은 파일인지 확인한다', '큰 파일을 지운다'], 1, '크기가 바이트까지 같으면 같은 파일일 가능성이 높아요. 열어서 확인하세요.', '파일 이름을 믿지 말 것', 'AI 판단')]))
R.append(dict(
 id='rE', work='업무에서는: 부도 예측 모델을 보고받으면 "정확도"보다 "부도 기업 220곳 중 몇 곳을 찾았나"를 먼저 물어요.', code='E', name='변수 사전 붙여 읽기와 기업 부도 데이터', folder=E, orig='Revolution5', fmt='개인 발표', team='fly', presenters='하루 (초파리 팀)',
 lead='대출 장부 74개 열 이름 옆에 뜻풀이 사전을 붙여 한 줄씩 출력하는 작은 함수를 만들고, 대만 기업 6,819곳의 재무 건강검진표(부도 데이터)를 여는 코드예요. 하루가 개인 발표를 했어요.',
 key='맞혀야 할 대상이 드물면(부도 3.2%) "다 정상"이라고 찍어도 정확도가 96.8%가 된다. 정확도만 보면 속는다.',
 scene=[T('doc', 'front', '다섯 번째는 하루의 개인 발표예요. 은행에서 "이 회사에 돈을 빌려줘도 될까?"를 판단하는 심사팀을 떠올려 보세요.'),
        T('asst', 'guide', '하루의 개인 발표 시작할게요! 대출 장부 열 이름이 영어 약어라 하나도 모르겠더라고요. 그래서 사전을 붙였어요.'),
        T('asst', 'report', f'사전에는 {N["desc_rows"]}개 설명이 있고, 74개 열 중 71개는 뜻을 찾았어요. 3개(verification_status, verification_status_joint, total_rev_hi_lim)는 사전에 없었어요.'),
        T('x1', 'wow', '기업 부도 데이터는 열이 96개나 되네요. 이걸로 부도를 맞히면 정확도가 엄청 높겠어요!'),
        T('asst', 'firm', f'그게 함정이에요. 부도 기업은 {N["bk_1"]}곳, {N["bk_pct"]:.1f}%뿐이에요. 아무 계산 없이 "전부 부도 아님"이라고 찍어도 96.8% 맞혀요.'),
        T('doc', 'think', '그래서 이런 데이터에서는 "부도 기업 220곳 중 몇 곳을 찾아냈나"를 따로 봐야 해요. 7회차(모델 평가)에서 배운 재현율이에요.'),
        T('fly', 'clip', '하나 더 있어. 열 이름 앞에 띄어쓰기가 숨어 있어서 "Debt ratio %"로 찾으면 못 찾아. 이름 앞뒤의 띄어쓰기를 지우는 정리부터 해야 해.')],
 what=['대출 장부와 변수 설명 사전(80줄)을 읽어요.', 'description(열 이름) 함수: 사전에서 그 열 이름을 찾아 뜻을 돌려줘요.', 'print_description(열 목록) 함수: 열마다 "이름 = 뜻"을 출력하고, 사전에 없으면 빨간색으로 이름만 출력해요.', '기업 부도 데이터(6,819곳 × 96열)를 읽고 크기를 봐요. 실행판은 부도 비율과 열 이름 공백 정리를 더했어요.'],
 analogy='외국 식당 메뉴판 옆에 번역 쪽지를 붙여 읽는 일이에요. 쪽지에 없는 메뉴 3개는 점원에게 물어봐야 하죠.',
 data=[('변수 설명 사전', 'loan_data_description.csv', (N['desc_rows'], 3), '열 이름(LoanStatNew)과 영어 설명(Description)', '설명 빈 값 3줄'),
       ('대출 장부', 'D 폴더의 loan.csv 조각', LOAN['shape'], '라운드 D와 같은 파일', '—'),
       ('기업 부도', 'company_bankruptcy.csv', N['bk_shape'], '기업 한 곳이 한 줄. 부도 여부(Bankrupt?)와 재무비율 95개(자산수익률·부채비율 등)', f'빈 값 0, 열 이름 앞 공백 {N["bk_space"]}개')],
 result=['사전으로 뜻을 찾은 열 71개, 사전에 없는 열 3개.',
         f'기업 부도: {nf(N["bk_shape"][0])}곳 중 부도 {N["bk_1"]}곳({N["bk_pct"]:.1f}%).',
         f'부채비율 평균: 부도 기업 {N["bk_debt"][1]:.3f}, 정상 기업 {N["bk_debt"][0]:.3f} — 부도 기업이 더 높아요(0~1로 바꾼 값).',
         '원본 코드는 termcolor라는 추가 도구로 색을 입혔어요. 실행판은 추가 설치 없이 돌아가게 print로 바꿨어요.'],
 charts=['E1'],
 trap=('AI 판단 코너 — "정확도 96.8%의 부도 예측 모델"', '누군가 "정확도 96.8%"를 자랑하면 "그 모델은 부도 기업을 몇 곳 찾았나요?"라고 물어보세요. 전부 "정상"이라고만 답하는 모델도 96.8%예요. 드문 사건을 맞히는 문제에서는 정확도 하나로 판단하면 안 돼요.'),
 why=dict(problem='부도를 맞히는 모델을 만들기 전에, "아무것도 안 하는 모델"이 몇 점인지 알아야 해요.', limit='정확도는 많은 쪽(정상 기업)을 맞히기만 해도 높게 나와요.', solve='먼저 비율을 보고 "기준 점수(다 정상이라고 찍기)"를 계산해 둬요. 모델은 이 점수보다 나아야 의미가 있어요.', easy='시험 문제 100개 중 97개 답이 ①번이면, 전부 ①을 찍어도 97점이에요.'),
 math=dict(q='96.8%는 어떻게 나온 숫자예요? 모델을 안 만들었는데요?', school='중학교 확률 — 전체 경우의 수 중 그 경우의 수', fx='기준 정확도 = 많은 쪽 개수 ÷ 전체 개수', parts=[('많은 쪽 개수', '정상 기업 수 (6,819 − 220 = 6,599)'), ('전체 개수', '기업 수 6,819')],
           try_=['6,599 ÷ 6,819 = 0.9677', '→ 96.8%', '→ 모델은 96.8%보다 높아야 하고, 부도 220곳 중 몇 곳을 찾는지도 따로 봐요'], comment='"아무것도 안 해도 받는 점수"를 먼저 아는 거군요. 이제 96%가 높아 보이지 않아요.'),
 snip=[("def description(column_name):", "열 이름 하나를 받아 뜻을 돌려주는 작은 함수를 만들어요"), ("loan_status.loc[loan_status.LoanStatNew == column_name].Description.values[0]", "사전 표에서 이름이 같은 줄을 찾아 설명을 꺼내요"), ("try: … except Exception:", "사전에 없어서 오류가 나면 멈추지 말고 다른 방법으로 출력해요"), ("bankruptcy.columns.str.strip()", "실행판: 열 이름 앞뒤 공백을 지워요")],
 judge=dict(score=(4, 5, 4), line='"아무것도 안 해도 96.8%"를 먼저 계산한 게 가장 쉬운 설명이었어요. 다만 사전에 없는 열 3개를 어떻게 처리할지(원자료 문서 확인)까지 말했으면 만점이에요.'),
 quiz=[Q('부도 기업이 3.2%인 데이터에서 "모두 정상"이라고만 답하는 모델의 정확도는?', ['3.2%', '50%', '96.8%'], 2, '정상 기업 6,599곳을 모두 맞혀요. 6,599 ÷ 6,819 = 96.8%.', '기준 정확도 공식', '계산'),
       Q('"Debt ratio %" 열을 찾았는데 없다고 나와요. 표를 열어 보니 열 이름이 " Debt ratio %"예요. 해결 방법은?', ['열 이름 앞뒤 공백을 지운다', '데이터를 다시 내려받는다', '그 열은 포기한다'], 0, 'str.strip()으로 열 이름 앞뒤 공백을 지우면 찾을 수 있어요.', '초파리의 지적', '코드 읽기')]))
R.append(dict(
 id='rF', work='업무에서는: 모델 성능이 너무 좋으면 축하하기 전에 정답이 새어 들어간 열이 없는지 점검해요. 추천 서비스는 비어 있는 98%를 어떻게 채울지가 핵심 과제예요.', code='F', name='문장·뉴스·평점 — 글자로 된 금융 데이터', folder=F, orig='Revolution6', fmt='조별 발표 + 반론', team='robo', presenters='주판봇 팀 (모아 · X3) 발표, 초파리 팀 (X2) 반론',
 lead='숫자가 아니라 글자(금융 문장·뉴스)와 별점으로 된 데이터 다섯 가지를 불러오는 코드예요. 주판봇 팀이 발표하고, 초파리 팀이 반론을 했어요.',
 key='"이 열 하나로 정답이 갈린다"면 분석이 잘된 게 아니라 정답이 새어 들어간 것(데이터 누수)일 수 있다.',
 scene=[T('doc', 'front', '마지막 라운드예요. 고객 민원 문자, 뉴스, 별점 리뷰처럼 글자로 된 데이터가 매일 쌓이는 회사라면 무엇부터 셀까요?'),
        T('moa', 'report', f'주판봇 팀 발표예요. 금융 문장 {nf(N["se_shape"][0])}개에 긍정·중립·부정 꼬리표가 붙어 있어요. 중립이 {N["se"]["neutral"]/N["se_shape"][0]*100:.0f}%로 가장 많아요.'),
        T('x3', 'joy', f'가짜 뉴스 {nf(N["fake"])}건, 진짜 뉴스 {nf(N["true"])}건이에요. 그리고 대발견! 뉴스 분류(subject)만 보면 가짜와 진짜를 100% 가를 수 있어요!'),
        T('robo', 'coin', '100%! 이걸로 가짜 뉴스 탐지기를 만들면 완벽하겠군!'),
        T('x2', 'think', '반론이에요. 가짜 뉴스는 News·politics·left-news 같은 분류만 쓰고, 진짜 뉴스는 politicsNews·worldnews만 써요. 두 쪽이 겹치는 분류가 0개예요.'),
        T('fly', 'arms', '데이터를 모은 곳이 달라서 꼬리표 이름이 다를 뿐이야. 새 뉴스에는 이런 꼬리표가 없어. 이건 탐지가 아니라 정답 엿보기야(데이터 누수).'),
        T('doc', 'judge', f'좋은 반론이에요. 그리고 평점 데이터도 봐요. 사용자 {N["ra_u"]}명 × 영화 {nf(N["ra_m"])}편 표에서 실제로 채워진 곳은 {N["ra_density"]:.2f}%뿐이에요. 추천 시스템은 비어 있는 98%를 채우는 일이에요.')],
 what=['금융 문장 감성 표(문장과 긍정/중립/부정)를 읽어요.', '가짜 뉴스·진짜 뉴스 표를 따로 읽고 크기와 분류(subject) 종류를 봐요.', '종목 이름 두 개가 같은 종목인지 표시한 학습용(train)·시험용(test) 표를 읽어요. 시험용은 정답 열이 비어 있어요.', '실행판은 영화 평점 10만 개와 넷플릭스 작품 목록도 열고, 중복 문장과 채워진 비율을 세요.'],
 analogy='고객센터에 온 손편지·문자·별점 리뷰를 상자째 받아 "몇 통이고 어떤 종류인지"부터 분류하는 일이에요.',
 data=[('금융 문장 감성', 'Financial_Sentiment_Analysis.csv', N['se_shape'], '문장 한 개가 한 줄. 꼬리표 positive/neutral/negative', f'빈 값 0, 같은 문장 중복 {N["se_dup"]}개'),
       ('가짜·진짜 뉴스', 'News_Fake_and_Real_*.csv.gz', (N['fake'] + N['true'], 4), f'제목·본문·분류·날짜. 가짜 {nf(N["fake"])} + 진짜 {nf(N["true"])}', '두 표의 분류 이름이 하나도 안 겹침'),
       ('종목 이름 유사도', 'text_similarity_train/test.csv', (N['sim_tr'], 5), f'종목 설명 두 개와 같은 종목인지(True/False). 시험용 {N["sim_te"]}줄', '시험용은 정답 열이 전부 비어 있음(맞힐 대상)'),
       ('영화 평점', 'ratings_small.csv', (N['ra_n'], 4), '평점 하나가 한 줄. 사용자·영화·점수(0.5~5)·시각', '빈 값 0'),
       ('넷플릭스 작품', 'netflix_list.csv.gz', N['nf_shape'], '작품 한 편이 한 줄. 제목·장르·평점·출연진 등', '등급 등 빈 값 많음')],
 result=[f'감성 꼬리표: 중립 {nf(N["se"]["neutral"])}, 긍정 {nf(N["se"]["positive"])}, 부정 {nf(N["se"]["negative"])}. 같은 문장 중복 {N["se_dup"]}개.',
         f'가짜 뉴스 분류 {len(N["fake_subj"])}종, 진짜 뉴스 분류 {len(N["true_subj"])}종 — 겹치는 분류 0개.',
         f'종목 유사도 학습용 {nf(N["sim_tr"])}쌍 중 같은 종목 {nf(N["sim_true"])}쌍.',
         f'평점: 사용자 {N["ra_u"]}명, 영화 {nf(N["ra_m"])}편, 평점 {nf(N["ra_n"])}개 → 채워진 비율 {N["ra_density"]:.2f}%.'],
 charts=['F1', 'F2'],
 trap=('AI 판단 코너 — "분류 열 하나로 정확도 100%"', 'AI나 자동 분석 도구가 "subject 열이 가장 중요한 단서"라고 알려 주면 반가워하기 전에 의심하세요. 정답과 함께 만들어진 꼬리표는 새 데이터에는 없어요. 정확도가 100%에 가까우면 먼저 누수를 찾아보세요.'),
 why=dict(problem='평점 10만 개 — 많아 보이지만 추천에 충분할까요?', limit='줄 수만 보면 데이터가 꽉 찬 것처럼 느껴져요.', solve='"사용자 × 영화" 전체 자리 수와 비교해 채워진 비율(밀도)을 봐요.', easy='극장 좌석 600만 석 중 10만 석만 찬 상태예요.'),
 math=dict(q='1.64%는 어떻게 나와요? 10만 개나 있는데 왜 이렇게 작아요?', school='초등 곱셈과 비율 — 직사각형의 넓이(가로 × 세로)', fx='채워진 비율 = 평점 수 ÷ (사용자 수 × 영화 수) × 100', parts=[('평점 수', '실제로 매긴 점수의 개수 (100,004)'), ('사용자 수 × 영화 수', '모든 사람이 모든 영화를 봤다면 생길 자리 수'), ('× 100', '퍼센트로 바꾸기')],
           try_=['671 × 9,066 = 6,083,286 자리', '100,004 ÷ 6,083,286 = 0.0164', '→ 1.64% — 98% 넘게 비어 있어요'], comment='줄 수가 아니라 "자리 대비 몇 %"를 봐야 하는군요. 추천이 어려운 이유를 알겠어요.'),
 snip=[("pd.read_csv(…, index_col=0)", "맨 앞 번호 열을 줄 이름으로 써요"), ("fake_df['subject'].unique()", "그 열에 나오는 값의 종류를 한 번씩만 보여 줘요"), ("pd.read_csv('…csv.gz')", "실행판: gzip으로 줄인 파일도 그대로 읽어요"), ("ratings['userId'].nunique()", "실행판: 서로 다른 사용자가 몇 명인지 세요")],
 judge=dict(score=(4, 4, 4), line='주판봇 팀 발표는 숫자가 정확했고 평점 데이터까지 꼼꼼했어요. 하지만 "100% 가를 수 있다"를 발견으로 소개한 건 아쉬워요. 초파리 팀 X2의 반론이 이 라운드의 핵심이었어요. 반론 점수 5점을 초파리 팀에 줍니다.'),
 bonus=dict(fly=5),
 quiz=[Q('가짜 뉴스와 진짜 뉴스의 분류(subject) 이름이 하나도 겹치지 않아요. 이 열로 정확도 100%가 나온다면?', ['완벽한 탐지기를 만든 것이다', '정답과 함께 만들어진 꼬리표라 새 뉴스에는 쓸 수 없다(데이터 누수)', '뉴스가 너무 적어서다'], 1, '모은 곳이 달라 생긴 꼬리표 차이일 뿐, 새 뉴스의 진위를 알려 주지 않아요.', 'X2의 반론', 'AI 판단'),
       Q('사용자 10명, 영화 20편, 평점 40개인 표의 채워진 비율은?', ['20%', '40%', '4%'], 0, '10 × 20 = 200자리 중 40개 → 40 ÷ 200 = 20%.', '평점 수 ÷ (사용자 × 영화)', '계산')]))

# 점수판 (심판: 박사, 기준 3개 × 5점)
SC = []
for r in R:
    j = r['judge']
    if r.get('duel'):
        SC.append((r, 'fly', r['duel']['fly'])); SC.append((r, 'robo', r['duel']['robo']))
    else:
        SC.append((r, r['team'], sum(j['score'])))
    for t, v in r.get('bonus', {}).items(): SC.append((r, t + '_bonus', v))
tot = {'fly': sum(v for r, t, v in SC if t.startswith('fly')), 'robo': sum(v for r, t, v in SC if t.startswith('robo'))}
cnt = {'fly': sum(1 for r, t, v in SC if t == 'fly'), 'robo': sum(1 for r, t, v in SC if t == 'robo')}
base = {'fly': sum(v for r, t, v in SC if t == 'fly'), 'robo': sum(v for r, t, v in SC if t == 'robo')}
avg = {k: base[k] / cnt[k] for k in cnt}
assert tot == {'fly': 45, 'robo': 48} and round(avg['fly'], 1) == 13.3 and avg['robo'] == 12.0, (tot, avg)

GL = {
 '행': G('행', '용어', '표의 가로줄 하나. 보통 고객 한 명·하루·거래 한 건.', 'row', 'lab:term/row', 0),
 '열': G('열', '용어', '표의 세로줄 하나. 나이·금액처럼 같은 종류의 값이 모인 항목.', 'column', 'lab:term/column', 0),
 '빈 값': G('빈 값', '용어', '값이 적혀 있지 않은 자리(결측값). NaN으로 표시되거나 "?", "Unknown" 같은 글자로 숨기도 함.', 'missing value', 'lab:concept/missing-value', 1),
 '결측값': G('결측값', '통계', '빈 값의 정식 이름.', 'missing value', 'lab:concept/missing-value-term', 1),
 'CSV': G('CSV', '약어', '쉼표로 값을 나눠 적은 글자 파일. 엑셀로도 열림.', 'comma-separated values', 'lab:term/csv', 0),
 '판다스': G('판다스', '도구', '파이썬에서 표를 다루는 도구(pandas).', 'pandas', 'lab:term/pandas', 0),
 'shape': G('shape', '함수', '표의 (줄 수, 열 수)를 알려 주는 명령.', 'shape', 'lab:term/shape', 0),
 'info()': G('info()', '함수', '열마다 비어 있지 않은 값의 수와 자료형을 보여 주는 명령.', 'info', 'lab:term/info', 1),
 '자료형': G('자료형', '용어', '값의 종류. 숫자(int·float)인지 글자(object·str)인지.', 'data type', 'lab:term/dtype', 2),
 '종가': G('종가', '금융', '그날 거래가 끝났을 때의 마지막 가격.', 'closing price', 'lab:term/closing-price', 2),
 '정규화': G('정규화', '통계', '출발점이나 단위가 다른 값을 같은 기준(예: 첫날=100)으로 맞추는 일.', 'normalization', 'lab:concept/normalization', 2),
 '로그 눈금': G('로그 눈금', '차트', '같은 간격이 "몇 배"를 뜻하는 눈금(10→100→1000).', 'log scale', 'lab:term/log-scale', 2),
 '표준편차': G('표준편차', '통계', '값들이 평균에서 평균적으로 떨어진 정도. 여기서는 하루 수익률이 흔들린 크기.', 'standard deviation', 'lab:concept/standard-deviation', 2),
 '수익률': G('수익률', '금융', '가격이 전날보다 몇 % 변했는지.', 'return', 'lab:concept/return', 2),
 '불균형': G('불균형', '통계', '맞힐 대상(부도 등)이 전체 중 아주 적은 상태.', 'class imbalance', 'lab:concept/class-imbalance', 4),
 '정확도': G('정확도', '평가', '전체 중 맞힌 비율. 불균형 데이터에서는 높게 나와도 속을 수 있음.', 'accuracy', 'lab:concept/accuracy', 4),
 '재현율': G('재현율', '평가', '실제 부도 기업 중 모델이 찾아낸 비율.', 'recall', 'lab:concept/recall', 4),
 '데이터 누수': G('데이터 누수', '용어', '정답과 함께 만들어진 정보가 입력에 섞여 성능이 부풀려지는 일.', 'data leakage', 'lab:concept/data-leakage', 5),
 '밀도': G('밀도', '용어', '전체 자리 중 값이 채워진 비율(희소할수록 낮음).', 'density', 'lab:concept/density', 5),
 '피싱': G('피싱', '금융', '진짜처럼 꾸민 가짜 사이트로 개인정보를 빼 가는 사기.', 'phishing', 'lab:term/phishing', 1),
 '허위 청구': G('허위 청구', '금융', '실제와 다르게 꾸며 보험금을 청구하는 일.', 'insurance fraud claim', 'lab:term/fraud-claim', 1),
 '노트북': G('노트북', '도구', '코드와 설명·실행 결과를 한 문서에 담는 파일(.ipynb). Colab에서 열 수 있음.', 'Jupyter notebook', 'lab:term/notebook', 0),
}
CORE = ['행', '열', '빈 값', '정규화', '로그 눈금', '불균형', '정확도', '데이터 누수', '밀도', 'info()', 'shape', '노트북']

def node_of(r, i):
    m = {'rA': ('lab:method/first-look', 'Method', '표 첫 확인(크기·빈 값)', 'first look at a table'), 'rB': ('lab:concept/hidden-missing', 'Concept', '숨은 빈 값', 'hidden missing values'),
         'rC': ('lab:concept/normalization', 'Concept', '정규화(첫날=100)', 'normalization to base 100'), 'rD': ('lab:method/file-check', 'Method', '파일 내용 확인', 'verifying file contents'),
         'rE': ('lab:concept/class-imbalance', 'Concept', '불균형과 기준 정확도', 'class imbalance and baseline accuracy'), 'rF': ('lab:concept/data-leakage', 'Concept', '데이터 누수와 밀도', 'data leakage and density')}[r['id']]
    return m + (r['key'],)

LIMS = {'rA': ('처음 몇 줄만 본다', '앞 몇 줄만 보면 뒤쪽의 이상한 값(118세, "Unknown")은 안 보여요. 그래서 다음 라운드에서는 빈 값과 숨은 빈 값을 셉니다.'),
        'rB': ('숫자 표 위주', '모든 열이 이미 숫자이거나 꼬리표라 시간 흐름이 없어요. 다음 라운드는 날짜가 있는 데이터예요.'),
        'rC': ('종가만 있다', '거래량·배당이 없어서 "실제 투자 수익"과는 달라요. 그리고 데이터가 작아요. 다음 라운드는 88만 줄짜리예요.'),
        'rD': ('열 뜻을 모른다', '74개 열 이름이 영어 약어라 뜻을 모르면 쓸 수 없어요. 다음 라운드에서 사전을 붙여요.'),
        'rE': ('숫자만 다룬다', '재무비율은 모두 숫자예요. 고객 문자·뉴스 같은 글자 데이터는 다음 라운드에서 봐요.'),
        'rF': ('불러오기까지만', '이 코드는 데이터를 여는 데서 끝나요. 감성 분류·누수 없는 가짜 뉴스 탐지·추천 모델은 다음 편(#02)에서 이어져요.')}
for i, r in enumerate(R):
    r['node'] = node_of(r, i); r['limit_short'], lim = LIMS[r['id']]
    r['explain'] = {'limit': lim, 'title': '풀이', 'steps': r['result']}
    r['sim_title'] = f'코드 {r["code"]} 실행 결과'; r['pair'] = {'short': r['analogy'][:30], 'left': r['analogy'], 'right': ''}
    r['short'] = f'코드 {r["code"]}'

P = dict(
 num='실전 #01', file=FILE, kind='hands_on', domain=['fintech'], family='fintech', finance=True,
 title='핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01', short_title='실제로 해보는 데이터 분석편 #01 — 핀테크 데이터 연구실',
 desc='fintech-data 실습 코드 6개(Revolution~Revolution6)에 어울리는 이름을 붙이고, 코드 설명·데이터 요약·실행 결과를 두 팀의 조별 발표·개인 발표·상담으로 풀어 본 연구실 해설.',
 eyebrow='핀테크 데이터 연구실 · 실제로 해보는 데이터 분석편 #01',
 question='공개 금융 데이터 코드 6개를 직접 돌리면, 화면에 나온 숫자는 무엇을 말하고 무엇을 숨길까?',
 question_en='What do the outputs of six public fintech data-loading notebooks tell us, and what do they hide?',
 intro='이번 편은 강의가 아니라 발표회예요. fintech-data의 실습 코드 6개를 이 저장소로 그대로 복사하고, Revolution 같은 번호 대신 하는 일에 맞는 이름을 붙였어요. 두 팀이 코드 하나씩 맡아 발표하고, 박사가 심판을 봅니다.',
 kpis=[('6개', '코드 (A~F)', 'i'), (f'{NFILES}개', '복사한 데이터 파일', 'g'), (f'{nf(LOAN["shape"][0])}', '가장 큰 표의 줄 수', 'a'), ('45 : 48', '최종 점수 (초파리 팀 : 주판봇 팀)', 'r')],
 three=dict(what='공개 금융 데이터를 불러오는 코드 6개를 실제로 돌려 보고, 코드가 하는 일·데이터 요약·실행 결과를 하나씩 읽어요.', why='데이터 분석의 8할은 "불러와서 확인하기"예요. 여기서 놓친 빈 값·가짜 파일 이름·누수는 나중에 모델 전체를 망가뜨려요.', work='새 데이터 파일을 받으면 ① 크기 ② 빈 값(숨은 것 포함) ③ 파일 내용 ④ 비율을 먼저 보고, AI가 낸 요약은 이 네 가지로 다시 확인해요.'),
 abbr=[('CSV', 'Comma-Separated Values · 쉼표로 나눈 글자 표 파일'), ('NaN', 'Not a Number · 판다스가 빈 값을 표시하는 기호'), ('P2P', 'Peer to Peer · 은행 없이 개인끼리 돈을 빌려주는 대출'), ('ROA', 'Return On Assets · 자산 대비 이익률'), ('Colab', 'Google Colaboratory · 설치 없이 브라우저에서 노트북을 돌리는 서비스')],
 levels=R, quiz={r['id']: r['quiz'] for r in R}, gloss=GL, core=CORE,
 duel=dict(question='같은 주가 일기장, 어느 차트가 고객에게 맞나?', fly_choice='첫날=100 + 로그 눈금 차트', robo_choice='원래 가격 차트', metric='심판 점수(15점 만점)', lv=2),
 next_q='불러온 데이터로 실제 모델(분류·회귀·추천)을 만들면 어떤 숫자가 나올까? (실제로 해보는 데이터 분석편 #02 예정)',
 sources=['fintech-data (GitHub) Revolution · Revolution2 · Revolution3 · Revolution4 · Revolution5 · Revolution6 — 각 저장소의 Loading_Data.ipynb와 README, data/ 폴더. 이 저장소 hands_on/01/ 폴더에 복사.',
          '실행 결과: hands_on/01/의 실행판 노트북 6개(A~F)를 2026-11-26에 실행한 출력. 계산 코드 src/hands_on/h01_build.py.',
          '원 데이터의 원 출처(Kaggle 공개 데이터 등)는 각 폴더의 README_original.md를 따름.'],
 examples=['팀 편성·발표 장면·심판 점수는 설명을 위한 가상 설정이에요. 데이터에서 나온 숫자는 모두 실제 계산값입니다.', '투자·대출·보험 관련 숫자는 교육용이며 투자·금융 권유가 아니에요.'],
 changes=['원본 저장소 이름 Revolution~Revolution6을 이 페이지에서는 코드 A~F와 하는 일에 맞는 이름으로 바꿉니다(원본 노트북은 original_Loading_Data.ipynb로 그대로 보관).',
          '원본 Revolution2 노트북이 여행자보험 표를 insurance_claim에 덮어쓰는 부분을 실행판에서는 travel_insurance로 바꿉니다.',
          'Git LFS로만 받을 수 있던 큰 파일(대출 장부·뉴스·넷플릭스·영화 정보)은 gzip으로 줄여 넣었고, 대출 장부는 세 조각으로 나눴습니다. 이어 붙이면 원본과 같아요.',
          '원본 Revolution5 노트북의 termcolor(추가 설치 필요)를 실행판에서는 print로 바꿉니다.'],
 refs=[{'id': 'fintechdata', 'type': 'dataset', 'title': 'fintech-data: Revolution~Revolution6 실습 데이터 저장소', 'author': [{'literal': 'fintech-data'}], 'issued': {'date-parts': [[2021]]}, 'URL': 'https://github.com/fintech-data',
        'lab': {'work': 'lab:work/fintechdata', 'role': 'primary', 'verified': {'title': True, 'authors': False, 'year': False, 'venue': False}, 'checkedBy': 'GitHub 저장소 README·노트북 (2026-11-26 복사)', 'note': '이 저장소 hands_on/01/ 폴더로 복사해 사용'}},
       {'id': 'ahn2026handson01', 'type': 'software', 'title': '실제로 해보는 데이터 분석편 #01 실행판 노트북 (코드 A~F)', 'author': [{'family': '안', 'given': '상선'}], 'issued': {'date-parts': [[2026]]}, 'URL': GH,
        'lab': {'work': 'lab:work/ahn2026handson01', 'role': 'data', 'verified': {'title': True, 'authors': True, 'year': True, 'venue': False}, 'checkedBy': '이 저장소', 'note': '원본 노트북에 설명과 확인 셀을 더해 실행한 판'}}],
 facts=[dict(id='F01', ko=f'은행 고객 10,127명 중 떠난 고객은 1,627명(16.1%)이다', work='fintechdata', loc='Revolution/data/Bank_customers_data.csv', anchor='#rA', lv=0),
        dict(id='F02', ko=f'보험 청구 1,000건 중 허위는 247건이고, "?"로 적힌 빈 값이 881개 있다', work='fintechdata', loc='Revolution2/data/insurance_claims.csv', anchor='#rB', lv=1),
        dict(id='F03', ko='2013-05-01~2019-05-14 첫날 대비 마지막 날 가격은 아마존 7.4배, 비트코인 77배다', work='fintechdata', loc='Revolution3/data/portfolio_data.csv', anchor='#rC', lv=2),
        dict(id='F04', ko='Revolution4의 bank_customers.csv와 direct_marketimg.csv는 내용이 같은 파일이며 열 이름 줄이 없다', work='fintechdata', loc='Revolution4/data/', anchor='#rD', lv=3),
        dict(id='F05', ko='기업 6,819곳 중 부도는 220곳(3.2%)이다', work='fintechdata', loc='Revolution5/data/company_bankruptcy.csv', anchor='#rE', lv=4),
        dict(id='F06', ko='가짜·진짜 뉴스의 분류(subject) 이름은 하나도 겹치지 않는다', work='fintechdata', loc='Revolution6/data/News_Fake_and_Real_*.csv', anchor='#rF', lv=5),
        dict(id='F07', ko='평점 데이터는 사용자 671명 × 영화 9,066편 중 1.64%만 채워져 있다', work='fintechdata', loc='Revolution6/data/ratings_small.csv', anchor='#rF', lv=5)],
)

# ───────────────────────── 4. HTML 조립 ─────────────────────────
EXTRA_CSS = '''
.say[data-who=sia] img.who,.say[data-who=sia]>div{border-color:var(--c-sia)}.say[data-who=sia] .name{color:var(--c-sia)}
.say[data-who=moa] img.who,.say[data-who=moa]>div{border-color:var(--c-moa)}.say[data-who=moa] .name{color:var(--c-moa)}
.say[data-who=x1] img.who,.say[data-who=x1]>div,.say[data-who=x2] img.who,.say[data-who=x2]>div,.say[data-who=x3] img.who,.say[data-who=x3]>div{border-color:var(--c-x)}
.say[data-who=x1] .name,.say[data-who=x2] .name,.say[data-who=x3] .name{color:var(--c-x)}
.say .role{font-size:12px;color:var(--muted);font-weight:400;margin-left:6px}
.teams{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.team{border:2px solid var(--rule);border-radius:14px;padding:18px;display:flex;flex-direction:column;gap:12px;background:#fff;min-width:0}
.team.fly{border-color:var(--c-fly)}.team.robo{border-color:var(--c-robo)}
.team h3{margin:0;font-size:19px}.team.fly h3{color:var(--c-fly)}.team.robo h3{color:var(--c-robo)}
.members{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.member{display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center;font-size:13px}
.member img{width:64px;height:64px;object-fit:contain;background:var(--panel2);border-radius:10px}
.member b{font-size:14px}.member .cap{font-size:11px;color:#fff;background:var(--c-fly);border-radius:99px;padding:1px 8px}.team.robo .member .cap{background:var(--c-robo)}
.judgebar{display:flex;gap:14px;align-items:center;border:2px dashed var(--c-doc);border-radius:14px;padding:14px 18px;background:rgba(122,69,214,.05)}
.judgebar img{width:72px;height:72px;object-fit:contain}
@media (max-width:760px){.teams{grid-template-columns:1fr}.members{grid-template-columns:repeat(4,minmax(0,1fr))}}
.fmt{display:inline-block;font-size:13px;font-weight:700;border-radius:99px;padding:3px 12px;color:#fff;background:var(--c-doc)}
.fmt.fly{background:var(--c-fly)}.fmt.robo{background:var(--c-robo)}.fmt.both{background:linear-gradient(90deg,var(--c-fly),var(--c-robo))}
.origname{font-size:14px;color:var(--muted)}.origname code{font-size:13px}
.trio{display:grid;grid-template-columns:1fr;gap:16px}
.box3{border:1px solid var(--rule);border-radius:12px;padding:20px;background:#fff;display:flex;flex-direction:column;gap:10px;min-width:0}
.box3>h3{margin:0;font-size:17px;display:flex;gap:8px;align-items:center}.box3>h3 i{font-style:normal;width:28px;height:28px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:#fff;font-size:14px;flex:none}
.box3.c1>h3 i{background:var(--seq)}.box3.c2>h3 i{background:var(--gfp)}.box3.c3>h3 i{background:var(--amber)}
.box3 ol,.box3 ul{margin:0;padding-left:20px;display:flex;flex-direction:column;gap:8px;line-height:1.8}
.box3 .ana{background:var(--panel2);border-radius:10px;padding:12px 14px;margin:0}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:14px}
svg.chart{width:100%;max-width:640px;margin:0 auto;display:block;height:auto;background:#fff;border:1px solid var(--rule);border-radius:10px}
svg.chart .ct{font-size:14px;font-weight:700;fill:#2b2f3a}svg.chart .cv{font-size:12px;font-weight:700;fill:#2b2f3a}svg.chart .cl{font-size:11.5px;fill:#5d6278}svg.chart .cn{font-size:12px;fill:#5d6278}
.trap{border:2px solid var(--amber);border-radius:12px;padding:16px 18px;background:rgba(217,130,43,.06)}
.trap h4{margin:0 0 6px;color:var(--amber);font-size:16px}
.judge{display:flex;gap:14px;align-items:flex-start;border-top:1px dashed var(--rule);padding-top:16px}
.judge .pts{display:flex;gap:6px;flex-wrap:wrap}.judge .pts span{font-size:13px;border:1px solid var(--rule);border-radius:8px;padding:3px 9px;background:#fff}
.judge .pts b{font-variant-numeric:tabular-nums}
.score{width:100%;border-collapse:collapse;font-size:15px;min-width:560px}.score th,.score td{border-bottom:1px solid var(--rule);padding:9px 10px;text-align:left}.score td.n{text-align:right;font-variant-numeric:tabular-nums}
.score tr.sum td{font-weight:700;border-top:2px solid var(--text)}
.vote{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.maptb td:first-child{white-space:nowrap}
.review30{border:1px solid rgba(63,95,168,.35);background:rgba(63,95,168,.05);border-radius:12px;padding:18px 20px}
.review30 h3{margin:0 0 8px;font-size:17px;color:var(--seq)}
.tabletoy{border-collapse:collapse;font-size:14px;margin:8px 0}.tabletoy td,.tabletoy th{border:1px solid #c9ced9;padding:5px 10px;text-align:center}.tabletoy th{background:var(--panel2)}.tabletoy .na{background:rgba(204,52,52,.12);color:var(--c-fly);font-weight:700}
.faq details{border:1px solid var(--rule);border-radius:10px;padding:12px 16px;background:#fff}.faq summary{cursor:pointer;font-weight:700}
.faq{display:flex;flex-direction:column;gap:10px}
.scene{margin:0}.scene img{width:100%;height:auto;border-radius:12px;image-rendering:pixelated;border:1px solid var(--rule)}
@media (max-width:860px){.dsum{overflow:visible}.dsum table.tb{min-width:0}.dsum tr:first-child{display:none}.dsum tr{display:block;border:1px solid var(--rule);border-radius:10px;padding:10px 12px;margin-bottom:10px;background:#fff}.dsum td{display:block;border:0;padding:3px 0;text-align:left!important}.dsum td::before{content:attr(data-l);display:block;font-size:12px;color:var(--muted)}}
.runbox{display:flex;gap:10px;flex-wrap:wrap}.runbox a{font-size:14px}
'''

SCENE_ALT = {'A': '초파리 팀이 펼친 장부 네 권에서 빈 곳을 찾는 장면', 'B': 'X1이 돋보기로 보험 서류 속 물음표 모양 빈 곳을 찾는 장면', 'C': '원래 가격 차트와 첫날=100 차트를 나란히 놓고 박사가 판정하는 장면',
             'D': '모아가 박사에게 똑같은 두 상자에 대해 상담하는 장면', 'E': '하루가 변수 사전과 100개 건물 중 빨간 3개를 보여 주는 장면', 'F': '리본 색으로만 구분되는 신문 두 더미를 두고 X2가 반론하는 장면', 'score': '두 팀이 트로피 두 개를 받는 공동 우승 장면'}
def scene_img(key, alt):
    import base64
    f = os.path.join(SRC, 'build', 'scenes', key + '.webp')
    if not os.path.exists(f): return ''
    from PIL import Image
    import io
    im = Image.open(f).convert('RGB'); small = im.resize((im.width // 4, im.height // 4), Image.NEAREST)
    # 4배 정수 격자 그림이므로 원래 격자(300×200)로 넣고 브라우저가 픽셀 그대로 키운다(무손실·용량 1/8)
    assert small.resize(im.size, Image.NEAREST).tobytes() == im.tobytes(), key + ': 4배 격자가 아님'
    buf = io.BytesIO(); small.save(buf, 'WEBP', lossless=True, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f'<figure class="scene"><img src="data:image/webp;base64,{b64}" width="1200" height="800" alt="{e(alt)}" loading="lazy" decoding="async"></figure>'

def say2(who, mood, text, M):
    s = B.say(who, mood, text, M)
    return s.replace(f'<b class="name">{B.NAMES[who]}</b>', f'<b class="name">{B.NAMES[who]}<span class="role">{ROLE.get(who, "")}</span></b>', 1)

def team_html(M):
    o = ['<div class="teams">']
    for k in ('fly', 'robo'):
        nm, mem = TEAM[k]
        cards = ''.join(f'<div class="member">{B.img(w, B.DEFM[w] if w not in ("x1","x2","x3") else "neutral", M, "")}<b style="color:var(--c-{w if w[0] != "x" else "x"})">{B.NAMES[w]}</b>{"<span class=cap>조장</span>" if i == 0 else ""}</div>' for i, w in enumerate(mem))
        motto = {'fly': '"그 숫자, 진짜야?" — 의심하고 확인하는 팀', 'robo': '"크고 높은 숫자가 좋아!" — 빠르고 과감한 팀'}[k]
        o.append(f'<div class="team {k}"><h3>{nm}</h3><p class="muted" style="margin:0">{motto}</p><div class="members">{cards}</div></div>')
    o.append('</div>')
    o.append(f'<div class="judgebar">{B.img("doc", "judge", M, "")}<div><b style="color:var(--c-doc)">심판 · 박사</b><p style="margin:4px 0 0">발표마다 세 가지로 점수를 매겨요(각 5점, 합 15점). ① <b>정확</b> 숫자가 맞나 ② <b>쉬움</b> 처음 배우는 사람이 알아듣나 ③ <b>함정 찾기</b> AI·코드 결과에서 이상한 점을 찾았나. 상담도 "좋은 질문"으로 점수를 받아요.</p></div></div>')
    return ''.join(o)

def map_html():
    rows = ''.join(f'<tr><td><b>코드 {r["code"]}</b></td><td>{r["name"]}</td><td><code>fintech-data/{r["orig"]}</code></td><td><a href="{GH}{r["folder"]}" target="_blank" rel="noopener">{r["folder"]}/</a></td><td>{r["fmt"]}</td></tr>' for r in R)
    return f'<div class="tw"><table class="tb maptb"><tr><th>새 이름</th><th>하는 일</th><th>원래 저장소</th><th>이 저장소 폴더</th><th>발표 형식</th></tr>{rows}</table></div>'

def round_html(r, i, M):
    o = [f'<section class="level" id="{r["id"]}"><div class="wrap stack">']
    fc = r['team'] if r['team'] in ('fly', 'robo') else 'both'
    o.append(f'<div class="lvhead"><div class="hexrow"><div class="hexno">{r["code"]}<small>라운드 {i+1}</small></div><h2>코드 {r["code"]} · {r["name"]}</h2></div>'
             f'<p class="sub"><span class="fmt {fc}">{e(r["fmt"])}</span> <span class="lvtag">발표: {e(r["presenters"])}</span></p>'
             f'<p class="origname">원래 이름: <code>fintech-data/{r["orig"]} · Loading_Data.ipynb</code> → 이 저장소 <code>hands_on/01/{r["folder"]}/</code></p><p class="lead">{r["lead"]}</p></div>')
    o.append(f'<div class="keyline"><span class="kl-tag">이 코드에서 가져갈 한 가지</span><p>{r["key"]}</p></div>')
    o.append(scene_img('h01_' + r['code'], SCENE_ALT[r['code']]))
    o.append('<div class="talk">' + ''.join(say2(w, m, t, M) for w, m, t in r['scene']) + '</div>')
    # 세 상자
    what = ''.join(f'<li>{x}</li>' for x in r['what'])
    drow = ''.join(f'<tr><td data-l="표"><b>{a}</b><br><code style="font-size:12px">{e(f)}</code></td><td class="n" data-l="줄 × 열">{nf(s[0])} × {s[1]}</td><td data-l="한 줄은 무엇?">{d}</td><td data-l="빈 값·주의">{na}</td></tr>' for a, f, s, d, na in r['data'])
    res = ''.join(f'<li>{x}</li>' for x in r['result'])
    charts = ''.join(CH[c] for c in r['charts'])
    o.append(f'''<div class="trio">
<div class="box3 c1"><h3><i>1</i>이 코드가 하는 일</h3><ol class="plainol">{what}</ol><p class="ana"><b>일상으로 치면</b> {r["analogy"]}</p></div>
<div class="box3 c2"><h3><i>2</i>데이터 요약</h3><div class="tw dsum"><table class="tb"><tr><th>표</th><th>줄 × 열</th><th>한 줄은 무엇?</th><th>빈 값·주의</th></tr>{drow}</table></div></div>
<div class="box3 c3"><h3><i>3</i>실행 결과 — 화면에 나온 숫자 읽기</h3><ul>{res}</ul><div class="charts">{charts}</div><p class="ana"><b>{r["work"].split(":")[0]}</b>{r["work"].split(":",1)[1]}</p></div>
</div>''')
    w, m = r.get('why'), r.get('math')
    if w or m:
        o.append('<div class="whymath">')
        if w: o.append(f'<div class="whybox"><h4>왜 이 방법을 쓰나</h4><div class="row"><b>문제 상황</b><p>{w["problem"]}</p></div><div class="row"><b>앞 방법의 한계</b><p>{w["limit"]}</p></div><div class="row"><b>해법</b><p>{w["solve"]}</p></div><p class="easy"><b>쉽게 말하면</b> {w["easy"]}</p></div>')
        if m:
            parts = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in m['parts']); tr_ = ''.join(f'<span>{x}</span>' for x in m['try_'])
            o.append(f'<details class="more mathmore"><summary>수식이 궁금하면 펼쳐 보기 — 수학 수식을 어려워하는 조수가 대신 물어봅니다</summary><div class="mathbox"><div class="who">{B.img("asst","shock",M)}<p>{m["q"]}</p></div><p class="school"><b>학교 수학으로 보면</b> {m["school"]}</p><div class="fx">{m["fx"]}</div><table>{parts}</table><div class="try"><b>숫자로 한 번 해 보기</b>{tr_}</div><div class="who">{B.img("asst","spark",M)}<p>{m["comment"]}</p></div></div></details>')
        o.append('</div>')
    t_h, t_p = r['trap']
    o.append(f'<div class="trap"><h4>🔍 {t_h}</h4><p style="margin:0">{t_p}</p></div>')
    o.append(f'<p class="limit"><b>이 코드의 한계</b> · {r["explain"]["limit"]}</p>')
    rows = ''.join(f'<tr><td><code>{e(c)}</code></td><td>{t}</td></tr>' for c, t in r['snip'])
    o.append(f'<details class="code"><summary>원본 파이썬 코드로 보면 (몰라도 됩니다)</summary><table>{rows}</table>'
             f'<p class="colab runbox">직접 돌려 보기 → <a href="{COLAB}{r["folder"]}/{r["folder"]}.ipynb" target="_blank" rel="noopener">실행판 노트북 Colab에서 열기</a> · <a href="{GH}{r["folder"]}/original_Loading_Data.ipynb" target="_blank" rel="noopener">원본 노트북 보기</a> · <a href="{GH}{r["folder"]}/data" target="_blank" rel="noopener">데이터 폴더</a></p></details>')
    j = r['judge']
    if j['score']:
        pts = f'<span>정확 <b>{j["score"][0]}</b></span><span>쉬움 <b>{j["score"][1]}</b></span><span>함정 찾기 <b>{j["score"][2]}</b></span><span>합 <b>{sum(j["score"])}</b>/15</span>'
    else:
        pts = f'<span style="border-color:var(--c-fly)">초파리 팀 <b>{r["duel"]["fly"]}</b>/15</span><span style="border-color:var(--c-robo)">주판봇 팀 <b>{r["duel"]["robo"]}</b>/15</span>'
    if r.get('bonus'): pts += ''.join(f'<span style="border-color:var(--c-fly)">반론 보너스 {TEAM[k][0]} <b>+{v}</b></span>' for k, v in r['bonus'].items())
    o.append(f'<div class="judge">{B.img("doc", "judge", M, "who")}<div><b style="color:var(--c-doc)">심판 박사의 판정</b><div class="pts">{pts}</div><p style="margin:6px 0 0">{j["line"]}</p></div></div>')
    o.append(f'<div class="quiz" data-quiz="{r["id"]}"></div>\n</div></section>')
    return '\n'.join(o)

def score_html(M):
    rows = []
    for r in R:
        j = r['judge']
        if r.get('duel'): f_, b_ = r['duel']['fly'], r['duel']['robo']
        elif r['team'] == 'fly': f_, b_ = sum(j['score']), '—'
        else: f_, b_ = '—', sum(j['score'])
        bon = r.get('bonus', {}).get('fly', '')
        rows.append(f'<tr><td>코드 {r["code"]} · {e(r["fmt"])}</td><td class="n">{f_}{f" (+{bon})" if bon else ""}</td><td class="n">{b_}</td></tr>')
    rows.append(f'<tr class="sum"><td>총점</td><td class="n" style="color:var(--c-fly)">{tot["fly"]}</td><td class="n" style="color:var(--c-robo)">{tot["robo"]}</td></tr>')
    rows.append(f'<tr><td>발표 횟수</td><td class="n">{cnt["fly"]}번</td><td class="n">{cnt["robo"]}번</td></tr>')
    rows.append(f'<tr class="sum"><td>발표 한 번당 평균 (보너스 빼고)</td><td class="n" style="color:var(--c-fly)">{avg["fly"]:.1f}</td><td class="n" style="color:var(--c-robo)">{avg["robo"]:.1f}</td></tr>')
    return f'''<section class="level" id="score"><div class="wrap stack">
<div class="lvhead"><h2>최종 판정 — 심판 박사의 점수판</h2><p class="lead">여섯 라운드가 끝났어요. 점수를 더해 볼까요? 그런데 이 점수판에도 함정이 하나 있어요.</p></div>
{scene_img('h01_score', SCENE_ALT['score'])}<div class="tw"><table class="score"><tr><th>라운드</th><th style="color:var(--c-fly)">초파리 팀</th><th style="color:var(--c-robo)">주판봇 팀</th></tr>{"".join(rows)}</table></div>
<div class="talk">
{say2("robo","happy",f"총점 {tot['robo']} 대 {tot['fly']}! 주판봇 팀 승리다!",M)}
{say2("fly","clip",f"잠깐. 너희는 {cnt['robo']}번 발표했고 우리는 {cnt['fly']}번이야. 한 번당 평균은 우리가 {avg['fly']:.1f}, 너희가 {avg['robo']:.1f}이야.",M)}
{say2("doc","judge","둘 다 맞는 말이에요. 합계로 보면 주판봇 팀, 평균으로 보면 초파리 팀이 이겨요. 어느 숫자를 볼지는 질문이 정해요. \"누가 더 많이 기여했나\"면 합계, \"누가 발표를 더 잘했나\"면 평균이에요.",M)}
{say2("doc","magic","그래서 오늘은 공동 우승으로 하겠습니다. 그리고 이 점수판 자체가 마지막 문제였어요. AI가 \"주판봇 팀 승\"이라고 요약하면, 여러분은 이제 \"무엇으로 나눈 숫자인가요?\"라고 물을 수 있죠.",M)}
</div>
<div class="panel"><h3>여러분이 심판이라면? (기록만 하고 저장하지 않아요)</h3><div class="vote"><button class="bt" type="button" data-v="합계">합계로 — 주판봇 팀</button><button class="bt" type="button" data-v="평균">평균으로 — 초파리 팀</button><button class="bt" type="button" data-v="공동">공동 우승</button></div><p class="muted" id="voteRes" aria-live="polite" style="text-align:center;margin:0"></p></div>
</div></section>'''

FAQ = [('코드를 하나도 몰라도 이 페이지를 볼 수 있나요?', '네. 각 라운드의 ① 하는 일 ② 데이터 요약 ③ 실행 결과만 읽어도 충분해요. 코드는 접어 두었어요. 직접 돌려 보고 싶을 때만 Colab 링크를 누르면 돼요.'),
       ('Colab에서 노트북을 열었는데 무엇을 눌러야 하나요?', '왼쪽 위 ▶(실행) 버튼을 맨 위 셀부터 차례로 누르거나, 메뉴 "런타임 → 모두 실행"을 누르세요. 데이터는 GitHub에서 자동으로 읽어요. 처음 실행하면 "이 노트북은 Google이 만든 것이 아닙니다"라는 경고가 나오는데 "무시하고 계속"을 누르면 돼요.'),
       ('왜 Revolution이라는 원래 이름을 바꿨나요?', '번호(Revolution2, 3…)만 보면 무슨 데이터인지 알 수 없어요. 폴더를 열지 않아도 내용을 알 수 있게 "하는 일" 이름(A~F)을 붙였어요. 원본 노트북은 각 폴더에 original_Loading_Data.ipynb로 그대로 있어요.'),
       ('대출 장부 파일이 왜 세 조각(part0~2)인가요?', 'GitHub는 파일 하나가 100MB를 넘으면 올릴 수 없어요. 441MB를 gzip으로 103MB까지 줄인 뒤 40MB씩 세 조각으로 나눴어요. 실행판 노트북의 load_loan() 함수가 자동으로 이어 붙여 읽어요.'),
       ('"빈 값"과 "결측값"은 다른 건가요?', '같은 말이에요. 결측값이 정식 용어고, 이 페이지에서는 쉽게 "빈 값"이라고 불렀어요. 판다스는 NaN이라고 표시해요.'),
       ('AI에게 데이터 분석을 시킬 때 오늘 배운 걸 어떻게 써요?', '네 가지를 물어보세요. ① 몇 줄·몇 열인가요? ② "?"나 "Unknown"처럼 글자로 숨은 빈 값은요? ③ 파일 이름과 실제 내용이 맞나요? ④ 그 비율은 무엇으로 나눈 건가요? 이 네 질문만으로 오늘 본 함정 대부분을 피할 수 있어요.')]

def page():
    M = B.Moods()
    for k, v in B.DEFM.items(): M.add(k, v)
    links = [('three', '3줄 요약'), ('cast', '두 팀'), ('map', '코드 이름표'), ('review', '30초 복습')] + [(r['id'], f'코드 {r["code"]}') for r in R] + [('score', '판정'), ('sum', '정리'), ('faq', '상담실'), ('kg', '색인'), ('export', '꾸러미')]
    h = B.head(P, P['title'], P['desc'], FILE)
    ogf = 'assets/og/cover_hands_on_01.jpg' if os.path.exists(os.path.join(ROOT, 'assets', 'og', 'cover_hands_on_01.jpg')) else 'assets/og_series.jpg'
    h = re.sub(r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{B.SITE}{ogf}">', h)
    h = h.replace('</style>', EXTRA_CSS + '\n</style>')
    h = h.replace('\uce78 대화', '단계 대화').replace('아홉 \uce78 같은 크기', '아홉 장 같은 크기')
    navh = '<nav class="top" aria-label="섹션 바로가기"><div class="wrap"><a class="logo" href="index.html"><i></i>핀테크 데이터 연구실 · 실전 #01</a><div class="links">' + ''.join(f'<a href="#{i}">{e(t)}</a>' for i, t in links) + '</div></div></nav>\n'
    cov = re.sub(r'alt="[^"]*"', 'alt="실제로 해보는 데이터 분석편 #01 표지: 초파리 팀(초파리 연구원·시아·하루·X2)과 주판봇 팀(주판봇·모아·X1·X3)이 발표회장 양쪽에 서고, 가운데 심판석에서 박사가 빨강·청록 판을 든 장면"', B.cover(P, M, 'cover_hands_on_01'), count=1)
    o = [h, navh, cov]
    kp = ''.join(f'<div class="kpi {c}"><b>{v}</b><span>{t}</span></div>' for v, t, c in P['kpis'])
    hero = [('doc', 'front', '오늘은 강의 대신 발표회예요. 코드 여섯 개를 두 팀이 나눠 발표하고, 저는 심판을 봅니다.'),
            ('fly', 'point', '초파리 팀은 숫자를 의심하는 팀. 시아, 하루, X2가 함께해.'),
            ('robo', 'coin', '주판봇 팀은 빠르고 과감하다! 모아, X1, X3, 가자!'),
            ('asst', 'smile', '처음 오신 분은 코드를 몰라도 괜찮아요. 화면에 나온 숫자를 함께 읽어요.')]
    o.append(f'<header class="hero" id="hero"><div class="wrap hero-grid"><div class="hero-text"><span class="eyebrow">{e(P["eyebrow"])}</span><h1>{P["title"]}</h1><p class="q">{P["question"]}</p><p>{P["intro"]}</p><section class="kpis k4">{kp}</section></div><div class="dialog">{"".join(say2(*t, M) for t in hero)}</div></div></header>')
    T3 = P['three']; ab = ''.join(f'<dt>{e(a)}</dt><dd>{b}</dd>' for a, b in P['abbr'])
    o.append(f'''<section class="level" id="three"><div class="wrap"><div class="three"><h2>처음 오신 분께 — 이 페이지를 3줄로</h2><ol><li><b>무엇을</b><span>{T3["what"]}</span></li><li><b>왜 중요한가</b><span>{T3["why"]}</span></li><li><b>업무에서는</b><span>{T3["work"]}</span></li></ol><div class="route"><p><b>처음이라면 이렇게 읽으세요.</b> 라운드마다 ① <b>가져갈 한 가지</b> → ② <b>장면 대화</b> → ③ <b>세 상자(하는 일·데이터 요약·실행 결과)</b>만 봐도 충분해요. 코드·수식은 접어 두었어요(몰라도 됩니다). 여기서 한 번에 다 이해하지 못해도 괜찮아요. 처음엔 다들 여러 번 봅니다.</p><button class="bt" type="button" id="openAll" aria-pressed="false">접어 둔 내용 모두 펼치기</button></div><details class='abbr'><summary>영어 약어 풀이</summary><dl>{ab}</dl></details></div></div></section>''')
    o.append(f'<section class="level" id="cast"><div class="wrap stack"><div class="lvhead"><h2>오늘의 두 팀과 심판</h2><p class="lead">인턴 시아·모아, 조수 하루, 그리고 처음 무대에 오른 X1·X2·X3가 두 팀으로 나뉘었어요. 초파리 연구원과 주판봇이 조장, 박사가 심판이에요.</p></div>{team_html(M)}<p class="muted">노란 점선 밑줄을 누르거나 손가락으로 대면 뜻이 나옵니다. 오른쪽 아래 도우미에서 밑줄을 핵심 → 전체 → 끄기로 바꿀 수 있어요.</p></div></section>')
    o.append(f'''<section class="level" id="map"><div class="wrap stack"><div class="lvhead"><h2>코드 이름표 — Revolution 대신 하는 일로 부르기</h2><p class="lead">원래 저장소 여섯 개는 이름이 Revolution, Revolution2 … Revolution6이라 열어 보기 전에는 무엇인지 알 수 없어요. 그대로 복사한 뒤, 코드가 하는 일에 맞춰 A~F 이름을 붙였어요.</p></div>{map_html()}
<div class="steps"><div><b>폴더마다 들어 있는 것</b><p>① <code>original_Loading_Data.ipynb</code> 원본 노트북(손대지 않음) ② <code>README_original.md</code> 원본 설명 ③ <code>data/</code> 데이터 ④ 설명과 확인 셀을 더해 실행까지 마친 <b>실행판 노트북</b></p></div><div><b>오늘 진행 방식</b><p>조별 발표 2번, 개인 발표 2번, 시각화 대결 1번, 상담 1번. 라운드가 끝날 때마다 박사가 점수를 매기고 확인 퀴즈 2문제가 나와요.</p></div><div><b>직접 돌려 보려면</b><p>각 라운드의 "원본 파이썬 코드로 보면" 상자에서 Colab 링크를 누르세요. 설치할 것이 없어요. <a href="{GH}" target="_blank" rel="noopener">hands_on/01 폴더 전체 보기</a></p></div></div></div></section>''')
    o.append(f'''<section class="level" id="review"><div class="wrap stack"><div class="lvhead"><h2>30초 복습 — 표 데이터를 읽는 네 단어</h2></div>
<div class="review30"><h3>엑셀 시트 하나를 떠올려 보세요</h3>
<table class="tabletoy"><tr><th></th><th>나이</th><th>흡연</th><th>의료비</th></tr><tr><th>1번 고객</th><td>19</td><td>yes</td><td>16,885</td></tr><tr><th>2번 고객</th><td>18</td><td>no</td><td>1,726</td></tr><tr><th>3번 고객</th><td class="na">?</td><td>no</td><td class="na">(비어 있음)</td></tr></table>
<ol style="margin:8px 0 0;padding-left:20px;line-height:1.9"><li><b>행</b>(가로줄): 고객 한 명. 이 표는 3행이에요.</li><li><b>열</b>(세로줄): 나이·흡연·의료비 같은 항목. 이 표는 3열이에요.</li><li><b>shape</b>: (행 수, 열 수) = (3, 3). 코드가 알려 주는 표의 크기예요.</li><li><b>빈 값</b>: 빨간 두 곳. "(비어 있음)"은 컴퓨터가 알아채지만 "?"는 글자라서 못 알아챌 수 있어요.</li></ol></div>
{say2("doc","explain","이 네 단어만 있으면 오늘 여섯 코드를 모두 따라올 수 있어요. 앞으로 시리즈에서 배운 회귀·분류·시각화도 전부 이 표에서 시작해요.",M)}
</div></section>''')
    for i, r in enumerate(R): o.append(round_html(r, i, M))
    o.append(score_html(M))
    srows = ''.join(f'<tr><td>코드 {r["code"]} · {r["name"]}</td><td>{r["key"]}</td><td>{r["limit_short"]}</td></tr>' for r in R)
    o.append(f'''<section class="level" id="sum"><div class="wrap stack"><div class="lvhead"><h2>정리 — 새 데이터를 받았을 때의 네 가지 확인</h2></div>
<div class="tw"><table class="tb"><tr><th>코드</th><th>가져갈 한 가지</th><th>남은 한계</th></tr>{srows}</table></div>
<div class="steps four"><div><b>① 크기</b><p>shape로 몇 줄·몇 열인지. 88만 줄이면 열리는 데 시간이 걸려요.</p></div><div><b>② 빈 값</b><p>NaN뿐 아니라 "?", "Unknown", 118세 같은 임시 숫자까지.</p></div><div><b>③ 내용</b><p>파일 이름이 아니라 열 이름과 첫 줄을 직접 확인.</p></div><div><b>④ 비율</b><p>개수 대신 비율, 그리고 "무엇으로 나눈 비율인가".</p></div></div>
<div class="explain"><h4>비유의 한계</h4><ul><li>반 명부 비유: 실제 데이터는 수만~수십만 줄이라 눈으로 다 볼 수 없어요. 그래서 코드로 세요.</li><li>출발선 비유(첫날=100): 같은 출발선에 세워도 "위험(흔들림)"은 따로 봐야 해요.</li><li>극장 좌석 비유(밀도): 추천에서는 빈 자리 대부분이 "안 봤다"일 뿐 "싫어한다"는 뜻이 아니에요.</li></ul></div>
{say2("doc","magic","코드 여섯 개는 모두 데이터를 \"불러오기만\" 했어요. 그런데도 함정이 여섯 개 나왔죠. 분석은 불러온 다음이 아니라 불러오는 순간부터 시작돼요.",M)}</div></section>''')
    faq = ''.join(f'<details><summary>{q}</summary><p style="margin:8px 0 0">{a}</p></details>' for q, a in FAQ)
    o.append(f'''<section class="level" id="faq"><div class="wrap stack"><div class="lvhead"><h2>박사의 상담실 — 처음 배우는 분들이 자주 묻는 것</h2></div>
{say2("moa","think","저도 라운드 D에서 상담받기 전엔 이런 게 궁금했어요. 모아서 박사님께 물어봤어요.",M)}<div class="faq">{faq}</div></div></section>''')
    outro = [('doc', 'cheer', '오늘 발표회는 여기까지예요. 두 팀 모두 수고했어요. 다음 편에서는 오늘 불러온 데이터로 실제 모델을 돌려 봐요.'),
             ('robo', 'sheep', '총점으로 이겼는데 공동 우승이라니… 그래도 평균이라는 걸 배웠다.'),
             ('fly', 'coffee', '다음엔 우리가 발표를 한 번 더 해야겠네. 물론 숫자는 다시 확인하고.'),
             ('sia', 'cheer', '처음 무대에 선 X1, X2, X3도 멋졌어요!'),
             ('x2', 'proud', '데이터 누수, 이제 절대 잊지 않을 거예요.'),
             ('asst', 'smile', '여러분도 실행판 노트북을 Colab에서 한 번 돌려 보세요. ▶만 누르면 돼요!')]
    o.append('<section class="level" id="outro"><div class="wrap stack"><div class="lvhead"><h2>아웃트로</h2></div>' + ''.join(say2(*t, M) for t in outro) + '</div></section>')
    o.append(B.KG_SEC.replace('<h3>\uc0ac\ub2e4\ub9ac 경로</h3>', '<h3>개념 흐름</h3>')); o.append(B.export_sec(M))
    o.append(B.footer(P).replace('<a href="index.html">목차</a>', '<a href="index.html">핀테크 데이터 연구실 목차</a>'))
    # 지식 그래프
    P['flow'] = []
    for l in R: P['flow'] += [[l['node'][2], 0], [l['limit_short'], 1]]
    G_ = B.kg_build(P)
    o.append(B.sprites(M))
    js = open(os.path.join(SRC, 'build', 'lab.js'), encoding='utf-8').read()
    js += '\nvar FD={};var SIMS={};function initDash(){}\n'
    js += "document.addEventListener('DOMContentLoaded',function(){});(function(){var r=document.getElementById('voteRes');document.querySelectorAll('.vote .bt').forEach(function(b){b.addEventListener('click',function(){document.querySelectorAll('.vote .bt').forEach(function(x){x.classList.remove('on')});b.classList.add('on');r.textContent='\"'+b.dataset.v+'\"을(를) 골랐어요. 박사의 답: 질문에 따라 둘 다 맞아요. 합계는 기여, 평균은 발표 실력을 보여 줘요.'})})})();\n"
    B.JS = js
    P['duels_js'] = []
    o.append(B.tail(P, G_))
    return ''.join(o)

if __name__ == '__main__':
    htm = page()
    htm = htm.replace('AI 판단 코너 1개', 'AI 판단 코너')
    bad = [w for w in ('\uc0ac\ub2e4\ub9ac', '\uad00\ud1b5', '\uc218\ud3ec\uc790', '\ud1b5\ud3ec\uc790', '\uc27d\uc8e0', '\ub2f9\uc5f0\ud788', '\uae30\ucd08\uc778\ub370') if w in re.sub(r'<script[^>]*>.*?</script>', '', htm, flags=re.S)]
    kan = re.findall('.{12}\uce78.{12}', re.sub(r'<script[^>]*>.*?</script>', '', htm, flags=re.S))
    assert not bad, bad
    assert not kan, kan[:5]
    out = os.path.join(OUTDIR, FILE)
    open(out, 'w', encoding='utf-8').write(htm)
    print(out, len(htm.encode()) // 1024, 'KB')
