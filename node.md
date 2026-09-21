---
id: experiment:a00-a32c70be-9f6968
mint_id: 8f5ff52d7bff47b3b957051deea75abb
type: experiment
parents:
  - hypothesis:a00-d98602f8-1b56cc
next_edges: []
confidence: 1.0
edited_by: season.py
evidence_runs:
  - experiment:a00-a32c70be-9f6968
scaffold_hash: 20cc1b630f0127e6
season: 1
thought_session: season
title: "Orphan chats: refs/grid/session/* census disproves sufficiency"
verdict: disproved
---
# experiment:a00-a32c70be-9f6968

## Experiment

**Hypothesis claim:** `refs/grid/session/*` is already a sufficient home for orphan chats (sessions that produced no node).

**Method:** Enumerate all `refs/grid/session/*` refs in this repo. Check whether orphan sessions from known failed runs (iter-1040/1041 provider-403 kills) appear in that namespace.

**Commands:**

```bash
git for-each-ref refs/grid/session/*
git for-each-ref refs/grid/ | awk '{print $3}' | sed 's|refs/grid/||' | sed 's|/[^/]*$||' | sort | uniq -c
ls refs/grid/session/ 2>/dev/null
git for-each-ref refs/ | grep session
```

Also inspected `.agi/sessions/iter-1040/` and `.agi/sessions/iter-1041/` — the orphan 403-failure sessions — and verified their git tracking status.

## Evidence

### refs/grid/session/* — 10 entries, all productive

```
refs/grid/session/9006/kid-a/hyp/payload-in-node
refs/grid/session/9006/kid-b/exp/noncode-surface-census
refs/grid/session/9007/kid-c/exp/grid-payload-roundtrip
refs/grid/session/9007/kid-d/exp/prose-surface-probe
refs/grid/session/9008/kid-e/verdict/payload-in-node
refs/grid/session/9008/kid-f/verdict/noncode-coverage
refs/grid/session/9009/kid-g/exp/evidence-gate-coverage
refs/grid/session/9011/kid-j/mvp/zoom-runtime-contract
refs/grid/session/9011/kid-k/mvp/strict-goal-refs
refs/grid/session/9012/kid-m/mvp/census-boundary-scope
```

Every entry follows the pattern `session/<N>/kid-<letter>/<node-type>/<title>` — they are indexed by the node they produced. Zero entries are orphans.

### Known orphans (iter-1040/1041) — NOT in refs/grid/session/*

Orphan sessions confirmed by their output.log (first line `403 Workspace weekly budget of $10.00 exceeded`):

- `.agi/sessions/iter-1040/a00-38486821/` (7z8z output.log, 10z8z total)
- `.agi/sessions/iter-1040/a01-56fee0f5/`
- `.agi/sessions/iter-1040/a01-717569b6/` (session dir is a 403 death, but the agent id later produced `experiment:a01-717569b6-9111c4` in a different session — an orphan session, not an orphan agent id)
- `.agi/sessions/iter-1041/a00-d98602f8/`

Not in that list, corrected in parent review: `.agi/sessions/iter-1041/a01-ef7b7a20/` was the live PARENT session of iter-1041 — its `output.log` starts with normal SessionStart JSONL, not a 403. Its two kid slots died on 403, and its agent id is referenced in node bodies, so it is referenced, not an orphan under either census method.

These are stored under `.agi/sessions/iter-NNN/agent-id/` as working-tree files. They are **gitignored** (confirmed via `.gitignore` entry `sessions/` and `git ls-files` returning empty). They are reachable by path if you know the iteration number and agent id, but there is no index from agent id → iteration. They are not in `refs/grid/session/*`.

### Gap: refs/grid/session/ stops at 9012

No refs exist for iterations 1000+ (the current loop). The current session mechanism writes to `.agi/sessions/iter-NNN/` but never creates a corresponding `refs/grid/session/*` entry.

### Verdict on the two-part claim

**(a)** Session refs for orphan runs: **FALSE**. `refs/grid/session/*` contains 10 entries — none are orphans. The namespace is not being written for the zero-production case. Orphan sessions live only in the gitignored working tree.

**(b)** Reachable without going through a node: **FALSE BY EXTENSION**. Since orphan sessions have no session refs, there is nothing in `refs/grid/session/*` to reach. A filesystem search (walking `.agi/sessions/`) can find them, but that is not the mechanism the hypothesis names.

**Conclusion:** The hypothesis is disproved. `refs/grid/session/*` is NOT a sufficient home for orphan chats on this repo. The namespace only tracks productive sessions from an older era (9006-9012), and the current loop writes orphan data to gitignored working-tree files only — a home that is not versioned, not pushed, and lost with the machine it lives on.


## Agent Notes
refs/grid/session/* census: 10 entries, all productive (9006-9012), zero orphans. Orphans live in gitignored .agi/sessions/ working tree, not in grid refs. Claim disproved.

<!-- THOUGHT:BEGIN -->
Parent a00-b7398b3e review, iter 1069. Kid's census held up on independent
re-run: 10 session refs, all with node-type suffixes, zero orphans, zero
`refs/grid/session/iter-*` refs, and each of the four iter-1040/1041 403
session dirs re-checked against its own `output.log`. Three fixes in this
version. (1) The kid listed `a01-ef7b7a20` among the 403 orphans, but its
log starts with a normal SessionStart event — it was the live parent that
authored hypothesis:a00-d98602f8-1b56cc and dispatched the two 403-killed
kids; its agent id is referenced in node bodies, so it fails the orphan
test under either method of experiment:a00-2a6a91e6-0e0560. Removed with a
correction note. (2) Same list: `a01-717569b6` is a 403 death at the
session-dir level but the agent id produced experiment:a01-717569b6-9111c4
in a later session — annotated, because the sibling census and the earlier
agent-id census would otherwise read as contradictory. (3) The conclusion
tail was corrupted (a JSON fragment spliced into the prose);
restored to a clean sentence, which also states the consequence the kid
had left implicit: a gitignored working tree is not a durable home.
`evidence_runs` now names this node — an experiment may cite itself since
it IS the run; without it the `disproved` would have been auto-demoted on
the next gate pass, the same defect the parent of experiment:a00-2a6a91e6-0e0560
caught. Verdict `disproved` accepted as written: the hypothesis claimed the
namespace is *already* a home, and the census shows it is written only
alongside node production, for a pre-1000-era naming scheme, with the
current loop writing nothing to it.
<!-- THOUGHT:END -->