"""페이지 데이터를 짧게 쓰기 위한 도우미."""
import json, os
R = json.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'analysis', 'results.json'), encoding='utf-8'))

def pc(v, d=1):
    return f'{v * 100:.{d}f}%'

def nf(v, d=0):
    return f'{v:,.{d}f}'

def Q(q, o, a, why, hint='', kind='개념'):
    return dict(q=q, o=o, a=a, why=why, hint=hint, kind=kind)

def LV(id, short, title, tags, lead, key, node, limit_short, limit_en, why, math, pair, talk, sim_title, sim, explain, bridge, code=None, code_src='example', say=None, sim2=None, sim2_title=None):
    d = dict(id=id, short=short, title=title, tags=tags, lead=lead, key=key, node=node, limit_short=limit_short, limit_en=limit_en,
             why=dict(zip(['problem', 'limit', 'solve', 'easy'], why)), pair=dict(zip(['short', 'left', 'right'], pair)), talk=talk,
             sim_title=sim_title, sim=sim, explain=dict(zip(['title', 'steps', 'limit'], explain)), bridge=dict(zip(['gen', 'gen_lim', 'field', 'field_lim'], bridge)),
             code=code, code_src=code_src, say=say)
    if math:
        d['math'] = dict(zip(['q', 'school', 'fx', 'parts', 'try', 'comment'], math))
    if sim2:
        d['sim2'] = sim2; d['sim2_title'] = sim2_title
    return d

def G(ko, cat, desc, en, lab, lv):
    return [ko, cat, desc, en, lab, lv]
