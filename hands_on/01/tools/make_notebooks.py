#!/usr/bin/env python3
"""실제로 해보는 데이터 분석편 #01 — 코드 A~F 실행판 노트북 만들기.
원본(original_Loading_Data.ipynb)은 그대로 두고, 같은 일을 하는 '설명이 붙은 실행판'을 새로 만들어 실행 결과까지 저장한다.
사용: python3 tools/make_notebooks.py  (hands_on/01 폴더에서)
"""
import os, nbformat as nbf
from nbclient import NotebookClient
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_RAW = 'https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/hands_on/01/'

def loader(folder):
    return f'''import os, io, urllib.request
import pandas as pd
pd.set_option('display.max_columns', 12); pd.set_option('display.width', 120)

# 데이터 위치: 이 폴더의 data/ 에 있으면 그걸 쓰고, 없으면(Colab 등) GitHub에서 바로 읽습니다.
RAW = '{REPO_RAW}{folder}/data/'
def load(name, **kw):
    local = os.path.join('data', name)
    src = local if os.path.exists(local) else RAW + urllib.parse.quote(name)
    return pd.read_csv(src, low_memory=False, **kw)
print('준비 완료')'''

LOAN = '''# loan.csv(441MB)는 GitHub 한 파일 한도 때문에 gzip으로 줄인 뒤 세 조각(part0~2)으로 나눠 두었습니다.
# 조각을 이어 붙이면 원래 파일과 똑같습니다.
def load_loan(folder='{folder}', **kw):
    parts = []
    for i in range(3):
        local = os.path.join({base}, f'loan.csv.gz.part{{i}}')
        if os.path.exists(local):
            parts.append(open(local, 'rb').read())
        else:
            parts.append(urllib.request.urlopen('{raw}D_loan_ledger_check/data/' + f'loan.csv.gz.part{{i}}').read())
    return pd.read_csv(io.BytesIO(b''.join(parts)), compression='gzip', low_memory=False, **kw)'''

def md(s): return nbf.v4.new_markdown_cell(s)
def code(s): return nbf.v4.new_code_cell(s)

NB = {}
NB['A_customer_data_tour'] = ('코드 A · 고객 데이터 4종 둘러보기', 'Revolution', [
 md('## 이 코드가 하는 일\n은행 고객 명부, 쇼핑몰 마케팅 명부, 건강보험료 표, 여행자보험 판매 장부 — **표 네 권을 차례로 펼쳐서 첫 장만 훑어보는** 코드입니다.\n\n> 비유: 새 학기에 받은 반 명부 네 권을 책상에 펼쳐 놓고 "몇 명이지? 어떤 항목이 적혀 있지?"를 확인하는 일.\n\n원본 노트북은 `original_Loading_Data.ipynb`에 그대로 있습니다. 이 노트북은 같은 일을 하면서 결과를 한 줄씩 설명합니다.'),
 'LOADER',
 md('### ① 은행 고객 명부 (Bank_customers_data.csv)\n고객 한 명이 한 줄(행)입니다. `Attrition_Flag`는 고객이 떠났는지(Attrited) 남았는지(Existing)를 적은 열이에요.'),
 code("bank_customers = load('Bank_customers_data.csv')\nbank_customers.head()"),
 code("print('행(고객 수), 열(항목 수):', bank_customers.shape)\nbank_customers['Attrition_Flag'].value_counts()"),
 code("# 떠난 고객과 남은 고객의 1년 거래 횟수 평균\nbank_customers.groupby('Attrition_Flag')['Total_Trans_Ct'].mean().round(1)"),
 md('### ② 다이렉트 마케팅 명부 (DirectMarketing.csv)\n쇼핑몰 고객 1,000명. 마지막 열 `AmountSpent`(1년 이용액)를 맞히는 데 쓰는 데이터입니다.'),
 code("direct_marketing = load('DirectMarketing.csv')\ndirect_marketing.head()"),
 code("# 빈 값(결측값) 세기 — History 열에 빈 값이 많아요\ndirect_marketing.isna().sum()"),
 md('### ③ 건강보험료 표 (insurance.csv)'),
 code("insurance = load('insurance.csv')\nprint(insurance.shape)\ninsurance.groupby('smoker')['charges'].mean().round(0)"),
 md('### ④ 여행자보험 판매 장부 (travel insurance.csv)'),
 code("travel_insurance = load('travel insurance.csv')\nprint(travel_insurance.shape)\ntravel_insurance['Claim'].value_counts()"),
 code("# 이상한 값 찾기: 성별 빈 값 수, 가장 많은 나이, 음수 보험기간\nprint('Gender 빈 값:', travel_insurance['Gender'].isna().sum())\nprint('Age 최댓값:', travel_insurance['Age'].max(), '/ 118세 행 수:', (travel_insurance['Age'] >= 118).sum())\nprint('Duration이 음수인 행:', (travel_insurance['Duration'] < 0).sum())"),
 code("import matplotlib.pyplot as plt\nfig, ax = plt.subplots(1, 2, figsize=(9, 3.2))\nbank_customers['Attrition_Flag'].value_counts().plot.bar(ax=ax[0], color=['#5b8def', '#e8833a'], rot=0, title='Bank customers')\ninsurance.groupby('smoker')['charges'].mean().plot.bar(ax=ax[1], color=['#5b8def', '#e8833a'], rot=0, title='Mean insurance charge by smoker')\nplt.tight_layout(); plt.show()"),
])
NB['B_fraud_phishing_check'] = ('코드 B · 보험사기·피싱 탐지 데이터 점검', 'Revolution2', [
 md('## 이 코드가 하는 일\n가짜 웹사이트(피싱)와 허위 보험금 청구를 가려내는 데 쓸 **표 네 개를 불러오고 `info()`로 건강검진**을 합니다.\n\n> 비유: 은행 창구 직원이 "수상한 서류 묶음"을 받아 우선 장수와 빈 값부터 세어 보는 일.\n\n원본에서 여행자보험 표를 `insurance_claim`이라는 이름에 다시 담아 앞의 청구 표를 덮어쓰는 부분이 있어, 여기서는 `travel_insurance`로 이름을 바꿨습니다.'),
 'LOADER',
 code("website_phishing = load('Website Phishing.csv')\nprint(website_phishing.shape)\n# Result: 1 정상 / 0 의심 / -1 피싱\nwebsite_phishing['Result'].value_counts()"),
 code("website_phishing.info()"),
 code("insurance = load('insurance.csv')\ninsurance.info()"),
 code("insurance_claim = load('insurance_claims.csv')\nprint(insurance_claim.shape)\ninsurance_claim['fraud_reported'].value_counts()"),
 code("# 빈 값은 NaN 말고 '?'로도 숨어 있습니다\nprint('NaN 빈 값:', insurance_claim.isna().sum()[lambda s: s > 0].to_dict())\nprint(\"'?' 빈 값:\", {c: int((insurance_claim[c] == '?').sum()) for c in insurance_claim.columns if (insurance_claim[c] == '?').any()})"),
 code("# 사고 심각도별 허위 청구 비율\n(insurance_claim['fraud_reported'] == 'Y').groupby(insurance_claim['incident_severity']).mean().round(3)"),
 code("travel_insurance = load('travel insurance.csv')  # 원본은 이 표를 insurance_claim에 덮어썼어요\ntravel_insurance.shape"),
 code("import matplotlib.pyplot as plt\nr = (insurance_claim['fraud_reported'] == 'Y').groupby(insurance_claim['incident_severity']).mean()\nr.sort_values().plot.barh(color='#e8833a', title='Fraud rate by incident severity', figsize=(6, 2.8)); plt.tight_layout(); plt.show()"),
])
NB['C_portfolio_price_diary'] = ('코드 C · 주가 일기장 — 포트폴리오 시계열 읽기', 'Revolution3', [
 md('## 이 코드가 하는 일\n날짜별 종가(그날 마지막 가격)를 적은 **주가 일기장** 두 권(미국 4종목, 한·미 국제 지표)을 불러옵니다. 원본에 없던 세 번째 일기장(`new_portfolio_data.csv`)도 함께 열어 봅니다.\n\n> 비유: 매일 저녁 몸무게를 적은 다이어리. 한 줄이 하루입니다.'),
 'LOADER',
 code("portfolio_data = load('portfolio_data.csv')\nprint(portfolio_data.shape, portfolio_data['Date'].iloc[0], '→', portfolio_data['Date'].iloc[-1])\nportfolio_data.head()"),
 code("prices = portfolio_data.set_index(pd.to_datetime(portfolio_data['Date']))[['AMZN', 'DPZ', 'BTC', 'NFLX']]\nprint('처음 대비 마지막 값(배):'); print((prices.iloc[-1] / prices.iloc[0]).round(1))\nprint('하루 수익률의 표준편차(%) — 흔들림의 크기:'); print((prices.pct_change().std() * 100).round(2))"),
 code("import matplotlib.pyplot as plt\n(prices / prices.iloc[0] * 100).plot(logy=True, figsize=(8, 3.2), title='Start = 100 (log scale)'); plt.tight_layout(); plt.show()"),
 code("international_portfolio_data = load('international_portfolio_data.csv', index_col=0)\ninternational_portfolio_data.info()"),
 code("# 숫자여야 할 열이 글자(object)로 읽혔어요 — '2,326.17'처럼 쉼표가 들어 있기 때문\nip = international_portfolio_data.copy()\nfor c in ['kospi', 'gold', 'dol', 'VIX1']:\n    ip[c] = pd.to_numeric(ip[c].astype(str).str.replace(',', ''), errors='coerce')\nip[['kospi', 'gold', 'dol']].describe().round(1)"),
 code("# 빈 값이 많은 이유: 주말·휴장일에는 주식시장 값이 없고 코인 값만 있어요\nip['요일'] = pd.to_datetime(ip['real_date']).dt.day_name()\nip.groupby('요일')['kospi'].apply(lambda s: s.isna().mean()).round(2)"),
 code("new_portfolio_data = load('new_portfolio_data.csv')\nprint(new_portfolio_data.shape, new_portfolio_data['Date'].iloc[0], '→', new_portfolio_data['Date'].iloc[-1])"),
])
NB['D_loan_ledger_check'] = ('코드 D · 대출 장부와 고객 명부 크기 재기', 'Revolution4', [
 md('## 이 코드가 하는 일\n미국 P2P 대출회사의 **대출 장부(88만 건 × 74열)**를 불러와 크기(`shape`)와 열 목록(`info`)을 확인하고, 은행 고객 명부와 마케팅 명부도 크기를 잽니다.\n\n> 비유: 도서관 서고 전체를 처음 맡은 사서가 "책장 몇 개, 선반 몇 개"부터 세는 일.\n\n⚠️ 이 폴더의 `bank_customers.csv`와 `direct_marketimg.csv`는 **내용이 똑같은 파일**이고 첫 줄에 열 이름이 없습니다. 원본 노트북은 이 파일 대신 코드 A 저장소의 파일을 읽어서 문제가 드러나지 않았어요. 아래에서 직접 확인합니다.'),
 'LOADER', 'LOAN:"data"',
 code("loan = load_loan()\nloan.shape"),
 code("loan['loan_status'].value_counts()"),
 code("# 신용등급(A가 가장 좋음)별 평균 금리(%)\nloan.groupby('grade')['int_rate'].mean().round(2)"),
 code("# 90% 넘게 비어 있는 열\nnull_rate = loan.isna().mean()\nnull_rate[null_rate > 0.9].round(3).sort_values(ascending=False)"),
 code("A_file = '../A_customer_data_tour/data/Bank_customers_data.csv'\nbank_customers = pd.read_csv(A_file if os.path.exists(A_file) else RAW.replace('D_loan_ledger_check', 'A_customer_data_tour') + 'Bank_customers_data.csv')\nprint('코드 A의 은행 고객 명부:', bank_customers.shape)"),
 code("same = load('bank_customers.csv', header=None).equals(load('direct_marketimg.csv', header=None))\nprint('두 파일이 똑같은가?', same)\nb4 = load('bank_customers.csv')\nprint('그냥 읽으면 열 이름이 첫 고객 값이 됩니다:', list(b4.columns[:4]), b4.shape)\nb4 = load('bank_customers.csv', header=None, names=bank_customers.columns)\nprint('header=None으로 읽으면:', b4.shape)"),
 code("import matplotlib.pyplot as plt\nloan.groupby('grade')['int_rate'].mean().plot.bar(rot=0, color='#5b8def', title='Mean interest rate by grade (%)', figsize=(6, 3)); plt.tight_layout(); plt.show()"),
])
NB['E_dictionary_and_bankruptcy'] = ('코드 E · 변수 사전 붙여 읽기와 기업 부도 데이터', 'Revolution5', [
 md('## 이 코드가 하는 일\n① 대출 장부의 74개 열 이름 옆에 **뜻풀이 사전**(`loan_data_description.csv`)을 붙여 한 줄씩 출력하는 작은 함수를 만들고, ② 대만 기업 6,819곳의 재무비율 95개와 부도 여부를 담은 **기업 부도 데이터**를 엽니다.\n\n> 비유: 외국어 메뉴판 옆에 번역 쪽지를 붙여 읽는 일, 그리고 회사 건강검진표 6,819장 넘겨보기.'),
 'LOADER', 'LOAN:"../D_loan_ledger_check/data"',
 code("loan = load_loan(usecols=None)\nloan_status = load('loan_data_description.csv')\nprint(loan.shape, loan_status.shape)"),
 code("def description(column_name):\n    # 열 이름을 사전에서 찾아 뜻을 돌려줍니다\n    return loan_status.loc[loan_status.LoanStatNew == column_name].Description.values[0]\n\ndef print_description(column_list):\n    missing = []\n    for column in column_list:\n        try:\n            print(f'- {column} = {description(column)}')\n        except Exception:\n            missing.append(column)\n    print('\\n사전에 없는 열:', missing)\n\nprint_description(loan.columns[:10])"),
 code("print_description(loan.columns)"),
 code("bankruptcy = load('company_bankruptcy.csv')\nprint(bankruptcy.shape)\nbankruptcy['Bankrupt?'].value_counts()"),
 code("# 열 이름 앞에 빈 값(공백)이 숨어 있어요\nprint(repr(bankruptcy.columns[1]))\nbankruptcy.columns = bankruptcy.columns.str.strip()\nprint(repr(bankruptcy.columns[1]))"),
 code("# 부도 기업 비율\nprint(round(bankruptcy['Bankrupt?'].mean() * 100, 1), '%')\nbankruptcy.groupby('Bankrupt?')[['Debt ratio %', 'Net worth/Assets']].mean().round(3)"),
])
NB['F_text_and_ratings'] = ('코드 F · 문장·뉴스·평점 — 글자로 된 금융 데이터', 'Revolution6', [
 md('## 이 코드가 하는 일\n숫자가 아니라 **글자(문장·뉴스)와 평점**으로 된 데이터 다섯 가지를 불러옵니다: 금융 문장 감성, 가짜/진짜 뉴스, 종목 이름 유사도, 영화 평점, 넷플릭스 작품 목록.\n\n> 비유: 고객의 손편지·민원 문자·별점 리뷰를 상자째 받아 "몇 통이고 어떤 종류인지"부터 분류하는 일.\n\n큰 파일(뉴스·넷플릭스·영화 정보)은 `.csv.gz`로 줄여 두었고 pandas가 그대로 읽습니다.'),
 'LOADER',
 code("data = load('Financial_Sentiment_Analysis.csv', index_col=0)\nprint(data.shape)\ndata['Sentiment'].value_counts()"),
 code("print('완전히 같은 문장이 두 번 이상 나온 수:', data['Sentence'].duplicated().sum())\nprint('문장 평균 단어 수:', round(data['Sentence'].str.split().str.len().mean(), 1))"),
 code("fake_df = load('News_Fake_and_Real_Fake.csv.gz')\ntrue_df = load('News_Fake_and_Real_True.csv.gz')\nprint('가짜', fake_df.shape, '/ 진짜', true_df.shape)\nprint('가짜 뉴스 분류:', fake_df['subject'].unique())\nprint('진짜 뉴스 분류:', true_df['subject'].unique())"),
 code("train = load('text_similarity_train.csv', index_col=0)\ntest = load('text_similarity_test.csv', index_col=0)\nprint(train.shape, test.shape)\ntrain['same_security'].value_counts()"),
 code("ratings = load('ratings_small.csv')\nn_u, n_m = ratings['userId'].nunique(), ratings['movieId'].nunique()\nprint('사용자', n_u, '/ 영화', n_m, '/ 평점', len(ratings))\nprint('채워진 비율(%):', round(len(ratings) / (n_u * n_m) * 100, 2))"),
 code("netflix = load('netflix_list.csv.gz')\nprint(netflix.shape)\nnetflix['type'].value_counts().head()"),
 code("import matplotlib.pyplot as plt\nfig, ax = plt.subplots(1, 2, figsize=(9, 3))\ndata['Sentiment'].value_counts().plot.bar(ax=ax[0], rot=0, color='#5b8def', title='Sentiment labels')\nratings['rating'].value_counts().sort_index().plot.bar(ax=ax[1], rot=0, color='#e8833a', title='Movie ratings')\nplt.tight_layout(); plt.show()"),
])

def build(folder, run=True):
    title, orig, cells = NB[folder]
    nb = nbf.v4.new_notebook()
    head = md(f'# {title}\n**핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01**  \n원본: [fintech-data/{orig}](https://github.com/fintech-data/{orig}) `Loading_Data.ipynb` → 이 폴더의 `original_Loading_Data.ipynb`  \n해설 페이지: https://adminmrobo.github.io/fintech_data_analysis/hands_on_01.html\n\n> 코드를 몰라도 괜찮아요. 위에서부터 ▶ 실행 버튼만 차례로 누르면 됩니다.')
    out = [head]
    for c in cells:
        if c == 'LOADER': out.append(code(loader(folder)))
        elif isinstance(c, str) and c.startswith('LOAN:'):
            out.append(code(LOAN.format(folder=folder, base=c[5:], raw=REPO_RAW)))
        else: out.append(c)
    nb.cells = out
    nb.metadata['kernelspec'] = {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}
    if run:
        NotebookClient(nb, timeout=900, kernel_name='python3', resources={'metadata': {'path': os.path.join(H, folder)}}).execute()
    nbf.write(nb, os.path.join(H, folder, folder + '.ipynb'))
    print('ok', folder)

if __name__ == '__main__':
    import sys
    for f in (sys.argv[1:] or NB): build(f)
