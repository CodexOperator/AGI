---
id: verdict:declared-commands-delete-four-copies
mint_id: e8e446a4898946c087243404bafe1ae1
type: verdict
parents:
  - experiment:the-table-runs-and-caught-a-bug
next_edges: []
confidence: 0.93
edited_by: season.py
evidence_runs:
  - experiment:the-table-runs-and-caught-a-bug
scaffold_hash: e00a2a6cbba53b8c
season: 1
thought_session: season
title: A declared command table is executable, so a wrong one fails instead of being believed
verdict: proved
---
# verdict:declared-commands-delete-four-copies

## Verdict

proved

## Evidence

`experiment:the-table-runs-and-caught-a-bug`:

- **`grid-commit` was declared as `grid.py --all`; the real command is
  `grid.py commit --all`.** The same string sat correct in `HANDOFF.md` §5 and
  `CLAUDE.md` — but declaring it made writing it wrong *catchable*, and it was
  caught on the table's first run.
- All six `read` commands execute and exit 0 through the resolver.
- The table renders into `context/INJECTION.md` via the normal `--smoke` path,
  above the ASCII view, since both injectors truncate at 80 lines.
- The node holds no absolute path; `<root>` and `<engine>` substitute at
  resolve time.
- 11 new tests, including "every declared command points at a file that
  exists" and "the table stays under 20 entries". Suite 1301 → 1312.

## What is proved

**Prose is read and believed; a command table is run.** That is the difference
declaring buys, and it is observable rather than aesthetic — a typo that four
copies of prose carried correctly for months became a first-run failure the
moment the command became data.

Two further defects fell out of the same property. The renderer described an
unordered inspection set as *"in this order"*, which `INJECTION.md` would have
delivered to every agent on every session; and `_load_node` returned the same
empty result for "no node" and "node present but unreadable", reporting *"no
commands declared"* about a parseable node at exactly the path it named.
Neither would have been visible in prose, because prose has no output to read
and no failure to observe.

## What is NOT proved — read this before citing it

- **The four prose copies are NOT deleted.** `CLAUDE.md`, `SKILL.md` and
  `QUICKSTART.md` still list commands. This iteration made a **fifth** copy
  that happens to be executable. The copies are only deleted when the prose
  *derives* from the node, and the title of this verdict overstates it — kept,
  because it names the goal the work is aimed at, but read the sentence above
  it before citing the title.
- **`run` is the least-exercised path.** The six `read` commands went through
  the resolver; the five `verify` commands were run directly, not through it.
- **No agent has been observed using the injected table.** It lands in
  `INJECTION.md`; whether that changes behaviour is unmeasured.
- **Scope is enforced by a test, not by judgement.** `<= 20` entries is a
  crude proxy for *"just the commands used during standard workflows"*, and a
  determined future session could satisfy it while still building a dumping
  ground.

## Consequence

The next increment is making the prose derive: `CLAUDE.md` and `QUICKSTART.md`
should render their command lists from this node rather than restating them.
Until that happens `goal:g1.10` is half-done, and this verdict is the record of
which half.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The title overstates and the body says so. That is an uncomfortable shape and
it was the honest one available: "declared commands delete four copies" is the
goal, the slug was minted from it before the work exposed that deletion is a
separate step, and renaming the node would change its address for a reason
that is really about my own tidiness. Better to leave the address alone and
put the correction in the first limit, where a reader hits it immediately.

Confidence 0.93 because the central claim — a wrong command fails rather than
being believed — is demonstrated by exactly one instance. It is a good
instance, found on first contact and pre-existing in two prose copies, but one
is one.

The scope-test caveat is included because I wrote that test and I know what it
is worth. `len(table) <= 20` cannot tell a standard workflow from a
convenience alias; it can only stop the most obvious version of the failure.
Recording that here is cheaper than a later session discovering the guard was
softer than it looked.
<!-- THOUGHT:END -->