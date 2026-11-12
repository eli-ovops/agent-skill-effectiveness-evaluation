"""Probe only synthetic files and a blocked loopback port, never credentials."""
import errno
import json
import socket
import sys
from pathlib import Path

canary = Path(sys.argv[1])
checks = {}
try:
    with canary.open('rb'):
        checks['read_outside'] = False
except PermissionError:
    checks['read_outside'] = True
try:
    with canary.open('ab'):
        checks['write_outside'] = False
except PermissionError:
    checks['write_outside'] = True
try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        result = sock.connect_ex(('127.0.0.1', 0))
    checks['network_outbound'] = result in (errno.EPERM, errno.EACCES)
    checks['network_errno'] = result
except PermissionError as exc:
    checks['network_outbound'] = True
    checks['network_errno'] = exc.errno
print(json.dumps(checks, sort_keys=True))
raise SystemExit(0 if all(v for k, v in checks.items() if k != 'network_errno') else 1)
