import contextlib, collections

def p1a(l):
    s = 0
    for x in l: s += x
    return s

def p1b(l):
    s, i = 0, iter(l)
    with contextlib.suppress(StopIteration):
        while True: s += next(i)
    return s

def p1c(l):
    try: first, *rest = l
    except ValueError: return 0
    else: return first + p1c(rest)

p1 = sum

def p2(*lists): return [x for t in zip(*lists) for x in t]

def p3():
    r = list(range(2))
    for _ in range(98): r.append(r[~0] + r[~1])
    return r

def p4(numbers):
    class NumStr(str):
        def __lt__(self, other): return self + other < other + self
    return int(''.join(sorted(map(NumStr, numbers), reverse=True)))

def p5(e='1', n=2):
    if n > 9:
        if eval(e) == 100: print(e)
    else:
        for j in '+', '-', '': p5(e + j + str(n), n + 1)
