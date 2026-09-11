---
id: goal:g15.13
mint_id: ee292e2e1a4144a5a1073484c2b95217
type: goal
parents:
  - goal:g15
  - build:bin-sensei
next_edges: []
confidence: 0.6
edited_by: sensei-director
goal_id: G15.13
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 23018ecc27ff3773
season: 2
seeds:
  - hypothesis:l4-rotate-out-audit-mirrors-wake-audit-over-the-predecessor-window
  - hypothesis:l4-the-audit-classifier-is-derived-and-the-window-is-bounded-by-the-record
status: active
tags:
  - goal
  - subgoal
  - l4
  - sanctuary-director
thought_session: sensei-director-genI-L1
title: "G15.13: sensei.py rotate-out-audit — the outgoing predecessor's rotate-out calls are classified by the tool that classifies the successor's wake"
town: core
---
<!-- BODY:BEGIN -->
**`sensei.py rotate-out-audit --seat S [--gen N]`: the OUTGOING predecessor's rotate-out calls are classified by the same tool that classifies the successor's wake.** Owner, 2026-09-11 15:5xZ, verbatim in `doc:l4-owner-decisions`: "check the logs and calls of the outgoing predecessor for all roles, not just the successor … minimize number of tool calls needed to rotate out". The Sensei's §2 names the exact shape: "the mirror of wake-audit: the window is [last merge-up or last owner turn -> record success]".

## Why this exists

- `goal:g15` is the parent because this is an optimization of the seat protocol's rotate-out cost, done in-loop as the perpetual goal prescribes; the Sensei measured three rotate-outs BY HAND with no tool behind them (sanctuary-director 135144Z = gen XIV out, sanctuary-helper 152548Z = gen III out, belam 140328Z = gen IX out) — the hand measurement is the cost this goal removes.
- `build:bin-sensei` is the parent because `sensei.py wake-audit` (LANDED merge-up 36, L4.225; `--gen` defaulting to the latest record + `## facts` labels in L4.240) is the mechanism this goal mirrors: `wake_audit()` classifies the successor's calls from the first tool_use to the first real act; the outgoing side is the same classifier run over the predecessor's transcript from its last real input to the record's `recorded_at`. A second tool with its own classifier would drift from the first; the goal is a SUBCOMMAND of the same file reusing `classify_call`'s helpers.

## Testable claim (a build order — measure, implement, prove)

1. `sensei.py rotate-out-audit --seat S [--gen N] [--transcript PATH]` exists as a subcommand (no new `bin/` file). `--gen N` names the generation that ROTATED OUT; default = the latest record's `b_generation.before`.
2. The PREDECESSOR's transcript is resolved from the rotation records, never from the newest transcript in a slug dir (that one is the successor's): the previous record of the same seat (`b_generation.after == N`) carries `handover.join.transcript`; fallback `~/.claude/sessions/<pid>.json` for a pid in the outgoing record's `s12_self_reap.chain` / `handover.reap_own_pid`; neither resolving is a named refusal (exit 2), and `--transcript` is the explicit override.
3. The window is [the last real input -> the record's `recorded_at`]: every assistant tool_use after the LAST user turn that is not a tool_result (the last merge-up reply or owner/Prime turn) to the end of the transcript; the window's start turn index, its timestamp and the call count are printed.
4. Each call is classified: (a) a step rotate-self already performs or could pre-fill (re-measured §0 numbers `verify`/the record already holds; `git status`/`log` re-reads of what `rotate-self --dry-run` prints; the seats-row/meter/ack/bootstrap reads of fields the record carries) — the row names the record field or rotate-self step it duplicates; (b) a hand poll or read of a record or a pane (`ls`/`cat` under `sessions/rotations`, `tmux capture-pane`, `rotate.py status`, `ps`, read-backs of the handoff just written); (c) protocol learning (`-h`, source/log greps); (d) the genuine decision (the card edit — where-it-stops/banked —, the `rotate-self` invocation, the ack, the one-line rotation report).
5. Output mirrors `wake-audit`: header, window bounds, `counts: a= b= c= d=`, one row per call with the duplicated field/step label; exit 2 with a named reason on no seat row / no record / no transcript / no template.
6. Tests (`test_sensei_rotate_out_audit.py`, run WITH `test_sensei_wake_audit.py` + `test_sensei.py`): a fixture transcript + fixture records where a hand re-measured count -> (a) naming the record field; `tmux capture-pane` -> (b); `rotate.py -h` -> (c); the card edit and `rotate-self` -> (d); a transcript with no user turn after the first -> the whole transcript is the window; the predecessor transcript resolved through the previous record, refused when absent.
7. LIVE PROBE in the parent's verdict: the subcommand run on the three held rotations, counts pasted, one hand-classified call per rotation checked against the tool's row.

**Falsifiers:** a call the Sensei classified by hand that the tool classifies differently with no rule naming why; the predecessor transcript resolving to the successor's; a window that starts at the transcript head when a later user turn exists.

**FILE SCOPE:** `extensions/agi/bin/sensei.py` (new subcommand; shared helpers refactored, not copied), `extensions/agi/tests/test_sensei_rotate_out_audit.py` (new). EXCLUDED: `rotate.py`, `config:rotations`, the hooks, any `bin/` file. **CEILING:** 1 parent, up to 2 kids.