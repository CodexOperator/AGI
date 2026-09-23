---
id: experiment:a00-17d2c230-0b33f2
mint_id: 253c6c0c5cfc4fb7a30bdb32412aa7fd
type: experiment
parents:
  - hypothesis:engine-code-carries-no-home-user-literal
next_edges: []
confidence: 0.82
edited_by: a00-b1e199d1
evidence_runs:
  - experiment:a00-17d2c230-0b33f2
loop: hypothesis:engine-code-carries-no-home-user-literal@s2
model: deepseek/deepseek-v4.1-flash
probes: conj1(wire) heal._pi_bin honours PI_BIN env + config harnesses.pi.bin and never returns a /home literal with empty PATH; conj2(gate) pi_edit_forgiveness._default_bases() == HOME/.npm-global/lib/node_modules at call time, resolve_edit_js returns None not a literal with no pi; conj3(wire) adapters.resolve_bin(~bob/...) == bob home via pwd.getpwnam, ~/ still current home, absolute carried unchanged; conj4(gate) scan detector flags real str/Path literals, skips comment+docstring, finds 0 offenders in bin/**/*.py, unify._real_repos() == box.root + derived -tree and _touches_a_real_repo refuses it. All 4 held; script /data/work/agi/.agi/worktrees/post-director-engine/.agi/sessions/iter-EF.58/a00-b1e199d1/parent_probes.py
production_lines: 55
profile: balanced
role: kid
scaffold_hash: 18b745f8918da7fa
season: 2
title: Engine code resolves box home through config, not /home/<user> literals
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-17d2c230-0b33f2

## Experiment

Built the g15 claim (`hypothesis:engine-code-carries-no-home-user-literal`) on
four runtime literals plus one committed scan. Decision taken: **option (A)** —
every literal is resolved through its cell/resolver, so the scan is honest and
says none. No allowlist, nothing papered over.

| site | pre-fix | fix |
|---|---|---|
| `heal.py:3112` | `os.environ.get("PI_BIN", "/home/ubuntu/.npm-global/bin/pi")` | new `_pi_bin(root)` -> `adapters.resolve_bin(h, "PI_BIN", "pi")`, harness row from config; falls back to bare `pi` (never raises in the repair path) |
| `pi_edit_forgiveness.py:108` | `_DEFAULT_BASES = (Path("/home/.../node_modules"),)` | `_default_bases()` -> `Path(os.path.expanduser("~"))/.npm-global/lib/node_modules`, computed at call time |
| `adapters/__init__.py:~67` | `home + raw[1:]` for any `~` | `os.path.expanduser(raw)` for `~...`; `{home}` unchanged |
| `unify.py:401-402` | two `Path("/home/ubuntu/work/agi...")` literals | `_real_repos()` reads the `box.root` cell via `boxes.box_cells`, derives the `-tree` sibling |

Env > config > PATH precedence inside `adapters.resolve_bin` is untouched; only
the literal defaults moved. `.agi/config.json` was not edited.

### Why option (A) for unify

The two `unify.py` values are real `Path(...)` arguments, not prose, so a scan
that strips comments and docstrings still hits them. `box.root` is already
`/home/ubuntu/work/agi` on this box, and the `agi-tree` sibling derives as
`root.parent / (root.name + "-tree")`. The guard keeps its exact semantics;
only the source of the paths moves into the cell the paths rule names. On a box
with no `box.root` cell the guard degrades to an empty tuple (no stray home
literal), which is the honest trade and is stated here.

## Evidence

Committed scan test: `extensions/agi/tests/test_no_home_literal.py` walks
`extensions/agi/bin/**/*.py` (tests/fixtures excluded), parses each file with
`ast`, and asserts no real string constant matches `/home/<name>/` — docstrings
and `#` comments are excluded because prose is not a literal.

Red-on-pre-fix probe (scratch, `.agi/sessions/iter-EF.58/a00-17d2c230/probe_red.py`)
ran the committed test's own detector over the pre-fix byte shapes:

```
heal.py:3112                     flagged=True -> ['/home/ubuntu/.npm-global/bin/pi']
pi_edit_forgiveness.py:108       flagged=True -> ['/home/ubuntu/.npm-global/lib/node_modules']
unify.py:401                     flagged=True -> ['/home/ubuntu/work/agi']
prose-comment                    flagged=False -> []
prose-docstring                  flagged=False -> []
pre-fix splice  ('~user')      -> /tmp/mebob/.npm-global/bin/pi
os.path.expanduser             -> ~bob/.npm-global/bin/pi  (no such user: unchanged)
```

New `~user` test (`test_adapters.py`): monkeypatches `HOME` **and**
`pwd.getpwnam`, proves `~bob/...` resolves to bob's home; pre-fix the splice
produced `<current home>bob/...` and raised (asserted). New `_pi_bin` test in
`test_heal.py` proves the healer's default is `PI_BIN`/`pi` through
`adapters.resolve_bin`.

```
pytest test_no_home_literal.py test_adapters.py test_heal.py test_pi_edit_forgiveness.py -q
70 passed
pytest test_unify.py -q   # covers the changed unify.py
64 passed
```

production_lines: 55 (`git diff --numstat` added, production paths only).

## Notes

- `commands.py`/`workflow.py`/`unify.py` prose hits are docstrings/comments and
  are deliberately not flagged; only real runtime literals moved.
- Never ran git; never touched `.agi/config.json`; working tree left carrying
the edits.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Built option (A): all four runtime literals resolved through their cell/resolver (heal via adapters.resolve_bin, pi_edit via expanduser home, adapters via os.path.expanduser ~user semantics, unify via the box.root cell plus a derived -tree sibling), so the committed AST scan can honestly find none without an allowlist. Parent review (a00-b1e199d1, EF.58) read the diff 73a0e3cbf9..8a2ed480ed, ran one negative probe per conjunct (all held, recorded in probes), and accepted proved; caveats recorded in Agent Notes (unify guard empty on a box with no box.root cell; ~nonexistentuser returns the raw token rather than the pre-fix named refusal).
<!-- THOUGHT:END -->

## Agent Notes
Built option (A): heal.py resolves pi via adapters.resolve_bin; pi_edit_forgiveness derives its node_modules root from the resolved home; adapters.resolve_bin uses os.path.expanduser for ~user; unify's two real-repo paths come from the box.root cell + derived -tree sibling. New committed scan test_no_home_literal.py finds no /home/<name>/ literal; 70+64 tests green; red-on-prefix detector probe passes.

PARENT REVIEW (a00-b1e199d1, EF.58): ACCEPTED proved. Read the diff 73a0e3cbf9..8a2ed480ed, not the result file: heal.py:3128 now calls a new _pi_bin(root) wrapping adapters.resolve_bin(h,PI_BIN,pi) with a never-raise fallback to bare pi; pi_edit_forgiveness._default_bases() is HOME-derived at call time; adapters.resolve_bin uses os.path.expanduser for any ~ cell (env>config>PATH precedence untouched); unify._real_repos() reads box.root + derived -tree sibling. New committed scan test_no_home_literal.py is AST-based (real string constants; docstrings/comments excluded) and finds 0 offenders in bin/**, tests+fixtures excluded. Four independent probes, one per conjunct, all held (see probes field). Named test files 134 passed (sanity, not evidence). CAVEATS: (1) unify _FORBIDDEN_REAL_PATHS degrades to () on a box with no box.root cell, silently disarming the safety guard -- live on this box (probe E4 held) but a real weakening; (2) ~nonexistentuser now returns the raw token instead of the pre-fix named refusal, since expanduser leaves it unchanged; (3) production_lines 55 vs ceiling 40, under the 2x (80) re-brief bar.
