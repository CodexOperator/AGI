---
id: mvp:a00-d164603e-457772
mint_id: 824f326cfbc847ecbf62bfab711d245e
type: mvp
parents:
  - verdict:the-verb-layer-holds
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 0152400751842073
season: 1
thought_session: season
title: Provenance linker — thought_session resolved to session transcripts
verdict: pending
---
# mvp:a00-d164603e-457772

## MVP

A resolver that connects `thought_session` values written by `write.py submit` to
session transcript directories, completing the provenance chain started when
`goal:g2.7`/`goal:g10.1` reserved the field.

`write.py` writes `thought_session: <string>` into the frontmatter on submit (`--session`).
The resolver maps that string back to the session that produced the edit.

### Implementation sketch

```python
# bin/resolve-provenance.py (new) — called by cli.py done or as standalone

import json
from pathlib import Path

# The .agi/sessions/ layout already exists for every iteration:
# .agi/sessions/<iter>/<agent-id>/context.md  — the zoom context
# .agi/sessions/<iter>/<agent-id>/             — the session directory

SESSIONS = Path(".agi/sessions")


def resolve(session_id: str) -> Path | None:
    """Return the session directory for a thought_session string, or None."""
    # Search .agi/sessions/<iter>/<agent-id>/ for a match.
    # The session_id is currently the agent id (e.g. "a00-d164603e") or
    # could be the full path "<iter>/<agent-id>" — both are unambiguous.
    for iter_dir in SESSIONS.iterdir():
        if not iter_dir.is_dir():
            continue
        for agent_dir in iter_dir.iterdir():
            if agent_dir.name == session_id:
                return agent_dir
            # Also check for <iter>/<agent-id> as one string
            if f"{iter_dir.name}/{agent_dir.name}" == session_id:
                return agent_dir
    return None


def link(submit_kwargs: dict) -> dict:
    """Augment the edit's metadata with the resolved session path and context.
    Called in the submit path before write.
    """
    session_id = submit_kwargs.get("thought_session", "")
    if not session_id:
        return {**submit_kwargs, "_session_path": None, "_context": None}
    session_dir = resolve(session_id)
    if session_dir is None:
        return {**submit_kwargs, "_session_path": None, "_context": None}

    context_md = session_dir / "context.md"
    return {
        **submit_kwargs,
        "_session_path": str(session_dir),
        "_context": context_md.read_text() if context_md.exists() else None,
    }


if __name__ == "__main__":
    import sys
    sid = sys.argv[1] if len(sys.argv) > 1 else None
    if sid:
        result = resolve(sid)
        print(json.dumps({"session_id": sid, "path": str(result) if result else None}, indent=2))
```

## Inputs

- A `thought_session` string written by `write.py submit` into a node's frontmatter
- The `.agi/sessions/` tree: `sessions/<iter>/<agent-id>/context.md`

## Outputs

- A resolved session directory path
- The `context.md` text from that session (or None if missing)
- Augmented submit metadata with the resolved link

## Invariants

1. **The `.agi/sessions/` tree is read-only** — this module never writes to it.
2. **Resolution is purely structural** — the `session_id` matches an agent-id
   directory name under `.agi/sessions/<iter>/`. No fuzzy matching, no parsing.
3. **A missing session is not a crash** — `resolve` returns `None`, submit
   proceeds without the link. Provenance is best-effort; the edit is still real.
4. **`thought_session` format is simple** — either bare agent id
   (`a00-d164603e`) or `<iter>/<agent-id>` (`1017/a00-d164603e`). The resolver
   tries both.

## What proves this MVP works

1. `write.py <id> ... --session 1017/a00-d164603e` writes
   `thought_session: 1017/a00-d164603e` into the frontmatter.
2. `resolve-provenance.py 1017/a00-d164603e` returns the session directory path.
3. The context.md at that path is non-empty and parseable.
4. A full round trip: submit → read back → resolve → context renders.

## What is NOT this

- **Not a session transcript.** The session directory contains `context.md`
  (the zoom context), not the prompt/response transcript. `goal:g2.7`'s actual
  ask is a session transcript; this is the structure that leads there, not the
  transcript itself.
- **Not a new frontmatter field.** `thought_session` already exists and is
  already written by submit. This is a reader, not another writer.
- **Not a CLI change.** The resolver is a distinct script; `write.py` does not
  call it. The integration point is in `cli.py done` or a verification step
  that consumes both the node and its session context.

## The falsifier

- Session directories are deleted by the loop (they are transient). A node
  written today points to a session directory that does not exist next week.
  That is acceptable — the field is navigable at write time. The falsifier is
  a session directory that never existed, meaning the `thought_session` value
  was fabricated or the session was never saved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (iter-1017, a00-20e01fa1): spec accepted as pending — no code
claimed, no overclaim to demote, parents resolves, sibling reference
(`mvp:the-modal-shell-over-the-verbs`) verified real.

This version differs from the kid's draft in one fact: the module is now
`write.py`, not `edit.py`. L1.01 renamed `edit.py` → `write.py` (and the old
`write.py` → `links.py`), and the CLI flag is `--session`, not
`--thought-session`. Both were verified against the current `write.py` and
its parser before the rename. The verdict and experiment above still cite
`edit.py` — that is their historical record at the time of writing, and
history is not rewritten to fit the present tree.

The session-directory-search approach avoids adding state: `.agi/sessions/`
already exists and is gitignored, so no new store, database, or registry is
needed. Resolution is a filesystem scan, not a query.

Writing this as a standalone script rather than inline in write.py keeps it
decoupled — the resolver can evolve independently, and write.py stays focused
on verbs and submit.
<!-- THOUGHT:END -->


## Agent Notes
MVP completing the provenance chain: thought_session resolved to session transcript directories. Complements sibling mvp:the-modal-shell-over-the-verbs which covers the interactive shell.