TITLES = {1: '핀테크 산업의 이해와 핀테크 데이터', 2: '핀테크 데이터 수집 기술', 3: '데이터 분석을 위한 준비', 4: '데이터 분석 개념의 이해',
          5: '데이터 분석 모형 : 분류모형(1)', 6: '데이터 분석 실습', 7: '데이터 분석 모델의 평가', 8: '데이터 분석 모형 : 회귀모형(1)',
          9: '데이터 분석 모형 : 회귀모형(2)', 10: '딥러닝 모델과 시계열 데이터 분석', 11: '핀테크 데이터 시각화', 12: '데이터 기반의 핀테크 서비스 기획',
          13: '데이터 보안 및 품질 관리'}
def REF0(n, t=None):
    """n = 원 교안 회차 번호(1~13)."""
    t = t or TITLES[n]
    return {'id': f'ahn2024fintech{n:02d}', 'type': 'manuscript', 'title': f'핀테크 데이터 분석 기초 {n}회차: {t} (강의 원고)', 'author': [{'family': '안', 'given': '상선'}], 'issued': {'date-parts': [[2024]]},
            'lab': {'work': f'lab:work/ahn2024fintech{n:02d}', 'role': 'primary', 'verified': {'title': True, 'authors': True, 'year': True, 'venue': False}, 'checkedBy': '원고 PPTX 버전 정보(v.1.0~1.1, 2024)', 'note': '온라인 강의 원고(스토리보드). NCS 핀테크 데이터 분석(2001010802_19v2) 매칭'}}
def DATA_REF():
    return {'id': 'fintechdata', 'type': 'dataset', 'title': 'fintech-data: Revolution~Revolution6 실습 데이터 저장소', 'author': [{'literal': 'fintech-data'}], 'issued': {'date-parts': [[2021]]}, 'URL': 'https://github.com/fintech-data',
            'lab': {'work': 'lab:work/fintechdata', 'role': 'data', 'verified': {'title': True, 'authors': False, 'year': False, 'venue': False}, 'checkedBy': 'GitHub 저장소 README', 'note': '이 시리즈 data/ 폴더로 복사해 사용. 원 출처(Kaggle 등)는 각 README 참조'}}
def REF(id, typ, title, authors, year, venue='', role='background', note='', url=''):
    r = {'id': id, 'type': typ, 'title': title, 'author': authors, 'issued': {'date-parts': [[year]]}, 'lab': {'work': f'lab:work/{id}', 'role': role, 'verified': {'title': False, 'authors': False, 'year': False, 'venue': False, 'doi': False}, 'checkedBy': '미확인 — 원문 대조 필요', 'note': note}}
    if venue: r['container-title'] = venue
    if url: r['URL'] = url
    return r
def SRC0(n, t=None):
    return f'안상선 (2024). 핀테크 데이터 분석 기초 {n}회차 「{t or TITLES[n]}」 강의 원고 v1.1. 이 페이지의 주 자료.'
DATA_SRC = '실습 데이터: fintech-data (GitHub, Revolution~Revolution6) — 이 저장소 data/ 폴더에 복사. 계산 코드 src/analysis/compute.py.'
