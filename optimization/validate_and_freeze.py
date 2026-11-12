#!/usr/bin/env python3
"""Validate bounded Skill edits and preserve reproducible before/after inputs."""
from pathlib import Path
import datetime
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / "backup-manifest.json").read_text())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def yaml_frontmatter(path):
    result = subprocess.run(
        ["ruby", "-rpsych", "-rjson", "-e",
         "s=File.read(ARGV[0]); m=s.match(/\\A---\\n(.*?)\\n---/m); "
         "abort('missing frontmatter') unless m; "
         "puts JSON.generate(Psych.safe_load(m[1], [], [], false))", str(path)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip())
    return json.loads(result.stdout)


def missing_refs(text, source):
    missing = set()
    # Local Markdown links only. Code samples and runtime-variable paths are
    # reported separately by the prose review, not interpreted as file access.
    for value in re.findall(r"\]\(([^\s)]+)\)", text):
        value = value.strip("<>").split("#", 1)[0]
        if not value or "://" in value or "$" in value:
            continue
        target = Path(value) if value.startswith("/") else source.parent / value
        if not target.exists():
            missing.add(value)
    return sorted(missing)


changes = []
diff_lines = []
failures = []
validation = []
entries = []
for item in manifest["files"]:
    path = Path(item["source"])
    before_path = Path(item["backup"])
    before_raw, after_raw = before_path.read_bytes(), path.read_bytes()
    if digest(before_raw) != item["sha256_before"]:
        failures.append("backup hash mismatch: " + str(path))
    before, after = before_raw.decode("utf-8"), after_raw.decode("utf-8")
    missing_before = missing_refs(before, path)
    missing_after = missing_refs(after, path)
    new_missing = sorted(set(missing_after) - set(missing_before))
    if new_missing:
        failures.append("new missing references: " + str(path))
    row = {"source": str(path), "backup_verified": digest(before_raw) == item["sha256_before"],
           "new_missing_references": new_missing, "existing_missing_references": missing_before}
    if path.name == "SKILL.md":
        old_meta, new_meta = yaml_frontmatter(before_path), yaml_frontmatter(path)
        if new_meta.get("name") != old_meta.get("name"):
            failures.append("Skill identity changed: " + str(path))
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", new_meta.get("name", "")):
            failures.append("invalid Skill name: " + str(path))
        desc = new_meta.get("description")
        if not isinstance(desc, str) or not desc.strip():
            failures.append("invalid description: " + str(path))
        # Preserve host metadata and active safety hooks. The bundled validator
        # does not recognize all existing host extensions; do not drop them to
        # manufacture a validator pass.
        preserved = {k for k in old_meta if k not in {"name", "description", "triggers"}}
        if any(new_meta.get(k) != old_meta[k] for k in preserved):
            failures.append("unplanned metadata change: " + str(path))
        row["frontmatter"] = "valid YAML; identity and unrelated metadata preserved"
        row["bundled_validator_extensions"] = sorted(set(new_meta) - {"name", "description", "license", "allowed-tools", "metadata"})
        entries.append(path)
    validation.append(row)
    changes.append({"source": str(path), "sha256_before": digest(before_raw),
                    "sha256_after": digest(after_raw), "changed": before_raw != after_raw,
                    "bytes_before": len(before_raw), "bytes_after": len(after_raw),
                    "chars_before": len(before), "chars_after": len(after)})
    diff_lines.extend(difflib.unified_diff(before.splitlines(keepends=True), after.splitlines(keepends=True),
                                        fromfile="before" + str(path), tofile="after" + str(path), n=3))

# The retained identical design copies must stay identical, without deleting
# either entry or changing registration/symlinks.
design = [Path(x["source"]).read_bytes() for x in manifest["files"]
          if x["source"].endswith("design-taste-frontend/SKILL.md")]
if len(design) == 2 and design[0] != design[1]:
    failures.append("paired design-taste copies diverged")

result = {"time": datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
          "status": "PASS" if not failures else "FAIL", "failures": failures,
          "changed_files": sum(x["changed"] for x in changes), "files": validation,
          "bundled_validator": "not run: default Python lacks PyYAML; independent Psych YAML validation used; existing host extensions retained",
          "behavior_status": "pending independent paired evaluation; static checks do not prove compliance"}
(ROOT / "validation.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
(ROOT / "change-summary.json").write_text(json.dumps(changes, ensure_ascii=False, indent=2) + "\n")
(ROOT / "changes.diff").write_text("".join(diff_lines))
if failures:
    print(json.dumps({"status": "FAIL", "failures": failures}, ensure_ascii=False))
    raise SystemExit(1)

if "--validate-only" in sys.argv:
    print(json.dumps({"status": result["status"], "changed_files": result["changed_files"],
                      "mode": "validate-only; original frozen experiment inputs unchanged"}, ensure_ascii=False))
    raise SystemExit(0)

frozen = ROOT / "frozen"
if frozen.exists():
    raise SystemExit("Frozen inputs already exist; never overwrite a running evaluation")
source_map = {x["source"]: x for x in manifest["files"]}
mapping = []
for entry in entries:
    tag = "project" if "/Documents/skills/" in str(entry) else ("user" if "/.agents/" in str(entry) else "codex")
    skill_id = tag + "-" + entry.parent.name
    pair = {"id": skill_id, "source": str(entry), "arms": {}}
    for arm in ("before", "after"):
        dest = frozen / arm / skill_id
        for resource in entry.parent.rglob("*.md"):
            rel = resource.relative_to(entry.parent)
            if resource.is_symlink() or any(p in {".git", "node_modules", ".venv", "vendor"} for p in rel.parts):
                continue
            target = dest / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            source = Path(source_map[str(resource)]["backup"]) if arm == "before" and str(resource) in source_map else resource
            shutil.copy2(source, target)
        pair["arms"][arm] = {"entry": str(dest / "SKILL.md"), "sha256": digest((dest / "SKILL.md").read_bytes())}
    mapping.append(pair)
(frozen / "mapping.json").write_text(json.dumps(mapping, ensure_ascii=False, indent=2) + "\n")
frozen_files = [{"path": str(p.relative_to(frozen)), "sha256": digest(p.read_bytes()), "bytes": p.stat().st_size}
                for p in sorted(frozen.rglob("*.md"))]
(frozen / "manifest.json").write_text(json.dumps(frozen_files, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"status": result["status"], "changed_files": result["changed_files"],
                  "skill_entries": len(mapping), "frozen_markdown_files": len(frozen_files),
                  "root": str(ROOT), "new_missing_references": 0}, ensure_ascii=False))
