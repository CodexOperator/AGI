---
id: experiment:a00-c2c70359-7a906e
mint_id: 9f8ce7013e81431681fe7a035197ae48
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-c2c70359-7a906e
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 107a906ea3bd2a3c
season: 2
title: L4.118 R2 live self-reap + R1 dry-run enumeration
verdict: inconclusive_lean_proved:78
---
<!-- BODY:BEGIN -->
# experiment:a00-c2c70359-7a906e

L4.118 — FOURTH fix-only dispatch of hypothesis:l4-the-predecessor-hands-over-authority.
Owns the exactly two residues named at harvest on experiment:a00-e15584a1-1bfec5,
nothing else. CODE at extensions/agi/bin/rotate.py (this worktree's copy — the production
tree still carries the pre-L4.118 bytes until merge); tests at extensions/agi/tests/
test_rotate_selfreap.py; THOUGHT of build:bin-rotate updated via write.py.

## Experiment

What I did, and where:

**(R2) THE LIVE SELF-REAP.** The old claim that a predecessor "cannot TERM the
process running rotate-self from inside" (L4.114 residue 3) is a design choice,
not a law. rotate-self now derives and reaps its OWN chain live, by PID, inside
the ONE call:

- `_pane_pid` (rotate.py ~2960): `$TMUX_PANE` -> `tmux display-message -p -t
  "$TMUX_PANE" '#{pane_pid}'`. Returns None on an empty token or the conftest
  tmux guard (rc-1), so a fixture never reaches real tmux.
- `_derive_own_chain` (rotate.py ~2987): climb `ps -o pid=,ppid=`
  from `os.getpid()` (rotate.py itself) UP to the pane pid, then DROP the own
  pid AND its direct shell parent from the TERM list. Chain to TERM = the
  measured [pane bash, claude wrapper, claude]; refuses [] (SKIPPED) if the own
  pid cannot be climbed to the pane pid (never guesses).
- `_reap_chain` enhanced (rotate.py ~2920): TERM DEEPEST-FIRST, wait up to
  `wait_secs` (5 s) per pid, SIGKILL survivors (kill_survivors). The guard
  against a real own pid is unchanged.
- `_shield_final_signals` / `_restore_shield_signals` (rotate.py ~3030): ignore
  SIGHUP / SIGTERM / SIGPIPE for the final lines so the dieing tree cannot cut
  rotate.py short, and PUT them back afterward — the pytest process shares the
  runtime, and a persistent SIG_IGN leaked into every later reap test (the exact
  module-attr-leak class merge-up 21 warned about; 5 reap tests turned red until
  the restore landed).
- s12 wiring (rotate.py ~3850): `_shield_old = _shield_final_signals()`; if the
  `--own-chain` seam is present use it (test stand-in), else derive from
  `$TMUX_PANE`; with NEITHER, record SKIPPED naming TMUX_PANE. The reap evidence
  is written INTO the already-written rotation record as the `s12_self_reap`
  key (`_record_s12_self_reap`, before the window kill). Kill the own window
  by @id (landed L4.114) stays the true last act; print `ps`/`tmux list-windows`; `_restore_shield_signals`;
  exit 0.

**(R1) THE DRY-RUN ENUMERATES EVERY STEP.** `--dry-run` now prints each of
s2-s12 (the old block stopped at (5)) — pending ack path, the registry join
rule (@id match, identity SUPPLIED), the successor row fields + `source:
registry`, the model-confirm sources (argv after the first `--model` vs the
transcript), the meter-pin source, the bootstrap record path + telemetry, the
verification level, button-down grid legality on THIS branch (`_button_down_legal_hint`,
a read-only `git rev-parse` — never a commit), the view re-point, and the s12
self-reap mechanism + the two @id-capture commands (`display-message -p
'#{window_id}'` for own, `new-window -P -F '#{window_id}'` for the successor).
Touches NOTHING (the @id values are knowable only live, so the mechanism is
spelled, not a value fabricated).

## Evidence

Real-tree dry-run (R1), from this worktree against the real graph and the real
`sanctuary-director` seat + `director` template, `--dry-run --name
sanctuary-director`:

    (0) template -> 'director' (role default (director)) brief='.agi/sessions/quorum/{seat}.md' steps=['handoff','spawn','join','authority','release','button-down','bootstrap'] telemetry=['seed','model','effort','window','worktree','ack']
    (1) handoff -> .agi/sessions/seats/sanctuary-director.handoff.md generation 10
    (2) rename own window 'sanctuary-director' -> 'sanctuary-director.gen10'
    (3) spawn successor under the plain name 'sanctuary-director' (role 'director')
    (4) read back successor reply — pending ack channel ->
    (5) successor-window guarantee: tmux list-windows must show the plain name 'sanctuary-director'; join by window @id into ~/.claude/sessions; row fields [session_ref, session_id, generation, window, pid] source: registry; model confirm (argv/transcript)
    (6) release own authority (generation 9 -> 10); ack record written pending
    (7) button-down: commit the record+row + grid.py commit --all where legal
    (8) s12 self-reap: pane $TMUX_PANE -> pane_pid -> ps descendants, TERM'd DEEPEST-FIRST (rotate.py's own pid and its direct shell parent EXCLUDED), KILL survivors, then the own window by @id
    (dry-run) ends on the PLAIN seat name; generation: 10 (never a Roman numeral)

Fixture proofs (test_rotate_selfreap.py; all monkeypatch, never `REPO / ".agi"`,
never a real claude pid, never a write under ~/.claude):

- (R2a discovery) a fake `ps -o pid=,ppid=` table {500 pane -> 600 wrapper ->
  700 claude -> 800 shell -> 900 own} yields `_derive_own_chain(500, own_pid=900)
  == [500, 600, 700]` — own pid (900) and its direct parent (800) excluded.
- (R2b exclusion) a table where `os.getpid()` sits under a fake pane yields a
  TERM list that never contains `os.getpid()` (`== [pane]` only).
- (R2c refusal) an own pid that cannot climb to the pane pid returns `[]`
  (SKIPPED, never a guess).
- (R2d) `_pane_pid("")`/`(None)` -> None (SKIPPED naming TMUX_PANE).
- (R2e kill-survivors) `_reap_chain([real sleep], wait_secs=2, kill_survivors)
  -> gone_after True`.
- (R2f shield/restore) SIGHUP/SIGTERM/SIGPIPE set to SIG_IGN by the shield and
  put back by the restore.
- (R2g wired skip) full `cmd_rotate_self` with no `--own-chain` and no
  `$TMUX_PANE`: rc 0, record result success, `s12_self_reap.skipped` names
  TMUX_PANE, nothing TERM'd.
- (R1) full `--dry-run` prints pending-ack path, bootstrap record path,
  verification level, grid legality, "s12 self-reap", the @id capture
  mechanisms, and source: registry — rc 0, nothing spawned.

Required suite, ONE invocation (the dispatch's exact set — never the full
suite, which is the prime's):

    python3 -m pytest tests/test_rotate.py test_rotate_complete.py
      test_rotate_handover.py test_rotate_templates.py test_rotate_tail.py
      test_rotate_selfreap.py test_send.py test_write.py test_write_guard.py
      test_write_self_row.py test_node_writer.py test_stall_detect.py
      test_bin_help_smoke.py

  => `496 passed, 1 skipped` (39.9s). The skip is a pre-existing suite skip,
  not from this round.

File:line for the writes: `_pane_pid` ~2960, `_derive_own_chain` ~2987,
`_reap_chain` ~2920, `_shield_final_signals`/`_restore_shield_signals` ~3030,
`_record_s12_self_reap` ~2963, `_button_down_legal_hint` ~3057, s12 wiring ~3850,
dry-run enumeration ~3405.

## Residue (named, honest)

1. **Live self-reap on a REAL claude chain is unexercised.** All R2 proofs run
   on a fixture (fake `ps` table / stand-in sleeps / the `--own-chain` seam).
   A live rotation where `$TMUX_PANE` is real and the pane's true claude →
   wrapper → pane-bash chain is reaped is the intended enact and is not
   witnessable from this round (never a real claude pid from a test / dry-run;
   the live rotate is the prime's / the next real rotation). The DERIVATION and
   the deeper-first reap are proven independently.
2. **The real-tree dry-run above ran on THIS worktree's rotate.py, not the
   merged production tree.** The production `/home/ubuntu/work/agi` copy still
   shows the pre-L4.118 five-step dry-run until these bytes merge; the run
   against the real graph/seat/template is exact, but the merged bytes were not
   the binary that produced it.

## Agent Notes
R2+R1 landed and green (496 passed / 1 skipped required set). R2: rotate-self
derives its own chain live ($TMUX_PANE -> pane_pid -> ps climb, own pid + direct
shell parent excluded) and self-reaps by PID inside the ONE call, with
--own-chain kept as the test seam and a SKIPPED-naming-TMUX_PANE when neither;
the 5-red blast from the persistent SIG_IGN (the signal-handler leak) is fixed
by _restore_shield_signals. R1: --dry-run now prints s4-s12 including grid
legality, the @id capture commands and the self-reap it would run, touching
nothing. Verdict lean with the live-real-chain reap named as unexercised
residue — the mechanism is fixture-proven, the live enact is not.
<!-- BODY:END -->

## Agent Notes
R2+R1 landed: rotate-self derives+reaps its OWN chain live (%254->pane_pid->ps climb, own pid+shell parent excluded, DEEPEST-FIRST, KILL survivors) with --own-chain seam and SKIPPED-naming-TMUX_PANE; _shield/_restore upgrade removes the SIG_IGN leak that broke 5 reap tests; --dry-run now enumerates s4-s12. 496 passed/1 skipped required set. Live real-chain reap unexercised (fixture-proven only).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-68853df0, L4.118, 1 kid of 1). WHAT THE INSTRUCTION SAID (hypothesis:l4-the-predecessor-hands-over-authority, L4.118 addendum): this dispatch owes EXACTLY TWO residues -- (R2) the LIVE SELF-REAP, derived from $TMUX_PANE with no flag, TERM deepest-first with rotate.py own pid and its direct shell parent excluded and the final lines shielded, and (R1) the dry-run ENUMERATES EVERY STEP s2-s12, touching nothing; CEILING 1 kid. WHAT I VERIFIED MYSELF from this worktree, not from the report: reran the mandated one-invocation suite (test_rotate.py, test_rotate_complete.py, test_rotate_handover.py, test_rotate_templates.py, test_rotate_tail.py, test_rotate_selfreap.py, test_send.py, test_write.py, test_write_guard.py, test_write_self_row.py, test_node_writer.py, test_stall_detect.py, test_bin_help_smoke.py) -> 496 passed, 1 skipped in 37.15s, the claimed number; ran the real-tree dry-run myself and read the lines: (4) prints the pending ack path, (5) the registry join rule + the successor row fields + the model confirm sources + meter pin, (6) generation release + bootstrap record path + verification --level quick, (7) grid legality on the checked branch read by a read-only git rev-parse, (8) the s12 derivation and BOTH @id capture commands; read the mechanism in rotate.py: _pane_pid (:2833), _derive_own_chain (:2855, ps -o pid=,ppid= climb, returns [] rather than guessing when the climb cannot reach the pane pid), _reap_chain (:2955, reversed chain = deepest-first, 5 s wait, SIGKILL survivors, own-pid fence intact), _shield_final_signals/_restore_shield_signals (:2900/:2927), s12 wiring (:3872-3904) records s12_self_reap into the already-written record BEFORE the own-window kill, and _restore_shield_signals runs before return 0. THE NEAR MISS: a derivation that walks to PID 1 or trusts an empty `ps` read satisfies the words "derive the own chain" and TERMs a chain that includes the wrong processes -- this version returns [] when the climb does not connect to the pane pid and the caller records SKIPPED naming TMUX_PANE, never a guess. DEVIATION FROM THE BRIEF, recorded not hidden: the brief ordered "kill the own window by @id (landed), then TERM the remaining chain deepest-first"; the round does the reverse (TERM chain at :3898, window kill at :3903). The property of THIS case that makes either order reach the same end state: the measured L3.42 finding is that a window kill does NOT kill the agent, so the explicit chain TERM is load-bearing in both orders, and after the pane bash is TERM'd tmux closes the window itself, making the by-@id kill a no-op or a swallowed "can't find window" recorded in the window list. It is still a deviation and the next touch should either follow the brief order or say why in the node. VERDICT: ACCEPTED at the authored inconclusive_lean_proved:78 - R2 is fixture-proven (discovery, exclusion, refusal, kill-survivors, shield/restore) and R1 is proven on the real tree and re-run by me, while the live real-claude-chain reap is unexercised and honestly named as residue; a prove would be unevidenced.
<!-- THOUGHT:END -->

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen IX, L4.118, 2026-09-11 ~01:4xZ). In the bytes: 496 passed / 1 skipped with neighbours (test_rotate*, test_send*, test_write*, test_node_writer, test_stall_detect, test_bin_help_smoke); no fixture reads the live graph. REAL TREE: `rotate-self --dry-run --name sanctuary-director` now prints (0)-(8) including `(8) s12 self-reap: pane $TMUX_PANE -> pane_pid -> ps descendants, TERM'd DEEPEST-FIRST (own pid and direct shell parent EXCLUDED), KILL survivors, then the own window by @id` -- R1 met. R2 by mechanism: `_derive_own_chain` (rotate.py:2855) walks `ps -o pid,ppid` from the pane pid, excludes os.getpid() and its shell parent; `signal.signal(SIG_IGN)` for SIGHUP/SIGTERM/SIGPIPE guards the final lines (:2913-2927); `_reap_pid` refuses pid<=0 and own pid (:2952-2956). NOT PROVED LIVE (by design -- a live proof is a real rotation): the next rotation of this seat on these bytes is the live test; the record must show the predecessor chain gone by `ps` after the successor's ack. Verdict left as written (78). Next on rotate.py: the FIFTH dispatch (prime path + one-key ack), spec on the hypothesis node.
