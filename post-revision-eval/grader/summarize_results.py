"""Summarize observed native event and token counters without estimating cost."""
import json
from pathlib import Path

base = Path(__file__).resolve().parent.parent
runs = base / 'runs'
rows = json.loads((runs / 'assignment.json').read_text()) + json.loads((runs / 'repeat-assignment.json').read_text())
result = []
for row in rows:
    root = runs / row['case']
    trace = json.loads((root / 'raw-trace.json').read_text())
    usage = [json.loads(x) for x in (root / 'native-usage.jsonl').read_text().splitlines()]
    contexts = [x for x in usage if x.get('kind') == 'turn_context']
    totals = [x for x in usage if x.get('kind') == 'token_count' and x.get('total_token_usage')]
    if not contexts or not totals:
        raise SystemExit('missing native usage or context for ' + row['case'])
    tokens = totals[-1]['total_token_usage']
    tokens['uncached_input_tokens'] = tokens['input_tokens'] - tokens['cached_input_tokens']
    commands = [x for x in trace['items'] if x['type'] == 'commandExecution']
    test_commands = [x for x in commands if 'run-python -m unittest' in x['command']
                     and 'cat >' not in x['command']]
    check = json.loads((root / 'independent-checks.json').read_text())
    result.append({
        'case': row['case'], 'phase': 'main' if int(row['case'][-2:]) <= 6 else 'supplemental',
        'task': row['fixture'], 'target': row['target'], 'arm': row['arm'],
        'duration_ms': trace['durationMs'], 'native_command_events': len(commands),
        'native_file_change_events': sum(x['type'] == 'fileChange' for x in trace['items']),
        'worker_test_exit_codes': [x['exitCode'] for x in test_commands],
        'independent_blackbox_exit': check['blackbox'].get('exit'),
        'independent_candidate_tests_exit': check['candidate_tests'].get('exit'),
        'context_model': contexts[-1].get('model'), 'context_effort': contexts[-1].get('effort'),
        'native_tokens': tokens,
    })
fields = ('input_tokens', 'cached_input_tokens', 'uncached_input_tokens', 'output_tokens',
          'reasoning_output_tokens', 'total_tokens')
aggregate = {k: sum(x['native_tokens'].get(k, 0) for x in result) for k in fields}
output = {'cases': result, 'distinct_worker_sessions': len(result), 'workers_only': aggregate,
          'accounting': 'cached input is part of input; reasoning output is part of output; '
                        'parent and reviewer overlap are unknown and must not be added'}
(base / 'METRICS.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'cases': len(result), 'worker_totals': aggregate,
                  'model_effort': sorted({(x['context_model'], x['context_effort']) for x in result})}))
