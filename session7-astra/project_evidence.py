"""Create readable derived views; MCP envelopes remain canonical evidence."""
import pathlib,json,struct
R=pathlib.Path(__file__).resolve().parent;O=R/'views';O.mkdir(exist_ok=True)
rows=[]
for p in sorted((R/'evidence').glob('*.json')):
 try:
  envelope=json.loads(p.read_text())
  if not isinstance(envelope,dict):continue
  d=envelope.get('structuredContent')
  if d is None:continue
  n=d.get('normalized_result',{})
  rows.append(dict(file=p.name,evidence_id=d.get('evidence_id'),operation=d.get('operation'),parameters=d.get('parameters')))
  if isinstance(n,dict) and 'pseudocode' in n:
   (O/(p.stem+'.txt')).write_text('Evidence: '+d['evidence_id']+'\nAddress: '+n['procedure']['address']+'\n'+n['pseudocode'].replace('\r',''),encoding='utf8')
  if isinstance(n,dict) and 'bytes_hex' in n and 'table' in p.stem:
   b=bytes.fromhex(n['bytes_hex']);v=[dict(offset=hex(i),pointer=hex(struct.unpack_from('<Q',b,i)[0])) for i in range(0,len(b)-7,8)]
   (O/(p.stem+'.json')).write_text(json.dumps(v,indent=2))
 except (KeyError,ValueError):continue
(R/'evidence-catalog.json').write_text(json.dumps(rows,indent=2))
print('Projected',len(rows),'MCP responses')
