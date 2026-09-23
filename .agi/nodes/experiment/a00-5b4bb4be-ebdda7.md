---
id: experiment:a00-5b4bb4be-ebdda7
mint_id: e079146062fd44bfbd591246705d5131
type: experiment
parents:
  - hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey
next_edges: []
confidence: 0.85
edited_by: a00-5b4bb4be
evidence_runs:
  - experiment:a00-5b4bb4be-ebdda7
  - experiment:a00-1838a1cd-bf0d92
loop: hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey@s2
model: deepseek/deepseek-v4.1-flash
probes: "\"C4_FIXED: parent probe probe_c4_first_seating_readback now PASSES (aa row PARSED back, close--- index 6 > aa_line index 5); probe_c4_no_row_refuses still PASSES (authority: REFUSED, ref unmoved). C1/C2/C3 parent probes still PASS. Unit probe: pre-fix base+row -> aa parsed back = False; _insert_row_into_frontmatter -> True with _NEW.\""
production_lines: 25
profile: balanced
role: kid
scaffold_hash: 0fa5b0e7c12f6240
season: 2
title: inserts the first-seating row inside the frontmatter so whois reads it back
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-5b4bb4be-ebdda7

## Experiment

FIXED C4 of `hypothesis:the-key-authority-publish-respects-the-veto-and-fires-only-on-a-rekey`
(the parent falsified it on kid 1's bytes). C1/C2/C3 are NOT re-implemented;
they were already proved. The defect and the fix:

```
agent        defect                                            fix
_publish_row base + row  -> row lands AFTER the closing  ->  _insert_row_into_
_to_authority `---` of posts.md frontmatter              frontmatter(base, row)
              so load_node_file stops before it        inserts the row immediately
              and send._pushed_seats sees NO seat row   before the closing `---`
               (parent probe: aa line idx 6 > close 5)  (aa line idx 5 < close 6)
new test     raw `"name": "aa"` bytes was the only     adds send._pushed_seats
             assertion -> passed on an unreadable row   parse-back + by-name refusal
```

Lines changed (git diff --numstat over `extensions/agi/bin/rotate.py`):
**25** (22 added, 3 removed) — under the 40-line ceiling.

## Evidence

**Red on the pre-fix bytes** (`parent_probes.py:probe_c4_first_seating_readback`,
kid 1's committed bytes; reproduced block from the parent):
```
C4 first-seating publish outcome: authority: OK -- ... -> season2/main
C4 aa row PARSED back by _pushed_seats: False
C4 closing '---' line indexes: [0, 5]  aa row line indexes: [6]
C4 aa row after the closing --- (unparseable)? True
```

**Unit red -> green** (`c4_unit_probe.py`, the same row, two shapes, read by
the engine's OWN `send._load_seats_rows`):
```
  pre-fix append: aa parsed back = False  pubkey_ok = False  rows=1
                  close---=[0, 5] aa_line=[6] order_ok=False
 post-fix insert: aa parsed back = True   pubkey_ok = True   rows=2
                  close---=[0, 6] aa_line=[5] order_ok=True
```

**Green on the built bytes** (all five parent probes pass):
```
  PASS  C4_first_seating_publishes_a_PARSED_row
  PASS  C4_no_row_refuses_by_name
  PASS  C2_veto
  PASS  C1_rekey_only
  PASS  C3_authority_gated_swap
```
`C4b no-row outcome: authority: REFUSED -- the new content carries no 'aa'
row to seat on season2/main | moved: False`

**Tests** (the named GREEN set + the file edited):
```
_test_rotate_key_authority.py_ 9 passed
_test_send.py + test_seatsig.py_ (one run) 358 passed total for the three files
```

**Neighbour reds (RECORDED, not edited -- the intended C3 invariant, inherited
from kid 1; those fixtures use branch `master` so `origin/season2/main` does
not exist, the publish returns `authority: FAILED`, and the swap correctly
defers):**
```
test_rotate.py  3 failed / 325 passed:
  test_rotate_self_completes_pending_swap_before_minting
  test_rotate_self_stops_push_completes_pending_swap_site
  test_rotate_self_merge_push_completes_pending_swap_site
test_rotate_alert_two_tree.py  1 failed / 4 passed / 1 xfailed:
  test_self_cmd_success_reaches_verified_alert
```

## THOUGHT

**What the instruction said vs what the machine does.** The parent probe named
the exact mechanism: `_publish_row_to_authority`'s C4 branch wrote
`content = base + row`, placing the new seat row after the closing frontmatter
`---`, and `load_node_file` stops at that delimiter — so the authority commit
moved while `whois` (`send._pushed_seats`) never saw the seat. Kid 1's own test
asserted only raw bytes (`'"name": "aa"' in new_bytes`), which a fragment
satisfies without being readable — the mechanism, not the bytes, is the claim.

**The fix.** `_insert_row_into_frontmatter(base, row)` finds the FIRST closing
`---` (the same delimiter `_parse_md` finds) and inserts the row immediately
before it, so the row joins the `posts:` list. A base with no frontmatter
delimiter falls back to a plain append — the only shape left that can carry
the row at all. The refusal branch is unchanged and still refuses by name
(`authority: REFUSED -- the new content carries no '<seat>' row ...`) because
`row is None` is checked before the insert.

**Deviation (documented).** The strengthened test adds a second fixture under
`tmp_path / "refuse"` inside the same test rather than a new test function, so
the round stays at the parent's named test. No production line was added to
satisfy a neighbour test; the 4 neighbour reds are the intended C3 invariant
and stay recorded, not edited.

## Agent Notes
C4 fixed: first-seating row now inserted before the closing frontmatter --- via _insert_row_into_frontmatter, so send._pushed_seats parses aa with the NEW pubkey; by-name REFUSED preserved; parent probes C1-C4 all PASS; test_rotate_key_authority 9 passed, test_send+test_seatsig 358 passed; 25 production lines
