from collections.abc import Mapping


def summarize(records):
    groups = {}
    total = 0
    for record in records:
        if not isinstance(record, Mapping):
            raise ValueError('invalid record')
        group = record.get('group')
        units = record.get('units')
        if (not isinstance(group, str) or not group.strip()
                or not isinstance(units, int) or isinstance(units, bool)
                or units < 0):
            raise ValueError('invalid record')
        group = group.strip()
        groups[group] = groups.get(group, 0) + units
        total += units
    return {'records': len(records), 'total': total, 'groups': dict(sorted(groups.items()))}


def format_summary(summary):
    lines = [f"Records: {summary['records']}", f"Total units: {summary['total']}"]
    lines.extend(f"{group}: {units}" for group, units in sorted(summary['groups'].items()))
    return '\n'.join(lines)
