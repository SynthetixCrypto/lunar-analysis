"""Static Java/native ABI follow-up. No target loading or execution."""
import analysis_helper as h
import json,re,subprocess,hashlib,zipfile,sys
O=h.OUT/'evidence-native';O.mkdir(exist_ok=True)
C=h.cache();A={h.short(n):n for n in C}
def save(n):
 alias=h.short(n);stem=alias.replace('$','--');member=n.replace('.','/')+'.class'
 jars=[h.pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver')/x for x in ['lunar.jar','modern-0.1.0-SNAPSHOT-all-nomappings.jar','common-0.1.0-SNAPSHOT-all-nomappings.jar','genesis.jar']]
 jar=next(p for p in jars if p.exists() and member in zipfile.ZipFile(p).namelist())
 t=subprocess.run(['C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/javap.exe','-p','-c','-v','-classpath',str(jar),n],capture_output=True,text=True,encoding='utf8',check=True).stdout
 (O/(stem+'.verbose.txt')).write_text(t,encoding='utf8');(O/(stem+'.aliases.txt')).write_text(h.short(t),encoding='utf8')
 (O/(stem+'.code.txt')).write_text(h.short(C.get(n,t)),encoding='utf8')
 return {'class':n,'alias':alias,'artifact':str(jar),'class_sha256':hashlib.sha256(zipfile.ZipFile(jar).read(member)).hexdigest(),'evidence':stem+'.verbose.txt'}
op,*args=sys.argv[1:]
if op=='collect':
 aliases=['L._81676d._21aca6._590f69._cfe983._cfe983','ML._d4ca6c._1e73d7._590f69._88f3cf._2f4182._cfe983','L._81676d._21aca6._21aca6._cfe983','com.moonsworth.webosr.wrappers.Session','com.moonsworth.webosr.wrappers.PromiseJS','com.moonsworth.webosr.javascript.FunctionBus']
 manifest=[save(A[a]) for a in aliases]
 (O/'class-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
 refs=[]
 for n,t in C.items():
  for b in h.blocks(h.short(t)):
   if re.search(r'(?:wrappers/Session\.(?:name|getName):|bridge\$uploadBgra|lunar\$uploadOpenGl|lunar\$uploadCompactRgba|wrappers/(?:WebEngine|Browser)\.(?:close|destroy):)',b): refs.append({'class':n,'alias':h.short(n),'method':b.splitlines()[0],'code':b})
 (O/'boundary-call-sites.json').write_text(json.dumps({'cache_classes':len(C),'matches':refs},indent=2),encoding='utf8')
 declarations=[]
 for n,t in C.items():
  if n.startswith('com.moonsworth.webosr.'):
   for l in t.splitlines():
    if re.match(r'  (?:public|protected|private).*\bnative\b',l):
     method=re.search(r'(\w+)\(',l)[1]
     declarations.append({'class':n,'declaration':l.strip(),'symbol':'Java_'+n.replace('.','_')+'_'+method})
 prior=json.loads((h.ROOT/'session4-sol/evidence-native/binding-pe-addresses.json').read_text())
 (O/'jni-declarations.json').write_text(json.dumps({'declarations':declarations,'count':len(declarations),'note':'Compare exact symbols with retained shipped PE export table; static declarations only.'},indent=2),encoding='utf8')
 print('Saved',len(manifest),'fresh classes;',len(refs),'call-site blocks;',len(declarations),'native declarations; PE keys',list(prior))
elif op=='show':
 a,pat=args
 for b in h.blocks(h.short(C[A[a]])):
  if re.search(pat,b.splitlines()[0]):print(b)
elif op=='refs':
 pat,label=args;rows=[]
 for n,t in C.items():
  for b in h.blocks(h.short(t)):
   if re.search(pat,b):rows.append({'class':n,'alias':h.short(n),'method':b.splitlines()[0],'code':b})
 (O/(label+'.json')).write_text(json.dumps({'cached_classes':len(C),'pattern':pat,'matches':rows},indent=2),encoding='utf8')
 print(json.dumps([{k:v for k,v in r.items() if k!='code'} for r in rows],indent=2))
elif op=='save':
 rows=[save(A[a]) for a in args]
 (O/'lifecycle-manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
 print(json.dumps(rows,indent=2))
