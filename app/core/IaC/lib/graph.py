from collections import defaultdict, deque
from typing import Dict, List, Set, Tuple, Optional, Any

class DirectedAcyclicGraph:
    """
    A specialized graph data structure for Directed Acyclic Graphs (DAGs).
    Automatically prevents cycle creation and provides DAG-specific algorithms.
    """
    
    def __init__(self):
        self.adj_list = defaultdict(list)  # adjacency list representation
        self.vertices = set()
        self.edges = set()
        self.in_degree = defaultdict(int)  # track incoming edges for each vertex
        
    def add_vertex(self, vertex: Any) -> None:
        """Add a vertex to the DAG."""
        if vertex not in self.vertices:
            self.vertices.add(vertex)
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
        if vertex not in self.in_degree:
            self.in_degree[vertex] = 0
    
    def add_edge(self, u: Any, v: Any, weight: float = 1) -> bool:
        """
        Add an edge from u to v with optional weight.
        Returns False if adding the edge would create a cycle.
        """
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Check if adding this edge would create a cycle
        if self._would_create_cycle(u, v):
            return False
        
        # Add the edge
        self.adj_list[u].append((v, weight))
        self.edges.add((u, v, weight))
        self.in_degree[v] += 1
        
        return True
    
    def _would_create_cycle(self, u: Any, v: Any) -> bool:
        """Check if adding edge u->v would create a cycle."""
        # If there's already a path from v to u, adding u->v creates a cycle
        return self._has_path(v, u)
    
    def _has_path(self, start: Any, end: Any) -> bool:
        """Check if there's a path from start to end using DFS."""
        if start == end:
            return True
        
        visited = set()
        stack = [start]
        
        while stack:
            current = stack.pop()
            if current == end:
                return True
            
            if current in visited:
                continue
                
            visited.add(current)
            for neighbor, _ in self.adj_list[current]:
                if neighbor not in visited:
                    stack.append(neighbor)
        
        return False
    
    def remove_vertex(self, vertex: Any) -> None:
        """Remove a vertex and all its edges from the DAG."""
        if vertex not in self.vertices:
            return
        
        # Remove all edges where this vertex is the destination
        for source in list(self.adj_list.keys()):
            self.adj_list[source] = [(neighbor, weight) for neighbor, weight in self.adj_list[source] 
                                   if neighbor != vertex]
        
        # Remove from data structures
        del self.adj_list[vertex]
        del self.in_degree[vertex]
        self.vertices.remove(vertex)
        
        # Remove from edges set
        edges_to_remove = [edge for edge in self.edges if vertex in edge[:2]]
        for edge in edges_to_remove:
            self.edges.remove(edge)
    
    def remove_edge(self, u: Any, v: Any) -> bool:
        """Remove an edge from u to v. Returns True if edge existed."""
        if u not in self.vertices or v not in self.vertices:
            return False
        
        # Find and remove the edge
        original_length = len(self.adj_list[u])
        self.adj_list[u] = [(neighbor, weight) for neighbor, weight in self.adj_list[u] 
                           if neighbor != v]
        
        if len(self.adj_list[u]) < original_length:
            self.in_degree[v] -= 1
            # Remove from edges set
            for edge in self.edges:
                if edge[:2] == (u, v):
                    self.edges.remove(edge)
                    break
            return True
        
        return False
    
    def get_successors(self, vertex: Any) -> List[Tuple[Any, float]]:
        """Get all successors (outgoing neighbors) of a vertex with their edge weights."""
        return self.adj_list.get(vertex, [])
    
    def get_predecessors(self, vertex: Any) -> List[Tuple[Any, float]]:
        """Get all predecessors (incoming neighbors) of a vertex with their edge weights."""
        predecessors = []
        for v in self.vertices:
            for neighbor, weight in self.adj_list[v]:
                if neighbor == vertex:
                    predecessors.append((v, weight))
        return predecessors
    
    def has_edge(self, u: Any, v: Any) -> bool:
        """Check if an edge exists from u to v."""
        if u not in self.vertices or v not in self.vertices:
            return False
        return any(neighbor == v for neighbor, _ in self.adj_list[u])
    
    def get_edge_weight(self, u: Any, v: Any) -> Optional[float]:
        """Get the weight of the edge from u to v."""
        for neighbor, weight in self.adj_list.get(u, []):
            if neighbor == v:
                return weight
        return None
    
    def vertex_count(self) -> int:
        """Return the number of vertices in the DAG."""
        return len(self.vertices)
    
    def edge_count(self) -> int:
        """Return the number of edges in the DAG."""
        return len(self.edges)
    
    def get_roots(self) -> List[Any]:
        """Get all vertices with no incoming edges (roots/sources)."""
        return [vertex for vertex in self.vertices if self.in_degree[vertex] == 0]
    
    def get_leaves(self) -> List[Any]:
        """Get all vertices with no outgoing edges (leaves/sinks)."""
        return [vertex for vertex in self.vertices if len(self.adj_list[vertex]) == 0]
    
    # def dfs(self, start: Any, visited: Optional[Set] = None) -> Set[Any]:
    #     """Depth-First Search traversal starting from a vertex."""
    #     if visited is None:
    #         visited = set()
        
    #     if start not in self.vertices or start in visited:
    #         return visited
        
    #     visited.add(start)
    #     for neighbor, _ in self.adj_list[start]:
    #         if neighbor not in visited:
    #             self.dfs(neighbor, visited)
        
    #     return visited
    
    # def bfs(self, start: Any) -> List[Any]:
    #     """Breadth-First Search traversal starting from a vertex."""
    #     if start not in self.vertices:
    #         return []
        
    #     visited = set()
    #     queue = deque([start])
    #     result = []
        
    #     while queue:
    #         vertex = queue.popleft()
    #         if vertex not in visited:
    #             visited.add(vertex)
    #             result.append(vertex)
                
    #             for neighbor, _ in self.adj_list[vertex]:
    #                 if neighbor not in visited:
    #                     queue.append(neighbor)
        
    #     return result
    
    # def shortest_path_dijkstra(self, start: Any, end: Any) -> Tuple[List[Any], float]:
    #     """Find shortest path using Dijkstra's algorithm."""
    #     if start not in self.vertices or end not in self.vertices:
    #         return [], float('inf')
        
    #     distances = {vertex: float('inf') for vertex in self.vertices}
    #     distances[start] = 0
    #     previous = {}
    #     pq = [(0, start)]
    #     visited = set()
        
    #     while pq:
    #         current_dist, current = heapq.heappop(pq)
            
    #         if current in visited:
    #             continue
            
    #         visited.add(current)
            
    #         if current == end:
    #             break
            
    #         for neighbor, weight in self.adj_list[current]:
    #             if neighbor not in visited:
    #                 new_dist = current_dist + weight
    #                 if new_dist < distances[neighbor]:
    #                     distances[neighbor] = new_dist
    #                     previous[neighbor] = current
    #                     heapq.heappush(pq, (new_dist, neighbor))
        
    #     # Reconstruct path
    #     path = []
    #     current = end
    #     while current in previous:
    #         path.append(current)
    #         current = previous[current]
    #     path.append(start)
    #     path.reverse()
        
    #     return path if distances[end] != float('inf') else [], distances[end]
    
    # def topological_sort_kahn(self) -> List[Any]:
    #     """Topological sort using Kahn's algorithm (BFS-based)."""
    #     # Create a copy of in_degree to avoid modifying the original
    #     in_degree_copy = self.in_degree.copy()
    #     queue = deque([vertex for vertex in self.vertices if in_degree_copy[vertex] == 0])
    #     result = []
        
    #     while queue:
    #         current = queue.popleft()
    #         result.append(current)
            
    #         # Reduce in-degree of all successors
    #         for neighbor, _ in self.adj_list[current]:
    #             in_degree_copy[neighbor] -= 1
    #             if in_degree_copy[neighbor] == 0:
    #                 queue.append(neighbor)
        
    #     return result
    
    # def topological_sort_dfs(self) -> List[Any]:
    #     """Topological sort using DFS-based algorithm."""
    #     visited = set()
    #     stack = []
        
    #     def dfs_topo(vertex):
    #         visited.add(vertex)
    #         for neighbor, _ in self.adj_list[vertex]:
    #             if neighbor not in visited:
    #                 dfs_topo(neighbor)
    #         stack.append(vertex)
        
    #     for vertex in self.vertices:
    #         if vertex not in visited:
    #             dfs_topo(vertex)
        
    #     return stack[::-1]
    
    # def longest_path(self, start: Any, end: Any) -> Tuple[List[Any], float]:
    #     """Find longest path from start to end (useful for critical path analysis)."""
    #     if start not in self.vertices or end not in self.vertices:
    #         return [], float('-inf')
        
    #     # Use topological sort to process vertices in order
    #     topo_order = self.topological_sort_kahn()
        
    #     # Initialize distances (use negative infinity for longest path)
    #     distances = {vertex: float('-inf') for vertex in self.vertices}
    #     distances[start] = 0
    #     previous = {}
        
    #     # Process vertices in topological order
    #     for vertex in topo_order:
    #         if distances[vertex] != float('-inf'):
    #             for neighbor, weight in self.adj_list[vertex]:
    #                 new_dist = distances[vertex] + weight
    #                 if new_dist > distances[neighbor]:
    #                     distances[neighbor] = new_dist
    #                     previous[neighbor] = vertex
        
    #     # Reconstruct path
    #     path = []
    #     current = end
    #     while current in previous:
    #         path.append(current)
    #         current = previous[current]
    #     path.append(start)
    #     path.reverse()
        
    #     return path if distances[end] != float('-inf') else [], distances[end]
    
    def remove_vertex_cascade(self, vertex: Any) -> Set[Any]:
        """
        Remove a vertex and all vertices that point to it (cascade deletion).
        Returns the set of all vertices that were removed.
        """
        if vertex not in self.vertices:
            return set()
        
        vertices_to_remove = set()
        
        def find_predecessors(target_vertex, visited=None):
            """Recursively find all vertices that can reach target_vertex."""
            if visited is None:
                visited = set()
            
            if target_vertex in visited:
                return
            
            visited.add(target_vertex)
            vertices_to_remove.add(target_vertex)
            
            # Find all vertices that point to target_vertex
            for v in self.vertices:
                if v not in visited:
                    for neighbor, _ in self.adj_list[v]:
                        if neighbor == target_vertex:
                            find_predecessors(v, visited)
        
        # Start the cascade from the target vertex
        find_predecessors(vertex)
        
        # Remove all identified vertices
        for v in vertices_to_remove.copy():
            if v in self.vertices:
                self.remove_vertex(v)
        
        return vertices_to_remove
    
    def remove_vertext_cascade_reverse(self, vertex: Any) -> Set[Any]:
        """
        Remove a vertex and all vertices that it points to (cascade deletion).
        Returns the set of all vertices that were removed.
        """
        if vertex not in self.vertices:
            return set()
        
        vertices_to_remove = set()
        
        def find_successors(target_vertex, visited=None):
            """Recursively find all vertices that are reachable from target_vertex."""
            if visited is None:
                visited = set()
            
            if target_vertex in visited:
                return
            
            visited.add(target_vertex)
            vertices_to_remove.add(target_vertex)
            
            # Find all successors of target_vertex
            for neighbor, _ in self.adj_list[target_vertex]:
                if neighbor not in visited:
                    find_successors(neighbor, visited)
        
        # Start the cascade from the target vertex
        find_successors(vertex)
        
        # Remove all identified vertices
        for v in vertices_to_remove.copy():
            if v in self.vertices:
                self.remove_vertex(v)
        
        return vertices_to_remove

    def get_all_paths(self, start: Any, end: Any) -> List[List[Any]]:
        """Find all paths from start to end."""
        if start not in self.vertices or end not in self.vertices:
            return []
        
        all_paths = []
        
        def dfs_paths(current, target, path):
            if current == target:
                all_paths.append(path[:])
                return
            
            for neighbor, _ in self.adj_list[current]:
                if neighbor not in path:  # Avoid cycles (shouldn't happen in DAG)
                    path.append(neighbor)
                    dfs_paths(neighbor, target, path)
                    path.pop()
        
        dfs_paths(start, end, [start])
        return all_paths
    
    def get_reachable_vertices(self, start: Any) -> Set[Any]:
        """Get all vertices reachable from the start vertex."""
        return self.dfs(start)
    
    def is_ancestor(self, ancestor: Any, descendant: Any) -> bool:
        """Check if ancestor can reach descendant."""
        return self._has_path(ancestor, descendant)
    
    def __str__(self) -> str:
        """String representation of the DAG."""
        result = ["Directed Acyclic Graph:"]
        result.append(f"Vertices: {len(self.vertices)}")
        result.append(f"Edges: {len(self.edges)}")
        result.append(f"Roots: {self.get_roots()}")
        result.append(f"Leaves: {self.get_leaves()}")
        result.append("Adjacency List:")
        
        for vertex in sorted(self.vertices):
            successors = [f"{neighbor}({weight})" for neighbor, weight in self.adj_list[vertex]]
            in_deg = self.in_degree[vertex]
            result.append(f"  {vertex} (in-degree: {in_deg}): {successors}")
        
        return "\n".join(result)


# Example usage and testing
# if __name__ == "__main__":
#     # Create a DAG
#     dag = DirectedAcyclicGraph()
    
#     # Add vertices and edges
#     print("Adding edges to DAG:")
#     print(f"A -> B: {dag.add_edge('A', 'B', 4)}")
#     print(f"A -> C: {dag.add_edge('A', 'C', 2)}")
#     print(f"B -> D: {dag.add_edge('B', 'D', 5)}")
#     print(f"C -> D: {dag.add_edge('C', 'D', 8)}")
#     print(f"D -> E: {dag.add_edge('D', 'E', 2)}")
    
#     # Try to add an edge that would create a cycle
#     print(f"E -> A (would create cycle): {dag.add_edge('E', 'A', 1)}")
#     print()
    
#     print("DAG Structure:")
#     print(dag)
#     print()
    
#     # Test DAG-specific methods
#     print("Roots (no incoming edges):", dag.get_roots())
#     print("Leaves (no outgoing edges):", dag.get_leaves())
#     print()
    
#     # Test traversals
#     print("BFS from A:", dag.bfs('A'))
#     print("DFS from A:", list(dag.dfs('A')))
#     print()
    
#     # Test topological sorts
#     print("Topological Sort (Kahn's):", dag.topological_sort_kahn())
#     print("Topological Sort (DFS):", dag.topological_sort_dfs())
#     print()
    
#     # Test shortest and longest paths
#     short_path, short_dist = dag.shortest_path_dijkstra('A', 'E')
#     print(f"Shortest path A to E: {short_path} (distance: {short_dist})")
    
#     long_path, long_dist = dag.longest_path('A', 'E')
#     print(f"Longest path A to E: {long_path} (distance: {long_dist})")
#     print()
    
#     # Test all paths
#     all_paths = dag.get_all_paths('A', 'E')
#     print(f"All paths from A to E: {all_paths}")
#     print()
    
#     # Test ancestry
#     print(f"Is A ancestor of E? {dag.is_ancestor('A', 'E')}")
#     print(f"Is E ancestor of A? {dag.is_ancestor('E', 'A')}")
#     print()
    
#     # Test cascade removal
#     print("Testing cascade removal:")
#     test_dag = DirectedAcyclicGraph()
#     test_dag.add_edge('A', 'B')
#     test_dag.add_edge('B', 'D')
#     test_dag.add_edge('C', 'D')
#     test_dag.add_edge('E', 'F')
    
#     print("Before cascade removal:")
#     print(test_dag)
#     print()
    
#     removed = test_dag.remove_vertex_cascade('D')
#     print(f"Removed vertices: {removed}")
#     print("After cascade removal:")
#     print(test_dag)