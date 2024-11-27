import functools

class Keycache:
    def __init__(self, stats=False):
        self._stats = stats
    
    class _KeycacheWithStats:
        def __init__(self, fn):
            self._cache = {}
            self._hits = 0
            self._misses = 0
            @functools.wraps(fn)
            def _cached_fn(*args, **kwargs):
                k = kwargs['key']
                if k not in self._cache:
                    self._misses += 1
                    v = fn(*args, **kwargs)
                    self._cache[k] = v
                else:
                    self._hits += 1
                    v = self._cache[k]
                return v
            self._cached_fn = _cached_fn

        def __call__(self, *args, **kwargs):
            return self._cached_fn(*args, **kwargs)

        def stats(self):
            return self._hits, self._misses

        def reset(self, stats_only=False):
            if not stats_only:
                self._cache = {}
            self._hits = 0
            self._misses = 0

    def __call__(self, fn):
        if not self._stats:
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
        return self._KeycacheWithStats(fn)
