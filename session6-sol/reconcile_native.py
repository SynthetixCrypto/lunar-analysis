"""PE-byte identity and class constant-pool reference checks; no target execution."""
import pathlib,json,hashlib,struct,zipfile
ROOT=pathlib.Path(__file__).resolve().parent.parent;O=ROOT/'session6-sol/evidence-native';O.mkdir(exist_ok=True)
prior=json.loads((ROOT/'session4-sol/evidence-native/binding-pe-addresses.json').read_text())
print('EXPORT SAMPLE',prior['exports'][0])
decl=json.loads((O/'jni-declarations.json').read_text())['declarations']
exports={r['name'] for r in prior['exports']};java={r['symbol'] for r in decl}
out={'java_count':len(decl),'export_count':len(exports),'shared':len(java&exports),'java_only':sorted(java-exports),'dll_only':sorted(exports-java),'authority':'Java declarations + retained PE table, fresh DLL digest checked separately'}
dll=pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver/natives/WebOSR-Binding.dll');data=dll.read_bytes()
out['dll_sha256']=hashlib.sha256(data).hexdigest();out['matches_prior_sha256']=out['dll_sha256']==prior['sha256']
(O/'jni-reconciliation.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(json.dumps(out,indent=2))
def methodrefs(b):
 p=10;count=struct.unpack_from('>H',b,8)[0];cp=[None]*count;i=1
 while i<count:
  tag=b[p];p+=1
  if tag==1:
   z=struct.unpack_from('>H',b,p)[0];p+=2;cp[i]=(tag,b[p:p+z].decode('utf8',errors='replace'));p+=z
  elif tag in [7,8,16,19,20]:cp[i]=(tag,struct.unpack_from('>H',b,p)[0]);p+=2
  elif tag in [9,10,11,12,17,18]:cp[i]=(tag,*struct.unpack_from('>HH',b,p));p+=4
  elif tag in [3,4]:p+=4
  elif tag in [5,6]:p+=8;i+=1
  elif tag==15:p+=3
  else:raise ValueError(tag)
  i+=1
 def utf(i):return cp[i][1]
 refs=[]
 for i,r in enumerate(cp):
  if r and r[0] in [10,11]:
   owner=utf(cp[r[1]][1]);nat=cp[r[2]]
   if owner=='com/moonsworth/webosr/wrappers/Session':refs.append({'constant_pool_index':i,'owner':owner,'method':utf(nat[1]),'descriptor':utf(nat[2])})
 return refs
rows=[];scope=[]
base=pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver')
for name in ['lunar.jar','modern-0.1.0-SNAPSHOT-all-nomappings.jar','common-0.1.0-SNAPSHOT-all-nomappings.jar','genesis-0.1.0-SNAPSHOT-all.jar']:
 jar=base/name;z=zipfile.ZipFile(jar);count=0
 for e in z.infolist():
  if not e.filename.endswith('.class'):continue
  b=z.read(e);count+=1
  if b'com/moonsworth/webosr/wrappers/Session' not in b:continue
  refs=methodrefs(b)
  if refs:rows.append({'artifact':name,'class_member':e.filename,'class_sha256':hashlib.sha256(b).hexdigest(),'references':refs})
 scope.append({'artifact':str(jar),'sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'class_count':count})
scan={'scope':scope,'matches':rows,'name_method_references':[r for r in rows if any(x['method']=='name' for x in r['references'])],'limitations':['Constant-pool method references include symbolic references, not proof of executed invocation.','Excludes reflection, JNI-table resolution, external code and other artifacts.']}
(O/'session-methodrefs.json').write_text(json.dumps(scan,indent=2),encoding='utf8');print('SESSION METHODREFS',json.dumps(scan,indent=2))
