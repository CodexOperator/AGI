---
id: experiment:a00-95f48ef6-a6f8af
mint_id: c9c74a29edb44531bf4aeec1d9eb5198
type: experiment
parents:
  - hypothesis:verification-and-write-guard-join-the-choice-surface
next_edges: []
confidence: 0.9
edited_by: a00-eb351f20
evidence_runs:
  - experiment:a00-95f48ef6-a6f8af
loop: hypothesis:verification-and-write-guard-join-the-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": "both CLIs join _LISTED_CLIS; introspection sees real vocab", "class": "wire", "cmd": "import test_commands_manifest; _introspect_cli(verification.py) and _introspect_cli(write_guard.py) against the live CLIs; read len(_LISTED_CLIS)", "expected": "verification.py vocabulary {bare, window}; write_guard.py vocabulary {check, hook}; _LISTED_CLIS == 69", "observed": "{'': {...}, 'window': {...}} and {'hook': set(), 'check': set()}; _LISTED_CLIS = 69; declared==introspected for both", "result": "held"}
  - {"conjunct": "nothing that runs the suite / stamps / signs a ring / installs a hook is proposable", "class": "gate", "cmd": "commands.manifest(.agi) over all 220 entries; flag any proposable argv carrying --suite, --stamp, --ring-*, or write_guard.py + hook", "expected": "no flagged proposable entry", "observed": "empty bad set; verify-suite, verification.py:, verification.py:window, write_guard.py:hook all proposable:false", "result": "held"}
  - {"conjunct": "legacy write-guard/verify/verify-suite still resolve; propose imports and executes nothing", "class": "auth", "cmd": "commands.load(.agi) membership; commands.propose on verification.py:, verification.py:window, write_guard.py:hook, verify-suite, write-guard", "expected": "all three legacy names present; the four operator keys refuse by name with a reason; write-guard proposes the read-only check argv", "observed": "verify/verify-suite/write-guard present; 4 x CommandError with reason; propose(write-guard) = [python3, write_guard.py, check]", "result": "held"}
  - {"conjunct": "enumeration test red on pre-fix bytes, green after", "class": "gate", "cmd": "recompute test_every_engine_cli_is_listed_write_py_or_named_outside missed set, once with _LISTED_CLIS minus the two new names", "expected": "pre-fix missed == [verification.py, write_guard.py]; post-fix missed == []", "observed": "pre-fix exactly those two; post-fix []; _OUTSIDE_CLIS = {analyze-chat-structure.py, snapshot-build-site.py}", "result": "held"}
  - {"conjunct": "the change touches nothing else on the choice surface", "class": "wire", "cmd": "diff commands.manifest over the parent commit 102658116c node vs the live .agi node", "expected": "only verify-suite proposable True->False plus the 4 new keys; no unrelated field moves", "observed": "exactly that; 216 -> 220 entries; zero other same-key field changes", "result": "held"}
  - {"conjunct": "the three named test files green; manifest render deterministic", "class": "gate", "cmd": "env -u TMUX -u TMUX_PANE python3 -m pytest test_commands_manifest.py test_commands.py test_graphweb.py -q ; render_manifest twice", "expected": "232 passed 7 skipped; two renders byte-identical", "observed": "232 passed, 7 skipped in 156.79s; two renders identical (151828 bytes)", "result": "held"}
production_lines: 37
profile: balanced
role: kid
scaffold_hash: 7b7e87293fa8be43
season: 2
title: verification.py and write_guard.py join the choice surface; all 70 engine CLIs surveyed
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-95f48ef6-a6f8af

**Claim** (parent `hypothesis:verification-and-write-guard-join-the-choice-surface`):
`verification.py` and `write_guard.py` join the choice surface; every verb is a
`<cli>:<verb>` key in `command:commands` (declared or excluded with a reason);
nothing that runs the suite / stamps the baseline / signs a ring / installs a
hook is proposable; an enumeration test covers every engine CLI.

## What was built

```
surface   command:commands (DATA only -- nothing under extensions/agi/bin/)
          verification.py:        excluded  suite/stamp/ring flags, bare check
          verification.py:window  excluded  shares --suite-ring/--ring-sig
          verify-suite (legacy)   excluded  was proposable:true with --suite
          write_guard.py:check    proposable read
          write_guard.py:hook     excluded  installs a pre-commit hook
harness   extensions/agi/tests/test_commands_manifest.py
          _LISTED_CLIS += verification.py, write_guard.py        (67 -> 69)
          _PARSERLESS_CLIS += write_guard.py
          _declared_subcommands(): read a hand-rolled SUBCOMMANDS tuple
          _introspect_cli: optional `subcommand` positional -> bare "" verb
          _OUTSIDE_CLIS {analyze-chat-structure.py, snapshot-build-site.py}
          + enumeration, operator-flag, and legacy-name tests (below)
```

The survey is now: 71 `bin/*.py` with a `__main__` block = 69 listed (68 with a
parser + `write_guard.py`'s declared `SUBCOMMANDS`) + `write.py` (its own VERBS
drift test) + 2 named outside with a reason.

## Evidence

Red on the pre-fix bytes (the enumeration test ran before the two names were
added to `_LISTED_CLIS`):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q -k every_engine_cli_is_listed
E  AssertionError: engine CLIs with a `__main__` block and no entry in the choice
E  surface survey: ['verification.py', 'write_guard.py']
1 failed, 172 deselected
```

Green after the build (all three files the claim names):

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_commands_manifest.py \
    extensions/agi/tests/test_commands.py \
    extensions/agi/tests/test_graphweb.py -q
232 passed, 7 skipped in 86.06s
```

The live manifest, read from the node (never a copied list):

```
'verification.py:'        verb=''        proposable=False  side=read
'verification.py:window'  verb='window'  proposable=False  side=read
'verify-suite'            verb='--suite' proposable=False  side=read
'write_guard.py:check'    verb='check'   proposable=True   side=read
'write_guard.py:hook'     verb='hook'    proposable=False  side=graph-write
```

New committed assertions in `test_commands_manifest.py`:
`test_every_engine_cli_is_listed_write_py_or_named_outside` (red pre-fix),
`test_no_suite_stamp_ring_or_hook_verb_is_proposable` (catches the pre-fix
`verify-suite`), and
`test_legacy_verification_names_resolve_and_the_suite_is_refused` (the three
legacy names still resolve; `propose verify-suite` refuses with its reason).
`propose` still imports and executes no CLI (`test_propose_never_imports_a_cli_or_touches_argparse`),
and no existing assertion was relaxed -- the harness gained three shapes.

## Production lines

`git diff --numstat -- .agi/nodes/.geometry/commands.md` = **37 added, 0 removed**
(under the 40-line ceiling; the test file is excluded from the measure).

## Agent Notes
Built the choice-surface join: command:commands now excludes verification.py (bare + window) and verify-suite (--suite was proposable), excludes write_guard.py:hook, declares write_guard.py:check; _LISTED_CLIS 67->69 with the harness reading an optional subcommand positional and write_guard's SUBCOMMANDS; enumeration test red pre-fix (verification.py, write_guard.py), 232 passed post-fix across the three named test files; commands.md +37 production lines under the 40 ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review a00-eb351f20, EF.69. Read the diff 102658116c..24b2cb625d (commands.md +37, test_commands_manifest.py +135/-11) and the live bytes, never the kid result file. Six probes I ran myself, one per claim conjunct, all held.
WHAT THE INSTRUCTION SAID: nothing that runs the suite (--suite), stamps the baseline (--stamp), signs a ring (--ring-*) or installs a hook (write_guard.py hook) is proposable, and a committed test enumerates every bin/*.py with a __main__ block.
WHAT THE MACHINE DOES: commands.manifest() applies a node manifest: override inside its FIRST loop (commands.py:240-244, dec.get(name) fed to _entry), so the verify-suite entry flips to proposable:false; the rendered manifest diff over commit 102658116c is exactly that one flip (True->False) plus the four new keys verification.py:, verification.py:window, write_guard.py:check, write_guard.py:hook, 216->220, with zero other same-key field moves. Propose refuses all four operator keys by name; verification.py introspection reads {bare, window} off its optional subcommand positional and write_guard.py reads {check, hook} off its declared SUBCOMMANDS; _LISTED_CLIS = 69.
NEAR MISS: a manifest: entry whose name ALSO appears in commands: is consumed in loop 1; loop 2 skips names already in `out`. A reviewer reading only loop 2 would conclude the verify-suite override is dead and the suite is still proposable -- a false negative. The probe checks the live render, not the source order.
Enumeration test is red on the pre-fix set: with the two names removed from _LISTED_CLIS the missed set is exactly [verification.py, write_guard.py]; post-fix []. Three named test files green (232 passed, 7 skipped) and render_manifest is byte-identical twice. Accepted as proved.
<!-- THOUGHT:END -->

Parent a00-eb351f20 accepts: live manifest flips verify-suite pro->false and adds verification.py:/.window + write_guard.py:check/.hook; _LISTED_CLIS 67->69; enumeration test red pre-fix [{verification.py, write_guard.py}], green after; three named test files 232 passed/7 skipped. Six probes recorded in probes:.
