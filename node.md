---
id: hypothesis:mem-cap-probe-cache-is-private-and-atomic
mint_id: 2404c6c29a634d0881b5b9bdaf62fcc1
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass7-0926-residue-batch
next_edges: []
edited_by: a00-d8e5d627
scaffold_hash: f550a789f2281019
season: 2
testable_claim: The mem_cap probe cache lives in a per-user private dir, is written atomically, and a corrupt, partial or foreign-owned cache is ignored and re-probed.
thought_session: belam-S2-L5-VII
title: "the mem_cap probe cache is private and atomic (assigned: director-engine)"
town: core
---
# hypothesis:mem-cap-probe-cache-is-private-and-atomic

# hypothesis:mem-cap-probe-cache-is-private-and-atomic

assigned: director-engine. PASS 7 residue (hypothesis:pass7-0926-residue-batch).

## Measured
mem_cap.py:79 falls back to a predictable path in /tmp for the per-boot probe cache (landed with the goal:g6.49 hot patch 48e16356f0) and writes it with plain write_text: non-atomic, and a predictable /tmp path can be pre-created by another user.

## CLAIM
The probe cache lives in a per-user private dir (0700), is written atomically (temp file + os.replace), and a corrupt, partial or foreign-owned cache is ignored and re-probed.

## Dispatch line
config-max: the cache dir resolves through the existing locations resolver, not a literal / template-max: none / code: the write + trust check in mem_cap.py.

## FALSIFIERS
A pre-created symlink or foreign-owned file at the old path is followed or trusted; a partial write is read as a verdict.

## TESTS
extensions/agi/tests/test_mem_cap*.py -- a fake probe on tmp_path, never a real systemd-run.

## FILE SCOPE
extensions/agi/bin/mem_cap.py · its tests

## CEILING
1 parent (pi-free) · <= 2 kids · 10-12 production lines per conjunct · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
the dir is the unit of privacy, not the file: a 0700 dir we own plus an atomic replace plus a body that must be exactly 0 or 1 -- all three were needed, and the pre-fix replay showed a planted symlink being written THROUGH
<!-- THOUGHT:END -->
