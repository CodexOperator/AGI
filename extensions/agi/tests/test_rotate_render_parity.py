"""`hypothesis:non-prime-rotate-self-renders-through-brief-render` — the
comparison the claim asks for ("a committed test compares the two renders").

The claim has two clauses and this file measures BOTH on ONE fixture, so the
answer is a byte diff rather than a reading of the source:

  (1) the non-prime rotate-self path renders the successor's first turn
      through `brief.render`, exactly as the prime path does; and
  (2) a committed test compares the two renders.

WHAT THE MACHINE ACTUALLY DOES (rotate.py:19570-19590, the (3) prompt_file
resolution): the `brief_file` cell is resolved for EVERY template EXCEPT
`prime_director` —

    if (not args.dry_run and prompt_file is None
            and role != "prime_director"
            and tmpl is not None and tmpl.get("brief_file")):
        prompt_file = _resolve_brief_file(root, ..., tmpl["brief_file"])

so a non-prime hands `spawn_window` a FILE and lands in `_successor_command`
(file body + `brief.successor_prompt`), while the prime hands it `None` and
lands in `_assembled_successor_command` (`brief.render`). The two renders are
therefore NOT the same render, and the live `director` template DOES declare
`brief_file: .agi/sessions/quorum/{seat}.md` (config:rotations), so this is
the live path, not an edge case.

The exemption is DELIBERATE and load-bearing (rotate.py:19574-19582, and the
GATE `test_non_prime_rotate_self_still_resolves_its_template_brief`): a
non-prime's successor must read the post's OWN quorum card at the path the
rename boundary renamed, which `brief.render`'s `card` part cannot be trusted
to reach (L5.11 `hypothesis:l5-rename-surfaces-and-the-successor-brief-
resolve-from-the-rotating-worktree-root`). So this file pins the DIVERGENCE
as measured, and pins the one place the two paths DO agree — the head bytes
both prepend — rather than asserting a parity that does not exist.
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



def test_the_two_rotations_take_different_render_paths(tmp_path, monkeypatch):
    """CLAUSE (1), MEASURED: the prime hands `spawn_window` no prompt file
    (so it renders through `brief.render`), and a non-prime whose template
    declares `brief_file` hands it a FILE (so it never renders). The claim as
    written is FALSIFIED here, and this is the live `director` template."""
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
    assert director["prompt_file"] == str(
        dir_wt / ".agi" / "sessions" / "quorum" / "director-row.md"), (
        "a non-prime resolves its template brief_file instead of rendering")


def test_a_non_prime_without_a_brief_file_cell_does_render(tmp_path,
                                                           monkeypatch):
    """THE NEAR MISS, stated as a counterfactual: the non-prime path DOES
    reach `brief.render` — but only when the template declares no
    `brief_file`. This is why the claim reads plausibly from the source: the
    `role != "prime_director"` guard is the ONLY thing separating the two
    renders, and a template with no `brief_file` cell removes it."""
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


def test_the_two_bodies_share_the_head_and_diverge_below_it(tmp_path,
                                                            monkeypatch):
    """CLAUSE (2), the COMPARISON: compose both successors' real first turns
    and diff them. The head bytes are the ONE thing the two paths agree on —
    `brief.render`'s `head` part and `brief.successor_prompt`'s
    `render_head` are the same function — and everything below it is a
    different render: the prime carries role template + card + harness block
    + trajectory, the non-prime carries only its quorum card's bytes."""
    root = _root(tmp_path)
    card = _write(root, "sessions/quorum/director-seat.md", QUORUM_CARD_SENTINEL + "\n")
    seen = {}

    def _capture(harness, **kw):
        seen[seen.pop("slot")] = kw["prompt_text"]
        return ["x"]

    monkeypatch.setattr(rotate, "_build_harness_command", _capture)

    # the prime's path: prompt_file None -> _assembled_successor_command
    seen["slot"] = "prime"
    rotate._assembled_successor_command(
        name="prime-seat", tier="prime_director", model=None, effort=None,
        settings=None, debug_file="/dev/null", harness="pi", project_root=root)

    # the non-prime's path: a prompt file -> _successor_command
    seen["slot"] = "nonprime"
    rotate._successor_command(
        name="director-seat", tier="director", prompt_file=str(card),
        model=None, effort=None, settings=None, debug_file="/dev/null",
        harness="pi", project_root=root)

    prime, nonprime = seen["prime"], seen["nonprime"]
    head = brief.render_head(project_root=root)
    assert head and HEAD_SENTINEL in head
    # AGREE: the same head bytes open both, from the same function.
    assert prime.startswith(head)
    assert nonprime.startswith(head)
    # DIVERGE: only the prime's body carries the config render's parts.
    assert TEMPLATE_SENTINEL in prime
    assert TRAJECTORY_SENTINEL in prime
    assert HARNESS_SENTINEL in prime
    assert TEMPLATE_SENTINEL not in nonprime
    assert TRAJECTORY_SENTINEL not in nonprime
    assert HARNESS_SENTINEL not in nonprime
    # and the non-prime's body is the quorum FILE, which `brief.render` would
    # have replaced with its own `card` part.
    assert QUORUM_CARD_SENTINEL in nonprime
    assert prime != nonprime
