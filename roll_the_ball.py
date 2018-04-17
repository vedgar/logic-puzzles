import collections

start = '''\
x.R  /    /    +oLU
+oDR +oUD +.LR /
+.LD +.UR +.UD /
x.U  +oLR +.LU +oUD
'''.splitlines()
N = len(start)

rotate = str.maketrans('URDL', 'RDLU')

class Tile(collections.namedtuple('_', 'i j m r e')):
    def move(self, di, dj):
        return self._replace(i=self.i+di, j=self.j+dj)

    def rotate(self):
        return self._replace(e=frozenset(x.translate(rotate) for x in self.e))

    def neighbors(self):
        if self.m:
            for d in 1, 1j, -1, -1j:
                yield self.move(int(d.real), int(d.imag))
        if self.r:
            yield self.rotate()

    def __eq__(self, other):
        return (self.i, self.j) == (other.i, other.j)

    def __hash__(self):
        return hash((self.i, self.j))


class Board(frozenset):
    def neighbors(self):
        for tile in self:
            without = self - {tile}
            for neigh in tile.neighbors():
                if neigh not in without and {neigh.i, neigh.j} <= set(range(N)):
                    yield Board(without | {neigh})

    def pprint(self):
        slots = [['' for _ in range(N)] for _ in range(N)]
        for tile in self:
            slots[tile.i][tile.j] = ''.join(tile.e)
        for line in slots:
            for slot in line:
                print(end=slot.ljust(3))
            print()

    def heuristic(self, goal):
        ...

tiles = set()
for i, line in enumerate(start):
    for j, str_tile in enumerate(line.split()):
        if str_tile != '/':
            m, r, *e = str_tile
            tiles.add(Tile(i, j, m=='+', r=='o', frozenset(e)))
board = Board(tiles)
