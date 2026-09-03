---
id: experiment:the-viewport-reaches-parity
mint_id: c6c5b278701e49feb5f737396f494773
type: experiment
parents:
  - hypothesis:the-briefing-is-the-missing-half
next_edges: []
scaffold_hash: c6d51a69d6c7149a
title: "The briefing extracted, INJECTION.md byte-identical, and the viewport at full section parity"
verdict: proved
confidence: 0.95
evidence_runs: 1
---

# experiment:the-viewport-reaches-parity

## Experiment

Extract the nine briefing sections into `bin/briefing.py`; have both
`render-context.py` and `viewport.py` compose that one object; verify the
output of the renderer did not move and the viewport gained the sections.

## Evidence

### 1. `INJECTION.md` is byte-identical

The extraction moved text; it did not rewrite it.

```
$ diff <(grep -v '^_generated' INJECTION.before.md) \
       <(grep -v '^_generated' .agi/context/INJECTION.md)
(no output)
```

Only the generation timestamp differs. **This is the load-bearing result** —
it is what distinguishes an extraction from a reimplementation that happens
to look similar, and it is the reason deleting `render-context.py` in L1.05
is now safe.

### 2. Section parity, exactly

```
viewport --emit llm          INJECTION.md
## graph snapshot            ## graph snapshot
## chain diagnostics         ## chain diagnostics
## attractive ideas          ## attractive ideas
## big-vs-small decision     ## big-vs-small decision
## verdict taxonomy          ## verdict taxonomy
## chain rules               ## chain rules
## next-step suggestions     ## next-step suggestions
## standard commands         ## standard commands
## the graph                 ## ASCII view (≤200 lines)
```

Eight of nine identical. The ninth is the intended difference — the frame
stream replaces the ASCII renderer, which is the whole point of the swap.
The rule text is identical byte for byte, because there is now one copy:

```
$ diff <(viewport --emit llm | sed -n '/## chain rules/,/## next-step/p') \
       <(sed -n '/## chain rules/,/## next-step/p' INJECTION.md)
IDENTICAL — one source
```

45 → **111 lines** at the default 40-frame window, **216** at `--height 200`.
The residual line-count difference is window size, not content.

### 3. `--verify` still passes, and now checks more

```
frames in slice: 40   human lines: 43   llm ids: 40   briefing: yes
PASS — one stream, two formatters, same nodes in the same order
```

`_verify` gained a briefing check: the node count, the primary metric name and
the coverage figure must appear in **both** renderings, and the llm view must
carry the chain rules. Two readers being told different numbers about one
graph is what `goal:g9.7` forbids one layer up.

### 4. A regression this nearly shipped with

`_verify` extracted node ids from **"any line containing a backtick"**. The
briefing is full of backticks — `metric_primary`, the verdict taxonomy, every
declared command — so adding it turned the verifier's own input into noise.
It would not have failed; it would have quietly started measuring different
lines and kept printing PASS.

Fixed with a `_FRAME_LINE` pattern that matches a frame line and only a frame
line, and pinned by a test that asserts the **naive match no longer agrees**,
so the test cannot rot into a tautology:

```python
naive = [ln.split("`")[1] for ln in llm.splitlines() if "`" in ln]
assert naive != ids, "if the naive match still works, this test tests nothing"
```

### 5. Suite

`1346 → 1352`, all passing. Six new tests: the rules reach the kid, both
readers get the same facts, the frame order survives the briefing, no-briefing
is a supported state, the compact projection states the same numbers, and a
gameable primary is named as invalid.

## What is NOT proved

- **`INJECTION.md` is not retired.** `render-context.py` still writes it and
  the SessionStart hook still reads it. That is L1.05, and it is now a
  deletion rather than a migration.
- **`dashboard.py` and `zoom.py`'s three internal renderers are untouched.**
  The "five render paths" count is unchanged; this made the *replacement*
  viable, it did not perform it.
- **No kid has been spawned against the viewport's output.** Parity is proved
  by comparison, not by an agent successfully working from it.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The byte-identical diff is the only claim here I would defend hard. Everything else — section parity, line counts, the passing verify — is consistent with a careful reimplementation that happens to agree today and drifts next month. Byte-identical output from a moved block of text is not consistent with that, and it is cheap to check, so it is the check that was run first and the one this node leads with.

The `_verify` regression is recorded at length because of what kind of failure it is. It would not have gone red; it would have gone green about the wrong lines. That is the second time in this session a guard silently measured nothing (the first was the command-subcommand test, three attempts), and the two share a cause: a check written against a shape, which then had its input reshaped underneath it. The defence in both cases was the same and it is worth naming as a habit rather than a fix — assert that the OLD, broken predicate now disagrees, so the test fails if it ever becomes a tautology again.

Verdict `proved` with evidence_runs 1: one extraction, verified four ways. Confidence 0.95 rather than 1.0 because parity was measured against today's corpus, and a section that happens to be empty right now (chain diagnostics reports 0 chains) could differ under a corpus where it is not.
<!-- THOUGHT:END -->
