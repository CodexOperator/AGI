"""The retired box prefix must never come back as a LIVE executable path.

`goal:g73314-a-nonworkflow-residue` asked for "0 grep hits outside the frozen
fixture" and measured 22 live hits. `experiment:a00-600cf080-0cd865-exp` then
measured that **0 of the 22 sit on an executing line**: 11 are prose
prohibitions, 5 are negative assertions, 4 are inert fixture command strings,
1 is a constant read only by `@live`-skipped tests, and 1 is a config cell.
Satisfying the count-based falsifier means deleting the warnings.

So the gate here is CLASS-based, and it is the goal's clause 2 ("enforced by a
committed test") made satisfiable:

| test | property |
|---|---|
| T1 | no live hit outside `EXEMPT`, each entry of which carries a one-line reason |
| T2 | every `EXEMPT` entry is still live in its file — deleting a warning deletes its exemption |
| T3 | every exemption is prose (comment / docstring span) or is in `BOX_BOUND`; every entry owes a one-line reason |
| T4 | the frozen fixture exemption is by name and still exists |
| T5 | the guard itself carries the prefix only inside `PREFIX`/`EXEMPT`/`BOX_BOUND` |

Docstrings are marked by SPAN (`lineno..end_lineno`), not by first line: a guard
that only marks the first line flags 7 prose lines forever, and the first person
to "fix" that failure deletes the warnings (recorded in the experiment node).
"""
from __future__ import annotations

import ast
import io
import tokenize
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
EXT = REPO / "extensions" / "agi"
PREFIX = "/home/ubuntu/work/agi"
SCAN_DIRS = ("bin", "hooks", "briefs", "tests")
SCAN_FILES = (REPO / ".agi" / "config.json",)
# Exempt BY NAME and for a stated reason: recorded argv of a past run
# (l4_85_frozen). Rewriting those bytes would falsify the record.
FROZEN_PREFIX = "extensions/agi/tests/fixtures/l4_85_frozen"
# The guard's own table has to name the strings it bans; it is exempted by
# name, and test_t5 proves its only hits are the PREFIX constant and the
# EXEMPT table (an occurrence anywhere else in this file is a real failure).
SELF = "extensions/agi/tests/test_retired_box_prefix.py"

# (relpath, exact stripped line text) -> (class, one-line reason)
EXEMPT = {
    ("extensions/agi/bin/commands.py", "A table full of `/home/ubuntu/work/agi/...` would be a table that stops"): ("P", "prose: the warning that paths belong in config"),
    ("extensions/agi/bin/unify.py", "happens to keep at `/home/ubuntu/work/agi` and `/home/ubuntu/work/agi-tree`."): ("P", "prose: the guard exists precisely because a box can"),
    ("extensions/agi/bin/unify.py", "repos — the thing that must never be `/home/ubuntu/work/agi` is the"): ("P", "prose: the guard exists precisely because a box can"),
    ("extensions/agi/bin/env-get.sh", '#                   "key": "!/home/ubuntu/work/agi/extensions/agi/bin/env-get.sh OPENROUTER_API_KEY" }'): ("P", "prose: example of the !command indirection shape"),
    ("extensions/agi/hooks/rotation_alert.py", '#          "command": "python3 /home/ubuntu/work/agi/extensions/agi/hooks/rotation_alert.py",'): ("P", "prose: sample unit file shown in a docstring"),
    ("extensions/agi/hooks/rotation_alert.py", "`/home/ubuntu/work/agi/.agi/sessions/` (where every reader looks) and"): ("P", "prose: sample unit file shown in a docstring"),
    ("extensions/agi/tests/test_unify.py", "**Never point this test file at `/home/ubuntu/work/agi` or"): ("P", "prose: the isolation rule these fixtures implement"),
    ("extensions/agi/tests/test_unify.py", "`/home/ubuntu/work/agi-tree`.** Every fixture builds its own tiny repos under"): ("P", "prose: the isolation rule these fixtures implement"),
    ("extensions/agi/tests/test_unify.py", "# symlink to CLAUDE.md, same directory, same as `/home/ubuntu/work/agi-tree`."): ("P", "prose: comment on the fixture's shape"),
    ("extensions/agi/tests/test_dispatch_forward_env.py", "`TYPESAFE_KEY` sits in `/home/ubuntu/work/agi/.env`."): ("P", "prose: names the file the env cell points at"),
    ("extensions/agi/tests/test_workflow.py", "# used to `cd /home/ubuntu/work/agi`, so a run started in a git worktree"): ("P", "prose: why the cwd knob exists"),
    ("extensions/agi/tests/test_workflow.py", 'assert "/home/ubuntu/work/agi" not in out, (st["label"], out)'): ("F", "inert data: negative assertion, the string is never a path"),
    ("extensions/agi/tests/test_workflow.py", 'assert all("/home/ubuntu/work/agi &&" not in c or f"cd {REPO} &&" in c'): ("F", "inert data: negative assertion, the string is never a path"),
    ("extensions/agi/tests/test_sensei_wake_audit.py", 'cmd = "git -C /home/ubuntu/work/agi status -sb | head -3"'): ("F", "inert data: classified by sensei.classify_call, never shelled out"),
    ("extensions/agi/tests/test_sensei_wake_audit.py", 'cmd = "ls -la /home/ubuntu/work/agi/.agi/sessions/rotations | tail -5"'): ("F", "inert data: classified by sensei.classify_call, never shelled out"),
    ("extensions/agi/tests/test_sensei_wake_audit.py", '"ls -la /home/ubuntu/work/agi/.agi/sessions/rotations | tail -5",'): ("F", "inert data: fixture entry passed to the classifier, never run"),
    ("extensions/agi/tests/test_sensei_wake_audit.py", '("Bash", "ls -la /home/ubuntu/work/agi/.agi/sessions/rotations "'): ("F", "inert data: fixture entry passed to the classifier, never run"),
    (".agi/config.json", '"root": "/home/ubuntu/work/agi",'): ("B", "the one code-level exemption left: the box.root CELL, owned by group a00-3b546363; correcting the cell removes the hit and this entry with it (T2)"),
}
# Class B only: a hit on a line that EXECUTES. DERIVED from EXEMPT, never
# hand-listed, and never TALLIED: a count in a gate breaks when a coupled
# literal is repointed, for a reason that is not a defect. Today this is the
# single box.root cell in .agi/config.json (group a00-3b546363 owns it); the
# three test_unify literals and the test_provisioning ROOT constant were
# repointed to unify._git_common_root() and to the checkout this file lives in.
BOX_BOUND = {k for k, (cls, _r) in EXEMPT.items() if cls == "B"}


def _scanned() -> list[Path]:
    out: list[Path] = []
    for d in SCAN_DIRS:
        base = EXT / d
        if base.is_dir():
            out += [p for p in base.rglob("*") if p.is_file()]
    out += [p for p in SCAN_FILES if p.is_file()]
    return sorted(out)


def _hits() -> list[tuple[str, str, int]]:
    found = []
    for p in _scanned():
        rel = p.relative_to(REPO).as_posix()
        if rel.startswith(FROZEN_PREFIX) or rel == SELF:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for n, line in enumerate(text.splitlines(), 1):
            if PREFIX in line:
                found.append((rel, line.strip(), n))
    return found


def _prose_lines(path: Path) -> set[int]:
    """Comment lines + full docstring SPANS (a first-line-only mark is the
    known false-positive generator). Non-Python files get no prose."""
    if path.suffix not in (".py", ".sh", ".bash"):
        return set()
    if path.suffix != ".py":  # a shell comment line is prose, byte for byte
        return {n for n, l in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
                if l.lstrip().startswith("#")}
    try:
        src = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return set()
    dead = {t.start[0] for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type == tokenize.COMMENT}
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return dead
    for node in ast.walk(tree):
        body = getattr(node, "body", None)
        if not isinstance(body, list) or not body:
            continue
        first = body[0]
        if (isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
                and isinstance(first.value.value, str)):
            dead.update(range(first.lineno, (first.end_lineno or first.lineno) + 1))
    return dead


def test_t1_no_live_hit_outside_a_named_and_reasoned_exemption():
    """The class-based restatement of falsifier clause 1: a new occurrence of
    the retired prefix anywhere live fails, and passing means adding an entry
    WITH a reason — never deleting the warning."""
    unexempted = [
        f"{rel}:{n}: {text}"
        for rel, text, n in _hits() if (rel, text) not in EXEMPT
    ]
    assert not unexempted, (
        "retired box prefix reappeared outside EXEMPT; add a (relpath, exact "
        "line text) entry with a one-line reason, or remove the hit:\n  "
        + "\n  ".join(unexempted))


def test_t2_every_exemption_is_still_live():
    """Deleting a prose warning must delete its exemption, so EXEMPT cannot
    quietly become a blanket waiver as files move around."""
    corpus: dict[str, set[str]] = {}
    stale = []
    for (rel, text) in EXEMPT:
        lines = corpus.get(rel)
        if lines is None:
            lines = corpus[rel] = {
                l.strip() for l in (REPO / rel).read_text(encoding="utf-8").splitlines()
            } if (REPO / rel).is_file() else set()
        if text not in lines:
            stale.append(f"{rel}: {text!r}")
    assert not stale, "exemption no longer matches any line; drop it:\n  " + "\n  ".join(stale)


def test_t3_every_exemption_is_prose_or_carries_a_stated_reason():
    """The class story, mechanically: a hit that executes is tolerated only
    because it is in BOX_BOUND (DERIVED from the class, never hand-listed) and
    because its reason is a real one-line sentence.

    There is deliberately NO count here. An earlier revision ended in
    `assert len(BOX_BOUND) == 5`: a tally that breaks when the coupled literals
    are repointed — for a reason that is not a defect, and that the cheapest
    repair (`delete the entry`) would hide. The property that survives a
    refactor is 'every non-prose exemption says why it may execute', not 'there
    are five of them'. The same brittleness this subgoal argues against."""
    misfiled = []
    for rel, text, n in _hits():
        key = (rel, text)
        if key not in EXEMPT:
            continue
        cls = EXEMPT[key][0]
        prose = n in _prose_lines(REPO / rel)
        if cls == "P" and not prose:
            misfiled.append(f"{rel}:{n} claims class P but executes: {text!r}")
        if cls in ("F", "B") and prose:
            misfiled.append(f"{rel}:{n} claims class {cls} but is prose: {text!r}")
    assert not misfiled, "\n  ".join(misfiled)
    unsaid = [
        f"{rel}:{text[:40]!r} -> {reason!r}"
        for (rel, text), (cls, reason) in EXEMPT.items()
        if not reason.strip() or "\n" in reason or len(reason.strip()) < 20
    ]
    assert not unsaid, ("every exemption owes a one-line reason of real "
                        "substance, especially the code-level ones:\n  "
                        + "\n  ".join(unsaid))
    assert BOX_BOUND <= set(EXEMPT), "BOX_BOUND must stay derived from EXEMPT"


def test_t4_the_frozen_fixture_is_the_only_exempted_tree():
    """Falsifier clause 1's exemption is by name and by reason — the frozen
    fixture holds recorded argv of a past run; nothing else may be skipped."""
    frozen = [p for p in _scanned()
              if p.relative_to(REPO).as_posix().startswith(FROZEN_PREFIX)
              and PREFIX in p.read_text(encoding="utf-8", errors="ignore")]
    assert frozen, "the named exemption must still exist; a test that exempts nothing is not a gate"


def test_t5_the_guard_only_names_the_prefix_it_bans():
    """The guard is exempt by name, so it must contain no hit beyond the
    PREFIX constant and the EXEMPT table it exists to hold."""
    src = (REPO / SELF).read_text(encoding="utf-8")
    tree = ast.parse(src)
    allowed: set[int] = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        names = [t.id for t in node.targets if isinstance(t, ast.Name)]
        if set(names) & {"PREFIX", "EXEMPT", "BOX_BOUND"}:
            allowed.update(range(node.lineno, (node.end_lineno or node.lineno) + 1))
    stray = [
        f"{SELF}:{n}: {l.strip()}"
        for n, l in enumerate(src.splitlines(), 1)
        if PREFIX in l and n not in allowed
    ]
    assert not stray, ("the guard must not carry the banned prefix outside "
                       "PREFIX/EXEMPT/BOX_BOUND:\n  " + "\n  ".join(stray))
    assert allowed, "vacuous: the guard does not even mention the prefix"
