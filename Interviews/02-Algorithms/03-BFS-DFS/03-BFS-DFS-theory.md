# BFS & DFS: Complete Guide

## Explanation

**BFS (Breadth-First Search)** and **DFS (Depth-First Search)** are fundamental graph traversal algorithms with different exploration strategies:

- **BFS**: Explores level by level, uses queue
- **DFS**: Explores depth first, uses stack (recursion)

## Implementation

### Graph Representation
```python
from collections import deque, defaultdict

# Adjacency List Representation
class Graph:
    def __init__(self, directed=False):
        self.graph = defaultdict(list)
        self.directed = directed
    
    def add_edge(self, u, v):
        self.graph[u].append(v)
        if not self.directed:
            self.graph[v].append(u)
    
    def get_neighbors(self, node):
        return self.graph.get(node, [])
```

### BFS Implementation
```python
def bfs(graph, start):
    """
    BFS Implementation - Iterative with queue
    
    Args:
        graph: dict or Graph object
        start: starting node
    
    Returns:
        visited: set of visited nodes
        parent: dict tracking traversal path
        level: dict tracking distances from start
    """
    if isinstance(graph, dict):
        neighbors = lambda x: graph.get(x, [])
    else:
        neighbors = graph.get_neighbors
    
    visited = set()
    parent = {}
    level = {}
    queue = deque()
    
    # Initialize start node
    visited.add(start)
    parent[start] = None
    level[start] = 0
    queue.append(start)
    
    while queue:
        current = queue.popleft()
        
        for neighbor in neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                level[neighbor] = level[current] + 1
                queue.append(neighbor)
    
    return visited, parent, level

def bfs_path(graph, start, target):
    """BFS to find shortest path"""
    visited, parent, _ = bfs(graph, start)
    
    if target not in visited:
        return None  # No path exists
    
    # Reconstruct path
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = parent[current]
    
    return path[::-1]  # Reverse to get start->target
```

### DFS Implementation
```python
def dfs_iterative(graph, start):
    """
    DFS Implementation - Iterative with stack
    """
    if isinstance(graph, dict):
        neighbors = lambda x: graph.get(x, [])
    else:
        neighbors = graph.get_neighbors
    
    visited = set()
    parent = {}
    stack = [start]
    
    while stack:
        current = stack.pop()
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in neighbors(current):
                if neighbor not in visited:
                    parent[neighbor] = current
                    stack.append(neighbor)
    
    return visited, parent

def dfs_recursive(graph, start, visited=None, parent=None):
    """
    DFS Implementation - Recursive
    """
    if visited is None:
        visited = set()
    if parent is None:
        parent = {}
    
    if isinstance(graph, dict):
        neighbors = lambda x: graph.get(x, [])
    else:
        neighbors = graph.get_neighbors
    
    visited.add(start)
    
    for neighbor in neighbors(start):
        if neighbor not in visited:
            parent[neighbor] = start
            dfs_recursive(graph, neighbor, visited, parent)
    
    return visited, parent

# DFS with timestamps (for advanced applications)
def dfs_timestamps(graph, start):
    """DFS with discovery/finish times"""
    visited = set()
    discovery = {}
    finish = {}
    parent = {}
    time = [0]  # Use list for mutable reference
    
    def dfs_visit(node):
        time[0] += 1
        discovery[node] = time[0]
        visited.add(node)
        
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                dfs_visit(neighbor)
        
        time[0] += 1
        finish[node] = time[0]
    
    dfs_visit(start)
    return visited, parent, discovery, finish
```

## Time Complexity Analysis

### Comparative Analysis

| Algorithm | Best Case | Average Case | Worst Case | In Practice |
|-----------|-----------|--------------|------------|-------------|
| **BFS** | Ω(1) | Θ(V + E) | O(V + E) | Fast for sparse graphs, level-by-level |
| **DFS** | Ω(1) | Θ(V + E) | O(V + E) | Fast for deep graphs, memory efficient |

### Mathematical Breakdown

**Both BFS and DFS**:
- **V** = number of vertices
- **E** = number of edges
- Each vertex visited once: O(V)
- Each edge examined once: O(E)
- **Total**: O(V + E)

### Real-world Performance
```python
def benchmark_traversal():
    """Compare BFS vs DFS performance"""
    import time
    import random
    
    # Generate different graph types
    def generate_graph(num_nodes, edge_probability=0.3):
        graph = {}
        for i in range(num_nodes):
            graph[i] = []
            for j in range(num_nodes):
                if i != j and random.random() < edge_probability:
                    graph[i].append(j)
        return graph
    
    graph_sizes = [100, 1000, 5000]
    
    for size in graph_sizes:
        graph = generate_graph(size, 0.1)  # Sparse graph
        start_node = 0
        
        # Time BFS
        start_time = time.time()
        bfs(graph, start_node)
        bfs_time = time.time() - start_time
        
        # Time DFS
        start_time = time.time()
        dfs_iterative(graph, start_node)
        dfs_time = time.time() - start_time
        
        print(f"Graph size {size}: BFS={bfs_time:.4f}s, DFS={dfs_time:.4f}s")
```

## Space Complexity Analysis

### Detailed Breakdown

| Algorithm | Auxiliary Space | Total Space | Common Pitfalls |
|-----------|-----------------|-------------|-----------------|
| **BFS** | O(V) | O(V + E) | Queue can store all nodes in worst case |
| **DFS Iterative** | O(V) | O(V + E) | Stack depth, but usually less than BFS |
| **DFS Recursive** | O(V) | O(V + E) | Call stack overflow for deep graphs |

### Memory Usage Patterns
```python
def space_analysis():
    """
    Space Complexity Details:
    
    BFS:
    - Queue stores nodes at current level
    - Worst case: O(V) for complete graphs
    - Also needs visited set, parent dict: O(V)
    
    DFS Iterative:
    - Stack stores current path
    - Worst case: O(V) for linear graphs
    - Usually more memory efficient than BFS
    
    DFS Recursive:
    - Call stack depth = longest path
    - System limit (~1000 frames in Python)
    - Risk of stack overflow for deep graphs
    
    Graph Storage:
    - Adjacency list: O(V + E)
    - Adjacency matrix: O(V²)
    """
    
    # Example: Worst-case scenarios
    worst_case_bfs = "Complete graph - queue stores all nodes"
    worst_case_dfs = "Linear graph - stack stores all nodes"
    
    return {
        'bfs_worst_case': 'O(V)',
        'dfs_worst_case': 'O(V)', 
        'graph_storage': 'O(V + E) for adjacency list'
    }
```

## Correctness & Assumptions

### Input Validation & Preconditions
```python
def validated_bfs(graph, start):
    """BFS with comprehensive validation"""
    
    # PRECONDITIONS
    if not graph:
        raise ValueError("Graph cannot be empty")
    
    if start not in graph:
        raise ValueError(f"Start node {start} not in graph")
    
    if not isinstance(graph, (dict, Graph)):
        raise TypeError("Graph must be dict or Graph object")
    
    # Check for None nodes
    if start is None:
        raise ValueError("Start node cannot be None")
    
    # MAIN ALGORITHM
    visited = set([start])
    parent = {start: None}
    level = {start: 0}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        # Validate current node exists in graph
        if current not in graph:
            continue
            
        for neighbor in graph[current]:
            # Validate neighbor
            if neighbor is None:
                continue
                
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                level[neighbor] = level[current] + 1
                queue.append(neighbor)
    
    # POSTCONDITIONS
    assert start in visited, "Start node must be visited"
    assert all(level[node] >= 0 for node in visited), "All levels non-negative"
    
    return visited, parent, level
```

### Edge Cases Testing
```python
def test_traversal_edge_cases():
    """Comprehensive edge case testing for BFS/DFS"""
    
    test_cases = [
        # (graph, start, description)
        ({0: []}, 0, "Single node"),
        ({}, 0, "Empty graph - should error"),
        ({0: [1], 1: [0]}, 0, "Two nodes connected"),
        ({0: [1], 1: [2], 2: []}, 0, "Linear graph"),
        ({0: [1, 2], 1: [0, 2], 2: [0, 1]}, 0, "Triangle graph"),
        ({0: [1], 1: [2], 2: [0]}, 0, "Cycle"),
        ({0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}, 0, "Tree structure"),
    ]
    
    algorithms = [
        ('BFS', bfs),
        ('DFS Iterative', dfs_iterative),
        ('DFS Recursive', dfs_recursive)
    ]
    
    for graph, start, description in test_cases:
        print(f"\nTesting: {description}")
        
        for algo_name, algo_func in algorithms:
            try:
                if algo_name == 'DFS Recursive' and len(graph) > 100:
                    print(f"{algo_name:15}: Skipped (too large for recursion)")
                    continue
                    
                visited, parent, _ = algo_func(graph, start) if algo_name == 'BFS' else algo_func(graph, start)
                
                # Validate results
                assert start in visited, "Start node must be visited"
                if len(graph) > 0:
                    assert len(visited) <= len(graph), "Cannot visit more nodes than exist"
                
                print(f"{algo_name:15}: PASS - visited {len(visited)} nodes")
                
            except Exception as e:
                print(f"{algo_name:15}: FAIL - {e}")
```

## Practical Considerations

### Constant Factors & Optimization
```python
def optimized_bfs(graph, start, target=None):
    """
    Optimized BFS with early termination and bidirectional search
    """
    if target is not None and start == target:
        return [start]
    
    # Early termination BFS
    visited = set([start])
    parent = {start: None}
    queue = deque([start])
    
    while queue:
        current = queue.popleft()
        
        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                
                # Early termination if target found
                if neighbor == target:
                    # Reconstruct path
                    path = []
                    node = neighbor
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    return path[::-1]
    
    return None

def bidirectional_bfs(graph, start, target):
    """
    Bidirectional BFS - search from both ends
    """
    if start == target:
        return [start]
    
    # Forward search
    forward_visited = {start: None}
    forward_queue = deque([start])
    
    # Backward search  
    backward_visited = {target: None}
    backward_queue = deque([target])
    
    while forward_queue and backward_queue:
        # Expand forward search
        current_forward = forward_queue.popleft()
        for neighbor in graph.get(current_forward, []):
            if neighbor not in forward_visited:
                forward_visited[neighbor] = current_forward
                forward_queue.append(neighbor)
                
                # Check meeting point
                if neighbor in backward_visited:
                    return construct_bidirectional_path(neighbor, forward_visited, backward_visited)
        
        # Expand backward search
        current_backward = backward_queue.popleft()
        for neighbor in graph.get(current_backward, []):
            if neighbor not in backward_visited:
                backward_visited[neighbor] = current_backward
                backward_queue.append(neighbor)
                
                # Check meeting point
                if neighbor in forward_visited:
                    return construct_bidirectional_path(neighbor, forward_visited, backward_visited)
    
    return None

def construct_bidirectional_path(meeting_point, forward_parent, backward_parent):
    """Construct path from bidirectional search results"""
    # Build path from start to meeting point
    path_forward = []
    node = meeting_point
    while node is not None:
        path_forward.append(node)
        node = forward_parent[node]
    path_forward.reverse()
    
    # Build path from meeting point to target (excluding meeting point)
    path_backward = []
    node = backward_parent[meeting_point]
    while node is not None:
        path_backward.append(node)
        node = backward_parent[node]
    
    return path_forward + path_backward
```

### Cache Performance Analysis
```python
def cache_performance_analysis():
    """
    Cache Performance Characteristics:
    
    BFS Cache Behavior:
    - Queue operations: Good locality (sequential access)
    - Level-by-level: Nodes at same level often stored contiguously
    - Good for: Social networks, level-based queries
    
    DFS Cache Behavior:
    - Stack operations: Excellent locality
    - Depth exploration: May jump between memory locations
    - Good for: Maze solving, dependency resolution
    
    Memory Access Patterns:
    - BFS: More predictable, level-oriented
    - DFS: Less predictable, path-oriented
    - For large graphs: DFS often better cache performance
    
    Optimization Tips:
    - Use arrays instead of linked lists for adjacency
    - Pre-allocate memory when possible
    - Use iterative DFS for deep graphs to avoid stack overflow
    """
    pass
```

### Real-world Data Patterns
```python
def adaptive_traversal(graph, start, target=None, graph_type=None):
    """
    Choose traversal strategy based on graph characteristics
    """
    if graph_type is None:
        # Analyze graph properties
        num_nodes = len(graph)
        avg_degree = sum(len(neighbors) for neighbors in graph.values()) / num_nodes
        
        # Determine graph type
        if avg_degree < 2:
            graph_type = "sparse"
        elif avg_degree > num_nodes * 0.1:
            graph_type = "dense" 
        else:
            graph_type = "moderate"
    
    # Choose algorithm based on scenario
    if target is not None:
        # Path finding scenario
        if graph_type == "sparse" and abs(ord(str(start)[0]) - ord(str(target)[0])) < 3:
            return bidirectional_bfs(graph, start, target)
        else:
            return optimized_bfs(graph, start, target)
    
    else:
        # Exploration scenario
        if graph_type == "dense":
            return bfs(graph, start)  # BFS better for dense graphs
        else:
            return dfs_iterative(graph, start)  # DFS better for sparse graphs

def specialized_traversals():
    """
    Specialized versions for common scenarios
    """
    
    def bfs_level_order(graph, start):
        """BFS that returns nodes by level"""
        if start not in graph:
            return []
        
        levels = []
        visited = set([start])
        queue = deque([start])
        
        while queue:
            level_size = len(queue)
            current_level = []
            
            for _ in range(level_size):
                node = queue.popleft()
                current_level.append(node)
                
                for neighbor in graph.get(node, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            levels.append(current_level)
        
        return levels
    
    def dfs_topological(graph):
        """DFS for topological sorting (DAGs only)"""
        visited = set()
        stack = []
        
        def dfs(node):
            visited.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)
        
        for node in graph:
            if node not in visited:
                dfs(node)
        
        return stack[::-1]
    
    return bfs_level_order, dfs_topological
```

## Applications & Use Cases

### Problem-Specific Implementations
```python
def shortest_path_unweighted(graph, start, target):
    """Shortest path in unweighted graph (BFS)"""
    return bfs_path(graph, start, target)

def connected_components(graph):
    """Find connected components using BFS/DFS"""
    visited = set()
    components = []
    
    for node in graph:
        if node not in visited:
            # Use BFS to find component
            component_visited, _, _ = bfs(graph, node)
            visited.update(component_visited)
            components.append(list(component_visited))
    
    return components

def cycle_detection_directed(graph):
    """Cycle detection in directed graphs using DFS"""
    visited = set()
    recursion_stack = set()
    
    def has_cycle(node):
        visited.add(node)
        recursion_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if has_cycle(neighbor):
                    return True
            elif neighbor in recursion_stack:
                return True
        
        recursion_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if has_cycle(node):
                return True
    
    return False
```

## Key Takeaways

### When to Use Which Algorithm

| Scenario | Recommended Algorithm | Reason |
|----------|---------------------|---------|
| **Shortest path (unweighted)** | BFS | Guaranteed shortest path |
| **Memory constraints** | DFS Iterative | Lower memory usage |
| **Deep graphs** | DFS Iterative | Avoids recursion limits |
| **Wide, shallow graphs** | BFS | More efficient |
| **Cycle detection** | DFS | Natural for depth exploration |
| **Topological sort** | DFS | Natural ordering |
| **Bidirectional search** | Bidirectional BFS | Faster for known target |

### Performance Guidelines
1. **BFS**: Use when you need shortest paths or level-by-level processing
2. **DFS**: Use when memory is constrained or for deep graph exploration
3. **Bidirectional BFS**: Use when both start and target are known
4. **Iterative DFS**: Preferred over recursive for large graphs

### Best Practices
- **Validate inputs** - check for empty graphs, valid start nodes
- **Consider graph density** - sparse vs dense graphs
- **Watch for recursion limits** - use iterative DFS for large graphs
- **Use early termination** when target is known
- **Consider bidirectional search** for pathfinding problems