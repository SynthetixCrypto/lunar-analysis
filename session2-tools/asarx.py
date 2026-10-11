import json,struct,os,sys
A='C:/Users/Admin/AppData/Local/Programs/Lunar Client/resources/app.asar'
f=open(A,'rb'); h=f.read(16)
hsize=struct.unpack('<I',h[12:16])[0]; header=json.loads(f.read(hsize)); base=16+((hsize+3)&~3)
B=chr(92); out=B+B+'?'+B+os.path.abspath('asar')
n=0
def walk(node,path):
    global n
    for k,v in node.get('files',{}).items():
        p=path+[k]
        if 'files' in v: walk(v,p)
        elif v.get('unpacked'): continue
        elif 'offset' in v:
            if not (p[0] in ('dist-electron','package.json') or (p[0]=='dist' and (p[1]=='html' or k.endswith('.js')))): continue
            f.seek(base+int(v['offset'])); data=f.read(v['size'])
            dst=os.path.join(out,*p); os.makedirs(os.path.dirname(dst),exist_ok=True); open(dst,'wb').write(data); n+=1
walk(header,[])
print(n)
