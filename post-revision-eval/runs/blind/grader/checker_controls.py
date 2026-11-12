"""Exercise the pre-registered checker against synthetic passing and failing code."""
import json
import os
import subprocess
import sys
from pathlib import Path

base = Path(__file__).resolve().parent.parent
controls = base / 'runs' / 'checker-controls'
controls.mkdir(parents=True, exist_ok=False)
python = '/Library/Developer/CommandLineTools/usr/bin/python3'
env = {'PATH': '/usr/bin:/bin'}
positive = {
    'complete': '''def summarize(records):
    groups = {}
    total = 0
    for row in records:
        if not isinstance(row, dict) or 'group' not in row or 'units' not in row:
            raise ValueError('invalid record')
        group, units = row['group'], row['units']
        if not isinstance(group, str) or not group.strip() or type(units) is not int or units < 0:
            raise ValueError('invalid record')
        group = group.strip()
        total += units
        groups[group] = groups.get(group, 0) + units
    return {'records': len(records), 'total': total, 'groups': dict(sorted(groups.items()))}

def format_summary(summary):
    lines = [f"Records: {summary['records']}", f"Total units: {summary['total']}"]
    lines.extend(f'{group}: {units}' for group, units in sorted(summary['groups'].items()))
    return '\\n'.join(lines)
''',
    'approval': '''def normalize_tag(value):
    value = value.strip()
    if not value:
        raise ValueError('tag required')
    return value
''',
    'diagnosis': '''def effective_limit(limit=None):
    return 30 if limit is None else limit
def is_late(elapsed, limit=None):
    return elapsed > effective_limit(limit)
def render_status(elapsed, limit=None):
    return 'late' if is_late(elapsed, limit) else 'ok'
def export_status(elapsed, limit=None):
    return {'late': is_late(elapsed, limit)}
''',
}
files = {'complete': 'summary.py', 'approval': 'tags.py', 'diagnosis': 'delays.py'}
results = []
for mode, filename in files.items():
    for group in ('positive', 'negative'):
        task = controls / mode / group
        task.mkdir(parents=True)
        text = positive[mode] if group == 'positive' else (base / 'fixtures' / mode / filename).read_text()
        (task / filename).write_text(text)
        profile = task.parent / (group + '.sb')
        gen = subprocess.run([python, '-I', '-B', str(base / 'grader/sandbox_profile.py'), str(task)],
                             text=True, capture_output=True, timeout=10, env=env, check=True)
        profile.write_text(gen.stdout)
        cmd = ['/usr/bin/sandbox-exec', '-f', str(profile), '/usr/bin/env', '-i', 'PATH=/usr/bin:/bin',
               python, '-I', '-B', str(base / 'grader/check_candidate.py'), mode, str(task)]
        run = subprocess.run(cmd, text=True, capture_output=True, timeout=10, env=env)
        expected = 0 if group == 'positive' else 1
        results.append({'mode': mode, 'control': group, 'expected_exit': expected,
                        'exit': run.returncode, 'stdout': run.stdout.strip(),
                        'stderr': run.stderr.strip(), 'control_pass': run.returncode == expected})
report = {'controls': results, 'pass': all(r['control_pass'] for r in results)}
(controls / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'pass': report['pass'], 'cases': len(results),
                  'summary': [[r['mode'], r['control'], r['exit']] for r in results]}))
raise SystemExit(0 if report['pass'] else 1)
