import zipfile,struct,sys,re,subprocess,os
from google.protobuf import descriptor_pb2
J='C:/Users/Admin/.lunarclient/offline/multiver/lunar.jar'
z=zipfile.ZipFile(J)
def mutf8(b):
    out=[];i=0
    while i<len(b):
        c=b[i]
        if c<0x80: out.append(chr(c)); i+=1
        elif (c&0xE0)==0xC0: out.append(chr(((c&0x1F)<<6)|(b[i+1]&0x3F))); i+=2
        else: out.append(chr(((c&0x0F)<<12)|((b[i+1]&0x3F)<<6)|(b[i+2]&0x3F))); i+=3
    return ''.join(out)
def cpool(b):
    n=struct.unpack('>H',b[8:10])[0]; i=10; cp=[None]*n; k=1
    while k<n:
        t=b[i]
        if t==1:
            l=struct.unpack('>H',b[i+1:i+3])[0]; cp[k]=('u',mutf8(b[i+3:i+3+l])); i+=3+l
        elif t in(3,4): i+=5
        elif t in(5,6): i+=9; k+=1
        elif t in(7,8,16,19,20): cp[k]=(t,struct.unpack('>H',b[i+1:i+3])[0]); i+=3
        elif t==15: i+=4
        elif t in(9,10,11,12,17,18): i+=5
        else: raise Exception('tag %d'%t)
        k+=1
    return cp
def clinit_ldcs(b,cp):
    # find methods; parse to <clinit> code
    n=len(cp); i=10
    # skip cpool again
    k=1
    while k<n:
        t=b[i]
        if t==1: l=struct.unpack('>H',b[i+1:i+3])[0]; i+=3+l
        elif t in(3,4): i+=5
        elif t in(5,6): i+=9; k+=1
        elif t in(7,8,16,19,20): i+=3
        elif t==15: i+=4
        else: i+=5
        k+=1
    i+=6; ic=struct.unpack('>H',b[i:i+2])[0]; i+=2+2*ic
    fc=struct.unpack('>H',b[i:i+2])[0]; i+=2
    def skip_attrs(i):
        ac=struct.unpack('>H',b[i:i+2])[0]; i+=2
        for _ in range(ac):
            l=struct.unpack('>I',b[i+2:i+6])[0]; i+=6+l
        return i
    for _ in range(fc): i=skip_attrs(i+6)
    mc=struct.unpack('>H',b[i:i+2])[0]; i+=2
    for _ in range(mc):
        name=cp[struct.unpack('>H',b[i+2:i+4])[0]][1]; i+=6
        ac=struct.unpack('>H',b[i:i+2])[0]; i+=2
        for _ in range(ac):
            an=cp[struct.unpack('>H',b[i:i+2])[0]][1]; l=struct.unpack('>I',b[i+2:i+6])[0]
            if name=='<clinit>' and an=='Code':
                cl=struct.unpack('>I',b[i+10:i+14])[0]; code=b[i+14:i+14+cl]
                res=[];p=0
                # linear scan for ldc/ldc_w only (sufficient for descriptor string array init)
                while p<len(code):
                    op=code[p]
                    if op==0x12: res.append(code[p+1]); p+=2
                    elif op==0x13: res.append(struct.unpack('>H',code[p+1:p+3])[0]); p+=3
                    else: p+=1
                return res
            i+=6+l
    return []
out={}
for n in z.namelist():
    if not n.startswith('com/lunarclient/gameipc/') or not n.endswith('Proto.class'): continue
    b=z.read(n); cp=cpool(b)
    cls=n[:-6].replace('/','.')
    jp=subprocess.run(['javap','-c','-p','-cp',J,cls],capture_output=True,text=True).stdout
    sec=jp.split('static {};')[-1].split('internalBuildGeneratedFileFrom')[0]
    idx=[int(m) for m in re.findall(r'ldc(?:_w)?\s+#(\d+)\s+// String',sec)]
    s=''
    for x in idx:
        e=cp[x]
        if e and e[0]==8: s+=cp[e[1]][1]
    try:
        raw=s.encode('latin-1'); fd=descriptor_pb2.FileDescriptorProto(); fd.ParseFromString(raw)
        out[n]=fd
    except Exception as ex:
        print('fail',n,ex)
import json
from google.protobuf import text_format
with open('gameipc_descriptors.txt','w') as f:
    for n,fd in sorted(out.items()):
        f.write('### '+n+'  file='+fd.name+' package='+fd.package+'\n')
        for m in fd.message_type:
            f.write('message '+m.name+' { '+'; '.join(f'{fl.name}={fl.number}:{descriptor_pb2.FieldDescriptorProto.Type.Name(fl.type)[5:].lower()}{(" "+fl.type_name) if fl.type_name else ""}{" repeated" if fl.label==3 else ""}' for fl in m.field)+' }\n')
            for nm in m.nested_type: f.write('  nested '+nm.name+' { '+'; '.join(f'{fl.name}={fl.number}' for fl in nm.field)+' }\n')
            for ne in m.enum_type: f.write('  enum '+ne.name+' {'+','.join(v.name+'='+str(v.number) for v in ne.value)+'}\n')
        for e in fd.enum_type: f.write('enum '+e.name+' {'+','.join(v.name+'='+str(v.number) for v in e.value)+'}\n')
        for sv in fd.service: f.write('service '+sv.name+' { '+'; '.join(f'{m.name}({m.input_type})->{m.output_type}' for m in sv.method)+' }\n')
print(len(out))
