"""Validate Session 6 citations against read-only shipped classes; never execute targets."""
from pathlib import Path
import hashlib,json,re,zipfile

BASE=Path(__file__).resolve().parent
def sha(b): return hashlib.sha256(b).hexdigest()
rows=[]
for directory in ('evidence-reach','evidence-potion','evidence-armor','evidence-native','evidence-bus','evidence-support','evidence-rpc','evidence-functionbus'):
    for p in (BASE/directory).glob('*.json'):
        d=json.loads(p.read_text(encoding='utf-8-sig'))
        candidates=d if isinstance(d,list) else d.get('classes',d.get('evidence',[d])) if isinstance(d,dict) else []
        if not isinstance(candidates,list):candidates=[d]
        for x in candidates:
            if not isinstance(x,dict): continue
            name=x.get('class') or x.get('actual_class')
            artifact=x.get('artifact') or (d.get('artifact') if isinstance(d,dict) else None)
            evidence=x.get('evidence') or x.get('file')
            if name and artifact and isinstance(evidence,str):
                rows.append((p,x,name,artifact,evidence))
archives={}; checked=[]; errors=[]
for p,x,name,artifact,evidence in rows:
    ap=Path(artifact)
    if artifact not in archives: archives[artifact]=zipfile.ZipFile(ap)
    try: raw=archives[artifact].read(name.replace('.','/')+'.class')
    except KeyError:
        errors.append({'manifest':str(p.relative_to(BASE)),'class':name,'error':'class absent from referenced artifact'})
        continue
    h=sha(raw)
    if x.get('class_sha256') and x['class_sha256']!=h:
        errors.append({'manifest':str(p.relative_to(BASE)),'class':name,'error':'class SHA mismatch'})
    ep=p.parent/evidence
    if not ep.exists(): errors.append({'manifest':str(p.relative_to(BASE)),'error':'evidence file missing','file':evidence})
    if ep.exists() and p.parent.name in ('evidence-support','evidence-functionbus') and x.get('sha256') and x['sha256']!=sha(ep.read_bytes()):
        errors.append({'manifest':str(p.relative_to(BASE)),'class':name,'error':'disassembly output SHA mismatch'})
    checked.append({'manifest':p.relative_to(BASE).as_posix(),'class':name,'alias':x.get('alias'),'artifact':str(ap),'class_sha256':h,'evidence':ep.relative_to(BASE).as_posix(),'evidence_sha256':sha(ep.read_bytes()) if ep.exists() else None,'manifest_hash_field_kind':'class bytes' if 'class_sha256' in x else 'see original schema; supplemental class hash supplied here'})
for z in archives.values():z.close()
core=['java-gap-resolution.md','native-rendering-analysis.md','jni-and-webosr.md','additional-findings.md','evidence-index.md','remaining-unknowns.md','session-summary.md']
for f in core:
    if not (BASE/f).is_file() or not (BASE/f).stat().st_size:errors.append({'error':'missing/empty core report','file':f})
links=0
for p in BASE.glob('*.md'):
    text=p.read_text(encoding='utf-8')
    for target in re.findall(r'\]\(([^\n)]+)\)',text):
        target=target.strip('<>').split('#')[0]
        if not target or re.match(r'\w+://',target):continue
        links+=1
        if not (p.parent/target).exists():errors.append({'error':'broken link','report':p.name,'target':target})
out={'analysis':'read-only ZIP class hashing and local citation validation; no target execution','checked_class_manifest_rows':len(checked),'markdown_links_checked':links,'errors':errors,'classes':checked}
(BASE/'evidence-validation.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
files=[]
for p in sorted(BASE.rglob('*')):
    if p.is_file() and '__pycache__' not in p.parts and p.name not in ('evidence-integrity.json','validation-output.txt'):
        files.append({'path':p.relative_to(BASE).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())})
(BASE/'evidence-integrity.json').write_text(json.dumps({'algorithm':'SHA-256','scope':'Session 6 reports/helpers/evidence; excludes this self-manifest, transient pycache and validation-output.txt','files':files},indent=2),encoding='utf-8')
print(json.dumps({'checked_class_manifest_rows':len(checked),'markdown_links_checked':links,'hashed_files':len(files),'errors':errors}))
raise SystemExit(1 if errors else 0)
