"""Session 6 local static research helper; never loads or executes Lunar code."""
import sys, pathlib, json, re, subprocess, os, hashlib
import pickle,importlib.util,shutil
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
ROOT=pathlib.Path(__file__).resolve().parent.parent
OUT=ROOT/'session6-sol'
SCRATCH=pathlib.Path('C:/Users/Admin/AppData/Local/Temp/claude/C--Users-Admin-Downloads-New-folder-lunar-analysis/eeca5643-ee80-46b2-970c-8533c6845d76/scratchpad')
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def short(t):
    t=t.replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.','ML.').replace('com/moonsworth/lunar/','ML/')
    return TOK.sub(lambda m:'_'+hashlib.md5(m[0].encode()).hexdigest()[:6],t)
def cache():return pickle.loads((SCRATCH/'classes.pkl').read_bytes())
def blocks(t):return re.split(r'\n(?=  \S)',t)
def read(paths):
    for p in paths:
        q=pathlib.Path(p); q=q if q.is_absolute() else ROOT/q
        print('\nFILE '+str(q)+'\n'+q.read_text(encoding='utf-8-sig',errors='replace'))
def main():
    op,*args=sys.argv[1:]
    if op=='read': read(args)
    elif op=='list':
        for a in args:
            for p in (ROOT/a).iterdir(): print(str(p.relative_to(ROOT)),p.stat().st_size)
    elif op=='search':
        pat,*dirs=args
        cmd=['rg','-n','--no-heading',pat,*dirs]
        subprocess.run(cmd,cwd=ROOT,check=False)
    elif op=='probe':
        roots=[pathlib.Path('C:/Program Files'),pathlib.Path('C:/Program Files (x86)'),pathlib.Path('C:/tools'),pathlib.Path('C:/Users/Admin/Downloads'),pathlib.Path('C:/Users/Admin/Desktop'),pathlib.Path('C:/Users/Admin/AppData/Local/Programs'),pathlib.Path('C:/Users/Admin/scoop/apps')]
        found=[]
        for root in roots:
            if not root.exists(): continue
            for base,ds,fs in os.walk(root):
                depth=len(pathlib.Path(base).relative_to(root).parts)
                if depth>=5: ds[:]=[]
                ds[:]=[d for d in ds if d not in ['node_modules','.git','lunar-analysis','Lunar Client','WindowsApps']]
                if 'analyzeHeadless.bat' in fs or any('ghidra' in d.lower() for d in ds): found.append({'path':base,'matching_dirs':[d for d in ds if 'ghidra' in d.lower()],'headless':'analyzeHeadless.bat' in fs})
        result={'ghidra_search_roots':[str(x) for x in roots],'depth_limit':5,'matches':found,'shell_java_home':os.environ.get('JAVA_HOME'),'ghidra_env':os.environ.get('GHIDRA_INSTALL_DIR'),'java21':subprocess.run(['C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/java.exe','-version'],capture_output=True,text=True).stderr}
        (OUT/'environment-probe.json').write_text(json.dumps(result,indent=2))
        print(json.dumps(result,indent=2))
    elif op=='tools':
        print({x:bool(importlib.util.find_spec(x)) for x in ['capstone','pefile','iced_x86','lief']})
        print({x:shutil.which(x) for x in ['dumpbin','llvm-objdump','objdump','rg','node','rea']})
    elif op=='class':
        c=cache(); name=next(n for n in c if short(n)==args[0]); t=short(c[name])
        if len(args)>1:t='\n'.join(x for x in blocks(t) if re.search(args[1],x.split('\n')[0]))
        print(t)
    elif op=='xref':
        pat,label=args; out=OUT/'evidence-bus';out.mkdir(exist_ok=True)
        matches=[]
        for n,t in cache().items():
            for block in blocks(short(t)):
                lines=[l for l in block.splitlines() if re.search(pat,l)]
                if lines:matches.append({'class':n,'alias':short(n),'method':block.splitlines()[0],'lines':lines})
        (out/(label+'.json')).write_text(json.dumps({'scope':'retained classes.pkl, all cached disassembly; exact lines and enclosing method signatures','matches':matches},indent=2),encoding='utf-8')
        print(json.dumps(matches,indent=2))
    elif op=='fresh':
        alias,group=args;c=cache();name=next(n for n in c if short(n)==alias)
        jars=[pathlib.Path('C:/Users/Admin/.lunarclient/offline/multiver')/p for p in ['lunar.jar','modern-0.1.0-SNAPSHOT-all-nomappings.jar','common-0.1.0-SNAPSHOT-all-nomappings.jar','genesis.jar']]
        import zipfile
        jar=next(p for p in jars if p.exists() and name.replace('.','/')+'.class' in zipfile.ZipFile(p).namelist())
        out=OUT/('evidence-'+group);out.mkdir(exist_ok=True)
        r=subprocess.run(['C:/Program Files/Microsoft/jdk-21.0.10.7-hotspot/bin/javap.exe','-p','-c','-v','-classpath',str(jar),name],capture_output=True,text=True,check=True)
        stem=alias.replace('$','--')
        (out/(stem+'.javap.txt')).write_text(r.stdout,encoding='utf-8')
        (out/(stem+'.aliases.txt')).write_text(short(r.stdout),encoding='utf-8')
        data=zipfile.ZipFile(jar).read(name.replace('.','/')+'.class')
        manifest={'alias':alias,'class':name,'artifact':str(jar),'artifact_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'class_sha256':hashlib.sha256(data).hexdigest(),'evidence':stem+'.javap.txt'}
        (out/(stem+'.json')).write_text(json.dumps(manifest,indent=2),encoding='utf-8');print(json.dumps(manifest))
    elif op=='native':
        import native_collect
        native_collect.main(args)
    else: raise SystemExit('Unknown operation')
if __name__=='__main__':main()
