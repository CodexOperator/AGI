#!/usr/bin/env python3
"""
G6.8 payload boundary predicate.

Classifies every tracked file in the `agi` engine repo as `in` (a candidate
payload for a node) or `out` (no thought attaches). Total, mechanical: every
file gets exactly one verdict from properties a script can read off the path
and off git's own configuration -- no per-file allowlist.

Usage:
    python3 payload_boundary.py /path/to/agi/repo

Exit: prints a TSV of `path<TAB>verdict<TAB>reason` to stdout, and a summary
to stderr.
"""
import subprocess
import sys
from pathlib import Path


def git_ls_files(repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True, text=True, check=True,
    )
    return [l for l in out.stdout.splitlines() if l]


def gitignore_matched(repo: Path, paths: list[str]) -> set[str]:
    """
    Which of `paths` match a pattern in the repo's own .gitignore (or any
    nested gitignore), evaluated with --no-index so already-tracked files
    are not silently exempted just because git stopped flagging them as
    ignored the moment they were added to the index. This is the mechanical
    reading of "under a directory the engine itself declares transient":
    ask the engine's own version-control config, not our outside judgment.
    """
    if not paths:
        return set()
    proc = subprocess.run(
        ["git", "-C", str(repo), "check-ignore", "--no-index", "-z", "--stdin"],
        input="\0".join(paths), capture_output=True, text=True,
    )
    # check-ignore exits 1 when *some* paths don't match -- that's normal,
    # only treat >1 as a real error.
    if proc.returncode not in (0, 1):
        raise RuntimeError(f"git check-ignore failed: {proc.stderr}")
    matched = set(p for p in proc.stdout.split("\0") if p)
    return matched


def is_test_fixture(path: str) -> bool:
    """
    Directory-naming convention, not a filename allowlist: any path that
    passes through a `tests/fixtures/` (or `test/fixtures/`) directory.
    Category reason: these files are synthetic input manufactured for a
    test harness to read -- deliberately fake headings, placeholder JSON,
    dummy directory trees -- authored to be consumed by test code, not to
    communicate anything to a human or an agent forming a thought.
    """
    parts = Path(path).parts
    for i, part in enumerate(parts):
        if part in ("tests", "test") and i + 1 < len(parts) and parts[i + 1] == "fixtures":
            return True
    return False


def is_the_graph_itself(path: str) -> bool:
    """Anything inside the graph directory — **goal:g11, and this one bites.**

    Before G11 the graph lived in a different repository, so `git ls-files` on
    the engine could never return a node file and no rule was needed. One repo
    makes the graph tracked content of the repo being scanned, and without this
    the boundary answers "in" for all 809 node files plus every schema, kit and
    plan — because each is, literally, a file in the repo.

    Observed live the hour the migration landed: `level3.py` went from 190
    files scanned to **4131**, minting a build node for every node, then a
    build node for *that* node's file, producing names like
    `nodes-build-nodes-build-nodes-build-....md.md.md`. A generator whose
    output is inside its own input set does not converge.

    The boundary rule stays "anything that exists as a file in the repo"
    (goal:g6.8); this says the graph is not a *payload* of itself. A node is
    already a node — wrapping it in a build node inverts the relationship
    exactly the way g6.8 rejects for grid refs, and for the same reason.
    """
    return Path(path).parts[:1] == (".agi",)


def is_log_stream(path: str) -> bool:
    """
    Extension-based, category reason: `.jsonl` (newline-delimited JSON) is
    an append-only event-stream format by construction -- one line per run
    event, not one authored thought. This catches every jsonl file whether
    or not it happens to live under a gitignored directory (sessions/*.jsonl
    does; autoresearch.jsonl at repo root does not, despite being the same
    kind of artifact) -- the extension rule is what makes the exclusion
    consistent instead of needing a directory-shaped special case.
    """
    return path.endswith(".jsonl")


def classify(repo: Path) -> list[tuple[str, str, str]]:
    files = git_ls_files(repo)
    ignored = gitignore_matched(repo, files)

    rows = []
    for f in sorted(files):
        if f in ignored:
            rows.append((f, "out", "gitignore-declared-transient"))
        elif is_the_graph_itself(f):
            rows.append((f, "out", "graph-not-payload"))
        elif is_log_stream(f):
            rows.append((f, "out", "jsonl-event-stream"))
        elif is_test_fixture(f):
            rows.append((f, "out", "test-fixture-directory"))
        else:
            rows.append((f, "in", "file-in-repo"))
    return rows


def classify_paths(repo: Path, rel_paths: list[str]) -> list[tuple[str, str, str]]:
    """Same verdict as `classify`, for paths that are NOT tracked in `repo`.

    `classify` asks git what exists; this asks the boundary about paths the
    caller already has — specifically files that exist only in the graph's
    payload checkout because they were **authored in the graph** and have never
    been in the engine tree (goal:g6.1). The gitignore question is still put to
    the engine repo, with `--no-index`, so one repo's declared-transient rules
    decide for both sources rather than the boundary meaning two things.
    """
    if not rel_paths:
        return []
    ignored = gitignore_matched(repo, rel_paths)
    rows = []
    for f in sorted(rel_paths):
        if f in ignored:
            rows.append((f, "out", "gitignore-declared-transient"))
        elif is_the_graph_itself(f):
            rows.append((f, "out", "graph-not-payload"))
        elif is_log_stream(f):
            rows.append((f, "out", "jsonl-event-stream"))
        elif is_test_fixture(f):
            rows.append((f, "out", "test-fixture-directory"))
        else:
            rows.append((f, "in", "file-in-payload-checkout"))
    return rows


def main(argv: list[str] | None = None) -> None:
    import argparse
    if argv is None:
        argv = sys.argv[1:]
    p = argparse.ArgumentParser(
        prog="payload_boundary.py",
        description="Classify every tracked file in an `agi` engine repo as `in` "
                    "(candidate payload for a node) or `out` (no thought attaches).")
    p.add_argument("repo", nargs="?", default=".",
                   help="path to the agi engine repo (default: current dir)")
    args = p.parse_args(argv)
    repo = Path(args.repo)
    rows = classify(repo)

    for path, verdict, reason in rows:
        print(f"{path}\t{verdict}\t{reason}")

    total = len(rows)
    n_in = sum(1 for _, v, _ in rows if v == "in")
    n_out = total - n_in
    from collections import Counter
    reason_counts = Counter(r for _, v, r in rows if v == "out")
    print(f"\ntotal={total} in={n_in} out={n_out}", file=sys.stderr)
    for reason, count in reason_counts.most_common():
        print(f"  out[{reason}]={count}", file=sys.stderr)


if __name__ == "__main__":
    main()
