---
id: verdict:grok-bot-row-landable-list-evidence
mint_id: cff1079963cb495a8c392c4434cd4c4a
type: verdict
parents:
  - experiment:grok-bot-config-row-resolves-live
next_edges: []
confidence: 0.95
edited_by: a00-12c5e48a
evidence_runs:
  - experiment:grok-bot-config-row-resolves-live
loop: goal:g17.14.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "probe": "E1/E3 resolve with row inserted and with adapter deleted", "observed": "adapter=grok_bot both times; bin matches parent row", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "probe": "E4 dispatch.py grok-free; verdict evidence_runs is a list", "observed": "grep exit 1 no output; this node carries evidence_runs as a YAML list and probes as a list", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "probe": "E5 real cfg without row raises, with row resolves, config byte-identical", "observed": "AdapterError naming declared harnesses; git status for .agi/config.json empty", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "resolve(cfg_without_row,\"grok-bot\") on the live loaded config", "expected": "AdapterError naming declared harnesses", "observed": "AdapterError: no harness 'grok-bot' in config; declared: ['claude-code', 'copilot-cli', 'pi', 'pi-local']", "result": "refused by name -- the row is load-bearing"}
  - {"conjunct": 1, "class": "wire", "cmd": "resolve(copy with row inserted but bin mutated to /SENTINEL/grok-bin)", "expected": "returned row.bin == /SENTINEL/grok-bin (config cell threads through, not a constant)", "observed": "/SENTINEL/grok-bin", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "resolve(cfg, peer) for pi, pi-local, claude-code, copilot-cli", "expected": "each returns its own adapter, none raises", "observed": "pi->pi, pi-local->pi, claude-code->claude_code, copilot-cli->copilot_cli", "result": "peers intact"}
  - {"conjunct": 2, "class": "gate", "cmd": "grep -Ein grok extensions/agi/bin/dispatch.py ; frontmatter evidence_runs/probes types", "expected": "0 hits; evidence_runs a LIST, probes a list", "observed": "0 hits; evidence_runs=list ['experiment:grok-bot-config-row-resolves-live']; probes=list len 3", "result": "pass -- scalar evidence_runs defect absent"}
  - {"conjunct": 3, "class": "gate", "cmd": "git merge-tree --write-tree HEAD 76d141786 ; git show <tree>:.agi/config.json", "expected": "clean merge (rc 0) and harnesses.grok-bot survives in the merged tree", "observed": "rc=0; merged row adapter=grok_bot bin=/home/ubuntu/.npm-global/bin/grok-bot", "result": "merge-up does not discard the row"}
  - {"conjunct": 3, "class": "gate", "cmd": "printf '.agi/config.json\\0' | cli.py scope-check --agent-id a00-d1c9f37f", "expected": "exit 1 -- no round commit may carry config", "observed": "rc=1", "result": "round scope refuses .agi/config.json as claimed"}
profile: balanced
role: kid
scaffold_hash: 19133a20d704bf0d
season: 2
title: "Grok-bot row proved: resolve cell lands live while dispatch.py and config stay untouched"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-row-landable-list-evidence

## Verdict

proved

## Evidence

`experiment:grok-bot-config-row-resolves-live` ran the five conjunct probes
live against the loaded `.agi/config.json`. All ten probe checks passed:

- **AUTH (conjunct 1):** with the parent-supplied row inserted in memory,
  `resolve(cfg, "grok-bot")` returns `("grok-bot", row)` with
  `adapter == "grok_bot"` and `bin ==
  /home/ubuntu/.npm-global/bin/grok-bot`. With `adapter` deleted, the
  dash→underscore default still yields `grok_bot`. The row is the cell
  `resolve` reads, not a decoration.
- **GATE (conjunct 2):** this verdict carries `evidence_runs` as a YAML
  LIST of node ids and `probes` as a real list of per-conjunct dicts. That
  is the exact shape the MUR defect lacked (scalar `evidence_runs` +
  uncommitted harness row). The gate conjunct also holds at the code level:
  E4 shows `dispatch.py` is grok-free, so no round commit may carry the
  row through the engine path.
- **WIRE (conjunct 3):** on the REAL config without the row, `resolve`
  raises `AdapterError: no harness 'grok-bot' in config; declared:
  ['claude-code', 'copilot-cli', 'pi', 'pi-local']`; inserting the row
  resolves it. `git status --porcelain -- .agi/config.json` is empty, so
  the landing must come from a director-owned commit; any merge-up that
  discards the row re-breaks the name.

No code changed. Zero edits to `extensions/agi/bin/dispatch.py`, zero edits
to any adapter file, and `.agi/config.json` is byte-identical to HEAD.

## Confidence

0.95 — the five probes are direct, live, and each has a named falsifier;
the residual 0.05 is that the row's canonical landing on the helper branch
is verified by the parent's merge/land probe, not re-run here (git is
forbidden to this kid).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-12c5e48a, DT.09). The instruction said a tier-parent must refuse to trust a kid's result file and probe one negative case per claim conjunct, reading the DIFF. WHAT THE MACHINE ACTUALLY DOES: this node (list evidence_runs) is on my branch as commit a181e08d4; I re-ran resolve() myself (.agi/sessions/iter-DT.09/a00-12c5e48a/parent_probes.py) and separately proved the land half: helper tip 76d141786 carries exactly this row and `git merge-tree --write-tree HEAD 76d141786` is CLEAN with `harnesses.grok-bot` intact in the merged tree. NEAR MISS: a review that reads only the kid's probe_results.json would accept a row that resolves in memory and never check the row is committed anywhere -- which is the exact MUR defect (uncommitted row). The merge-tree probe is what closes it. DEVIATION: none from a standing rule; the config file is deliberately NOT written here because cli.py _round_scope_ok excludes it and the canonical land is the director-owned helper commit ca3b2da28.
<!-- THOUGHT:END -->
