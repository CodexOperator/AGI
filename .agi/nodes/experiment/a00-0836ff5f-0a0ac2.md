---
id: experiment:a00-0836ff5f-0a0ac2
mint_id: fb4c03946fde491f86a9e5dc12c1103c
type: experiment
parents:
  - hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
next_edges: []
confidence: 0.85
edited_by: a00-0836ff5f
evidence_runs:
  - experiment:a00-0836ff5f-0a0ac2
loop: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9b1b3b5313649bec
season: 2
title: the live card HYBRID slot shape (prose then fence) gets a committed row -- the shape only a parent probe covered
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0836ff5f-0a0ac2

## What this round is

Not a re-measure of the capture. The two sibling experiments
(`a00-05314567` the hook payload, `a00-606aa96b` the `###` writer branch) already
built the fix and were reviewed. What their parent review left open, verbatim:

> Residue carried to the next round: ... and a test row for the live cards
> HYBRID shape (prose line + fence), which probe A covers but the committed
> suite does not.

So this is the missing-row card: the shape `doc:card-belam` actually carries had
coverage from a throwaway probe script and from nothing committed.

| committed fixture | heading | prose line | fence |
|---|---|---|---|
| `LIVE_SHAPE_CARD` (sibling 1) | `##` | — | immediately after heading |
| `UNFENCED_SLOT_CARDS[h2]` (sibling 2) | `##` | body IS the owed list | none |
| `UNFENCED_SLOT_CARDS[h3]` (sibling 2) | `###` | body IS the owed list | none |
| **`HYBRID_SLOT_CARD` (this row)** | `##` | **yes** | below the prose |

## The byte at risk in this shape, and why the row is not a green duplicate

`_fenced_payload` (rotation_alert.py:855) starts its walk AT the fence, so on the
HYBRID shape the `s3` payload it builds carries **no prose at all** — the owed
list plus the appended capture line. The timestamp/state prose line survives
only because the writer (`rotate._replace_stops_body` -> `_replace_fence_after`,
rotate.py:8060) keeps `lines[:fence+1]`, i.e. everything above the fence.

That is a two-part accident spanning two files, and nothing committed held it
in place. Measured on this card:

```
$ python3 .agi/sessions/iter-DH.550/a00-0836ff5f/probe_hybrid.py
=== _capture_stops s3 payload ===
"0. RESUME (OWNER 13:0xZ, no funds): ...\n1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass).\nauto-captured at f=0.4500 after 10 min without a self-rotate"
=== locate === (1, -1)      # (section 1, sub -1) -- the ## heading IS the slot
head identical: True
BANKED identical: True
```

Note the payload: the prose line is absent from it. If the writer ever stopped
keeping the region above the fence, this row's prose assertion is what fails.

## RED, on the pre-fix bytes

The row is green on arrival, so "RED first" here is the **pre-fix-bytes** check,
not a pre-change run. `prefixify.py` (this node's scratch dir) swaps
`hook._capture_stops` back to its pre-fix bare-line form at `runtest_setup` —
reaching the test module's own `hook` object through the pytest item, because
the file builds it with `module_from_spec`, which never registers in
`sys.modules` (my first two attempts silently no-op'd for exactly that reason):

```
$ env -u TMUX -u TMUX_PANE PYTHONPATH=.agi/sessions/iter-DH.550/a00-0836ff5f \
    python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py -q -p prefixify
FAILED ...::test_capture_appends_its_line_and_keeps_the_slot_and_banked
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h2]
FAILED ...::test_capture_keeps_unfenced_stops_slot_and_banked[h3]
FAILED ...::test_capture_keeps_the_hybrid_prose_then_fence_slot_and_banked
4 failed, 13 passed
```

And the loss on THIS card, driven directly (`probe_hybrid_red.py`):

```
### PRE-FIX _capture_stops (bare line): rc=0 owed_lines=4 LOST=3 prose_kept=True capture_line_count=1
    LOST: 0. RESUME (OWNER 13:0xZ, no funds): DE [decision] 13:1xZ -- zero_usd lanes mint below the floor.
    LOST:    OWED after DH.501 merges up: F13 'Spend checked by hand' -> 'Spend by hand'.
    LOST: 1. CHECK every 4 h (cron f86b1cf9, skill agi-merge-pass).
    after-slot:
      13:1xZ 09-27 probe-S2-L5-XIII: account drained, paid mur paths closed; resume waits on the zero-usd fix
      ```
      auto-captured at f=0.4500 after 10 min without a self-rotate
      ```
```

`LOST=3` of 4, and the slot is now a fence around one line. The prose line
surviving there is exactly the accident named above — the capture line plus the
prose is the whole inherited list.

## GREEN, on the live bytes

```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py -q
17 passed, 4 warnings in 1.27s
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py \
    extensions/agi/tests/test_rotation_alert.py \
    extensions/agi/tests/test_rotation_alert_captive.py \
    extensions/agi/tests/test_session_start_bootstrap.py \
    extensions/agi/tests/test_bin_help_smoke.py -q
162 passed, 6 skipped, 4 warnings in 15.70s
```

The row asserts, on the LIVE card's shape: heading byte-identical; the prose
line present verbatim; each of the 3 owed lines present; the fence run count
unchanged (`"\n```\n"` == 2 before and after, so not broken or doubled); exactly
one `auto-captured` line, landing AFTER the last owed step and inside the fence;
every other non-blank slot line identical to before; BANKED byte-identical.

## Production lines

```
$ git diff --numstat
91   0   extensions/agi/tests/test_rotation_alert_capture.py
```

**0 production lines.** The claim was already built by the two siblings; this
card adds the regression row that pins it, so the ≤20-line production ceiling
is met at 0. No byte outside FILE SCOPE's test file was touched.

## Honest residue (not closed here)

- The **prose-above-the-fence** save is still an accident of two cooperating
  files, now pinned by one assertion. A writer change that stopped keeping
  `lines[:fence+1]` would break exactly this row — which is the intended alarm,
  but the card shape is now the thing that would have to be re-derived.
- The writer's own **trailing-blank normalisation** (the blank line between the
  closing fence and the next section disappears) is still there and still
  excused by the `_content`-style non-blank comparison every row in this file
  uses. Unchanged by this card, and named rather than normalised.
- A `###`-level HYBRID (subheader, prose, fence) has no committed row; the two
  parts are each covered separately (`h3` unfenced, `LIVE_SHAPE_CARD` fenced at
  `##`) but not in combination.
- The scratch `graph/` root the probes built under this node's session dir is
  deleted; `probe_hybrid.py`, `probe_hybrid_red.py` and `prefixify.py` remain.

## Evidence

Raw probe output and both plugins: `.agi/sessions/iter-DH.550/a00-0836ff5f/`
(`probe_hybrid.py`, `probe_hybrid_red.py`, `prefixify.py`). Re-run the RED with
the `PYTHONPATH=... -p prefixify` line above.

## Agent Notes
closed the parent-review residue: committed row for the live card HYBRID slot (## heading, prose line, fenced owed list) -- RED on pre-fix bytes via prefixify (LOST=3/4), GREEN on live, 91 test lines / 0 production
