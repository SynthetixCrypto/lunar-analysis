"""Static-only evidence collection: javap and retained analyst disassembly.
Never imports/executes Lunar classes. Auth bodies and handshake construction excluded.
"""
from pathlib import Path
import hashlib, json, pickle, re, subprocess, zipfile

OUT = Path(__file__).resolve().parent
SCRATCH = Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
JAR = Path(r'C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar')
JAVAP = r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe'
C = pickle.loads((SCRATCH / 'classes.pkl').read_bytes())
TOK = re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
REV = {'_' + hashlib.md5(t.encode()).hexdigest()[:6]: t for n in C for t in TOK.findall(n)}
def full(s):
    s = re.sub(r'_[0-9a-f]{6}', lambda m: REV[m.group()], s)
    return s.replace('L.', 'com.moonsworth.lunar.client.', 1) if s.startswith('L.') else s
def short(s):
    return TOK.sub(lambda m: '_' + hashlib.md5(m.group().encode()).hexdigest()[:6], s.replace('com.moonsworth.lunar.client.', 'L.'))
def blocks(text):
    return re.findall(r'^  (?:public|private|protected|static).*?(?=^  (?:public|private|protected|static)|^\}\s*$|\Z)', text, re.M | re.S)
def dump(name, verbose=False, artifact=JAR):
    args = [JAVAP, '-J-Dfile.encoding=UTF-8', '-J-Dsun.stdout.encoding=UTF-8', '-classpath', str(artifact), '-p', '-c'] + (['-v'] if verbose else []) + [name]
    return subprocess.run(args, capture_output=True, text=True, encoding='utf-8', check=True).stdout
def write(name, text):
    (OUT / name).write_text(text, encoding='utf-8')

aliases = ['L._cb9292._21aca6', 'L._cb9292._21aca6$_cfe983', 'L._cb9292._cfe983', 'L.util._d930e6', 'L._21aca6._bb4487', 'L._cfe983']
write('class-map.tsv', 'alias\toriginal_jvm_class\n' + ''.join(a + '\t' + full(a) + '\n' for a in aliases))
manifest = {'artifact': str(JAR), 'sha256': hashlib.sha256(JAR.read_bytes()).hexdigest(), 'javap': JAVAP, 'static_only': True, 'outputs': []}
for alias, stem in [(aliases[0], 'rpc-channel'), (aliases[1], 'pending-entry'), (aliases[3], 'callback-dispatch')]:
    for verbose in (False, True):
        fname = stem + ('.verbose' if verbose else '') + '.javap.txt'
        write(fname, dump(full(alias), verbose))
        manifest['outputs'].append(fname)

transport = dump(full(aliases[2]))
selected = [b for b in blocks(transport) if any(k in short(b.splitlines()[0]) for k in (' onOpen(', ' onMessage(', ' onClose(', ' onError(', ' bootstrap(', ' _429bf0('))]
write('transport-lifecycle.javap.txt', '\n'.join(selected))
ctor = next(b for b in blocks(transport) if 'public ' + full(aliases[2]) + '(' in b.splitlines()[0])
write('transport-channel-binding.javap.txt', ctor.splitlines()[0] + '\n    Code excerpt (connection timeout argument and per-transport channel allocation only):\n' + '\n'.join(l for l in ctor.splitlines() if re.match(r'\s+(?:3[4-9]|4[0-9]|151|152|155):', l)) + '\n')
# Fresh verbose output: preserve bootstrap bindings only, not unrelated bodies/constant pool.
for alias, stem, indexes in [(aliases[2], 'transport', {12, 13, 14}), (aliases[5], 'client', {20, 29})]:
    verbose = dump(full(alias), True)
    tail = verbose[verbose.index('BootstrapMethods:'):].split('InnerClasses:')[0]
    entries = re.findall(r'^  \d+:.*?(?=^  \d+:|\Z)', tail, re.M | re.S)
    write(stem + '-bootstrap.txt', 'BootstrapMethods (selected entries):\n' + ''.join(b for b in entries if int(re.match(r'  (\d+):', b).group(1)) in indexes))
client = dump(full(aliases[5]))
write('client-reconnect.javap.txt', '\n'.join(b for b in blocks(client) if any(k in short(b.splitlines()[0]) for k in (' _555303(', ' _a61e7a('))))
# Shared backoff: only constructor null-input path and timing method retained.
backoff = dump(full(aliases[4]))
bs = blocks(backoff)
ctor = next(b for b in bs if 'WebSocketRichClosePush, long)' in b.splitlines()[0])
write('backoff-null-path.javap.txt', ctor.splitlines()[0] + '\n    Code excerpt (null input only; entry branch 4..5 goes to 101):\n' + '\n'.join(l for l in ctor.splitlines() if re.match(r'\s+(?:10[1-9]|11[0-9]|12[0-5]):', l)) + '\n\n' + next(b for b in bs if ' _a289d1(' in short(b.splitlines()[0])))
stub = 'com.lunarclient.gameipc.location.v1.LocationService$Stub'
write('location-stub.javap.txt', dump(stub))
write('protocol-common-proto.javap.txt', dump('com.lunarclient.gameipc.protocol.v1.CommonProto'))
response = dump('com.lunarclient.gameipc.protocol.v1.IPCRpcResponse')
write('response-accessors.javap.txt', '\n'.join(b for b in blocks(response) if any(k in b.splitlines()[0] for k in (' getRequestId();', ' getOutput();'))))
method_rows = []
for alias in aliases:
    for b in blocks(C[full(alias)]):
        if 'Code:' not in b:
            continue
        sig = b.splitlines()[0].strip()
        if alias == aliases[2] and not any(k in short(sig) for k in (' onOpen(', ' onMessage(', ' onClose(', ' onError(', ' bootstrap(', ' _429bf0(')):
            continue
        if alias == aliases[5] and not any(k in short(sig) for k in (' _555303(', ' _a61e7a(')):
            continue
        if alias == aliases[4] and not ('WebSocketRichClosePush, long)' in sig or ' _a289d1(' in short(sig)):
            continue
        offsets = re.findall(r'^\s+(\d+):', b, re.M)
        method_rows.append((alias, short(sig), sig, offsets[0], offsets[-1]))
write('method-map.tsv', 'class_alias\talias_signature\toriginal_signature\tfirst_offset\tlast_offset\n' + ''.join('\t'.join(row) + '\n' for row in method_rows))
# Bounded negative search: whole channel + non-auth gameipc caller method bodies in retained index.
hits = []
for name, text in C.items():
    for b in blocks(text):
        if re.search(r'InterfaceMethod com/lunarclient/gameipc/(?!auth/)[^\s]+', b):
            hits.append({'class': name, 'signature': b.splitlines()[0].strip(), 'future_or_timeout_symbols': sorted(set(re.findall(r'\b(?:CompletableFuture|SettableFuture|ListenableFuture|TimeoutException|orTimeout|completeOnTimeout)\b', b)))})
write('bounded-future-search.json', json.dumps({'scope': 'Retained classes.pkl; non-auth gameipc interface call-containing method bodies only, not transitive caller bodies or generated code', 'method_count': len(hits), 'methods': hits}, indent=2))
libraries = ['org.java_websocket.client.WebSocketClient', 'org.java_websocket.WebSocketImpl', 'com.google.common.cache.LocalCache', 'com.google.common.cache.LocalCache$Segment', 'com.google.common.cache.LocalCache$LocalManualCache']
library_methods = {
    libraries[0]: [' send(byte[]);', ' onWebsocketClose(', ' onWebsocketError('],
    libraries[1]: [' send(byte[]);', ' send(java.nio.ByteBuffer);', ' send(java.util.Collection<'],
    libraries[2]: [' getIfPresent(', ' isExpired(', ' processPendingNotifications('],
    libraries[3]: [' getLiveEntry(', ' get(java.lang.Object, int);', ' postReadCleanup(', ' runUnlockedCleanup(', ' tryExpireEntries(', ' expireEntries('],
    libraries[4]: [' getIfPresent(', ' invalidate(', ' invalidateAll(', ' cleanUp('],
}
for name in libraries:
    member = name.replace('.', '/') + '.class'
    providers = []
    for candidate in [JAR, JAR.parent / 'genesis-0.1.0-SNAPSHOT-all.jar', JAR.parent / 'common-0.1.0-SNAPSHOT-all-nomappings.jar']:
        with zipfile.ZipFile(candidate) as z:
            if member in z.namelist():
                providers.append(candidate)
    if not providers:
        continue
    provider = providers[0]
    fname = name.split('.')[-1] + '.selected.javap.txt'
    text = dump(name, artifact=provider)
    write(fname, '\n'.join(b for b in blocks(text) if any(k in b.splitlines()[0] for k in library_methods[name])))
    if name == libraries[0]:
        timing = []
        for b in blocks(text):
            sig = b.splitlines()[0]
            if 'java.util.Map<java.lang.String, java.lang.String>, int)' in sig or 'public void run();' in sig:
                lines = b.splitlines()
                selected = set()
                for i, line in enumerate(lines):
                    if 'Field connectTimeout:I' in line or 'Method java/net/Socket.connect:' in line:
                        selected.update(range(max(2, i - 3), min(len(lines), i + 2)))
                if selected:
                    timing.append(sig + '\n    Code excerpt:\n' + '\n'.join(lines[i] for i in sorted(selected)))
        write('WebSocketClient-connect-timeout.txt', '\n\n'.join(timing) + '\n')
    manifest.setdefault('library_artifacts', []).append({'class': name, 'provider': str(provider), 'sha256': hashlib.sha256(provider.read_bytes()).hexdigest(), 'output': fname})
manifest['supporting_files'] = [{'path': p.name, 'bytes': p.stat().st_size, 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(OUT.iterdir()) if p.is_file() and p.name != 'manifest.json']
write('manifest.json', json.dumps(manifest, indent=2))
print(json.dumps({'artifact_sha256': manifest['sha256'], 'non_auth_gameipc_call_methods': len(hits), 'future_timeout_hits': [h for h in hits if h['future_or_timeout_symbols']]}, indent=2))
