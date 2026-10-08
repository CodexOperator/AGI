---
build_kind: code
confidence: 1.0
id: "build:tests-test-season"
mint_id: e84b2e52eae547d49b4b1dde52efbcd7
origin: build-scan
parents:
  - mvp:tests
payload_ref: extensions/agi/tests/test_season.py
tags:
  - build
  - code
  - g2.1
title: "Build: extensions/agi/tests/test_season.py"
type: build
---

`extensions/agi/tests/test_season.py` — level-3 code node (one file, one canonical node).

Census parent: `mvp:tests`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/tests/test_season.py
parse_ok: true
inputs:
- name: __future__.annotations
  how: '`from __future__ import annotations` at line 5'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json
  how: '`import json` at line 7'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: os
  how: '`import os` at line 8'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: shutil
  how: '`import shutil` at line 9'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: subprocess
  how: '`import subprocess` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: sys
  how: '`import sys` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pathlib.Path
  how: '`from pathlib import Path` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: pytest
  how: '`import pytest` at line 14'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: o2
  how: '`o2.read_text()` at line 822'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: faith
  how: '`faith.read_text()` at line 868'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs:
- name: engine_on_path
  how: 'defines public function `engine_on_path` at line 27, signature: (monkeypatch)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: season_py
  how: defines public function `season_py` at line 34
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: temp_graph
  how: 'defines public function `temp_graph` at line 40, signature: (tmp_path, engine_on_path)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestStatus
  how: defines public class `TestStatus` at line 192
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestRollover
  how: defines public class `TestRollover` at line 241
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestJudge
  how: defines public class `TestJudge` at line 294
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestJudgeQuorum
  how: defines public class `TestJudgeQuorum` at line 421
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestRolloverGenesis
  how: defines public class `TestRolloverGenesis` at line 555
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestRetag
  how: defines public class `TestRetag` at line 767
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestErrorHandling
  how: defines public class `TestErrorHandling` at line 911
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _git
  how: 'defines private function `_git` at line 946, signature: (tmp, *args)'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _init_project
  how: 'defines private function `_init_project` at line 951, signature: (tmp_path,
    season=''season/s1'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: _commit
  how: 'defines private function `_commit` at line 962, signature: (tmp, msg, filename=''file.txt'',
    content=''x\n'')'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: TestMergeUp
  how: defines public class `TestMergeUp` at line 969
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: ladder_dir / "ladder.md"
  how: '`(ladder_dir / "ladder.md").write_text(ladder)` at line 85'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: cfg
  how: '`cfg.write_text(''{"project": "test"}'')` at line 91'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goals_dir / "sub1.md"
  how: '`(goals_dir / "sub1.md").write_text(subgoal)` at line 108'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goals_dir / "short1.md"
  how: '`(goals_dir / "short1.md").write_text(short)` at line 120'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: goals_dir / "lt1.md"
  how: '`(goals_dir / "lt1.md").write_text(lt)` at line 132'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outcomes_dir / "o1.md"
  how: '`(outcomes_dir / "o1.md").write_text(outcome)` at line 145'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: outcomes_dir / "o2.md"
  how: '`(outcomes_dir / "o2.md").write_text(outcome2)` at line 156'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: visions_dir / "v1.md"
  how: '`(visions_dir / "v1.md").write_text(vision)` at line 169'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: morals_dir / "faith.md"
  how: '`(morals_dir / "faith.md").write_text(moral)` at line 182'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: tmp / filename
  how: '`(tmp / filename).write_text(content)` at line 963'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: visions_dir / "v2.md"
  how: '`(visions_dir / "v2.md").write_text(vision_with_parent)` at line 327'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: overviews_dir / "test1.md"
  how: '`(overviews_dir / "test1.md").write_text(overview)` at line 341'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: visions_dir / "v3.md"
  how: '`(visions_dir / "v3.md").write_text(vision_v3)` at line 380'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: overviews_dir / "test2.md"
  how: '`(overviews_dir / "test2.md").write_text(overview)` at line 396'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: fp
  how: '`fp.write_text( f"# {title}\n\nOwner text, 2026-09-06, verbatim.\n\n" "\"the
    graph invites completion.\"\n\n" "## Owner''s gloss\n\n\"the ladder running itself.\"\n")`
    at line 562'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: overviews / f"{oid.split(':')[-1]}.md"
  how: '`(overviews / f"{oid.split('':'')[-1]}.md").write_text( f"---\nid: {oid}\ntype:
    overview\nparents: [bigger_outcome:bo]\n" f"season: {season}\n{judged_line}\n---\n#
    {oid}\n")` at line 573'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: o2
  how: '`o2.write_text(text)` at line 823'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: faith
  how: '`faith.write_text(text)` at line 870'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: dep / "ancient.md"
  how: '`(dep / "ancient.md").write_text(old)` at line 897'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: git_shim
  how: '`git_shim.write_text( "#!/bin/sh\n" f"REAL={real_git}\n" ''case \"$*\" in\n''
    "*''--no-edit''*)\n" "    \"$REAL\" \"$@\"   # do the real commit; merge completes\n"
    "    if [ \"$?\" -eq 0 ]; then exit 8; fi   # then lie about it\n" "    ;;\n"
    "es...[truncated, 268 chars total]` at line 1086'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: record
  how: '`record.write_text(json.dumps({ "branch": "loop/parent-aaaa@s2", "base_branch":
    "tier1/director", "worktree": str(worktree), "suite": "exit 0", }))` at line 1160'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: json.dumps
  how: '`json.dumps({ "branch": "loop/parent-aaaa@s2", "base_branch": "tier1/director",
    "worktree": str(worktree), "suite": "exit 0", })` at line 1160'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.
