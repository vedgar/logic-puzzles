import time, random

# http://jkkramer.com/sudoku.html

# r is a row,    e.g. 'A'
# c is a column, e.g. '3'
# s is a square, e.g. 'A3'
# d is a digit,  e.g. '9'
# u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
# g is a grid (81 non-blank chars), e.g. starting with '.18...7...
# v is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

cs = ds = '123456789'
rs = 'ABCDEFGHI'
cross = lambda A, B: [a + b for a in A for b in B]
mcross = lambda As, Bs: [cross(A, B) for A in As for B in Bs]
some = lambda seq: next(filter(None, seq), None)
ss = cross(rs, cs)
part3 = lambda x: (x[:3], x[3:6], x[6:])
ul = mcross([rs], cs) + mcross(rs, [cs]) + mcross(part3(rs), part3(cs))
us = {s: [u for u in ul if s in u] for s in ss}
peers = {s: set().union(*us[s]) - {s} for s in ss}
solve = lambda g: search(parse_grid(g))
from_file = lambda filename, sep='\n': open(filename).read().strip().split(sep)

def consistency_test():
    "A set of tests that must pass."
    assert all((len(ss) == 81, len(ul) == 27,
        all(len(us[s]) == 3 for s in ss),
        all(len(peers[s]) == 20 for s in ss),
        us['C2'] == ['A2 B2 C2 D2 E2 F2 G2 H2 I2'.split(),
                        'C1 C2 C3 C4 C5 C6 C7 C8 C9'.split(),
                        'A1 A2 A3 B1 B2 B3 C1 C2 C3'.split()],
        peers['C2'] == {'A2','B2','D2','E2','F2','G2','H2','I2','C1','C3',
                           'C4','C5','C6','C7','C8','C9','A1','A3','B1','B3'}))
    print('All internal tests pass.')

def parse_grid(g):
    """Convert grid to a dict of possible values, {square: digits}, or
    return None if a contradiction is detected."""
    v = dict.fromkeys(ss, ds)
    for s, d in grid_values(g).items():
        if d in ds and not assign(v, s, d):
            return  # Fail if we can't assign d to square s.
    return v

def grid_values(g):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    dg = [d for d in g if d in ds + '0.']
    assert len(ss) == len(dg)
    return dict(zip(ss, dg))

def assign(v, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, or None if a contradiction is detected."""
    if all(eliminate(v, s, d2) for d2 in v[s].replace(d, '')):
        return v

def eliminate(v, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, or None if a contradiction is detected."""
    if d not in v[s]:
        return v  # Already eliminated
    v[s] = v[s].replace(d, '')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if not v[s]:
        return  # Contradiction: removed last value
    elif len(v[s]) == 1:
        d2 = v[s]
        if not all(eliminate(v, s2, d2) for s2 in peers[s]):
            return
    # (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in us[s]:
        dplaces = [s for s in u if d in v[s]]
        if not dplaces:
            return  # Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(v, dplaces[0], d):
                return
    return v

def display(v):
    "Display these values as a 2-D grid."
    if v:
        w = 1 + max(len(v[s]) for s in ss)
        for r in rs:
            print(*(v[r + c].center(w) + '|'*(c in '36') for c in cs), sep='')
            if r in 'CF':
                print('+'.join(3 * [3 * w * '-']))
    print()

def search(v):
    "Using depth-first search and propagation, try all possible values."
    if v is None:
        return ## Failed earlier
    if all(len(v[s]) == 1 for s in ss):
        return v ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    def possibilities(s):
        l = len(v[s])
        return l + 10 * (l == 1)
    s = min(ss, key=possibilities)
    return some(search(assign(v.copy(), s, d)) for d in v[s])

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

def solve_all(grids, name='', showif=0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(g):
        start = time.clock()
        v = solve(g)
        t = time.clock() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(g))
            display(v)
            print(f'({t:.2f} seconds)\n')
        return t, solved(v)
    times, results = zip(*map(time_solve, grids))
    N = len(grids)
    avg = sum(times) / N
    print(f'Solved {sum(results)} of {N} {name} puzzles (avg {avg:.2f}s ({round(1/avg)}Hz)'
          f', max {max(times):.2f}s).')

def solved(v):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(u): return set(v[s] for s in u) == set(ds)
    return v is not None and all(map(unitsolved, ul))

def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    while True:
        v = dict.fromkeys(ss, ds)
        for s in shuffled(ss):
            if not assign(v, s, random.choice(v[s])):
                break
            da = [v[s] for s in ss if len(v[s]) == 1]
            if len(da) >= N and len(set(da)) >= 8:
                return ''.join(v[s] if len(v[s])==1 else '.' for s in ss)

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':
    consistency_test()
    solve_all([grid1, grid2], 'example', None)
    solve_all(from_file("easy50.txt"), "easy", None)
    solve_all(from_file("top95.txt"), "hard", None)
    solve_all(from_file("hardest.txt"), "hardest", None)
    solve_all([random_puzzle() for _ in range(99)], "random", 99)
    solve_all([hard1], 'extreme', None)
