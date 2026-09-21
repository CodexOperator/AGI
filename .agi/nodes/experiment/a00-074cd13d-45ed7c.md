---
id: experiment:a00-074cd13d-45ed7c
mint_id: 6c8e958834bc47a680b516e466892a09
type: experiment
parents:
  - hypothesis:l4-the-cron-node-is-the-whole-schedule-any-job-is-one-entry-one-variable-silences-the-box-audit-names-the-undeclared-and-apply-is-the-box-init
next_edges: []
confidence: 0.9
edited_by: a00-38963541
evidence_runs:
  - experiment:a00-074cd13d-45ed7c
  - experiment:a00-0e932af3-130352
line_ceiling: 60
loop: hypothesis:l4-the-cron-node-is-the-whole-schedule-any-job-is-one-entry-one-variable-silences-the-box-audit-names-the-undeclared-and-apply-is-the-box-init@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "crons.load_crons_node() on a fixture cadence entry {\"ghost_job\": {\"every_mins\": 5, \"cmd\": \"   \"}} (whitespace-only cmd) -- unchanged by this round, re-checked because kid 1's node was demoted", "expected": "CronsError refusing the job by name", "observed": "CronsError: ...cadences declares unknown job 'ghost_job' with no `cmd`", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "render_managed_lines(root, root, root, node) with crons_live: false + a generic cmd job enabled:true -- unchanged by this round", "expected": "[] total, generic entries included", "observed": "[]", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "crons.cmd_audit(root=/home/ubuntu/work/agi/.agi, crontab_file=<empty tmp fixture>, unit_dir=~/.config/systemd/user) -- RE-RUN against this round's fix, same real box directory that falsified experiment:a00-0e932af3-130352", "expected": "claude-remote-control.service flagged; this project's own agi-agi-reaper-2f118e6f.service NOT flagged", "observed": "both true: claude-remote-control.service (and 6 other ordinary-named real units in the same dir) now flagged, agi-agi-reaper-2f118e6f.service silent", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "crons.load_crons_node(<live worktree .agi>) + crons._substitute() round-trip vs git show 12072bdde absolute values -- unchanged by this round (file scope excluded it)", "expected": "byte-identical", "observed": "byte-identical", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "render_managed_lines() generic job with box: [local-town, other-town], box_name in vs out of list -- unchanged by this round", "expected": "renders only when box_name is in the list", "observed": "matched", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "crons.cmd_apply(crons_live: false + a declared service, --unit-dir <fixture with the unit file present>) vs the SAME call with NO --unit-dir (plain `crons.py apply`), run by parent a00-38963541 iter143", "expected": "hypothesis conjunct 2: 'crons_live: false ... stops + disables every services: entry ... crons_live: true + crons.py apply restores both'", "observed": "with --unit-dir: ['systemctl --user disable --now agi-agi-reaper-001f2564.service (dry-run)', 'remove unit ... (dry-run)']; NO --unit-dir: unit_actions=[] -- plain apply never touches units (reconcile_units returns [] when unit_dir is None, crons.py L751). Production still reaches the service because the rendered grid_sync self-reapply line bakes --unit-dir (crons.py L550).", "result": "fail"}
  - {"conjunct": 3, "class": "wire", "cmd": "crons.cmd_audit(root=<tmp project>, crontab_file=<empty fixture>, unit_dir=None) with HOME holding ~/.config/systemd/user/claude-remote-control.service -- the plain `crons.py audit` invocation, run by parent a00-38963541 iter143 on the bytes BEFORE the corrective", "expected": "the unit is named", "observed": "[] for the unit side -- 'clean' while an undeclared unit runs; this is the probe that spawned the corrective, now fixed by experiment:a00-5d3a3267-adc1a5 and re-probed pass there", "result": "fail"}
production_lines: 15
profile: balanced
role: kid
scaffold_hash: 9a2919116cf232cb
season: 2
title: "Fix crons.py audit unit loop: flag any non-agi-shaped .service, stay silent on another project hash"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-074cd13d-45ed7c

## Experiment

Round-2 fix of the ONE falsified conjunct of the parent hypothesis: the
`crons.py audit` unit loop (`cmd_audit`, extensions/agi/bin/crons.py).

**Pre-fix defect, reproduced against the box's REAL `~/.config/systemd/user/`:**
`claude-remote-control.service` (named in the hypothesis's own testable_claim)
was NOT flagged. The loop only entered either branch when `p.name.startswith("agi-")`,
so an ordinary-named unit fell through silently (false negative), and an
agi-shaped unit for ANOTHER project's hash was flagged as undeclared
(false positive).

**The fix (15 changed production lines in `cmd_audit`'s unit loop only):**

```python
AGI_UNIT_RE = re.compile(r"^agi-(.+)-([0-9a-f]{8})\.service$")
...
for p in (sorted(ud.glob("*.service")) if ud.is_dir() else []):
    m = AGI_UNIT_RE.match(p.name)
    if m:
        if m.group(2) == ours[:8]:
            if m.group(1) not in declared:
                found.append(...)          # ours, undeclared -- kept
        # else: another project's own unit -- silent, not our business
    else:
        found.append(f"unit: {p.name} (not declared by this node)")
```

No other part of the file was touched (crontab side, generic-entry renderer,
`_substitute` were already probed correct).

## Evidence

Both bugs fixed, each with a new test in extensions/agi/tests/test_crons.py:

- FALSE NEGATIVE fixed: `test_audit_flags_an_ordinary_named_unit` — a fixture
  `some-other-tool.service` (no agi shape) is now flagged, rc=1. This is the
  case `claude-remote-control.service` / `hermes-gateway.service` hit on the
  live box, and the one the parent's real-directory probe falsified.
- FALSE POSITIVE fixed: `test_audit_is_silent_on_another_projects_unit` — a
  fixture `agi-something-deadbeef.service` (foreign 8-hex hash) is silent,
  rc=0. Same treatment the crontab side already gives a foreign `agi-crons
  <hash>` block.
- The three pre-existing audit tests are unchanged and still pass: the new
  `AGI_UNIT_RE` does not match their `agi-ghost-99.service` (2 hex, not 8), so
  it correctly falls to the always-flag branch; no assertion was loosened.

```
$ python3 -m pytest extensions/agi/tests/test_crons.py -q
82 passed in 4.35s
```

Production lines: `git diff --numstat -- extensions/agi/bin/crons.py` = 15+/5-
under the 60-line ceiling.

## Agent Notes
cmd_audit unit loop: replaced the startswith('agi-') gate with hash-agnostic AGI_UNIT_RE; ordinary-named units now flagged (false negative fixed), another project's agi-shaped unit now silent (false positive fixed). 2 new tests + 3 pre-existing unchanged, 82 passed in test_crons.py. 15 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-837f99b1, iteration 125). Verdict kept at `proved`
(confidence adjusted 0.95 -> 0.9); this node is the one the parent cites as
the primary evidence run for the target hypothesis, alongside
experiment:a00-0e932af3-130352 (demoted, see that node's own THOUGHT).

WHAT THE INSTRUCTION SAID: this round's own brief (the parent's, not the
hypothesis directly) asked for exactly one thing — fix `cmd_audit`'s unit
loop so it no longer misses an ordinary-named undeclared unit and no longer
false-positives on another agi project's own correctly-hash-matched unit.

WHAT THE MACHINE ACTUALLY DOES: re-ran the exact probe that falsified the
previous round, unchanged, against this round's own diff — `cmd_audit`
against the box's REAL `~/.config/systemd/user/` directory (not a fixture).
`claude-remote-control.service` is now flagged, along with six other real,
ordinary-named units in that same directory that were silent before
(hermes-gateway.service, live-bridge.service, local-town-tunnel.service,
openclaw-gateway.service, openclaw-reactive.service, streamer-stub.service).
This project's own declared unit, `agi-agi-reaper-2f118e6f.service`, stays
silent, as it must. Also re-ran the four conjuncts this round did not touch
(1/2/4/5) to confirm the file-scope promise held — none of them regressed
(full `probes:` list on this node covers all five).

THE NEAR MISS, avoided this time: the tempting fix is "flag anything that
was previously silent," which would also flag a SECOND agi project's own
legitimately declared unit sharing this same `~/.config/systemd/user/`
directory (`unit_filename` keys only on `Path.home()`, not per-project) —
a false positive the crontab side of `audit` already avoids for a foreign
`agi-crons <hash>` block. `AGI_UNIT_RE`'s hash-agnostic-then-hash-check
structure (match the shape first, then compare the captured hash to
`ours[:8]`, silent when it belongs to someone else) is what keeps both
directions correct at once — probed by the two new tests
(`test_audit_flags_an_ordinary_named_unit`,
`test_audit_is_silent_on_another_projects_unit`) and confirmed live on the
real directory, which only happens to carry this box's own agi ecosystem
today and so never exercised the foreign-hash branch for real — the parent
did not attempt to construct a second real agi project on this box to probe
that branch against production bytes; it is covered by the kid's own
fixture test only. Recorded honestly rather than claimed as independently
probed.

Residual, not fixed by design: `cmd_audit`'s unit side is scoped to
`--unit-dir` (`~/.config/systemd/user`, user-scope units only). `earlyoom`,
the hypothesis's OTHER named example, is a SYSTEM-scope unit
(`/etc/systemd/system/earlyoom.service` / `/lib/systemd/system/earlyoom.service`
on this box, confirmed via `systemctl list-units --all` vs `--user`) and is
structurally unreachable by this seam regardless of the name-matching fix —
auditing system units would need root and a different seam entirely, out of
scope for a read-only per-user tool and not attempted here. The hypothesis's
own text names both `earlyoom.service` and `claude-remote-control.service`
in one breath; only the second is actually reachable by the `--unit-dir`
design this hypothesis specifies, and it is now caught.

No deviation from a standing rule.
<!-- THOUGHT:END -->
