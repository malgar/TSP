import math

from gurobipy import *

import callbacks


# Euclidean distance between two points
def distance(points, i, j):
    dx = points[i][0] - points[j][0]
    dy = points[i][1] - points[j][1]
    return math.sqrt(dx*dx + dy*dy)


def solve(points, output_file):
    n = len(points)
    m = Model()

    # Create variables
    vars = {}
    for i in range(n):
        for j in range(i+1):
            vars[i,j] = m.addVar(obj=distance(points, i, j), vtype=GRB.BINARY,
                                 name='e'+str(i)+'_'+str(j))
            vars[j,i] = vars[i,j]
        m.update()

    # Create constraints
    # Add degree-2 constraint, and forbid loops
    for i in range(n):
        m.addConstr(quicksum(vars[i,j] for j in range(n)) == 2)
        vars[i,i].ub = 0

    m.update()

    # TODO: OJO!!!! Lo ideal seria saber como obtener el valor de lazy constraints anadidas
    callbacks.no_lazy = 0
    # Optimize model
    m._vars = vars
    m.params.LazyConstraints = 1
    # TODO: Pasarlo como parametro
    m.setParam("TimeLimit", 900)
    m.optimize(callbacks.subtourelim)

    # Build solution
    selected = []
    if m.getAttr("Status") == 2:
        solution = m.getAttr('x', vars)
        selected = [(i, j) for i in range(n) for j in range(i + 1, n) if solution[i, j] > 0.5]

        print "Total distance = " + str(m.getAttr("ObjVal"))

        output_file.write(
            "1;" + str(m.getAttr("Runtime")) + ";" + str(m.getAttr("MIPGap")) +
            ";" + str(callbacks.no_lazy) + ";" + str(int(math.floor(m.getAttr("ObjVal")))))
    elif m.getAttr("status") == 9:
        gap = m.getAttr("MIPGap")
        if gap < 1:
            solution = m.getAttr('x', vars)
            selected = [(i, j) for i in range(n) for j in range(i + 1, n) if solution[i, j] > 0.5]

            print "Total distance (not optimal) = " + str(m.getAttr("ObjVal"))

            output_file.write(
                "0;" + str(m.getAttr("Runtime")) + ";" + str(m.getAttr("MIPGap")) +
                ";" + str(callbacks.no_lazy) + ";" + str(int(math.floor(m.getAttr("ObjVal")))))
        else:
          output_file.write("0;;;")
    else:
        output_file.write("-1;;;")

    return selected

    #assert len(subtour(selected, n)) == n