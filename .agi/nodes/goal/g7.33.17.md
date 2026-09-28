---
id: goal:g7.33.17
mint_id: 6725d60a79324b62936412fcfd2b30c2
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.17
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 4218327a919460bf
season: 2
seeds: []
status: active
tags:
  - local-maxxing
  - engine
title: "G7.33.17: THE 09-25 QUEUE RECONCILED -- every carried item (8 PASS 3 code defects with 0 experiments, CMP.02, E5, .14/.23/ML-3, EF.92, E6) held as a row here until DONE or VOID (TMM.238)"
town: core
---
# goal:g7.33.17

# goal:g7.33.17

## Why this exists
**Parent `goal:g7.33`.** TMM.238 (thought-master, 2026-09-26): reconcile the 09-25 queue on board row 8. Items with
no goal leaf and not on director-engine's card, reconciled 16:3xZ by the bytes (landing commits on
local-maxxing/season2/main since 09-24; experiments per hypothesis in `.agi/nodes/experiment/`). The OWED ones are
held HERE, one row each, so none lives only on a board row or a card. One leaf with rows rather than 14 leaves:
each row becomes its own round (and its own sub-leaf if it grows) when it is dispatched.

## Target end-state -- every row DONE (sha) or VOID (reason)
| # | item | source | state 09-26 |
|---|---|---|---|
| 1 | hypothesis:harness-bin-absolute-token-free-bins-refused-by-name | PASS 3 (pass3-0924-residue-batch) | DONE DH.404 3f38e2b8b (an absolute bin that does not exist refuses by name; 1 kid proved) |
| 2 | hypothesis:refused-authority-publish-defers-the-successor-key-swap | PASS 3 | VOID (disproved by design) fed9e93bb: SKIPPED/REFUSED completes the swap, FAILED/HELD defers; EF.56 tests pin it |
| 3 | hypothesis:grok-bot-adapter-uses-or-refuses-the-rendered-brief | PASS 3 | DONE DH.406 7a209c4e3 (the adapter dropped the rendered brief; empty prompt now refused by name) |
| 4 | hypothesis:migrate-refuses-an-inadmissible-grant-before-worktree-and-spawn | PASS 3 | DONE DH.407 (test-only: the refusal holds on today\'s bytes; pinned through the real grant reader) |
| 5 | hypothesis:non-prime-rotate-self-renders-through-brief-render | PASS 3 | DONE DH.410 c11128889 (non-prime successor = the ONE brief.render; red 2/green) |
| 6 | hypothesis:restart-admission-honours-the-per-harness-live-bound | PASS 3 (E3 rotation + restart) | DONE DH.402 501dc66c5 |
| 7 | hypothesis:required-any-diagnostic-names-the-declared-alternatives | PASS 3 (E4 harness + diagnostics) | DONE DH.403 718773bfe |
| 8 | hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced | PASS 3 | DONE DH.401 4a1b95a06 |
| 9 | CMP.02 cross-box reap guard (a reaper on one box revoking another box's live kid keys) | TMM.114/116; design pinned in .agi/sessions/de-0923/cmp02-pinned.md | OWED: never dispatched |
| 10 | E5: the 31 non-lm demotes of PASS 3 (node text corrected in place, reason in THOUGHT) | TMM.112 | OWED: unverified which remain -- the round re-runs evidence_gate + reads each |
| 11 | residue .14 (mkstemp + index cleanup) · .23 (the E2 test) · ML-3 (harness through every lease rewrite) | TMM.112 queue | OWED: content re-read from TMM.112 before dispatch |
| 12 | EF.92 (LH-2) | held by TM (TMM.91 list) | VOID: DONE c876dbf72 on 09-24 (TMM.241) |
| 13 | E6 the coalesced-nudge sweep | 09-25 queue | OWED: content re-read before dispatch |
| 14 | test_f1_rename_mode_strands_the_live_writer_on_a_BOUNDED_archive trunk load flake: freeze the stranded writer across the apply like 569ea9a1b | TMM.241 (1) | DONE 071f2ec15 (test-only; 12/12 under load; red not reproduced -- rare) |
| 15 | DH.401 successor shape: a slot [P, fence(n)[P, ```...```]] still compounds +1 per rotation -> drop the outer fence + the duplicated P; prove on the successor shape | TMM.241 (2) | LIVE DH.409 a00-f28911bd |
| 16 | a capture refuses whenever trunk moved (rotate-self skips the bare rotate's origin merge) -- goal:g7.33.15 residue | TMM.241 (3) + DE 17:01Z [red] | DONE DH.408 242dd3475 (registered behind seat merges at the guard; red 3/green) |
| 17 | model_fence: _cap_from_config KeyError at import when a config lacks the cell (-> cap 0, fail closed) + the refusal names model_slot.py, not 'this suite asserts on bytes' | TMM.256 + TMM.260 (2) | DONE (director, direct; test_model_fence_cap.py red 5/green 6) |
| 18 | a round's kid cannot fan out pytest past the box's bound -- an ENGINE fence (the suite lock and spawn_budget did not stop DH.419's 127 procs) | TMM.258/260 (1) | DONE DH.421 091808547 (TasksMax on the round scope; peaks sent to TM; the seat-wrap half NOT taken) |
| 19 | DH.410's first live render (TMM.261): the render INLINES CLAUDE.md (26,597 B + COMMANDS) where the claude-code harness already loads it as project instructions, and prints the role template heading twice (the render's + the node's own) -> 106,144 vs 64,896 chars (+64 pct). Drop the inline CLAUDE.md for a harness that loads it itself; one template heading | TMM.261 | DONE DH.423 e636d7aa9 (director-engine render 62,304 -> 35,589 chars; only CLAUDE.md dropped) |
| 20 | send.py read prints 'inbox ... empty' while unread dm blocks sit in the raw inbox file with the read marker already past them (TM inbox 02:20:05Z: DE 01:49Z [red] + 02:16Z [rule]), and a dm-file send can skip the nudge (DT 21:37Z [merge-up] never nudged) -> find what advances the marker without printing, and why a dm-file send skips the nudge | TMM.270 (owner in TM's pane 02:28:27Z) | DISPATCHED DH.490 a00-5bde5739 (TMM.271 dispatch now): harvested, 1 red (withheld-block test) -> mur490 + corrective |
| 21 | the captive AUTO-CAPTURE (rotation_alert.py ~971 -> _force_capture) REPLACES a card's 'Where it stops' slot body AND its BANKED section with its one 'auto-captured at f=...' line -- a successor loses the whole owed list (DT 03:02Z; restored from f76c09619 by 8384aa443) -> a capture keeps the slot + BANKED byte-identical and APPENDS its line; test: a captured card with a multi-line slot + BANKED diffed before/after | TMM.277 | DISPATCHED DH.493 a00-7af19a42 (hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line, 43447b04e) |

## Who
director-engine (engine leaf of g7.33). Model-free rounds; one row per round.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Row 20 added by director-engine on TMM.270 (thought-master 02:31Z). OWNER in thought-master's pane 02:28:27Z 09-27, verbatim: "Check dm file directly nudges have been buggy". Measured by thought-master: send.py read printed 'inbox ... empty' twice while director-engine's 01:49Z [red] and 02:16Z [rule] sat in .agi/sessions/inbox/thought-master.md with the read marker already past them (file mtime 02:20:05Z), and director-thought's 21:37Z [merge-up] in its dm file never nudged at all. Also seen by director-engine 02:3xZ: its own send.py read printed 'inbox for director-engine: empty' and then the unread dm block beneath it -- the 'empty' line describes the inbox file only, not the dm rooms.
<!-- THOUGHT:END -->
