# 실습 데이터 (fintech-data 복사본)

출처: https://github.com/fintech-data (Revolution, Revolution2 ~ Revolution6). 원 저장소의 README는 각 폴더의 `README_original.md`로 함께 복사했습니다. 원 데이터의 1차 출처(Kaggle 등)와 이용 조건은 원 저장소를 따릅니다.

| 폴더 | 파일 | 쓰는 회차 |
|---|---|---|
| Revolution | Bank_customers_data.csv · insurance.csv · travel insurance.csv · DirectMarketing.csv | 1·2·4~7·9·10·12·14 |
| Revolution2 | Website Phishing.csv · insurance_claims.csv (insurance.csv · travel insurance.csv는 Revolution과 같음) | 2 |
| Revolution3 | portfolio_data.csv · new_portfolio_data.csv · international_portfolio_data.csv | 3·11~13 |
| Revolution4 | loan_data_description.csv · bank_customers.csv · direct_marketimg.csv · travel insurance.csv | 3·14 |
| Revolution5 | company_bankruptcy.csv | 10 |
| Revolution6 | Financial_Sentiment_Analysis.csv · text_similarity_*.csv · ratings_small.csv | 14 |

## 복사하지 않은 파일
Git LFS로 올라가 있는 대용량 파일(Revolution4·5의 `loan.csv`, Revolution6의 `News_Fake_and_Real_*.csv`, `movies_metadata.csv`, `netflix_list.csv`)은 이 저장소에 넣지 않았습니다. 필요하면 원 저장소에서 받으세요.

## 알려진 품질 문제 (14회차에서 진단)
- Revolution4의 `bank_customers.csv`와 `direct_marketimg.csv`는 바이트까지 같은 파일이며 열 이름 줄이 없습니다(내용은 Revolution의 은행 고객 데이터).
- 여행자 보험: 성별 결측 71%, 나이 118세 984건, 여행 기간 음수 5건, 순매출 음수 678건.
- 감성 데이터: 중복 문장 520개, 같은 문장에 다른 라벨 514개.
- 국제 지표: 나라별 휴일 차이로 다우·VIX 결측 645행.

모든 숫자는 `src/analysis/compute.py`로 다시 계산할 수 있습니다.
