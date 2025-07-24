from z3 import *


x = Real('x')
y = Int('y')
a, b, c = Reals('a b c')
s, r = Ints('s r')
print (x + y + 1 + (a + s))
print (ToReal(y) + c)

x = Int('x')
y = Int('y')
f = Function('f', IntSort(), IntSort())
solve(f(f(x)) == x, f(x) == y, x != y)