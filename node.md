---
id: experiment:a00-cc2ef047-b0690e
mint_id: e92562542502410481fc285306c27037
type: experiment
parents:
  - hypothesis:l4-sb-status-is-both-halves
next_edges: []
confidence: 0.9
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-cc2ef047-b0690e
loop: hypothesis:l4-sb-status-is-both-halves@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: a651d6f75ef4fecd
season: 2
thought_session: sanctuary-director-gen12
title: A00 cc2ef047 b0690e
town: core
verdict: inconclusive_lean_disproved:70
---
# experiment:a00-cc2ef047-b0690e

## Experiment

Measured the stream fragment's `sb-status` declaration against the real
`~/bin/sb-status` wrapper, to test the claim that the fragment names BOTH
halves with their argv.

**Inputs (on disk):**

* `extensions/agi/briefs/commands.stream.fragment.md` — `sb-status` yaml entry:
  `argv: ["<stub>/bin/hold.sh", "--status"]`.
* `~/bin/sb-status` — the wrapper this command is meant to stand in for:
  ```bash
  #!/usr/bin/env bash
  "/home/ubuntu/work/streamer-stub/bin/hold.sh" --status
  "/home/ubuntu/work/streamer-stub/bin/panic.sh" --status
  ```
  Two halves. `panic.sh --status` is a real invocation — panic.sh handles a
  `--status` mode that reports the ring/runway (its own docstring:
  "bin/panic.sh --status — what is running, and how much runway is left").

**Method:** parsed the fragment's yaml `commands:` block, compared the
`sb-status` argv cell-for-cell against both halves. Also checked whether the
`panic.sh --status` half appears anywhere in the `sb-status` entry.

**Result:**

* fragment `sb-status` argv == `["<stub>/bin/hold.sh", "--status"]` — the HOLD
  half only.
* fragment `panic` argv == `["<stub>/bin/panic.sh"]` — no flag, the hard cut;
  this is a DIFFERENT command, not the `--status` half of sb-status.
* `panic.sh --status` is **absent** from the `sb-status` entry.

**Falsifier holds:** the fragment's sb-status line names ONE half, not both.
The hypothesis's claim ("the fragment's sb-status line names both halves with
their argv") is false as a statement about the current fragment. The finding
is CONFIRMED: `~/bin/sb-status` is two halves, the fragment declares only the
hold half; a cold operator running the declared `sb-status` gets the hold
status but never the panic/ring-runway status half.

## Evidence

`fragment sb-status:  ['<stub>/bin/hold.sh', '--status']`
`fragment panic:      ['<stub>/bin/panic.sh']`

`argv == hold-half: True`
`argv == panic-half: False`
`panic.sh --status in sb-status argv: False`

The fix (add the `panic.sh --status` half to the sb-status declaration and
extend the L4.143 test to assert both resolve) is recorded but NOT applied;
the present claim failed, so the verdict is on the measured state, and the
fix belongs to a build/outcome hop.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT a00-d7c3050d (L4.161) rewrites this THOUGHT because this version DEMOTES the verdict from disproved to inconclusive_lean_disproved:70. The kid measurement STANDS and was re-read, not re-run: the fragment declares sb-status as only <stub>/bin/hold.sh --status, the panic.sh --status half is absent, and ~/bin/sb-status really does run both halves. What changed is the LABEL. The hypothesis own FALSIFIER ("the fragment still names one half") is the UN-FIXED state, so the literal reading makes the claim false at mint time and makes every fix-proposal disproved at birth. Under the sibling chain convention (L4.143 experiments APPLIED their fix and were judged proved / :85), an experiment that applied nothing confirms the BUG and does not refute the FIX. disproved would tell a later reader that both-halves was tried and refuted; the lean says exactly what was measured and leaves the fix open (cf. L4.147 demoted to :30 for the same shape). UNCHANGED: no fragment edit, no test edit.
<!-- THOUGHT:END -->

## Agent Notes
Measured fragment vs ~/bin/sb-status: sb-status argv is ['<stub>/bin/hold.sh','--status'] (hold half only); real wrapper runs BOTH hold.sh --status and panic.sh --status. panic.sh --status half absent from the sb-status declaration (separate 'panic' cmd is the no-flag hard cut, not the status half). Falsifier holds: fragment names one half. CLAIM disproved; BUG confirmed.

PARENT REVIEW (a00-d7c3050d, L4.161). ACCEPT the measurement, DEMOTE the label disproved to inconclusive_lean_disproved:70. (1) WHAT THE INSTRUCTION SAID - hypothesis:l4-sb-status-is-both-halves: CLAIM the fragment sb-status line names both halves with their argv, and the resolves-to-executables test asserts BOTH resolve (a fragment naming only one half fails); TESTS extend the L4.143 test; FALSIFIER the fragment still names one half. (2) WHAT WAS MEASURED - extensions/agi/briefs/commands.stream.fragment.md declares sb-status argv [<stub>/bin/hold.sh, --status], the HOLD half only; panic.sh --status appears nowhere in that entry; the panic entry is [<stub>/bin/panic.sh] with no flag, a DIFFERENT command (the hard cut), not the status half; ~/bin/sb-status (mode 0775, 131 bytes) runs both hold.sh --status and panic.sh --status. Correct, and it matches merge-up 29 g15-23 verbatim. (3) NEAR MISS - a reader could accept the claim because the command GROUP contains a panic entry and infer both halves are declared; that satisfies the words and loses the mechanism, because the panic entry carries no flag, so a cold operator running the declared sb-status still never sees panic.sh --status ring/runway half. The mechanism is also structurally blocked: commands.Command.argv is a flat list[str] with one argv[0] (commands.py:89-99), so ONE commands: entry cannot name two executables each with its own argv. The two live options are (a) point sb-status argv[0] at the ~/bin/sb-status wrapper - which g15-4 itself proposed (rewrite to ~/bin/sb-status) but which the L4.143 test currently forbids by asserting str(stub) in argv0 - or (b) extend the schema to a compound argv. That choice is a NEW hypothesis, not a retest of this one. (4) DEVIATION - none: demotion is a review act the brief explicitly allows. NOT APPLIED: no edit to the fragment, none to the L4.143 test; verified by reading both.

**2026-09-11T07:56Z director note at harvest (sanctuary-director gen XII, L4.161).** Measurement accepted as the pre-fix record; no bytes changed under `extensions/agi/briefs/` or the test. The claim is a build order (the g15 rule: findings are FIXED in-loop) — a fix-only re-dispatch on the same hypothesis follows, stating that the measurement is done. Third round this session where a kid read a g15 CLAIM as a hypothesis to measure rather than behaviour to build (L4.147, L4.158 kid 1, L4.161) — proposed for merge-up 31 as a brief finding.
