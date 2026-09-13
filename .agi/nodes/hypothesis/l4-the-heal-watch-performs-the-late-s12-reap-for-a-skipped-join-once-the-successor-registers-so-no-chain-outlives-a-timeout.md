---
id: hypothesis:l4-the-heal-watch-performs-the-late-s12-reap-for-a-skipped-join-once-the-successor-registers-so-no-chain-outlives-a-timeout
mint_id: b00c1ccf7ee44b87bf7f6e5d73801878
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: cb46524efd05afa7
season: 2
testable_claim: "goal:g15.25 SM.12 (intake: master-sensei 07:2xZ audit XVIII->XIX, drafts/belam-wake-audit-20260913T013315Z.md). MEASURED on season2/main @4b5054f31: record belam.20260913T013315Z.json = result skipped, refusal_reason \"registry file for @348 not found in ~/.claude/sessions within the bounded join poll\", handover own @335 (XVIII) -> successor @348 (XIX), observations.a_successor_window_under_plain_name.windows lists belam-S1-L4-XIV, XV, XVI, XVII, XVIII, XIX ALL live at 01:39Z; a skipped join returns before s12 (rotate.py _record_s12_self_reap :8264 / _reap_chain :8499 run only on a confirmed join), and NOTHING later reaps: the watch (heal.py:452-470) performs a late after_join for a seat but has no late-REAP branch; the XIX registry landed 5 h 35 min after spawn (box stalled 01:33-07:14Z, load 217 / 4 cores) — a longer join bound is not the lever. CLAIM: (1) NEW heal.py watch branch `_late_reap_for_skipped(root, record)`: for a rotation record with result == skipped whose refusal_reason names the registry poll AND whose handover carries own_window + successor_window ids — when the successor registry file for successor_window.id NOW exists (the same registry lookup the join uses, by @id; never by name), perform the s12 reap the rotation would have performed: `_reap_chain` on the pids of every chain window OLDER than the successor (chain = windows matching <seat>-S1-L4-<ROM> with numeral < successor numeral; the numeral is the generation, P1), TERM then KILL with the same wait the live s12 uses, then write `s12_self_reap` into THAT record with performer: watch + reaped_late_at, and flip result to `success_late`; (2) the successor own window is never reaped (assert by @id != successor id); a plain-seat (non-chain) skipped record reaps only the renamed own window seat.gen<N> — say the line; (3) a skipped record whose successor registry is STILL absent is left alone (one waiting line per record, never per pass — reuse SM.04 once-per-pair pattern); (4) --once and dry-run: report, never reap; (5) observations gain spawn_to_registry_s (registry mtime - spawn ts) and loadavg_1_5_15 at the late reap. FALSIFIERS: the successor reaped; a reap on a record whose registry is still absent; a reap by window NAME; a second reap on an already success_late record; the live s12 path changed. TESTS (test_heal_watch.py <= 5, fixture record + fake registry dir + monkeypatched _reap_chain recording pids): registry absent -> no reap, one waiting line; registry present -> reap called with exactly the older-chain pids, record flipped success_late with performer watch; successor pid never in the reap list; second pass -> no second reap; --once -> report only. FILE SCOPE: heal.py (new branch + helper), rotate.py ONLY if a shared helper (chain-window enumeration) must be exposed — name it; test_heal_watch.py. CEILING: <= 70 lines net, <= 5 tests."
title: the heal watch performs the LATE s12 reap for a record whose join timed out (result skipped, registry not found within the bounded poll) once the successor registry appears — the predecessor chain never outlives a join timeout (belam XIV-XVIII all alive at 01:39Z, ~400 MB each, 28 h oldest; box load 217 on 4 cores)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-heal-watch-performs-the-late-s12-reap-for-a-skipped-join-once-the-successor-registers-so-no-chain-outlives-a-timeout

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
