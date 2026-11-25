#!/usr/bin/env python3
"""강사용 진행 가이드(docs/INSTRUCTOR_GUIDE.md)를 페이지 데이터에서 만든다.
사용: cd src && python3 build/make_guide.py"""
import os, re, sys, importlib.util
sys.path[:0] = ['build', 'pages']
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SITE = 'https://adminmrobo.github.io/fintech_data_analysis/'
COLAB = 'https://colab.research.google.com/github/adminmrobo/fintech_data_analysis/blob/main/notebooks/'


def load(p):
    s = importlib.util.spec_from_file_location('x', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.P


def t(x):
    """HTML 태그를 지우고 한 줄로."""
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', str(x))).strip()


pages = [load(os.path.join('pages', f)) for f in sorted(os.listdir('pages')) if re.match(r'p\d\d\.py$', f)]
L = ['# 강사용 진행 가이드 — 핀테크 데이터 분석 기초 (15회차)', '',
     '해설 페이지를 수업 화면에 띄우고, 실습은 회차별 Colab 노트북으로 하는 진행안입니다. '
     '**1회 100분 기준**으로 적었습니다. 수업 시간이 다르면 단계별 시간을 같은 비율로 늘리거나 줄이세요.', '',
     '## 공통 진행 순서 (100분)', '',
     '| 단계 | 시간 | 화면 | 하는 일 |', '|---|---|---|---|',
     '| 1. 여는 질문 | 5분 | 히어로의 질문 | 질문을 읽고 손을 들어 짐작 답을 받는다. 정답은 말하지 않는다 |',
     '| 2. 3줄 요약 | 5분 | 「처음 오신 분께」 | 무엇을 · 왜 · 업무에서는 세 줄을 함께 읽는다 |',
     '| 3. 단계 ①②③ | 각 15분 | 단계마다 실험 | "가져갈 한 가지"를 먼저 말하고, 실험 조절기를 학생에게 맡겨 움직여 보게 한다. 수식 상자는 원하는 학생만 |',
     '| 4. 대결 | 10분 | 대결 | 결과를 열기 전에 초파리·주판봇 중 누가 이길지 투표 → 결과 공개 → "왜?"를 2~3명에게 묻는다 |',
     '| 5. 실습 | 25분 | Colab 노트북 | 대결 셀을 직접 실행해 같은 숫자가 나오는지 확인하고, 숫자 하나(시드·k·임계값)를 바꿔 본다 |',
     '| 6. 정리·퀴즈 | 10분 | 정리 · 확인 퀴즈 | 단계 ③의 AI 판단 문항은 짝과 토론 후 답한다 |', '',
     '**투표가 중요한 이유:** 대결 결과는 초파리 6 · 주판봇 3 · 조건부 3 · 무승부 1로 나눠 두었습니다. '
     '"의심하는 쪽이 늘 이긴다"고 외우지 않게, 투표 → 결과 → 이유 순서를 지켜 주세요.', '',
     '**중간·기말(8·15회차):** 1부 요약 갤러리(30분) → 2부 교안 문제(40분, 정답 표시를 고친 문항 먼저 확인) → 3부 계산 문제(30분, 계산기 허용).', '',
     '**금융 회차(11·13):** 주가 실험은 2013~2019년 데이터로 한 교육용 백테스트입니다. 투자 자문이 아니라고 수업 처음에 한 번 말해 주세요.', '']
for P in pages:
    num = P['num']
    if 'duel' not in P and P.get('kind') != 'review': continue
    if P.get('kind') == 'review':
        L += [f'## {num}회차 — {t(P["title"])}', '', f'- 페이지: [{P["file"]}]({SITE}{P["file"]})', f'- 여는 질문: {t(P["question"])}',
              f'- 구성: 교안 문제 {len(P.get("orig", []))}문항 · 계산 문제 {len(P.get("calc", []))}개', '']
        if P.get('changes'):
            L += ['**원자료와 다르게 쓴 곳 (수업 전 확인)**', ''] + [f'- {t(c if isinstance(c, str) else " — ".join(map(str, c)))}' for c in P['changes']] + ['']
        continue
    stem = P['file'].replace('.html', '')
    nb = os.path.exists(os.path.join(ROOT, 'notebooks', stem + '.ipynb'))
    T = P['three']; D = P['duel']
    L += [f'## {num}회차 — {t(P["title"])}', '',
          f'- 페이지: [{P["file"]}]({SITE}{P["file"]})' + (f' · 실습: [Colab 노트북]({COLAB}{stem}.ipynb)' if nb else ''),
          f'- 여는 질문: **{t(P["question"])}**', '',
          '| 3줄 요약 | |', '|---|---|', f'| 무엇을 | {t(T["what"])} |', f'| 왜 중요한가 | {t(T["why"])} |', f'| 업무에서는 | {t(T["work"])} |', '',
          '| 단계 | 제목 | 가져갈 한 가지 | 이 단계의 한계 |', '|---|---|---|---|']
    for i, l in enumerate(P['levels'], 1):
        L.append(f'| {"①②③"[i - 1]} | {t(l["title"])} | {t(l.get("key", ""))} | {t(l.get("limit_short", ""))} |')
    L += ['', f'**대결** — {t(D["question"])}', '',
          f'- 설정: {t(D["setup"])}',
          f'- 초파리: {t(D["fly_choice"])} / 주판봇: {t(D["robo_choice"])} · 판정 기준: {t(D.get("metric", ""))}',
          f'- 결과 뒤에 칠판에 쓸 한 문장: {t(D.get("cond_lesson") or D.get("lesson", ""))}', '']
    if P.get('changes'):
        L += ['**원자료와 다르게 쓴 곳 (수업 전 확인)**', ''] + [f'- {t(c if isinstance(c, str) else " — ".join(map(str, c)))}' for c in P['changes']] + ['']
    if P.get('next_q'):
        L += [f'**다음 회차로 넘기는 질문:** {t(P["next_q"])}', '']
L += ['## 자주 나오는 질문', '',
      '| 질문 | 답의 방향 |', '|---|---|',
      '| 노트북 숫자가 페이지와 조금 달라요 | 시드(RS=42)와 분할 비율을 바꾸지 않았는지 확인. 라이브러리 버전에 따라 소수 셋째 자리가 달라질 수 있습니다 |',
      '| 원고 실습(생선·와인·농어)은 어디 갔나요? | 같은 과정을 fintech-data의 금융 데이터로 바꿨습니다. 과정과 코드 흐름은 같습니다 |',
      '| 코드 상자를 그대로 실행하면 오류가 나요 | 페이지의 코드 상자는 설명용 조각입니다. 실행은 Colab 노트북으로 하세요 |',
      '| 3D 타워가 안 보여요 | 휴대폰에서는 「3D 타워 보기」 버튼을 눌러야 불러옵니다. 학교망에서 CDN이 막히면 오른쪽 안내판으로 이동하면 됩니다 |', '',
      '---', '', '글 · 안상선 ((주)M-Robo 대표)']
open(os.path.join(ROOT, 'docs', 'INSTRUCTOR_GUIDE.md'), 'w').write('\n'.join(L) + '\n')
print('ok', len(L), 'lines')
