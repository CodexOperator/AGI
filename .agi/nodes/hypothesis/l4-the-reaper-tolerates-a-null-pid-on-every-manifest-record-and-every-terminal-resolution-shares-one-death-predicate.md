---
id: hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate
mint_id: 7873d0db921f4d4482c82803988a550d
type: hypothesis
parents:
  - goal:g6.47
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 97f9f4c970ee94a0
season: 2
testable_claim: "goal:g6.47 SM.23 = RED fix-only (belam XIX 16:30Z from mur-51 on L4.345, merged in merge-up 51). MEASURED on season2/main @HEAD: L4.345 hoisted `int(rec.get(\"pid\", 0))` onto every manifest record — heal.py:183 (spid), :221, :2560 and dispatch.py:2554; a committed record can carry \"pid\": null (.agi/sessions/iter-L4.16/a00-1e3af37b/agent.json:8 — dict.get returns the stored None) so int(None) raises TypeError: in the persistent watcher per-manifest loop the exception is swallowed in the service lane (that round is never reaped/mirrored/alarmed again) and propagates in the inline lane; not fired yet only because the reaper unit has not re-exec-ed onto these bytes (SM.04 gate). The stalled-dead class writes fail_reason \"stalled; pid N disappeared …\" (dispatch.py:2857-2860) while the alarm gate matches fail_reason.startswith(\"pid N died\") — no dm, no reaper-log line for a stalled death. CLAIM: (i) `int(rec.get(\"pid\") or 0)` at all FOUR sites (name each), plus a non-int pid (\"abc\") -> 0 through one tiny helper `_rec_pid(rec) -> int` used by all four (one implementation); (ii) ONE shared death predicate `_is_death(rec) -> bool` (or the existing one — measure and name it) that the dead-running path AND the stalled-dead path both call before alarming/logging; the stalled-dead branch produces the same dm + reaper-log line the dead-running branch does; RULE in the docstring: a new terminal-resolution branch reuses the predicate, never string-matches a message; (iii) the residue (heal.py live-stalled skip `continue` before all_terminal=False -> exit-0 misreport) may ride if it fits the ceiling, else named as the next slice. FALSIFIERS: any remaining int(rec.get(\"pid\", 0)); a stalled death that produces no dm; a second predicate; a message string matched anywhere the predicate should be. TESTS (test_heal_watch.py / test_dispatch.py, 2 minimum: a manifest with pid null and one with pid \"abc\" flows through the loop without raising and is reaped as pid-0/unknown; a stalled-dead record alarms through the shared predicate — dm + log line asserted). FILE SCOPE: heal.py + dispatch.py at the named sites; the two test files. CEILING: <= 30 lines net, 2-3 tests. DO NOT restart the reaper unit before this lands (Prime); after landing, restart with the card pre-check."
title: "the reaper never crashes on a committed record with \"pid\": null — `int(rec.get(\"pid\") or 0)` at every hoisted site — and a stalled-dead resolution is a death through the SAME predicate/alarm the dead-running path uses, never a caller string-matching a message (RED from mur-51 on L4.345; fix-only, top of the SM queue)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-reaper-tolerates-a-null-pid-on-every-manifest-record-and-every-terminal-resolution-shares-one-death-predicate

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
harvested on the post 18:38Z (2 kids; kid1 over-claim caught by the parent probe, kid2 closed it; 182 green; 66 production lines under the raised 80 ceiling, re-briefed at 2.2x as the rule asks). Residue: heal.py:391 builds its death dict inline rather than calling _is_death (second construction site); cli.py status can show a kid ORIGINAL self-verdict after the parent demotes at node level. Rides the next window; reaper unit restarts only after.

SM review by name (SL2#30 CLOSED @ac12854ca, suite 4766/15/0 in 471 s, nodes 2830/198/3028): ACCEPT for (i) + (ii) — _rec_pid at the four sites, one death predicate, stalled-dead alarms; residue (iii) hunk REVERTED by the Prime @912363623 after it sent a test into a 30-min poll (3 suites over 1800 s) — re-landed as SM.23b. First merge pushed on a parent subset before the full suite; the no-exception rule is now on the director card.
