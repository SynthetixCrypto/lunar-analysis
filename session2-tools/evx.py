import pickle,re,hashlib,json,collections,csv
C=pickle.load(open('classes.pkl','rb'))
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def sh(x): return TOK.sub(lambda m:'_'+hashlib.md5(m.group(0).encode()).hexdigest()[:6],x).replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.client.','L.').replace('com.moonsworth.lunar.','ML.').replace('com/moonsworth/lunar/','ML/')
BASE='com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.RROHOCRCCHCIORHICIHCOHRIRCIHCI'
CANC='com.moonsworth.lunar.client.RCRHOOHIOCHHHHOCRIOCHRICIRCRRR.OHRORRHCHCRICORRRCIRIOCCIRCRII'
par={}
for n,t in C.items():
    m=re.match(r'.*?class \S+ extends (\S+)',t.split('\n')[0])
    if m: par[n]=re.sub(r'<.*','',m.group(1))
def chain(n):
    out=[]
    while n in par and len(out)<20: n=par[n]; out.append(n)
    return out
events={n:chain(n) for n in C if BASE in chain(n)}
rows=json.load(open('hooks.json'))
posts=collections.defaultdict(list)
for cn,meth,ev,tgt,ann in rows:
    if not ev: continue
    e=ev.replace('/','.')
    t=(tgt[0] if tgt else '').replace('L','',1).rstrip(';').split('/')[-1] if tgt else ''
    posts[e].append((t or 'core:'+sh(cn).split('.')[-1], meth, ann))
out=[]
for n,ch in sorted(events.items(), key=lambda x:sh(x[0])):
    t=C[n]; hdr=t.split('\n')[0]
    fields=[sh(l.strip().rstrip(';')) for l in t.split('\n') if re.match(r'  (private|protected|public)( final)? [\w.$<>\[\], ?]+ \w+;$',l) and ' static ' not in l]
    ctors=[sh(l.strip()) for l in t.split('\n') if re.match(r'  (public|protected|private)? ?'+re.escape(n)+r'\(',l.replace(' '+n,' '+n))]
    ctors=[sh(l.strip().rstrip(';')) for l in t.split('\n') if l.startswith('  ') and not l.startswith('    ') and (n+'(') in l]
    canc=CANC in ch
    p=posts.get(n,[])
    out.append({'alias':sh(n),'class':n,'abstract':' abstract ' in hdr,'cancellable':canc,'parent':sh(ch[0]),'fields':fields,'ctors':ctors,'post_sites':len(p),'hooks':sorted(set(f'{a}.{b}' for a,b,c in p))[:12]})
json.dump(out,open('events.json','w'),indent=1)
print(len(out), sum(1 for o in out if o['post_sites']), sum(1 for o in out if o['cancellable']))
