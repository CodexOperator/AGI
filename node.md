---
id: doc:card-director-general-1
mint_id: 960e181d30924fb3ba1a63ca4a6698f4
type: doc
parents:
  - goal:g7.31.1
next_edges: []
edited_by: director-general-1
scaffold_hash: 67b067422d7509fe
season: 2
tags: []
title: Card director general 1
town: core
---
# doc:card-director-general-1 — director-general-1's card (the ONE scratch; replaced whole). Written whole 11-16 ~07:3xZ at the meter line (0.47): rotating; the successor runs Sonnet (owner 02:12Z 11-12).

Role: doc:unified-director-brief + this card. Post director-general-1 (uid 979), builder, council loop: SM gates and lands, belam wraps RULES lands, the council (alive, all-is-one, self-perpetuating) rules. Skills: agi-node-write, agi-goal, agi-send, agi-rotate, agi-verify, agi-post.
Method that works: lane = `git clone -q --shared --no-checkout ~/t <lane> && git -C <lane> fetch -q ~/t origin/posts/belam && git -C <lane> checkout -q -b <branch> FETCH_HEAD`; build, run the lanes ALONE (one pytest at a time: the suite lock), commit (signed G), `git push -q ~/t HEAD:refs/heads/<branch>`, then ONE [merge-up] to sanctuary-master naming the branch + tip + what you did NOT run. Never amend a branch SM has queued: a child commit.

## §0 State (11-16 ~07:3xZ)
- LANDED this stretch (mine): L555 (agi-project no fixture default) L570 (fallback cut) L573 L574 (agi.sh host) L575 (RAM stand-in) L576 (n7 + masked refusal) L577 (P7: Fable OFF in the brief + 2 skills). L581 = my e4 test fix (armed behind L580). L583 = DGo1's alarm-id MINT (leaf g7.16.1.11.20.2.1, third re-cut 213590f492) lands FIRST.
- AT SM'S GATE / ARMED, mine: P7b dg1-p7b-fable-grants e504418de7 (L579, RULES, GATE768 = every lane green, 2 timeout reds attributed to load, a WHOLE re-run on bd7a2f7982 started 07:1xZ in g397 ~2 h, re-arms itself). MASKED v2 dg1-masked-v2 be965f3e35 (L582 on GATE772, 3/3 words). ALARM-ID BUILD dg1-alarm-id-build 42adb9d395 (3 commits on fa58b8b8c3: token_hex(8), the one skip line, three-valued already_sent, HOLD bounded by rec['holds'] / --max-holds, reset on a good read, [alarm-unverified]; 43 tests; waits for L583, then SM gates it WHOLE).
- NOTHING for me to build until a residue comes, except the OWED list (§1).

## §1 Plan
- OWED next touch, ONE tip, agi.sh host (not RULES): sp+aio+alive's rule: the act writes its two units only to a REGULAR file or a missing path; a symlink at either unit path that masked() does not call masked is REFUSED by name ('a symlink, not ours: nothing written'); guards test -L too; masked() resolves EACH hop under $R (strip the leading /, re-prefix $R) for the rehearsal ROOT; rows n8d (dangling: nothing created at its target), n8x (link to an existing non-empty file outside /etc: refused, target byte-identical), sp's in-root chain unit -> /etc/x -> /dev/null; mutant: the -L refusal dropped = RED on n8x. Lane d8 holds masked v2.
- OWED, a plain skill clause: skills/agi-research-then-design section 7 (:104): add '(under the 11-10 exception, L509, now OFF: today's design alias is opus)'; the example file stays as record.
- P9 (SM 19:39Z 11-15, mine to MINT): a COUNCIL DESIGN leaf under goal:g7.16.1: rank meters (a more senior post's one window lasts for more progress; what 'progress' counts); through SM's gate (agi-goal skill); owner Q7.
- P5 (auto hub fallback on quota) = goal:g7.16.1.11.46.37 (director-goals-1 minted it; the ENGINE half is director-general-2's, mine only if DG2 cannot).
- The plan-master umbrella goal:g7.31.1.7: leaf 1 (g7.31.1.7.1, agi-project grok arm) CLOSED L555; leaves 2-5 NOT minted (2 agi-run's grok arm, 3 the non-claude mail wake, 4 the row + doc:role-plan-master, 5 live: belam's host act, the owner's word). Read goal:g7.31.1.7 for their text.
- LATER (named, no leaf): f1.sh v2.4 cleanup; heal's pane-unknown line wording; agi-run's grok arm; the old FINDINGS (rotate _derive_pred_pids '0', heal _rotation_in_flight silent skip).

## §2 Landed (one line each; full list in git)
L542 L546 L548 L549 L551 (g7.31.1.6/7 mints + heal) · L555 L570 L573 (agi-project grok arm, no-default AGI_BOX, gate reads carry.env once) · L574 L575 L576 (agi.sh host: no default box, E-only RAM unit + slice, stand-in, masked refusal, n7 under SYSTEMD_UNIT_PATH) · L577 (P7).

## 🔴 Where it stops
Idle at the meter line 11-16 ~07:3xZ. NEXT: read the inbox (below), then the OWED list in §1 in order (the masked-symlink tip; the skill clause; P9 mint). When SM sends a residue on P7b / masked v2 / the alarm-id build, fix it in the lane as a CHILD commit.
Next command: `cd ~/t && AGI_POST=director-general-1 box n && AGI_POST=director-general-1 box read | fold -s -w 200`
Lanes (all under /data/scratch/director-general-1/lanes/, removable after landing): d1 (agi-project cut + boot lanes, LANDED), d2 d3 d4 (agi.sh host, LANDED), d5 (P7, LANDED), d6 (P7b e504418de7, at gate), d7 (e4 fix), d8 (masked v2 be965f3e35, at gate: START the next masked tip from it), d9 (alarm-id build 42adb9d395, at gate).

## §4 Traps (this generation's; move each to its skill at the next rotation)
- A mutant that asserts 'no masked line' is VACUOUS when its setup string was expanded before the fixture var existed (the `ln` failed): single-quote the setup so it expands inside the case, and read that the row PASSES for the real code first.
- The act's backup dir is named by the SECOND: two acts in one second die by name; a lane that runs two acts back to back needs `sleep 1`.
- Lanes launched in the background while I edited the lane file mid-run read the NEW bytes (sh reads lazily): never edit a script a background run is executing.
- `readlink -f` needs every parent to exist: a relative-symlink fixture needs its dir (\$X/dev) created, and the relative path counts from the LINK's dir (three ../ from etc/systemd/system).
- A test pinning a string the code derives from a comment/help text breaks when the text moves: anchor mutants on a code line only the target owns (count == 1 asserted).
- `$(...) || exit` inside an eval'd ok() row exits the WHOLE lane: wrap ok()'s eval in a subshell (already done in the harness lane).
- Two pytests at once are refused by the suite lock (verify-suite.lock): wait for one to finish, never start a second.
- The branch name dg1-alarm-id is DGo1's MINT: mine is dg1-alarm-id-build; check `git -C ~/t rev-parse <branch>` before pushing a new name.

## §5 Verification
Per tip: the lane's rows each with a mutant that reads RED (and the GREEN case run first); merge-tree is SM's; `git show --stat`; list what was NOT run in the merge-up; LOAD > 8: only own lanes, niced; a whole pytest at load ~13 flakes (timeouts): re-run ALONE before reading a red as the tip's.

## §6 BANKED
- agi-reaper (for belam, to the owner): a second uid for heal would close g7.31.1.2's T2 and g7.31.1.6's F4; the ask was banked 11-12, not yet made.
- P8 (the owner's, banked by SM): director class row effort max vs post rows high, and rotate.py's director fallback ultracode True on sonnet.
- DISK: in the home, 11 clones with dirty files or unreachable commits (w5 w7 w8 w10 w11 w12 w15 w16 w17 w20 w22) and 15 git-less exports/scratch (w9 w14 w23-w37) need a person's OK to remove; /data/scratch/director-general-1/lanes/* and tmp.* are mine (a person may remove after the lands).
- P10: gsend refuses tokens and private-range addresses until the capsule leaf lands (SM relaxes nothing).

## §7 ATOMS (inbound owner/parent asks; one row per atom; open > one lap = red)
| atom | from | state |
|---|---|---|
| goal:g7.31.1.7.1 BUILD + every carried NIT | council via SM | DONE L555 L570 L573-L576 (the masked-symlink rule is §1 OWED) |
| P7 Fable OFF (owner 11-15 19:01Z) | owner via belam/SM | P7 DONE L577; P7b at gate (L579) |
| P9 rank meters design leaf | owner Q7 via SM | OPEN: mint after the owed tip (§1) |
| alarm-id leaf BUILD | SM placement 3/3 | AT GATE after L583 |
| plan-master umbrella leaves 2-5 | owner 11-10 via belam/SM | OPEN: leaf 2 next, not minted |
| ROOT DISK, the stream, hub quota (P5) | SM/belam | P5 = DG2's; the rest not mine |

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
address doc:card-director-general-1 reused at G5: before the G3 4a land ba8faaad3a (10-21) it named card mint 241494f333 (goals-1), now doc:card-director-goals-1; from G5 it is this card, mint 960e181d30924fb3ba1a63ca4a6698f4, the card of the post that was director-general-3 (goal:g7.16.1.11.45).
<!-- THOUGHT:END -->
