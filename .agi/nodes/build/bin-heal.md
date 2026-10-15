---
id: build:bin-heal
mint_id: 2405ecff7d3a4584af5cd7ec815bc679
type: build
parents:
  - goal:g7.16.1.2.1
  - idea:engine-heal
build_kind: code
confidence: 1.0
edited_by: belam
origin: build-scan
payload_ref: extensions/agi/bin/heal.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: director-general-5
title: "Build: extensions/agi/bin/heal.py"
---
`extensions/agi/bin/heal.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-heal`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/bin/heal.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 18'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: argparse
  how: '`import argparse` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 21'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 22'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shlex
  how: '`import shlex` at line 23'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: signal
  how: '`import signal` at line 24'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 25'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: time
  how: '`import time` at line 27'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: uuid
  how: '`import uuid` at line 28'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 29'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: locations
  how: '`import locations` at line 42'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dispatch.pi_model_args
  how: '`from dispatch import pi_model_args` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dispatch.scrubbed_env
  how: '`from dispatch import scrubbed_env as _scrubbed_env` at line 43'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(manifest_path.read_text())` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.read_text()` at line 83'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(cfg_path.read_text())` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.loads
  how: '`json.loads(ap_file.read_text())` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: log_path
  how: '`log_path.read_bytes()` at line 160'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg_path
  how: '`cfg_path.read_text()` at line 57'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap_file
  how: '`ap_file.read_text()` at line 96'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cli-args
  how: builds an `argparse.ArgumentParser` (module-wide, no single call site)
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: _pi_model_args
  how: 'defines private function `_pi_model_args` at line 46, signature: (root: Path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: main
  how: defines public function `main` at line 64
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _pid_alive
  how: 'defines private function `_pid_alive` at line 132, signature: (pid: int)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _heal
  how: 'defines private function `_heal` at line 140, signature: (root: Path, iter_n:
    int, agent_id: str, rec: dict)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: healer_ctx
  how: '`healer_ctx.write_text( f"""# HEALER for hung agent {agent_id} (iter {iter_n})
    The original agent timed out. Diagnose what blocked it and patch. ## Original
    Agent Record ```json {json.dumps(rec, indent=2)} ``` ## Last 4 KiB of Agent Output
    `...[truncated, 1264 chars total]` at line 170'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sess_dir / "agent.json"
  how: '`(sess_dir / "agent.json").write_text(json.dumps(rec, indent=2))` at line
    255'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: manifest_path
  how: '`manifest_path.write_text(json.dumps(manifest, indent=2))` at line 122'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: healer_log
  how: '`open(healer_log, "wb")` at line 235 (mode=''wb'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 255'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(manifest, indent=2)` at line 122'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 177'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ap_file
  how: '`ap_file.write_text(json.dumps(rec, indent=2))` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps(rec, indent=2)` at line 117'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: stdout
  how: 7 `print()` call(s) at line(s) [59, 81, 120, 124, 128, 142, 256]
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
goal:g7.16.1.7.1.2.1 (0706358c2): prime recovery drops rotate.DEFAULT_PROMPT_FILE -- every recovered post renders its row (prime: head + template + card + trajectory); prompt_file is always None here now. d52d4bfbb: director recovery renders with the seat tree card node as card_file.
10-07 goal:g7.16.1.5.3.2 (director-general-3; lanes DG2 d86be2c8da, test_heal_sweep_failed_read.py): the worktree sweep never reads a FAILED git read as clean. DEVIATION from the first build, which discarded git's return code (`status_lines, _ = _git(...)`): `git status --porcelain` rc != 0 -> `[sweep] refused <id>: git status failed (rc N)`, refused += 1, recorded in _SWEEP_SKIP (live pass only), continue; MERGED trees too, a failed read proves nothing. Never archived, never removed on a failed read: an OOM-killed child or a corrupt index on an UNMERGED tree gave dirty=[] and needs_archive=True, _sweep_archive pinned HEAD only and `worktree remove --force` dropped the uncommitted bytes. Same class at `rev-parse HEAD`: on a tree whose gitdir EXISTS, an empty head was NOT already safe (an empty head plus a failed status gave an empty `want` list in _sweep_archive, which returns None, read as archived, then the --force remove), so it is refused by name too (`git rev-parse HEAD failed (rc N)`, not worded orphan). R3 (SM mur, DG1 reproduction): a FAILED rev-parse is NO head whatever it printed, because on an UNBORN branch it prints the literal `HEAD` on stdout with rc 128, which the first cut took for a head (it read the return code only when stdout was empty) so the tree went into the archive path and was refused for the wrong reason (archive failed); now `head = head_lines[0] if head_lines and hd_rc == 0 else ""`, and an unborn HEAD is refused by name by the rev-parse line, never archived. R4 (SM's reviewer, DG1 reproduced in plain git 2.43): `git worktree list --porcelain` prints the NULL oid `HEAD 0000..0` for an UNBORN (--orphan) LISTED tree, and _sweep_worktree_heads cached it, so the cached head was non-empty, rev-parse never ran and the R3 guard never fired; the tree then reached _sweep_archive, where `git update-ref <ref> 0000..0` on an EXISTING ref (a reused agent id's refs/archive/worktrees/<name>) returns rc 0 and DELETES it. Ruled at the SOURCE: in _sweep_worktree_heads._flush an all-zero HEAD is NO head (`if head and set(head) == {"0"}: head = ""`), the only producer of cached heads, so rev-parse runs, hd_rc != 0, head stays empty and the R3 refusal fires by name; nothing reaches _sweep_archive. The DG2.C1 orphan branch (gitdir gone) is byte-for-byte as before and still runs first. The existing `_SWEEP_SKIP.pop(agent_id, None)` on the healthy path clears the record. _git itself is NOT widened. NOT touched, by design: :_code_files_clean and the root rev-parse in the watcher re-exec (best-effort, documented).
<!-- THOUGHT:END -->
