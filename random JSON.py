# http://www.catonmat.net/blog/generate-random-json-data-structures/

from random import choice, randrange, random, choices

def random_JSON(max_depth):
    types = [number, string, boolean] + [array, object]*bool(max_depth)
    return choice(types)(max_depth)

def number(_, max_num=1<<32):
    num = random() * max_num if randrange(2) else randrange(max_num)
    return num if randrange(2) else -num

def string(_, max_len=100):
    import string
    return ''.join(choices(string.printable[:-5], k=randrange(max_len)))

def boolean(_): return choice([True, False])

def array(max_depth, max_len=10):
    return [random_JSON(max_depth-1) for _ in range(randrange(max_len))]

def object(max_depth, max_len=10, max_key_len=10):
    return {string(max_depth, max_key_len): random_JSON(max_depth-1)
                for _ in range(randrange(max_len))}
