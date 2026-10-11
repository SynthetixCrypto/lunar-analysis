import pickle,sys,re,os
S=os.path.dirname(os.path.abspath(__file__))
C=pickle.load(open(os.path.join(S,'classes.pkl'),'rb'))
A={'F':'com.moonsworth.lunar.client.RIHHCHHHROOHOOIOIIRIOOCRHHOOOR.','S':'com.moonsworth.lunar.client.OHRHIRHIHIORRCHRHCCCOOOCORCRIR.','L':'com.moonsworth.lunar.client.','B':'com.moonsworth.lunar.RORCICOHRIOIIIOIOHIIIICRCIHRII.'}
import hashlib,builtins
_p=builtins.print
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def sh(x):
    x=str(x).replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.','ML.').replace('com/moonsworth/lunar/','ML/')
    return TOK.sub(lambda m:'_'+hashlib.md5(m.group(0).encode()).hexdigest()[:6],x)
SHORT=os.environ.get('FULL')!='1'
def print(*a,**k):
    _p(*[sh(i) if SHORT else i for i in a],**k)
def ex(n):
    n=n.replace('/','.')
    for k,v in A.items():
        if n.startswith(k+':'): n=v+n[2:]
    if '_' in n:  # resolve short hash tokens
        global REV
        try: REV
        except NameError:
            REV={}
            for c in C:
                for t in TOK.findall(c): REV['_'+hashlib.md5(t.encode()).hexdigest()[:6]]=t
        n=re.sub(r'_[0-9a-f]{6}',lambda m:REV.get(m.group(0),m.group(0)),n)
        n=n.replace('L.','com.moonsworth.lunar.client.',1) if n.startswith('L.') else n
        n=n.replace('ML.','com.moonsworth.lunar.',1) if n.startswith('ML.') else n
    return n
cmd=sys.argv[1]
if cmd=='show':  # full class
    n=ex(sys.argv[2]); t=C.get(n)
    lim=int(sys.argv[3]) if len(sys.argv)>3 else 400
    print('\n'.join(t.split('\n')[:lim]) if t else 'NOTFOUND '+n)
elif cmd=='sig': # header + member signatures only
    n=ex(sys.argv[2]); t=C.get(n)
    if not t: print('NOTFOUND',n); sys.exit()
    for l in t.split('\n'):
        if l and (not l.startswith('    ')) : print(l)
elif cmd=='meth': # method body by name substring
    n=ex(sys.argv[2]); t=C[n]; pat=sys.argv[3]
    lines=t.split('\n'); on=False
    for l in lines:
        if l.startswith('  ') and not l.startswith('    ') and l.strip():
            on = pat in sh(l) or pat in l
        if on: print(l)
elif cmd=='grep': # classes whose text matches regex
    r=re.compile(sys.argv[2]); lim=int(sys.argv[3]) if len(sys.argv)>3 else 50
    k=0
    for n,t in C.items():
        if r.search(t):
            print(n); k+=1
            if k>=lim: break
elif cmd=='grepl': # matching lines with class
    r=re.compile(sys.argv[2]); lim=int(sys.argv[3]) if len(sys.argv)>3 else 80
    k=0
    for n,t in C.items():
        for l in t.split('\n'):
            if r.search(l):
                print(n.replace('com.moonsworth.lunar.client.','L:'),'|',l.strip()[:220]); k+=1
                if k>=lim: sys.exit()
elif cmd=='sub': # direct subclasses/implementors
    n=ex(sys.argv[2])
    for c,t in C.items():
        h=t.split('\n')[0]
        if re.search(r'(extends|implements)[^{]*\b'+re.escape(n)+r'\b(?![.$\w])',h): print(c)
elif cmd=='strings':
    n=ex(sys.argv[2]); t=C[n]
    for s in re.findall(r'// String (.*)',t): print(s)
