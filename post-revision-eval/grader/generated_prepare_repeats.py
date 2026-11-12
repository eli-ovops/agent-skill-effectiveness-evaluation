"""Create isolated synthetic workspaces from already-frozen inputs."""
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

base = Path(__file__).resolve().parent.parent
optimization = base.parent / 'optimization'
frozen = optimization / 'frozen'
mapping = {r['id']: r for r in json.loads((frozen / 'mapping.json').read_text())}
files = json.loads((frozen / 'manifest.json').read_text())
backups = {r['source']: r for r in json.loads((optimization / 'backup-manifest.json').read_text())['files']}
python = '/Library/Developer/CommandLineTools/usr/bin/python3'
env = {'PATH': '/usr/bin:/bin'}

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def copy_skill(identity, arm, dest):
    row = mapping[identity]
    entry = Path(row['arms'][arm]['entry'])
    if sha(entry) != row['arms'][arm]['sha256']:
        raise ValueError('entry hash mismatch')
    if arm == 'before':
        record = backups[row['source']]
        if record['sha256_before'] != sha(entry) or sha(Path(record['backup'])) != sha(entry):
            raise ValueError('backup mismatch')
    prefix = f'{arm}/{identity}/'
    selected = [r for r in files if r['path'].startswith(prefix)]
    if not selected:
        raise ValueError('no frozen resources')
    for r in selected:
        rel = Path(r['path'][len(prefix):])
        source = frozen / r['path']
        if source.is_symlink() or sha(source) != r['sha256']:
            raise ValueError('resource missing or mismatch')
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha(target) != r['sha256']:
            raise ValueError('copy mismatch')
    return {'entry_sha256': sha(entry), 'resources': len(selected)}

# Supplementary interleaved order; see SUPPLEMENTARY_REPEATS.md.
cases = [
    ('case-07', 'complete', 'user-ponytail', 'after'),
    ('case-08', 'complete', 'user-ponytail', 'before'),
    ('case-09', 'approval', 'user-tdd', 'before'),
    ('case-10', 'approval', 'user-tdd', 'after'),
]
output = []
for name, fixture, identity, arm in cases:
    root = base / 'runs' / name
    root.mkdir(parents=True, exist_ok=False)
    task = root / 'task'
    shutil.copytree(base / 'fixtures' / fixture, task)
    target = copy_skill(identity, arm, root / 'skill')
    common = None
    if identity != 'user-ponytail':
        common = copy_skill('user-ponytail', 'after', root / 'common' / 'ponytail')
    profile = root / 'sandbox.sb'
    result = subprocess.run([python, '-I', '-B', str(base / 'grader/sandbox_profile.py'), str(task)],
                            env=env, capture_output=True, text=True, timeout=10, check=True)
    profile.write_text(result.stdout)
    runner = root / 'run-python'
    runner.write_text('#!/bin/sh\ncd ' + json.dumps(str(task)) + ' || exit 1\n' +
        'exec /usr/bin/sandbox-exec -f ' + json.dumps(str(profile)) +
        ' /usr/bin/env -i PATH=/usr/bin:/bin ' + python + ' -I -B "$@"\n')
    runner.chmod(0o755)
    output.append({'case': name, 'fixture': fixture, 'target': identity, 'arm': arm,
                   'target_frozen': target, 'common_frozen': common,
                   'fixture_sha256': {p.name: sha(p) for p in task.iterdir() if p.is_file()}})
(base / 'runs' / 'repeat-assignment.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'prepared': len(output), 'pairs': 2,
                  'common_ponytail_sha256': mapping['user-ponytail']['arms']['after']['sha256']}))
