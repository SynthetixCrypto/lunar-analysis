import struct,sys,hashlib,json,os
def u16(b,o): return struct.unpack_from('<H',b,o)[0]
def u32(b,o): return struct.unpack_from('<I',b,o)[0]
def parse(path):
    b=open(path,'rb').read(); r={'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
    pe=u32(b,0x3c); mach=u16(b,pe+4); nsec=u16(b,pe+6); ts=u32(b,pe+8); opt=pe+24; magic=u16(b,opt)
    r['machine']=hex(mach); r['timestamp']=ts; r['pe32plus']=magic==0x20b
    dd=opt+(112 if magic==0x20b else 96); ndd=u32(b,dd-4)
    dirs=[(u32(b,dd+8*i),u32(b,dd+8*i+4)) for i in range(min(ndd,16))]
    secs=[]; so=opt+u16(b,pe+20)
    for i in range(nsec):
        o=so+40*i; name=b[o:o+8].rstrip(b'\0').decode('latin1'); vs,va,rs,ro=u32(b,o+8),u32(b,o+12),u32(b,o+16),u32(b,o+20); ch=u32(b,o+36)
        secs.append((name,va,vs,ro,rs,hex(ch)))
    r['sections']=[s[0] for s in secs]
    def rva(x):
        for n,va,vs,ro,rs,ch in secs:
            if va<=x<va+max(vs,rs): return x-va+ro
        return None
    def cstr(o):
        e=b.index(b'\0',o); return b[o:e].decode('latin1')
    # exports
    ex=[]
    if dirs[0][0]:
        o=rva(dirs[0][0]); nn=u32(b,o+24); an=rva(u32(b,o+32))
        for i in range(nn): ex.append(cstr(rva(u32(b,an+4*i))))
    r['exports']=ex
    im={}
    if dirs[1][0]:
        o=rva(dirs[1][0])
        while True:
            oft,_,_,nm,ft=struct.unpack_from('<IIIII',b,o)
            if nm==0: break
            dll=cstr(rva(nm)); funcs=[]; t=rva(oft or ft)
            while t is not None:
                v=struct.unpack_from('<Q' if magic==0x20b else '<I',b,t)[0]
                if v==0: break
                if v>>(63 if magic==0x20b else 31): funcs.append('#%d'%(v&0xffff))
                else: funcs.append(cstr(rva(v&0x7fffffff)+2))
                t+=8 if magic==0x20b else 4
            im[dll]=funcs; o+=20
    r['imports']=im
    r['has_authenticode']=bool(dirs[4][0])  # security dir is file offset
    pdb=None
    if len(dirs)>6 and dirs[6][0]:
        o=rva(dirs[6][0])
        for i in range(dirs[6][1]//28):
            t=u32(b,o+28*i+12); po=u32(b,o+28*i+24)
            if t==2 and b[po:po+4]==b'RSDS': pdb=cstr(po+24)
    r['pdb']=pdb
    return r
if __name__=='__main__':
    out=[parse(p) for p in sys.argv[1:]]
    json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'pe_out.json'),'w'),indent=1)
    for r in out:
        print(os.path.basename(r['path']),r['bytes'],r['sha256'][:16],r['machine'],'sig' if r['has_authenticode'] else 'nosig','pdb=',r['pdb'],'exports',len(r['exports']),'importDLLs',len(r['imports']),'sections',r['sections'])
