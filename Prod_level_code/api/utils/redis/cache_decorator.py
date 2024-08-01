# cache_decorator.py

import functools
from redis_client import RedisClient

redis_client = RedisClient()

def cache(seconds=300):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}"
            cached_data = redis_client.get(key)
            if cached_data:
                return cached_data.decode('utf-8')
            else:
                result = func(*args, **kwargs)
                redis_client.set(key, result, expire_time=seconds)
                return result
        return wrapper
    return decorator
