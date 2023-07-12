import redis
import numpy as np
import pickle
import concurrent.futures

source_redis = redis.Redis(host='ub-ec.prod.eu-west-2.infra', port=6379, db=1)

keys = source_redis.keys('embeddings*')


def process_key(key):
    value = source_redis.get(key)
    query_vector = pickle.loads(value)
    if np.max(query_vector[0]) == np.min(query_vector[0]) == 0.0:
        return 1
    else:
        return 0

c = 0

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    results = executor.map(process_key, keys)
    c = sum(results)

print(c)
