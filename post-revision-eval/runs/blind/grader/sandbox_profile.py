"""Build a defense-in-depth macOS profile; not a complete tool sandbox."""
import json
import sys
from pathlib import Path

here = Path(__file__).resolve().parent
base = here.parent
task = Path(sys.argv[1]).resolve()
if (base / 'runs').resolve() not in task.parents or not task.is_dir():
    raise SystemExit('task directory must exist inside evaluation runs')
q = lambda s: json.dumps(str(s))
print('(version 1)')
print('(allow default)')
print('(deny network*)')
print('(deny file-write*)')
print('(deny file-read-data ' + ' '.join('(subpath ' + q(x) + ')' for x in [
    '/Users', '/Volumes', '/private', '/Library', '/usr/local', '/opt',
    '/Applications', '/cores', '/System/Volumes/Data',
]) + ')')
print('(deny mach-lookup)')
print('(deny process-fork)')
print('(deny process-exec)')
print('(allow sysctl-read)')
print('(allow file-read-data ' + ' '.join('(subpath ' + q(x) + ')' for x in [
    '/Library/Developer/CommandLineTools', str(here), str(task),
]) + ')')
print('(allow file-write-data (literal "/dev/null"))')
print('(allow process-exec (literal "/usr/bin/env") (literal "/usr/bin/python3")' +
      ' (subpath "/Library/Developer/CommandLineTools"))')
