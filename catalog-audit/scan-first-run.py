#!/usr/bin/env python3
"""Read only discoverable SKILL.md and invocation-policy metadata; never execute them."""
import hashlib
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOTS = tuple(Path(p) for p in (
    '/Users/USER/.codex/skills', '/Users/USER/.agents/skills',
    '/Users/USER/Documents/skills/.agents/skills',
    '/Users/USER/.codex/plugins/cache/openai-bundled',
    '/Users/USER/.codex/plugins/cache/openai-curated-remote',
    '/Users/USER/.codex/plugins/cache/openai-primary-runtime',
))
EXCLUDED = {'.git', 'node_modules', '.venv', 'venv', '__pycache__'}
PATTERNS = {
    'persistent': re.compile(r'(?i)active every|always active|always on|every response|all (?:future )?(?:tasks|turns|responses)|across (?:tasks|sessions)|persist(?:s|ence|ent)|永久生效|持续激活|每次(?:回复|回答|任务)|全局生效'),
    'approval': re.compile(r'(?i)(?:ask|request|obtain|require|wait for|seek|need).{0,55}(?:approv|permission|confirmation|user input)|(?:approv|permission|confirmation).{0,45}(?:required|before|must)|(?:必须|需要|等待|征求).{0,20}(?:审批|授权|许可|用户确认|用户同意)'),
    'planning_gate': re.compile(r'(?i)(?:before|until|cannot|do not|never|must|gate|block).{0,65}(?:plan|design|brainstorm|spec|test|user|approval)|(?:先|必须|禁止).{0,30}(?:计划|设计|规划|验收|测试|确认|询问)'),
    'forced_tool_model': re.compile(r'(?i)(?:must|always|only|required|mandatory|never).{0,70}(?:tool|model|skill|agent|install|dependenc|cli|plugin)|(?:tool|model|skill|agent|install|dependenc|cli|plugin).{0,45}(?:mandatory|required|must)|(?:必须|强制|只能|唯一).{0,25}(?:工具|模型|技能|插件|安装|依赖|代理)'),
    'output_limit': re.compile(r'(?i)(?:always|never|only|at most|no more than|maximum|must|exactly|first).{0,60}(?:response|answer|reply|paragraph|sentence|line|word|output)|(?:必须|只能|不超过|禁止).{0,25}(?:回复|回答|输出|字|句|行|段落)'),
    'skill_load': re.compile(r'(?i)(?:read|load|invoke|use|call|consult|trigger|dispatch).{0,70}(?:skill|SKILL\.md)|(?:skill|SKILL\.md).{0,55}(?:must|required|always|before)|(?:读取|调用|使用|加载).{0,30}(?:技能|Skill|SKILL\.md)'),
    'scope_simplify': re.compile(r'(?i)(?:laziest|simplest|shortest|yagni|minimum viable|skip the|ship the lazy|do less)|(?:最少|最短|最简|缩减|不必|省略).{0,25}(?:实现|功能|测试|验证|需求|步骤)'),
    'broad_trigger': re.compile(r'(?i)(?:use (?:this )?(?:skill )?(?:for|on|when)|always use|must use|whenever|any (?:coding|task|request)|every (?:task|time|response)|whenever in doubt)|(?:任何任务|所有任务|一律|每次都|必须使用)'),
}
SUSPECT_SECRET = re.compile(r'(?i)(?:sk-[A-Za-z0-9_-]{16,}|gh[pousr]_[A-Za-z0-9_]{16,}|xox[baprs]-[A-Za-z0-9-]{12,}|AKIA[A-Z0-9]{16}|(?:api[_ -]?key|access[_ -]?token|secret|password)\s*[:=]\s*[\x22\x27]?[A-Za-z0-9._~+/-]{12,}|[A-Za-z0-9_+/=-]{64,})')


def snippet(line):
    line = line.strip()
    return None if SUSPECT_SECRET.search(line) else line[:260]


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return '', 0, False
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == '---')
    except StopIteration:
        return '', 0, False
    head = lines[1:end]
    name = ''
    description = []
    collecting = False
    for line in head:
        m = re.match(r'^name:\s*(.*)$', line)
        if m:
            name = m.group(1).strip().strip('\"\'')
        m = re.match(r'^description:\s*(.*)$', line)
        if m:
            collecting = True
            value = m.group(1).strip()
            if value not in ('>', '|', '>-', '|-', '>+', '|+'):
                description.append(value)
            continue
        if collecting:
            if line and not line[0].isspace():
                collecting = False
            elif line.strip():
                description.append(line.strip())
    return name, len(' '.join(description)), True


def policy(path):
    p = path.parent / 'agents' / 'openai.yaml'
    try:
        if not p.is_file():
            return 'MISSING'
        text = p.read_text(encoding='utf-8')
    except (OSError, UnicodeError):
        return 'UNREADABLE'
    matches = re.findall(r'(?im)^\s*allow_implicit_invocation:\s*(true|false)\s*(?:#.*)?$', text)
    return matches[-1].lower() if matches else 'UNSPECIFIED'


def main():
    injected = [json.loads(x) for x in (BASE / 'injected-catalog.jsonl').read_text(encoding='utf-8').splitlines()]
    by_logical = defaultdict(list)
    by_real = defaultdict(list)
    for item in injected:
        by_logical[item['logical_path']].append(item['name'])
        by_real[os.path.realpath(item['logical_path'])].append(item['name'])
    paths = {}
    errors = []
    skips = []
    symlinks = []

    def walk(path, root, ancestors):
        try:
            real = os.path.realpath(path)
            if real in ancestors:
                skips.append({'path': str(path), 'reason': 'symlink_cycle'})
                return
            with os.scandir(path) as it:
                entries = list(it)
            for item in entries:
                p = Path(item.path)
                if item.name in EXCLUDED:
                    if item.is_dir(follow_symlinks=False):
                        skips.append({'path': str(p), 'reason': 'non_skill_dependency_or_vcs'})
                    continue
                if item.name == 'SKILL.md' and item.is_file(follow_symlinks=True):
                    paths[str(p)] = str(root)
                elif item.is_dir(follow_symlinks=False):
                    walk(p, root, ancestors | {real})
                elif item.is_symlink() and item.is_dir(follow_symlinks=True):
                    target = os.path.realpath(p)
                    under_root = any(target == str(x) or target.startswith(str(x) + os.sep) for x in ROOTS)
                    direct_skill = (p / 'SKILL.md').is_file()
                    catalog_ancestor = any(k.startswith(str(p) + os.sep) for k in by_logical)
                    followed = under_root or direct_skill or catalog_ancestor
                    symlinks.append({'logical': str(p), 'real': target, 'followed': followed})
                    if followed:
                        walk(p, root, ancestors | {real})
                    else:
                        skips.append({'path': str(p), 'reason': 'external_symlink_not_known_skill'})
        except (OSError, RuntimeError) as exc:
            errors.append({'path': str(path), 'error_type': type(exc).__name__})

    for root in ROOTS:
        if root.is_dir():
            walk(root, root, set())
        else:
            errors.append({'path': str(root), 'error_type': 'root_missing'})
    for item in injected:
        p = Path(item['logical_path'])
        if p.is_file():
            paths.setdefault(str(p), 'injected_catalog')
        else:
            errors.append({'path': str(p), 'error_type': 'injected_path_missing'})

    cache = {}
    inventory = []
    hits = []
    for logical, root in sorted(paths.items()):
        p = Path(logical)
        real = os.path.realpath(p)
        if real not in cache:
            try:
                raw = Path(real).read_bytes()
                text = raw.decode('utf-8')
                name, desc_chars, has_frontmatter = frontmatter(text)
                if SUSPECT_SECRET.search(name):
                    name = '[OMITTED_POSSIBLE_SECRET]'
                sha = hashlib.sha256(raw).hexdigest()
                categories = Counter()
                for n, line in enumerate(text.splitlines(), 1):
                    found = [key for key, rx in PATTERNS.items() if rx.search(line)]
                    if found:
                        categories.update(found)
                        hits.append({'real_path': real, 'sha256': sha, 'line': n,
                                     'categories': found, 'snippet': snippet(line),
                                     'snippet_omitted': snippet(line) is None})
                cache[real] = {'sha256': sha, 'bytes': len(raw), 'chars': len(text),
                               'declared_name': name, 'description_chars': desc_chars,
                               'frontmatter_present': has_frontmatter, 'hit_counts': dict(categories)}
            except (OSError, UnicodeError) as exc:
                errors.append({'path': logical, 'error_type': type(exc).__name__})
                continue
        tags = []
        lower = logical.lower()
        if '/plugins/cache/' in lower:
            tags.append('plugin_cache')
        if any('/' + x + '/' in lower for x in ('reference', 'references', 'upstream', 'archive', 'archived')):
            tags.append('reference_upstream_or_archive')
        if '/.system/' in lower:
            tags.append('system')
        item = {'logical_path': logical, 'real_path': real, 'root': root,
                'is_file_symlink': p.is_symlink(),
                'through_symlink': logical != real,
                'location_tags': tags,
                'session_catalog_exact': by_logical.get(logical, []),
                'session_catalog_same_real': sorted(set(by_real.get(real, []))),
                'implicit_policy_text': policy(p),
                **cache[real]}
        inventory.append(item)

    for filename, values in (('inventory.jsonl', inventory), ('hits.jsonl', hits),
                             ('symlinks.jsonl', symlinks), ('scan-skips.jsonl', skips),
                             ('scan-errors.jsonl', errors)):
        with (BASE / filename).open('x', encoding='utf-8') as f:
            for value in values:
                f.write(json.dumps(value, ensure_ascii=False) + '\n')
    names = defaultdict(set)
    hashes = defaultdict(set)
    for item in inventory:
        if item['declared_name']:
            names[item['declared_name']].add(item['sha256'])
        hashes[item['sha256']].add(item['real_path'])
    with (BASE / 'name-collisions.jsonl').open('x', encoding='utf-8') as f:
        for name, values in sorted(names.items()):
            if len(values) > 1:
                members = [{'logical_path': x['logical_path'], 'real_path': x['real_path'],
                            'sha256': x['sha256'], 'session_catalog_exact': x['session_catalog_exact']}
                           for x in inventory if x['declared_name'] == name]
                f.write(json.dumps({'name': name, 'members': members}, ensure_ascii=False) + '\n')
    with (BASE / 'duplicate-contents.jsonl').open('x', encoding='utf-8') as f:
        for sha, values in sorted(hashes.items()):
            if len(values) > 1:
                members = [{'logical_path': x['logical_path'], 'real_path': x['real_path'],
                            'declared_name': x['declared_name'], 'session_catalog_exact': x['session_catalog_exact']}
                           for x in inventory if x['sha256'] == sha]
                f.write(json.dumps({'sha256': sha, 'members': members}, ensure_ascii=False) + '\n')
    overview = {'roots': [str(x) for x in ROOTS], 'logical_paths': len(inventory),
                'real_files': len(cache), 'distinct_sha256': len(hashes),
                'session_injected_entries': len(injected),
                'session_exact_paths_found': sum(bool(x['session_catalog_exact']) for x in inventory),
                'session_catalog_names_distinct': len({x['name'] for x in injected}),
                'aliases_same_real': sum(bool(x['session_catalog_same_real']) and not x['session_catalog_exact'] for x in inventory),
                'other_logical_paths': sum(not x['session_catalog_exact'] and not x['session_catalog_same_real'] for x in inventory),
                'symlink_dirs': len(symlinks), 'skips': len(skips), 'errors': len(errors),
                'names_with_multiple_content_hashes': sum(len(v) > 1 for v in names.values()),
                'same_content_multiple_real_paths': sum(len(v) > 1 for v in hashes.values()),
                'hit_lines': len(hits), 'hit_category_counts': dict(sum((Counter(x['categories']) for x in hits), Counter()))}
    with (BASE / 'summary.json').open('x', encoding='utf-8') as f:
        json.dump(overview, f, ensure_ascii=False, indent=2)
    print(json.dumps(overview, ensure_ascii=False))


if __name__ == '__main__':
    if '--self-test' in sys.argv:
        assert frontmatter('---\nname: demo\ndescription: >\n  one\n  two\n---\nbody')[0:2] == ('demo', 7)
        assert PATTERNS['persistent'].search('ACTIVE EVERY RESPONSE')
        assert PATTERNS['approval'].search('ask for approval before proceeding')
        assert snippet('api_key = "sk-examplexxxxxxxxxxxxxxxx"') is None
        assert snippet('Read the current user request') == 'Read the current user request'
        print('scanner fixture: PASS')
    else:
        main()
