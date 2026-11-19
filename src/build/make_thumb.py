#!/usr/bin/env python3
"""포트폴리오 카드용 픽셀아트 썸네일(800×450)을 만든다.
400×225 픽셀 바탕에 평평한 색면으로 장면을 그리고, 캐릭터 팩 스프라이트를 nearest로 얹은 뒤
색 수를 줄이고(48색) 정확히 2배 nearest 확대한다. 글자는 넣지 않는다.
사용: cd src && python3 build/make_thumb.py  → assets/thumb_portfolio.webp"""
import os, json, base64, io
from PIL import Image, ImageDraw

B = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(B))
S = json.load(open(os.path.join(B, 'sprites.json')))
W, H = 400, 225


def sprite(alias, size):
    k = S['alias'].get(alias, alias)
    im = Image.open(io.BytesIO(base64.b64decode(S['img'][k].split(',')[1]))).convert('RGBA')
    return im.resize((size, size), Image.NEAREST)


im = Image.new('RGBA', (W, H), (246, 248, 252, 255))
d = ImageDraw.Draw(im)
# 벽 · 바닥
d.rectangle([0, 0, W, 150], fill=(233, 239, 247))
d.rectangle([0, 150, W, H], fill=(214, 222, 234))
for x in range(0, W, 20):                       # 바닥 타일 줄
    d.line([x, 150, x, H], fill=(203, 212, 226))
d.line([0, 150, W, 150], fill=(176, 188, 207), width=2)

# 창문: 밖으로 보이는 쌍둥이 타워와 스카이브리지
d.rectangle([14, 14, 128, 104], fill=(196, 222, 236), outline=(120, 136, 160), width=2)
d.rectangle([14, 80, 128, 104], fill=(172, 204, 222))
d.rectangle([34, 46, 58, 102], fill=(124, 186, 188)); d.rectangle([80, 30, 104, 102], fill=(112, 172, 178))
for y in range(50, 100, 6):
    d.line([35, y, 57, y], fill=(150, 205, 205)); d.line([81, y - 14, 103, y - 14], fill=(140, 196, 198))
d.rectangle([58, 60, 80, 66], fill=(160, 214, 190))   # 8층 스카이브리지
d.rectangle([90, 22, 94, 30], fill=(80, 100, 150))    # 동관 옥상 지구본 기둥
d.line([71, 14, 71, 104], fill=(120, 136, 160), width=2)

# 큰 모니터: 주가 캔들 차트
d.rectangle([150, 14, 300, 102], fill=(32, 44, 70), outline=(70, 84, 110), width=3)
d.rectangle([218, 102, 232, 116], fill=(150, 160, 178)); d.rectangle([200, 116, 250, 120], fill=(150, 160, 178))
import random
random.seed(7)
y = 70
for i, x in enumerate(range(160, 292, 9)):
    o = y; y = [62, 66, 58, 52, 57, 46, 40, 44, 34, 38, 30, 42, 36, 28, 33][i]
    up = y < o
    c = (88, 214, 141) if up else (235, 98, 98)
    top, bot = min(o, y), max(o, y)
    d.line([x + 2, top - 4, x + 2, bot + 4], fill=c)
    d.rectangle([x, top, x + 4, max(bot, top + 2)], fill=c)
d.line([158, 96, 294, 96], fill=(70, 84, 110))

# 오른쪽 선반: 금고 · 동전 더미 · 휴대폰
d.rectangle([318, 60, 384, 112], fill=(120, 132, 150), outline=(78, 88, 104), width=2)   # 금고
d.ellipse([340, 74, 362, 96], fill=(170, 180, 196), outline=(78, 88, 104), width=2)
d.line([351, 78, 351, 92], fill=(78, 88, 104), width=2); d.line([344, 85, 358, 85], fill=(78, 88, 104), width=2)
for i in range(5):                                                                        # 동전
    d.rectangle([322, 50 - i * 4, 342, 54 - i * 4], fill=(240, 196, 70), outline=(176, 128, 30))
d.rounded_rectangle([352, 30, 372, 58], 3, fill=(40, 48, 64))                             # 휴대폰
d.rectangle([355, 34, 369, 52], fill=(120, 200, 230)); d.rectangle([357, 44, 367, 48], fill=(240, 196, 70))

# 책상
d.rectangle([140, 150, 312, 158], fill=(176, 132, 92)); d.rectangle([146, 158, 152, 196], fill=(150, 110, 76)); d.rectangle([300, 158, 306, 196], fill=(150, 110, 76))
d.rectangle([168, 140, 206, 150], fill=(250, 250, 252), outline=(160, 170, 186))          # 서류
d.rectangle([226, 136, 262, 150], fill=(60, 70, 90)); d.rectangle([229, 139, 259, 147], fill=(110, 190, 225))  # 노트북

# 캐릭터 (스프라이트 팩 그대로, nearest)
for alias, sz, x, yy in [('doc_board', 92, 6, 112), ('asst_smile', 84, 92, 130), ('fly_e01', 76, 228, 146), ('robo_e01', 86, 304, 128)]:
    sp = sprite(alias, sz)
    im.alpha_composite(sp, (x, yy - 0 if yy + sz <= H else H - sz))

# 색 수 줄이기 → 정확히 2배 확대
q = im.convert('RGB').quantize(colors=48, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
out = q.resize((W * 2, H * 2), Image.NEAREST)
p = os.path.join(ROOT, 'assets', 'thumb_portfolio.webp')
out.save(p, 'WEBP', lossless=True, method=6)
out.save('/tmp/thumb.png')
print(p, os.path.getsize(p) // 1024, 'KB')
