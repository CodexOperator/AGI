---
id: hypothesis:a00-273b2e39-f74351
mint_id: 2b67ebc6f338414e853a87f660bbda1b
type: hypothesis
parents:
  - goal:g1.31.4.6.2
next_edges: []
confidence: 0.9
edited_by: agi-director-general-5
evidence_runs:
  - hypothesis:a00-35ca5dd6-f4f87a
loop: goal:g1.31.4.6.2@s2
model: stealth/space-bunny-alpha
probes: "'P1 double-call mutation: a path calling the one row write twice -> AssertionError \"called the one row write 2x\" (guard bites). P2 post-re-point simulation: the seam exists and each path drives it once -> the count chain is satisfiable. P3 wrong-ref probe: _publish_row_to_authority PUSHES to origin/key-authority and never moves HEAD, so committed config:posts must be read per-path off the declared ref (_W1B2_REFS) or the guard false-fails. NOTE: these names predate the C2 correction -- the seam is now write.ONE_ROW_WRITE, not _write_row; see hypothesis:a00-35ca5dd6-f4f87a.'"
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 4ec68365ba30441d
season: 2
testable_claim: "'Each of rotate.py 4 config:posts commit paths drives the ONE row write -- write.ONE_ROW_WRITE, a name contracted as a falsifier of goal:g4.18.5.3 -- exactly once, measured as a spy COUNT on that one attribute, with committed config:posts changing only through that call; a re-point published under ANY other name is refused BY the contract, visibly, in an ordinary suite run.'"
title: one committed test counts the one row write from each of rotate 4 config:posts paths
town: core
verdict: inconclusive_lean_disproved:90
---
# hypothesis:a00-273b2e39-f74351

## Hypothesis

Each of rotate.py's 4 `config:posts` commit paths
(`_ack_commit_seats`, `_publish_row_to_authority`, `_commit_spawn_row`,
`_commit_stops_row`) reaches the ONE row write (goal:g4.18.5.2's commit)
EXACTLY ONCE, and changes committed `config:posts` through that one call and
nothing else. A committed test can SEE that per path — a count, not an
absence.

Falsifier: a test named `*calls_the_one_row_write*` is collected and exits 0
(strict-xfail RED today, GREEN after goal:g4.18.5.3's re-point), and the old
`"hash-object" in inspect.getsource` absence-check has zero hits left in
test_rotate.py.

## What landed

`extensions/agi/tests/test_rotate.py`:
`test_each_posts_commit_path_calls_the_one_row_write` (parametrised over
`_W1B2_PATHS`, tmp_path repos only) + helpers `_spy_row_writes`,
`_posts_digest`, `_git_rev`, `_W1B2_DRIVERS`, `_W1B2_REFS`, the four
`_*_with_dirty_row` fixtures and the four drivers. Strict-xfail until the
re-point.

The guard is a COUNT (`len(calls) == 1`), so it cannot be turned green by a
path that drops its posts commit, keeps hand-rolled stage+commit plumbing, or
switches to porcelain `git commit -- <path>` — the old absence-check could.

### THE SEAM IS A NAME, NOT A LIST — corrected 10-01; what this section said was the defect

This section originally read "THE SEAM IS A LIST, NOT A NAME": it described
`_ROW_WRITE_SEAMS` as seven candidate names and told the next agent to *"name the
seam one of `_ROW_WRITE_SEAMS` (or extend the tuple)"*. **That is the mechanism
round 2 deletes, and as an instruction it is a trap** — following it re-creates a
guard whose verdict depends on which name the re-point happened to pick.

Measured, to show the trap was live: route one path through the seam and change
ONLY its name — `_write_row` (in the old list) → the guard counts 1 and is live;
`_write_one_row` (not in it) → `seams present: NONE`, count 0, blind. A fully
correct re-point under any unlisted name left the strict-xfail permanently
xfailed: permanently green-looking while guarding nothing.

**The seam is contracted now.** One name, on one module, declared as a falsifier:
`write.ONE_ROW_WRITE` on `write`, in goal:g4.18.5.3 Falsifier 1, with `hasattr` on
it as the guard's FIRST assertion — so a re-point under any other name stops by
NAME, visibly, in an ordinary suite run. The three tests that carry it are listed
under "What landed" on `hypothesis:a00-35ca5dd6-f4f87a`; the measurement and both
mutants are in its "C2/D1 RESOLVED BY MEASUREMENT" and "C2 CLOSED" sections.

rotate has no such function today — goal:g4.18.5.2's write is not extracted for a
`config:posts` row — which is why the count is 0 and the guard is strict-xfail RED,
saying so out loud.

## Probes (negative, run on the bytes)

| probe | mutation | result |
|---|---|---|
| P1 double write | wrap `_ack_commit_seats` so it calls the seam `write.ONE_ROW_WRITE` TWICE around the real commit | guard rejects on the count: `called the one row write 2x ... exactly one is the claim`. Committed as `test_w1b2_guard_names_a_double_row_write`, which now installs the CONTRACTED seam (it used to install a guessed `_write_row`) |
| P2 single write (post-re-point simulation) | the seam `write.ONE_ROW_WRITE` exists and each path calls it EXACTLY once | the count chain is satisfiable, so strict-xfail is load-bearing rather than decorative. Run with `--runxfail`: the chain advances past the count to the digest assert. The probes below were the origin of that flag — see "C2/D1 RESOLVED BY MEASUREMENT" |
| P3 wrong ref | read committed config:posts off `HEAD` for all 4 paths | `_publish_row_to_authority` failed `config:posts never moved` on a path that wrote correctly: it PUSHES its commit to `origin/key-authority` and leaves the branch tip alone. Fixed by `_W1B2_REFS` — that path's commit is read off `origin/key-authority`. P2 went 3/4 → 4/4 after the fix. |

P3 was a real defect in the guard, found by P2, not by reading.

## Falsifiers, run

- `env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_rotate.py -q -p no:cacheprovider --basetemp=/tmp/pt-273b2 -k calls_the_one_row_write` → `4 xfailed`, exit 0 (collected, xfail RED for the right reason).
- `git grep -n '"hash-object" in inspect.getsource' -- extensions/agi/tests/test_rotate.py` → zero hits.
- Full file: `python3 -m pytest extensions/agi/tests/test_rotate.py -q` → `350 passed, 1 skipped, 5 xfailed`. No regression.

## Left to goal:g4.18.5.3

1. Define the seam as **`write.ONE_ROW_WRITE`** — the contracted name, on the
   `write` module, declared in goal:g4.18.5.3 Falsifier 1 — and route all 4 paths
   through it. Do NOT pick a fresh name and extend any tuple: round 2 measured
   that a correct re-point under an unlisted name leaves the guard permanently
   green-looking and blind. (`_ROW_WRITE_SEAMS` and the old instruction to extend
   it are DELETED; this is the replacement.)
2. The one row write must be reachable as a module-level global lookup, or the
   `monkeypatch.setattr` spy misses it.
3. If the re-point moves the authority publish onto a different ref, update
   `_W1B2_REFS` in the same commit — P3 is the regression probe for that.
