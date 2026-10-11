import pickle,re,json,hashlib,collections
C=pickle.load(open('classes.pkl','rb'))
ev={e['class']:e for e in json.load(open('events.json'))}
POST='RCRHOOHIOCHHHHOCRIOCHRICIRCRRR/RORCICOHRIOIIIOIOHIIIICRCIHRII.COOCHIRORIICRCIIRIROHIIRIRICCH:(Ljava/lang/Class;Ljava/util/function/Supplier;)'
rows=json.load(open('hooks.json'))
stat=collections.Counter(); bad=[]
for cn,meth,evc,tgt,ann in rows:
    if not tgt or not evc: continue
    e=ev.get(evc.replace('/','.'))
    if not e or not e['cancellable']: continue
    t=C[cn]; body=''; on=False
    for l in t.split('\n'):
        if l.startswith('  ') and not l.startswith('    ') and '(' in l: on=(re.search(r'\b'+re.escape(meth)+r'\(',l) is not None)
        elif on: body+=l+'\n'
    checks='isCancelled' in body
    cancels=('CallbackInfo.cancel' in body or 'CallbackInfoReturnable.setReturnValue' in body or 'CallbackInfoReturnable.cancel' in body)
    wraps='Operation.call' in body
    k=('checks' if checks else 'nocheck')+'/'+('cancelsCI' if cancels else ('wrapOp' if wraps else 'other'))
    stat[k]+=1
    if not checks: bad.append((tgt[0].split('/')[-1],meth,evc.split('/')[-1][-30:]))
print(stat); print(len(bad)); print(bad[:25])
