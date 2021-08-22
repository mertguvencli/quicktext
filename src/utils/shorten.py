import string
import random
from cachetools import TTLCache


def generate(cache: TTLCache):
    size = 4
    # chars = string.ascii_lowercase + string.digits
    chars = string.digits

    code = ""
    while True:
        code = ''.join(random.choice(chars) for _ in range(size)).lower()
        if code in cache.keys():
            continue
        else:
            break
    return code
