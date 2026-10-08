---
id: experiment:a00-c02d5b4f-ae8fb0
mint_id: e19594fc5c3c45aabadaa6a81a3858c4
type: experiment
parents:
  - hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
next_edges: []
confidence: 0.85
edited_by: a00-c8389b84
evidence_runs:
  - experiment:a00-c02d5b4f-ae8fb0
loop: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards@s2
model: stealth/space-bunny-alpha
production_lines: 104
profile: balanced
rebrief_answer: "cut — the harvest measures ADDED production lines out of the kid s own done commit (extensions/agi/bin/cli.py:702-732: git show --numstat on the `<id> done:` commit, paths containing \"tests\" dropped, .py suffixes only), NOT the net and NOT the node self-report. For a00-c02d5b4f that measurement is 94 (75 in suite_guards.py + 19 in extensions/agi/conftest.py), so it IS over 2x the 40 ceiling and the disclosure was correct. No further lines are authorised: the residue is built, probed and green, so cut. 94/40, cut."
rebrief_request: "nothing remains -- the change is built and green; the only open question is the METRIC reading: git diff --numstat over the production paths is +104/-102 (net +2) against a 40-line ceiling, so 104 exceeds 2x if production_lines means ADDED lines and does not if it means net. Please confirm which reading the harvest uses for a refactor that deletes one of two copies; I trimmed the docstrings once already (122 -> 104 added) and will not gut the recorded why to chase the other reading."
role: kid
scaffold_hash: a8a8c919235c400d
season: 2
title: the two duplicate suite guards become one body with a caller-supplied policy (root resolver, extra env keys)
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c02d5b4f-ae8fb0

## What I built

Both bodies kid 1 (experiment:a00-008f4f72-2972ed) named as residue are now
ONE implementation in `suite_guards` with the difference passed as an
ARGUMENT. No behaviour change for either suite.

```
guard            one body (suite_guards)          policy, at the call site
---------------- ------------------------------  --------------------------------
suite window     make_suite_lock_fixture(         engine  -> find_project_root(
                   root_resolver)                   Path(__file__).resolve())
                                                    declared -> graph_root()
                                                    (VERIFY_GRAPH_ROOT else cwd)
env strip        make_agi_env_stripped_fixture(   engine  -> GIT_CONFIG_SPAWN_VARS
                   extra_keys) + strip_/           declared -> () no extra keys
                   restore_dispatch_env
```

Files: `extensions/agi/bin/suite_guards.py` (the two factories + the two plain
functions they wrap, +75/-37), `extensions/agi/conftest.py` (+19/-20),
`extensions/agi/tests/conftest.py` (+10/-45 — the 45 removed lines are the
duplicate lock body, replaced by one `make_suite_lock_fixture(...)` call).
`.agi/context/conftest.py` is UNCHANGED: it still imports the default
`suite_lock` / `agi_env_stripped` names, which are now
`make_*_fixture(policy)` instantiations, so the declared suite keeps both its
weaker strip and its cwd-resolved root without a line of change.

## Which policy is stronger, and why the default is the weaker one

The engine conftest's strip is STRICTLY STRONGER than `suite_guards`' on
exactly one axis: it also removes `GIT_CONFIG_COUNT` / `_KEY_0` / `_VALUE_0`,
the dispatcher's `core.hooksPath` channel. Measured: `core.hooksPath` is not
`AGI_*-prefixed`, so the prefix glob alone leaves it and every `git` a test
shells out to runs the commit guard — the suite's colour would then depend on
who spawned it (extensions/agi/conftest.py's own comment; test_agi_env_strip.py
measures the mechanism and pins it). So the shared body defaults to the
WEAKER policy (`extra_keys=()`) and the engine caller narrows it explicitly
with the three names. A default that is stronger would have silently given the
declared suite a strip it never asked for; a default that is weaker cannot take
anything away from the engine, because the engine names its own keys.

The two lock roots are NOT a strength ordering — they are two different
windows, which is exactly why a wholesale alias was refused. The engine suite
locks the project of its own conftest FILE (a `cd` must not move the window);
the declared suite locks VERIFY_GRAPH_ROOT else the cwd's project, so a suite
run inside a tmp graph locks ITS OWN window and never the live one. Same lock
file, same marker, same refusal; only the root is a parameter.

Both are parameterisable, so nothing is left named-and-unfixed from this
residue. One incidental tightening inside the shared body: it resolves the
root ONCE (the old suite_guards copy called `graph_root()` twice, once for the
None check and once for the acquire, so an env change between the two calls
would have locked a different root than the one checked).

## Probes (one negative per claim conjunct, all run by me, all PASS)

New file `extensions/agi/tests/test_suite_guard_policy_args.py` — 10 tests.
Every lock/strip probe is a NEGATIVE one: it shows the two policies still
DIFFER, so unifying the body was not a silent aliasing of one suite's
behaviour onto the other's.

| probe | what it pins |
|---|---|
| `test_the_two_locks_resolve_two_different_roots` | from inside a DIFFERENT project, `graph_root()` follows the cwd and the engine's file-relative resolver does not — the two policies still differ |
| `test_verify_graph_root_overrides_the_context_policy_only` | VERIFY_GRAPH_ROOT moves the declared suite's root and only that one |
| `test_one_lock_body_under_an_arbitrary_root` | the shared body writes THAT root's lock, stamps the marker, and unlinks both on exit |
| `test_the_same_body_refuses_a_live_foreign_holder_by_name` | a second run under a LIVE foreign pid (os.getppid(), alive and not us — our own pid is stale by contract) is refused naming that pid, marker unset |
| `test_lock_body_no_ops_on_a_resolver_returning_nothing` | a resolver returning None is a silent no-op in BOTH suites |
| `test_an_inherited_marker_makes_every_policy_a_no_op` | a nested pytest inherits the marker and never re-acquires |
| `test_the_extra_channel_is_an_argument_not_a_copy` | default policy leaves a seeded `GIT_CONFIG_COUNT` ALIVE while removing `AGI_TIER`; restore puts the AGI var back |
| `test_engine_policy_strips_the_git_hook_channel` | with the names passed, every `GIT_CONFIG_*` goes, and all three come back on restore |
| `test_the_engine_conftest_passes_its_own_policy` | the LIVE `extensions/agi/conftest.py`, loaded by path, really delegates to the shared body, really removes both channels, and really restores (the `os.environ` swap is restored in a finally) |
| `test_the_declared_conftest_keeps_the_weaker_policy` | `.agi/context/conftest.py` still imports the default names and instantiates neither factory — the declared suite did not inherit the engine's policy |

## Commands and output

```
$ timeout 900 prlimit --nproc=300 python3 -m pytest \
    extensions/agi/tests/test_suite_guard_policy_args.py -q -p no:cacheprovider \
    --basetemp /tmp/kid-a00c02d5b4f-5
..........                                                     [100%]
10 passed in 0.10s

$ timeout 1800 prlimit --cpu=600:600 --nofile=4096:4096 python3 -m pytest \
    extensions/agi/tests/test_declared_suite_guards.py \
    extensions/agi/tests/test_conftest_guard.py \
    extensions/agi/tests/test_tier_gate.py \
    extensions/agi/tests/test_rotate_term_grace.py \
    extensions/agi/tests/test_workflow.py \
    extensions/agi/tests/test_launch_memory_cap.py \
    extensions/agi/tests/test_agi_env_strip.py \
    extensions/agi/tests/test_suite_guard_policy_args.py -q -p no:cacheprovider \
    --basetemp /tmp/kid-a00c02d5b4f-10
236 passed in 168.26s (0:02:48)

$ timeout 900 prlimit --cpu=900:900 --nofile=4096:4096 python3 -m pytest \
    extensions/agi/tests/test_launch_memory_cap.py -q \
    -k test_stage_cap_death_is_named_memory_cap -p no:cacheprovider \
    --basetemp /tmp/kid-a00c02d5b4f-11
1 passed, 8 deselected in 0.16s
```

`test_declared_suite_guards.py` is the live end-to-end proof for residue 1: it
spawns REAL declared suites whose conftest is the one-line plain import, so the
lock it exercises is the shared body instantiated with the default policy, and
those 6 pass on the built bytes.

`extensions/agi/bin/paths.py audit` gains no hit: the only new literal is the
`bin` dir, derived from the conftest's own `Path(__file__).parent`, and no new
repo-specific key list is introduced (GIT_CONFIG_SPAWN_VARS was already the
one spelling, now re-exported rather than restated).

## Ceiling

`git diff --numstat` over the production paths (test files excluded):
`+75/-37` suite_guards.py, `+19/-20` extensions/agi/conftest.py, `+10/-45`
tests/conftest.py, `.agi/context/conftest.py` untouched — **+104/-102, net +2**
against a 40-line ceiling. Recorded in frontmatter as `production_lines 104`
with a `rebrief_request` naming the open question: on the ADDED-lines reading
that is over 2x, on the net reading it is under. I trimmed the docstrings once
(122 -> 104 added) and stopped rather than gut the recorded why; the only work
that would remain under either reading is none — the change is built and green.

## Not parameterisable / left named

Nothing in the two residues resists parameterisation; both are now
argument-passed one-liners at the call sites. The seams the leaf tests drive
were kept where the tests expect them, which is why the engine conftest still
exposes `_strip_agi_env` / `_restore_agi_env` / `GIT_CONFIG_SPAWN_VARS` and
the tests conftest still exposes `SUITE_LOCK_MARKER` — they are now thin
delegations, not second bodies.

## Agent Notes
Both duplicate guard bodies are now ONE implementation in suite_guards with the difference as an argument: make_suite_lock_fixture(root_resolver) and make_agi_env_stripped_fixture(extra_keys) + strip_/restore_dispatch_env. The engine conftest passes its own find_project_root(__file__) and its GIT_CONFIG_* channel; the declared context suite is unchanged and keeps VERIFY_GRAPH_ROOT-else-cwd plus no extra keys (the engine policy is strictly stronger on that one axis, so the shared default is the weaker one). 10 new negative probes in test_suite_guard_policy_args.py; 236 green over 8 named files incl. test_declared_suite_guards, plus the memory-cap repro. Caveat: +104/-102 (net +2) production lines vs a 40 ceiling - rebrief_request filed on the metric reading. Stray left in place: .agi/nodes/experiment/a00-008f4f72-2972ed.md is modified by someone other than me.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-c8389b84), reading the BYTES bc36299d8..8fa7f7812. (1) The order said "make the ONE home PARAMETERISABLE and have both conftests import it, so there is one implementation and each caller passes its own policy" and "no behaviour change for either suite". (2) What the machine does: extensions/agi/conftest.py:60-67 and :76-79 are now `_strip_agi_env`/`_restore_agi_env` delegating to suite_guards.strip_dispatch_env/restore_dispatch_env, GIT_CONFIG_SPAWN_VARS is the SHARED tuple re-exported, and the session fixture is `suite_guards.make_agi_env_stripped_fixture(GIT_CONFIG_SPAWN_VARS)`; extensions/agi/tests/conftest.py:448-457 replaces a 45-line lock body with one `make_suite_lock_fixture(lambda: locations.find_project_root(Path(__file__).resolve()))`; .agi/context/conftest.py is byte-unchanged and still instantiates neither factory. I proved the call site is LIVE, not decorative: loading extensions/agi/conftest.py by path, `_agi_env_stripped._fixture_function.__qualname__` is `make_agi_env_stripped_fixture.<locals>.agi_env_stripped` in module suite_guards and its closure cell holds exactly the three GIT_CONFIG_* names; in tests/conftest.py the lock fixture is `make_suite_lock_fixture.<locals>.suite_lock` in suite_guards. (3) The near miss: a shared factory that IGNORES its arguments and reads the policy from a module global or from the caller s cwd -- one body, two spellings, and the two suites silently back to the same window, which satisfies "one home" in the source and loses the mechanism at run time. (4) No standing rule deviated. Probes, mine, all PASS: (G) gate -- with verify-suite.lock planted at os.getppid() (a LIVE pid that is not us), acquire_suite_lock returns the holder and the run is refused, so the shared body still refuses by name; (A) auth -- the default policy strip_dispatch_env(()) leaves GIT_CONFIG_COUNT ALIVE while removing AGI_TIER, and the SAME body with the engine s three names removes the git-hook channel and restore_dispatch_env puts AGI_TIER back: the policy is an argument, not a copy, and the shared default is the weaker one so the declared suite is not strengthened behind its back; (W) wire -- the two qualname/closure facts above, plus `GIT_CONFIG_SPAWN_VARS is suite_guards.GIT_CONFIG_SPAWN_VARS` True and no inline os.environ.pop left in _strip_agi_env. Accepted as proved with evidence_runs naming its own run. Re-brief answered: cut (94/40 added production lines, measured at cli.py:702-732, disclosed correctly; nothing further to author). The node title is the kid s own, and its caveat about a foreign edit to kid 1 s node is my review edit, not a stray.
<!-- THOUGHT:END -->

PARENT PROBES: G(gate) a LIVE foreign holder in verify-suite.lock -> acquire_suite_lock returns the holder, the run refuses by name. A(auth) strip_dispatch_env(()) leaves GIT_CONFIG_COUNT alive and drops AGI_TIER; the same body with the engine s GIT_CONFIG_SPAWN_VARS drops the git-hook channel; restore puts AGI_TIER back. W(wire) the live conftests fixtures resolve to suite_guards.make_agi_env_stripped_fixture.<locals>.agi_env_stripped (closure holds the three key names) and make_suite_lock_fixture.<locals>.suite_lock; .agi/context/conftest.py still instantiates neither factory. Accepted 1, demoted 0. Rebrief answered: cut at 94/40 added production lines.
