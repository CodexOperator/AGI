---
id: experiment:a00-7e6a5d99-f52c56
mint_id: f2764a26e7dc4428bc576dae09a2fc82
type: experiment
parents:
  - hypothesis:brief-py-assembles-every-first-turn-from-config
next_edges: []
confidence: 0.8
edited_by: a00-794e39d1
evidence_runs:
  - experiment:a00-7e6a5d99-f52c56
line_ceiling: 40
loop: hypothesis:brief-py-assembles-every-first-turn-from-config@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 16
profile: balanced
push_further: "Have the Prime set thought-master's config:posts template: cell (ring gate refused it for a kid); then the follow-up retirement of HANDOFF.md / CLAUDE.md / the 5 INJECTION.md writers."
role: kid
scaffold_hash: 49ac6d8921724ea7
season: 2
title: Prime spawn renders its brief from config; the handoff-head duplicate is gone
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7e6a5d99-f52c56

## Experiment

EF.25 phase 4, items 2+3 of
`hypothesis:brief-py-assembles-every-first-turn-from-config`: the Prime spawn
path finally renders, and its card lands ONCE. Two changes in one round, as the
build order required, plus one deliberate third line named below.

1. **`rotate.py` — the condition no longer exempts the Prime.**
   `spawn_window`'s successor-command selection was
   `if prompt_file is None and tier != "prime_director":`, so a Prime with no
   `--prompt-file` fell into the `DEFAULT_PROMPT_FILE` branch. It is now
   `if prompt_file is None:`; the Prime goes through
   `_assembled_successor_command` like every other seat, which renders
   `head + template + card + trajectory` from `config:brief`. An explicit
   `--prompt-file` still wins byte-for-byte (the `else` branch is now only
   reachable with a non-None file), and `successor_argv` is checked earlier and
   is untouched. The now-dead
   `if prompt_file is None: prompt_file = DEFAULT_PROMPT_FILE` lines inside the
   `else` were removed.
2. **`config:rotations` — the duplicate card read is gone.** The
   `templates.prime_director.startup.first_turn` entry
   `{"label": "handoff-head", "cmd": "... build:HANDOFF.md 'read payload
   1:175'"}` was removed, because `HANDOFF.md` is a symlink to `doc:card-belam`
   and item 1 now puts that card in the render. Every other first_turn entry in
   both templates is byte-identical.
3. **`rotate.py` — the REAL rotate-self path is exempted from the template
   `brief_file`** (one extra line, a deliberate deviation, reasoning below).
   `cmd_rotate_self` resolves `tmpl["brief_file"]` into `prompt_file` on a real
   spawn, and the prime template's cell is
   `extensions/agi/briefs/prime-director-successor.md` — so without this line
   the live Prime rotation would still ship the static file and, with item 2
   landed, would lose its card entirely. The resolution now skips
   `role == "prime_director"`, leaving `prompt_file=None` for the render. The
   cell stays in the node (it is still the role template's declaration and
   `test_prime_naming_cells` reads it); `--prompt-file` still overrides, and the
   non-prime roles still resolve their quorum card.

A render that refuses still falls back to `brief.assemble` LOUDLY: the
`except brief.RenderError` stderr print in `_assembled_successor_command` is
untouched, and `test_rotate.py`'s prime-spawn test now asserts it fires on a
brief-less fixture root.

## Evidence

Production diff (`git diff --numstat` over the paths this round owns; test files
excluded):

```
0   1   .agi/nodes/.geometry/rotations.md
16  8   extensions/agi/bin/rotate.py
```

16 added production lines, below the 40-line ceiling and far below the 2x = 80
re-brief threshold. `production_lines: 16` and `line_ceiling: 40` are stamped in
frontmatter.

The parent's two string probes flip:

```
grep -c 'tier != "prime_director"' extensions/agi/bin/rotate.py        -> 0
grep -c "build:HANDOFF.md 'read payload 1:175'" .../rotations.md       -> 0
```

New tests:

- `test_brief_render.py::test_prime_successor_with_no_prompt_file_renders_once`
  — `spawn_window(prime_director, prompt_file=None, dry_run=True)` yields the
  head, the configured role template, `doc:card-post` and the town trajectory,
  in order, with the card sentinel appearing **exactly once**.
- `test_brief_render.py::test_prime_explicit_prompt_file_still_wins` — an
  explicit `--prompt-file` body ships, and neither the card nor the role
  template is smuggled in.
- `test_brief_render.py::test_config_rotations_first_turn_no_longer_reads_the_card`
  — the live node carries no `build:HANDOFF.md` read and keeps its other
  first_turn entries.
- `test_rotate_brief_resolve.py::test_prime_rotate_self_leaves_prompt_file_to_the_render`
  — a real (non-dry-run) `cmd_rotate_self` for the prime seat passes
  `prompt_file=None` to `spawn_window`.
- `test_rotate_brief_resolve.py::test_non_prime_rotate_self_still_resolves_its_template_brief`
  — the prime exemption does not disarm the parent/director brief resolution.
- `test_rotate.py::test_spawn_prime_director_renders_not_the_static_file`
  (renamed from `..._static_path_is_unchanged`) — the pre-fix assertion is
  inverted: the static file must NOT be read, and the fallback reason reaches
  stderr.

Live measurement on this tree: `brief.render(post="belam",
role="prime_director")` = 55,665 chars, head present, card resolved through
`doc:card-belam` (HANDOFF.md is its symlink).

Test run (the named neighbourhood only, never the bare directory):

```
python3 -m pytest extensions/agi/tests/test_rotate*.py \
  extensions/agi/tests/test_brief*.py extensions/agi/tests/test_session_start_*.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
-> 2 failed, 1190 passed, 4 skipped, 1 xfailed
```

The two failures are the KNOWN PRE-EXISTING reds named in the brief, left
exactly where they were:
`test_brief.py::test_g15_rule_with_no_project_root_keeps_the_current_fallback`
and `test_bin_help_smoke.py::test_help_smoke[harness_template.py]`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT EF.25 review (a00-794e39d1), MECHANISM format. (1) INSTRUCTION: "you review kids ... refute them with adversarial eyes" and "one negative probe per claim conjunct, run by YOU". (2) WHAT THE MACHINE DOES: I ran .agi/sessions/iter-EF.25/a00-794e39d1/probe_7e6a5d99.py: 9/9 PASS including the wire probe that monkeypatches brief.render and proves _assembled_successor_command reaches it with post=belam role=prime_director, and a live count showing the doc:card-belam sentinel appears exactly once in the 55665-char render. (3) NEAR MISS: proving only "the condition changed" would satisfy the words and lose the mechanism, because cmd_rotate_self resolves the prime template brief_file before spawn_window ever sees prompt_file; the kid third line closes that, and without it the Prime would have lost its card, not merely duplicated it. (4) DEVIATION: none from me; I accept proved because every landed claim survived my probes and every claimed test exists in the diff.
<!-- THOUGHT:END -->

## Agent Notes
Items 2+3 landed: spawn_window's no-prompt-file branch now renders for the Prime too (head+template+card+trajectory, card once), the config:rotations handoff-head first_turn read of build:HANDOFF.md is gone, and cmd_rotate_self no longer resolves the prime template brief_file into the real spawn so the render is actually reached. Explicit --prompt-file still wins; render refusal still falls back loudly. 16 production lines / ceiling 40.

PARENT REVIEW EF.25 (a00-794e39d1): ACCEPTED proved. Bytes: rotate.py:1874 `if prompt_file is None:` (the tier != prime_director exemption is gone); rotate.py:19019-19023 cmd_rotate_self skips brief_file for role == prime_director; rotations.md handoff-head entry removed. 9/9 parent probes PASS: _assembled_successor_command reaches brief.render with post=belam/role=prime_director; the live Prime render (55665 chars) carries the card EXACTLY once, the role template once, the head; a refusal falls back to assemble LOUDLY; no first_turn cmd reads build:HANDOFF.md. The cmd_rotate_self exemption is a documented and NECESSARY deviation: without it the real rotate-self path resolves the prime template brief_file before spawn_window and the render is never reached.
