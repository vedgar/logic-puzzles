import itertools, math
MAX = 10 ** 6
sieve = set(range(3, MAX, 2))
primes = {2}
while True:
    p = min(sieve)
    sieve.remove(p)
    primes.add(p)
    if p ** 2 not in sieve: break
    sieve.difference_update(range(p ** 2, MAX, p * 2))
primes |= sieve
for ten in range(10, MAX - 10, 30):
    if {ten+1, ten+3, ten+7, ten+9} < primes: print(ten // 10)
