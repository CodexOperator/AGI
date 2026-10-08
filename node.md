---
id: experiment:a00-55989f04-dd8011
mint_id: 8fbffbcefc1f4f1fb6e15f795e944bd7
type: experiment
parents:
  - hypothesis:the-last-engine-clis-join-the-choice-surface
next_edges: []
confidence: 0.9
edited_by: a00-e65928ba
evidence_runs:
  - experiment:a00-55989f04-dd8011
loop: hypothesis:the-last-engine-clis-join-the-choice-surface@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - "auth: commands.propose refused by name with reason for lm_bench.py:, mail_alert.py:, plan_master.py:record-run, stall_detect.py:, success_metrics.py:, telemetry_rollup.py:, ws_raw_client.py: (all not proposable: <reason>)"
  - "auth: the 6 proposable read verbs returned an argv; reconciler.py: and verify_unified.py: refused with missing required until iter_dir / before+after supplied, then returned the argv"
  - "gate: introspected verb set == manifest+excluded set for all 12 (plan_master 2 verbs, others 1); manifest suite 167 passed"
  - "gate (falsifier): dropping one declared key makes introspected != declared -- verify_unified.py missing=[''] and plan_master.py missing=['trend'] -- so the coverage equality test is load-bearing, not vacuous"
production_lines: 22
profile: balanced
role: kid
scaffold_hash: 6e8ec066a71b1e69
season: 2
title: "Command manifest: the last 12 plain-main CLIs join the choice surface"
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-55989f04-dd8011

## Experiment

**Slice:** the last 12 engine CLIs whose parser is a plain module-level `main`
(EF.54, kid 3 of 3). Appended a `_LISTED_CLIS += [12]` block at the end of
`extensions/agi/tests/test_commands_manifest.py` and declared every verb's typed
args and side effects in the `manifest:` / `excluded:` maps of
`command:commands`. No harness change: all 12 are already captured by
`_drive_module`.

| CLI | verb | disposition |
|---|---|---|
| lm_bench.py | '' | excluded (spend: runs llama-bench) |
| mail_alert.py | '' | excluded (graph-write: alerted_at state) |
| payload_boundary.py | '' | manifest (read) |
| plan_master.py | record-run | excluded (graph-write: seat log) |
| plan_master.py | trend | manifest (read) |
| reconciler.py | '' | manifest (read) |
| rolslice.py | '' | manifest (read) |
| seat_status.py | '' | manifest (read) |
| stall_detect.py | '' | excluded (graph-write: --record) |
| success_metrics.py | '' | excluded (graph-write by default) |
| telemetry_rollup.py | '' | excluded (graph-write: report node) |
| verify_unified.py | '' | manifest (read) |
| ws_raw_client.py | '' | excluded (network: live model server) |

6 proposable, 7 excluded. Two placement overrides added
(`payload_boundary.py:.repo`, `seat_status.py:.root`), both positionals.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_commands_manifest.py -q` →
  **167 passed** (drift: introspected verb set == declared ∪ excluded for all
  12; placement matches each CLI's argparse at test time).
- `python3 -m pytest extensions/agi/tests/test_commands.py
  extensions/agi/tests/test_graphweb.py extensions/agi/tests/test_bin_help_smoke.py -q`
  → **124 passed, 12 skipped**.
- `probe.py` (scratch): all 6 proposable returned a full argv; all 7 excluded
  refused by name with their reason.
- `git diff --numstat -- .agi/nodes/.geometry/commands.md` → **22 added, 0
  removed** (ceiling 40).

## Agent Notes
12 last plain-main CLIs declared: 6 read-only verbs proposable, 7 spend/write/network excluded by name, 2 positional placement overrides; manifest suite 167 passed, sibling suite 124 passed/12 skipped, 22 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review EF.54 (a00-e65928ba) ACCEPT proved. (1) The brief said "your slice is 12 CLIs ... work is DATA plus one _LISTED_CLIS append". (2) The diff carries it: 6 manifest read verbs + 7 excluded spend/write/network verbs, 2 placement positionals, and one appended _LISTED_CLIS block of 12 (the file now lists 67). My probes reproduce it: 7 excluded refused by name with reason, the 6 proposable return argv (2 only after their required args), introspected==declared for all 12, and the equality test fails if one key is dropped. (3) Near miss: declaring success_metrics.py or telemetry_rollup.py proposable because their --json/--dry-run paths read -- their default path writes; excluded is the safe call. (4) No deviation. AGGREGATE (parent): _LISTED_CLIS grew 32 -> 67; write.py is covered by its own VERB-table drift test and the remaining bin CLIs (write_guard.py, verification.py, analyze-chat-structure.py, snapshot-build-site.py) are outside this node set.
<!-- THOUGHT:END -->

PARENT ACCEPT EF.54 (a00-e65928ba): three kids, three proved, zero demoted. Kid 1 (experiment:a00-5aab333e-2f9412) built the _drive_module introspection harness and covered the 11 parser-outside-main CLIs; kid 2 (experiment:a00-531a5750-dcf426) covered 12 plain-main CLIs; kid 3 (this node) covered the last 12. Final measured state at the round tip: _LISTED_CLIS 32 -> 67, command:commands carries all 35 batch-3 CLIs declared or excluded by name, and the four named test files are 291 passed / 12 skipped / 0 failed. The parent ran the negative probes (auth/gate/wire) recorded as probes: on each node. GAP, stated honestly: the node's headline "all 70 engine CLIs" is not literally reproduced by _LISTED_CLIS=67 -- write.py is covered separately by test_the_write_py_manifest_matches_its_verb_table, and write_guard.py, verification.py, analyze-chat-structure.py and snapshot-build-site.py are outside this node's 35-CLI set. The explicit deliverable (the last 35) is complete and green.
