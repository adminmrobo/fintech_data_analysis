# 포트폴리오 카드 표지 — Genspark 그림 지시문

- 키: `portfolio_fintech` · 판: 16:9 픽셀아트 (480×270 → 4배 1920×1080)
- 쓰는 곳: ahnboat_lab_cover_status 포트폴리오 「저서·이러닝 › 이러닝 › 핀테크 데이터분석 기초」 카드 (800×450으로 줄여 씀)
- 참고 이미지: 네 캐릭터 기본 그림 4장 + 이 시리즈 표지 cover_00 (그림체 맞추기)
- 회차 표지와 겹치지 않게: 건물 **밖**에서 본 장면 — 쌍둥이 타워와 스카이브리지가 배경, 네 식구가 앞 광장에 섬
- 완료: 2026-11-20 받은 그림을 넣음 (원본 docs/portfolio_fintech_1920.png, 카드용 assets/thumb_portfolio.webp · cover_status thumbs/cats/E-fintech-lab.webp)

## 한국어 요약

- **그림체는 반드시 16비트 RPG풍 픽셀아트(도트)** — 매끈한 일러스트·3D·수채화 금지
- 비율 16:9, 480×270 픽셀로 그린 뒤 4배(1920×1080)로 흐림 없이 확대
- 장면: 여의도 강변의 맑은 오후. 청록빛 유리의 쌍둥이 타워(왼쪽 서관이 낮고 오른쪽 동관이 높음), 두 동을 잇는 공중 다리, 동관 옥상의 파란 지구본 모형
- 앞 광장에 박사·조수·초파리 연구원·주판봇 넷이 서서 관람객 쪽을 봄. 조수는 태블릿에 오르는 차트, 주판봇은 주판, 초파리는 돋보기, 박사는 타워를 가리킴
- 광장에 작은 소품: 동전 더미, 큰 스마트폰 모양 안내판(화면엔 무늬만), 벤치, 나무 몇 그루
- 아래쪽 띠는 밝은 흰 광장 바닥으로 끝나게(흰 페이지에 어울리게)
- 글자·숫자·로고 없음

## Genspark에 붙여 넣을 지시문

```
16-bit RPG style PIXEL ART illustration, wide 16:9.
Art style (mandatory): retro 16-bit pixel art like a SNES-era RPG scene. Draw on a low-resolution grid of 480x270 pixels, then upscale exactly 4x with nearest-neighbor to 1920x1080, so every pixel is a crisp square block.
  Limited palette (about 32 colors), bold dark 1-pixel outlines, flat 2-3 tone cel shading, small pixel highlights, hard pixel edges, no anti-aliasing, no blur.
  The characters must look like the attached pixel-art sprite reference images: same pixel style, same proportions, same colors.
Scene: a bright, clear afternoon on a riverside business district plaza. In the background stand twin office towers with teal-tinted glass: the left tower is shorter, the right tower is taller, and a glass sky bridge connects them in the middle. A small blue wireframe globe sits on the roof of the taller tower.
In the foreground plaza, four characters stand side by side facing the viewer:
  a chibi scientist with spiky black-and-white hair, glasses and a white lab coat, pointing up at the towers;
  a girl assistant with long pink hair in twin buns with blue streaks, lab coat over a lavender hoodie, holding a tablet that shows a simple rising bar chart (shapes only);
  a fruit-fly researcher in a lab coat with big red eyes and a blue helmet with cables, holding a magnifying glass, on the left facing right;
  a boxy beige retro-computer robot with a green smiling screen face and tank treads, holding a wooden abacus, on the right facing left.
Small props on the plaza: a stack of gold coins, a tall smartphone-shaped kiosk with a plain colorful screen pattern, a bench, a few round trees.
Make the bottom strip a plain near-white plaza floor so the image sits well on a white page (use flat pixel dithering, not a smooth gradient).
Cheerful, clean, friendly mood; leave some empty sky at the top.
Avoid: smooth digital painting, vector illustration, 3D render, anime cel illustration, watercolor, soft gradients, photorealism, high-resolution detail, blurry or anti-aliased edges.
No text, no letters, no numbers, no logos, no weapons, no cigarettes, no alcohol, no blood, no real brands.
```

고칠 때: `Same four characters, same 16-bit pixel art style (480x270 grid, 4x nearest-neighbor, crisp square pixels) and composition. Change only: {고칠 점}. Still no text.`
