import zipfile,re,json,hashlib
out={}
pat=re.compile(rb'([A-Z][A-Za-z0-9$]{2,60})\(((?:[a-zA-Z_][A-Za-z0-9_]*=\x01(?:, )?)+)\)')
M='C:/Users/Admin/.lunarclient/offline/multiver/'
for jar in ('lunar.jar','modern-0.1.0-SNAPSHOT-all-nomappings.jar','common-0.1.0-SNAPSHOT-all-nomappings.jar','genesis-0.1.0-SNAPSHOT-all.jar'):
    z=zipfile.ZipFile(M+jar)
    for n in z.namelist():
        if not (n.startswith('com/moonsworth') or n.startswith('genesis')) or not n.endswith('.class'): continue
        b=z.read(n); cls=n[:-6].replace('/','.')
        for m in pat.finditer(b):
            st=m.start(); name=m.group(1).decode()
            for cand in (st,st+1):
                if cand>=2 and int.from_bytes(b[cand-2:cand],'big')==m.end()-cand:
                    name=b[cand:m.start(1)+len(m.group(1))].decode(); break
            out.setdefault(cls,[]).append((name,[x.split('=')[0] for x in m.group(2).decode().split(', ') if x]))
json.dump(out,open('lombok_names.json','w'),indent=0)
def h(x): return re.sub(r'[CHIOR]{30}',lambda m:'_'+hashlib.md5(m.group(0).encode()).hexdigest()[:6],x).replace('com.moonsworth.lunar.client.','L.').replace('com.moonsworth.lunar.','ML.')
with open('lombok_names.txt','w') as f:
    for c,v in sorted(out.items()):
        for n,fl in v: f.write(h(c).ljust(52)+' '+n+' '+','.join(fl)[:140]+'\n')
print(len(out))
