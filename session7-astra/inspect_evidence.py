"""Readable projections of locally retained MCP responses; never edits targets."""
import json,sys,pathlib
root=pathlib.Path(__file__).parent
def load(name):
    r=json.loads((root/'evidence'/f'{name}.json').read_text())
    return r.get('structuredContent') or json.loads(r['content'][0]['text'])
if sys.argv[1]=='schema':
    d=json.loads((root/'tools-catalog.json').read_text())
    for t in d['tools']:
        if t['name'] in sys.argv[2:]: print(json.dumps(t,indent=2))
elif sys.argv[1]=='pseudo':
    for name in sys.argv[2:]:
        d=load(name); n=d.get('normalized_result',d)
        print('\n###',name,'Evidence:',d.get('evidence_id'))
        if isinstance(n,dict) and 'pseudocode' in n:
            print(n['procedure']['address'],n['procedure']['name']); print(n['pseudocode'].replace('\r',''))
        else: print(json.dumps(n,indent=2))
elif sys.argv[1]=='make':
    calls=[]
    for item in sys.argv[3:]:
        if ':' in item:
            ident,proc=item.split(':',1)
        else: ident=proc=item
        calls.append(dict(id=ident,name='analyze_function',arguments=dict(procedure=proc)))
    (root/sys.argv[2]).write_text(json.dumps(dict(calls=calls),indent=2))
else:
    for name in sys.argv[1:]:
        d=load(name); n=d.get('normalized_result',d)
        print('\n###',name,'Evidence:',d.get('evidence_id'))
        if isinstance(n,dict) and 'pseudocode' in n:
            print(json.dumps(n,indent=2))
        else: print(json.dumps(n,indent=2))
