import matplotlib.pyplot as plt


def plot_solution(benchmark_name, points, solution, solution_path):
    plt.title(benchmark_name, fontsize=30)
    plt.scatter([p[0] for p in points], [p[1] for p in points], s=2)
    for edge in solution:
        plt.plot([points[edge[0]][0], points[edge[1]][0]], [points[edge[0]][1], points[edge[1]][1]],
                 'b', linewidth=0.85)

    plt.axis(compute_plot_bbox(points))
    plt.savefig(solution_path + benchmark_name)
    plt.close()

def compute_plot_bbox(points):
    xmin = min([p[0] for p in points])
    xmax = max([p[0] for p in points])
    ymin = min([p[1] for p in points])
    ymax = max([p[1] for p in points])
    margin = max(xmin, xmax, ymin, ymax) * 0.1
    xmin -= margin
    xmax += margin
    ymin -= margin
    ymax += margin
    return [xmin, xmax, ymin, ymax]