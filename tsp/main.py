import os
import time

import data_loader
import plotter
import solver.gurobi.gurobi_model as grb_m

INPUT_PATH = '.../TSP/data/input/'
OUTPUT_PATH = '.../TSP/data/output/'

output_file = open(OUTPUT_PATH + 'solution.txt', 'w')
try:
    output_file.write('name;no_nodes;optimal;time;gap;no_lazy;total_distance;total_time\n')
    for filename in os.listdir(INPUT_PATH):
        start = time.time()
        dl = data_loader.DataLoader(INPUT_PATH + filename)
        nodes = dl.load_data()
        if 2 < len(nodes) < 1100:
            output_file.write(dl.benchmark_name + ';' + str(len(dl.nodes)) + ';')
            solution = grb_m.solve(nodes, output_file)
            #solution = cplx_m.solve(nodes, output_file)
            if len(solution) > 0:
                output_tour = open(OUTPUT_PATH + dl.benchmark_name + '_tour.txt', 'w')
                output_tour.write(str(solution))
                output_tour.close()
                #dl.plot_solution(solution)
                plotter.plot_solution(dl.benchmark_name, nodes, solution, OUTPUT_PATH)
            end = time.time()
            output_file.write(";" + str(end-start) + "\n")
except Exception as exc:
    print "Exception: " + str(exc)
finally:
    output_file.close()