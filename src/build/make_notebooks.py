#!/usr/bin/env python3
"""회차별 Colab 실습 노트북(notebooks/NN_*.ipynb)을 만들고 실제로 실행해 결과까지 저장한다.
페이지의 실험·대결 숫자와 같은 값이 나오도록 compute.py 와 같은 분할(random_state=42)을 쓴다.
사용: cd src && python3 build/make_notebooks.py"""
import os, sys, nbformat
from nbformat.v4 import new_notebook, new_markdown_cell as M, new_code_cell as C

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'notebooks'); os.makedirs(OUT, exist_ok=True)
REPO = 'adminmrobo/fintech_data_analysis'
SITE = 'https://adminmrobo.github.io/fintech_data_analysis/'

SETUP = '''# 준비: 라이브러리와 데이터 불러오기 (Colab에서는 그대로 실행하면 됩니다)
import os, urllib.parse, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 30)

BASE = 'https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/data/'
def load(path, **kw):
    """저장소의 data/ 폴더에서 CSV를 읽는다. 내 컴퓨터에 저장소가 있으면 그 파일을, 없으면 GitHub에서 읽는다."""
    for root in ('data', '../data'):
        f = os.path.join(root, path)
        if os.path.exists(f):
            return pd.read_csv(f, **kw)
    return pd.read_csv(BASE + urllib.parse.quote(path), **kw)

RS = 42   # 해설 페이지와 같은 숫자가 나오도록 무작위 시드를 고정'''

BANK = '''b = load('Revolution/Bank_customers_data.csv')
b['y'] = (b.Attrition_Flag == 'Attrited Customer').astype(int)   # 1 = 이탈 고객
print(b.shape, '이탈 비율:', round(b.y.mean(), 3))'''

# (번호, 파일, 제목, 셀 목록)
NB = []

NB.append(('01', '01_fintech_industry', '핀테크 산업의 이해와 핀테크 데이터', [
 M('## 1. 은행 고객 데이터 한눈에 보기\n신용카드 고객 10,127명의 정보입니다. 한 줄이 고객 한 명, 한 열이 정보 하나예요.'),
 C(BANK + '\nb.head()'),
 M('## 2. 열마다 이탈 비율이 어떻게 다른가\n숫자 열은 5개 구간으로 나눠 구간별 이탈 비율을, 글자 열은 값별 이탈 비율을 봅니다.'),
 C('''for c in ['Gender', 'Income_Category', 'Total_Trans_Ct']:
    s = b[c]
    if not pd.api.types.is_numeric_dtype(s):
        print(b.groupby(c).y.mean().round(3), '\\n')
    else:
        print(b.groupby(pd.qcut(s, 5)).y.mean().round(3), '\\n')'''),
 M('## 3. 대결 재현: 행동 1열 vs 인구통계 16열\n거래 횟수 한 열만 쓴 로지스틱 회귀와, 나이·성별·학력·소득·결혼(더미 16열)을 쓴 로지스틱 회귀를 AUC로 비교합니다.'),
 C('''from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, recall_score

def lr_eval(X, y):
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.25, random_state=RS, stratify=y)
    sc = StandardScaler().fit(Xtr)
    m = LogisticRegression(max_iter=2000, class_weight='balanced').fit(sc.transform(Xtr), ytr)
    p = m.predict_proba(sc.transform(Xte))[:, 1]
    return round(roc_auc_score(yte, p), 3), round(recall_score(yte, p >= .5), 3)

demo = pd.get_dummies(b[['Customer_Age', 'Gender', 'Education_Level', 'Income_Category', 'Marital_Status']], drop_first=True).astype(float)
print('인구통계', demo.shape[1], '열  (AUC, 재현율):', lr_eval(demo, b.y))
print('거래 횟수 1열     (AUC, 재현율):', lr_eval(b[['Total_Trans_Ct']], b.y))'''),
 M('**AI 판단 연습** — 누군가 "열이 많을수록 예측이 좋다"고 하면, 위 결과로 어떻게 반박할 수 있을까요? 열의 개수와 열의 정보량은 다릅니다.'),
]))

NB.append(('02', '02_data_collection', '핀테크 데이터 수집 기술', [
 M('## 1. 수집한 데이터 두 가지 살펴보기'),
 C('''ins = load('Revolution/insurance.csv'); ph = load('Revolution2/Website Phishing.csv')
print(ins.shape, ph.shape)
print(ph.Result.value_counts())   # 원자료: 1 = 피싱, 0 = 의심, -1 = 정상
ins.head()'''),
 M('## 2. 대결 재현: 점검한 600건 vs 라벨 오류가 섞인 전부\n깨끗한 라벨 600건으로 학습한 모델과, 학습 세트 전부를 쓰되 라벨의 20%를 일부러 뒤집은 모델을 비교합니다. 이어서 라벨이 **한쪽으로** 틀린 경우(피싱을 정상으로 40% 잘못 적음)도 봅니다.'),
 C('''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score

X = ph.drop(columns='Result').values; y = (ph.Result == 1).astype(int).values
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=.3, random_state=RS, stratify=y)
rng = np.random.default_rng(RS)
idx = rng.choice(len(ytr), size=min(1000, len(ytr)), replace=False)
noisy = ytr.copy(); flip = rng.random(len(noisy)) < .2; noisy[flip] = 1 - noisy[flip]

clean = LogisticRegression(max_iter=2000).fit(Xtr[idx[:600]], ytr[idx[:600]])
rand = LogisticRegression(max_iter=2000).fit(Xtr, noisy)
biased_y = ytr.copy(); f2 = (ytr == 1) & (rng.random(len(ytr)) < .4); biased_y[f2] = 0
biased = LogisticRegression(max_iter=2000).fit(Xtr, biased_y)
for name, m in [('깨끗한 600건', clean), ('전부 + 무작위 오류 20%', rand), ('전부 + 한쪽 오류', biased)]:
    print(f'{name:16s} 정확도 {m.score(Xte, yte):.3f}  피싱 재현율 {recall_score(yte, m.predict(Xte)):.3f}')'''),
 M('**AI 판단 연습** — 무작위 오류와 한쪽으로 치우친 오류 중 어느 쪽이 재현율을 더 크게 떨어뜨리나요? 데이터를 "많이" 모으는 것과 "제대로" 모으는 것의 차이를 한 문장으로 적어 보세요.'),
]))

NB.append(('03', '03_collection_plan', '데이터 분석을 위한 준비 — 수집 계획', [
 M('## 1. 데이터 사전: 열 이름만 보고는 뜻을 모른다'),
 C('''ld = load('Revolution4/loan_data_description.csv')
ld = ld[ld.LoanStatNew.notna()]
print(len(ld), '개 열 설명'); ld.head(10)'''),
 M('## 2. 대결 재현: 수집 주기가 길면 숫자가 얼마나 낡나\n주가를 매일 모으면 오늘 값을 바로 쓰고, 한 달(21거래일)마다 모으면 그 사이에는 마지막으로 받은 값을 씁니다. 그 차이를 평균 상대 오차로 봅니다.'),
 C('''p = load('Revolution3/portfolio_data.csv')
def stale(x, gap):
    x = np.asarray(x, float)
    est = np.array([x[(i // gap) * gap - 1] if (i // gap) * gap >= 1 else x[0] for i in range(len(x))])
    m = np.arange(len(x)) >= gap
    return np.mean(np.abs(x[m] - est[m]) / x[m])
for c in ['AMZN', 'BTC']:
    print(c, {g: f'{stale(p[c], gap):.1%}' for g, gap in [('매일', 1), ('주 1회', 5), ('월 1회', 21), ('분기 1회', 63)]})'''),
 M('**AI 판단 연습** — "매일 모으면 오차 0%"는 당연한 결과일까요? 매일 모으는 데 드는 비용(저장·점검·사람)까지 생각하면 어떤 데이터는 월 1회로도 충분할 수 있어요. 어떤 데이터일까요?'),
]))

NB.append(('04', '04_analysis_concepts', '데이터 분석 개념의 이해', [
 M('## 1. 학습 점수와 시험 점수\n거래 횟수·거래 금액 두 열로 KNN 분류기를 만들고, k를 바꿔 가며 학습 데이터 점수와 시험 데이터 점수를 비교합니다.'),
 C(BANK + '''
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
X = b[['Total_Trans_Ct', 'Total_Trans_Amt']].values.astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, b.y, test_size=.25, random_state=RS, stratify=b.y)
sc = StandardScaler().fit(Xtr); Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)
rows = []
for k in [1, 3, 5, 9, 15, 31, 51]:
    m = KNeighborsClassifier(k).fit(Xtr, ytr)
    rows.append((k, round(m.score(Xtr, ytr), 3), round(m.score(Xte, yte), 3)))
pd.DataFrame(rows, columns=['k', '학습 점수', '시험 점수'])'''),
 M('## 2. 대결 재현: 학습 점수 99.8%의 k=1 vs 시험 점수로 고른 k=15\nk=1은 학습 데이터를 거의 외웁니다. 시험 점수는 어떨까요? 위 표에서 두 줄을 비교해 보세요.'),
 C('''plt.plot([r[0] for r in rows], [r[1] for r in rows], 'o-', label='train')
plt.plot([r[0] for r in rows], [r[2] for r in rows], 's-', label='test')
plt.xscale('log'); plt.xlabel('k'); plt.ylabel('accuracy'); plt.legend(); plt.show()'''),
 M('**AI 판단 연습** — 어떤 업체가 "우리 모델 정확도 99.8%"라고 광고합니다. 가장 먼저 물어야 할 질문 하나는? (힌트: 어떤 데이터로 잰 점수인가)'),
]))

NB.append(('05', '05_preprocessing', '분류모형(1) — Colab과 전처리', [
 M('## 1. 빈 값 대신 "Unknown"으로 적힌 값'),
 C(BANK + '''
for c in ['Education_Level', 'Income_Category', 'Marital_Status']:
    print(c, (b[c] == 'Unknown').sum())'''),
 M('## 2. 이상치: IQR 규칙\n제3사분위수(Q3) + 1.5 × IQR 보다 큰 거래 금액을 이상치 후보로 봅니다.'),
 C('''q1, q3 = b.Total_Trans_Amt.quantile([.25, .75]); iqr = q3 - q1
up = q3 + 1.5 * iqr
out = b.Total_Trans_Amt > up
print(f'Q1={q1:.0f}, Q3={q3:.0f}, IQR={iqr:.0f}, 위 경계={up:.0f}, 이상치 후보 {out.sum()}명, 그중 이탈 비율 {b.y[out].mean():.1%}')'''),
 M('이상치 후보의 이탈 비율이 전체(16%)와 크게 다르다면, 지우기 전에 "왜 튀는가"를 먼저 봐야 합니다.'),
 M('## 3. 대결 재현: Unknown 행 삭제 vs 범주로 유지'),
 C('''from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
feat = ['Customer_Age', 'Gender', 'Education_Level', 'Income_Category', 'Marital_Status',
        'Total_Trans_Ct', 'Total_Trans_Amt', 'Total_Relationship_Count', 'Months_Inactive_12_mon']
mask = (b.Education_Level != 'Unknown') & (b.Income_Category != 'Unknown') & (b.Marital_Status != 'Unknown')
tr_i, te_i = train_test_split(np.arange(len(b)), test_size=.25, random_state=RS, stratify=b.y)
tr, te = b.iloc[tr_i], b.iloc[te_i]
def fit(train):
    Xa = pd.get_dummies(pd.concat([train, te])[feat], drop_first=True).astype(float)
    Xtr, Xte = Xa.iloc[:len(train)], Xa.iloc[len(train):]
    s = StandardScaler().fit(Xtr)
    return LogisticRegression(max_iter=3000).fit(s.transform(Xtr), train.y).score(s.transform(Xte), te.y)
print('Unknown 행 삭제 (학습', mask.iloc[tr_i].sum(), '명):', round(fit(tr[mask.iloc[tr_i].values]), 4))
print('Unknown 범주 유지 (학습', len(tr), '명):', round(fit(tr), 4))'''),
 M('**손으로 한 번** — 아무 모델 없이 "모두 이탈 안 함"이라고 하면 정확도는? 8,500 ÷ 10,127 ≈ 83.9%. 위 두 숫자가 이 기준보다 얼마나 높은지 보세요.'),
]))

NB.append(('06', '06_knn_svm', '데이터 분석 실습 — KNN·SVM·분할·표준화', [
 M('## 1. 순서대로 자르면 생기는 일\n이탈 여부로 정렬된 데이터의 앞 75%를 학습, 뒤 25%를 시험으로 쓰면?'),
 C(BANK + '''
bs = b.sort_values('y'); cut = int(len(bs) * .75)
print('학습 세트 이탈 고객:', bs.y.values[:cut].sum(), ' / 시험 세트 이탈 고객:', bs.y.values[cut:].sum(), '명 중', len(bs) - cut)'''),
 M('## 2. 대결 재현: 표준화한 SVM vs 그대로 SVM\n거래 횟수(10~139)와 거래 금액(510~18,484)은 단위 크기가 100배 넘게 다릅니다.'),
 C('''from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import recall_score
X = b[['Total_Trans_Ct', 'Total_Trans_Amt']].values.astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, b.y.values, test_size=.25, random_state=RS, stratify=b.y)
sc = StandardScaler().fit(Xtr)
raw = SVC(kernel='rbf', C=1).fit(Xtr, ytr)
std = SVC(kernel='rbf', C=1).fit(sc.transform(Xtr), ytr)
print('그대로   정확도', round(raw.score(Xte, yte), 4), ' 이탈 재현율', round(recall_score(yte, raw.predict(Xte)), 4))
print('표준화   정확도', round(std.score(sc.transform(Xte), yte), 4), ' 이탈 재현율', round(recall_score(yte, std.predict(sc.transform(Xte))), 4))
print('시험 세트 이탈 고객 수:', yte.sum())'''),
 M('**AI 판단 연습** — "그대로" 모델의 정확도 83.9%는 무엇과 같은 숫자인가요? (5회차의 "모두 이탈 안 함" 기준과 비교)'),
]))

NB.append(('07', '07_model_evaluation', '데이터 분석 모델의 평가', [
 M('## 1. 여행자 보험 청구 데이터: 청구가 1.5%뿐'),
 C('''t = load('Revolution/travel insurance.csv')
t['y'] = (t.Claim == 'Yes').astype(int)
print(t.shape, '청구 비율', round(t.y.mean(), 4))'''),
 C('''from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score, recall_score, accuracy_score
X = pd.get_dummies(t[['Agency', 'Agency Type', 'Distribution Channel', 'Product Name', 'Duration',
                      'Net Sales', 'Commision (in value)', 'Age']], drop_first=True).astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, t.y, test_size=.25, random_state=RS, stratify=t.y)
s = StandardScaler().fit(Xtr)
pr = LogisticRegression(max_iter=3000).fit(s.transform(Xtr), ytr).predict_proba(s.transform(Xte))[:, 1]
print('AUC', round(roc_auc_score(yte, pr), 3))'''),
 M('## 2. 대결 재현: "모두 청구 없음" vs 로지스틱(임계값 0.02)'),
 C('''for name, p in [('모두 청구 없음', np.zeros(len(yte), int)), ('로지스틱 0.02', (pr >= .02).astype(int))]:
    tn, fp, fn, tp = confusion_matrix(yte, p).ravel()
    print(f'{name:10s} 정확도 {accuracy_score(yte, p):.3f}  재현율 {recall_score(yte, p, zero_division=0):.3f}  TP={tp} FP={fp} FN={fn} TN={tn}')'''),
 M('## 3. 임계값을 바꾸면'),
 C('''for th in [0.01, 0.02, 0.05, 0.1, 0.3, 0.5]:
    tn, fp, fn, tp = confusion_matrix(yte, (pr >= th).astype(int)).ravel()
    print(f'임계값 {th:<5} 잡은 청구 {tp:3d} / 놓친 청구 {fn:3d} / 잘못 경보 {fp:5d}')'''),
 M('**AI 판단 연습** — 원고의 "정확도 77% → 97%로 개선" 같은 문장을 보면, 같은 데이터에서 "모두 아니오"의 정확도부터 계산해 보세요.'),
]))

NB.append(('09', '09_regression', '회귀모형(1)', [
 M('## 1. 보험료를 나이·BMI·흡연으로 예측'),
 C('''from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score, mean_absolute_error
ins = load('Revolution/insurance.csv'); ins['sm'] = (ins.smoker == 'yes').astype(int)
tr, te = train_test_split(ins, test_size=.25, random_state=RS)
for cols in (['age'], ['age', 'bmi'], ['age', 'bmi', 'sm']):
    m = LinearRegression().fit(tr[cols], tr.charges)
    print(cols, 'R² =', round(r2_score(te.charges, m.predict(te[cols])), 3), ' 계수', dict(zip(cols, m.coef_.round(0).tolist())))'''),
 M('## 2. 대결 재현: 데이터 범위 밖(외삽) — 선형 vs KNN 회귀\n쇼핑몰 고객 중 연봉 하위 90%로 학습하고 상위 10% 고객의 소비액을 맞혀 봅니다.'),
 C('''dm = load('Revolution/DirectMarketing.csv')
x = dm.Salary.values.reshape(-1, 1) / 1000; y = dm.AmountSpent.values
cut = np.quantile(x[:, 0], .9); lo, hi = x[:, 0] <= cut, x[:, 0] > cut
knn = KNeighborsRegressor(5).fit(x[lo], y[lo]); lin = LinearRegression().fit(x[lo], y[lo])
print(f'경계 연봉 {cut:.1f}천 달러, 상위 고객 {hi.sum()}명, 실제 평균 소비 {y[hi].mean():.0f}')
print('KNN MAE', round(mean_absolute_error(y[hi], knn.predict(x[hi]))), '  KNN 예측 최댓값', knn.predict(x[hi]).max())
print('선형 MAE', round(mean_absolute_error(y[hi], lin.predict(x[hi]))))'''),
 C('''xs = np.linspace(x.min(), x.max(), 300).reshape(-1, 1)
plt.scatter(x, y, s=4, c=np.where(hi, 'tab:red', 'tab:gray'))
plt.plot(xs, knn.predict(xs), label='KNN'); plt.plot(xs, lin.predict(xs), label='linear')
plt.axvline(cut, ls='--', c='k'); plt.xlabel('salary (k$)'); plt.ylabel('amount spent'); plt.legend(); plt.show()'''),
 M('**AI 판단 연습** — KNN 예측이 경계선 오른쪽에서 평평해지는 이유를 "이웃"이라는 말로 설명해 보세요.'),
]))

NB.append(('10', '10_logistic_tree', '회귀모형(2) — 로지스틱·결정나무·특성공학', [
 M('## 1. 로지스틱 곡선: 거래 횟수로 이탈 확률'),
 C(BANK + '''
from sklearn.linear_model import LogisticRegression
lr = LogisticRegression().fit(b[['Total_Trans_Ct']], b.y)
xs = np.arange(10, 140).reshape(-1, 1)
plt.plot(xs, lr.predict_proba(xs)[:, 1], label='logistic')
g = b.groupby(pd.cut(b.Total_Trans_Ct, range(10, 141, 10))).y.mean()
plt.plot([iv.mid for iv in g.index], g.values, 'o', label='actual (10-wide bins)')
plt.xlabel('Total_Trans_Ct'); plt.ylabel('P(attrition)'); plt.legend(); plt.show()'''),
 M('실제 비율(점)은 40~50회 구간에서 다시 튀어 오릅니다. S자 곡선 하나로는 이 모양을 못 따라가요.'),
 M('## 2. 결정나무: 깊이에 따른 학습·시험 점수'),
 C('''from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text
X = b[['Total_Trans_Ct', 'Total_Revolving_Bal']].values.astype(float)
Xtr, Xte, ytr, yte = train_test_split(X, b.y, test_size=.25, random_state=RS, stratify=b.y)
for d in [1, 2, 3, 4, 6, 10, None]:
    m = DecisionTreeClassifier(max_depth=d, random_state=RS).fit(Xtr, ytr)
    print(f'깊이 {str(d):4s} 학습 {m.score(Xtr, ytr):.3f}  시험 {m.score(Xte, yte):.3f}  잎 {m.get_n_leaves()}')
print(export_text(DecisionTreeClassifier(max_depth=2, random_state=RS).fit(Xtr, ytr), feature_names=['Trans_Ct', 'Revolving_Bal']))'''),
 M('## 3. 대결 재현: 기본 특성 3개 vs 이유 있게 만든 특성 6개'),
 C('''from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
ins = load('Revolution/insurance.csv')
ins['sm'] = (ins.smoker == 'yes').astype(int); ins['obese'] = (ins.bmi >= 30).astype(int)
ins['age2'] = ins.age ** 2; ins['sm_obese'] = ins.sm * ins.obese; ins['sm_bmi'] = ins.sm * ins.bmi
tr, te = train_test_split(ins, test_size=.25, random_state=RS)
for cols in (['age', 'bmi', 'sm'], ['age', 'age2', 'bmi', 'sm', 'sm_obese', 'sm_bmi']):
    m = LinearRegression().fit(tr[cols], tr.charges)
    print(len(cols), '개 특성  R² =', round(r2_score(te.charges, m.predict(te[cols])), 3))'''),
 M('**AI 판단 연습** — "흡연 × 비만"이라는 특성은 왜 의미가 있을까요? 데이터 산점도(흡연자만 BMI 30을 넘으면 보험료가 뜀)로 확인해 보세요.'),
]))

NB.append(('11', '11_deep_learning_timeseries', '딥러닝 모델과 시계열 데이터 분석', [
 M('> 이 노트북은 교육용이며 투자 자문이 아닙니다. 주가는 2013~2019년 저장소 데이터입니다.\n\n## 1. 가격과 수익률'),
 C('''p = load('Revolution3/portfolio_data.csv'); p['Date'] = pd.to_datetime(p.Date)
fig, ax = plt.subplots(1, 2, figsize=(11, 3))
ax[0].plot(p.Date, p.NFLX); ax[0].set_title('NFLX price')
ax[1].plot(p.Date[1:], np.diff(np.log(p.NFLX)) * 100); ax[1].set_title('NFLX daily log return (%)')
plt.show()'''),
 M('## 2. 대결 재현: "내일 = 오늘" vs AR(10)\n과거 10일 가격으로 내일 가격을 맞히는 선형 모델(AR)과, 오늘 가격을 그대로 내일 예측으로 쓰는 기준을 마지막 120거래일로 비교합니다.'),
 C('''from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
def ar_vs_naive(series, lags=10, ntest=120):
    y = np.asarray(series, float); n = len(y)
    X = np.column_stack([y[lags - i - 1:n - i - 1] for i in range(lags)]); t = y[lags:]
    m = LinearRegression().fit(X[:-ntest], t[:-ntest])
    return mean_absolute_error(t[-ntest:], X[-ntest:, 0]), mean_absolute_error(t[-ntest:], m.predict(X[-ntest:]))
for c in ['NFLX', 'BTC']:
    nv, ar = ar_vs_naive(p[c])
    print(f'{c}: 내일=오늘 MAE {nv:.2f}   AR(10) MAE {ar:.2f}')'''),
 M('**AI 판단 연습** — 예측 그래프가 실제 선과 "거의 겹친다"면 좋은 모델일까요? 하루씩 늦게 따라가는 선도 겹쳐 보입니다. 기준(내일 = 오늘)과 먼저 비교하세요.'),
]))

NB.append(('12', '12_visualization', '핀테크 데이터 시각화', [
 M('## 1. 꼬리가 긴 분포: 보험료'),
 C('''ins = load('Revolution/insurance.csv')
plt.hist(ins.charges, bins=40); plt.axvline(ins.charges.mean(), c='r', label='mean'); plt.axvline(ins.charges.median(), c='k', label='median')
plt.legend(); plt.xlabel('charges ($)'); plt.show()
print('평균', round(ins.charges.mean()), ' 중앙값', round(ins.charges.median()), ' 왜도', round(ins.charges.skew(), 2))'''),
 M('## 2. 대결 재현: 숫자 하나로 새 고객 보험료 맞히기 — 평균 vs 중앙값\n잣대(MAE, RMSE)에 따라 승자가 바뀝니다.'),
 C('''r = np.random.default_rng(RS); i = r.permutation(len(ins))
a, c = ins.charges.values[i[:900]], ins.charges.values[i[900:]]
for name, v in [('평균', a.mean()), ('중앙값', np.median(a))]:
    print(f'{name:4s} {v:8.0f}   MAE {np.abs(c - v).mean():8.0f}   RMSE {np.sqrt(((c - v) ** 2).mean()):8.0f}')'''),
 M('## 3. 상관 행렬: 수익률로 볼 것'),
 C('''p = load('Revolution3/portfolio_data.csv')
ret = p[['AMZN', 'DPZ', 'BTC', 'NFLX']].pct_change().dropna()
print('가격 상관\\n', p[['AMZN', 'DPZ', 'BTC', 'NFLX']].corr().round(2))
print('\\n수익률 상관\\n', ret.corr().round(2))'''),
 M('**AI 판단 연습** — 가격 상관이 0.9를 넘는데 수익률 상관은 0.2 안팎이라면, "두 종목이 같이 움직인다"는 말은 어느 쪽 숫자에 근거해야 할까요?'),
]))

NB.append(('13', '13_robo_advisor', '데이터 기반 핀테크 서비스 기획 — 로보어드바이저', [
 M('> 교육용 백테스트이며 투자 자문이 아닙니다. 거래 비용 0.1%를 가정했습니다.\n\n## 1. 이동평균 교차 전략 백테스트'),
 C('''p = load('Revolution3/portfolio_data.csv')
def ma_bt(series, s, l, fee=0.001):
    x = pd.Series(np.asarray(series, float)); r = x.pct_change().fillna(0)
    sig = (x.rolling(s).mean() > x.rolling(l).mean()).astype(int).shift(1).fillna(0)
    strat = sig * r - sig.diff().abs().fillna(0) * fee
    eq, bh = (1 + strat).cumprod(), (1 + r).cumprod()
    mdd = lambda e: (e / e.cummax() - 1).min()
    return eq, bh, dict(전략배수=round(float(eq.iloc[-1]), 2), 보유배수=round(float(bh.iloc[-1]), 2), 전략낙폭=round(float(mdd(eq)), 3), 보유낙폭=round(float(mdd(bh)), 3))
for c in ['AMZN', 'BTC']:
    print(c, ma_bt(p[c], 20, 60)[2])'''),
 C('''eq, bh, _ = ma_bt(p.BTC, 20, 60)
plt.plot(eq / eq.cummax() - 1, label='MA 20/60'); plt.plot(bh / bh.cummax() - 1, c='gray', label='buy & hold')
plt.title('BTC drawdown'); plt.legend(); plt.show()'''),
 M('## 2. 위험 성향별 배분 (주식 3종 동일 비중 + 안전자산 연 2% 가정)'),
 C('''ret = p[['AMZN', 'DPZ', 'NFLX']].pct_change().dropna().mean(axis=1)
for w in [0, .2, .4, .6, .8, 1]:
    rr = w * ret + (1 - w) * 0.02 / 252; e = (1 + rr).cumprod()
    print(f'주식 {w:.0%}: 연 수익 {rr.mean() * 252:.1%}  연 변동성 {rr.std() * np.sqrt(252):.1%}  최대 낙폭 {(e / e.cummax() - 1).min():.1%}')'''),
 M('**AI 판단 연습** — 같은 전략이 아마존에서는 지고 비트코인에서는 이겼습니다. "이 전략이 좋다"고 말하려면 무엇을 더 확인해야 할까요? (기간, 종목, 비용, 과최적화)'),
]))

NB.append(('14', '14_security_quality', '데이터 보안 및 품질 관리', [
 M('## 1. 준식별자 조합으로 한 사람이 특정되는가'),
 C('''ins = load('Revolution/insurance.csv'); ins['bmi_r'] = ins.bmi.round(1)
for cols in (['age', 'sex', 'bmi_r', 'children', 'region'], ['age', 'sex', 'children', 'region'], ['age', 'sex', 'region']):
    g = ins.groupby(cols).size()
    print(cols, ' 혼자인 묶음', (g == 1).sum(), '/ 전체 묶음', len(g))'''),
 M('## 2. 대결 재현: 덜 묶은 비식별 vs 크게 묶은 비식별 (k-익명성)'),
 C('''def kanon(w, region, children):
    d = ins.copy(); d['ab'] = (d.age // w) * w
    cols = ['ab', 'sex'] + (['region'] if region else []) + (['children'] if children else [])
    g = d.groupby(cols).size()
    return dict(k=int(g.min()), 묶음=len(g), 위험인원=int(g[g < 5].sum()))
print('나이 5살 단위 + 자녀 공개:', kanon(5, 0, 1))
print('나이 20살 단위, 지역·자녀 삭제:', kanon(20, 0, 0))'''),
 M('## 3. 원자료 품질 점검'),
 C('''t = load('Revolution/travel insurance.csv')
print('성별 결측', t.Gender.isna().sum(), '/', len(t))
print('여행 기간 음수', (t.Duration < 0).sum(), '  나이 100세 초과', (t.Age > 100).sum(), '  순매출 음수', (t['Net Sales'] < 0).sum())
s = load('Revolution6/Financial_Sentiment_Analysis.csv')
print('감성 문장 중복', s.Sentence.duplicated().sum(), '  같은 문장에 다른 라벨', s.groupby('Sentence').Sentiment.nunique().gt(1).sum())'''),
 M('**AI 판단 연습** — 나이 118세 고객이 여럿이라면 오류일까요, 기본값(코드)일까요? 지우기 전에 누구에게 무엇을 물어야 할까요?'),
]))


def header(num, fname, title):
    url = f'https://colab.research.google.com/github/{REPO}/blob/main/notebooks/{num}_{fname.split("_", 1)[1]}.ipynb'
    return M(f'# {num}회차 실습 노트북 — {title}\n\n'
             f'[![Colab에서 열기](https://colab.research.google.com/assets/colab-badge.svg)]({url})\n\n'
             f'해설 페이지: [{SITE}{fname}.html]({SITE}{fname}.html)\n\n'
             '위에서부터 셀을 차례로 실행하세요(Shift+Enter). 데이터는 저장소 `data/` 폴더(fintech-data 복사본)에서 읽으며, '
             '무작위 시드를 42로 고정해 해설 페이지의 대결 숫자와 같은 값이 나옵니다.\n\n'
             '글 · 안상선 ((주)M-Robo 대표)')


def build(run=True):
    from nbclient import NotebookClient
    made = []
    for num, fname, title, cells in NB:
        nb = new_notebook(cells=[header(num, fname, title), C(SETUP)] + cells)
        nb.metadata = {'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'},
                       'language_info': {'name': 'python'}, 'colab': {'provenance': []}}
        path = os.path.join(OUT, f'{fname}.ipynb')
        if run:
            NotebookClient(nb, timeout=300, kernel_name='python3', resources={'metadata': {'path': OUT}}).execute()
        nbformat.write(nb, path); made.append(path); print('ok', path)
    return made


if __name__ == '__main__':
    build(run='--no-run' not in sys.argv)
