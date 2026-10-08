---
id: experiment:a00-bc250f78-245b3e
mint_id: f310b538d96e4247b0f9e2cdf7278d49
type: experiment
parents:
  - hypothesis:l2w15-write-guard
next_edges: []
confidence: 0.85
edited_by: ubuntu
evidence_runs:
  - experiment:a00-bc250f78-245b3e
loop: hypothesis:l2w15-write-guard@s1
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 89aa7088048cb73a
season: 1
title: A00 bc250f78 245b3e
verdict: inconclusive_lean_proved:85
---
# experiment:a00-bc250f78-245b3e

## Experiment

Implemented the SETTLED (owner 2026-09-06) mint-id rekey of the write log
and write_guard, closing the last open item on hypothesis:l2w15-write-guard
and unblocking `write.py retitle` (L3 brief §2.7b).

Changes:
- `node_writer._log_write` / `log_write`: every log line now carries `mint_id`,
  read from the node's frontmatter at write time. `write_node` and
  `update_node` pass `fm.get("mint_id","")`. A payload created before its node
  exists (ensure_payload raising a build node's mint_id unknown at creation)
  logs without one and relies on the sha256-only fallback.
- `snapshot-goals.log_write` (public wrapper) unchanged in signature — it can
  omit the new optional param; guard falls back to sha-only.
- `write_guard._load_log`: returns a `Sanctioned` matcher holding two sets —
  `by_key = {(mint_id, sha256)}` and `by_sha = {sha256}`. `has(mint_id, sha)`
  matches (mint_id, sha) first, sha256-alone as fallback for bytes written
  before a node carried a mint_id.
- `write_guard.cmd_check`: reads the changed node's `mint_id` from its
  frontmatter and uses `san.has(mi, sha)`; cleans up the leftover `sha_to_path`
  return for redo hints. Payload check also keys on `(mint_id, sha256)`.
- `_read_payload_refs` now carries each build node's `mint_id`.

Red-first tests added to `test_write_guard.py`:
- `test_write_log_carries_mint_id`, `test_update_log_carries_mint_id` —
  the logged mint_id equals the mint_id actually stamped into the node.
- `test_git_mv_logged_node_stays_silent` — a clean `git mv` of a logged node
  must not WARN (was the L2.13 follow-up #1 defect).
- `test_hand_edit_after_git_mv_still_warns` — a hand edit to the moved node's
  bytes must still WARN under `--strict`.

## Evidence

Verify commands and output:

```
$ python3 -m pytest extensions/agi/tests/test_write_guard.py -q
................                                          [100%]
16 passed in 0.62s
```

(4 new mint-id / git-mv tests included; 12 pre-existing still green.)

```
$ python3 -m pytest extensions/agi/tests/ -q
... 1745 passed, 1 skipped in 96.26s
```

```
$ python3 extensions/agi/bin/write_guard.py check ; echo "EXIT=$?"
EXIT=0
```

Repo scope is silent against HEAD — no unsanctioned writes. The rename
defect (L2.13 follow-up #1) is closed: a logged node moved via `git mv`
keeps its `(mint_id, sha256)` log line, so the check is silent, while a hand
edit after the move changes the bytes and warns. This is the precondition the
owner named for `write.py retitle`.

## Agent Notes
Foreign files seen before/while working, not created by me, left untouched:
MOD `conftest.py`, `driver.sh`; UNTRACKED `test_agi_env_strip.py`,
`.agi/nodes/hypothesis/l3w1-goal-kind-perpetual.md`,
`.agi/nodes/hypothesis/l3w1-tier0-director-brief.md`,
`.agi/nodes/experiment/a00-737e29f7-e656af.md`. Mine: `node_writer.py`,
`write_guard.py`, `test_write_guard.py`, and this node.

## Agent Notes
Mint-id rekey of write log + write_guard: log lines carry mint_id, check indexes (mint_id,sha)+sha fallback; git mv of logged node silent, hand edit after mv warns; red-first tests green, full suite 1745 green, repo check exit 0.

Parent review (a00-e8dffc43): ACCEPTED as-is, no demotion. parents resolves to hypothesis:l2w15-write-guard (exists). verdict inconclusive_lean_proved:85 is an honest lean with evidence_runs=[self], a valid self-naming experiment run. Verified the artifact, not the report: node_writer._log_write now logs mint_id and write_node/update_node pass it; write_guard._load_log returns a Sanctioned matcher keying (mint_id,sha) with sha-only fallback; payload refs carry mint_id. Read the new tests (git mv silent / hand-edit-after-mv warns) — real, red-first, run against a throwaway tmp git repo. Re-ran: test_write_guard 16 passed; test_write+node_writer+snapshot_goals 171 passed; repo write_guard check exit 0. Closes L2.13 follow-up #1; unblocks write.py retitle. Minor caveat banked (not blocking): snapshot-goals.py write_frontmatter log_write omits mint_id, relying on sha-only fallback — functionally fine (bytes unchanged => silent), a candidate for a future tightening.
