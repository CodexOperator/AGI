---
id: experiment:a00-4e37bd90-durable-auth-probe
mint_id: 58ada008514c4dbfa1d4f4744d002449
type: experiment
parents:
  - hypothesis:a00-4e37bd90-ef5439
next_edges: []
edited_by: a00-4e37bd90
line_ceiling: 40
loop: goal:g7.31.3.2@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "auth", "cmd": "P=/tmp/a00-4e37bd90-probe; mkdir -p $P/arm-a/.agi/sessions/iter-99/kid-probe $P/arm-a/.agi/sessions/inbox; echo '{\"metric_primary\":\"outcome_coverage\"}' > $P/arm-a/.agi/config.json; echo '{\"spawned_by_agent\":\"parent-x\"}' > $P/arm-a/.agi/sessions/iter-99/kid-probe/agent.json; cd $P/arm-a; AGI_TIER=kid AGI_AGENT_ID=kid-probe python3 $ENG/extensions/agi/bin/send.py send parent-other 'probe text'", "expected": "REFUSED: kid kid-probe may dm only its parent parent-x, not parent-other; exit 3; inbox untouched", "observed": "REFUSED: kid kid-probe may dm only its parent parent-x, not parent-other; rc=3; inbox empty", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "P=/tmp/a00-4e37bd90-probe; mkdir -p $P/arm-b/.agi/sessions/inbox; echo '{\"metric_primary\":\"outcome_coverage\"}' > $P/arm-b/.agi/config.json; cd $P/arm-b; AGI_TIER=kid AGI_AGENT_ID=kid-norec python3 $ENG/extensions/agi/bin/send.py send parent-other 'probe text'", "expected": "warn: kid kid-norec has no spawned_by_agent record; the dm gate fails open; rc=0; dm written", "observed": "warn: kid kid-norec has no spawned_by_agent record; the dm gate fails open (l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-); rc=0; $P/arm-b/.agi/sessions/inbox/parent-other.md written", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "python3 -m pytest extensions/agi/tests/test_send.py -q -k 'kid_dm_gate'", "expected": "the two committed regression tests build the sessions state and assert both arms", "observed": "2 passed, 330 deselected in 1.78s (rc=0)", "result": "pass"}
production_lines: 0
profile: balanced
role: kid
scaffold_hash: e6d8223ab294dcd9
season: 2
title: "DT.50 durable kid-dm auth probe: both arms self-contained, regression committed"
town: core
---
# experiment:a00-4e37bd90-durable-auth-probe

DT.50 corrective round under `goal:g7.31.3.2`, base tip `e32522cf4` (the DT.48
carry line). This run closes the last two residues of the DT.46 round:
(PRIMARY 1) the duplicate `## Agent Notes` heading on
`hypothesis:a00-75145740-c77fbe`, and (PRIMARY 2) a durable, tip-reachable
kid-dm auth probe that does not depend on an ephemeral worktree session
record. NOTEs 3-5 are recorded below.

## What was wrong

`hypothesis:a00-75145740-c77fbe` carried TWO real `## Agent Notes` headings
(the last two sections of the body) because two writers each appended their
own. `grep -c '## Agent Notes'` returned 9 only because five other lines
*mention* the string in prose; the heading count `grep -c '^## Agent Notes'`
was **2** and had to become **1**.

Its THOUGHT block also ended `VERDICT: accepted proved`, a false strong
claim: the frontmatter says `verdict: inconclusive_lean_proved:90`. The real
lean had to be named in the authored region.

The prior auth probe (`experiment:a00-75145740-residue1-auth-probe`) ran with
kid `a00-75145740`, whose `agent.json` lived only in an unreachable worktree.
On the merged tip `send.py`'s kid-dm gate (`_kid_dm_refusal` ->
`_kid_parent_id`, `extensions/agi/bin/send.py:920`) scans
`locations.shared_sessions_dir(root)` + `locations.sessions_dir(root)`; with
no reachable record carrying `spawned_by_agent` it FAILS OPEN (warn, real dm,
rc=0), so the recorded REFUSED was not reproducible. Durability requires a
probe that CONSTRUCTS the state the gate reads.

## PRIMARY 1 — duplicate heading collapsed

Read the body, then replaced the two-heading range as ONE sanctioned write:

    python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe \
        'replace body 59:63 -'   # new text on stdin: ONE heading + both bodies

Verified after the write:

    grep -c '^## Agent Notes' .agi/nodes/hypothesis/a00-75145740-c77fbe.md
    -> 1
    grep -c 'DT.46 residue round on goal:g7.31.3.2 closed' ...  -> 1
    grep -c 'DT.46 corrective round: three MUR residues closed' ... -> 1

Both prior note bodies survive verbatim under the single heading.

## PRIMARY 2 — durable, tip-reachable auth probe

Two forms, both self-contained. The CLI probe builds its own project root
under /tmp, so no live agent record and no worktree is involved.

### Arm (a) — record present -> REFUSED, exit 3

    ENG=$PWD; P=/tmp/a00-4e37bd90-probe
    mkdir -p $P/arm-a/.agi/sessions/iter-99/kid-probe $P/arm-a/.agi/sessions/inbox
    echo '{"metric_primary":"outcome_coverage"}' > $P/arm-a/.agi/config.json
    echo '{"spawned_by_agent":"parent-x"}' \
        > $P/arm-a/.agi/sessions/iter-99/kid-probe/agent.json
    cd $P/arm-a
    AGI_TIER=kid AGI_AGENT_ID=kid-probe \
      python3 $ENG/extensions/agi/bin/send.py send parent-other "probe text"

OBSERVED (verbatim stderr), rc=3, inbox untouched:

    REFUSED: kid kid-probe may dm only its parent parent-x, not parent-other

### Arm (b) — record absent -> fail-open warn, exit 0

    mkdir -p $P/arm-b/.agi/sessions/inbox
    echo '{"metric_primary":"outcome_coverage"}' > $P/arm-b/.agi/config.json
    cd $P/arm-b
    AGI_TIER=kid AGI_AGENT_ID=kid-norec \
      python3 $ENG/extensions/agi/bin/send.py send parent-other "probe text"

OBSERVED (verbatim stderr), rc=0, dm written to
`$P/arm-b/.agi/sessions/inbox/parent-other.md`:

    warn: kid kid-norec has no spawned_by_agent record; the dm gate fails
    open (l4-a-kid-reports-to-its-parent-and-the-seat-hears-one-dm-)

TRAP HIT: run from inside the repo, `shared_sessions_dir` routes through
`git_common_root` and arm (b) writes into the LIVE
`/data/work/agi/.agi/sessions/inbox/` (a real dm from `kid-norec`). The probe
root must live under /tmp, outside any git worktree. The stray file was
removed.

### Regression test (durable at the merged tip)

`extensions/agi/tests/test_send.py` gains
`test_kid_dm_gate_refuses_a_non_parent_by_name` and
`test_kid_dm_gate_fails_open_without_a_parent_record`; a shared
`_kid_gate_root` fixture builds the controlled `<sessions>/iter-99/<kid>/
agent.json`. Command and observed output:

    python3 -m pytest extensions/agi/tests/test_send.py -q -k 'kid_dm_gate'
    -> 2 passed, 330 deselected in 1.78s  (rc=0)

These tests CONSTRUCT the gate's state, so they reproduce from any merged
checkout and cannot lean on a live worktree. The gate's behaviour was NOT
changed — the durability is in the probe.

## NOTE 3 — THOUGHT aligned with the verdict

    python3 extensions/agi/bin/write.py hypothesis:a00-75145740-c77fbe \
        'thought ...'   # rewritten from scratch, naming the real 90 lean

The false `VERDICT: accepted proved` was replaced; the reasoning was kept and
now names the real `inconclusive_lean_proved:90`.

## NOTE 4 — evidence experiment parentage

`experiment:a00-75145740-residue1-auth-probe` had
`parents: [hypothesis:a00-37392a90-0d3366]` while the corrected node's
`evidence_runs` pointed at it. Reparented in ONE write to the node it is
evidence for:

    python3 extensions/agi/bin/write.py experiment:a00-75145740-residue1-auth-probe \
        'set parents [hypothesis:a00-75145740-c77fbe]'
    -> updated (parent resolves; single write)

## NOTE 5 — bookkeeping

No `GOALS.md` hand-edit. The `goal:g7.31.3.2` §3d residue table is refreshed
at merge-up, not here; closed DT.45/DT.41 rows were not reopened.

## Touched-surface runs

    python3 -m pytest extensions/agi/tests/test_send.py \
        extensions/agi/tests/test_write.py -q
    python3 extensions/agi/bin/links.py links   # 0 broken

## Production lines

The only production-path change this round is the two regression tests plus
their fixture in `extensions/agi/tests/test_send.py` — a TEST file, excluded
from production-line accounting. `git diff --numstat` over `extensions/
bin/`, `extensions/agi/bin/`, `src/` and `skills/` shows no non-test change.

    production_lines: 0 / ceiling 40

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DT.50 corrective round. PRIMARY 1: the duplicate Agent Notes on hypothesis:a00-75145740-c77fbe was two real headings from two writer paths; collapsed to ONE via one sanctioned replace-body write, both note bodies kept verbatim (grep ^## Agent Notes == 1). PRIMARY 2: the DT.46 probe was not tip-reproducible because its REFUSED depended on an ephemeral worktree agent record; the durable form constructs that state itself. Proven two ways: a self-contained CLI probe under /tmp (arm a record present -> REFUSED exit 3; arm b record absent -> fail-open warn exit 0 with a real dm) and two committed regression tests in test_send.py sharing a _kid_gate_root fixture. Gate behaviour unchanged. NOTE 3: THOUGHT rewritten to name the real inconclusive_lean_proved:90 instead of the false accepted-proved. NOTE 4: reparented experiment:a00-75145740-residue1-auth-probe to the node it is evidence for, one write. TRAP: running the CLI probe from inside the repo makes shared_sessions_dir route through git_common_root and write into the LIVE inbox; probe roots must be under /tmp. CONFLICT: the brief said parent the new experiment under goal:g7.31.3.2 but the experiment schema rejects goal parents, so it is parented under this round hypothesis instead (still inside the goal subtree).
<!-- THOUGHT:END -->
