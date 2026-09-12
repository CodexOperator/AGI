---
id: goal:g13.1
mint_id: 7a1f4d02c6b84e39ae5c30b7f2481d6e
type: goal
parents:
  - goal:g13
confidence: 1.0
edited_by: sensei-director
goal_id: G13.1
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds:
  - build:bin-node-writer
  - build:bin-locations
  - build:bin-write
  - build:bin-links
  - build:tests-test-write
status: active
tags:
  - goal
  - subgoal
thought_session: season
title: "G13.1: Edit mode: a modal shell over the read and write paths, so a human edit is an engine action"
---
**The write-side counterpart of the viewport, and the reason it is a separate
goal from it.** `goal:g9.4` gave the graph a *reader* a human can drive.
Everything a human does to *change* the graph is still a text editor and a
commit — which is to say, outside the engine entirely.

**The owner's statement of the problem, and it is the sharpest framing of it:**

> This allows us to edit configs or other nodes using engine-native paths
> rather than just lodge a completely stray and untraceable commit from my end.

**A hand edit is currently an undeclared write.** It bypasses
`node_writer.write_node`, so it bypasses the `scaffold_hash` stamp, the
evidence gate, schema validation, and every guard the write path exists to
apply. The node changes and nothing records that a human changed it or why.
Under `goal:g1`'s config-maxxing framing this is the last large improvised
action in the system: the engine's own owner is the one actor who cannot edit
the graph mechanically.

## What it is

**A modal shell, in the vim sense.** One command enters edit mode; from there
it **drives the CLI completely** until a submit signal ends it. Inside the
mode, keys and short verbs act on the node under the cursor; on submit, every
accumulated change goes out through `write.py` as one recorded operation.

**It composes nothing new.** The renderer draws, the writer writes, and this
goal is the interactive wrapper around them — *"relies on the renderer and the
writer to do everything in the background but just wraps it in a more dynamic
and interactive shell for ease-of-use."* If edit mode needs its own parser or
its own file-writing code, the seam is wrong and `goal:g13` has not actually
unified anything.

**Deliberately separate from the viewport.** `goal:g9.4` is the spiderweb view:
read-only, safe to run mid-iteration, `goal:g9`'s invariant. This is a
*different instrument* that happens to share a renderer. Folding them would put
a writer inside the one surface this project has promised is a reader — the
invariant `goal:g9` states in bold and that `viewport.py` enforces with a test
that greps its own source. **Edit mode may call the same renderer; the viewport
must never gain a write path.**

## The two callers are not the same, and that is the design

**For a human**, the mode is the point: modal editing, a cursor, live
re-render after each change, and one submit.

**For an LLM**, the owner notes the whole session serialises into a single
`&&`-joined command. That is not a lesser path — it is the *same* operations
with the interaction removed, and it is the reason the verbs must be nameable
rather than only keystrokes. **A keystroke an agent cannot spell is a verb that
exists only for humans**, which would split the write path exactly as
`goal:g9.7` forbids splitting the read path.

So: one set of named operations; a modal shell that binds keys to them; a
serial form that runs the identical operations non-interactively. The
`goal:g9.7` argument, applied to writing.

## What it must not become

**Not a second way to write.** If a change can be made in edit mode that
`write.py` cannot make, edit mode has become a bypass rather than a front end
— reintroducing the stray untraceable write it was built to eliminate.

**Not a text editor.** The unit is a node operation, not a buffer. Dropping to
`$EDITOR` for a body is legitimate; hand-editing frontmatter is the thing being
replaced.

**Provenance is the payoff, so it must actually be recorded.** A submitted
edit should say who made it and why — `thought_session:` is reserved in
frontmatter for exactly this (`goal:g2.7`, `goal:g10.1`) and nothing writes it
yet. An edit mode that produces an untraceable change has delivered the
convenience and none of the reason.

## Falsifier

Make the same node change three ways — by hand, through edit mode, and through
the serialised single-command form — and get byte-identical results, with the
hand edit being the only one that fails a validation the other two pass. Then
confirm the viewport still holds `goal:g9`'s reader-only invariant with edit
mode installed beside it.

## Depends on

**`goal:g13`'s write half**, which does not exist yet — `read.py`'s equivalent
landed 2026-09-02 and `write.py` did not. This goal is the first real consumer
of it, so it is also the thing that will say whether that seam is right.
**`goal:s31`** is the first defect it should be able to fix from the inside.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted 2026-09-02 at the owner's direction, alongside `goal:g1.10`, and filed
`active` on their explicit instruction that they will use it immediately —
accepting that it pushes `goals_active` further past the configured cap. Their
call, recorded rather than quietly absorbed.

Written as a subgoal of `goal:g13` rather than of `goal:g9` because its
dependency is the *writer*, not the view. It shares a renderer with the
viewport the way two programs share a library; the thing it cannot exist
without is `write.py`.

The paragraph insisting the viewport never gains a write path is the one most
likely to be eroded later, because "edit where you are looking" is an obvious
and appealing feature. It is recorded as a prohibition now, while nothing has
been built and the cost of the rule is zero — `goal:g9`'s reader-only
invariant is currently enforced by a test that greps `viewport.py` for write
surfaces, and that test is what would have to be deleted to break it.

The human/LLM symmetry section is the load-bearing design claim and it is
deliberately stated as a constraint on the verbs rather than as a feature. It
is `goal:g9.7` one surface over: there, one render for two readers; here, one
set of operations for two drivers. Stating it now is what stops edit mode
shipping as keystroke handlers with no nameable operations behind them, which
is the shape it would naturally take if built for the human case first.
<!-- THOUGHT:END -->

## Agent Notes
Sensei ask 12:04Z (master-sensei wake-audit 11:52Z): a one-line write.py replace body on config:rotations re-serialized two unrelated first_turn entries (em-dash -> \u2014: node_writer._render_value renders a list-of-dict entry as json.dumps with ensure_ascii=True, node_writer.py:338, on EVERY write verb) — brief hypothesis:l4-a-container-entry-in-frontmatter-round-trips-its-utf8-unchanged-through-every-write-verb (parents g13.1 + g15), fix fully known (one keyword argument, one round-trip test), dispatching as SL7.43.

SL7.43 harvested 12:19Z (Sensei ask 11:52Z, seat b6713f896): node_writer._render_value renders a list-of-dict frontmatter entry with json.dumps(i, ensure_ascii=False), so a container entry carrying non-ASCII round-trips byte-identical through every write.py verb and an unrelated one-line edit no longer rewrites a first_turn entry's em-dash to an escape; a pre-escaped entry normalizes ONCE to the literal characters on its next engine write (the four rotations.md entries will, on the next engine write of config:rotations). Kid experiment:a00-6b82217f-dbef27 proved 0.9 (fix reverted: both new tests fail on the claim; restored: pass); test_node_writer 75 + test_write 99 passed.
