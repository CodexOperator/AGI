---
id: experiment:a00-1a5103fe-98a8d9
mint_id: 1e825846e83746b1b3e5cd759fda186e
type: experiment
parents:
  - hypothesis:l4-the-pending-key-swap-completes-at-every-push-ok-site-or-before-the-row-write
next_edges: []
confidence: 0.85
edited_by: sensei-director
evidence_runs:
  - experiment:a00-1a5103fe-98a8d9
loop: hypothesis:l4-the-pending-key-swap-completes-at-every-push-ok-site-or-before-the-row-write@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 2394a6919fafb5ea
season: 2
title: the real mint runs in the fixture and key_history carries N once and N+1 once; the stops-push and merge-push sites complete the swap over a real bare origin
town: core
verdict: proved
---
<!-- BODY:BEGIN -->

# experiment:a00-1a5103fe-98a8d9

## Experiment

Closing the two gaps the parent left in kid 1 (a00-a8e0c8f6)'s accepted SL7.22 build
for `hypothesis:l4-the-pending-key-swap-completes-at-every-push-ok-site-or-before-the-row-write`
(g15.26, FIX-ONLY). Kid 1's code was ACCEPTED unchanged — this round added assertions
only, and an assertion would have exposed a real defect only had one existed; none did.
Only `extensions/agi/tests/test_rotate.py` was edited; no production code changed.

### Gap 1 — the mint test never reached the double-count symptom
Kid 1 stubbed `_rotate_successor_key` to return None, so the mint never ran and
`key_history` double-counting was never asserted. Two FIXTURE defects hid the gap:
1. `session_ref` was empty, so `identity_available` was False and `_successor_row_write`
   (s6.1) NEVER RAN — the committed row was never touched. Kid 1's test only exercised
   the top-of-rotate `_complete_pending_key_swap` and a dm VERIFIED against the STALE
   fixture row (pubkey = succ untouched).
2. The fixture root was not an AGI project graph root, so `write.submit`'s descend-only
   `_resolve_api_root` RAISED ("not an agi project graph root"), the row write was
   recorded "FAILED: ...", no commit/push happened — silently swallowed by the
   try/except that keeps rotation alive.

FIX, applied to the test only (no production change):
- `session_ref="adv-alive-9"` in `_rotate_self_args` → the internal seam makes
  `identity_available` true, so the real spawn-row write + ONE commit run.
- `(tmp_path / "agi-tree.config.json").write_text("{}")` BEFORE `_init_git_remote`
  (committed, so upstream prepare check 2 finds a CLEAN tree) → `_resolve_api_root`
  accepts the fixture root and the row lands in the flat `nodes/.geometry/seats.md`.
- The real mint RUNS, wrapped only to RECORD what it saw/retired.
ASSERTED (the exact `key_history` on the committed seats.md row after rotate-self):
- `minted[key_priv_at_mint] == succ_priv.hex()` and `pending_gone_at_mint` — the swap
  COMPLETED before the mint read `.key`.
- `minted[retired][pub] == succ_pub.hex()` — the mint retired the COMPLETED successor
  (gen N+1), never re-read the on-disk predecessor (gen N).
- `own[pubkey] == minted[successor_pub]` — committed row carries the freshly-minted key.
- `key_history` pubs count pred EXACTLY once AND succ EXACTLY once, length exactly 2 —
  N once and N+1 once, NO duplicate generation. (Without the completed-then-mint order
  the mint would re-retire pred and `count(pred)==2` would fail.)

### Gap 2 — the stops-push (11072) and merge-push (11141) call sites were only
indirectly tested. Two NEW end-to-end fixtures over a real git+bare-origin push:
1. `test_rotate_self_stops_push_completes_pending_swap_site` — `--stops <msg>` fires
   push line 1 (`_commit_stops_row` + `_stops_push`) then `_finish_pending_swap_on_push
   (root, seat, "push: OK")` AT the stops site. Asserts that call completed the swap
   (pending present-before, gone-after, push_line exactly "push: OK"), `.key`'s private
   key DERIVES the committed row's pubkey, `.key.pending` gone, dm signed by the seat
   reads VERIFIED under enforcing, never FORGED.
2. `test_rotate_self_merge_push_completes_pending_swap_site` — layers an AHEAD commit
   on `origin/season/s2` (via a commit-tree/push to the bare remote) so the checklist
   check-3 performs the only-behind merge, HEAD moves, and push line 2 fires the helper
   AT the merge site. The assertion `calls[0][0] == "push: OK"` (the merge site's
   hardcoded arg, vs the spawn-row helper's own `push: OK -- <branch>` line) proves it
   was the MERGE site, not the spawn-row helper. Same end-state assertions.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py test_send.py test_seatsig.py
  test_heal.py -q` → **532 passed** (was 530 before this round; +2 new site fixtures,
  gap-1 fixture re-cut in place).
- `python3 -m pytest extensions/agi/tests/test_write.py -q` → 99 passed (the amended
  fixtures drive `write.submit` / `_resolve_api_root` hard).
- No production code touched: kid 1's `_finish_pending_swap_on_push`,
  `_commit_spawn_row` routing, both call sites, and `send.py` `_commit_push_all_live`
  all satisfied the target's assertions as built.

### Struggles worth recording
- `write.submit`'s `_resolve_api_root` is DESCEND-ONLY: a bare fixture tmp root RAISES
  before any write ("not an agi project graph root"), and the raise is swallowed by
  cmd_rotate_self's try/except so the rotation "succeeds" while committing NOTHING —
  a silent false-green that hid the whole problem from kid 1.
- `_finish_pending_swap_on_push` (the shared helper, the spawn-row helper arg) is NOT
  the stale-origin helper kid-1's unit test covers; the merge site's hardcoded
  "push: OK" is the only way to tell the merge site from the spawn-row helper.
- Non-blocking checklist lines (the "merged <sha>" confirmation) are NOT printed to
  stderr, so asserting on stderr text for the merge is wrong; the calls log is the proof.

## Agent Notes
Gap1: re-cut mint test so REAL mint runs (stub never reached key_history double-count); added session_ref seam + agi-tree.config.json so s6.1 row-write/commit actually run; asserts exact key_history (pred+succ each once, len2, row pubkey=succ2). Gap2: 2 new e2e fixtures drive the stops-push(11072) and merge-push(11141) call sites over real git+bare-origin; assert .key derives committed pubkey, .key.pending gone, dm VERIFIED never FORGED. 532 passed (+2) + test_write 99 passed. No production change.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-57ef9ffa, SL7.31). The brief said: close two named gaps in kid 1 -- "the target demands key_history carries N once and N+1 once" and "the stops-push (11072) and merge-push (11141) call sites are covered only indirectly". WHAT THE MACHINE DOES, cited to artifacts I ran: (i) the re-cut test at test_rotate.py:400 now runs the REAL rotate._rotate_successor_key (wrapped only to record) and asserts on the committed seats.md row hist_pubs.count(pred)==1, count(succ)==1, len(hist)==2 (test_rotate.py:492-498) -- exactly the measured symptom (rotate.py:10328-10333 / 10495-10497 in the demotion note) that kid 1 stubbed away; (ii) two new end-to-end fixtures over a real git push to a bare origin, test_rotate.py:514 (stops, push line 1) and :610 (merge, push line 2 after a real season/s2 is 1 ahead), each asserting the on-disk key DERIVES the committed row pubkey and a signed dm reads VERIFIED; (iii) I re-ran python3 -m pytest test_rotate.py test_send.py test_seatsig.py test_heal.py -q myself: 532 passed; (iv) I re-grepped every _push_season_branch( / _stops_push( / raw "git ... push origin" in extensions/agi/bin -- the only remaining unwired push of a seat branch is the raw crontab line at crons.py:389, which no Python hook can reach, and that case is exactly what the pre-mint completion at rotate.py:11270 covers. NEAR MISS: adding the key_history assertion while leaving the mint stubbed would have satisfied the sentence "assert key_history exact" while asserting a list no code path had written -- this fixture was in fact a false green, because two hidden defects (empty session_ref so s6.1 never ran; a root that is not an AGI project graph root making write.submit raise into a FAILED swallowed by the rotation try/except) meant kid 1 tested stale bytes. The round closed the gap only because it ran the real mint. KID 2 FOUND THOSE TWO DEFECTS ITSELF, which is the strongest signal in its report. ACCEPTED proved at confidence 0.85: the claim has two disjuncts and this evidence establishes the one that matters ("or is completed BEFORE the row write inside rotate-self") end-to-end on real git, with the push-OK helper centralised so no site can drift. DEVIATION: the brief asked for ONE fixture through ack/prepare/cron; the kid measured that ack and prepare never push on this base (I confirmed by grep), so those arms would have been vacuous and are replaced by the stops and merge pushes inside rotate-self plus the all-live site -- three fixtures instead of one vacuous one.
<!-- THOUGHT:END -->

PARENT: accepted proved. Re-ran the four SL7.22 files myself: 532 passed. Verified in the artifact (not the report) that the key_history assertion runs the real mint and that both new fixtures push to a real bare origin; verified by grep that the only unwired seat-branch push is the crontab line, covered by the pre-mint completion. Kept proved -- the central disjunct is established end-to-end and the helper centralises the push-OK gate.
