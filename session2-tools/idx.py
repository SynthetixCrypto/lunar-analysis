import re,sys,pickle,os
S=os.path.dirname(os.path.abspath(__file__))
hdr=re.compile(r'^(?:(?:public|private|protected|final|abstract|static|sealed|non-sealed|synchronized|strictfp)\s+)*(class|interface|enum|@interface)\s+(\S+)(.*)\{\s*$')
def parse(path):
    classes={}
    cur=None;buf=[]
    for line in open(path,encoding='utf-8',errors='replace'):
        if line.startswith('Compiled from'): continue
        m=hdr.match(line) if not line.startswith(' ') else None
        if m:
            if cur: classes[cur]=''.join(buf)
            name=m.group(2); name=re.sub(r'<.*','',name)
            cur=name; buf=[line]
        else:
            buf.append(line)
    if cur: classes[cur]=''.join(buf)
    return classes
allc={}
for f in ['lunar_moonsworth.javap','modern.javap','common.javap','genesis.javap']:
    c=parse(os.path.join(S,f))
    for k in c: c[k]=c[k]
    print(f,len(c))
    for k,v in c.items(): allc.setdefault(k,v)
pickle.dump(allc,open(os.path.join(S,'classes.pkl'),'wb'))
print(len(allc))
