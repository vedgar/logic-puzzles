# http://wiki.c2.com/?HomoiconicExampleInManyProgrammingLanguages

from ast import *

def execute(statement):
    print(dump(statement))
    suite = fix_missing_locations(Interactive([statement]))
    code = compile(suite, '<artificially constructed>', 'single')
    eval(code, globals())

assign = Assign([Name('b', Store())], Num(15))
execute(assign)
print(b)
assign.value.n = 37
execute(assign)
print(b)
