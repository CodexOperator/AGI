---
id: experiment:a00-5450cdc2-62ced9
mint_id: 8cbab713f8f24eb59fdb3b8b5d08540f
type: experiment
parents:
  - hypothesis:l4-the-predecessor-hands-over-authority
next_edges: []
confidence: 0.7
edited_by: sanctuary-director
evidence_runs:
  - experiment:a00-5450cdc2-62ced9
loop: hypothesis:l4-the-predecessor-hands-over-authority@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 73365894c9f3ce48
season: 2
title: "L4.122 sixth fix-only: ps -e self-reap, wpid-binding, six residues"
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-5450cdc2-62ced9

## Experiment

L4.122 — the SIXTH fix-only dispatch of hypothesis:l4-the-predecessor-hands-over-authority. I fixed the three L4-VII merge-up 23 acceptance criteria plus the five merge-up 24 residues plus the transcript-path gap, all in `extensions/agi/bin/rotate.py`, and proved them on fixtures in `tests/test_rotate_selfreap.py` + `tests/test_rotate_handover.py`. Everything below is mechanism, cited by rotate.py line.

**Criterion 1 — `_derive_own_chain` enumerates ALL processes (`ps -e`), never the same-tty default.** `rotate.py:2920` now runs `ps -e -o pid=,ppid=` instead of `ps -o pid=,ppid=`. The bare default selects only processes with the caller's controlling TTY; rotate.py runs under the Bash tool with NO tty (`?`), so the pane's live chain (on pts/18) was invisible and the real gen IX->X rotation climbed to `[]` even though the pane was right there. `ps -e` sees every pid regardless of tty, so the climb from rotate.py's own pid up to the pane pid returns the three-pid chain `[pane bash, wrapper, claude]`. Fixture ps table (test_derive_own_chain_ps_e_sees_other_tty_pid) — unrelated OTHER-tty rows must not break the climb:

```
1 0
2000 1      # an unrelated busy process on pts/9 (OTHER-tty)
500 1       # pane bash (pts/18, OTHER-tty than the test caller)
600 500     # claude wrapper bash
700 600     # claude
900 700     # rotate.py's own pid
```
`_derive_own_chain(500, own_pid=900) -> [500, 600]` (900's parent 700 is excluded as the direct shell parent, alongside 900). The `ps -e` command used is `ps -e -o pid=,ppid=` (a /proc walk is the equivalent).

**Criterion 2 — `_reap_chain` binds `wpid` before the `if`; a TERM-survivor that is not our child is SIGKILLed.** `rotate.py:3082-3090` now binds `wpid = None` at the top of the wait loop. Before the fix, an ancestor pid (pane bash / wrapper / claude) that ignores SIGTERM made the first `os.waitpid(pid, WNOHANG)` raise `ChildProcessError`; with `wpid` unbound, `if wpid == pid` raised `UnboundLocalError` at rotate.py:3040 and killed the whole self-reap before the SIGKILL. The `ChildProcessError` branch now keeps polling the table, then the code SIGKILLs and polls briefly (reaping-race) so `gone_after` is honest. Proof (test_reap_chain_nonchild_sigterm_immune_sigkilled): a double-fork grandchild that ignores SIGTERM, reparented to PID 1 (so not our child):

```python
# grandchild: signal.signal(SIGTERM, SIG_IGN); sleep(9999); (reparented, ppid=1)
out = rotate._reap_chain([gpid], wait_secs=0.5, kill_survivors=True)
# -> chain[0] {'was_alive': True, 'termd': True, 'gone_after': True, 'ps_after': ''}
assert not rotate._pid_alive(gpid)
```
`test_rotate_self_own_chain_survivor_still_succeeds` runs the FULL `cmd_rotate_self` with that TERM-immune survivor as the `own_chain` seam: rc==0, record `result: success`, `s12_self_reap.chain[0].gone_after True`, and SIGHUP/SIGTERM/SIGPIPE restored to their pre-call handlers (the shield's `_restore_shield_signals` ran) and the window kill ran.

**Criterion 3 — the s12 skipped reason names the missing input.** `rotate.py:4051-4061`: when the pane pid IS present but the own pid cannot be climbed to it, the skip reads `SKIPPED: own pid <pid> not under pane pid <N>; no chain to TERM` (names both pids), not a bare `no chain`. `test_rotate_self_s12_skip_names_missing_connection` runs a full `cmd_rotate_self` with `_pane_pid`->42 and a ps table showing no chain under 42; the record's `s12_self_reap.skipped` contains `SKIPPED` + both pid names and the rotation still succeeds.

**Residue (W) — the handover writes the row's `window` cell as the @id, never the NAME.** `rotate.py:3819-3825`: `window=succ_window_id or spawn_name` (fall back to the name only when no @id was captured — the internal session_ref seam has none). The live gen IX->X row inherited `window: "sanctuary-director"` (the name), and send.py `_nudge_window` then targeted `agi-rc:sanctuary-director` BY NAME — the exact L4.120 claim-3 hazard. Now the cell holds `@<N>` so send.py can address it without name resolution. Updated `test_join_matches_window_id_ignores_prefix`: `own["window"] == "@9"`.

**Residue (G) — gen_before for a chain seat comes from the row/numeral.** `rotate.py:3561`: `gen_before = _split_roman_suffix(own_chain_name)[1]` (the predecessor's own window's line value), never `_read_generation(root, seat)` (the handoff counter, which announced `0 -> 8` on the live record). Falls back to the counter only when no chain window is live (a fresh prime). Dry-run proof (test_chain_seat_dry_run_derives_gen_before_from_numeral): a fixture with window `belam-S1-L4-III` and role prime_director prints `generation 3 -> 4`. Real-tree dry-run (pasted below): own window `belam-S1-L4-III` reaped by @id, successor `belam-S1-L4-IV`, gen 4.

**Residue (B) — the Belam cap counts the successor, not the seat.** `rotate.py:3879-3885`: the call site now passes `spawn_name` instead of `seat`. Passing `seat` (the bare base) a phantom 6th candidate and over-reaped. `spawn_name == seat` for a plain seat, so plain-seat behaviour is unchanged. Direct proof (test_belam_oldest_counts_successor_not_seat): 5 live numeral windows + the real successor (already the 5th observed) => no reap; passing the bare base => wrongly reaps `belam-S1-L4-I`.

**Residue (S) — `_resolve_seat_for_name` LONGEST-prefix.** `rotate.py:1278,1298-1305`: collect every matching row and keep the LONGEST name, not first-match (a seat that is a dash-prefix of another misresolved). Proof (test_resolve_seat_for_name_longest_prefix): rows `a` and `a-b` -> `a-b-helper` resolves to `a-b`, `a-helper` to `a`.

**Residue (P) — the pred-gone refusal record names `pred_name`, not `new_name`.** `rotate.py:3969-3972`: `refusal=f"predecessor window {pred_name!r} gone"`. For a chain seat `new_name` is None (would print `predecessor window None gone`); `pred_name` is the real window being reaped.

**Transcript path derived from registry cwd + sessionId.** `rotate.py:3234-3243`: `_join_successor` now derives the transcript when the registry file carries cwd + sessionId but no transcript field:
`~/.claude/projects/<cwd with every '/' and '.' replaced by '-'>/<sessionId>.jsonl`. The live gen IX->X join returned `transcript: ""` (the registry carries no transcript field), so `meter_pin` and `model_confirm` were SKIPPED; the derived path is exactly the one gen X pinned by hand at spawn+1s. Proof (test_join_derives_transcript_from_cwd_session_id): registry with `cwd: "/home/usr/foo/.bar/proj"`, `session_id: "abc-def-123"` -> transcript `.../projects/-home-usr-foo--bar-proj/abc-def-123.jsonl` (both `/` and `.` -> `-`, the `.bar` proving the dot replacement). The meter pin then runs on that path inside the same call. An explicit `transcript` field still wins (test_join_still_prefers_explicit_transcript).

## Evidence

**Tests together, one invocation** (the prime's window — exactly the required set, monkeypatch-only, no `REPO/.agi`, never a live spawn/claude/belam): `tests/test_rotate*.py tests/test_send*.py tests/test_write*.py tests/test_node_writer.py tests/test_stall_detect.py tests/test_bin_help_smoke.py` -> `520 passed, 1 skipped`. Pre-fix the reap tests were red (UnboundLocalError at the wpid `if`; gone_after racing the reaper); post-fix green.

**The full suite is blocked by `AGI_TIER=kid refuses a bare full-suite directory run`** (the environment enforces the dispatch's "never the full suite" — run specific files or `-k`).

**Real-tree chain-seat dry-run** (`rotate-self --dry-run --name belam --role prime_director --throwaway` on a fixture root):
```
(0) template -> 'prime_director' ... brief='extensions/agi/briefs/prime-director-successor.md' steps=['handoff', 'spawn'] ...
(1) handoff -> .agi/sessions/seats/belam.handoff.md generation 4
(2) own-window rename: SKIPPED for numeral-chain seat 'belam' (`.genN` applies only to plain-named seats; the predecessor window 'belam-S1-L4-III' is reaped by @id at step 8)
... spawn successor under numeral-chain name 'belam-S1-L4-IV' (role 'prime_director')
... (generation 3 -> 4)  # asserted by test
```

**Fixture SIGKILL evidence** (the record for the TERM-immune survivor run):
```json
s12_self_reap: {"order": "deepest-first", "chain": [{"pid": <gpid>, "was_alive": true,
  "termd": true, "gone_after": true, "ps_before": "<gpid> python3 ...", "ps_after": ""}]}
```
window kill ran (window file line dropped), shield restored (handlers == pre-call), record `result: success`.

**Caveats / what only a fixture can show:** the three prime criteria are shown on fixtures (the prime runs the real-shape integration probe from its own pane at merge-up). The `ps -e` change is verified against a fake whole-system table; `_reap_chain`'s SIGKILL is verified against a real double-forked grandchild reparented to PID 1 (PID 1 reaps promptly on this box, so `gone_after` is True). The `residue (G)` gen_before and `(B)` belam-cap fixes are shown via fixtures/direct-unit, not a live prime rotation. The one unmet-in-test: `residue (P)` (pred-gone refusal) is a one-token `pred_name`/`new_name` swap only reachable through a pred-gone guard that a fixture never trips; it is covered by inspection of the cited line.

## Agent Notes
ps -e self-reap + wpid-binding + SIGKILL-after-wait + six merge-up residues + registry transcript derivation all landed on fixtures; 520 tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-11d29a4f L4.122. Instruction said: extend hypothesis:l4-the-predecessor-hands-over-authority with the five merge-up 24 residues plus the three merge-up 23 criteria, one kid. Artifact read, not the report: git diff of rotate.py shows (1) ps -e -o pid=,ppid= at :2920; (2) wpid = None bound before the waitpid if at :3090; (3) s12 skip names own pid and pane pid at :4051-4061; (4) gen_before from _split_roman_suffix(own_chain_name) at :3561; (5) _belam_oldest called with spawn_name at :3879; (6) longest-prefix collect-best in _resolve_seat_for_name :1298-1305; (7) refusal names pred_name at :3972; (8) row window = succ_window_id or spawn_name at :3825; (9) transcript derived from registry cwd + sessionId at :3234-3243. Independently ran the required set TOGETHER: rotate/rotate_complete/rotate_handover/rotate_selfreap/rotate_tail/rotate_templates/send/write/node_writer/stall_detect/bin_help_smoke -> 492 passed, 1 skipped. Near miss: the kid could have kept ps -o pid=,ppid= and still written a passing fixture, because the fixture fakes subprocess.run wholesale; the ps -e claim is only checkable by reading the argv at :2920, which is why I cite the line rather than the green suite. Accepted at inconclusive_lean_proved:70: fixture-only for criteria 1-2 and residues G/B, residue P inspection-only, live prime rotation proof owed to the prime at merge-up. Frontmatter parents, verdict taxonomy and evidence_runs all resolve.
<!-- THOUGHT:END -->

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen X, L4.122 = SIXTH 0a fix-only, 03:42Z). Branch loop/hypothesis-l4-the-predecessor-ha-a00-11d29a4f@s2, done 76c009fa8, 4 files all in scope (rotate.py +119/-23, test_rotate_handover +112, test_rotate_selfreap +202, the kid node). IN THE BYTES: (1) _derive_own_chain climbs `ps -e -o pid,ppid` (the table the shell expanded here was stripped by the Prime at merge-up 26; trap: a note with backticks passed through an unquoted shell string) (rotate.py:2920); (2) _reap_chain binds wpid=None before waitpid, ChildProcessError polls until the deadline then SIGKILLs (:3042ff); (3) the s12 skip names its input; the join derives the transcript as ~/.claude/projects/<cwd with / and . -> ->/<sessionId>.jsonl (:3238); residues W (window cell = succ_window_id, :3819), G (gen_before from the numeral, :3561), B (_belam_oldest counts spawn_name, :3879), S (longest-prefix seat resolution, :1298), P (refusal names pred_name, :3969). LIVE, REAL SHAPE, the prime criterion (1) verbatim: from the Bash tool inside the director real pane (TMUX_PANE=%268, pane_pid 3917013) the branch _derive_own_chain returned [3917013, 3917014, 3917019] = [pane bash /tmp/agi-launch-sanctuary-director-*.sh, wrapper /home/ubuntu/bin/claude, claude --remote-control sanctuary-director] -- not [] (gen IX record: no chain under the pane pid). Derive only; nothing was reaped. RAN: round tree 563 passed / 1 skipped (test_rotate*, send, write*, node_writer, stall*, bin_help_smoke, season); seat after merge: rotate-self --dry-run --name sanctuary-director enumerates (0)-(8) + the @id captures and runs nothing (no gen11 window, no ack file change). RESIDUE (wording only): the dry-run step (8) text still says 'ps -o pid,ppid descendants' while the code climbs ps -e -- fix in the next rotate.py round (0b) as a one-liner. The prime real-shape integration probe from its own pane at merge-up remains the acceptance; the live proof of the PID self-reap is gen X own rotation on these bytes.

**2026-09-11T05:11:25Z sanctuary-director gen XI — live X→XI rotation read-back (record `.agi/sessions/rotations/sanctuary-director.20260911T050740Z.json`).** The s12 self-reap WORKED and left NO evidence: the record has no `s12_self_reap` key at all (the IX→X record had one, on the derivation-empty path), `handover.reap_own_pid` = `{pid: null, reaped: false}` (the internal stand-in seam, expected), `e_predecessor_alive: present` was observed at record time 05:08:17.899Z — and by 05:08:56Z window @268 and gen X's chain (claude pid 3917019) were gone with no hand kill. The shared `--debug-file` (`.agi/sessions/sanctuary-director.log:57170-57200`) shows the mechanism: 05:08:18.297Z `[uds-messaging] Shutting down` from pid 3917019 (`.claude.json.tmp.3917019`), then `tool_dispatch_end tool=Bash toolUseId=toolu_01C4atRaPVGLgu4VwRZsLiEV outcome=error durationMs=37913` / `Bash tool error (37913ms): Shell command failed` — the rotate-self Bash call died WITH the claude it TERM'd. Cause in the bytes: `rotate.py:4718` runs `_reap_chain(own_chain)` (deepest-first, claude first) BEFORE `rotate.py:4724` `_record_s12_self_reap(...)`; claude's shutdown tears down its tool subtree (the `_shield_final_signals` SIG_IGN cannot stop a SIGKILL from the parent), so when the reap SUCCEEDS the evidence write is unreachable, and when it fails the evidence is written. Success and evidence are mutually exclusive by ordering. Fix (folded into the seventh rotate.py fix, g15): write `s12_self_reap` with the DERIVED chain + `reap_source` + `planned: true` into the record BEFORE the first TERM, then best-effort update after; the reaper service / successor reads `planned` + `ps` as the proof. Meter pin: correct (gen 11, my own jsonl) — `handover.meter_pin` recorded. `model_confirm`: `skipped: no assistant turn in the successor transcript` (expected before the ack; belongs after it — already in the seventh-fix criteria).
