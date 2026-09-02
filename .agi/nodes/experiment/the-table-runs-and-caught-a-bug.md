---
id: experiment:the-table-runs-and-caught-a-bug
mint_id: 52a5cdee52d34dbb9626e20567637623
type: experiment
title: The table runs and caught a bug
parents:
  - hypothesis:commands-are-config-not-prose
next_edges:
  - verdict:declared-commands-delete-four-copies
scaffold_hash: f3809c94d908f726
verdict: proved
confidence: 0.93
evidence_runs:
  - experiment:the-table-runs-and-caught-a-bug
---

# experiment:the-table-runs-and-caught-a-bug

## Experiment

`.geometry/commands.md` declares 11 commands in two workflows, minted by
copying `.geometry/crons.md`'s shape. `bin/commands.py` resolves them;
`render-context.py` renders them into `context/INJECTION.md`.

### The claim's sharp half: declaring found an error prose did not

**`grid-commit` was declared as `grid.py --all`.** The real command is
`grid.py commit --all`. That exact string had been sitting in `HANDOFF.md`
§5's verification sequence and in `CLAUDE.md`, correct in both — but the
moment it became *executable data* rather than prose, writing it wrong became
a thing that could be caught, and it was, on the first run of the table.

This is the whole claim in one line. **Prose is read and believed; a command
table is run.**

### Every declared read command executes

```
links        exit 0        schema       exit 0
budget       exit 0        credentials  exit 0
secrets      exit 0        crons        exit 0
```

### It reaches `INJECTION.md` through the normal path

`driver.sh --smoke` now writes the table into `context/INJECTION.md` above the
ASCII view — deliberately above, because both injectors truncate at 80 lines
and a command an agent never sees is a command it reinvents from memory.

### A second defect, in the renderer, found by reading the output

The first render described **both** workflows as *"in this order"*. `verify`
is a sequence; `read` is a set. That is a false instruction, and
`INJECTION.md` delivers it to every agent on every session — the same class as
`goal:s8`, where every pi kid was handed a contract contradicting its own
runtime.

Fixed with one optional schema field, `ordered`, listing which workflows are
sequences. `verify` is listed; `read` renders as `- **read**:`.

**Found by looking at the output, not by a test** — the same route as
iteration 106's breadth-first tree bug.

### A third: a silent `except` reported a present node as absent

`_load_node` returned `{}` for both "no node" and "node present but
unreadable", so a missing `src/` on `sys.path` printed *"no commands declared
at nodes/.geometry/commands.md"* about a fully parseable node at exactly that
path. Absence is silent because it is normal; **failing to read something
present is never normal**, and it now warns.

### Counts

11 new tests, including one asserting every declared command points at a file
that exists, and one asserting the table stays under 20 entries — the owner's
scope constraint, enforced rather than hoped for. Suite 1301 → **1312**.

### What this experiment does NOT show

- **The four prose copies are not deleted.** `CLAUDE.md`, `SKILL.md` and
  `QUICKSTART.md` still list commands. The declaration is now the executable
  source; making the prose *derive* from it is a separate change.
- **`run` is the least-exercised path.** The six read commands were run; the
  five `verify` commands were not run *through the resolver*, only directly.
- **No agent has been observed using the injected table.** That it lands in
  `INJECTION.md` is verified; that it changes behaviour is not.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Three defects in one iteration, and only one of them was in the thing being
built. The `grid-commit` typo is the hypothesis proving itself on first
contact; the ordered-versus-set line is a renderer bug found by reading
output; the silent `except` is a self-inflicted instance of the exact failure
mode I had flagged twice earlier in this session while writing other modules.
All three are recorded because a clean experiment record here would be a less
accurate one.

The `ordered` field is the most defensible bit of scope growth in the
iteration and it is worth saying why: a schema field is expensive, and the
alternative was one adjective in a rendered line. It got the field because the
rendered line is read by every agent, which makes an inaccuracy there a
different kind of object from an inaccuracy in a doc.

The first limit matters most. "Four copies drift" was the motivation, and this
iteration made a fifth copy that happens to be executable. The copies are only
deleted when the prose derives from the node, and claiming otherwise would be
the s17 shape wearing a fix's clothes.
<!-- THOUGHT:END -->
