import importlib.util
import json
from pathlib import Path

path = Path(__file__).parents[1] / 'extract_usage.py'
spec = importlib.util.spec_from_file_location('usage_extractor', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

row = {'type': 'event_msg', 'timestamp': 'synthetic', 'payload': {
    'type': 'token_count',
    'info': {'last_usage_includes_reasoning': True,
             'total_token_usage': {'input_tokens': 100, 'cached_input_tokens': 70,
                                   'output_tokens': 20, 'reasoning_output_tokens': 5,
                                   'total_tokens': 120},
             'last_token_usage': {'input_tokens': 10, 'cached_input_tokens': 7,
                                  'output_tokens': 2, 'reasoning_output_tokens': 1,
                                  'total_tokens': 12}},
    'rate_limits': {'ignored': 'DO_NOT_EXPORT_SYNTHETIC'}}}
out = module.extract(row, 'synthetic', 1)
assert out['total_token_usage']['total_tokens'] == 120
assert out['total_token_usage']['cached_input_tokens'] == 70
assert out['last_token_usage']['reasoning_output_tokens'] == 1
assert out['last_usage_includes_reasoning'] is True
assert out['call_id'] is None
assert 'DO_NOT_EXPORT_SYNTHETIC' not in str(out) and 'rate_limits' not in out
assert module.extract({'type': 'response_item', 'payload': {'text': 'synthetic'}}, 'synthetic', 2) is None
wire = json.dumps(row, separators=(',', ':'))
parsed = module.parse_line(wire)
assert 'rate_limits' not in parsed['payload']
assert module.extract(parsed, 'synthetic', 1)['total_token_usage']['total_tokens'] == 120
reordered = {'type': 'event_msg', 'payload': {'type': 'token_count',
             'rate_limits': {'ignored': 'DO_NOT_EXPORT_SYNTHETIC'}, 'info': row['payload']['info']}}
assert module.parse_line(json.dumps(reordered, separators=(',', ':'))) is None
assert module.parse_line('{"type":"event_msg","payload":{"type":"token_count"') is None

class GuardedBuffer:
    def __init__(self, data):
        self.data = data
        self.stop = data.index(b',"rate_limits":')

    def find(self, *args):
        return self.data.find(*args)

    def __getitem__(self, key):
        assert isinstance(key, slice) and key.stop <= self.stop
        return self.data[key]


raw = wire.encode()
safe, candidate = module.safe_line(GuardedBuffer(raw), 0, len(raw))
assert candidate and 'DO_NOT_EXPORT_SYNTHETIC' not in safe
assert module.extract(module.parse_line(safe), 'synthetic', 1)['total_token_usage']['total_tokens'] == 120
assert module.safe_line(b'{"type":"token_count","info":{}}', 0, 32) == (None, True)
print('usage extractor fixture: PASS')
