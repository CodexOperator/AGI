#!/usr/bin/env python3
"""
pi_tree_adapter.py — Adapter to feed graph output into pi's /tree feature
DB-augmented directed code generation via unified graph memory
"""

import json
import os
import sys
from typing import List, Dict, Any, Optional

# Add parent directory for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .graph_builder import build_graph, GraphBuilder
from .asciirender import ASCIIRenderer


class PiTreeAdapter:
    """
    Adapter to convert graph data into pi's /tree format.
    
    pi's /tree feature expects a specific JSON structure:
    {
      "nodes": [
        {"id": "...", "label": "...", "children": [...]}
      ]
    }
    """
    
    def __init__(self, builder: GraphBuilder):
        self.builder = builder
        self._node_lookup = {n["id"]: n for n in builder.nodes}
    
    def to_pi_tree(self, root_id: Optional[str] = None, 
                   max_depth: int = 3) -> Dict[str, Any]:
        """Convert graph to pi's tree format."""
        if not self.builder.nodes:
            return {"nodes": [], "stats": {}}
        
        # Find root(s)
        if root_id is None:
            # Use doc_sections as roots
            section_nodes = [n for n in self.builder.nodes if n["type"] == "doc_section"]
            roots = section_nodes[:3] if section_nodes else [self.builder.nodes[0]]
        else:
            roots = [self._node_lookup[root_id]] if root_id in self._node_lookup else []
        
        nodes = []
        visited = set()
        
        for root in roots:
            tree = self._build_tree_recursive(root["id"], visited, max_depth, 0)
            nodes.append(tree)
        
        return {
            "nodes": nodes,
            "stats": {
                "total_nodes": len(self.builder.nodes),
                "total_edges": len(self.builder.edges),
                "rendered_nodes": len(visited)
            }
        }
    
    def _build_tree_recursive(self, node_id: str, visited: set, 
                              max_depth: int, current_depth: int) -> Dict[str, Any]:
        """Recursively build tree structure."""
        if node_id in visited or current_depth > max_depth:
            return {"id": node_id, "label": "...", "collapsed": True}
        
        visited.add(node_id)
        node = self._node_lookup.get(node_id)
        
        if not node:
            return {"id": node_id, "label": "unknown"}
        
        children = []
        
        # Get child edges
        for edge in self.builder.edges:
            if edge["from"] == node_id and edge["type"] == "contains":
                child = self._build_tree_recursive(
                    edge["to"], visited, max_depth, current_depth + 1
                )
                children.append(child)
        
        result = {
            "id": node["id"],
            "label": node["label"][:50],
            "type": node["type"]
        }
        
        if children:
            result["children"] = children
        
        return result
    
    def to_pi_search_format(self, query: str) -> Dict[str, Any]:
        """Convert search results to pi format."""
        results = []
        
        query_lower = query.lower()
        for node in self.builder.nodes:
            score = 0
            if query_lower in node.get("label", "").lower():
                score += 2
            if query_lower in node.get("content", "").lower():
                score += 1
            
            if score > 0:
                results.append({
                    "id": node["id"],
                    "label": node["label"],
                    "type": node["type"],
                    "source": node["source"],
                    "score": score
                })
        
        results.sort(key=lambda x: -x["score"])
        
        return {
            "query": query,
            "results": results[:20],
            "total_matches": len(results)
        }
    
    def to_pi_path_format(self, path: List[str]) -> Dict[str, Any]:
        """Convert a path to pi's format."""
        nodes = []
        
        for node_id in path:
            node = self._node_lookup.get(node_id)
            if node:
                nodes.append({
                    "id": node["id"],
                    "label": node["label"],
                    "type": node["type"],
                    "content": node.get("content", "")[:100]
                })
        
        return {
            "path": nodes,
            "length": len(nodes),
            "formatted": self._format_path_ascii(path)
        }
    
    def _format_path_ascii(self, path: List[str]) -> str:
        """Format path as ASCII art."""
        lines = []
        
        for i, node_id in enumerate(path):
            node = self._node_lookup.get(node_id)
            if not node:
                continue
            
            if i == 0:
                lines.append(f"╭─ {node['label'][:50]}")
            elif i == len(path) - 1:
                lines.append(f"╰─ {node['label'][:50]}")
            else:
                lines.append(f"├─ {node['label'][:50]}")
        
        return '\n'.join(lines)
    
    def to_pi_subgraph(self, center_id: str, radius: int = 2) -> Dict[str, Any]:
        """Get subgraph around a center node for pi."""
        if center_id not in self._node_lookup:
            return {"error": f"Node not found: {center_id}"}
        
        # BFS to find reachable nodes
        reachable = {center_id}
        frontier = {center_id}
        
        for _ in range(radius):
            next_frontier = set()
            for node in frontier:
                for neighbor in self.builder.adj.get(node, []):
                    if neighbor not in reachable:
                        reachable.add(neighbor)
                        next_frontier.add(neighbor)
            frontier = next_frontier
        
        # Build subgraph
        nodes = [self._node_lookup[n] for n in reachable if n in self._node_lookup]
        edges = [e for e in self.builder.edges 
                if e["from"] in reachable and e["to"] in reachable]
        
        return {
            "center": center_id,
            "radius": radius,
            "nodes": nodes,
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges)
        }


def output_for_pi(builder: GraphBuilder, output_path: str):
    """Output graph in pi-compatible format."""
    adapter = PiTreeAdapter(builder)
    
    # Main tree
    tree = adapter.to_pi_tree()
    
    # Search format
    search = adapter.to_pi_search_format("agent")
    
    # Stats
    stats = builder.get_stats()
    
    output = {
        "tree": tree,
        "search": search,
        "stats": stats,
        "generated_at": __import__('time').time()
    }
    
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    hermes = os.path.expanduser("~/.hermes")
    agi = os.path.dirname(os.path.abspath(__file__))
    
    print("Building graph...")
    builder, build_time = build_graph(hermes, agi)
    print(f"Build: {build_time:.2f}ms")
    
    adapter = PiTreeAdapter(builder)
    
    # Output pi tree
    tree = adapter.to_pi_tree()
    print(f"\nPi tree: {len(tree['nodes'])} root nodes")
    print(json.dumps(tree, indent=2)[:500])
