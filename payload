#!/usr/bin/env python3
"""
query_engine.py — Path finding and graph traversal for unified graph memory
DB-augmented directed code generation via unified graph memory
"""

import json
import time
import heapq
from typing import List, Dict, Any, Optional, Tuple, Set
from collections import deque
from .graph_builder import GraphBuilder


class QueryEngine:
    """Query engine for graph traversal and path finding."""
    
    def __init__(self, builder: GraphBuilder):
        self.builder = builder
        self._cache: Dict[str, Any] = {}
    
    def find_path_bfs(self, start_id: str, end_id: str, 
                      max_depth: Optional[int] = None) -> Optional[List[str]]:
        """Find shortest path using BFS."""
        if start_id not in self.builder._node_ids or end_id not in self.builder._node_ids:
            return None
        
        # Dynamic max_depth based on node count if not specified
        if max_depth is None:
            max_depth = min(len(self.builder.nodes), 100)
        
        visited: Set[str] = {start_id}
        queue = deque([(start_id, [start_id])])
        
        while queue:
            current, path = queue.popleft()
            
            if current == end_id:
                return path
            
            if len(path) >= max_depth:
                continue
            
            for neighbor in self.builder.adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def find_path_dijkstra(self, start_id: str, end_id: str,
                           edge_weights: Optional[Dict[str, float]] = None) -> Tuple[Optional[List[str]], float]:
        """Find shortest path using Dijkstra's algorithm."""
        if start_id not in self.builder._node_ids or end_id not in self.builder._node_ids:
            return None, float('inf')
        
        if edge_weights is None:
            edge_weights = {}
        
        dist: Dict[str, float] = {start_id: 0}
        prev: Dict[str, Optional[str]] = {start_id: None}
        visited: Set[str] = set()
        pq = [(0, start_id)]
        
        while pq:
            current_dist, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            visited.add(current)
            
            if current == end_id:
                # Reconstruct path
                path = []
                node = end_id
                while node is not None:
                    path.append(node)
                    node = prev[node]
                return list(reversed(path)), dist[end_id]
            
            for neighbor in self.builder.adj.get(current, []):
                if neighbor in visited:
                    continue
                
                edge_key = f"{current}->{neighbor}"
                weight = edge_weights.get(edge_key, 1.0)
                new_dist = dist[current] + weight
                
                if neighbor not in dist or new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = current
                    heapq.heappush(pq, (new_dist, neighbor))
        
        return None, float('inf')
    
    def find_reachable(self, start_id: str, max_depth: int = 3) -> Set[str]:
        """Find all nodes reachable within max_depth hops."""
        if start_id not in self.builder._node_ids:
            return set()
        
        reachable: Set[str] = {start_id}
        frontier = {start_id}
        
        for _ in range(max_depth):
            next_frontier = set()
            for node in frontier:
                for neighbor in self.builder.adj.get(node, []):
                    if neighbor not in reachable:
                        reachable.add(neighbor)
                        next_frontier.add(neighbor)
            frontier = next_frontier
            if not frontier:
                break
        
        return reachable
    
    def find_common_neighbors(self, node1: str, node2: str) -> Set[str]:
        """Find nodes reachable from both node1 and node2."""
        neighbors1 = self.find_reachable(node1, max_depth=2)
        neighbors2 = self.find_reachable(node2, max_depth=2)
        return neighbors1 & neighbors2 - {node1, node2}
    
    def get_subgraph(self, center_id: str, depth: int = 2) -> Dict[str, Any]:
        """Get subgraph centered on a node."""
        reachable = self.find_reachable(center_id, max_depth=depth)
        
        subgraph_nodes = [n for n in self.builder.nodes if n[0] in reachable]
        subgraph_edges = [e for e in self.builder.edges 
                          if e["from"] in reachable and e["to"] in reachable]
        
        return {
            "nodes": subgraph_nodes,
            "edges": subgraph_edges,
            "center": center_id,
            "node_count": len(subgraph_nodes),
            "edge_count": len(subgraph_edges)
        }
    
    def query_by_type(self, node_type: str) -> List[Dict[str, Any]]:
        """Get all nodes of a specific type."""
        return [n for n in self.builder.nodes if n[1] == node_type]
    
    def query_by_source(self, source: str) -> List[Dict[str, Any]]:
        """Get all nodes from a specific source."""
        return [n for n in self.builder.nodes if source in n[4]]
    
    def search_content(self, query: str, limit: int = 10) -> List[Tuple[Dict[str, Any], int]]:
        """Search nodes by content (simple keyword match)."""
        query_lower = query.lower()
        results = []
        
        for node in self.builder.nodes:
            score = 0
            if query_lower in node[2].lower():
                score += 2
            if query_lower in node[3].lower():
                score += 1
            if score > 0:
                results.append((node, score))
        
        results.sort(key=lambda x: -x[1])
        return results[:limit]


def timed_query(engine: QueryEngine, start_id: str, end_id: str) -> Tuple[Optional[List[str]], float]:
    """Execute a query with timing."""
    start = time.perf_counter()
    path = engine.find_path_bfs(start_id, end_id)
    elapsed_ms = (time.perf_counter() - start) * 1000
    return path, elapsed_ms


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from .graph_builder import build_graph
    
    hermes = os.path.expanduser("~/.hermes")
    agi = os.path.dirname(os.path.abspath(__file__))
    
    print("Building graph...")
    builder, build_time = build_graph(hermes, agi)
    print(f"Build: {build_time:.2f}ms, {len(builder.nodes)} nodes, {len(builder.edges)} edges")
    
    engine = QueryEngine(builder)
    
    # Find path between first and last section
    section_nodes = [n for n in builder.nodes if n[0].startswith("agents_section_")]
    if len(section_nodes) >= 2:
        path, query_time = timed_query(
            engine, 
            section_nodes[0][0], 
            section_nodes[-1][0]
        )
        print(f"Path query: {query_time:.2f}ms")
        if path:
            print(f"Path length: {len(path)} hops")
