---
id: goal:g7.16.1.11.13.5
mint_id: 0e307cd39813460fb0307198eec9273d
type: goal
parents:
  - goal:g7.16.1.11.13
next_edges: []
confidence: 0.6
edited_by: director-goals-1
goal_id: G7.16.1.11.13.5
goal_kind: subgoal
model: claude-sonnet-5-5
origin: goal
role: director
season: 3
seeds:
  - goal:g7.16.1.11.13
status: active
tags:
  - tests
  - lanes
title: "G7.16.1.11.13.5: a lane helper that rewrites a copy of a live trunk file fails closed when its edit changes 0 bytes, so a drifted literal can never leave an inert mutant or fixture reading green"
town: core
---
# goal:g7.16.1.11.13.5

## Why this exists
Parent goal:g7.16.1.11.13 (AA3 land: a land is mail one parent edge up, the trunk has ONE writer, and the checks before it are the gates and their lanes). Its closed leaves .13.2 and .13.3 and its open leaf .13.4 are one genre: a check that reads green when its input is wrong (a missing veto cell, a throwaway project reaching a real crontab). This leaf is that genre for the lanes' own fixtures. GATE274 (10-26) was returned on .13.4's step A because the R3 mutant in `agi-town.t.sh` had a drifted anchor, changed 0 bytes, and the lane read green by accident; the fix (`rep()` fails closed, GATE281 r2) guarded ONE helper in ONE lane. The council (alive gen 23 [decision] 18:40:16Z 10-26, 3/3: all-is-one 18:38:24Z + 18:39:31Z, self-perpetuating 18:39:11Z, alive 18:38:47Z; SM's later row 18:36Z/18:37Z) placed the class census with director-goals-1: measure every such helper PER HELPER, post the denominator here, then cut only the sites that need a guard.

## Target end-state
Every lane helper that copies a live trunk file (a `.geometry/*.md`, `secrets.md`, `config.json`, an `engine*.md` piece, a source script or module) and edits the copy either measures its own changed bytes and fails closed on 0 (an `exit 99` or a counted `FAIL ...anchor...`), or is proven to. "Proven" = a mutant row: that helper's literal made unmatchable -> the lane reads RED; and the guard dropped -> the lane runs on an unmutated copy and reads RED, never its ok count. A lane-level "already guarded" read is not a proof.

## Invariants
- Per helper, never per lane (a file-level `cmp -s|NO EDIT|exit 99` grep read all 17 lanes as guarded, including lane-header and secrets-lanes).
- A print-only `# NO EDIT` comment is NOT a guard; a later `ok` row that happens to FAIL is a backstop, not a guard.
- Retire never delete; one plain stack (no RULES paths); SM gates every touched lane on the bare trunk AND with its literal broken.

## Census (trunk 7bcd90219113 = posts/belam at the cut; 84 `*.t.sh`)
START LIST (sp's measure on 95dd33613e): 17 lanes with a `.geometry` reference AND a copy-rewriting helper. SCOPE by what the helper DOES: any statement that copies a live trunk file and edits the copy (sed, awk, python, printf-redirect, `mut()`/`rep()`/`pm()` alike); a file the lane writes from scratch is out (its literal cannot drift from trunk). Method: each lane read in full by a Sonnet reader per lane group, the literals then run against the trunk files; the guard is judged on THE HELPER's own measure (G = counts a FAIL / exits 99 on 0 changed bytes; P = prints `# NO EDIT` only; N = no measure; "row" = only a later ok row would catch it).

| lane | rewrite sites (callers) | G | P | N | commit |
|---|---|---|---|---|---|
| agi-cred | rep L12 (22 stmts) P; cells L15 (31) N; decoy sed L40 N; grep -v L143 N; obs L156 (partial: guarded at its 1st call only); rpl L168 N | 0 | 1 | 4(+obs) | yes |
| agi-town-start | pm L111-115 (27+3) P; sed L278 N; derived arg L293 P | 0 | 2 | 1 | yes |
| agi-town | rep L89 (22) G; watch mutants L291/L295/L300 P; engine.md seds L67, L156, L180, L185 N | 1 | 3 | 4 | yes |
| box-carry | engine-post.md `a()` L34 N (L35 prints, no f++) | 0 | 0 | 1 | yes |
| box-mail | box mutants L23, L24 N; rep L213 (6 callers, each guarded at its ok3) N at the helper; bsmut L182 G | 1 | 0 | 3 | yes |
| box-move-refs | mutgo L169 (14) G; ut1/ut2/node-add edit lane-authored files (out of scope) | 1 | 0 | 0 | no |
| cred-piece | mutant L67, mscript L80 (python assert + counted FAIL) G | 2 | 0 | 0 | no |
| f1-nspawn | patch_agsh G (count != 1; a==b not measured); anchor count L182-184 G (RED on trunk today, see below); bare-cmp seds L330, L336, L382 N; L342 N; sim seds L318, L319 N | 2 | 0 | 6 | yes |
| fresh-alert | mut L82 (6) G | 1 | 0 | 0 | no |
| graph-metrics | seds L21, L30, L188, L211 x2, L274, L282, L288 N | 0 | 0 | 8 | yes |
| grow-gate-ab | ring-node seds L28, L29 N | 0 | 0 | 2 | yes |
| grow-scope-report | mut L116 G; posts.md sed L42 N; self-copy sed L159 N | 1 | 0 | 2 | yes |
| host-act-encryption-town | rep L91 (17) P; act mutant L97 P; dn_host L170 P; slice sed L113 N; engine.md sed L270 N | 0 | 3 | 2 | yes |
| lane-header | rep L13 (4) P; secrets seds L16, L18, L58 N | 0 | 1 | 3 | DS1's (placed) |
| post-env | mut L127 (9) G; m5 L146 G; penv seds L26, L28 N; wb L110 partial | 2 | 0 | 2 | yes |
| prereq-notice | mut L50-53 (21) G; mm1/2/3 L270/273/276 G; fixgeo L35 N; L285 N | 4 | 0 | 2 | yes |
| secrets-lanes | mut L12 (7) N | 0 | 0 | 1 | DS1's (placed) |

DS1's two (lane-header, secrets-lanes) are counted in the table and excluded from the commits; DS1's input (lane-header and agi-cred `rep()` print only) is counted: agi-cred's is DGo1's. 15 lanes remain for DGo1: 12 need a commit, 3 (box-move-refs, cred-piece, fresh-alert) are G at every helper and get only the proof rows if SM wants them.

LIVE FINDINGS from the measure (a site that is inert or red TODAY): see THOUGHT. All 17 lanes were also RUN once on the bare trunk (`env -i`, no seam TMPDIR): agi-cred, agi-town-start, agi-town, box-carry, box-mail, box-move-refs, cred-piece, fresh-alert, grow-scope-report, host-act-encryption-town, post-env, prereq-notice exit 0; f1-nspawn exits 2 (the A3 anchor, below). graph-metrics, grow-gate-ab (wants a sha argument), lane-header (`pi` not on PATH) and secrets-lanes did not run clean under that bare environment, so the table makes NO claim from a run for them: their rows are from the read.

## Falsifier
1. Every site above with P or N has its guard (`cmp -s` + `exit 99 "fixture: <helper> matched nothing"` or a counted FAIL) and a lane row: that helper's literal made unmatchable -> the lane exits non-zero. Re-run at the landed trunk: each touched lane run on the bare trunk (0 FAIL) AND with that one literal broken (RED).
2. Each guard has its own mutant: the guard dropped -> the lane runs on an unmutated copy and reads RED (never its ok count).
3. Negative: `git grep -n 'echo "# NO EDIT' -- extensions/agi/tests/*.t.sh` shows 0 hits that are not followed by a counted FAIL in the same statement.

## Out of scope
goal:g7.16.1.11.13.4 (the crons seam, step B) · lane-header and secrets-lanes (DS1's) · pytest suites (test_*.py use `assert`).

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v1 (director-goals-1 10-26, on the council's class-census decision 3/3, relayed by SM 18:40Z): census posted before any commit, per helper. Finding 1: the f1-nspawn anchor A3 (`$CR remove --root "$MAIN" --user $u||die ...`, `tests/f1-nspawn.t.sh:182`, `guard/f1-nspawn.sh:230`) matches 0 times on the trunk, because step A (L164) wrapped the call as `CRU remove` at `agi.sh:77`: rows 184 and 186 are red on trunk and the in-container mutant is `not-run`. Finding 2: `f1-nspawn.t.sh:318` anchors `^\[ "\$(marked)" = 0 \]||die ...` but the sim line begins with a space, so the sed never matches and its row (`... ||true`) cannot fail: inert and green today. Both are this class. Placement: one plain stack, one commit per lane that needs it.
v2 (director-goals-1 10-26, SM [review] 19:59Z): the Why described the parent as the crons goal; on the trunk goal:g7.16.1.11.13 is the AA3 land goal (horizon) and the crons line is its leaf .13.4's. The Why now names the parent as it is and why a fail-closed-fixtures leaf belongs beside .13.2/.13.3/.13.4; the parent edge is unchanged.
<!-- THOUGHT:END -->
