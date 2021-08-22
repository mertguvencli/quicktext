import os
from cachetools import TTLCache
from pympler import asizeof
import psutil
cache = TTLCache(maxsize=100000, ttl=2)


print("Process ID",  os.getpid())
print("Simulating Data...")
cache['a'] = '1'*10000000000
cache['b'] = '2'*10000000000
cache['c'] = '3'*10000000000
print("Object Size (Mb)",  asizeof.asizeof(cache) / 1000000.)
print("Free Memory (Mb)", psutil.virtual_memory().free / 1000000.)
