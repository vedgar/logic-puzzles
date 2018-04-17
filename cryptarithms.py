# http://code.activestate.com/recipes/576615/


import itertools, contextlib, string, collections


def solve(s):
    chars = set(filter(str.isupper, s))
    for perm in itertools.permutations(string.digits[1:], len(chars)):
        table = str.maketrans(dict(zip(chars, perm)))
        equation = s.translate(table)
        with contextlib.suppress(ArithmeticError, SyntaxError):
            if eval(equation): print(*perm, ' | ', equation)


def possible_values(s):
    chars = set(filter(str.isalpha, s))
    for perm in itertools.permutations(string.digits, len(chars)):
        table = str.maketrans(dict(zip(chars, perm)))
        equation = s.translate(table)
        with contextlib.suppress(ArithmeticError, SyntaxError):
            yield eval(equation)
    

solve('A/B/C + D/E/F + G/H/I == 1 and A < D < G and B < C and E < F and H < I')
solve('A/BC + D/EF + G/HI == 1 and A < D < G')
