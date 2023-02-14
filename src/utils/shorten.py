import string
import random
from cachetools import TTLCache


def generate(cache: TTLCache):
    size = 4
    chars = string.ascii_lowercase + string.digits
    code = None

    while not code:
        generated_code = ''.join(random.choice(chars) for _ in range(size))

        if generated_code not in cache.keys():
            code = generated_code

    return code
