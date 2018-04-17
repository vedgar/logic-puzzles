import itertools, collections, operator
def scalar_product(d1, d2): return sum(map(operator.mul, d1, d2))
cube = set(itertools.product([-1,0,1], repeat=3))
dirs = {d for d in cube if scalar_product(d, d) == 1}
orth = {d1: {d2 for d2 in dirs if not scalar_product(d1, d2)} for d1 in dirs}
# snake = [0, 0, 1] + [1, 0, 1] * 8 + [1, 0, 0]
snake = [0,0,1,1,1,0,1,1,0,1,1,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,0]
def fill(free, pos, dir, n, path):  # print(pos, dir, n, bool(snake[n]), path)
    if not free: yield path
    if pos in free:
        for newdir in orth[dir] if snake[n] else {dir}:
            newpos = tuple(map(operator.add, pos, newdir))
            yield from fill(free - {pos}, newpos, newdir, n + 1, path + [pos])
for c in fill(cube, (1,1,1), (-1,0,0), 0, []): print(*c, sep='\n', end='\n'*2)
