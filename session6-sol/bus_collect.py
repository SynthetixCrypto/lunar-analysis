"""Focused static caller audit. Runs only javap, never target code."""
import analysis_helper as h
import re,json,sys,subprocess,zipfile,hashlib
O=h.OUT/'evidence-bus';O.mkdir(exist_ok=True)
C=h.cache(); A={h.short(n):n for n in C}
def dump(alias):
 n=A[alias]; t=C[n]; stem=alias.replace('$','--')
 (O/(stem+'.aliases.txt')).write_text(h.short(t),encoding='utf8')
 jars=[h.pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver')/x for x in ['lunar.jar','modern-0.1.0-SNAPSHOT-all-nomappings.jar','common-0.1.0-SNAPSHOT-all-nomappings.jar','genesis.jar']]
 member=n.replace('.','/')+'.class'
 jar=next(p for p in jars if p.exists() and member in zipfile.ZipFile(p).namelist())
 r=subprocess.run(['C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/javap.exe','-p','-c','-v','-classpath',str(jar),n],capture_output=True,text=True,encoding='utf8',check=True)
 (O/(stem+'.verbose.txt')).write_text(r.stdout,encoding='utf8')
 return {'class':n,'alias':alias,'artifact':str(jar),'class_sha256':hashlib.sha256(zipfile.ZipFile(jar).read(member)).hexdigest(),'raw':stem+'.verbose.txt'}
if sys.argv[1]=='collect':
 pats=[r'L/_d4ca6c/_(?:590f69|cfe983)\._ef97c4:\(\)Ljava/util/HashMap;',r'L/_d4ca6c/_(?:590f69|cfe983)\._bb4487:\(Ljava/lang/Class;Ljava/util/function/Consumer;\)V',r'L/_d4ca6c/_(?:590f69|cfe983)\._cfe983:\(Ljava/lang/Class;Ljava/lang/Class;Ljava/util/function/Function;Ljava/lang/Runnable;\)V',r'L/_d4ca6c/_(?:590f69|cfe983)\._(?:13ea87|57e17e):']
 hits=[];names=set()
 for n,t in C.items():
  for b in h.blocks(h.short(t)):
   if any(re.search(p,b) for p in pats):
    hits.append({'class':n,'alias':h.short(n),'method':b.splitlines()[0],'code':b});names.add(h.short(n))
 (O/'focused-callers.json').write_text(json.dumps({'cached_classes':len(C),'patterns':pats,'matches':hits},indent=2),encoding='utf8')
 for a in ['L._d4ca6c._590f69','L._d4ca6c._cfe983','L._767dc1._590f69','L._767dc1._1e73d7']:names.add(a)
 manifest=[dump(a) for a in sorted(names)]
 (O/'focused-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
 print(json.dumps([{k:v for k,v in x.items() if k!='code'} for x in hits],indent=2))
elif sys.argv[1]=='show':
 alias,pat=sys.argv[2:]
 for b in h.blocks(h.short(C[A[alias]])):
  if re.search(pat,b.splitlines()[0]): print(b)
