---
id: hypothesis:pass9-0926-residue-batch
mint_id: d7bfef8f63cf4643b00b05951656a880
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: belam
scaffold_hash: d3bfe856ea3b2fd5
season: 2
testable_claim: Every PASS 9 residue is closed in place (node text corrected with a THOUGHT; code through the five new defect hypotheses and follow-ups on the named existing ones) and PASS 10 finds none of these rows again.
thought_session: belam-S2-L5-X
title: "PASS 9 residue batch: trunk @9e16b8ed90 -> season2/main 49d2b6f6a (assigned: director-engine)"
town: core
---
# hypothesis:pass9-0926-residue-batch

# hypothesis:pass9-0926-residue-batch

# PASS 9 residue batch -- trunk @9e16b8ed90 -> season2/main 49d2b6f6a (09-26)

assigned: director-engine (engine rows); the research rows route through thought-master to director-thought. Minted by belam-S2-L5-X at PASS 9 step (6).

## Measured
| | |
|---|---|
| reviewed | 56 rounds (51 hypotheses / 86 experiments + 5 engine-delta over 55 paths; 3 rotate test files excluded) · 28 chunks x 2 at <= 6 pi (the user@ guard) · agi-merge-up-review --harness pi-free · 13:47-17:22Z · 0 USD (credits 13.75 before and after) · 2 empty-response reviews re-run alone (p9retry1/2), 1 unstructured verify return read by hand (band-byte-audit), 3 runaway reviewer greps killed by the PASS monitor |
| verdicts | 52 accept_with_residue · 4 demote · 0 RED (0 secret-pattern hits on 14,165 added lines; 0 deletions in 236 files; links 0 broken; goals byte-identical; smoke 4,525 = TIP's node files; RED keyword hits in 12 run files, all negations, a test fixture or an env-var name) · verify ruled 289 first-reviewer defects: 182 stand, 107 refuted, +218 it found |
| merge | season2/main 2c6e8953c -> 49d2b6f6a (merge --no-ff of TIP 9e16b8ed90; tree == TIP but the 3 season2/main key rows in posts.md) · local-maxxing/main a288a071d -> 9e16b8ed9 (ff) · grid 28 versions on season2/main, 0 demoted |
| runs | .agi/sessions/workflows/runs/mur-p9chunk{1..28}of28 + mur-p9retry{1,2}/{review,verify}_<round>.json (box-local on local-town) |

## CLAIM
Every row below is closed in place -- node text corrected with a THOUGHT, code through the five new defect hypotheses and follow-ups on the named existing ones -- and PASS 10 finds none of them again.

## Demotes -- the claim is false in the bytes (re-open the named hypothesis)
| round | mechanism (at TIP 9e16b8ed9) | state |
|---|---|---|
| engine-delta-1 + hypothesis:a-rounds-named-node-set-is-its-dispatch-time-ids-never-a-kid-supplied-parent | cmd_done overwrites the dispatch-time record (cli.py:1602 `rec["parent"] = args.parent`) and hands it to _round_named_node_ids (:1740, read at :2140): a kid's --parent re-enters the named set and a foreign round-editable node is swept (reproduced on the real schemas); DH.390's d24c16a51 is defeated by it; test_cli.py:2101 builds a rec cmd_done never produces. And [command]/[cron]/[ladder] carry neither written_by nor round_commit, so cli.py:2196 returns True for 3 .geometry types; the conjunct's only .geometry evidence (config:geometry-seats) is an id that exists nowhere | open |
| engine-delta-5 | the capture latch: _force_capture returns 'capture-latched' silently (rotation_alert.py:865-866), _captive_rotate returns True regardless (:965-970), main early-returns (:1485-1488) -- every captive prompt after the first is mute | FIXED on the trunk at b6438bd7e (DH.395; :979-990 returns `which in ("captured","capture-no-spawn")`), the file the live hook runs -- PASS 10 reviews it |
| hypothesis:l4-suite-green-on-main-the-18-reds-after-h2-and-rc-propagation-are-fixtures-that-learn-the-resolver-plus-one-no-repo-predicate-fix | CLASS A's one production change is inert: git_common_root is `-> Path` and returns root on every failure branch, so the `is not None` guard at locations.py:289 is a tautology; the cause at a00-25355804-78e3b9.md:43-46 never existed in this lineage (fixed before the round, 3195931fc^); the no-git-path test cannot fail (test_suite_live_checkout.py:40; a /tmp leak at :44); lean_proved:80 / :50 still credit it | open |

## Code defects -- director-engine (new)
| defect | where (at TIP) | node |
|---|---|---|
| the declared context suite runs outside every engine conftest: `pytest <.agi/context>` with no env= -- no suite lock (two --suite runs overlap), no real-process / live-config guard, the caller seat's AGI_* reaches the tests; DH.392's .agi/context/conftest.py (4ca024b00, after TIP) refuses model loads only | bin/verification.py:1524-1551 | hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards |
| write.py's schema gate is CLI-only: submit() never calls it, and rotate.py:9518 writes list cells straight through write.submit | bin/write.py submit() · bin/rotate.py:9518 | hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb |
| heal can reseat a worktree post into MAIN: _seat_geometry_dir falls back to MAIN when the worktree dir is missing; the launcher is retried WITHOUT cwd on any TypeError; a failed launch leaves the launch file and the whole prompt in /tmp (`rm -f "$0"` runs only if the shell runs the file) | bin/heal.py:3199-3204 + _seat_geometry_dir + the launch-file writer | hypothesis:heal-never-reseats-a-worktree-post-into-main |
| the .agi/bin shadow guard is vacuous: test_agi_bin_absent.py:24 asserts a doubled path, not the one driver.sh consults, so it cannot fail -- the paid-for H0 rule (a stale copy wiped nodes/ once) has no biting test | tests/test_agi_bin_absent.py:24 | hypothesis:the-agi-bin-shadow-guard-bites-at-the-path-driver-sh-resolves |
| a round's commit can write the inputs of the gate that scopes it: _round_scope_ok returns True for any path outside .agi/nodes/ bar config.json and quorum (cli.py:2090-2103), so a round's done commit wrote the schema cells the gate reads; a corrupt schema opens the gate silently (cli.py:2185-2186 `except Exception: pass`), untested | bin/cli.py:2090-2103, :2185-2186 | hypothesis:a-rounds-commit-never-writes-its-own-gate-inputs-and-an-unreadable-schema-refuses |

## Follow-ups on existing hypotheses -- director-engine
| residue | where (at TIP) | on |
|---|---|---|
| logs.non_append='rename' returns True on the copytruncate base, so the in-place truncate still runs under a non-append writer (the NUL hole), and test_crons_log_cap_declared_scope.py:218/:232 asserts the refusal is ABSENT; the nested prune unlinks before any size check; cmd_apply writes the crontab before the new cell refusals; rotations=0 empties the base with no archive; _ARCHIVE_RE/_NESTED_RE dead; log-cap-holds' test_f4 no longer discriminates and its docstring states the removed mechanism | crons.py:589, :784, :716, :683, :1346-1349, :488, :623 · test_crons_log_cap_long_lived_writer.py:5, :143-180 | crons-log-cap-bounds-archives-and-prunes-only-its-own-files · every-in-place-log-trim-refuses-a-non-append-holder · log-cap-holds-while-a-long-lived-writer-keeps-the-log-open |
| the late-reap key is `late-reap\|{seat}\|{succ_id}` (two records sharing a successor share one age); late-reap-first-seen.json is never pruned; _state_save's temp name is fixed (two heal processes share one temp inode); no test starts from a non-empty state | heal.py:920, :836 | heal-late-reap-bound-covers-an-unparsable-record-and-stale-pin-logs-once |
| the process guard: the kill guard exempts the PARENT pid; it patches the subprocess module attribute while rotate.py binds _RUN at import (rotate.py:5094); os.open('/proc/...') is unfenced; os.system / execv / posix_spawn / pty.spawn / killpg unhooked; function-scoped (import-time escapes); its own red-first probe arms a real SIGKILL of pid 1 | tests/conftest.py:637-719 · tests/test_conftest_guard.py:135-146 | rotate-term-grace-tests-never-touch-a-real-process-or-the-live-config |
| memory_alarm.py:22 docstring names the old alerts.log; --alerts-log (:178) bypasses the cap guard; :62/:83/:190 path literals; crons.py:456 logs_dir() is Path.home()/"logs" beside box.logs_dir; crons.py:450 ALERTS_FILE copies the logs.alerts_file cell; guard-init.sh --status reads the old path (the owner's file, banked) | memory_alarm.py · crons.py:450, :456 | memory-alarm-cli-is-declared-and-its-log-is-capped |
| the captive capture beside the fixed latch: capture_chain_log is undeclared in [ladder].md, so any ladder without it refuses capture by name (92 of 134 live seat worktrees at TIP; each gains the cell at its next season2/main sync); the chain log is /tmp/agi-rotation-<uid>/capture-chain.log, outside the managed log cap; its handle is never closed (:899); read-then-unlink of the failure marker drops a concurrent append (:849-850); the fail-closed and chain-failure prints bypass render() (:884-886, :1466-1472) and no test binds the call sites to render() | hooks/rotation_alert.py · context/schemas/[ladder].md | the-captive-capture-never-writes-into-the-live-card-and-a-failed-forced-rotation-is-logged-and-latched · rotation-alert-t1-capture-cluster-templated · a-captive-capture-rotates-even-when-its-driven-handoff-refuses |
| a failed fetch discards a measurable behind and fails open onto a stale branch (looser than the claim's 'exactly as today'); no test pins the fetch-before-count order | rotate.py:16436 · tests/test_rotate_prepare.py | l4-prepare-fetches-before-it-measures-behind-so-a-clean-worktree-post-merges-main-itself-and-no-hand-fetch-precedes-rotate-self |
| GRID_PUSH_DEFAULTS still holds the literal 200 (the falsifier fires); the round deleted the only test pinning a still-active sibling hypothesis and asserted its negation | grid.py:186 · tests/test_grid.py:268-275 | grid-sync-survives-a-project-without-push-batch-limit |
| session-reap reads paths.core.worktrees_dir, which no config declares -- the literal '.agi/worktrees' is the live value (a round cannot commit .agi/config.json: a director cell); _REAP_EXITED is an invented 5-token vocabulary | heal.py:170, :196-199 | heal-reaps-only-exited-bg-sessions-in-kid-worktrees |
| post_wire's verdict-stub create arm is refused in every schemas-loaded project (parent = the agent's own unfound id) and its comment says the opposite; the yaml round-trip test became a string round-trip | post_wire.py:440-521 · tests/test_node_writer.py:283 | node-writer-create-refuses-a-brand-new-node-whose-parent-id-does-not-resolve |
| claude_code's restart restores ANTHROPIC_* / CLAUDE_CODE_* from the raw env by design, so testable_claim clause 2 and FALSIFIER 1 are false for 8 of 20 scrub names; harness.env is applied after the scrub, filtered only against NEVER_HANDED_DOWN; the round test skips the NO_REAL_PROCESSES opt-in; the adapters still document '`base` arrives already scrubbed' | adapters/claude_code_adapter.py:367-386 · copilot_cli_adapter.py:153-166 · pi_adapter.py:129 | every-adapter-restart-spawns-from-the-scrubbed-env · a-spawned-round-never-inherits-a-model-slot-lock-override |
| the retired-box-prefix guard: the scan set is still narrower than clause 1 (src/ scripts/ templates/ shims/ lib/ web/, driver.sh, conftest.py unscanned -- PASS 8 row half-fixed); `BOX_BOUND <= set(EXEMPT)` is a tautology; the Result table asserts BOX_BOUND == 5 | tests/test_retired_box_prefix.py:41-43, :74, :197 | a00-b9700763-8d8657 · a00-acc4e078-35fa9a · a00-600cf080-0cd865 |
| counts.update() overwrites duplicate count keys across declared suite roots (being worked after TIP: 212f8078c, c9344a2cc) | verification.py:1528 | a-declared-suite-fail-names-its-failing-tests-and-the-context-flake-is-named |

## Node text and test residues -- the owning round (correct in place, reason in THOUGHT)
a-kid-can-commit-the-existing-nodes-its-orders-name (6/7: the claim's second conjunct is absent from the bytes; the scaffold's doubled H1, node_writer.py:740, sits in 107/1243 hypothesis nodes) · write-py-set-is-schema-checked (4/9: CLAIM/FALSIFIERS still certify the removed refusal, :32; the experiment is its own only evidence run) · brief-extras-refs-cannot-escape-context (2/2: Measured :22 stale; the absolute-ref test passes via _node_text, not the containment check) · brainstorm-manifest-route-refuses-a-missing-goal (1/1: the positive path unpinned, test_workflow.py:788; a falsy explicit arg refused as missing, workflow.py:2253) · l2-graph-hygiene (4/5) · l3w4-master-sensei (2/7: the owner-authority boundary hard-coded, sensei.py:56) · launch-memory-cap-tests-never-touch-real-systemd (1/4) · l4-pred-pids-is-an-alternation... (0/3: _row_pred_pid_usable fails closed for every genless non-prime record, unstated, untested) · l3-partial-write-adoption (1/3) · l4-the-gui-session-label... (4/4) · l4-the-town-create-gate... (3/4) · mem-cap-probe-cache-is-private-and-atomic (1/2) · pi-agents-load-no-context-file... (2/4) · authority-publish-fails-closed-on-an-unreadable-veto-cell (3/3: a THOUGHT rewrite deleted the only record of why the experiment lean-disproved) · a00-f30b6285-0e37a6 (2/3) · context-fixture-tests-run-in-a-configured-suite (4/6) · cron-layer-keeps-its-disk-footprint-bounded (2/6) · engine-delta-2/3/4 (2/7, 4/6, 3/4). Detail: runs/<chunk>/verify_<round>.json.

## Research residues -- thought-master -> director-thought (correct in place, reason in THOUGHT)
| round | stands | first residue |
|---|---|---|
| osc-np64-noise-band-per-cell | 6/8 | injected THOUGHT + Agent Notes assert a rejected root verdict (a00-0306a534-0e07d3.md:133, :139; a00-643f7eda-f236d0.md:120); seed tests import pytest at module scope, so their __main__ runner dies in the numpy/torch interpreter |
| lm-band-derived-beats-uniform-matched-grid | 6/7 | ITEM 7's runnability mechanism is stale at the tip (hypothesis :72; ledger a00-486862eb-a0bdd4.md:42) |
| band-byte-audit | 4/8 | the ceiling measured on the round's 26 lines, not 124 over 2 kids vs a 60-line 1-kid budget; the rebrief's 'ceiling 0' vs 26 shipped never reconciled; citations off by 1-8 lines |
| band-headline-reproducer | 3/4 | Agent Notes report three REJECTED items as landed (a00-00e0f92a-bc5cdc.md:112); a stale PYTHONPATH prescription (:39); ceiling missed by 5 |
| qwen2-np32-seed-band-4-budgets | 4/6 | PASS 8's caveat appended as a second copy, the first left false (a00-2b3ca8c4-582f1e.md:91); caveats read off the pre-correction table (:88-89) |
| qwen2-margin-vs-band-declared-test | 2/4 | 'well inside' survives under the corrected 10-vs-40 ceiling (a00-56509ff1-cf43ef.md:39) |
| lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared | 7/7 | a false collection claim (a00-6cbe5da1-6824ca.md:55); THOUGHT :144 misstates the test's I/O |
| lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot | 3/6 | the pairing falsifier is decidable in the logs but no test asserts it (test_hook_trim_fixture_a00-faa1fb92.py:253) |
| cc-seat-context-ceiling | 1/4 | the parent hypothesis has no verdict and an untouched scaffold body (:18) |
| a00-56d3787f · a00-66d002ad · a00-95b6cd1c · a00-ee9a5cdc (osc band-call) | 2/4 · 1/2 · 1/2 · 4/8 | a second live call rule landed 22 min later ('exactly ONE' false); an unannotated fired falsifier (a00-66d002ad:60); a config-only extension promised, a script literal shipped; '18 tracked files' is 84 |

## Agent Notes
assigned: director-engine (PASS 9 residue, belam-S2-L5-X 09-26; runs mur-p9chunk{1..28}of28 + mur-p9retry{1,2})

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version. The one judgement call: engine-delta-5's demote is a live safety regression at TIP (the capture latch swallows every captive prompt after the first), and the PASS rule reads "RED = ... protocol regression -> no merge". (1) Said: section 2 step (4), "protocol regression -> no merge, one [red] dm to thought-master". (2) Machine: ~/.claude/settings.json registers exactly one UserPromptSubmit hook, `python3 /data/work/agi/extensions/agi/hooks/rotation_alert.py` -- MAIN's working file on the trunk, which carries the fix b6438bd7e (:979-990); season2/main's copy is executed by nothing on this box; each seat worktree reads its ladder from its own graph, and 92 of 134 lacked capture_chain_log at TIP, which the MAIN hook refuses by name. (3) Near miss: holding the merge as RED satisfies the words and protects no running process, while it keeps the ladder cell away from the 92 worktrees (they gain it only through season2/main at their next rotation sync) and strands 55 other reviewed rounds. (4) The property of this case: the regressed bytes are already superseded on the trunk the hook runs, so the merge introduces no running regression; the verifier itself ruled demote, not RED. Also: the verifier cited 8221df8a0 for the fix, a card commit; the fix is b6438bd7e, measured.
<!-- THOUGHT:END -->
