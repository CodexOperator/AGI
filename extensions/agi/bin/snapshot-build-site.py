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
PROJECT_ROOT = Path(
    os.environ.get("AGI_TREE_PROJECT_ROOT")
    or os.environ.get("AUTORESEARCH_TREE_PROJECT_ROOT")  # legacy, rename window
    or os.environ.get("PROJECT_ROOT")
    or os.getcwd()
).resolve()

# Canonical name first; the legacy name stays accepted during the rename window.
CONFIG_NAMES = ("agi-tree.config.json", "autoresearch-tree.config.json")


def config_path(root: Path) -> Path | None:
    """First existing config file in `root`, or None if it is not a project."""
    for name in CONFIG_NAMES:
        p = root / name
        if p.exists():
            return p
    return None
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
                from graph_core.persistence.sqlite_backend import SQLiteBackend
                _upsert_node_to_db._backend = SQLiteBackend(db_path)
    if _upsert_node_to_db._backend is None:
        return
    from graph_core.persistence.frontmatter import NodeFile
    fm = dict(fm)
    fm["id"] = node_id
    fm["origin"] = origin
    nf = NodeFile(frontmatter={**fm, "body": body}, body=body, suffix=".json")
    _upsert_node_to_db._backend.save(node_id, nf)


def write_frontmatter(path: Path, fm: dict, body: str, origin: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if origin:
        fm = dict(fm)  # copy so we don't mutate caller's dict
        fm["origin"] = origin
    lines = ["---"]
    for k in sorted(fm.keys()):
        v = fm[k]
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    lines.append(f"  - {item}")
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        else:
            sval = str(v).replace("\n", " ").strip()
            if any(c in sval for c in ":#'\""):
                sval = '"' + sval.replace('"', "'") + '"'
            lines.append(f"{k}: {sval}")
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


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
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1]) or {}
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
