import sys,re
t=open(sys.argv[1],encoding='utf-8').read()
pat=sys.argv[2]; w=int(sys.argv[3]) if len(sys.argv)>3 else 300; lim=int(sys.argv[4]) if len(sys.argv)>4 else 5
for i,m in enumerate(re.finditer(pat,t)):
    if i>=lim: break
    s=max(0,m.start()-w); e=min(len(t),m.end()+w)
    print(f'@{m.start()}:', t[s:e].replace('\n',' '),'\n')
