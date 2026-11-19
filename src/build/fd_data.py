"""analysis/results.json → 페이지에 넣을 FD(실제 데이터 표본·계산 결과) 객체."""
import json, os
B = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(os.path.dirname(B), 'analysis', 'results.json'), encoding='utf-8'))

KO = {'Customer_Age': ('나이', '인구통계', '나이만으로는 이탈을 거의 가를 수 없어요.'),
      'Gender': ('성별', '인구통계', '성별 차이는 작아요.'),
      'Dependent_count': ('부양가족 수', '인구통계', '부양가족 수에 따른 차이도 작아요.'),
      'Education_Level': ('학력', '인구통계', '"Unknown"(모름)이 1,519명 있어요. 빈칸 대신 글자로 들어간 숨은 결측입니다.'),
      'Marital_Status': ('결혼 여부', '인구통계', '"Unknown" 749명이 있어요.'),
      'Income_Category': ('소득 구간', '인구통계', '숫자처럼 보이지만 "$40K - $60K" 같은 글자 범주예요. "Unknown" 1,112명.'),
      'Card_Category': ('카드 등급', '상품', 'Blue 등급이 93%라 한쪽으로 크게 치우친 열이에요.'),
      'Months_on_book': ('거래 기간(개월)', '관계', '오래된 고객이라고 덜 떠나지는 않았어요.'),
      'Total_Relationship_Count': ('보유 상품 수', '관계', '상품을 적게 가진 고객이 더 많이 떠나요. 교차 판매가 이탈을 막는 이유예요.'),
      'Months_Inactive_12_mon': ('최근 1년 비활동 개월', '행동', '쉬는 달이 많을수록 이탈 위험이 커요.'),
      'Contacts_Count_12_mon': ('최근 1년 상담 횟수', '행동', '상담을 자주 한 고객이 오히려 더 떠나요. 불만의 신호일 수 있어요.'),
      'Credit_Limit': ('신용 한도', '상품', '한도가 가장 낮은 구간만 이탈률이 높고, 나머지 구간은 고르게 비슷해요.'),
      'Total_Revolving_Bal': ('회전 잔액', '행동', '잔액이 거의 없는(카드를 안 쓰는) 고객의 이탈률이 높아요.'),
      'Total_Trans_Amt': ('연간 거래 금액', '행동', '거래 금액 구간에 따라 이탈률이 크게 달라요. 행동 데이터의 힘입니다.'),
      'Total_Trans_Ct': ('연간 거래 횟수', '행동', '거래 횟수가 적은 고객은 이탈률이 매우 높아요. 가장 강한 단서 중 하나입니다.'),
      'Avg_Utilization_Ratio': ('평균 한도 사용률', '행동', '한도를 거의 안 쓰는 고객이 더 떠나요.')}

def fd():
    b = R['bank']
    cols = []
    for c in b['cols']:
        ko, grp, note = KO[c['c']]
        rate = [[str(a).replace('-0.00', '0').replace('-0~', '0~').replace('.00', ''), v] for a, v in c['rate']]
        d = dict(c=c['c'], ko=ko, group=grp, note=note, kind=c['kind'], rate=rate)
        if c['kind'] == 'num': d['mean'] = c['mean']
        else: d['top'] = c['top']
        cols.append(d)
    ins = R['ins']
    return dict(
        bank=dict(n=b['n'], attr=b['attr'], rate=round(b['attr'] / b['n'], 4)), bankcols=cols,
        ins=dict(n=ins['n'], uniq=ins['uniq'], ch=ins['charges_sample'], skew=ins['skew']),
        loan_dict=R['loan_dict'], knn={k: R['knn'][k] for k in ['std', 'raw', 'mu', 'sd', 'base', 'ntr', 'nte', 'svm_lin', 'svm_rbf', 'svm_raw', 'pos_te']},
        knn_s=R['knn_sample'], amt=R['amt'], out=R['outlier'], rows5=R['rows5'],
        travel={k: R['travel'][k] for k in ['cms', 'roc', 'auc', 'nte', 'pos_te', 'rate']}, cv=R['cv'],
        dm={k: R['dm'][k] for k in ['lin_coef', 'lin_b0', 'knn_r2', 'lin_r2']}, dm_s=R['dm']['sample'],
        ins_s=dict(age=R['ins_scatter']['age'], ch=R['ins_scatter']['ch'], sm=R['ins_scatter']['sm']),
        logit=R['logit'], tree={k: R['tree'][k] for k in ['leaves', 'depth', 'root', 'sample']}, fe=R['fe'],
        port={k: R['port'][k] for k in ['AMZN', 'DPZ', 'BTC', 'NFLX', 'dates', 'corr', 'mu', 'start', 'end']},
        intl={k: R['intl'][k] for k in ['corr', 'names', 'missing', 'n']}, ar=R['ar'], ar_dir=R['ar_dir'], alloc=R['alloc'], kanon=R['kanon'], quality=R['quality'],
        d=dict(duel01=R['duel01'], phish=R['phish'], duel03=R['duel03'], duel04=R['duel04'], duel05=R['duel05'], duel06=R['duel06'], duel07=R['duel07'],
               duel09=R['duel09'], fe=R['fe'], duel11=R['duel11'], duel12=R['duel12'], duel13=R['duel13'], duel14=R['duel14']))

def fd_json():
    return json.dumps(fd(), ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
