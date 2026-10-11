"""Static evidence capture. Reads analyst pickle/class bytes; runs only JDK javap.
Never imports, loads, or executes target classes. Outputs confined to this directory.
"""
import sys, pathlib, pickle, hashlib, re, subprocess, json, zipfile

HERE = pathlib.Path(__file__).resolve().parent
SCRATCH = pathlib.Path(r'C:\Users\Admin\AppData\Local\Temp\claude\C--Users-Admin-Downloads-New-folder-lunar-analysis\eeca5643-ee80-46b2-970c-8533c6845d76\scratchpad')
JAVAP = pathlib.Path(r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe')
ARCHIVES = {
    'lunar': pathlib.Path(r'C:\Users\Admin\.lunarclient\offline\multiver\lunar.jar'),
    'modern': pathlib.Path(r'C:\Users\Admin\.lunarclient\offline\multiver\modern-0.1.0-SNAPSHOT-all-nomappings.jar'),
}
C = pickle.loads((SCRATCH / 'classes.pkl').read_bytes())
TOK = re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')
REV = {}
for name in C:
    for token in TOK.findall(name):
        key = '_' + hashlib.md5(token.encode()).hexdigest()[:6]
        if key in REV and REV[key] != token:
            raise ValueError('Ambiguous alias ' + key)
        REV[key] = token

def expand(alias):
    name = alias.replace('L.', 'com.moonsworth.lunar.client.', 1) if alias.startswith('L.') else alias
    if name.startswith('ML.'):
        name = name.replace('ML.', 'com.moonsworth.lunar.', 1)
    return re.sub(r'_[0-9a-f]{6}', lambda m: REV[m.group(0)], name)

def shorten(text):
    text = text.replace('com.moonsworth.lunar.client.', 'L.').replace('com/moonsworth/lunar/client/', 'L/')
    text = text.replace('com.moonsworth.lunar.', 'ML.').replace('com/moonsworth/lunar/', 'ML/')
    return TOK.sub(lambda m: '_' + hashlib.md5(m.group(0).encode()).hexdigest()[:6], text)

ALIASES = [
    'L._d4ca6c._590f69', 'L._d4ca6c._cfe983',
    'L._d4ca6c._bb4487', 'L._d4ca6c._590f69$_cfe983',
    'L._d4ca6c._590f69$_21aca6', 'L._d4ca6c._21aca6',
    'L._d4ca6c._1e73d7', 'L._ba7d98._1e73d7._590f69',
    'ML._590f69._bb4487._13ea87._a1dd3a',
]
SELECTED = {
    'ML._d4ca6c._d4ca6c._21aca6._21aca6._21aca6': lambda signature: '_3d8570' in shorten(signature),
    'L._cfe983': lambda signature: expand('L._cfe983') + '();' in signature,
    'L._88f3cf._bb4487._a1dd3a._21aca6._21aca6._21aca6': lambda signature: '_f54c89' in shorten(signature),
    'L._88f3cf._bb4487._a1dd3a._d4ca6c': lambda signature: '_3c6778' in shorten(signature) or '_1253fc(' in shorten(signature),
}
ALIASES += list(SELECTED)

def selected_blocks(text, alias):
    lines = text.splitlines()
    out = [lines[0], '// SELECTED METHODS ONLY; unrelated methods omitted.']
    active = False
    for line in lines[1:]:
        if line.startswith('  ') and not line.startswith('    ') and line.strip():
            active = SELECTED[alias](line)
        if active:
            if alias == 'L._cfe983':
                # Preserve only constructor lock acquire/release/tail and exception table.
                m = re.match(r'\s+(\d+):', line)
                if m and not (int(m.group(1)) <= 50 or int(m.group(1)) >= 1720):
                    continue
            out.append(line)
    return '\n'.join(out) + '\n'
manifest = {'method': 'fresh JDK javap -p -c and -p -v; cached analyst index for comparison',
            'javap': str(JAVAP), 'scratch': str(SCRATCH),
            'archives': {k: {'path': str(v), 'sha256': hashlib.sha256(v.read_bytes()).hexdigest()} for k,v in ARCHIVES.items()},
            'classes': []}
ZIPS = {k: zipfile.ZipFile(v) for k,v in ARCHIVES.items()}
for alias in ALIASES:
    name = expand(alias)
    member = name.replace('.', '/') + '.class'
    present = [k for k,z in ZIPS.items() if member in z.namelist()]
    if not present:
        raise FileNotFoundError(name)
    artifact = present[0]
    data = ZIPS[artifact].read(member)
    stem = alias.replace('.', '-').replace('$', '--')
    cache = C.get(name)
    row = {'alias': alias, 'original_jvm_class': name, 'artifact': artifact,
           'archive_member': member, 'archive_path': str(ARCHIVES[artifact]),
           'class_sha256': hashlib.sha256(data).hexdigest()}
    for option, suffix in (('-c', 'javap-c.txt'), ('-v', 'javap-v.txt')):
        # Archive classpath avoids long Windows extracted-member paths; javap only parses bytes.
        result = subprocess.run([str(JAVAP), '-p', option, '-classpath', str(ARCHIVES[artifact]), name], capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        raw = result.stdout
        if alias in SELECTED:
            raw = selected_blocks(raw, alias)
        out = HERE / (stem + '.' + suffix)
        out.write_text(raw, encoding='utf-8')
        row[suffix] = out.name
        if option == '-c' and cache is not None:
            # Cache may differ only in leading/trailing newlines.
            if alias in SELECTED:
                cache = selected_blocks(cache, alias)
            row['cached_code_matches_fresh'] = raw.strip() == cache.strip()
            (HERE / (stem + '.aliases.txt')).write_text(shorten(raw), encoding='utf-8')
    manifest['classes'].append(row)
(HERE / 'class-mapping.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
bus_name = expand('L._d4ca6c._590f69').replace('.', '/')
debug_name = expand('L._d4ca6c._cfe983').replace('.', '/')
searches = {'scope': 'retained classes.pkl (all cached com/moonsworth disassembly only); references matched by exact owner and alias-rendered member', 'matches': []}
for n,t in C.items():
    for line in t.splitlines():
        if 'Method' not in line:
            continue
        s = shorten(line)
        if (bus_name + '.' in line and '_ef97c4:' in s) or (debug_name + '.' in line and '_ef6f38:' in s):
            searches['matches'].append({'class': n, 'alias': shorten(n), 'line': line})
searches['bus_ignore_flag_occurrences'] = [line for line in shorten(C[expand('L._d4ca6c._590f69')]).splitlines() if '_09429d' in line]
(HERE / 'bounded-reference-search.json').write_text(json.dumps(searches, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
