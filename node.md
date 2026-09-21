---
id: hypothesis:commands-are-config-not-prose
mint_id: bb68183002e6441b83856d5ee1f211fc
type: hypothesis
parents:
  - goal:g1.10
next_edges:
  - experiment:the-table-runs-and-caught-a-bug
confidence: 0.85
edited_by: season.py
scaffold_hash: 7e09937831345e6e
season: 1
testable_claim: "A command table declared as a `.geometry` node, with one resolver, is strictly better than prose in a way that is **observable rather than aesthetic**: the table is executable, so a wrong command in it *fails* instead of being read and believed; and it is injectable, so an agent is **handed** the commands rather than remembering them."
thought_session: season
title: Commands are config not prose
verdict: pending
---
# hypothesis:commands-are-config-not-prose

## Hypothesis

The engine's standard commands lived in four places — `CLAUDE.md` prose,
`SKILL.md`'s table, `QUICKSTART.md`, and whatever the last `HANDOFF.md` wrote
down. Four copies drifting independently is `goal:s17`'s shape, and this repo
already paid for it once with the ancestor walk restated eleven times.

### Testable claim

A command table declared as a `.geometry` node, with one resolver, is strictly
better than prose in a way that is **observable rather than aesthetic**: the
table is executable, so a wrong command in it *fails* instead of being read
and believed; and it is injectable, so an agent is **handed** the commands
rather than remembering them.

The falsifiable form: **declaring the commands finds at least one error that
four copies of prose did not**, every declared command runs, and the set
reaches `INJECTION.md` without any agent being told to look it up.

### What would prove it

- Every declared command executes and exits 0 when run through the resolver.
- The declaration is rendered into `context/INJECTION.md` by the normal
  `--smoke` path, so a cold session is handed it with no motion spent.
- A test asserts every declared command points at a file that exists — the
  failure a cold session would otherwise hit first.
- The node holds **no absolute path**, so it survives a clone (`goal:g8.2`).

### What would disprove it

- The table becoming a fifth copy: declared, rendered, and never read by code.
  `goal:g10.2`'s rule is that a `.geometry` node is the input a code path
  resolves against, not documentation about one.
- The table growing without bound. The owner's scope — *"not a command for
  every custom test call, just the commands used during standard workflows"* —
  is the constraint, and a shell-alias dumping ground would be a worse artifact
  than the prose it replaced.
- Anything in the rendered output being **false**, since `INJECTION.md` is read
  by every agent. A false line here is a false instruction delivered at scale.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The claim is deliberately not "declaring commands is tidier". Tidiness is not
falsifiable and would have produced a node nobody could argue with or check.
"Declaring them finds an error prose did not" is checkable in one direction and
embarrassing in the other, which is what a claim should be.

The third disproof clause was added last and is the one that shaped the
implementation: because the rendered table lands in `INJECTION.md`, any
inaccuracy in it is not a documentation bug, it is an instruction handed to
every agent on every session. That is a higher bar than prose in `CLAUDE.md`
has to clear, and it is the reason the ordered-versus-set distinction ended up
being worth a schema field rather than being waved through.
<!-- THOUGHT:END -->