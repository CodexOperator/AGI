#!/usr/bin/env python3
"""completion.py — is the node finished? One shared function, harness-blind.

mvp:unified-spawn-path clause 5: *the finish signal is the scaffolded node
acquiring real content* — not a pid (`heal.py` polls those), not `agent.json`
(`cli.py done` writes it), not a harness name. Both of those are the pi
process model wearing a general name: a Claude Code kid has no pid to poll,
and a kid that wrote its node and then died looks *identical* to one that
never started (the 2026-08-31 field note is that failure, already observed).

`is_complete(root, node_id)` is the one completion check. It reads the node
file and nothing else:

  primary   the node's `scaffold_hash` frontmatter, stamped by
            `node_writer.write_node` at write time. Complete = the body's
            hash differs from the stamp. Drift-safe: a changed `BODY_PROMPTS`
            cannot make an untouched scaffold look filled.
  fallback  nodes scaffolded before the field existed: compare the body
            against the placeholder regenerated from the current
            `BODY_PROMPTS`. Weaker — a template change makes an untouched
            legacy scaffold look complete. The stamp exists to retire this
            fallback, not to replace it.

`cli.py done` is demoted from *the definition of done* to *one way to
announce it*: it stamps the verdict frontmatter, and this module does not
look at it. A kid that filled its node and died before running `done` is
complete here — that is falsifier 4 of the MVP.

`heal.py`'s finished-detection is out of scope until `goal:g4.7`; this file
is what that goal ports rather than re-invents.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import node_writer  # noqa: E402


def scaffold_body_for(node_id: str) -> str:
    """The placeholder body a fresh `node_id` opens with.

    The same two parts `node_writer.write_node` joins — the `# <node-id>`
    heading plus the type's `BODY_PROMPTS` entry — recomputed from the id so
    a legacy node (no `scaffold_hash`) can be checked without its original
    write.
    """
    if ":" not in node_id:
        return ""
    ntype = node_writer.canonical_node_type(node_id.split(":", 1)[0])
    return f"\n# {node_id}\n\n" + node_writer.BODY_PROMPTS.get(ntype, "")


def is_complete(root: Path, node_id: str) -> bool:
    """True once the scaffolded node has acquired real content.

    There is no pid, no `agent.json`, no manifest and no harness name in this
    file — the finish is a graph event, observable identically on every
    harness, and a kid killed after its node landed but before `cli.py done`
    is still counted complete.
    """
    path = node_writer.find_node_file(Path(root), node_id)
    if path is None or not path.exists():
        return False
    parts = path.read_text(encoding="utf-8").split("---", 2)
    if len(parts) < 3:
        return False  # no frontmatter — not a node this function recognizes
    import yaml
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        # A node whose frontmatter will not parse is not a finished node, and
        # this is a PREDICATE -- it answers True or False, it does not get to
        # take the caller down. `post_wire.cmd_wire` calls this inside its
        # agent loop, so a raise here would lose the whole iteration's wiring
        # rather than one node. That is a regression this file introduced on
        # 2026-09-01 by acquiring its first caller: with zero callers the raise
        # was unreachable.
        #
        # `skip_quiet` is the right policy HERE and is not a vote on the
        # unified reader's default (`hypothesis:a00-6b4ad6b2-a60b78` is
        # deciding that): a boolean predicate has exactly one safe answer for
        # input it cannot read.
        return False
    stored = fm.get("scaffold_hash") if isinstance(fm, dict) else None
    body = parts[2]
    if isinstance(stored, str) and stored.strip():
        return node_writer.scaffold_hash(body) != stored
    return (node_writer.scaffold_hash(body)
            != node_writer.scaffold_hash(scaffold_body_for(node_id)))


def owns_all_complete(root: Path, node_ids) -> bool:
    """True when every node an agent is responsible for is complete. `goal:s27`.

    **A parent's completion is its kids' completion, propagated.** The owner's
    framing, and it is better than the alternatives it replaced: a parent is
    not nodeless, it is responsible for its children's nodes the way a real
    parent is responsible for its children rather than for some separate
    object of its own.

    That keeps completion a **graph event** on the same terms as
    `is_complete` — every id here is checked by the same predicate, with no
    pid, no `agent.json` and no harness name anywhere in the decision. Tier is
    a first-class concept in this engine; a harness name is not. Branching on
    the first is not the thing `goal:g4.6` forbids.

    **Empty is not complete.** A parent that spawned nothing and reviewed
    nothing has not finished its loop — it failed to start one. Returning True
    for an empty list would make the most common parent failure mode
    indistinguishable from success, which is exactly the shape of defect that
    hid the dropped-verdict bug for the whole life of the pi runtime.
    """
    ids = [n for n in (node_ids or []) if isinstance(n, str) and n.strip()]
    if not ids:
        return False
    return all(is_complete(root, n.strip()) for n in ids)


if __name__ == "__main__":
    import argparse
    import locations

    def main(argv: list[str] | None = None) -> int:
        p = argparse.ArgumentParser(
            prog="completion.py",
            description="Is the node finished? Exit 0 if complete, 1 if not and "
                        "reachable, 2 if the root is unresolvable.")
        p.add_argument("root", help="project root or any path inside it")
        p.add_argument("node_id", help="node id to check, e.g. experiment:x")
        args = p.parse_args(argv)
        r = Path(args.root)
        root = locations.find_project_root(r) or r
        return 0 if is_complete(root, args.node_id) else 1

    sys.exit(main())
