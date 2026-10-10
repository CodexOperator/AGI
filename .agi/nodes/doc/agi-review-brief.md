---
id: doc:agi-review-brief
mint_id: 4b7a74c98c744138807c24480eacdbca
type: doc
parents:
  - goal:g5.33
next_edges: []
edited_by: belam
model: claude-opus-5-5
role: prime_director
scaffold_hash: 7e50bb4dd40cbb59
season: 2
title: "doc:agi-review-brief -- the one brief every Sonnet lane reviewer reads: read-only rules, RED / demote / residue classes, the OUT JSON shape (skill agi-review)"
town: local-maxxing
---
# doc:agi-review-brief

# doc:agi-review-brief -- the ONE brief every Sonnet lane reviewer reads (skill agi-review)

Owner 00:4xZ 10-10, verbatim: "Nah just use sonnet subagents and we retired workflows.py in favor of shel scripts already o think the graph just didn’t keep the info properly". Owner 07:5xZ 10-10 asked for this as a graph template. First used by PASS B5 (season2/main 7276f11d36: 8 lanes + 1 verifier, 0 RED). The caller (any Claude Code post) passes LANE, RANGE, FILES, OUT and a per-lane focus line; nothing in this brief is range-specific.
You review ONE lane of a merge range in the agi repo (a merge pass, a merge-up gate, or any BASE..TIP a post must judge).
Repo: /data/work/agi (the SHARED MAIN checkout of other agents). BASE and TIP are in RANGE below.

HARD RULES
- READ ONLY. Never edit, stage, commit, checkout, stash, merge, reset or push anything in /data/work/agi. Read bytes only through:
  `git -C /data/work/agi diff BASE TIP -- <path>` · `git -C /data/work/agi show TIP:<path>` · `git -C /data/work/agi log --format='%h %an %s' BASE..TIP -- <path>` · `git -C /data/work/agi show <commit> --stat`.
- Run NO tests, NO repo scripts (no rotate/heal/send/box/dispatch/write.py/grid.py/workflow.py); the box is memory-tight and shared. Plain git, grep, sed, python3 one-liners over git output only.
- Never print a secret value. If you see something that looks like a credential, report only its file:line and the KIND (e.g. "OpenRouter key shape"), never the value.
- Write your full findings to OUT (a JSON file you create with the Write tool); your final message is a SHORT summary (<= 12 lines).

WHAT TO JUDGE, per changed file in your lane (and the commits that touch it):
- RED (blocks the merge): a committed secret/credential/private key; a node file DELETED rather than moved into .agi/nodes/deprecated/<type>/ (check the mint_id: a move is not a deletion); a link in a node to an id that no longer exists at TIP; a protocol regression = a change that removes or weakens a safety rail (a guard, a fail-closed check, a refusal, a lock) without the commit saying why.
- demote: node text (a hypothesis/experiment/verdict/goal/doc) claims something the bytes at TIP do not support (e.g. "PASS"/"landed"/"proved" with no evidence file, numbers that do not match).
- residue: a real defect that does not block (a bug, a test that cannot fail, a stale reference, a wrong path), with file:line.
- Everything else: ok. Do not report style.
Be concrete: every finding cites file:line at TIP (or the commit sha) and quotes <= 2 lines of evidence. Prefer fewer, verified findings over many guesses; mark confidence high/medium.

OUT JSON shape:
{"lane": "<name>", "files_reviewed": N, "red": [{"file":"", "line":0, "commit":"", "what":"", "evidence":"", "confidence":""}], "demote": [...same...], "residue": [...same...], "notes": "<= 5 lines"}
