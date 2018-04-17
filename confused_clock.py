#http://puzzling.stackexchange.com/questions/33792/confused-clock-face-puzzle
import graph

edge = lambda i, j: frozenset({i, j})
edges = {edge(12, 1)} | {edge(i, i + 1) for i in range(1, 12)}
edges |= {edge(0, k) for k in {3, 6, 9, 12}}

class Clock(graph.Node, tuple):  # _[0] center, _[1].._[12] around
    def heuristic(self, goal):
        return sum(i != v for i, v in enumerate(self) if i)
    def neighbors(self):
        # print('visiting', self)
        i0 = self.index(0)
        for i1 in range(13):
            if {i0, i1} in edges:
                tmp = list(self)
                tmp[i0] = mover = tmp[i1]
                tmp[i1] = 0
                yield Clock(tmp), (mover, i0, i1), 1
    def move(self, mover, to, fr):
        tmp = list(self)
        tmp[to], tmp[fr] = mover, 0
        return Clock(tmp)

goal = Clock(range(13))
start = Clock([0, 12, *range(2, 12), 1])
other = Clock([6, 1, 2, 3, 4, 0, 5, 7, 8, 9, 10, 11, 12])
# print(start.astar(goal))

sol = [(3, 0, 3), (2, 3, 2), (12, 2, 1), (1, 1, 12), (11, 12, 11),
    (10, 11, 10), (9, 10, 9), (8, 9, 8), (7, 8, 7), (6, 7, 6), (5, 6, 5),
    (4, 5, 4), (2, 4, 3), (12, 3, 2), (1, 2, 1), (11, 1, 12), (3, 12, 0),
    (12, 0, 3), (2, 3, 4), (4, 4, 5), (5, 5, 6), (6, 6, 7), (7, 7, 8),
    (8, 8, 9), (12, 9, 0), (3, 0, 12), (11, 12, 1), (1, 1, 2), (2, 2, 3),
    (3, 3, 0), (12, 0, 9), (9, 9, 10), (10, 10, 11), (11, 11, 12), (12, 12, 0)]

for mv in [None] + sol:
    cl = cl.move(*mv) if mv else start
    for n in cl:
        print(format(n, '2'), end=' ')
    print(mv)
