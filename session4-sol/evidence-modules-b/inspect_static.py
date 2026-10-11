"""Analyst-only static disassembly reader. Never loads target classes."""
import sys, re, pickle, hashlib, subprocess, json
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
S = Path(r'\\?\C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
O = Path(__file__).resolve().parent
C = pickle.load((S/'classes.pkl').open('rb'))
T = re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def short(s):
    s=s.replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.','ML.').replace('com/moonsworth/lunar/','ML/')
    return T.sub(lambda m:'_'+hashlib.md5(m[0].encode()).hexdigest()[:6],s)
N = {short(n):n for n in C}
def keep(alias, verbose=False):
    n=N[alias]; stem=alias.replace('.','-').replace('$','--')
    (O/(stem+'.cached.javap.txt')).write_text(C[n],encoding='utf-8')
    (O/(stem+'.short.txt')).write_text(short(C[n]),encoding='utf-8')
    root=next((r for r in ('lunar','modern','common','genesis') if (S/r/(n.replace('.','/')+'.class')).exists()),None)
    if verbose and root:
        p=subprocess.run([r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe','-p','-c','-v','-classpath',str(S/root),n],capture_output=True,encoding='utf-8',errors='replace',check=True)
        (O/(stem+'.verbose.javap.txt')).write_text(p.stdout,encoding='utf-8')
        (O/(stem+'.verbose.short.txt')).write_text(short(p.stdout),encoding='utf-8')
    mp=O/'full-name-mappings.json'; data=json.loads(mp.read_text()) if mp.exists() else {}
    f=S/root/(n.replace('.','/')+'.class') if root else None
    data[alias]={'full_name':n,'extracted_root':root,'class_path':str(f) if f else None,'class_sha256':hashlib.sha256(f.read_bytes()).hexdigest() if f else None}
    mp.write_text(json.dumps(data,indent=2),encoding='utf-8')
    return short(C[n])
if sys.argv[1]=='keep':
    for a in sys.argv[2:]: print(keep(a,True))
elif sys.argv[1]=='refs':
    pattern=re.compile(sys.argv[2]); found=[]
    for n,t in C.items():
        method=''; lines=[]
        for l in short(t).splitlines():
            if l.startswith('  ') and not l.startswith('    ') and l.strip(): method=l.strip()
            if pattern.search(l): lines.append({'class':short(n),'method':method,'line':l})
        if lines: found.extend(lines)
    print(json.dumps(found,indent=2))
elif sys.argv[1]=='find':
    for n in C:
        if re.search(sys.argv[2],short(n)): print(short(n))
elif sys.argv[1]=='external':
    data=json.loads((O/'exact-module-refs.json').read_text(encoding='utf-8-sig'))
    print(json.dumps([r for r in data if not r['class'].startswith(('L._88f3cf._bb4487._91398c','L._88f3cf._bb4487._327414'))],indent=2))
elif sys.argv[1]=='meth':
    on=False
    for l in short(C[N[sys.argv[2]]]).splitlines():
        if l.startswith('  ') and not l.startswith('    ') and l.strip(): on=bool(re.search(sys.argv[3],l))
        if on: print(l)
