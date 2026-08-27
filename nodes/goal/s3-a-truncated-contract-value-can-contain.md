---
confidence: 1.0
goal_id: S3
goal_kind: short-term
heading_level: 2
id: "goal:s3"
mint_id: 99dbc70857fd4bccb9fa9ddb8014f4d0
order: 68
origin: goals-doc
seeds: []
status: active
tags:
  - goal
  - root
  - short-term
title: "S3: A truncated contract value can contain a fence lookalike"
type: goal
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
`LEVEL3-CONTRACT:BEGIN/END` markers and taking the **last** fence in that span;
there is a regression test reproducing the exact `bin-heal.md` shape.

Fix it at the source, cheaply: either neutralise fence-lookalike sequences in
`_cap()`'s output, or document the bounded-extraction requirement in a comment
beside `_cap()` and the marker constants. **The next consumer is the G2.2 model
pass** that fills `why`/`perf`/`security`, so this should land before that runs.
Must not regress the 20 existing level3 tests.
