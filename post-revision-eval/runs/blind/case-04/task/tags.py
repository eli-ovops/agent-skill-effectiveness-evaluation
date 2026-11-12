def normalize_tag(value):
    tag = value.strip()
    if not tag:
        raise ValueError("tag required")
    return tag
