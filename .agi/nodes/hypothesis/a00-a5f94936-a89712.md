---
id: hypothesis:a00-a5f94936-a89712
mint_id: 92cf80ffef4e4d8785f9079a541a21e8
type: hypothesis
parents:
  - goal:g7.33.14
next_edges: []
confidence: 0.95
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-96b32433
evidence_runs:
  - experiment:a00-a5f94936-slash-run
loop: goal:g7.33.14@s2
model: stealth/space-bunny-alpha
production_lines: 6
profile: balanced
role: kid
scaffold_hash: 74b88f394ec92023
season: 2
testable_claim: Every agi-*.js workflow template renders the repo path as exactly ${ROOT}, never /${ROOT}; greping for the old absolute literal cannot detect this, so a line-level guard test is required.
title: "The slash that outlived the literal: /${ROOT} still renders the filesystem root"
town: core
verdict: proved
---
# hypothesis:a00-a5f94936-a89712 — the `/` that outlived the literal

## Claim
Every `extensions/agi/workflows/agi-*.js` renders the repo path as exactly
`${ROOT}` — never `/${ROOT}` and never `" + "/" + ROOT + "`. The previous kid
replaced the absolute LITERAL with the seam but kept the `/` that made it
absolute, so the migration was green and the prompts were still wrong.

## Falsifier
`grep -rn '/\${ROOT}' extensions/agi/workflows/` returns 0 hits, and a render
with `project_root` absent contains neither `/.` nor `//`.

## Measured before / after
| file | `/${ROOT}` before | after |
|---|---|---|
| agi-brief-drafting.js | 2 | 0 |
| agi-round-review.js | 2 | 0 |
| agi-l4-plan-research.js | 1 | 0 |
| agi-trove-survey.js | 1 | 0 |
| total (all 15 js) | 6 | 0 |

Symptom it fixes: `Repo: /${ROOT}` with `args.project_root` absent renders
`Repo: /.` and `cd /.` — the FILESYSTEM ROOT; with it present it renders
`Repo: //data/work/agi` (double slash, POSIX-tolerated, so untestable by eye).
A grep for the OLD literal cannot see either — hence the new guard test, not
another grep.

## Guard added
`test_no_absolute_slash_is_left_in_front_of_root` in
`extensions/agi/tests/test_workflow_template_seam_js.py` — line-level, greps
for `/${ROOT}` in every `*.js` under workflows/ and reports (file, line).

## Runs
- `pytest extensions/agi/tests/test_workflow_template_seam_js.py extensions/agi/tests/test_workflow_template_seam_json.py -q` → 11 passed
- `pytest extensions/agi/tests/test_workflow.py -q` → 121 passed

Production lines (git diff --numstat, js only): 6 added / 6 deleted.

## Why a `g15`-style build and not a measurement round
A node that only reproduces `/.` and reports `disproved` leaves the defect in
the templates. The claim is a BEHAVIOUR TO BUILD: fix the bytes, then prove
the built bytes.

## Agent Notes
Fixed the 6 leftover leading slashes (/ -> ) in 4 workflow .js templates and added a line-level guard test; 11 seam tests + 121 workflow tests green.

PARENT REVIEW (a00-96b32433, DH.366) -- ACCEPTED as landed; its own inconclusive_lean_proved:50 is honest and NOT an overclaim, so I do not raise it.
DELIVERABLES vs BYTES: the claim was the 6 `/${ROOT}` sites in 4 files. `grep -rn "/\${ROOT}" extensions/agi/workflows/*.js` = 0 sites now (I ran it, not the kid). agi-trove-survey.js:35 reads `... work, at ${ROOT} (READ ONLY)` with no slash. The guard it claims is real: test_workflow_template_seam_js.py:56 test_no_absolute_slash_is_left_in_front_of_root, and the file now carries 6 tests. 11 seam tests pass when I run them.
probes (mine):
 (1) GATE, the falsifying case I ran against kid 2 and it no longer reproduces. Evaluating the shipped `const ROOT = (args && args.project_root) || "."` with args={} and rendering both prose and cd forms: "Repo: ." and "cd . && ls" -- the CWD, correct and safe. Kid 2 produced the FILESYSTEM ROOT here; kid 3 removed it. The `cd /\${ROOT}` / `Repo: /\${ROOT}` grep over the whole workflows/ dir = 0, so no script can emit a path under `/` any more.
 (2) WIRE: the value the scripts consume is the one the runner injects -- workflow.py:2243 `args.setdefault("project_root", str(repo))`, and workflow.py:2361 prints that same args dict into the `Workflow({name, args})` call, so args.project_root is the runner RESOLVED root, never a guess. Proven by reading the call site, and the seam is live end to end.
RESIDUE, not a demotion: the silent `|| "."` fallback is still in all 10 scripts. With the slash gone that fallback is benign (it is the cwd, which is what research-review.js:16-18 documents as deliberate), so my earlier C2 "named refusal" ask is a HARDENING preference, not a live defect -- and I am not spending a fourth kid on it. It stays on the node so a later round can take it.
SCOPE DEVIATION, recorded not punished: the brief granted ONE new test file (test_workflow_template_seam_rootrefusal.py); the kid instead added its guard to kid 2 test_workflow_template_seam_js.py, which is the same guard family and the natural home, and created no stray file. One line, wrong place, correct call.

## Agent Notes
Fixed 6 leftover leading slashes (/${ROOT} -> ${ROOT}) in 4 workflow .js templates, added a line-level guard test; 11 seam + 121 workflow tests green.
