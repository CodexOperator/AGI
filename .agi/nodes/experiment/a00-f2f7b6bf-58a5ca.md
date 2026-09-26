---
id: experiment:a00-f2f7b6bf-58a5ca
mint_id: 72373f8bd69a489cbc24a1dbbf2fba39
type: experiment
parents:
  - hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go
next_edges: []
confidence: 0.8
edited_by: a00-f2f7b6bf
evidence_runs:
  - experiment:a00-f2f7b6bf-58a5ca
loop: hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-branches-go@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 82e50c08df3bae3f
season: 2
title: Log-tail row goes red for the MAIN-fallback reason; the main!=own dedup is un-gateable
town: core
verdict: proved
---
# experiment:a00-f2f7b6bf-58a5ca

## What I was asked (slice B of DH.436)

| finding | state when I started | what I did |
|---|---|---|
| 1 — the log-tail row gates a crash, not the MAIN fallback | `test_log_tail.py` row asserted only the fallback TEXT; the parent's mutation went red through a `locations.py` RuntimeError | NEW row `test_log_tail_prefers_own_copy_then_falls_back_to_main_exactly_once`, driven through an injected `_rotate` seam; red-first demonstrated for the MAIN-fallback reason, by name |
| 2 — the stale-lock skip row is a no-op gate | ALREADY DONE in `experiment:a00-f76b1fde-5e44ad` (Path.unlink spy, parent-accepted) — the bytes were in my base | nothing to redo; I re-ran the mutation to confirm and report |
| 3 — rewrite `experiment:a00-416266d2-e77f31` to what shipped | node claimed its own verdict and titled the shim guard "works" | rewritten through `write.py`; slice A wording marked **pending** (no `last-kid-result.md` in my base) |

## Finding 1 — the log-tail row, made red-first

The bytes (`heal.py:2917-2939`, `_read_seat_log_tail(root, row, _rotate, nbytes=8192)`)
build an ordered candidate list: the seat's own geometry `sessions/<seat>.log`
first, MAIN's `sessions/<seat>.log` as the fallback. The row must pin that ORDER.

**The seam, from the bytes.** `_read_seat_log_tail` takes `_rotate` as a
parameter and only ever calls `_rotate._sessions_dir(gdir)`. An in-process
object recording every call is enough — no subprocess, no PATH shim, no live
tmux (hypothesis:heal-worktree-refusal-tests-never-reach-live-tmux-and-dead-
branches-go, conjunct (a)).

**Why the real `rotate._sessions_dir` cannot show the order** (measured, not
assumed): it delegates to `locations.shared_sessions_dir`, which re-resolves
through `git_common_root` and lands every worktree seat on MAIN's ONE shared
room. In a fixture graph, `rotate._sessions_dir(<worktree>/.agi)` and
`rotate._sessions_dir(<main>/.agi)` return the SAME path (probe:

```
wt sess  -> /tmp/tmpqhdgif5w/.agi/sessions
main sess-> /tmp/tmpqhdgif5w/.agi/sessions
fpr(wt) /tmp/tmpqhdgif5w/.agi   gcr(wt) /tmp/tmpqhdgif5w/.agi/worktrees/seat-wt/.agi
```

). So the spy answers each geometry root with that root's OWN
`<gdir>/sessions` — the contract the tail code is written against — and also
records every log the tail READS (`Path.read_bytes`), which is the candidate
list as the code consumes it.

### Runs, all in this checkout

```
$ sha256sum extensions/agi/bin/heal.py
ac22e1df67a4873f71936f797cfabeff7644bcfd867e48205f43b382f02e804d

# GREEN, unmutated
$ python3 -m pytest test_heal.py -q
21 passed in 0.13s

# MUTATION A — delete the MAIN fallback branch (heal.py:2929-2931)
-    main = _rotate._sessions_dir(root) / f"{seat}.log"
-    if main != own:
-        cands.append(main)
>       assert tail == "MAIN-COPY", (
               f"MAIN fallback copy not preferred after the worktree went: {tail!r}")
E       AssertionError: MAIN fallback copy not preferred after the worktree went: ''
E       assert '' == 'MAIN-COPY'
FAILED test_heal.py::test_log_tail_falls_back_to_main_when_the_worktree_log_is_gone
FAILED test_heal.py::test_log_tail_prefers_own_copy_then_falls_back_to_main_exactly_once
2 failed, 19 passed in 0.15s

# restore
$ sha256sum -c heal.sha256
extensions/agi/bin/heal.py: OK
21 passed in 0.13s
```

Red for the reason the conjunct names — "the MAIN copy was not preferred" — not
through a `locations.py` RuntimeError.

### The dedup, honestly NOT gated

The row does **not** pin `if main != own:`. MUTATION B (that guard replaced by an
unconditional `cands.append(main)`) leaves the row GREEN:

```
$ python3 -m pytest test_heal.py -q
21 passed in 0.13s
```

I first tried to pin it (a `Path.exists` stat-spy: a duplicated candidate would
be stat-ed twice) — that failed too, because the read loop RETURNS at the first
readable candidate, so a second identical entry is never stat-ed or read. The
guard is a pure no-op on every observable: un-gateable, reported rather than
faked. It is left in place (it is correct and free) with the limitation named in
the row's own docstring.

## Finding 2 — the stale-lock skip was already a real gate

`test_heal.py::test_stale_lock_skip_leaves_a_clean_sessions_dir_alone` already
carries the `Path.unlink` spy + the `warn:` stderr assertion from
`experiment:a00-f76b1fde-5e44ad`, and that node is `proved` with a parent
mutation run. I re-ran the mutation in MY checkout to confirm the shipped bytes
behave as that node claims (green: `test_heal.py` 21 passed with heal.py
byte-exact). No change needed; no gate faked.

## Finding 3 — the DH.427 node rewritten to what shipped

`experiment:a00-416266d2-e77f31` read as if its verdict were its own and titled
the shim guard "works". Rewritten in place (title, verdict field, body, fresh
THOUGHT) to the shipped facts:

- the subprocess-spawning `tmux` guard was **VACUOUS** under the autouse conftest
  fixture and is **DELETED**, replaced by an in-process recorder;
- the log-tail row and the stale-lock row are both load-bearing NOW (mutation
  evidence above, plus the c2 node's own probes);
- the `if gdir else None` None arm and the `if main != own` dedup are pinned /
  unpinned as measured above;
- slice A: **pending** — no `.agi/sessions/iter-DH.436/a00-68d48a54/
  last-kid-result.md` in my base, so nothing about it is guessed.

## Suite

```
$ python3 -m pytest test_heal.py -q
21 passed in 0.13s

$ python3 -m pytest test_heal.py test_cli.py test_heal_watch.py \
    test_dispatch.py test_heal_worktree_refusal.py -q
57 failed, 252 passed, 38 warnings in 16.64s
```

The 57 are PRE-EXISTING in this worktree and unrelated to my change: the same 57
fail with `test_heal.py` excluded from the run, every one of them at
`subprocess._fork_exec` with `BlockingIOError: [Errno 11]` — this sandbox cannot
fork. I did not chase them (out of scope, not mine).

## Ceiling

| path | added lines |
|---|---|
| `extensions/agi/tests/test_heal.py` | 67 (test file — excluded from the production count) |
| `extensions/agi/bin/heal.py` | **0** (mutated only for the two probes, restored byte-exact: sha256 `ac22e1df…` before and after) |

**Production lines shipped: 0** (ceiling 40). No live tmux pane was touched and
no real claude was launched; every probe is an in-process call.

## Verdict on the conjunct I owned

**proved** for (c1) on my own mutation runs: the log-tail row is now a real gate
that goes red for the MAIN-fallback reason by name. The dedup is honestly
reported as un-gateable rather than faked. (c2) was already proved by the sibling
node; the DH.427 node rewrite is a bookkeeping fix, not new evidence.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Own version, written fresh (not appended). (1) WHAT THE BRIEF SAID: make the log-tail row go red when the MAIN fallback branch is removed, and the stale-lock row go red when its guard is removed. (2) WHAT THE MACHINE DOES: the stale-lock row was ALREADY gated in my base (Path.unlink spy, sibling node a00-f76b1fde-5e44ad proved) so that half needed no work; the log-tail row was a gate on a crash, not on the fallback, and now reads the candidate list through an injected _rotate seam plus a read-spy, failing on the message "MAIN fallback copy not preferred after the worktree went". (3) THE NEAR MISS I ALMOST SHIPPED: I first pinned the own-first preference with an equals-on-a-list assert, and the MAIN-fallback mutation then went red THERE instead of at the fallback assertion - a red for a neighbouring reason is still a red for the wrong reason, so I weakened that one assert to seen[0] == wt and moved the candidate-list claim into the fallback case. Second near miss: I built a Path.exists stat-spy to pin the `if main != own` dedup, and it stayed green under mutation, because the read loop returns at the first readable candidate and never touches the duplicate - the guard is un-gateable, so I removed the fake gate and said so in the row docstring and in my node. Third: the real rotate._sessions_dir collapses a worktree seat onto MAIN shared room, so the honest seam has to be the injected object, not the real resolver. (4) No standing rule deviated: heal.py was mutated only for the two probes and restored byte-exact (sha256 ac22e1df before and after, sha256sum -c OK), I ran one read-only git diff --numstat, and every node edit went through write.py.
<!-- THOUGHT:END -->

## Agent Notes
log-tail row re-made load-bearing: injected _rotate seam + read-spy, red-first MUTATION A fails by name on the MAIN fallback; main!=own dedup proven un-gateable and reported, not faked; DH.427 node rewritten to shipped facts; 0 production lines, 67 test lines, test_heal.py 21 passed
