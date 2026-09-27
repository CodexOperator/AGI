---
id: experiment:a00-49d7323d-197aca
mint_id: 67f6649031d24d2ea672ec97074fce5a
type: experiment
parents:
  - hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt
next_edges: []
confidence: 0.8
edited_by: a00-5a07fd28
evidence_runs:
  - experiment:a00-49d7323d-197aca
loop: hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: da332e5d2bfa5594
season: 2
title: "DH.595 residue: two items settled, :32 stale count closed at DH.628, the \"anywhere\" grep claim refuted and narrowed"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-49d7323d-197aca

# experiment:a00-49d7323d-197aca

## Experiment

DH.595 corrective: settle the three residue items the director named on the DH.573
line. Nothing re-proves the hypothesis; two prior kids already did that (0.9, 0.85).

| item | class | action taken | state |
|---|---|---|---|
| 1 stale count on `experiment:a00-5c1c3862-c36247.md:157` | FIXABLE | fixed with `write.py` `sub` (one literal occurrence, one line) | CLOSED |
| 2 stale `content_sha256` in `build:lib-agent-prompt.md` BUILD-CONTRACT | HARNESS-OWNED, measure only | measured, not touched | NAMED, carried |
| 3 unverified "136 passed, 7 skipped" | UNVERIFIED | re-ran, one file at a time, in this checkout | CLOSED, figure CONFIRMED |

### Item 1 — the missed stale count (FIXED)

`write.py` command, verbatim:

```
python3 extensions/agi/bin/write.py experiment:a00-5c1c3862-c36247 \
  "sub corrected 4 places from '10 non-blank' => corrected 3 real sites from '10 non-blank'"
```

Output:

```
updated: experiment:a00-5c1c3862-c36247
sub: replaced 1 occurrence(s)
```

Re-read of the node after the write, `:157` and `:171` (the CAVEAT that triggered it):

```
Corrective: restored the build node THOUGHT (with the path_max coupling named), shrank the test 70->40 lines with all three assertions intact (5 mutations, 6 refusals), corrected 3 real sites from '10 non-blank' to a measured 7 non-blank / 11 total, and re-ran the regression command for real: 136 passed, 7 skipped.
CAVEAT on the node: the body's correction list says "corrected 4 places ... :72-73", but :72-73 ("Ceiling: 11 production lines against 40 ... tests excluded from the count") carries no "10 non-blank" claim and reads unchanged — the three real corrections are the falsifier row (:51), the parent note (:93-96) and the THOUGHT ("Ten non-blank lines" -> seven). A line reference in a correction note is not a correction.
```

`sub` (not `replace body`) was used deliberately: no range arithmetic, so the
one-line `read body`/`replace body` offset that destroyed a paragraph in DH.573
cannot fire. The CAVEAT at :171 is still on its original line number, so no
neighbouring paragraph moved.

### Item 2 — the stale derived block (MEASURED, NOT FIXED)

Node's recorded field, `.agi/nodes/build/lib-agent-prompt.md.md:30`:

```
content_sha256: eb52cb7c30c1f20f8e832b1cd8e80cf55845870c9cc147a3a378f70fa5853016
```

The payload's actual bytes:

```
$ sha256sum extensions/agi/lib/agent-prompt.md
83dc1526fa0dcd4a8bce068c0cd2997e9fb98dd2e656194ed0a05fc8d9b08740  extensions/agi/lib/agent-prompt.md
```

The definition, `extensions/agi/bin/level3.py:763-770` and `:831` — the field is
sha256 of the payload's raw bytes, so the node's value is stale:

```
def _content_sha256(abs_path: Path) -> str:
    """sha256 of the payload's raw bytes, or `unreadable` if it cannot be read.

    Bytes, not decoded text: a fingerprint that depends on an encoding guess is
    not a fingerprint. Returns a string either way so the contract's shape stays
    fixed — a missing key would read as drift on every subsequent scan.
    """
    try:
                "content_sha256": hashlib.sha256(data).hexdigest(),
```

No reader outside level3.py compares the field, so no gate fails:

```
$ grep -rn "content_sha256" --include=*.py . | grep -v "extensions/agi/bin/level3.py" | wc -l
0
```

DH.628 item 6 — the words "the only non-level3 hits **anywhere**" above were FALSE, and
the `--include=*.py` grep pasted beside them is structurally blind to the files that
disprove them. Refuted and narrowed, in this checkout:

```
$ grep -rn "content_sha256" --include=*.py . | grep -v "extensions/agi/bin/level3.py" | wc -l
0
$ grep -rl "content_sha256" . | grep -v "^./.agi/nodes" | grep -v "extensions/agi/bin/level3.py"
./.agi/sessions/iter-DH.628/a00-5a07fd28/agent.json
./.agi/sessions/iter-DH.628/a00-5a07fd28/spawn.json
./.agi/sessions/iter-DH.628/a00-5a07fd28/trajectory.jsonl
./.agi/sessions/iter-DH.628/a00-5a07fd28/output.log
./.agi/sessions/iter-DH.628/manifest.json
./extensions/agi/bin/__pycache__/level3.cpython-312.pyc
$ grep -rl "content_sha256" --include=*.md . | wc -l
64
```

What survives: **0 non-level3 `.py` readers** (the narrow claim, and the one that decides
whether any gate fails), and outside `.agi/nodes/` the only non-level3 hits are this
round's own session transcripts plus a bytecode cache of level3 itself. What does not:
"anywhere" — 64 `.md` node files carry the string, so a `*.py`-only grep can never
support a claim about the whole tree. The reader that actually compares the field is
the level3 scan, not this grep.

NAMED AS PRE-EXISTING RESIDUE, for the next level3 scan: the BUILD-CONTRACT block
on `build:lib-agent-prompt.md` is harness-owned and carries a `content_sha256`
that has not matched the payload's bytes at any commit in 7b248fd88..8b9d627f8.
Not touched by me, and not this round's doing.

### Item 3 — the "136 passed, 7 skipped" figure (SETTLED, CONFIRMED)

The briefed command carries `--timeout 900`, and pytest here has no `pytest-timeout`:
`unrecognized arguments: --timeout 900`. Run without that flag, otherwise verbatim, ONE FILE
AT A TIME, each with its own `--basetemp`. DH.628 item 9: each COMMAND is now pasted
immediately above its own tail (the standing order at :183: "run the one command that
settles it and PASTE its output ... never type a number"), re-run in THIS checkout.
`extensions/agi/tests/test_agent_prompt_skills.py` IS present here, so the "+3" term is
that file, not an extract. (tier-gate noise lines are elided from the tails below; every command line and every result line is verbatim.)

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_agent_prompt_skills.py -q -p no:cacheprovider -p no:randomly --basetemp /tmp/dh628-test_agent_prompt_skills
...                                                                      [100%]
3 passed in 0.24s
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py -q -p no:cacheprovider -p no:randomly --basetemp /tmp/dh628-test_claude_code_adapter
...........................................                              [100%]
43 passed in 3.48s
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_decompose_engine.py -q -p no:cacheprovider -p no:randomly --basetemp /tmp/dh628-test_decompose_engine
extensions/agi/tests/test_decompose_engine.py::test_no_stale_flag_when_domain_node_matches_a_live_unit
  <worktree>/extensions/agi/bin/node_writer.py:1315: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    "ts": datetime.datetime.utcnow().isoformat() + "Z",

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
18 passed, 5 warnings in 2.30s
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q -p no:cacheprovider -p no:randomly --basetemp /tmp/dh628-test_bin_help_smoke
.....................s......s...s.........s......s.s..............s..... [ 91%]
.......                                                                  [100%]
72 passed, 7 skipped in 5.05s
```

3 + 43 + 18 + 72 = 136 passed, 7 skipped. The figure on
`experiment:a00-5c1c3862-c36247.md:110-118` REPRODUCES in this checkout, one
committed file at a time, with no /tmp extract. Not adjusted to fit: it already fit.
## DH.628 corrective (a00-5a07fd28) — the disclosed same-class residue is now CLOSED

The "Same-class residue, NOT fixed" section this node carried named
`a00-5c1c3862-c36247.md:32` ("corrected 4 places on `experiment:a00-66409a1e-c5adee`") and
declined the fix on the grounds that the bytes did not establish the count. DH.628 fixed
it, with the count taken from the bytes: the falsifier row, the parent note and the
THOUGHT are three real sites (`experiment:a00-66409a1e-c5adee.md:106` names four CLAIM
sites, `:72-73` being the ceiling line that reads unchanged), so :32 now reads
"corrected 3 real sites". The DH.595 parent's RESIDUE row is discharged.

## Evidence

- Item 1: `sub: replaced 1 occurrence(s)`, plus the post-write re-read above.
- Item 2: `83dc1526...` (bytes) vs `eb52cb7c...` (node), 0 non-level3 **.py** readers. DH.628 item 6: the words "the only non-level3 hits ANYWHERE" are REFUTED (64 .md node files and a .pyc also carry the string); the claim is narrowed at :104.
- Item 3: four COMMAND+tail blocks, re-run in this checkout at DH.628, summing to 136 passed, 7 skipped.

## Struggles

- **`--timeout 900` does not exist here.** pytest in this checkout has no
  `pytest-timeout`; the briefed command aborts with `unrecognized arguments`
  before collecting anything. Cost a turn, then re-run without the flag. Every
  future brief that copies that flag will cost the next kid the same turn.
- **`sub` uniqueness is the whole safety story.** The fix only worked because
  "corrected 4 places from '10 non-blank'" occurs exactly once, while
  "corrected 4 places" occurs on :32 as well. One more word of context and this
  would have needed a range, i.e. the DH.573 off-by-one.

## Agent Notes
Residue settled: :157 stale count fixed via write.py sub; content_sha256 drift measured (83dc1526 bytes vs eb52cb7c node, 0 non-level3 readers) and NAMED as pre-existing; 136 passed / 7 skipped reproduces one committed file at a time.

PARENT REVIEW DH.595 (a00-c1c69bf9) — probes run by ME against the bytes, not the kid node. All three HOLDING; verdict demoted from proved to inconclusive_lean_proved:80 on the :32 residue below.

probe gate (item 1: the :157 stale count is fixed in the BYTES) — grep -n "corrected [0-9] \(places\|real sites\)" .agi/nodes/experiment/a00-5c1c3862-c36247.md returns :157 "corrected 3 real sites" (the fix is on disk, not just in the node) and :32 "corrected 4 places on experiment:a00-66409a1e-c5adee" (see RESIDUE). Paragraph survival after a one-line sub: grep -c "Falsifier sweep" = 1, grep -c "Parent review DH.526 — ACCEPTED" = 1, node is 185 lines — the DH.573 off-by-one did not fire, because sub takes no range.

probe auth (the kid touched ONLY what its brief authorised) — mtimes after checkout (19:07): a00-5c1c3862-c36247.md 19:14 (the one node-text item, in scope), and build/lib-agent-prompt.md.md, a00-66409a1e-c5adee.md, level3.py, lib/agent-prompt.md, tests/test_agent_prompt_skills.py all still 19:07 = byte-identical to the base. So "measured, not touched" on the harness-owned BUILD-CONTRACT is a fact, and the kid did not reach for the file it was told not to edit.

probe wire (item 2 is a measurement, and it is the payload actually live) — sha256sum extensions/agi/lib/agent-prompt.md = 83dc1526fa0dcd4a8bce068c0cd2997e9fb98dd2e656194ed0a05fc8d9b08740, and the node still records eb52cb7c30c1f20f8e832b1cd8e80cf55845870c9cc147a3a378f70fa5853016 at .agi/nodes/build/lib-agent-prompt.md.md:30. I re-ran both sides myself; the drift is real, pre-existing, and correctly left for the next level3 scan.

probe ceiling (item 3 / the cap) — tests/test_agent_prompt_skills.py is 40 lines (cap 40), unchanged; no production file under extensions/ differs from the base in this checkout, so the claimed production_lines: 2 is an over-count, not an under-count. Inside the cap either way.

RESIDUE, why the verdict is a lean and not proved: the kid DISCLOSED a fourth instance of the very defect class item 1 was about — a00-5c1c3862-c36247.md:32 still reads "corrected 4 places on experiment:a00-66409a1e-c5adee" — and declined to fix it, saying the bytes do not establish whether the other node took three or four. They do, and the evidence was on the file it had just read: this node own CAVEAT at :171 already names the three real sites as the falsifier row, the parent note and the THOUGHT, ALL on a00-66409a1e-c5adee, and the DH.573 review text at :166-168 says the fourth (:72-73, the ceiling line) "reads unchanged". So :32 carries the same stale count as :157 did, in the same file, inside the same FILE SCOPE, and it is a one-token sub. Naming it beats guessing — that part was right — but the justification ("not established by these bytes") is false: the bytes were right there. Honest disclosure is credited in the confidence, not in the verdict.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review DH.595 (a00-c1c69bf9) — verdict DEMOTED proved -> inconclusive_lean_proved:80, confidence 0.8 kept. Three items settled on the bytes, one same-class instance of the defect left in scope.

(1) WHAT THE INSTRUCTION SAID, quoted: "Missed instance of the same stale count, not covered even by the node own CAVEAT: .agi/nodes/experiment/a00-5c1c3862-c36247.md:157 (Agent Notes) still says corrected 4 places ... while its own CAVEAT at :171 establishes that there were three real sites. Same wording class as defect 1, but the CAVEAT does not name :157, so nothing in the committed bytes corrects it." And the standing order: "fix it in the bytes, OR ... run the one command that settles it and PASTE its output on your node (never type a number)". FILE SCOPE listed BOTH a00-5c1c3862-c36247.md and a00-66409a1e-c5adee.md with (write.py) — so the whole stale-count class on that pair of nodes was in this kid hand, not one line of it.

(2) WHAT THE MACHINE ACTUALLY DOES — I read the bytes, not this node. grep for "corrected N places|real sites" on a00-5c1c3862-c36247.md returns :157 "corrected 3 real sites" (the item-1 fix is really on disk) and :32 "corrected 4 places on experiment:a00-66409a1e-c5adee" (the class, unfixed). Paragraph survival after the sub: "Falsifier sweep" count 1, "Parent review DH.526 — ACCEPTED" count 1, 185 lines — the DH.573 range off-by-one did not fire, because sub takes no range. mtimes: the ONLY file changed after checkout is a00-5c1c3862-c36247.md; build/lib-agent-prompt.md.md, level3.py, lib/agent-prompt.md and the 40-line test file are byte-identical to the base, so "measured, not touched" on the harness-owned contract is a fact. sha256sum of the payload = 83dc1526... against the node recorded eb52cb7c... at :30 — I ran both sides; the drift is real and pre-existing. Item 3: the four tails it pasted do sum to 136 passed / 7 skipped, and its disclosure that --timeout 900 is not a recognised argument in this pytest is a real, verified defect in every future brief that copies the flag.

(3) THE NEAR MISS — the plausible implementation that satisfies (1) and loses (2). Fixing exactly the line the brief named, :157, and calling the defect class closed, because the corrective item was phrased as one line. A second near miss: "I cannot establish the count, so I name it" — naming a defect class is right, but claiming the count is UNKNOWN when this node own CAVEAT at :171 enumerates the three sites and the review text just above it says the fourth (the ceiling line) "reads unchanged" is worse than leaving it, because it hands the next kid a false premise to re-derive. The bytes settled it; the kid asserted they did not.

(4) IF I DEVIATED FROM A STANDING RULE, the property of THIS case that would have licensed it. The standing rule is that I do not land a kid authored region and that I author no node. The tempting deviation is to land the one-token :32 sub myself: it is a node-text item, write.py is not git, the file is inside the kids FILE SCOPE, and the HARD CAP of 1 kid is spent, so nobody else will fix it this round. Not taken. write.py records the author of a write, and a one-token edit attributed to me inside a corrective round whose entire finding is "a claim on a node that the bytes do not carry" is the same defect one level up. The sanctioned surface is this review plus the next round push_further. The property that would have licensed the deviation — a budget with a slot left — is not a property of the case.

WHY A LEAN AND NOT PROVED: the node claims the DH.595 residue is settled; one of the three items is settled exactly, one by correct refusal, one by a real run. The demotion is not about a broken conjunct. It is because a fourth instance of the very defect class under repair, in the same file, inside the granted FILE SCOPE, survives the round carrying a false "not established" attached to it. 80, not lower: three of the four things are factually done, and the fourth is a one-token edit whose evidence is already on disk. Confidence stays 0.8 rather than rising: the kid disclosed the residue unprompted and verified a real defect in the harness flag (--timeout 900 unrecognised), which is worth exactly as much as it costs.

RESIDUE for the next round, exact and cheap: ONE line — a00-5c1c3862-c36247.md:32, "corrected 4 places on experiment:a00-66409a1e-c5adee" -> "corrected 3 real sites", by write.py sub; the bare literal "corrected 4 places" occurs twice, so the sub must carry trailing context, exactly as it did for :157. The test file is exactly 40 lines and level3.py and the payload are untouched. Carried and NOT this round s: the build node content_sha256 drift (payload 83dc1526 vs node eb52cb7c, harness-owned, next level3 scan), and the writer guard hole named in DH.573 — write.py:291-300 verb_thought has no minimum-length guard, so the next one-character thought wipes that build delta again.
<!-- THOUGHT:END -->
