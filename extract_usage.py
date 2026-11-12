#!/usr/bin/env python3
"""Extract only session-level token metadata; do not export rate limits or content."""
import json
import mmap
import sys
from pathlib import Path

FIELDS = ('input_tokens', 'cached_input_tokens', 'output_tokens', 'reasoning_output_tokens', 'total_tokens')


def extract(row, source, line):
    payload = row.get('payload') or {}
    if row.get('type') == 'turn_context':
        mode = payload.get('collaboration_mode') or {}
        return {'source': str(source), 'line': line, 'ordinal': row.get('ordinal'), 'kind': 'turn_context',
                'timestamp': row.get('timestamp'), 'model': payload.get('model'),
                'effort': payload.get('effort'), 'mode': mode.get('mode')}
    if row.get('type') != 'event_msg' or payload.get('type') != 'token_count':
        return None
    info = payload.get('info') or {}
    result = {'source': str(source), 'line': line, 'ordinal': row.get('ordinal'), 'kind': 'token_count',
              'timestamp': row.get('timestamp'), 'call_id': payload.get('call_id'),
              'last_usage_includes_reasoning': info.get('last_usage_includes_reasoning')}
    for key in ('total_token_usage', 'last_token_usage'):
        item = info.get(key) or {}
        result[key] = {name: item[name] for name in FIELDS if type(item.get(name)) is int}
    return result


def parse_line(line):
    if '"type":"token_count"' in line:
        # Native token events place unrelated rate limits after the usage info.
        # Cut that field out before JSON parsing; never export it.
        if ',"rate_limits":' in line:
            if '"info":' not in line or line.index(',"rate_limits":') < line.index('"info":'):
                return None  # unsupported ordering; do not emit partial usage
            line = line.split(',"rate_limits":', 1)[0] + '}}'
    elif '"type":"turn_context"' not in line:
        return None
    try:
        row = json.loads(line)
        if row.get('type') == 'event_msg' and row.get('payload', {}).get('type') == 'token_count':
            if not isinstance(row['payload'].get('info'), dict):
                return None
        return row
    except json.JSONDecodeError:
        return None  # a live session may end with an incomplete line


def safe_line(buffer, start, end):
    """Copy token metadata only up to the account-limit field, never its value."""
    header_end = min(end, start + 160)
    if buffer.find(b'"type":"token_count"', start, header_end) >= 0:
        info = buffer.find(b'"info":', start, end)
        stop = buffer.find(b',"rate_limits":', start, end)
        if info < 0 or stop < info:
            return None, True  # unrecognised schema: leave usage UNKNOWN
        return (buffer[start:stop] + b'}}').decode('utf-8'), True
    if buffer.find(b'"type":"turn_context"', start, header_end) >= 0:
        return buffer[start:end].decode('utf-8'), False
    return None, False


if __name__ == '__main__':
    sessions = (Path.home() / '.codex' / 'sessions').resolve()
    for arg in sys.argv[1:]:
        path = Path(arg).resolve()
        if sessions not in path.parents or not path.name.startswith('rollout-') or path.suffix != '.jsonl':
            raise SystemExit(f'Refusing non-session path: {path}')
        with path.open('rb') as handle:
            if not path.stat().st_size:
                continue
            with mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as data:
                start = line_no = 0
                while start < len(data):
                    end = data.find(b'\n', start)
                    end = len(data) if end < 0 else end
                    line_no += 1
                    try:
                        line, candidate = safe_line(data, start, end)
                    except UnicodeDecodeError:  # live record may be incomplete
                        line, candidate = None, True
                    start = end + 1
                    if line is None:
                        if candidate:
                            print(json.dumps({'source': str(path), 'line': line_no,
                                              'kind': 'unparsed_token_candidate'}, ensure_ascii=False))
                        continue
                    row = parse_line(line)
                    if row is None:
                        if candidate:
                            print(json.dumps({'source': str(path), 'line': line_no,
                                              'kind': 'unparsed_token_candidate'}, ensure_ascii=False))
                        continue
                    value = extract(row, path, line_no)
                    if value is not None:
                        print(json.dumps(value, ensure_ascii=False))
