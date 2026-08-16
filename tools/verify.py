"""Verify every extracted dataset against the Hugging Face API.

The point of this catalogue is that its numbers are checked, not copied from cards.
Anything the API cannot confirm is marked unverified rather than guessed.
"""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.error

TOK = open('/home/goksel/.cache/huggingface/token').read().strip() if __import__('os').path.exists('/home/goksel/.cache/huggingface/token') else None
H = {'User-Agent': 'tr-datasets-catalogue'}
if TOK: H['Authorization'] = f'Bearer {TOK}'

def get(url, timeout=25):
    try:
        req = urllib.request.Request(url, headers=H)
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r), r.status
    except urllib.error.HTTPError as e:
        return None, e.code
    except Exception:
        return None, 0

def one(rec):
    i = rec['id']
    info, code = get(f'https://huggingface.co/api/datasets/{i}')
    out = dict(rec); out['http'] = code
    if not info:
        out['status'] = 'gone' if code == 404 else ('gated' if code in (401, 403) else 'unreachable')
        return out
    card = info.get('cardData') or {}
    lic = card.get('license')
    if isinstance(lic, list): lic = lic[0] if lic else None
    if not lic:
        lic = next((t.split(':', 1)[1] for t in info.get('tags', []) if t.startswith('license:')), None)
    out.update(status='ok',
               downloads=info.get('downloads'), likes=info.get('likes'),
               modified=(info.get('lastModified') or '')[:10],
               license=lic, gated=bool(info.get('gated')),
               tags=[t for t in info.get('tags', []) if t.startswith(('task_categories:', 'language:', 'modality:'))][:12])
    sz, c = get(f'https://datasets-server.huggingface.co/size?dataset={i}')
    if sz:
        try:
            s = sz['size']['dataset']
            out['bytes'] = s.get('num_bytes_original_files') or s.get('num_bytes_parquet_files')
            out['rows'] = s.get('num_rows')
        except Exception:
            pass
    return out

recs = json.load(open('extracted.json'))
with ThreadPoolExecutor(max_workers=8) as ex:
    res = list(ex.map(one, recs))
json.dump(res, open('verified.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(r['status'] for r in res))
print('with size:', sum(1 for r in res if r.get('bytes')))
