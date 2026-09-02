---
id: hypothesis:verbs-before-keystrokes
mint_id: 6ee87e315e8447f4b9df4fea9546e725
type: hypothesis
title: Verbs before keystrokes
testable_claim: "Edit mode's nameable verb set is the thing with a right and a wrong answer; the modal shell is skin over it, and building the shell first would produce verbs shaped by keybindings rather than by operations."
parents:
  - goal:g13.1
next_edges:
  - experiment:both-callers-one-edit
scaffold_hash: a7b54ad286879bee
verdict: pending
confidence: 0.85
---

# hypothesis:verbs-before-keystrokes

## Hypothesis

`goal:g13.1` insists its two callers run the *same* operations: a human drives
a modal shell, an LLM serialises the whole session into one `&&`-joined
command, and *"a keystroke an agent cannot spell is a verb that exists only for
humans"*.

### Testable claim

If that constraint is real, **the nameable verb set is the artefact with a
right and a wrong answer and the shell is skin over it.** Building the shell
first would produce verbs shaped by keybindings — one-character, positional,
stateful — which is precisely the split `goal:g9.7` forbids on the read side.

Concretely: a verb layer plus a serial form can be built and falsified **with
no interactive code at all**, and the modal shell then binds keys to verbs that
already exist.

### What would prove it

- The `&&`-serialised form and the equivalent direct verb calls produce an
  **identical** accumulated edit — asserted on the object, not on the output.
- Every verb is nameable and spellable on a command line.
- `edit.py` contains **no file write**: every verb ends in `update_node`. If a
  change can be made in edit mode that `write.py` cannot make, edit mode is a
  bypass rather than a front end.
- Identity and completion fields (`id`, `mint_id`, `type`, `scaffold_hash`)
  are refused by every verb. Edit mode is not a loophole in the rule the kid
  brief already follows.
- Provenance lands: `edited_by` and `thought_session`, the latter reserved
  since `goal:g2.7` with nothing writing it.

### What would disprove it

- A verb that only makes sense as a keystroke — one that needs a cursor, a
  selection, or a mode to mean anything. That would show the operations
  genuinely differ between callers and the shell must come first.
- Needing a parser. `goal:g13.1` says if edit mode needs its own parser or its
  own file-writing code, the seam is wrong and `goal:g13` has not unified
  anything. Splitting on `&&` is not a parser; anything more would be.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The claim is about build ORDER, which is unusual for a hypothesis and is the
reason this one is worth stating rather than just doing. "Build the verbs
first" is a judgement that could be wrong, and it is falsifiable in a specific
way: if a verb turns up that only makes sense with a cursor, the order was
wrong and the shell should have led.

The second disproof clause is lifted from the goal's own text and is the
cheapest available check on scope creep. Splitting a string on `&&` is not a
parser; the moment quoting, nesting or precedence appears, it is one, and the
seam has moved.
<!-- THOUGHT:END -->
