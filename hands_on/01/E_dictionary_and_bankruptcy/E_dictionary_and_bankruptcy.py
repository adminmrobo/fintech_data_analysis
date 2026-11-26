# -*- coding: utf-8 -*-
# E_dictionary_and_bankruptcy.py — 실행판 노트북을 파이썬 파일 하나로 옮긴 풀버전
# 실행: python E_dictionary_and_bankruptcy.py  (이 폴더 안에서는 data/를, 밖에서는 GitHub의 데이터를 읽어요)
# Colab: %run E_dictionary_and_bankruptcy.py

# # 코드 E · 변수 사전 붙여 읽기와 기업 부도 데이터
# **핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01**  
# 원본: [fintech-data/Revolution5](https://github.com/fintech-data/Revolution5) `Loading_Data.ipynb` → 이 폴더의 `original_Loading_Data.ipynb`  
# 해설 페이지: https://adminmrobo.github.io/fintech_data_analysis/hands_on_01.html
#
# > 코드를 몰라도 괜찮아요. 위에서부터 ▶ 실행 버튼만 차례로 누르면 됩니다.

# ## 이 코드가 하는 일
# ① 대출 장부의 74개 열 이름 옆에 **뜻풀이 사전**(`loan_data_description.csv`)을 붙여 한 줄씩 출력하는 작은 함수를 만들고, ② 대만 기업 6,819곳의 재무비율 95개와 부도 여부를 담은 **기업 부도 데이터**를 엽니다.
#
# > 비유: 외국어 메뉴판 옆에 번역 쪽지를 붙여 읽는 일, 그리고 회사 건강검진표 6,819장 넘겨보기.

import os, io, urllib.request
import pandas as pd
pd.set_option('display.max_columns', 12); pd.set_option('display.width', 120)

# 데이터 위치: 이 폴더의 data/ 에 있으면 그걸 쓰고, 없으면(Colab 등) GitHub에서 바로 읽습니다.
RAW = 'https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/hands_on/01/E_dictionary_and_bankruptcy/data/'
def load(name, **kw):
    local = os.path.join('data', name)
    src = local if os.path.exists(local) else RAW + urllib.parse.quote(name)
    return pd.read_csv(src, low_memory=False, **kw)
print('준비 완료')

# loan.csv(441MB)는 GitHub 한 파일 한도 때문에 gzip으로 줄인 뒤 세 조각(part0~2)으로 나눠 두었습니다.
# 조각을 이어 붙이면 원래 파일과 똑같습니다.
def load_loan(folder='E_dictionary_and_bankruptcy', **kw):
    parts = []
    for i in range(3):
        local = os.path.join("../D_loan_ledger_check/data", f'loan.csv.gz.part{i}')
        if os.path.exists(local):
            parts.append(open(local, 'rb').read())
        else:
            parts.append(urllib.request.urlopen('https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/hands_on/01/D_loan_ledger_check/data/' + f'loan.csv.gz.part{i}').read())
    return pd.read_csv(io.BytesIO(b''.join(parts)), compression='gzip', low_memory=False, **kw)

loan = load_loan(usecols=None)
loan_status = load('loan_data_description.csv')
print(loan.shape, loan_status.shape)

def description(column_name):
    # 열 이름을 사전에서 찾아 뜻을 돌려줍니다
    return loan_status.loc[loan_status.LoanStatNew == column_name].Description.values[0]

def print_description(column_list):
    missing = []
    for column in column_list:
        try:
            print(f'- {column} = {description(column)}')
        except Exception:
            missing.append(column)
    print('\n사전에 없는 열:', missing)

print(print_description(loan.columns[:10]))

print(print_description(loan.columns))

bankruptcy = load('company_bankruptcy.csv')
print(bankruptcy.shape)
print(bankruptcy['Bankrupt?'].value_counts())

# 열 이름 앞에 빈 값(공백)이 숨어 있어요
print(repr(bankruptcy.columns[1]))
bankruptcy.columns = bankruptcy.columns.str.strip()
print(repr(bankruptcy.columns[1]))

# 부도 기업 비율
print(round(bankruptcy['Bankrupt?'].mean() * 100, 1), '%')
print(bankruptcy.groupby('Bankrupt?')[['Debt ratio %', 'Net worth/Assets']].mean().round(3))

