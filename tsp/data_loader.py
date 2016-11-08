

# This should not be a class
class DataLoader:

    def __init__(self, file_path):
        self.benchmark_name = ""
        self.file_path = file_path
        self.nodes = []

    def is_node(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    def load_data(self):
        tsp_file = open(self.file_path, 'r')
        for line in tsp_file:
            node_info = line.split()
            if "NAME" in node_info[0]:
                self.benchmark_name = node_info[len(node_info) - 1].split('.')[0]
            if len(node_info) == 3 and self.is_node(node_info[0]):
                self.nodes.append((float(node_info[1]), float(node_info[2])))
            if "EOF" in node_info:
                break
        return self.nodes
