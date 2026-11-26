#!/usr/bin/env python3
"""실제로 해보는 데이터 분석편 #01 그림 넣기.
incoming/cover_hands_on_01.png, incoming/h01_A.png … h01_F.png, h01_score.png 를 받아
픽셀아트가 뭉개지지 않게(정수배 NEAREST) 무손실 WebP로 바꾼다. 사용: cd src && python3 hands_on/add_images_h01.py"""
import os, glob, re
from PIL import Image
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT = os.path.dirname(SRC)
IN = os.path.join(ROOT, 'incoming'); COV = os.path.join(SRC, 'build', 'covers'); SCN = os.path.join(SRC, 'build', 'scenes'); OG = os.path.join(ROOT, 'assets', 'og')
for d in (COV, SCN, OG): os.makedirs(d, exist_ok=True)

def pixel_fit(im, w, h):
    """원래 격자(그림의 1/4 크기 근처)를 찾아 정수배로만 키운다."""
    W, H = im.size; r = w / h
    if abs(W / H - r) > 0.01:  # 비율 맞추기(가운데 자르기)
        if W / H > r: nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
        else: nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    gw, gh = w // 4, h // 4
    return im.resize((gw, gh), Image.NEAREST).resize((w, h), Image.NEAREST)

for f in sorted(glob.glob(os.path.join(IN, '*'))):
    b = os.path.basename(f); m = re.match(r'(cover_hands_on_01|h01_[A-F]|h01_score|h01_ig_(?:skel|[A-F]))\.(png|jpe?g|webp)$', b, re.I)
    if not m: continue
    k = m.group(1); im = Image.open(f).convert('RGB')
    if k.startswith('cover'):
        big = pixel_fit(im, 1920, 1080); big.save(os.path.join(COV, k + '.webp'), 'WEBP', lossless=True, method=6)
        og = big.crop((0, 45, 1920, 1053)).resize((1200, 630), Image.LANCZOS); og.save(os.path.join(OG, k + '.jpg'), quality=88)
    else:
        pixel_fit(im, 1200, 800).save(os.path.join(SCN, k + '.webp'), 'WEBP', lossless=True, method=6)
    print('ok', k)
