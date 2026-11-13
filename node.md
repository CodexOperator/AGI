---
id: doc:card-director-science-1
mint_id: d55057fc5ba24e7ab2bb66cbf9d326bf
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-science-1
scaffold_hash: b3449e9971f09f91
season: 2
tags: []
title: Card director science 1
town: core
---
# doc:card-director-science-1

# doc:card-director-science-1 — director-science-1's card (was director-general-2; council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines. Skills: agi-send · agi-goal · agi-verify · agi-rotate · agi-memory-guard · agi-master-gate. Template: doc:unified-director-brief + role doc:role-director-science.
My lane: FALSIFIER lanes first (test-only + a sha), RED on the build's parent, GREEN on a scratch reference, one-edit mutants + named stays-greens; SM gates. SM also hands me whole leaves (lane + build).

## §0 State (11-12 02:33Z, rotation at an idle close: the owner's model switch, directors -> claude-sonnet-5-5; SM [note] 02:33:11Z: model cell on the trunk 65ded11e0b, this unit read opus at its 02:19Z start, rotate at this idle close to come up on sonnet)
| Field | Value |
|---|---|
| Owner rule | quiet: mail ONLY SM (directors); ONE message per finished thing, no acks. STANDING CLOSE FORM: "CLOSE <leaf> = <sha> + falsifiers RE-RUN at <trunk sha>: <counts>". Owner 10-22: close the CURRENTLY active season leaves, report, IDLE; no new starts |
| Model | owner 02:12Z 11-12 (via belam [decision] 02:14Z, SM relay): directors go to claude-sonnet-5-5, effort unchanged; each takes it at its NEXT idle close, never forced. This rotation is mine. Fable is the owner's, season rollover only |
| Board | trunk = core/season3/main. A plain commit in ~/t is refused (detached view); the turn end commits the card. Leaf commits go in /data/work/gate-director-science-1/wt-close (LOCKED): checkout --detach the live trunk, edit, commit, [merge-up] the sha to SM |
| Worktrees | /data/work/gate-director-science-1/wt-* all LOCKED (wt-39-3, wt-44-7, wt-close, wt-links, wt-ren, wt-sci1, wt-w1). wt-w1 removable only on SM's or belam's word |
| .44.7 | ACTIVE: built + lane-proven; live half = the first real box move between two boxes, PAIRED with .44.8's fresh-box leg. SM places no move to close a leaf. Before any box-move.sh touch: blob 00e4e20ea9 (capsule-xfer.* KNOWN LEAK) |
| .44.8 | NOT mine; stays ACTIVE on the owner's legs. Do NOT set its status |
| .44.8.1 | HELD, not started: 8acb585a24 on my branch only. Banked BY NAME in the owner's report; first item when .44.8 resumes. Two items: pidchk refuses ZERO-row posts.md (mutant: re-indented posts.md); dsig adds stat %n %a %u %g |

## §1 Plan
- done: .46.6 (L309) · .46.7 (L468, 11-09) · .46.8 (L310) · .46.20 V2 (L475 474269e5a8, 11-09) · .13.6 (L230) · .38.2 (L284).
- next: nothing placed. Act only on what arrives in the box.
- blocked: .44.7 live half (a real box move) · .44.8.1 (waits .44.8) · JOB 3 (idea:an-evidenced-disproof-scores-as-a-proof; my MEASURE [finding] sent 11-05: the 63:6 demotions are all season-1 writes; primary outcome_coverage = mvps/hyps, proof-only 6.4% vs disproof-only 1.4%) waits for the council's leaf placement, then ONE tip (idea node finding + leaf) to SM's gate.

## §2 Landed (one line each)
- L475 474269e5a8: .46.20 CLOSE re-cut 2 (gate tip 7a8eb7c7d7), 3/3, belam [landed] 18:39:27Z 11-09.
- L467 350da62c26 + wrap 4abbc8571c: the 53-claude-login.conf drop-in; belam's root act PASS 12:27:42Z 11-09 (first run 12:19Z rolled back: StandardOutput=null on agi-post@ hides any ExecStartPre line).
- L468 d2c3e96f5a: .46.7 CLOSE (one shared workspace named; per-lane caps an owner act).

## 🔴 Where it stops + the exact next command
Idle: all placed leaves closed, rotating to Sonnet per SM 02:33Z; next = box read, act only on what arrives.
Cold start: `box read` (whole, never piped through head). Nothing is mid-gate or mid-send from this generation. The model switch needs no reply to SM (quiet rule: no acks).
Worktrees under /data/work/gate-director-science-1/ also hold wt-44-7b, wt-close2, wt-g6, wt-note, wt-s1, wt-s1-base, wt-s17, wt-s25, wt-s25-base, wt-sci1.dead (older generations; untouched, not removed).
NEXT TOUCH of .46.20 / the drop-in (only when placed): (1) the leaf THOUGHT names the F1 mutant (scratch HOME under the post's uid, EXIT trap, no .credentials.json, prints rc + one line, scratch checked gone: RED rc 1 'Not logged in'); (2) drop or reroute the '[cred] login seeded' echo (it goes to /dev/null on every agi-post@ unit); (3) a build node for extensions/agi/guard/claude-login/53-claude-login.conf (NO-NODE today); (4) if sp's ':' prefix (ExecStartPre=:sh -c) is taken, sd()'s anchor at cred-piece.t.sh:109 moves in the SAME tip; (5) ImportCredential= is a re-tip + a root run, not a one-word swap; (6) header + node line: the credstore file and the drop-in leave TOGETHER, drop-in FIRST (a missing credstore file = 243/CREDENTIALS on every start).
The seeded login survived its first refresh (expiresAt moved 16:55Z -> 02:40Z, 11-09): the live file is the login; the credstore copy is spent by design. A dead login = rm the file + a fresh owner /login + re-seal (leaf Agent Notes).

## §4 Traps (this generation only)
- A plain `claude -p` in this post's shell answers through ANTHROPIC_AUTH_TOKEN (set in the post env, it takes precedence; the harness warns) and proves NOTHING about the login: any login test runs `env -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_BASE_URL -u ANTHROPIC_API_KEY claude -p` (11-09, F1 of .46.20).
- `cmp == credstore` is not a post-start invariant: claude adds fields (subscriptionTypeSource, 524 -> 559 B) with no refresh. Whether a copy is spent is read from the four token fields, compared, never printed.
(Older-generation traps dropped at this rotation as stale or carried: box read whole = agi-send §2; worktree --lock, scratch-export dirs, quoted-line edits, agi-town 7 FAILs under my uid = one-off, not re-hit this generation.)

## §5 Verification (11-09, at 474269e5a8)
F1 seeded home answers (env -u form), 0 re-auth · F1 mutant RED rc 1 · F2 cred-piece.t.sh 29 ok / 0 FAIL, s-d mutant RED · F3 0 token-shaped strings in the drop-in and credpiece.py.

## §6 BANKED
Nothing needs the owner beyond what SM's report carries (.44.7 live half, .44.8 legs, .44.8.1, .46.20 atom 2.25: a second subscription is an owner act).

## §7 ATOMS
None open on this post.
