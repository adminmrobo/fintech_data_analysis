#!/usr/bin/env python3
"""fintech-data 원자료(data/)로 회차별 실험·대결·대시보드에 쓸 숫자와 표본을 계산한다.
결과: src/analysis/results.json  (빌드 때 pages/*.py 가 읽어 씀)
모든 무작위 과정은 random_state=42 로 고정."""
import json, os, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc,
                             confusion_matrix, mean_squared_error, mean_absolute_error, r2_score)
warnings.filterwarnings('ignore')
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = lambda *p: os.path.join(ROOT, 'data', *p)
R = {}
rs = 42
r3 = lambda v: float(round(float(v), 4))

# ---------------- 은행 고객(이탈) ----------------
b = pd.read_csv(D('Revolution', 'Bank_customers_data.csv'))
b['y'] = (b.Attrition_Flag == 'Attrited Customer').astype(int)
R['bank'] = dict(n=len(b), attr=int(b.y.sum()), cols=len(b.columns) - 1,
                 unknown={c: int((b[c] == 'Unknown').sum()) for c in ['Education_Level', 'Income_Category', 'Marital_Status']},
                 dtypes={'int': int((b.dtypes == 'int64').sum()), 'float': int((b.dtypes == 'float64').sum()), 'str': int((b.dtypes == object).sum() + (b.dtypes == 'str').sum())})
# 컬럼 요약 (1회차 실험)
cols = []
for c in ['Customer_Age', 'Gender', 'Dependent_count', 'Education_Level', 'Marital_Status', 'Income_Category', 'Card_Category', 'Months_on_book',
          'Total_Relationship_Count', 'Months_Inactive_12_mon', 'Contacts_Count_12_mon', 'Credit_Limit', 'Total_Revolving_Bal', 'Total_Trans_Amt', 'Total_Trans_Ct', 'Avg_Utilization_Ratio']:
    s = b[c]
    if s.dtype == object or str(s.dtype) == 'str':
        vc = s.value_counts()
        cols.append(dict(c=c, kind='cat', top=[[str(k), int(v)] for k, v in vc.head(6).items()],
                         rate=[[str(k), r3(b.loc[s == k, 'y'].mean())] for k in vc.head(6).index]))
    else:
        q = np.quantile(s, [0, .2, .4, .6, .8, 1])
        bins = pd.cut(s, bins=np.unique(q), include_lowest=True)
        g = b.groupby(bins, observed=True)['y'].agg(['mean', 'size'])
        cols.append(dict(c=c, kind='num', mean=r3(s.mean()), med=r3(s.median()), min=r3(s.min()), max=r3(s.max()),
                         rate=[[f'{iv.left:.0f}~{iv.right:.0f}' if s.max() > 5 else f'{iv.left:.2f}~{iv.right:.2f}', r3(m)] for iv, (m, n) in zip(g.index, g.values)]))
R['bank']['cols'] = cols

# 1회차 대결: 행동 데이터 1개 vs 인구통계 5개 (로지스틱, 정확도·재현율)
demo = pd.get_dummies(b[['Customer_Age', 'Gender', 'Education_Level', 'Income_Category', 'Marital_Status']], drop_first=True).astype(float)
beh = b[['Total_Trans_Ct']].astype(float)
yb = b.y.values
def lr_eval(X):
    Xtr, Xte, ytr, yte = train_test_split(X, yb, test_size=.25, random_state=rs, stratify=yb)
    sc = StandardScaler().fit(Xtr); m = LogisticRegression(max_iter=2000, class_weight='balanced').fit(sc.transform(Xtr), ytr)
    p = m.predict(sc.transform(Xte)); pr = m.predict_proba(sc.transform(Xte))[:, 1]
    fpr, tpr, _ = roc_curve(yte, pr)
    return dict(acc=r3(accuracy_score(yte, p)), rec=r3(recall_score(yte, p)), auc=r3(auc(fpr, tpr)), f1=r3(f1_score(yte, p)))
R['duel01'] = dict(beh=lr_eval(beh), demo=lr_eval(demo), n_demo_cols=demo.shape[1])

# 5·6회차: 2특성(거래 횟수, 거래 금액) 표본
sm = b.sample(400, random_state=7)
R['knn_sample'] = dict(x=sm.Total_Trans_Ct.tolist(), y=sm.Total_Trans_Amt.tolist(), t=sm.y.tolist())
X2 = b[['Total_Trans_Ct', 'Total_Trans_Amt']].values.astype(float)
Xtr, Xte, ytr, yte = train_test_split(X2, yb, test_size=.25, random_state=rs, stratify=yb)
sc = StandardScaler().fit(Xtr)
knn_raw = {}; knn_std = {}
for k in [1, 3, 5, 7, 9, 11, 15, 21, 31, 51]:
    m = KNeighborsClassifier(k).fit(Xtr, ytr); knn_raw[k] = [r3(m.score(Xtr, ytr)), r3(m.score(Xte, yte))]
    m = KNeighborsClassifier(k).fit(sc.transform(Xtr), ytr); knn_std[k] = [r3(m.score(sc.transform(Xtr), ytr)), r3(m.score(sc.transform(Xte), yte))]
svm_lin = SVC(kernel='linear', C=1).fit(sc.transform(Xtr), ytr); svm_rbf = SVC(kernel='rbf', C=1).fit(sc.transform(Xtr), ytr)
svm_raw = SVC(kernel='rbf', C=1).fit(Xtr, ytr)
R['knn'] = dict(raw=knn_raw, std=knn_std, mu=sc.mean_.tolist(), sd=sc.scale_.tolist(),
                svm_lin=r3(svm_lin.score(sc.transform(Xte), yte)), svm_rbf=r3(svm_rbf.score(sc.transform(Xte), yte)), svm_raw=r3(svm_raw.score(Xte, yte)),
                svm_lin_w=svm_lin.coef_[0].tolist(), svm_lin_b=float(svm_lin.intercept_[0]), base=r3(1 - yb.mean()),
                ntr=len(ytr), nte=len(yte))
# 6회차 대결: 표준화 전 vs 후 KNN(k=5)
R['duel06'] = dict(raw=knn_raw[5][1], std=knn_std[5][1])
# 6회차: 순서대로 자르기(정렬된 데이터의 앞 75%) vs 무작위 분할
bs = b.sort_values('y')  # 기존 고객이 앞, 이탈 고객이 뒤 (교안의 도미 35 · 빙어 14 순서와 같은 상황)
cut = int(len(bs) * .75)
m = KNeighborsClassifier(5).fit(StandardScaler().fit_transform(bs[['Total_Trans_Ct', 'Total_Trans_Amt']].values[:cut]), bs.y.values[:cut])
sc2 = StandardScaler().fit(bs[['Total_Trans_Ct', 'Total_Trans_Amt']].values[:cut])
R['order_split'] = dict(train_attr=int(bs.y.values[:cut].sum()), test_attr=int(bs.y.values[cut:].sum()), test_n=len(bs) - cut,
                        acc=r3(KNeighborsClassifier(5).fit(sc2.transform(bs[['Total_Trans_Ct', 'Total_Trans_Amt']].values[:cut]), bs.y.values[:cut]).score(sc2.transform(bs[['Total_Trans_Ct', 'Total_Trans_Amt']].values[cut:]), bs.y.values[cut:])))

# 4회차: 학습 데이터로 평가(1-NN) vs 분리 평가
m1 = KNeighborsClassifier(1).fit(sc.transform(Xtr), ytr)
R['duel04'] = dict(train_acc=r3(m1.score(sc.transform(Xtr), ytr)), test_acc=r3(m1.score(sc.transform(Xte), yte)),
                   k15_train=knn_std[15][0], k15_test=knn_std[15][1])

# 5회차: Unknown 행 삭제 vs 범주로 유지 (로지스틱, 인구통계+행동 몇 개)
feat = ['Customer_Age', 'Gender', 'Education_Level', 'Income_Category', 'Marital_Status', 'Total_Trans_Ct', 'Total_Trans_Amt', 'Total_Relationship_Count', 'Months_Inactive_12_mon']
def prep(df):
    return pd.get_dummies(df[feat], drop_first=True).astype(float)
mask = (b.Education_Level != 'Unknown') & (b.Income_Category != 'Unknown') & (b.Marital_Status != 'Unknown')
tr_idx, te_idx = train_test_split(np.arange(len(b)), test_size=.25, random_state=rs, stratify=yb)
te = b.iloc[te_idx]
def fit_lr(train_df, test_df):
    Xa = prep(pd.concat([train_df, test_df])); Xtr_ = Xa.iloc[:len(train_df)]; Xte_ = Xa.iloc[len(train_df):]
    s = StandardScaler().fit(Xtr_); m = LogisticRegression(max_iter=3000).fit(s.transform(Xtr_), train_df.y)
    return m.predict(s.transform(Xte_))
tr = b.iloc[tr_idx]
p_drop = fit_lr(tr[mask.iloc[tr_idx].values], te); p_keep = fit_lr(tr, te)
R['duel05'] = dict(n_all=len(b), n_drop=int(mask.sum()), dropped=int((~mask).sum()),
                   drop_acc=r3(accuracy_score(te.y, p_drop)), keep_acc=r3(accuracy_score(te.y, p_keep)),
                   drop_train=int(mask.iloc[tr_idx].sum()), keep_train=len(tr_idx))
# 이상치(IQR) 개수
q1, q3 = b.Total_Trans_Amt.quantile([.25, .75]); iqr = q3 - q1
R['outlier'] = dict(q1=r3(q1), q3=r3(q3), iqr=r3(iqr), up15=r3(q3 + 1.5 * iqr), n15=int((b.Total_Trans_Amt > q3 + 1.5 * iqr).sum()),
                    n3=int((b.Total_Trans_Amt > q3 + 3 * iqr).sum()), attr_rate_out=r3(b.y[b.Total_Trans_Amt > q3 + 1.5 * iqr].mean()))

# ---------------- 여행자 보험 청구 (7회차) ----------------
t = pd.read_csv(D('Revolution', 'travel insurance.csv'))
t['y'] = (t.Claim == 'Yes').astype(int)
tX = pd.get_dummies(t[['Agency', 'Agency Type', 'Distribution Channel', 'Product Name', 'Duration', 'Net Sales', 'Commision (in value)', 'Age']], drop_first=True).astype(float)
ty = t.y.values
Xtr, Xte, ytr, yte = train_test_split(tX, ty, test_size=.25, random_state=rs, stratify=ty)
s = StandardScaler().fit(Xtr)
lr = LogisticRegression(max_iter=3000).fit(s.transform(Xtr), ytr)
pr = lr.predict_proba(s.transform(Xte))[:, 1]
fpr, tpr, th = roc_curve(yte, pr)
# 임계값 0.005~0.5 에서 혼동행렬
cms = []
for th_ in [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.07, 0.1, 0.15, 0.2, 0.3, 0.5]:
    p = (pr >= th_).astype(int); tn, fp, fn, tp = confusion_matrix(yte, p).ravel()
    cms.append(dict(th=th_, tp=int(tp), fp=int(fp), fn=int(fn), tn=int(tn)))
# ROC 점 줄이기
idx = np.unique(np.linspace(0, len(fpr) - 1, 60).astype(int))
R['travel'] = dict(n=len(t), claim=int(ty.sum()), rate=r3(ty.mean()), nte=len(yte), pos_te=int(yte.sum()),
                   cms=cms, roc=[[r3(fpr[i]), r3(tpr[i])] for i in idx], auc=r3(auc(fpr, tpr)),
                   gender_missing=int(t.Gender.isna().sum()), dur_neg=int((t.Duration < 0).sum()), age_over100=int((t.Age > 100).sum()))
# 7회차 대결: '모두 청구 없음' vs 로지스틱(임계값 0.02)
p_all0 = np.zeros_like(yte); p_lr = (pr >= .02).astype(int)
R['duel07'] = dict(all0=dict(acc=r3(accuracy_score(yte, p_all0)), rec=0.0, caught=0),
                   lr=dict(acc=r3(accuracy_score(yte, p_lr)), rec=r3(recall_score(yte, p_lr)), caught=int(((p_lr == 1) & (yte == 1)).sum()),
                           prec=r3(precision_score(yte, p_lr))))
# 7회차 단계③: 교차검증 (은행 데이터, KNN k=5) 한 번 분할 vs 5겹
Xs = StandardScaler().fit_transform(X2)
singles = []
for seed in range(20):
    a, c, d_, e_ = train_test_split(Xs, yb, test_size=.25, random_state=seed, stratify=yb)
    singles.append(r3(KNeighborsClassifier(5).fit(a, d_).score(c, e_)))
cv = cross_val_score(KNeighborsClassifier(5), Xs, yb, cv=StratifiedKFold(5, shuffle=True, random_state=rs))
# 앙상블: 결정나무 1개 vs 랜덤포레스트 (은행 전체 수치 특성)
numc = [c for c in b.columns if b[c].dtype != object and str(b[c].dtype) != 'str' and c not in ('CLIENTNUM', 'y')]
Xa, Xb_, ya, yb_ = train_test_split(b[numc].values, yb, test_size=.25, random_state=rs, stratify=yb)
dt = DecisionTreeClassifier(random_state=rs).fit(Xa, ya); rf = RandomForestClassifier(200, random_state=rs, n_jobs=-1).fit(Xa, ya)
R['cv'] = dict(singles=singles, cv=[r3(v) for v in cv], cv_mean=r3(cv.mean()), cv_sd=r3(cv.std()),
               tree=r3(dt.score(Xb_, yb_)), forest=r3(rf.score(Xb_, yb_)), nfeat=len(numc))

# ---------------- 2회차: 피싱 데이터 품질 대결 ----------------
ph = pd.read_csv(D('Revolution2', 'Website Phishing.csv'))
phX = ph.drop(columns='Result').values; phy = (ph.Result == 1).astype(int).values  # 1 = 피싱(원자료 Result=1)
Xtr, Xte, ytr, yte = train_test_split(phX, phy, test_size=.3, random_state=rs, stratify=phy)
clean_n = 1000
rng = np.random.default_rng(rs)
idx = rng.choice(len(ytr), size=min(clean_n, len(ytr)), replace=False)
noisy = ytr.copy(); flip = rng.random(len(noisy)) < .2; noisy[flip] = 1 - noisy[flip]
# 깨끗한 쪽은 학습 세트의 일부(적게)만, 시끄러운 쪽은 전부(많이) + 라벨 20% 오류
dt_c = LogisticRegression(max_iter=2000).fit(Xtr[idx[:600]], ytr[idx[:600]])
dt_n = LogisticRegression(max_iter=2000).fit(Xtr, noisy)
R['phish'] = dict(n=len(ph), cols=ph.shape[1] - 1, counts={str(k): int(v) for k, v in ph.Result.value_counts().items()},
                  clean_n=600, noisy_n=len(ytr), clean_acc=r3(dt_c.score(Xte, yte)), noisy_acc=r3(dt_n.score(Xte, yte)), flip=int(flip.sum()))
# 더 심한 오류(라벨이 한쪽으로 치우침: 피싱을 정상으로 30% 잘못 적음)
noisy2 = ytr.copy(); f2 = (ytr == 1) & (rng.random(len(ytr)) < .4); noisy2[f2] = 0
dt_n2 = LogisticRegression(max_iter=2000).fit(Xtr, noisy2)
R['phish']['biased_acc'] = r3(dt_n2.score(Xte, yte)); R['phish']['biased_rec'] = r3(recall_score(yte, dt_n2.predict(Xte)))
R['phish']['clean_rec'] = r3(recall_score(yte, dt_c.predict(Xte))); R['phish']['noisy_rec'] = r3(recall_score(yte, dt_n.predict(Xte)))
R['phish']['flip2'] = int(f2.sum())

# ---------------- 보험료 (2·9·10·12·14회차) ----------------
ins = pd.read_csv(D('Revolution', 'insurance.csv'))
# 비식별: 준식별자 조합의 유일성
def uniq(df, cols):
    g = df.groupby(cols).size(); return int((g == 1).sum()), int(g.min()), int(len(g))
R['ins'] = dict(n=len(ins), mean=r3(ins.charges.mean()), median=r3(ins.charges.median()), sd=r3(ins.charges.std()),
                skew=r3(ins.charges.skew()), smoker=int((ins.smoker == 'yes').sum()),
                q=[r3(v) for v in ins.charges.quantile([0, .25, .5, .75, 1])])
ins2 = ins.copy(); ins2['bmi_r'] = ins2.bmi.round(1)
k_levels = []
for name, cols in [('나이·성별·BMI·자녀·지역', ['age', 'sex', 'bmi_r', 'children', 'region']), ('나이·성별·자녀·지역', ['age', 'sex', 'children', 'region']),
                   ('나이·성별·지역', ['age', 'sex', 'region'])]:
    u, k, g = uniq(ins2, cols); k_levels.append([name, u, k, g])
R['ins']['uniq'] = k_levels
# k-익명성: 나이 구간 폭 × 지역 공개 여부 × 자녀수 공개 여부
kan = []
for w in [1, 5, 10, 20]:
    for reg in [1, 0]:
        for ch in [1, 0]:
            d = ins.copy(); d['ab'] = (d.age // w) * w
            cols = ['ab', 'sex'] + (['region'] if reg else []) + (['children'] if ch else [])
            g = d.groupby(cols).size(); kan.append(dict(w=w, reg=reg, ch=ch, k=int(g.min()), groups=int(len(g)), small=int((g < 5).sum()),
                                                        rows_small=int(g[g < 5].sum())))
R['kanon'] = kan
# 12회차: 평균 vs 중앙값 대결 (보험료 대표값으로 무작위 고객 맞히기)
r = np.random.default_rng(rs); tr_i = r.permutation(len(ins)); a = ins.charges.values[tr_i[:900]]; c = ins.charges.values[tr_i[900:]]
mu, md = a.mean(), np.median(a)
R['duel12'] = dict(mean=r3(mu), median=r3(md), mae_mean=r3(np.abs(c - mu).mean()), mae_med=r3(np.abs(c - md).mean()),
                   rmse_mean=r3(np.sqrt(((c - mu) ** 2).mean())), rmse_med=r3(np.sqrt(((c - md) ** 2).mean())), n_test=len(c))
# 히스토그램 표본(12회차)
R['ins']['charges_sample'] = [r3(v) for v in ins.charges.values]
# 9·10회차: 회귀
ins['sm'] = (ins.smoker == 'yes').astype(int); ins['male'] = (ins.sex == 'male').astype(int); ins['obese'] = (ins.bmi >= 30).astype(int)
ins['age2'] = ins.age ** 2; ins['sm_bmi'] = ins.sm * ins.bmi; ins['sm_obese'] = ins.sm * ins.obese
tr_i, te_i = train_test_split(np.arange(len(ins)), test_size=.25, random_state=rs)
def reg(cols):
    m = LinearRegression().fit(ins.iloc[tr_i][cols], ins.iloc[tr_i].charges); p = m.predict(ins.iloc[te_i][cols]); y = ins.iloc[te_i].charges
    n, k = len(y), len(cols); r2 = r2_score(y, p)
    return dict(r2=r3(r2), adj=r3(1 - (1 - r2) * (n - 1) / (n - k - 1)), rmse=r3(np.sqrt(mean_squared_error(y, p))), mae=r3(mean_absolute_error(y, p)),
                coef={c: r3(v) for c, v in zip(cols, m.coef_)}, b0=r3(m.intercept_))
fe = {}
for name, cols in [('나이', ['age']), ('나이+BMI', ['age', 'bmi']), ('나이+BMI+흡연', ['age', 'bmi', 'sm']), ('+나이²', ['age', 'age2', 'bmi', 'sm']),
                   ('+흡연×비만', ['age', 'age2', 'bmi', 'sm', 'sm_obese']), ('+흡연×BMI', ['age', 'age2', 'bmi', 'sm', 'sm_obese', 'sm_bmi']),
                   ('+자녀·성별', ['age', 'age2', 'bmi', 'sm', 'sm_obese', 'sm_bmi', 'children', 'male'])]:
    fe[name] = reg(cols)
R['fe'] = fe
# 산점도 표본: 나이-보험료(흡연 여부)
smp = ins.sample(400, random_state=3)
R['ins_scatter'] = dict(age=smp.age.tolist(), ch=[r3(v) for v in smp.charges], sm=smp.sm.tolist(), bmi=[r3(v) for v in smp.bmi])

# DirectMarketing: 소비액 회귀 (9회차)
dm = pd.read_csv(D('Revolution', 'DirectMarketing.csv'))
dmx = dm.Salary.values.reshape(-1, 1) / 1000; dmy = dm.AmountSpent.values
Xtr, Xte, ytr, yte = train_test_split(dmx, dmy, test_size=.25, random_state=rs)
kr = KNeighborsRegressor(5).fit(Xtr, ytr); li = LinearRegression().fit(Xtr, ytr)
poly = LinearRegression().fit(np.c_[Xtr, Xtr ** 2], ytr)
R['dm'] = dict(n=len(dm), hist_missing=int(dm.History.isna().sum()), knn_r2=r3(kr.score(Xte, yte)), lin_r2=r3(li.score(Xte, yte)),
               poly_r2=r3(poly.score(np.c_[Xte, Xte ** 2], yte)), lin_coef=r3(li.coef_[0]), lin_b0=r3(li.intercept_),
               poly_c=[r3(v) for v in poly.coef_], poly_b0=r3(poly.intercept_),
               knn_mae=r3(mean_absolute_error(yte, kr.predict(Xte))), lin_mae=r3(mean_absolute_error(yte, li.predict(Xte))),
               knn_train_r2=r3(kr.score(Xtr, ytr)), lin_train_r2=r3(li.score(Xtr, ytr)))
smp = dm.sample(300, random_state=5)
R['dm']['sample'] = dict(x=(smp.Salary / 1000).round(1).tolist(), y=smp.AmountSpent.tolist())
# KNN 회귀 외삽 대결: 연봉 하위 90%로 학습 → 상위 10% 고객 예측
cut = np.quantile(dmx[:, 0], .9)
lo_, hi_ = dmx[:, 0] <= cut, dmx[:, 0] > cut
kr2 = KNeighborsRegressor(5).fit(dmx[lo_], dmy[lo_]); li2 = LinearRegression().fit(dmx[lo_], dmy[lo_])
R['duel09'] = dict(cut=r3(cut), n_hi=int(hi_.sum()), knn_mae=r3(mean_absolute_error(dmy[hi_], kr2.predict(dmx[hi_]))),
                   lin_mae=r3(mean_absolute_error(dmy[hi_], li2.predict(dmx[hi_]))), knn_max=r3(kr2.predict(dmx[hi_]).max()), actual_mean=r3(dmy[hi_].mean()))
# 결측 대체: History 결측을 '없음' 범주로 vs 행 삭제 (선형회귀 R²)
dm2 = dm.copy(); dm2['History'] = dm2.History.fillna('None')
Xd = pd.get_dummies(dm2[['Age', 'Gender', 'OwnHome', 'Married', 'Location', 'Salary', 'Children', 'History', 'Mailing']], drop_first=True).astype(float)
Xtr, Xte, ytr, yte = train_test_split(Xd, dm2.AmountSpent, test_size=.25, random_state=rs)
R['dm']['full_r2'] = r3(LinearRegression().fit(Xtr, ytr).score(Xte, yte))

# ---------------- 10회차: 로지스틱·결정나무 ----------------
# 로지스틱 곡선: 거래 횟수 하나로 이탈 확률
lr1 = LogisticRegression().fit(b[['Total_Trans_Ct']], yb)
R['logit'] = dict(w=r3(lr1.coef_[0][0]), b0=r3(lr1.intercept_[0]),
                  bins=[[int(lo), int(lo + 10), r3(b.y[(b.Total_Trans_Ct >= lo) & (b.Total_Trans_Ct < lo + 10)].mean()), int(((b.Total_Trans_Ct >= lo) & (b.Total_Trans_Ct < lo + 10)).sum())] for lo in range(10, 140, 10)])
# 결정나무 깊이별 (은행 2특성 + 회전잔액)
feat2 = ['Total_Trans_Ct', 'Total_Revolving_Bal']
X3 = b[feat2].values.astype(float)
Xtr, Xte, ytr, yte = train_test_split(X3, yb, test_size=.25, random_state=rs, stratify=yb)
depth = {}
for d_ in [1, 2, 3, 4, 5, 6, 8, 10, 15, None]:
    m = DecisionTreeClassifier(max_depth=d_, random_state=rs).fit(Xtr, ytr)
    depth[str(d_)] = [r3(m.score(Xtr, ytr)), r3(m.score(Xte, yte)), int(m.get_n_leaves())]
R['tree'] = dict(depth=depth, feats=feat2)
# 깊이별 잎(직사각형) — 브라우저 그림용 (깊이 1~4)
def leaves(m, lo=(10, 0), hi=(140, 2600)):
    T = m.tree_; out = []
    def rec(n, box):
        if T.children_left[n] == -1:
            v = T.value[n][0]; out.append([*box, r3(v[1] / v.sum()), int(T.n_node_samples[n])]); return
        f, th = T.feature[n], T.threshold[n]; l = list(box); rr = list(box)
        if f == 0: l[2] = th; rr[0] = th
        else: l[3] = th; rr[1] = th
        rec(T.children_left[n], l); rec(T.children_right[n], rr)
    rec(0, [lo[0], lo[1], hi[0], hi[1]]); return out
R['tree']['leaves'] = {}
R['tree']['rules'] = {}
for d_ in [1, 2, 3, 4]:
    m = DecisionTreeClassifier(max_depth=d_, random_state=rs).fit(Xtr, ytr)
    R['tree']['leaves'][d_] = leaves(m)
m1 = DecisionTreeClassifier(max_depth=1, random_state=rs).fit(Xtr, ytr)
v = m1.tree_.value
R['tree']['root'] = dict(feat=feat2[m1.tree_.feature[0]], th=r3(m1.tree_.threshold[0]), gini=r3(m1.tree_.impurity[0]),
                         left_gini=r3(m1.tree_.impurity[1]), right_gini=r3(m1.tree_.impurity[2]), nl=int(m1.tree_.n_node_samples[1]), nr=int(m1.tree_.n_node_samples[2]),
                         left_rate=r3(v[1][0][1] / v[1][0].sum()), right_rate=r3(v[2][0][1] / v[2][0].sum()))
sm2 = b.sample(400, random_state=11)
R['tree']['sample'] = dict(x=sm2.Total_Trans_Ct.tolist(), y=sm2.Total_Revolving_Bal.tolist(), t=sm2.y.tolist())
R['duel10'] = dict(deep=depth['None'], shallow=depth['4'])
# 부도 예측(회사) — 참고
cb = pd.read_csv(D('Revolution5', 'company_bankruptcy.csv'))
cy = cb['Bankrupt?'].values; cX = cb.drop(columns='Bankrupt?').values
Xtr, Xte, ytr, yte = train_test_split(cX, cy, test_size=.25, random_state=rs, stratify=cy)
s = StandardScaler().fit(Xtr)
lrb = LogisticRegression(max_iter=5000, class_weight='balanced').fit(s.transform(Xtr), ytr)
dtb = DecisionTreeClassifier(max_depth=4, random_state=rs, class_weight='balanced').fit(Xtr, ytr)
R['bankrupt'] = dict(n=len(cb), pos=int(cy.sum()), feats=cX.shape[1], lr_rec=r3(recall_score(yte, lrb.predict(s.transform(Xte)))), lr_acc=r3(lrb.score(s.transform(Xte), yte)),
                     dt_rec=r3(recall_score(yte, dtb.predict(Xte))), dt_acc=r3(dtb.score(Xte, yte)))

# ---------------- 11회차: 시계열 (포트폴리오) ----------------
p = pd.read_csv(D('Revolution3', 'portfolio_data.csv')); p['Date'] = pd.to_datetime(p.Date)
R['port'] = dict(n=len(p), start=str(p.Date.min().date()), end=str(p.Date.max().date()))
for c in ['AMZN', 'DPZ', 'BTC', 'NFLX']:
    R['port'][c] = [r3(v) for v in p[c].values]
R['port']['dates'] = [d.strftime('%Y-%m-%d') for d in p.Date]
ret = p[['AMZN', 'DPZ', 'BTC', 'NFLX']].pct_change().dropna()
R['port']['corr'] = ret.corr().round(3).values.tolist()
R['port']['vol'] = (ret.std() * np.sqrt(252)).round(3).to_dict(); R['port']['mu'] = (ret.mean() * 252).round(3).to_dict()
R['port']['skew'] = ret.skew().round(3).to_dict()
R['port']['corr_price'] = p[['AMZN', 'DPZ', 'BTC', 'NFLX']].corr().round(3).values.tolist()
# AR(p) — 수익률 대신 가격으로 (교안과 같이), 마지막 120일 시험
def ar_eval(series, lags, ntest=120):
    y = np.asarray(series, float); n = len(y)
    X = np.column_stack([y[lags - i - 1:n - i - 1] for i in range(lags)]); t_ = y[lags:]
    Xtr_, ttr = X[:-ntest], t_[:-ntest]; Xte_, tte = X[-ntest:], t_[-ntest:]
    m = LinearRegression().fit(Xtr_, ttr); pr_ = m.predict(Xte_)
    naive = Xte_[:, 0]
    return dict(mae=r3(mean_absolute_error(tte, pr_)), mape=r3(np.mean(np.abs((tte - pr_) / tte))), naive_mae=r3(mean_absolute_error(tte, naive)),
                naive_mape=r3(np.mean(np.abs((tte - naive) / tte))), pred=[r3(v) for v in pr_])
R['ar'] = {}
for c in ['AMZN', 'NFLX', 'BTC']:
    R['ar'][c] = {lg: ar_eval(p[c].values, lg) for lg in [1, 2, 5, 10, 20]}
# 방향 맞히기 (수익률 AR vs 동전): 정상 시계열
def dir_acc(series, lags=5, ntest=300):
    r_ = np.diff(np.log(np.asarray(series, float))); n = len(r_)
    X = np.column_stack([r_[lags - i - 1:n - i - 1] for i in range(lags)]); t_ = r_[lags:]
    m = LinearRegression().fit(X[:-ntest], t_[:-ntest]); pr_ = m.predict(X[-ntest:])
    return r3(np.mean(np.sign(pr_) == np.sign(t_[-ntest:]))), r3(np.mean(t_[-ntest:] > 0))
R['ar_dir'] = {c: dir_acc(p[c].values) for c in ['AMZN', 'NFLX', 'BTC']}
# 정상성: 롤링 평균·표준편차 (가격 vs 수익률) 구간별
def halves(x):
    x = np.asarray(x); k = len(x) // 4
    return [[r3(x[i * k:(i + 1) * k].mean()), r3(x[i * k:(i + 1) * k].std())] for i in range(4)]
R['station'] = {c: dict(price=halves(p[c].values), ret=halves(np.diff(np.log(p[c].values)) * 100)) for c in ['AMZN', 'BTC']}
# 11회차 대결: naive vs AR(10) (NFLX 가격)
R['duel11'] = dict(naive=R['ar']['NFLX'][10]['naive_mae'], ar=R['ar']['NFLX'][10]['mae'], naive_btc=R['ar']['BTC'][10]['naive_mae'], ar_btc=R['ar']['BTC'][10]['mae'])
# 국제 포트폴리오: VIX-DOW 상관
ip = pd.read_csv(D('Revolution3', 'international_portfolio_data.csv'))
for c in ['DOW', 'VIX', 'BTC', 'ETH', 'kospi', 'vkospi', 'gold', 'dol']:
    ip[c] = pd.to_numeric(ip[c].astype(str).str.replace(',', ''), errors='coerce')
ipr = ip.sort_values('real_date')[['real_date', 'DOW', 'VIX', 'BTC', 'kospi', 'vkospi', 'gold', 'dol']].dropna()
rr = ipr[['DOW', 'VIX', 'BTC', 'kospi', 'vkospi', 'gold', 'dol']].pct_change().dropna()
R['intl'] = dict(n=len(ipr), start=str(ipr.real_date.min()), end=str(ipr.real_date.max()), names=['다우', 'VIX', '비트코인', '코스피', 'V코스피', '금', '달러'],
                 corr=rr.corr().round(3).values.tolist(), missing={c: int(ip[c].isna().sum()) for c in ['DOW', 'VIX', 'kospi', 'gold', 'dol']}, rows=len(ip))

# ---------------- 13회차: 로보어드바이저 (이동평균 교차) ----------------
def ma_bt(series, s_, l_, fee=0.001):
    x = pd.Series(np.asarray(series, float)); r_ = x.pct_change().fillna(0)
    sig = (x.rolling(s_).mean() > x.rolling(l_).mean()).astype(int).shift(1).fillna(0)
    trades = sig.diff().abs().fillna(0)
    strat = sig * r_ - trades * fee
    eq = (1 + strat).cumprod(); bh = (1 + r_).cumprod()
    def mdd(e): return float((e / e.cummax() - 1).min())
    def sharpe(rr_): return float(rr_.mean() / rr_.std() * np.sqrt(252)) if rr_.std() > 0 else 0
    return dict(ret=r3(eq.iloc[-1] - 1), bh=r3(bh.iloc[-1] - 1), mdd=r3(mdd(eq)), bh_mdd=r3(mdd(bh)), sharpe=r3(sharpe(strat)), bh_sharpe=r3(sharpe(r_)),
                trades=int(trades.sum()), inmkt=r3(sig.mean()))
R['ma'] = {}
for c in ['AMZN', 'BTC', 'NFLX', 'DPZ']:
    R['ma'][c] = {f'{s_}-{l_}': ma_bt(p[c].values, s_, l_) for s_, l_ in [(5, 20), (10, 50), (20, 60), (20, 120), (50, 200)]}
R['duel13'] = dict(BTC=R['ma']['BTC']['20-60'], AMZN=R['ma']['AMZN']['20-60'])
# 위험성향별 배분 (주식 = AMZN·NFLX·DPZ 동일가중, 안전자산 연 2% 가정)
eq_r = ret[['AMZN', 'DPZ', 'NFLX']].mean(axis=1)
alloc = []
for w in [0, .2, .4, .6, .8, 1.0]:
    rr_ = w * eq_r + (1 - w) * (0.02 / 252)
    e = (1 + rr_).cumprod()
    alloc.append(dict(w=w, mu=r3(rr_.mean() * 252), vol=r3(rr_.std() * np.sqrt(252)), mdd=r3(float((e / e.cummax() - 1).min())), worst_day=r3(rr_.min())))
R['alloc'] = alloc

# ---------------- 14회차: 데이터 품질 (실제 원자료의 문제) ----------------
r4 = pd.read_csv(D('Revolution4', 'bank_customers.csv'), header=None)
r4b = pd.read_csv(D('Revolution4', 'direct_marketimg.csv'), header=None)
import hashlib
h = lambda f: hashlib.md5(open(f, 'rb').read()).hexdigest()
R['quality'] = dict(r4_rows=len(r4), r4_header_missing=True, r4_same_file=h(D('Revolution4', 'bank_customers.csv')) == h(D('Revolution4', 'direct_marketimg.csv')),
                    r4_vs_r1_rows=[len(r4), len(b)],
                    travel_gender_missing=int(t.Gender.isna().sum()), travel_rows=len(t), travel_dur_neg=int((t.Duration < 0).sum()), travel_age_118=int((t.Age > 100).sum()),
                    travel_sales_neg=int((t['Net Sales'] < 0).sum()),
                    bank_unknown=R['bank']['unknown'], bank_n=len(b),
                    intl_missing=R['intl']['missing'], intl_rows=R['intl']['rows'],
                    dm_hist_missing=int(dm.History.isna().sum()), dm_rows=len(dm),
                    ins_dup=int(ins[['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']].duplicated().sum()))
# 감성 데이터 중복 문장
sent = pd.read_csv(D('Revolution6', 'Financial_Sentiment_Analysis.csv'))
R['quality']['sent_rows'] = len(sent); R['quality']['sent_dup'] = int(sent.Sentence.duplicated().sum())
R['quality']['sent_conflict'] = int(sent.groupby('Sentence').Sentiment.nunique().gt(1).sum())

# ---------------- 3회차: 대출 데이터 사전 ----------------
ld = pd.read_csv(D('Revolution4', 'loan_data_description.csv'))
R['loan_dict'] = [[str(a).strip(), str(c)[:140]] for a, c in zip(ld.LoanStatNew, ld.Description) if isinstance(a, str) and a.strip()]


# ---------------- 추가: 3회차 수집 주기 대결, 14회차 비식별 대결, SVM 균형 가중 ----------------
def stale(series, gap):
    x = np.asarray(series, float); est = np.array([x[(i // gap) * gap - 1] if (i // gap) * gap >= 1 else x[0] for i in range(len(x))])
    m = np.arange(len(x)) >= gap
    return r3(np.mean(np.abs(x[m] - est[m]) / x[m]))
R['duel03'] = {c: dict(daily=stale(p[c].values, 1), weekly=stale(p[c].values, 5), monthly=stale(p[c].values, 21), quarterly=stale(p[c].values, 63)) for c in ['AMZN', 'BTC', 'NFLX', 'DPZ']}
def gen_r2(w, reg, ch):
    d = ins.copy(); d['ab'] = (d.age // w) * w + w / 2
    cols = ['ab', 'male', 'bmi', 'sm'] + (['children'] if ch else [])
    X = pd.get_dummies(d[cols + (['region'] if reg else [])], drop_first=True).astype(float)
    tr_, te_ = train_test_split(np.arange(len(d)), test_size=.25, random_state=rs)
    return r3(LinearRegression().fit(X.iloc[tr_], d.charges.iloc[tr_]).score(X.iloc[te_], d.charges.iloc[te_]))
R['duel14'] = dict(fly=dict(w=5, reg=0, ch=1, r2=gen_r2(5, 0, 1)), robo=dict(w=20, reg=0, ch=0, r2=gen_r2(20, 0, 0)), raw_r2=gen_r2(1, 1, 1))
for k_ in R['kanon']:
    if (k_['w'], k_['reg'], k_['ch']) == (5, 0, 1): R['duel14']['fly'].update(k_)
    if (k_['w'], k_['reg'], k_['ch']) == (20, 0, 0): R['duel14']['robo'].update(k_)
Xtr, Xte, ytr, yte = train_test_split(X2, yb, test_size=.25, random_state=rs, stratify=yb)
sc = StandardScaler().fit(Xtr)
sv = SVC(kernel='linear', C=1, class_weight='balanced').fit(sc.transform(Xtr), ytr)
pv = sv.predict(sc.transform(Xte))
R['svm_bal'] = dict(acc=r3(accuracy_score(yte, pv)), rec=r3(recall_score(yte, pv)), w=sv.coef_[0].tolist(), b=float(sv.intercept_[0]), nsv=int(sv.n_support_.sum()))
sv2 = SVC(kernel='rbf', C=1, class_weight='balanced').fit(sc.transform(Xtr), ytr); pv2 = sv2.predict(sc.transform(Xte))
R['svm_bal']['rbf_acc'] = r3(accuracy_score(yte, pv2)); R['svm_bal']['rbf_rec'] = r3(recall_score(yte, pv2))
svr = SVC(kernel='rbf', C=1, class_weight='balanced').fit(Xtr, ytr); pr_ = svr.predict(Xte)
R['svm_bal']['raw_acc'] = r3(accuracy_score(yte, pr_)); R['svm_bal']['raw_rec'] = r3(recall_score(yte, pr_))
R['duel06'] = dict(raw=R['knn']['svm_raw'], std=R['knn']['svm_rbf'], raw_rec=r3(recall_score(yte, svm_raw.predict(Xte))), std_rec=r3(recall_score(yte, svm_rbf.predict(sc.transform(Xte)))))
print('duel03', R['duel03']); print('duel14', R['duel14']); print('svm_bal', R['svm_bal']); print('duel06', R['duel06'])

R['amt'] = [r3(v) for v in b.Total_Trans_Amt.sample(1500, random_state=1).values]
R['rows5'] = [[int(r.CLIENTNUM), int(r.Total_Trans_Ct), int(r.Total_Trans_Amt), int(r.y)] for r in pd.concat([b[b.y == 0].sample(4, random_state=4), b[b.y == 1].sample(1, random_state=4)]).itertuples()]
R['knn']['pos_te'] = int(Xte.shape[0] and yte.sum())

json.dump(R, open(os.path.join(os.path.dirname(__file__), 'results.json'), 'w', encoding='utf-8'), ensure_ascii=False)
# 요약 출력
show = {k: R[k] for k in ['duel01', 'duel04', 'duel05', 'duel06', 'duel07', 'duel09', 'duel10', 'duel11', 'duel12', 'duel13', 'phish', 'knn', 'cv', 'fe', 'dm', 'tree', 'logit', 'bankrupt', 'ar_dir', 'alloc', 'quality', 'outlier', 'order_split', 'kanon', 'travel']}
for k, v in show.items():
    s_ = json.dumps(v, ensure_ascii=False)
    if k == 'travel': v = {kk: vv for kk, vv in v.items() if kk not in ('roc',)}; s_ = json.dumps(v, ensure_ascii=False)
    if k == 'tree': s_ = json.dumps({kk: vv for kk, vv in v.items() if kk not in ('leaves', 'sample')}, ensure_ascii=False)
    print(k, s_[:1500])
