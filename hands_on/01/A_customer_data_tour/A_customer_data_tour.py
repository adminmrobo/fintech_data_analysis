# -*- coding: utf-8 -*-
# A_customer_data_tour.py — 실행판 노트북을 파이썬 파일 하나로 옮긴 풀버전
# 실행: python A_customer_data_tour.py  (이 폴더 안에서는 data/를, 밖에서는 GitHub의 데이터를 읽어요)
# Colab: %run A_customer_data_tour.py

# # 코드 A · 고객 데이터 4종 둘러보기
# **핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01**  
# 원본: [fintech-data/Revolution](https://github.com/fintech-data/Revolution) `Loading_Data.ipynb` → 이 폴더의 `original_Loading_Data.ipynb`  
# 해설 페이지: https://adminmrobo.github.io/fintech_data_analysis/hands_on_01.html
#
# > 코드를 몰라도 괜찮아요. 위에서부터 ▶ 실행 버튼만 차례로 누르면 됩니다.

# ## 이 코드가 하는 일
# 은행 고객 명부, 쇼핑몰 마케팅 명부, 건강보험료 표, 여행자보험 판매 장부 — **표 네 권을 차례로 펼쳐서 첫 장만 훑어보는** 코드입니다.
#
# > 비유: 새 학기에 받은 반 명부 네 권을 책상에 펼쳐 놓고 "몇 명이지? 어떤 항목이 적혀 있지?"를 확인하는 일.
#
# 원본 노트북은 `original_Loading_Data.ipynb`에 그대로 있습니다. 이 노트북은 같은 일을 하면서 결과를 한 줄씩 설명합니다.

import os, io, urllib.request
import pandas as pd
pd.set_option('display.max_columns', 12); pd.set_option('display.width', 120)

# 데이터 위치: 이 폴더의 data/ 에 있으면 그걸 쓰고, 없으면(Colab 등) GitHub에서 바로 읽습니다.
RAW = 'https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/hands_on/01/A_customer_data_tour/data/'
def load(name, **kw):
    local = os.path.join('data', name)
    src = local if os.path.exists(local) else RAW + urllib.parse.quote(name)
    return pd.read_csv(src, low_memory=False, **kw)
print('준비 완료')

# ### ① 은행 고객 명부 (Bank_customers_data.csv)
# 고객 한 명이 한 줄(행)입니다. `Attrition_Flag`는 고객이 떠났는지(Attrited) 남았는지(Existing)를 적은 열이에요.

bank_customers = load('Bank_customers_data.csv')
print(bank_customers.head())

print('행(고객 수), 열(항목 수):', bank_customers.shape)
print(bank_customers['Attrition_Flag'].value_counts())

# 떠난 고객과 남은 고객의 1년 거래 횟수 평균
print(bank_customers.groupby('Attrition_Flag')['Total_Trans_Ct'].mean().round(1))

# ### ② 다이렉트 마케팅 명부 (DirectMarketing.csv)
# 쇼핑몰 고객 1,000명. 마지막 열 `AmountSpent`(1년 이용액)를 맞히는 데 쓰는 데이터입니다.

direct_marketing = load('DirectMarketing.csv')
print(direct_marketing.head())

# 빈 값(결측값) 세기 — History 열에 빈 값이 많아요
print(direct_marketing.isna().sum())

# ### ③ 건강보험료 표 (insurance.csv)

insurance = load('insurance.csv')
print(insurance.shape)
print(insurance.groupby('smoker')['charges'].mean().round(0))

# ### ④ 여행자보험 판매 장부 (travel insurance.csv)

travel_insurance = load('travel insurance.csv')
print(travel_insurance.shape)
print(travel_insurance['Claim'].value_counts())

# 이상한 값 찾기: 성별 빈 값 수, 가장 많은 나이, 음수 보험기간
print('Gender 빈 값:', travel_insurance['Gender'].isna().sum())
print('Age 최댓값:', travel_insurance['Age'].max(), '/ 118세 행 수:', (travel_insurance['Age'] >= 118).sum())
print('Duration이 음수인 행:', (travel_insurance['Duration'] < 0).sum())

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
bank_customers['Attrition_Flag'].value_counts().plot.bar(ax=ax[0], color=['#5b8def', '#e8833a'], rot=0, title='Bank customers')
insurance.groupby('smoker')['charges'].mean().plot.bar(ax=ax[1], color=['#5b8def', '#e8833a'], rot=0, title='Mean insurance charge by smoker')
plt.tight_layout(); plt.show() if "inline" in plt.get_backend() or "ipykernel" in plt.get_backend() else plt.close("all")

