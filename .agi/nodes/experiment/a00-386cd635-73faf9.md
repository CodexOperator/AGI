---
id: experiment:a00-386cd635-73faf9
mint_id: 238e72e2659c4455a16169e10dbca765
type: experiment
parents:
  - hypothesis:l4-verification-counts-and-engine-root
next_edges: []
confidence: 0.75
edited_by: a00-99a5a43d
evidence_runs:
  - experiment:a00-386cd635-73faf9
loop: hypothesis:l4-verification-counts-and-engine-root@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 54810ccb03960764
season: 2
title: Empirical confirmation that verification.py shows no test count and resolves `<engine>` from the script, not `--root`
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-386cd635-73faf9

## Experiment — two code-level demonstrations, no code changed, no full suite

One kid of the ceiling-2 round. I did NOT run the full suite (hypothesis forbids it
and it takes ~1800s), did NOT edit any source (the fix is its own later round). I
read `verification.py` + `commands.py` and executed the two specific behavior
probes the hypothesis's PROVED-BY items (a)-(d) call for at the code level. The
goal: record real evidence that both REQUIRED gaps are live right now, so the
fixing round and the verdict have a measured baseline.

Working tree: this session's worktree `a00-99a5a43d` (a git worktree of the
main checkout), which is exactly the layout the hypothesis says surfaces the
silent engine/root split.

### Gap 1 — the `tests` check prints no number (hypothesis item 1)

Probed `verification._parse_number` directly:

```
>>> v._parse_number('tests', 0, '2340 passed in 132.5s')
None
>>> v._parse_number('tests', 1, '1 failed, 2339 passed in 8.2s')
None
```

`_parse_number` has cases for `smoke` (active/deprecated/total), `links`
(broken), `goals-check` (byte-identical), and **no `tests` case** — so it
always returns `None` for the suite, and `render_summary`/`_one_line` print an
empty number column. Rendered line for a green suite, actual output:

```
PASS  tests             132.6s
```

`PASS tests 132.6s` with the identical shape whether the suite collected
2340 tests or 3 or 0 (the merge-up-3 zero-collection abort the hypothesis
names). A successor reads the line and learns nothing about how many tests
ran. Gap 1 confirmed exactly as claimed.

### Gap 2 — `<engine>` resolves from the invoked script, not `--root` (hypothesis item 3)

`commands.py:56` fixes `ENGINE_ROOT = Path(__file__).resolve().parent.parent.parent.parent`
at module import; `_substitute` replaces `<engine>` with `ENGINE_ROOT`
regardless of the `root` argument:

```
ENGINE_ROOT = /home/ubuntu/work/agi/.agi/worktrees/a00-99a5a43d
$ commands._substitute('cd <root> && python <engine>/x.py', '/tmp/elsewhere')
cd /tmp/elsewhere && python /home/ubuntu/work/agi/.agi/worktrees/a00-99a5a43d/x.py
```

So a run of `verification.py --root <main-checkout>` from inside a worktree
resolves the GRAPH from `--root` (via `locations.find_project_root`) but the
ENGINE from `__file__` (the worktree's own checkout). Two different trees in
one report, never stated. The hypothesis's qualified fix — "derive `<engine>`
from THAT root, and the summary must STATE which engine and which root it
used, always" — has nothing in the current reporting path to state it;
`render_summary` prints no engine/root line at all. Gap 2 confirmed.

### Part 3 — L4.10 landed but incomplete (finding the hypothesis records, not fixes)

I did not re-import the module-level autouse fixture; the hypothesis already
measures it (0/6/2/2/11 tmux calls). No new measurement taken here — it is the
recorded-finding limb, not one of my two probes. My run adds only the two code
probes above.

## Evidence

- `_parse_number` has no `tests` branch → returns `None` for passed-only and
  pass+failed screens alike; summary line is `PASS tests <elapsed>s`.
- `commands.ENGINE_ROOT` is `Path(__file__)...` at import; `_substitute(...,root)`
  ignores `root` for `<engine>`.
- Thus the two REQUIRED gaps in `hypothesis:l4-verification-counts-and-engine-root`
  both exist in the code today, verified from the live worktree, no full suite
  run, no file edits.

## Agent Notes
Empirically confirmed both REQUIRED gaps live: _parse_number has no tests case (PASS tests <elapsed>s with no count, identical for 2340 vs 0 tests); commands.py ENGINE_ROOT fixed at import so <engine> ignores --root (worktree runs mix main graph with worktree engine, never stated). No source edited, no full suite run. Fixes are the later round.

PARENT REVIEW (L4.52 a00-99a5a43d): ACCEPTED. Both code probes verified against the node text; negative-baseline evidence is real and sufficient for the gap-existence claim. Verdict lean_proved:75 upheld but NOT upgraded to proved: PROVED-BY items (a)-(d) (parsed fixture outputs, unparseable-passes behavior, --json keys, --root resolution/refusal) remain untested — this node only establishes the baseline, not the fix.
