import os, sys, json, re
sys.path.insert(0, 'build'); sys.path.insert(0, 'pages')
import importlib.util
def load(p):
    s = importlib.util.spec_from_file_location('x', p); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m.P
pages = [load(os.path.join('pages', f)) for f in sorted(os.listdir('pages')) if re.match(r'p\d\d\.py$', f)]
META = {
 '00': ('밝은 연구실 로비', 'a bright lobby of a glass office tower with a floor directory board of 15 blank colored floor plates and a soft glowing data river flowing up the floors', '박사 center pointing at the directory; 조수 holding a blank tablet; 초파리 on the left looking up; 주판봇 on the right counting floors on its abacus'),
 '01': ('은행 창구와 휴대폰 앱이 마주 보는 연구실', 'an old bank counter with a numbered ticket machine on one side and a giant smartphone showing blank app tiles on the other, glowing transaction dots flowing into the phone', '박사 standing between them; 조수 tapping the phone; 초파리 inspecting the transaction dots; 주판봇 waving from behind the old counter'),
 '02': ('데이터 수집실', 'pipes and funnels collecting floating paper forms, plug-shaped API connectors and web page cards into labeled-but-blank jars; one jar has a red warning sticker (no text)', '박사 checking a jar; 조수 pouring forms into a funnel; 초파리 holding a magnifier over a mislabeled jar; 주판봇 pushing an overflowing cart of jars'),
 '03': ('기획 회의실', 'a large whiteboard with a six-step blank flowchart and a shopping-list style checklist, a network of dots connecting on one side', '박사 drawing the first step; 조수 holding a blank checklist; 초파리 pointing at the first box; 주판봇 eager at the last box'),
 '04': ('도구 창고', 'a tool wall with a calculator, a spreadsheet grid, a big snake-shaped coding tool and a dashboard screen (all blank), and two exam papers side by side', '박사 picking a tool; 조수 holding two blank exam sheets; 초파리 comparing the sheets; 주판봇 hugging the biggest tool'),
 '05': ('연구실 부엌', 'a kitchen counter where data cards are being washed, sorted into bowls labeled with blank tags, and one odd giant card sticking out of a bowl', '박사 in an apron sorting cards; 조수 lining up bowls; 초파리 examining the odd card; 주판봇 about to throw cards in a bin'),
 '06': ('저울이 있는 실험실', 'a scatter of blue and red glowing dots on the floor, a triangle marker with lines to its five nearest dots, a wide road dividing two groups, and a big balance scale', '박사 balancing the scale; 조수 placing the triangle; 초파리 measuring a distance with a tape; 주판봇 stretching a ruler the wrong way'),
 '07': ('검증 심사실', 'a large 2-by-2 glowing grid on the wall, a curved line rising to the top-left on a chart (no numbers), and a fire alarm on the ceiling', '박사 stamping a blank approval paper; 조수 pointing at one grid cell; 초파리 watching the alarm; 주판봇 holding up a huge shiny blank trophy'),
 '08': ('중간 점검 라운지', 'a cozy lounge with seven blank cards pinned on a board, small plants, and a ribbon marking halfway up a staircase', '박사 tapping the board; 조수 handing out blank cards; 초파리 raising a hand; 주판봇 holding a blank score tally'),
 '09': ('보험 가격 산정실', 'a scatter of dots on a wall chart split into three bands, a straight glowing line and a gently curving line over it, and a dartboard', '박사 drawing the line; 조수 measuring gaps with small rulers; 초파리 pointing at dots beyond the edge; 주판봇 stuck at the chart edge'),
 '10': ('나무가 자라는 정원 연구실', 'a small glowing decision tree with yes/no fork branches, an S-shaped curve floating above, and two puzzle pieces clicking together', '박사 pruning the tree; 조수 holding the S-curve; 초파리 fitting the puzzle pieces; 주판봇 watering the tree too much'),
 '11': ('시장 데이터 관측소', 'a wall of glowing neurons connected by lines, and a long winding price line with a dashed forecast line one step behind it', '박사 adjusting a neuron dial; 조수 tracing the price line; 초파리 holding a calendar showing today = tomorrow (no text); 주판봇 pushing a huge complicated machine'),
 '12': ('시각화 스튜디오', 'easels with a line chart, bar chart, pie chart, box plot and scatter plot (no numbers), and a long-tailed histogram on the floor', '박사 choosing an easel; 조수 painting a box plot; 초파리 pointing at the long tail; 주판봇 painting a giant pie chart'),
 '13': ('자산관리 상담실', 'a desk with a blank questionnaire, a pie of assets, two moving average lines crossing on a screen, and a robot advisor kiosk', '박사 reviewing the questionnaire; 조수 adjusting the pie slices; 초파리 watching the lines cross; 주판봇 pressing buy-sell buttons'),
 '14': ('정보보호 센터', 'a vault door, a shield with three segments, a crowd of silhouettes blurred into groups, and a health-check clipboard for data files', '박사 locking the vault; 조수 grouping silhouettes; 초파리 inspecting files with the clipboard; 주판봇 erasing faces with a giant eraser'),
 '15': ('15층 전망대', 'a rooftop observatory with a telescope looking down at the tower floors glowing below, six closed books on a bench and a sunset sky', '박사 at the telescope; 조수 placing the last book; 초파리 looking back down the stairs; 주판봇 waving a small flag'),
}
KO = {'00': '15색 층 안내판과 층을 타고 오르는 데이터 물줄기', '01': '옛 은행 창구(번호표 기계) vs 큰 스마트폰, 거래 점들이 폰으로 흘러듦', '02': '깔때기·파이프로 서류·API 플러그·웹 카드를 병에 모음, 빨간 경고 스티커 병 하나', '03': '6단계 빈 흐름도 화이트보드와 체크리스트', '04': '계산기·스프레드시트·뱀 모양 코딩 도구·대시보드가 걸린 도구 벽, 시험지 두 장', '05': '데이터 카드를 씻고 그릇에 나누는 부엌, 튀어나온 큰 카드 하나', '06': '바닥의 파란·빨간 점, 가장 가까운 5개 점을 잇는 삼각형 표지, 두 무리를 가르는 넓은 길, 저울', '07': '벽의 2×2 빛나는 칸, 왼쪽 위로 휘는 곡선, 천장 화재경보기', '08': '게시판의 빈 카드 7장, 계단 중간의 리본', '09': '세 띠로 나뉜 점 차트 위 직선과 곡선, 다트판', '10': '예/아니오로 갈라지는 작은 나무, 떠 있는 S자 곡선, 맞물리는 퍼즐 두 조각', '11': '선으로 이어진 뉴런 벽, 한 걸음 늦게 따라가는 점선 예측선', '12': '선·막대·원·상자·산점도 이젤과 바닥의 꼬리 긴 히스토그램', '13': '빈 설문지, 자산 원그래프, 교차하는 이동평균선 두 개, 로보어드바이저 키오스크', '14': '금고 문, 세 조각 방패, 흐릿하게 묶인 사람 실루엣들, 데이터 건강검진 클립보드', '15': '타워 층을 내려다보는 망원경, 벤치 위 닫힌 책 여섯 권, 노을'}
SC = {'00': ('핀데이터 그룹 본사 타워 로비', 'the bright glass lobby of a fintech company headquarters tower'), '01': ('1F 핀테크 전략기획실', 'a bright strategy office of a fintech company'), '02': ('2F 데이터 수집팀', 'a bright data-collection room with pipes and shelves'), '03': ('3F 데이터 기획실', 'a bright planning meeting room'), '04': ('4F 분석 도구 지원실', 'a bright tool room of an analytics team'), '05': ('5F 데이터 전처리 센터', 'a bright, clean data-preparation kitchen-like workshop'), '06': ('6F 고객 이탈 분석팀', 'a bright analysis lab with a large floor map of dots'), '07': ('7F 모델 검증실', 'a bright model-review room'), '08': ('8F 중간 점검 라운지', 'a bright cozy lounge halfway up the tower'), '09': ('9F 보험 가격 산정팀', 'a bright insurance pricing office'), '10': ('10F 신용 리스크 모델링실', 'a bright indoor garden lab'), '11': ('11F 시장 데이터 랩', 'a bright market-data observatory room'), '12': ('12F 데이터 시각화 스튜디오', 'a bright painting studio for charts'), '13': ('13F 로보어드바이저 사업부', 'a bright wealth-advice consulting room'), '14': ('14F 정보보호·데이터 거버넌스 센터', 'a bright security center'), '15': ('15F 전망대', 'a bright rooftop observatory in late afternoon light')}
C = {'doc': 'chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie',
     'asst': 'girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans',
     'fly': 'anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings',
     'robo': 'boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus'}
L = ['# 표지 지시문 모음 — 핀테크 데이터 분석 기초', '', '각 페이지 맨 위 `data-img="cover_{N}"` 자리에 넣을 16:9 표지 그림 지시문입니다(ai-lab-explainer 18-14). 지금 페이지에는 네 캐릭터를 나란히 세운 대체 표지가 들어 있어요. 그림을 받으면 WebP 1600×900(220 KB 이하)으로 바꿔 넣습니다.', '', '**참고 이미지(함께 올리기):** 네 캐릭터 기본 그림 4장 — GitHub `adminmrobo/fruitfly-lab-expressions`. 첫 표지(목차)를 먼저 받아 그림체를 확인한 뒤 나머지에 참고 그림으로 함께 올리세요.', '']
for P in pages:
    key = P.get('key', P['num'].lower())
    k = key if key in META else P['num']
    _p, meta, pose = META[k]
    place, scene = SC[k]
    ps = [re.sub(r'^(박사|조수|초파리|주판봇)( on the (left|right))?\s*', '', x.strip()) for x in pose.split(';')]
    alt = f'{P["title"]}의 표지: 박사, 조수, 초파리 연구원, 주판봇이 {place}에서 주제 소품을 바라보는 장면'
    prompt = f'''Website top cover illustration, wide 16:9.
Match the art style, proportions and colors of the attached reference images exactly
  (if there are no reference images: 16-bit RPG style pixel art, bold dark outline, 2-3 tone shading, small highlights).
Scene: {scene} in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), gentle shadows, pale blue monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  {C['doc']}, {ps[0]};
  {C['asst']}, {ps[1]};
  {C['fly']}, on the left facing right, {ps[2]};
  {C['robo']}, on the right facing left, {ps[3]}.
Visual metaphor of the topic: {meta}.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); let the bottom edge fade to near-white so the image melts into a white page; the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.'''
    L += [f'## cover_{key} — {P["title"]}', '', '| 항목 | 내용 |', '|---|---|', f'| 키 · 판 | cover_{key} · L (16:9, 1920 이상) |', f'| 페이지 | `{P["file"]}` |', f'| 장소 | {place} |', f'| 주제 소품 | {KO[k]} |', f'| 주제 은유 | {meta} |', f'| 대체 글(alt) | {alt} |', '', '**Genspark에 붙여 넣기 ↓**', '```', '웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.', '- 비율 16:9, 가로 1920px 이상', '- 첨부한 참고 이미지의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 그림체·같은 외형으로, 넷 모두 등장', '- 그림 안에 글자·숫자·로고를 넣지 말 것', '- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게', '- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면', '아래 영어 프롬프트를 그대로 써 줘.', '', prompt, '```', '', '고칠 때: `Same four characters, same art style and composition. Change only: {고칠 점}. Still no text.`', '']
OV = ['## 작업 순서', '',
      '1. **cover_00(목차)부터** 만듭니다. 참고 이미지로 네 캐릭터 기본 그림 4장을 함께 올리세요.',
      '2. 마음에 드는 cover_00을 받으면, 나머지 15장을 만들 때 **cover_00도 참고 이미지로 같이 올려** 그림체를 맞춥니다.',
      '3. 받은 파일은 `cover_NN.png` 이름으로 저장소 루트 `incoming/` 폴더에 넣고 `cd src && python3 build/add_covers.py` → `python3 build/build.py ..` 를 실행합니다.',
      '4. 글자·숫자·로고가 섞여 나오면 맨 아래 "고칠 때" 문장으로 다시 요청합니다.', '',
      '| 키 | 층 · 장면 | 주제 소품 (한 줄) |', '|---|---|---|']
for P in pages:
    key = P.get('key', P['num'].lower()); k = key if key in META else P['num']
    OV.append(f'| cover_{key} | {SC[k][0]} | {KO[k]} |')
L[6:6] = OV + ['']
open('out/docs/COVER_PROMPTS_series.md', 'w').write('\n'.join(L))
# 이미지 명세서(시리즈 공용)
man = []
for P in pages:
    key = P.get('key', P['num'].lower())
    man.append({'key': f'cover_{key}', 'board': 'L', 'size': '1600x900', 'page': P['file'], 'status': 'needed', 'fallback': 'CSS 그라데이션 + 캐릭터 팩 4명 나란히'})
    if P.get('kind', 'lesson') == 'lesson':
        man.append({'key': f'thumb_{key}', 'board': 'I', 'size': '600x400', 'page': 'index.html', 'status': 'needed', 'fallback': '목차 카드는 글자만'})
man.append({'key': 'og_series', 'board': 'K', 'size': '1200x630', 'page': 'all', 'status': 'done', 'file': 'assets/og_series.jpg', 'note': '대체 표지 화면을 찍은 임시 공유 그림. 목차 표지를 받으면 잘라 바꿈'})
doc = ['# 이미지 제작 명세서 — 핀테크 데이터 분석 기초 (시리즈 공용)', '', '## 1. 그림체와 고정 외형', '캐릭터 팩 `CHAR_lab4` 18-3·18-4를 따릅니다. 16비트 RPG풍 픽셀아트, 굵은 어두운 외곽선, 흰 배경에 어울리는 밝은 낮 연구실 조명. 그림 안에 글자·숫자·로고 없음.', '', '## 2. 지금 쓰는 그림', '- 캐릭터 표정: 캐릭터 팩 1.3(fruitfly-lab-expressions @ 86d04ac) 96px를 페이지마다 필요한 키만 base64로 넣었습니다(페이지당 약 13~16장, 100 KB 안팎). 새로 그릴 표정은 없습니다.', '- 장면·컷: 모든 실험 그림은 Canvas로 그려 그림 파일이 필요 없습니다.', '- 표지: 16쪽 모두 대체 표지(그림 없이 완성 상태). 표지 지시문은 `COVER_PROMPTS_series.md`.', '', '## 3. 새로 그릴 그림 (우선순위)', '| 우선 | 키 | 판 | 내용 |', '|---|---|---|---|', '| P1 | cover_00 | L | 목차 표지(그림체 기준) |', '| P1 | cover_01 ~ cover_07, cover_09 ~ cover_14 | L | 회차 표지 13장 |', '| P2 | cover_08, cover_15 | L | 중간·기말 점검 표지 |', '| — | thumb_01 ~ thumb_15 | I | 따로 그리지 않음 — 빌드가 표지에서 자동으로 만듦 |', '| P3 | og_series | K | 목차 표지를 1200×630으로 잘라 교체 |', '', '## 4. 넘겨받은 뒤 처리', '1. 16:9·글자 없음·네 캐릭터 외형 확인 → 2. 저장소 루트 `incoming/` 폴더에 `cover_NN.png` 이름으로 넣기 → 3. `cd src && python3 build/add_covers.py` (WebP 1600×900·220 KB 이하, 공유 미리보기 1200×630 자동) → 4. `python3 build/build.py ..` → 5. 390·768·1280 폭에서 얼굴 잘림 확인 → 6. 아래 매니페스트 status를 done으로.', '', '## 5. 매니페스트', '```json', json.dumps(man, ensure_ascii=False, indent=1), '```']
open('out/docs/IMG_00_index.md', 'w').write('\n'.join(doc))
print('docs ok', len(pages))
