#!/usr/bin/env python3
"""glitch_master.py — the Glitch Master seat (hypothesis:l3w4-bug-master-seat).

The strict graph-submission review Master. On a round landing the director
that asked summons it; it runs agi-round-review.js, takes the returned
{iter, global, targets} JSON and this script posts it to the tier3-quorum
room. This file is the pure half of the seat: it never spawns, never runs a
real reviewer, never touches the launch machinery. It only FORMATS.

Usage:

    workflow.py run review --harness pi --args '{iter,targets}'  # the reviewer
      | glitch_master.py format-record --iter <id> [--root GRAPH_ROOT]

`format-record` reads the workflow JSON on stdin, writes it VERBATIM to
`.agi/sessions/iter-<id>/review/results.json`, and prints one REVIEW line per
target plus one GLOBAL line, each shaped for:

    send.py send --room tier3-quorum --from glitch-master

Pure and side-effect-light. The two standing prohibitions hold by
construction: it does not install a row in config:seats (that is the
Sanctuary Master's), and it does not start a seat — it is a formatter, not
a runner. A normal `--dry-run` review needs no spawn of this seat at all.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:  # runs from extensions/agi/bin/ as part of the package
    from . import locations
except ImportError:  # runs as a plain script from a checkout
    import locations  # type: ignore

MSG_PREFIX = "[glitch-master] "


def _read_json() -> dict:
    """Read and parse the workflow JSON from stdin, verbatim-capable."""
    raw = sys.stdin.read()
    if not raw.strip():
        print(f"{MSG_PREFIX}no JSON on stdin", file=sys.stderr)
        sys.exit(2)
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        print(f"{MSG_PREFIX}bad JSON on stdin: {exc}", file=sys.stderr)
        sys.exit(2)


def _out_dir(root: Path, iter_id: str) -> Path:
    """`.agi/sessions/iter-<id>/review/` — the single result drop-point.

    `root` here is the REPO root, not the graph root: this function appends
    `/.agi/sessions/...` itself, so handing it the graph root `<repo>/.agi`
    would double the `.agi`. `format_record` normalizes with
    `locations.repo_root` before calling here.
    """
    return root / ".agi" / "sessions" / f"iter-{iter_id}" / "review"


def format_record(args: argparse.Namespace) -> int:
    """Write stdin JSON verbatim; print N REVIEW lines + one GLOBAL line.

    Exit code 0 on success. `--iter` names the round and the output
    directory; `--root` is the graph root or repo root (defaults to nearest
    enclosing `.agi/`) and is normalized to the repo root so the `.agi/`
    here is never doubled. `--out` overrides the whole results path for tests.
    """
    data = _read_json()
    iter_id = args.iter_data or data.get("iter") or "?"
    root = Path(args.root).resolve() if args.root else locations.find_project_root(
        Path.cwd().resolve())
    if root is None:
        print(f"{MSG_PREFIX}could not resolve graph root", file=sys.stderr)
        return 1
    # `_out_dir` appends `/.agi/sessions/...`, so it must be handed the REPO
    # root. `find_project_root` yields the GRAPH root (`<repo>/.agi`), and a
    # caller passing the graph root per the docstring does too; feeding that
    # straight into `_out_dir` doubles the `.agi` into
    # `<repo>/.agi/.agi/sessions/iter-<id>/review`. Normalize with
    # `locations.repo_root` (identity for a repo-root input), keeping the
    # resolved drop-point at `<repo>/.agi/sessions/iter-<id>/review`.
    root = locations.repo_root(root)

    target = data.get("targets", []) or []
    global_rec = data.get("global") or {}

    out_path = Path(args.out) if args.out else (_out_dir(root, iter_id) / "results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data), encoding="utf-8")

    for t in target:
        print(_review_line(iter_id, t))
    print(_global_line(iter_id, global_rec))
    return 0


def _review_line(iter_id: str, t: dict) -> str:
    """One `REVIEW ...` line, shaped for send.py send --room tier3-quorum."""
    files_changed = t.get("files_changed") or []
    overclaims = t.get("overclaims") or []
    open_gaps = t.get("open_gaps") or []
    return (
        f"REVIEW iter={iter_id} target={t.get('hypothesis', '?')} "
        f"verdict={t.get('verdict', '?')} "
        f"overclaims={len(overclaims)} open_gaps={len(open_gaps)} "
        f"files_changed={len(files_changed)} "
        f'summary="{t.get("summary", "")}"'
    )


def _global_line(iter_id: str, g: dict) -> str:
    """One `GLOBAL ...` line; guard is `clean` iff guard_output is empty."""
    guard_output = g.get("guard_output") or ""
    guard = "clean" if not str(guard_output).strip() else f"WARN:{len(str(guard_output).splitlines())}"
    return (
        f"GLOBAL iter={iter_id} links_broken={g.get('links_broken', 0)} "
        f"suite={g.get('suite_passed', 0)}/{g.get('suite_failed', 0)}/"
        f"{g.get('suite_skipped', 0)} guard={guard} "
        f'summary="{g.get("summary", "")}"'
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="glitch_master.py",
        description="Glitch Master seat review formatter: workflow JSON -> REVIEW/GLOBAL lines.",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    fr = sub.add_parser("format-record", help="format agi-round-review.js output for the quorum room")
    fr.add_argument("--iter", dest="iter_data", type=str, default="",
                    help="round/iteration id; also names the output dir (defaults to payload iter)")
    fr.add_argument("--root", type=str, default=None,
                    help="graph root or repo root (defaults to nearest "
                         "enclosing .agi/); normalized to the repo root")
    fr.add_argument("--out", type=str, default=None,
                    help="override the whole results path (tests)")
    fr.set_defaults(func=format_record)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())