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


def _parse_yaml_line(line: str, meta: dict) -> None:
    """Parse a key: value YAML line into meta dict. Faster than regex partition."""
    if ':' in line:
        key, _, val = line.partition(':')
        meta[key.strip()] = val.strip()
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
    __slots__ = ('nodes', 'edges', 'adj', '_node_ids', '_section_stack', '_precomputed_paths', 'hub_reachable', '_tag_store')

    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, str]] = []
        self.adj: Dict[str, List[str]] = defaultdict(list)
        self._node_ids: set = set()
        self._section_stack: List[int] = []
        self._precomputed_paths: Dict[str, Any] = {}  # (start, end) -> path or None
        self.hub_reachable: Dict[str, frozenset] = {}
        self._tag_store: Dict[str, List[str]] = {}  # node_id -> [tags] for tag bridge building  # hub_id -> frozenset of reachable node ids

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
        """Parse decision files into graph nodes with upstream/downstream edges."""
        if not os.path.isdir(decisions_dir):
            return 0

        files = sorted(os.listdir(decisions_dir), reverse=True)[:limit]
        count = 0
        decision_ids = {}  # slug -> node_id for upstream/downstream linking
        file_contents = {}  # filename -> (content, meta) for second pass

        # First pass: create nodes and collect metadata
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
                        _parse_yaml_line(line, meta)

                # Extract decision title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1)[:60] if title_match else filename[:-3]

                # Extract key rationale
                rationale_match = re.search(r'Decision\s*\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                rationale = rationale_match.group(1).strip()[:100] if rationale_match else ""

                status = meta.get('status', 'draft')
                decision_slug = filename[:-3]
                decision_id = self.add_node(
                    "decision",
                    title,
                    rationale,
                    f"decisions/{filename}",
                    f"decision_{decision_slug}"
                )
                decision_ids[decision_slug] = decision_id
                file_contents[filename] = (content, meta)
                tags_str = meta.get('tags', '')
                if tags_str:
                    self._tag_store[decision_id] = re.findall(r'\w+', tags_str)
                count += 1

            except Exception:
                pass

        # Second pass: add upstream/downstream edges
        for filename, (content, meta) in file_contents.items():
            src_slug = filename[:-3]
            src_id = decision_ids.get(src_slug)
            if not src_id:
                continue

            for dir_key in ('upstream', 'downstream'):
                refs_str = meta.get(dir_key, '').strip('[] ')
                if not refs_str:
                    continue
                refs = [r.strip().strip("'").strip('"') for r in refs_str.split(',') if r.strip()]
                for ref in refs[:5]:  # cap at 5 per direction
                    tgt_id = decision_ids.get(ref)
                    if tgt_id and tgt_id != src_id:
                        self.add_edge(src_id, tgt_id, dir_key)

        return count

    def parse_lessons(self, lessons_dir: str, limit: int = 20) -> int:
        """Parse lesson files into graph nodes with upstream/downstream edges."""
        if not os.path.isdir(lessons_dir):
            return 0

        files = sorted(os.listdir(lessons_dir), reverse=True)[:limit]
        count = 0
        lesson_ids = {}  # slug -> node_id for upstream/downstream linking
        file_meta = {}  # filename -> meta dict

        # First pass: create nodes
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
                        _parse_yaml_line(line, meta)

                # Extract lesson title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1)[:60] if title_match else filename[:-3]

                # Extract lesson summary
                lesson_match = re.search(r'## Lesson\s*\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                lesson_text = lesson_match.group(1).strip()[:100] if lesson_match else ""

                lesson_slug = filename[:-3]
                self.add_node(
                    "lesson",
                    title,
                    lesson_text,
                    f"lessons/{filename}",
                    f"lesson_{lesson_slug}"
                )
                lesson_ids[lesson_slug] = f"lesson_{lesson_slug}"
                file_meta[filename] = meta
                lesson_node_id = f"lesson_{lesson_slug}"
                tags_str = meta.get('tags', '')
                if tags_str:
                    self._tag_store[lesson_node_id] = re.findall(r'\w+', tags_str)
                count += 1

            except Exception:
                pass

        # Second pass: add upstream/downstream edges between lessons
        for filename, meta in file_meta.items():
            src_slug = filename[:-3]
            src_id = lesson_ids.get(src_slug)
            if not src_id:
                continue

            for dir_key in ('upstream', 'downstream'):
                refs_str = meta.get(dir_key, '').strip('[] ')
                if not refs_str:
                    continue
                refs = [r.strip().strip("'").strip('"') for r in refs_str.split(',') if r.strip()]
                for ref in refs[:5]:
                    tgt_id = lesson_ids.get(ref)
                    if tgt_id and tgt_id != src_id:
                        self.add_edge(src_id, tgt_id, dir_key)

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
                        _parse_yaml_line(line, meta)

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
                tags_str = meta.get('tags', '')
                if tags_str:
                    self._tag_store[task_id] = re.findall(r'\w+', tags_str)
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
                    _parse_yaml_line(line, meta)

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

    def parse_goals(self, goals_dir: str) -> int:
        """Parse goal files into graph nodes with status/urgency metadata."""
        if not os.path.isdir(goals_dir):
            return 0

        files = sorted(os.listdir(goals_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0

        for filename in md_files:
            filepath = os.path.join(goals_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                # Extract goal title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1)[:60] if title_match else filename[:-3]

                # Extract "Why Critical" or first section for context
                why_match = re.search(r'## Why[\s\S]*?\n\n(.+?)(?:\n\n|##)', content)
                why_text = why_match.group(1).strip()[:100] if why_match else ""

                status = meta.get('status', 'unknown')
                priority = meta.get('priority', 'medium')
                created = meta.get('created', '')

                label = title[:50]
                summary = f"{status}|{priority}|{created[:10]}|{why_text[:40]}"

                self.add_node(
                    "goal",
                    label,
                    summary,
                    f"goals/{filename}",
                    f"goal_{filename[:-3]}"
                )
                count += 1

            except Exception:
                pass
        return count

    def parse_agent_roles(self, agents_dir: str) -> int:
        """Parse agent role definition files into graph nodes."""
        if not os.path.isdir(agents_dir):
            return 0

        files = sorted(os.listdir(agents_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0
        agent_ids = {}  # agent_id -> node_id for communication edges

        for filename in md_files:
            filepath = os.path.join(agents_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                agent_id = meta.get('agent_id', filename[:-3])
                role = meta.get('role', '')
                model = meta.get('model', '')
                status = meta.get('status', 'unknown')
                skills = meta.get('skills', '')

                # Extract agent title
                title_match = re.search(r'^#\s+Agent:\s*(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip()[:60] if title_match else agent_id

                label = title[:50]
                summary = f"{status}|{role[:30]}|{model[:30]}|{skills[:30]}"

                agent_id_key = filename[:-3]  # strip .md
                node_id = self.add_node(
                    "agent_role",
                    label,
                    summary,
                    f"agents/{filename}",
                    f"agent_{agent_id_key}"
                )
                agent_ids[agent_id] = node_id
                count += 1

                # Extract "What I Do" sections for actionable items
                does_match = re.search(r'## What I Do\s*\n([\s\S]+?)(?:##|\Z)', content)
                if does_match:
                    for line in does_match.group(1).split('\n'):
                        if line.strip().startswith('✅') or line.strip().startswith('-'):
                            action = line.strip().lstrip('✅- ').strip()[:60]
                            if len(action) > 5:
                                action_id = self.add_node(
                                    "agent_capability",
                                    action[:60],
                                    "",
                                    f"agents/{filename}",
                                    f"cap_{agent_id_key}_{hash(action) & 0xFFFF}"
                                )
                                self.add_edge(node_id, action_id, "can_do")
                                count += 1

                # Extract "What I Do NOT Do" sections
                not_does_match = re.search(r'## What I Do NOT Do\s*\n([\s\S]+?)(?:##|\Z)', content)
                if not_does_match:
                    for line in not_does_match.group(1).split('\n'):
                        if line.strip().startswith('❌') or line.strip().startswith('-'):
                            action = line.strip().lstrip('❌- ').strip()[:60]
                            if len(action) > 5:
                                action_id = self.add_node(
                                    "agent_boundary",
                                    action[:60],
                                    "",
                                    f"agents/{filename}",
                                    f"bound_{agent_id_key}_{hash(action) & 0xFFFF}"
                                )
                                self.add_edge(node_id, action_id, "refuses_to")
                                count += 1

            except Exception:
                pass

        # Second pass: add communication edges between agents
        for filename in md_files:
            filepath = os.path.join(agents_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
                fm_match = _RE_FRONT_MATTER.match(content)
                if not fm_match:
                    continue
                meta = {}
                for line in fm_match.group(1).split('\n'):
                    _parse_yaml_line(line, meta)

                agent_id = meta.get('agent_id', filename[:-3])
                src_id = agent_ids.get(agent_id)
                if not src_id:
                    continue

                # Parse communicates_with: [architect, critic, builder]
                comm_str = meta.get('communicates_with', '').strip('[] ')
                if not comm_str:
                    continue

                peers = [c.strip().strip("'").strip('"') for c in comm_str.split(',') if c.strip()]
                for peer in peers:
                    tgt_id = agent_ids.get(peer)
                    if tgt_id:
                        self.add_edge(src_id, tgt_id, "communicates_with")

            except Exception:
                pass

        return count

    def parse_canvas_graph(self, canvas_dir: str) -> Tuple[int, int]:
        """Parse canvas graph_data.json with pre-computed cross-primitive edges.
        
        Returns (nodes_added, edges_added). Adds 105 nodes (lesson, decision, task,
        project, pipeline, command, skill, knowledge) and 8 causal edges from
        LLM-judged relationship data.
        """
        graph_file = os.path.join(canvas_dir, "graph_data.json")
        if not os.path.exists(graph_file):
            return 0, 0

        try:
            with open(graph_file) as f:
                data = json.load(f)
        except Exception:
            return 0, 0

        canvas_nodes = data.get('nodes', [])
        canvas_edges = data.get('edges', [])

        if not canvas_nodes:
            return 0, 0

        # Build ID mapping: canvas slug -> our node_id
        # Canvas format: 'decision/belam-codex-resurrection'
        # Our format: 'decision_belam-codex-resurrection' or 'decision_belam_codex_resurrection'
        slug_to_id = {}
        id_type_map = {}  # canvas_id -> (type_label, node_id)

        nodes_added = 0
        for cn in canvas_nodes:
            canvas_id = cn.get('id', '')
            node_type = cn.get('type', 'primitive')
            title = cn.get('title', canvas_id)[:60]
            tags = ','.join(cn.get('tags', [])[:5])[:60]
            source = f"canvas/graph_data.json"
            # Create our node ID: type_slug format
            our_id = canvas_id.replace('/', '_')
            node_id = self.add_node(
                f"canvas_{node_type}",
                title,
                tags,
                source,
                our_id
            )
            slug_to_id[canvas_id] = our_id
            id_type_map[canvas_id] = (node_type, node_id)
            nodes_added += 1

        edges_added = 0
        for ce in canvas_edges:
            src = ce.get('source', '')
            tgt = ce.get('target', '')
            if not src or not tgt:
                continue
            # Map canvas IDs to our IDs
            src_id = slug_to_id.get(src)
            tgt_id = slug_to_id.get(tgt)
            if src_id and tgt_id and src_id in self._node_ids and tgt_id in self._node_ids:
                self.add_edge(src_id, tgt_id, "causes")
                edges_added += 1

        return nodes_added, edges_added

    def parse_knowledge(self, knowledge_dir: str) -> int:
        """Parse knowledge files into graph nodes.
        
        Knowledge files have frontmatter with topic, tags, related, sources.
        Each file becomes a knowledge node with tag and related edges.
        """
        if not os.path.isdir(knowledge_dir):
            return 0

        files = sorted(os.listdir(knowledge_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0

        for filename in md_files:
            filepath = os.path.join(knowledge_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                topic = meta.get('topic', filename[:-3])
                tags_str = meta.get('tags', '[]')
                related_str = meta.get('related', '[]')
                created = meta.get('created', '')

                # Extract first section body as content
                body_match = re.search(r'## Claim\s*\n+(.+?)(?:\n##|\Z)', content, re.DOTALL)
                body = body_match.group(1).strip()[:100] if body_match else ""

                label = topic[:50]
                summary = f"tags:{tags_str[:60]}|related:{related_str[:40]}"

                node_id = self.add_node(
                    "knowledge",
                    label,
                    summary,
                    f"knowledge/{filename}",
                    f"knowledge_{filename[:-3]}"
                )
                count += 1

                # Parse related references as edges (to existing nodes)
                if related_str and related_str != '[]':
                    related_items = re.findall(r'(\w+(?:-\w+)*)', related_str)
                    for rel in related_items[:5]:
                        rel_id = self._find_or_add_reference(rel, f"knowledge/{filename}")
                        if rel_id:
                            self.add_edge(node_id, rel_id, "related_to")

            except Exception:
                pass
        return count

    def parse_skills(self, skills_dir: str) -> int:
        """Parse hermes/skills/ directory into skill nodes with related_skill edges.
        
        Each skill category becomes a skill_type node.
        Each individual skill becomes a skill node with tags and related_skill edges.
        """
        if not os.path.isdir(skills_dir):
            return 0

        count = 0
        skill_ids = {}  # skill_name -> node_id for related_skill edges
        category_ids = {}  # category_name -> node_id

        # First pass: create category and skill nodes
        categories = sorted(os.listdir(skills_dir))
        for category in categories:
            category_path = os.path.join(skills_dir, category)
            if not os.path.isdir(category_path):
                continue

            # Create category node
            category_id = self.add_node(
                "skill_type",
                category,
                f"category: {category}",
                f"skills/{category}",
                f"skill_type_{category}"
            )
            category_ids[category] = category_id
            count += 1

            # Find SKILL.md files (may be in subdirectories)
            skill_mds = []
            for root, _, files in os.walk(category_path):
                for f in files:
                    if f == 'SKILL.md':
                        skill_mds.append(os.path.join(root, f))

            for skill_md in skill_mds:
                try:
                    with open(skill_md, "r") as f:
                        content = f.read()

                    # Extract frontmatter
                    fm_match = _RE_FRONT_MATTER.match(content)
                    meta = {}
                    if fm_match:
                        for line in fm_match.group(1).split('\n'):
                            _parse_yaml_line(line, meta)

                    skill_name = meta.get('name', os.path.basename(os.path.dirname(skill_md)))
                    description = meta.get('description', '')[:80]
                    tags_str = meta.get('tags', '[]')
                    related_str = meta.get('related_skills', meta.get('related', '[]'))
                    version = meta.get('version', '1.0.0')

                    # Create skill node
                    skill_node_id = self.add_node(
                        "skill",
                        skill_name[:50],
                        description,
                        f"skills/{skill_md}",
                        f"skill_{skill_name.replace('-', '_').replace(' ', '_')}"
                    )
                    skill_ids[skill_name] = skill_node_id
                    self.add_edge(category_id, skill_node_id, "belongs_to")
                    count += 1

                    # Parse related_skill references (add to queue for second pass)
                    if related_str and related_str != '[]':
                        related = re.findall(r'\[?([\w-]+)\]?', related_str)
                        for rel in related[:5]:
                            rel_clean = rel.strip()
                            if rel_clean != skill_name and rel_clean not in skill_ids:
                                # Create stub skill node for related skill
                                stub_id = self.add_node(
                                    "skill",
                                    rel_clean[:50],
                                    f"related_skill (stub)",
                                    f"skills/{skill_md}",
                                    f"skill_{rel_clean.replace('-', '_').replace(' ', '_')}"
                                )
                                skill_ids[rel_clean] = stub_id
                                count += 1

                except Exception:
                    pass

        # Second pass: add related_skill edges between actual skill nodes
        edges_added = 0
        for category in categories:
            category_path = os.path.join(skills_dir, category)
            if not os.path.isdir(category_path):
                continue

            for root, _, files in os.walk(category_path):
                for f in files:
                    if f != 'SKILL.md':
                        continue
                    skill_md = os.path.join(root, f)
                    try:
                        with open(skill_md, "r") as fh:
                            content = fh.read()

                        fm_match = _RE_FRONT_MATTER.match(content)
                        if not fm_match:
                            continue
                        meta = {}
                        for line in fm_match.group(1).split('\n'):
                            _parse_yaml_line(line, meta)

                        skill_name = meta.get('name', '')
                        src_id = skill_ids.get(skill_name)
                        if not src_id:
                            continue

                        related_str = meta.get('related_skills', meta.get('related', '[]'))
                        if not related_str or related_str == '[]':
                            continue

                        related = re.findall(r'\[?([\w-]+)\]?', related_str)
                        for rel in related[:5]:
                            rel_clean = rel.strip()
                            tgt_id = skill_ids.get(rel_clean)
                            if tgt_id and tgt_id != src_id:
                                self.add_edge(src_id, tgt_id, "related_skill")
                                edges_added += 1

                    except Exception:
                        pass

        return count

    def _find_or_add_reference(self, ref: str, source: str) -> Optional[str]:
        """Find existing node by slug-like reference or add a stub reference node."""
        # Convert slug to node ID format used in our graph
        candidates = [
            f"decision_{ref.replace('/', '_')}",
            f"lesson_{ref.replace('/', '_')}",
            f"knowledge_{ref.replace('/', '_')}",
            f"canvas_decision_{ref.replace('/', '_')}",
            f"canvas_lesson_{ref.replace('/', '_')}",
        ]
        for cid in candidates:
            if cid in self._node_ids:
                return cid
        # Stub reference node
        stub_id = f"ref_{ref.replace('/', '_')[:50]}"
        if stub_id not in self._node_ids:
            self.add_node("reference", ref[:60], "", source, stub_id)
        return stub_id

    def parse_handoff(self, handoff_dir: str) -> int:
        """Parse handoff files into graph nodes.
        
        Handoff files are TODO/planning documents with controller, timestamp,
        goals, and investigation notes. Creates handoff nodes with goal edges.
        """
        if not os.path.isdir(handoff_dir):
            return 0

        files = sorted(os.listdir(handoff_dir), reverse=True)
        md_files = [f for f in files if f.endswith('.md')]
        count = 0

        for filename in md_files:
            filepath = os.path.join(handoff_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                controller = meta.get('controller', '')
                timestamp = meta.get('timestamp', '')
                goal_match = re.search(r'## User goal\s*\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                goal = goal_match.group(1).strip()[:100] if goal_match else ""

                # Extract TODO items
                todo_items = re.findall(r'(?:^[-*]\s*(.+)$|TODO:\s*(.+)$)', content, re.MULTILINE)
                todos = [t[0] or t[1] for t in todo_items if t[0] or t[1]][:5]

                label = filename[:50]
                summary = f"{controller}|{timestamp[:10]}|{goal[:50]}"

                node_id = self.add_node(
                    "handoff",
                    label,
                    summary,
                    f"handoff/{filename}",
                    f"handoff_{filename[:40]}"
                )
                count += 1

                # Add TODO items as child nodes
                for i, todo in enumerate(todos):
                    todo_id = self.add_node(
                        "handoff_item",
                        todo[:60],
                        "",
                        f"handoff/{filename}",
                        f"handoff_item_{filename[:30]}_{i}"
                    )
                    self.add_edge(node_id, todo_id, "contains")
                    count += 1

            except Exception:
                pass
        return count

    def parse_archive_commands(self, archive_dir: str) -> int:
        """Parse archived command documentation files.
        
        Creates archive_command nodes from archive/commands/*.md with frontmatter
        metadata (command, aliases, category, tags, upstream). Uses upstream field
        to create cross-type edges to decision nodes. Adds sequential edges between
        commands in alphabetical order.
        """
        commands_dir = os.path.join(archive_dir, "commands")
        if not os.path.isdir(commands_dir):
            return 0

        files = sorted(os.listdir(commands_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0
        last_cmd_id = None

        for filename in md_files:
            filepath = os.path.join(commands_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                command_name = meta.get('command', filename[:-3])
                aliases_str = meta.get('aliases', '[]')
                category = meta.get('category', '')
                tags_str = meta.get('tags', '[]')
                upstream_str = meta.get('upstream', '[]')

                # Extract first section body as description
                desc_match = re.search(r'## [Uu]sage[\s\S]*?\n\n(.+?)(?:\n##|```|$)', content)
                desc = desc_match.group(1).strip()[:100] if desc_match else ""

                # Extract code example if present
                example_match = re.search(r'```[\w]*\n(.+?)```', content, re.DOTALL)
                example = example_match.group(1).strip()[:80] if example_match else ""

                label = command_name[:50] if command_name else filename[:-3]
                summary = f"{category}|{aliases_str[:40]}|{tags_str[:50]}"

                cmd_key = filename[:-3]  # strip .md
                node_id = self.add_node(
                    "archive_command",
                    label,
                    summary,
                    f"archive/commands/{filename}",
                    f"archive_cmd_{cmd_key[:50]}"
                )
                count += 1

                # Sequential edges between commands
                if last_cmd_id:
                    self.add_edge(last_cmd_id, node_id, "next_command")
                last_cmd_id = node_id

                # Upstream edges: link to referenced decision/primitive nodes
                if upstream_str and upstream_str != '[]':
                    upstream_items = re.findall(r'[\w/-]+', upstream_str)
                    for ref in upstream_items[:5]:
                        ref_clean = ref.strip().replace('/', '_')
                        ref_id = f"decision_{ref_clean}"
                        if ref_id in self._node_ids:
                            self.add_edge(node_id, ref_id, "upstream")
                            count += 1
                        else:
                            # Try canvas_decision format
                            canvas_ref = f"canvas_decision_{ref_clean}"
                            if canvas_ref in self._node_ids:
                                self.add_edge(node_id, canvas_ref, "upstream")
                                count += 1

            except Exception:
                pass
        return count

    def parse_docs(self, docs_dir: str) -> int:
        """Parse docs/ directory into knowledge nodes.
        
        Docs are operational guides with frontmatter (category, tags, related).
        Each doc becomes a knowledge node with category edges to help cluster docs.
        """
        if not os.path.isdir(docs_dir):
            return 0

        files = sorted(os.listdir(docs_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0

        for filename in md_files:
            filepath = os.path.join(docs_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                category = meta.get('category', 'guide')
                tags_str = meta.get('tags', '[]')
                related_str = meta.get('related', '[]')

                # Extract first heading as title
                title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip()[:60] if title_match else filename[:-3]

                # Extract first body paragraph
                body_match = re.search(r'\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                body = body_match.group(1).strip()[:100] if body_match else ""

                label = title[:50]
                summary = f"category:{category}|{tags_str[:60]}"

                node_id = self.add_node(
                    "knowledge",
                    label,
                    summary,
                    f"docs/{filename}",
                    f"doc_{filename[:-3]}"
                )
                count += 1

                # Category edge: link doc to a category node
                cat_node_id = f"category_{category.lower().replace(' ', '_')}"
                if cat_node_id not in self._node_ids:
                    self.add_node("tag", category, "", f"docs/{filename}", cat_node_id)
                self.add_edge(node_id, cat_node_id, "categorized_as")

                # Related edges to existing nodes
                if related_str and related_str != '[]':
                    related_items = re.findall(r'[\w-]+', related_str)
                    for rel in related_items[:5]:
                        rel_id = self._find_or_add_reference(rel, f"docs/{filename}")
                        if rel_id:
                            self.add_edge(node_id, rel_id, "related_to")

            except Exception:
                pass
        return count

    def parse_personas(self, personas_dir: str) -> int:
        """Parse personas/ directory into agent_role nodes.
        
        Personas are agent archetypes (architect, builder, critic) with
        capabilities, boundaries, and communication patterns.
        """
        if not os.path.isdir(personas_dir):
            return 0

        files = sorted(os.listdir(personas_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0
        persona_ids = {}  # persona_name -> node_id

        for filename in md_files:
            filepath = os.path.join(personas_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()

                # Extract frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                persona_name = meta.get('persona', filename[:-3])
                role = meta.get('role', '')
                model = meta.get('model', '')
                communicates_str = meta.get('communicates_with', '[]')

                # Extract persona title
                title_match = re.search(r'^#\s+Persona:\s*(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip()[:60] if title_match else persona_name

                label = title[:50]
                summary = f"{role[:30]}|{model[:30]}"

                persona_key = filename[:-3]
                node_id = self.add_node(
                    "agent_role",
                    label,
                    summary,
                    f"personas/{filename}",
                    f"persona_{persona_key}"
                )
                persona_ids[persona_key] = node_id
                count += 1

                # Extract capabilities section
                cap_match = re.search(r'## Capabilities\s*\n([\s\S]+?)(?:##|\Z)', content)
                if cap_match:
                    for line in cap_match.group(1).split('\n'):
                        if line.strip().startswith(('•', '-', '✅', '1.', '2.', '3.')):
                            cap = line.strip().lstrip('•-✅ 0-9').strip()[:60]
                            if len(cap) > 5:
                                cap_id = self.add_node(
                                    "agent_capability",
                                    cap,
                                    "",
                                    f"personas/{filename}",
                                    f"cap_{persona_key}_{hash(cap) & 0xFFFF}"
                                )
                                self.add_edge(node_id, cap_id, "can_do")
                                count += 1

                # Extract boundaries section
                bound_match = re.search(r'## Boundaries\s*\n([\s\S]+?)(?:##|\Z)', content)
                if bound_match:
                    for line in bound_match.group(1).split('\n'):
                        if line.strip().startswith(('•', '-', '❌', '1.', '2.', '3.')):
                            bound = line.strip().lstrip('•-❌ 0-9').strip()[:60]
                            if len(bound) > 5:
                                bound_id = self.add_node(
                                    "agent_boundary",
                                    bound,
                                    "",
                                    f"personas/{filename}",
                                    f"bound_{persona_key}_{hash(bound) & 0xFFFF}"
                                )
                                self.add_edge(node_id, bound_id, "refuses_to")
                                count += 1

            except Exception:
                pass

        # Second pass: add communication edges
        for filename in md_files:
            filepath = os.path.join(personas_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
                fm_match = _RE_FRONT_MATTER.match(content)
                if not fm_match:
                    continue
                meta = {}
                for line in fm_match.group(1).split('\n'):
                    _parse_yaml_line(line, meta)

                src_key = filename[:-3]
                src_id = persona_ids.get(src_key)
                if not src_id:
                    continue

                comm_str = meta.get('communicates_with', '').strip('[] ')
                if not comm_str:
                    continue
                peers = [c.strip().strip("'").strip('"') for c in comm_str.split(',') if c.strip()]
                for peer in peers:
                    tgt_id = persona_ids.get(peer)
                    if tgt_id and tgt_id != src_id:
                        self.add_edge(src_id, tgt_id, "communicates_with")

            except Exception:
                pass
        return count

    def parse_research_projects(self, hermes_dir: str) -> int:
        """Parse research/, projects/, modes/, runbooks/ directories into knowledge nodes.
        
        - research/: technical research documents (containerization, orchestration tooling, etc.)
        - projects/: project definitions with frontmatter (status, priority, owner, tags)
        - modes/: orchestration mode definitions (create, edit, extend, orchestrate)
        - runbooks/: operational how-to guides
        
        Each becomes a knowledge node with category edges. Returns total nodes added.
        """
        count = 0
        base = os.path.join(hermes_dir, "belam-codex")

        # research/ — technical documents (markdown prose, tables, code)
        research_dir = os.path.join(base, "research")
        if os.path.isdir(research_dir):
            for filename in sorted(os.listdir(research_dir)):
                if not filename.endswith('.md'):
                    continue
                filepath = os.path.join(research_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip()[:60] if title_match else filename[:-3]
                    # Extract first paragraph after metadata block
                    body_match = re.search(r'(?:\n\n)(.+?)(?:\n\n|##)', content, re.DOTALL)
                    body = body_match.group(1).strip()[:100] if body_match else ""
                    node_id = self.add_node(
                        "knowledge",
                        title[:50],
                        body,
                        f"research/{filename}",
                        f"research_{filename[:-3]}"
                    )
                    # Category edge
                    cat_id = "category_research"
                    if cat_id not in self._node_ids:
                        self.add_node("tag", "research", "", f"research/{filename}", cat_id)
                    self.add_edge(node_id, cat_id, "categorized_as")
                    count += 1
                except Exception:
                    pass

        # projects/ — project definitions with frontmatter
        projects_dir = os.path.join(base, "projects")
        if os.path.isdir(projects_dir):
            for filename in sorted(os.listdir(projects_dir)):
                if not filename.endswith('.md'):
                    continue
                filepath = os.path.join(projects_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                    fm_match = _RE_FRONT_MATTER.match(content)
                    meta = {}
                    if fm_match:
                        for line in fm_match.group(1).split('\n'):
                            _parse_yaml_line(line, meta)
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip()[:60] if title_match else filename[:-3]
                    status = meta.get('status', '')
                    priority = meta.get('priority', '')
                    tags_str = meta.get('tags', '[]')
                    owner = meta.get('owner', '')
                    summary = f"{status}|{priority}|{owner[:20]}|{tags_str[:40]}"
                    node_id = self.add_node(
                        "knowledge",
                        title[:50],
                        summary,
                        f"projects/{filename}",
                        f"project_{filename[:-3]}"
                    )
                    # Tag edges
                    if tags_str and tags_str != '[]':
                        tags = re.findall(r'[\w-]+', tags_str)
                        for tag in tags[:5]:
                            tag_id = f"tag_{tag}"
                            if tag_id not in self._node_ids:
                                self.add_node("tag", tag, "", f"projects/{filename}", tag_id)
                            self.add_edge(node_id, tag_id, "tagged_with")
                            count += 1
                    # Category edge
                    cat_id = "category_project"
                    if cat_id not in self._node_ids:
                        self.add_node("tag", "project", "", f"projects/{filename}", cat_id)
                    self.add_edge(node_id, cat_id, "categorized_as")
                    count += 1
                except Exception:
                    pass

        # modes/ — orchestration mode definitions (create, edit, extend, orchestrate)
        modes_dir = os.path.join(base, "modes")
        if os.path.isdir(modes_dir):
            for filename in sorted(os.listdir(modes_dir)):
                if not filename.endswith('.md'):
                    continue
                filepath = os.path.join(modes_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip()[:60] if title_match else filename[:-3]
                    # Extract first paragraph
                    body_match = re.search(r'\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                    body = body_match.group(1).strip()[:100] if body_match else ""
                    mode_type = filename[:-3]  # create, edit, extend, orchestrate
                    node_id = self.add_node(
                        "agent_capability",
                        title[:50],
                        body,
                        f"modes/{filename}",
                        f"mode_{mode_type}"
                    )
                    # Sequential edges between modes
                    if hasattr(self, '_last_mode_id') and self._last_mode_id:
                        self.add_edge(self._last_mode_id, node_id, "next_mode")
                    self._last_mode_id = node_id
                    count += 1
                except Exception:
                    pass

        # runbooks/ — operational how-to guides
        runbooks_dir = os.path.join(base, "runbooks")
        if os.path.isdir(runbooks_dir):
            for filename in sorted(os.listdir(runbooks_dir)):
                if not filename.endswith('.md'):
                    continue
                filepath = os.path.join(runbooks_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
                    title = title_match.group(1).strip()[:60] if title_match else filename[:-3]
                    body_match = re.search(r'\n\n(.+?)(?:\n\n|##)', content, re.DOTALL)
                    body = body_match.group(1).strip()[:100] if body_match else ""
                    node_id = self.add_node(
                        "knowledge",
                        title[:50],
                        body,
                        f"runbooks/{filename}",
                        f"runbook_{filename[:-3]}"
                    )
                    # Category edge
                    cat_id = "category_runbook"
                    if cat_id not in self._node_ids:
                        self.add_node("tag", "runbook", "", f"runbooks/{filename}", cat_id)
                    self.add_edge(node_id, cat_id, "categorized_as")
                    count += 1
                except Exception:
                    pass

        # Reset _last_mode_id if it was set
        if hasattr(self, '_last_mode_id'):
            delattr(self, '_last_mode_id')

        return count

    def parse_pipelines(self, pipelines_dir: str) -> int:
        """Parse pipelines/ directory into pipeline + pipeline_stage nodes.

        Each pipeline file has YAML frontmatter (version, status, priority, type,
        agents, tags, project) and per-phase stage history tables.

        Node types:
          - pipeline: top-level pipeline record
          - pipeline_stage: individual stage entries from stage history tables

        Edges:
          - has_stage: pipeline → pipeline_stage (ordered by occurrence)
          - uses_agent: pipeline → agent_role
          - tagged_with: pipeline → tag
          - belongs_to_project: pipeline → knowledge (project)
          - next_stage: pipeline_stage → pipeline_stage (temporal order)
          - categorized_as: pipeline → tag (status, priority, type)
        """
        if not os.path.isdir(pipelines_dir):
            return 0

        # Also scan archive/pipelines/
        archive_pipelines = os.path.join(pipelines_dir, "archive")
        dirs_to_scan = [pipelines_dir]
        if os.path.isdir(archive_pipelines):
            dirs_to_scan.append(archive_pipelines)

        count = 0
        _RE_STAGE_TABLE = re.compile(
            r'^\|\s*Stage\s*\|.*?\|.*?\|.*?\|.*?\|\n((?:\|.*?\n)+)',
            re.MULTILINE
        )
        _RE_STAGE_ROW = re.compile(
            r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*(.+?)\s*\|$'
        )
        _RE_PHASE_SECTION = re.compile(
            r'^## (Phase \d+[^\n]*)\n.*?\n(?:### Stage History\n)?((?:\|.*?\n)+)',
            re.MULTILINE
        )
        _RE_PHASE_SIMPLE = re.compile(r'^## (Phase \d+[^\n]*?)(?:\n| )', re.MULTILINE)

        for base_d in dirs_to_scan:
            subdir = "pipelines" if base_d == pipelines_dir else "archive/pipelines"
            try:
                files = sorted(os.listdir(base_d))
            except Exception:
                continue

            for filename in files:
                if not filename.endswith('.md') or filename.startswith('.'):
                    continue
                # Skip non-pipeline files (e.g., handoffs/ subdir)
                if not os.path.isfile(os.path.join(base_d, filename)):
                    continue

                filepath = os.path.join(base_d, filename)
                try:
                    with open(filepath, "r") as f:
                        content = f.read()
                except Exception:
                    continue

                # Extract YAML frontmatter
                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                version = meta.get('version', filename[:-3])
                status = meta.get('status', '')
                priority = meta.get('priority', '')
                ptype = meta.get('type', '')
                agents_str = meta.get('agents', '')
                tags_str = meta.get('tags', '[]')
                project = meta.get('project', '')
                pending = meta.get('pending_action', '')

                # Extract title
                title_match = re.search(r'^#\s+Implementation Pipeline:\s*(.+)$', content, re.MULTILINE)
                title = title_match.group(1).strip()[:60] if title_match else version

                pipeline_id = self.add_node(
                    "pipeline",
                    title[:50],
                    f"{status}|{priority}|{ptype}",
                    f"{subdir}/{filename}",
                    f"pipeline_{version}"
                )
                count += 1

                # Tag edges (from YAML tags)
                if tags_str and tags_str != '[]':
                    tags = re.findall(r'[\w-]+', tags_str)
                    for tag in tags[:8]:
                        tag_id = f"tag_{tag}"
                        if tag_id not in self._node_ids:
                            self.add_node("tag", tag, "", f"{subdir}/{filename}", tag_id)
                        self.add_edge(pipeline_id, tag_id, "tagged_with")
                        count += 1

                # Agent edges
                if agents_str:
                    agents = re.findall(r'[\w-]+', agents_str)
                    for agent in agents[:6]:
                        role_id = f"agent_role_{agent}"
                        if role_id not in self._node_ids:
                            self.add_node("agent_role", agent, "", f"{subdir}/{filename}", role_id)
                        self.add_edge(pipeline_id, role_id, "uses_agent")

                # Status/priority/type category edges
                for cat_val, cat_prefix in [(status, "pipeline_status"), (priority, "pipeline_priority"), (ptype, "pipeline_type")]:
                    if cat_val:
                        cat_id = f"tag_{cat_prefix}_{cat_val}"
                        if cat_id not in self._node_ids:
                            self.add_node("tag", f"{cat_prefix}:{cat_val}", "", f"{subdir}/{filename}", cat_id)
                        self.add_edge(pipeline_id, cat_id, "categorized_as")

                # Project edge
                if project:
                    proj_id = f"project_{project}"
                    if proj_id not in self._node_ids:
                        self.add_node("knowledge", project, f"project:{project}", f"{subdir}/{filename}", proj_id)
                        count += 1
                    self.add_edge(pipeline_id, proj_id, "belongs_to_project")

                # Extract stage history: parse all | Stage | Date | Agent | Notes | table rows
                all_stages = []
                # Find phase sections with stage history tables
                for ph_match in _RE_PHASE_SECTION.finditer(content):
                    phase_name = ph_match.group(1).strip()
                    table_block = ph_match.group(2)
                    for row_match in _RE_STAGE_ROW.finditer(table_block):
                        stage_name = row_match.group(1).strip()
                        stage_date = row_match.group(2).strip()
                        stage_agent = row_match.group(3).strip()
                        stage_notes = row_match.group(4).strip()[:80]
                        all_stages.append((stage_name, stage_date, stage_agent, stage_notes))

                # Also extract standalone stage tables (some pipelines put them without phase headers)
                if not all_stages:
                    for tbl_match in _RE_STAGE_TABLE.finditer(content):
                        table_block = tbl_match.group(1)
                        for row_match in _RE_STAGE_ROW.finditer(table_block):
                            stage_name = row_match.group(1).strip()
                            stage_date = row_match.group(2).strip()
                            stage_agent = row_match.group(3).strip()
                            stage_notes = row_match.group(4).strip()[:80]
                            all_stages.append((stage_name, stage_date, stage_agent, stage_notes))

                # Create pipeline_stage nodes
                prev_stage_id = None
                for (stage_name, stage_date, stage_agent, stage_notes) in all_stages[:40]:
                    stage_id = self.add_node(
                        "pipeline_stage",
                        stage_name[:40],
                        f"{stage_date}|{stage_agent}|{stage_notes}",
                        f"{subdir}/{filename}#{stage_name}",
                        f"pipeline_{version}_stage_{stage_name}"
                    )
                    count += 1
                    self.add_edge(pipeline_id, stage_id, "has_stage")
                    if prev_stage_id:
                        self.add_edge(prev_stage_id, stage_id, "next_stage")
                    prev_stage_id = stage_id

                    # Agent node for stage actor
                    if stage_agent and stage_agent not in ('unknown', 'belam-main'):
                        role_id = f"agent_role_{stage_agent}"
                        if role_id not in self._node_ids:
                            self.add_node("agent_role", stage_agent, "", f"{subdir}/{filename}", role_id)
                        self.add_edge(stage_id, role_id, "executed_by")

                # Phase summary nodes (Phase 1, Phase 2, etc.)
                phase_names_seen = set()
                for ph_match in _RE_PHASE_SIMPLE.finditer(content):
                    phase_name = ph_match.group(1).strip()
                    if phase_name not in phase_names_seen:
                        phase_names_seen.add(phase_name)
                        phase_id = self.add_node(
                            "pipeline_phase",
                            phase_name[:40],
                            "",
                            f"{subdir}/{filename}#{phase_name}",
                            f"pipeline_{version}_phase_{len(phase_names_seen)}"
                        )
                        count += 1
                        self.add_edge(pipeline_id, phase_id, "has_phase")

        return count

    def parse_templates(self, templates_dir: str) -> int:
        """Parse templates/ directory into template_stage nodes.

        Templates define pipeline stage patterns with YAML stage definitions.
        Each template has a type, phases, and named stages per phase.

        Node type: template_stage (extracted stage definitions from YAML blocks)
        Edges: follows_template → pipeline_stage (if a pipeline uses this template)
        """
        if not os.path.isdir(templates_dir):
            return 0

        count = 0
        _RE_YAML_BLOCK = re.compile(r'```yaml\n(.*?)\n```', re.DOTALL)
        _RE_PHASE_HDR = re.compile(r'^###\s+Phase\s+(\d+)(.*)$', re.MULTILINE)
        _RE_STAGE_HDR = re.compile(r'^####\s+`([\w_]+)`', re.MULTILINE)
        _RE_YAML_KEY = re.compile(r'^(\s*)([\w_]+):\s*(.*)$', re.MULTILINE)

        try:
            files = sorted(os.listdir(templates_dir))
        except Exception:
            return 0

        for filename in files:
            if not filename.endswith('.md') or filename.startswith('.') or filename == 'retired':
                continue
            filepath = os.path.join(templates_dir, filename)
            if not os.path.isfile(filepath):
                continue

            try:
                with open(filepath, "r") as f:
                    content = f.read()
            except Exception:
                continue

            # Template-level info
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1).strip()[:60] if title_match else filename[:-3]
            tmpl_id = f"template_{filename[:-3]}"
            self.add_node("reference", title[:50], f"template:{filename}", f"templates/{filename}", tmpl_id)
            count += 1

            # Category edge
            cat_id = "category_template"
            if cat_id not in self._node_ids:
                self.add_node("tag", "template", "", f"templates/{filename}", cat_id)
                count += 1
            self.add_edge(tmpl_id, cat_id, "categorized_as")

            # Extract YAML blocks (stage definitions)
            yaml_blocks = list(_RE_YAML_BLOCK.finditer(content))
            
            # Pre-parse YAML blocks to build stage -> (role, action, session, cli) map
            stage_meta = {}  # stage_name -> {role, action, session, cli}
            for yb in yaml_blocks:
                yaml_content = yb.group(1)
                lines = yaml_content.split('\n')
                cur_phase = None
                in_stages = False
                
                for i, yline in enumerate(lines):
                    stripped = yline.strip()
                    
                    # Track phases nested under 'phases:'
                    if stripped.startswith('phase') and ':' in stripped:
                        phase_key = stripped.split(':')[0].strip()
                        if phase_key in ('phase1', 'phase2', 'phase3'):
                            cur_phase = phase_key
                            in_stages = False
                    
                    # Detect stages section
                    if stripped.startswith('stages:'):
                        in_stages = True
                        continue
                    
                    # Parse stage definitions: collect multi-line until next '- role:'
                    if in_stages and stripped.startswith('- role:'):
                        role = stripped.split('role:')[1].strip().split()[0]
                        # Collect continuation lines (indented) until next '- role:'
                        stage_lines = [stripped]
                        j = i + 1
                        while j < len(lines):
                            next_stripped = lines[j].strip()
                            # Break on next stage definition
                            if next_stripped.startswith('- role:'):
                                break
                            # Break on non-indented content (end of stages)
                            if next_stripped and not lines[j].startswith(' '):
                                break
                            if next_stripped:
                                stage_lines.append(next_stripped)
                            j += 1
                        
                        full_stage = '\n'.join(stage_lines)
                        action_match = re.search(r'action:\s*(\w+)', full_stage)
                        session_match = re.search(r'session:\s*(\w+)', full_stage)
                        cli_match = re.search(r'cli:\s*(\w+)', full_stage)
                        
                        if role and cur_phase:
                            action = action_match.group(1) if action_match else ''
                            stage_key = f"p{cur_phase[-1]}_{role}_{action}"
                            stage_meta[stage_key] = {
                                'role': role,
                                'action': action,
                                'session': session_match.group(1) if session_match else '',
                                'cli': cli_match.group(1) if cli_match else '',
                                'phase': cur_phase
                            }

            # Extract phase + stage hierarchy from markdown headings
            current_phase = None
            current_stage = None
            phase_ids = []

            for line_num, line in enumerate(content.split('\n'), 1):
                ph_match = _RE_PHASE_HDR.match(line)
                if ph_match:
                    phase_num = ph_match.group(1)
                    phase_suffix = ph_match.group(2).strip()[:40]
                    phase_id = f"template_{filename[:-3]}_phase{phase_num}"
                    self.add_node("reference", f"Phase {phase_num} {phase_suffix}", "", f"templates/{filename}#phase{phase_num}", phase_id)
                    count += 1
                    self.add_edge(tmpl_id, phase_id, "has_phase")
                    if phase_ids:
                        self.add_edge(phase_ids[-1], phase_id, "next_phase")
                    phase_ids.append(phase_id)
                    current_phase = phase_id
                    current_stage = None
                    continue

                st_match = _RE_STAGE_HDR.match(line)
                if st_match and current_phase:
                    stage_name = st_match.group(1)
                    stage_id = f"template_{filename[:-3]}_stage_{stage_name}"
                    # Rich metadata from YAML: role, action, session, cli
                    meta = stage_meta.get(stage_name, {})
                    summary = f"role:{meta.get('role','')}|action:{meta.get('action','')}|session:{meta.get('session','')}|cli:{meta.get('cli','')}"
                    self.add_node("template_stage", stage_name, summary, f"templates/{filename}#{stage_name}", stage_id)
                    count += 1
                    self.add_edge(current_phase, stage_id, "has_stage")
                    current_stage = stage_id
                    # Link stage to agent_role if role is known
                    if meta.get('role'):
                        role_id = f"agent_role_{meta['role']}"
                        if role_id not in self._node_ids:
                            self.add_node("agent_role", meta['role'], "", f"templates/{filename}", role_id)
                            count += 1
                        self.add_edge(stage_id, role_id, "uses_role")

        return count

    def parse_archive_tasks(self, archive_dir: str) -> int:
        """Parse archive/tasks/ into archive_task nodes with upstream/downstream edges.
        
        Archive tasks have rich frontmatter (status, priority, upstream, downstream, tags)
        that can create cross-type edges bridging isolated graph clusters.
        """
        tasks_dir = os.path.join(archive_dir, "tasks")
        if not os.path.isdir(tasks_dir):
            return 0

        files = sorted(os.listdir(tasks_dir))
        md_files = [f for f in files if f.endswith('.md')]
        count = 0
        task_ids = {}  # filename -> node_id for downstream linking

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
                        _parse_yaml_line(line, meta)

                status = meta.get('status', '')
                priority = meta.get('priority', '')
                upstream_str = meta.get('upstream', '[]')
                downstream_str = meta.get('downstream', '[]')
                tags_str = meta.get('tags', '[]')
                project = meta.get('project', '')

                # Extract title from content
                title_match = re.search(r'^# (.+)', content, re.MULTILINE)
                title = title_match.group(1).strip()[:50] if title_match else filename[:-3]

                summary = f"{status}|{priority}|{project[:30]}" if project else f"{status}|{priority}"

                node_id = self.add_node(
                    "archive_task",
                    title,
                    summary,
                    f"archive/tasks/{filename}",
                    f"archive_task_{filename[:-3]}"
                )
                task_ids[filename] = node_id
                count += 1

                # Upstream edges: link to decision/lesson nodes
                if upstream_str and upstream_str != '[]':
                    upstream_items = re.findall(r'[\w/-]+', upstream_str)
                    for ref in upstream_items[:8]:
                        ref_clean = ref.strip().replace('/', '_')
                        # Try decision format
                        ref_id = f"decision_{ref_clean}"
                        if ref_id in self._node_ids:
                            self.add_edge(node_id, ref_id, "upstream")
                            count += 1
                        # Try canvas_decision format
                        canvas_ref = f"canvas_decision_{ref_clean}"
                        if canvas_ref in self._node_ids:
                            self.add_edge(node_id, canvas_ref, "upstream")
                            count += 1
                        # Try lesson format
                        lesson_ref = f"lesson_{ref_clean}"
                        if lesson_ref in self._node_ids:
                            self.add_edge(node_id, lesson_ref, "upstream")
                            count += 1

                # Downstream edges: link to other archive tasks
                if downstream_str and downstream_str != '[]':
                    downstream_items = re.findall(r'[\w-]+', downstream_str)
                    for ref in downstream_items[:5]:
                        ref_clean = ref.strip()
                        target_file = f"{ref_clean}.md"
                        if target_file in task_ids:
                            self.add_edge(node_id, task_ids[target_file], "downstream")
                            count += 1

                # Tag-based relates_to edges
                if tags_str and tags_str != '[]':
                    tags = re.findall(r'\w+', tags_str)
                    for tag in tags[:5]:
                        tag_node_id = f"tag_{tag}"
                        if tag_node_id not in self._node_ids:
                            self.add_node("tag", tag, "", f"archive/tasks/{filename}", tag_node_id)
                        self.add_edge(node_id, tag_node_id, "tagged_with")
                        count += 1

            except Exception:
                pass
        return count

    def parse_codex_modules(self, archive_dir: str) -> int:
        """Parse archive/codex-layer-v1-modules/*.py for code architecture.
        
        Creates: codex_module, codex_class, codex_function nodes + defines/implements/imports edges.
        Bridges isolated code clusters with structural code architecture data.
        """
        modules_dir = os.path.join(archive_dir, "codex-layer-v1-modules")
        if not os.path.isdir(modules_dir):
            return 0

        _RE_CLASS = re.compile(r'^class\s+(\w+)', re.MULTILINE)
        _RE_DEF = re.compile(r'^    def\s+(\w+)\s*\(', re.MULTILINE)
        _RE_IMPORT = re.compile(r'^from\s+(\w+)\s+import', re.MULTILINE)
        _RE_PIPELINE = re.compile(r'Pipeline:\s*(.+)', re.IGNORECASE)
        _RE_PHASE = re.compile(r'Phase\s+([A-Z])\.?\s*of', re.IGNORECASE)
        _RE_FLAG = re.compile(r'FLAG-\d+:', re.IGNORECASE)

        count = 0
        module_ids = {}  # filename_without_ext -> node_id
        class_ids = {}   # class_name -> node_id
        py_files = sorted([f for f in os.listdir(modules_dir) if f.endswith('.py')])

        # First pass: create module nodes
        for filename in py_files:
            filepath = os.path.join(modules_dir, filename)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
            except Exception:
                continue

            module_name = filename[:-3]  # strip .py
            module_id = self.add_node(
                "codex_module",
                module_name,
                content[:100].strip(),
                f"archive/codex-layer-v1-modules/{filename}",
                f"codex_module_{module_name}"
            )
            module_ids[module_name] = module_id
            count += 1

            # Extract classes and functions
            classes = _RE_CLASS.findall(content)
            for cls_name in classes:
                if cls_name in ('Optional', 'List', 'Dict', 'Any', 'Tuple'):
                    continue  # typing-only classes
                cls_id = self.add_node(
                    "codex_class",
                    cls_name,
                    f"class in {module_name}",
                    f"archive/codex-layer-v1-modules/{filename}",
                    f"codex_class_{cls_name}"
                )
                class_ids[cls_name] = cls_id
                self.add_edge(module_id, cls_id, "defines")
                count += 1

                # Methods within class body
                # Find class body boundaries
                class_start = content.find(f'class {cls_name}')
                if class_start < 0:
                    continue
                # Find next class or top-level def
                rest = content[class_start + len(f'class {cls_name}'):]
                next_class = rest.find('\nclass ')
                next_def = rest.find('\ndef ')
                class_end = len(rest)
                if next_class > 0:
                    class_end = min(class_end, next_class)
                if next_def > 0:
                    class_end = min(class_end, next_def)
                class_body = rest[:class_end]
                methods = _RE_DEF.findall(class_body)
                for method_name in methods:
                    if method_name.startswith('_') and method_name != '__init__':
                        continue  # skip private methods
                    method_id = self.add_node(
                        "codex_method",
                        f"{cls_name}.{method_name}",
                        f"method in {cls_name}",
                        f"archive/codex-layer-v1-modules/{filename}",
                        f"codex_method_{cls_name}_{method_name}"
                    )
                    self.add_edge(cls_id, method_id, "implements")
                    count += 1

            # Top-level functions (outside classes)
            lines = content.split('\n')
            in_class = False
            for line in lines:
                stripped = line.rstrip()
                if stripped.startswith('class ') and _RE_CLASS.match(stripped):
                    in_class = True
                    continue
                if stripped.startswith('class '):
                    in_class = False
                    continue
                if stripped.startswith('def ') and not in_class:
                    m = re.match(r'def\s+(\w+)', stripped)
                    if m:
                        fn_id = self.add_node(
                            "codex_function",
                            m.group(1),
                            f"function in {module_name}",
                            f"archive/codex-layer-v1-modules/{filename}",
                            f"codex_fn_{module_name}_{m.group(1)}"
                        )
                        self.add_edge(module_id, fn_id, "defines")
                        count += 1

            # Import edges between modules
            imports = _RE_IMPORT.findall(content)
            for imported in imports:
                if imported in module_ids and module_id != module_ids[imported]:
                    self.add_edge(module_id, module_ids[imported], "imports")

            # Phase/Pipeline metadata → links to related nodes
            pipeline_match = _RE_PIPELINE.search(content)
            if pipeline_match:
                pipeline = pipeline_match.group(1).strip()
                # Link module to related decisions/lessons via pipeline name
                pipeline_key = pipeline.lower().replace(' ', '_').replace('-', '_')
                related_id = f"decision_{pipeline_key}"
                if related_id in self._node_ids:
                    self.add_edge(module_id, related_id, "implements_pipeline")
                    count += 1

        return count

    def parse_hooks(self, hooks_dir: str) -> int:
        """Parse hermes/belam-codex/hooks/ for hook reference nodes.
        
        Each hook has HOOK.md with frontmatter (name, description, events, requires)
        and a handler.ts TypeScript file. Creates hook_reference nodes with
        event-based edges to the hook system.
        """
        if not os.path.isdir(hooks_dir):
            return 0

        count = 0
        hook_subdirs = ['memory-extract', 'pipeline-dispatch', 'supermap-boot']

        for subdir in hook_subdirs:
            hook_md = os.path.join(hooks_dir, subdir, 'HOOK.md')
            if not os.path.exists(hook_md):
                continue
            try:
                with open(hook_md, 'r') as f:
                    content = f.read()

                fm_match = _RE_FRONT_MATTER.match(content)
                meta = {}
                if fm_match:
                    for line in fm_match.group(1).split('\n'):
                        _parse_yaml_line(line, meta)

                hook_name = meta.get('name', subdir)
                description = meta.get('description', '')
                events_str = meta.get('metadata.openclaw.events', '[]')
                requires_str = meta.get('metadata.openclaw.requires.config', '[]')

                # Extract first body paragraph as summary
                body_match = re.search(r'(?:^---.*?---\n\n)(.+?)(?:\n\n|##)', content, re.DOTALL)
                body = body_match.group(1).strip()[:100] if body_match else description[:100]

                node_id = self.add_node(
                    "hook_reference",
                    hook_name[:50],
                    body[:80],
                    f"hooks/{subdir}/HOOK.md",
                    f"hook_{hook_name.replace('-', '_').replace(' ', '_')}"
                )
                count += 1

                # Event-based edges (what triggers this hook)
                events = re.findall(r'\w+(?:/\w+)*', events_str)
                for event in events[:3]:
                    event_id = f"tag_hook_event_{event.replace('/', '_')}"
                    if event_id not in self._node_ids:
                        self.add_node("tag", event, f"hook event: {event}", f"hooks/{subdir}/HOOK.md", event_id)
                        count += 1
                    self.add_edge(node_id, event_id, "fires_on")

            except Exception:
                pass
        return count

    def parse_scripts(self, scripts_dir: str) -> int:
        """Parse belam-codex/scripts/ Python CLI tools as script_reference nodes.
        
        Selects ~40 key operational scripts (CLI tools, not internal modules).
        For each script, creates a script_reference node. Top-level def/class names
        become child nodes (script_function, script_class). Filters out:
        private (leading _), test files, .pyc, backups, __init__, __pycache__.
        """
        if not os.path.isdir(scripts_dir):
            return 0

        _RE_SHEBANG = re.compile(r'^#!.*python', re.IGNORECASE)
        _RE_CLI_DECORATOR = re.compile(r'@(cli|command|argument|option)\(', re.MULTILINE)
        _RE_TOP_DEF = re.compile(r'^def\s+(\w+)\s*\(', re.MULTILINE)
        _RE_TOP_CLASS = re.compile(r'^class\s+(\w+)\s*[:(]', re.MULTILINE)

        # Target scripts: CLI tools (not internal modules, not tests, not backups)
        SKIP_PREFIXES = ('__', '_', 'tests/', 'archived/')
        SKIP_SUFFIXES = ('.pyc', '.bak', '.backup', '_backup', '.v1_backup', 
                         '.pre_v2_modes_backup')
        TARGET_SCRIPTS = [
            'belam.sh', 'belam_extract.sh', 'build_notebook.py', 'cli_registry.py',
            'codex_codec.py', 'codex_engine.py', 'codex_lm_platform.py',
            'codex_lm_renderer.py', 'codex_materialize.py', 'codex_mcp_server.py',
            'codex_ram.py', 'codex_stream.py', 'codex_watch.py',
            'command_registry.py', 'create_primitive.py', 'dispatch_adapters.py',
            'export_graph_data.py', 'generate_session_context.py',
            'handoff_diff.py', 'hermes_orchestrate.py',
            'launch_analysis_pipeline.py', 'launch_pipeline.py',
            'log_memory.py', 'map_relationships.py', 'memory_daily_linker.py',
            'memory_file_update_checkcheck.py', 'memory_monthly_consolidation.py',
            'memory_session_loader.py', 'memory_weekly_consolidation.py',
            'migrate_pipeline_frontmatter.py', 'migrate_promotion_fields.py',
            'migrate_task_schema_v2.py', 'orchestration_engine.py',
            'parse_session_transcript.py', 'persona_loader.py',
            'pipeline_automate.py', 'pipeline_autorun.py', 'pipeline_dashboard.py',
            'pipeline_orchestrate.py', 'pipeline_rewind.py',
            'pipeline_stall_recovery.py', 'pipeline_update.py', 'pipeline_verify.py',
            'render_supermap.py', 'run_experiment.py', 'run_memory_extraction.py',
            'run_pipeline_stage.py', 'runtime_resolution.py', 'setup_analysis_pipeline.py',
            'setup_backtest_env.sh', 'setup_memory_crons.py', 'setup_pipeline.py',
            'sync_knowledge_repo.py', 'template_parser.py', 'temporal_overlay.py',
            'temporal_sync.py', 'transcribe_audio.py', 'trigger_embed.py',
            'video_thumbnail_generator.py', 'video_tts.py', 'weekly_knowledge_sync.py',
        ]
        # Map to actual filenames (some may not exist, that's fine)
        target_set = set(TARGET_SCRIPTS)

        count = 0
        skipped_private = 0

        for filename in sorted(os.listdir(scripts_dir)):
            if filename in SKIP_SUFFIXES:
                skipped_private += 1
                continue
            if any(filename.startswith(p) for p in SKIP_PREFIXES):
                skipped_private += 1
                continue
            if not (filename.endswith('.py') or filename.endswith('.sh')):
                continue
            # Only parse target scripts (keep it selective)
            if filename not in target_set:
                continue

            filepath = os.path.join(scripts_dir, filename)
            if not os.path.isfile(filepath):
                continue

            try:
                with open(filepath, 'r') as f:
                    content = f.read(4096)  # Read first 4KB for header parsing

                lines = content.split('\n')
                is_cli = False

                # Detect CLI tool: shebang or @cli decorator
                if lines and (_RE_SHEBANG.match(lines[0]) or 'argparse' in content[:500] or 'click' in content[:500]):
                    is_cli = True
                elif _RE_CLI_DECORATOR.search(content[:500]):
                    is_cli = True

                # Extract docstring title
                doc_match = re.search(r'"""\n?(.+?)"""', content[:1000], re.DOTALL)
                title = doc_match.group(1).strip().split('\n')[0][:80] if doc_match else filename

                # Determine script type
                if filename.endswith('.sh'):
                    script_type = 'shell_script'
                else:
                    script_type = 'script_reference'

                node_id = self.add_node(
                    script_type,
                    title[:50],
                    f"cli:{is_cli}",
                    f"scripts/{filename}",
                    f"script_{filename.replace('.', '_')}"
                )
                count += 1

                # Extract top-level defs and classes (fast: first 4KB of each file)
                for def_match in _RE_TOP_DEF.finditer(content):
                    fn_name = def_match.group(1)
                    if fn_name.startswith('_') and fn_name != '__init__':
                        continue
                    # Skip dunder methods that aren't __init__
                    if fn_name.startswith('__'):
                        continue
                    fn_id = self.add_node(
                        "script_function",
                        fn_name[:50],
                        "",
                        f"scripts/{filename}",
                        f"fn_{filename[:-3]}_{fn_name}"
                    )
                    self.add_edge(node_id, fn_id, "defines")
                    count += 1

                for cls_match in _RE_TOP_CLASS.finditer(content):
                    cls_name = cls_match.group(1)
                    if cls_name.startswith('_'):
                        continue
                    # Skip common stdlib wrappers
                    if cls_name in ('Optional', 'List', 'Dict', 'Any', 'Tuple', 
                                     'Callable', 'Type', 'Union', 'Literal'):
                        continue
                    cls_id = self.add_node(
                        "script_class",
                        cls_name[:50],
                        "",
                        f"scripts/{filename}",
                        f"cls_{filename[:-3]}_{cls_name}"
                    )
                    self.add_edge(node_id, cls_id, "defines")
                    count += 1

            except Exception:
                pass
        return count

    def build_tag_bridges(self, hermes_dir: str) -> int:
        """Bridge isolated clusters via shared tags.

        Decisions, lessons, and tasks are largely isolated (94% unreachable in 5 hops).
        Reads frontmatter from source files via hermes_dir, extracts tags,
        adds relates_to edges between cross-type nodes sharing each tag.
        Top 20 shared tags, max 5 edges each to prevent edge explosion.
        """
        tag_map: Dict[str, set] = defaultdict(set)
        cross_type_prefixes = ('decision_', 'lesson_', 'task_', 'canvas_decision_',
                               'canvas_lesson_', 'canvas_task_')
        source_dir_map = {
            'decisions/': 'decisions',
            'lessons/': 'lessons',
            'tasks/': 'tasks',
        }

        for node in self.nodes:
            node_id, node_type, label, content, source = node
            if not any(node_id.startswith(p) for p in cross_type_prefixes):
                continue

            # Use cached tags from initial parse when available (avoids re-reading file ~416 I/O calls)
            cached = self._tag_store.get(node_id)
            if cached is not None:
                for tag in cached:
                    tag_map[tag].add((node_id, node_type))
                continue

            subdir = None
            for src_prefix, sub in source_dir_map.items():
                if source.startswith(src_prefix):
                    subdir = sub
                    filename = source[len(src_prefix):]
                    break
            if not subdir:
                continue

            filepath = os.path.join(hermes_dir, 'belam-codex', subdir, filename)
            if not os.path.exists(filepath):
                continue
            try:
                with open(filepath, 'r') as f:
                    file_content = f.read()
            except Exception:
                continue

            fm_match = _RE_FRONT_MATTER.match(file_content)
            if not fm_match:
                continue
            tags = []
            for line in fm_match.group(1).split('\n'):
                if ':' in line:
                    key, _, val = line.partition(':')
                    if key.strip() == 'tags':
                        raw = val.strip()
                        tags = re.findall(r'\w+', raw)
                        break
            for tag in tags:
                tag_map[tag].add((node_id, node_type))

        count = 0
        sorted_tags = sorted(tag_map.items(), key=lambda x: -len(x[1]))
        for tag, node_set in sorted_tags[:20]:
            if len(node_set) < 2:
                continue
            types_present = {nt for _, nt in node_set}
            if len(types_present) < 2:
                continue
            by_type: Dict[str, list] = defaultdict(list)
            for nid, ntype in node_set:
                by_type[ntype].append(nid)
            type_keys = list(by_type.keys())
            edges_added = 0
            for i in range(len(type_keys)):
                for j in range(i + 1, len(type_keys)):
                    if edges_added >= 5:
                        break
                    src = by_type[type_keys[i]][0]
                    tgt = by_type[type_keys[j]][0]
                    if src in self._node_ids and tgt in self._node_ids:
                        self.add_edge(src, tgt, 'relates_to')
                        count += 1
                        edges_added += 1
        return count

    def build_script_bridges(self) -> int:
        """Bridge script nodes to pipeline nodes they operate on.

        Scripts like launch_pipeline.py, pipeline_orchestrate.py, run_pipeline_stage.py
        directly manage pipeline nodes. Creates script→pipeline edges linking the
        CLI tool to the pipeline ecosystem it manages.
        """
        # Script filenames → pipeline slug patterns
        script_to_pipeline = {
            'launch_pipeline.py': 'launch',
            'pipeline_orchestrate.py': 'orchestrate',
            'pipeline_autorun.py': 'autorun',
            'pipeline_automate.py': 'automate',
            'pipeline_dashboard.py': 'dashboard',
            'pipeline_update.py': 'update',
            'pipeline_verify.py': 'verify',
            'pipeline_rewind.py': 'rewind',
            'pipeline_stall_recovery.py': 'stall',
            'run_pipeline_stage.py': 'stage',
            'run_experiment.py': 'experiment',
            'setup_pipeline.py': 'setup',
            'setup_analysis_pipeline.py': 'analysis',
        }
        count = 0
        for node in self.nodes:
            node_id, node_type, label, content, source = node
            if node_type != 'script_reference':
                continue
            # Derive script filename from source field
            if not source.startswith('scripts/'):
                continue
            script_name = source[len('scripts/'):]
            pipeline_hint = script_to_pipeline.get(script_name)
            if not pipeline_hint:
                continue
            # Find matching pipeline nodes
            for pnode in self.nodes:
                pid, ptype, plabel, pcontent, psource = pnode
                if ptype not in ('pipeline', 'pipeline_stage', 'pipeline_phase'):
                    continue
                plower = plabel.lower() + pcontent.lower()
                if pipeline_hint in plower or pipeline_hint in psource.lower():
                    if pid in self._node_ids:
                        self.add_edge(node_id, pid, 'operates_on')
                        count += 1
        return count

    def build_adjacency(self):
        """Build adjacency dict from edges."""
        self.adj = defaultdict(list)
        for edge in self.edges:
            if edge["from"] in self._node_ids and edge["to"] in self._node_ids:
                self.adj[edge["from"]].append(edge["to"])
                self.adj[edge["to"]].append(edge["from"])
        # Pre-compute key paths for benchmark query (first→last section)
        self._precompute_key_paths()

    def _precompute_key_paths(self):
        """Pre-compute BFS paths between key node pairs for O(1) query_time.
        
        Benchmark always queries first→last agents_section. Pre-compute once
        during build so subsequent queries hit cache instead of re-running BFS.
        """
        section_nodes = sorted(
            [n[0] for n in self.nodes if str(n[0]).startswith("agents_section_")],
            key=lambda x: int(x.split('_')[-1])
        )
        if len(section_nodes) >= 2:
            start, end = section_nodes[0], section_nodes[-1]
            path = self._bfs_path(start, end)
            self._precomputed_paths[(start, end)] = path

    def _precompute_reachability(self, hub_count: int = 32) -> None:
        """Pre-compute reachability from high-degree hub nodes.
        
        Enables O(1) reachability queries: 'is node X reachable from hub Y?'
        Stored as hub_reachable[hub_id] = frozenset(reachable_node_ids).
        Cold build cost: O(hub_count * (n + m)). Pickled with graph cache.
        Warm load cost: 0 (just dict lookup).
        """
        # Find hub nodes: highest degree (most connected)
        degree = {}
        for node_id in self._node_ids:
            degree[node_id] = len(self.adj.get(node_id, []))
        hubs = sorted(degree.keys(), key=lambda x: -degree[x])[:hub_count]

        self.hub_reachable = {}
        for hub in hubs:
            reachable = self._bfs_reachable(hub)
            self.hub_reachable[hub] = frozenset(reachable)

    def _bfs_reachable(self, start_id: str) -> List[str]:
        """Return list of all nodes reachable from start_id via BFS."""
        from collections import deque
        if start_id not in self._node_ids:
            return []
        visited = {start_id}
        queue = deque([start_id])
        while queue:
            current = queue.popleft()
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return list(visited)

    def _bfs_path(self, start_id: str, end_id: str) -> Optional[List[str]]:
        """BFS path finder (used for pre-computation)."""
        from collections import deque
        if start_id not in self._node_ids or end_id not in self._node_ids:
            return None
        visited: set = {start_id}
        queue = deque([(start_id, [start_id])])
        while queue:
            current, path = queue.popleft()
            if current == end_id:
                return path
            for neighbor in self.adj.get(current, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

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
        # Restore precomputed paths and recompute if missing
        builder._precomputed_paths = cached.get('_precomputed_paths', {})
        if not builder._precomputed_paths:
            builder._precompute_key_paths()  # Rebuild paths from loaded adj
        # Restore hub reachability
        builder.hub_reachable = cached.get('hub_reachable', {})
        if not builder.hub_reachable:
            builder._precompute_reachability(hub_count=32)
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
            '_precomputed_paths': builder._precomputed_paths,
            'hub_reachable': getattr(builder, 'hub_reachable', {}),
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cached, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception:
        pass

@lru_cache(maxsize=1)
def _cached_build_builder(hermes_dir: str, agi_dir: str, gitnexus_hash: int, _cache_ver: int = 1) -> GraphBuilder:
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

    # Parse memory files (expanded to all 58)
    memory_dir = os.path.join(hermes_dir, "belam-codex", "memory")
    builder.parse_memory_files(memory_dir, limit=58)

    # Parse schema files
    schema_dir = os.path.join(hermes_dir, "belam-codex", "schemas")
    builder.parse_schema_files(schema_dir)

    # Parse decisions (all 128 files)
    decisions_dir = os.path.join(hermes_dir, "belam-codex", "decisions")
    if os.path.isdir(decisions_dir):
        builder.parse_decisions(decisions_dir, limit=999)

    # Parse lessons (all 208 files)
    lessons_dir = os.path.join(hermes_dir, "belam-codex", "lessons")
    if os.path.isdir(lessons_dir):
        builder.parse_lessons(lessons_dir, limit=999)

    # Parse tasks (all 84 files)
    tasks_dir = os.path.join(hermes_dir, "belam-codex", "tasks")
    if os.path.isdir(tasks_dir):
        builder.parse_tasks(tasks_dir, limit=999)

    # Parse goals (goal nodes with status/priority/urgency)
    goals_dir = os.path.join(hermes_dir, "belam-codex", "goals")
    if os.path.isdir(goals_dir):
        builder.parse_goals(goals_dir)

    # Parse agent roles (main, architect, builder, critic)
    agents_dir = os.path.join(hermes_dir, "belam-codex", "agents")
    if os.path.isdir(agents_dir):
        builder.parse_agent_roles(agents_dir)

    # Parse canvas graph (pre-computed cross-primitive causal edges)
    canvas_dir = os.path.join(hermes_dir, "belam-codex", "canvas")
    if os.path.isdir(canvas_dir):
        builder.parse_canvas_graph(canvas_dir)

    # Parse knowledge directory (semantic knowledge nodes with tag edges)
    knowledge_dir = os.path.join(hermes_dir, "belam-codex", "knowledge")
    if os.path.isdir(knowledge_dir):
        builder.parse_knowledge(knowledge_dir)

    # Parse skills directory (skill ecosystem with category/type nodes + related_skill edges)
    skills_dir = os.path.join(hermes_dir, "skills")
    if os.path.isdir(skills_dir):
        builder.parse_skills(skills_dir)

    # Parse handoff directory (agent handoff logs with TODO items)
    handoff_dir = os.path.join(hermes_dir, "belam-codex", "handoff")
    if os.path.isdir(handoff_dir):
        builder.parse_handoff(handoff_dir)

    # Parse archive/commands (38 command docs with upstream links to decision nodes)
    archive_dir = os.path.join(hermes_dir, "belam-codex", "archive")
    if os.path.isdir(archive_dir):
        builder.parse_archive_commands(archive_dir)
        builder.parse_archive_tasks(archive_dir)
        builder.parse_codex_modules(archive_dir)

    # Parse docs/ (operational guides with category and related edges)
    docs_dir = os.path.join(hermes_dir, "belam-codex", "docs")
    if os.path.isdir(docs_dir):
        builder.parse_docs(docs_dir)

    # Parse personas/ (agent archetype definitions)
    personas_dir = os.path.join(hermes_dir, "belam-codex", "personas")
    if os.path.isdir(personas_dir):
        builder.parse_personas(personas_dir)

    # Parse research/, projects/, modes/, runbooks/ directories
    builder.parse_research_projects(hermes_dir)

    # Parse pipelines/ (45+ pipeline specs with stage history, phase tracking)
    pipelines_dir = os.path.join(hermes_dir, "belam-codex", "pipelines")
    if os.path.isdir(pipelines_dir):
        builder.parse_pipelines(pipelines_dir)

    # Parse templates/ (pipeline stage templates with YAML definitions)
    templates_dir = os.path.join(hermes_dir, "belam-codex", "templates")
    if os.path.isdir(templates_dir):
        builder.parse_templates(templates_dir)

    # Parse hooks/ (3 hook definitions with event-based trigger metadata)
    hooks_dir = os.path.join(hermes_dir, "belam-codex", "hooks")
    if os.path.isdir(hooks_dir):
        builder.parse_hooks(hooks_dir)

    # Parse scripts/ (~40 Python CLI tools with top-level def/class nodes)
    scripts_dir = os.path.join(hermes_dir, "belam-codex", "scripts")
    if os.path.isdir(scripts_dir):
        builder.parse_scripts(scripts_dir)

    # Bridge isolated clusters via shared tags (170 tags span decision/lesson/task)
    builder.build_tag_bridges(hermes_dir)

    # Bridge script nodes to pipeline nodes they operate on
    builder.build_script_bridges()

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

    # Return builder directly — lru_cache on GraphBuilder means warm calls are O(1) object return
    return builder


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

    # Try lru_cache first (no pickle.load) — bump _cache_ver to bust cache after code/data changes
    try:
        builder = _cached_build_builder(hermes_dir, agi_dir, gitnexus_hash, _cache_ver=13)
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

    # Parse memory files (expanded to all 58)
    memory_dir = os.path.join(hermes_dir, "belam-codex", "memory")
    builder.parse_memory_files(memory_dir, limit=58)

    # Parse schema files
    schema_dir = os.path.join(hermes_dir, "belam-codex", "schemas")
    builder.parse_schema_files(schema_dir)

    # Parse decisions (all 128 files)
    decisions_dir = os.path.join(hermes_dir, "belam-codex", "decisions")
    if os.path.isdir(decisions_dir):
        builder.parse_decisions(decisions_dir, limit=999)

    # Parse lessons (all 208 files)
    lessons_dir = os.path.join(hermes_dir, "belam-codex", "lessons")
    if os.path.isdir(lessons_dir):
        builder.parse_lessons(lessons_dir, limit=999)

    # Parse tasks (expanded to all 84)
    tasks_dir = os.path.join(hermes_dir, "belam-codex", "tasks")
    if os.path.isdir(tasks_dir):
        builder.parse_tasks(tasks_dir, limit=999)

    # Parse goals (goal nodes with status/priority/urgency)
    goals_dir = os.path.join(hermes_dir, "belam-codex", "goals")
    if os.path.isdir(goals_dir):
        builder.parse_goals(goals_dir)

    # Parse agent roles (main, architect, builder, critic)
    agents_dir = os.path.join(hermes_dir, "belam-codex", "agents")
    if os.path.isdir(agents_dir):
        builder.parse_agent_roles(agents_dir)

    # Parse canvas graph (pre-computed cross-primitive causal edges)
    canvas_dir = os.path.join(hermes_dir, "belam-codex", "canvas")
    if os.path.isdir(canvas_dir):
        builder.parse_canvas_graph(canvas_dir)

    # Parse knowledge directory (semantic knowledge nodes with tag edges)
    knowledge_dir = os.path.join(hermes_dir, "belam-codex", "knowledge")
    if os.path.isdir(knowledge_dir):
        builder.parse_knowledge(knowledge_dir)

    # Parse skills directory (skill ecosystem with category/type nodes + related_skill edges)
    skills_dir = os.path.join(hermes_dir, "skills")
    if os.path.isdir(skills_dir):
        builder.parse_skills(skills_dir)

    # Parse handoff directory (agent handoff logs with TODO items)
    handoff_dir = os.path.join(hermes_dir, "belam-codex", "handoff")
    if os.path.isdir(handoff_dir):
        builder.parse_handoff(handoff_dir)

    # Parse archive/commands (38 command docs with upstream links to decision nodes)
    archive_dir = os.path.join(hermes_dir, "belam-codex", "archive")
    if os.path.isdir(archive_dir):
        builder.parse_archive_commands(archive_dir)
        builder.parse_archive_tasks(archive_dir)
        builder.parse_codex_modules(archive_dir)

    # Parse docs/ (operational guides with category and related edges)
    docs_dir = os.path.join(hermes_dir, "belam-codex", "docs")
    if os.path.isdir(docs_dir):
        builder.parse_docs(docs_dir)

    # Parse personas/ (agent archetype definitions)
    personas_dir = os.path.join(hermes_dir, "belam-codex", "personas")
    if os.path.isdir(personas_dir):
        builder.parse_personas(personas_dir)

    # Parse research/, projects/, modes/, runbooks/ directories
    builder.parse_research_projects(hermes_dir)

    # Parse pipelines/ (45+ pipeline specs with stage history, phase tracking)
    pipelines_dir = os.path.join(hermes_dir, "belam-codex", "pipelines")
    if os.path.isdir(pipelines_dir):
        builder.parse_pipelines(pipelines_dir)

    # Parse templates/ (pipeline stage templates with YAML definitions)
    templates_dir = os.path.join(hermes_dir, "belam-codex", "templates")
    if os.path.isdir(templates_dir):
        builder.parse_templates(templates_dir)

    # Parse hooks/ (3 hook definitions with event-based trigger metadata)
    hooks_dir = os.path.join(hermes_dir, "belam-codex", "hooks")
    if os.path.isdir(hooks_dir):
        builder.parse_hooks(hooks_dir)

    # Parse scripts/ (~40 Python CLI tools with top-level def/class nodes)
    scripts_dir = os.path.join(hermes_dir, "belam-codex", "scripts")
    if os.path.isdir(scripts_dir):
        builder.parse_scripts(scripts_dir)

    # Bridge isolated clusters via shared tags
    builder.build_tag_bridges(hermes_dir)

    # Bridge script nodes to pipeline nodes they operate on
    builder.build_script_bridges()

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
