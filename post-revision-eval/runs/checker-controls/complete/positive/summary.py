def summarize(records):
    groups = {}
    total = 0
    for row in records:
        if not isinstance(row, dict) or 'group' not in row or 'units' not in row:
            raise ValueError('invalid record')
        group, units = row['group'], row['units']
        if not isinstance(group, str) or not group.strip() or type(units) is not int or units < 0:
            raise ValueError('invalid record')
        group = group.strip()
        total += units
        groups[group] = groups.get(group, 0) + units
    return {'records': len(records), 'total': total, 'groups': dict(sorted(groups.items()))}

def format_summary(summary):
    lines = [f"Records: {summary['records']}", f"Total units: {summary['total']}"]
    lines.extend(f'{group}: {units}' for group, units in sorted(summary['groups'].items()))
    return '\n'.join(lines)
