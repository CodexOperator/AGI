#!/usr/bin/env python3
"""snapshot-build-site.py — convert build-site.md into a directory of node files.

Reads `context/plans/build-site.md` and writes one frontmatter file per:
- task (T-NNN)            — schema [task]
- cavekit requirement (R) — schema [hypothesis] (each R is a hypothesis-to-test)
- domain                  — schema [idea] (each domain is a big idea)

Output: `nodes/<type>/<id>.md`

Run: `python3 bin/snapshot-build-site.py`
"""
from __future__ import annotations

import json
import os
import re
import sys
import yaml
from datetime import datetime, timezone
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# goal:g11.1 — one resolver for every path. `bin/` goes on sys.path so the
# hyphenated filename can still reach its importable siblings.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
from frontmatter import split_frontmatter  # noqa: E402

#: This file is the sharp one: it unlinks every `origin: build-site` node it
#: does not re-derive on that run (H0i). Its own copy of the walk resolved
#: `os.getcwd()` with no ancestor walk at all, so running it from the repo root
#: under the goal:g11 layout aimed it at `<repo>/nodes` instead of
#: `<repo>/.agi/nodes` — silently, the level3.py failure shape. Only the
#: missing-`build-site.md` guard below (L18) kept that from pruning.
PROJECT_ROOT = locations.project_root_from_env() or Path(os.getcwd()).resolve()

# `ensure_mint_id` and `write_frontmatter` from snapshot-goals.py, by file path
# (hyphenated filename, not importable) — the same convention level3.py,
# decompose-engine.py and backfill-mint-ids.py already use, and for the same
# reason: one definition of how a node is written, never a second one free to
# disagree (goal:s14).  The serializer joined the mint hook here on 2026-08-27;
# before that this file kept its own copy and the two had already drifted.
import importlib.util  # noqa: E402
_sg_spec = importlib.util.spec_from_file_location(
    "snapshot_goals_for_build_site", PLUGIN_ROOT / "bin" / "snapshot-goals.py")
_sg = importlib.util.module_from_spec(_sg_spec)
_sg_spec.loader.exec_module(_sg)
ensure_mint_id = _sg.ensure_mint_id


#: Re-exported from `locations` rather than redefined: the accepted marker
#: names are a property of the layout, not of this script.
config_path = locations.config_path

BUILD_SITE = PROJECT_ROOT / "context" / "plans" / "build-site.md"
KITS_DIR = PROJECT_ROOT / "context" / "kits"
NODES_DIR = PROJECT_ROOT / "nodes"

TASK_RE = re.compile(r"^####\s+(T-\d{3}):\s+(.+)$")
TIER_RE = re.compile(r"^##\s+Tier\s+(\d+)")
KIT_RE = re.compile(r"^####\s+T-\d{3}:.*$")
FIELD_RE = re.compile(r"^-\s+\*\*(?P<key>[\w ]+):\*\*\s*(?P<val>.+)$")


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9\- ]", "", s.lower())
    s = re.sub(r"\s+", "-", s.strip())
    parts = s.split("-")[:6]
    return "-".join(p for p in parts if p) or "untitled"


def _add_graph_core_to_path() -> None:
    """Put graph_core on sys.path, plugin src last so a project can override.

    Mirrors driver.sh's convention and zoom.py's `_add_graph_core_to_path`.
    Without this the sqlite branch below raised ModuleNotFoundError *mid-run*,
    after some node files had already been written — a project with
    `persistence.type: sqlite` could not snapshot at all.
    """
    plugin_src = PLUGIN_ROOT / "src"
    if plugin_src.is_dir() and str(plugin_src) not in sys.path:
        sys.path.insert(0, str(plugin_src))
    proj_src = PROJECT_ROOT / "src"
    if (proj_src / "graph_core").is_dir() and str(proj_src) not in sys.path:
        sys.path.insert(0, str(proj_src))


def _upsert_node_to_db(node_id: str, fm: dict, body: str, origin: str) -> None:
    """Upsert a node into SQLite if persistence.type=sqlite.

    Writes to filesystem via write_frontmatter first (existing behavior);
    this call syncs the DB when configured.
    """
    if not hasattr(_upsert_node_to_db, "_backend"):
        cfg_path = config_path(PROJECT_ROOT)
        _upsert_node_to_db._backend = None
        if cfg_path is not None:
            cfg = json.loads(cfg_path.read_text())
            if cfg.get("persistence", {}).get("type") == "sqlite":
                db_path = PROJECT_ROOT / cfg["persistence"]["path"]
                _add_graph_core_to_path()
                # The DB is a mirror of the files just written, so an
                # unavailable backend must degrade to a warning. Raising here
                # aborts mid-corpus and leaves a partially-snapshotted graph —
                # a project shadowing graph_core with a stale copy that predates
                # sqlite_backend hit exactly that.
                try:
                    from graph_core.persistence.sqlite_backend import SQLiteBackend
                    _upsert_node_to_db._backend = SQLiteBackend(db_path)
                except Exception as exc:
                    print(f"WARN: sqlite persistence unavailable ({exc}); "
                          f"nodes written to files only", file=sys.stderr)
    if _upsert_node_to_db._backend is None:
        return
    from graph_core.persistence.frontmatter import NodeFile
    fm = dict(fm)
    fm["id"] = node_id
    fm["origin"] = origin
    nf = NodeFile(frontmatter={**fm, "body": body}, body=body, suffix=".json")
    _upsert_node_to_db._backend.save(node_id, nf)


# The serializer itself, from snapshot-goals.py, by the same file-path import
# as `ensure_mint_id` above.  This file used to carry its own copy, and the two
# drifted exactly the way goal:s14 predicted when it closed with "there are two
# `write_frontmatter` definitions ... S13's finding applies with double force to
# a function that exists twice."
#
# What the drift had already cost, measured before collapsing: the copy here
# was missing BOTH null round-trip fixes the canonical one grew on 2026-08-25.
# A `None` list entry came back as the literal string "None", and a YAML-null
# scalar came back as "None" too -- silent data corruption, in the writer that
# touches all 159 build-site nodes on every single loop iteration.  Collapsing
# fixes that as a side effect rather than as a separate repair, which is the
# argument for collapsing rather than re-syncing by hand a third time.
write_frontmatter = _sg.write_frontmatter


def load_existing_nodes() -> dict:
    """Load all existing nodes. Returns dict keyed by node id.
    Each value: {path: Path, origin: str, fm: dict}
    """
    nodes = {}
    if not NODES_DIR.exists():
        return nodes
    for md_path in NODES_DIR.rglob("*.md"):
        try:
            text = md_path.read_text(encoding="utf-8")
            if text.strip().startswith("---"):
                parted = split_frontmatter(text)
                if parted is not None:
                    fm = yaml.safe_load(parted[0]) or {}
                    node_id = fm.get("id", "")
                    if node_id:
                        nodes[node_id] = {
                            "path": md_path,
                            "origin": fm.get("origin", ""),
                            "fm": fm,
                        }
        except Exception:
            pass
    return nodes


def parse_tasks() -> list[dict]:
    """Parse build-site.md into a list of task dicts."""
    if not BUILD_SITE.exists():
        print(f"ERR: build site not found: {BUILD_SITE}", file=sys.stderr)
        sys.exit(1)
    text = BUILD_SITE.read_text(encoding="utf-8")
    lines = text.splitlines()
    tasks: list[dict] = []
    current: dict | None = None
    current_tier = -1
    for line in lines:
        m_tier = TIER_RE.match(line)
        if m_tier:
            current_tier = int(m_tier.group(1))
            continue
        m_task = TASK_RE.match(line)
        if m_task:
            if current is not None:
                tasks.append(current)
            current = {
                "id": m_task.group(1),
                "title": m_task.group(2).strip(),
                "tier": current_tier,
                "status": "pending",
                "blocked_by": [],
                "acceptance_criteria": [],
                "cavekit_req": "",
                "effort": "M",
                "body": [],
            }
            continue
        if current is None:
            continue
        m_field = FIELD_RE.match(line)
        if m_field:
            key = m_field.group("key").strip().lower().replace(" ", "_")
            val = m_field.group("val").strip()
            if key == "cavekit_requirement":
                current["cavekit_req"] = val
            elif key == "blockedby":
                if val.lower() == "none":
                    current["blocked_by"] = []
                else:
                    current["blocked_by"] = [v.strip() for v in val.split(",")]
            elif key == "acceptance_criteria_mapped":
                current["acceptance_criteria"] = [v.strip() for v in val.split(",")]
            elif key == "effort":
                current["effort"] = val
            elif key == "description":
                current["body"].append("**Description:** " + val)
            elif key == "files":
                current["body"].append("**Files:** " + val)
            elif key == "test_strategy":
                current["body"].append("**Test Strategy:** " + val)
        elif current["body"] and line.strip().startswith("-"):
            current["body"].append(line)
    if current is not None:
        tasks.append(current)
    return tasks


def parse_kits() -> tuple[list[dict], list[dict]]:
    """Return (domains, requirements)."""
    domains: list[dict] = []
    requirements: list[dict] = []
    for kit_path in sorted(KITS_DIR.glob("cavekit-*.md")):
        if kit_path.name == "cavekit-overview.md":
            continue
        domain = kit_path.stem.replace("cavekit-", "")
        text = kit_path.read_text(encoding="utf-8")
        scope_match = re.search(r"## Scope\s*\n+(.+?)(?=\n##)", text, flags=re.DOTALL)
        scope = scope_match.group(1).strip() if scope_match else domain
        domains.append({
            "id": f"idea:domain-{domain}",
            "title": f"Domain: {domain}",
            "body": scope,
            "scale": "big",
        })
        # Pull each ### Rn block
        for m in re.finditer(
            r"^### (R\d+):\s+(.+?)\n(.+?)(?=\n### |\Z)", text, flags=re.DOTALL | re.MULTILINE
        ):
            rnum = m.group(1)
            rtitle = m.group(2).strip()
            rbody = m.group(3).strip()
            requirements.append({
                "id": f"hyp:{domain}-{rnum.lower()}",
                "title": f"{domain}/{rnum}: {rtitle}",
                "domain": domain,
                "rnum": rnum,
                "body": rbody,
                "testable_claim": rtitle,
            })
    return domains, requirements


def main() -> int:
    # goal:g5 / L18 — a project is legitimate at three depths: goals only,
    # goals + seed ideas, goals + build site. A goals-only project is a valid
    # state, not a broken one, so a missing build site must degrade the way a
    # missing GOALS.md already does.
    #
    # Two separate defects are closed by returning here, and the second is the
    # dangerous one:
    #   1. `sys.exit(1)` from parse_tasks aborted the whole driver, because
    #      driver.sh runs under `set -euo pipefail` and pipes this through
    #      `tee`. A build-site-less project could not run the loop at all.
    #   2. Falling through with zero tasks would reach the stale-prune below,
    #      which unlinks every `origin: build-site` node not rewritten this
    #      run. With nothing parsed, that is the whole build-site corpus —
    #      159 of 661 nodes in agi-tree. Returning *before* any write or
    #      unlink is what makes this safe (H0i).
    if not BUILD_SITE.exists():
        print(f"no build site at {BUILD_SITE} — goals-only project, nothing to "
              "snapshot (L18). Wrote 0 nodes, pruned 0.")
        return 0

    # Load existing nodes (preserve agent-generated, track build-site-owned)
    existing = load_existing_nodes()
    written: set = set()

    domains, reqs = parse_kits()
    tasks = parse_tasks()

    # 1. Idea nodes (one per domain)
    for d in domains:
        slug = slugify(d["title"])
        write_frontmatter(
            NODES_DIR / "idea" / f"{slug}.md",
            {
                "id": d["id"],
                "type": "idea",
                "title": d["title"],
                "scale": d["scale"],
                "tags": ["domain", "seed"],
                "status": "open",
                "confidence": 1.0,
            },
            d["body"],
            origin="build-site",
            preserve=existing.get(d["id"], {}).get("fm"),
        )
        _upsert_node_to_db(d["id"], {
            "id": d["id"],
            "type": "idea",
            "title": d["title"],
            "scale": d["scale"],
            "tags": ["domain", "seed"],
            "status": "open",
            "confidence": 1.0,
        }, d["body"], origin="build-site")
        written.add(d["id"])

    # 2. Hypothesis nodes (one per cavekit requirement)
    for r in reqs:
        slug = slugify(f"{r['domain']}-{r['rnum']}-{r['title']}")
        write_frontmatter(
            NODES_DIR / "hypothesis" / f"{slug}.md",
            {
                "id": r["id"],
                "type": "hypothesis",
                "title": r["title"],
                "parents": [f"idea:domain-{slugify(r['domain'])}"],
                "testable_claim": r["testable_claim"],
                "tags": [r["domain"], r["rnum"]],
                "confidence": 0.5,
                "subgraph": False,
            },
            r["body"][:2000],  # cap body size
            origin="build-site",
            preserve=existing.get(r["id"], {}).get("fm"),
        )
        _upsert_node_to_db(r["id"], {
            "id": r["id"],
            "type": "hypothesis",
            "title": r["title"],
            "parents": [f"idea:domain-{slugify(r['domain'])}"],
            "testable_claim": r["testable_claim"],
            "tags": [r["domain"], r["rnum"]],
            "confidence": 0.5,
            "subgraph": False,
        }, r["body"][:2000], origin="build-site")
        written.add(r["id"])

    # 3. Task nodes (one per T-NNN)
    for t in tasks:
        slug = slugify(f"{t['id'].lower()}-{t['title']}")
        # Map cavekit_req like "graph-core/R1" → hyp parent id
        parent_hyp = ""
        if "/" in t["cavekit_req"]:
            domain, rnum = t["cavekit_req"].split("/", 1)
            rnum = rnum.split(".")[0]  # R1.2 → R1
            parent_hyp = f"hyp:{domain}-{rnum.lower()}"
        write_frontmatter(
            NODES_DIR / "task" / f"{slug}.md",
            {
                "id": f"task:{t['id'].lower()}",
                "type": "task",
                "title": f"{t['id']}: {t['title']}",
                "cavekit_req": t["cavekit_req"],
                "acceptance_criteria": t["acceptance_criteria"][:5],
                "blocked_by": [f"task:{b.lower()}" for b in t["blocked_by"]],
                "effort": t["effort"],
                "tier": t["tier"],
                "status": "pending",
                "parents": [parent_hyp] if parent_hyp else [],
                "tags": [t["effort"], f"tier-{t['tier']}"],
            },
            "\n\n".join(t["body"]),
            origin="build-site",
            preserve=existing.get(f"task:{t['id'].lower()}", {}).get("fm"),
        )
        _upsert_node_to_db(f"task:{t['id'].lower()}", {
            "id": f"task:{t['id'].lower()}",
            "type": "task",
            "title": f"{t['id']}: {t['title']}",
            "cavekit_req": t["cavekit_req"],
            "acceptance_criteria": t["acceptance_criteria"][:5],
            "blocked_by": [f"task:{b.lower()}" for b in t["blocked_by"]],
            "effort": t["effort"],
            "tier": t["tier"],
            "status": "pending",
            "parents": [parent_hyp] if parent_hyp else [],
            "tags": [t["effort"], f"tier-{t['tier']}"],
        }, "\n\n".join(t["body"]), origin="build-site")
        written.add(f"task:{t['id'].lower()}")

    # Delete stale build-site nodes (exist but not written this run)
    stale = [
        node["path"]
        for node_id, node in existing.items()
        if node["origin"] == "build-site" and node_id not in written
    ]
    for path in stale:
        path.unlink(missing_ok=True)
        print(f"removed stale: {path}")

    print(f"wrote: {len(domains)} idea + {len(reqs)} hypothesis + {len(tasks)} task = "
          f"{len(domains) + len(reqs) + len(tasks)} nodes")
    print(f"target dir: {NODES_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
