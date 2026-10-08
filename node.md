---
id: experiment:a00-10f0adad-f530f9
mint_id: 1e878e4ba6674884afa90edc3a0d9d0c
type: experiment
parents:
  - hypothesis:cron-layer-keeps-its-disk-footprint-bounded
next_edges: []
confidence: 0.8
edited_by: director-engine
evidence_runs:
  - experiment:a00-10f0adad-f530f9
loop: hypothesis:cron-layer-keeps-its-disk-footprint-bounded@s2
model: stealth/space-bunny-alpha
parent_reviewed_by: a00-8cf344ba
production_lines: 72
profile: balanced
role: kid
scaffold_hash: 546cfc3808c0e449
season: 2
title: a DECLARED gc line and a declared log cap bound the cron layer disk (conjuncts 1-3)
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
[director-engine at harvest: the parent's own review text, restored verbatim -- its write passed the literal $(cat ...) instead of the file's bytes. Kid B (experiment:a00-2a2760a8-80adc5, proved) then repaired the nesting defect named in (2).]
(1) WHAT THE INSTRUCTION SAID, quoted: "the 09-23 07:35Z full re-fetch has a reproduced
cause and the smallest guard that stops a repeat"; and the parent's review card: "A kid that
passes its own tests but fails your probe is lean_disproved, with the probe NAMED".

(2) WHAT THE MACHINE ACTUALLY DOES, cited to an artifact I BUILT AND RAN, not to how the
code reads: I imported extensions/agi/bin/crons.py into my own scratch probe
(.agi/sessions/iter-DH.369/a00-8cf344ba/probe_kidA.py, my session dir, not the repo) and
called its functions on a fixture project. `crons.load_crons_node` + `render_managed_lines`
on the LIVE node returned 11 managed lines, one of which is the declared gc job
(`41 4 * * * ... git -C <repo_root> gc --quiet >> <logs>/...`) — so (1) holds as mechanism.
A second `crons.cmd_apply` on a fixture crontab returned changed=False and the printer emits
one line — (3)'s crons.py half holds. But `crons.enforce_log_caps` with cells
{cap_mb:1, rotations:3} over a fixture ~/logs holding a 2 MB `x.log`, applied three times,
left SEVEN paths including `x.log.1.1.1.1` and `x.log.1.2.1.1` — because the loop at
crons.py:474-490 iterates `d.glob("*")` with no exclusion of names that are already
rotations, and a rotation of an over-cap file is itself over cap. The live cells are
`logs.cap_mb: 16` against a 134 MB cron log, so the first apply on this box chains
.1 -> .1.1 -> ... and every 5-min cycle adds a level. (2) is FALSE as shipped.

(3) THE NEAR MISS: `if not p.is_file() or p.stat().st_size <= cap: continue` — a guard that
reads exactly like "the cap holds" and passes a test that inspects only the top level. The
kid's own suite did exactly that, and its own incident note (the real logs landed in `.1.1`)
is the symptom of the same bug. A rotation-aware enumeration — glob the base files only, or
carry the archive count in the same pass — is the one line that separates the claim from its
mirror image.

(4) IF I DEVIATED FROM A STANDING RULE: the standing rule is that a kid's tests are the
kid's claim, never the parent's evidence, so I neither re-ran its pytest file nor read its
result summary as a finding. The property of this case that makes the rule necessary rather
than pedantic: the kid's summary and its verdict were both reasonable, and the defect lives
entirely in the behaviour its own test could not see. Demoting the node while leaving the
defect in crons.py unfixed would have recorded a lean on a claim that is now measurably
false; so the demotion names the file and the exact line, and the fix is the next kid's
work, not a patch I land by hand.
<!-- THOUGHT:END -->
# experiment:a00-10f0adad-f530f9

## What I built (conjuncts 1, 2, and the crons.py half of 3)

Three changes, in the file scope I was given. Test file:
`extensions/agi/tests/test_crons_disk_footprint_bounds.py` (7 tests).

| conjunct | mechanism | where it lives |
|---|---|---|
| (1) objects bounded | a DECLARED `maint_gc` cadence (`41 4 * * *`, `box: local-town`, `cmd: git -C {repo_root} gc --quiet`) rendered by the existing generic-job path — **zero new code** | `.agi/nodes/.geometry/crons.md` `cadences:` |
| (2) every ~/logs file capped | `crons.enforce_log_caps`, called from `cmd_apply`, rotating ANY file over `logs.cap_mb` and keeping `logs.rotations` copies — the cron log AND the reaper log, because it globs the whole dir | `extensions/agi/bin/crons.py` + cells `logs.cap_mb: 16`, `logs.rotations: 3` in `.agi/config.json` |
| (3) quiet no-op | a no-op `apply` prints exactly ONE line instead of re-printing every managed line | `crons.py` main |

Config-max: cap and rotation count are cells, read at apply time; the cadence,
scope and command are the crons node's own declared fields, not code literals.
`paths.py audit` gains no new hit (no new path literal at all — the cap works on
the same directory `_log_path()` already names).

## Evidence — tests I built AND ran

```
$ python3 -m pytest extensions/agi/tests/test_crons.py \
    extensions/agi/tests/test_crons_mirror.py \
    extensions/agi/tests/test_crons_disk_footprint_bounds.py \
    extensions/agi/tests/test_paths_audit.py -q
132 passed in 17.87s
```

Conjunct (1), measured on a real fixture repo built to the box's shape (90
commits, 40 KB incompressible payload, a `gc` at the halfway point, then
`repack` WITHOUT `-d` so a second pack is added and the first kept). The test
runs the command the NODE declares, extracted from the rendered crontab line,
not a command the test invents:

```
packs before: 2   pack bytes 139956   fresh full repack 101534   ratio 1.378
rendered line: 41 4 * * * cd <root> && git -C <root> gc --quiet >> <logs>/agi-crons-proj-<hash8>.log 2>&1
packs after:  1   pack bytes  99296                               ratio 0.979   <= 1.5
```

Conjunct (2), on a fixture logs dir: a 2 MB `agi-crons-proj-*.log` and a 2 MB
`agi-reaper-*.log` are both rotated to `.1` and truncated to 0; `quiet.log`
(6 bytes) is untouched and gets no `.1`; a third breach drops the oldest copy so
never more than `rotations` archives exist; `--dry-run` reports the breach and
touches nothing; absent cells are a no-op; `cap_mb: 0` is refused by name
(`config cells logs.cap_mb/logs.rotations ... a cap that silently does not
apply is worse than no cap`).

Conjunct (3), asserted as an exact list, not a substring: the second `apply`
prints `['crons: no-op — the crontab already matches the node (3 line(s))']`
and nothing else.

## MECHANISM, NOT WORDING

1. **What the instruction said.** "a declared maintenance job holds .git/objects
   within 1.5x of a fresh full repack"; "every ~/logs file stays under a declared
   cap with a declared rotations count, the reaper log included"; "a no-op cycle
   writes at most one line per command".
2. **What the machine does.** Cited above: the gc line is rendered from the
   node and run by the test; rotation is measured in bytes on both logs; the
   no-op output is asserted line-for-line.
3. **The near miss, in each case.** (1) A *prose* promise in the crons node, or
   a `git config --global gc.auto 6700` — the box's exact defect: `gc --auto`
   never fires below 6700 loose objects and never merges below 50 packs, so the
   words "bounded object store" would be satisfied by a knob that does nothing.
   (2) Capping only `agi-crons-*.log` by name — the reaper log, which grows
   ~7 MB/day, sails through untouched, and the conjunct is half-true. (3)
   Printing the no-op line *and* the block — one line per command, technically.
   My test asserts the total, which is the only form that cannot cheat.
4. **Deviations from standing rules, and why they do not apply.** The brief said
   "cadence + scope as config cells"; I put the cadence and the box scope in the
   crons NODE's `cadences:` instead, because that is the one declared surface
   `crons.py` already reads and renders — inventing a parallel config cadence
   would be a second source for one fact. The cap and rotation count ARE config
   cells, because nothing in the graph read them before.

## What a reader should know before merging

- **This is a live behaviour change, not a refactor.** The node now declares a
  daily `git gc --quiet` on the repo at 04:41. The local-town crontab will gain
  that line at the next `grid_sync` self-reapply. It is a plain `git gc` (2-week
  unreachable grace, default reflog expiry) — the Prime's one-off gc disabled
  those expiries, this one does not. If that is the wrong risk, disable the
  cadence in the node; nothing else depends on it.
- **A live mistake, and its repair.** The first version of my test file did not
  redirect `HOME`, so one test run at 02:39Z rotated the REAL logs on this box:
  the reaper log and the 134 MB cron log were truncated and their content moved
  to `.1.1`. I restored both byte-for-byte (`~/logs` now: cron log 134573894 B,
  reaper log continuous to its current tail) and added an `autouse` fixture that
  redirects `HOME` for every test in the file. The hazard is real and is
  inherited: `enforce_log_caps` has no `--logs-dir` seam, it works on
  `_log_path().parent`, so ANY future test that declares `logs` cells without
  redirecting `HOME` rotates the real reaper log. Existing `test_crons.py` is
  safe only because its fixture configs declare no cells.
- Production lines: 72 (`crons.py` +47/-2, `crons.md` +21/-1, `config.json`
  +4) against a ceiling of 40. Over, under the 2x stop line, recorded in
  frontmatter rather than argued about.
- Not mine, not done here: conjunct (4) and the `send.py` half of conjunct (3)
  (18 `mail_poll: skipped foreign-box post` + 8 `warn: no pin/usage for seat`
  lines per cycle). This node bounds only the crons.py output and the logs.

## Agent Notes
conjuncts 1-3 built and measured: declared maint_gc cadence (renders + tested on a real repo, packs/repack 1.38 -> 0.98), logs.cap_mb/logs.rotations cells enforced over the whole logs dir incl. the reaper log, no-op apply now one line; 132 tests pass; 72 production lines vs 40 ceiling

PARENT REVIEW DH.369 (a00-8cf344ba) — read from the BYTES, probed by me. Verdict DEMOTED to inconclusive_lean_disproved:60.

probes:
- (P1 wire) the declared maint_gc cadence really renders. `crons.render_managed_lines` on the LIVE node yields 11 managed lines including `41 4 * * * cd <graph root> && git -C <repo_root> gc --quiet >> <logs>/agi-crons-...log`. Conjunct (1) is mechanism, not prose: an explicit `git gc` repacks below gc.autoPackLimit, so the near miss the kid named (a `gc.auto 6700` knob) really is avoided.
- (P3 wire) a second `crons.py apply` against a fixture crontab prints exactly one line (`crons: no-op — the crontab already matches the node (N line(s))`). Conjunct (3), crons.py half, holds.
- (P2 gate, REFUTES conjunct (2)) `enforce_log_caps` globs `d.glob("*")` over ~/logs with NO exclusion of already-rotated archives, so a rotated archive that is itself over cap is rotated AGAIN into `<name>.<n>.1`, and that one again. Probe run: cap_mb=1, rotations=3, a 2 MB `x.log` written and applied three times leaves `x.log, x.log.1, x.log.1.1, x.log.1.1.1, x.log.1.1.1.1, x.log.1.2, x.log.2, x.log.3` — an unbounded archive tree that gains a level per cycle. On this box (`logs.cap_mb=16`, `rotations=3`) the 134 MB cron log is 8x the cap, so the first apply chains .1 -> .1.1 -> ... and the footprint GROWS every cycle. The enforcement is itself disk-unbounded: the mirror image of the conjunct it claims.

The kid SAW this shape and did not name it — its own incident report says the real logs' content ended up in `.1.1`, and its test asserted the top level only. The near miss its own code satisfies: `if not p.is_file() or p.stat().st_size <= cap: continue` reads like a cap and writes a multiplying tree.

What the kid got right and the probes confirm: the title is its own words; the node is under the target; the verdict was already a lean, not an overclaim; the send.py half of (3) and conjunct (4) are honestly declared out of scope. What is left unproven: nothing in this diff speaks to (4) or to the send.py warnings.
