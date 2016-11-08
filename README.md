# TSP
Travelling Salesman Problem. Linear Programming

Based on the following article:

https://nathanbrixius.wordpress.com/2016/06/09/computing-optimal-road-trips-using-operations-research/

I decided to try a linear programming approach to solve the (symmetric) TSP.

The modeling is simple: Minimize total distance considering only constraints related to visiting every city. Subtour elimination constraints are added dynamically only when needed.

Performance is tested using well known benchmarks and different optimization solvers (for now, CPLEX and Gurobi)
