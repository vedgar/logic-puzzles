import functools

def tostr(n):
    return str(n)

def conc(m, n):
    return tostr(m) + tostr(n)

def lt(m, n):
    return conc(m, n) < conc(n, m)

def test_transitivity():
    for a in range(999):
        print(end='.')
        for b in range(999):
            if lt(a, b):
                for c in range(999):
                    if lt(b, c) and lt(c, a):
                        print(a, b, c)

@functools.cmp_to_key
def key(m, n):
    return lt(n, m) - lt(m, n)

def sortem():
    return sorted(range(1000), key=key)
