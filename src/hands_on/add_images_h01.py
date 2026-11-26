#!/usr/bin/env python3
"""실제로 해보는 데이터 분석편 #01 그림 넣기.
incoming/cover_hands_on_01.png, incoming/h01_A.png … h01_F.png, h01_score.png 를 받아
고해상도 그림은 1600×900(표지)·1200×800(장면) WebP로, 예전 4배 격자 그림은 정수배 무손실 WebP로 바꾼다. 사용: cd src && python3 hands_on/add_images_h01.py"""
import os, glob, re
from PIL import Image
SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); ROOT = os.path.dirname(SRC)
IN = os.path.join(ROOT, 'incoming'); COV = os.path.join(SRC, 'build', 'covers'); SCN = os.path.join(SRC, 'build', 'scenes'); OG = os.path.join(ROOT, 'assets', 'og')
for d in (COV, SCN, OG): os.makedirs(d, exist_ok=True)

def crop_ratio(im, w, h):
    W, H = im.size; r = w / h
    if abs(W / H - r) > 0.01:  # 비율 맞추기(가운데 자르기)
        if W / H > r: nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
        else: nh = int(W / r); im = im.crop((0, (H - nh) // 2, W, (H - nh) // 2 + nh))
    return im

def is_grid4(im):
    """작은 그림을 4배로 키운 거친 픽셀 그림인지(예전 지시문) 확인"""
    s = im.resize((im.width // 4, im.height // 4), Image.NEAREST)
    return s.resize(im.size, Image.NEAREST).tobytes() == im.tobytes()

def save_fit(im, w, h, out, max_kb):
    """고해상도 그림: 비율 맞춰 자르고 LANCZOS로 목표 크기, WebP 품질을 낮춰 가며 max_kb 이하로.
    예전 4배 격자 그림: 정수배 NEAREST·무손실 그대로."""
    im = crop_ratio(im, w, h)
    if is_grid4(im) and im.size == (w, h):
        im.save(out, 'WEBP', lossless=True, method=6); return 'grid4 lossless'
    im = im.resize((w, h), Image.LANCZOS)
    for q in (90, 86, 82, 78, 74, 70):
        im.save(out, 'WEBP', quality=q, method=6)
        if os.path.getsize(out) <= max_kb * 1024: break
    return f'hd q{q} {os.path.getsize(out)//1024}KB'

for f in sorted(glob.glob(os.path.join(IN, '*'))):
    b = os.path.basename(f); m = re.match(r'(cover_hands_on_01|h01_[A-F]|h01_score|h01_ig_(?:skel|[A-F]))\.(png|jpe?g|webp)$', b, re.I)
    if not m: continue
    k = m.group(1); im = Image.open(f).convert('RGB')
    if k.startswith('cover'):
        hd = not is_grid4(crop_ratio(im, 1920, 1080))
        out = os.path.join(COV, k + '.webp')
        info = save_fit(im, 1600, 900, out, 220) if hd else save_fit(im, 1920, 1080, out, 9999)
        big = Image.open(out).convert('RGB')
        og = crop_ratio(big, 1200, 630).resize((1200, 630), Image.LANCZOS); og.save(os.path.join(OG, k + '.jpg'), quality=88)
    else:
        info = save_fit(im, 1200, 800, os.path.join(SCN, k + '.webp'), 180)
    print('ok', k, info)
