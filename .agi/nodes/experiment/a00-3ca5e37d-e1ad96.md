---
id: experiment:a00-3ca5e37d-e1ad96
mint_id: a2dd1ef658714104b2031c5d035929fb
type: experiment
parents:
  - hypothesis:brief-py-assembles-every-first-turn-from-config
next_edges: []
confidence: 0.75
edited_by: a00-426b02c5
evidence_runs:
  - experiment:a00-3ca5e37d-e1ad96
line_ceiling: 160
loop: hypothesis:brief-py-assembles-every-first-turn-from-config@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "tmp root with .agi/nodes/.geometry/brief.md and config.json={} ; brief._brief_cell(tmp)", "expected": "the ONE config cell resolves from the committed node with no config.json cell", "observed": "parts resolved {kid:[head,card,extras],...} ; git diff carries .agi/nodes/.geometry/brief.md ; no config cell in config.json needed", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "brief.py head --tier director | md5sum vs brief.render_head() md5sum ; brief.py render --role <5 roles> | md5sum", "expected": "one head, byte identical for the hook and every role", "observed": "both b051679b552f7b539098b7c216e69600 ; render --role identical across kid/parent/director/prime_director/master", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "rotate._assembled_successor_command(name=director-thought,tier=director,...) argv", "expected": "a rotated director successor first turn is head + card from the same render", "observed": "argv contains --HEAD-- and the director-thought card ; legacy assemble role brief (Hold the lens) is NOT present", "result": "pass"}
  - {"conjunct": 6, "class": "gate", "cmd": "git status --porcelain around brief.render(...)", "expected": "a render creates or modifies no file", "observed": "no new file from render ; only the pre-existing uncommitted config.json stays dirty", "result": "pass"}
  - {"conjunct": 7, "class": "wire", "cmd": "grep -n brief.assemble rotate.py dispatch.py ; grep -n brief.py head hooks/cc-session-start.sh", "expected": "all three call sites call the same render", "observed": "rotate.py now calls brief.render ; hook cc-session-start.sh:267 calls brief.py head which now delegates to render_head ; dispatch.py / the harness adapters STILL call brief.assemble (phase 3, disclosed)", "result": "fail"}
production_lines: 54
profile: balanced
role: kid
scaffold_hash: fad68668c57178ae
season: 2
title: brief.py render reads its one brief cell from a committable config:brief node, and rotate.py + the SessionStart hook share render's one unified head
town: local-maxxing
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-3ca5e37d-e1ad96

## Experiment

Phase 2 of `hypothesis:brief-py-assembles-every-first-turn-from-config` (the
second kid), on top of the phase-1 render.

**Gap fixed — the cell is now committable.** Phase 1 put the one `brief` cell
in `.agi/config.json`, which a round's own `done` commit refuses
(`cli.py:_round_scope_ok`, cli.py:2094), so the landed branch carried no cell
and `brief.py render` raised on a fresh checkout. The cell now lives in a new
`config:brief` node (`.agi/nodes/.geometry/brief.md`), named in `--owns`, and
`_brief_cell` reads it NODE-FIRST with `.agi/config.json` as the fallback. A
render driven only by the node works with no `brief` key in config.json.

**Phase 2 — two call sites share ONE render.**

- `rotate.py::_assembled_successor_command` (non-prime seats) now builds the
  successor's first turn from `brief.render(post=name, harness=...)`: head +
  card + the harness block. When a post has no row or no card (an advisor with
  none yet) render refuses and the seat falls back to the legacy
  `brief.assemble` body — a missing card must not make a rotation impossible.
- `brief.successor_prompt` (the Prime and any `--prompt-file` successor) and
  `brief._cmd_head` (the SessionStart hook, `cc-session-start.sh:267`) both read
  the new `brief.render_head()` = `render`'s `head` part = the HEAD region of
  `doc:unified-head`. The hook and a rotated successor are now byte-identical
  at one SHA, by construction, not by a second copy.

Consequence, deliberate and disclosed: the injected head is the unified head
(the owner's 09-23 "same across any role"), so the director-tier MORAL region
no longer rides it (it still reaches the legacy `assemble()` brief, and belongs
to the card under the 3-doc model). The tests that encoded the old
`─── CONSTITUTION HEAD ───` on the hook/successor path were updated; `assemble`
still emits it and every assemble test still passes.

NOT this round: `extensions/agi/bin/dispatch.py` (phase 3, a separate kid) and
retiring HANDOFF.md / CLAUDE.md / the 5 INJECTION.md writers.

## Evidence

```
$ python3 extensions/agi/bin/brief.py head --tier director | head -1
─── HEAD ───
$ python3 -c "import brief; h=brief.render_head(); p=brief.successor_prompt(tier='director', body='CARD'); print(p[:p.index('CARD')].strip()==h)"
True
```

`_brief_cell` resolves the node, and `done --owns config:brief` commits it:
```
find_node_file(.agi, 'config:brief') -> .agi/nodes/.geometry/brief.md
own_paths: {'.agi/nodes/experiment/a00-3ca5e37d-e1ad96.md', '.agi/nodes/.geometry/brief.md'}
.agi/nodes/.geometry/brief.md -> _round_scope_ok True
```

Named neighbourhoods, run as files (kid-tier gate):
```
test_brief_render.py                                    10 passed  (7 phase-1 + 3 new phase-2 falsifiers)
test_brief.py                                    150 passed, 1 failed (PRE-EXISTING: test_g15_rule_with_no_project_root... geometry renumber)
test_rotate.py                                   328 passed
test_rotate_brief_resolve.py + 14 test_rotate_*.py  428 passed, 1 xfailed
test_session_start_bootstrap.py + seat_pre_spawn.py  7 passed
test_session_start_seat_pre_spawn.py                7 passed
test_briefing.py + test_rotate_brief_resolve.py     15 passed
test_dispatch_dry_run.py + test_claude_code_adapter.py  70 passed
test_bin_help_smoke.py                            71 passed, 4 skipped, 1 failed (PRE-EXISTING: harness_template.py has no main())
test_prime_naming_cells.py                          12 passed
```

New falsifiers pinned in `test_brief_render.py`: the committed cell node
drives a render with no config.json cell (the gap); a rotated director
successor is `head + card` and a Prime fixture is `head + card`; the hook head
equals `render_head()` equals a successor's prefix at one SHA.

Production lines: `git diff --numstat` over brief.py (35+/6-) and rotate.py
(19+/10-) = **54 added**, under the 80 2x threshold. The `config:brief` node is
graph content (untracked in the diff), not code.

## Agent Notes
Phase 2 landed: the one brief cell moved to a committable config:brief node (read node-first, config.json fallback) so the landed diff carries it; rotate.py's non-prime successor path and successor_prompt now build head+card from the SAME brief.render head as the SessionStart hook; dispatch.py remains phase 3.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-426b02c5, EF.18). Phase 2 CLOSES the gap that demoted kid 1 and passes my own probes, read from the diff: the ONE brief cell now lives in a COMMITTABLE config:brief node named in --owns, resolves NODE-FIRST with config.json as fallback, and a tmp root with the node and config.json={} resolves the parts (my gate probe); brief.py head --tier director, render_head() and the five role renders are ONE md5 (b051679b552f7b539098b7c216e69600); rotate._assembled_successor_command for director-thought returns head + the card; a render writes no file. I did NOT re-run its suite as evidence. ACCEPTED with residue at lean_proved:75, not the kid own 85, on two named grounds: conjunct 7 is 2/3 -- dispatch.py and the harness adapters still call brief.assemble, so the claim one-pattern-for-every-role is not yet true for parents and kids (disclosed by the kid); and a real transitional hazard the kid notes but does not pin in a test: a rotated successor now gets head + card ONLY, so the legacy assemble role brief (the director blueprint) leaves the first turn, while no card yet carries a {{template:doc:<role-brief>}} line to replace it (grep finds 0 template lines in .agi/sessions/quorum/*.md). That is by the claim design (head+card) but it is a live change to every rotation and belongs in the next round. Also noted from the bytes, not a probe: rotate catches only RenderError around brief.render while _part(head) can raise FaithRefError (brief.py render_head catches both; rotate does not), so a missing moral:faith breaks a rotation instead of falling back.
<!-- THOUGHT:END -->

Phase 2 accepted-with-residue: the config cell is committable and node-first (gap closed), rotate.py + the SessionStart hook share render_head (one md5), a render writes no file; leans 75 not 85 because dispatch.py/adapters still call assemble (conjunct 7 is 2/3) and a rotated successor now loses the legacy role brief with no card template to replace it. Phase 3 = dispatch.py. Automatic done by the loop.
