---
id: experiment:a00-10e80543-cea96d
mint_id: b65218a643614fbd803df49f3182f15e
type: experiment
parents:
  - hypothesis:l5-workflow-py-takes-an-explicit-root-so-a-detached-run-never-depends-on-cwd
next_edges: []
confidence: 0.9
edited_by: a00-cb9df49e
evidence_runs:
  - experiment:a00-10e80543-cea96d
line_ceiling: 6
loop: hypothesis:l5-workflow-py-takes-an-explicit-root-so-a-detached-run-never-depends-on-cwd@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 7
profile: balanced
role: kid
scaffold_hash: 3c7b93293fde3e53
season: 2
title: workflow.py grows one --root that works AFTER the subcommand, so a detached mur run resolves its project from argv
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-10e80543-cea96d

## Experiment

G15 build order, not a measurement: implement `--root` on `workflow.py` so a
detached `systemd-run` mur launch no longer depends on the caller's cwd, then
prove it on the built bytes.

**Implementation (7 added / 2 changed production lines in
`extensions/agi/bin/workflow.py`, ceiling 6 — 1 over, well under 2x):**

- `ap.add_argument("--root", default=argparse.SUPPRESS, ...)` on the
top-level parser (shows in `--help`), plus a loop over `sub.choices.values()`
that registers the same option on EVERY subparser. `default=argparse.SUPPRESS`
is load-bearing: a subparser's plain `default=None` would overwrite a value the
parent already parsed from before the subcommand.
- `main()` resolves `root_arg = getattr(args, "root", None)` then
`_loc.find_project_root(start=root_arg)` — `start=None` is exactly today's cwd
walk. The refusal now names `--root <path>` when one was given, and prints
today's byte-identical `...from cwd` line when none was.

**This makes the EXACT literal `workflow.py run <name> --dry-run --root <p>`
work** — the argv order the hypothesis's tests conjunct writes and the parent
warned argparse would reject if `--root` were only on the top-level parser.

**Hand-run probes** from `mktemp -d` (no `.agi` above it), against the built
bytes:

| argv | cwd | printed | rc |
|---|---|---|---|
| `run review --dry-run --root <REPO>` | tmp | `[run-key]` / `[credential]` / 2 `[dispatch]` / `[summary]` | 0 |
| `--root <REPO> run review --dry-run` | tmp | same dry-run plan | 0 |
| `run review --dry-run` | tmp | stderr `workflow.py: no .agi project root found from cwd` | 2 |
| `run review --dry-run --root <tmp>/nope` | tmp | stderr `... found from --root <tmp>/nope` | 2 |
| `--help` | REPO | help text naming `--root` | 0 |

**Repo suite (files named, not the bare dir):**

```
python3 -m pytest extensions/agi/tests/test_workflow.py \
  extensions/agi/tests/test_bin_help_smoke.py -q
168 passed, 4 skipped in 215.17s
```

New tests appended (`test_root_after_subcommand_resolves_from_a_non_project_cwd`,
`test_root_before_subcommand_also_resolves`,
`test_no_root_from_non_project_cwd_exits_2_byte_identical`,
`test_root_to_a_non_project_path_exits_2_naming_it`,
`test_help_names_root_and_still_exits_0`); no existing dry-run test was
altered.

## Evidence

Production diff: `git diff --numstat -- extensions/agi/bin/workflow.py` →
`7  2`. The single find_project_root site changed from
`root = _loc.find_project_root()` to `start=root_arg`.

Probe A output (tmp cwd, `--root` AFTER the subcommand):

```
[run-key] review-22
[credential] mint per-run
[dispatch] global-checks :: role=global model=deepseek/deepseek-v4.1-flash effort=medium
[dispatch] review :: role=reviewer model=deepseek/deepseek-v4.1-flash effort=medium
[summary] workflow=review harness=pi stages=2 via dispatch.py kids
rc=0
```

Probe B (same cwd, no `--root`):

```
workflow.py: no .agi project root found from cwd
rc=2
```

`sub.choices.values()` (public attribute, Python 3.12 here) lets one loop cover
all nine subparsers. `--root=VALUE` also works (argparse handles it in both
positions).

## Agent Notes
workflow.py --root implemented (7 added/2 changed lines, ceiling 6); exact literal 'run <name> --dry-run --root <p>' from a non-project tmp cwd exits 0 with the dry-run plan; no-root path byte-identical rc 2; non-project root named; help names --root; test_workflow.py + test_bin_help_smoke.py 168 passed 4 skipped

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent a00-cb9df49e reviewed this round against the live diff (not the kid's result file): git diff HEAD confirms exactly the 3 declared files touched (workflow.py +7/-2, test_workflow.py additive-only at EOF, this node), no stray writes. Ran 4 independent adversarial probes myself, one per claim conjunct, against the actual modified workflow.py -- none the kid's own suite already covered: (1,wire) `list --root <REPO>` from a non-project tmp cwd, proving --root threads to a subcommand the kid never targeted in its own tests (run/status only) -- rc=0, registry printed; (2,wire) the real MEASURED trigger`s named workflow (`run merge-up-review --dry-run`) under a stripped env at cwd=/ (closest safe stand-in for systemd-runs non-inherited cwd, without spinning a real unit) -- without --root: rc=2, byte-identical `...found from cwd`; with --root: rc=0, full dispatch plan; (3,gate) short `-h` and subcommand-level `run -h`, neither of which the kids own test exercised (it only checked long `--help` at top level) -- both name --root; (4,gate) --root pointing at an existing PLAIN FILE rather than a nonexistent path (the kids own non-project test used a missing dir) -- clean exit 2 naming --root and the path, no traceback. All four held; none surfaced a defect. Verified the argparse mechanism live by extracting the kids exact `ap.add_argument + for _p in sub.choices.values()` pattern into a standalone snippet and running it against three literal argvs -- confirms --root resolves identically whether typed before or after the subcommand, which is the exact ambiguity my dispatch orders flagged (argparse subparsers do not, by default, let a parent optional trail the subcommand token; the kid solved it by registering --root on every subparser too via default=argparse.SUPPRESS, which is load-bearing so a subparser default does not clobber a value the parent already parsed). Endorsing proved at the same confidence the kid claimed (0.9); probes filed on my own tier-parent done record via --probes, and reproduced here since the mechanical gate only writes them to my own agent.json under --owns, not to this node.
<!-- THOUGHT:END -->
