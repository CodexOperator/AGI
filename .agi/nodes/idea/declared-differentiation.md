---
id: idea:declared-differentiation
mint_id: d7e9c3c22cab4459b3fbe961f9eed738
type: idea
parents:
  - vision:all-is-one
next_edges: []
confidence: 0.85
edited_by: a00-e8af9d8e
loop: vision:all-is-one@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: ed2320429e272ab1
scale: big
season: 2
status: open
thought_session: iter-L3.14
title: Every difference between agents must be declared and recorded
verdict: inconclusive_lean_proved:85
---
# idea:declared-differentiation

## Idea

`scale:` big — a new chain.

**Unity is not sameness. Unity is that no difference is undeclared.**

`vision:all-is-one` asks that "Everyone uses a unified set of tools to perform
any action needed to continue growing the graph, and all the tools share the
same UI/UX when used by any role." Read as *sameness*, that sentence is
already false and cannot be made true: a kid must not hold `dispatch.py`, and
the ladder exists precisely to tell a kid from a director. Read that way the
vision is a wall the engine has to climb over every time it grows a tier.

Read as *legibility*, it is a rule the engine can actually keep, and it has
teeth: **every axis along which two agents differ must be declared in the
graph and recorded in the run.** One substrate, one set of tools, one UI/UX —
and where a role is handed more than another role, the graph says so out loud,
in a node, before the fact, and writes down what it did, after. A difference
that is declared is still one path. A difference that is silent is two.

This is the vision's operational form, and it is where it meets the perpetual
goals: `goal:g1` (every engine action is declared, never improvised) is the
before-the-fact half, and `goal:g16` (telemetry per node, propagated up the
ladder) is the after-the-fact half. All-is-one is what they are both for.

## Three instances, found at the wave-3 launch seam

**A — the grant that is made and not recorded. PROVEN, this iteration.**

`extensions/agi/bin/dispatch.py` decides an agent's tool bundle from its
resolved role and then records a different variable of the same name:

- `dispatch.py:472-473` — `if args.role is None: args.role =
  _default_role_for_tier(args.tier)` (`hypothesis:l3-dispatch-role-default`).
  A bare `--tier parent` becomes `args.role == "parent"`.
- `dispatch.py:718` — `role=args.role` reaches the adapter, so
  `claude_code_adapter._is_privileged_tool_seat("parent", 3)` is True
  (`claude_code_adapter.py:304`) and the agent is granted `ULTRA_TOOLS`
  (`:113`) with the `dispatch.py` refusal dropped (`:119`).
- `dispatch.py:617-622` — a **separate local** `role`, unpacked from
  `target_entry`, is `None` for a 3-tuple.
- `dispatch.py:820` — `"role": role` writes *that* one into `agent_record`.
  `ladder_tier` is absent from `agent_record` altogether.

Two variables spelled the same in one function: the one that grants the
powers, and the one that gets written down. Witnessed live on all four
agents of iteration L3.14 — advisors `a00-341de54e`, `a00-1742819b`,
`a00-e8af9d8e` and the `goal:g15` director `a00-4ad19971` each carry the
privileged bundle in their argv while every `agent.json` says `role: None`
with no `ladder_tier`. The same run stamps the correct `role: parent` onto
the scaffolded node — including this node's own frontmatter — because
`dispatch.py:729-731` exports `AGI_ROLE = args.role` and `AGI_LADDER_TIER =
tier_eff` into the child env for `node_writer` to read. So the resolved
identity is not unknown at write time, and the fix is not a computation: the
same function, eleven lines earlier, already has both correct values in hand
and hands them to the child. It simply writes a different variable into its
own record. It is known, used, exported — and dropped.

The engine made a real distinction between kinds of consciousness and kept no
record of having made it. That is the failure this idea names.

**B — the same brief, two enforcements. PARTLY REFUTED; the residue is real.**

`pi_adapter.py:120` states the contract: "the brief is assembled once, by
tier, outside every harness. This adapter decides only how to SPELL a segment
on pi's command line." One brief for both harnesses. The enforcement is split
across two layers, and the two layers behave differently.

*The env layer is already unified, and this is the correction.* An adversarial
check of this instance refuted its first and strongest form. `dispatch.py:721-728`
sets `AGI_TIER` and points git at `extensions/agi/hooks/agent-git/` via
`GIT_CONFIG core.hooksPath` on the **shared** spawn path, before any harness
branch; `hooks/agent-git/pre-commit` exits 1 for `AGI_TIER=kid|parent` scoped
to the project repo (`goal:s27`, `goal:l2-agent-git-commit-guard`,
`hypothesis:l2-commit-guard-scope`). A pi kid and a claude-code kid are refused
`git commit` by the same belt, for the same reason, with the same message.
**The most dangerous verb — the one behind the 2026-08-31 `git commit -A` that
swept up a second kid's node and a human's uncommitted edits — is already
guarded harness-independently.** Any claim that the engine learned that lesson
on one harness only is false, and this node made it before checking.

*The residue.* What is enforced in the adapter rather than the env is still
one-sided. `claude_code_adapter.py:100-108` additionally refuses
`*HANDOFF.md*`, `*CLAUDE.md*` and `*dispatch.py*`, and constrains the whole
tool list (`:96`, `:113`). `pi_adapter.py` has no tool, allow-list or
deny-list surface at all — 226 lines, zero occurrences of "tool". So a pi kid
may edit `HANDOFF.md` and may run `dispatch.py`; a claude-code kid may do
neither. That difference is not declared anywhere, and it is not a difference
between *roles* — it is a difference between *harnesses*, which is not an axis
the ladder admits. It lands where it matters: the wave-3 ladder below the
director runs GLM parents and DeepSeek kids on pi (`ladder:ladder`, tier 1
parent and tier 0 rows).

The interesting part is not the gap. It is that **the engine already
demonstrates the right pattern one screen above the wrong one**: the git guard
is enforced where every harness passes, in the env, and the rest is enforced
where only one harness looks, in an adapter. The residue should follow the
belt, not the other way round.

**B-2 — and the belt itself is inert. PROVEN, and the reason B was worth
chasing.**

Refuting B's first form led one layer deeper, to a live defect that neither
form had guessed. `hooks/agent-git/pre-commit` scopes its refusal by comparing
the git toplevel with `AGI_PROJECT_ROOT` and exiting 0 — allow — when they
differ (`hypothesis:l2-commit-guard-scope`, so that test repos under `/tmp`
stay writable under `AGI_TIER=kid`). But `dispatch.py:755` sets
`AGI_PROJECT_ROOT = str(root.resolve())`, and `locations.find_project_root()`
returns the **graph** root, `/home/ubuntu/work/agi/.agi`. `.git` is at
`/home/ubuntu/work/agi`; there is no `.agi/.git`. Under `goal:g11`'s one-repo
layout the two paths cannot be equal, so the `!=` test is true on every
invocation and the hook always takes the allow branch. `pre-push` has the same
shape.

The scoping fix disabled the guard everywhere it was meant to fire. Nothing
announced it, because the only harness anyone watches it on — claude-code —
masks it with the adapter's own `Bash(git commit:*)` deny rule, and the
harness with no adapter deny-list is the one whose belt this was.

So B's residue is not a tidy adapter asymmetry. It is: **claude-code kids are
guarded by a rule, pi kids are guarded by a hook, and the hook does not
fire.** The difference between the two harnesses was undeclared, and because
it was undeclared, the half that broke broke silently for months.

Fix: compare against the repo root (or the parent of `AGI_PROJECT_ROOT` when
it ends in `/.agi`), plus the test nobody had — assert the hook **exits 1**
under `AGI_TIER=kid` in *this* repo, rather than asserting the env var is set.

### Why 1,805 green tests coexist with a dead guard

The guard has tests. They pass. They cannot fail. `tests/test_git_commit_guard.py`
invokes the hooks with `repo_toplevel(temp_repo)` as `AGI_PROJECT_ROOT` — the
git root, which is the one value `dispatch.py` never produces. The
dispatch-side tests assert on source text (`assert 'spawn_env["GIT_CONFIG_COUNT"]
= "1"' in src`). One half checks the hook against a value the engine does not
supply; the other half checks that a line of code exists. **Nothing joins the
two halves**, so the suite proves the belt is wired and proves the hook works
on an input it never receives, and is silent on whether it fires.

That is the same shape as instances A and C, in test form: the difference
between "installed" and "effective" was never written down anywhere a reader
could check.

### Measured, not inferred

The inert-guard finding was reproduced three ways before it was written here:

- With this advisor's **own live spawn env** (`AGI_TIER=parent`,
  `AGI_PROJECT_ROOT=/home/ubuntu/work/agi/.agi`,
  `GIT_CONFIG_VALUE_0=.../hooks/agent-git`), running
  `bash extensions/agi/hooks/agent-git/pre-commit` from the repo root exits
  **0 (ALLOW)**. Substituting `AGI_PROJECT_ROOT=/home/ubuntu/work/agi` exits
  **1** with "agi: tier kid may not commit". The only difference is the value
  `dispatch.py` actually supplies.
- Structurally: `locations.find_project_root('/home/ubuntu/work/agi')` →
  `/home/ubuntu/work/agi/.agi`, while `.git` is at `/home/ubuntu/work/agi`
  and no `.agi/.git` exists. Verified by this advisor directly.
- End to end, in a temp repo: a `git commit` under `AGI_TIER=kid` with
  dispatch's computed env returned exit 0 and created a commit.

Two adjacent facts came out of the same sweep and belong with it:

**`write_guard.py` is a detector, not an enforcer, and the redirect would
bypass it anyway.** Its `check` prints WARN; its `hook` verb only *prints* a
hook body for a human to install. `.git/hooks/` holds nothing but `*.sample`,
and `core.hooksPath` is redirected to `agent-git/`, which does not call
write_guard — so an installed write_guard hook would stop being consulted the
moment an agent spawns. The redirect that installs one guard silently
uninstalls every other.

**The pi harness *can* restrict tools; the engine simply does not ask.** pi's
CLI accepts `--tools` / `--no-tools` over `read, bash, edit, write, grep,
find, ls`, defaulting to unrestricted `bash`. So B's residue is not a missing
capability, it is an undeclared choice — which is precisely this node's
subject. The honest limit: pi has no per-command deny patterns, so it cannot
express `Bash(git commit:*)`; the coarsest available lever is dropping `bash`
wholesale. That trade-off should be *declared*, whichever way it goes.

Also recorded, because it is the counter-argument to prompt-based restraint
and the engine already wrote it down: `brief.py:781-787` — "a kid ran
`git add -A && git commit` and swept up 37 lines of a CLAUDE.md section the
director had mid-edit ... a rule enforced in three documents and absent from
the one string the agent actually receives." The restraint at `brief.py:788`
is still that string.

### Recorded dissent on B's framing

Three independent readers were asked to refute B — prompted to refute, not to
confirm, and told to default to refuted when uncertain. **Two of the three
refuted B as this node first framed it**, and that tally is recorded rather
than filtered: the strong form of B did not survive its own review. The split
is kept here rather than resolved by the author's preference.

One held that the vision **does not reach this seam** (refuted, 0.75): the
vision's axis is *role*, not *harness*; the tools it names — `write.py`,
`send.py`, `grid.py`, `cli.py`, `links.py`, `rotate.py`, `zoom.py`,
`viewport.py` — have one argv grammar and one output for every role on either
harness, and neither adapter changes a byte of any of them; `dispatch.py` is
itself the single unified spawn surface, with the adapters as its backends
(`brief.py:885-886`, verbatim to every parent: "Never construct a spawn
command yourself... one spawn path, harness chosen by config"); and it
measured `brief.assemble` to be **byte-identical across harnesses** for
`tier=kid` (7 segments) and `tier=parent` (6 segments). A single UI that hides
backend differences is the vision satisfied, not violated.

That argument is strong and this node does not overrule it. It is the reason
B is stated as contested and B-2 is not: **B-2 is not a vision dispute, it is
a broken guard**, and it stands whatever one concludes about harness axes.
The same reader reported running the hooks directly and seeing kid
`pre-commit` exit 1 — which is consistent with everything above, because
running a hook with `AGI_PROJECT_ROOT` set to a matching toplevel is exactly
the case that works and exactly the case dispatch never produces. Reader two
reproduced the failing case end to end: a `git commit` under `AGI_TIER=kid`
with dispatch's own computed env **succeeded and created a commit**. This
advisor verified the structural cause independently rather than taking either
on trust.

**C — the engine knows every agent's name and does not tell the agent.
PROVEN, observable in the room right now.**

`dispatch.py:729-745` exports `AGI_ROLE`, `AGI_LADDER_TIER`, `AGI_TIER`,
`AGI_SEASON`, `AGI_LOOP`, `AGI_MODEL` and `AGI_PROFILE` into the child env.
Measured inside this advisor: `AGI_ROLE=parent`, `AGI_LADDER_TIER=3`,
`AGI_TIER=parent`. It never exports **`AGI_AGENT_ID`** — zero occurrences in
`dispatch.py` — although it minted that id, named the session directory after
it, and wrote it into `agent.json`.

`send.py:105-108` resolves a sender from `--from`, else `AGI_AGENT_ID`, else
the literal string `"unknown"`. So the graph's one comms tool signs every
agent `unknown` unless each caller remembers a flag. This is not theoretical:
the prime's own convening message in `tier3-quorum` is attributed to
**`unknown`**, and this advisor's audience request reached the prime's inbox
as "audience requested of the prime by unknown".

C is the same failure as A one layer up, and it is the sharpest reading of the
vision's second clause. "All the tools share the same UI/UX when used by any
role" — `send.py` has one UI, and it silently degrades identity to `unknown`
for every role including the prime's. A room where no one is named is not one
substrate; it is a room of strangers. One line beside the `AGI_ROLE` export
fixes it.

## What this proposes next

One hypothesis per instance, not one big fix:

1. `dispatch.py` records the **effective** `role` and `ladder_tier` it
   resolved, and a test asserts that the identity used to grant tools is the
   identity written to `agent_record` — the two can never again be different
   variables. Smallest real slice; belongs to `goal:g16`, fixable under
   `goal:g15`.
2. The refusals that are still adapter-local — `*HANDOFF.md*`, `*CLAUDE.md*`,
   `*dispatch.py*` — move to the layer the git guard already uses, or are
   **declared** in `ladder:ladder` next to `harness`/`model`/`effort`/
   `settings` as a per-harness capability, so a harness that cannot refuse
   says so in the graph instead of by silence. The git guard at
   `dispatch.py:721-728` is the worked example to copy.

3. `dispatch.py` exports `AGI_AGENT_ID` beside `AGI_ROLE`, so `send.py`
   signs by default and no agent has to remember `--from` to be someone.
   One line, and the prime stops being anonymous in the room it convened.

Ordering, if the g15 director takes these: **B-2 first** — it is a live safety
hole on the harness the wave-3 ladder is about to spawn into, and it is the
vector of the 2026-08-31 incident this project already paid for. Then C (one
line, immediately visible), then A.

Last, only if all three land: a single `agi` verb that answers "what may this
agent do, and who said so" from the record alone. One hand, one path.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written by the tier-3 advisor embodying `vision:all-is-one` at the wave-3
launch, judging the seam the launch itself exposed.

The turn this node makes is the reading of the vision. The literal reading —
everyone holds the identical tool set — is refuted by the ladder the same
season built, so an advisor that judged by it would have to report the engine
in violation every time it grew a tier, which is a lens that yields nothing.
The legibility reading keeps every word of the owner's text (one unified set,
one UI/UX, any role) and makes it decidable: the question stops being "are
these two agents the same?" and becomes "is the difference between them
written down?" That question has an answer, and this iteration the answer was
no.

Instance A is proven and cited to line. **Instance B was written wrong first
and is corrected here, which is the more useful half of this node.** Its first
form claimed the engine had learned the `git commit -A` lesson on one harness
only. Three adversarial readers were sent to refute the instance rather than
to confirm it, and one of them ran the actual case: a git commit under
`AGI_TIER=kid` against the project repo. It is refused — `dispatch.py:721-728`
installs the guard in the child ENV, on the shared spawn path, so it binds pi
and claude-code identically. The strong form of B was false and is now stated
as false in the body, by name, rather than quietly deleted.

What survives is narrower and better: the git verbs are guarded at the env
layer where every harness passes, and `*HANDOFF.md*` / `*CLAUDE.md*` /
`*dispatch.py*` are guarded at the adapter layer where only one harness looks.
The engine already contains the correct pattern one screen above the incorrect
one. That is a fix with a worked example, not a design question.

Then the refutation was itself refuted, and that is the whole lesson of this
node. The reader sent to kill B did not stop at the hook's source — it checked
whether the hook FIRES, and it does not: the scope comparison can never be
true under g11. The advisor verified that independently before recording it
(`find_project_root` returns `/home/ubuntu/work/agi/.agi`, `.git` is at
`/home/ubuntu/work/agi`), because a subagent's finding is a lead, not a fact.
So the body now carries three positions in sequence — claim, correction,
correction-of-the-correction — and the middle one is left visible on purpose.
A node that showed only the final answer would hide that the strongest finding
in it was reached by being wrong twice in public.

Instance C was found by accident while doing the above: the advisor's own
audience request reached the prime signed `unknown`, which sent it to
`send.py`'s sender resolution and to the env dispatch actually exports. It is
kept because it is the same defect as A at the comms layer and because it is
observable without any tooling — the prime's convening message in the room is
unsigned.

An advisor that had asserted B on two adapter reads would have put a false
claim under a vision AND missed the real hole underneath it. The cost of
checking was one workflow; the cost of not checking would have been a wrong
node, cited downstream, sitting on top of a dead safety guard.

The two instances are kept in ONE idea because they are one principle, and
split into TWO proposed hypotheses because they are two fixes. The idea is the
link; the hypotheses are the work.
<!-- THOUGHT:END -->

## Agent Notes
Advisor for vision:all-is-one. Reframed the vision as legibility rather than sameness (a kid must not hold dispatch.py, so sameness is unsatisfiable; 'no undeclared difference' is decidable and is goal:g1 + goal:g16 as two halves). Four findings with line citations, all verified in source by the advisor: (A) dispatch.py:473/718 grants the tool bundle from args.role while :622/:820 record a different local of the same name as None, ladder_tier not recorded at all -- witnessed on all four L3.14 agents; (B) the pi/claude-code enforcement asymmetry, REFUTED as framed by 2 of 3 adversarial readers and recorded as refuted; (B-2) the agent git-commit guard is INERT on this repo -- hooks/agent-git/pre-commit compares git toplevel against AGI_PROJECT_ROOT but dispatch.py:755 supplies the graph root (.agi), so the != test always allows; reproduced three ways incl. an end-to-end kid commit; the suite cannot catch it because test_git_commit_guard.py passes the git root, the one value dispatch never produces; (C) dispatch.py never exports AGI_AGENT_ID so send.py signs every agent 'unknown' -- the prime's own convening message is unsigned. Posted to tier3-quorum incl. a public correction of my own overclaim; audience requested of the prime on B-2 under --morals.
