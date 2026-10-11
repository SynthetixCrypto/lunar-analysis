"""Display-only compact bytecode preserving instruction offsets and branch operands."""
import pathlib,re
O=pathlib.Path(__file__).parent
for p in O.glob('*.short.txt'):
    lines=[]
    for l in p.read_text(encoding='utf-8').splitlines():
        if not l.strip(): continue
        l=re.sub(r'#\d+\s+// ', '// ',l)
        l=re.sub(r':\([^)]*\)\S+', '',l)
        l=re.sub(r':(?:LL/|LML/|Ljava/|Lit/)[^;]+;', '',l)
        l=re.sub(r'\s+', ' ',l).strip()
        lines.append(l)
    p.with_suffix('.compact.txt').write_text('\n'.join(lines),encoding='utf-8')
for p in O.glob('*.verbose-short.txt'):
    text=p.read_text(encoding='utf-8')
    boot=text.split('BootstrapMethods:',1)[1].split('InnerClasses:',1)[0] if 'BootstrapMethods:' in text else 'No BootstrapMethods'
    p.with_suffix('.bootstrap.txt').write_text(boot,encoding='utf-8')
inventory=[]
for p in O.glob('*.short.txt'):
    inventory.append(p.name)
    inventory.extend(l.strip() for l in p.read_text(encoding='utf-8').splitlines() if l.startswith('  ') and not l.startswith('    ') and ('(' in l or 'static {}' in l))
(O/'method-inventory.txt').write_text('\n'.join(inventory),encoding='utf-8')
