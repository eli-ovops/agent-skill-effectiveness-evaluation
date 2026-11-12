"""Produce a separate blinded dossier for the two supplemental pairs."""
from pathlib import Path

here = Path(__file__).resolve().parent
source = (here / 'build_blind_dossier.py').read_text()
replacements = {
    "'runs/assignment.json'": "'runs/repeat-assignment.json'",
    "base / 'runs' / 'blind'": "base / 'runs' / 'blind' / 'repeats'",
    "'runs/input-integrity.json'": "'runs/repeat-input-integrity.json'",
}
for old, new in replacements.items():
    if source.count(old) != 1:
        raise SystemExit('original dossier script changed; refusing to improvise')
    source = source.replace(old, new)
snapshot = here / 'generated_build_repeat_dossier.py'
with snapshot.open('x') as f:
    f.write(source)
exec(compile(source, str(snapshot), 'exec'), {'__file__': str(snapshot), '__name__': '__main__'})
