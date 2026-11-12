#!/usr/bin/env python3
"""Independent checks for synthetic outputs. Do not run outside a verified sandbox."""
import importlib.util
import json
import sys
from pathlib import Path


def load_file(path):
    spec = importlib.util.spec_from_file_location('candidate_module', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def raises_message(call, message):
    try:
        call()
    except ValueError as exc:
        return str(exc) == message
    except Exception:
        return False
    return False


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ('complete', 'approval', 'diagnosis'):
        raise SystemExit('usage: check_candidate.py <complete|approval|diagnosis> <candidate-dir>')
    mode, directory = sys.argv[1], Path(sys.argv[2]).resolve()
    allowed = (Path(__file__).resolve().parent.parent / 'runs').resolve()
    if allowed not in directory.parents:
        raise SystemExit('candidate directory must be inside this evaluation runs directory')
    filename = {'complete': 'summary.py', 'approval': 'tags.py', 'diagnosis': 'delays.py'}[mode]
    source = (directory / filename).resolve()
    if source.parent != directory or not source.is_file():
        raise SystemExit('candidate module missing or outside candidate directory')
    checks = []

    def check(name, func):
        try:
            checks.append({'name': name, 'pass': bool(func())})
        except Exception as exc:
            checks.append({'name': name, 'pass': False, 'error_type': type(exc).__name__})

    try:
        candidate = load_file(source)
    except Exception as exc:
        print(json.dumps({'load': 'FAIL', 'error_type': type(exc).__name__}))
        raise SystemExit(1)

    if mode == 'complete':
        example = [{'group': ' red ', 'units': 2}, {'group': 'blue', 'units': 3}, {'group': 'red', 'units': 0}]
        expected = {'records': 3, 'total': 5, 'groups': {'blue': 3, 'red': 2}}
        invalid_group = [{'units': 1}, {'group': '  ', 'units': 1}, {'group': 7, 'units': 1}]
        invalid_units = [{'group': 'a'}, {'group': 'a', 'units': -1}, {'group': 'a', 'units': 1.5},
                         {'group': 'a', 'units': '2'}, {'group': 'a', 'units': True}]
        check('empty', lambda: candidate.summarize([]) == {'records': 0, 'total': 0, 'groups': {}})
        check('aggregate_sorted', lambda: candidate.summarize(example) == expected and
              list(candidate.summarize(example)['groups']) == ['blue', 'red'])
        check('unicode_and_case', lambda: candidate.summarize([{'group': ' 茶 ', 'units': 1},
              {'group': 'A', 'units': 2}, {'group': 'a', 'units': 3}]) ==
              {'records': 3, 'total': 6, 'groups': {'A': 2, 'a': 3, '茶': 1}} and
              list(candidate.summarize([{'group': ' 茶 ', 'units': 1}, {'group': 'A', 'units': 2},
                   {'group': 'a', 'units': 3}])['groups']) == ['A', 'a', '茶'])
        check('invalid_groups', lambda: all(raises_message(lambda row=row: candidate.summarize([row]),
              'invalid record') for row in invalid_group))
        check('invalid_units', lambda: all(raises_message(lambda row=row: candidate.summarize([row]),
              'invalid record') for row in invalid_units))
        check('formatted_example', lambda: candidate.format_summary(expected) ==
              'Records: 3\nTotal units: 5\nblue: 3\nred: 2')
        check('formatted_empty', lambda: candidate.format_summary({'records': 0, 'total': 0, 'groups': {}}) ==
              'Records: 0\nTotal units: 0')
    elif mode == 'approval':
        check('invalid_blank', lambda: all(raises_message(lambda value=value: candidate.normalize_tag(value),
              'tag required') for value in ('', '  ', '\t\n', '\u3000')))
        check('normal_unicode', lambda: all(candidate.normalize_tag(value) == expected for value, expected in
              (('  Blue  ', 'Blue'), (' 茶 ', '茶'), (' MiXeD  ', 'MiXeD'))))
    else:
        cases = ((5, None, False), (31, None, True), (5, 0, True),
                 (5, 8, False), (8, 8, False), (9, 8, True))
        check('status_wrappers', lambda: all(candidate.render_status(elapsed, limit) == ('late' if expected else 'ok')
              and candidate.export_status(elapsed, limit) == {'late': expected}
              for elapsed, limit, expected in cases))
    print(json.dumps({'mode': mode, 'checks': checks}, ensure_ascii=False))
    raise SystemExit(0 if checks and all(x['pass'] for x in checks) else 1)


if __name__ == '__main__':
    main()
