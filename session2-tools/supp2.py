import pickle,re,hashlib,json
C=pickle.load(open('classes.pkl','rb'))
V=json.load(open('verfields.json'))
TOK=re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
def sh(x): return TOK.sub(lambda m:'_'+hashlib.md5(m.group(0).encode()).hexdigest()[:6],x).replace('com/moonsworth/lunar/client/','L/').replace('com.moonsworth.lunar.client.','L.').replace('com/moonsworth/lunar/','ML/')
B='CCHRHCCCHRIHCICICIRCORHRORIOCI$COOCHIRORIICRCIIRIROHIIRIRICCH.'
def fid(cls):
    for c in (cls, cls.split('$')[0]):
        t=C.get(c,'')
        m=re.search(r'public java.lang.String getId\(\);\n\s+Code:\n\s+0: ldc\s+#\d+\s+// String (\S+)',t)
        if m: return m.group(1)
    return '?'
NAMES={'_bb4487(I':'versionsAllowed','_1e73d7(I':'versionsDenied','_83cb4e(I)':'fromOrdinal..LATEST','_d3a8fd(I)':'0..ordinal','_e93d3c(II':'range','_0a1c78()':'1.8 + 1.21.2..LATEST','_596f3e()':'1.16.1(6)..LATEST','_d97743()':'0..1.12(5)','_05bcff()':'1.17.1(9)..LATEST','_21aca6(L':'server','_2f4182([':'requireAnyModule','_429bf0([':'requireAnyModuleAbsent','_bb4487(L':'fromVersion..LATEST','_1253fc(L':'v1_7..version','_cfe983(L':'range(versions)','_21aca6([':'versionsDenied(enum)','_cfe983([':'versionsAllowed(enum)','_88f3cf([':'requireAnyModule','_2ce426([':'requireAnyModuleAbsent'}
rows=[]
for n,t in C.items():
    if B not in t: continue
    cur=None; buf=[]
    blocks=[]
    for l in t.split('\n'):
        if l.startswith('  ') and not l.startswith('    ') and '(' in l:
            if cur: blocks.append((cur,buf))
            cur=l.strip(); buf=[]
        elif cur: buf.append(l)
    if cur: blocks.append((cur,buf))
    for meth,buf in blocks:
        if not any(B in x for x in buf): continue
        if 'static L._88f3cf._ba7d98$_cfe983 _a37102' in sh(meth) or n.endswith('$COOCHIRORIICRCIIRIROHIIRIRICCH') and 'CCHRHCCCHRIHCICICIRCORHRORIOCI' in n: continue
        seq=[]
        for l in buf:
            m=re.search(r'iconst_(\d)|bipush\s+(\d+)|sipush\s+(\d+)|ldc\s+#\d+\s+// String (.*)|getstatic .*Field (?:ML/|com/moonsworth/lunar/)(?:_cb9292|COOIOIRCCICRCCIHCCRHRCIHROHCCI)/_?\w*?[./](\w+):|getstatic .*_dd3308/_cfe983\.(\w+)|'+re.escape(B)+r'(\w+):\(([^)]*)\)',sh(l) if 'getstatic' in l and 'COOIOIRCCICRCCIHCCRHRCIHROHCCI' in l else l)
            if not m: continue
            g=m.groups()
            if g[0] or g[1] or g[2]: seq.append(g[0] or g[1] or g[2])
            elif g[3] is not None: seq.append('"'+g[3]+'"')
            elif g[4]: seq.append(V.get(g[4],g[4]))
            elif g[5]: seq.append('SERVER='+g[5])
            elif g[6]:
                k=sh(g[6])+'('+g[7][:2]
                seq.append('.'+next((v for kk,v in NAMES.items() if k.startswith(kk)),k))
        rows.append((fid(n),sh(n),' '.join(seq)))
for r in sorted(rows): print(' | '.join(r))
