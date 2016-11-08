import math

import cplex

import auxiliar_functions as auxfs
import callbacks


def distance(nodes, i, j):
    dx = nodes[i][0] - nodes[j][0]
    dy = nodes[i][1] - nodes[j][1]
    return math.sqrt(dx*dx + dy*dy)


def calculate_cost(nodes):
    d = []
    for i in range(len(nodes) - 1):
        for j in range(i+1, len(nodes)):
            d.append(distance(nodes, i, j))
    return d


def create_var_names(nodes):
    names = []
    for i in range(len(nodes) - 1):
        for j in range(i+1, len(nodes)):
            names.append("edge[" + str(i) + "," + str(j) + "]")
    return names


def solve(nodes, output_file):
    model = cplex.Cplex()

    no_nodes = len(nodes)
    no_vars = (no_nodes**2 - no_nodes)/2

    # Variable creation
    model.variables.add(obj=calculate_cost(nodes),
                        types=[model.variables.type.binary]*no_vars,
                        names=create_var_names(nodes))

    # Constraint creation
    # (1) sum(j, edge[i,j]) == 2; for every i
    # Since no variable edge[i,j] with i>=j is defined:
    # sum(j : j>i, edge[i,j]) + sum(j : j<i, edge[j,i]) == 2; for every i
    # for i in range(no_nodes - 1):
    #     lin_expr_vars = []
    #     for j in range(i + 1, no_nodes):
    #         lin_expr_vars.append("edge[" + str(i) + "," + str(j) + "]")
    #     for k in range(i):
    #         lin_expr_vars.append("edge[" + str(k) + "," + str(i) + "]")
    #
    #     lin_expr_coeffs = [1.0]*len(lin_expr_vars)
    #
    #     model.linear_constraints.add(lin_expr=[[lin_expr_vars, lin_expr_coeffs]],
    #                                  rhs=[2.0])

    # Try to reduce time by adding all constraints at a time
    model.linear_constraints.add(lin_expr=[[["edge[" + str(i) + "," + str(j) + "]" for j in range(i + 1, no_nodes)] + [
        "edge[" + str(k) + "," + str(i) + "]" for k in range(i)], [1.0] * (no_nodes - 1)] for i in range(no_nodes - 1)],
                                 rhs=[2.0] * (no_nodes - 1))

    # Objective function
    model.objective.set_sense(model.objective.sense.minimize)

    # Parameter setting due to lazy constraint use
    model.parameters.preprocessing.reduce.set(0)
    model.parameters.advance.set(0)
    model.parameters.timelimit.set(900)

    model.register_callback(callbacks.SubtourEliminationCallback)

    # model.write("model", "lp")

    # Model solving
    solution = []
    start_time = model.get_time()
    model.solve()
    end_time = model.get_time()
    cplex_time = end_time - start_time
    status = model.solution.get_status()
    print "Solution status = " + str(status)
    if status in (101, 102, 107, 113):
        distance_msg = "Total distance "
        if status is 107:
            distance_msg += "(not optimal) "
        distance_msg += " = " + str(model.solution.get_objective_value())
        print distance_msg

        values = model.solution.get_values("edge[0,1]", "edge[" + str(no_nodes - 2) + "," + str(no_nodes - 1) + "]")
        for i in range(len(values)):
            if values[i] > 0.5:
                p0 = auxfs.get_node_1(i, no_nodes)
                p1 = auxfs.get_node_2(i, no_nodes, p0)
                solution.append([p0, p1])

        if status in (101,102):
            output_file.write("1;")
        else:
            output_file.write("0;")

        output_file.write(str(cplex_time) + ";" + str(model.solution.MIP.get_mip_relative_gap()) + ";" +
                          str(model.solution.MIP.get_num_cuts(model.solution.MIP.cut_type.user)) + ";" +
                          str(model.solution.get_objective_value()))

    else:
        output_file.write("-1;;;;")

    return solution
