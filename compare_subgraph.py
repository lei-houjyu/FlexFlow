import sys
import re

class Node:
    def __init__(self, op_type, guid, idx):
        self.op_type = op_type
        self.guid = guid
        self.idx = idx

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.op_type == other.op_type and \
                   self.guid == other.guid and \
                   self.idx == other.idx
        return False

    def __hash__(self):
        return hash((self.op_type, self.guid, self.idx))

    def __str__(self):
        return '(' + self.op_type + '/' + str(self.guid) + '/' + str(self.idx) + ')'

class Edge:
    def __init__(self, edge):
         words = re.split(r'[()]', edge)
         self.src = Node(words[1], int(words[3]), int(words[5]))
         self.dst = Node(words[7], int(words[9]), int(words[11]))

    def __eq__(self, other):
        if isinstance(other, Edge):
            # print('src equivelance', self.src == other.src)
            # print('dst equivelance', self.dst == other.dst)

            return self.src == other.src and self.dst == other.dst
        return False

    def __hash__(self):
        return hash((self.src, self.dst))

    def __str__(self):
        return str(self.src) + ' -> ' + str(self.dst) + '\n'

class Subgraph:
    def __init__(self, edges, sink_node, input_shape, output_shape):
        self.edges = edges
        self.sink_node = sink_node
        self.input_shape = input_shape
        self.output_shape = output_shape

    def __eq__(self, other):
        if isinstance(other, Subgraph):
            # print('edges equivelance', self.edges == other.edges)
            # print('sink_node equivelance', self.sink_node == other.sink_node)
            # print('input_shape equivelance', self.input_shape == other.input_shape)
            # print('output_shape equivelance', self.output_shape == other.output_shape)

            return self.edges == other.edges and \
                   self.sink_node == other.sink_node and \
                   self.input_shape == other.input_shape and \
                   self.output_shape == other.output_shape
        return False

    def __hash__(self):
        v = hash((self.sink_node, self.input_shape, self.output_shape))
        for e in self.edges:
            v += hash(e)
        return v

    def __str__(self):
        s = 'sink_node: ' + self.sink_node + '\n' + \
            'input_shape: ' + self.input_shape + '\n' + \
            'output_shape: ' + self.output_shape + '\n'
        for e in self.edges:
            s += str(e)
        return s

class Model:
    def __init__(self, name):
        self.name = name
        self.subgraphs = set()

    def __str__(self):
        boundary = '----------\n'
        s = boundary + self.name + '\n'
        for g in self.subgraphs:
            s += boundary + str(g)
        s += boundary
        return s

    def read_subgraphs(self):
        with open(self.name, 'r') as f:
            line = f.readline()
            while line:
                if line.startswith('type('):
                    edges = set()
                    input_shape = ''
                    while not line.startswith('sink_node'):
                        e = Edge(line)
                        edges.add(e)
                        line = f.readline()
                    sink_node = line.split()[1]
                    line = f.readline() # the prompt output_shape:
                    line = f.readline() # the actual output shape
                    if line != 'input shape: ':
                        output_shape = line
                    line = f.readline()
                    if line[:1].isdigit():
                        input_shape = line
                    
                    g = Subgraph(edges, sink_node, input_shape, output_shape)
                    self.subgraphs.add(g)
                else:
                    line = f.readline()

    def add_subgraph(self, graph):
        self.subgraphs.add(graph)

    def duplication_rate(self, other):
        if not isinstance(other, Model):
            print("Input should be a model!")

        subgraph_num = len(self.subgraphs)
        duplication = 0

        for g in self.subgraphs:
            if g in other.subgraphs:
                duplication += 1

        return float(duplication) / subgraph_num

if len(sys.argv) < 3:
    sys.exit("Usage: python3 compare_subgraph.py log_file_1 log_file_2 ...")

model_num = len(sys.argv)
models = list()

for i in range(1, model_num):
    name = sys.argv[i]
    m = Model(name)
    m.read_subgraphs()
    models.append(m)

for m in models:
    print('\t', m.name[:-4], end='')
print()

for m1 in models:
    print(m1.name[:-4], end='\t')
    for m2 in models:
        print(m1.duplication_rate(m2), end='\t')
    print()