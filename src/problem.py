
class Graph[V]:
    def __init__(self, vertices: list[V], edges: list[tuple[V, V]]):
        self.vertices = vertices
        self.edges = edges


class VertexCoverProblem:
    def __init__(self, graph: Graph, k: int):
        self.graph = graph
        self.k = k