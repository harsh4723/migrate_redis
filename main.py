import redis
import datetime
import concurrent.futures
import pickle
import numpy as np

print("Loading migration.....")

source_redis = redis.Redis(host='ub-ec.prod.eu-west-2.infra', port=6379, db=1)

destination_redis = redis.Redis(host='reranker-ec.prod.eu-west-2.infra', port=6379, db=1)

keys = source_redis.keys('embeddings*')

print("Len of keys",len(keys))

start = datetime.datetime.now()


def copy_key(key):
    value = source_redis.get(key)
    ttl = source_redis.ttl(key)
    query_vector = pickle.loads(value)
    if np.max(query_vector[0]) == np.min(query_vector[0]) == 0.0:
        pass
    else:
        if ttl >=0:
            destination_redis.setex(key, ttl, value)
        else:
            destination_redis.set(key, value)


max_threads = 100

with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    futures = [executor.submit(copy_key, key) for key in keys]
    concurrent.futures.wait(futures)

source_redis.close()
destination_redis.close()

time_clocked = datetime.datetime.now() - start

total_time = int(time_clocked.total_seconds())
print("Copied Successfully total time taken",total_time)