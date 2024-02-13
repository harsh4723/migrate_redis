local pattern = ARGV[1]
local keys = redis.call('keys', pattern)
local totalMemory = 0

for _, key in ipairs(keys) do
    totalMemory = totalMemory + redis.call('MEMORY', 'USAGE', key)
end

return totalMemory
