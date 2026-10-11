import zipfile,os
B=chr(92); base=B+B+'?'+B+os.path.abspath('genesis')
z=zipfile.ZipFile('C:/Users/Admin/.lunarclient/offline/multiver/genesis-0.1.0-SNAPSHOT-all.jar')
n=0
for e in z.namelist():
    if e.startswith('com/moonsworth/lunar/ichor/') or (e.startswith('com/moonsworth/lunar/genesis/') and e.count('/')<=5) or e.startswith('com/moonsworth/lunar/ORCO'):
        if e.endswith('/'): continue
        p=os.path.join(base,*e.split('/')); os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'wb').write(z.read(e)); n+=1
print(base[:10],n)
