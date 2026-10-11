"""Read saved javap text and TSV evidence; never load or execute target code.

Usage: python verify.py SCRATCH RESEARCH
Writes derived event citation tables, using the saved analyst index only.
"""
import collections
import csv
import hashlib
import json
import pathlib
import pickle
import re
import sys

scratch, research = map(pathlib.Path, sys.argv[1:3])
classes = pickle.loads((scratch / 'classes.pkl').read_bytes())
token = re.compile(r'(?<![A-Z])[CHIOR]{30}(?![A-Z])')


def short(text):
    text = text.replace('com.moonsworth.lunar.client.', 'L.').replace('com/moonsworth/lunar/client/', 'L/')
    text = text.replace('com.moonsworth.lunar.', 'ML.').replace('com/moonsworth/lunar/', 'ML/')
    return token.sub(lambda m: '_' + hashlib.md5(m[0].encode()).hexdigest()[:6], text)


def methods(text):
    signature, body = None, []
    for line in text.splitlines():
        if line.startswith('  ') and not line.startswith('    ') and line.strip():
            if signature is not None:
                yield signature, '\n'.join(body)
            signature, body = line.strip(), []
        else:
            body.append(line)
    if signature is not None:
        yield signature, '\n'.join(body)


def span(body):
    offsets = re.findall(r'^\s+(\d+):', body, re.M)
    return f'{offsets[0]}..{offsets[-1]}' if offsets else 'N/A (no Code)'


events = list(csv.DictReader((research / 'event-catalog.tsv').open(encoding='utf-8'), delimiter='\t'))
by_class = {row['event_class']: row for row in events}
by_alias = {row['event_alias']: row for row in events}
hooks = list(csv.DictReader((research / 'mixin-event-post-map.tsv').open(encoding='utf-8'), delimiter='\t'))
counts = collections.Counter()
audit = []
hook_locations = []
for row in hooks:
    candidates = [(sig, body) for sig, body in methods(classes[row['mixin_class']])
                  if re.search(r'\b' + re.escape(row['mixin_method']) + r'\(', sig)]
    hook_locations.append([short(row['mixin_class']), row['mixin_class'], row['mixin_method'],
                           row['event_class_alias'], '; '.join(span(b) for _, b in candidates)])
    event = by_class.get(row['event_class'].replace('/', '.'))
    if not event or event['cancellable'] != 'True' or not row['mixin_target']:
        continue
    body = '\n'.join(body for _, body in candidates)
    checks = 'isCancelled' in body
    counts['checks' if checks else 'no_check'] += 1
    posts = ','.join(re.findall(r'^\s+(\d+):.*(?:InterfaceMethod|Method).*\(Ljava/lang/Class;Ljava/util/function/Supplier;\)', body, re.M))
    audit.append([row['mixin_target'], short(row['mixin_class']), row['mixin_method'], event['event_alias'],
                  str(checks), '; '.join(span(b) for _, b in candidates), posts])
with (research / 'event-cancellation-audit.tsv').open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['mixin_target', 'mixin_alias', 'mixin_method', 'event_alias', 'reads_isCancelled', 'method_code_offsets', 'post_offsets'])
    writer.writerows(audit)

with (research / 'event-hook-bytecode-locations.tsv').open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['mixin_alias', 'mixin_class', 'mixin_method', 'event_alias', 'method_code_offsets'])
    writer.writerows(hook_locations)

with (research / 'event-bytecode-locations.tsv').open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['event_alias', 'artifact', 'event_class', 'constructor_signature', 'code_offsets'])
    for event in events:
        cn = event['event_class']
        for sig, body in methods(classes.get(cn, '')):
            if cn + '(' in sig:
                writer.writerow([event['event_alias'], 'lunar.jar', cn, short(sig), span(body)])

summary = {'event_classes': len(events), 'posted_types': sum(int(e['post_sites']) > 0 for e in events),
           'cancellable_classes': sum(e['cancellable'] == 'True' for e in events),
           'posted_skyblock_types': sum(int(e['post_sites']) > 0 and e['event_alias'].startswith('L._88f3cf._bb4487._23f752.') for e in events),
           'cancellable_mixin_post_sites': dict(counts)}
print(json.dumps(summary, indent=2))

migration_classes = []
for line in (research / 'settings-migration-steps.tsv').read_text(encoding='utf-8').splitlines():
    parts = line.split('\t')
    if len(parts) >= 4 and parts[0].isdigit():
        migration_classes.append((parts[0] + '->' + parts[1], parts[3]))
for cn in classes:
    if short(cn) in ['L._2b0ee0._cfe983._bb4487$1', 'L._02d7ad._d4ca6c']:
        migration_classes.append(('supporting', cn))
with (research / 'settings-migration-bytecode-locations.tsv').open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['transition', 'artifact', 'class_alias', 'jvm_class', 'method_signature', 'code_offsets', 'confidence'])
    for transition, cn in migration_classes:
        for sig, body in methods(classes.get(cn, '')):
            if '(' in sig or sig == 'static {};':
                writer.writerow([transition, 'lunar.jar', short(cn), cn, short(sig), span(body), 'Confirmed'])

selected = {'L._2f4182._1253fc._bb4487', 'L._2f4182._6c713e._cfe983',
            'L.util._d0d09a', 'L._02d7ad._1253fc._1253fc._590f69',
            'L._02d7ad._1253fc._1253fc._bb4487', 'L._2b0ee0._cfe983._bb4487',
            'L._02d7ad._cfe983', 'L._02d7ad._d4ca6c', 'L._ec7e36._13ea87',
            'L._d4ca6c._21aca6', 'L._d4ca6c._1e73d7',
            'L._81676d._21aca6._21aca6', 'L._81676d._21aca6._21aca6._cfe983',
            'L._81676d._21aca6._21aca6._cfe983._21aca6',
            'L._81676d._21aca6._590f69._cfe983._cfe983',
            'L._81676d._21aca6._590f69._02d7ad',
            'L._88f3cf._590f69._1253fc', 'L._88f3cf._590f69._cfe983'}
with (research / 'session3-bytecode-locations.tsv').open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['artifact', 'class_alias', 'jvm_class', 'method_signature', 'code_offsets', 'confidence'])
    for cn, text in classes.items():
        if short(cn) in selected:
            for sig, body in methods(text):
                if '(' in sig or sig == 'static {};':
                    writer.writerow(['lunar.jar', short(cn), cn, short(sig), span(body), 'Confirmed'])

reports = ['feature-registration-deep-dive.md', 'event-payloads.md', 'hud-math.md',
           'additional-module-traces.md', 'settings-persistence.md', 'native-analysis-preparation.md']
report_text = '\n'.join((research / name).read_text(encoding='utf-8') for name in reports)
with (research / 'session3-class-locations.tsv').open('w', encoding='utf-8', newline='') as out:
    writer = csv.writer(out, delimiter='\t')
    writer.writerow(['class_alias', 'jvm_class'])
    for cn in sorted(classes):
        if short(cn) in report_text:
            writer.writerow([short(cn), cn])
