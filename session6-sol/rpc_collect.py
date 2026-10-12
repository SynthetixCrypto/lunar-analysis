"""Static RPC caller evidence collection, never executes target classes."""
from pathlib import Path
import json,pickle,re,hashlib,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'session6-sol'/'evidence-rpc'; OUT.mkdir(exist_ok=True)
S=Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
C=pickle.loads((S/'classes.pkl').read_bytes())
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def short(t): return TOK.sub(lambda m:'_'+hashlib.md5(m.group().encode()).hexdigest()[:6],t.replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/client/','L/'))
def blocks(t):return re.findall(r'^  (?:public|private|protected|static).*?(?=^  (?:public|private|protected|static)|^\}\s*$|\Z)',t,re.M|re.S)
JAR=Path(r'C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar')
JAVAP=r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe'
def dump(n,verbose=False,jar=JAR):
 return subprocess.run([JAVAP,'-J-Dfile.encoding=UTF-8','-classpath',str(jar),'-p','-c']+(['-v'] if verbose else [])+[n],capture_output=True,text=True,encoding='utf8',check=True).stdout
def write(n,t): (OUT/n).write_text(t,encoding='utf8')
def main():
 op,*args=sys.argv[1:]
 if op=='collect':
  rows=json.loads((ROOT/'session4-sol/evidence-rpc/bounded-future-search.json').read_text())['methods']
  names=list(dict.fromkeys(r['class'] for r in rows)); manifest=[]
  for i,n in enumerate(names):
   t=dump(n); b=blocks(t)
   if i==0: b=[x for x in b if x.splitlines()[0].strip() in [r['signature'] for r in rows if r['class']==n] or 'Response)' in x.splitlines()[0]]
   fn=f'caller-{i:02}.javap.txt'; write(fn,'\n'.join(b));write(fn+'.aliases.txt',short('\n'.join(b)))
   v=dump(n,True);v=v[v.index('BootstrapMethods:'):].split('InnerClasses:')[0] if 'BootstrapMethods:' in v else ''
   write(f'caller-{i:02}.bootstrap.txt',short(v))
   manifest.append({'class':n,'alias':short(n),'file':fn,'method_count':len(b)})
  write('caller-manifest.json',json.dumps({'artifact':str(JAR),'sha256':hashlib.sha256(JAR.read_bytes()).hexdigest(),'classes':manifest,'coverage':'16 prior non-auth IPC call-containing methods plus same-class callbacks; transport auth and handshake bodies excluded'},indent=2));print(json.dumps(manifest,indent=2))
 elif op=='show':
  for a in args:print((OUT/a).read_text(encoding='utf8'))
 elif op=='methods':
  t=(OUT/args[0]).read_text(encoding='utf8');p=re.compile(args[1])
  for b in blocks(t):
   if p.search(b.splitlines()[0]) or (len(args)>2 and p.search(b)):print(b)
 elif op=='search':
  p=re.compile(args[0]);lim=int(args[1]) if len(args)>1 else 60;k=0
  for n,t in C.items():
   for b in blocks(t):
    if p.search(short(b)):
     print(short(n),short(b));k+=1
     if k>=lim:return
 elif op=='library':
  jar=JAR
  for n in args:
   t=dump(n,jar=jar);write(n.split('.')[-1]+'.javap.txt',t);print(n,len(t))
 elif op=='refs':
  p=re.compile(args[0]);hits=[]
  for n,t in C.items():
   for b in blocks(t):
    if p.search(short(b)):hits.append(short(n)+'\n'+short(b))
  write(args[1]+'.txt','\n'.join(hits));print('matched methods',len(hits))
 elif op=='dump':
  rev={'_'+hashlib.md5(t.encode()).hexdigest()[:6]:t for n in C for t in TOK.findall(n)}
  n=re.sub(r'_[0-9a-f]{6}',lambda m:rev.get(m.group(),m.group()),args[0]).replace('L.','com.moonsworth.lunar.client.',1)
  t=dump(n);write(args[1]+'.txt',t);write(args[1]+'.aliases.txt',short(t));print(n,len(t))
if __name__=='__main__':main()
