def effective_limit(limit=None):
    return 30 if limit is None else limit


def is_late(elapsed, limit=None):
    return elapsed > effective_limit(limit)


def render_status(elapsed, limit=None):
    return 'late' if is_late(elapsed, limit) else 'ok'


def export_status(elapsed, limit=None):
    return {'late': is_late(elapsed, limit)}
