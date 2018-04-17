import itertools, operator
coords = set(itertools.product(range(3), repeat=2))
crits = *map(operator.itemgetter, range(2)), sum, lambda p: p[1] - p[0]
line3 = lambda a, b, c: any(crit(a) == crit(b) == crit(c) for crit in crits)
for candidate in itertools.combinations(coords, 6):
    if not any(itertools.starmap(line3, itertools.combinations(candidate, 3))):
        for i in range(3):
            for j in range(3):
                print(end='#' if (i, j) in candidate else '.')
            print()
        print('-' * 5)
