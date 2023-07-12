import redis
import numpy as np
import pickle

source_redis = redis.Redis(host='ub-ec.prod.eu-west-2.infra', port=6379, db=1)

keys = source_redis.keys('embeddings*')

c = 0
for key in keys:
    value = source_redis.get(key)
    query_vector = pickle.loads(value)
    if c%1000 == 0:
        print(c)
    if np.max(query_vector[0]) == np.min(query_vector[0]) == 0.0:
        c = c+1

print(c)
