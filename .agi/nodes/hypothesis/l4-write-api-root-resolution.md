---
id: hypothesis:l4-write-api-root-resolution
mint_id: 1c9bd2c6c4254319a2839625a5f8aed7
type: hypothesis
parents:
  - idea:l4-write-api-root-resolution
next_edges: []
edited_by: sanctuary-helper
scaffold_hash: 29497577fe009dba
season: 2
testable_claim: "write.py's Python API (create(root, ...) at write.py:1109, submit(root, edit, ...) at write.py:691) takes `root` raw with no call through locations.find_project_root(), unlike main()'s two CLI call sites (write.py:1208, :1253), which do resolve it. Verified directly: _load_seats (write.py:519) does `Path(root) / \"nodes\" / \".geometry\" / \"seats.md\"`, and _enforce_written_by (write.py:600) does `Path(root) / \"context\" / \"schemas\"` then `if not schemas_dir.is_dir(): return` -- a silent no-op, not a refusal, when the schema directory is unreachable from a wrong root. So an in-process caller that passes an unresolved or wrong root (e.g. \".\" from the repo root instead of the resolved \"<root>/.agi\") gets: (a) a real node written to the wrong location (\"<root>/nodes/<type>/<slug>.md\" instead of \"<root>/.agi/nodes/<type>/<slug>.md\"), stamped with whatever `season` the wrong location's config carries or defaults to, and (b) the written_by spawn gate silently degrading to unverified rather than refusing, because the schema lookup misses and the missing-schema path returns instead of raising -- so a wrong root presents as success, not failure. Falsifiable: (1) call write.create or write.submit directly (not through main()) with an unresolved root from a directory whose child is the real .agi project, and confirm which of these it does -- if it instead correctly resolves or refuses, the hypothesis is false. (2) Confirm whether the exact runtime warning text the assignment quoted (\"SPAWN-GATE SCHEMA ERROR\", \"SPAWN-GATE UNVERIFIED\") exists verbatim in node_writer.py's own separate parent/child spawn gate (not grep-found by the director's own reviewer in node_writer.py or extensions/agi/src/ -- pin down its real source or its real wording, don't assume the quote is exact)."
thought_session: sanctuary-helper-6b
title: write.py's create()/submit() take root raw; a wrong root degrades the spawn gate to unverified rather than refusing
---
<!-- BODY:BEGIN -->
# hypothesis:l4-write-api-root-resolution

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.5x brief -- write.py's Python API can mint outside the graph with the gate silently unverified

Assigned by sanctuary-director (seat rotated mid-session; verify your own
correspondent the same way before reporting -- tmux list-windows -t agi-rc
cross-referenced with ListAgents, never a display name alone). Root-caused
already, both by the assigning director and independently reproduced here
against the current, synced write.py (this seat's branch was 157 commits
behind season/s2 when the assignment arrived -- write.py itself had grown
from 1209 to 1415 lines since this seat's branch forked; synced before
writing this brief so the line numbers below are real, not stale).

MEASURED (by the assigning director, in their own seat worktree, an hour
before this brief): `write.create(".", "hypothesis", <slug>, [<parent>], ...)`
called from the repo root wrote a REAL node to `<worktree>/nodes/hypothesis/
<slug>.md` -- NOT `<worktree>/.agi/nodes/` -- stamped `season: 1` instead of
2, printed something to the effect of a spawn-gate schema error naming the
schemas directory as missing and the gate as unverified, then returned
`rejected: False written: True`. Removing the stray file and re-minting
against the resolved root made the gate approve correctly -- same node, same
parents, same call, only the root argument differed.

ROOT CAUSE, verified independently against write.py as it stands now:
- `main()` resolves `--root` through `locations.find_project_root(Path(args.
  root).resolve())` at TWO call sites: write.py:1208 and write.py:1253. CLI
  callers are safe.
- The Python API is NOT: `create(root, ...)` (write.py:1109) and `submit(root,
  edit, ...)` (write.py:691) take `root` as a plain argument and never call
  find_project_root on it.
- `_load_seats(root)` (write.py:514-519) builds `Path(root) / "nodes" /
  ".geometry" / "seats.md"` directly. `_enforce_written_by(root, ...)`
  (write.py:600-627) builds `Path(root) / "context" / "schemas"`, and when
  that directory does not exist, the function returns -- silently, no
  exception, no printed warning from THIS function specifically (confirmed by
  reading it end to end). Whatever prints the "SPAWN-GATE SCHEMA ERROR" /
  "SPAWN-GATE UNVERIFIED" text the assignment quoted was NOT found by grep in
  node_writer.py or extensions/agi/src/ in this review -- it may be phrased
  slightly differently, or it may live in node_writer's own SEPARATE
  parent/child spawn gate (the one that prints "SPAWN-GATE APPROVED ..." on a
  normal create -- distinct from _enforce_written_by, which is the
  written_by/moral-node restricted-writer check specifically). PIN DOWN THE
  REAL SOURCE of that message before writing your fix; do not assume the
  quoted text is the literal string without finding it.

THE SHARP HALF, worth restating precisely because it is the actual severity
claim: a wrong root does not fail loudly. It degrades enforcement to
unverified and the write proceeds, so "wrong root" and "correct root,
nothing to enforce" are visually identical in a stream nobody diffs by
default -- the failure mode is silent success with a warning, not an error.

TWO DIRECTIONS, both defensible. Root-cause first, then pick one (or a better
one you find), and say which and why in the node's THOUGHT block on your
experiment -- this is the actual engineering decision, not pre-made for you:

(1) Resolve `root` inside `create`/`submit` the way the CLI does.
    🔴 DESCEND ONLY, NEVER ASCEND. `locations.find_project_root` WALKS UP
    the filesystem looking for an enclosing `.agi/`. A caller (in particular
    a TEST that passes a bare `tmp_path`, which has no `.agi/` of its own)
    would, if the resolver is allowed to walk up past `tmp_path`, resolve
    into a REAL ancestor graph -- e.g. this very project's own `.agi/` -- and
    write a real node into it. That is a DATA-LOSS-SHAPED hazard (a test
    writing into production graph state), not merely a bug. If you take this
    direction: the resolution must refuse to ascend past the root it was
    handed (verify a project's own `.agi/` directly under the given root, or
    fail, never walk further up than that), AND that never-ascend property
    needs its OWN direct test asserting it -- not an inference from the
    passing tests around it.

(2) Make the gate REFUSE instead of degrading, when the schemas directory
    (and/or the seats file) is absent. Arguably the deeper fix: it closes the
    whole CLASS of "wrong root looks like success" rather than patching one
    caller. Before committing to this direction: find out what, if anything,
    legitimately relies on the current fall-through-permissive behaviour (a
    test fixture with no schemas dir on purpose? a bootstrap path that runs
    before schemas exist? read the git history / callers, don't guess) --
    the assigning director explicitly has not traced this and flagged it as
    the open question. If NOTHING legitimate relies on it, direction (2)
    is straightforwardly correct AND is the more valuable finding to report
    (see REPORT below). If something does rely on it, say so precisely
    (which caller, why) rather than either breaking it silently or refusing
    to touch the gate at all.

CONSTRAINTS:
- Dispatch it, don't hand-code it -- standing preference restated by the
  assigning director for this round specifically.
- Kid ceiling: 2. No full-suite run -- the targeted files below are the
  scope; do not run pytest against the bare directory.
- Do NOT touch `extensions/agi/bin/locations.py`. A separate live round owns
  `project_root_from_env` there (same bug family: the env branch returns its
  value raw without validation, which is a DIFFERENT symptom -- every
  `--branch` child's `goals-check` exiting 1 on a clean tree -- do not fold
  the two together or touch that file even to fix something adjacent).
- Do NOT weaken an existing assertion to go green, ever, for any reason.
- Targeted tests, all three, the gate's behaviour is the subject of this
  round, not a bystander to it: `extensions/agi/tests/test_write.py`,
  `extensions/agi/tests/test_node_writer.py`,
  `extensions/agi/tests/test_spawn_gate.py`. Confirmed all three currently
  pass (215 passed) before this brief was written -- your diff must not
  regress that count, and should grow it (new tests for the fix and for the
  never-ascend property if you take direction 1).
- Mint your own chain under this hypothesis, commit AND push before
  dispatching a kid, ceiling and assignment live in this node, never in a
  message. `grid.py commit --all` will refuse on your own seat/loop branch
  (branch-blind by design) -- that is expected, not an error to chase.

REPORT: write one `experiment` node whose parents is this hypothesis, with a
verdict on the testable claim. State plainly which direction you took (or
both, if you judge both warranted -- they are not mutually exclusive: a
refuse-on-missing-schema gate AND a properly-resolved root are not in
tension) and why, cite the never-ascend test if you took direction 1, and
state precisely what (if anything) you found relying on the permissive
fallback if you investigated direction 2. If direction (2) turns out to be
load-bearing for something legitimate, that is a significant finding -- name
it clearly and explicitly in the experiment node; it is the kind of thing
that changes a standing rule elsewhere, not a routine result.
