import pathlib,pickle,re,sys,json,hashlib,subprocess
ROOT=pathlib.Path(__file__).resolve().parent.parent
S=pathlib.Path('C:/Users/Admin/AppData/Local/Temp/claude/C--Users-Admin-Downloads-New-folder-lunar-analysis/eeca5643-ee80-46b2-970c-8533c6845d76/scratchpad')
C=pickle.load(open(S/'classes.pkl','rb'))
OUT=ROOT/'session6-sol/evidence-reach';OUT.mkdir(exist_ok=True)
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def sh(s):
 s=s.replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.','ML.').replace('com/moonsworth/lunar/','ML/')
 return TOK.sub(lambda m:'_'+hashlib.md5(m.group(0).encode()).hexdigest()[:6],s)
N={sh(n):n for n in C}
op,*args=sys.argv[1:]
if op=='find':
 r=re.compile(args[0]);rows=[]
 for n,t in C.items():
  lines=t.splitlines()
  if r.search(sh(t)):
   hit=[sh(x) for x in lines if r.search(sh(x))]
   rows.append({'alias':sh(n),'class':n,'hits':hit})
 out=OUT/(args[1]+'.json');out.write_text(json.dumps(rows,indent=2),encoding='utf8');print(json.dumps(rows,indent=2)[:24000]);print('SAVED',len(rows),out)
elif op=='dump':
 for alias in args:
  n=N[alias];t=C[n];(OUT/(alias+'.javap.txt')).write_text(sh(t),encoding='utf8')
  p=None;kind=None
  for k in ['lunar','modern','common','genesis']:
   q=S/k/(n.replace('.','/')+'.class')
   if q.exists():p=q;kind=k;break
  manifest={'alias':alias,'original':n,'extracted_root':kind,'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest() if p else None}
  (OUT/(alias+'.identity.json')).write_text(json.dumps(manifest,indent=2),encoding='utf8')
  if p:
   v=subprocess.run(['C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/javap.exe','-p','-c','-v',str(p)],capture_output=True,text=True,encoding='utf8',errors='replace')
   (OUT/(alias+'.verbose.javap.txt')).write_text(v.stdout,encoding='utf8')
  print(alias,'SAVED',len(t))
elif op=='method':
 alias,pattern=args;n=N[alias];on=False
 for line in sh(C[n]).splitlines():
  if line.startswith('  ') and not line.startswith('    ') and line.strip():on=bool(re.search(pattern,line))
  if on:print(line)
