"""Index retained evidence and validate research deliverables. Static reads only."""
import gc,hashlib,json,pathlib,re
R=pathlib.Path(__file__).resolve().parent
REPORTS=['research-onboarding.md','ghidra-verification.md','native-jni-mapping.md','webosr-rendering.md','native-threading-lifecycle.md','cross-language-contracts.md','evidence-index.md','remaining-gaps.md','session-summary.md']
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def rel(p):return p.relative_to(R).as_posix()
def esc(s):return str(s).replace('|','&#124;').replace('\n',' ')
rows=[];other=[];errors=[];known=set();badjson=[];json_count=0
for p in sorted((R/'evidence').glob('*.json')):
 d=json.loads(p.read_text(encoding='utf8'))
 if not isinstance(d,dict):continue
 s=d.get('structuredContent',{})
 if not isinstance(s,dict):continue
 if s.get('evidence_id'):
  n=s.get('normalized_result',{})
  address=n.get('procedure',{}).get('address') if isinstance(n,dict) and isinstance(n.get('procedure'),dict) else None
  address=address or s.get('parameters',{}).get('address') or s.get('parameters',{}).get('procedure') or ''
  rows.append(dict(file=rel(p),id=s['evidence_id'],operation=s.get('operation',''),address=address,artifact=pathlib.PureWindowsPath(s.get('subject',{}).get('name','')).name))
  known.add(s['evidence_id'])
 else:
  status='Receipt or local derived data'
  if s.get('error') or d.get('isError'):
   status='Tool error/coverage boundary (not a successful finding)';errors.append(rel(p))
  other.append((rel(p),status))
bundle_info=[];bundle_only=[]
for name in ['binding-evidence-bundle.json','binding-final-evidence-bundle.json','ultralight-evidence-bundle.json']:
 d=json.loads((R/name).read_text(encoding='utf8'))
 records=d.get('records',[]);bundle_info.append((name,len(records),len(d.get('unknowns',[]))))
 for s in records:
  eid=s.get('evidence_id')
  if eid and eid not in known:
   bundle_only.append(dict(file=name,id=eid,operation=s.get('operation',''),address=s.get('parameters',{}).get('address') or s.get('parameters',{}).get('procedure') or '',artifact=pathlib.PureWindowsPath(s.get('subject',{}).get('name','')).name));known.add(eid)
 del d,records
 gc.collect()
lines=['# Session 7 — Evidence index','','Date: 2026-10-12. This index maps exact retained Evidence IDs to raw MCP envelopes or exported bundle records. Addresses are provider virtual addresses, not file offsets. Read each envelope\'s limitations and target digest before reusing it.','',
'## Foundational local evidence','',
'- [PE identities, exports and sections](evidence/pe-identities.json): independently parsed installed DLL bytes.',
'- [JNI reconciliation](evidence/jni-reconciliation-fresh.json): class-file native declarations and full mapping.',
'- [JNI ABI offsets](evidence/jni-abi-offsets.json): indexed installed JDK header and its digest.',
'- [Registration search bounds](evidence/registration-bounded-scan.json): four DLL ASCII searches and binding .text byte candidates.',
'- [Texture class hash checks](evidence/java-hash-verification.json) and [lifecycle class checks](evidence/lifecycle-fresh-hashes.json): original identities reused only as leads, fresh byte reads agree.',
'- Fresh `*.javap.txt` files under `evidence/`: static Java bytecode, descriptors and original class names. No target class initialization was performed.',
'- [Content manifest](file-manifest.json) and [validation result](validation.json): SHA-256 and integrity checks for retained files. These are local validation records, not REA Evidence IDs.','',
'## Exported bundles and snapshots','',
'| Bundle | Records reported in file | Unknown records |','|---|---:|---:|']
for n,count,unknowns in bundle_info:lines.append(f'| [{n}]({n}) | {count} | {unknowns} |')
lines += ['','Bundle unknown-record counts are REA ledger metadata, not counts of research questions left open. See [remaining gaps](remaining-gaps.md) for substantive unknowns.',
'', '[Binding initial snapshot](binding-analysis-snapshot.json), [binding final snapshot](binding-final-analysis-snapshot.json), [Ultralight snapshot](ultralight-analysis-snapshot.json). Full request inputs and completion receipts are in the root batch files and `queue/`.',
'', '## Raw response Evidence records', '', f'{len(rows)} envelopes below contain inline Evidence. Duplicate Evidence IDs may legitimately occur when the same observation was requested more than once. The complete unique set including bundle-only records has {len(known)} IDs.',
'', '| Raw response | Binary | Operation / location | Evidence ID |','|---|---|---|---|']
for row in rows:
 lines.append(f"| [{pathlib.Path(row['file']).stem}]({row['file']}) | {esc(row['artifact'])} | {esc(row['operation'])} `{esc(row['address'])}` | `{row['id']}` |")
lines += ['','## Records retained through exported bundles','',
'Some large tool responses hit transport limits; the analysis record is retained in the exported bundle rather than reconstructed from a truncated preview. The bundle record with the exact ID below is the evidence authority.',
'','| Bundle | Binary | Operation / location | Evidence ID |','|---|---|---|---|']
for row in bundle_only:lines.append(f"| [{row['file']}]({row['file']}) | {esc(row['artifact'])} | {esc(row['operation'])} `{esc(row['address'])}` | `{row['id']}` |")
lines += ['','## Lifecycle receipts, local data and unsuccessful tool boundaries','','An MCP envelope can have `isError: false` while its structured payload reports an operation error. These files are not automatically positive evidence of the requested operation.','', '| File | Classification |','|---|---|']
for name,status in other:lines.append(f'| [{pathlib.Path(name).name}]({name}) | {status} |')
lines += ['','## Interpretation and coverage rules','',
'- **Verified** means static artifact evidence, not observed runtime execution. **Inferred** conclusions and **Unknown** questions are labeled in the reports.',
'- Analyst filenames can be exploratory guesses. [Corrections](ghidra-verification.md) identify misleading names and their authoritative replacements.',
'- `views/` files project pseudocode/table values for readability. Full raw/normalized results, profile metadata and limitations stay in the JSON envelope or bundle.',
'- No claim of universal absence follows from a bounded negative string, byte or direct-reference search.',
'- JSON syntax and file hashes are validated locally; this script does not independently recompute REA canonical Evidence IDs or certify a decompiler result.',
'- Snapshots contain retained analysis products; they are not original executable modifications or a persistent GUI database.','']
(R/'evidence-index.md').write_text('\n'.join(lines),encoding='utf8')
broken=[];links=0
for name in REPORTS:
 p=R/name
 if not p.exists():broken.append(dict(report=name,target='MISSING REPORT'));continue
 for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',p.read_text(encoding='utf8')):
  if re.match(r'^[a-zA-Z]+://',target) or target.startswith('#'):continue
  target=target.split('#',1)[0];links+=1
  if target in ['validation.json','file-manifest.json']:continue
  if not (R/target).exists():broken.append(dict(report=name,target=target))
for p in sorted(R.rglob('*.json')):
 if p.name in ['validation.json','file-manifest.json']:continue
 try:
  with p.open(encoding='utf8') as f: obj=json.load(f)
  json_count+=1;del obj
 except (ValueError,UnicodeError) as e:badjson.append(dict(file=rel(p),error=str(e)))
 gc.collect()
identities=json.loads((R/'evidence/pe-identities.json').read_text());target_checks=[]
for x in identities:
 p=pathlib.Path(x['path']);actual=sha(p);target_checks.append(dict(path=str(p),expected=x['sha256'],actual=actual,matches=actual==x['sha256']))
j=json.loads((R/'evidence/jni-reconciliation-fresh.json').read_text());jp=pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver/lunar.jar');jh=sha(jp)
target_checks.append(dict(path=str(jp),expected=j['jar_sha256'],actual=jh,matches=jh==j['jar_sha256']))
validation=dict(date='2026-10-12',reports=REPORTS,report_count=len(REPORTS),local_links_checked=links,broken_links=broken,json_files_parsed=json_count,json_errors=badjson,inline_evidence_envelopes=len(rows),unique_evidence_ids=len(known),bundle_only_records=len(bundle_only),structured_tool_error_files=errors,target_hash_checks=target_checks,limits=['JSON syntax/structure and file digests checked; REA canonical Evidence IDs not independently recalculated.','Report semantic conclusions depend on cited static analysis; no target execution.'])
class_checks=json.loads((R/'evidence/java-hash-verification.json').read_text())+json.loads((R/'evidence/lifecycle-fresh-hashes.json').read_text())
validation['selected_class_hash_checks']=len(class_checks)
validation['selected_class_hashes_match']=all(x['matches'] for x in class_checks)
validation['jni_counts_verified']={k:j[k] for k in ['java_count','dll_count','shared_count']}
validation['passed']=not broken and not badjson and all(x['matches'] for x in target_checks) and validation['selected_class_hashes_match'] and (j['java_count'],j['dll_count'],j['shared_count'])==(56,58,55)
(R/'validation.json').write_text(json.dumps(validation,indent=2),encoding='utf8')
manifest=[]
for p in sorted(R.rglob('*')):
 if not p.is_file() or p.name=='file-manifest.json' or '__pycache__' in p.parts:continue
 manifest.append(dict(path=rel(p),bytes=p.stat().st_size,sha256=sha(p)))
(R/'file-manifest.json').write_text(json.dumps(dict(exclusions=['file-manifest.json (self-reference)','__pycache__ (interpreter cache)'],files=manifest),indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in validation.items() if k!='target_hash_checks'},indent=2))
print('Manifest:',len(manifest),'files;',sum(x['bytes'] for x in manifest),'bytes; target hashes:',all(x['matches'] for x in target_checks))
if not validation['passed']:raise SystemExit(1)
