"""Turn the verified records into the catalogue the Space renders."""
import json, re
from collections import Counter

COMMERCIAL = {'cc0-1.0','cc-by-4.0','cc-by-3.0','cc-by-2.0','mit','apache-2.0','bsd','odc-by',
              'cc-by-sa-4.0','cc-by-sa-3.0','openrail','bsd-3-clause','gpl-3.0','lgpl-3.0','unlicense','wtfpl'}
NONCOMM   = {'cc-by-nc-4.0','cc-by-nc-sa-4.0','cc-by-nc-2.0','cc-by-nc-nd-4.0','cc-by-nc-sa-3.0','other'}

TASK = [
 ('asr','automatic-speech-recognition'), ('tts','text-to-speech'), ('audio','audio-classification'),
 ('ocr','image-to-text'), ('vqa','visual-question-answering'), ('detection','object-detection'),
 ('image','image-classification'), ('image','image-segmentation'), ('image','text-to-image'),
 ('translation','translation'), ('summarisation','summarization'), ('qa','question-answering'),
 ('classification','text-classification'), ('ner','token-classification'),
 ('instruction','text2text-generation'), ('pretraining','text-generation'),
 ('embedding','sentence-similarity'), ('embedding','feature-extraction'),
]

def modality(r):
    t = ' '.join(r.get('tags') or [])
    if 'modality:audio' in t: return 'speech'
    if 'modality:image' in t or 'image' in t or 'ocr' in r['id'].lower(): return 'vision'
    if 'vision' in r['cats']: return 'vision'
    if 'speech' in r['cats']: return 'speech'
    return 'llm'

def task(r):
    t = ' '.join(r.get('tags') or [])
    for label, key in TASK:
        if f'task_categories:{key}' in t: return label
    return {'speech':'asr','vision':'ocr','llm':'corpus'}[modality(r)]

def posture(lic):
    if not lic: return 'unverified'
    l = lic.lower()
    if l in COMMERCIAL: return 'commercial'
    if l in NONCOMM or 'nc' in l.split('-'): return 'non-commercial'
    return 'unverified'

def desc(r):
    """En bilgilendirici tablo hucresini sec: kimlik/sayi/lisans olmayan en uzun metin."""
    best = ''
    for c in (r.get('cells') or []):
        c = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', c).replace('`','').strip()
        if len(c) < 18 or 'huggingface.co' in c: continue
        if re.fullmatch(r'[\d\s.,~%kKMGBhtoken+\-/()]*', c): continue
        if len(c) > len(best): best = c
    return best[:260]

recs = json.load(open('verified.json'))
out = []
for r in recs:
    if r['status'] != 'ok':
        continue
    m = modality(r)
    out.append({
        'id': r['id'], 'url': f"https://huggingface.co/datasets/{r['id']}", 'host': 'huggingface',
        'modality': m, 'task': task(r), 'desc': desc(r),
        'license': r.get('license'), 'posture': posture(r.get('license')),
        'gated': r.get('gated', False),
        'bytes': r.get('bytes'), 'rows': r.get('rows'),
        'downloads': r.get('downloads'), 'likes': r.get('likes'),
        'modified': r.get('modified'), 'verified': '2026-08-16',
    })
out.sort(key=lambda x: (-(x['downloads'] or 0), x['id']))
json.dump(out, open('catalogue_hf.json','w'), ensure_ascii=False, indent=1)
print('entries:', len(out))
print('modality:', Counter(x['modality'] for x in out))
print('posture :', Counter(x['posture'] for x in out))
print('with desc:', sum(1 for x in out if x['desc']))
tb = sum(x['bytes'] or 0 for x in out)/1e12
print(f'verified volume: {tb:.2f} TB across {sum(1 for x in out if x["bytes"])} sized entries')
