import json, os, re, urllib.request
from concurrent.futures import ThreadPoolExecutor
TOK=open('/home/goksel/.cache/huggingface/token').read().strip() if os.path.exists('/home/goksel/.cache/huggingface/token') else None
H={'User-Agent':'tr-datasets-catalogue'}
if TOK: H['Authorization']=f'Bearer {TOK}'

BAD_START = re.compile(r'^\s*([-*+>|]|\d+\.|#|<|!\[|\[!)')
BAD_WORDS = re.compile(r'^(personal and sensitive|social impact|discussion of|additional inform|dataset (card|struct|creation|descri)|table of contents|curation rational|source data|annotations?$|licensing|citation|contributions|supported tasks|languages?$|data (fields|splits|instances))', re.I)

def sentencelike(s):
    if BAD_START.match(s) or BAD_WORDS.match(s): return False
    w = s.split()
    if len(w) < 7: return False
    if s.count(',') >= len(w) / 3: return False          # virgul listesi
    if sum(c.isupper() for c in s) > len(s) * 0.35: return False
    return True

def summary(dsid):
    try:
        req=urllib.request.Request(f"https://huggingface.co/datasets/{dsid}/raw/main/README.md", headers=H)
        txt=urllib.request.urlopen(req, timeout=20).read().decode('utf-8','ignore')
    except Exception:
        return dsid, ''
    if txt.lstrip().startswith('---'):
        p=txt.split('---',2); txt=p[2] if len(p)>2 else txt
    for line in txt.splitlines():
        s=re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', line.strip())
        s=re.sub(r'[*`_#]', '', s).strip()
        if 'http' in s: continue
        if sentencelike(s): return dsid, s[:230]
    return dsid, ''

c=json.load(open('catalogue_hf.json'))
orig=json.load(open('extracted.json'))                     # katalogdan gelen orijinal desc'ler
need=[x['id'] for x in c]
with ThreadPoolExecutor(max_workers=10) as ex:
    got=dict(ex.map(summary, need))
kept=0
for x in c:
    # once kendi katalogumuzun aciklamasi (insan yazmis, daha degerli), yoksa kart cumlesi
    if not x['desc'] or not sentencelike(x['desc']):
        x['desc'] = got.get(x['id'], '') or (x['desc'] if x['desc'] else '')
    if x['desc']: kept+=1
json.dump(c, open('catalogue_hf.json','w'), ensure_ascii=False, indent=1)
print(f'with description: {kept}/{len(c)}')
for x in c[:8]: print(f"  {x['id'][:38]:<38} {x['desc'][:80]}")
