---
id: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
mint_id: db9975ffca0e467ca1cfc2ce510630e9
type: hypothesis
parents:
  - goal:g7.33.17
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: f38bbb2ebd9a7dbe
season: 2
tags:
  - engine
  - rotate
  - capture
testable_claim: "(1) a captive capture leaves the card where-it-stops slot body and its BANKED section byte-identical and appends its one line (2) a committed test diffs a multi-line-slot + BANKED card before and after: the only change is the appended line (3) the test covers the fenced-slot shape the live cards carry (assigned: director-engine)"
title: "the captive auto-capture keeps the where-it-stops slot and BANKED byte-identical and appends its line -- g7.33.17 row 21 (assigned: director-engine)"
town: core
---
# hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line

# hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line

## Measured
- The captive auto-capture (`extensions/agi/hooks/rotation_alert.py` ~971 -> `_force_capture` :856) REPLACED director-thought's card 'Where it stops' slot body AND its BANKED section with the single 'auto-captured at f=0.4129 ...' line (DT 03:02Z [engine]; the loss is 51dd24bce's diff; DT restored from f76c09619 in 8384aa443). A successor loses the whole owed list.
- `extensions/agi/tests/test_rotation_alert_capture.py:186` only checks that the capture line is PRESENT, so the destruction is green.
- The hook runs from MAIN for EVERY session the moment it lands (goal:g7.33.17 row 21, TMM.277).

## CLAIM
(1) a captive capture leaves the card's 'Where it stops' slot body and its BANKED section byte-identical and APPENDS its one capture line; (2) a committed test captures a card with a multi-line slot and a BANKED section and diffs before/after: the only change is the appended line; (3) the first live capture after landing is gated: the test covers the exact card shape the live cards carry (a code-fenced slot).

## Dispatch line
config-max: none (the capture ratio is already a ladder cell). template-max: none. code: the slot writer in rotation_alert.py -- append, never replace.

## FALSIFIERS
- after a capture, any byte of the slot body or BANKED differs from before (other than the appended line).
- a card whose slot is a fenced block gets its fence broken or duplicated.
- test_rotation_alert*.py or the hook neighbourhood is red.

## TESTS
test_rotation_alert_capture.py (the before/after diff row). Neighbourhood (hook): test_rotation_alert*.py test_session_start_bootstrap.py test_bin_help_smoke.py. tmp cards only -- never a live card, never a live seat.

## FILE SCOPE
extensions/agi/hooks/rotation_alert.py (`_force_capture` and the slot writer only) · extensions/agi/tests/test_rotation_alert_capture.py

## CEILING
1 kid · <= 15 production lines · pi-free tier-0 · 0 USD.

## CORRECTIVE DH.550 -- closes mur-director-engine-23 DH.509-k1 demote + DH.509-k2 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-captive-capture-keeps-a00-df266356 tip d8030e722 (branch de-base-550; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. The capture's own rotate-self step overwrites the slot the round preserves (rotate.py:19167 via rotation_alert.py:935 in the same chain); the committed rows stop at cmd_handoff (test:506, :602), so the claim's end-state is unproved and false on the live path
2. 2. Second copy of the writer's payload rule - rotation_alert.py:856-870 re-implements rotate._replace_stops_body (rotate.py:8080-8102), and this round moved that rule
3. 3. Silent degradation to the destructive bare-line payload - rotation_alert.py:889 `except Exception: pass`
4. 4. Parent hypothesis FILE SCOPE still names only the hook + test while the round shipped 9 production lines in rotate.py
5. 6. No committed row for the live hybrid card shape (test:447)
6. 7. Module-level sys.path mutation + loose header substring match in the new test module (test:29, test:462)
7. There are TWO where-it-stops writers and the round fixed the wrong one for the live chain - the actionable card behind defect 1. `cmd_handoff` composes the slot through `_replace_stops_body` (rotate.py:8254) and the round's 9 lines + all three committed rows live there; the capture chain's SECOND step runs `rotate-self --stops`, which goes through a different writer entirely, `_write_stops_section` (rotate.py:18091, called at 19167), whose `##`-level fenced branch at 18172 does the replacing. The fix is not in the writer at all: it is one line in the hook - build argvs[1]'s `--stops` from the card's own slot the same way `_capture_stops` builds s3 (rotation_alert.py:873-891), instead of from `_stops_line` (rotation_alert.py:935). Until that exists, every committed row is green over a two-step chain whose second step still destroys the payload.
8. The committed suite cannot catch defect 1 by construction: the second argv's payload is asserted by SUBSTRING only - `stops = rot[rot.index('--stops') + 1]; assert 'auto-captured at f=' in stops` (test:192-194) and the same shape at test:436-437. That assertion passes identically for the destructive one-line payload and for a preserving one, so the missing row is exactly the one assertion the round needed: drive `hook._CAPTURE_LOGGED[1]`'s --stops through the same writer and diff the slot, the way test:506/:602 do for argv[0].
9. The new rotate.py branch (8094-8100) changes a caller the claim never authorises and no committed test exercises: a HUMAN `handoff --driven` typing its own s3 into an unfenced `###` slot now keeps the subheader and SILENTLY DROPS the prose under it (pre-fix the whole body was replaced, so nothing appeared to survive; now the header survives and the tail vanishes with no marker). The committed rows only pass because the capture's s3 coincidentally carries that tail. The node declares this as residue, but the writer is shared, so the change is broader than the round's scope measured.
10. 1. `###` unfenced tail below the subheader is dropped for any non-capture caller (rotate.py:8100)
11. 2. no committed row for the live card shape (prose line ABOVE the fence) (test:441)
12. 3. TOCTOU: the payload is read in the hook and written by a later child that re-reads the card (rotation_alert.py:880)
13. 4. stale sub_offset when STATE and the `### where it stops` subheader share one `##` section (rotate.py:8254)
14. 5. the kid widened its own assigned claim and raised the parent ceiling 15->20 with no reason, and flipped edited_by (hypothesis:16)
15. THE CHAIN'S SECOND WRITER IS NEVER DRIVEN BY A COMMITTED TEST AND, BY INSPECTION, REPLACES THE FENCED SLOT PAYLOAD THE FIRST WRITER JUST PRESERVED. The capture spawns handoff THEN rotate-self (rotation_alert.py:824-830 _CHAIN_SCRIPT, :949-952) and the second argv is `rotate-self --force --stops "<stops line> | <capture line>"` (rotation_alert.py:935, :1122-1128). _stops_line is built from `git log -1` and the last signed dm (rotation_alert.py:760-782) -- it carries NO owed list. cmd_rotate_self phase 2 calls _write_stops_section (rotate.py:19167), which replaces the slot's WHOLE fenced region with the rendered stops text (rotate.py:18167-18171, :18050-18090) and preserves only prose OUTSIDE the fence (rotate.py:17961-17986, :18149-18162), while the live owed list is INSIDE the fence (.agi/sessions/quorum/belam.md:54-72). The committed test drives only _CAPTURE_LOGGED[0] (test:504-508) and asserts the second argv's SHAPE (test:438-440), so the capture's end state is unproved on both conjuncts. UNVERIFIED whether it fires live: the one recorded incident (51dd24bce) carries the handoff's fingerprint (outer ```` fence preserved) and not the rotate-self fingerprint (which would re-render the fence at depth 3, rotate.py:18043-18044). Probe I would run and did NOT: tmp root + tmp card, AGI_HOOK_NO_SPAWN, real hook, then _CAPTURE_LOGGED[1] through rotate.cmd_rotate_self(SimpleNamespace(name='probe-director', role='director', force=True, stops=..., timeout=900, ...), tmp_root) and diff the slot -- in a tmp tree, never in this pane.
16. The newly machine-readable clause is violated by the hypothesis's OWN first round: testable_claim now parses (20, 1) (spawn_budget.py:343-349) while experiment a00-05314567-1e363a carries `production_lines: 44` (.agi/nodes/experiment/a00-05314567-1e363a.md:20) -- 2.2x, over the 2x re-brief threshold the brief itself states (brief.py:1452-1455). That round was accepted against the inert default, so nothing surfaced the conflict when the clause became live.
17. Template gap: the generalisable fact the round discovered (a `## CEILING` body clause is inert; the machine clause must live in frontmatter testable_claim) landed only in one node's prose (.agi/nodes/hypothesis/captive-capture-keeps-the-slot-and-banked-and-appends-its-line.md:47), while the schema that mints that section still prescribes the inert location (.agi/context/schemas/[hypothesis].md:49) and the dispatch brief never mentions testable_claim at all (extensions/agi/bin/brief.py:1437-1455; zero hits). The next dispatcher repeats the mistake.
18. The node's `## FILE SCOPE` (hypothesis:44) still names only rotation_alert.py and the test file, yet the round landed rotate.py bytes and rewrote the hypothesis node itself; the re-brief that widened it exists only post-hoc in the child's THOUGHT. A future round scoping from the node would forbid the file the fix lives in.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_rotation_alert_capture.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/rotate.py · extensions/agi/hooks/rotation_alert.py · extensions/agi/tests/test_rotation_alert_capture.py · .agi/nodes/experiment/a00-05314567-1e363a.md · .agi/nodes/experiment/a00-606aa96b-3b1e5c.md · .agi/nodes/hypothesis/captive-capture-keeps-the-slot-and-banked-and-appends-its-line.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (split the numbered items between them, no overlap) · <= 25 production lines net over d8030e722 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.550: mur-director-engine-23 DH.509-k1 + DH.509-k2 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
