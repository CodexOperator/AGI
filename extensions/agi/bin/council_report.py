#!/usr/bin/env python3
"""council_report.py -- ONE report row per council round + ONE leaf row per
verify residue (hypothesis:g716105-...-routes-residues). `add --run KEY --args
FILE [--root R]`. Residues come from VERIFY, never the review list alone
(skill agi-merge-pass S4): `missed[]` are residues, `refuted: true` is not,
review defects only when there is no verify file. Owner = the parent goal
title's `(assigned: <post>)`, else the commit subject's post, else
director-engine; the Prime never owns a residue. The leaf is the ONE cell
`council.residue_leaves`; absent = rc 2 naming it. Writes go through write.py.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "src"))

import frontmatter  # noqa: E402
import node_writer  # noqa: E402
from graph_core.persistence import frontmatter as fm_reader  # noqa: E402

LEAF_CELL = "council.residue_leaves"
REPORT_NODE = "doc:council-report"
PRIME_POST = "belam"
FALLBACK_POST = "director-engine"
HEADER = ("| round | old..new | state | verdict | residues | reds |",
          "|---|---|---|---|---|---|")
RESIDUE_HEADER = ("| round | source | residue |", "|---|---|---|")


def rounds(rundir: Path) -> list[dict]:
    """One dict per LABEL: {label, state, verdict, residues[(title, source)]}."""
    labels = sorted({p.name.split("_", 1)[1][:-5] for p in rundir.glob("*.json")
                     if p.name.startswith(("review_", "verify_"))})
    out = []
    for label in labels:
        review, verify = _read(rundir / f"review_{label}.json"), _read(
            rundir / f"verify_{label}.json")
        residues, verdict, state = [], "", "REVIEWED:review-only"
        if verify:
            state, verdict = "REVIEWED", str(verify.get("final_recommendation", ""))
            residues = [(_title(v.get("defect")), "verify")
                        for v in verify.get("verdicts", []) if not v.get("refuted")]
            residues += [(str(m), "verify") for m in verify.get("missed", [])]
        else:
            verdict = str(review.get("verdict_recommendation", ""))
            residues = [(str(d.get("title", "")), "review-only")
                        for d in review.get("defects", [])
                        if d.get("severity") == "residue"]
        out.append({"label": label, "state": state, "verdict": verdict,
                    "residues": residues})
    return out


def _read(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def _title(defect) -> str:
    return str(defect.get("title", "")) if isinstance(defect, dict) else str(defect)


def owner_post(assigned: str, subject: str) -> str:
    """The ONE owner of a round's residues; the Prime never owns one."""
    m = re.search(r"\(assigned:\s*([\w-]+)\)", assigned or "")
    m = m or re.search(r"\(([\w-]+)\)\s*$", (subject or "").strip())
    post = (m.group(1) if m else "") or FALLBACK_POST
    return FALLBACK_POST if post == PRIME_POST else post


def leaf_for(post: str, cell: dict) -> str:
    """The owner's leaf from the ONE cell; a post absent = `default`."""
    return str(cell.get(post) or cell.get("default") or "")


def cell_of(root: Path) -> dict:
    """The `council` -> `residue_leaves` table; no table and no leaves are the
    SAME absence. `root` is the GRAPH root (the `.agi` dir locations resolves)."""
    cell = (json.loads((root / "config.json").read_text()).get("council")
            or {}).get("residue_leaves")
    if not isinstance(cell, dict):
        raise KeyError(LEAF_CELL)
    return cell


def merge_table(body: str, new_rows: list[str], header: tuple,
                unique: bool = False) -> str:
    """Fold new_rows into the node's ONE table.

    The key is the FIRST cell -- the round -- so a re-add of a round REPLACES
    its row instead of duplicating it. A residue leaf carries MANY rows per
    round, so `unique=True` keys the whole row there: one row per residue.
    """
    key = (lambda r: r) if unique else (lambda r: r.split("|")[1].strip())
    lines = body.splitlines()
    tbl = [i for i, line in enumerate(lines) if line.strip().startswith("|")]
    rows = {key(lines[i]): lines[i] for i in tbl[2:]}
    for row in new_rows:
        rows[key(row)] = row
    keep = [l for l in lines if not l.strip().startswith("|")]
    while keep and not keep[-1].strip():
        keep.pop()
    return "\n".join(keep + ["", *header]
                     + [rows[k] for k in sorted(rows)]).rstrip("\n") + "\n"


def node_body(root: Path, node_id: str) -> str:
    """The node body as write.py's `replace body` sees it -- the CANONICAL
    reader (`load_node_file(...).body`), not `split_frontmatter`, whose body
    keeps the blank line after the closing `---` and would offset every range."""
    path = node_writer.find_node_file(root, node_id)
    return fm_reader.load_node_file(path).body if path else ""


def _title_of(root: Path, node_id: str) -> str:
    """The node's frontmatter title, else its H1, else "" (never raises)."""
    path = node_writer.find_node_file(root, node_id) if node_id else None
    if path is None:
        return ""
    text = path.read_text()
    fm = frontmatter.read_frontmatter(text) or {}
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return str(fm.get("title") or (m.group(1) if m else ""))


def write_body(root: Path, node_id: str, body: str) -> None:
    """The ONE writer: write.py `replace body 1:<n>` on the whole body (the
    sanctioned splice; `body_patch`'s splitter refuses a body whose last line
    has no newline of its own). An unchanged body writes nothing, and a refusal
    is LOUD, never a silent no-op."""
    old = node_body(root, node_id)
    if old == body:
        return
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as fh:
        fh.write(body)
        tmp = fh.name
    proc = subprocess.run(
        [sys.executable, str(_HERE / "write.py"), node_id,
         f"replace body 1:{max(1, len(old.splitlines()))} {tmp}"],
        text=True, cwd=root if root.name != ".agi" else root.parent,
        capture_output=True, check=False)
    os.unlink(tmp)
    if proc.returncode != 0:
        raise SystemExit(f"council_report: write.py refused the {node_id} row: "
                         f"{(proc.stderr or proc.stdout).strip()}")


def add(root: Path, run_key: str, args: dict, writer=write_body) -> list[str]:
    """Write the report rows and route the residues. Returns the messages."""
    try:
        cell = cell_of(root)
    except KeyError as exc:
        raise SystemExit(f"council_report: config cell {exc} is absent — add it "
                         "(default goal:g7.33.19) before routing any residue")
    runs_root = root / args.get("runs_root", "sessions/workflows/runs")
    report = args.get("report_node", REPORT_NODE)
    assigned = _title_of(root, args.get("parent", ""))
    old, new = args.get("old", "?"), args.get("new", "?")
    leaf = leaf_for(owner_post(assigned, args.get("subject", "")), cell)
    out, cache = [], {}

    def body_of(node_id: str) -> str:
        """ONE read per node per add, and the FOLDED body afterwards: the next
        row of the same run merges onto the rows already written, never onto a
        stale copy that would drop them."""
        if node_id not in cache:
            cache[node_id] = node_body(root, node_id)
        return cache[node_id]

    for r in rounds(runs_root / run_key):
        key = f"{run_key}/{r['label']}"
        row = (f"| {key} | {old}..{new} | {r['state']} | {r['verdict']} | "
               f"{len(r['residues'])} | unchecked |")
        cache[report] = merge_table(body_of(report), [row], HEADER)
        writer(root, report, cache[report])
        for title, source in r["residues"]:
            cache[leaf] = merge_table(body_of(leaf),
                                      [f"| {key} | {source} | {title} |"],
                                      RESIDUE_HEADER, unique=True)
            writer(root, leaf, cache[leaf])
            out.append(f"{key}: {source} residue -> {leaf} ({title})")
        out.append(f"{key}: {row}")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    add_p = sub.add_parser("add", help="one row per round, residues to owners")
    for flag in ("--run", "--args"):
        add_p.add_argument(flag, required=True)
    add_p.add_argument("--root", default="", help="project root")
    ns = ap.parse_args(argv)
    args = json.loads(Path(ns.args).read_text())
    root = Path(ns.root).resolve() if ns.root else Path.cwd()
    try:
        for line in add(_graph_root(root), ns.run, args):
            print(line)
    except SystemExit as exc:
        print(exc)
        return 2
    return 0


def _graph_root(root: Path) -> Path:
    return root if (root / "nodes").is_dir() else root / ".agi"


if __name__ == "__main__":
    raise SystemExit(main())