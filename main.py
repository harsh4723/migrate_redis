import redis
from datetime import timedelta

print("Loading migration.....")

source_redis = redis.Redis(host='ub-ec.prod.eu-west-2.infra', port=6379, db=1)

destination_redis = redis.Redis(host='reranker-ec.prod.eu-west-2.infra', port=6379, db=1)

keys = source_redis.keys('*convo*')

print("Len of keys",len(keys))

for key in keys:
    value = source_redis.get(key)
    ttl = source_redis.ttl(key)
    ttl_timedelta = timedelta(seconds=ttl)
    destination_redis.setex(key, ttl, value)

print("Copied Successfully")