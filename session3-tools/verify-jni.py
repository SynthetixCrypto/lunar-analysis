"""Compare javap native declarations with retained DLL exports; no target execution.

Usage: python verify-jni.py SCRATCH RESEARCH
"""
import hashlib
import json
import pathlib
import re
import struct
import subprocess
import sys

scratch, research = map(pathlib.Path, sys.argv[1:3])
root = scratch / 'lunar'
names = sorted(str(p.relative_to(root).with_suffix('')).replace('\\', '.')
               for p in (root / 'com/moonsworth/webosr').rglob('*.class'))
javap = r'C:\Program Files\Microsoft\jdk-21.0.10.7-hotspot\bin\javap.exe'
text = subprocess.run([javap, '-p', '-c', '-classpath', str(root), *names],
                      capture_output=True, text=True, check=True).stdout
(research / 'webosr-native-declarations.javap.txt').write_text(text, encoding='utf-8')
expected = []
current = None
for line in text.splitlines():
    match = re.search(r'\b(?:class|interface) (com\.moonsworth\.webosr\.[^ <{]+)', line)
    if match:
        current = match[1]
    if current and ' native ' in line:
        method = re.search(r'\b([\w$]+)\(', line)[1]
        encoded = (current.replace('_', '_1').replace('$', '_00024').replace('.', '_')
                   + '_' + method.replace('_', '_1').replace('$', '_00024'))
        expected.append({'class': current, 'declaration': line.strip(), 'symbol': 'Java_' + encoded})
native = json.loads((research / 'native-pe-session3.json').read_text())[0]
exports = set(native['exports'])
symbols = {item['symbol'] for item in expected}
p = pathlib.Path(native['path']).parent / 'webp-imageio32.dll'
b = p.read_bytes()
coff = struct.unpack_from('<I', b, 0x3c)[0] + 4
result = {'java_native_declarations': len(expected), 'dll_exports': len(exports),
          'java_only': [item for item in expected if item['symbol'] not in exports],
          'dll_only': sorted(exports - symbols), 'declarations': expected,
          'webp32': {'path': str(p), 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest(),
                     'machine': hex(struct.unpack_from('<H', b, coff)[0]), 'machine_file_offset': coff}}
(research / 'native-jni-session3-verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k != 'declarations'}, indent=2))
