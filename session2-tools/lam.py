import sys,subprocess,re,os,hashlib
S=os.path.dirname(os.path.abspath(__file__))
full=subprocess.run(['python',os.path.join(S,'rev.py'),sys.argv[1]],capture_output=True,text=True).stdout.split('= ',1)[1].strip()
for root in ('lunar','modern','genesis','common'):
    out=subprocess.run(['javap','-v','-p','-cp',os.path.join(S,root),full],capture_output=True,text=True).stdout
    if 'BootstrapMethods' in out: break
bm=out.split('BootstrapMethods:')[1].split('\n')
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def sh(x): return TOK.sub(lambda m:'_'+hashlib.md5(m.group(0).encode()).hexdigest()[:6],x).replace('com/moonsworth/lunar/client/','L/').replace('com/moonsworth/lunar/','ML/')
cur=None
for l in bm:
    m=re.match(r'\s+(\d+): #\d+ (\S+)',l)
    if m: cur=m.group(1); kind='lambda' if 'LambdaMetafactory' in l else ('concat' if 'StringConcat' in l else 'other'); continue
    if cur is not None and 'REF_' in l and 'LambdaMetafactory' not in l and kind=='lambda':
        print(cur,'->',sh(l.split('REF_',1)[1].strip())); cur=None
