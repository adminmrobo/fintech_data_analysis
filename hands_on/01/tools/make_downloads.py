#!/usr/bin/env python3
"""받기용 파일 만들기: 코드별 풀버전 .py, 코드 zip, CSV zip, 전체 zip.
사용: cd hands_on/01 && python3 tools/make_downloads.py"""
import os, ast, json, zipfile, glob
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDERS = ['A_customer_data_tour', 'B_fraud_phishing_check', 'C_portfolio_price_diary', 'D_loan_ledger_check', 'E_dictionary_and_bankruptcy', 'F_text_and_ratings']
DL = os.path.join(H, 'downloads'); os.makedirs(DL, exist_ok=True)

def to_py(folder):
    nb = json.load(open(os.path.join(H, folder, folder + '.ipynb'), encoding='utf-8'))
    out = ['# -*- coding: utf-8 -*-', f'# {folder}.py — 실행판 노트북을 파이썬 파일 하나로 옮긴 풀버전', '# 실행: python ' + folder + '.py  (이 폴더 안에서는 data/를, 밖에서는 GitHub의 데이터를 읽어요)', '# Colab: %run ' + folder + '.py', '']
    for c in nb['cells']:
        src = ''.join(c['source']).rstrip()
        if c['cell_type'] == 'markdown':
            out += ['# ' + l if l else '#' for l in src.splitlines()]; out.append('')
            continue
        tree = ast.parse(src); lines = src.splitlines()
        last = tree.body[-1] if tree.body else None
        if isinstance(last, ast.Expr) and not (isinstance(last.value, ast.Call) and getattr(last.value.func, 'id', '') == 'print') and not (isinstance(last.value, ast.Call) and 'plt' in ast.unparse(last.value.func)):
            seg = '\n'.join(lines[last.lineno - 1:last.end_lineno])
            lines = lines[:last.lineno - 1] + [f'print({seg})']
        out += lines + ['']
    out = [l.replace('plt.show()', 'plt.show() if "inline" in plt.get_backend() or "ipykernel" in plt.get_backend() else plt.close("all")') for l in out]
    p = os.path.join(H, folder, folder + '.py'); open(p, 'w', encoding='utf-8').write('\n'.join(out) + '\n'); return p

def plain_csvs(folder):
    return sorted(f for f in glob.glob(os.path.join(H, folder, 'data', '*.csv')))

allc = zipfile.ZipFile(os.path.join(DL, 'all_code.zip'), 'w', zipfile.ZIP_DEFLATED)
alld = zipfile.ZipFile(os.path.join(DL, 'all_csv.zip'), 'w', zipfile.ZIP_DEFLATED)
seen = set()
for f in FOLDERS:
    py = to_py(f)
    with zipfile.ZipFile(os.path.join(DL, f + '_code.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for name in [f + '.ipynb', f + '.py', 'original_Loading_Data.ipynb', 'README_original.md']:
            z.write(os.path.join(H, f, name), f'{f}/{name}'); allc.write(os.path.join(H, f, name), f'{f}/{name}')
    with zipfile.ZipFile(os.path.join(DL, f + '_csv.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for c in plain_csvs(f):
            z.write(c, f'{f}/' + os.path.basename(c))
            alld.write(c, f'{f}/' + os.path.basename(c))
allc.close(); alld.close()
for p in sorted(glob.glob(os.path.join(DL, '*.zip'))): print(os.path.basename(p), round(os.path.getsize(p) / 1e6, 2), 'MB')
