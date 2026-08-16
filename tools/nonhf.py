import json, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

KEEP = ('github.com','archive.org','openslr.org','catalog.ldc.upenn.edu','catalogue.elra.info',
        'magichub.com','magicdatatech.com','futurebeeai.com','shaip.com','appen.com',
        'commonvoice.mozilla.org','datacollective.mozillafoundation.org','librivox.org',
        'open.bible','metu.edu.tr','tdd.ai','kaggle.com','zenodo.org','data.gov.tr','nexdata.ai')
DROP = ('arxiv.org','mdpi.com','youtube.com','youtu.be','doi.org','aclanthology.org','sciencedirect')

def clean(c):
    c = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', c).replace('`','').strip()
    return c

def head(u):
    try:
        req=urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0 (catalogue link check)'}, method='GET')
        with urllib.request.urlopen(req, timeout=20) as r: return r.status
    except urllib.error.HTTPError as e: return e.code
    except Exception: return 0

raw=json.load(open('nonhf_raw.json'))
cand=[r for r in raw if any(k in r['domain'] for k in KEEP) and not any(d in r['domain'] for d in DROP)]
print('candidates:', len(cand))
with ThreadPoolExecutor(max_workers=10) as ex:
    codes=list(ex.map(lambda r: head(r['url']), cand))
out=[]
for r,c in zip(cand,codes):
    desc=''
    for cell in r['cells']:
        t=clean(cell)
        if len(t)>18 and 'http' not in t and len(t)>len(desc): desc=t
    out.append({'id': r['url'].split('//')[1][:70], 'url': r['url'], 'host': r['domain'],
                'modality': r['cats'][0] if r['cats'] else 'llm', 'task':'external',
                'desc': desc[:260], 'license': None, 'posture':'unverified',
                'http': c, 'alive': c in (200,301,302,403), 'verified':'2026-08-16'})
json.dump(out, open('catalogue_nonhf.json','w'), ensure_ascii=False, indent=1)
from collections import Counter
print('alive:', Counter(x['alive'] for x in out))
print(Counter(x['host'] for x in out).most_common(10))
