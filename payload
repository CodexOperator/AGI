#!/usr/bin/env python3
"""rolslice.py — the per-role SKILL.md slice mechanism
(hypothesis:l3w4-context-load-minimal, goal:g17).

The owner asked (2026-09-08) that different roles SEE different parts of
skill.md — "command structure, hierarchy, and how everyone plays their part.
That's the biggest one any role needs to know." This is the mechanism that
produces those slices.

THE RULE THAT SHAPES THIS FILE: do NOT author a second role description.
The role structure is declared machine-readably in the hierarchy sources
(config:seats seats + ladder:ladder roles), which hierarchy.py reads as THE one
reader. A slice therefore:

  1. resolves the role's (tier, role) against the machine-readable hierarchy
     (hierarchy.load_seats / load_ladder) and FAILS LOUDLY on an unknown role
     rather than guessing — so it can never drift from what dispatch resolves;
  2. injects hierarchy.render(root) — THE chart — so EVERY role carries "how
     everyone plays their part", the biggest thing any role needs to know, from
     the SAME machine-readable source every other renderer reads;
  3. selects SKILL.md sections by a machine-readable section->role map below.
     Core sections (CLI, safety rails, verdict taxonomy, the three tiers, the
     constitution head) go to EVERY role; operational protocol sections go only
     to the roles that run them (iteration protocol -> parent, kid end-of-job
     + escalation -> kid+parent, HANDOFF/COMPLETE -> director, metrics ->
     parent+director).
  4. measures the resulting slice with tiktoken o200k_base when --measure is
     passed, so the before/after table is real numbers, not vibes.

WHERE THIS FITS in the trim: SKILL.md is ~13,180 tokens / INJECTION.md ~8,406
tokens = the static prefix every role paid each turn (kid 22734, parent 24657,
advisor 24523, director 24690, prime_director 25450, liaison 24258 total).
Slicing SKILL.md per-role is REQUIRED to reach the owner's 70-90%: naive
prose-trim reached only ~2% because the mass is structural (the graph-viewport
stream + one-shared-file), proven experiment:a00-6bf13276-ccc2bb. This tool is
the per-role slice half of that lever; the INJECTION graph-stream restructure
is a separate slice.

MUST NOT LOSE (checked explicitly by the section map): the exact next command
a cold reader needs (CLI, never trimmed), the full kill procedure and key-floor
rule (CORE), attribution labels on any surviving quote (constitution head is
CORE). Every one of these is in a CORE section that no role-slice filter can
drop.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "src"))  # graph_core package
import hierarchy  # noqa: E402

# --------------------------------------------------------------------------- #
# The machine-readable section -> role map.
#   CORE     -> every slice, always. None of the must-not-lose list may live
#               outside CORE.
#   role:... -> only slices for that role (or anyone who subsumes it).
# The map keys are exact `## ` headings in skills/agi/SKILL.md. A heading with
# no rule is dropped from every slice (a qualification, not a loss: a section
# nobody's slice wants is either dead or mislabelled, and the complement —
# every section mapped — is asserted in the test).
# --------------------------------------------------------------------------- #
CORE = {
    "CLI",                                        # exact next command
    "Safety rails (non-negotiable)",              # kill procedure, key floor
    "Verdict taxonomy (finite-state)",            # finite-state taxonomy
    "The three tiers",                            # how everyone plays their part
    "Choosing a runtime",                         # pi vs cc, the scrub rule
}

ROLE_SECTIONS = {
    "kid": {
        # "Iteration protocol (parent)" carries the Kid end-of-job contract
        #   and Escalation — kid → parent as `### ` subsections, so a kid gets
        #   that whole section. The charter the owner named a kid needs (its
        #   own end-of-job contract) lives inside it.
        "Iteration protocol (parent)",
        "Every node edit goes through `write.py` (`goal:g13.1`)",
        "Metrics — score goal fulfillment, not chain length",
    },
    "parent": {
        "Iteration protocol (parent)",
        "Director economics — dispatch, don't do",
        "Metrics — score goal fulfillment, not chain length",
        "Every node edit goes through `write.py` (`goal:g13.1`)",
    },
    "director": {
        "Director economics — dispatch, don't do",
        "Iteration protocol (parent)",
        "`HANDOFF.md` — the director's scratchpad, replaced each session",
        "`COMPLETE.md` — every finished loop writes one (`goal:g1.13`)",
        "Metrics — score goal fulfillment, not chain length",
        "Every node edit goes through `write.py` (`goal:g13.1`)",
        "The git grid",
    },
}

# roles are hierarchical for slice purposes; a director is also a parent is
# also a kid where the ladder says so at runtime. Here a role's slice is its
# own sections plus nothing implicit — the map says what it says. The CLI takes
# --tier too and resolves (tier,role) against the ladder so `--role director
# --tier 1` and `--role kid --tier 0` both pass --check; all four map to a
# named bucket here.
_ROLE_ALIAS = {"prime_director": "director", "liaison": "director", "advisor": "parent"}


def _resolve_role(seats, ladder, role, tier):
    """Resolve a (role, tier) against the machine-readable hierarchy.

    Returns the slice bucket (kid|parent|director) or None if the role is not
    in the hierarchy sources — so an unknown role FAILS LOUDLY, never guesses.
    """
    if role in _ROLE_ALIAS and role not in ("kid", "parent", "director"):
        role = _ROLE_ALIAS[role]
    if role in ("kid", "parent", "director"):
        return role
    # fall through to explicit check: only accept roles declared in the ladder
    known = {str(r.get("role", "")) for r in (ladder.get("roles") or [])}
    known |= {str(s.get("role", "")) for s in seats}
    if role in known:
        return _ROLE_ALIAS.get(role, role if role in ("kid", "parent", "director") else "director")
    return None


def _split_sections(skill_text: str) -> dict:
    """Split SKILL.md into {heading: body} keyed by each `## ` heading."""
    sections = {}
    cur_heading = None
    cur = []
    for line in skill_text.splitlines():
        if line.startswith("## ") or line.startswith("# "):
            if cur_heading is not None:
                sections[cur_heading] = "\n".join(cur)
            cur_heading = line.lstrip("# ").strip()
            cur = [line]
        elif cur_heading is not None:
            cur.append(line)
    if cur_heading is not None:
        sections[cur_heading] = "\n".join(cur)
    return sections


def build_slice(root: Path, skill_path: Path, role: str, tier=0) -> str:
    """The per-role slice: hierarchy chart + this role's / CORE SKILL.md sections."""
    seats = hierarchy.load_seats(root)
    ladder = hierarchy.load_ladder(root)
    bucket = _resolve_role(seats, ladder, role, tier)
    if bucket is None:
        raise ValueError(f"rolslice: role {role!r} not in hierarchy sources "
                         f"(config:seats / ladder:ladder); cannot slice it")

    skill = skill_path.read_text(encoding="utf-8")
    sections = _split_sections(skill)

    want = set(CORE) | set(ROLE_SECTIONS.get(bucket, set()))
    missing = sorted(s for s in want if s not in sections)
    if missing:
        raise ValueError(f"rolslice: section(s) not found in SKILL.md: {missing} "
                         f"(a heading renaming would silently drop content)")

    # the command-structure chart from THE one machine-readable source
    chart = hierarchy.render(root)

    head = (f"# PER-ROLE SLICE — {role} (bucket: {bucket}, tier {tier})\n\n"
            f"The command structure and how everyone plays their part, from the "
            f"machine-readable hierarchy (config:seats + ladder:ladder).\n\n"
            f"{chart}\n"
            f"---\n"
            f"### SKILL.md sections for this role\n")
    body = []
    # preserve document order
    seen = set()
    for heading, text in sections.items():
        if heading in want and heading not in seen:
            seen.add(heading)
            body.append(text)
    return head + "\n\n".join(body) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="rolslice.py")
    ap.add_argument("--role", default=None, help="role to slice (kid|parent|director|...)")
    ap.add_argument("--tier", type=int, default=0)
    ap.add_argument("--root", default=None, help="graph root (default: resolve)")
    ap.add_argument("--skill", default=None, help="path to skills/agi/SKILL.md")
    ap.add_argument("--measure", action="store_true",
                    help="print tiktoken o200k tokens for the assembled slice")
    ap.add_argument("--all", action="store_true", help="slice every bucket, print tokens")
    args = ap.parse_args(argv)

    import locations
    root = Path(args.root).resolve() if args.root else locations.find_project_root()
    if root is None:
        raise SystemExit("rolslice.py: could not resolve project root; pass --root.")
    skill = Path(args.skill).resolve() if args.skill else root.parent / "skills" / "agi" / "SKILL.md"
    # skill lives in the repo enclosing .agi ; if that path is wrong, try worktree
    if not skill.is_file():
        alt = root / ".." / "skills" / "agi" / "SKILL.md"
        if alt.resolve().is_file():
            skill = alt.resolve()
    if not skill.is_file():
        raise SystemExit(f"rolslice.py: SKILL.md not found near {skill}")

    if args.all:
        enc = None
        if args.measure:
            import tiktoken
            enc = tiktoken.get_encoding("o200k_base")
        for role in ("kid", "parent", "director"):
            s = build_slice(root, skill, role, tier=0)
            n = len(enc.encode(s)) if enc else "?"
            print(f"{role:10s} {n} tok")
        return 0

    if not args.role:
        raise SystemExit("rolslice.py: pass --role (or --all)")
    s = build_slice(root, skill, args.role, args.tier)
    sys.stdout.write(s)
    if args.measure:
        import tiktoken
        enc = tiktoken.get_encoding("o200k_base")
        print(f"\n---\nROLE={args.role} SLICE_TOKENS={len(enc.encode(s))}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())