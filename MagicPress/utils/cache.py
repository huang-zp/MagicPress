from flask import request
from functools import wraps
from MagicPress import cache


def cached(timeout=5 * 60, key='view_%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.full_path
            value = cache.get(cache_key)
            if value is None:
                value = f(*args, **kwargs)
                cache.set(cache_key, value, timeout=timeout)
            return value
        return decorated_function
    return decorator


def key_prefix():
    cache_key = 'view_%s' % request.full_path
    return cache_key
