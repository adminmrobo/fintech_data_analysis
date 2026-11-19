#!/usr/bin/env python3
"""Genspark 등에서 받은 표지 그림을 페이지에 넣을 형식으로 바꾼다.
1) 받은 그림을 incoming/ 폴더(저장소 루트)에 cover_00.png ~ cover_15.png 처럼 키 이름으로 넣는다 (png·jpg·webp 모두 가능)
2) cd src && python3 build/add_covers.py
   → src/build/covers/cover_NN.webp (1600×900, 220 KB 이하)
   → assets/og/cover_NN.jpg (1200×630, 공유 미리보기), cover_00 이면 assets/og_series.jpg 도 교체
3) python3 build/build.py ..   (표지·목차 썸네일이 자동으로 들어감)"""
import os, glob, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IN = os.path.join(ROOT, 'incoming')
CDIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'covers')
OG = os.path.join(ROOT, 'assets', 'og')
os.makedirs(CDIR, exist_ok=True); os.makedirs(OG, exist_ok=True)


def fit(im, w, h):
    """가운데 기준으로 비율을 맞춰 자른 뒤 크기를 바꾼다(16:9 → 1200×630 은 위아래를 조금 자름)."""
    W, H = im.size; r = w / h
    if W / H > r:
        nw = int(H * r); im = im.crop(((W - nw) // 2, 0, (W - nw) // 2 + nw, H))
    else:
        nh = int(W / r); top = max(0, int((H - nh) * 0.4)); im = im.crop((0, top, W, top + nh))
    return im.resize((w, h), Image.LANCZOS)


done = []
for f in sorted(glob.glob(os.path.join(IN, '*'))):
    m = re.match(r'cover_(\d\d)\.(png|jpe?g|webp)$', os.path.basename(f), re.I)
    if not m:
        print('건너뜀(이름이 cover_NN 이 아님):', os.path.basename(f)); continue
    k = m.group(1); im = Image.open(f).convert('RGB')
    if abs(im.size[0] / im.size[1] - 16 / 9) > 0.03:
        print(f'주의: cover_{k} 비율이 16:9가 아님 {im.size} → 가운데를 잘라 맞춥니다')
    big = fit(im, 1600, 900); out = os.path.join(CDIR, f'cover_{k}.webp')
    for q in (82, 76, 70, 64, 58, 52):
        big.save(out, 'WEBP', quality=q, method=6)
        if os.path.getsize(out) <= 220 * 1024: break
    og = fit(im, 1200, 630); og.save(os.path.join(OG, f'cover_{k}.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)
    if k == '00':
        og.save(os.path.join(ROOT, 'assets', 'og_series.jpg'), 'JPEG', quality=84, optimize=True, progressive=True)
    done.append(f'cover_{k} ({os.path.getsize(out) // 1024} KB)')
print('처리:', ', '.join(done) if done else '없음 — incoming/ 폴더에 cover_NN.png 를 넣으세요')
