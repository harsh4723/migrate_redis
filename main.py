import redis
import datetime

print("Loading migration.....")

source_redis = redis.Redis(host='ub-ec.prod.eu-west-2.infra', port=6379, db=1)

destination_redis = redis.Redis(host='reranker-ec.prod.eu-west-2.infra', port=6379, db=1)

keys = source_redis.keys('*convo*')

print("Len of keys",len(keys))

start = datetime.datetime.now()

for key in keys:
    value = source_redis.get(key)
    ttl = source_redis.ttl(key)
    if ttl >=0:
        destination_redis.setex(key, ttl, value)
    else:
        destination_redis.set(key, value)

time_clocked = datetime.datetime.now() - start

total_time = int(time_clocked.total_seconds())

print("Copied Successfully total time taken",total_time)