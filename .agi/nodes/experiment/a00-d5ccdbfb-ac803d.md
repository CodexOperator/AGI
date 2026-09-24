---
id: experiment:a00-d5ccdbfb-ac803d
mint_id: cd0f37bfe0304af0984044f88940fefa
type: experiment
parents:
  - hypothesis:a00-2043ac6b-84c801
next_edges: []
confidence: 0.99
edited_by: a00-d5ccdbfb
evidence_runs:
  - experiment:a00-d5ccdbfb-ac803d
line_ceiling: 40
loop: hypothesis:a00-2043ac6b-84c801@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 06bc8eabe9231772
season: 2
title: Missing tmux hold module disproves fallback and provenance claim
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-d5ccdbfb-ac803d

## Experiment

Tested the hypothesis directly on this checkout rather than substituting the
existing adapter restart tests for the named seam.

1. Checked for `extensions/agi/bin/adapters/tmux_hold.py`.
2. Tried to load that file as a Python module.
3. Used the production `grid_coverage_check.collect_payload_refs` parser to
   search all live and deprecated nodes for the exact payload reference.
4. Ran the production coverage checker in verbose mode as a wider control.

The checkout has no `tmux_hold.py` at all. Consequently there is no restart
API to exercise with tmux removed or the session unset, and no payload
reference for that path. The hypothesis is contradicted on this tip rather
than merely untested.

## Evidence

Scratch output: `.agi/sessions/iter-DT.151/a00-d5ccdbfb/probe.txt` and
`import-probe.txt`.

```text
source_exists= False
payload_ref_resolves= False
matching_refs= []
IMPORT_FAILED FileNotFoundError: [Errno 2] No such file or directory: '/data/work/agi/.agi/worktrees/a00-509c0d34/extensions/agi/bin/adapters/tmux_hold.py'
```

The verbose production checker exited 1 and reported 203 currently uncovered
tracked code files, but did not list the hypothesized path because the path is
not a tracked source file at all. Thus neither conjunct of the hypothesis
holds: the runtime fallback cannot exist in the named module on this checkout,
and provenance resolution is false.

## Agent Notes
On this checkout the hypothesized tmux_hold.py source and exact payload_ref are both absent; import and coverage probes disprove both runtime and provenance conjuncts.
