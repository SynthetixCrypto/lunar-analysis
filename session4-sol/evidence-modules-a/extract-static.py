"""Analyst-only extraction of cached disassembly; javap never executes target classes."""
import contextlib, io, runpy, sys, pathlib, subprocess, hashlib, zipfile, struct, json
S=pathlib.Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
O=pathlib.Path(__file__).parent
sys.argv=['q.py','sig','L._88f3cf._bb4487._21aca6._cfe983']
with contextlib.redirect_stdout(io.StringIO()): Q=runpy.run_path(str(S/'q.py'))
C,sh,ex=Q['C'],Q['sh'],Q['ex']
prefixes=['L._88f3cf._bb4487._21aca6.','L._88f3cf._bb4487._52e8ee.']
extra=sys.argv[1:] if False else []
selected=[n for n in C if any(sh(n).startswith(p) for p in prefixes)]
if (O/'class-map.tsv').exists(): selected += [x.split('\t')[1] for x in (O/'class-map.tsv').read_text().splitlines()[1:]]
if len(sys.orig_argv)>2: selected += [ex(x) for x in sys.orig_argv[2:]]
selected=list(dict.fromkeys(selected))
mapping=['alias\toriginal\tcached_file\tverbose_file']
J=pathlib.Path(r'C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar')
Z=zipfile.ZipFile(J)
for n in selected:
    alias=sh(n); stem=alias.replace('.','_').replace('$','__')
    (O/(stem+'.cached.txt')).write_text(C[n],encoding='utf-8')
    (O/(stem+'.short.txt')).write_text(sh(C[n]),encoding='utf-8')
    v=subprocess.run([r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe','-p','-c','-v','-classpath',str(J),n],capture_output=True,check=True)
    (O/(stem+'.verbose.txt')).write_bytes(v.stdout)
    (O/(stem+'.verbose-short.txt')).write_text(sh(v.stdout.decode('utf-8',errors='replace')),encoding='utf-8')
    mapping.append('\t'.join([alias,n,stem+'.cached.txt',stem+'.verbose.txt']))
    entry=n.replace('.','/')+'.class'
    if entry in Z.namelist():
        b=Z.read(entry); count=struct.unpack_from('>H',b,8)[0]; at=10; idx=1; strings={}
        while idx<count:
            tag=b[at]; at+=1
            if tag==1:
                size=struct.unpack_from('>H',b,at)[0]; at+=2
                strings[idx]=b[at:at+size].decode('utf-8',errors='replace'); at+=size
            elif tag in (3,4): at+=4
            elif tag in (5,6): at+=8; idx+=1
            elif tag in (7,8,16,19,20): at+=2
            elif tag in (9,10,11,12,17,18): at+=4
            elif tag==15: at+=3
            else: raise ValueError(tag)
            idx+=1
        (O/(stem+'.utf8.json')).write_text(json.dumps(strings,ensure_ascii=True,indent=2),encoding='utf-8')
(O/'class-map.tsv').write_text('\n'.join(mapping)+'\n',encoding='utf-8')
(O/'provenance.txt').write_text('Static javap -p -c -v; no target execution.\n'+str(J)+'\nSHA256 '+hashlib.sha256(J.read_bytes()).hexdigest()+'\nCached input: '+str(S/'classes.pkl')+'\n',encoding='utf-8')
print('Retained',len(selected),'classes')
