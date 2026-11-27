# 표지 지시문 모음 — 핀테크 데이터 분석 기초

각 페이지 맨 위 `data-img="cover_{N}"` 자리에 넣을 16:9 표지 그림 지시문입니다(ai-lab-explainer 18-14). **그림체는 16비트 RPG풍 픽셀아트(도트)로 통일합니다** — 캐릭터 팩 스프라이트와 같은 그림체여야 해요. 지금 페이지에는 네 캐릭터를 나란히 세운 대체 표지가 들어 있고, 그림을 받으면 픽셀이 뭉개지지 않게 1920×1080 WebP로 넣습니다.

> **2026-11-27 고해상도판으로 고침:** 처음 지시문(480×270 격자로 그린 뒤 4배 확대)은 그림이 거친 큰 블록으로 나와, 가로 1920에서 직접 그린 촘촘한 픽셀아트(본 스킬 18-15-2 v1.19)로 바꿨습니다. 세밀함 기준은 `style_quality_reference.png`(AI 텍스트 가독성 연구실 표지)입니다.

**참고 이미지(함께 올리기):** 세밀함 기준 1장 + 네 캐릭터 기본 그림 4장 — GitHub `adminmrobo/fruitfly-lab-expressions`. 첫 표지(목차)를 먼저 받아 그림체를 확인한 뒤 나머지에 참고 그림으로 함께 올리세요.

## 작업 순서

1. **cover_00(목차)부터** 만듭니다. 참고 이미지로 네 캐릭터 기본 그림 4장을 함께 올리세요.
2. 마음에 드는 cover_00을 받으면, 나머지 15장을 만들 때 **cover_00도 참고 이미지로 같이 올려** 그림체를 맞춥니다.
3. 받은 파일은 `cover_NN.png` 이름으로 zip에 묶어 올려 주세요. 1600×900 WebP(220KB 이하)로 넣고 다시 빌드합니다.
4. 매끈한 일러스트로 나오거나 글자·숫자·로고가 섞여 나오면 "고칠 때" 문장으로 다시 요청합니다. **픽셀아트가 아니면 쓰지 않습니다.**

| 키 | 층 · 장면 | 주제 소품 (한 줄) |
|---|---|---|
| cover_00 | 핀데이터 그룹 본사 타워 로비 | 15색 층 안내판과 층을 타고 오르는 데이터 물줄기 |
| cover_01 | 1F 핀테크 전략기획실 | 옛 은행 창구(번호표 기계) vs 큰 스마트폰, 거래 점들이 폰으로 흘러듦 |
| cover_02 | 2F 데이터 수집팀 | 깔때기·파이프로 서류·API 플러그·웹 카드를 병에 모음, 빨간 경고 스티커 병 하나 |
| cover_03 | 3F 데이터 기획실 | 6단계 빈 흐름도 화이트보드와 체크리스트 |
| cover_04 | 4F 분석 도구 지원실 | 계산기·스프레드시트·뱀 모양 코딩 도구·대시보드가 걸린 도구 벽, 시험지 두 장 |
| cover_05 | 5F 데이터 전처리 센터 | 데이터 카드를 씻고 그릇에 나누는 부엌, 튀어나온 큰 카드 하나 |
| cover_06 | 6F 고객 이탈 분석팀 | 바닥의 파란·빨간 점, 가장 가까운 5개 점을 잇는 삼각형 표지, 두 무리를 가르는 넓은 길, 저울 |
| cover_07 | 7F 모델 검증실 | 벽의 2×2 빛나는 구역, 왼쪽 위로 휘는 곡선, 천장 화재경보기 |
| cover_08 | 8F 중간 점검 라운지 | 게시판의 빈 카드 7장, 계단 중간의 리본 |
| cover_09 | 9F 보험 가격 산정팀 | 세 띠로 나뉜 점 차트 위 직선과 곡선, 다트판 |
| cover_10 | 10F 신용 리스크 모델링실 | 예/아니오로 갈라지는 작은 나무, 떠 있는 S자 곡선, 맞물리는 퍼즐 두 조각 |
| cover_11 | 11F 시장 데이터 랩 | 선으로 이어진 뉴런 벽, 한 걸음 늦게 따라가는 점선 예측선 |
| cover_12 | 12F 데이터 시각화 스튜디오 | 선·막대·원·상자·산점도 이젤과 바닥의 꼬리 긴 히스토그램 |
| cover_13 | 13F 로보어드바이저 사업부 | 빈 설문지, 자산 원그래프, 교차하는 이동평균선 두 개, 로보어드바이저 키오스크 |
| cover_14 | 14F 정보보호·데이터 거버넌스 센터 | 금고 문, 세 조각 방패, 흐릿하게 묶인 사람 실루엣들, 데이터 건강검진 클립보드 |
| cover_15 | 15F 전망대 | 타워 층을 내려다보는 망원경, 벤치 위 닫힌 책 여섯 권, 노을 |

## cover_00 — 핀테크 데이터 분석 기초

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_00 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `index.html` |
| 장소 | 핀데이터 그룹 본사 타워 로비 |
| 주제 소품 | 15색 층 안내판과 층을 타고 오르는 데이터 물줄기 |
| 주제 은유 | a bright lobby of a glass office tower with a floor directory board of 15 blank colored floor plates and a soft glowing data river flowing up the floors |
| 대체 글(alt) | 핀테크 데이터 분석 기초의 표지: 박사, 조수, 초파리 연구원, 주판봇이 핀데이터 그룹 본사 타워 로비에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: the bright glass lobby of a fintech company headquarters tower in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, center pointing at the directory;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, holding a blank tablet;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, looking up;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, counting floors on its abacus.
Visual metaphor of the topic: a bright lobby of a glass office tower with a floor directory board of 15 blank colored floor plates and a soft glowing data river flowing up the floors.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_01 — 핀테크 산업의 이해와 핀테크 데이터

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_01 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `01_fintech_industry.html` |
| 장소 | 1F 핀테크 전략기획실 |
| 주제 소품 | 옛 은행 창구(번호표 기계) vs 큰 스마트폰, 거래 점들이 폰으로 흘러듦 |
| 주제 은유 | an old bank counter with a numbered ticket machine on one side and a giant smartphone showing blank app tiles on the other, glowing transaction dots flowing into the phone |
| 대체 글(alt) | 핀테크 산업의 이해와 핀테크 데이터의 표지: 박사, 조수, 초파리 연구원, 주판봇이 1F 핀테크 전략기획실에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright strategy office of a fintech company in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, standing between them;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, tapping the phone;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, inspecting the transaction dots;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, waving from behind the old counter.
Visual metaphor of the topic: an old bank counter with a numbered ticket machine on one side and a giant smartphone showing blank app tiles on the other, glowing transaction dots flowing into the phone.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_02 — 핀테크 데이터 수집 기술

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_02 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `02_data_collection.html` |
| 장소 | 2F 데이터 수집팀 |
| 주제 소품 | 깔때기·파이프로 서류·API 플러그·웹 카드를 병에 모음, 빨간 경고 스티커 병 하나 |
| 주제 은유 | pipes and funnels collecting floating paper forms, plug-shaped API connectors and web page cards into labeled-but-blank jars; one jar has a red warning sticker (no text) |
| 대체 글(alt) | 핀테크 데이터 수집 기술의 표지: 박사, 조수, 초파리 연구원, 주판봇이 2F 데이터 수집팀에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright data-collection room with pipes and shelves in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, checking a jar;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, pouring forms into a funnel;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, holding a magnifier over a mislabeled jar;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, pushing an overflowing cart of jars.
Visual metaphor of the topic: pipes and funnels collecting floating paper forms, plug-shaped API connectors and web page cards into labeled-but-blank jars; one jar has a red warning sticker (no text).
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_03 — 데이터 분석을 위한 준비 — 수집 계획 세우기

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_03 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `03_collection_plan.html` |
| 장소 | 3F 데이터 기획실 |
| 주제 소품 | 6단계 빈 흐름도 화이트보드와 체크리스트 |
| 주제 은유 | a large whiteboard with a six-step blank flowchart and a shopping-list style checklist, a network of dots connecting on one side |
| 대체 글(alt) | 데이터 분석을 위한 준비 — 수집 계획 세우기의 표지: 박사, 조수, 초파리 연구원, 주판봇이 3F 데이터 기획실에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright planning meeting room in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, drawing the first step;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, holding a blank checklist;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at the first box;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, eager at the last box.
Visual metaphor of the topic: a large whiteboard with a six-step blank flowchart and a shopping-list style checklist, a network of dots connecting on one side.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_04 — 데이터 분석 개념의 이해 — 도구, 모델, 검증

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_04 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `04_analysis_concepts.html` |
| 장소 | 4F 분석 도구 지원실 |
| 주제 소품 | 계산기·스프레드시트·뱀 모양 코딩 도구·대시보드가 걸린 도구 벽, 시험지 두 장 |
| 주제 은유 | a tool wall with a calculator, a spreadsheet grid, a big snake-shaped coding tool and a dashboard screen (all blank), and two exam papers side by side |
| 대체 글(alt) | 데이터 분석 개념의 이해 — 도구, 모델, 검증의 표지: 박사, 조수, 초파리 연구원, 주판봇이 4F 분석 도구 지원실에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright tool room of an analytics team in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, picking a tool;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, holding two blank exam sheets;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, comparing the sheets;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, hugging the biggest tool.
Visual metaphor of the topic: a tool wall with a calculator, a spreadsheet grid, a big snake-shaped coding tool and a dashboard screen (all blank), and two exam papers side by side.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_05 — 분류모형(1) — Colab 환경과 데이터 입력·전처리

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_05 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `05_preprocessing.html` |
| 장소 | 5F 데이터 전처리 센터 |
| 주제 소품 | 데이터 카드를 씻고 그릇에 나누는 부엌, 튀어나온 큰 카드 하나 |
| 주제 은유 | a kitchen counter where data cards are being washed, sorted into bowls labeled with blank tags, and one odd giant card sticking out of a bowl |
| 대체 글(alt) | 분류모형(1) — Colab 환경과 데이터 입력·전처리의 표지: 박사, 조수, 초파리 연구원, 주판봇이 5F 데이터 전처리 센터에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright, clean data-preparation kitchen-like workshop in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, in an apron sorting cards;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, lining up bowls;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, examining the odd card;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, about to throw cards in a bin.
Visual metaphor of the topic: a kitchen counter where data cards are being washed, sorted into bowls labeled with blank tags, and one odd giant card sticking out of a bowl.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_06 — 데이터 분석 실습 — KNN·SVM, 데이터 분할과 표준화

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_06 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `06_knn_svm.html` |
| 장소 | 6F 고객 이탈 분석팀 |
| 주제 소품 | 바닥의 파란·빨간 점, 가장 가까운 5개 점을 잇는 삼각형 표지, 두 무리를 가르는 넓은 길, 저울 |
| 주제 은유 | a scatter of blue and red glowing dots on the floor, a triangle marker with lines to its five nearest dots, a wide road dividing two groups, and a big balance scale |
| 대체 글(alt) | 데이터 분석 실습 — KNN·SVM, 데이터 분할과 표준화의 표지: 박사, 조수, 초파리 연구원, 주판봇이 6F 고객 이탈 분석팀에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright analysis lab with a large floor map of dots in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, balancing the scale;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, placing the triangle;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, measuring a distance with a tape;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, stretching a ruler the wrong way.
Visual metaphor of the topic: a scatter of blue and red glowing dots on the floor, a triangle marker with lines to its five nearest dots, a wide road dividing two groups, and a big balance scale.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_07 — 데이터 분석 모델의 평가 — 혼동행렬, ROC, 최적화

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_07 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `07_model_evaluation.html` |
| 장소 | 7F 모델 검증실 |
| 주제 소품 | 벽의 2×2 빛나는 구역, 왼쪽 위로 휘는 곡선, 천장 화재경보기 |
| 주제 은유 | a large 2-by-2 glowing grid on the wall, a curved line rising to the top-left on a chart (no numbers), and a fire alarm on the ceiling |
| 대체 글(alt) | 데이터 분석 모델의 평가 — 혼동행렬, ROC, 최적화의 표지: 박사, 조수, 초파리 연구원, 주판봇이 7F 모델 검증실에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright model-review room in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, stamping a blank approval paper;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, pointing at one grid cell;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, watching the alarm;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, holding up a huge shiny blank trophy.
Visual metaphor of the topic: a large 2-by-2 glowing grid on the wall, a curved line rising to the top-left on a chart (no numbers), and a fire alarm on the ceiling.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_08 — 중간 요약정리 및 퀴즈 — 1~7회차

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_08 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `08_midterm_review.html` |
| 장소 | 8F 중간 점검 라운지 |
| 주제 소품 | 게시판의 빈 카드 7장, 계단 중간의 리본 |
| 주제 은유 | a cozy lounge with seven blank cards pinned on a board, small plants, and a ribbon marking halfway up a staircase |
| 대체 글(alt) | 중간 요약정리 및 퀴즈 — 1~7회차의 표지: 박사, 조수, 초파리 연구원, 주판봇이 8F 중간 점검 라운지에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright cozy lounge halfway up the tower in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, tapping the board;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, handing out blank cards;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, raising a hand;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, holding a blank score tally.
Visual metaphor of the topic: a cozy lounge with seven blank cards pinned on a board, small plants, and a ribbon marking halfway up a staircase.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_09 — 데이터 분석 모형: 회귀모형(1) — "얼마"를 맞히는 모델

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_09 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `09_regression.html` |
| 장소 | 9F 보험 가격 산정팀 |
| 주제 소품 | 세 띠로 나뉜 점 차트 위 직선과 곡선, 다트판 |
| 주제 은유 | a scatter of dots on a wall chart split into three bands, a straight glowing line and a gently curving line over it, and a dartboard |
| 대체 글(alt) | 데이터 분석 모형: 회귀모형(1) — "얼마"를 맞히는 모델의 표지: 박사, 조수, 초파리 연구원, 주판봇이 9F 보험 가격 산정팀에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright insurance pricing office in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, drawing the line;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, measuring gaps with small rulers;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at dots beyond the edge;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, stuck at the chart edge.
Visual metaphor of the topic: a scatter of dots on a wall chart split into three bands, a straight glowing line and a gently curving line over it, and a dartboard.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_10 — 데이터 분석 모형: 회귀모형(2) — 로지스틱 회귀, 결정나무, 특성공학

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_10 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `10_logistic_tree.html` |
| 장소 | 10F 신용 리스크 모델링실 |
| 주제 소품 | 예/아니오로 갈라지는 작은 나무, 떠 있는 S자 곡선, 맞물리는 퍼즐 두 조각 |
| 주제 은유 | a small glowing decision tree with yes/no fork branches, an S-shaped curve floating above, and two puzzle pieces clicking together |
| 대체 글(alt) | 데이터 분석 모형: 회귀모형(2) — 로지스틱 회귀, 결정나무, 특성공학의 표지: 박사, 조수, 초파리 연구원, 주판봇이 10F 신용 리스크 모델링실에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright indoor garden lab in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, pruning the tree;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, holding the S-curve;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, fitting the puzzle pieces;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, watering the tree too much.
Visual metaphor of the topic: a small glowing decision tree with yes/no fork branches, an S-shaped curve floating above, and two puzzle pieces clicking together.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_11 — 딥러닝 모델과 시계열 데이터 분석

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_11 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `11_deep_learning_timeseries.html` |
| 장소 | 11F 시장 데이터 랩 |
| 주제 소품 | 선으로 이어진 뉴런 벽, 한 걸음 늦게 따라가는 점선 예측선 |
| 주제 은유 | a wall of glowing neurons connected by lines, and a long winding price line with a dashed forecast line one step behind it |
| 대체 글(alt) | 딥러닝 모델과 시계열 데이터 분석의 표지: 박사, 조수, 초파리 연구원, 주판봇이 11F 시장 데이터 랩에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright market-data observatory room in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, adjusting a neuron dial;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, tracing the price line;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, holding a calendar showing today = tomorrow (no text);
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, pushing a huge complicated machine.
Visual metaphor of the topic: a wall of glowing neurons connected by lines, and a long winding price line with a dashed forecast line one step behind it.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_12 — 핀테크 데이터 시각화 — 대표값, 상관, 차트 고르기

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_12 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `12_visualization.html` |
| 장소 | 12F 데이터 시각화 스튜디오 |
| 주제 소품 | 선·막대·원·상자·산점도 이젤과 바닥의 꼬리 긴 히스토그램 |
| 주제 은유 | easels with a line chart, bar chart, pie chart, box plot and scatter plot (no numbers), and a long-tailed histogram on the floor |
| 대체 글(alt) | 핀테크 데이터 시각화 — 대표값, 상관, 차트 고르기의 표지: 박사, 조수, 초파리 연구원, 주판봇이 12F 데이터 시각화 스튜디오에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright painting studio for charts in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, choosing an easel;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, painting a box plot;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, pointing at the long tail;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, painting a giant pie chart.
Visual metaphor of the topic: easels with a line chart, bar chart, pie chart, box plot and scatter plot (no numbers), and a long-tailed histogram on the floor.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_13 — 데이터 기반의 핀테크 서비스 기획 — 로보어드바이저

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_13 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `13_robo_advisor.html` |
| 장소 | 13F 로보어드바이저 사업부 |
| 주제 소품 | 빈 설문지, 자산 원그래프, 교차하는 이동평균선 두 개, 로보어드바이저 키오스크 |
| 주제 은유 | a desk with a blank questionnaire, a pie of assets, two moving average lines crossing on a screen, and a robot advisor kiosk |
| 대체 글(alt) | 데이터 기반의 핀테크 서비스 기획 — 로보어드바이저의 표지: 박사, 조수, 초파리 연구원, 주판봇이 13F 로보어드바이저 사업부에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright wealth-advice consulting room in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, reviewing the questionnaire;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, adjusting the pie slices;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, watching the lines cross;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, pressing buy-sell buttons.
Visual metaphor of the topic: a desk with a blank questionnaire, a pie of assets, two moving average lines crossing on a screen, and a robot advisor kiosk.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_14 — 데이터 보안 및 품질 관리

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_14 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `14_security_quality.html` |
| 장소 | 14F 정보보호·데이터 거버넌스 센터 |
| 주제 소품 | 금고 문, 세 조각 방패, 흐릿하게 묶인 사람 실루엣들, 데이터 건강검진 클립보드 |
| 주제 은유 | a vault door, a shield with three segments, a crowd of silhouettes blurred into groups, and a health-check clipboard for data files |
| 대체 글(alt) | 데이터 보안 및 품질 관리의 표지: 박사, 조수, 초파리 연구원, 주판봇이 14F 정보보호·데이터 거버넌스 센터에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright security center in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, locking the vault;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, grouping silhouettes;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, inspecting files with the clipboard;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, erasing faces with a giant eraser.
Visual metaphor of the topic: a vault door, a shield with three segments, a crowd of silhouettes blurred into groups, and a health-check clipboard for data files.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`

## cover_15 — 기말 요약정리 및 퀴즈 — 9~14회차

| 항목 | 내용 |
|---|---|
| 키 · 판 | cover_15 · L (16:9 고해상도 픽셀아트, 1920×1080(최소 1600×900)) |
| 페이지 | `15_final_review.html` |
| 장소 | 15F 전망대 |
| 주제 소품 | 타워 층을 내려다보는 망원경, 벤치 위 닫힌 책 여섯 권, 노을 |
| 주제 은유 | a rooftop observatory with a telescope looking down at the tower floors glowing below, six closed books on a bench and a sunset sky |
| 대체 글(alt) | 기말 요약정리 및 퀴즈 — 9~14회차의 표지: 박사, 조수, 초파리 연구원, 주판봇이 15F 전망대에서 주제 소품을 바라보는 장면 |

**Genspark에 붙여 넣기 ↓**
```
웹페이지 맨 위에 거는 표지 그림 1장을 만들어 줘.
- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트 그림)**: 매끈한 일러스트·3D·수채화·애니메이션풍 금지, 픽셀이 작고 촘촘한 고해상도로 얼굴·손·소품을 세밀하게(함께 올린 style_quality_reference.png 정도)
- 비율 16:9, 가로 1920(최소 1600) 픽셀 고해상도로. 작은 그림을 크게 확대해 큰 네모 블록이 보이는 그림은 안 됨
- 첨부한 참고 이미지(픽셀아트 스프라이트)의 네 캐릭터(박사, 조수, 초파리 연구원, 주판봇)를 같은 픽셀 그림체·같은 외형으로, 넷 모두 등장
- 그림 안에 글자·숫자·로고를 넣지 말 것
- 얼굴과 손은 가장자리에서 떨어진 가운데 영역에, 왼쪽 아래 구석은 밝고 단순하게(흰 벽), 아래 가장자리는 흰 페이지로 자연스럽게 이어지게
- 밤 장면·어두운 배경 금지, 전체적으로 밝은 낮 장면
아래 영어 프롬프트를 그대로 써 줘.

16-bit RPG style PIXEL ART website cover, wide 16:9, output 1920x1080 (at least 1600x900), high-resolution detailed pixel art.
Art style (mandatory): HIGH-RESOLUTION, highly detailed 16-bit RPG style pixel art, like a polished modern pixel-art game key visual. Render natively at 1920x1080 with SMALL, dense pixels (each art pixel only about 2 screen pixels wide) — NOT a tiny low-resolution image blown up into big square blocks.
  Rich detail in faces, eyes, hair strands, hands, clothes folds and props; bold dark outlines, 2–3 tone shading, small highlights, subtle dithering, crisp edges, no blur. Match the detail level of the attached quality reference image (style_quality_reference.png), but keep this page's bright daytime colors.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright rooftop observatory in late afternoon light in soft daylight, styled like a friendly research lab, clean white walls and pale gray-blue furniture (#ffffff to #f6f7fb), simple flat pixel shadows, pale blue pixel monitor glow, small accents of magenta (#a8329f), green (#138a52) and blue (#2563c9). High-key image that blends into a white web page; no dark background, no night sky.
All four characters together:
  chibi scientist, thin teal rectangular glasses, spiky black hair with one white streak, small ponytail at the back, white lab coat over black vest and tie, at the telescope;
  girl researcher, long pink hair with two round buns and a navy streak, blue eyes, white lab coat over lavender hoodie, jeans, placing the last book;
  anthropomorphic fruit fly researcher, black body, big red compound eyes, blue helmet with a gold stripe and pink and blue cables, white lab coat over a black vest, black gloves, transparent wings, on the left facing right, looking back down the stairs;
  boxy beige retro CRT-monitor robot, dark green screen face with mint pixel eyes and mouth, short antenna topped with a red-brown abacus bead, gray segmented arms, two small tank treads, holding a wooden abacus, on the right facing left, waving a small flag.
Visual metaphor of the topic: a rooftop observatory with a telescope looking down at the tower floors glowing below, six closed books on a bench and a sunset sky.
Composition: keep every face and hand inside the central safe area (12% margin left and right, 10% top, 18% bottom);
  keep the bottom-left corner light and simple (plain white wall); make the bottom strip a plain near-white floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient); the topic prop is the most saturated spot.
Mood: curious, friendly rivalry, the moment before the result.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, big blocky low-resolution pixels, blurry edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same high-resolution 16-bit pixel art style (small dense pixels, detailed faces) and composition. Change only: {고칠 점}. Still no text.`
