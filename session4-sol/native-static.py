"""Read-only PE export/RUNTIME_FUNCTION and exact Java-wrapper evidence extraction.
No library is loaded; no target code is executed. Writes only beside this script.
"""
import hashlib, json, pathlib, pickle, re, struct, subprocess
OUT = pathlib.Path(__file__).resolve().parent / 'evidence-native'
OUT.mkdir(exist_ok=True)
ROOT = pathlib.Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
P = pathlib.Path(r'C:\Users\Admin\.lunarclient\offline\multiver\natives\WebOSR-Binding.dll')
b = P.read_bytes()
u16 = lambda o: struct.unpack_from('<H', b, o)[0]
u32 = lambda o: struct.unpack_from('<I', b, o)[0]
pe = u32(0x3c); opt = pe+24; dd = opt+112
sections=[]
for i in range(u16(pe+6)):
    o=opt+u16(pe+20)+40*i
    name=b[o:o+8].rstrip(b'\0').decode('ascii')
    vs,va,rs,ro=struct.unpack_from('<IIII',b,o+8)
    sections.append(dict(name=name,rva=va,virtual_bytes=vs,file_offset=ro,file_bytes=rs))
def off(r):
    for s in sections:
        if s['rva']<=r<s['rva']+s['file_bytes']:
            return s['file_offset']+r-s['rva']
    raise ValueError('RVA not file-backed: '+hex(r))
def cstr(o): return b[o:b.index(b'\0',o)].decode('ascii')
dirs=[struct.unpack_from('<II',b,dd+8*i) for i in range(16)]
eo=off(dirs[0][0]); base,nf,nn,af,an,ao=struct.unpack_from('<IIIIII',b,eo+16)
functions=[]
if dirs[3][0]:
    po=off(dirs[3][0])
    for p in range(po,po+dirs[3][1],12):
        start,end,unwind=struct.unpack_from('<III',b,p)
        functions.append(dict(start_rva=start,end_rva=end,unwind_rva=unwind,pdata_offset=p))
exports=[]
for i in range(nn):
    name=cstr(off(u32(off(an)+4*i))); index=u16(off(ao)+2*i); r=u32(off(af)+4*index)
    forward=dirs[0][0]<=r<dirs[0][0]+dirs[0][1]
    row=dict(name=name,ordinal=base+index,rva=r,file_offset=off(r),forwarder=cstr(off(r)) if forward else None)
    fn=next((f for f in functions if f['start_rva']<=r<f['end_rva']),None)
    row['runtime_function']=fn
    count=min(64,fn['end_rva']-r) if fn else 32
    row['entry_bytes_hex']=b[off(r):off(r)+count].hex()
    exports.append(row)
strings=[]
for m in re.finditer(rb'[\x20-\x7e]{4,}\x00',b):
    s=m.group()[:-1].decode('ascii')
    if re.search(r'com/moonsworth/webosr|onPaint|on.*Loaded|texture|upload|Promise|invoke|JNI_OnLoad|RegisterNatives|\(.*\)[VZJIDLF]',s,re.I) or 0x5dd40<=m.start()<0x5de50 or 0x5e750<=m.start()<0x5e8d0:
        strings.append(dict(text=s,file_offset=m.start(),bytes=len(m.group())))
result=dict(path=str(P),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),machine=u16(pe+4),sections=sections,exports=exports,callback_string_candidates=strings,limitations=['PE metadata and selected raw bytes only; not disassembled.','No absence of RegisterNatives proven by string/export search.','RUNTIME_FUNCTION ranges may describe only a fragment, not complete semantic function.'])
(OUT/'binding-pe-addresses.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
C=pickle.load(open(ROOT/'classes.pkl','rb'))
names=[n for n in C if n.startswith('com.moonsworth.webosr.')]
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
aliases=['L._81676d._21aca6._590f69','L._81676d._21aca6._590f69._cfe983','L._81676d._21aca6._590f69._cfe983._cfe983','L._81676d._21aca6._21aca6','L._81676d._21aca6._21aca6._cfe983']
def alias(s):
    return TOK.sub(lambda m:'_'+hashlib.md5(m.group().encode()).hexdigest()[:6],s.replace('com.moonsworth.lunar.client.','L.'))
names += [n for n in C if alias(n) in aliases]
mapping=[]
for n in names:
    dest=alias(n)+'.javap.txt'
    (OUT/dest).write_text(C[n],encoding='utf-8')
    mapping.append(dict(class_name=n,alias=alias(n),raw_file=dest,source='retained javap cache'))
(OUT/'class-map.json').write_text(json.dumps(mapping,indent=2),encoding='utf-8')
for n in ['com.moonsworth.webosr.wrappers.WebEngine','com.moonsworth.webosr.javascript.FunctionBus','com.moonsworth.webosr.NativeHandle','com.moonsworth.webosr.wrappers.NativeFuture','com.moonsworth.webosr.wrappers.PromiseJS']:
    p=subprocess.run([r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe','-p','-c','-v','-classpath',str(ROOT/'lunar'),n],capture_output=True,text=True,check=True)
    (OUT/(n+'.fresh-verbose.txt')).write_text(p.stdout,encoding='utf-8')
print(json.dumps(dict(exports=len(exports),runtime_functions=len(functions),wrapper_classes=len(mapping),strings=len(strings),sha256=result['sha256'])))
