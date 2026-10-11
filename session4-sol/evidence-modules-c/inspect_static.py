"""Read-only class-cache lookup; javap reads extracted class bytes, never target execution."""
import sys, os, pickle, re, hashlib, subprocess, json
from pathlib import Path
S=Path(r'\\?\C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
OUT=Path(__file__).parent
C=pickle.load(open(S/'classes.pkl','rb'))
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
REV={ '_'+hashlib.md5(t.encode()).hexdigest()[:6]:t for c in C for t in TOK.findall(c) }
def expand(n):
    n=re.sub(r'_[0-9a-f]{6}',lambda m:REV.get(m.group(),m.group()),n)
    if n.startswith('L.'): n='com.moonsworth.lunar.client.'+n[2:]
    if n.startswith('ML.'): n='com.moonsworth.lunar.'+n[3:]
    return n
def short(n):
    n=n.replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.','ML.').replace('com/moonsworth/lunar/','ML/')
    return TOK.sub(lambda m:'_'+hashlib.md5(m.group().encode()).hexdigest()[:6],n)
if sys.argv[1]=='dump':
    for alias in sys.argv[2:]:
        n=expand(alias)
        rel=Path(*n.split('.')).with_suffix('.class')
        roots=[r for r in ('lunar','modern','common','genesis') if (S/r/rel).is_file()]
        if not roots: print('NOTFOUND',alias,n); continue
        root=roots[0]
        for mode in ('c','v'):
            p=subprocess.run([r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe','-J-Dstdout.encoding=UTF-8','-J-Dfile.encoding=UTF-8','-p','-'+mode,'-classpath',str(S/root),n],capture_output=True)
            if p.returncode: raise RuntimeError(p.stderr)
            text=p.stdout.decode('utf-8',errors='strict').replace('\r\n','\n')
            (OUT/(alias+'.javap-'+mode+'.txt')).write_text(text,encoding='utf-8',newline='')
            if mode=='c': (OUT/(alias+'.alias.txt')).write_text(short(text),encoding='utf-8',newline='')
        with open(OUT/'class-manifest.jsonl','a',encoding='utf-8') as f:
            f.write(json.dumps({'alias':alias,'original':n,'root':root,'path':str(S/root/rel),'sha256':hashlib.sha256((S/root/rel).read_bytes()).hexdigest()})+'\n')
        print(alias,n,root)
elif sys.argv[1]=='find':
    pat=re.compile(sys.argv[2])
    for n,t in C.items():
        matches=[l for l in short(t).splitlines() if pat.search(l)]
        if matches: print(short(n)+'\n'+'\n'.join(matches))
elif sys.argv[1]=='show':
    print(short(C[expand(sys.argv[2])]))
elif sys.argv[1]=='meth':
    text=(OUT/(sys.argv[2]+'.alias.txt')).read_text(encoding='utf-8')
    on=False
    for l in text.splitlines():
        if l.startswith('  ') and not l.startswith('    ') and l.strip(): on=bool(re.search(sys.argv[3],l))
        if on: print(l)
elif sys.argv[1]=='retain-find':
    pat=re.compile(sys.argv[3]); results=[]
    for n,t in C.items():
        text=short(t)
        matches=[l for l in text.splitlines() if pat.search(l)]
        if matches: results.append(short(n)+'\n'+'\n'.join(matches))
    (OUT/sys.argv[2]).write_text('\n\n'.join(results),encoding='utf-8')
    print(len(results),'matched classes')
elif sys.argv[1]=='boot':
    t=(OUT/(sys.argv[2]+'.javap-v.txt')).read_text(encoding='utf-8')
    print(short(t[t.index('BootstrapMethods:'):]))
