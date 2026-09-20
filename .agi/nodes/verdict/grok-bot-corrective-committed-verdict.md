---
id: verdict:grok-bot-corrective-committed-verdict
mint_id: ae9992771a1f4057bc68c8ee7fd0cc8f
type: verdict
parents:
  - experiment:grok-bot-adapter-corrective-committed
next_edges: []
confidence: 0.9
edited_by: a00-677f5141
evidence_runs:
  - experiment:grok-bot-adapter-corrective-committed
line_ceiling: 180
loop: goal:g17.14.1@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "adapter folded byte-identical to the committed blob", "class": "wire", "cmd": "sha256sum extensions/agi/bin/adapters/grok_bot_adapter.py vs git show a824caf71:... | sha256sum vs git show e554c440c:... | sha256sum", "expected": "all three equal 66b7891f...081c", "observed": "all three 66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c", "result": "held"}
  - {"conjunct": "REQUIRED surface is live on the import path (stub build_command threads the row's bin cell)", "class": "wire", "cmd": "adapters.load('grok_bot'); build_command(harness={bin:'/SENTINEL/grok-bot', models:{kid:'grok-4-fast'}}, tier='kid')", "expected": "['/SENTINEL/grok-bot','--model','grok-4-fast','-p',ctx]; REQUIRED all present; DEFAULT_BIN bare", "observed": "exact argv match; REQUIRED present; DEFAULT_BIN='grok-bot'", "result": "held"}
  - {"conjunct": "a tier with no declared model refuses by name; needs_credential explicit False", "class": "gate", "cmd": "model_args({models:{kid:'x'}}, 'parent'); needs_credential({'adapter':'grok_bot'})", "expected": "KeyError naming 'parent' and known tiers; explicit False", "observed": "KeyError \"harness 'grok_bot' declares no model for tier 'parent'; known tiers: ['kid']\"; needs_credential -> False", "result": "held"}
  - {"conjunct": "the harnesses.grok-bot config row is genuinely unlanded (the named residue)", "class": "auth", "cmd": "adapters.resolve(committed .agi/config.json, 'grok-bot')", "expected": "AdapterError by name; committed keys lack grok-bot", "observed": "AdapterError \"no harness 'grok-bot' in config; declared: ['claude-code','copilot-cli','pi','pi-local']\"", "result": "held"}
  - {"conjunct": "the respawn probe tears down its whole process group (no orphan sleep 30)", "class": "gate", "cmd": "python3 extensions/agi/tests/probes/probe_grok_bot_restart.py; pgrep -af 'sleep 30'", "expected": "group_gone True, teardown_ok True, no surviving sleeper", "observed": "new_pid 2862946 is_alive True; group_gone True; teardown_ok True; NO ORPHAN sleep 30", "result": "held"}
  - {"conjunct": "committed-only production_lines is 162; config.json untouched", "class": "wire", "cmd": "git show --numstat --format= 2f93a3685 (non-test .py) ; config.json grep", "expected": "162; config.json absent", "observed": "162 extensions/agi/bin/adapters/grok_bot_adapter.py; config.json NOT in kid commit; dispatch.py zero grok hits", "result": "held"}
production_lines: 162
profile: balanced
rebrief_answer: proceed with ceiling 180
rebrief_request: "162/40: byte-fold re-adds committed DT.17 adapter bytes verbatim; the config row is goal:g17.14.2 and out of scope"
role: kid
scaffold_hash: bd2ccf3c15c9d760
season: 2
title: Grok-bot corrective verified except the unlanded config row
town: core
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# verdict:grok-bot-corrective-committed-verdict

## Verdict

inconclusive_lean_proved:90

## Evidence

The corrective re-lands on this tip byte-honest, and
`experiment:grok-bot-adapter-corrective-committed` records the checks: adapter
sha256 `66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c` equal
to the `a824caf71` blob; the superset test file present whole (246 lines); the
in-tree probe unmocked with `new_pid 2784092`, `is_alive True`, `group_gone
True`, `teardown_ok True`; `test_adapters.py` 35 passed;
`test_grok_bot_adapter.py` 13 passed / 2 failed; `dispatch.py` zero `grok`
hits; `links.py schema` hypothesis row 126 → 124 and `links.py links` broken 0.

### The one named residue (deliberately NOT cleared)

The `harnesses.grok-bot` row in `.agi/config.json` is `goal:g17.14.2`'s
deliverable, and `cli.py:2093` (`_round_scope_ok`) forbids this round's
round-done commit from adding `.agi/config.json`. With the row absent from a
fresh checkout, `test_live_config_grok_row_resolves` and
`test_live_bin_cell_threads_through_to_argv` fail until the row is folded from
the live-config line (`ca330ac35` / `ca3b2da28`). The superset test file means
that fold loses no peer test. This unlanded dependency is why the verdict is a
strong lean, not `proved`.

### Production lines: 162, committed only

The DT.17 tip's `production_lines: 174` counted 12 UNCOMMITTED `.agi/config.json`
lines. This tip does not touch that file (`git diff --numstat HEAD --
.agi/config.json` is empty). The committed-only production measure is 162 — the
adapter alone; the probe and test live under `extensions/agi/tests/` and are
excluded.

## Confidence

0.9 — everything except the config row is byte-verified on this tip; the row
is a real unlanded dependency, so the honest statement is a strong lean, not a
proof.

## Agent Notes
DT.20 re-land of the DT.17 grok-bot corrective: adapter folded byte-identical to a824caf71 (sha256 66b7891f…), probe teardown now killpg+waitpid with group_gone True, committed-only production_lines 162 (not 174), schema hypothesis row 126→124, links broken 0; the harnesses.grok-bot config row stays unlanded for goal:g17.14.2.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.20 parent review a00-677f5141. (1) THE INSTRUCTION: the DT.20 corrective orders name three MUR residues to clear -- a schema-invalid scaffolded hypothesis, a probe whose teardown kills only the bash parent, and a production_lines count of 174 that includes 12 uncommitted config lines -- and mark the config row OUT OF SCOPE; the parent task requires reading the kid DIFF and running one negative probe per claim conjunct. (2) WHAT THE MACHINE ACTUALLY DOES: the folded adapter sha256 66b7891f4f19a0628a0410bf6e9203536d4504b40b0e85185b27bc310826081c equals BOTH the a824caf71 and e554c440c blobs (my sha256 of the live file, three-way); adapters.load('grok_bot') exposes all five adapters.REQUIRED names and build_command(['/SENTINEL/grok-bot','--model','grok-4-fast','-p',ctx]) threads the row bin cell live; model_args refuses an undeclared tier with KeyError naming it; needs_credential returns explicit False; adapters.resolve on the committed .agi/config.json raises AdapterError by name (row unlanded, as designed); the fixed probe prints group_gone True/teardown_ok True and pgrep finds no surviving sleep 30; git show --numstat on the kid commit counts 162 non-test .py lines and carries no .agi/config.json; dispatch.py has zero grok hits; links.py schema hypothesis row is 124. (3) THE NEAR MISS: a parent that read the kid's prose ('teardown fixed, 162 committed-only') and never re-ran the probe or numstat would accept the same two sentences from a probe that still orphaned its sleeper and from a count copied out of the old node rather than measured on the commit -- the words are cheap; only the live pgrep and the commit numstat are evidence. (4) DEVIATION: none; config.json was not touched and the parent recorded its probes here rather than trusting the kid's suite.
<!-- THOUGHT:END -->

Parent review a00-677f5141 (DT.20): ACCEPTED kid a00-6c2bf233, verdict inconclusive_lean_proved:90. Residues 1-3 cleared on the committed tip and independently probed by the parent: adapter three-way sha256 identical to a824caf71/e554c440c (66b7891f...081c); model_args/needs_credential gates hold; adapters.resolve on committed config refuses grok-bot by name (residue 4, out of scope for goal:g17.14.2); probe killpg+waitpid -> group_gone True with no orphan sleep 30; committed-only production_lines 162, config.json untouched; dispatch.py zero grok hits; links.py schema hypothesis 124. The two failing live-config tests are the named, unlanded config-row dependency and were NOT skipped or xfailed.
