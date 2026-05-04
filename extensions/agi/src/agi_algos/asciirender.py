#!/usr/bin/env python3
"""
asciirender.py — ASCII art rendering for unified graph memory
DB-augmented directed code generation via unified graph memory
"""

from typing import List, Dict, Any, Optional, Tuple
from .graph_builder import GraphBuilder


class ASCIIRenderer:
    """Renders graph as ASCII art."""
    
    MAX_WIDTH = 200
    MAX_LINES = 200
    
    def __init__(self, builder: GraphBuilder):
        self.builder = builder
        # Nodes are tuples: (id, type, label, content, source)
        self._node_lookup = {n[0]: n for n in builder.nodes}
    
    def render_summary(self) -> str:
        """Render a summary view of the graph."""
        lines = []
        lines.append(" UNIFIED GRAPH ")
        lines.append("=" * 60)
        
        stats = self.builder.get_stats()
        lines.append(f" nodes={stats['node_count']}  edges={stats['edge_count']}")
        lines.append("-" * 60)
        
        # Show nodes by type
        for node_type, count in sorted(stats['nodes_by_type'].items()):
            type_label = node_type.replace('_', ' ').title()
            lines.append(f" {type_label}: {count}")
        
        return '\n'.join(lines)
    
    def render_tree(self, max_depth: int = 2, root_id: Optional[str] = None) -> str:
        """Render graph as ASCII tree starting from root."""
        if not self.builder.nodes:
            return "(empty graph)"
        
        lines = []
        lines.append(" GRAPH TREE ")
        lines.append("=" * 60)
        
        # Default root — nodes are tuples (id, type, label, content, source)
        if root_id is None:
            section_nodes = [n for n in self.builder.nodes if n[1] == "doc_section"]
            if section_nodes:
                root_id = section_nodes[0][0]
            else:
                root_id = self.builder.nodes[0][0]
        
        visited = set()
        self._render_node_tree(root_id, "", True, lines, visited, max_depth, 0)
        
        return '\n'.join(lines)
    
    def _render_node_tree(self, node_id: str, prefix: str, is_last: bool,
                          lines: List[str], visited: set, max_depth: int, current_depth: int):
        """Recursively render a node and its children."""
        if node_id in visited or current_depth > max_depth:
            return
        visited.add(node_id)
        
        node = self._node_lookup.get(node_id)
        if not node:
            return
        
        connector = "└─ " if is_last else "├─ "
        label = node[2][:50]
        node_type = node[1][:15]
        lines.append(f"{prefix}{connector}[{node_type}] {label}")
        
        # Get children
        new_prefix = prefix + ("   " if is_last else "│  ")
        
        # Find direct children (outgoing edges)
        children = [e["to"] for e in self.builder.edges 
                   if e["from"] == node_id and e["type"] == "contains"]
        
        for i, child_id in enumerate(children[:5]):
            self._render_node_tree(
                child_id, new_prefix, i == len(children) - 1,
                lines, visited, max_depth, current_depth + 1
            )
    
    def render_hierarchy(self, max_sections: int = 10) -> str:
        """Render top-level sections with their children."""
        lines = []
        lines.append(" GRAPH HIERARCHY ")
        lines.append("=" * 60)
        
        section_nodes = [n for n in self.builder.nodes if n[1] == "doc_section"]
        
        for i, node in enumerate(section_nodes[:max_sections]):
            indent = "  " if i > 0 else ""
            is_last = i == min(len(section_nodes) - 1, max_sections - 1)
            
            label = node[2][:50]
            
            # Get children
            children = [e["to"] for e in self.builder.edges 
                       if e["from"] == node[0] and e["type"] == "contains"]
            
            child_labels = []
            for c in children[:3]:
                cn = self._node_lookup.get(c)
                if cn:
                    child_labels.append(cn[2][:20])
            
            child_str = f" → {', '.join(child_labels)}" if child_labels else ""
            connector = "└─" if is_last else "├─"
            
            lines.append(f"{indent}{connector} {label}{child_str}")
        
        if len(section_nodes) > max_sections:
            lines.append(f"  ... +{len(section_nodes) - max_sections} more sections")
        
        return '\n'.join(lines)
    
    def render_path(self, path: List[str]) -> str:
        """Render a path through the graph."""
        lines = []
        lines.append(" PATH ")
        lines.append("=" * 60)
        
        for i, node_id in enumerate(path):
            node = self._node_lookup.get(node_id)
            if not node:
                continue
            
            connector = "→" if i > 0 else "●"
            label = node[2][:50]
            lines.append(f"{connector} {label}")
        
        return '\n'.join(lines)
    
    def render_node_detail(self, node_id: str) -> str:
        """Render detailed view of a single node."""
        node = self._node_lookup.get(node_id)
        if not node:
            return f"Node not found: {node_id}"
        
        lines = []
        lines.append(f" NODE: {node[2]} ")
        lines.append("=" * 60)
        lines.append(f" ID:     {node[0]}")
        lines.append(f" Type:   {node[1]}")
        lines.append(f" Source: {node[4]}")
        lines.append("-" * 60)
        lines.append(" Content:")
        lines.append(node[3] or '(none)')
        lines.append("-" * 60)
        
        # Show neighbors
        neighbors = list(self.builder.adj.get(node_id, []))
        lines.append(f" Neighbors ({len(neighbors)}):")
        for n in neighbors[:5]:
            nn = self._node_lookup.get(n)
            if nn:
                lines.append(f"  - {nn[1]}: {nn[2][:40]}")
        
        return '\n'.join(lines)
    
    def render_stats(self) -> str:
        """Render graph statistics."""
        stats = self.builder.get_stats()
        
        lines = []
        lines.append(" GRAPH STATS ")
        lines.append("=" * 60)
        lines.append(f" Total Nodes:    {stats['node_count']}")
        lines.append(f" Total Edges:    {stats['edge_count']}")
        lines.append(f" Unique IDs:     {stats['node_ids']}")
        lines.append("-" * 60)
        lines.append(" Nodes by Type:")
        
        for node_type, count in sorted(stats['nodes_by_type'].items(), key=lambda x: -x[1]):
            type_label = node_type.replace('_', ' ').title()
            bar = "█" * min(count, 40)
            lines.append(f" {type_label:20s} {count:4d} {bar}")
        
        return '\n'.join(lines)
    
    def render_full(self, path: Optional[List[str]] = None) -> str:
        """Render full ASCII representation of the graph."""
        sections = []
        
        sections.append(self.render_summary())
        sections.append("")
        sections.append(self.render_hierarchy())
        
        if path:
            sections.append("")
            sections.append(self.render_path(path))
        
        sections.append("")
        sections.append(self.render_stats())
        
        output = '\n'.join(sections)
        
        # Truncate if too long
        lines = output.split('\n')
        if len(lines) > self.MAX_LINES:
            lines = lines[:self.MAX_LINES]
            lines.append(f"... (truncated, {len(self.builder.nodes)} nodes total)")
        
        return '\n'.join(lines)


def render_to_string(builder: GraphBuilder, mode: str = "full", 
                     path: Optional[List[str]] = None) -> Tuple[str, int]:
    """Render graph to string. Returns (output, line_count)."""
    renderer = ASCIIRenderer(builder)
    
    if mode == "summary":
        output = renderer.render_summary()
    elif mode == "tree":
        output = renderer.render_tree()
    elif mode == "hierarchy":
        output = renderer.render_hierarchy()
    elif mode == "stats":
        output = renderer.render_stats()
    elif path:
        output = renderer.render_path(path)
    else:
        output = renderer.render_full(path)
    
    line_count = len(output.strip().split('\n'))
    return output, line_count


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from .graph_builder import build_graph
    
    hermes = os.path.expanduser("~/.hermes")
    agi = os.path.dirname(os.path.abspath(__file__))
    
    print("Building graph...")
    builder, build_time = build_graph(hermes, agi)
    print(f"Build: {build_time:.2f}ms")
    
    renderer = ASCIIRenderer(builder)
    print()
    print(renderer.render_full())
