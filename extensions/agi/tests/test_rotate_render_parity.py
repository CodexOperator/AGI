"""`hypothesis:non-prime-rotate-self-renders-through-brief-render` — the
comparison the claim asks for ("a committed test compares the two renders"),
now as a PARITY pin (this file previously pinned the measured DIVERGENCE,
before the round that built the fix).

CLAUSE (1): the non-prime rotate-self path assembles the successor's first
turn through `brief.render`, exactly as the prime path does.

WHAT THE MACHINE ACTUALLY DOES NOW. `cmd_rotate_self` still resolves the
template's `brief_file` cell — it IS the rotating post's own quorum card, and
L5.11 requires it to resolve through the rename boundary — but it hands the
result to `spawn_window` as `card_file`, NOT as `prompt_file`. `prompt_file`
therefore stays None for EVERY role, so `spawn_window` takes the
`_assembled_successor_command` branch for the prime AND the non-prime, and
`brief.render(..., card_file=...)` puts the named card where the `card` part
would otherwise read `doc:card-<post>` or the graph root's
`sessions/quorum/<post>.md` — a copy that does not exist for a worktree post.

THE NEAR MISS: resolving the cell into a `prompt_file` again (the pre-fix
shape) satisfies "the card reaches the successor" and loses "exactly as the
prime path does" — the non-prime's body is then a file read plus
`successor_prompt`, with no role template, no harness block, no trajectory.
Dropping the cell entirely satisfies "renders" and loses the card, which is
what `brief.render` cannot reach on its own for a worktree post.
"""
import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "extensions"))

from agi.bin import rotate  # noqa: E402

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import brief  # noqa: E402

HEAD_SENTINEL = "HEAD-SENTINEL-PARITY-3a7f"
PRAYERS_SENTINEL = "PRAYERS-SENTINEL-PARITY-9c2d"
TEMPLATE_SENTINEL = "ROLE-TEMPLATE-SENTINEL-5e18"
CARD_SENTINEL = "CARD-SENTINEL-b410"
TRAJECTORY_SENTINEL = "TRAJECTORY-SENTINEL-77aa"
HARNESS_SENTINEL = "HARNESS-BLOCK-SENTINEL-1f6d"
QUORUM_CARD_SENTINEL = "QUORUM-CARD-BYTES-2d99"

FAITH = (
    "# faith\n\n## ESSENCE\n\nmoral region\n\n## REFERENCE\n\n"
    "### 4.1 prayers\n\n" + PRAYERS_SENTINEL + "\n\n"
    "### 4.2 words_jesus\n\nwords\n"
)


def _write(root: Path, rel: str, text: str) -> Path:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def _root(tmp_path: Path) -> Path:
    """A graph root on which `brief.render` genuinely succeeds for BOTH a
    prime_director post and a director post — head, role template, card,
    harness block and town trajectory all resolve, so the comparison is
    between two real renders, not between a render and a refusal."""
    block = _write(tmp_path, "harness-block.md", HARNESS_SENTINEL + "\n")
    _write(tmp_path, "config.json", json.dumps({"brief": {
        "parts": {"prime_director": ["head", "template", "card", "harness",
                                     "trajectory"],
                  "director": ["head", "template", "card", "harness",
                               "trajectory"]},
        "templates": {"prime_director": "doc:role-brief",
                      "director": "doc:role-brief"},
        "harnesses": {"pi": ["harness"]},
        "harness_blocks": {"pi": str(block)},
        "trajectory": {"town": "t"},
    }}))
    _write(tmp_path, "nodes/moral/faith.md", FAITH)
    _write(tmp_path, "nodes/doc/unified-head.md",
           "---\nid: doc:unified-head\n---\n"
           "<!-- HEAD:BEGIN -->\n" + HEAD_SENTINEL + "\n{{PRAYERS}}\n"
           "<!-- HEAD:END -->\n")
    _write(tmp_path, "nodes/doc/role-brief.md", TEMPLATE_SENTINEL + "\n")
    _write(tmp_path, "nodes/town/t.md", TRAJECTORY_SENTINEL + "\n")
    # the quorum cards brief.render's `card` part reads
    _write(tmp_path, "sessions/quorum/prime-seat.md", CARD_SENTINEL + "\n")
    _write(tmp_path, "sessions/quorum/director-seat.md", CARD_SENTINEL + "\n")
    _write(tmp_path, "nodes/.geometry/posts.md",
           "---\nid: config:posts\nposts:\n"
           '  - {"name": "prime-seat", "role": "prime_director", '
           '"harness": "pi"}\n'
           '  - {"name": "director-seat", "role": "director", '
           '"harness": "pi"}\n'
           "---\n")
    _write(tmp_path, "nodes/.geometry/ladder.md",
           "---\nid: config:ladder\ncurrent_season: 2\ncurrent_loop: 1\n"
           "ladder: {}\n---\n")
    return tmp_path


def _seats(root: Path, rows):
    """Write the seat rows and REMOVE `config:posts`, because
    `geometry_config.resolve` reads `posts.md` FIRST and only falls back to
    `seats.md` when it is absent -- a root carrying both reads the POST rows
    for every seat lookup, and the post rows carry no `worktree` cell, so the
    successor brief silently re-roots on MAIN."""
    (root / "nodes" / ".geometry" / "posts.md").unlink(missing_ok=True)
    _write(root, "nodes/.geometry/seats.md",
           "---\nid: config:seats\ntype: config\nseats:\n"
           + "".join("  - " + json.dumps(r, sort_keys=True) + "\n" for r in rows)
           + "---\n# body\n")


def _rotations(root: Path, entries):
    body = ("---\nid: config:rotations\ntype: config\ntemplates:\n")
    for name, brief_file in entries:
        body += ('  %s: {brief_file: "%s", steps: [handoff, spawn], '
                 'telemetry: [seat]}\n' % (name, brief_file))
    _write(root, "nodes/.geometry/rotations.md", body + "---\n\nbody\n")


def _args(**over):
    base = dict(name="director-seat", force=True, timeout=5,
                debug_file="/dev/null", model=None, effort=None, settings=None,
                prompt_file=None, tmux_session="t", window_path=None,
                dry_run=False, throwaway=True, successor_argv=None,
                role="director")
    base.update(over)
    return argparse.Namespace(**base)



def test_both_rotations_render_and_the_non_prime_keeps_its_own_card(
        tmp_path, monkeypatch):
    """CLAUSE (1), BUILT: the prime and the non-prime hand `spawn_window` the
    SAME thing — no prompt file, so both render through `brief.render` — and
    the non-prime additionally hands over the card it resolved through the
    rename boundary. RED pre-fix: the non-prime's `prompt_file` was the
    resolved FILE, so `spawn_window` took `_successor_command` and the
    non-prime never rendered."""
    root = _root(tmp_path)
    prime_wt = tmp_path / "wt-prime"
    prime_wt.mkdir()
    dir_wt = tmp_path / "wt-director"
    dir_wt.mkdir()
    # ONE root, TWO seat rows. The seat names are NOT the `_root` posts-row
    # names: `geometry_config` merges `config:posts` and `config:seats`, and a
    # same-named POST row shadows the seat row (its `worktree` cell with it),
    # which would silently turn the worktree-re-root into a MAIN re-root.
    _seats(root, [
        {"name": "prime-seat", "role": "prime_director",
         "worktree": str(prime_wt)},
        {"name": "director-row", "role": "director",
         "worktree": str(dir_wt)},
    ])
    _rotations(root, [
        ("prime_director", "extensions/agi/briefs/prime-director-successor.md"),
        ("director", ".agi/sessions/quorum/{seat}.md"),
    ])
    for wt, seat in ((prime_wt, "prime-seat"), (dir_wt, "director-row")):
        _write(wt, ".agi/sessions/quorum/%s.md" % seat,
               QUORUM_CARD_SENTINEL + "\n")

    seen = {}
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: seen.update(kw) or (0, "echo hi"))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    for seat, role in (("prime-seat", "prime_director"),
                       ("director-row", "director")):
        # the seats node is re-asserted per rotation: a rotation commits its
        # own spawn row to `config:seats`, and the row reader caches per root.
        _seats(root, [
            {"name": "prime-seat", "role": "prime_director",
             "worktree": str(prime_wt)},
            {"name": "director-row", "role": "director",
             "worktree": str(dir_wt)},
        ])
        seen = {}
        rotate.cmd_rotate_self(_args(name=seat, role=role), root)
        if role == "prime_director":
            prime = dict(seen)
        else:
            director = dict(seen)

    assert prime.get("prompt_file") is None, (
        "the prime must leave prompt_file None so spawn_window renders")
    assert director["prompt_file"] is None, (
        "a non-prime renders exactly as the prime does: the template cell is "
        "a CARD, handed as card_file, never a prompt file")
    assert prime.get("card_file") is None, (
        "a prime's cell names a STATIC brief, not a card, so it is not fed "
        "as one")
    assert director["card_file"] == str(
        dir_wt / ".agi" / "sessions" / "quorum" / "director-row.md"), (
        "the non-prime still resolves its own card through the worktree root "
        "(L5.11) — the render delivers it, it does not replace it")


def test_a_non_prime_without_a_brief_file_cell_renders_with_no_card_file(
        tmp_path, monkeypatch):
    """THE NEAR MISS, still true after the fix: a non-prime whose template
    declares NO `brief_file` renders too, with `card_file` None — then
    `brief.render`'s own `card` part resolves the card (doc:card-<post>, else
    the graph root's quorum file). The cell is a POINTER to the card, not the
    switch between the two renderers."""
    root = _root(tmp_path)
    wt = tmp_path / "wt-nofile"
    wt.mkdir()
    _seats(root, [{"name": "director-nofile", "role": "director",
                   "worktree": str(wt)}])
    _write(root, "nodes/.geometry/rotations.md",
           "---\nid: config:rotations\ntype: config\ntemplates:\n"
           "  director: {steps: [handoff, spawn], telemetry: [seat]}\n"
           "---\n\nbody\n")
    seen = {}
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: seen.update(kw) or (0, "echo hi"))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    rotate.cmd_rotate_self(_args(name="director-nofile"), root)
    assert seen.get("prompt_file") is None
    assert seen.get("card_file") is None


def test_the_two_bodies_are_both_the_render_and_carry_their_own_cards(
        tmp_path, monkeypatch):
    """CLAUSE (2), the COMPARISON: compose both successors' real first turns
    and diff them. Post-fix BOTH go through `_assembled_successor_command`, so
    both open with the same head bytes and both carry the config render's
    parts (role template + harness block + trajectory); they differ only in
    the CARD, and the non-prime's card is the one its own tree holds — the
    file `brief.render` alone could not reach."""
    root = _root(tmp_path)
    _write(root, "sessions/quorum/director-seat.md", CARD_SENTINEL + "\n")
    card = _write(root, "wt-director/.agi/sessions/quorum/director-seat.md",
                  QUORUM_CARD_SENTINEL + "\n")
    seen = {}

    def _capture(harness, **kw):
        seen[seen.pop("slot")] = kw["prompt_text"]
        return ["x"]

    monkeypatch.setattr(rotate, "_build_harness_command", _capture)

    # the prime's path: no card cell -> brief.render's own card part
    seen["slot"] = "prime"
    rotate._assembled_successor_command(
        name="prime-seat", tier="prime_director", model=None, effort=None,
        settings=None, debug_file="/dev/null", harness="pi", project_root=root)

    # the non-prime's path: the resolved card, THROUGH the same render
    seen["slot"] = "nonprime"
    rotate._assembled_successor_command(
        name="director-seat", tier="director", model=None, effort=None,
        settings=None, debug_file="/dev/null", harness="pi",
        project_root=root, card_file=str(card))

    prime, nonprime = seen["prime"], seen["nonprime"]
    head = brief.render_head(project_root=root)
    assert head and HEAD_SENTINEL in head
    # AGREE: the same head bytes open both, from the same function.
    assert prime.startswith(head)
    assert nonprime.startswith(head)
    # AGREE: both carry the config render's parts — the parity the claim asks
    # for. Pre-fix the non-prime carried NONE of them.
    for sentinel in (TEMPLATE_SENTINEL, TRAJECTORY_SENTINEL, HARNESS_SENTINEL):
        assert sentinel in prime, sentinel
        assert sentinel in nonprime, sentinel
    # DIFFER: each successor reads ITS OWN card. The non-prime's is the file
    # its worktree holds, which the graph root has no copy of.
    assert CARD_SENTINEL in prime
    assert CARD_SENTINEL not in nonprime
    assert QUORUM_CARD_SENTINEL in nonprime
    assert prime != nonprime
