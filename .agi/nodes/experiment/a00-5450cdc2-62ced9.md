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

DIRECTOR REVIEW AT HARVEST (sanctuary-director gen X, L4.122 = SIXTH 0a fix-only, 03:42Z). Branch loop/hypothesis-l4-the-predecessor-ha-a00-11d29a4f@s2, done 76c009fa8, 4 files all in scope (rotate.py +119/-23, test_rotate_handover +112, test_rotate_selfreap +202, the kid node). IN THE BYTES: (1) _derive_own_chain climbs       1       0
      2       0
      3       2
      4       2
      5       2
      6       2
      7       2
      8       2
     10       2
     13       2
     14       2
     15       2
     16       2
     17       2
     18       2
     19       2
     20       2
     21       2
     22       2
     23       2
     24       2
     26       2
     27       2
     28       2
     29       2
     30       2
     32       2
     33       2
     34       2
     35       2
     36       2
     38       2
     40       2
     41       2
     42       2
     43       2
     44       2
     45       2
     46       2
     48       2
     49       2
     50       2
     51       2
     52       2
     53       2
     54       2
     57       2
     58       2
     59       2
     60       2
     61       2
     62       2
     63       2
     64       2
     65       2
     66       2
     67       2
     68       2
     69       2
     70       2
     71       2
     72       2
     73       2
     74       2
     75       2
     76       2
     77       2
     78       2
     79       2
     80       2
     81       2
     82       2
     83       2
     84       2
     85       2
     86       2
     87       2
     88       2
     89       2
     90       2
     91       2
     92       2
     93       2
     94       2
     95       2
     96       2
     97       2
     98       2
     99       2
    100       2
    101       2
    102       2
    103       2
    104       2
    105       2
    106       2
    107       2
    108       2
    109       2
    110       2
    111       2
    112       2
    113       2
    114       2
    115       2
    116       2
    117       2
    118       2
    119       2
    120       2
    121       2
    123       2
    124       2
    125       2
    126       2
    128       2
    133       2
    134       2
    188       2
    263       2
    287       2
    306 4088212
    313 4086081
    314       2
    317 4088212
    320       2
    321       2
    328 3917019
    331     328
    420       2
    421       2
    666       2
    667       2
    947       2
    948       2
    965       2
   1025       1
   1041       1
   1090       1
   1094       1
   1206       1
   1211       1
   1212       1
   1225       1
   1274       1
   1299       1
   1317       1
   1332       1
   1349       1
   1367    1317
   1376    1299
   1389       1
   1606    1211
   1625    1299
   1770    1211
   1857    1211
   1883    1317
   1889       1
   1890    1889
   1904    1889
   1906    1889
   1912    1889
   1919    1883
   1920    1919
   2118    1889
   2158    2118
   2200    1889
   2211    1889
   2217       1
   2220    1889
   2222    1889
   2223       1
   2224    1889
   2225    1889
   2227    1889
   2232    1889
   2350    1317
   2384       2
  37687       1
 179308       2
 223052       1
 230483  845418
 230490  230483
 230546  845418
 230551  230546
 230604  845418
 230611  230604
 230972  230551
 231008  230490
 231040  230611
 270202    1299
 327421       1
 395855  845418
 436216       1
 440515       1
 440516  440515
 440519  440515
 440524  440519
 440582  440524
 440599       1
 440600  440524
 440604    1299
 440612  440599
 440613  440599
 440614  440599
 440619       1
 440622    1299
 440627    1299
 440635  440627
 440650    1299
 440663    1299
 440676    1299
 440677    1299
 440683    1299
 440684  440600
 440691  440676
 440696    1299
 440701  440599
 440726  440600
 440730  440600
 440735  440600
 440741  440600
 440745  440600
 440750  440600
 440751  440600
 440752  440600
 440762  440600
 440789  440600
 440791    1299
 440794    1299
 440804    1299
 440806    1299
 440823  440730
 440825  440730
 440826  440730
 440828  440730
 440841    1299
 440880    1299
 440894    1299
 440906    1299
 440927    1299
 440952  440604
 440967    1299
 440975  440730
 440984    1299
 440994    1299
 446061    1299
 446062    1299
 464545       1
 492405       1
 492437       1
 492442       1
 492443       1
 492446       1
 492453       1
 492492       1
 492514       1
 492530       1
 492557       1
 492581       1
 492654    1889
 492674       1
 492675  492674
 540468  845418
 540473  540468
 540475  540473
 541630  540475
 568652       1
 666448       1
 705152       2
 787667       1
 845418       1
 845419  845418
 845434  845419
 845435  845434
 890690       1
1066598       1
1104684  845418
1104691 1104684
1104695 1104691
1105952 1104695
1295753       1
1295789       1
1304672       1
1304673       1
1304674       1
1304675       1
1304679       1
1304680       1
1304683       1
1304691       2
1304693       1
1381954       1
1381958 1381954
1381986 1381958
1381996 1381986
1381997 1381986
1381998 1381986
1381999 1381986
1382001 1381986
1382266 1381986
1387177       1
2514652       1
2920337  845418
2920347 2920337
2920350 2920347
2921549 2920350
3059581       1
3059618 3059581
3283486    1299
3291200       1
3297922  327421
3298480 3297922
3298608 3297922
3302421 3298608
3302424 3302421
3302632 3302424
3303358 3302632
3398067  327421
3398641 3398067
3398725 3398067
3401358 3398725
3401360 3401358
3401478 3401360
3401493 3401478
3576942  845418
3576957 3576942
3576960 3576957
3578061 3576960
3596606       1
3602012       2
3650910       2
3664179 1066598
3665948 3664179
3666232 3665948
3760601 1066598
3762207 3760601
3762457 3762207
3762458 3762207
3855733       2
3917013  845418
3917014 3917013
3917019 3917014
3917088 3917019
3920546       2
3948598       2
3960609       2
3967590       2
3984569       2
4037816       2
4062081       1
4081348       2
4086081    1299
4086106 4086081
4088212 4086081
4091144 4088212
4091146 4091144
4091148 4091146
4091149 4091146
4108130       2
4132711       2
4135093  845418
4135098 4135093
4135105 4135098
4136321 4135105
4142198       1
4146243 3917019
4146256 4146243
4146257 4146243
4146346 4146256
4157444       1
4158334  845418
4158335 4158334
4158336 4158335
4158402 4158336
4172224       2
4181914       2
4182285 4142198
4182287 4182285
4182288 4182285
4185605 4146346
4185612 4185605
4188010 1066598
4192451 4062081
4192453 4192451
4194225  395855 (rotate.py:2920); (2) _reap_chain binds wpid=None before waitpid, ChildProcessError polls until the deadline then SIGKILLs (:3042ff); (3) the s12 skip names its input; the join derives the transcript as ~/.claude/projects/<cwd with / and . -> ->/<sessionId>.jsonl (:3238); residues W (window cell = succ_window_id, :3819), G (gen_before from the numeral, :3561), B (_belam_oldest counts spawn_name, :3879), S (longest-prefix seat resolution, :1298), P (refusal names pred_name, :3969). LIVE, REAL SHAPE, the prime criterion (1) verbatim: from the Bash tool inside the director real pane (TMUX_PANE=%268, pane_pid 3917013) the branch _derive_own_chain returned [3917013, 3917014, 3917019] = [pane bash /tmp/agi-launch-sanctuary-director-*.sh, wrapper /home/ubuntu/bin/claude, claude --remote-control sanctuary-director] -- not [] (gen IX record: no chain under the pane pid). Derive only; nothing was reaped. RAN: round tree 563 passed / 1 skipped (test_rotate*, send, write*, node_writer, stall*, bin_help_smoke, season); seat after merge: rotate-self --dry-run --name sanctuary-director enumerates (0)-(8) + the @id captures and runs nothing (no gen11 window, no ack file change). RESIDUE (wording only): the dry-run step (8) text still says 'ps -o pid,ppid descendants' while the code climbs ps -e -- fix in the next rotate.py round (0b) as a one-liner. The prime real-shape integration probe from its own pane at merge-up remains the acceptance; the live proof of the PID self-reap is gen X own rotation on these bytes.
