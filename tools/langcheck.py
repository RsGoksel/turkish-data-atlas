import json, os, urllib.request
from concurrent.futures import ThreadPoolExecutor
TOK=open('/home/goksel/.cache/huggingface/token').read().strip() if os.path.exists('/home/goksel/.cache/huggingface/token') else None
H={'User-Agent':'tr-data-atlas'}
if TOK: H['Authorization']=f'Bearer {TOK}'
def langs(i):
    try:
        req=urllib.request.Request(f'https://huggingface.co/api/datasets/{i}', headers=H)
        d=json.load(urllib.request.urlopen(req, timeout=25))
    except Exception: return i, None
    L=[t.split(':',1)[1] for t in d.get('tags',[]) if t.startswith('language:')]
    if not L:
        cd=(d.get('cardData') or {}).get('language')
        L=cd if isinstance(cd,list) else ([cd] if cd else [])
    return i, L
full=json.load(open('datasets.full.json'))
hf=[x for x in full['datasets'] if x['host']=='huggingface']
with ThreadPoolExecutor(max_workers=10) as ex:
    got=dict(ex.map(langs, [x['id'] for x in hf]))
TR={'tr','tur','tr-TR','turkish'}
for x in hf:
    L=got.get(x['id'])
    x['langs']=L
    x['n_langs']=len(L) if L is not None else None
    x['multilingual']= bool(L) and len(L)>1
    # YENI: tek-dilli hacim yalnizca dili Turkce olanlari sayar
    x['turkish_only'] = bool(L) and len(L)==1 and L[0] in TR
json.dump(full, open('datasets.full.json','w'), ensure_ascii=False, indent=1)

mono_old=[x for x in hf if not x['multilingual'] and x.get('bytes')]
tr_only =[x for x in hf if x.get('turkish_only') and x.get('bytes')]
print(f"eski 'tek-dilli'  : {len(mono_old):>3} set  {sum(x['bytes'] for x in mono_old)/1e12:.2f} TB")
print(f"gercekten TR      : {len(tr_only):>3} set  {sum(x['bytes'] for x in tr_only)/1e12:.2f} TB")
bad=[x for x in mono_old if not x.get('turkish_only')]
bad.sort(key=lambda x:-x['bytes'])
print(f"\nyanlis sayilanlar (tek dilli ama Turkce degil) — ilk 8:")
for x in bad[:8]:
    print(f"  {x['bytes']/1e9:8.1f} GB  {x['id'][:44]:<44} lang={x.get('langs')}")
