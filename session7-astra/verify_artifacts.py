"""Independent PE export/class declaration inventory. Static reads only."""
import struct,json,hashlib,pathlib,zipfile,subprocess,re
ROOT=pathlib.Path(__file__).resolve().parent
BASE=pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver')
OUT=ROOT/'evidence';OUT.mkdir(exist_ok=True)
def pe(p):
 b=p.read_bytes();u16=lambda o:struct.unpack_from('<H',b,o)[0];u32=lambda o:struct.unpack_from('<I',b,o)[0]
 h=u32(0x3c);assert b[h:h+4]==b'PE\0\0';o=h+24;assert u16(o)==0x20b
 base=struct.unpack_from('<Q',b,o+24)[0];ss=[]
 for i in range(u16(h+6)):
  q=o+u16(h+20)+40*i;ss.append(dict(name=b[q:q+8].rstrip(b'\0').decode(),virtual_size=u32(q+8),rva=u32(q+12),raw_size=u32(q+16),file_offset=u32(q+20)))
 def off(r):
  if r<u32(o+60):return r
  for s in ss:
   if s['rva']<=r<s['rva']+s['raw_size']:return s['file_offset']+r-s['rva']
  raise ValueError(hex(r))
 def string(r):
  q=off(r);return b[q:b.index(b'\0',q)].decode('ascii')
 er,es=u32(o+112),u32(o+116);exports=[]
 if er:
  q=off(er);func,names,ords=off(u32(q+28)),off(u32(q+32)),off(u32(q+36))
  for i in range(u32(q+24)):
   ordinal=u16(ords+2*i);r=u32(func+4*ordinal)
   try: file_offset=hex(off(r))
   except ValueError: file_offset=None
   exports.append(dict(name=string(u32(names+4*i)),ordinal=ordinal+u32(q+16),rva=hex(r),va=hex(base+r),file_offset=file_offset,forwarder=string(r) if er<=r<er+es else None))
 return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b),machine=hex(u16(h+4)),image_base=hex(base),sections=ss,exports=exports)
def class_methods(b):
 p=8
 def read(fmt):
  nonlocal p
  x=struct.unpack_from('>'+fmt,b,p);p+=struct.calcsize('>'+fmt);return x[0] if len(x)==1 else x
 n=read('H');cp=[None]*n;i=1
 while i<n:
  t=read('B')
  if t==1:z=read('H');cp[i]=b[p:p+z].decode('utf8',errors='replace');p+=z
  elif t in (7,8,16,19,20):cp[i]=read('H')
  elif t in (9,10,11,12,17,18):read('HH')
  elif t in (3,4):read('I')
  elif t in (5,6):read('Q');i+=1
  elif t==15:read('BH')
  else:raise ValueError(t)
  i+=1
 access,this,super_=read('HHH');owner=cp[cp[this]]
 for _ in range(read('H')):read('H')
 def attrs():
  nonlocal p
  for _ in range(read('H')):read('H');size=read('I');p+=size
 for _ in range(read('H')):read('HHH');attrs()
 methods=[]
 for _ in range(read('H')):
  a,n,d=read('HHH');methods.append(dict(owner=owner,name=cp[n],descriptor=cp[d],access=a,native=bool(a&0x100)));attrs()
 return methods
images=[pe(BASE/'natives'/n) for n in ['WebOSR-Binding.dll','Ultralight.dll','UltralightCore.dll','WebCore.dll']]
(OUT/'pe-identities.json').write_text(json.dumps(images,indent=2))
declarations=[];classes=[]
with zipfile.ZipFile(BASE/'lunar.jar') as z:
 for n in z.namelist():
  if n.startswith('com/moonsworth/webosr/') and n.endswith('.class'):
   b=z.read(n);methods=class_methods(b);classes.append(dict(member=n,sha256=hashlib.sha256(b).hexdigest()));declarations.extend(m for m in methods if m['native'])
def mangle(s):
 return ''.join('_1' if c=='_' else '_' if c in './' else '_2' if c==';' else '_3' if c=='[' else c if c.isascii() and c.isalnum() else '_0'+format(ord(c),'04x') for c in s)
for d in declarations:d['symbol']='Java_'+mangle(d['owner'])+'_'+mangle(d['name'])
j={d['symbol'] for d in declarations};e={x['name'] for x in images[0]['exports'] if x['name'].startswith('Java_')}
result=dict(java_count=len(declarations),dll_count=len(e),shared_count=len(j&e),java_only=sorted(j-e),dll_only=sorted(e-j),declarations=declarations,classes=classes,jar_sha256=hashlib.sha256((BASE/'lunar.jar').read_bytes()).hexdigest())
(OUT/'jni-reconciliation-fresh.json').write_text(json.dumps(result,indent=2))
javap='C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/javap.exe'
selected=['com.moonsworth.webosr.TextureHandler','com.moonsworth.webosr.wrappers.WebEngine','com.moonsworth.webosr.wrappers.Browser','com.moonsworth.webosr.wrappers.WebOSR','com.moonsworth.webosr.wrappers.Session','com.moonsworth.webosr.wrappers.NativeHandle','com.moonsworth.webosr.wrappers.image.TexturedImageSource','com.moonsworth.webosr.config.ThreadConfig','com.moonsworth.webosr.config.UltralightConfig']
with zipfile.ZipFile(BASE/'lunar.jar') as z:
 selected=[n for n in selected if n.replace('.','/')+'.class' in z.namelist()]
for n in selected:
 r=subprocess.run([javap,'-p','-c','-s','-classpath',str(BASE/'lunar.jar'),n],capture_output=True,text=True,check=True)
 (OUT/(n+'.javap.txt')).write_text(r.stdout,encoding='utf8')
# Independently re-read and disassemble the prior texture implementation identities.
prior=json.loads((ROOT.parent/'session6-sol/evidence-native/class-manifest.json').read_text())
matches=[]
for row in prior[:3]:
 with zipfile.ZipFile(row['artifact']) as z:b=z.read(row['class'].replace('.','/')+'.class')
 matches.append(dict(alias=row['alias'],sha256=hashlib.sha256(b).hexdigest(),matches=hashlib.sha256(b).hexdigest()==row['class_sha256']))
 r=subprocess.run([javap,'-p','-c','-s','-classpath',row['artifact'],row['class']],capture_output=True,text=True,check=True)
 (OUT/(row['alias']+'.javap.txt')).write_text(r.stdout,encoding='utf8')
(OUT/'java-hash-verification.json').write_text(json.dumps(matches,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['declarations','classes']},indent=2));print(matches)
