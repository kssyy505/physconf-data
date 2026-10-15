#!/usr/bin/env python3
"""conferences.json 스키마 검사. 커밋 전에 반드시 실행: python3 scripts/validate.py
오류가 하나라도 있으면 exit 1 (앱이 깨진 데이터를 받지 않도록)."""
import json, re, sys
from datetime import datetime, date

PATH = sys.argv[1] if len(sys.argv) > 1 else 'conferences.json'
CATS = {'DEV', 'CIR', 'MAT', 'PHY', 'QNT', 'NEU', 'OPT', 'IND'}
DL_TYPES = {'abstract', 'paper', 'latenews', 'poster', 'registration'}
YMD = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ISO_UTC = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')

errors, warnings = [], []
def err(cid, msg): errors.append(f'[{cid}] {msg}')
def warn(cid, msg): warnings.append(f'[{cid}] {msg}')

try:
    doc = json.load(open(PATH, encoding='utf-8'))
except Exception as e:
    print(f'JSON 파싱 실패: {e}'); sys.exit(1)

for k in ('schema', 'version', 'updatedAt', 'conferences'):
    if k not in doc: errors.append(f'최상위 필드 누락: {k}')
if not YMD.match(str(doc.get('version', ''))): errors.append('version은 YYYY-MM-DD 형식이어야 함')

confs = doc.get('conferences', [])
if not isinstance(confs, list) or len(confs) < 10:
    errors.append(f'conferences 배열이 비었거나 너무 적음 ({len(confs) if isinstance(confs, list) else "?"}개) — 실수로 지운 것 아닌지 확인')
    confs = confs if isinstance(confs, list) else []

ids = set()
for c in confs:
    cid = c.get('id', '?')
    if not isinstance(c.get('id'), str) or not re.match(r'^[a-z0-9]+\d{4}$', cid): err(cid, 'id는 소문자+연도4자리 (예: iedm2027)')
    if cid in ids: err(cid, 'id 중복')
    ids.add(cid)
    series = c.get('series')
    if not isinstance(series, str) or cid != f"{series}{c.get('edition')}": err(cid, 'series + edition 이 id와 일치해야 함')
    for f in ('short', 'name', 'city', 'country', 'website', 'description', 'verified'):
        if not isinstance(c.get(f), str) or not c.get(f): err(cid, f'필드 누락/빈 값: {f}')
    if c.get('region') not in ('KR', 'INTL'): err(cid, 'region은 KR 또는 INTL')
    if c.get('verified') not in ('primary', 'secondary'): err(cid, 'verified는 primary/secondary')
    cats = c.get('categories')
    if not isinstance(cats, list) or not cats or not set(cats) <= CATS: err(cid, f'categories 오류: {cats}')
    for f in ('start', 'end'):
        v = c.get(f)
        if v is not None and not (isinstance(v, str) and YMD.match(v)): err(cid, f'{f}는 YYYY-MM-DD 또는 null')
    if c.get('start') and c.get('end') and c['end'] < c['start']: err(cid, 'end < start')
    if c.get('start') and not c['start'].startswith(str(c.get('edition'))):
        warn(cid, 'start 연도와 edition이 다름 (연말·연초 걸친 학회면 무시)')
    for f in ('lat', 'lng'):
        v = c.get(f)
        if v is not None and not isinstance(v, (int, float)): err(cid, f'{f}는 숫자 또는 null')
    if not str(c.get('website', '')).startswith('http'): err(cid, 'website는 http(s) URL')
    srcs = c.get('sources')
    if not isinstance(srcs, list) or not srcs: err(cid, 'sources가 최소 1개 필요 (출처 없는 정보 금지)')
    else:
        for s in srcs:
            if not str(s.get('url', '')).startswith('http') or not s.get('title'): err(cid, f'source 형식 오류: {s}')
    dls = c.get('deadlines')
    if not isinstance(dls, list): err(cid, 'deadlines는 배열'); dls = []
    for d in dls:
        if d.get('type') not in DL_TYPES: err(cid, f'deadline type 오류: {d.get("type")}')
        if not ISO_UTC.match(str(d.get('at', ''))): err(cid, f'deadline at은 UTC ISO (YYYY-MM-DDTHH:MM:SSZ): {d.get("at")}')
        if not d.get('tz'): err(cid, 'deadline tz(공지 기준 시간대) 누락')
    lc = c.get('lastChecked')
    if lc is not None and not (isinstance(lc, str) and YMD.match(lc)): err(cid, 'lastChecked는 YYYY-MM-DD')

for w in warnings: print('경고', w)
for e in errors: print('오류', e)
print(f'검사 완료: 학회 {len(confs)}개, 오류 {len(errors)}, 경고 {len(warnings)}')
sys.exit(1 if errors else 0)
