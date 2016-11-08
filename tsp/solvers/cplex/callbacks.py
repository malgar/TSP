import auxiliar_functions as auxfs
import cplex
import math
import numpy as np


# Determine what methods we need
class SubtourEliminationCallback(cplex.callbacks.LazyConstraintCallback):

    def __init__(self, env):
        cplex.callbacks.LazyConstraintCallback.__init__(self, env)
        self.no_nodes = -1

    def __call__(self):
        if self.no_nodes is -1:
            # (no_nodes^2 - no_nodes)/2 = num_cols
            self.no_nodes = int((1 + math.sqrt(1 + 8*self.get_num_cols())) / 2)
            print "Number of nodes = " + str(self.no_nodes)

        if not self.is_unbounded_node():
            init_var = "edge[0,1]"
            final_var = "edge[" + str(self.no_nodes-2) + "," + str(self.no_nodes-1) + "]"
            values = self.get_values(init_var, final_var)

            edges = []
            for i in range(len(values)):
                if values[i] > 0.5:
                    p0 = auxfs.get_node_1(i, self.no_nodes)
                    p1 = auxfs.get_node_2(i, self.no_nodes, p0)
                    edges.append([p0, p1])

            # Shortest tour ordered by node_id
            shortest_tour = self.subtour(edges)
            if len(shortest_tour) < self.no_nodes:
                edge_vars = []
                for i in range(len(shortest_tour) - 1):
                    for j in range(i+1, len(shortest_tour)):
                        edge_vars.append("edge[" + str(shortest_tour[i]) + "," + str(shortest_tour[j]) + "]")
                # ATTENTION: Would it be better to add a local lazy constraint?
                self.add(constraint=[edge_vars, [1.0]*len(edge_vars)],
                         sense="L",
                         rhs=len(shortest_tour) - 1)
                print "Lazy constraint added (Subtour eliminated: )" + str(shortest_tour)
        else:
            print "Unbounded node"

    # Returns all subtour ids containing one vertex from the edge
    def get_subtour_ids(self, edge, subtours):
        ids = []
        for i in range(len(subtours)):
            if edge[0] in subtours[i] or edge[1] in subtours[i]:
                ids.append(i)
        return ids

    # Merges subtours that are not so, reindexing the others
    def merge(self, subtours, i, j):
        subtours[i].extend(subtours[j])
        for k in range(j, len(subtours) - 1):
            subtours[k] = subtours[k + 1]
        del subtours[len(subtours) - 1]

    # Given a list of edges, finds the shortest subtour
    def subtour(self, edges):
        subtours = []
        for edge in edges:
            subtour_ids = self.get_subtour_ids(edge, subtours)
            if len(subtour_ids) == 0:
                subtours.append([edge[0], edge[1]])
            elif len(subtour_ids) == 1:
                st_id = subtour_ids[0]
                if edge[0] not in subtours[st_id]:
                    subtours[st_id].append(edge[0])
                elif edge[1] not in subtours[st_id]:
                    subtours[st_id].append(edge[1])
            elif len(subtour_ids) == 2:
                self.merge(subtours, subtour_ids[0], subtour_ids[1])
            else:
                print "ERROR: Subtour identifying found more than one container with same node"

        subtour_lengths = [len(subtours[i]) for i in range(len(subtours))]
        shortest_subtour = subtours[subtour_lengths.index(min(subtour_lengths))]
        return sorted(shortest_subtour)
