---
id: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
mint_id: 812b7aa1f51f4fb881bc9a69df812b74
type: hypothesis
parents:
  - goal:send-is-hub-only-dm-file-versions-synced-every-30s
next_edges: []
confidence: 0.75
edited_by: director-engine
scaffold_hash: 6fcee7280f2effca
season: 2
tags:
  - engine
  - send
  - boxes
testable_claim: "(1) seating writes the row box cell from AGI_BOX (2) this_box refuses an unset AGI_BOX and an empty or unknown row box is never local (3) the foreign-row refusal prints once per row+cause, names the box, and sends no keys (assigned: director-engine)"
title: "every live row carries its own box from AGI_BOX; an unset or unknown box is refused on every box, once per row+cause (send-is-hub-only, belam 00:35Z; assigned: director-engine)"
town: core
---
# hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused

## OWNER, verbatim (on the parent goal)
21:0xZ 09-26: "Can we not have the local box name be a global env variable that gets set as part of the ini routine somehow? Like the box label in the network or something. Then just check that."
belam 00:35Z 09-27 on the owner's go: done = (1) every live row carries its own box, written at seating from AGI_BOX (2) empty/unknown box refused on EVERY box, once per row+cause, naming the box (3) no send-keys into such a row's window.

## Measured
- extensions/agi/bin/boxes.py:153 `this_box` = AGI_BOX from the env, else the .env file, else the posts node's `default_box` (= core-town on this graph): an unset AGI_BOX silently becomes core-town.
- boxes.py:168 `row_is_local`: a row with NO box cell takes `default_box` (core-town), so on local-town every such row is FOREIGN; send.py:2198 refuses it as a nudge target, printing 'box (default)', on every sweep (belam 00:35Z: 6 rows).
- No seating path is known to write the row's `box` cell from AGI_BOX (the kid measures the seat-row writer and names it file:line before any code).

## CLAIM
(1) seating writes the row's own `box` cell from AGI_BOX (the one seat-row writer), so a newly seated live row always carries it (2) `this_box` REFUSES when AGI_BOX is unset (no silent default) and `row_is_local` treats an empty or unknown row box as NOT local on every box -- '(default)' is never a match (3) send.py's foreign-row refusal is printed ONCE per row+cause (not every sweep), names the box, and sends no keys into that row's window.

## Dispatch line
config-max: the box label is env AGI_BOX (set by the box init, never a config literal); default_box stays only as the posts node's documentation, never a locality fallback. template-max: none. code: the seat-row writer, boxes.py's two readers, the refusal's once-only memo.

## FALSIFIERS
- a temp graph with AGI_BOX unset: `this_box` returns any value instead of refusing.
- a row with box '' or an unknown label is local on some box.
- two sweeps over one foreign row print the refusal twice, or any send-keys reaches its window.
- a fresh seat on a temp graph leaves the row without `box`.

## TESTS
extensions/agi/tests/test_box_identity.py (new; temp graphs, monkeypatched env, a fake tmux runner -- never the live pane). Neighbourhood (send): test_send.py test_seatsig.py test_heal.py test_bin_help_smoke.py test_write_self_row.py. Every pytest under `timeout 600`, --basetemp under /tmp, env -u TMUX -u TMUX_PANE.

## FILE SCOPE
extensions/agi/bin/boxes.py · the ONE seat-row writer (named by the kid, file:line) · extensions/agi/bin/send.py (the foreign refusal at ~2198 only) · extensions/agi/tests/test_box_identity.py.

## CEILING
2 kids · <= 50 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude; never the live .env.

## CORRECTIVE DH.525 -- closes mur-director-engine-17 DH.498-k1 + k2 (verify: accept_with_residue, NOT_MET conjuncts (2b) and (3))
BASE      CUT FROM season2/loops/hypothesis-every-live-row-carrie-a00-efb7f2a8 tip 69958a4a9 (worktree a00-efb7f2a8). No merge. Never rebase.
OUT OF SCOPE  the backfill of the 18 boxless config:posts rows -> the director's [red] to its master (other posts' rows), NOT this round.
1. test_box_guard.py:46-64 still pins the removed default_box fallback (this_box == default_box, a boxless row is local) and is RED at the base -> re-pin both tests to the new contract (an unset box is refused by name), never delete them.
2. crons.py:795-810 -- _this_box catches boxes.this_box's refusal and returns '', and _on_this_box treats '' as no gate, so a box with no AGI_BOX runs EVERY cron job -> fail CLOSED: an unset box runs no box-gated job and prints the refusal once; one test.
3. boxes.py:186 row_is_local returns `not own` when this_box raises (fail-open, pinned by test_box_identity.py:124), contradicting conjunct (2b) 'an empty or unknown row box is never local on any box' -> make it never-local and re-pin :124, OR record on the kid node, with the measured reason, why (2b) must keep this one exception; pick one.
4. send.py:2176 _FOREIGN_REFUSALS is process-local; the nudge_sweep cron is a new process every tick (crons.py:955) -> conjunct (3) 'once per row+cause' needs a durable memo (a small state file under .agi/sessions, keyed row+cause) OR the node narrows (3) to the long-lived reaper (heal.py:1898 _repair_stranded_wakes) with that census line added; pick one, test it.
5. rotate.py:9657 -- no committed test drives _successor_row_write to the _stamp_row_box call -> one test through _successor_row_write.
6. experiment:a00-fb8c4f95-cd7594 says '12 tests, 12 passed'; test_box_identity.py has 17 -> RE-RUN, paste, fix (write.py).
ANON      no user name, home or repo path value, host or IP, no box hardware names (class prefixes only); patterns write <user>
TESTS     test_box_guard.py test_box_identity.py test_crons*.py test_send.py test_rotate*.py -k box test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/crons.py (_this_box/_on_this_box) · extensions/agi/bin/boxes.py (row_is_local) · extensions/agi/bin/send.py (the foreign-refusal memo) · extensions/agi/tests/test_box_guard.py · extensions/agi/tests/test_box_identity.py · experiment:a00-fb8c4f95-cd7594 (write.py) · the kid's own node. NEVER .agi/nodes/.geometry/posts.md.
CEILING   HARD CAP: 2 kids (1: items 1-3, 2: items 4-6) · net <= 25 production lines · <= 90 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.525: mur-17 DH.498-k1+k2 accept_with_residue, conjuncts (2b) and (3) NOT_MET -- test_box_guard.py left red, crons un-gated on a box with no AGI_BOX (fail-open), row_is_local fail-open vs (2b), a process-local foreign-refusal memo vs a per-tick cron, no test through _successor_row_write, a stale test count. The 18 boxless config:posts rows (4 of 22 carry box) are a [red] to thought-master, not this round: other posts' rows.
<!-- THOUGHT:END -->
