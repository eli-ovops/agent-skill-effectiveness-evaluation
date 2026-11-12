"""Freeze anonymous artifacts, verify input identity, and prepare blind review."""
import hashlib
import json
import shutil
from pathlib import Path

base = Path(__file__).resolve().parent.parent
frozen = base.parent / 'optimization' / 'frozen'
assignments = json.loads((base / 'runs/assignment.json').read_text())
manifest = json.loads((frozen / 'manifest.json').read_text())
blind = base / 'runs' / 'blind'
blind.mkdir(exist_ok=False)
shutil.copyfile(base / 'BLACK_BOX_RUBRIC.md', blind / 'BLACK_BOX_RUBRIC.md')
audit = []

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def compare_resources(identity, arm, destination):
    prefix = f'{arm}/{identity}/'
    resources = [r for r in manifest if r['path'].startswith(prefix)]
    return all((destination / r['path'][len(prefix):]).is_file() and
               sha(destination / r['path'][len(prefix):]) == r['sha256'] for r in resources)

for row in assignments:
    root = base / 'runs' / row['case']
    dst = blind / row['case']
    dst.mkdir()
    shutil.copytree(root / 'task', dst / 'task', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    for name in ('process.md', 'result.md', 'independent-checks.json', 'blind-trace.json'):
        source = root / name
        if source.is_file():
            shutil.copyfile(source, dst / name)
    fixtures_ok = sha(root / 'task/TASK.md') == row['fixture_sha256']['TASK.md']
    target_ok = compare_resources(row['target'], row['arm'], root / 'skill')
    common_ok = (row['target'] == 'user-ponytail' or
                 compare_resources('user-ponytail', 'after', root / 'common/ponytail'))
    trace = json.loads((root / 'raw-trace.json').read_text())
    audit.append({'case': row['case'], 'task_unchanged': fixtures_ok,
                  'target_resources_unchanged': target_ok, 'common_resources_unchanged': common_ok,
                  'source_thread_id': trace['sourceThreadId'], 'turn_id': trace['turnId'],
                  'duration_ms': trace['durationMs'],
                  'commands': sum(x['type'] == 'commandExecution' for x in trace['items']),
                  'file_change_events': sum(x['type'] == 'fileChange' for x in trace['items']),
                  'truncated_outputs': sum(bool(x.get('output', {}).get('truncated'))
                                           for x in trace['items'] if isinstance(x.get('output'), dict))})
(base / 'runs/input-integrity.json').write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'cases': len(audit),
                  'inputs_all_match': all(x['task_unchanged'] and x['target_resources_unchanged']
                                          and x['common_resources_unchanged'] for x in audit),
                  'truncated_outputs': sum(x['truncated_outputs'] for x in audit)}))
