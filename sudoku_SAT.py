import itertools

forma = set()
r = range(9)
r2 = list(itertools.combinations(r, 2))
rr = list(itertools.product(r, repeat=2))
rr2 = list(itertools.combinations(rr, 2))
# varijable = itertools.product(r, repeat=3)

def var(redak, stupac, broj):
    return redak * 81 + stupac * 9 + broj + 1

for redak in r:
    for stupac in r:
        for broj1, broj2 in r2:
            forma.add((-var(redak, stupac, broj1),
                       -var(redak, stupac, broj2)))
        forma.add(tuple(var(redak, stupac, broj) for broj in r))

for redak in r:
    for stupac1, stupac2 in r2:
        for broj in r:
            forma.add((-var(redak, stupac1, broj),
                       -var(redak, stupac2, broj)))

for redak1, redak2 in r2:
    for stupac in r:
        for broj in r:
            forma.add((-var(redak1, stupac, broj),
                       -var(redak2, stupac, broj)))

for (redak1, stupac1), (redak2, stupac2) in rr2:
    if (redak1 // 3, stupac1 // 3) == (redak2 // 3, stupac2 // 3):
        for broj in r:
            forma.add((-var(redak1, stupac1, broj),
                       -var(redak2, stupac2, broj)))

grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'

for (redak, stupac), znamenka in zip(rr, grid2):
    if znamenka != '.':
        forma.add((var(redak, stupac, int(znamenka)),))

with open('SAT.txt', 'w') as izlaz:
    for klauzula in forma:
        print(*klauzula, file=izlaz)
