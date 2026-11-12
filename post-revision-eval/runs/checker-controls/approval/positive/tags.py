def normalize_tag(value):
    value = value.strip()
    if not value:
        raise ValueError('tag required')
    return value
