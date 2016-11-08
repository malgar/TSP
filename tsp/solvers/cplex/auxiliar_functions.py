# Functions used throughout the different files


# node_1 = min{k : sum(i=1..k, n-i) > p} - 1
def get_node_1(p, no_nodes):
    node_1 = -1
    accum = 0
    for i in range(1, no_nodes):
        accum += no_nodes - i
        if accum > p:
            node_1 = i - 1
            break
    return node_1


# node_2 = n - 1 - ( sum(i=1..(node_1+1), n-i) - p - 1) = n + p - sum(i=1..(node_1+1), n-i) =
#        = n + p - n*(node_1+1) + (node_1+1)(node_1+2)/2
def get_node_2(p, no_nodes, node_1):
    node_2 = no_nodes + p - no_nodes*(node_1+1) + (node_1+1)*(node_1+2)/2
    return node_2