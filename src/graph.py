class DirectedGraph:
    def __init__(self, nodes=None, arcs=None):
        self.nodes = nodes or []
        self.arcs = arcs or []

    def add_node(self, node):
        self.nodes.append(node)

    def add_arc(self, src, dst, label=None):
        self.arcs.append(Arc(src, dst, label))

    def incoming(self, node):
        for arc in self.arcs:
            if arc.dst == node:
                yield arc

    def outgoing(self, node):
        for arc in self.arcs:
            if arc.src == node:
                yield arc


class Arc:
    def __init__(self, src, dst, label):
        self.src = src
        self.dst = dst
        self.label = label

    def __repr__(self):
        return "<({src}, {dst}): {label}>".format(**self.__dict__)
