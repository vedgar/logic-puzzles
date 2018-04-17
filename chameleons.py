from collections import deque
start = (13, 15, 17)
def neighbors(conf):
    a, b, c = conf
    if a < 0 or b < 0 or c < 0: return
    if a == b == 0 or a == c == 0 or b == c == 0: print('yes')
    yield a - 1, b - 1, c + 2
    yield a - 1, b + 2, c - 1
    yield a + 2, b - 1, c - 1

q = deque([start])
poss = set()
while q:
    a, b, c = conf = q.popleft()
    if a < 0 or b < 0 or c < 0:
        continue
    if conf in poss:
        continue
    poss.add(conf)
    q.extend(neighbors(conf))
poss2 = {(a, b) for a, b, c in poss}
for a in range(45):
    for b in range(45):
        if (a, b) in poss2:
            print(end='#')
        else:
            print(end='.')
    print()
