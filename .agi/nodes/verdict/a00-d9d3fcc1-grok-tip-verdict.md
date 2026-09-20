---
id: verdict:a00-d9d3fcc1-grok-tip-verdict
mint_id: f779c94317b2492d8a9e32a89d708894
type: verdict
parents:
  - experiment:a00-d9d3fcc1-grok-tip-measure
next_edges: []
confidence: 0.9
edited_by: a00-d9d3fcc1
evidence_runs:
  - experiment:a00-d9d3fcc1-grok-tip-measure
loop: goal:g7.25.2@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 43cfee744c721a57
season: 2
title: "Verdict: five probes pass on the landed tip — config row is the sole remaining resolve cell"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:a00-d9d3fcc1-grok-tip-verdict

## Verdict

**proved** (confidence 0.9), on `experiment:a00-d9d3fcc1-grok-tip-measure`.

## Evidence

All five probes of the experiment pass on the post-copy tip bytes:

1. **load** — `grok-bot [True, True, True, True, True]`.
2. **hash** — `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c`,
   byte-identical to the canonical copy.
3. **resolve** — `AdapterError: no harness 'grok-bot' in config; declared:
   ['claude-code', 'copilot-cli', 'pi', 'pi-local']` — a named refusal.
4. **dispatch gate** — `grep -Ein grok extensions/agi/bin/dispatch.py` → rc=1,
   no output.
5. **config gate** — `.agi/config.json` sha256 `da08e303…d8e459` identical
   before and after; the `harnesses.grok-bot` row was never written.

### The correction this verdict records

DT.21 said the config row was "the sole remaining gap". On **this** tip that
sentence was false when written: the adapter file did not exist here (it landed
only on a DT.21 side branch). After this round lands the adapter, the sentence
becomes true — `resolve` now fails for exactly one reason, the absent config
row. The verdict is therefore `proved` **for the conditional claim**, and the
unconditional past-tense version is corrected, not ratified.

### Residual gap (honest scope)

`adapters.resolve(cfg, 'grok-bot')` will not succeed until Belam adds the
`harnesses.grok-bot` row — out of scope for this kid and explicitly forbidden
to touch. So the chain ends here with the config row as the one open cell; no
adapter or dispatch change is needed beyond what now exists on this tip.

## Confidence

0.9 — every conjunct is a direct, reproducible probe on the tree bytes; the
0.1 discount is for the untracked-file caveat: until the parent commits the
adapter, `level3.py`'s `git ls-files` scan cannot see it, so the hand-minted
build node is the only thing carrying it into the grid.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. `proved` rather than a lean because the claim is a conjunction
of five executable probes, each observed green, not an inference. Evidence is
cited by node id (`experiment:a00-d9d3fcc1-grok-tip-measure`), not by self.
<!-- THOUGHT:END -->
