"""Static cache/xref selector and fresh javap only; never loads target classes."""
import pathlib,sys,runpy,re,json,subprocess,hashlib
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
S=pathlib.Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
argv=sys.argv[1:];sys.argv=['q.py','sig','L._dd3308._1e73d7']
q=runpy.run_path(str(S/'q.py')); C=q['C'];sh=q['sh'];ex=q['ex']
O=pathlib.Path(__file__).parent/'evidence-support';O.mkdir(exist_ok=True)
op,*args=argv
if op=='xref':
    out=[]
    for c,t in C.items():
        method=''
        for l in t.splitlines():
            if l.startswith('  ') and not l.startswith('    ') and l.strip():method=l.strip()
            if re.match(r'\s*\d+:',l) and any(a in sh(l) for a in args):
                out.append({'class':c,'alias':sh(c),'method':method,'method_alias':sh(method),'instruction':l.strip(),'instruction_alias':sh(l.strip())})
    (O/('xref-'+hashlib.sha256('|'.join(args).encode()).hexdigest()[:10]+'.json')).write_text(json.dumps({'patterns':args,'cache_classes':len(C),'matches':out},indent=2),encoding='utf-8')
    for x in out:print(x['alias'],x['method_alias'],x['instruction_alias'])
    print('TOTAL',len(out),'CACHE_CLASSES',len(C))
elif op=='dump':
    for a in args:
        c=ex(a)
        p=subprocess.run([r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe','-classpath',r'C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar','-p','-c','-v',c],capture_output=True,text=True,encoding='utf-8')
        if p.returncode:raise RuntimeError(p.stderr)
        (O/(sh(c)+'.verbose.txt')).write_text(p.stdout,encoding='utf-8')
        (O/(sh(c)+'.short.txt')).write_text(sh(C.get(c,p.stdout)),encoding='utf-8')
        print(sh(c),c,len(p.stdout),hashlib.sha256(p.stdout.encode()).hexdigest())
elif op=='method':
    t=sh(C[ex(args[0])]);on=False
    for l in t.splitlines():
        if l.startswith('  ') and not l.startswith('    ') and l.strip():on=any(a in l for a in args[1:])
        if on:print(l)
elif op=='sub':
    n=ex(args[0]);result=[]
    for c,t in C.items():
        if re.search(r'(extends|implements)[^{]*\b'+re.escape(n)+r'\b(?![.$\w])',t.splitlines()[0]): result.append(sh(c))
    print('\n'.join(result))
elif op=='read':
    for a in args: print((O/a).read_text(encoding='utf-8'))

elif op=="hierarchy":
    rows=[]
    for c,t in C.items():
        h=next((l for l in t.splitlines() if " class " in " "+l or " interface " in " "+l),"")
        if any(a in sh(h) for a in args):rows.append({"alias":sh(c),"actual":c,"header":sh(h)})
    (O/"hierarchy.json").write_text(json.dumps(rows,indent=2),encoding="utf-8")
    print(json.dumps(rows,indent=2))
