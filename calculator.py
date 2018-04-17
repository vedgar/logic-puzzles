import itertools, contextlib, collections, math, re
from operator import add, sub, mul, floordiv, truediv
moves = 5
goal = 268
start = 25
labels = 'Store'
buttons = set(labels.split())

def exactdiv(x, y):
    r = x / y
    if r.is_integer():
        return int(r)
    raise ZeroDivisionError

def apply(button, num):
    if button.casefold() == 'mirror':
        res = str(num).strip('-')
        res += res[::-1]
        return -int(res) if num < 0 else int(res)
    if 'shift' in button.casefold():
        res = str(num).strip('-')
        if button.startswith('<'):
            res = res[1:] + res[0]
        elif button.endswith('>'):
            res = res[~0] + res[:-1]
        return -int(res) if num < 0 else int(res)
    if button.casefold() == 'sum':
        res = sum(map(int, str(num).strip('-')))
        return -res if num < 0 else res
    if button.casefold() == 'reverse':
        res = int(str(num).strip('-')[::-1])
        return -res if num < 0 else res
    if button == '<<': button = '//10'
    if button == '+-': button = '*-1'
    valid = {'+': add, '-': sub, '**': pow, '*': mul,
             '//': floordiv, '/': exactdiv}
    for sign, operation in valid.items():
        if button.startswith(sign):
            other = int(button[len(sign):])
            return operation(num, other)
    left, arrow, right = button.partition('=>')
    if arrow:
        return int(str(int(num)).replace(left, right))
    return int(str(int(num)) + button)

def old_API():
    found = False
    for moves1 in range(1 + moves):
        for seq in itertools.product(buttons, repeat=moves1):
            num = start
            with contextlib.suppress(AssertionError, ZeroDivisionError):
                for button in seq:
                    num = apply(button, num)
                    assert num < 10**7
                    if num == goal:
                        print(' '.join(seq))
                        found = True
                        break
        if found:
            break

def explore(display, goal, buttons, path, move, moves):
    if display == goal:
        yield path
    elif display < 10 ** 7:
        for button in buttons:
            if button.startswith('['):
                metabutton = button.replace('[', '').replace(']', '')
                newbuttons = [bapply(metabutton, button) for button in buttons]
                yield from explore(display, goal, newbuttons, path + [button],
                                   move + 1, moves)
            else:
                newdisplay = apply(button, display)
                yield from explore(newdisplay, goal, buttons, path + [button],
                                   move + 1, moves)

def bfs(display, goal, buttons, moves):
    queue = collections.deque([(display, buttons, [])])
    minlen = None
    while queue:
        display, buttons, path = queue.popleft()
        pathlen = sum('store' not in button.casefold() for button in path)
        if display == goal:
            if minlen is None: minlen = pathlen
            if minlen == pathlen: print('\t'.join(path))
        elif display >= 10 ** 7 or pathlen >= moves:
            continue
        for button in buttons:
            if button.casefold().startswith('store'):
                ...
            elif button.startswith('['):
                newdisplay = display
                metabutton = button.replace('[', '').replace(']', '')
                newbuttons = [bapply(metabutton, button) for button in buttons
                              if not button.startswith('[')]
            else:
                newdisplay = apply(button, display)
                newbuttons = buttons
            queue.append((newdisplay, newbuttons, path + [button]))

def bapply(metabutton, button):
    def applymeta(match):
        return str(apply(metabutton, int(match.group())))
    return re.sub(r'\d+', applymeta, button)

bfs(start, goal, buttons, moves)
