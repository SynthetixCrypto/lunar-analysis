"""Analyst-only static cache selector and javap collector; never imports target code."""
import sys, pathlib, runpy, subprocess, hashlib, json
S=pathlib.Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
sys.argv=['q.py','sig','L._dd3308._1e73d7']
q=runpy.run_path(str(S/'q.py'))
O=pathlib.Path(__file__).parent
names=sys.argv[1:] if False else [
 'L._dd3308._1e73d7','L._88f3cf._2ce426','L._88f3cf._cfe983',
 'L._88f3cf._1e73d7._a1dd3a','L._02d7ad._d4ca6c._cfe983._13ea87',
 'L._88f3cf._1e73d7._ba7d98','L._88f3cf._ba7d98',
 'L._c8175c._cfe983._1e73d7','L._c8175c._cfe983._cfe983',
 'L._88f3cf._bb4487','L._88f3cf._1e73d7._bb4487',
 'L._02d7ad._cfe983','L._ec7e36._13ea87',
 'L._d4ca6c._cfe983._13ea87._00e05b','L._d4ca6c._cfe983._13ea87._c8175c','L._d4ca6c._cfe983._13ea87._1e73d7']
if len(sys.orig_argv)>2: names=sys.orig_argv[2:]
manifest=json.loads((O/'mapping.json').read_text(encoding='utf-8')) if (O/'mapping.json').exists() else []
for alias in names:
 full=q['ex'](alias)
 text=q['C'].get(full)
 if text is None:
  print('MISSING',alias,full); continue
 (O/(alias+'.cache.javap.txt')).write_text(text,encoding='utf-8')
 (O/(alias+'.short.javap.txt')).write_text(q['sh'](text),encoding='utf-8')
 out=subprocess.run([r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe','-classpath',r'C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar','-p','-c','-v',full],capture_output=True,text=True,encoding='utf-8')
 if out.returncode: raise RuntimeError(out.stderr)
 raw=out.stdout
 (O/(alias+'.verbose.javap.txt')).write_text(raw,encoding='utf-8')
 (O/(alias+'.verbose.short.txt')).write_text(q['sh'](raw),encoding='utf-8')
 manifest=[m for m in manifest if m['alias']!=alias]
 manifest.append({'alias':alias,'actual_class':full,'verbose_sha256':hashlib.sha256(raw.encode()).hexdigest()})
 print(alias,full,len(raw))
(O/'mapping.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
