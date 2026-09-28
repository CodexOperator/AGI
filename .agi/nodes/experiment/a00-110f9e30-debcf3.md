---
id: experiment:a00-110f9e30-debcf3
mint_id: 747e3737d0f241dd8f38c199623f6fa5
type: experiment
parents:
  - hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent
next_edges: []
confidence: 0.8
edited_by: a00-298f04df
evidence_runs:
  - experiment:a00-110f9e30-debcf3
loop: hypothesis:a-stale-index-lock-is-cleared-or-named-and-a-failed-round-commit-is-never-silent@s2
model: stealth/space-bunny-alpha
probes:
  - "PARENT PROBES (a00-d4da08e3, DH.668) — 4/4 run by ME, scripts probe_p1.py + probe_p23.py (NOT in the tree and NOT re-runnable from the repo: .agi/sessions/ is gitignored, .gitignore:104; the outputs below are pasted; P1 re-run in EG.45 from `git archive 37bf99a1a extensions` with cli.py:2413 reverted to `return \"?\"` -> `1 failed, 17 passed, 6 warnings in 0.97s` (FAILED test_a_pid_that_exits_between_the_fd_listing_and_the_stat_is_not_a_holder); restored -> `18 passed, 6 warnings in 0.78s`), tmp repos only, env -u TMUX -u TMUX_PANE. The kid's suite is its CLAIM, not my evidence. | P1 gate/base-bytes falsifier (item 3): MY OWN /tmp copy of extensions/agi with the ONE arm reverted (return \"\" if sexc.errno == errno.ENOENT else \"?\" -> return \"?\") and the NEW fixture run against it -> 1 failed, 2 passed, 15 deselected; the failure is test_a_pid_that_exits_between_the_fd_listing_and_the_stat_is_not_a_holder with assert '?' == ''. The fixture DISCRIMINATES base from tree, so the round is not vacuous. | P2 gate/item-5 exactness, run LIVE: with the fixture built for target pid 2102, os.stat('/proc/2102') raises the INJECTED PermissionError while /proc/21020, /proc/2102x and /proc/2102/fd do NOT. startswith, or an f-string segment form, would have darkened the neighbour and let the narrowness assertion go green for the wrong pid. Latent on this host; closed in the fixture. | P3 wire/visited-and-named (item 3, the binding half): _lock_is_held(lock, repo) under the fixture returns the STRING /proc/4194303 (?) fd table unreadable (unreadable) -- holder UNKNOWN, lock NOT removed — the synthetic pid is genuinely VISITED by the walk, because a pid is visited iff os.listdir('/proc') yields it. | P3b gate/same-visited-pid-ENOENT: that identical pid with an ENOENT stat -> 'cleared stale index.lock ... age=3600s > 60s, no git holder', reason None, lock gone. The arm is load-bearing on this fixture, not decoration. | P3c gate/fresh-lock NEGATIVE control under the same fixture: age 0s -> index.lock ... age=0s stale_after=60s held=no -- NOT removed, lock still on disk. The fixture does not make the gate pass everything."
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f3f0e6d28c7a61fe
season: 2
title: A pure /proc fixture replaces the host-bound pid hunt, and three cites of a function that never existed are repaired
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
# experiment:a00-110f9e30-debcf3

## What this round did

DH.668 corrective on the residue of DH.627 (mur-director-engine-38, accept_with_residue). NOT the feature:
the four test-fixture residue items, plus the two node-text items. Production bytes: **0**.

| item | shape | what landed |
|---|---|---|
| 1 | three cites of a function that does not exist | `experiment:a00-064385b1-d30690.md` :59, :172, :199 `workflow.py _round_git_wait` -> `_round_git_harvest` (def at :2167; the `rec.get("status")` first branch at :2225), via write.py `sub!` / `sub` |
| 2 | `experiment:a00-9dfef904-01bf3b.md` had no verdict, no evidence_runs | `verdict: inconclusive_lean_proved:70` + `evidence_runs: [a00-9dfef904-01bf3b, a00-064385b1-d30690]` + a `note` saying the verdict is the PARENT's review of a dead kid's bytes. The links.py half is an OUTSIDE finding below; links.py untouched |
| 3 | VACUOUS test: a fabricated pid the walk never visits | the pid is now named by the LISTING (item 4 fixture) |
| 4 | HOST BINDING in `_a_live_same_uid_pid_not_us` | that helper is GONE; `_synthetic_proc` replaces the whole `/proc` table |
| 5 | NUMERIC PREFIX match in `fake_stat` | gone with the same helper; the stat match is EXACT equality |

## ITEM 4 FIRST — the fixture (items 3 and 5 live inside it)

```
    _SYNTH_PID = 4194303   # a pid no host runs, and the ONLY one the fixture lists

    def _synthetic_proc(monkeypatch, pid, fd_exc, stat_exc):
        real_listdir, real_stat = os.listdir, os.stat
        def fake_listdir(p, *a, **k):
            if str(p) == "/proc":
                return [str(pid)]                       # THE LISTING is the fix
            if str(p) == f"/proc/{pid}/fd":
                raise fd_exc[0](fd_exc[1], "unreadable", str(p))
            return real_listdir(p, *a, **k)
        def fake_stat(p, *a, **k):
            if str(p) == f"/proc/{pid}":                # EXACT (item 5)
                raise stat_exc[0](stat_exc[1], "no stat for you", str(p))
            return real_stat(p, *a, **k)
```

Why this is the only shape that closes all three items at once:

```
  question                        old shape                       new shape
  -----------------------------------------------------------------------------------
  is the pid VISITED?              no: max(pid)+7 is free, so     yes: the walk only ever
                                   `os.listdir("/proc")` never    visits what the listing
                                   yields it -> arm unreached     returns, and the listing
                                   (item 3: provably vacuous)     returns ONLY it
  does it need a host?             yes: needs a live same-uid     no: no os.stat of a real
                                   non-git pid or it RAISES on a   /proc entry ever happens
                                   minimal container (item 4)       (the stat arm raises), so
                                                                nothing about the box is read
  can a neighbour answer for it?   yes: startswith("/proc/4194303")
                                   also matches /proc/41943030    no: `str(p) == f"/proc/{pid}"`
```

ITEM 5, said once and precisely: the tight form is `str(p) == f"/proc/{pid}"` (EXACT EQUALITY), not the
`f"/proc/{pid}/" in str(p)` segment form. The stat this fixture intercepts is the pid DIRECTORY
(`/proc/<pid>`: the `os.stat(base)` `_uninspectable` calls at cli.py:2405 -- NOT cli.py:2407, which is the uid-0 `os.stat(f"{base}/fd")` arm; exact equality never intercepts that one, and neither test reaches it because the :2405 stat raises first); there is no subpath to segment on, so the
segment form buys nothing and only widens the blast radius. Under it, `/proc/41943030` and
`/proc/4194303/fd` both match the pid under test, so the EACCES assertion in
`test_a_stat_that_fails_with_anything_but_ENOENT_still_refuses` could be satisfied by a NEIGHBOURING pid
and the "the fix is NARROW" half would be green for the wrong reason. This one is LATENT, not live on
this host: no real pid here is a digit-extension of another, so the old test was not wrong today.

## PROBES (one per item, run by me)

Class GATE for items 3+4+5 (a test fixture's probe is the falsifier of the OLD test): the SAME new
fixture run against the BASE bytes — a /tmp copy of `cli.py` with the one line of the fix reverted to
`return "?"  # BASE: no ENOENT arm on the stat` — and against the CURRENT bytes. Copy + revert + run in
this session dir under `base_probe/`.

```
BASE  env -u TMUX -u TMUX_PANE python3 -m pytest <session>/base_probe/extensions/agi/tests/test_stale_index_lock.py -q \
        --basetemp=/tmp/dt668base -k "exited_mid_walk or exits_between or anything_but"
  ...
  >       assert cli._uninspectable(f"/proc/{pid}", PermissionError(13, "denied")) == ""
  E       AssertionError: assert '?' == ''
  ...
  FAILED ...::test_a_pid_that_exited_mid_walk_is_not_a_holder
  FAILED ...::test_a_pid_that_exits_between_the_fd_listing_and_the_stat_is_not_a_holder
  FAILED ...::test_a_stat_that_fails_with_anything_but_ENOENT_still_refuses
  3 failed, 15 deselected in 11.19s

TREE  env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stale_index_lock.py -q --basetemp=/tmp/dt668tree
  18 passed, 6 warnings in 3.81s
```

Read honestly, one of the three base failures is the first run's fault, not the fix's: the base copy was
missing `extensions/agi/src`, so all three died on `ModuleNotFoundError: No module named 'graph_core'`
before touching a byte. `cp -r extensions/agi/src` into the copy and re-run, and the real picture is:

```
  1 failed, 2 passed, 15 deselected in 0.21s
  FAILED test_a_pid_that_exits_between_the_fd_listing_and_the_stat_is_not_a_holder
  E   AssertionError: assert '?' == ''
```

ONE test discriminates, which is the correct number, not a shortfall:

- `..._exits_between_the_fd_listing_and_the_stat...` FAILS on base, PASSES on tree. That is the fix under
  test, exercised for the first time: pre-fix the ENOENT on the stat was an UNKNOWN HOLDER ("?"), which
  refused every commit on a host that spawns and reaps agents. The old test could not see this because
  (item 4) it needed a live same-uid pid and (item 3) its sibling's pid was never visited.
- `..._exited_mid_walk...` and `..._anything_but_ENOENT...` PASS on both sides BY DESIGN: they are the
  pre-existing arms (the listdir-ENOENT exit, and the EACCES-narrowness guard). They are the
  POSITIVE-HALF controls — a fixture that over-refuses, or a fix widened to `except OSError: return ""`,
  would still be caught by the second one. They are NOT evidence for the fix and I do not count them as
  such. A new test that passes on both sides is vacuous; these two are not new, they are the arms the new
  one had to keep honest, and I say so rather than let three green ticks imply three findings.

## Regression run, both suites, once each

```
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stale_index_lock.py -q --basetemp=/tmp/dt668tree
  18 passed, 6 warnings in 3.81s
env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/dt668smoke
  72 passed, 7 skipped in 43.97s
```

The 3.81s is itself a datum: DH.627 measured 60.68s for the same 18. The synthetic table is ONE pid
instead of the whole live `/proc`, so the walk stopped walking the box.

## Ceiling, measured

DH.668 kid round (the test fixture), working tree against that round's base:

```
git diff --numstat -- extensions/agi/bin/cli.py extensions/agi/tests/test_stale_index_lock.py
42      39      extensions/agi/tests/test_stale_index_lock.py
```

Production **net 0** against a 40-line budget (cli.py never opened; the brief's 15-line production budget
is headroom, not a target, and this round needed none). Test net **+3** against the `<= 40` test cap —
DOWN from DH.627's disclosed +76 overage, because the 15-line host-bound helper it bought is deleted and
one 22-line fixture serves all three tests. No re-brief needed.

Corrective range, measured against the CUT tip `dedca8545` (EG.64, before this block was pasted; the
final range incl. this block is pasted on `experiment:a00-298f04df-fe3499`):

```
git diff --numstat dedca8545
2       2       .agi/nodes/experiment/a00-110f9e30-debcf3.md
```

Production **0**, test **0** -- node text only, inside the 0/0 cap.

## OUTSIDE FINDING (item 2, second half — NOT touched, links.py is out of file scope)

`.agi/context/schemas/[experiment].md` -> `validation.required: [id, type, mint_id, title]`, and
`extensions/agi/bin/links.py:470 _schema_report` validates exactly that required list, so a node whose kid
DIED before `done` — no `verdict`, no `evidence_runs`, no title — is schema-CLEAN and links.py prints
nothing about it. The exact shape item 2 had to be closed by hand is the shape the linter cannot see.
One sentence: making the evidence requirement checkable needs a `cli.py done`/harvest-side probe, not the
schema (the schema's own repair rule, quoted in that file, forbids requiring a field the corpus does not
use — and on experiments it does not).

## The near miss this round avoided, named for the next one

Reading the two fixes as "add a pid number" — `max(pid)+7` for item 3, a wider skip list for item 4. Both
are green and both are wrong: a pid is VISITED iff `os.listdir("/proc")` YIELDS it, so the number is not
where the bug lives, it is in the LISTING; and any skip rule in the helper is a host binding that still
raises on a host with no other same-uid pid. The fixture removes the host question rather than answering
it.

## Files

- `extensions/agi/tests/test_stale_index_lock.py` (test only, in FILE SCOPE)
- `.agi/nodes/experiment/a00-064385b1-d30690.md` (item 1, write.py only)
- `.agi/nodes/experiment/a00-9dfef904-01bf3b.md` (item 2, write.py only)
- this node

No unexpected files seen in the tree. No git beyond the one read-only `--numstat` measurement.

## Agent Notes
DH.668 residue: one pure synthetic /proc fixture retires the host binding (item 4), the never-visited pid (item 3) and the numeric-prefix stat match (item 5) at test net +3; base-vs-tree falsifier shows the ENOENT-on-stat test FAILS on the pre-fix bytes; the three _round_git_wait cites now name workflow.py:2167; the dead kid's node carries a lean verdict and evidence. Production net 0.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
EG.64 corrective (mur-eg-14 EG.45-k1 accept_with_residue), node text only. WHY THIS VERSION DIFFERS: (1) the body line on the pid-dir stat dropped its round pointer "corrected in EG.45 per mur-eg-13"; the delta it recorded now lives here: EG.45 moved that cite from cli.py:2407 (the uid-0 os.stat of <pid>/fd, now 2407-2408) to cli.py:2405 (os.stat(base), the one the fixture intercepts), re-read in the bytes at dedca8545. (2) the Ceiling section now labels its 42/39 numstat as the DH.668 round and adds the corrective range measured against the CUT tip dedca8545 (production 0, test 0). The DH.668 parent review that this block carried before is in the prior grid version, unchanged.
<!-- THOUGHT:END -->
