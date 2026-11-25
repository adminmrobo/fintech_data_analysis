# 핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01

> 해설 페이지: https://adminmrobo.github.io/fintech_data_analysis/hands_on_01.html

[fintech-data](https://github.com/fintech-data)의 실습 저장소 6개(Revolution ~ Revolution6)를 **그대로 복사(포크)**해 이 폴더에 모았습니다. 저장소 이름이 번호뿐이라 무엇인지 알기 어려워서, **코드가 하는 일에 맞는 이름(코드 A~F)**을 붙였습니다.

해설 페이지에서는 연구실 식구들이 두 팀으로 나뉘어 코드 하나씩 발표합니다.
- 초파리 팀: 초파리 연구원(조장) · 시아(인턴1) · 하루(조수) · X2
- 주판봇 팀: 주판봇(조장) · 모아(인턴2) · X1 · X3
- 심판: 박사

## 코드 이름표

| 새 이름 | 하는 일 | 원래 저장소 | 발표 형식 |
|---|---|---|---|
| [A_customer_data_tour](A_customer_data_tour/) | 고객 데이터 4종 둘러보기 (은행 고객·쇼핑몰 마케팅·건강보험료·여행자보험) | [fintech-data/Revolution](https://github.com/fintech-data/Revolution) | 초파리 팀 조별 발표 |
| [B_fraud_phishing_check](B_fraud_phishing_check/) | 보험사기·피싱 탐지 데이터 점검 | [fintech-data/Revolution2](https://github.com/fintech-data/Revolution2) | X1 개인 발표 |
| [C_portfolio_price_diary](C_portfolio_price_diary/) | 주가 일기장 — 포트폴리오 시계열 읽기 | [fintech-data/Revolution3](https://github.com/fintech-data/Revolution3) | 시각화 조별 대결 |
| [D_loan_ledger_check](D_loan_ledger_check/) | 대출 장부와 고객 명부 크기 재기 | [fintech-data/Revolution4](https://github.com/fintech-data/Revolution4) | 상담 (모아 → 박사) |
| [E_dictionary_and_bankruptcy](E_dictionary_and_bankruptcy/) | 변수 사전 붙여 읽기와 기업 부도 데이터 | [fintech-data/Revolution5](https://github.com/fintech-data/Revolution5) | 하루 개인 발표 |
| [F_text_and_ratings](F_text_and_ratings/) | 문장·뉴스·평점 — 글자로 된 금융 데이터 | [fintech-data/Revolution6](https://github.com/fintech-data/Revolution6) | 조별 발표 + 반론 |

## 폴더마다 들어 있는 것

| 파일 | 내용 |
|---|---|
| `original_Loading_Data.ipynb` | 원본 노트북 (손대지 않음) |
| `README_original.md` | 원본 저장소의 설명 (열 이름과 뜻) |
| `data/` | 원본 데이터 복사본 |
| `<폴더 이름>.ipynb` | **실행판 노트북** — 원본과 같은 일을 하면서 한국어 설명과 확인 셀(줄 수·빈 값·비율·차트)을 더하고, 실행 결과까지 저장한 판 |

실행판 노트북은 이 폴더의 `data/`가 있으면 그것을, 없으면(Colab) GitHub에서 데이터를 바로 읽습니다. Colab에서 열기:

- [A](https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/A_customer_data_tour/A_customer_data_tour.ipynb) · [B](https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/B_fraud_phishing_check/B_fraud_phishing_check.ipynb) · [C](https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/C_portfolio_price_diary/C_portfolio_price_diary.ipynb) · [D](https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/D_loan_ledger_check/D_loan_ledger_check.ipynb) · [E](https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/E_dictionary_and_bankruptcy/E_dictionary_and_bankruptcy.ipynb) · [F](https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/hands_on/01/F_text_and_ratings/F_text_and_ratings.ipynb)

## 코드별 요약 (실행 결과 기준)

### A · 고객 데이터 4종 둘러보기
- **하는 일:** CSV 4개를 읽어 앞뒤 몇 줄을 봅니다.
- **데이터:** 은행 고객 10,127 × 21 · 쇼핑몰 마케팅 1,000 × 10 · 건강보험료 1,338 × 7 · 여행자보험 63,326 × 11
- **실행 결과:** 떠난 고객 1,627명(16.1%) · 흡연자 평균 의료비 약 3.8배 · 여행자보험 성별 빈 값 45,107줄 · 118세 고객 984명(임시 숫자 의심)

### B · 보험사기·피싱 탐지 데이터 점검
- **하는 일:** 표 4개를 읽고 `info()`로 빈 값과 자료형을 봅니다.
- **데이터:** 피싱 사이트 1,353 × 10 · 자동차 보험 청구 1,000 × 39 (+ A와 같은 표 2개)
- **실행 결과:** 허위 청구 247건(24.7%) · NaN 91개 외에 `"?"`로 숨은 빈 값 881개 · 큰 파손 사고의 허위 비율 60.5%
- **원본과 다른 점:** 원본은 여행자보험 표를 `insurance_claim`에 덮어씀 → 실행판은 `travel_insurance`

### C · 주가 일기장 — 포트폴리오 시계열 읽기
- **하는 일:** 날짜별 종가 표 2개(+ 원본이 읽지 않은 1개)를 읽습니다.
- **데이터:** 미국 4종목 1,520일(2013-05-01~2019-05-14) · 한·미 지표 2,070일 × 18 · 새 포트폴리오 2,468일
- **실행 결과:** 처음 대비 아마존 7.4배 · 넷플릭스 11.4배 · 도미노피자 5.3배 · 비트코인 77배 / 하루 흔들림(표준편차) 비트코인 10.46%, 아마존 1.90% · 국제 지표의 코스피·금·달러가 쉼표 때문에 글자로 읽힘

### D · 대출 장부와 고객 명부 크기 재기
- **하는 일:** 대출 장부(441MB)를 읽어 `shape`와 `info()`를 봅니다.
- **데이터:** 대출 887,379 × 74 · `bank_customers.csv`와 `direct_marketimg.csv`(둘 다 10,127 × 21)
- **실행 결과:** 부실 처리 45,248건(5.1%) · 등급 A 금리 7.24% → G 25.63% · 90% 넘게 빈 열 17개 · **두 CSV는 내용이 똑같고 열 이름 줄이 없음** (`header=None`으로 읽어야 함)

### E · 변수 사전 붙여 읽기와 기업 부도 데이터
- **하는 일:** 열 이름 옆에 뜻을 붙여 출력하는 함수 `print_description()`을 만들고, 기업 부도 데이터를 읽습니다.
- **데이터:** 변수 사전 80 × 3 · 기업 부도 6,819 × 96
- **실행 결과:** 74개 열 중 71개 뜻 찾음(3개 사전에 없음) · 부도 220곳(3.2%) → "전부 정상"이라고만 해도 정확도 96.8% · 열 이름 95개 앞에 공백

### F · 문장·뉴스·평점 — 글자로 된 금융 데이터
- **하는 일:** 감성 문장·가짜/진짜 뉴스·종목 이름 유사도·영화 평점·넷플릭스 목록을 읽습니다.
- **데이터:** 감성 5,842 × 2 · 가짜 뉴스 23,481 / 진짜 뉴스 21,417 · 유사도 학습용 2,142 / 시험용 516 · 평점 100,004 · 넷플릭스 7,008 × 19
- **실행 결과:** 중립 3,130 / 긍정 1,852 / 부정 860, 중복 문장 520 · 가짜·진짜 뉴스의 분류(subject) 이름이 하나도 안 겹침(데이터 누수 위험) · 평점은 671명 × 9,066편 중 1.64%만 채워짐

## 큰 파일 처리

원본 저장소의 큰 파일은 Git LFS로만 받을 수 있어, 여기서는 gzip으로 줄였습니다. 내용은 원본과 같습니다.

| 원본 | 이 폴더 | 메모 |
|---|---|---|
| Revolution4·5 `loan.csv` (441MB) | `D_loan_ledger_check/data/loan.csv.gz.part0~2` | gzip 103MB를 40MB씩 세 조각. 실행판의 `load_loan()`이 이어 붙여 읽음. 직접 합치려면 `cat loan.csv.gz.part* > loan.csv.gz` |
| Revolution6 `News_Fake_and_Real_Fake.csv`, `…True.csv` | `F_text_and_ratings/data/*.csv.gz` | pandas가 `.gz`를 그대로 읽음 |
| Revolution6 `netflix_list.csv`, `movies_metadata.csv` | `F_text_and_ratings/data/*.csv.gz` | `movies_metadata`는 원본 노트북에서 쓰지 않지만 함께 보관 |

## 다시 만들기

```bash
cd hands_on/01 && python3 tools/make_notebooks.py        # 실행판 노트북 6개 생성·실행
cd ../../src && python3 hands_on/h01_build.py ..          # 해설 페이지 hands_on_01.html
```

데이터의 원 출처(Kaggle 공개 데이터 등)와 라이선스는 각 폴더의 `README_original.md`와 원본 저장소를 따릅니다. 이 페이지의 숫자는 교육용이며 투자·금융 권유가 아닙니다.

글 · 안상선 ([www.ahnboat.xyz](https://www.ahnboat.xyz)) · (주)M-Robo 대표
