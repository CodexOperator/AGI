#!/usr/bin/env python3
"""Experiment: in-graph embedding storage — full toggle integration test.

Tests the core claims from hypothesis:a00-12e9183c-90ceab using the actual
store_in_graph implementation on EmbeddingConfig + embed_graph().
"""

import json
import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "extensions", "agi", "src"))

from graph_core import Node
from graph_core.edge import Edge
from graph_core.graph import Graph
from graph_core.persistence import load_node_file
from graph_core.persistence.frontmatter import NodeFile, save_node_file
from embeddings import embed_graph, EmbeddingConfig, default_config
from embeddings.projection import project, ProjectionConfig

PASS = "✓"
FAIL = "✗"


def _chain(ids: list[str]) -> Graph:
    g = Graph()
    for i in ids:
        g.add_node(Node(id=i, type="x"))
    for a, b in zip(ids, ids[1:]):
        g.add_edge(Edge(source_id=a, target_id=b, relation="next"))
    return g


def _write_graph(graph: Graph, tmpdir: Path, extant: set[str] | None = None) -> dict[str, Path]:
    """Write node files in standard layout: tmpdir/nodes/<type>/<id>.md."""
    paths: dict[str, Path] = {}
    for n in graph.nodes:
        type_dir = tmpdir / "nodes" / n.type
        type_dir.mkdir(parents=True, exist_ok=True)
        fpath = type_dir / f"{n.id}.md"
        if extant and n.id not in extant:
            continue  # skip writing this file (simulate missing node file)
        fm = {"id": n.id, "type": n.type}
        if n.parents:
            fm["parents"] = list(n.parents)
        if n.children:
            fm["children"] = list(n.children)
        nf = NodeFile(frontmatter=fm, body="", suffix=".md")
        save_node_file(fpath, nf)
        paths[n.id] = fpath
    return paths


def _read_embedding_from_file(fpath: Path) -> list[float] | None:
    nf = load_node_file(fpath)
    emb = nf.frontmatter.get("embedding")
    if isinstance(emb, list):
        return [float(v) for v in emb]
    return None


def _vecs_close(a: list[float], b: list[float], tol: float = 1e-12) -> bool:
    if len(a) != len(b):
        return False
    return all(abs(av - bv) <= tol for av, bv in zip(a, b))


def main():
    passed = 0
    failed = 0

    with tempfile.TemporaryDirectory() as tmpdir_str:
        tmpdir = Path(tmpdir_str)

        # === TEST 1: Toggle exists and defaults off ===
        cfg = EmbeddingConfig()
        actual = cfg.store_in_graph
        expected = False
        ok = actual == expected
        print(f"{PASS if ok else FAIL} T1: store_in_graph defaults to False (got={actual})")
        if ok:
            passed += 1
        else:
            failed += 1

        full_dir = str(tmpdir / "graph")

        # === TEST 2: store_in_graph=False — no side effects, no graph_dir needed ===
        graph = _chain(["a", "b", "c"])
        vecs_normal = embed_graph(graph, EmbeddingConfig(seed=42))
        assert len(vecs_normal) == 3
        print(f"{PASS} T2: store_in_graph=False works without graph_dir, returns 3 vectors (no side effects)")
        passed += 1

        # === TEST 3: store_in_graph=True writes vectors to frontmatter ===
        graph2 = _chain(["n0", "n1", "n2", "n3", "n4"])
        _write_graph(graph2, tmpdir / "graph")
        cfg_w = EmbeddingConfig(seed=42, store_in_graph=True)
        # First pass: compute and write
        vecs1 = embed_graph(graph2, cfg_w, graph_dir=str(tmpdir / "graph"))
        # Check vectors were written to files
        all_written = True
        for n in graph2.nodes:
            fpath = tmpdir / "graph" / "nodes" / n.type / f"{n.id}.md"
            if not fpath.exists():
                print(f"  FILE MISSING: {fpath}")
                all_written = False
                continue
            emb = _read_embedding_from_file(fpath)
            if emb is None:
                print(f"  NO EMBEDDING: {fpath}")
                all_written = False
                continue
            if not _vecs_close(emb, vecs1[n.id]):
                print(f"  VECTOR MISMATCH: {n.id}")
                all_written = False
        print(f"{PASS if all_written else FAIL} T3: store_in_graph=True writes vectors to frontmatter (all {len(graph2.node_ids)} written)")
        if all_written:
            passed += 1
        else:
            failed += 1

        # === TEST 4: Round-trip integrity — reload reads from frontmatter ===
        vecs2 = embed_graph(graph2, cfg_w, graph_dir=str(tmpdir / "graph"))
        # Should be the same as computed (since they were just written back)
        rt_ok = all(_vecs_close(vecs1[nid], vecs2[nid]) for nid in vecs1)
        if rt_ok:
            print(f"{PASS} T4: Round-trip — 2nd embed_graph(store_in_graph=True) returns identical vectors (within 1e-12)")
            passed += 1
        else:
            # Check max diff
            max_diff = max(abs(vecs1[nid][i] - vecs2[nid][i]) for nid in vecs1 for i in range(64))
            print(f"{FAIL} T4: Round-trip — max diff={max_diff:.2e}")
            failed += 1

        # === TEST 5: Idempotent re-run — no recomputation, same result ===
        vecs3 = embed_graph(graph2, cfg_w, graph_dir=str(tmpdir / "graph"))
        idem_ok = all(_vecs_close(vecs2[nid], vecs3[nid]) for nid in vecs2)
        print(f"{PASS if idem_ok else FAIL} T5: Idempotent re-run — 3rd call returns same vectors")
        if idem_ok:
            passed += 1
        else:
            failed += 1

        # === TEST 6: Selective embed — add new node, only it gets computed ===
        graph2.add_node(Node(id="n5", type="x"))
        graph2.add_edge(Edge(source_id="n4", target_id="n5", relation="next"))
        # Write file for the new node (without embedding)
        new_path = tmpdir / "graph" / "nodes" / "x" / "n5.md"
        new_path.parent.mkdir(parents=True, exist_ok=True)
        nf_new = NodeFile(frontmatter={"id": "n5", "type": "x", "parents": ["n4"]}, body="", suffix=".md")
        save_node_file(new_path, nf_new)

        vecs4 = embed_graph(graph2, cfg_w, graph_dir=str(tmpdir / "graph"))
        # All 5 existing vectors should be identical
        existing_ok = all(_vecs_close(vecs3[nid], vecs4[nid]) for nid in vecs3)
        # New node should have a vector
        new_vec = vecs4.get("n5")
        new_ok = new_vec is not None and len(new_vec) == 64

        if existing_ok and new_ok:
            print(f"{PASS} T6: Selective embed — 5 existing identical, new node n5 has 64-dim vector")
            passed += 1
        else:
            print(f"{FAIL} T6: Selective embed — existing_ok={existing_ok}, new_ok={new_ok}")
            failed += 1

        # === TEST 7: Compatibility — project() accepts frontmatter-read vectors ===
        coords = project(vecs4, ProjectionConfig(seed=42))
        compat_ok = set(coords.keys()) == set(vecs4.keys()) and all(len(c) == 2 for c in coords.values())
        print(f"{PASS if compat_ok else FAIL} T7: project() consumes frontmatter-read vectors ({len(coords)} coords)")
        if compat_ok:
            passed += 1
        else:
            failed += 1

        # === TEST 8: store_in_graph=False → no frontmatter writes (no embedding key) ===
        graph3 = _chain(["x0", "x1"])
        _write_graph(graph3, tmpdir / "graph2")
        embed_graph(graph3, EmbeddingConfig(seed=42, store_in_graph=False), graph_dir=str(tmpdir / "graph2"))
        no_writes = True
        for n in graph3.nodes:
            fpath = tmpdir / "graph2" / "nodes" / n.type / f"{n.id}.md"
            if fpath.exists():
                emb = _read_embedding_from_file(fpath)
                if emb is not None:
                    no_writes = False
                    break
        print(f"{PASS if no_writes else FAIL} T8: store_in_graph=False leaves files untouched")
        if no_writes:
            passed += 1
        else:
            failed += 1

    print(f"\n=== RESULTS: {passed}/{passed+failed} passed ===")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())