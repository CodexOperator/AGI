---
id: hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs
mint_id: 3b64852f6e51491b8d9e6127b2a74699
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sensei-director
scaffold_hash: c515be27fc546390
season: 2
testable_claim: "goal:g15.25 FIX-ONLY node (master-sensei gen 4 dm 15:56Z relaying owner 15:5xZ (third order; verbatim at doc:l4-owner-decisions); cite at seat tip 92563a7f5, re-measure on your base. finding (2), measured by the Sensei on 91 rotation records: after_join has NEVER been performed for any post — 86 records lack the key, the 5 that carry it hold {} (sensei-director 000346Z/085900Z/103731Z, sanctuary-director 091510Z, stream-master 002842Z); the performer is heal.py's watch loop (heal.py:107-112 `heal.py watch`, run_after_join_for_seat reached from it) or rotate-self's post-spawn tail, and NO heal watch process is alive on the box (only launch-wrap), so the template's whole after_join list — join, pin (the meter), ack printer, reap-proof, model_confirm, prime belam-chain + sensei-wake — is dead declaration and the second-input dm the delivery clause promises has never arrived). SL7.54 (landed SL2#23) made the performer REACHABLE (3-arg _resolve_template, _after_join_performer_armed at rotate.py:9234, _inline_reaper_enabled :9216); this node makes it LIVE. CLAIM: (a) rotate-self's own tail — the wrapper that already waits for the ack and self-reaps (F1) — performs run_after_join_for_seat itself when _after_join_performer_armed is False OR no heal watch process is alive (measure liveness by the watch unit's pid file or the reaper log's last heartbeat within N seconds — name which), so a rotation never depends on a watcher that is not running; (b) when the watch IS alive it stays the performer and the tail does not double-perform (the record's after_join key is written once, by whichever performed, with performer: watch|tail); (c) the record's after_join key is never absent or {} after a completed rotation — at minimum it names the performer and each list entry's outcome. FALSIFIERS: a rotate-self on a box with no heal watch leaves a record without after_join or with {}; a live watch and the tail both perform (two model_confirm writes); the tail performs while the record says deferred: after_join. TESTS: test_rotate_handover.py / test_after_join_service.py — tail performs when no watcher (fixture: armed False), watch performs and tail skips when armed + alive, key never empty. FILE SCOPE: extensions/agi/bin/rotate.py — the rotate-self post-spawn tail and _after_join_performer_armed's liveness input; extensions/agi/bin/heal.py only for a pid/heartbeat the liveness check reads; the two test files. EXCLUDED: the after_join list's entries themselves, the templates, the confirm (SL7.40/54). CEILING: one liveness check, one tail call, three tests."
thought_session: sensei-director-genXIII-L13
title: after_join is PERFORMED for every rotation — heal.py watch is the live performer when its process runs, and rotate-self's own post-spawn tail performs the after_join list itself when no watcher is alive — so a record's after_join key is never absent or {}
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-after-join-is-performed-live-by-a-running-watch-or-by-rotate-selfs-own-tail-when-no-watcher-runs

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
