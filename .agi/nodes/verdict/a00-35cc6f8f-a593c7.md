---
id: verdict:a00-35cc6f8f-a593c7
mint_id: 537c851b1f1e440da8fed95f6667f4ec
type: verdict
parents:
  - experiment:a00-879cb9e8-625883
next_edges: []
confidence: 0.75
edited_by: a00-84c9c98d
evidence_runs:
  - experiment:a00-879cb9e8-625883
loop: experiment:a00-879cb9e8-625883@s2
model: stealth/space-bunny-alpha
production_lines: 15
profile: balanced
role: kid
scaffold_hash: 0d0661cb8e76fde0
season: 2
title: Both refuted test items fixed - repair driven and asserted on a parsed key, live pin skips without an .agi
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# verdict:a00-35cc6f8f-a593c7

Correction round on experiment:a00-879cb9e8-625883 (k1). The production half is
ACCEPTED and untouched; two of the test-half items were REFUTED by the parent's
own probes. Both are fixed here, and both fixes are re-probed below.

## 1 · Two refutations, two fixes

| item | parent's probe | fix |
|---|---|---|
| 5 | `assert "on" in text or True in text` — two SUBSTRING tests; `True in text` is a `TypeError` that only survives on `or` short-circuit; and the fixture carried `parents:` + `mint_id`, so `_ensure_frontmatter` returned `frontmatter ok` with byte-identical output and the re-salvage branch **never ran** | fixture drops `parents` + `mint_id` (the node's own probe9 shape) and a real spawn manifest supplies the parent; the assertion is now `True in fm2` — a KEY on the PARSED mapping; added `fm2["parents"] == ["hypothesis:h1"]` so the test proves the repair actually ran |
| 6 | `test_the_LIVE_repaired_artifact_is_still_in_shape` divided `find_project_root(...)`, which returns `None` in a tree with no `.agi` → `TypeError: unsupported operand type(s) for /: 'NoneType' and 'str'` | `root = locations.find_project_root(...)`; `if root is None: pytest.skip(...)`. The pin still asserts the real thing when a `.agi` IS present |

Both are **test-only**. Zero production bytes were added or changed this round.

## 2 · Both parent probes, RE-RUN on the corrected bytes

Raw output: `.agi/sessions/iter-DH.605/a00-35cc6f8f/probe_recheck.out`
(script `probe_recheck.py`; every dir a `tempfile.TemporaryDirectory`, no live
pane, seat, worktree or mint touched).

```
=== PARENT PROBE 1 (item 5): the old assertion form ===
  "on" in text     -> False  (passes on a file the repair never touched)
  True in text    -> TypeError: 'in <string>' requires string as left operand, not bool
  the PARSED mapping, on the real repair output:
  _ensure_frontmatter -> True 'frontmatter repaired'
  re-load ok= True defect= None
  parents back : ['hypothesis:h1']
  True in fm2  : True    <-- the assertion the test now makes
  off_shape    : []

=== PARENT PROBE 1b: the OLD fixture (parents+mint_id) never reached the branch ===
  ok= True msg= 'frontmatter ok' bytes identical: True

=== PARENT PROBE 2 (item 6): the live pin with NO .agi above ===
  SKIPPED cleanly -> no .agi above this checkout; the live pin has no subject

=== and with a .agi present, the pin still ASSERTS (real subject) ===
  find_project_root -> /data/work/agi/.agi/worktrees/a00-49582ae0/.agi
  live file exists  -> True
  loads ok= True probes non-empty= True off_shape= []
```

Read the last block first: probe 2's fix is a skip **only in the no-`.agi` case**.
With a real `.agi` the pin still reads
`.agi/nodes/experiment/a00-fe05fdae-a240f5.md` and asserts
`ok and fm["probes"] and not _off_shape_keys(fm)` — it did all three. A pin that
only skips would be the same defect in the other direction.

## 3 · Tests

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
      extensions/agi/tests/test_links.py \
      extensions/agi/tests/test_bin_help_smoke.py -q          → 101 passed, 6 skipped, 1 failed
```

The one failure is `test_help_smoke[suite_guards.py]`, PRE-EXISTING and unrelated
— `suite_guards.py` is tracked, unmodified at base, and outside this node's FILE
SCOPE; its `--help` subprocess trips the kid-tier gate
(`ERROR: AGI_TIER=kid refuses a bare full-suite directory run`) and exits non-zero.
Not touched, not claimed as fixed.

## 4 · Line accounting (read-only `git diff --numstat 17d7c3dbe`)

```
22  7  extensions/agi/bin/node_writer.py      → 15 net production   (cap 15, UNCHANGED this round)
62 25  extensions/agi/tests/test_links.py     → 37 net test         (cap 40)
```

Nothing staged, committed or pushed — the loop owns every commit.

## 5 · What this verdict does and does not say

**Says:** the two test items the parent refuted are now closed on the bytes, each
by a probe that runs the branch rather than matching a word. The suite that
exercises the writer's shape is 37 net test lines and 29/29 green, and the live
pin no longer dies in a plugin-only tree.

**Does not say:** the node's own residual stands — the `on: yes` → `True: true`
re-spelling is still there, still named as OUTSIDE FILE SCOPE
(`cli.py:429-434` needs the raw header text, and `render_frontmatter` is handed
the re-parsed mapping). The pinned claim is that the field SURVIVES and is
in-shape, which is what the probe above measures; it is not a claim that the
original spelling round-trips. The **production** half of k1 is re-affirmed, not
re-measured: it was accepted on bytes last round and nothing about it moved.

## Evidence

- `probe_recheck.out` / `probe_recheck.py` — this round, both parent probes re-run
- experiment:a00-879cb9e8-625883 — the k1 run these bytes correct
- `git diff --numstat 17d7c3dbe` — 15 net production, 37 net test
- pytest: test_links.py 29 passed; +test_bin_help_smoke.py 101 passed / 6 skipped / 1 pre-existing failure

## Agent Notes
Test-only correction: item 5's substring tautology replaced by a driven branch (parents/mint_id dropped, real manifest, assert True in fm2 on the PARSED mapping); item 6's live pin now pytest.skips when find_project_root is None and still asserts the real node when a .agi exists. Both parent probes re-run and pasted on the node. 15 net production (unchanged), 37 net test (cap 40), test_links.py 29 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-49582ae0, DH.605 k1b). ACCEPTED; verdict kept at inconclusive_lean_proved:75, no demotion. I re-ran BOTH of my own probes against the corrected bytes before accepting, and both now hold.

(1) WHAT THE ORDERS SAID, quoted: "assert on the PARSED MAPPING-s key -- `True in fm2` -- never on substrings of the file text. Delete the `or True in text` form entirely."; "the live pin must SKIP (pytest.skip) when there is no `.agi` to pin, and must still assert the real thing when there is."; "node_writer.py is already at its 15. DO NOT add a production line; this is a TEST-ONLY correction."

(2) WHAT THE MACHINE ACTUALLY DOES. I read the diff (node_writer.py 22/7 UNCHANGED from k1 -- the production half was not re-litigated, as I required; test_links.py 62/25, i.e. 37 net test lines, still under the 40 cap) and re-ran my probes MYSELF, not the kid-s recheck. PROBE 2: with `locations.find_project_root` returning None the live pin now raises `Skipped: no .agi above this checkout; the live pin has no subject` -- no TypeError -- and with the real tree present it PASSES on the real node a00-fe05fdae-a240f5.md, so the pin is not a skip-in-disguise. PROBE 1: the fixture now omits `parents`/`mint_id` and a real spawn manifest supplies the parent, so the re-salvage branch IS reached (the kid-s own output shows msg `frontmatter repaired` and `parents back: [hypothesis:h1]`), and the assertion is `True in fm2` on the PARSED mapping plus `fm2["parents"] == [...]` as proof the repair ran. I confirmed the old form is gone from the file: no `in text` substring assertion remains. test_links.py = 29 passed on my own run.

(3) THE NEAR MISS, the one I looked for because a correction round is where a near miss hides: satisfying "the pin skips" by skipping ALWAYS -- `pytest.skip` at the top of the function, unconditional, so the live coverage the corrective item 6 exists to restore silently evaporates in CI while the suite stays green. Not shipped: the guard is `if root is None` and I ran it both ways, skip-without-subject and assert-with-subject. The second near miss, "drive the branch" satisfied by a fixture that merely LOOKS broken: not shipped either -- the new `fm2["parents"] == ["hypothesis:h1"]` line is the assertion that would fail if the branch were not reached.

(4) NO DEVIATION. Ceiling held on both halves, file scope held, no git beyond read-only numstat.

RESIDUE I AM NAMING, NOT LETTING RIDE: the corrective-s k2 slice (links.py exit code on off-shape nodes) is UNRUN -- my two kids went to the k1 slice, so that item never got a pass this round. And the k1 residual the kid named as OUTSIDE FILE SCOPE stands: the repair can only recover the ORIGINAL spelling (`on`, `~`) from the raw header, and that is cli.py:429-434, so a repaired collapsed key still renders as `True: true`. The field survives and round-trips; the spelling does not come back. Both are the next round-s work, not this one-s.
<!-- THOUGHT:END -->
