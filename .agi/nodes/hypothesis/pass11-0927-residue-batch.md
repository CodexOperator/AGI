---
id: hypothesis:pass11-0927-residue-batch
mint_id: 4af032c7eb634ec3933c7328c34430ce
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: b2a2369f824ed2e8
season: 2
status: open
testable_claim: The falsifier grep of goal:g1.27 returns 0 hits and each row below is fixed at its cited line.
title: "PASS 11 doc and skill residue batch: no text names the paid route, points past its block, cites a wrong line, or hand-copies the skill index (assigned: director-engine)"
town: core
---
# hypothesis:pass11-0927-residue-batch

# hypothesis:pass11-0927-residue-batch

PASS 11 residue table (verify-upheld; run mur-p11chunk1of1):
| # | where | residue |
|---|---|---|
| 1 | skills/agi-rotate/SKILL.md:12 | facts pointer `read body 37:64` -- the region is 37:57 since cdcfe5c0b |
| 2 | skills/agi-master-gate/SKILL.md:55 | cites rotate.py:16159 (a bare pass); the mirror gate is rotate.py:4053 branches.mirror_and_prove in _prepare_merge_target |
| 3 | extensions/agi/briefs/director-belam-duties.md:5, master-sensei-duties.md:5, sensei-director-duties.md:3 | 'a review by name on pi' (the PAID harness) + a hand-copied skills index that the startup `skills` entry now loads (owner 05:33Z: no duplication) |
| 4 | extensions/agi/workflows/round-research-review.json:7 | description still 'Requires --harness pi' against its own provider pi-free |
| 5 | .agi/config.json:200,205,210 | workflows notes still name provider pi / the pi harness |
| 6 | .agi/nodes/build/bin-provisioning.md:121 | BUILD-CONTRACT stale: can_fund at line 177 with the old signature |
| 7 | skills/agi-dispatch/SKILL.md:36 | hardcodes '<= 8 live parents' while values.local_maxxing.de_live_parents is the cell |

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.670 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11; evidence run mur-p11chunk1of1 verify_engine-delta-{1,2}.json)
Dispatch line  config-max: row 7 cites the cell values.local_maxxing.de_live_parents, never a number · template-max: rows 1-5 are template/doc text, fixed there · code: none
ORDER      ROW 3 FIRST (belam: "the duty briefs still say review on pi = PAID -- do that row first"): name pi-free for a review by name, and replace the hand-copied skills index with a pointer to the startup skills entry. Then rows 1 2 4 5 7.
ROW 6      a BUILD-CONTRACT is regenerated, never hand-edited: regenerate it with the engine's regenerator and paste the command + its output on your node; if none regenerates it in scope, NAME it on your node for the director (file:line), never hand-edit.
FALSIFIERS each row's cited string still present at its line (paste the grep per row, before and after) · any row fixed by hand-editing a derived block
TESTS      test_bin_help_smoke.py + every test that pins these files' bytes (git grep -l the edited file names in extensions/agi/tests, run those) once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE)
FILE SCOPE skills/agi-rotate/SKILL.md · skills/agi-master-gate/SKILL.md · extensions/agi/briefs/director-belam-duties.md · extensions/agi/briefs/master-sensei-duties.md · extensions/agi/briefs/sensei-director-duties.md · extensions/agi/workflows/round-research-review.json · .agi/config.json (the workflows notes only) · skills/agi-dispatch/SKILL.md · .agi/nodes/build/bin-provisioning.md (regenerated only) · the kid's own node
CEILING    HARD CAP: 1 kid · 0 production code lines · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.670 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.670; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE EG.55 -- closes mur-eg-17 DH.670-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-pass11-0927-residue-b-a00-065c47fc tip 96db57094 (branch de-base-EG.55; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Falsifier conjunct false on the tip — .agi/nodes/goal/g1.27.md:42 — the declared grep returns 13 hits (7 in the files this round edited), unmeetable while `--harness pi-free` matches `pi\b` and dispatch still routes on paid `pi` -- FIX = rewrite ONLY the falsifier grep line on goal:g1.27 (write.py) so it matches the paid `pi` lane and NOT `pi-free`, and paste its hit count on the committed tip; a hit that is a legitimate paid-pi route stays and is named, never deleted
2. Row 3's pointer target does not cover the flows the removed line routed — a real mechanism loss the first reviewer read as a PASS. The three briefs at 96db57094 line 5 (director-belam-, master-sensei-, sensei-director-duties.md) now say 'Your skill set is PRINTED AT YOUR START (… extensions/agi/lib/agent-prompt.md §"Your skills", by tier)', but agent-prompt.md:35-38 is a TWO-row table for tiers `parent` (dispatch, node-write, send, verify) and `kid` (node-write, verify) only, and agent-prompt.md:40 resolves an unstated tier as a kid. agi-goal, agi-rotate, agi-workflow and agi-merge-pass — four of the eight flows the deleted line named — occur NOWHERE in that section (`grep -n 'agi-goal\|agi-rotate\|agi-workflow\|agi-merge-pass' extensions/agi/lib/agent-prompt.md` = 0 hits), and test_agent_prompt_skills.py:13-14 pins that two-tier set deliberately ('names paths not rules', :35). So the round pointed a DIRECTOR/MASTER-SENSEI/SENSEI-DIRECTOR brief at a parent/kid table; following the pointer stops the post being told to read agi-goal before minting, agi-rotate before rotating, agi-workflow before a review by name, agi-merge-pass before a CHECK/PASS. The node's own P3 asserts only 'the pointer they cite resolves: agent-prompt.md:31-38 … (PASS)' — it never checked coverage. Silent: `grep -n duties extensions/agi/tests/test_briefing.py` = 0 hits, so no committed test catches it. Residue-grade (the top-level rule 'Flows have skills — read the matching one BEFORE the flow' still ships in CLAUDE.md/AGENTS.md), but the round's PASS on row 3 is over-claimed.
3. The round-mur residue is named with a FALSE inheritance chain, on a reader the round never read. The node says round-mur.json 'inherits `merge-up-review.json` -> `research-review.json`, whose provider is `claude-code`. extensions/agi/workflows/merge-up-review.json has NO `extends` and NO `provider` (keys: context_timeout_s, description, name, script, stages, type) — the chain does not exist. The real answer is already measured by a committed test the brief ordered the round to run: test_workflow_round_manifests.py:255-271, parametrized over MANIFESTS = ['round-mur','round-research-review'] (:31), asserts round-mur's bare run resolves to a pi adapter with `hcfg.get('zero_usd') is True` — i.e. pi-free. So the residue's stated blocking reason ('it needs a provider decision, not a word swap') is wrong; the correct replacement text is settled by a test in the suite the round ran.
4. Config-max residue on the very line the round config-maxed: extensions/agi/briefs/director-belam-duties.md:29 @96db57094 replaces `<=8 live parents` with `values.local_maxxing.de_live_parents` but leaves `≤5 kids each` as a bare literal two words later, while the cited cell is a DICT (.agi/config.json:359 `{"arm": 10, "arms": [10,5,15], "ceiling": 16, "ceiling_if": {…}}`) — so the new sentence is not evaluable as written. The node also cites the cell at config.json:357; measured, it is :359. Row 7 is declared 'already fixed' on the strength of the SKILL's prose (skills/agi-dispatch/SKILL.md:36, which honestly says 'the cap cell its master names'), which no code reads — `grep -rn de_live_parents --include=*.py` = 0 hits.
5. Record inconsistency inside the reviewed node: the frontmatter note says 'ACCEPTED at lean 70 (kid self-reported 85)' while the same file carries `verdict: inconclusive_lean_proved:85` and `confidence: 0.85`. Wording, not mechanism — recorded so the next reader does not inherit two numbers for one review.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_bin_help_smoke.py once (timeout 900, TMPDIR + --basetemp under /dev/shm, env -u TMUX -u TMUX_PANE -u AGI_POST -u AGI_SEAT (TMM.322)); TEXT-ONLY round: no code, no test logic, no config cell
FILE SCOPE extensions/agi/briefs/director-belam-duties.md · extensions/agi/briefs/master-sensei-duties.md · extensions/agi/briefs/sensei-director-duties.md · .agi/nodes/experiment/a00-f4e64241-bb0a18.md · .agi/nodes/goal/g1.27.md (the falsifier grep line ONLY, write.py) · the kid's own node
CEILING   HARD CAP: this kid only (claude-code text-fix, skill agi-corrective §3a) · 0 production lines · 0 test lines · text only · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 96db57094 <your final tip>` on your node (an empty range is not a measurement)
KID       you ARE the round: commit every edit on your loop branch (cli.py done) before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.55: mur-eg-17 DH.670-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
