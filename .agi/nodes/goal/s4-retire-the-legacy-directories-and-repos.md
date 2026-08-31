---
confidence: 1.0
goal_id: S4
goal_kind: short-term
heading_level: 2
id: "goal:s4"
mint_id: 351125dd5d3942a2aa032920cb12771c
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
title: "S4: Retire the legacy directories and repos"
type: goal
---

Housekeeping carried from TODO **C1–C6**, gated on bug-sweep clearance and
grouped here because none of it is worth its own long-term goal:

- `~/autoresearch-tree/` local directory (C1) and the
  `CodexOperator/autoresearch-tree` repo (C2) — archive rather than delete.
- The old pi fallback under `~/.pi/agent/git/.../extensions/autoresearch-tree/`
  (C3), pending verification that nothing resolves through it.
- The modularNN spike worktree (C4) and legacy `~/.hermes/agi/` artifacts (C5).
- `.claude/skills/gitnexus/*/SKILL.md` accidentally tracked (C6).

Do these last. Every one is a deletion, and the two data-loss defects this
project has already paid for both arrived as routine cleanup.

## `agi-tree` disarmed 2026-08-31 — and it shows the cheaper move

`~/work/agi-tree` still carried `agi-tree.config.json` after `goal:g11` moved
the graph into `agi/.agi/`, so both resolvers answered that it was a **live**
legacy project — and its `source_root` resolved through the
`agi -> ~/work/agi` symlink to the *live engine*. A loop run from there would
have rewritten that repo's `GOALS.md` from 809 stale goal nodes and minted
build nodes from live engine source into the retired graph. Nothing warns,
because the resolver is behaving correctly for what the marker file claims.

Found the way these things always are: the owner opened the directory out of
habit and asked whether the session's work had landed there. It had not.

**The fix was one `git mv` of the marker file** (`agi-tree.config.json` →
`.RETIRED`, commit `bb9d29be8` in that repo). Files, history and remote
untouched.

**That is the generalisable part, and it should shape the rest of this list.**
A legacy directory is dangerous because it still *identifies* as a project,
not because it still exists. Renaming the one marker file removes every
hazard — nothing resolves it, nothing writes to it — while keeping the archive
intact and the change reversible in one command. Deletion buys nothing extra
and is the operation whose two failures this goal already warns about.

So: **disarm first, on everything here that carries a marker; decide about
deletion later, separately, or never.** The two steps were being treated as one
and they are not.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The node was a checklist of five deletions with a sensible warning attached.
What changed is not the list but the shape of the work: acting on one item
showed that the hazard and the storage are separable, and that only the hazard
needs addressing now.

Written in as a general rule rather than a note under one bullet, because the
same reasoning covers `~/autoresearch-tree/` and the pi fallback path — both
are dangerous for exactly the reason `agi-tree` was, and both can be defused
without deleting a byte. That also resolves the tension in the closing warning:
"do these last, every one is a deletion" was true and is why nothing had
happened, and splitting off the reversible half means the risky half can keep
waiting indefinitely at no cost.

Kept at `horizon`: one item is handled, the rule is stated, nobody is working
the rest.
<!-- THOUGHT:END -->
