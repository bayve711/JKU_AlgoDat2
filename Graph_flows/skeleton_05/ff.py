# Ford-Fulkerson algorithm in Python

class Graph:

    def __init__(self, graph):
        self.graph = graph  # original graph
        self.residual_graph = [[cell for cell in row] for row in graph]  # cloned graph
        self.latest_augmenting_path = [[0 for _ in row] for row in graph]  # empty graph with same dimension as graph
        self.current_flow = [[0 for _ in row] for row in graph]  # empty graph with same dimension as graph

    def ff_step(self, source, sink):
        """
        Perform a single flow augmenting iteration from source to sink. Update the latest augmenting path, the residual
        graph and the current flow by the maximum possible amount, according to the path found by BFS.
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the amount by which the flow has increased.
        """

        path, parent = self.bfs(source, sink)

        if path is False:
            return 0

        self.latest_augmenting_path = [[0] * len(self.graph) for _ in range(len(self.graph))]

        min_flow = float('inf')
        s = sink
        while s is not source:
            par = parent[s]
            min_flow = min(min_flow, self.residual_graph[par][s])
            s = par

        s = sink
        while s is not source:
            par = parent[s]
            self.residual_graph[par][s] -= min_flow
            self.residual_graph[s][par] += min_flow

            if self.graph[par][s] != 0:
                self.current_flow[par][s] += min_flow
                self.latest_augmenting_path[par][s] = min_flow
            else:
                self.current_flow[s][par] -= min_flow
                self.latest_augmenting_path[s][par] = -min_flow

            s = par

        return min_flow

    def ford_fulkerson(self, source, sink):
        max_flow = 0

        while True:
            flow = self.ff_step(source, sink)
            if flow == 0:
                break
            max_flow += flow

        return max_flow


    def bfs(self, source, sink):
        visited = [False] * len(self.residual_graph)
        parent = [-1] * len(self.residual_graph)
        queue = []

        queue.append(source)
        visited[source] = True

        while queue:
            u = queue.pop(0)

            for v, capacity in enumerate(self.residual_graph[u]):
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u

        return visited[sink], parent






