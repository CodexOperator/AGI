---
id: goal:s4
mint_id: 351125dd5d3942a2aa032920cb12771c
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S4
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: horizon
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S4: Retire the legacy directories and repos"
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

## Completed the same day: archive, then make it read-only

The owner's call was to finish the job rather than leave a half-retired repo:
push everything, then close it. Both halves matter and the order is not
optional — an archived GitHub repo refuses pushes, so the archive has to be
*complete* before it is *sealed*.

**Verified complete ref-by-ref, not assumed:** 3 branches and 1080 grid refs on
the remote at the same sha, zero local-only refs. `master` was 5 ahead and
`iter24-extend-300hop` 9 ahead; both pushed. Those 9 were not unique work —
every one is reachable from `master`, so the remote branch pointer was merely
stale. Worth recording, because that is the branch `CLAUDE.md` warns about and
someone will eventually go looking for lost commits on it.

**Then three guards, and the third is the non-obvious one:**

1. marker file renamed — no tooling resolves it,
2. repo archived on GitHub — remote read-only, pushes get 403,
3. a local `pre-commit` hook that refuses.

**(3) exists because of (2).** Once the remote is read-only a local commit
still *succeeds* — it just becomes unpushable and sits in that working copy
forever, with nothing saying so until someone tries. Sealing the far end
converts a loud failure into a silent one, so the near end needs a refusal to
match. That generalises to every item left on this list: **whatever makes a
thing unwritable remotely creates a new silent-failure mode locally, and both
ends have to be closed together.**

All three are reversible: unarchive in settings, `git mv` the marker back,
delete the hook. Nothing was deleted at any point.

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

Second pass the same day, after the owner said to finish rather than leave it
half-retired. The addition worth flagging is the third guard, which was not in
the plan and came out of testing the second: archiving the remote made a local
commit *succeed* and become unpushable, which is a worse failure than the one
being prevented. Sealing one end created a silent failure at the other. That is
now written as the general rule for the remaining items rather than as a note
about this one, because `~/autoresearch-tree/` and the pi fallback path will
each hit it in the same shape.
<!-- THOUGHT:END -->