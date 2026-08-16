import json, os, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
TOK=open('/home/goksel/.cache/huggingface/token').read().strip() if os.path.exists('/home/goksel/.cache/huggingface/token') else None
H={'User-Agent':'tr-datasets-catalogue'}
if TOK: H['Authorization']=f'Bearer {TOK}'
def one(x):
    try:
        req=urllib.request.Request(f"https://huggingface.co/api/datasets/{x['id']}", headers=H)
        with urllib.request.urlopen(req, timeout=25) as r: info=json.load(r)
    except Exception:
        return x['id'], None
    langs=[t.split(':',1)[1] for t in info.get('tags',[]) if t.startswith('language:')]
    if not langs:
        cd=(info.get('cardData') or {}).get('language')
        langs=cd if isinstance(cd,list) else ([cd] if cd else [])
    return x['id'], langs
c=json.load(open('catalogue_hf.json'))
with ThreadPoolExecutor(max_workers=8) as ex:
    res=dict(ex.map(one, c))
for x in c:
    L=res.get(x['id'])
    x['n_langs']=len(L) if L is not None else None
    x['multilingual']= (len(L)>1) if L else False
json.dump(c, open('catalogue_hf.json','w'), ensure_ascii=False, indent=1)
mono=[x for x in c if not x['multilingual'] and x['bytes']]
multi=[x for x in c if x['multilingual'] and x['bytes']]
print(f"monolingual (tr-only): {len(mono)} entries, {sum(x['bytes'] for x in mono)/1e12:.2f} TB")
print(f"multilingual         : {len(multi)} entries, {sum(x['bytes'] for x in multi)/1e12:.2f} TB (ALL languages)")
print(f"no language tag      : {sum(1 for x in c if x['n_langs'] in (0,None))}")
