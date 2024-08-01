# redis_client.py

import redis

class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, key):
        return self.redis.get(key)

    def set(self, key, value, expire_time=None):
        self.redis.set(key, value, ex=expire_time)

    def delete(self, key):
        self.redis.delete(key)
