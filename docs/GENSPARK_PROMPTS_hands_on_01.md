# Genspark 이미지 지시문 — 실제로 해보는 데이터 분석편 #01

페이지: `hands_on_01.html` (핀테크 데이터 분석 : 실제로 해보는 데이터 분석편 #01)
지금 페이지는 그림 없이도 완성 상태예요(대체 표지 + 캐릭터 팩 표정). 아래 그림을 받으면 자리에 자동으로 들어갑니다.

**그림체는 모두 16비트 RPG풍 픽셀아트(도트)이되, 픽셀이 작고 촘촘한 고해상도입니다.** 매끈한 일러스트·3D·수채화·애니메이션풍으로 나오면 쓰지 않고 다시 요청합니다. 배경은 밝은 낮, 흰 페이지에 어울리는 흰 벽 위주입니다. 그림 안에 글자·숫자·로고는 넣지 않습니다.

## 1. 그림 전체 목록

| 우선 | 키 | 비율 · 크기 | 자리 | 장면 한 줄 |
|---|---|---|---|---|
| P1 | `cover_hands_on_01` | 16:9 · 1920×1080 (최소 1600×900) | 맨 위 표지 | 연구실 발표회장. 왼쪽 초파리 팀, 오른쪽 주판봇 팀, 가운데 심판석의 박사 |
| P2 | `h01_A` | 3:2 · 1536×1024 (최소 1200×800) | 코드 A | 초파리 팀 조별 발표 — 펼친 장부 네 권과 빈 곳 찾기 |
| P2 | `h01_B` | 3:2 | 코드 B | X1 개인 발표 — 돋보기로 서류 속 물음표 모양 빈 곳 찾기 |
| P2 | `h01_C` | 3:2 | 코드 C | 시각화 대결 — 이젤 두 개(솟은 선 하나 vs 한 점에서 퍼지는 선 넷) |
| P2 | `h01_D` | 3:2 | 코드 D | 상담 — 모아와 박사, 똑같은 상자 두 개 |
| P2 | `h01_E` | 3:2 | 코드 E | 하루 개인 발표 — 사전과 쪽지, 100개 건물 중 빨간 3개 |
| P2 | `h01_F` | 3:2 | 코드 F | 조별 발표 + 반론 — 리본 색이 다른 신문 두 더미, 손 든 X2 |
| P3 | `h01_score` | 3:2 | 최종 판정 | 공동 우승 — 트로피 두 개와 두 팀 |
| — | 썸네일·공유 미리보기 | — | — | 따로 그리지 않음. 표지에서 자동으로 자름 |

**만드는 순서:** ① 표지(`cover_hands_on_01`)를 먼저 받아 그림체를 확인 → ② 마음에 들면 표지를 참고 그림으로 함께 올려 P2 여섯 장을 3장씩 두 번에 나눠 요청(같은 비율끼리) → ③ P3.

**참고 그림(매번 함께 올리기):** GitHub `adminmrobo/fruitfly-lab-expressions`의 `images/` 폴더에서 등장 캐릭터의 `E13_neutral.png`
- 박사 `doctor/` · 조수 하루 `haru/` · 초파리 연구원 `fruitfly/` · 주판봇 `jupanbot/` · 시아 `sia/` · 모아 `moa/` · X1 `x1/` · X2 `x2/` · X3 `x3/`
- 한 번에 올리는 참고 그림은 그 장면에 나오는 캐릭터만(최대 6장).

## 2. 고정 외형 (모든 지시문에 같은 문장을 씁니다)

| 캐릭터 | 팀 · 역할 | 영어 고정 문장 |
|---|---|---|
| 박사 | 심판 | chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie |
| 조수(하루) | 초파리 팀 | girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans |
| 초파리 연구원 | 초파리 팀 조장 | anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings |
| 주판봇 | 주판봇 팀 조장 | boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus |
| 시아(인턴1) | 초파리 팀 | calm anime girl maid intern, long straight jet-black hair to the waist, calm gray eyes, small silver drop earrings, charcoal-black maid dress with white lace cuffs, white high collar with a large soft gray bow, long white frilled apron |
| 모아(인턴2) | 주판봇 팀 | gentle cheerful anime girl maid intern, long ash-beige wavy hair, white frilled maid headband with a thin ribbon, big round amber-brown eyes, white shirt with a red and navy plaid bow tie, camel knit cardigan, white frilled apron, black skirt |
| X1 | 주판봇 팀 | cute solid dark navy-black silhouette (#1B1A2E) with a thin purple rim light, white dot eyes, pink blush pixels, chibi girl silhouette with a long side ponytail tied with a big bright pink (#E9709A) bow as the only colored part |
| X2 | 초파리 팀 | cute solid dark navy-black silhouette (#1B1A2E) with a thin purple rim light, white dot eyes, pink blush pixels, chibi silhouette with a round beret and short hair, round glasses whose lenses show two small teal (#3FC8C0) reflections as the only colored part |
| X3 | 주판봇 팀 | cute solid dark navy-black silhouette (#1B1A2E) with a thin purple rim light, white dot eyes, pink blush pixels, very small chibi silhouette wearing a hood with cat ears and an oversized lab coat, two hood drawstrings ending in small yellow (#F2C744) pompoms as the only colored part |

**팀 색:** 초파리 팀 = 빨강(#cc3434) 리본·깃발, 주판봇 팀 = 청록(#14899a) 리본·깃발, 심판 = 보라(#7a45d6) 완장. 팀 표시는 글자가 아니라 **색 리본과 깃발**로만 합니다.

## 3. 공통 그림체 문장 (지시문 맨 앞에 붙임)

```
HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art illustration, like a polished modern pixel-art game key visual. Render natively at the full output size with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks. Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level and finish of the attached quality reference image (style_quality_reference.png), but keep THIS scene's bright daytime colors. The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors. Bright daylight research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), high-key image that blends into a white web page, no dark background, no night. No text, no letters, no numbers, no logos, no watermark anywhere in the image (charts and papers show only shapes and lines).
```

---

## P1 · cover_hands_on_01 — 표지 (16:9)

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- 그림체는 16비트 RPG풍 픽셀아트(도트 그림)이되, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·옷 주름·소품을 세밀하게. 매끈한 일러스트·3D·수채화 금지
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 캐릭터들을 같은 그림체·같은 외형으로
- 그림 안에 글자·숫자·로고 금지. 얼굴은 가장자리에서 떨어진 가운데 영역에
아래 영어 프롬프트를 그대로 써 줘.

[공통 그림체 문장]
Wide 16:9 website cover, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Scene: a bright lab presentation hall set up like a friendly school contest. A large blank projector screen at the back center showing only simple bar and line shapes. Six colorful file folders (A to F shown only by six different tab colors, no letters) pinned in a row under the screen.
Left side, the red team with small red ribbons and a little red flag: [초파리 연구원 고정 문장] as team leader standing in front pointing at the screen; [시아 고정 문장]; [하루 고정 문장] holding a blank tablet; [X2 고정 문장].
Right side, the teal team with small teal ribbons and a little teal flag: [주판봇 고정 문장] as team leader proudly raising its abacus; [모아 고정 문장] holding a clipboard; [X1 고정 문장]; [X3 고정 문장].
Center front, a small judge's desk with a purple armband: [박사 고정 문장] sitting as the referee, holding two small paddles, one red and one teal.
Cheerful, playful contest mood. All nine characters visible, nobody cut off at the edges.
```
**고칠 때:** "매끈한 그림이 아니라 픽셀이 네모로 보이는 16비트 픽셀아트로 다시", "글자처럼 보이는 것은 모두 지우고 색 막대만", "X1·X2·X3는 실루엣 그대로, 색은 리본·안경 반사·방울만".

---

## P2 · 라운드 장면 6장 (3:2, 1200×800)

모두 **[공통 그림체 문장] + "3:2 scene illustration, output 1536x1024 (at least 1200x800), high-resolution detailed pixel art."** 로 시작합니다. 3장씩 두 번(A~C, D~F)으로 나눠 요청하세요.

### h01_A — 코드 A · 초파리 팀 조별 발표
```
Four thick open ledger books lying side by side on a long white table, each page filled with neat grid lines and tiny colored dots instead of writing; a few empty grid spots on the pages glow soft red. [초파리 연구원 고정 문장] stands at the head of the table with a pointer. [시아 고정 문장] counts rows with one finger, [하루 고정 문장] holds a blank tablet showing two bars of different height, [X2 고정 문장] peers through its glasses at a glowing red empty spot. Small red ribbons on the three members. Calm, focused team presentation mood.
```

### h01_B — 코드 B · X1 개인 발표
```
A small podium with a teal ribbon. [X1 고정 문장] stands at the podium holding a big magnifying glass over a stack of insurance papers; under the lens, several hollow question-mark shaped holes appear in the paper (shapes only, no text). Behind, a computer monitor shows a fake website with a tiny fishing hook icon on it. In the audience: [주판봇 고정 문장] cheering with its abacus raised, [초파리 연구원 고정 문장] pointing at a second paper sheet that is being covered by another identical sheet (overwritten). Bright, surprised discovery mood.
```

### h01_C — 코드 C · 시각화 대결
```
Two easels side by side. Left easel with a teal ribbon: a chart where one red line shoots straight up and three other lines lie flat along the bottom, almost invisible. Right easel with a red ribbon: a chart where four colored lines start from the same single point on the left and fan out upward at different slopes. [주판봇 고정 문장] and [모아 고정 문장] stand by the left easel, Moa sweating with a small sweat drop; [초파리 연구원 고정 문장] and [X2 고정 문장] stand by the right easel. In the middle [박사 고정 문장] as referee raises a red paddle. No numbers, no axis labels, only lines.
```

### h01_D — 코드 D · 상담 (모아 → 박사)
```
A cozy counseling corner in the lab: a small round table with two cups of tea. [모아 고정 문장] sits on one side looking puzzled, holding a clipboard. [박사 고정 문장] sits across, explaining kindly with one finger raised. On the table, two identical cardboard boxes with different colored stickers (one blue, one orange); both are open and show exactly the same stack of blue cards inside. Next to them, a very tall stack of paper reaching the ceiling and a small hourglass. In the doorway [X3 고정 문장] peeks in, surprised. Warm, reassuring mood.
```

### h01_E — 코드 E · 하루 개인 발표
```
[하루 고정 문장] stands at a podium with a red ribbon, presenting cheerfully. On the left, a long unrolled scroll with many small sticky notes attached beside each line (blank notes, no writing), and three spots on the scroll with no sticky note, marked by small gray question-mark shapes. On the right, a wall board showing a grid of 100 tiny pixel office buildings: 97 gray buildings and 3 red buildings. [X1 고정 문장] in the audience looks amazed with sparkling eyes, [박사 고정 문장] nods thoughtfully at the side.
```

### h01_F — 코드 F · 조별 발표 + 반론
```
Center: two separate piles of newspapers on a table (pages show only gray lines and simple picture boxes, no text); the left pile is tied with three different pink ribbons, the right pile with two different blue ribbons, so the piles can be told apart only by ribbon color. [모아 고정 문장] and [X3 고정 문장] present the piles happily, [주판봇 고정 문장] gives a thumbs-up. [X2 고정 문장] raises a hand from the side to object, with [초파리 연구원 고정 문장] crossing its arms next to X2. Background: a small cinema seating chart on the wall where only a few seats glow orange and most seats are dark gray. Lively debate mood.
```

## P3 · h01_score — 공동 우승 (3:2, 1200×800)
```
[공통 그림체 문장] 3:2 scene illustration, output 1536x1024 (at least 1200x800), high-resolution detailed pixel art.
A small award stage with two identical golden trophies, one with a red ribbon and one with a teal ribbon. [박사 고정 문장] stands in the middle as referee holding both arms up. Left: [초파리 연구원 고정 문장], [시아 고정 문장], [하루 고정 문장], [X2 고정 문장] celebrating. Right: [주판봇 고정 문장] looking a bit sheepish but happy, [모아 고정 문장], [X1 고정 문장], [X3 고정 문장] cheering. Confetti in red and teal. Behind them a scoreboard showing only two bars of nearly equal height (no numbers).
```

---

## 4. 받은 뒤 넣는 방법

1. 받은 그림을 저장소 루트 `incoming/` 폴더에 키 이름 그대로 저장합니다: `cover_hands_on_01.png`, `h01_A.png` … `h01_F.png`, `h01_score.png`
2. `cd src && python3 hands_on/add_images_h01.py`
   - 표지 → `src/build/covers/cover_hands_on_01.webp` (1600×900 WebP, 220KB 이하) + 공유 미리보기 `assets/og/cover_hands_on_01.jpg` (1200×630)
   - 장면·구조 일러스트 → `src/build/scenes/h01_*.webp` (1200×800 WebP, 180KB 이하)
3. `python3 hands_on/h01_build.py ..` — 표지와 라운드 장면이 페이지에 자동으로 들어갑니다.
4. 390px·1280px 화면에서 얼굴이 잘리지 않았는지 확인합니다.

## 5. 대체 글(alt)

| 키 | alt |
|---|---|
| cover_hands_on_01 | 실제로 해보는 데이터 분석편 #01 표지: 초파리 팀과 주판봇 팀이 발표회장 양쪽에 서고, 가운데 심판석에 박사가 앉은 장면 |
| h01_A | 초파리 팀이 펼친 장부 네 권에서 빈 곳을 찾는 장면 |
| h01_B | X1이 돋보기로 보험 서류 속 물음표 모양 빈 곳을 찾는 장면 |
| h01_C | 원래 가격 차트와 첫날=100 차트를 나란히 놓고 박사가 판정하는 장면 |
| h01_D | 모아가 박사에게 똑같은 두 상자에 대해 상담하는 장면 |
| h01_E | 하루가 변수 사전과 100개 건물 중 빨간 3개를 보여 주는 장면 |
| h01_F | 리본 색으로만 구분되는 신문 두 더미를 두고 X2가 반론하는 장면 |
| h01_score | 두 팀이 트로피 두 개를 받는 공동 우승 장면 |
