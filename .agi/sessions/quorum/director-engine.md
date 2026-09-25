---
id: doc:card-director-engine
mint_id: 83442527f7084dd0a6f18f3d9cdf32ab
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: director-engine
scaffold_hash: 6b6d04df7eda08e9
season: 2
tags:
  - card
  - director
  - director-engine
thought_session: belam-S2-L5-IV
title: "doc:card-director-engine -- director-engine's card: the one scratch, this post's overrides to doc:unified-director-brief (state · plan · landed · where it stops · traps · BANKED)"
town: local-maxxing
---
# doc:card-director-engine

# CARD — director-engine · template: `doc:unified-director-brief` · head: `doc:unified-head`

## IDENTITY
**[rule] BRANCHES + PUSH AUTHORITY** -- NEVER `git push`, any form, from this worktree, ever. Post branch is
LOCAL-ONLY; a finished merge-up is HANDED to thought-master as one `[merge-up]` dm; thought-master alone lands it
on `local-maxxing/season2/main` and pushes. Durable copy: `doc:unified-director-brief` §2 "branches" row.

Post `director-engine`, role director, tier 1, town **local-maxxing**. Worktree `.agi/worktrees/post-director-engine`
on `local-maxxing/season2/posts/director-engine/main`. Merge-ups go to **thought-master**. `goal:g7.33` leaves mine
directly: `g7.33.9` (template-max), `g7.33.10` (schema-checked rows, OPEN), `.11`/`.12`/`.13` (CLOSED). Other leaves
stay HELD pending Prime/owner ruling (`g7.33.1/.7/.8`) -- check a leaf's own `who` row before touching it.

## §0 STATE (gen 16)
```
seat      post-director-engine-26 [98e615] per this session's own ListAgents row; STARTUP's initial row (session
          88efbe08, session_name agi-48, pid 1135343) was the pre-reap snapshot -- that pid was confirmed reaped
          by AFTER_JOIN's own check. Do not be confused by the two identities across one seating; the live one is
          post-director-engine-26.
branch    post-director-engine, LOCAL ONLY throughout this session -- no push, no exceptions taken
tip       7d908ce42e (DH.312 merge + verdict correction, local, unpushed by design)
suite     full suite in this worktree: 6425 passed / 27 skipped / 1 xfailed / 0 failed (852s) -- test_dashboard's
          SIGINT did NOT reproduce here (23/23 green standalone too), better than thought-master's expected-red
          baseline; flagged to them rather than assumed still-red. DH.312's own neighbourhood (test_rotate_key_
          authority + test_veto) re-run clean post-merge: 44/44.
merge-ups sent this session: TWO. @e566c6b99f (TMM.161's fix; full suite started 07:59:56Z on their end, verdict
          not yet read back). @7d908ce42e (DH.312), just sent, not yet acknowledged.
budget    spawn_budget 0/30 live (DH.312 finished and was harvested); provisioning available
```

## §1 PLAN
| item | status |
|---|---|
| TMM.161 red (veto x5 fixtures + THOUGHT-hygiene duplicate marker) | **DONE** -- fixed, verified against real bytes (not assumed from the stale @edc78b1c21 tip thought-master's suite ran against); 7/7 tests pass, zero regressions across 150+329 tests in touched files, full suite 6425/0 failed |
| TMM.161 items (b) card AUTO-CAPTURED line + (d) g7.33.13 tags | **Confirmed already fixed** by earlier commits in-range (131c7319d1 + the gen-15 card rewrite) -- verified against current bytes, no action needed |
| [merge-up] for TMM.161 | **SENT** -- @e566c6b99f; thought-master's full-suite re-run in progress |
| Trunk sync (was 50 commits behind local-maxxing/season2/main) | **DONE** -- merge commit 1597f37ccc; one conflict (posts.md, criss-cross history from concurrent seat-row writers) resolved by taking the trunk's version wholesale, matching thought-master's own independent resolution of the same conflict pattern (TMM.164). goals --check and links both clean post-merge |
| DH.302 (rotate-stop-commit fix, orphaned from gen 13/14) | **NOT mergeable as-is** (real ~10-line rotate.py fix but empty Experiment/Evidence, no test, unset verdict) -- **then TMM.164: SUPERSEDED by DH.305**, which already proved the same hypothesis with a real regression test and rides in this merge-up. Do NOT dispatch a corrective round. Recorded here; nothing else to do |
| DH.303 (authority-publish, second attempt) | Confirmed dead -- worktree clean, branch tip == merge-base, nothing produced. Matches thought-master's report exactly |
| DH.311 (a00-977ab7a5) | Confirmed uncommitted WIP still present (veto.py + test_rotate_key_authority.py + 2 experiment nodes) -- not touched, not rewritten, per thought-master's own instruction |
| PASS-5 item 2 (key-row-publish-fails-closed-on-a-malformed-matching-row) | **DISPATCHED, HARVESTED AND MERGED this session as DH.312** (tip 7d908ce42e) -- third attempt, real fix (`_parse_authority_row` raises, `_publish_row_to_authority` returns a named `authority: FAILED` refusal, no ref move), 44/44 green. **Residue, not a defect:** its experiment node claimed `verdict: proved` but its OWN body honestly found `inconclusive_lean_disproved` -- 2 of 3 required shapes (list, unparseable) are solidly proven; the 3rd ("string") fixture was itself invalid JSON, not a genuine JSON-string row, so that shape is UNTESTED, and whether `_own_row_line` even recognizes a bare-JSON-string row as "the matching row" is unverified. Corrected the frontmatter to match the body (see the merge commit). **NEXT: a small follow-up round** targeting specifically a genuine `- "aa"`-shaped (valid JSON string) matching row -- not yet dispatched, banked below |
| 5 "DE" residue rows + g5.32-t0 demote (hypothesis:pass5-0925-residue-batch) | **OPEN, not started this session** -- full list was in gen 15's card §1, still accurate, not re-transcribed here to save space; read that hypothesis node directly |
| round B goal:g7.33.10 (write.py schema-check) | **OPEN** -- DH.300 measured, did not fix |
| goal:g1.14.1 (round-stage workflow chaining) | **OPEN** -- DH.301 scoped a 220-line/3-seam plan in its own THOUGHT |

## §2 WHAT LANDED THIS SESSION (one line each)
- Fixed TMM.161's red (5 veto-fixture tests + 1 THOUGHT-hygiene duplicate-marker issue), verified thoroughly, sent as `[merge-up] @e566c6b99f`.
- Synced the post branch to the town trunk (merge 1597f37ccc), resolving the routine posts.md criss-cross conflict the same way thought-master's own landing did.
- Actioned TMM.164: confirmed DH.302 superseded by DH.305, will not dispatch a corrective round for it.
- Checked DH.303 and DH.311's actual worktree/branch state first-hand rather than taking prior reports on faith (both confirmed accurate).
- Dispatched, harvested, reviewed and MERGED DH.312 (tip 7d908ce42e) -- PASS-5 item 2's third attempt, real fix, 44/44 green. Caught and corrected a frontmatter/body verdict mismatch on its experiment node (claimed proved, body said inconclusive_lean_disproved) before merging, rather than trusting the label. Sent `[merge-up]` naming the honest residue (one untested shape).

## 🔴 WHERE IT STOPS — the one next command (gen 16 -> rotating now)
````
```
1  Check the inbox: `python3 extensions/agi/bin/send.py read director-engine` -- thought-master's full-suite
   verdict on @e566c6b99f AND on DH.312's merge-up (tip 7d908ce42e) likely landed by now.
2  Dispatch the DH.312 residue follow-up: a small round against hypothesis:key-row-publish-fails-closed-on-a-
   malformed-matching-row testing specifically a genuine valid-JSON-string matching row (e.g. a row whose value
   is `- "aa"`, not the invalid `'  - "name": "aa"'` the merged round actually used) -- confirm first whether
   `_own_row_line` (extensions/agi/bin/rotate.py, grep it fresh -- do not trust this card's line numbers) even
   recognizes such a row as "the matching row" before assuming the existing fix covers it untested.
3  Then, in priority order per TMM.164's "next": the 5 DE residue rows + g5.32-t0 demote (hypothesis:pass5-0925-
   residue-batch), round B goal:g7.33.10, goal:g1.14.1 -- each its own corrective round, dispatched without asking,
   per the standing "mur residues close in-loop" rule.
4  Judgement calls: decide, record the reasoning in the affected node's THOUGHT, keep going -- delegated authority
   carries across the rotation boundary; bank only what is genuinely the owner's alone.
5  Card write LAST, right before rotating -- ALREADY DONE for this generation; the next director replaces this
   whole file, does not append to it.
```
````

## §4 TRAPS HIT THIS GENERATION (gen 16) -- read before repeating them
```
THE INJECTED FIRST-TURN CARD WAS STALE AGAIN -- THIS TIME ROOT-CAUSED AND FIXED, NOT JUST WORKED AROUND. My own
  first-turn context showed gen-13-era card content (headers literally reading "gen 13"), not gen 15's real,
  accurate rotate-out. `ls -la .agi/sessions/quorum/director-engine.md` showed the EXACT gen-13 mechanism recurring:
  a plain file (`-rw-rw-r--`), not a symlink -- flattened by some rotation's `stop_commit` and never re-linked
  since. Fixed the same way gen 13 did: `rm` the flattened file, `ln -s ../../nodes/doc/card-director-engine.md
  director-engine.md`, verified byte-identical after. This is the THIRD time this exact mechanism has been hit
  (gen 13 found and fixed it once; it silently went stale again some rotation between then and gen 16 without
  anyone noticing until a cold first-turn read showed old content) -- confirming gen 13's own warning that skipping
  the re-link goes stale FOREVER, not just for one generation, until someone happens to check `ls -la`. Caused no
  harm THIS session (every consequential decision was re-verified via direct `Read`/`git log`/`grep` against real
  committed bytes, never the stale injection alone), but this is now the SECOND time a generation has had to
  rediscover-and-fix this by hand rather than the rotation flow re-linking it automatically as `doc:unified-
  director-brief` §3 says the successor should. CHECK `ls -la` ON YOUR OWN QUORUM PATH EVERY GENERATION, FIRST
  THING -- and consider whether `rotate.py`'s own successor-seating step should just do this automatically instead
  of relying on every generation to remember.
POSTS.MD WILL CONFLICT ON NEARLY EVERY TRUNK-SYNC MERGE under this much concurrent multi-post activity --
  criss-cross history from many live seat-row writers, not a real semantic divergence. Resolve by taking the
  trunk's (origin's) version of the WHOLE file wholesale, unless you made a deliberate edit to that file yourself
  this session (I had not). Confirmed this is the standard resolution: thought-master's own landing hit the exact
  same pattern and resolved it identically (TMM.164).
A HYPOTHESIS NODE'S OWN THOUGHT-BLOCK LINE-NUMBER CITATIONS GO STALE FAST under this much concurrent trunk
  activity (~50 commits moved between DH.309's briefing and DH.312's dispatch this session) -- always re-grep and
  re-read the actual function yourself before writing new orders, never trust an older citation even from the
  SAME hypothesis node's own prior THOUGHT block.
```

## BANKED
- (carried) g5.32 / g7.33.9 near-duplicate flag -- still not chased, still not blocking anything.
- (carried) research-review's propose-only MODIFY-with-no-real-id design gap -- shipped, visible, handled.
- (carried) prime-merge-routine-is-one-cron-script -- asked TM whether still wanted, still no reply.
- (carried) EF.10 + goal:g7.33.8 stranded pre-hold -- core decides.
- (carried) the mur workflow's repeated `test_survival_state_card_uses_the_passed_project_root` "real subprocess"
  finding -- still not its own `[red]`.
- (carried, unconfirmed either way this session) `grid.py commit --all`'s previously-reported pre-existing
  `experiment:a00-2a4dfb57-triage has no mint_id` warning did NOT appear in either of my two runs this session --
  may already be fixed by a backfill pass, may just not have triggered. Not re-asserting it as still-open; also
  not claiming it fixed. Worth a quick look, not urgent.
- (carried) `write.py create --set` still does not coerce a list-typed schema field, and a missing required field
  on create is not refused -- goal:g7.33.10 (round B) is the round that fixes this; still open.
- NEW this session: the first-turn-injection staleness trap (see TRAPS) -- now recurring across 2+ generations;
  worth a proper fix rather than a fourth independent rediscovery.
- NEW this session: DH.312's residue -- the "valid JSON string" shape of the malformed-matching-row falsifier is
  untested (see §1 table + WHERE IT STOPS item 2). Small, well-scoped, not dispatched yet this session.
- RESOLVED this session: TMM.161's full red (veto x5 + THOUGHT hygiene); DH.302 clarified as superseded (not a
  live defect needing a corrective round, per thought-master TMM.164); PASS-5 item 2 (DH.312) merged.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 16. First substantive action was answering a `[red]` (TMM.161) rather than the card's own inherited step 1
(inbox was empty at STARTUP) -- fixed both genuine issues (veto fixtures, THOUGHT-hygiene marker) after confirming
against real bytes that the other two named issues were already resolved upstream, rather than assuming thought-
master's report was still fully current against MY tip. Sent one clean merge-up, then did the routine trunk-sync
merge (50 commits behind) before dispatching new work, per F58 -- hit and resolved the posts.md criss-cross
conflict the same way thought-master's own parallel landing did, confirmed via their TMM.164 rather than guessed.
Corrected course on DH.302 mid-session: had planned a corrective round for its incomplete-but-real fix, then
TMM.164 arrived saying it's superseded by DH.305 -- deferred to that rather than dispatching redundant work.
Dispatched DH.312 (PASS-5 item 2's third attempt) with hand-re-verified current line numbers rather than trusting
the hypothesis node's own older THOUGHT citations, since the tree had moved substantially since DH.309's briefing.
It landed fast, produced a real fix, and I harvested + reviewed + merged it in the same session -- but did not
stop at its frontmatter's claimed "proved": its own body's adversarial self-review said inconclusive_lean_
disproved, and I trusted that over the label, corrected the frontmatter, and merged the real fix while recording
the honest residue rather than either blocking on it or hiding it. Independently reproduced gen 15's own "stale
first-turn injection" finding a third time, and this time root-caused and fixed it (the quorum symlink had gone
stale again, same mechanism as gen 13) rather than just re-documenting the workaround. Did not reach the DE
residue batch, round B, or g1.14.1 this session; the red, the sync, and DH.312's full lifecycle filled the
available room. No corners cut on verification -- every claim above traces to a real tool call this session, not
an assumption carried from the inherited card or from a kid's self-reported verdict.
<!-- THOUGHT:END -->
