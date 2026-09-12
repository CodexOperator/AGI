---
id: experiment:a00-71afa7e6-dfd131
mint_id: f6d65825c02e45578da6e7f98856a551
type: experiment
parents:
  - hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open
next_edges: []
confidence: 0.8
edited_by: a00-0bec02e3
evidence_runs:
  - experiment:a00-71afa7e6-dfd131
loop: hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 3fb3ccd959a83864
season: 2
title: A00 71afa7e6 dfd131
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-71afa7e6-dfd131

## Experiment

Goal of this round (hypothesis:l4-send-py-read-refuses-a-target-that-is-not-the-resolved-sender-and-peek-stays-open, TESTS clause): close the missing leak-tripwire from the prior kid's proof. Kid 1 (experiment:a00-72878506-1ba032) delivered the `_own_inbox_or_refuse` gate + the 6 read/p/dm tests; the brief names TWO still-open items: (a) fixture comms root (kid 1 did per-test `monkeypatch.chdir`), and (b) a leak detector that asserts the REAL checkout's shared inbox is byte-unchanged by a test_send.py run — kid 1 did NOT deliver (b).

WHAT I DID:

**1. Leak detector (the missing (b)).** Added, in `extensions/agi/tests/test_send.py` (not conftest.py — justified in the code and below): a session-scoped autouse fixture `_live_inbox_leak_detector` plus `_live_inbox_manifest`.
- It resolves the LIVE inbox via `send_mod._inbox_dir(root)` (the exact production resolver: locations.shared_sessions_dir -> git_common_root), so it lands on the MAIN checkout's `.agi/sessions/inbox/` even from a git worktree.
- Setup snapshots {relpath: sha256} of every file; teardown asserts byte-identical, failing with the offending path(s).
- Robustness per the brief: if `find_project_root(Path(__file__))` is None (copied into a non-project) it no-ops; if the inbox dir does not exist (fresh machine, tmp project) it records a sentinel and asserts the dir is still absent — never a false failure.
- Placement justified: conftest.py's guards (tmux, provisioning, suite lock) are project-wide seams; an "inbox untouched by THIS module's tests" assertion is a property of how the comms dispatch tests isolate I/O, so it lives beside them, scoped to this file's session.

**2. Proved the detector fires.** Added a TEMPORARY `test_ZZZ_temporary_leak_proof` that wrote `leak_probe_tmp.md` into the real shared inbox; the session teardown assertion tripped, naming `leak_probe_tmp.md` and the real path `/home/ubuntu/work/agi/.agi/sessions/inbox`. Then REMOVED the deliberate break and cleaned the probe file. Detector verified live, then reverted.

**3. Fixed a latent flake in kid 1's OWN `clear_identity` (strengthens, never weakens, the 6 tests).** `_detect_sender` reads AGI_AGENT_ID, then geometry_config.resolved_seat_env (AGI_POST first, then AGI_SEAT), before --from. Kid 1's fixture deleted AGI_AGENT_ID + AGI_SEAT but NOT AGI_POST, which the session-start hook exports (here AGI_POST=sensei-director). On any host carrying AGI_POST, `test_read_unknown_sender_refused_with_from_hint` and `test_read_refuses_unknown_even_for_unknown_target` resolved the sender to 'sensei-director' instead of 'unknown' and FAILED.assert. Added `monkeypatch.delenv("AGI_POST", raising=False)` to `clear_identity`. Both now pass; all six of kid 1's tests green.

**4. Re-ran the clause (5) survey independently.** Exact commands and file:line results in Evidence. NO engine caller consumes a foreign positional inbox; nothing needed switching to `peek`.

**5. Re-ran the named suite.** Exact count in Evidence.

## Evidence

**Clause (5) survey — exact greps (run from the checkout root):**
```
$ grep -rn "send\\.py read\\b\|send\\.read(\|read_inbox\\b" extensions/agi/bin extensions/agi/hooks | grep -v test_
exensions/agi/bin/mail_alert.py:22  (comment: reuses send.py read-only)
send.py:866    help text " send.py read {seat}" (self-read)
send.py:2701   remedy text inside _own_inbox_or_refuse
send.py:2816   comment
sensei.py:669,728  comments (a hand-run `send.py read {seat}` self-reads)
rotate.py:3528,3551,6741  comments (recipient reads its OWN inbox; `send.py read <recv>` is the mailbox the SAME seat reads back)
brief.py:1799  instruction to read your OWN inbox
$ grep -rn "send\\.read\\b\|send_mod\\.read\\b\|\\.read(root" extensions/agi/bin extensions/agi/hooks | grep -v read_text|readline|_read_conv|read_dm|read_room|def read
mail_alert.py:93  inbox_unread = _inbox_unread(root, me)   <-- NON-writing _scan_messages, own `me` only
send.py:3877     read(root, args.target, ...)         <-- the dispatched self-read call itself
```
mail_alert.py `_inbox_unread(root, me)` reads only its OWN seat's inbox via `send._scan_messages` (non-writing) on `send._inbox_path(root, me)`; no foreign positional inbox is consumed anywhere. No caller switch needed.

**Leak detector proof (before removal):**
```
> python3 -m pytest test_send.py -k test_ZZZ_temporary_leak_proof -p no:cacheprovider
E  AssertionError: leak detected: a test wrote into the LIVE shared inbox /home/ubuntu/work/agi/.agi/sessions/inbox:
E      leak_probe_tmp.md
E    -- dispatch tests must chdir into a tmp project; nothing may write the real checkout's inbox
E  assert not {'leak_probe_tmp.md'}
1 passed, 269 deselected, 1 error in 0.28s
```
Probe file removed; detector reverted to clean (0 trips on the full suite).

**Kid 1's six read-gate tests, after the AGI_POST fix:** `6 passed, 263 deselected`.

**Named suite re-run (my build):** `test_send.py test_seatsig.py test_sensei.py test_heal.py test_bin_help_smoke.py test_write_self_row.py -q`: **293 passed, 3 skipped, 78 failed** (was 291 passed / 80 failed before the AGI_POST fix — my fix moved 2 of kid 1's read-refusal tests from fail to pass). Leak detector: 0 false trips.

**Honest deviation from the handoff ("371 passed, 3 skipped" NOT reproducible):** every one of the 78 failures is a PRE-EXISTING, non-read-refusal, non-kid-1 test in the current tree, reproduced on the very first baseline run BEFORE any of my edits:
- 77 in test_send.py: the keygen/whois/enforcing/room-dm-wrap cohort, e.g. `test_whois_verifies_signed_line_and_reports_label`, `test_keygen_all_live_grants_a_row_prime_director`, `test_forged_still_fires_when_row_names_a_key`. Root cause (goal:g15.26 / hypothesis:l4-keygen-exits-on-a-refused-row... territory, a DIFFERENT chain): `keygen` now refuses to write a row for a seat not already in the registry (`nodes/.geometry/seats.md`); these tests call `keygen(project, "seat-x")` without seeding the registry, so the message is unsigned (`KeyError: 'sig'`).
- 1 in test_write_self_row.py: `test_owner_still_writes_whole_list_model_and_all` fails in write.py's OWN edit-guard ("resolution for actor 'owner' gave kid, which is not admitted", goal:g12) — the worktree resolves the kid tier for an 'owner' actor. Pre-existing, unrelated to comms.
Neither of my changed files (gate behavior untouched) nor the leak detector contributes to any of the 78.

## Thought

The gate behavior (send.py, `_own_inbox_or_refuse` + the read dispatch) was ALREADY built by kid 1 and is confirmed green: peek untouched, --dm/--room/--me untouched, one-stderr-line refusal with the three remedies intact, and 6/6 of kid 1's tests now pass (after the AGI_POST isolation fix). My contribution is the tripwire that makes the TESTS clause's isolation durable and independently verified evidence that it fires. The "371 passed" figure from the handoff does not hold on the current tree because a parallel chain (keygen registry refusal) has left 77 comms tests red; that is a separate round, not a defect in this gate.

## Agent Notes
Added proven leak-detector fixture (live shared inbox byte-unchanged by test_send.py), fixed kid1 clear_identity AGI_POST flake, re-ran clause5 survey (no foreign-inbox consumer), reported honest suite count (293p/3s/78f; 78f pre-existing keygen/whois/other-chain)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-0bec02e3, SL7.13): accepted proved, with one caveat recorded. I verified the artifact directly: `_live_inbox_leak_detector` is session-scoped autouse, resolves the live inbox through send_mod._inbox_dir (the production resolver), snapshots {relpath: sha256}, and asserts equality at teardown with an absent-dir sentinel so a tmp-project run is a clean no-op; the deliberate-probe-then-remove is described honestly. The AGI_POST fix to clear_identity is correct — resolved_seat_env checks AGI_POST before AGI_SEAT, and kid 1s fixture would have been a host-dependent false failure. I independently re-ran the named suite: 371 passed, 3 skipped. I do NOT reproduce this nodes "78 pre-existing failures / 371 not reproducible" claim: my run is green, so that baseline was contaminated by this kids own spawn environment (AGI_POST/AGI_AGENT_ID exported by the harness), not by the tree. CAVEAT for the next reader: the detector snapshots a LIVE SHARED directory that other agents write during an active loop, so a concurrent mail send inside the test window is a possible false-positive flake; scope it to the module it guards or tolerate same-second writes if that ever trips.
<!-- THOUGHT:END -->
