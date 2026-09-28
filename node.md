---
id: hypothesis:verification-and-write-guard-join-the-choice-surface
mint_id: 2868ed12de8a4303b4af8a64d43d93d7
type: hypothesis
parents:
  - goal:g1.25.5
next_edges: []
assigned: director-engine (leaf goal:g1.25.5, its first round; the jev notice waits on it)
ceiling: "1 kid, 10-12 production lines per conjunct, pi parent (scope, never spend: owner 09-23 14:xZ)"
edited_by: director-engine
scaffold_hash: f294afb3e8c04bef
season: 2
testable_claim: After the round, command:commands keys every verb of verification.py and write_guard.py as <cli>:<verb> (declared with typed args, placement, side_effects and proposable, or excluded by name with a reason) so nothing that runs the engine suite (--suite; today the legacy verify-suite entry is proposable true, side_effects read), stamps the baseline (--stamp), signs a ring (--ring-*) or installs a hook (write_guard.py hook) is proposable; both CLIs join _LISTED_CLIS with the introspection seeing each one's real vocabulary (verification.py's bare check beside its optional window; write_guard.py's declared SUBCOMMANDS), so the coverage test covers 69 CLIs and write.py's own VERBS drift test the 70th; a committed test enumerates every extensions/agi/bin/*.py with a __main__ block and asserts each is listed, is write.py, or sits in a named outside set with a reason (analyze-chat-structure.py, snapshot-build-site.py), red on the pre-fix bytes; the legacy write-guard/verify/verify-suite names still resolve and propose imports and executes nothing; test_commands_manifest.py, test_commands.py and test_graphweb.py green.
title: verification.py and write_guard.py join the choice surface -- no suite, stamp, ring or hook verb is proposable, and a test enumerates all 70 engine CLIs
town: local-maxxing
---
# hypothesis:verification-and-write-guard-join-the-choice-surface

# hypothesis:verification-and-write-guard-join-the-choice-surface

**Assigned: director-engine** (leaf goal:g1.25.5, its first round; the owner's cli-maxxing, goal:g1.25) · build loop · one `[merge-up]` to thought-master. The jev notice to director-thought ("[jev] choice surface complete") waits on this round.

## Measured (director-engine, 20:4xZ 09-23, post tip 6eea914744)
```
coverage       test_commands_manifest.py:269-314 _LISTED_CLIS = 67 (13+10+9+11+12+12); write.py rides its own VERBS drift test (:8)
the 70         bin/*.py with a __main__ block = 71 -> NOT listed: verification.py · write_guard.py · write.py (its own drift test) ·
               analyze-chat-structure.py · snapshot-build-site.py (outside the survey, named nowhere)
legacy         commands.md:91 `write-guard` · :105 `verify` · :111 `verify-suite` are NAME-keyed (commands.py:241-243), never <cli>:<verb>
the defect     `commands.py manifest`: verify-suite = cli verification.py, verb "--suite", side_effects read, proposable TRUE --
               a proposer can offer the whole engine suite, which runs under the one-runner suite lock
introspection  verification.py:1748 positional `subcommand` nargs="?" choices=["window"] -> _introspect_cli
               (test_commands_manifest.py:441-446) keys only `window`, never the bare check · write_guard.py:384
               SUBCOMMANDS = ("check", "hook"), a hand-rolled dispatcher (:387-406) -> the parserless path returns only {"": set()} (:413-414)
mur            R-EF54 verify: "all 70 not established" -- refuted: false, a residue; the EF.54 parent says so (a00-55989f04-dd8011.md:79)
```

## CLAIM
After the round, command:commands keys every verb of verification.py and write_guard.py as `<cli>:<verb>` -- declared (typed args, placement, side_effects, proposable) or excluded by name with a reason -- so nothing that runs the engine suite (`--suite`; today the legacy `verify-suite` entry: proposable true, side_effects read), stamps the baseline (`--stamp`), signs a ring (`--ring-*`) or installs a hook (`write_guard.py hook`) is proposable. Both CLIs join `_LISTED_CLIS` with the introspection seeing each one's real vocabulary (verification.py's bare check beside its optional `window`; write_guard.py's declared `SUBCOMMANDS`), so the coverage test covers 69 CLIs and write.py's own VERBS drift test the 70th. A committed test enumerates every `extensions/agi/bin/*.py` with a `__main__` block and asserts each is listed, is write.py, or sits in a named outside set with a reason (analyze-chat-structure.py, snapshot-build-site.py) -- red on the pre-fix bytes. The legacy `write-guard` / `verify` / `verify-suite` names still resolve; propose still imports and executes nothing.

## Dispatch line
config-max: every verb of both CLIs is a `<cli>:<verb>` cell in command:commands, declared or excluded with a reason / template-max: none -- the `about` lines stay the node's / code: none in bin/ -- the test harness learns an optional positional and a declared SUBCOMMANDS tuple

## FALSIFIERS
- a verb of verification.py or write_guard.py that the introspection sees but command:commands neither declares nor excludes
- any manifest entry whose argv carries `--suite`, `--stamp`, a `--ring-*` flag or `write_guard.py hook` with proposable: true
- a bin/*.py with a `__main__` block that is neither listed, write.py, nor in the named outside set -- or the enumeration test green on the pre-fix bytes
- `commands.py propose` importing or running a CLI; a legacy `write-guard` / `verify` / `verify-suite` name that no longer resolves
- an existing assertion relaxed to make room (extend the harness, never weaken it)

## TESTS
test_commands_manifest.py (coverage, drift, the new enumeration, propose) · test_commands.py · test_graphweb.py -- those files only, under `env -u TMUX -u TMUX_PANE`

## FILE SCOPE
.agi/nodes/.geometry/commands.md (command:commands -- pass `--owns command:commands` to `cli.py done`) · extensions/agi/tests/test_commands_manifest.py · extensions/agi/tests/test_commands.py -- nothing under extensions/agi/bin/

## CEILING
1 kid · 10-12 production lines per conjunct · pi parent · scope, never spend (owner 09-23 14:xZ)
