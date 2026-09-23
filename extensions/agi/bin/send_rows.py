#!/usr/bin/env python3
"""send_rows.py -- PURE LIBRARY (no __main__, no CLI): the seat-row
commit/push layer that goal:g7.32.4 clause (1) moves out of send.py.

It owns the five `--all-live` / keygen row writers and the row-resolution
helpers they depend on, so send.py stops reaching `rotate` for orchestration
and becomes a thin router. `rotate` is imported lazily inside each writer
(never at module import time, no cycle); this module imports nothing from
send.py. A linked-worktree caller resolves MAIN through the shared helpers
exactly as before -- the bodies are byte-for-byte the ones lifted from
send.py.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

_BIN = Path(__file__).resolve().parent
if str(_BIN) not in sys.path:
    sys.path.insert(0, str(_BIN))
import geometry_config  # noqa: E402
import locations  # noqa: E402


def _graph_root(root: Path) -> Path:
    """The graph root (the `.agi` dir holding config.json) for a given root.

    A G11 project root is the parent of `.agi/`; an already-resolved graph
    root IS the `.agi` dir. ``write.submit`` keys every node path off THIS
    root (write.py `_load_seats` reads `<root>/nodes/.geometry/seats.md`),
    so keygen must hand write.submit the graph root, never the project root.
    """
    if (root / ".agi" / "config.json").is_file():
        return root / ".agi"
    return root


def _live_row(row: dict) -> bool:
    """A LIVE seat row carries a live pid or a session_id (hypothesis
    l4-every-live-row-is-keyed...) -- exactly the rows a prime keys with
    `keygen --all-live`. A row with neither is not live and is left alone.
    """
    return bool(row.get("pid") or row.get("session_id"))


def _seats_rows(graph: Path) -> list:
    """The current `config:seats` rows on disk, or [] when absent."""
    try:
        import write as write_mod  # local
        return list(write_mod._load_seats(graph))
    except Exception:                                          # noqa: BLE001
        return []


def _shared_graph_root(root: Path) -> Path:
    """MAIN's project graph root (the directory holding `.agi`), never the
    caller's worktree — the ONE checkout the shared-seats reader (and the
    committed-row reader) must both address. A linked-worktree call rebases to
    MAIN through `locations.git_common_root`; a caller in the main checkout or
    outside git keeps its own literal root (the legacy/graph-root and
    test-fixture layouts read exactly the file they mean)."""
    graph = Path(root)
    main = locations.git_common_root(graph)
    if main is not None and main != graph:
        # inside a git repo: the MAIN checkout's graph root.
        graph = locations.find_project_root(main) or main
    return graph


def _shared_seats_path(root: Path) -> Path:
    """The MAIN checkout's `nodes/.geometry/seats.md`, identity for a
    non-worktree caller — the resolution `locations.git_common_root` performs
    (hypothesis:l4-a-seats-identity-cell-has-one-writer-and-it-writes-main).
    The seats row a rotation writes lives in MAIN, so this reader addresses
    the same copy. Only a real linked-worktree call rebases to MAIN; a caller
    in the main checkout or outside git keeps its own literal root (the
    legacy/graph-root and test-fixture layouts read exactly the file they
    mean)."""
    graph = _shared_graph_root(root)
    if (graph / locations.GRAPH_DIR_NAME / "nodes").is_dir():
        graph = graph / locations.GRAPH_DIR_NAME
    return geometry_config.geometry_config_path(graph) or (
        graph / "nodes" / ".geometry" / "posts.md")


def _commit_push_seat_row(root: Path, row: dict, seat: str,
                          origin: str) -> None:
    """CLAUSE (2) commit+push for a key-cell writer's own-row write.
    Commits the seat's own-row hunk as ONE pathspec commit on MAIN's season
    branch through SL6.01's `rotate._commit_spawn_row` (never a second copy)
    and pushes that branch via its push leg. Best-effort, never raises,
    never fails the mint: a refused commit or push prints one note line to
    stderr and the key stays minted."""
    try:
        import rotate  # local: same dir (send.py pattern, no import cycle)
    except Exception as exc:  # noqa: BLE001
        print(f"note: {origin} row commit/push skipped ({exc})",
              file=sys.stderr)
        return
    def _int(v):
        try:
            return int(v or 0)
        except (TypeError, ValueError):
            return 0
    try:
        out = rotate._commit_spawn_row(
            root, seat=seat, generation=_int(row.get("generation")),
            session_id=str(row.get("session_id") or ""),
            window=str(row.get("window") or ""),
            pid=_int(row.get("pid")))
        print(f"note: {out.splitlines()[0]}", file=sys.stderr)
    except Exception as exc:  # noqa: BLE001
        print(f"note: {origin} row commit/push skipped ({exc})",
              file=sys.stderr)

def _all_live_seats_content(root: Path, top: Path,
                            keyed_names: list[str]) -> str | None:
    """The seats.md blob the `--all-live` keygen commit should stage: HEAD's
    content with ONLY the changes that carry THIS pass's keyed rows applied
    (a changed line whose `name` cell keys one of the keyed seats, or the
    whole-node frontmatter `edited_by:` stamp the same write owns), and every
    FOREIGN change REVERTED to the committed (HEAD) line. Base is HEAD, never
    the index -- a pre-staged foreign hunk cannot ride the keygen commit.
    Returns None when there is no keyed-row change to stage.

    A multi-row generalisation of rotate._seats_ownrow_content (send.py never
    edits rotate.py; sibling rows sit ADJACENT so git's unified diff folds an
    own and a foreign row into ONE hunk -- the cut is therefore made per
    CHANGED LINE, into an in-memory buffer, never onto the working tree). The
    caller stages this content into the index via update-index (working tree
    untouched), so the keygen commit carries exactly the rows it keyed and
    every foreign hunk stays unstaged and byte-untouched in the tree.
    """
    import difflib  # local: only the buffer-builder needs it
    rel = os.path.relpath(_shared_seats_path(root), top)
    try:
        run = subprocess.run(["git", "-C", str(top), "show",
                              f"HEAD:{rel}"],
                             capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if run.returncode != 0:
        return None
    try:
        work = _shared_seats_path(root).read_text(encoding="utf-8")
    except OSError:
        return None
    base_lines = run.stdout.splitlines()
    work_lines = work.splitlines()
    cells = [f'"name": "{n}"' for n in keyed_names]

    def _own(l: str) -> bool:
        # a changed line is KEYED when its row-cell `name` names one of the
        # keyed seats, or it is the top-level YAML `edited_by: <writer>`
        # frontmatter provenance stamp the SAME write owns (value-agnostic:
        # the writer's actor, not a seat name -- mirror rotate._own_row_line).
        stripped = l.lstrip("+- ")
        if stripped.startswith("edited_by: ") or stripped == "edited_by:":
            return True
        return any(c in l for c in cells)

    staged: list[str] = []
    b = w = 0
    any_own = False
    sm = difflib.SequenceMatcher(None, base_lines, work_lines, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        staged.extend(base_lines[b:i1])
        removed = base_lines[i1:i2]
        added = work_lines[j1:j2]
        for k in range(max(len(removed), len(added))):
            old = removed[k] if k < len(removed) else None
            new = added[k] if k < len(added) else None
            is_own = ((old is not None and _own(old))
                      or (new is not None and _own(new)))
            if is_own:
                any_own = True
                if new is not None:
                    staged.append(new)   # keyed change: keep working line
                # else: a keyed deletion -- append nothing
            elif old is not None:
                staged.append(old)        # foreign change: keep committed line
        b, w = i2, j2
    staged.extend(base_lines[b:])
    if not any_own:
        return None
    return "\n".join(staged) + "\n"

def _commit_push_all_live(root: Path, keyed_names: list[str]) -> str:
    """CLAUSE (2)/(4b) -- the `--all-live` keygen commit: ONE commit of
    seats.md carrying EXACTLY the rows this pass keyed, whose message names
    EVERY seat it keyed (`keygen --all-live: keyed <a>, <b>, <c>`), then the
    clause-(2) season-branch push leg. Resolved against MAIN's graph tree (a
    linked-worktree caller commits MAIN, never its own fork). Staging seats.md
    ONLY AND ONLY the keyed rows: the committed blob is HEAD's seats.md plus
    exactly those rows (generalising rotate's own-row discipline -- see
    :func:`_all_live_seats_content`), committed against a THROWAWAY index
    seeded from HEAD via update-index --cacheinfo (working tree NEVER
    written), so keygen --all-live never sweeps a foreign writer's uncommitted
    row edit into its commit -- the foreign delta stays byte-untouched and
    uncommitted in the working copy. Best-effort, never raises, never fails
    the mint: a refused commit or push prints one note line to stderr and the
    keys stay minted. Returns the one note line.
    """
    listed = ", ".join(keyed_names)
    note = f"keygen --all-live: keyed {listed}"
    try:
        import rotate  # local: same dir (send.py pattern, no import cycle)
        import tempfile
        main_root = _shared_graph_root(root)
        top = rotate._git_toplevel(main_root)
        if top is None:
            _l = f"note: {note} — no git repo; rows stay uncommitted"
            print(_l, file=sys.stderr)
            return _l
        seats = _shared_seats_path(root)
        rel = os.path.relpath(seats, top)
        new_content = _all_live_seats_content(root, top, keyed_names)
        if new_content is None:
            _l = f"note: {note} — seats.md already clean after the write; " \
                "nothing committed"
            print(_l, file=sys.stderr)
            return _l
        # Build the keyed-only blob and commit it against a THROWAWAY index
        # seeded from HEAD (GIT_INDEX_FILE=<tmp>; read-tree HEAD, then
        # hash-object the content and update-index --cacheinfo under it) and
        # commit against THAT index with no pathspec, so git resolves the
        # committed tree from the temp index, never the working tree. The
        # shared seats.md working copy and every foreign hunk stay byte-
        # untouched throughout.
        fd, tmp_index = tempfile.mkstemp(prefix="alllive-idx-")
        os.close(fd)
        env = dict(os.environ)
        env["GIT_INDEX_FILE"] = tmp_index

        def _tmp_git(parts, input=None):
            return subprocess.run(["git", "-C", str(top)] + parts,
                                  capture_output=True, text=True, env=env,
                                  timeout=10, input=input)

        rc = None
        blob_sha = ""
        try:
            seed = _tmp_git(["read-tree", "HEAD"])
            if seed.returncode != 0:
                raise RuntimeError(seed.stderr.strip())
            blob = _tmp_git(["hash-object", "-w", "--stdin"],
                            input=new_content)
            if blob.returncode != 0 or not blob.stdout.strip():
                raise RuntimeError(blob.stderr.strip())
            blob_sha = blob.stdout.strip()
            upd = _tmp_git(["update-index", "--add", "--cacheinfo",
                            f"100644,{blob_sha},{rel}"])
            if upd.returncode != 0:
                raise RuntimeError(upd.stderr.strip())
            msg = f"keygen --all-live: keyed {listed}"
            rc = _tmp_git(["commit", "-q", "-m", msg])
        finally:
            try:
                os.unlink(tmp_index)
            except OSError:
                pass
        if rc is None or rc.returncode != 0:
            _l = f"note: {note} — git commit failed: " \
                f"{rc.stderr.strip() if rc else 'unknown'}"
            print(_l, file=sys.stderr)
            return _l
        # point the REAL index's seats.md at the committed blob so the keyed
        # rows no longer show staged; only foreign hunks remain.
        subprocess.run(["git", "-C", str(top), "update-index", "--add",
                        "--cacheinfo", f"100644,{blob_sha},{rel}"],
                       capture_output=True, text=True, timeout=10)
        push = rotate._push_season_branch(root)
        _l = f"note: {note}; {push}"
        print(_l, file=sys.stderr)
        # g15.26 claim (b): a successful all-live push means origin now
        # carries every committed row's pubkey -- so the completion loop runs
        # rotate's ONE shared helper for EVERY live row (not only the rows
        # this pass keyed). A live KEYED seat -- skipped by the walk because
        # it already carried a pubkey, so never in keyed_names -- is exactly
        # the seat that owns a `.key.pending` (only an already-keyed seat's
        # row could have committed the successor pubkey before an earlier
        # push FAILED), and this is the site that completes its deferred
        # swap. The helper is a strict NO-OP unless `push:` starts `push: OK`
        # AND a pending file exists whose pub_hex matches the committed row,
        # so looping every live row is safe and idempotent: a keyed seat
        # with no pending file, and a freshly-keyed seat, both keep their
        # `.key` byte-identical. Best-effort; never raises.
        _run_pending_swap_completion(root, push)
        return _l
    except Exception as exc:  # noqa: BLE001
        _l = f"note: {note} row commit/push skipped ({exc})"
        print(_l, file=sys.stderr)
        return _l

def _run_pending_swap_completion(root: Path, push: str) -> None:
    """g15.26 claim (b) -- run rotate's ONE shared pending-swap completion
    walk over every live row. Strict NO-OP unless ``push`` starts
    ``push: OK`` AND a pending file exists whose pub_hex matches the COMMITTED
    row, so looping every live row is safe and idempotent: a keyed seat with
    no pending file, and a freshly-keyed seat, both keep their `.key`
    byte-identical. Best-effort; never raises."""
    if not str(push or "").startswith("push: OK"):
        return
    import rotate  # local (send.py pattern)
    for _row in _seats_rows(_graph_root(root)):
        _live_name = str(_row.get("name") or "")
        if _live_name and _live_row(_row):
            rotate._finish_pending_swap_on_push(root, _live_name, push)

def _all_live_origin_sync_line(root: Path) -> str:
    """g15.26 claim (b) -- the push-like line the NO-WRITE --all-live path
    feeds the pending-swap completion walk. An ALL-KEYED registry (the
    steady state: every live row already keyed, wrote_any False) never
    commits or pushes of its own: it only confirms origin already carries
    HEAD's committed rows (a fetch + rev-parse READ, never a push) and
    reports ``push: OK`` only when origin is exactly at HEAD -- that is what
    makes completing a deferred swap against the already-pushed state safe.
    Any other outcome yields a non-``push: OK`` line so the walk stays a
    strict NO-OP (a deferred swap stays deferred until origin truly holds the
    committed successor row). Never raises."""
    import rotate  # local (send.py pattern)
    main_root = _shared_graph_root(root)
    top = rotate._git_toplevel(main_root)
    if top is None:
        return ("push: SKIPPED -- no git repo (gitless fixture/root); "
                "nothing to complete")
    try:
        branch_out = subprocess.run(
            ["git", "-C", str(top), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return "push: SKIPPED -- could not resolve the branch"
    branch = (branch_out.stdout or "").strip()
    if not branch or branch == "HEAD":
        return "push: SKIPPED -- detached HEAD, nothing to complete"
    try:
        fetch = subprocess.run(
            ["git", "-C", str(top), "fetch", "origin", branch],
            capture_output=True, text=True, timeout=60)
    except Exception as exc:  # noqa: BLE001
        return f"push: SKIPPED -- fetch failed ({exc}); cannot verify origin"
    if fetch.returncode != 0:
        return ("push: SKIPPED -- fetch failed, cannot verify origin carries "
                "the committed rows")
    try:
        head = subprocess.run(
            ["git", "-C", str(top), "rev-parse", "HEAD"],
            capture_output=True, text=True, timeout=10).stdout.strip()
        oref = subprocess.run(
            ["git", "-C", str(top), "rev-parse", f"origin/{branch}"],
            capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:  # noqa: BLE001
        return "push: SKIPPED -- could not compare HEAD to origin"
    if head and oref and head == oref:
        return f"push: OK -- {branch} (origin already carries HEAD)"
    return (f"push: SKIPPED -- origin {oref or '?'} is not at HEAD "
            f"{head or '?'}; a deferred swap stays deferred")
