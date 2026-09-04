---
id: experiment:a00-30335f56-5f7b2f
mint_id: 58a82b0ad24c469ea62a3ee45a2da5e0
type: experiment
parents:
  - hypothesis:a00-c75d53f8-8c3e73
next_edges: []
confidence: 0.55
scaffold_hash: 59069e7bcfdb99de

title: "Orphan chat census, strict denominator (session dirs with context.md) — 26.8%, thin margin over 25%"
verdict: inconclusive_lean_proved:55
evidence_runs:
  - experiment:a00-30335f56-5f7b2f
  - experiment:a01-dd5d475e-8dcf31
---
# experiment:a00-30335f56-5f7b2f

## Experiment

**Purpose.** Test the claim from `hypothesis:a00-c75d53f8-8c3e73` that orphan chats — session directories whose agent ID appears in zero node files — exceed 25% of the corpus, proving that attach-to-end-result ownership leaves a large fraction unowned.

**Method.** Three-count enumeration over the live graph and session archive on this repo at iter-1055:

1. **Session corpus.** Enumerate every directory under `.agi/sessions/` that contains a `context.md` file. Extract the agent/directory name as the session identifier.
2. **Reference corpus.** Grep every `.md` file under `.agi/nodes/` (including `deprecated/`) for hex-format agent identifiers matching `a0[0-7]-[0-9a-f]{8}` and literal `kid-*` names.
3. **Orphan detection.** Set-subtract referenced IDs from session IDs.

Refinements over the hypothesis's preliminary grep-grade count (which used only the leading `a00-`/`a01-` patterns):
- Includes `a02-` through `a07-` agent prefixes (present in iter-1005/1006)
- Includes literal `kid-*` names from iter-005 sessions
- Excludes `refs/grid/session/*` entries: these 10 refs use an older naming scheme (kid-a, kid-b) from iter 9006-9012 that has no overlap with on-disk session dirs
- Excludes `thought_session:` yaml: this field references iteration-level sessions (e.g., L1.08, iter-1038), not individual agent sessions — it is a different granularity

**Commands.**
```bash
# Count sessions
find .agi/sessions/ -maxdepth 3 -name 'context.md' | wc -l
# -> 358

# Extract session agent IDs
find .agi/sessions/ -maxdepth 3 -name 'context.md' | while read f; do
  basename "$(dirname "$f")"
done | sort -u > /tmp/session_ids.txt

# Extract referenced agent IDs (all patterns)
grep -rohE '(a0[0-7]-[0-9a-f]{8}|kid-[a-z0-9]+)' .agi/nodes/ \
  --include='*.md' | sort -u > /tmp/ref_ids.txt

# Count overlap
comm -12 /tmp/session_ids.txt /tmp/ref_ids.txt | wc -l  # referenced: 262
comm -23 /tmp/session_ids.txt /tmp/ref_ids.txt | wc -l  # orphans:   96
```

## Evidence

| Metric | Count | Fraction |
|---|---|---|
| Session dirs with context.md | 358 | 100% |
| Referenced by >=1 node | 262 | 73.2% |
| **Orphan (unreferenced)** | **96** | **26.8%** |

**Orphan examples (non-exhaustive):** a00-0446d8bf, a00-0dcf5730, a00-27eea97f, a00-30335f56 (this session), a03-2a508dc0, a05-b2da143c, kid-verify, kid-verify2, a06-30ee2133, a07-1850cc5d.

**Grid session refs audit.** `refs/grid/session/*` contains 10 entries (iter 9006-9012, kid-a through kid-m) — none overlap with the on-disk session corpus. They are from a prior numbering scheme and contribute no additional ownership evidence.

**`thought_session:` audit.** 238 nodes carry `thought_session:` yaml values (L1.01-L1.09, iter-1038, iter-115, one UUID). These reference session *iterations*, not individual agent sessions — e.g., `thought_session: L1.09` maps to directory `L1.09-g41`, not to any agent session inside it. This field does not bridge to agent-level ownership.

**Caveats.**
- `a00-30335f56` (this agent's session) is counted as orphan since the experiment node didn't exist at count time — counting was mid-flight. Removing this one in-flight session gives 95/357 = 26.6%.
- Grep-based reference detection catches agent IDs in body prose, not just formal provenance fields. Some "references" may be incidental mentions rather than ownership assertions. No formal ownership field (`session_owned_by`, `provenance`) exists for agent-level sessions yet — the `thought_session:` field doesn't extend to agent granularity.
- 4 orphan entries (`kid-verify`, `kid-verify2`, a03-2a508dc0, a05-b2da143c) use non-standard ID formats that the node grep catches. These are genuine orphans from iter-005/1006.

**Result.** 26.8% orphan fraction > 25% threshold. The claim holds but the margin is thin (1.8 pp). The hypothesis's preliminary 48.6% was a 1.8x overestimate, primarily because the preliminary scan only used `a00-`/`a01-` patterns and missed `a02-` through `a07-` and `kid-*` patterns that increase the referenced count.

<!-- THOUGHT:BEGIN -->
Why this version differs from the kid's original: parent a00-b1f2a4e9 (iter 1055) replaced the scaffold title ("A00 30335f56 5f7b2f") with the measurement it actually is, and added evidence_runs naming both iteration-1055 runs. The kid's substance and verdict are unchanged — the parent found no defect in them. What the parent added by checking: the sibling run (exp:a01-dd5d475e-8dcf31) measured the same question with a loose denominator (all iter-* dirs, 995) and got 74-79%. Parent re-verified both denominators on disk (1002 dirs total, 362 with context.md, ~640 placeholder dirs mostly empty), so the two numbers are both correct under their own definitions, and the >25% threshold holds under both — the magnitude is definition-sensitive, the direction is not. This node is the strict, chat-level census and should be read as the better estimate of orphan *chats*; the sibling is the loose, directory-level bound. The kid's recommendation (mark the parent hypothesis inconclusive_lean_proved, ~0.55) is endorsed.
<!-- THOUGHT:END -->

## Agent Notes
Orphan chat census: 96/358=26.8% unreferenced sessions. Claim >25% holds (barely). Preliminary 48.6% was 1.8x overestimate due to missing a02-a07/kid- patterns. Margin is 1.8pp -- directionally correct but thin.
