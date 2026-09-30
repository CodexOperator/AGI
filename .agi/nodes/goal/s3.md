---
id: goal:s3
mint_id: 99dbc70857fd4bccb9fa9ddb8014f4d0
type: goal
parents:
  - goal:g6
confidence: 1.0
edited_by: alive
goal_id: S3
goal_kind: short-term
heading_level: 2
origin: goals-doc
season: 1
seeds: []
status: retired
tags:
  - goal
  - root
  - short-term
thought_session: g1-g7-rewrite-2026-09-19
title: "S3: A truncated contract value can contain a fence lookalike"
---
`level3.py`'s `_cap()` truncates derived text to 240 characters. In
`nodes/level3/bin-heal.md` the `healer_ctx` input's `how` field is the truncated
source of a `write_text(f"""...```json ...```...""")` call, so the truncated
value contains a literal ` ```json ` sequence **inside** the YAML scalar.

The file is valid YAML today — `yaml.safe_dump` escapes it correctly. The trap
is on the reading side: any consumer that locates the contract's closing fence
by scanning for the first ` ``` ` after ` ```yaml ` stops at the embedded one and
gets a truncated, broken parse. This was hit for real while writing
`stitch.py`, and fixed there by bounding extraction on the
`BUILD-CONTRACT:BEGIN/END` markers and taking the **last** fence in that span;
there is a regression test reproducing the exact `bin-heal.md` shape.

Fix it at the source, cheaply: either neutralise fence-lookalike sequences in
`_cap()`'s output, or document the bounded-extraction requirement in a comment
beside `_cap()` and the marker constants. **The next consumer is the G2.2 model
pass** that fills `why`/`perf`/`security`, so this should land before that runs.
Must not regress the 20 existing level3 tests.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
RETIRED by the council (alive, 02:1xZ 09-30) on the owner line "All S goals should have been retired in favor of nested sub sub goals or whatever that fit under the umbrella goals." (00:5xZ 09-30, relayed by belam) Nothing left open, measured: level3.py:274-296 extracts the contract bounded on the BUILD-CONTRACT markers and takes the LAST fence in the span, with the lookalike documented in its docstring; level3.py is the only contract-fence reader in extensions/agi/bin (git grep). Retired in place per skill agi-goal (status retired, never deleted, never moved: 39 retired goals live in goal/).
<!-- THOUGHT:END -->
