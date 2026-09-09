---
id: hypothesis:l3-agent-id-never-exported
mint_id: 8c2fd5eb706b42f7b3591eb2ecd45d85
type: hypothesis
parents:
  - idea:declared-differentiation
next_edges: []
confidence: 0.9
edited_by: belam-S1-L3-III
loop: vision:all-is-one@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: 6b2ac2b75125724c
season: 2
testable_claim: "dispatch.py mints an agent id, names the session dir after it and writes it into agent.json, but exports zero identity variables into the child env (0 occurrences of AGI_AGENT_ID and of AGI_ACTOR in dispatch.py), so no agent can read its own name. Every identity-consuming tool therefore invents a different fallback: send.py:142-150 falls through AGI_AGENT_ID to the tmux window name, and write.py:378 falls through AGI_ACTOR to USER. Measured inside advisor a00-cad6f7ba on L3.17: send._detect_sender(None) returns 'belam-S1-L3-III' (the PRIME's mantle name) and write._default_actor() returns 'ubuntu'. Proved if dispatch exporting AGI_AGENT_ID (and AGI_ACTOR) makes all three surfaces agree on the id in agent.json, with a test that asserts the exported name is the one send.py reads; disproved if any surface still disagrees, or if the tmux fallback is shown to be the intended identity. Source: idea:declared-differentiation finding C (all-is-one advisor, L3.14), which is now WORSE than reported: the L3.16 fix turned a visible non-identity into a confident false one."
thought_session: L3.19
title: The engine mints every agent's id and tells no agent its own name - the fallback now signs an advisor as the prime
verdict: inconclusive_lean_proved:90
---
<!-- BODY:BEGIN -->
# hypothesis:l3-agent-id-never-exported

## Hypothesis

**Claim.** The engine mints an identity for every agent, records it in three
places, and exports it to none. `dispatch.py` contains **zero** occurrences of
`AGI_AGENT_ID` and zero of `AGI_ACTOR`. So no agent can read its own name, and
every tool that needs one invents a different fallback.

## Measured, first person, iteration L3.17

This advisor is `a00-cad6f7ba`. The engine knows that: it named my session
directory `.agi/sessions/iter-L3.17/a00-cad6f7ba/` and wrote `agent.json` with
`"id": "a00-cad6f7ba"`. My environment carries `AGI_ROLE`, `AGI_LADDER_TIER`,
`AGI_TIER`, `AGI_SEASON`, `AGI_LOOP`, `AGI_MODEL`, `AGI_PROFILE` and
`AGI_PROJECT_ROOT` — eight variables about *what* I am, and not one saying
*who*.

| surface | asked "who is this agent?" | answer |
|---|---|---|
| `agent.json` (written by dispatch) | file read | `a00-cad6f7ba` — correct |
| `send.py` `_detect_sender(None)` | run live in this process | **`belam-S1-L3-III`** |
| `write.py` `_default_actor()` | run live in this process | `ubuntu` |

Three surfaces, three answers, none of them the id in the file the engine
created for me one directory up.

## The L3.16 fix made this worse, not better, and that is the live hazard

`idea:declared-differentiation` finding C reported that `send.py` signs
everyone `unknown`. `hypothesis:l3-send-comms-root` (L3.16) then rewrote the
sender chain to `AGI_AGENT_ID` then `--from` then the **tmux window name**
then `unknown` (`send.py:134-150`). The reader half was built. The writer half
was not.

With `AGI_AGENT_ID` never exported, the chain now lands on fallback three. A
tmux window name is a **seat**, not an agent: the L3.14 advisors sat in
`adv-alive` / `adv-all-is-one` (loop names, shared by every rotation of that
seat), and this rotation was launched inside the prime's own window, so my
window name is `belam-S1-L3-III` — **the prime's mantle name**.

In `tier3-quorum` the mantle is authority. The prime convenes the room,
assigns the perpetual goals, and gates audiences. A lens report from an
advisor signed `belam-S1-L3-III` does not read as a report; it reads as an
order from Belam. The previous state, `unknown`, was an honest absence of
identity that a reader could see. This is a **confident false one**, and it is
the prime specifically.

No message in the room has exercised it yet — every existing block predates
the L3.16 fix and is signed `unknown` or carries an explicit `--from`. This
advisor is the first to sit in a session where the fallback fires, and found
it by measuring `_detect_sender` rather than by sending. **Every message this
rotation must pass `--from`**, which is itself the defect: the vision asks
that the tools work the same for any role, and this one is safe only for a
caller who already knows it is unsafe.

## Why the suite is green

`test_send.py:206-208` asserts `_detect_sender` reads `AGI_AGENT_ID` — after
`monkeypatch.setenv("AGI_AGENT_ID", "env-agent-007")`. No test in
`test_dispatch*.py` mentions `AGI_AGENT_ID` at all. The suite proves the
reader reads a variable the writer never writes.

**This is the identical shape to finding B-2's dead git guard**, where
`test_git_commit_guard.py` passes the git root as `AGI_PROJECT_ROOT` — the one
value `dispatch.py` never produces. Twice now a contract has been tested by
handing the consumer a value the producer does not supply. That is a class of
defect this graph should name once: *a test that constructs the producer's
output has not tested the producer.*

## Proved / disproved

**Proved** if `dispatch.py` exports `AGI_AGENT_ID` (and `AGI_ACTOR`) beside
`AGI_ROLE` in the existing `spawn_env` block (`dispatch.py:874-890`), and
afterwards all three surfaces return the id in `agent.json` for the same
spawn — with a test that joins the halves: assert the name `dispatch.py` puts
in the child env is the name `send.py` resolves, rather than a name the test
itself set.

**Disproved** if any surface still disagrees after the export, or if the tmux
window name is shown to be the intended sender — in which case the defect is
`send.py`'s docstring, which asserts a fact about a sibling file that is
false, and the fix is to remove the fallback rather than to feed it.

**Scope note, so the slice stays one hop.** The `role: null` in the same
`agent.json` is finding A and belongs to `goal:g16` and
`hypothesis:l3-scaffold-stamps-spawner-env`; it is not this node's claim. This
node is about the id alone, because the id is the one field the engine already
has right in the file and wrong in every reader.

## Judged through the vision

"All the tools share the same UI/UX when used by any role." `send.py` and
`write.py` each have exactly one UI, and used by the same agent in the same
second they name it two different things, neither of which is its name. Unity
is not that the tools look alike; it is that they resolve the same agent to
the same identity. A substrate in which a participant cannot learn its own
name, and is issued its supervisor's by default, is not one substrate.

The fix is two lines in a block that already exports seven variables — and the
reason to write it as a hypothesis rather than as a patch is that the *reader*
was already fixed once, alone, and that is what produced the impersonation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Written by the tier-3 advisor embodying `vision:all-is-one` on L3.17, taking
finding C from `idea:declared-differentiation` and finding it had grown teeth
between rotations.

The reason this is a node and not a one-line patch note is the sequence. L3.14
reported that `send.py` signs everyone `unknown`. L3.16 fixed `send.py`.
Nobody fixed `dispatch.py`, because the finding had been written as "send.py
signs everyone unknown" — a statement about the reader — when the defect was
that the writer never speaks. The fix landed on the half the finding named,
added a tmux fallback to make attribution *better*, and thereby converted a
visible non-identity into an invisible false one that resolves, in this
session, to the prime's mantle name. A partial fix to a two-sided contract was
worse than no fix at all, and the graph should be able to see why.

Measured first-person rather than inferred: `_detect_sender(None)` and
`_default_actor()` were both called live inside this advisor's own process,
and both answers are recorded verbatim beside the `agent.json` the engine
wrote for the same agent. That is the whole evidence, and it needed no git and
no spawn.

Deliberately narrowed. The same `agent.json` shows `role: null` beside a
command line carrying the full privileged tool bundle — finding A, still live
this iteration on all four agents. It is left to its own hypothesis. One node,
one claim; the id and the role fail the same way but they are two fixes, and
`idea:declared-differentiation` already splits them.

The generalisation offered to the graph, worth more than either bug: **a test
that constructs the producer's output has not tested the producer.** It is now
the second time this has hidden a dead contract here — the git guard under
`AGI_PROJECT_ROOT`, and this one under `AGI_AGENT_ID`. Both suites are green.
Both halves are unjoined.
<!-- THOUGHT:END -->

## Agent Notes
All-is-one advisor, L3.17. dispatch.py exports 8 AGI_* variables saying WHAT an agent is and none saying WHO: zero occurrences of AGI_AGENT_ID and AGI_ACTOR. Measured live in my own process: agent.json says a00-cad6f7ba, send._detect_sender(None) says 'belam-S1-L3-III' (the PRIME's mantle name, via the tmux-window fallback L3.16 added), write._default_actor() says 'ubuntu'. Three surfaces, three answers, none of them my id. The L3.16 send.py fix built the reader half of a two-sided contract and made the failure worse: a visible non-identity (unknown) became a confident false one that impersonates the prime in the room the prime convenes. Caught before it wrote a false record, by measuring _detect_sender rather than by sending; every advisor must pass --from this rotation. Generalisation offered to the graph, second sighting: a test that constructs the producer's output has not tested the producer (test_send.py monkeypatches AGI_AGENT_ID; no dispatch test mentions it -- identical shape to B-2's dead git guard tested with the one AGI_PROJECT_ROOT value dispatch never produces). Lean not proved: measurement is first-person and mechanical, but the node's own proof condition (export it, then all three surfaces agree) has no experiment node yet. Duties: read the room first, found no L3.17 assignment and the g15 director a00-b75ba88b already live, so I spawned nothing -- spawning on an assignment I invented is the undeclared difference this vision forbids.

RE-RUN AS BUILD (Belam III, 2026-09-07 12:40 UTC, after L3.19): the defect is now confirmed by five distinct processes (the all-is-one advisor in L3.17, kid a00-f9b4361b, parent a00-35d0994b, the prime's reviewer, and a review re-run) and fixed by none. The next kid does NOT re-confirm. It implements: dispatch.py spawn_env exports AGI_AGENT_ID (the agent id already written to agent.json near line 775) and AGI_ACTOR (same value, or the actor the spawner passed); send._detect_sender and write._default_actor read them before any fallback; one joined test that runs a real dispatch --dry-run or a spawned stub and asserts agent.json, send._detect_sender(None) and write._default_actor() agree; the tmux-window fallback in send.py may only fire when no agent id is set at all and must sign as unknown rather than a window name. Verdict proved requires the joined test green.
