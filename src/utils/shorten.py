import string
import random


def generate():
    size = 4
    chars = string.ascii_lowercase  # + string.digits
    return ''.join(random.choice(chars) for _ in range(size)).lower()
