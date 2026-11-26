"""실제로 해보는 데이터 분석편 #01 — 받기 상자(Colab 코드·풀버전·CSV)와 코드 구조 인포그래픽.
h01_build.py가 불러 쓴다. 픽셀 아이콘은 아래 격자 그림(글자 하나 = 픽셀 하나)으로 직접 그린다."""
import os, html, urllib.parse
import pandas as pd
e = html.escape
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(ROOT, 'hands_on', '01')
REPO = 'https://github.com/adminmrobo/fintech_data_analysis'
RAW = 'https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/hands_on/01/'
COLAB = 'https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/'
LOCAL = 'hands_on/01/'   # 페이지와 같은 사이트 안 상대 주소(받기 링크)

# ───────────── 픽셀 아이콘 (직접 그린 16비트풍 도트) ─────────────
PAL = {'K': '#2b2f3a', 'B': '#3f5fa8', 'L': '#9fb4e6', 'W': '#ffffff', 'Y': '#f2c744', 'R': '#cc3434', 'G': '#138a52', 'O': '#d9822b', 'C': '#bfe3f2', 'P': '#e9709a', 'N': '#8a6a3c', 'S': '#c9ced9', 'T': '#14899a'}
ICONS = {
 'tool': ['....KKKKKK....', '....K....K....', 'KKKKKKKKKKKKKK', 'KRRRRRRRRRRRRK', 'KRRRRRYYRRRRRK', 'KRRRRRYYRRRRRK', 'KKKKKKKKKKKKKK', 'KRRRRRRRRRRRRK', 'KRRRRRRRRRRRRK', 'KRRRRRRRRRRRRK', 'KKKKKKKKKKKKKK'],
 'get': ['.....BBBB.....', '.....BLLB.....', '.....BLLB.....', '..BBBBLLBBBB..', '...BLLLLLLB...', '....BLLLLB....', '.....BLLB.....', '......BB......', 'K............K', 'KSSSSSSSSSSSSK', 'KKKKKKKKKKKKKK'],
 'table': ['KKKKKKKKKKKKKK', 'KYYYYKYYYYKYYK', 'KKKKKKKKKKKKKK', 'KWWWWKWWWWKWWK', 'KKKKKKKKKKKKKK', 'KWWWWKWWWWKWWK', 'KKKKKKKKKKKKKK', 'KWWWWKRRRRKWWK', 'KKKKKKKKKKKKKK', 'KWWWWKWWWWKWWK', 'KKKKKKKKKKKKKK'],
 'look': ['...KKKKK......', '..KCCCCCK.....', '.KCWWCCCCK....', '.KCWCCCCCK....', '.KCCCCCCCK....', '.KCCCCCCCK....', '..KCCCCCK.....', '...KKKKKNN....', '.........NN...', '..........NN..', '...........NN.', '............N.'],
 'warn': ['......KK......', '.....KYYK.....', '.....KYYK.....', '....KYKKYK....', '....KYKKYK....', '...KYYKKYYK...', '...KYYKKYYK...', '..KYYYYYYYYK..', '..KYYYKKYYYK..', '.KYYYYYYYYYYK.', 'KKKKKKKKKKKKKK'],
 'fix': ['...........KK.', '..........KK..', '.........KK...', '........KK....', '.......KK.....', '....YYYYYY....', '...YYYYYYYY...', '..YYOYOYOYY...', '.YYOYOYOYY....', 'YYOYOYOYY.....'],
 'chart': ['K.............', 'K.........GG..', 'K.........GG..', 'K.....OO..GG..', 'K.....OO..GG..', 'K..BB.OO..GG..', 'K..BB.OO..GG..', 'K..BB.OO..GG..', 'KKKKKKKKKKKKKK'],
 'book': ['.KKKKKK.KKKKKK.', 'KWWWWWWKWWWWWWK', 'KWKKKKWKWKKKKWK', 'KWWWWWWKWWWWWWK', 'KWKKKWWKWKKKWWK', 'KWWWWWWKWWWWWWK', 'KWKKKKWKWYYYYWK', 'KWWWWWWKWWWWWWK', 'KKKKKKKKKKKKKKK'],
 'parts': ['KKKK.KKKK.KKKK', 'KBBK.KBBK.KBBK', 'KBBK.KBBK.KBBK', 'KKKK.KKKK.KKKK', '......KK......', '.....KKKK.....', 'KKKKKKKKKKKKKK', 'KBBBBBBBBBBBBK', 'KBBBBBBBBBBBBK', 'KKKKKKKKKKKKKK'],
 'mail': ['KKKKKKKKKKKKKK', 'KKWWWWWWWWWWKK', 'KWKWWWWWWWWKWK', 'KWWKWWWWWWKWWK', 'KWWWKKWWKKWWWK', 'KWWWWWKKWWWWWK', 'KWWWWWWWWWWWWK', 'KKKKKKKKKKKKKK'],
 'save': ['KKKKKKKKKKKKK.', 'KBWWWWWWWWBBK.', 'KBWWWWWWWWBBBK', 'KBWWWWWWWWBBBK', 'KBBBBBBBBBBBBK', 'KBBKKKKKKKBBBK', 'KBBKWWKKKKBBBK', 'KBBKWWKKKKBBBK', 'KKKKKKKKKKKKKK'],
 'colab': ['...OOOO..YYYY...', '..OO..OOYY..YY..', '.OO....YY....YY.', '.OO....YY....YY.', '..OO..OOYY..YY..', '...OOOO..YYYY...'],
 'zip': ['KKKKKKKKKKKK', 'KNNNNYNNNNNK', 'KNNNNKNNNNNK', 'KNNNNYNNNNNK', 'KNNNNKNNNNNK', 'KNNNNYNNNNNK', 'KNNNKKKNNNNK', 'KNNNKYKNNNNK', 'KNNNKKKNNNNK', 'KNNNNNNNNNNK', 'KKKKKKKKKKKK'],
}
def _rects(name):
    g = ICONS[name]; o = []
    for y, row in enumerate(g):
        x = 0
        while x < len(row):
            c = row[x]
            if c == '.': x += 1; continue
            x2 = x
            while x2 < len(row) and row[x2] == c: x2 += 1
            o.append(f'<rect x="{x}" y="{y}" width="{x2-x}" height="1" fill="{PAL[c]}"/>'); x = x2
    return ''.join(o)
def dims(name): g = ICONS[name]; return max(len(r) for r in g), len(g)
def symbols():
    """페이지에 한 번만 넣는 픽셀 아이콘 묶음 — 각 아이콘은 <use>로 다시 쓴다."""
    return ('<svg width="0" height="0" style="position:absolute" aria-hidden="true">' +
            ''.join(f'<symbol id="px-{n}" viewBox="0 0 {dims(n)[0]} {dims(n)[1]}" shape-rendering="crispEdges">{_rects(n)}</symbol>' for n in ICONS) + '</svg>')
def pix(name, size=44, title=''):
    w, h = dims(name)
    return f'<svg class="pix" viewBox="0 0 {w} {h}" width="{size}" height="{round(size*h/w)}" role="img" aria-label="{e(title or name)}"><use href="#px-{name}"/></svg>'

# ───────────── 코드별 파일 목록 ─────────────
# (data 폴더의 파일 이름, 변수 이름, read_csv 인자 문자열, 메모)
FILES = {
 'A_customer_data_tour': [('Bank_customers_data.csv', 'bank_customers', '', '은행 고객 명부'), ('DirectMarketing.csv', 'direct_marketing', '', '쇼핑몰 마케팅 명부'), ('insurance.csv', 'insurance', '', '건강보험료 표'), ('travel insurance.csv', 'travel_insurance', '', '여행자보험 판매 장부')],
 'B_fraud_phishing_check': [('Website Phishing.csv', 'website_phishing', '', '피싱 사이트'), ('insurance_claims.csv', 'insurance_claim', '', '자동차 보험 청구'), ('insurance.csv', 'insurance', '', '건강보험료 표'), ('travel insurance.csv', 'travel_insurance', '', '여행자보험 장부')],
 'C_portfolio_price_diary': [('portfolio_data.csv', 'portfolio_data', '', '미국 4종목 일기장'), ('international_portfolio_data.csv', 'international_portfolio_data', ', index_col=0', '한·미 국제 지표'), ('new_portfolio_data.csv', 'new_portfolio_data', '', '새 포트폴리오(2012~2021)')],
 'D_loan_ledger_check': [('loan.csv.gz.part0~2', 'loan', 'LOAN', '대출 장부 441MB (세 조각)'), ('loan_data_description.csv', 'loan_description', '', '대출 열 설명 사전'), ('bank_customers.csv', 'bank_customers_copy', ', header=None', '은행 고객 명부 복사본(열 이름 줄 없음)'), ('direct_marketimg.csv', 'direct_marketimg', ', header=None', '이름만 다른 같은 파일'), ('travel insurance.csv', 'travel_insurance', '', '여행자보험 (원본 폴더에 있던 파일)')],
 'E_dictionary_and_bankruptcy': [('loan_data_description.csv', 'loan_status', '', '대출 열 설명 사전'), ('company_bankruptcy.csv', 'bankruptcy', '', '기업 부도 데이터'), ('../D_loan_ledger_check/data/loan.csv.gz.part0~2', 'loan', 'LOAN', '대출 장부 (D 폴더의 세 조각)')],
 'F_text_and_ratings': [('Financial_Sentiment_Analysis.csv', 'sentiment', ', index_col=0', '금융 문장 감성'), ('News_Fake_and_Real_Fake.csv.gz', 'fake_df', '', '가짜 뉴스 (gzip)'), ('News_Fake_and_Real_True.csv.gz', 'true_df', '', '진짜 뉴스 (gzip)'), ('text_similarity_train.csv', 'train', ', index_col=0', '종목 이름 유사도 학습용'), ('text_similarity_test.csv', 'test', ', index_col=0', '종목 이름 유사도 시험용'), ('ratings_small.csv', 'ratings', '', '영화 평점'), ('netflix_list.csv.gz', 'netflix', '', '넷플릭스 작품 (gzip)'), ('movies_metadata.csv.gz', 'movies', '', '영화 정보 (gzip, 원본 노트북은 안 씀)')],
}
LOAN_FN = '''def load_loan():
    """대출 장부: gzip 세 조각을 받아 이어 붙여 읽어요 (약 1분, 메모리 2GB 안팎)"""
    parts = [urllib.request.urlopen(RAW + 'D_loan_ledger_check/data/loan.csv.gz.part%d' % i).read() for i in range(3)]
    return pd.read_csv(io.BytesIO(b''.join(parts)), compression='gzip', low_memory=False)
'''
def q(name): return urllib.parse.quote(name)
def fsize(path):
    if path.endswith('part0~2'):
        base = os.path.join(D, 'D_loan_ledger_check', 'data', 'loan.csv.gz.part')
        return sum(os.path.getsize(base + str(i)) for i in range(3))
    return os.path.getsize(path)
def human(n): return f'{n/1e6:.1f}MB' if n >= 1e6 else f'{n/1e3:.0f}KB'

_SHAPE = {}
def shape_of(folder, name, kw):
    key = (folder, name)
    if key in _SHAPE: return _SHAPE[key]
    if kw == 'LOAN': s = (887379, 74)
    else:
        args = {}
        if 'index_col=0' in kw: args['index_col'] = 0
        if 'header=None' in kw: args['header'] = None
        s = pd.read_csv(os.path.join(D, folder, 'data', name), low_memory=False, **args).shape
    _SHAPE[key] = s; return s

def data_cell(folder, with_imports=True, only=None):
    rows = [r for r in FILES[folder] if (only is None or r[1] in only)]
    loan = any(r[2] == 'LOAN' for r in rows)
    L = []
    if with_imports:
        L += ['import pandas as pd' + (', io, urllib.request' if loan else ''), f"RAW = '{RAW}'", '']
    if loan: L += [LOAN_FN]
    for name, var, kw, memo in rows:
        if kw == 'LOAN': L.append(f'{var} = load_loan()  # {memo}')
        else: L.append(f"{var} = pd.read_csv(RAW + '{folder}/data/{q(name)}'{kw})  # {memo}")
    L += ['', 'for name, df in [' + ', '.join(f"('{r[1]}', {r[1]})" for r in rows) + ']:', "    print(name, df.shape)"]
    return '\n'.join(L)

def full_cell(folder):
    return (f"# ① 풀버전 파이썬 파일 하나만 받아 실행 (데이터는 GitHub에서 자동으로 읽어요)\n"
            f"!wget -q -O {folder}.py {RAW}{folder}/{folder}.py\n%run {folder}.py\n\n"
            f"# ② 코드+데이터 폴더째 받기 (이 코드의 폴더만 골라서 받아요)\n"
            f"!git clone -q --depth 1 --filter=blob:none --sparse {REPO}.git\n%cd fintech_data_analysis\n!git sparse-checkout set hands_on/01/{folder}\n%cd hands_on/01/{folder}\n!ls data")

def csv_cell(folder):
    rows = FILES[folder]; L = ['from google.colab import files', '', '# 위의 "데이터를 Colab으로 받기"를 먼저 실행한 뒤 쓰세요']
    for name, var, kw, memo in rows:
        if kw == 'LOAN':
            L += [f"# {var}: 441MB라 통째로 받기보다 1만 줄 표본을 권해요", f"{var}.sample(10000, random_state=42).to_csv('loan_sample_10000.csv', index=False)", "files.download('loan_sample_10000.csv')"]
        else:
            out = os.path.basename(name).replace('.gz', '')
            idx = 'True' if 'index_col=0' in kw else 'False'
            hdr = ', header=False' if 'header=None' in kw else ''
            L += [f"{var}.to_csv('{out}', index={idx}{hdr})", f"files.download('{out}')"]
    return '\n'.join(L)

_cid = [0]
def codeblock(code, label):
    _cid[0] += 1; i = f'cb{_cid[0]}'
    return (f'<div class="cblk"><div class="cbar"><span>{e(label)}</span><button class="bt cpy" type="button" data-t="{i}">복사</button></div>'
            f'<pre><code id="{i}">{e(code)}</code></pre></div>')

def links_table(folder):
    rows = []
    for name, var, kw, memo in FILES[folder]:
        if kw == 'LOAN':
            parts = ' · '.join(f'<a href="{LOCAL}D_loan_ledger_check/data/loan.csv.gz.part{i}" download>조각{i}</a>' for i in range(3))
            rows.append(f'<tr><td data-l="파일"><b>{e(memo)}</b><br><code>loan.csv.gz.part0~2</code></td><td data-l="줄 × 열" class="n">887,379 × 74</td><td data-l="크기" class="n">{human(fsize("part0~2"))}</td><td data-l="받기">{parts}<br><span class="muted">세 조각을 이어 붙인 뒤 압축을 풀면 loan.csv</span></td></tr>')
            continue
        p = os.path.join(D, folder, 'data', name); s = shape_of(folder, name, kw)
        rows.append(f'<tr><td data-l="파일"><b>{e(memo)}</b><br><code>{e(name)}</code></td><td data-l="줄 × 열" class="n">{s[0]:,} × {s[1]}</td><td data-l="크기" class="n">{human(os.path.getsize(p))}</td>'
                    f'<td data-l="받기"><a href="{LOCAL}{folder}/data/{q(name)}" download>{"gzip 받기" if name.endswith(".gz") else "CSV 받기"}</a></td></tr>')
    return '<div class="tw dsum"><table class="tb"><tr><th>파일</th><th>줄 × 열</th><th>크기</th><th>받기</th></tr>' + ''.join(rows) + '</table></div>'

def get_box(r):
    f = r['folder']; c = r['code']
    btns = (f'<div class="getbtns"><a class="gbtn" href="{COLAB}{f}/{f}.ipynb" target="_blank" rel="noopener">{pix("colab", 30, "Colab")}<span>Colab에서 열기<small>실행판 노트북</small></span></a>'
            f'<a class="gbtn" href="{LOCAL}{f}/{f}.py" download>{pix("save", 26)}<span>풀버전 .py 받기<small>파이썬 파일 하나</small></span></a>'
            f'<a class="gbtn" href="{LOCAL}downloads/{f}_code.zip" download>{pix("zip", 24)}<span>코드 묶음 zip<small>노트북 2개 + .py + 원본 설명</small></span></a>'
            f'<a class="gbtn" href="{LOCAL}downloads/{f}_csv.zip" download>{pix("table", 26)}<span>CSV 묶음 zip<small>이 코드의 CSV 파일 모두</small></span></a></div>')
    return f'''<details class="getbox" id="get{c}"><summary>{pix("get", 22)} 코드 {c} 직접 받아 보기 — Colab으로 데이터 받기 · 풀버전 받기 · CSV로 받기</summary>
<p class="muted">모두 받을 필요는 없어요. 처음이라면 맨 위 <b>Colab에서 열기</b> 하나면 충분합니다. 아래 코드는 <b>복사</b> 버튼을 눌러 Colab 셀에 붙여 넣고 ▶ 실행하면 돼요.</p>
{btns}
<h4>① 데이터를 Colab으로 받기 — 표만 바로 불러오기</h4>
{codeblock(data_cell(f), f"코드 {c} · 데이터 받기 (Colab 셀 하나)")}
<h4>② 코드 풀버전 받기 — 설명·확인 셀까지 전부</h4>
{codeblock(full_cell(f), f"코드 {c} · 풀버전 받기 (둘 중 하나)")}
<h4>③ CSV 파일로 받기 — 내 컴퓨터에 저장</h4>
<p class="muted">가장 쉬운 방법은 아래 표의 <b>CSV 받기</b>를 누르는 거예요. Colab에서 고친 표를 저장하고 싶을 때는 아래 코드를 쓰세요.</p>
{links_table(f)}
{codeblock(csv_cell(f), f"코드 {c} · Colab에서 CSV로 저장해 내려받기")}
</details>'''

# ───────────── 코드 구조 인포그래픽 ─────────────
# (아이콘, 단계 이름, 코드 이름표, 결과, 원본|실행판)
STEPS = {
 'A': [('tool', '도구 꺼내기', 'import pandas as pd', '표 다루는 도구 준비', 'o'), ('get', '표 네 권 받기', 'pd.read_csv(…) × 4', '은행·마케팅·보험료·여행자보험', 'o'), ('table', '펼쳐 보기', 'df / df.shape', '(10127, 21) 등', 'o'),
       ('look', '빈 값 세기', 'df.isna().sum()', 'History 303 · Gender 45,107', 'p'), ('chart', '묶어서 평균', 'groupby().mean()', '흡연자 의료비 3.8배', 'p'), ('warn', '이상한 값 찾기', "df['Age'].max()", '118세 984명', 'p')],
 'B': [('tool', '도구 꺼내기', 'import pandas as pd', '표 다루는 도구 준비', 'o'), ('get', '표 네 개 받기', 'pd.read_csv(…) × 4', '피싱·청구·보험료·여행자보험', 'o'), ('table', '건강검진', 'df.info()', '열마다 비어 있지 않은 수', 'o'),
       ('warn', '숨은 빈 값', "(df[c] == '?').sum()", '"?" 881개', 'p'), ('fix', '이름표 고치기', 'travel_insurance = …', '앞 표 덮어쓰기 방지', 'p'), ('chart', '정도별 비율', 'groupby().mean()', '큰 파손 허위 60.5%', 'p')],
 'C': [('tool', '도구 꺼내기', 'import pandas as pd', '표 다루는 도구 준비', 'o'), ('get', '일기장 받기', 'pd.read_csv(…) × 2 (+1)', '미국 4종목·국제 지표·새 포트폴리오', 'o'), ('table', '건강검진', 'df.info()', '1,520일 × 5열', 'o'),
       ('chart', '첫날 = 100', 'prices / prices.iloc[0] * 100', '아마존 7.4배 · 비트코인 77배', 'p'), ('fix', '쉼표 지우기', "str.replace(',', '')", '글자 → 숫자', 'p'), ('look', '주말 빈 값', 'groupby(요일)', '토·일 코스피 100% 비어 있음', 'p')],
 'D': [('tool', '도구 꺼내기', 'import pandas as pd', '표 다루는 도구 준비', 'o'), ('parts', '세 조각 잇기', 'load_loan()', '441MB 대출 장부', 'p'), ('table', '크기 재기', 'loan.shape / info()', '(887379, 74)', 'o'),
       ('chart', '등급별 금리', "groupby('grade')", 'A 7.24% → G 25.63%', 'p'), ('look', '거의 빈 열', 'isna().mean() > 0.9', '17개 열', 'p'), ('warn', '똑같은 두 파일', 'a.equals(b) · header=None', '이름만 다른 같은 파일', 'p')],
 'E': [('tool', '도구 꺼내기', 'import pandas as pd', '표 다루는 도구 준비', 'o'), ('get', '장부와 사전 받기', 'pd.read_csv(…) × 2', '대출 장부 · 설명 80줄', 'o'), ('book', '뜻 붙이기 함수', 'def print_description()', '74열 중 71열 뜻 찾음', 'o'),
       ('get', '부도 데이터 받기', "pd.read_csv('company_bankruptcy.csv')", '6,819곳 × 96열', 'o'), ('fix', '이름 공백 지우기', 'columns.str.strip()', '95개 열 이름 정리', 'p'), ('chart', '부도 비율', "df['Bankrupt?'].mean()", '3.2% → 기준 정확도 96.8%', 'p')],
 'F': [('tool', '도구 꺼내기', 'import pandas as pd', '표 다루는 도구 준비', 'o'), ('mail', '글자 데이터 받기', 'pd.read_csv(…) × 5 (+2)', '감성·뉴스·유사도·평점·넷플릭스', 'o'), ('table', '꼬리표 세기', 'value_counts()', '중립 3,130 · 긍정 1,852 · 부정 860', 'p'),
       ('warn', '분류 이름 비교', "df['subject'].unique()", '겹치는 분류 0개 → 누수 위험', 'p'), ('look', '채워진 비율', 'nunique()', '671명 × 9,066편 중 1.64%', 'p'), ('chart', '그림 그리기', 'plot.bar()', '감성·평점 분포', 'p')],
}
GUIDE = {'A': ('sia', 'explain', '시아', '네 권을 받기 → 펼치기 → 세기 순서예요. 뒤의 세 단계는 실행판에서 더한 확인이에요.'),
         'B': ('x1', 'think', 'X1', '받자마자 건강검진(info)을 하고, 검진표가 놓친 "?"를 따로 셌어요.'),
         'C': ('fly', 'point', '초파리 연구원', '일기장은 날짜가 한 줄이야. 출발선을 맞춰야(첫날=100) 비교가 공평해.'),
         'D': ('moa', 'report', '모아', '조각 잇기 → 크기 재기 → 이상한 점 찾기. 저는 마지막 단계에서 상담을 받았어요.'),
         'E': ('asst', 'guide', '하루', '사전을 붙이는 작은 함수가 이 코드의 핵심이에요. 함수는 "반복할 일을 이름 붙여 묶은 것"이에요.'),
         'F': ('x3', 'joy', 'X3', '글자 데이터도 결국 표예요. 한 줄 = 문장 하나, 평점 하나.')}

def infographic(r, img):
    c = r['code']; who, mood, nm, line = GUIDE[c]
    files = ''.join(f'<span class="ig-chip in">{pix("table" if not n.endswith((".gz", "part0~2")) else ("parts" if "part" in n else "zip"), 16)}{e(os.path.basename(n))}</span>' for n, v, k, m in FILES[r['folder']] if not (c == 'D' and v == 'travel_insurance') and not (c == 'F' and v == 'movies'))
    dfs = ''.join(f'<span class="ig-chip out">{e(v)}</span>' for n, v, k, m in FILES[r['folder']] if not (c == 'D' and v == 'travel_insurance') and not (c == 'F' and v == 'movies'))
    steps = ''.join(f'<li class="{t}"><div class="ig-n">{i+1}</div>{pix(ic, 46, ti)}<b>{e(ti)}</b><code>{e(tok)}</code><span class="ig-out">→ {e(out)}</span><em>{"원본 코드" if t == "o" else "실행판에서 더함"}</em></li>' for i, (ic, ti, tok, out, t) in enumerate(STEPS[c]))
    return f'''<div class="infog" aria-label="코드 {c} 구조 인포그래픽">
<div class="ig-top"><h3>{pix("look", 26)} 코드 {c}의 구조 한눈에 보기</h3><div class="ig-guide">{img(who, mood)}<p><b>{nm}</b> {e(line)}</p></div></div>
<div class="ig-flow"><div><span class="ig-lab">들어가는 파일</span><div class="ig-chips">{files}</div></div><div class="ig-arrow" aria-hidden="true">{pix("get", 28)}</div><div><span class="ig-lab">만들어지는 표 이름(변수)</span><div class="ig-chips">{dfs}</div></div></div>
<ol class="ig-steps">{steps}</ol>
<p class="ig-legend"><span class="o">원본 코드</span> fintech-data 노트북에 있던 단계 · <span class="p">실행판에서 더함</span> 이 저장소의 실행판 노트북·.py에 더한 확인 단계 · 그림 속 코드 이름표는 몰라도 됩니다</p>
</div>'''

SKEL = [('tool', '도구 꺼내기', '판다스 불러오기'), ('get', '받기', '인터넷의 CSV를 표로'), ('table', '펼쳐 보기', '몇 줄·몇 열'), ('look', '확인하기', '빈 값·이상한 값'), ('fix', '고치기', '이름·글자·공백 정리'), ('chart', '요약·그림', '비율·평균·차트'), ('save', '저장하기', 'CSV로 내려받기')]
def skeleton(R):
    cells = ''.join(f'<li>{pix(ic, 52, t)}<b>{t}</b><span>{d}</span></li>' for ic, t, d in SKEL)
    kind = {'tool': 0, 'get': 1, 'mail': 1, 'parts': 1, 'table': 2, 'book': 2, 'look': 3, 'warn': 3, 'fix': 4, 'chart': 5}
    rows = ''
    for r in R:
        has = {kind[s[0]] for s in STEPS[r['code']]}
        rows += f'<tr><th><a href="#{r["id"]}">코드 {r["code"]}</a></th>' + ''.join(f'<td>{"●" if i in has else ("○" if i == 6 else "")}</td>' for i in range(7)) + '</tr>'
    return f'''<div class="infog skel"><h3>{pix("look", 26)} 여섯 코드의 공통 뼈대 — 데이터 분석의 첫 일곱 걸음</h3>
<ol class="sk-steps">{cells}</ol>
<div class="tw"><table class="tb sk-mx"><tr><th></th>{"".join(f"<th>{t}</th>" for _, t, _ in SKEL)}</tr>{rows}</table></div>
<p class="ig-legend">● 그 코드에 있는 단계 · ○ 이 페이지의 "CSV로 받기" 상자에서 직접 해 보는 단계. 코드마다 받는 데이터는 달라도 순서는 거의 같아요. 이 순서가 데이터 분석의 첫 걸음입니다.</p></div>'''

def all_data_cell(R):
    L = ['import pandas as pd, io, urllib.request', f"RAW = '{RAW}'", 'LOAD_LOAN = False   # 대출 장부(441MB)까지 받으려면 True로 바꾸세요 (약 1분)', '', LOAN_FN, 'data = {}']
    for r in R:
        f = r['folder']; L.append(f'# 코드 {r["code"]} · {r["name"]}')
        for name, var, kw, memo in FILES[f]:
            if kw == 'LOAN':
                if f == 'D_loan_ledger_check': L.append("if LOAD_LOAN: data['D.loan'] = load_loan()")
                continue
            L.append(f"data['{r['code']}.{var}'] = pd.read_csv(RAW + '{f}/data/{q(name)}'{kw})")
    L += ['', 'for k, df in data.items():', "    print(f'{k:35s} {df.shape}')"]
    return '\n'.join(L)

def all_full_cell(R):
    L = ['# 코드 A~F 전체(코드+데이터, 약 190MB)를 받아 풀버전 .py를 차례로 실행', f'!git clone -q --depth 1 --filter=blob:none --sparse {REPO}.git', '%cd fintech_data_analysis', '!git sparse-checkout set hands_on/01', '%cd hands_on/01', '!ls', '']
    for r in R: L += [f"%cd {r['folder']}", f"%run {r['folder']}.py", '%cd ..']
    return '\n'.join(L)

def all_csv_table(R):
    rows = []
    for r in R:
        for name, var, kw, memo in FILES[r['folder']]:
            if r['code'] == 'E' and kw == 'LOAN': continue
            if kw == 'LOAN':
                rows.append(f'<tr><td data-l="코드"><a href="#{r["id"]}">{r["code"]}</a></td><td data-l="파일"><b>{e(memo)}</b><br><code>loan.csv.gz.part0~2</code></td><td data-l="줄 × 열" class="n">887,379 × 74</td><td data-l="크기" class="n">{human(fsize("part0~2"))}</td><td data-l="받기">' + ' · '.join(f'<a href="{LOCAL}D_loan_ledger_check/data/loan.csv.gz.part{i}" download>조각{i}</a>' for i in range(3)) + '</td></tr>')
                continue
            s = shape_of(r['folder'], name, kw); p = os.path.join(D, r['folder'], 'data', name)
            rows.append(f'<tr><td data-l="코드"><a href="#{r["id"]}">{r["code"]}</a></td><td data-l="파일"><b>{e(memo)}</b><br><code>{e(name)}</code></td><td data-l="줄 × 열" class="n">{s[0]:,} × {s[1]}</td><td data-l="크기" class="n">{human(os.path.getsize(p))}</td><td data-l="받기"><a href="{LOCAL}{r["folder"]}/data/{q(name)}" download>{"gzip 받기" if name.endswith(".gz") else "CSV 받기"}</a></td></tr>')
    return '<div class="tw dsum"><table class="tb"><tr><th>코드</th><th>파일</th><th>줄 × 열</th><th>크기</th><th>받기</th></tr>' + ''.join(rows) + '</table></div>'

def get_section(R, img, say):
    zsize = lambda n: human(os.path.getsize(os.path.join(D, 'downloads', n)))
    btns = (f'<div class="getbtns"><a class="gbtn" href="{LOCAL}downloads/all_code.zip" download>{pix("zip", 24)}<span>코드 전체 zip<small>A~F 노트북·.py ({zsize("all_code.zip")})</small></span></a>'
            f'<a class="gbtn" href="{LOCAL}downloads/all_csv.zip" download>{pix("table", 26)}<span>CSV 전체 zip<small>보통 CSV 파일 모두 ({zsize("all_csv.zip")})</small></span></a>'
            f'<a class="gbtn" href="{REPO}/tree/main/hands_on/01" target="_blank" rel="noopener">{pix("get", 26)}<span>GitHub 폴더 보기<small>hands_on/01</small></span></a></div>')
    per = ''.join(f'<a class="gbtn sm" href="#get{r["code"]}" data-open="get{r["code"]}">{pix("get", 18)}<span>코드 {r["code"]}만 받기</span></a>' for r in R)
    return f'''<section class="level" id="get"><div class="wrap stack"><div class="lvhead"><h2>받아서 직접 해 보기 — 한꺼번에 받기</h2><p class="lead">여섯 코드를 처음에 한꺼번에 받을 수도 있고, 각 라운드의 "직접 받아 보기" 상자에서 하나씩 받을 수도 있어요. 처음이라면 Colab에서 코드 하나를 열어 ▶만 눌러 보는 것부터 시작하세요.</p></div>
{say}
{skeleton(R)}
<div class="panel"><h3>{pix("zip", 22)} 파일로 한꺼번에 받기</h3>{btns}<p class="muted" style="margin:10px 0 0">gzip으로 줄인 큰 파일(가짜·진짜 뉴스, 넷플릭스, 영화 정보)과 대출 장부 세 조각은 zip에 넣지 않았어요. 아래 표에서 따로 받거나 Colab 코드로 읽으세요.</p>
<p style="margin:12px 0 0"><b>장별로 받기</b></p><div class="getbtns">{per}</div></div>
<details class="getbox"><summary>{pix("colab", 26)} Colab으로 여섯 코드의 데이터를 한 번에 받기</summary>
<p class="muted">Colab 셀 하나에 붙여 넣고 ▶ 실행하면 여섯 코드의 표 23개가 <b>data</b>라는 상자에 담겨요(대출 장부는 기본으로 빼 두었어요). 예: <code>data['A.bank_customers']</code></p>
{codeblock(all_data_cell(R), "한꺼번에 · 데이터 받기 (Colab 셀 하나)")}</details>
<details class="getbox"><summary>{pix("save", 22)} 코드 풀버전을 한 번에 받아 차례로 실행하기</summary>
<p class="muted">여섯 코드의 실행판(.py)을 데이터와 함께 받아 A부터 F까지 차례로 돌려요. 대출 장부 때문에 몇 분 걸릴 수 있어요.</p>
{codeblock(all_full_cell(R), "한꺼번에 · 풀버전 받기와 실행 (Colab)")}</details>
<details class="getbox"><summary>{pix("table", 22)} CSV 파일 목록 — 하나씩 내려받기</summary>{all_csv_table(R)}</details>
</div></section>'''

CSS = '''
svg.pix{display:inline-block;flex:none;image-rendering:pixelated;vertical-align:middle}
.infog{border:2px solid #d5dbea;border-radius:14px;padding:18px;background:linear-gradient(#fff,#f8f9fc);display:flex;flex-direction:column;gap:14px}
.infog h3{margin:0;font-size:17px;display:flex;gap:8px;align-items:center}
.ig-top{display:flex;flex-wrap:wrap;gap:12px;justify-content:space-between;align-items:center}
.ig-guide{display:flex;gap:10px;align-items:center;max-width:560px}.ig-guide img{width:52px;height:52px;object-fit:contain;flex:none;background:var(--panel2);border-radius:10px}.ig-guide p{margin:0;font-size:14px;line-height:1.6;background:#fff;border:1px solid var(--rule);border-radius:10px;padding:8px 12px}
.ig-flow{display:grid;grid-template-columns:1fr auto 1fr;gap:12px;align-items:center}
.ig-arrow svg{transform:rotate(-90deg)}
.ig-lab{display:block;font-size:12px;color:var(--muted);margin-bottom:6px}
.ig-chips{display:flex;flex-wrap:wrap;gap:6px}
.ig-chip{display:inline-flex;gap:5px;align-items:center;font-size:12.5px;border-radius:8px;padding:4px 9px;font-family:ui-monospace,Menlo,Consolas,monospace;word-break:break-all}
.ig-chip.in{background:#fff;border:1px solid #c9ced9}.ig-chip.out{background:rgba(63,95,168,.1);border:1px solid rgba(63,95,168,.35);color:#2c4680}
.ig-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px 26px;counter-reset:s}
.ig-steps li{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:5px;border:1px solid #d5dbea;border-radius:12px;padding:14px 14px 12px;background:#fff;min-width:0}
.ig-steps li.p{border-style:dashed;border-color:#d9822b}
.ig-steps li:not(:last-child)::after{content:"→";position:absolute;right:-21px;top:38%;font-weight:700;color:#8a90a0;font-size:18px}
.ig-steps li:nth-child(3n)::after{content:"↓";right:auto;left:50%;top:auto;bottom:-24px}
.ig-steps li:last-child::after{content:none!important}
.ig-n{position:absolute;top:-10px;left:-8px;width:24px;height:24px;border-radius:50%;background:#2b2f3a;color:#fff;font-size:12px;font-weight:700;display:flex;align-items:center;justify-content:center}
.ig-steps b{font-size:15px}.ig-steps code{font-size:12px;background:var(--panel2);border-radius:6px;padding:2px 6px;word-break:break-all;max-width:100%}
.ig-out{font-size:13.5px;line-height:1.55}.ig-steps em{font-style:normal;font-size:11px;border-radius:99px;padding:1px 8px;margin-top:auto}
.ig-steps li.o em{background:rgba(63,95,168,.12);color:#2c4680}.ig-steps li.p em{background:rgba(217,130,43,.14);color:#9a5a17}
.ig-legend{margin:0;font-size:12.5px;color:var(--muted)}.ig-legend .o,.ig-legend .p{border-radius:99px;padding:1px 8px;font-size:11px}.ig-legend .o{background:rgba(63,95,168,.12);color:#2c4680}.ig-legend .p{background:rgba(217,130,43,.14);color:#9a5a17}
.sk-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:10px}
.sk-steps li{display:flex;flex-direction:column;align-items:center;text-align:center;gap:6px;border:1px solid #d5dbea;border-radius:12px;padding:12px 6px;background:#fff;position:relative}
.sk-steps li:not(:last-child)::after{content:"→";position:absolute;right:-10px;top:30%;color:#8a90a0;font-weight:700}
.sk-steps b{font-size:14px}.sk-steps span{font-size:12px;color:var(--muted);line-height:1.5}
.sk-mx td,.sk-mx th{text-align:center;font-size:13px;padding:6px}.sk-mx td{color:var(--seq);font-size:16px}
.getbox{border:1px solid var(--rule);border-radius:12px;padding:12px 16px;background:#fff}
.getbox>summary{cursor:pointer;font-weight:700;display:flex;gap:8px;align-items:center;list-style:none}.getbox>summary::-webkit-details-marker{display:none}
.getbox>summary::after{content:"펼치기 ▾";margin-left:auto;font-size:12px;color:var(--muted);font-weight:400}.getbox[open]>summary::after{content:"접기 ▴"}
.getbox[open]{display:flex;flex-direction:column;gap:10px}.getbox h4{margin:10px 0 0;font-size:15px}
.getbtns{display:flex;flex-wrap:wrap;gap:10px}
.gbtn{display:inline-flex;gap:10px;align-items:center;border:1px solid #c9ced9;border-radius:10px;padding:9px 14px;background:#fff;text-decoration:none;color:var(--text);min-height:44px}
.gbtn:hover{border-color:var(--seq);background:rgba(63,95,168,.05)}.gbtn span{display:flex;flex-direction:column;font-weight:700;font-size:14px}.gbtn small{font-weight:400;font-size:12px;color:var(--muted)}
.gbtn.sm{padding:6px 12px}
.cblk{border:1px solid #2b2f3a;border-radius:10px;overflow:hidden}
.cbar{display:flex;justify-content:space-between;align-items:center;gap:8px;background:#2b2f3a;color:#fff;font-size:12.5px;padding:6px 10px}
.cbar .bt{background:#fff;color:#2b2f3a;padding:4px 12px;min-height:30px;font-size:12.5px}
.cblk pre{margin:0;padding:12px 14px;background:#f6f7fb;overflow:auto;max-height:420px;font-size:12.5px;line-height:1.6}
@media (max-width:860px){.ig-steps{grid-template-columns:1fr;gap:22px}.ig-steps li::after{content:"↓"!important;right:auto!important;left:50%!important;top:auto!important;bottom:-22px!important}.ig-steps li:last-child::after{content:""!important}
.ig-flow{grid-template-columns:1fr}.ig-arrow svg{transform:none!important}.sk-steps{grid-template-columns:repeat(2,minmax(0,1fr))}.sk-steps li::after{display:none}}
'''
JS = r"""
(function(){function sel(el){var r=document.createRange();r.selectNodeContents(el);var s=window.getSelection();s.removeAllRanges();s.addRange(r)}
document.querySelectorAll('.cpy').forEach(function(b){b.addEventListener('click',function(){var el=document.getElementById(b.dataset.t);var t=el.innerText;var done=function(){b.textContent='복사됨 ✓';setTimeout(function(){b.textContent='복사'},1600)};
try{navigator.clipboard.writeText(t).then(done,function(){sel(el);b.textContent='선택됨 — Ctrl+C'})}catch(x){sel(el);b.textContent='선택됨 — Ctrl+C'}})});
document.querySelectorAll('[data-open]').forEach(function(a){a.addEventListener('click',function(){var d=document.getElementById(a.dataset.open);if(d)d.open=true})});
if(location.hash&&/^#get[A-F]$/.test(location.hash)){var d=document.querySelector(location.hash);if(d)d.open=true}})();
"""
