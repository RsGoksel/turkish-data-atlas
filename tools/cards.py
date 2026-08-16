import json, os, re, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
TOK=open('/home/goksel/.cache/huggingface/token').read().strip() if os.path.exists('/home/goksel/.cache/huggingface/token') else None
H={'User-Agent':'tr-datasets-catalogue'}
if TOK: H['Authorization']=f'Bearer {TOK}'

SKIP = re.compile(r'^\s*(#|---|\||!\[|<|\[!|license|task_categories|language|tags:|size_categories|configs|dataset_info|annotations|pretty_name|source_datasets|\*\*?\s*$)', re.I)

def summary(x):
    if x['desc']: return x['id'], x['desc']
    try:
        req=urllib.request.Request(f"https://huggingface.co/datasets/{x['id']}/raw/main/README.md", headers=H)
        with urllib.request.urlopen(req, timeout=20) as r:
            txt=r.read().decode('utf-8','ignore')
    except Exception:
        return x['id'], ''
    # YAML front-matter'i at
    if txt.lstrip().startswith('---'):
        parts=txt.split('---',2)
        txt=parts[2] if len(parts)>2 else txt
    for line in txt.splitlines():
        s=line.strip()
        if not s or SKIP.match(s): continue
        s=re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', s)
        s=re.sub(r'[*`_#>]', '', s).strip()
        if len(s) < 25 or 'http' in s: continue
        return x['id'], s[:230]
    return x['id'], ''

c=json.load(open('catalogue_hf.json'))
with ThreadPoolExecutor(max_workers=10) as ex:
    got=dict(ex.map(summary, c))
n=0
for x in c:
    if not x['desc'] and got.get(x['id']):
        x['desc']=got[x['id']]; n+=1
json.dump(c, open('catalogue_hf.json','w'), ensure_ascii=False, indent=1)
print(f'card summaries added: {n}  |  total with description: {sum(1 for x in c if x["desc"])}/{len(c)}')
