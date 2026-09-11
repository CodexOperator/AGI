---
id: experiment:a00-b643386a-164b6b
mint_id: 355aad4946e0483394e41e07d01a5987
type: experiment
parents:
  - hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly
confidence: 0.8
edited_by: a00-ca59f20b
evidence_runs:
  - experiment:a00-b643386a-164b6b
scaffold_hash: cb1cc7e5336deca3
title: A00 b643386a 164b6b
verdict: proved
---
# experiment:a00-b643386a-164b6b

## Experiment

Built the fix named by `hypothesis:l4-stall-candidate-measures-an-api-bound-parent-honestly` — the
`_round_status` verdict must not call a live, API-bound parent a STALL-CANDIDATE. Three edits to
`extensions/agi/bin/spawn_budget.py` (scope was hard-limited to that file + its test):

1. **Tick sample raised to the director's stall definition (8 s)**, as a module constant
   `TICK_SAMPLE_SECONDS = 8` and an overridable seam `_STATUS_SAMPLE_SECONDS = TICK_SAMPLE_SECONDS`
   that `_round_status` reads. The old `time.sleep(2)` was a bare literal — too short to catch a
   parent between API calls, and unreadable by tests.
2. **`_pid_established_sockets` → `_pid_sockets`** (renamed to say what it now does). The old helper
   counted only ESTABLISHED (state `01`) TCP sockets from `/proc/net/tcp|tcp6`; a parent mid-review
   holding a LISTEN/CLOSE-WAIT port or a unix control socket read `sockets=0`. The new helper
   intersects the pid's `socket:[inode]` fd links against the inode sets of `/proc/net/tcp`,
   `/proc/net/tcp6` (now ANY TCP state — the state-`01` filter is gone) and `/proc/net/unix`
   (inode is column 6, never `cols[-1]` because a trailing Path may hold spaces). Returns 0 on any
   unreadable edge, as before.
3. **Verdict line carries the numbers.** STALL-CANDIDATE is printed ONLY when all four signals say
   stalled (0 ticks over the 8 s sample, 0 sockets, 0 live kids, no terminal agent.json status).
   Every other parent-alone case prints `round L.NNN: parent alive, reviewing (ticks=N, sockets=M)`
   instead of the old generic `(active)` that hid the evidence it had just measured.

Tests in `extensions/agi/tests/test_spawn_budget.py` (31 pass):
- The FALSIFIER: a fake sampler reporting ticks>0/sockets=0 prints `reviewing`, NOT STALL-CANDIDATE;
  and the mirror: ticks=0/sockets=3 prints `reviewing`, NOT STALL-CANDIDATE. Both inject the
  samplers through monkeypatched module globals (`_pid_ticks`/`_pid_sockets`) and shrink the sample
  window via the `_STATUS_SAMPLE_SECONDS` seam, so no test sleeps 8 s.
- A `_pid_sockets` unit test against a synthetic `/proc` tree (redirected `Path`): verifies a
  LISTEN(0A) tcp6 inode and a unix inode both count, an unheld CLOSE_WAIT inode and an anon_inode
  do not, and a path-less unix row is parsed (inode column 6).
- The existing 4 `test_status_iter_*` tests stay green (sample shrunk through the seam).

## Evidence

Full-suite run: `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` → `31 passed`.

Real-tree probe (live round L4.176 on this tree — parent a00-9922846f + kid a00-401afaa5), command
`python3 extensions/agi/bin/spawn_budget.py status --iter L4.176`:

```
  a00-401afaa5 tier=kid pid=2187138 elapsed=989s ticks=0 sockets=2 agent=(no agent.json)
  a00-9922846f tier=parent pid=2180275 elapsed=1165s ticks=0 sockets=3 agent=(no agent.json)
round L176: parent alive, 1 live kid(s)
```

The round was FOUND; the live parent reported `sockets=3` (2 for the kid), which the pre-fix
helper — counting only ESTABLISHED TCP — would very plausibly have reported as 0, exactly the
L4.167/L4.170/L4.172 false-CANDIDATE class. The verdict correctly reads `parent alive, 1 live
kid(s)`, not STALL-CANDIDATE. Note the probe took 16 s wall (8 s per live row, two rows): the 8 s
sample is the honest, documented cost of the director's stall definition and scales with round size.

## Agent Notes
8s tick constant + _pid_sockets counts any TCP state + unix; verdict line carries numbers; STALL-CANDIDATE only on 0/0/0/no-done; falsifier+unit+real-tree(3 sockets) prove it.

PARENT REVIEW (a00-ca59f20b, L4.177) — ACCEPTED, verdict proved stands. Read the ARTIFACT not the report: spawn_budget.py:62 TICK_SAMPLE_SECONDS=8; :67 the _STATUS_SAMPLE_SECONDS seam; :507 _pid_sockets counts any TCP state (:545 drops the cols[3]=="01" filter) plus /proc/net/unix inode column 6; :618 calls it; :635-641 STALL-CANDIDATE gated on 0 ticks AND 0 sockets AND 0 kids AND no terminal. Verified by running `python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q` -> 31 passed in 1.01s. Both falsifier fixtures fail on the pre-fix bytes (the ticks>0 case: pre-fix printed the generic "(active)"; the sockets=3 case: pre-fix used _pid_established_sockets and read 0 -> CANDIDATE). Renamed helper has no stale callers (grep: only the docstring mentions the old name). Scope check by mtime: only spawn_budget.py, test_spawn_budget.py and the node file changed. CAVEAT recorded below. No demotion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS FROM THE KID'S: the kid's version asserted proved on its own report; this version carries the parent's independent check of the bytes and one honest caveat. (1) THE INSTRUCTION SAID: the target claim is that the tick sample is 8 s, the socket count includes unix + non-established sockets, and CANDIDATE is printed only when 0 ticks AND 0 sockets AND 0 live kids AND no done:. (2) THE MACHINE ACTUALLY DOES: verified at spawn_budget.py:62 (TICK_SAMPLE_SECONDS = 8), :507-552 (_pid_sockets intersects the pid fd socket inodes against /proc/net/tcp, /proc/net/tcp6 — ANY state, the old cols[3]=="01" filter gone — and /proc/net/unix inode column 6), :635-641 (all four conditions ANDed). Ran `pytest extensions/agi/tests/test_spawn_budget.py -q` -> 31 passed. (3) THE NEAR MISS: a version that kept the state-01 filter and merely renamed the helper would satisfy the words "counts sockets" and lose the mechanism — L4.170/L4.172 held unix/listening sockets, which state-01 never sees; the kid kept the actual intersection, so the near miss was avoided. (4) DEVIATION FROM A STANDING RULE: none — the kid stayed exactly in the declared file scope. WHAT IS WEAK: the node's real-tree paragraph says the pre-fix helper "would very plausibly have reported as 0" for the parent's 3 sockets — that is a plausibility, not a measurement (the pre-fix helper no longer exists to run against that live pid). The claim itself is still proved by the fixture falsifiers, which DO fail on the pre-fix bytes. Second cost, documented and accepted: the 8 s sample is paid per live row, so status --iter on a 5-agent round takes 40 s wall.
<!-- THOUGHT:END -->
