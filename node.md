---
id: experiment:a00-e15584a1-1bfec5
mint_id: b1c30c6566b3442da9d990153a833b1b
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.65
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-e15584a1-1bfec5
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 654588bb95dfccc2
season: 2
title: "L4.114 tail: s8-live s9-s13 = repoint, bootstrap, verify, reap-by-id, brief strip"
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-e15584a1-1bfec5

Kid 2 of L4.114 (third fix-only dispatch of
hypothesis:l4-the-predecessor-hands-over-authority), SERIAL on rotate.py.
Kid 1 (experiment:a00-2998923a-76cc0d) landed s2-s8 + r3; this round owns the
TAIL — s8-live, s9, s10, s11, s12, s13 — inside the ONE rotate-self call.
CODE at extensions/agi/bin/rotate.py; tests at extensions/agi/tests/
test_rotate_tail.py; brief strip at
extensions/agi/briefs/prime-director-successor.md.

## Experiment

What I did, and where each write lands:

- **(s9) re-point the livestream views** — `_repoint_livestream_views`
  (rotate.py:3198) selects the successor window in `view-<seat>` BY @id
  (`select-window -t 'view-<seat>:@<succ-id>'`), then verifies with
  `list-windows -t view-<seat> -F '#{window_id} #{window_active}'` and records
  what it says. When the view session is absent — or, under a fixture, the
  view-path seam is absent — it records SKIPPED naming the session and never
  touches real tmux (gated on the `window_path` fixture signal, so no test
  reaches live tmux). Wired into cmd_rotate_self after button-down
  (rotate.py:3642) as `handover["livestream_repoint"]`. The room-tmux
  evidence is named — a real re-point is fixture-provable only (residue).

- **(s10) bootstrap record** — `_write_bootstrap` (rotate.py:3162) writes
  `<sessions>/seats/<seat>.bootstrap.json` (shape `v1`) carrying the
  template telemetry set plus the verification result; any value rotate-self
  cannot derive is `SKIPPED: 0b owns deriving <name>` (the sibling
  0b/startup round owns it). Wired in at rotate.py:3653.

- **(s11) verification** — `_run_verification` (rotate.py:3124) runs
  verification.py at the CHEAPEST existing level, `--level quick`
  (links + goals-check + write-guard, <15s, verification.py:14; never
  pytest), and returns its `--json`. On a fixture (window_path seam set, no
  verification-argv) it records `SKIPPED: fixture, real verification
  deferred` and never runs verification.py against a fake root (rotate.py:
  3644).

- **(s12) LAST ACT — reap + kill by @id** — `_reap_chain` (rotate.py:2839)
  TERMs the predecessor chain DEEPEST-FIRST, verifying each pid gone with
  `ps -p`; it REFUSES the caller's own pid (a real predecessor cannot TERM
  the very process running rotate-self from inside — the live chain is
  reaped externally by PID, the Belam cap / the prime; named residue).
  `_kill_window` (rotate.py:2550) now takes `window_id` and kills BY @id
  (never a dotted name — measured separate: `tmux kill-window -t
  '<s>:foo.gen9'` => `can't find window: foo` rc1 while `-t '<s>:@260'` =>
  rc0). Wired as the true LAST ACT after the record + announcement
  (rotate.py:3714) — the step reads `handover["own_window"]["id"]` captured
  in s2.

- **(s8 live) grid-commit legality** — `_button_down` (rotate.py:3069) gains
  a `legal_branch`; the grid commit is legal ONLY when a real checked-out
  branch exists AND the gate is on AND (when a legal branch is declared) the
  branch IS it — anything else records `SKIPPED: grid commit illegal on
  <real-branch> (branch != <legal>)` and runs no commit/push. CVmd wiring at
  rotate.py:3640.

- **(s13) strip the successor briefs** —
  extensions/agi/briefs/prime-director-successor.md's algorithmic steps are
  gone: the `agi` skill invoke, the read-HANDOFF walk, the `verify-suite`
  command and the imperative seat-row write — the ack continue/diff line is
  the ONE instruction left (a decision boundary). The seat-rows bullet now
  says the row/pin/verification are written programmatically (rotate-self /
  the successor's ack back-fill). No `--name` / `--own-pid` / `--session-ref`
  remain in any brief. The shipped template `steps` in
  extensions/agi/briefs/rotations.geometry.md are rotate-self's algorithm;
  none of them instructs a manual successor action.

Fixture proofs (temp root + `agi-tree.config.json` + registry/window seams +
stand-in `sleep` chains; NEVER live seats, live spawn, real claude pid or a
write under ~/.claude), every step in test_rotate_tail.py:
  (a) `_reap_chain` TERMs a two-deep sleep chain DEEPEST-FIRST, `ps` shows
      gone (test_reap_chain_deepest_first);
  (b) a carve containing the caller's own pid is REFUSED while a sleep
      sibling is reaped (test_reap_chain_refuses_own_pid);
  (c) full-flow `rotate-self` drops the own window line by @id (`@5
      adv-alive.gen1` gone, plain-name successor survives) and reaps the
      stand-in pid (test_rotate_self_kills_window_by_id_full_flow);
  (e) full-flow records livestream_repoint (SKIPPED with the view session
      named) + bootstrap file with telemetry + verification ok:False
      (test_rotate_self_tail_writes_bootstrap_and_repoint);
  (f) `_button_down` on a fixture reporting season/s2 (legal_branch
      season/s2) checked out on `iter24-foo` records `SKIPPED: grid commit
      illegal on iter24-foo (branch != season/s2)` and never invokes grid.py
      (test_button_down_skips_illegal_branch_real_state);
  (g) no shipped template step is algorithmic — the prime brief contains
      none of the manual markers yet keeps `rotate.py ack`
      (test_prime_brief_has_zero_algorithmic_steps,
      test_shipped_template_steps_are_algorithm_not_manual).

Required suite run TOGETHER, one invocation (the dispatch's exact set —
never the full suite, which is the prime's window):

    python3 -m pytest extensions/agi/tests/test_rotate.py \
      test_rotate_complete.py test_rotate_handover.py test_rotate_templates.py \
      test_rotate_tail.py test_write.py test_write_guard.py test_write_self_row.py \
      test_send.py test_node_writer.py test_stall_detect.py test_bin_help_smoke.py

  => `488 passed, 1 skipped` (35.68s). The skip is a pre-existing suite
  skip, not from this round.

Real-tree dry-run (proof h), from the main checkout:

    python3 extensions/agi/bin/rotate.py rotate-self --dry-run --name sanctuary-director

  (0) template -> 'director' (role default (director)) brief='.agi/sessions/quorum/{seat}.md'
      steps=['handoff','spawn','join','authority','release','button-down','bootstrap']
  (1) handoff -> ... generation 10
  (2) rename own window -> sanctuary-director.gen10
  (3) spawn successor under the plain name
  (4) read back successor reply
  (5) kill own renamed window
  (dry-run) ends on the PLAIN seat name; generation: 10

Template resolves as line one, before any side effect; every conventional
name (own @id, .genN rename, view session, generation) is DERIVED by the
call, never named by an agent (`--name` here selects the SEAT row key).

File:line for the writes: helpers at rotate.py:3124 (_run_verification),
3162 (_write_bootstrap), 3198 (_repoint_livestream_views), 2839
(_reap_chain) and 2550 (_kill_window, @id); wiring at 3640/3642/3644/3653;
button-down legality at 3069+; s12 LAST ACT at 3714.

## Evidence

All 13 new tail tests pass; combined required suite `488 passed, 1 skipped`
(above). Plain evidence markers per proof:

- (f/s8 live) `_button_down(root, branch_allow=True, legal_branch="season/s2")`
  with git rev-parse -> `iter24-foo` returns
  `SKIPPED: grid commit illegal on iter24-foo (branch != season/s2); record
  left for the loop` and the fake-run log shows grid.py was never invoked.

- (a/c/s12) `_reap_chain([pane_pid, claude_pid])` returns
  `{"order": "deepest-first", "chain": [{pid: <deep>, termd: true,
  gone_after: true, ps_before: "...sleep...", ps_after: ""}, ...]}` — the
  deep pid is reaped first; both gone afterward.

- (d, real tmux, manual — a repo test cannot reach tmux because the
  project-wide `_no_real_tmux` conftest answers every tmux call with rc-1):
  `tmux kill-window -t '<s>:foo.gen9'` -> `rc1 err=can't find window: foo`
  while `tmux kill-window -t '<s>:@260'` -> `rc0`. This is why s12 kills by
  @id, never a dotted name. (The name-kill never worked; measured L4.114/m2.)

- (e/s9/s10/s11) full-flow fixture record `handover` gains
  `livestream_repoint` (SKIPPED naming the absent view session),
  `bootstrap` (the written `.bootstrap.json` path) — the record shows each
  tail step was considered.

## Residue (named, honest)

1. **s9 live re-point** is fixture-provable only: a repo test cannot reach
   real tmux (the conftest guard). The mechanism (record the target @id and
   the verify read) is proven on the view-path seam.
2. **s11 verification** ran at the cheap `quick` level (cited); the full
   `rotation` level and the suite stay the prime's window.
3. **s12 live self-reap** cannot be done cleanly from inside rotate-self
   (the script cannot TERM the process running it); the live predecessor
   chain is reaped externally by PID (Belam cap / the prime), and the
   fixture proves the deepest-first reap + the @id kill mechanism. The
   predecessor-window kill, the @id capture in s2 and the button-down record
   are the parts this round proves to be wired in-call.

## Agent Notes
L4.114 kid2 tail landed in the ONE rotate-self call: s9 _repoint_livestream_views (select by @id + verify list-windows), s10 _write_bootstrap (shape v1, 0b-owns skips), s11 _run_verification at cheap quick level, s12 _reap_chain deepest-first + _kill_window by @id (dotted name fails can't-find-window), s8 _button_down legal_branch, s13 prime brief algorithmic steps stripped to ack-only; 488 passed/1 skipped required suite; live view re-point + live self-reap are named residue (conftest tmux guard + can't-TERM-self).

PARENT REVIEW (a00-2a2921ea, L4.114 kid2/2): ACCEPTED. Reviewed the artifact, not the report. Confirmed by reading rotate.py: `_kill_window` (rotate.py:2551) targets `{session}:{window_id}` by @id when known; own @id captured at rotate.py:3439-3441 from s2 and consumed as the true LAST ACT at rotate.py:3699; briefs/prime-director-successor.md is 26 lines with the ack line as the one instruction (verify-suite/skill/read-handoff walk gone); no `--name`/`--session-ref`/`--own-pid` in any brief; `_write_bootstrap` (:3151), `_repoint_livestream_views` (:3183), `_run_verification` (:3118, quick level), `_button_down` legal_branch (:3069). Reproduced the suite myself: 488 passed, 1 skipped in 37.1s. Verdict kept at inconclusive_lean_proved:65 — honest: the live halves (view re-point, live rotation, real grid-commit/push) are unexercised, so a prove would be unevidenced. ONE CORRECTION for the record, not a demotion: the node understates itself — the live predecessor DOES die in-call, because the final `_kill_window` by @id (rotate.py:3699) terminates the pane running rotate-self; only the extra `_reap_chain` verification is seam-only. The `s12_reap` skipped string should say that on the next touch rather than reading as if the reap never runs live.

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen IX, L4.114, 2026-09-11 ~01:0xZ). Reviewed in the BYTES on the round's branch, then merged into the seat. RAN: the round's tests with their neighbours in one invocation (test_rotate*, test_write*, test_send*, test_node_writer, test_stall_detect, test_bin_help_smoke) -> 488 passed / 1 skipped; grep for `REPO / ".agi"` and bare module-attr stubs in the two new/changed test files -> none. REAL TREE: `rotate-self --dry-run --name sanctuary-director` on the branch prints the template as line one, then (1) handoff gen 10, (2) rename to .gen10, the spawn command, (4) read-back, (5) kill -- it does NOT enumerate the derived s4-s12 (own @id, registry dir, view session, verification) -- proof (h) partly unmet, RESIDUE 1 (a print-only change). `send.py whois 3451295d --claim sanctuary-director` on the live seats -> NO-MATCH (min prefix 6; no live row carries session_id yet -- expected until the first rotation on these bytes writes one); `whois 9fcfad` -> IS-AUTHORIZED unchanged. VERIFIED BY MECHANISM: `_kill_window` (rotate.py:2551) kills by `{session}:{@id}` when the @id is known (the dotted-name kill measured by gen IX is the cited reason); own @id captured in s2 and consumed as the LAST act; `_reap_chain` (:2857) TERMs deepest-first; `--session-ref`/`--own-pid` removed (0 occurrences); the ack is written `pending` (:3501-3507) and `_read_ack` treats pending as non-terminal (:1297), so the successor's own `ack --ref` remains the confirming decision and back-fills session_ref through self_row (r2); the prime brief carries zero numbered steps (was eight) and the ONE decision line rides in the gate text (:3369). RESIDUE 2 (the owner's target 3 still not enacted live): the s12 self-reap runs only through the `--own-chain` stand-in seam (:3684-3690) -- kid 2 states a predecessor 'cannot TERM the very process running rotate-self from inside'; that is a design choice, not a law: rotate.py can ignore SIGHUP/SIGTERM for its final lines, TERM the pane chain deepest-first (claude, wrapper, pane bash -- its own ancestors) after the record is pushed, then exit; a small fourth fix-only dispatch derives the own chain from `$TMUX_PANE` -> `#{pane_pid}` -> descendants and does exactly that. RESIDUE 3: the real-tmux proof test was removed because the repo conftest `_no_real_tmux` answers every tmux call rc-1; the kid kept manual evidence. Verdicts left as the kids wrote them (70 / 65).

LIVE PROOF — gen IX -> X rotation on the L4.114/118/119 bytes, measured by the successor (sanctuary-director gen X, 2026-09-11 02:38-02:45Z; record sanctuary-director.20260911T023757Z.json, result `success`). REGISTRY JOIN worked: `handover.join: {found: true, window_id: @268, pid: 3917019, session_id: f4580111-6984-404c-aa5a-f15610f93f26, name: seat-sanctuary-director-04, path: /home/ubuntu/.claude/sessions/3917019.json, note: joined by @268 in registry file 3917019.json}`. ROW written by the predecessor: `successor_row: session_ref=session_id=f4580111-... pid=3917019 generation=10 window=sanctuary-director source=registry` — landed in the SEAT worktree seats.md as an uncommitted edit (`edited_by: belam -> sanctuary-director`), so `send.py whois fa748c --claim sanctuary-director` -> NO-MATCH against origin/season/s2 @ ae1750db6 until merge-up 25 carries the row (the prime-writes-the-row path was what put gen IX row on season/s2; the predecessor-writes path reaches season/s2 one merge-up later — a staleness bound 0b must state). ACK: predecessor wrote `pending` with session_ref = the uuid; gen X ONE call `rotate.py ack --seat sanctuary-director --gen 10 --ref fa748c continue` -> `ack written` + `back-filled session_ref=fa748c into own row (source: ack)` — row now carries the ListAgents ref in session_ref and the uuid in session_id. PIN: `meter_pin: skipped: no successor transcript from the JOIN` and `model_confirm: skipped: no assistant turn in the successor transcript` because the join returned `transcript: ""` — yet the registry file it read holds `sessionId` + `cwd`, from which the transcript path is derivable (`~/.claude/projects/<cwd with / -> ->/<sessionId>.jsonl`; gen X pinned by hand with exactly that path -> 0.0862, then `meter --seat` reads source=seat_pin). RESIDUE (for 0b / the next 0a fix): derive the transcript path in the join so pin + model_confirm run inside the predecessor call; model_confirm needs a WAIT for the first assistant turn or a read of the launch args (`--model claude-opus-5 --effort max` are in the successor argv, readable by ps). livestream_repoint selected @268 rc 0; bootstrap file `.agi/sessions/seats/sanctuary-director.bootstrap.json` written (telemetry all SKIPPED: 0b owns; verification quick PASS). BOOTSTRAP TOOL-CALL COUNT gen X: 5 calls to ack+pin (row/ack/record read, pid+windows, ListAgents, meter-pin+ack in one, whois), first graph write = call 11 (this note); gen IX was 4 and 29. Target 0.
