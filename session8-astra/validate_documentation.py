"""Validate local Markdown links/fragments and sanitized Evidence ID membership.
No target execution, network access or Git mutation. Writes ignored local results.
"""
import json,pathlib,re,subprocess,sys,urllib.parse
R=pathlib.Path(__file__).resolve().parent.parent;S=R/'session8-astra';L=S/'.local';L.mkdir(exist_ok=True)
def outside_code(text):
 text=re.sub(r'```.*?```','',text,flags=re.S)
 return re.sub(r'`[^`\n]*`','',text)
def anchors(text):
 found=set(re.findall(r'<a\s+id="([^"]+)"',text));counts={}
 for title in re.findall(r'^#{1,6}\s+(.+?)\s*#*$',text,re.M):
  title=re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',title)
  slug=re.sub(r'[^\w\- ]','',title.lower()).replace(' ','-')
  n=counts.get(slug,0);counts[slug]=n+1;found.add(slug+(f'-{n}' if n else ''))
 return found
tracked=subprocess.check_output(['git','ls-files','-z'],cwd=R).decode().split('\0')
files={R/n for n in tracked if n.endswith('.md')};files.update(S.glob('*.md'));files.add(R/'README.md')
issues=[];checked=0;fragments=0;cache={}
for p in sorted(files):
 if not p.exists():issues.append(dict(file=p.relative_to(R).as_posix(),error='missing file'));continue
 text=outside_code(p.read_text(encoding='utf8'))
 for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',text):
  if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',url):continue
  path,_,fragment=url.partition('#');path=urllib.parse.unquote(path)
  target=(p.parent/path).resolve() if path else p
  checked+=1
  if not target.exists():issues.append(dict(file=p.relative_to(R).as_posix(),url=url,error='missing target'));continue
  if fragment and target.suffix=='.md':
   fragments+=1
   if target not in cache:cache[target]=anchors(target.read_text(encoding='utf8'))
   if urllib.parse.unquote(fragment) not in cache[target]:issues.append(dict(file=p.relative_to(R).as_posix(),url=url,error='missing fragment'))
index=S/'evidence-records.json';evidence_checked=0
if index.exists():
 d=json.loads(index.read_text());ids={x['evidence_id'] for x in d['native_records']}
 for p in S.glob('*.md'):
  for ev in re.findall(r'ev_[0-9a-f]{64}',p.read_text(encoding='utf8')):
   evidence_checked+=1
   if ev not in ids:issues.append(dict(file=p.name,error='unindexed Evidence ID',id=ev))
else:issues.append(dict(file='evidence-records.json',error='missing sanitized index'))
result=dict(markdown_files=len(files),local_links=checked,fragments=fragments,evidence_id_occurrences=evidence_checked,issues=issues,passed=not issues)
(L/'documentation-validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));sys.exit(0 if not issues else 1)
