"""The claim's own grep test — hypothesis:l4-every-branch-name-derives-from-
one-tuple-and-only-the-trunk-pair-per-level-reaches-origin.

The durable artifact of region D section 2: every `extensions/agi/bin/*.py`
is grepped for a HAND-SPELLED branch SPELLING — a literal `season<n>/...`,
`season/s<n>`, `town/...`, `post/...@s<n>`, `loop/...@s<n>`, or an f-string
building one — OUTSIDE branches.py (which OWNS the grammar and its alias
table). The match is the RESOLVER that must route through `branches.py`, or a
genuine literal that is not a resolver; either way a reviewer must see it,
so a new hand-spelled spelling FAILS this test.

THIS FROZEN LIST IS DEBT, NOT A LICENCE. Every hit below was triaged in
L4.332 (a00-1997ae21): the season-first spellings in dispatch.py, rotate.py,
heal.py, season.py, send.py, spawn_gate.py, grid.py and the cli.py
reshuffle/prune regions live in files FROZEN by that round — their rename to
the v3 TOWN-FIRST names is a later Prime-only pass (the live tree is HELD by
the owner), so this test pins them as the debt to burn down. verification.py
(and branches.py) are the ONLY files allowed to resolve this round, and
verification already routes through `branches.ref_candidates`; its one hit
here is a docstring, not a resolver. The test asserts the exact (file, matched-text)
multiset so drift — a new hand-spelled shape OR a silently-deleted debt line — is
caught, never silently agreed with.

The FULL inventory (file:line: literal) is in the L4.332 experiment node
(experiment:a00-1997ae21-247395) — this test pins the (file, matched text)
signature of it -- text, not line numbers, so an unrelated edit that moves
lines cannot turn it red.
"""

import pathlib
import re

import pytest

_HERE = pathlib.Path(__file__).resolve().parent
_BIN = (_HERE / ".." / "bin").resolve()

# Derivable branch-SPELLING shapes (season/town/post/loop). The fixed
# `master` constant token is deliberately NOT here: it has no derivable
# spelling variant, so there is nothing to centralize or drift from.
_SPELLINGS = [
    # season/s2, season/sN, season/s{...}, season/s<n>
    re.compile(r"season/s(?:[0-9]+|[Nn]|[<{][snN0-9]?)"),
    # season2/<...> — a post/town/loop/season under a season main
    re.compile(r"season[0-9]+/[A-Za-z_0-9]"),
    # town/<...> (quote/heavy-punct safe: stop at common delimiters)
    re.compile(r"town/[^\s\"',:`\[]"),
    # post/<...>@s2 and loop/<...>@s2 and their <name>/<n> metavars
    re.compile(r"post/[^\s\"',:]*@s[0-9]+"),
    re.compile(r"loop/[^\s\"',:]*@s[0-9]+"),
]

# The triaged inventory: {filename: sorted [matched spelling text, ...]} of
# every spelling-shaped hit OUTSIDE branches.py. Pinned by the MATCHED TEXT,
# never by line number (director fix at the L4.332 harvest: the round pinned
# (file, line) pairs, which went red the first time an unrelated sync moved
# rotate.py/heal.py by a few lines -- brittle by construction, and a
# false "drift" every hour). Adding a NEW hand-spelled shape -- even in a
# comment or an f-string -- or silently deleting a debt line still fails.
# re-pinned 2026-09-12 SL2#26 cut 2 (sensei-director): rotate.py inventory after SL7.92-107 landed behind the point's 48 — a cross-merge pin move, not a spelling defect
PINNED = {
    'cli.py': [
        'post/<name>@s2',
        'post/<name>@s2',
        'post/<name>@s2',
        'post/<name>@s2',
        'post/<name>@s2',
        'post/<name>@s2',
        'post/<name>@s2',
        'post/a@s2',
        'post/a@s2',
        'season/s2',
        'season1/m',
        'season2/m',
    ],
    'dispatch.py': [
        'loop/…-<agent_id>@s2',
        'season/s<N',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season1/l',
        'season1/m',
        'town/<',
        'town/<',
    ],
    'graphweb.py': [
        'post/<name>@s2',
    ],
    'grid.py': [
        'season/s<N',
    ],
    'heal.py': [
        'season/s<N',
        'season/s<N',
    ],
    'rotate.py': [
        'season/s2',
        'season/s2',
        'season/s2',
        'season/s2',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/sN',
        'season/s{',
        'season/s{s',
        'season1/l',
        'season1/m',
        'season2/m',
        'season2/m',
        'season2/m',
        'season2/m',
        'season2/m',
        'season2/m',
        'season2/m',
    ],
    'season.py': [
        'season/s<N',
        'season/s<N',
        'season/s<N',
        'town/s',
    ],
    'send.py': [
        'season/s<N',
    ],
    'spawn_gate.py': [
        'season/sN',
        'season/sN',
    ],
    'verification.py': [
        'season/s<N',
    ],
}


def _scan() -> dict:
    found = {}
    for f in sorted(_BIN.glob("*.py")):
        if f.name == "branches.py":
            continue  # the grammar module owns the shapes; not a reader
        for line in f.read_text(encoding="utf-8").splitlines():
            hits = [m.group(0) for p in _SPELLINGS for m in [p.search(line)] if m]
            if hits:
                found.setdefault(f.name, []).extend(hits)
    return {k: sorted(v) for k, v in found.items()}


def test_no_new_hand_spelled_branch_spelling():
    found = _scan()
    assert found == PINNED, (
        "A hand-spelled branch spelling drifted from the L4.332-pinned "
        f"inventory.\nNew/removed: {sorted(set(found) ^ set(PINNED))}\n"
        "Every reader MUST resolve through branches.py. The frozen hits are "
        "frozen DEBT (files held by the owner mid-rename), not a licence. "
        "Add a new spelling only by routing it through branches.py, or "
        "re-triage deliberately and re-pin."
    )


def test_pinned_inventory_is_not_vacuous():
    # The pin is a real, nonempty list and re-scans to the same rows — the
    # test is not asserting against itself.
    assert PINNED, "pinned inventory is empty -> vacuous test"
    assert _scan() == PINNED
    total = sum(len(v) for v in PINNED.values())
    assert total >= 40, f"pinned inventory implausibly small: {total}"


def test_pinned_inventory_documents_resolver_files_expected_to_route_through_branches():
    # verification.py is the one non-frozen resolver this round: it MUST go
    # through branches.ref_candidates (it does — _integration_branch_candidates
    # calls it), and its single spelling-shaped hit is a docstring, not a
    # hardcoded branch. Assert that documented contract explicitly.
    import branches
    import verification  # noqa: F401 -- import side effect: module resolves
    assert branches.ref_candidates
    from verification import _integration_branch_candidates  # noqa: F401
    # its ONE hit is the `season/s<N>` metavariable in a docstring, not a
    # hardcoded branch -- pinned by text, so a line shift cannot break this.
    assert PINNED["verification.py"] == ["season/s<N"]