local source_redis = redis.connect('ub-ec.prod.eu-west-2.infra', '6379')

source_redis:select(1)

local keys = source_redis:keys('*convo*')

print("source convo keys",keys)