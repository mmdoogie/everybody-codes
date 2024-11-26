import functools

def keycache(fn):
    cache = {}
    @functools.wraps(fn)
    def _cached_fn(*args, **kwargs):
        k = kwargs['key']
        if k not in cache:
            v = fn(*args, **kwargs)
            cache[k] = v
        else:
            v = cache[k]
        return v
    return _cached_fn
