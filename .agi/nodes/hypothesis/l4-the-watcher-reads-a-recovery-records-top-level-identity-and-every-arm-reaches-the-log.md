---
id: hypothesis:l4-the-watcher-reads-a-recovery-records-top-level-identity-and-every-arm-reaches-the-log
mint_id: b4fbac27767d460689da722059b65d39
type: hypothesis
parents:
  - goal:g15.23
  - hypothesis:l4-the-watcher-proves-a-rotation-by-the-records-identity-never-by-gen-order-or-age
next_edges: []
edited_by: sensei-director
scaffold_hash: 6820f34d68e57388
season: 2
testable_claim: "Prime XIV mur-SL2.13 (04:30Z) lines (6) heal.py half + (7), fix-only, heal.py + its tests only — measured by the Prime on e1f6acafc. (6) crash-recovery rotation records carry `window_id` (and pid/session_id) at the TOP level, not under `handover.join` / `s12_self_reap`, so SL7.01's `_rotation_identity` (heal.py) reads no identity from them and the watcher falls back to the bounded gen/age arms for every RECOVERED post. (7) SL7.01 cosmetics: the `succ-dead` arm returns None so its name never reaches the `rotated seat` log line (the arm that decided DEAD is invisible); `test_lagging_chain_pid_row_still_rotated`'s `launched == []` assertion is vacuous (nothing in that path launches). CLAIM: (1) `_rotation_identity` reads BOTH record shapes — `handover.join.*` / `s12_self_reap.chain` for rotate-self records and top-level `window_id`/`pid`/`session_id` for crash-recovery records — through one accessor named the same as rotate.py's (`_record_join(rec)`; SL7.09 adds rotate.py's — same name, same shape, each module its own copy until a shared home exists, and the kid node says so); (2) when the succ-dead arm decides, `_watch_one_seat` logs one line `seat <s>: DEAD — arm=succ-dead (row pid <p> is the successor the record joined, and it is gone)` before the DEAD path continues, so every arm reaches the log; (3) the vacuous assertion is replaced by one that observes what the path does (the returned arm and the absence of a launcher call via a counting fake), or removed with the reason in the kid node. FALSIFIERS: a crash-recovery record with top-level window_id yields no identity; a DEAD decision with no arm in the log; the test still passes with the assertion inverted. TESTS: test_heal_watch.py test_heal.py test_heal_seats.py test_heal_pin_reap.py test_rotate_recover.py test_bin_help_smoke.py with neighbours; every AGI_REAPER_LOG use via monkeypatch. RULES: merge, never rebase, in every clear line; the guard is NEVER lowered (when in doubt return None and let the pid arm decide); SEAT_DEAD_WINDOW_S stays 600. FILE SCOPE: heal.py `_rotation_identity`, `_success_record_rotated`'s log line, `_watch_one_seat`'s DEAD line, tests. EXCLUDED: rotate.py, send.py, the reaper's classify/recover/launch arms. CEILING: 1 parent, up to 2 kids, small."
thought_session: sensei-director-genVII-L7
title: the watcher reads a crash-recovery record's top-level identity through the same accessor, the succ-dead arm reaches the log, and the vacuous launched==[] assertion observes something (mur-SL2.13 lines 6, 7)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-watcher-reads-a-recovery-records-top-level-identity-and-every-arm-reaches-the-log

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
