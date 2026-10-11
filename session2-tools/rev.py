import sys,hashlib,pickle,re
C=pickle.load(open(__file__.replace('rev.py','classes.pkl'),'rb'))
toks=set()
for c in C: toks.update(re.findall(r'[CHIOR]{30}',c))
R={'_'+hashlib.md5(t.encode()).hexdigest()[:6]:t for t in toks}
def full(s):
    s=re.sub(r'_[0-9a-f]{6}',lambda m:R.get(m.group(0),m.group(0)),s)
    return s.replace('ML.','com.moonsworth.lunar.').replace('L.','com.moonsworth.lunar.client.') if s.startswith(('L.','ML.')) else s
for a in sys.argv[1:]: print(a,'=',full(a))
