"""Run checked-in evaluator and candidate tests after manual source inspection."""
import json
import subprocess
import sys
from pathlib import Path

base = Path(__file__).resolve().parent.parent
case, mode = sys.argv[1:]
if not case.startswith('case-') or mode not in ('complete', 'approval', 'diagnosis'):
    raise SystemExit('invalid case or mode')
root = (base / 'runs' / case).resolve()
task = (root / 'task').resolve()
if root.parent != (base / 'runs').resolve() or not task.is_dir():
    raise SystemExit('invalid task path')
python = '/Library/Developer/CommandLineTools/usr/bin/python3'
prefix = ['/usr/bin/sandbox-exec', '-f', str(root / 'sandbox.sb'), '/usr/bin/env', '-i',
          'PATH=/usr/bin:/bin', python, '-I', '-B']
commands = {
    'blackbox': [str(base / 'grader/check_candidate.py'), mode, str(task)],
    'candidate_tests': ['-m', 'unittest', 'discover', '-s', str(task), '-v'],
}
out = {}
for name, suffix in commands.items():
    try:
        result = subprocess.run(prefix + suffix, cwd=str(task), env={'PATH': '/usr/bin:/bin'},
                                capture_output=True, text=True, timeout=15)
        out[name] = {'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr,
                     'timeout': False}
    except subprocess.TimeoutExpired:
        out[name] = {'timeout': True}
destination = root / 'independent-checks.json'
if destination.exists():
    raise SystemExit('refusing to overwrite an existing validation record')
destination.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'case': case, 'results': {k: {'exit': v.get('exit'), 'timeout': v['timeout']}
                                           for k, v in out.items()}}))
