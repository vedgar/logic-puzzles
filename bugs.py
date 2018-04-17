src = '''\
a = 5
def g(x): return a + x
print(g(3))
'''
def comp(): exec(src)
comp()
