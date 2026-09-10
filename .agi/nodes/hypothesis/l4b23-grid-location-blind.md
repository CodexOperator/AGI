---
id: hypothesis:l4b23-grid-location-blind
mint_id: 02a5875632ea48bda7695d7313442ee4
type: hypothesis
parents:
  - idea:l4b23-grid-location-blind
next_edges: []
confidence: 0.6
edited_by: sanctuary-helper
scaffold_hash: 42251fe9119c7886
season: 2
tags:
  - hypothesis
testable_claim: "A payload recorded under a non-default location: stays inside the grid: grid.resolve_payload and write.py create --payload's link_ref agree on where it lives (owner-reported defect, l4-plan A:42)."
thought_session: sanctuary-helper-05
title: grid.resolve_payload and write.py create --payload's link_ref must agree on location
---
<!-- BODY:BEGIN -->
# hypothesis:l4b23-grid-location-blind

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## L4.12 brief -- grid.py's resolve_payload ignores the node's `location:` field

ROOT CAUSE, confirmed by reading the code (not guessed): a build node's
payload can be written under any key declared in the project config's
`locations:` map -- `write.py create --payload` (via
`node_writer.ensure_payload`) stamps a `location:` field on the node,
defaulting to `locations.DEFAULT_PAYLOAD_LOCATION` = `"source_root"`
(locations.py:357), and `locations.py` has its own resolver for turning a
`location:` key into a real directory (the function near
`locations.py:375-403`, look for what actually reads `locations:` from the
project config -- name it exactly in your experiment node once found).
But `extensions/agi/bin/grid.py`'s OWN `resolve_payload(root, payload_ref,
engine_root)` (grid.py:339-363) takes NO `location` parameter at all and
NEVER calls into `locations.py`'s resolver. It only ever tries two
hardcoded spots, in this fixed order: (1) `<project>/payloads/<payload_ref>`
(the staged grid checkout) and (2) `<engine_root>/<payload_ref>` (the live
engine tree) -- returning `None` ("neither exists") if the real file lives
anywhere else, even though the node's own `location:` field correctly
names where it is. For the DEFAULT location (`source_root`), this happens
to work by coincidence when `source_root` and `engine_root` are the same
tree (true for this project today) -- which is exactly why the bug has
stayed invisible: every payload minted with the default location still
resolves, and only a payload recorded under a NON-default location
(`graph_root`, `repo_root`, or a custom key) silently fails to resolve
through the grid even though `write.py create --payload`'s own
`link_ref`/`location:` say precisely where it is.

FILE: extensions/agi/bin/grid.py (`resolve_payload` and its callers --
grep for `resolve_payload(` to find every call site that will need the
node's `location:` field threaded in) and extensions/agi/bin/locations.py
(read-only reference for the resolver you call into; do not change its
behaviour, only call it).

CHANGE: make `resolve_payload` (or a new sibling function, if changing
the existing signature breaks too many callers -- your judgment, but say
which you chose and why) read the node's `location:` field and resolve
through the SAME mechanism `locations.py` already provides for every other
location-aware reader, rather than only ever trying the two hardcoded
spots. The staged-checkout-wins-over-engine priority (goal:g6.1's arrow)
must not change for the DEFAULT location -- only the non-default case
needs to start working.

VERIFY: mint a scratch build node (in a throwaway location, or as a
`--dry-run`) with `--set location=graph_root` (or another real non-default
key from the project's `locations:` config -- read `.agi/config.json` to
find one that actually exists; do not invent a key), put a payload file at
the path that location key resolves to, and show that
`grid.resolve_payload` returns it correctly AFTER your fix (and confirm it
returned `None` before, so the test is red-then-green, not just green).
Also re-run one existing default-location payload lookup to confirm
nothing regresses. Run ONLY the grid-related test file (find it: `grep -l
resolve_payload extensions/agi/tests/*.py`) -- never the full suite.

KID CEILING: 2. Single-function fix plus its test; a second kid is for
review only if the first kid's diff needs it.

DO NOT: touch anything about the staged-vs-engine priority for the
DEFAULT location. Do not add a build node. Do not `git add -A`. Do not
run `grid.py commit --all` on this seat branch -- end at `git commit` +
`git push` on your own branch/worktree.

REPORT: write one `experiment` node whose `parents` is this hypothesis,
with a verdict on the testable claim (`proved` only if the red-then-green
check above actually ran). `evidence_runs` must be a list of node ids that
resolve in the corpus; your own experiment node counts once it exists.
List every verify command and its actual output in the body, including
the exact `locations:` key and path you tested against.

## L4.12 FOLLOW-UP -- the RED leg is proven, now land the GREEN

Previous round (experiment:a00-0696a133-f021c0, disproved -- correctly:
it only ran the red leg and the brief requires red-then-green for
proved) confirmed the defect with real output, in this exact repo'''s
config shape:

    location=None          grid.resolve_payload=False  locations-resolves=False  AGREES yes
    location='''source_root'''  grid.resolve_payload=False  locations-resolves=False  AGREES yes
    location='''graph_root'''   grid.resolve_payload=False  locations-resolves=False  AGREES yes
    location='''docset'''       grid.resolve_payload=False  locations-resolves=True   AGREES NO <- bug

REAL-WORLD RELEVANCE, not just synthetic: this repo'''s OWN
`.agi/config.json` already declares a non-default location key --
`locations: {comms_root: comms/season-2}`. Any existing or future
build node with `location: comms_root` is ALREADY silently unresolvable
through `grid.resolve_payload` today. Check whether any node in
`.agi/nodes/build/` already carries `location: comms_root` (grep
`payload_ref`+`location:` together) as part of your verify -- if one
exists, that is a live, not hypothetical, breakage to confirm fixed.

EXACT MECHANISM, already traced (previous kid, verified by reading the
code): `node_writer.ensure_payload` (node_writer.py:425) and
`replace_payload` (node_writer.py:454) already call
`locations.resolve_payload_path(root, ref, location)` -- the correct,
location-aware resolver, which already handles arbitrary
`locations:`-declared keys (confirmed: it resolved the scratch
`docset` key fine). `grid.resolve_payload` (grid.py:339-363) takes NO
`location` parameter and only ever tries two hardcoded spots. Its
callers are at grid.py:894 and grid.py:1178 -- both currently pass only
`(root, payload_ref, engine_root)`; both need the node'''s `location:`
field threaded through once the signature changes.

FILE: extensions/agi/bin/grid.py (`resolve_payload` and its two callers
at :894 and :1178). Read-only reference: extensions/agi/bin/locations.py
(`resolve_payload_path`, already correct -- call into it, do not
reimplement its logic).

CHANGE: give `resolve_payload` a `location: str | None = None`
parameter (or thread it from a node'''s frontmatter at each call site --
your call on the cleanest shape). When a location is given, resolve
through `locations.resolve_payload_path` the same way
`node_writer.ensure_payload` does. PRESERVE the staged-checkout-wins-
over-engine priority for the DEFAULT location (`source_root`) exactly as
today -- do not let the new location-aware path change behavior for the
common case, only add coverage for the non-default one.

VERIFY, RED-THEN-GREEN, properly this time -- as a real pytest test in
extensions/agi/tests/test_grid.py, not a /tmp scratch script (the
previous round'''s scratch harness proved the point once; this round
should leave a permanent regression test behind): write a test that
declares a non-default location key (mirror this repo'''s own
`comms_root`, or reuse the previous round'''s `docset` shape), writes a
payload file there, and asserts `grid.resolve_payload` finds it BEFORE
your fix (this assertion should currently FAIL -- confirm it fails
first, then apply your fix, then confirm it passes) -- i.e. write the
test red, watch it fail, then make it pass, do not write the fix first
and the test after. Also re-run the DEFAULT-location case to confirm no
regression. Run ONLY `extensions/agi/tests/test_grid.py` -- never the
full suite (the prime is running it once, coordinated; do not add a
second concurrent run).

BUILD NODE: this DOES mint a build node for grid.py (parents:
grid.py'''s existing build node if one exists -- check
`.agi/nodes/build/` for its `payload_ref` -- plus `goal:g15`, per
`goal:s29`'''s `[build:<id>, goal:<id>]` shape for a new version of an
existing file). Never a bare `[goal:<id>]`.

KID CEILING: 2 -- the mechanism and the fix are already fully traced;
this is implement-the-fix-and-write-the-real-test work, not discovery.

DO NOT: touch node_writer.py or locations.py (both already correct; if
your investigation proves otherwise, say exactly why, do not silently
edit them). Do not change staged-checkout priority for the default
location. Do not `git add -A`. Do not run `grid.py commit --all` on
this seat branch, and do not use `season.py merge-up` either -- end at
`git commit` + `git push` on your own branch/worktree; the seat
reviews and merges manually.

REPORT: write one NEW `experiment` node whose `parents` is this
hypothesis (do not edit the previous disproved one -- it stands as the
red-leg record), with the red-then-green test output and a verdict.
`evidence_runs` must resolve to real node ids -- cite BOTH your new
experiment and the previous disproved one, since together they tell the
whole red-then-green story. List every verify command and its actual
output.
