"""Prepare the two separately authorized repeats with the original staging logic."""
from pathlib import Path

here = Path(__file__).resolve().parent
source = (here / 'prepare_runs.py').read_text()
start = source.index('# Fixed order, not randomized:')
end = source.index('output = []', start)
cases = '''# Supplementary interleaved order; see SUPPLEMENTARY_REPEATS.md.
cases = [
    ('case-07', 'complete', 'user-ponytail', 'after'),
    ('case-08', 'complete', 'user-ponytail', 'before'),
    ('case-09', 'approval', 'user-tdd', 'before'),
    ('case-10', 'approval', 'user-tdd', 'after'),
]
'''
generated = source[:start] + cases + source[end:]
old = "(base / 'runs' / 'assignment.json')"
new = "(base / 'runs' / 'repeat-assignment.json')"
if generated.count(old) != 1 or generated.count("'pairs': 3") != 1:
    raise SystemExit('original staging script shape changed; refusing to improvise')
generated = generated.replace(old, new).replace("'pairs': 3", "'pairs': 2")
snapshot = here / 'generated_prepare_repeats.py'
with snapshot.open('x') as f:
    f.write(generated)
exec(compile(generated, str(snapshot), 'exec'), {'__file__': str(snapshot), '__name__': '__main__'})
