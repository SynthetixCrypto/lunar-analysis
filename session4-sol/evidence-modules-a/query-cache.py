import contextlib,io,runpy,sys,re
S=r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad\q.py'
args=sys.argv[1:]; sys.argv=['q.py','sig','L._88f3cf._bb4487._21aca6._cfe983']
with contextlib.redirect_stdout(io.StringIO()): Q=runpy.run_path(S)
for n,t in Q['C'].items():
    t=Q['sh'](t)
    if args[0]=='refs':
        for l in t.splitlines():
            if re.search(args[1],l): print(Q['sh'](n),'|',l.strip())
    elif args[0]=='methods' and Q['sh'](n)==args[1]:
        on=False
        for l in t.splitlines():
            if l.startswith('  ') and not l.startswith('    ') and l.strip(): on=bool(re.search(args[2],l))
            if on: print(l)
