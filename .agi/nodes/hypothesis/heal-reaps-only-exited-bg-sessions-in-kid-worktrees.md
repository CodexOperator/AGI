---
id: hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees
mint_id: da5b5a4470e64793896da42b5bedaf54
type: hypothesis
parents:
  - hypothesis:pin-reap-never-names-a-live-session-and-a-reap-leaves-no-stale-app-session
  - goal:g6.49
next_edges: []
edited_by: director-engine
scaffold_hash: d77870f915a65130
season: 2
testable_claim: A heal/reap verb runs claude rm only with an explicit live flag and only on background, exited sessions whose cwd is a kid worktree; the default dry run prints candidates and skips; it never passes rm's force flags.
title: "heal reaps only exited --bg sessions whose cwd is a kid worktree, dry-run by default (assigned: director-engine)"
town: core
---
# hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees


# hypothesis:heal-reaps-only-exited-bg-sessions-in-kid-worktrees

## Measured
- OWNER 01:0xZ 09-26 (2c, via belam's card 38460c40f): "the app lists only live sessions". belam [decision] gen 9, 08:45Z 09-26 (VERIFIED): GO for an engine round -- "the heal/reap verb, dry-run default, live only on exited --bg sessions whose cwd is a KID worktree, never interactive or Remote Control, never the repo root; it lands through the normal gate."
- `claude agents --json --all` (CLI 2.1.283) lists sessions with {id, kind: background|interactive, state|status, cwd}; `claude rm <id>` deletes an exited background session and its worktree only "when that is safe".
- director-engine ran the one approved removal by hand 08:4xZ: `claude rm 5861181b` -> "removed 5861181b", rc 0; the session left the listing; its worktree .agi/worktrees/a00-5aaa03c7 was KEPT (a dirty .agi/config.json) and its branch kept -- rm refuses to lose uncommitted work.
- Still listed after: 710907bf (background, done, cwd = repo root) -- the owner's, must NEVER be a candidate.

## CLAIM
A heal/reap verb lists candidate sessions from `claude agents --json --all` and, only with an explicit live flag, runs `claude rm <id>` on exactly those that are kind=background AND exited (done/stopped) AND whose cwd is inside `.agi/worktrees/a00-*` (a kid worktree, resolved through the locations resolver); the default is a dry run that prints the candidates and why each other session was skipped, and it never passes rm's --discard-unpushed / --force-remove-worktree.

## Dispatch line
config-max: the kid-worktree prefix resolves through locations (never a literal path) / template-max: none / code: one heal.py verb (or rotate.py reap sub-verb) with the `claude` CLI behind a seam.

## FALSIFIERS
1. With a fixture listing {kid --bg exited, kid --bg RUNNING, repo-root --bg exited, interactive in a kid worktree, a Remote Control row}: anything but the first is a candidate.
2. The default (no live flag) invokes `claude rm` at all.
3. Any test execs the real `claude` binary (TMM.202: never start or touch a real claude session in a test -- seam only).
4. The verb ever passes --discard-unpushed or --force-remove-worktree.

## TESTS
a new test file with a fake `claude` on PATH (records argv, prints fixture JSON) -- the real binary is never reached.

## FILE SCOPE
extensions/agi/bin/heal.py (or rotate.py reap) -- one verb + one seam; the commands manifest entry (.agi/nodes/.geometry/commands.md); its test; this node + its experiment.

## CEILING
1-2 kids · ~50 production lines · pi-free · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
belam gen 9, [decision] 08:45Z 09-26, verbatim: "GO for claude rm 5861181b ONLY (a kid exited --bg throwaway probe in a kid worktree: the loop own artifact, and the owner 2c asks for exactly this end state). 710907bf (cwd repo root) and every class-B app row stay the owner call -- banked on my card. GO for the engine round too: the heal/reap verb, dry-run default, live only on exited --bg sessions whose cwd is a KID worktree, never interactive or Remote Control, never the repo root; it lands through the normal gate."
<!-- THOUGHT:END -->
