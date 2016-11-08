from gurobipy import *
import math

no_lazy = 0

# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.callback.MIPSOL:
        selected = []
        # make a list of edges selected in the solution
        no_nodes = int(math.sqrt(len(model._vars)))
        for i in range(no_nodes):
            sol = model.cbGetSolution([model._vars[i, j] for j in range(no_nodes)])
            selected += [(i, j) for j in range(no_nodes) if sol[j] > 0.5]
        # find the shortest cycle in the selected edge list
        tour = subtour(selected, no_nodes)
        if len(tour) < no_nodes:
            # add a subtour elimination constraint
            expr = 0
            for i in range(len(tour)):
                for j in range(i + 1, len(tour)):
                    expr += model._vars[tour[i], tour[j]]
            print "Lazy constraint added. (Subtour elimination: " + str(tour) + " )"
            model.cbLazy(expr <= len(tour) - 1)
            global no_lazy
            no_lazy += 1

# Given a list of edges, finds the shortest subtour

def subtour(edges, no_nodes):
    visited = [False] * no_nodes
    cycles = []
    lengths = []
    selected = [[] for i in range(no_nodes)]
    for x, y in edges:
        selected[x].append(y)
    while True:
        current = visited.index(False)
        thiscycle = [current]
        while True:
            visited[current] = True
            neighbors = [x for x in selected[current] if not visited[x]]
            if len(neighbors) == 0:
                break
            current = neighbors[0]
            thiscycle.append(current)
        cycles.append(thiscycle)
        lengths.append(len(thiscycle))
        if sum(lengths) == no_nodes:
            break
    return cycles[lengths.index(min(lengths))]