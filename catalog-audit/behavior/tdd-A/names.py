def normalize_name(name):
    name = name.strip()
    if not name:
        raise ValueError('name required')
    return name
