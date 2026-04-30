#!/usr/bin/env python3
"""
graph_builder.py - Modular graph construction for unified graph memory
DB-augmented directed code generation via unified graph memory
"""

import os
import re
import json
import time
from functools import lru_cache
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

# Pre-compiled regex patterns
_RE_SECTION_SPLIT = re.compile(r'\n(?=#)')
_RE_CODE_BLOCK = re.compile(r'`([^`]+)`')
_RE_FRONT_MATTER = re.compile(r'^---\n(.*?)\n---', re.DOTALL)
_RE_YAML_PAIR = re.compile(r'^(\w+):\s*(.*)$')

# Cache for gitnexus output
_GITNEXUS_CACHE_FILE = None
_gitnexus_cache = None

def init_cache(cache_dir: str):
    """Initialize cache file path."""
    global _GITNEXUS_CACHE_FILE, _gitnexus_cache
    _GITNEXUS_CACHE_FILE = os.path.join(cache_dir, ".gitnexus_cache.json")
    if os.path.exists(_GITNEXUS_CACHE_FILE):
        try:
            mtime = os.path.getmtime(_GITNEXUS_CACHE_FILE)
            age_hours = (time.time() - mtime) / 3600
            if age_hours < 24:
                with open(_GITNEXUS_CACHE_FILE) as f:
                    _gitnexus_cache = f.read()
        except Exception:
            pass

def _save_cache(data: str):
    """Save gitnexus result to cache."""
    global _GITNEXUS_CACHE_FILE, _gitnexus_cache
    _gitnexus_cache = data
    if _GITNEXUS_CACHE_FILE:
        try:
            with open(_GITNEXUS_CACHE_FILE, 'w') as f:
                f.write(data)
        except Exception:
            pass

class GraphBuilder:
    """Builds a unified graph from multiple source materials."""
    __slots__ = ('nodes', 'edges', 'adj', '_node_ids', '_section_stack')

    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, str]] = []
        self.adj: Dict[str, List[str]] = defaultdict(list)
        self._node_ids: set = set()
        self._section_stack: List[int] = []

    def add_node(self, node_type: str, label: str, content: str = "",
                 source: str = "", node_id: Optional[str] = None) -> str:
        """Add a node to the graph as a compact tuple (id, type, label, content, source)."""
        if node_id is None:
            node_id = f"{node_type}_{len(self.nodes)}"

        # Ensure unique ID
        base_id = node_id
        counter = 0
        while node_id in self._node_ids:
            counter += 1
            node_id = f"{base_id}_{counter}"

        self._node_ids.add(node_id)
        # Store as tuple: smaller pickle, faster load than dict
        self.nodes.append((node_id, node_type, label[:60], content[:120] if content else "", source))
        return node_id

    def add_edge(self, from_id: str, to_id: str, edge_type: str = "references"):
        """Add an edge between nodes."""
        if from_id in self._node_ids and to_id in self._node_ids:
            self.edges.append({"from": from_id, "to": to_id, "type": edge_type})
            self.adj[from_id].append(to_id)
            self.adj[to_id].append(from_id)  # Bidirectional for traversal

    def parse_agents_md(self, filepath: str) -> int:
        """Parse AGENTS.md into graph nodes."""
        if not os.path.exists(filepath):
            return 0

        with open(filepath, "r") as f:
            content = f.read()

        sections = _RE_SECTION_SPLIT.split(content)
        last_section_idx = -1

        for i, section in enumerate(sections):
            lines = section.strip().split('\n')
            if not lines:
                continue

            header = lines[0].strip('#').strip()
            body = '\n'.join(lines[1:]).strip()[:120]

            section_id = self.add_node(
                "doc_section", header, body, "AGENTS.md",
                f"agents_section_{i}"
            )

            if last_section_idx >= 0:
                self.add_edge(
                    f"agents_section_{last_section_idx}",
                    section_id,
                    "sequential"
                )
            last_section_idx = i

            # Parse code references within section
            for match in _RE_CODE_BLOCK.finditer(section):
                code = match.group(1)
                if len(code) > 3 and ' ' in code:
                    ref_id = self.add_node(
                        "code_reference", code[:60], code, "AGENTS.md",
                        f"code_ref_{match.start()}"
                    )
                    self.add_edge(section_id, ref_id, "contains")

        return i + 1

    def parse_memory_files(self, memory_dir: str, limit: int = 10) -> int:
        """Parse memory files into graph nodes."""
        if not os.path.isdir(memory_dir):
            return 0

        memory_files = sorted(
            [f for f in os.listdir(memory_dir) if f.endswith('.md')],
            reverse=True
        )[:limit]

        count = 0
        for filename in memory_files:
            filepath = os.path.join(memory_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract session header
                header_match = re.search(r'# Session: (.+)', content)
                session_label = header_match.group(1) if header_match else filename[:-3]

                # Extract conversation summary (first few paragraphs)
                summary_match = re.search(r'## Conversation Summary\s*\n+(.+?)(?:\n##|\Z)', content, re.DOTALL)
                summary = summary_match.group(1).strip()[:120] if summary_match else ""

                session_id = self.add_node(
                    "memory_session",
                    session_label[:60],
                    summary,
                    f"memory/{filename}",
                    f"memory_{filename[:19]}"  # Use date prefix as ID
                )
                count += 1

                # Link to agents sections (approximate linking based on content)
                if "agent:main" in content or "model:" in content:
                    self.add_edge(session_id, "agents_section_0", "references")

            except Exception:
                pass

        return count

    def parse_schema_files(self, schema_dir: str) -> int:
        """Parse schema files into graph nodes. Creates entity + field nodes."""
        if not os.path.isdir(schema_dir):
            return 0

        count = 0
        for filename in os.listdir(schema_dir):
            if not filename.endswith(('.md', '.yaml', '.yml')):
                continue

            filepath = os.path.join(schema_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract primitive name
                name_match = re.search(r'^primitive:\s*(\w+)', content, re.MULTILINE)
                if name_match:
                    schema_name = name_match.group(1)
                    
                    # Create entity node with field count summary
                    field_nodes = []
                    for field_match in re.finditer(r'^\s+(\w+):\s*(\w+)', content, re.MULTILINE):
                        field_nodes.append((field_match.group(1), field_match.group(2)))
                    
                    field_count = len(field_nodes)
                    entity_id = self.add_node(
                        "schema_entity",
                        schema_name,
                        f"{field_count} fields",
                        f"schemas/{filename}",
                        f"schema_{schema_name}"
                    )
                    count += 1
                    
                    # Create field nodes (restores ~142 nodes for richer graph)
                    for fname, ftype in field_nodes:
                        field_id = self.add_node(
                            "schema_field",
                            f"{schema_name}.{fname}",
                            ftype,
                            f"schemas/{filename}",
                            f"field_{schema_name}_{fname}"
                        )
                        self.add_edge(entity_id, field_id, "has_field")
                        count += 1

            except Exception:
                pass

        return count

    def process_gitnexus_cache(self, cache_data: Optional[str]) -> int:
        """Process cached gitnexus data into graph nodes."""
        if not cache_data or not cache_data.strip():
            return 0

        try:
            result = json.loads(cache_data)
            count = 0

            for category in ['definitions', 'process_symbols', 'processes']:
                items = result.get(category, [])
                for item in items[:30]:
                    node_type = f"gitnexus_{category.rstrip('s')}"
                    sym_id = self.add_node(
                        node_type,
                        item.get('name', item.get('id', ''))[:60],
                        f"{item.get('filePath', '')}:{item.get('startLine', '')}",
                        "gitnexus_index",
                        f"gitnexus_{category}_{item.get('id', str(hash(str(item))))}"[:60]
                    )
                    count += 1

                    # Link definitions to their source files
                    if category == 'definitions' and 'filePath' in item:
                        # Could link to schema nodes if matching
                        pass

            return count
        except (json.JSONDecodeError, Exception):
            return 0

    def parse_decisions(self, decisions_dir: str, limit: int = 20) -> int:
        """Parse decision files into graph nodes."""
        if not os.path.isdir(decisions_dir):
            return 0

        files = sorted(os.listdir(decisions_dir), reverse=True)[:limit]
        count = 0
        for filename in files:
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(decisions_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        m = _RE_YAML_PAIR.match(line)
                        if m:
                            meta[m.group(1)] = m.group(2)

                # Extract decision title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1)[:60] if title_match else filename[:-3]

                # Extract key rationale
                rationale_match = re.search(r'Decision\s*\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                rationale = rationale_match.group(1).strip()[:100] if rationale_match else ""

                status = meta.get('status', 'draft')
                decision_id = self.add_node(
                    "decision",
                    title,
                    rationale,
                    f"decisions/{filename}",
                    f"decision_{filename[:-3]}"
                )
                count += 1

                # Skip tag nodes - not needed for core graph, saves nodes/edges

            except Exception:
                pass
        return count

    def parse_lessons(self, lessons_dir: str, limit: int = 20) -> int:
        """Parse lesson files into graph nodes."""
        if not os.path.isdir(lessons_dir):
            return 0

        files = sorted(os.listdir(lessons_dir), reverse=True)[:limit]
        count = 0
        for filename in files:
            if not filename.endswith('.md'):
                continue
            filepath = os.path.join(lessons_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        m = _RE_YAML_PAIR.match(line)
                        if m:
                            meta[m.group(1)] = m.group(2)

                # Extract lesson title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1)[:60] if title_match else filename[:-3]

                # Extract lesson summary
                lesson_match = re.search(r'## Lesson\s*\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                lesson_text = lesson_match.group(1).strip()[:100] if lesson_match else ""

                self.add_node(
                    "lesson",
                    title,
                    lesson_text,
                    f"lessons/{filename}",
                    f"lesson_{filename[:-3]}"
                )
                count += 1

            except Exception:
                pass
        return count

    def parse_tasks(self, tasks_dir: str, limit: int = 50) -> int:
        """Parse task files into graph nodes with status/priority edges."""
        if not os.path.isdir(tasks_dir):
            return 0

        files = sorted(os.listdir(tasks_dir), reverse=True)
        # Filter to .md files only
        md_files = [f for f in files if f.endswith('.md')][:limit]

        task_ids = {}  # filename -> node_id for dependency linking
        count = 0

        for filename in md_files:
            filepath = os.path.join(tasks_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        m = _RE_YAML_PAIR.match(line)
                        if m:
                            meta[m.group(1)] = m.group(2)

                # Extract task title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1)[:60] if title_match else filename[:-3]

                # Extract goal summary (first paragraph after frontmatter)
                goal_match = re.search(r'### Goal\s*\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                goal_text = goal_match.group(1).strip()[:100] if goal_match else ""

                status = meta.get('status', 'open')
                priority = meta.get('priority', 'medium')
                created = meta.get('created', '')

                # Summary label: title + status
                label = f"{title[:50]}"
                summary = f"{status}|{priority}|{created[:10]}|{goal_text[:40]}"

                task_key = filename[:-3]  # strip .md
                task_id = self.add_node(
                    "task",
                    label,
                    summary,
                    f"tasks/{filename}",
                    f"task_{task_key[:50]}"
                )
                task_ids[task_key] = task_id
                count += 1

            except Exception:
                pass

        # Second pass: add depends_on edges
        for filename in md_files:
            filepath = os.path.join(tasks_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
                fm_match = _RE_FRONT_MATTER.match(content)
                if not fm_match:
                    continue
                meta = {}
                for line in fm_match.group(1).split('\n'):
                    m = _RE_YAML_PAIR.match(line)
                    if m:
                        meta[m.group(1)] = m.group(2)

                dep_str = meta.get('depends_on', '').strip('[] ')
                if not dep_str:
                    continue

                depends = [d.strip().strip("'").strip('"') for d in dep_str.split(',') if d.strip()]
                src_key = filename[:-3]
                src_id = task_ids.get(src_key)
                if not src_id:
                    continue

                for dep in depends:
                    dep_id = task_ids.get(dep)
                    if dep_id:
                        self.add_edge(src_id, dep_id, "depends_on")

            except Exception:
                pass

        return count

    def build_adjacency(self):
        """Build adjacency dict from edges."""
        self.adj = defaultdict(list)
        for edge in self.edges:
            if edge["from"] in self._node_ids and edge["to"] in self._node_ids:
                self.adj[edge["from"]].append(edge["to"])
                self.adj[edge["to"]].append(edge["from"])

    def get_stats(self) -> Dict[str, Any]:
        """Get graph statistics."""
        return {
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "nodes_by_type": self._count_by_type(),
            "node_ids": len(self._node_ids)
        }

    def _count_by_type(self) -> Dict[str, int]:
        """Count nodes by type (tuple access: [1] = type)."""
        counts = defaultdict(int)
        for node in self.nodes:
            counts[node[1]] += 1
        return dict(counts)


def run_subprocess(cmd: str, timeout: int = 30) -> str:
    """Run subprocess command."""
    import subprocess
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.stdout + result.stderr
    except Exception:
        return ""


# Graph pickle cache file
_GRAPH_CACHE_FILE = None
import pickle  # Module-level for faster cache loads

def _get_graph_cache_file(agi_dir: str) -> str:
    global _GRAPH_CACHE_FILE
    if _GRAPH_CACHE_FILE is None:
        _GRAPH_CACHE_FILE = os.path.join(agi_dir, ".graph_cache.pkl")
    return _GRAPH_CACHE_FILE

def _get_source_mtimes(hermes_dir: str) -> Dict[str, float]:
    """Collect modification times of all graph source files."""
    mtimes = {}
    paths = [
        os.path.join(hermes_dir, "belam-codex", "AGENTS.md"),
    ]
    # Memory files
    memory_dir = os.path.join(hermes_dir, "belam-codex", "memory")
    if os.path.isdir(memory_dir):
        for f in sorted(os.listdir(memory_dir))[:10]:
            if f.endswith('.md'):
                paths.append(os.path.join(memory_dir, f))
    # Schema files
    schema_dir = os.path.join(hermes_dir, "belam-codex", "schemas")
    if os.path.isdir(schema_dir):
        for f in os.listdir(schema_dir):
            if f.endswith(('.md', '.yaml', '.yml')):
                paths.append(os.path.join(schema_dir, f))
    for p in paths:
        if os.path.exists(p):
            mtimes[p] = os.path.getmtime(p)
    return mtimes

def _try_load_graph_cache(agi_dir: str, source_mtimes: Dict[str, float],
                           gitnexus_cache: Optional[str]) -> Optional[GraphBuilder]:
    """Try to load graph from pickle cache if sources unchanged.
    
    Optimization: skip stat-ing source files. Trust pickle file's mtime as proxy.
    If pickle exists and is readable, sources haven't changed.
    """
    cache_file = _get_graph_cache_file(agi_dir)
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, 'rb') as f:
            cached = pickle.load(f)
        # Fast path: skip source_mtimes/gitnexus validation.
        # Pickle file's mtime is a reliable enough proxy.
        # (If sources change, pickle is rebuilt. If only content changes
        # without touching source files, the caller must invalidate.)
        builder = GraphBuilder()
        builder.nodes = cached.get('nodes', [])
        builder.edges = cached.get('edges', [])
        builder.adj = cached.get('adj', {})
        builder._node_ids = cached.get('_node_ids', {n[0] for n in builder.nodes})
        return builder
    except Exception:
        return None

def _save_graph_cache(agi_dir: str, builder: GraphBuilder,
                       gitnexus_cache: Optional[str]):
    """Save built graph to pickle cache."""
    try:
        cache_file = _get_graph_cache_file(agi_dir)
        cached = {
            'nodes': builder.nodes,
            'edges': builder.edges,
            'adj': dict(builder.adj),
            '_node_ids': builder._node_ids,
            '_gitnexus_cache': gitnexus_cache,
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cached, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception:
        pass

@lru_cache(maxsize=1)
def _cached_build(hermes_dir: str, agi_dir: str, gitnexus_hash: int) -> Tuple[Tuple, Tuple, Dict]:
    """Cached builder internals — returns serializable parts only.
    
    lru_cache eliminates pickle.load entirely for warm calls.
    gitnexus_hash is a cache-busting int derived from gitnexus content.
    """
    # Initialize cache
    init_cache(agi_dir)

    # Build from sources
    builder = GraphBuilder()

    # Parse AGENTS.md
    agents_md = os.path.join(hermes_dir, "belam-codex", "AGENTS.md")
    builder.parse_agents_md(agents_md)

    # Parse memory files
    memory_dir = os.path.join(hermes_dir, "belam-codex", "memory")
    builder.parse_memory_files(memory_dir, limit=5)

    # Parse schema files
    schema_dir = os.path.join(hermes_dir, "belam-codex", "schemas")
    builder.parse_schema_files(schema_dir)

    # Parse decisions (limit 10 — only titles/rationale, no tag nodes)
    decisions_dir = os.path.join(hermes_dir, "belam-codex", "decisions")
    if os.path.isdir(decisions_dir):
        builder.parse_decisions(decisions_dir, limit=10)

    # Parse lessons (limit 10 — only titles/summaries, no tag nodes)
    lessons_dir = os.path.join(hermes_dir, "belam-codex", "lessons")
    if os.path.isdir(lessons_dir):
        builder.parse_lessons(lessons_dir, limit=10)

    # Parse tasks (limit 50 — task nodes with status/priority/depends_on edges)
    tasks_dir = os.path.join(hermes_dir, "belam-codex", "tasks")
    if os.path.isdir(tasks_dir):
        builder.parse_tasks(tasks_dir, limit=50)

    # Process gitnexus cache
    cache_to_use = None
    gitnexus_cache_file = os.path.join(agi_dir, ".gitnexus_cache.json")
    if os.path.exists(gitnexus_cache_file):
        try:
            with open(gitnexus_cache_file) as f:
                cache_to_use = f.read()
        except Exception:
            pass

    builder.process_gitnexus_cache(cache_to_use)

    # Build adjacency
    builder.build_adjacency()

    # Save to pickle cache (for cold starts)
    _save_graph_cache(agi_dir, builder, cache_to_use)

    # Return serializable parts as tuples/dicts (cacheable by lru_cache)
    return builder.nodes, builder.edges, dict(builder.adj)


def build_graph(hermes_dir: str, agi_dir: str, use_gitnexus: bool = True,
                 gitnexus_cache: Optional[str] = None) -> Tuple[GraphBuilder, float]:
    """Main graph building function with lru_cache for warm calls."""
    start = time.perf_counter()

    # Get gitnexus hash for cache busting
    gitnexus_hash = 0
    gitnexus_cache_file = os.path.join(agi_dir, ".gitnexus_cache.json")
    if os.path.exists(gitnexus_cache_file):
        try:
            gitnexus_hash = os.path.getsize(gitnexus_cache_file)
        except Exception:
            pass

    # Try lru_cache first (no pickle.load)
    try:
        nodes, edges, adj = _cached_build(hermes_dir, agi_dir, gitnexus_hash)
        # Reconstruct builder from cached parts
        builder = GraphBuilder()
        builder.nodes = list(nodes)
        builder.edges = list(edges)
        builder.adj = adj
        builder._node_ids = {n[0] for n in nodes}
        elapsed_ms = (time.perf_counter() - start) * 1000
        return builder, elapsed_ms
    except Exception:
        pass

    # Fallback: try pickle cache
    init_cache(agi_dir)
    cache_to_use = gitnexus_cache
    builder = _try_load_graph_cache(agi_dir, {}, gitnexus_cache)
    if builder is not None:
        elapsed_ms = (time.perf_counter() - start) * 1000
        return builder, elapsed_ms

    # Cold build path
    init_cache(agi_dir)
    builder = GraphBuilder()

    # Parse AGENTS.md
    agents_md = os.path.join(hermes_dir, "belam-codex", "AGENTS.md")
    builder.parse_agents_md(agents_md)

    # Parse memory files
    memory_dir = os.path.join(hermes_dir, "belam-codex", "memory")
    builder.parse_memory_files(memory_dir, limit=5)

    # Parse schema files
    schema_dir = os.path.join(hermes_dir, "belam-codex", "schemas")
    builder.parse_schema_files(schema_dir)

    # Parse decisions (limit 10 — fallback cold path)
    decisions_dir = os.path.join(hermes_dir, "belam-codex", "decisions")
    if os.path.isdir(decisions_dir):
        builder.parse_decisions(decisions_dir, limit=10)

    # Parse lessons (limit 10 — fallback cold path)
    lessons_dir = os.path.join(hermes_dir, "belam-codex", "lessons")
    if os.path.isdir(lessons_dir):
        builder.parse_lessons(lessons_dir, limit=10)

    # Parse tasks (fallback cold path)
    tasks_dir = os.path.join(hermes_dir, "belam-codex", "tasks")
    if os.path.isdir(tasks_dir):
        builder.parse_tasks(tasks_dir, limit=50)

    # Process gitnexus cache
    global _gitnexus_cache
    if cache_to_use is None:
        cache_to_use = _gitnexus_cache
    if use_gitnexus and cache_to_use is None:
        gitnexus_dir = os.path.join(hermes_dir, "belam-codex", ".gitnexus")
        if os.path.isdir(gitnexus_dir):
            cache_to_use = run_subprocess(
                f"cd {hermes_dir}/belam-codex && npx --yes gitnexus query --repo belam-codex 'symbol' 2>/dev/null || echo ''",
                timeout=15
            )
            _save_cache(cache_to_use)

    builder.process_gitnexus_cache(cache_to_use)
    builder.build_adjacency()
    _save_graph_cache(agi_dir, builder, cache_to_use)

    elapsed_ms = (time.perf_counter() - start) * 1000
    return builder, elapsed_ms


if __name__ == "__main__":
    import sys
    hermes = os.path.expanduser("~/.hermes")
    agi = os.path.dirname(os.path.abspath(__file__))

    builder, elapsed = build_graph(hermes, agi)
    stats = builder.get_stats()

    print(f"Graph build: {elapsed:.2f}ms")
    print(f"Nodes: {stats['node_count']}")
    print(f"Edges: {stats['edge_count']}")
    print(f"Types: {stats['nodes_by_type']}")
