# https://research.googleblog.com/2016/08/computational-thinking-for-all-
# students.html?utm_source=feedburner&utm_medium=feed&utm_campaign=
# Feed%3A+blogspot%2FgJZg+%28Official+Google+Research+Blog%29

from funclib import aggregate, compose
from itertools import zip_longest

@aggregate(compose(list, reversed, list))
def zbroji(x, y, *, baza=10):
    assert all(znamenka in range(baza) for pribrojnik in [x, y]
                                       for znamenka in pribrojnik)
    prijenos = 0
    for u, v in zip_longest(reversed(x), reversed(y), fillvalue=0):
        prijenos, zapisana = divmod(u + v + prijenos, baza)
        yield zapisana
    if prijenos:
        yield prijenos

print(zbroji([2, 3], [4, 1, 6], baza=8))
