"""Static JNI ABI and bounded registration evidence; never loads a target DLL."""
import hashlib,json,pathlib,re,subprocess,struct,zipfile
R=pathlib.Path(__file__).resolve().parent;E=R/'evidence'
H=pathlib.Path('C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/include/jni.h')
t=H.read_text();tables={}
for name in ['JNINativeInterface_','JNIInvokeInterface_']:
 body=t.split('struct '+name+' {',1)[1].split('\n};',1)[0]
 slots=re.findall(r'void\s*\*\s*(reserved\d+)\s*;|\(JNICALL\s*\*(\w+)\)',body)
 tables[name]=[dict(index=i,offset=hex(i*8),name=a or b) for i,(a,b) in enumerate(slots)]
assert tables['JNINativeInterface_'][215]['name']=='RegisterNatives'
assert tables['JNINativeInterface_'][229]['name']=='NewDirectByteBuffer'
assert tables['JNIInvokeInterface_'][7]['name']=='AttachCurrentThreadAsDaemon'
(E/'jni-abi-offsets.json').write_text(json.dumps(dict(header=str(H),sha256=hashlib.sha256(H.read_bytes()).hexdigest(),pointer_bytes=8,tables=tables),indent=2))
images=json.loads((E/'pe-identities.json').read_text());bounds=[]
for image in images:
 b=pathlib.Path(image['path']).read_bytes();base=int(image['image_base'],16)
 strings={s.decode():[hex(m.start()) for m in re.finditer(re.escape(s),b)] for s in [b'RegisterNatives',b'JNI_OnLoad',b'Java_com_moonsworth_webosr_wrappers_Session_name',b'Java_com_moonsworth_webosr_wrappers_Session_getName']}
 candidates=[]
 if pathlib.Path(image['path']).name=='WebOSR-Binding.dll':
  for sec in image['sections']:
   if sec['name']!='.text':continue
   start=sec['file_offset'];data=b[start:start+sec['raw_size']]
   for m in re.finditer(b'\xb8\x06\x00\x00',data):
    i=m.start();candidates.append(dict(file_offset=hex(start+i),displacement_va=hex(base+sec['rva']+i),context=data[max(0,i-8):i+8].hex()))
 bounds.append(dict(path=image['path'],sha256=image['sha256'],ascii_offsets=strings,binding_text_0x6b8_displacement_candidates=candidates))
(E/'registration-bounded-scan.json').write_text(json.dumps(dict(method='Exact ASCII search in four identified DLLs; raw little-endian 0x6b8 scan in binding .text only. Candidates are not disassembled JNI calls; no exclusion of computed-table calls or other modules.',images=bounds),indent=2))
base=pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver');javap=H.parent.parent/'bin/javap.exe'
for name in ['com.moonsworth.webosr.NativeHandle','com.moonsworth.webosr.config.ThreadConfig','com.moonsworth.webosr.config.UltralightConfig','com.moonsworth.webosr.javascript.FunctionBus']:
 p=subprocess.run([str(javap),'-p','-c','-s','-classpath',str(base/'lunar.jar'),name],text=True,capture_output=True,check=True)
 (E/(name+'.javap.txt')).write_text(p.stdout,encoding='utf8')
verified=[]
for row in json.loads((R.parent/'session6-sol/evidence-native/lifecycle-manifest.json').read_text()):
 with zipfile.ZipFile(row['artifact']) as z:b=z.read(row['class'].replace('.','/')+'.class')
 digest=hashlib.sha256(b).hexdigest()
 verified.append(dict(**row,fresh_sha256=digest,matches=digest==row['class_sha256']))
 p=subprocess.run([str(javap),'-p','-c','-s','-classpath',row['artifact'],row['class']],text=True,capture_output=True,check=True)
 (E/(row['alias']+'.javap.txt')).write_text(p.stdout,encoding='utf8')
(E/'lifecycle-fresh-hashes.json').write_text(json.dumps(verified,indent=2))
print(json.dumps({'jni_slots':{k:len(v) for k,v in tables.items()},'registration_candidates':bounds[0]['binding_text_0x6b8_displacement_candidates']},indent=2))
