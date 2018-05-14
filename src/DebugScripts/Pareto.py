from platypus import NSGAII, Problem, Real
from math import sqrt

def schaffer(x):
        return [x[0]**2, (x[0]-x[1]-2)**2]

problem = Problem(2, 2)
problem.types[:] = Real(0, 5)
problem.function = schaffer

algorithm = NSGAII(problem)
algorithm.run(10000)
for solution in algorithm.result:
    print(solution.objectives)

'''
exact1 = []
exact2 = []
dx = 5.0/1000
rmin = 1e10
xmin = 0.0
for i in range(1000):
    vals = schaffer([i*dx])
    exact1.append(vals[0])
    exact2.append(vals[1])
    r = vals[0]**2 + vals[1]**2
    r = sqrt(r)
    if rmin > r:
        rmin = r
        xmin = i*dx
'''
import matplotlib.pyplot as plt

plt.scatter([s.objectives[0] for s in algorithm.result],
            [s.objectives[1] for s in algorithm.result])

#plt.scatter(exact1, exact2)
plt.xlim([0, 5.1])
plt.ylim([0, 5.1])
plt.xlabel("$f_1(x)$")
plt.ylabel("$f_2(x)$")
plt.show()

#print("Min R:", xmin, rmin)
