import pickle,re,hashlib
C=pickle.load(open('classes.pkl','rb'))
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
H={}
for n in C:
    for t in TOK.findall(n): H['_'+hashlib.md5(t.encode()).hexdigest()[:6]]=t
def full(a): 
    a=re.sub(r'_[0-9a-f]{6}',lambda m:H.get(m.group(0),m.group(0)),a); return a.replace('L/','com/moonsworth/lunar/client/').replace('/','.')
def gid(cls):
    t=C.get(cls,'')
    m=re.search(r'java.lang.String getId\(\);\n\s+Code:\n((?:\s+\d+:.*\n){1,6})',t)
    if not m: 
        # inherited getId
        sup=re.match(r'.*?extends (\S+)',t.split('\n')[0])
        return ('(inherits '+gid(re.sub('<.*','',sup.group(1)))+')') if sup and sup.group(1)!='java.lang.Object' and sup.group(1) in C else '?'
    s=re.findall(r'// String (\S+)',m.group(1))
    return s[0] if s else 'computed'
rows=[];sec='always(varargs)'
for l in open('de.txt'):
    if '1419: getstatic' in l: sec='if !PRODUCTION'
    if '1549: getstatic' in l: sec='if !PRODUCTION && MC_VERSION>=8'
    if '1573: new' in l: sec='if !PRODUCTION'
    if '1693: getstatic' in l: sec='if RADIO flag'
    if '1723: new' in l: sec='always(appended)'
    m=re.search(r'new\s+#\d+\s+// class (L/\S+)',l)
    if m:
        a=m.group(1); rows.append((sec,a.replace('/','.'),gid(full(a))))
import collections
print(collections.Counter(r[0] for r in rows))
with open('registry.tsv','w') as f:
    f.write('order\tcondition\tclass_alias\tfeature_id\n')
    for i,r in enumerate(rows): f.write(f'{i}\t{r[0]}\t{r[1]}\t{r[2]}\n')
print([r[2] for r in rows if r[0]=='always(varargs)'][:100])
print([ (r[0],r[2]) for r in rows if r[0]!='always(varargs)'])
