# coding:utf-8
from flask import request
from functools import wraps
from MagicPress import cache

# 为评论量身制作的缓存
def cached(timeout=5 * 60, key='blog_view_%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.full_path
            if request.method == 'POST':
                value = f(*args, **kwargs)
                cache.set(cache_key, value, timeout=timeout)
                return value
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
