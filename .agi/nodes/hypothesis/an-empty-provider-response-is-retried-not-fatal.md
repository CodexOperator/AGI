---
id: hypothesis:an-empty-provider-response-is-retried-not-fatal
mint_id: 1e66c41fbaee45b0985f7e24a1860443
type: hypothesis
parents:
  - goal:g7.33.19
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - "'experiment:a00-b9e8e8d9-6211b4'"
probes: "\"wire: a stub pi that is ALWAYS empty, with .agi/config.json read LIVE from the worktree tip -> 3 runs = 1 + max_retries(2), 3 attempt_boundary records -- NOT 8 = 1 + 7 (a00-3f1f7f95 measured against the 7-cell tree EG.54 later reverted; `git show dab7b02c5:.agi/config.json` 296-298 reads 2 / 5.0, verified EG.141); gate: cells (0,0.01) -> 1 run, no retry; no config reachable -> 3 runs at the 5.0s documented default; auth: live-config guard RED with values.pi_retry deleted from a copy of the real config (a SHAPE guard, never a value pin); wire: exit-0 attempt with an empty response -> 1 run, the guard reached live\""
push_further: "\"EG.141 closed items (1) and (3) of this list, so this is what is actually OPEN, in order. (1) STRUCTURAL, not the detector: the live-config guard resolves through rotate.ENGINE_ROOT, the WORKING TREE, so a green run of it can never certify a commit (a00-8825ba12-ca762b item 7) -- and because EG.54 reverted the cell to the module default (2 / 5.0), no live probe in this worktree can distinguish the cell being read from the default being used; only a rig that writes its own tmp config (test_pi_trajectory_retry.py _project) proves the cells are read. (2) THE WIRE: no LIVE empty provider response has yet been retried end to end; every run in this chain is a stub, which is why the verdict is a lean and not proved. (3) PROCESS: the +30/-5 and +50 breach is recorded, not cut (CEILING section below), and the source edits are COMMITTED at dab7b02c5 -- the old claim that they sit uncommitted was false. (4) COSMETIC, cheap: a00-f7fcb77c-d36728 carries its whole report twice because that file has no BODY:END marker, a defect in the node WRITER, not in the round\""
scaffold_hash: 91bb770a1fb1bf7b
season: 2
tags:
  - parked:g7.16.2
testable_claim: an empty-response stopReason=error is retried a bounded, config-set number of times with backoff and logged; other errors end the round as today
title: "An empty provider response is retried, not fatal (EG.30, TMM.317, assigned: director-engine)"
town: core
verdict: inconclusive_lean_proved:85
---
# hypothesis:an-empty-provider-response-is-retried-not-fatal

## ROUND EG.30 (thought-master TMM.317 03:17Z 09-28: the empty-response retry = an engine fix under goal:g7.33, dispatched right after the EG.9 chain, pi-free)
Measured   02:45-03:15Z 09-28: 5 parent rounds (DH.660 EG.18 EG.19 DH.661 EG.20) died with 0 commits, each after 3 x `"stopReason":"error"` / `"errorMessage":"Provider returned an empty response"` in its output.log (director grep over iter-*/<agent>/output.log; dead logs kept as the director's d<N>.dead1.log), plus EG.23's kid died on its last write. Nothing retries: one transient empty response ends a whole round.
CLAIM      an empty-response stopReason=error from the provider is retried a BOUNDED number of times with backoff (count and delays are config cells), each retry counted in the round log; any other error, or the bound exhausted, ends the round exactly as today.
Dispatch line  config-max: the retry count and backoff are cells (a values.* or harness cell next to the existing pi harness settings), never literals · template-max: none · code: the retry in the pi wrapper only
FIRST ACT  MEASURE before any code: find where pi_trajectory.py (or the harness it wraps) sees the provider's stopReason=error, and paste the lines; reproduce with a committed test that feeds a stub pi emitting one empty-response error then a normal stop, RED on the base (the round dies), GREEN after.
FALSIFIERS the retry fires on a non-empty-response error · no bound (an always-empty provider loops forever) · the retry count is a literal · a retried round's log does not show the retries
TESTS      the new test file + test_bin_help_smoke.py (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); stub pi only, never the live provider
FILE SCOPE extensions/agi/bin/pi_trajectory.py · its new test under extensions/agi/tests/ · .agi/config.json (the retry cells only) · the kid's own node
CEILING    HARD CAP: 1 kid · <= 25 production lines net · <= 60 test lines · pi-free tier-0 · 0 USD -- measure against the cut tip, paste the numstat  [RECORD of the EG.30 order; NOT the governing ceiling -- see "## CEILING — the ONE governing line" below]
PARENT     paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit; check git status -s in the KID worktree before you accept


## CORRECTIVE EG.34 -- closes mur-eg-11 EG.30-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-an-empty-provider-res-a00-99e01741 tip 9e9d44ee8 (branch de-base-EG.34; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
ORDERS    THIS text is the order set; the loop branch's copy of the hypothesis node does not carry the director's CORRECTIVE sections (the post branch does) -- never report that as a defect.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. values.pi_retry absent from the shipped .agi/config.json, so the live bound is the code default (2/5.0s) and the cell is a no-op
2. 3. test_cancel_while_pi_runs_is_still_forwarded cannot tell forwarding from plain death and never checks the child
3. 4. The parent's hand-landed bytes-decode repair of the spawn path has no committed regression test
4. 5. A discarded attempt's trajectory records survive the retry (append mode per attempt) and the retry has no exit-code guard
5. 7. Unreachable `return code` tail in the retry loop
6. 8. Verdict frontmatter contradicts the node's own THOUGHT (lean_disproved:65 vs the written lean_proved:75) and the title still says proved
7. 10. Hypothesis left verdict-less after a decided round
8. The engine already OWNS a file for exactly this failure: extensions/agi/tests/test_live_config_cells.py ('exactly ONE place in the suite reads the live .agi/config.json ... if a cell is removed from the real config, this goes red'). No test was added there for values.pi_retry, so the absent cell that defect 1 names is the one failure that file exists to catch, and the config-max dispatch line (hypothesis:...not-fatal.md:20) has no guard behind it. This is the actionable form of defect 1.
9. The node's config evidence is unfalsifiable as written: a00-5b8a7c8a-39874b.md:73-78 shows 'The cells resolve live in this worktree: live cells -> (2, 5.0)' - but (2, 5.0) IS the module default (pi_trajectory.py:36-37), so that print is identical whether the cell is read or ignored. Re-run live, the cell is None; the evidence line cannot distinguish the two cases and should not be cited as proof the cell resolves.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_live_config_cells.py test_pi_trajectory_retry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE .agi/config.json (the ONE cell values.pi_retry {empty_response_max_retries, empty_response_backoff_s}; config-max, mur-eg-11: the claim is built on it and it is absent from the shipped config) · extensions/agi/bin/pi_trajectory.py · extensions/agi/tests/test_live_config_cells.py · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/nodes/experiment/a00-5aca24e8-1cf709.md · .agi/nodes/experiment/a00-5b8a7c8a-39874b.md · .agi/nodes/experiment/a00-e9c1e478-16f094.md · .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 9e9d44ee8 · <= 40 test lines net over 9e9d44ee8 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 9e9d44ee8 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE EG.54 -- closes mur-eg-16 EG.34-k1 demote
BASE      CUT FROM season2/loops/hypothesis-an-empty-provider-res-a00-3f1f7f95 tip 737712de1 (branch de-base-EG.54; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Three committed tests RED at the merge tip (extensions/agi/tests/test_pi_trajectory.py:79) — the new attempt_boundary row has no `tool` key and three consumers assert the exact row set
2. Test-shaped live policy — .agi/config.json:296 — 7 retries at a 0.01 s backoff (8 respawns in ~70 ms) shipped only so the test can tell the cell from the module default; the tmp-config test already proves the read
3. Config value duplicated as a test constant — extensions/agi/tests/test_live_config_cells.py:65 — `live == (7, 0.01)` makes operator tuning of the cell turn the suite red
4. Retry log misstates its own wait — extensions/agi/bin/pi_trajectory.py:171 — `{:.1f}s` renders the shipped 0.01 backoff as 'in 0.0s'
5. Node bloat — .agi/nodes/experiment/a00-f7fcb77c-d36728.md:22 — the report is duplicated in body and Agent Notes (262 lines)
6. UNVERIFIED, and it is the round's load-bearing guard: pi_trajectory.py:167 adds `or code == 0` so an exit-0 attempt is never respawned, but NO committed evidence establishes a real pi's exit code on a stopReason=error empty response. Every test synthesizes it — test_pi_trajectory_retry.py:75-77 derives rc from the events it itself emits, and the guard test at :116-121 passes `code=0` as a parameter. If real pi exits 0 on an empty response, the new guard suppresses EVERY retry and the feature the whole chain exists to add is inert in production while the suite stays green. The probe I WOULD run and did not (live provider, paid — outside my budget and this stage's rules): one real `pi --mode json` run against a local harness forced to return a single empty response, capturing the turn_end line and `echo $?` together, committed as a fixture; a cheaper first step is grepping the five dead rounds' output.log for the wrapper's propagated exit code.
7. The round's OWN committed tip was red, and its green evidence was measured in a dirty worktree. At 8be9ab063 (the round's own last commit) `.agi/config.json` carries zero `pi_retry` occurrences and `pytest extensions/agi/tests/test_live_config_cells.py` -> 1 failed, 2 passed, KeyError: 'pi_retry' at :62. The cell was left uncommitted and the DIRECTOR salvaged it in 737712de1 ('salvage EG.34's in-scope values.pi_retry cell left uncommitted by parent a00-3f1f7f95'). The node's evidence block '82 passed' (a00-f7fcb77c:169-172) could only be true in the worktree, because the live-cell test reads the working tree through rotate.ENGINE_ROOT, never the commit — so a green run of this test cannot certify the tip. That breaches the order's PARENT line ('COMMIT every kid edit AND every node edit on the loop branch before you exit').
8. The live-cell guard fails by KeyError, not by its own falsifier: test_live_config_cells.py:62 `cells = cfg["values"]["pi_retry"]` raises before the discriminating assert at :66-67 is ever reached, so the red names a dict key instead of the missing cell (reproduced above at 8be9ab063). The round's own CAVEATS (c) names it; residue.
9. The unread reader: the order's TESTS list (e04a59151:35) named only test_live_config_cells.py, test_pi_trajectory_retry.py and test_bin_help_smoke.py, so the round changed the trajectory.jsonl RECORD FORMAT (pi_trajectory.py:105-107) and updated only the one consumer inside its own test file (test_pi_trajectory_retry.py:107-112). test_pi_trajectory.py is the only other reader of that file anywhere in the tree (`grep -rn trajectory.jsonl extensions/agi` -> pi_adapter.py:120 writes the path, test_dispatch.py:138 checks the argv, nothing else parses rows) and it was never opened. That is how a one-line record addition turned three committed tests red at the tip.
POLICY    the live values.pi_retry cell is a PROVIDER policy, never a test discriminator: ship a sane retry/backoff (the module default 2 / 5.0 s is acceptable; seconds-scale backoff, never sub-second), and prove the cell is READ with a tmp config (tmp_path), never by forcing the live value off the default; test_live_config_cells asserts the cell is PRESENT and well-typed, never its value (an operator tuning it must not turn the suite red), and fails by its own message, not a KeyError
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_pi_trajectory.py (its 3 consumers of the record set) test_live_config_cells.py test_pi_trajectory.py test_pi_trajectory_retry.py + test_bin_help_smoke.py once (timeout 900, TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT (TMM.322)); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/pi_trajectory.py · extensions/agi/tests/test_live_config_cells.py · extensions/agi/tests/test_pi_trajectory.py · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/config.json · .agi/nodes/experiment/a00-5b8a7c8a-39874b.md · .agi/nodes/experiment/a00-f7fcb77c-d36728.md · .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 737712de1 · <= 40 test lines net over 737712de1 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 737712de1 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.104 -- closes mur-eg-27 EG.54-k1 demote
BASE      CUT FROM season2/loops/hypothesis-an-empty-provider-res-a00-917f3807 tip 65bcfbf19 (branch de-base-EG.104; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Empty-response detector reads stopReason at the event's TOP level while real pi nests it under event.message — the retry cannot fire in production (pi_trajectory.py:70, :92)
2. 2. The 'real pi shape' test asserts the engine's invented flat fixture, so a green suite certifies that defect (test_pi_trajectory_retry.py:32, test at :116-129)
4. 5. The hypothesis node at the tip carries no EG.54 delta and still reads inconclusive_lean_proved:80 / edited_by a00-3f1f7f95
5. The pre-existing detector's rescue path is UNREACHABLE, so the defect is inherited and the chain has never been live: pi_trajectory.py:90-93 — when json.loads succeeds, ev is a dict, so the raw-substring fallback `return '"stopReason":"error"' in raw and 'empty response' in raw.lower()` (which WOULD match the real nested line) only runs for unparseable text. The docstring at :76 ('5 rounds died on exactly this in EG.18-EG.20') is a fatality count, not evidence the detector ever matched. Nothing in the round's node or tests records that the feature has been dead on the wire since it shipped.
7. False wire evidence recorded on the tip's own node: a00-8825ba12:18 labels the flat stub 'real pi --mode json shape' as a committed probe observation. A production log refutes it (iter-EG.23/a00-bfab7d4a/output.log:7-8), and per the project's own rule an owner/evidence line that is wrong should be corrected in place on the node that produced it — this round corrected the exit-code claim on pi source and left the shape claim standing.
8. Latent next-break, from the same mechanism: _ended_on_empty keys on message_end as well as turn_end (pi_trajectory.py:65-66), but real pi emits a message_end for EVERY message including toolResult (iter-DH.378/a00-0c2aaab4/output.log, 166 message_end vs 81 turn_end). Harmless in the empty case (the error message_end/turn_end are the last two before agent_end, iter-EG.23:7-9), but once the nesting is fixed the 'LAST turn decides' state machine is keyed on a finer-grained event than a turn, and a toolResult message_end would reset the flag.
DIRECTOR (verified 10:2xZ against a production pi log, iter-EG.23 output.log lines 8-9): real pi emits {type: message_end|turn_end, message: {stopReason: error, errorMessage: '...empty response'}} -- NO top-level stopReason. pi_trajectory.py:58-70 _ended_on_empty and :73-95 _is_empty_response both read ev.get('stopReason') at the TOP level, so the retry never fires in production. FIX both to read event.message (keep the top-level read only if a committed fixture proves pi ever emits it), key the LAST-turn decision on turn_end only (M4: every toolResult emits a message_end), and prove it with a committed test whose fixture is the NESTED shape (copy the structure, never a real log line: no ids, paths or model names).
DIRECTOR: V3 (a00-f7fcb77c has no BODY:END) is a WRITER defect -- a findings row, not this round; never hand-edit that node. The +18 vs 15 ceiling breach of EG.54 is recorded as a findings row.
DIRECTOR (numstat self-reference): measure `git diff --numstat 65bcfbf19 <tip BEFORE your paste commit>`, paste it, label it so.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_live_config_cells.py test_pi_trajectory.py test_pi_trajectory_retry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/pi_trajectory.py · extensions/agi/tests/test_live_config_cells.py · extensions/agi/tests/test_pi_trajectory.py · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/nodes/experiment/a00-8825ba12-ca762b.md · .agi/nodes/experiment/a00-f7fcb77c-d36728.md · .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 20 production lines net over 65bcfbf19 (director: two detectors + turn_end keying) · <= 40 test lines net over 65bcfbf19 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 65bcfbf19 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.141 -- closes mur-eg-43 EG.104-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-an-empty-provider-res-a00-123593bc tip dab7b02c5 (branch de-base-EG.141; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. push_further item (3) is false in the commit that ships it (hypothesis node:13 says pi_trajectory.py +30/-5 and the +50 test lines 'sit uncommitted')
2. 3. Near-miss (b) + FOR THE NEXT ROUND are stale in the same commit (experiment node:128, :131)
3. PRIORITY -- Ordered item 7 unfixed: _ended_on_empty still keys on ('turn_end','message_end'); _attempt:155 lets a later message_end overwrite empty=True; no test carries that ordering
4. RECORDED CEILING BREACH (TMM.315), NO CUT: +30/-5 vs 20 and +50 vs 40 stay recorded; item on the THREE contradictory ceilings = state ONE governing line on the hypothesis, label the rest as their rounds' records.
5. FALSE EVIDENCE ROW IN THE NODE THIS COMMIT VERSIONS, uncorrected: hypothesis:12 claims 'shipped .agi/config.json read live from THIS worktree -> 8 runs = 1 + max_retries(7)' and hypothesis:39 claims 'config.json:296-299 now carries values.pi_retry = 7 / 0.01'. The config at BOTH 65bcfbf19 and dab7b02c5 reads 2 / 5.0 (`git show dab7b02c5:.agi/config.json` lines 296-299), and 65bcfbf19's own commit message is 'salvage EG.54's in-scope values.pi_retry cell (2 / 5.0 s) left uncommitted by the kid's done commit'. This commit edits and versions that node (frontmatter + Agent Notes) and leaves the false row standing -- the identical class of defect the order named for a00-8825ba12 at bc790428a ('false wire evidence ... an owner/evidence line that is wrong should be corrected in place on the node that produced it'). The first reviewer did not name it.
6. SECOND ALREADY-FALSE RESIDUE in the same node: hypothesis:42 says 'the live-config test pins the cell to the literal (7, 0.01), so an operator tuning the cell turns the suite red'. extensions/agi/tests/test_live_config_cells.py at dab7b02c5:52-70 asserts SHAPE and never VALUE, and its own docstring says so ('It asserts SHAPE, never VALUE'). The claim is already false in the tip and no one corrected it.
7. THREE CONTRADICTORY CEILINGS IN ONE CHAIN, only one of which governs: hyp:31 '25 net / 60 test' (EG.30), hyp:41 '12/15 ... 52 net vs 40' (EG.34), exp:110 'ceiling 40, test file excluded' (this round, wrong axis), exp:129 '20-line cap ... +50 against 40' (the governing one, from bc790428a). The first reviewer cited the right pair but did not notice the shipped node contradicting its own gate three more times -- which is the record a merge reader will hit first.
8. THE RED RIG HEADLINE IS A RIG ARTIFACT: exp:83-86 pastes 'FAILED test_the_bound_is_the_config_cell_and_holds / 3 failed, 8 passed'. I re-ran the committed file with AGI_TRAJ_WRAPPER against 65bcfbf19's bytes placed in a bin/ tree (so locations.py resolves): 2 failed, 9 passed -- the third failure exists only because the scratch wrapper sat outside bin/ and fell back to the module defaults, which exp:90-92 does explain. The claim itself survives; the pasted count does not.
KIDBRIEF  (mur-eg-31 EG.97 parent finding: the corrective reached the parent only, so the kid wrote code over a 0 cap) -- PARENT: dispatch your kid with --orders pointing at a file holding THIS WHOLE SECTION, and paste its FILE SCOPE + CEILING into the kid prompt; verify the kid's context carries the word CORRECTIVE before it starts.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_pi_trajectory_retry.py test_pi_trajectory.py test_live_config_cells.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/pi_trajectory.py · .agi/nodes/experiment/a00-8825ba12-ca762b.md (its false probe row only) · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/nodes/experiment/a00-b9e8e8d9-6211b4.md · .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over dab7b02c5 · <= 40 test lines net over dab7b02c5 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat dab7b02c5 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.151 -- closes mur-eg-55 EG.141-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-an-empty-provider-res-a00-5bd860ef tip 7575b0795 (branch de-base-EG.151; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. The hypothesis's own Agent Notes still asserts the fix is unfixed, and names a line number this same merge changes -- .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md:74 -- "ordered item 7 is still unfixed -- _ended_on_empty still returns on (\"turn_end\",\"message_end\") at pi_trajectory.py:89-90" is false at 7575b0795, where pi_trajectory.py:96 reads `!= "turn_end"`. The round annotated every other stale headline it touched (a00-b9e8e8d9, the 8-run row, the (7,0.01) pin) and left the one in the node it edited unannotated; a reader resolving that line against the tip gets a wrong statement about the shipped bytes.
2. The proved experiment's fixture order is the reverse of what the chain itself measured on the wire -- .agi/nodes/experiment/a00-4339e263-fd74ee.md:35 -- The node concludes "the empty LAST turn went unretried and the round died on exactly the failure this chain exists to prevent" under verdict: proved, on a fixture (test:232) that puts a toolResult message_end AFTER an empty turn_end. The chain's own measurement says the opposite: hypothesis node line 74, "every toolResult message_end precedes its own turn_end -- latent rather than live". No production log is cited for the post-turn_end ordering; the NESTED_TURN_EMPTY shape is measured (EG.104 log, test:36-39), the ordering is not. The code change is a strict narrowing and is correct; the proof framing is not measured. Expected fix: mark the experiment's claim as a latent-shape fix, not a live failure, or cite a log in which a toolResult message_end follows a turn_end.
3. Ordered item (2) dropped from the tracker with the refuted claim left live in the graph -- .agi/nodes/experiment/a00-8825ba12-ca762b.md:18 -- The parent's push_further ordered "correct a00-8825ba12-ca762b:18 in place with write.py -- it still labels a FLAT stub the real pi --mode json shape, which two production logs refute". The node is unchanged at the tip (probes[conjunct 4] still carries that label with result HOLD) and the rewritten push_further (hypothesis frontmatter:13) no longer lists it, so a claim two production logs refute is now both live and untracked.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_pi_trajectory_retry.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/pi_trajectory.py · extensions/agi/tests/test_pi_trajectory_retry.py · .agi/nodes/experiment/a00-4339e263-fd74ee.md · .agi/nodes/hypothesis/an-empty-provider-response-is-retried-not-fatal.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 7575b0795 · <= 40 test lines net over 7575b0795 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 7575b0795 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CEILING — the ONE governing line, and the records it supersedes (written EG.141, kid a00-4339e263)

GOVERNING: the ceiling the shipped bytes were actually built against, recorded on
`experiment:a00-b9e8e8d9-6211b4:129` — **20 production lines net, 40 test lines net**, the test
file excluded from the production count. Every other number attached to this chain is that
round's RECORD, kept because a round's number is evidence about that round, never the standing
ceiling:

| where | ceiling recorded there | status EG.141 |
|---|---|---|
| this node, EG.30 order (the CEILING line above) | 25 production / 60 test | RECORD of the EG.30 order |
| this node, EG.34 review, thoughts (3) and (4) | 15 production / 40 test; built 12/15 production, 52 net test | RECORD of EG.34 |
| experiment:a00-b9e8e8d9-6211b4:110 | "ceiling 40, test file excluded" | RECORD, and contradicted by its own :129 (the production cap there was 20, not 40) |
| **experiment:a00-b9e8e8d9-6211b4:129** | **20 production / 40 test** | **GOVERNING** |

RECORDED CEILING BREACH (TMM.315), NO CUT: against that 20/40, EG.104 shipped
`extensions/agi/bin/pi_trajectory.py` +30/-5 and `extensions/agi/tests/test_pi_trajectory_retry.py`
+50. The numbers stay on the record as the record; the over-cap lines are the `_stop_fields`
docstring quoting the measurement, not extra scope.

THIS ROUND (EG.141), measured against the CUT tip `dab7b02c5` (read-only `git diff --numstat`):

```
10	4	extensions/agi/bin/pi_trajectory.py
23	0	extensions/agi/tests/test_pi_trajectory_retry.py
```

PRODUCTION net +6 (the turn_end-only keying), TESTS net +23 (the masking test) — inside both 20 and 40.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
triage (parked, by tag): PARKING TEST, git grep 13:5xZ 09-29 -- the retry lives in pi_trajectory, reached ONLY via pi_adapter.build_command (pi_adapter.py:230 -> :119), whose only callers are dispatch.py:1414 :2669 :4381; workflow pi stages build their own argv (workflow.py:1944-1949) and never wrap it, and workflow.py:2512 is adapters.resolve, a config lookup -- dispatch-only (this version re-parks it: residue 44a, the keep call cited the wrong reach). Sanctuary-master mur wf_9a00e1d9-91a residue 44 (bundle 2 R2, goal:g7.16.1.2.2). THE TRIAGE RULE: goal:g7.16.1.1.2. Marked by director-general-2. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->

## Agent Notes
EG.104 (parent a00-123593bc, review of experiment:a00-b9e8e8d9-6211b4; the earlier EG.54 delta item was ordered but NOT done by the kid, so it is recorded here by the parent). The chain was DEAD ON THE WIRE until this round: both detectors read ev.get("stopReason") at the TOP level while real pi nests the stop fields under event["message"] (measured on two independent production logs: iter-EG.23/a00-bfab7d4a/output.log:7-8 and this round a00-b9e8e8d9s own log), so the retry never fired and the docstrings fatality count was never a match. The kid added one helper _stop_fields (top, then nested, then ev["error"]) that both detectors call, +30/-5 production and +50 test lines, and my own rig -- stub pi emitting the nested shape at exit 0 with the shipped config read live (2 / 5.0s) -- now gives 3 runs and 2 retry lines, where the pre-fix bytes from 65bcfbf19 give 1 run and 0 retries; a nested non-empty error still gives 1 run. Verdict raised 80 -> 85, still a lean, for two reasons: no LIVE empty response has yet been retried end to end (every run is a stub or a pre-fix one), and ordered item 7 is still unfixed -- _ended_on_empty still returns on ("turn_end","message_end") at pi_trajectory.py:89-90, latent rather than live because every toolResult message_end precedes its own turn_end. [STALE AS OF 7575b0795 -- annotated by CORRECTIVE EG.151, kid a00-725399ca: the last clause is FALSE at this tip. extensions/agi/bin/pi_trajectory.py:96 reads `if not isinstance(ev, dict) or ev.get("type") != "turn_end":`, so _ended_on_empty keys on turn_end and NOTHING ELSE and ordered item 7 IS fixed (EG.141, kid a00-4339e263). Everything before that clause still stands, including 'latent rather than live' -- a production log has never shown a toolResult message_end following a turn_end, so the hazard was real but unexercised. The sentence is kept as the record EG.104 wrote, not as a statement about the shipped bytes.]
