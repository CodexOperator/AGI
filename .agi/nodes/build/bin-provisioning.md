---
id: build:bin-provisioning
mint_id: 367745fdf488409ab06839a2b1170bf0
type: build
parents:
  - mvp:bin-modules
build_kind: code
confidence: 1.0
edited_by: director-engine
origin: build-scan
payload_ref: extensions/agi/bin/provisioning.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/bin/provisioning.py"
---
`extensions/agi/bin/provisioning.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:bin-modules`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/provisioning.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 54'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: datetime
  how: '`import datetime` at line 56'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 58'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 59'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: urllib.error
  how: '`import urllib.error` at line 60'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: urllib.parse
  how: '`import urllib.parse` at line 61'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: urllib.request
  how: '`import urllib.request` at line 62'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dataclasses.dataclass
  how: '`from dataclasses import dataclass` at line 63'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 64'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: envfile
  how: '`import envfile` at line 67'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(resp.read() or b"{}")` at line 324'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: ProvisioningError
  how: defines public class `ProvisioningError` at line 113
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: MintedKey
  how: defines public class `MintedKey` at line 118
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_provisioning_key
  how: 'defines private function `_read_provisioning_key` at line 128, signature:
    (root: Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: available
  how: 'defines public function `available` at line 145, signature: (root: Path |
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: credit_balance
  how: 'defines public function `credit_balance` at line 150, signature: (root: Path
    | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: can_fund
  how: 'defines public function `can_fund` at line 177, signature: (root: Path | str
    | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _read_runtime_key
  how: 'defines private function `_read_runtime_key` at line 197, signature: (root:
    Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: key_usage
  how: 'defines public function `key_usage` at line 217, signature: (root: Path |
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: min_key_remaining_floor
  how: 'defines public function `min_key_remaining_floor` at line 244, signature:
    (cfg: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: check_runtime_key_floor
  how: 'defines public function `check_runtime_key_floor` at line 256, signature:
    (cfg: dict, root: Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: settings
  how: 'defines public function `settings` at line 288, signature: (cfg: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: workspace
  how: 'defines public function `workspace` at line 301, signature: (cfg: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _call
  how: 'defines private function `_call` at line 315, signature: (method: str, url:
    str, key: str, payload: dict | None=None, timeout: int=30)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: key_name
  how: 'defines public function `key_name` at line 332, signature: (iter_n: int |
    str, agent_id: str, tier: str=''kid'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: mint
  how: 'defines public function `mint` at line 342, signature: (*, iter_n: int | str,
    agent_id: str, tier: str=''kid'', limit_usd: float=DEFAULT_LIMIT_USD, ttl_minutes:
    int=DEFAULT_TTL_MINUTES, workspace_id: str | None=None, root: Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: revoke
  how: 'defines public function `revoke` at line 420, signature: (key_hash: str, root:
    Path | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: list_keys
  how: 'defines public function `list_keys` at line 434, signature: (root: Path |
    str | None=None, workspace_id: str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: list_all_keys
  how: 'defines public function `list_all_keys` at line 466, signature: (root: Path
    | str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: reap_orphans
  how: 'defines public function `reap_orphans` at line 494, signature: (root: Path
    | str | None=None, live_hashes: set[str] | None=None, dry_run: bool=False, workspace_id:
    str | None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: 'defines public function `main` at line 539, signature: (argv: list[str] |
    None=None)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(payload)` at line 317'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 11 `print()` call(s) at line(s) [552, 561, 563, 576, 581, 585, 588, 595, 621,
    624, 626]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DEVIATION (director-engine, authorised by belam 13:1xZ): edited in my own seat, no kid -- a kid needs the key this fix unblocks. (1) belam relaying the OWNER: account drained (0.606 USD, no top-up) -> zero-USD lanes mint below the floor; policy: mint learns the harness, a zero_usd key is hard-capped by provisioning.zero_usd_key_limit_usd (0.01), the dispatch key/account floors exempt ONLY zero_usd lanes, paid lanes read their floor from a cell, never let the account go negative. (2) Machine: can_fund refused every mint under the literal MIN_REMAINING_CREDITS 1.0 (was :206), pi-free included; now can_fund(root, zero_usd) floors a free lane at its own key cap and a paid lane at provisioning.min_mint_remaining_usd; mint(zero_usd=True) forces limit = the cap; dispatch.py passes the harness row zero_usd and skips the openrouter floor block for it; workflow.py passes cfg harnesses[name].zero_usd. (3) Near miss: exempting the floor without the cap would let a free-lane key spend real money if a model were mis-labelled free; the cap bounds it at a cent. (4) The paid path calls can_fund(root) exactly as before so the old stubs stand. Tests: test_zero_usd_mint_floor.py 5 + provisioning/dispatch/workflow/help-smoke green.
<!-- THOUGHT:END -->
