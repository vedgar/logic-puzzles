# http://blog.plover.com/2016/07/12/#17-puzzle

import collections, operator, itertools
from expr import op, Fraction
ops4 = frozenset({op.add, op.sub, op.mul, op.truediv})

def subcounters(c):
    c1 = c.copy()
    if c:
        elem, count = c1.popitem()
        for c2 in subcounters(c1):
            for subcount in range(1 + count):
                c2[elem] = subcount
                yield +c2
    else:
        yield c1

def partitions(c):
    for part in subcounters(c):
        yield part, c - part

def obtainable(*nums, ops=ops4, factory=Fraction):
    def _obtainable(numc, main_ops):
        if sum(numc.values()) == 1:
            num, = numc.elements()
            yield factory(num)
        elif nums:
            for left, right in partitions(numc):
                if left and right:
                    for nleft in _obtainable(left, ops):
                        for op1 in main_ops:
                            ops2 = {o for o in ops if o.prec != op1.prec}
                            for nright in _obtainable(right, ops2):
                                if nright.value() or op1 is not op.truediv:
                                    yield op1.func(nleft, nright)
    yield from _obtainable(collections.Counter(nums), ops)


def obtain(nums, target):
    for expr in obtainable(nums):
        if expr.value() == target:
            print(expr)

#print(*{f"{expr} = {expr.value()}" for expr in obtainable(6, 6, 5, 2)
#        if expr.value() in {17, 24}}, sep='\n')

import fractions


class FMSet(tuple):
    def __new__(cls, arg):
        if isinstance(arg, int):
            return super().__new__(Number, [arg])
        elif arg:
            return super().__new__(cls, sorted(arg))

    def key(self):
        return self.order, tuple(self)

    def __lt__(self, other):
        return self.key() < other.key()

    def str(self, first=False):
        return self.between.join

    def __repr__(self):
        return f"{type(self).__name__}{super().__repr__()}"

class Number(FMSet):
    order = 1
    between = ''

    def __new__(cls, num):
        assert isinstance(num, int)
        return super().__new__(cls, [num])

    def value(self):
        return fractions.Fraction(self[0])
    
class Sum(FMSet):
    order = 2
    between = '+'

    def value(self):
        return sum(item.value() for item in self)

    def barestr(self):
        return ''.join(map(fullstr, self)).join('()')

    def fullstr(self):
        return '*' + self.barestr()

    def __str__(self):
        return '*' + ''.join(map(str, self)).join('()')

class InvertedSum(Sum):
    order = 3

    def value(self):
        return fractions.Fraction(1, super().value())

class Product(FMSet):
    order = 4

    def value(self):
        p = 1
        for item in self:
            p *= item.value()
        return p

class NegatedProduct(Product):
    order = 5

    def value(self):
        return -super().value()

