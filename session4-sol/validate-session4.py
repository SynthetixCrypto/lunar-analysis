"""Validate research files only. Does not open installation artifacts or run Lunar.

First run creates the retained-evidence digest manifest. Later runs compare it
without replacing it. Writes stay beside this script. Uses Python stdlib/Git.
"""
import csv
import hashlib
import json
import pathlib
import re
import subprocess
from urllib.parse import unquote, urlsplit

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
MANIFEST = HERE / 'evidence-files.sha256.tsv'
RESULT = HERE / 'session4-validation.json'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def text(path):
    data = path.read_bytes()
    if data.startswith((b'\xff\xfe', b'\xfe\xff')):
        return data.decode('utf-16')
    return data.decode('utf-8-sig')


def git(*args):
    try:
        p = subprocess.run(['git', '-C', str(ROOT), *args],
                           capture_output=True, check=False)
        return p.stdout if p.returncode == 0 else None
    except OSError:
        return None


def main():
    result = {
        'type': 'research-document-validation',
        'coverage': 'Session-4 Markdown links/citations/evidence hashes; prior root report Git comparisons',
        'target_execution_performed': False,
        'installation_artifacts_read_by_validator': False,
        'semantic_or_runtime_validation': False,
        'documents': {},
        'missing_relative_links': [],
        'missing_citation_paths': [],
    }
    documents = sorted(HERE.glob('*.md')) + [ROOT / 'README.md']
    for doc in documents:
        content = text(doc)
        name = doc.relative_to(ROOT).as_posix()
        result['documents'][name] = {
            'bytes': doc.stat().st_size, 'lines': len(content.splitlines()),
            'sha256': sha(doc.read_bytes()),
        }
        for link in re.findall(r'\]\(([^)]+)\)', content):
            link = link.strip().strip('<>')
            if not link or link.startswith('#') or urlsplit(link).scheme:
                continue
            local = unquote(link.split('#', 1)[0].split('?', 1)[0])
            target = (doc.parent / local).resolve()
            generated_outputs = {MANIFEST, RESULT}
            if local and not target.exists() and target not in generated_outputs:
                result['missing_relative_links'].append({'document': name, 'link': link})

    with (HERE / 'finding-locations.tsv').open(encoding='utf-8-sig', newline='') as f:
        locations = list(csv.DictReader(f, delimiter='\t'))
    ids = [row['finding_id'] for row in locations]
    result['finding_groups'] = len(ids)
    result['duplicate_finding_ids'] = sorted({key for key in ids if ids.count(key) > 1})
    for row in locations:
        for field in ('primary_evidence', 'mapping'):
            if not (HERE / row[field]).is_file():
                result['missing_citation_paths'].append({
                    'finding_id': row['finding_id'], 'field': field, 'path': row[field]})

    current = {}
    for directory in sorted(HERE.glob('evidence-*')):
        if directory.is_dir() and not directory.is_symlink():
            for path in sorted(directory.rglob('*')):
                if path.is_file() and not path.is_symlink():
                    current[path.relative_to(HERE).as_posix()] = sha(path.read_bytes())
    created = not MANIFEST.exists()
    if created:
        with MANIFEST.open('x', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter='\t', lineterminator='\n')
            writer.writerow(['path', 'sha256'])
            writer.writerows(current.items())
    with MANIFEST.open(encoding='utf-8-sig', newline='') as f:
        recorded = {r['path']: r['sha256'] for r in csv.DictReader(f, delimiter='\t')}
    result['evidence_manifest'] = {
        'path': MANIFEST.name,
        'created_this_run': created,
        'baseline_meaning': 'First validator run, not start of investigation',
        'files': len(current),
        'changed': sorted(p for p in current.keys() & recorded.keys() if current[p] != recorded[p]),
        'added': sorted(current.keys() - recorded.keys()),
        'missing': sorted(recorded.keys() - current.keys()),
    }

    historical = ROOT / 'session3-report-validation.json'
    result['historical_prefix_checks'] = {}
    if historical.is_file():
        old = json.loads(text(historical))
        for name, entry in old.get('preservation', {}).items():
            # Only named root research Markdown reports, never paths into installation.
            if pathlib.Path(name).name != name or not name.endswith('.md'):
                continue
            data = (ROOT / name).read_bytes()
            actual = sha(data[:entry['original_bytes']])
            result['historical_prefix_checks'][name] = {
                'bytes': entry['original_bytes'], 'sha256': actual,
                'matches_recorded_prefix': actual == entry['original_sha256'],
            }

    head = git('rev-parse', 'HEAD')
    result['git_preservation'] = {
        'baseline': head.decode().strip() if head else None,
        'baseline_meaning': 'Current HEAD, not a pre-session snapshot',
        'prior_root_markdown': {},
        'unavailable': [],
    }
    for report in sorted(ROOT.glob('*.md')):
        if report.name == 'README.md':
            continue
        prior = git('show', 'HEAD:' + report.name) if head else None
        if prior is None:
            result['git_preservation']['unavailable'].append(report.name)
        else:
            data = report.read_bytes()
            result['git_preservation']['prior_root_markdown'][report.name] = {
                'byte_identical_to_HEAD': prior == data,
                'same_after_CRLF_normalization': prior.replace(b'\r\n', b'\n') == data.replace(b'\r\n', b'\n'),
                'sha256': sha(data),
            }

    manifest = result['evidence_manifest']
    failures = bool(result['missing_relative_links'] or result['missing_citation_paths']
                    or result['duplicate_finding_ids'] or manifest['changed']
                    or manifest['added'] or manifest['missing'])
    failures |= any(not r['matches_recorded_prefix'] for r in result['historical_prefix_checks'].values())
    result['document_and_evidence_checks_passed'] = not failures
    result['limitations'] = [
        'Checks paths, hashes and historical comparisons, not Java/native semantics.',
        'No claim of a captured start-of-session preservation baseline.',
        'Git differences are reported, not reverted; unavailable history is not success.',
        'Raw Git byte comparison can differ because of text=auto line-ending normalization; normalized comparison is separate.',
        'Evidence hashes bind original bytes; later Git checkout filters can change text-file digests.',
        'Markdown fragment anchors are not checked; all links checked for local path existence.',
        'Research hash manifest does not authorize public redistribution.',
    ]
    RESULT.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({
        'checks_passed': not failures, 'documents': len(documents),
        'finding_groups': len(ids), 'evidence_files': len(current),
        'missing_links': len(result['missing_relative_links']),
        'missing_citation_paths': len(result['missing_citation_paths']),
        'prior_root_reports_content_different_from_HEAD': [
            n for n, v in result['git_preservation']['prior_root_markdown'].items()
            if not v['same_after_CRLF_normalization']],
        'result': str(RESULT),
    }, indent=2))
    return 1 if failures else 0


if __name__ == '__main__':
    raise SystemExit(main())
