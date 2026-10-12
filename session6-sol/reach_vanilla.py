import pathlib,zipfile,json,hashlib,subprocess
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'session6-sol/evidence-reach/vanilla';out.mkdir(exist_ok=True)
rows=[]
for z in pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver/cache').rglob('bake.zip'):
 with zipfile.ZipFile(z) as a:
  for n in ['net.minecraft.world.entity.Entity','net.minecraft.world.entity.LivingEntity','net.minecraft.world.entity.player.Player']:
   if n not in a.namelist():continue
   b=a.read(n);p=out/(z.parent.parent.name+'-'+n+'.class');p.write_bytes(b)
   r=subprocess.run(['C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/javap.exe','-p','-c',str(p)],capture_output=True,text=True,encoding='utf8',errors='replace')
   p.with_suffix('.javap.txt').write_text(r.stdout,encoding='utf8')
   rows.append({'archive':str(z),'entry':n,'sha256':hashlib.sha256(b).hexdigest(),'evidence':p.name,'javap_rc':r.returncode,'stderr':r.stderr})
(out/'manifest.json').write_text(json.dumps(rows,indent=2),encoding='utf8')
print(json.dumps(rows,indent=2))
