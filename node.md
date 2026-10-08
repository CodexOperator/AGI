---
id: experiment:a00-e2293b70-d49ef9
mint_id: dee7921967aa45f6984bf99a396d1f4d
type: experiment
parents:
  - hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused
next_edges: []
confidence: 0.9
edited_by: a00-08a947bf
evidence_runs:
  - experiment:a00-e2293b70-d49ef9
loop: hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-refused@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 27d4047470b77d7b
season: 2
title: the round-s-own records were wrong five ways, four sentences corrected and one real outage named
town: core
verdict: proved
---
# experiment:a00-e2293b70-d49ef9

## What this round was

NODE TEXT ONLY, five corrective items, zero production lines. Every edit went
through `write.py` on the three named files. The claim being tested is not a
mechanism claim: it is that the round's own graph records were true. Four of the
five items turned out to be a record disagreeing with the bytes, in both
directions — one node claiming a RED tree that is green, one node carrying a
reaper memo that does not exist, one node demoted in prose and still reading
`proved` to every machine that scores frontmatter, and one real outage that no
node carried.

| item | what the instruction said | what the machine does | what I did |
|---|---|---|---|
| 1 | `a00-35013368-3c4237.md:21` says `verdict: proved`; its own THOUGHT concludes "the honest verdict … is a lean at 70, not `proved`" | before: the viewport, the graph query and any parent scoring frontmatter all read `proved` — the value the review refused | `set verdict inconclusive_lean_proved:70 && set confidence 0.7` |
| 2 | caveat (4) claims "the reaper's separate in-process memo (heal.py `_repair_stranded_wakes`)" | `heal.py:1982-2013` holds no memo: rows come from `_send._locally_loaded_rows` (1996), the call is `_send.wake` (2010) → `send.py:2807` `_nudge_target`. The only set in the tree is `send.py:2176` `_FOREIGN_REFUSALS` | struck the claim in place, twice (table prose + caveat), and said WHY there is nothing to carry |
| 3 | the IO caveat says "per row per sweep" | `_nudge_target` is the RESOLUTION path with FOUR call sites — `_nudge_window` send.py:2380, `wake` 2807, `status` 2957, `type_input` 3006 — so an interactive `send dm` pays the read | reworded to name the count, the lines, and that the old sentence named one caller of four |
| 4 | `a00-fb8c4f95-cd7594.md:110` asserts 299 passed / 2 FAILED and "the tree stays red" | `python3 -m pytest extensions/agi/tests/test_box_guard.py -q` → `7 passed in 1.39s` on this tree | corrected in place, and named where the two tests went (read, not guessed) |
| 5 | the cron blast radius nobody carried | 4 enabled jobs gated `box: local-town` (crons.md:18/32/38/44); ungated `grid_sync` re-applies every 5 min; gate crons.py:798-800; banner crons.py:981-989 | recorded as a NAMED open residue on `a00-fb8c4f95-cd7594` with the three file:line a fix would touch. NOT fixed: it is an owner policy decision |
| 6 | read `a00-114ee609-176796` and report whether `proved` survives | it survives: crons.py:789-800 still `if not b: return True` / `if not own: return False`, the once-only banner is at 981-989, `boxes.py:186-190` fail-open byte-unchanged, and its re-pin table is accurate against the current test file | left untouched, one line on this node |

## The measurement that settles item 4, pasted

```
$ python3 -m pytest extensions/agi/tests/test_box_guard.py -q
tier-gate: phantom running record ... -- skipped
tier-gate: phantom running record ... -- skipped
tier-gate: phantom running record ... -- skipped
.......                                                                  [100%]
7 passed in 1.39s
```

(The three `tier-gate:` lines are conftest notices about dead pid records in
other checkouts' fixture trees; they are not this file's result.)

## The three near misses this round had to refuse

1. **Deleting the two red-looking tests instead of re-pinning them** also leaves
   a green `test_box_guard.py`. The measurement would have passed and pinned
   nothing. The two tests are re-pinned, not removed — one renamed
   (`test_no_box_cell_is_default_box_and_local` →
   `test_unset_box_is_refused_by_name_not_defaulted`, test_box_guard.py:48), one
   kept its name (`:60`).
2. **Rewriting item 5's residue as a code fix.** A one-line change at
   crons.py:798-800 (`return True` for an unnamed box) would make the tree
   green and the tests pass and put four jobs back on a box that never said who
   it is — which is precisely the fail-open a different node spent the round
   closing. Satisfying "record the blast radius" with a code edit is the near
   miss; the residue is filed with the decision left to the owner.
3. **Writing my own node's body and calling it done.** The five corrections land
   in OTHER people's nodes; a node that only reports them is how a false record
   stays false for another round. Every sentence above is cited to bytes I read
   this round, and each edit names the line it replaces.

## Deviations, with the property of this case

- Item 5 is NOT fixed. The standing rule is "fix it in the graph first", and
  the property that makes the rule not apply is that the correct fix is a
  POLICY — which jobs must survive a graph that cannot name its own box — not a
  mechanism. A kid choosing that policy would be wearing an owner decision as
  a code change. Recorded, with the three file:lines a fix would touch, and
  with the test that pins today's contract named (test_box_guard.py:166) so the
  eventual change cannot be silent.
- I did not touch `a00-114ee609-176796` at all. The brief allowed a fix if
  something it asserts were now false; nothing was, and manufacturing work
  there would have been the same defect in a different costume.

## Lines

0 production lines. The only files written were three node bodies, one node
frontmatter (`verdict`, `confidence`) and this node.

## Agent Notes
Five record-vs-bytes corrections: demoted 3c4237 to the lean its own THOUGHT concluded, struck a reaper memo that does not exist (heal.py:1982-2013 holds none), re-costed the memo read onto _nudge_target's four call sites, replaced a false 2-FAILED claim with 7 passed, and filed the ungated grid_sync stripping four box-gated jobs on an unnamed box as a named owner-decision residue.

PARENT REVIEW a00-08a947bf (probes run by the parent, script .agi/sessions/iter-DH.577/a00-08a947bf/parent_probes_k2.py, read-only, nothing applied): Q1 GATE (the demotion is machine-visible): parsing the node frontmatter gives verdict=inconclusive_lean_proved:70, confidence=0.7, and the node own review paragraph concludes a lean at 70 -- the value the graph scores is now the value the review concluded. Before this round it read proved. HOLDS. Q2 AUTH (the struck claim is really false): no refusal-set name is DEFINED anywhere in heal.py, heal.py reaches rows through _send.wake, and the only once-only set across extensions/agi/bin is _FOREIGN_REFUSALS in send.py -- so the reaper memo the old caveat carried does not exist and a residue that does not exist is worse than an open one. HOLDS. Q3 WIRE (the filed cron residue is REAL, not a plausible story): I rendered the LIVE cron:crons node through the real crons.load_crons_node + render_managed_lines in a temp graph with AGI_BOX unset. The loader reports four enabled+boxed jobs [mail_poll, maint_gc, memory_alarm, prime_merge]; render emitted THREE runnable lines -- grid_sync (grid.py commit, */5), branch_push (git push -q origin), nudge_sweep (send.py wake, */2) -- plus one banner line naming the four refused jobs. So the ungated grid_sync really does re-apply every five minutes a crontab in which mail_poll, maint_gc, prime_merge and memory_alarm are absent, and the banner makes it visible without preventing it. The outage mechanism is confirmed by the bytes, not by prose. HOLDS. ACCEPTED, 0 production lines as briefed. The residue stays OPEN and the decision (which jobs must survive an unnamed box) is the owner's, correctly left unbuilt.
