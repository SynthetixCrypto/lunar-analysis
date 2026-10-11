import pickle,re,json,hashlib,sys
C=pickle.load(open('classes.pkl','rb'))
M=json.load(open(r'C:/Users/Admin/Downloads/New folder/lunar-analysis/minecraft-mixin-metadata.json'))
mix={}
for m in M['mixins']:
    if 'modern' not in m['file']: continue
    tgt=[v.get('class') or v for v in m['mixin'].get('value',[])] or m['mixin'].get('targets')
    meths={}
    for me in m['methods']:
        ann=[a for a in me.get('annotations',[]) if 'injection' in a['type'] or 'Inject' in a['type'] or 'Wrap' in a['type'] or 'Modify' in a['type'] or 'Redirect' in a['type']]
        if ann: meths[me['name']]=ann
    mix[m['class'].replace('/','.')]=(tgt,meths)
POST='RCRHOOHIOCHHHHOCRIOCHRICIRCRRR/RORCICOHRIOIIIOIOHIIIICRCIHRII.COOCHIRORIICRCIIRIROHIIRIRICCH:(Ljava/lang/Class;Ljava/util/function/Supplier;)'
rows=[]
for cn,t in C.items():
    if POST not in t: continue
    cur=None; lastcls=None
    for l in t.split('\n'):
        if l.startswith('  ') and not l.startswith('    ') and l.strip() and '(' in l:
            cur=re.search(r'([\w$]+)\(',l).group(1); lastcls=None
        m=re.search(r'ldc\s+#\d+\s+// class (\S+)',l)
        if m: lastcls=m.group(1)
        if POST in l and cur:
            tgt,meths=mix.get(cn,(None,{}))
            ann=meths.get(cur)
            a=''
            if ann:
                v=ann[0]['values']; a=ann[0]['type'].split('/')[-1].rstrip(';')+' '+json.dumps({k:v[k] for k in v if k in('method','at','cancellable')})[:200]
            rows.append((cn,cur,lastcls,tgt,a))
json.dump(rows,open('hooks.json','w'))
print(len(rows))
