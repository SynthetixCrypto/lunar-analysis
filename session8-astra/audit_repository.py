"""Read-only repository audit. Findings contain filenames/counts, never secret values.
Raw baseline and scan results are local-only. Does not read Git credential config.
"""
import hashlib,json,pathlib,re,subprocess,sys
R=pathlib.Path(__file__).resolve().parent.parent;L=R/'session8-astra/.local';L.mkdir(exist_ok=True)
def git(*args):return subprocess.check_output(['git',*args],cwd=R).decode('utf8',errors='replace')
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
tracked=git('ls-files','-z').split('\0');tracked=[x for x in tracked if x]
if not (L/'baseline.json').exists():
 baseline={n:digest(R/n) for n in tracked if (R/n).is_file()}
 (L/'baseline.json').write_text(json.dumps(baseline))
 baseline_status=git('status','--porcelain=v1');(L/'baseline-status.txt').write_text(baseline_status)
rows=[];broken=[];credential_names=[];patterns={
 'machine_path':re.compile(rb'(?:[A-Z]:[\\/](?:Users|tools|Program Files)|/Users/[^/]+/)'),
 'private_key_marker':re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
 'token_shape':re.compile(rb'(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|AKIA[A-Z0-9]{16})'),
 'decompiled_or_bytecode':re.compile(rb'(?:\bFUN_180[0-9a-f]+\s*\(|\binvokevirtual\s+#\d+|\braw_result\b.*\bpseudocode\b)')}
for n in tracked:
 p=R/n
 if not p.is_file():continue
 row=dict(path=n,bytes=p.stat().st_size,flags=[])
 if p.name.startswith('.env') or p.suffix.lower() in ['.pem','.key','.p12','.pfx','.jks'] or re.search(r'(credentials|secrets)',p.name,re.I):
  row['flags'].append('credential_filename_not_opened');credential_names.append(n);rows.append(row);continue
 if p.suffix.lower() in ['.exe','.dll','.jar','.class','.asar','.pak','.png','.jpg','.ttf','.woff','.zip','.node']:
  row['flags'].append('binary_or_asset_candidate')
 if p.stat().st_size>10*1024*1024:row['flags'].append('over_10_MiB')
 if p.suffix.lower() in ['.md','.txt','.json','.jsonl','.tsv','.py','.mjs']:
  b=p.read_bytes()
  for k,pat in patterns.items():
   if pat.search(b):row['flags'].append(k)
  if p.suffix=='.md':
   text=b.decode('utf8',errors='replace')
   text=re.sub(r'```.*?```','',text,flags=re.S)
   text=re.sub(r'`[^`\n]*`','',text)
   for link in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
    if re.match(r'^[a-zA-Z]+:',link) or link.startswith('#'):continue
    target=link.split('#')[0]
    if target and not (p.parent/target).exists():broken.append(dict(file=n,target=target))
 if row['flags']:rows.append(row)
objects=git('rev-list','--objects','--all').splitlines()
p=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objecttype) %(objectsize) %(rest)'],cwd=R,input='\n'.join(objects)+'\n',text=True,capture_output=True,check=True)
large=[]
for line in p.stdout.splitlines():
 a=line.split(' ',3)
 if len(a)>=3 and a[1]=='blob' and int(a[2])>10*1024*1024:large.append(dict(object=a[0],bytes=int(a[2]),path=a[3] if len(a)>3 else ''))
ignored=git('ls-files','-ci','--exclude-standard').splitlines()
result=dict(tracked_count=len(tracked),tracked_bytes=sum((R/n).stat().st_size for n in tracked if (R/n).is_file()),flagged=rows,credential_filenames_not_opened=credential_names,broken_links=broken,tracked_ignored=ignored,large_history_blobs=large,history_scope='Reachable object metadata only; no full historical content secret scan.',git_status=git('status','--short'))
candidate=set(n for n in ignored if pathlib.Path(n).suffix.lower()!='.md')
candidate.update(x['path'] for x in rows if pathlib.Path(x['path']).suffix.lower()!='.md' and any(k in x['flags'] for k in ['binary_or_asset_candidate','over_10_MiB','decompiled_or_bytecode']))
candidate=sorted(candidate)
(L/'untrack-candidates.txt').write_text('\n'.join(candidate)+'\n',encoding='utf8')
(L/'untrack-candidates.nul').write_bytes(b'\0'.join(n.encode('utf8') for n in candidate)+b'\0')
result['cleanup_candidate_count']=len(candidate)
result['cleanup_manifest_sha256']=digest(L/'untrack-candidates.nul')
(L/'audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(tracked_count=result['tracked_count'],tracked_bytes=result['tracked_bytes'],flag_counts={k:sum(k in x['flags'] for x in rows) for k in list(patterns)+['binary_or_asset_candidate','over_10_MiB','credential_filename_not_opened']},broken_links=len(broken),tracked_ignored=len(ignored),large_history_blobs=len(large),cleanup_candidates=len(candidate)),indent=2))
