# -*- coding: utf-8 -*-
# C_portfolio_price_diary.py — 실행판 노트북을 파이썬 파일 하나로 옮긴 풀버전
# 실행: python C_portfolio_price_diary.py  (이 폴더 안에서는 data/를, 밖에서는 GitHub의 데이터를 읽어요)
# Colab: %run C_portfolio_price_diary.py

# # 코드 C · 주가 일기장 — 포트폴리오 시계열 읽기
# **핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01**  
# 원본: [fintech-data/Revolution3](https://github.com/fintech-data/Revolution3) `Loading_Data.ipynb` → 이 폴더의 `original_Loading_Data.ipynb`  
# 해설 페이지: https://adminmrobo.github.io/fintech_data_analysis/hands_on_01.html
#
# > 코드를 몰라도 괜찮아요. 위에서부터 ▶ 실행 버튼만 차례로 누르면 됩니다.

# ## 이 코드가 하는 일
# 날짜별 종가(그날 마지막 가격)를 적은 **주가 일기장** 두 권(미국 4종목, 한·미 국제 지표)을 불러옵니다. 원본에 없던 세 번째 일기장(`new_portfolio_data.csv`)도 함께 열어 봅니다.
#
# > 비유: 매일 저녁 몸무게를 적은 다이어리. 한 줄이 하루입니다.

import os, io, urllib.request
import pandas as pd
pd.set_option('display.max_columns', 12); pd.set_option('display.width', 120)

# 데이터 위치: 이 폴더의 data/ 에 있으면 그걸 쓰고, 없으면(Colab 등) GitHub에서 바로 읽습니다.
RAW = 'https://raw.githubusercontent.com/adminmrobo/fintech_data_analysis/main/hands_on/01/C_portfolio_price_diary/data/'
def load(name, **kw):
    local = os.path.join('data', name)
    src = local if os.path.exists(local) else RAW + urllib.parse.quote(name)
    return pd.read_csv(src, low_memory=False, **kw)
print('준비 완료')

portfolio_data = load('portfolio_data.csv')
print(portfolio_data.shape, portfolio_data['Date'].iloc[0], '→', portfolio_data['Date'].iloc[-1])
print(portfolio_data.head())

prices = portfolio_data.set_index(pd.to_datetime(portfolio_data['Date']))[['AMZN', 'DPZ', 'BTC', 'NFLX']]
print('처음 대비 마지막 값(배):'); print((prices.iloc[-1] / prices.iloc[0]).round(1))
print('하루 수익률의 표준편차(%) — 흔들림의 크기:'); print((prices.pct_change().std() * 100).round(2))

import matplotlib.pyplot as plt
(prices / prices.iloc[0] * 100).plot(logy=True, figsize=(8, 3.2), title='Start = 100 (log scale)'); plt.tight_layout(); plt.show() if "inline" in plt.get_backend() or "ipykernel" in plt.get_backend() else plt.close("all")

international_portfolio_data = load('international_portfolio_data.csv', index_col=0)
print(international_portfolio_data.info())

# 숫자여야 할 열이 글자(object)로 읽혔어요 — '2,326.17'처럼 쉼표가 들어 있기 때문
ip = international_portfolio_data.copy()
for c in ['kospi', 'gold', 'dol', 'VIX1']:
    ip[c] = pd.to_numeric(ip[c].astype(str).str.replace(',', ''), errors='coerce')
print(ip[['kospi', 'gold', 'dol']].describe().round(1))

# 빈 값이 많은 이유: 주말·휴장일에는 주식시장 값이 없고 코인 값만 있어요
ip['요일'] = pd.to_datetime(ip['real_date']).dt.day_name()
print(ip.groupby('요일')['kospi'].apply(lambda s: s.isna().mean()).round(2))

new_portfolio_data = load('new_portfolio_data.csv')
print(new_portfolio_data.shape, new_portfolio_data['Date'].iloc[0], '→', new_portfolio_data['Date'].iloc[-1])

