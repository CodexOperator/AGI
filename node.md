---
id: hypothesis:l4-a-manifest-is-a-document-too
mint_id: fade6328750d42a9b3a3f48c297a0252
type: hypothesis
parents:
  - hypothesis:l4-a-round-lives-in-two-trees-so-coming-home-is-a-merge
  - goal:g17.1
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 7874ffa62ab5c538
season: 2
status: pending
tags:
  - l4
  - g17.1
  - sessions
  - worktree
testable_claim: "THE CONFLICT RULE IS RIGHT FOR AGENT RECORDS AND ARBITRARY FOR MANIFESTS, AND THIS ROUND CLOSES THAT CHAIN. `cli.py`'s `_conflict_winner` (landed L4.67) resolves a conflicting `agent.json` by CONTENT via `_AGENT_STATUS_RANK` -- `done` beats `done-unreported`, the actor's own record over the reaper's inference -- and that part is correct, is well defended in its own comment, and IS NOT YOURS TO CHANGE. Everything else ranks -1 and falls to `_src_slug`, a lexicographic worktree- slug tiebreak. MEASURED, live, in dry-run: `python3 extensions/agi/bin/cli.py session-complete L4.56 --dry-run` prints `CONFLICT manifest.json : a00-04c03dd9 wins over sanctuary-director` -- decided by the alphabet. Run it yourself first and paste the three CONFLICT lines. WHY THAT IS WRONG RATHER THAN MERELY UNTIDY: the two `manifest.json` files are ALSO two different documents, exactly like the two `agent.json` files the content rule exists for. The DISPATCHER's manifest describes the round it launched -- the parent's own record, `commits_ahead`, restart bookkeeping. The CHILD's manifest describes the parent's own kids. Neither is a copy or a stale version of the other; they are complementary halves, and picking one by slug name silently discards half the round's bookkeeping from the file a later reader opens first. Nothing is LOST (the loser is kept at `.conflicts/<path>.from-<slug>`), so this is a correctness-of-the-winner problem, not a data-loss one -- say that plainly in your node rather than overstating it. REQUIRED: decide `manifest.json` by CONTENT the way agent records already are, and state your rule and its defence in the node. The obvious candidate is a UNION of the two manifests' `agents` lists keyed by agent id, with a per-entry rule for an id present in both -- and if you take it, the per-entry rule should reuse `_AGENT_STATUS_RANK` rather than invent a second ranking, because two rankings for one question is the defect this chain has been fixing all day. If you conclude a union is wrong and a whole-file precedence is right, SAY WHY and do that instead; a defended simple rule beats an undefended clever one. 🔴 `.manifest.lock` IS NOT A DOCUMENT -- it is a lock file, and merging or ranking one is meaningless. Decide explicitly what happens to it (dropping it from the migration entirely is a defensible answer) rather than letting it fall through the same path as data. PROVED BY: (a) the reproduce command's CONFLICT lines, before and after; (b) a fixture test that two manifests with DISJOINT `agents` lists produce a winner containing BOTH; (c) a fixture test for an agent id present in both, asserting the entry chosen and that it uses the SAME ranking as `agent.json`; (d) a fixture test for whatever you decided about `.manifest.lock`; (e) every EXISTING test in `extensions/agi/tests/test_session_complete.py` unchanged and green -- there are fifteen now and not one line of them may be edited; (f) `python3 -m pytest extensions/agi/tests/test_session_complete.py extensions/agi/tests/test_cli.py extensions/agi/tests/test_dispatch.py -q` GREEN, paste the count; (g) `python3 extensions/agi/bin/commands.py run verify` PASS. DISPROVED IF: `_AGENT_STATUS_RANK` or the `agent.json` rule is changed; a second ranking is introduced for the same question; any existing test is edited; a loser stops being recoverable; `--dry-run` writes; a conflict is still decided by slug for a document that has content semantics; or it is run against the live tree (dry-run only, other seats are dispatching). Do NOT touch `dispatch.py`, `locations.py`, `write.py`, `_sibling_session_lookup`, or the reaper's completion check. HARD CEILING: 2 kids. Do NOT run the full suite. 🔴 OPERATOR NOTE: watch `spawn_budget.py status` for an `-r1` between harvests; the dispatch wrapper's reaper phase ends at ~10 minutes, after which kill the pi pid directly and sweep twice by PID."
thought_session: sanctuary-director-genIV-L4
title: Two manifests are complementary halves, and the alphabet is picking one
---
<!-- BODY:BEGIN -->
# hypothesis:l4-a-manifest-is-a-document-too

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE LAST ROUND OF THIS CHAIN, and I am saying so in the node because the chain is four rounds long and none of it was in the queue I was handed. L4.65 was the prime's to bless and it did; L4.66 was the owner's L4.37 remainder and the prime named its constraints; L4.67 and this one are mine, found by running each round's own output against the real tree. Four rounds on one seam is close to the line my brief draws -- "a run that invents new goals to fill its remaining iterations has spent the owner's tokens on the director's ideas" -- and the reason I judge it on the right side is that every one of them fixed a defect the previous one shipped, in a command that MOVES DATA. Leaving a known-arbitrary conflict rule in code that migrates a round's bookkeeping is not tidiness deferred, it is a defect I found and declined to fix. After this, the seam is closed and the queue's remaining item is the `commands.py` leading flag.

THE MEASUREMENT IS ONE LINE OF DRY-RUN OUTPUT: `CONFLICT manifest.json : a00-04c03dd9 wins over sanctuary-director`. The alphabet is deciding which half of a round's bookkeeping a later reader opens. The dispatcher's manifest carries the parent's own record, `commits_ahead` and the restart bookkeeping; the child's carries the parent's kids. Complementary halves, not versions -- the same shape as the two `agent.json` files that already have a content rule, which is what makes this an inconsistency rather than a missing feature.

I DELIBERATELY DID NOT SPECIFY THE RULE, only its shape. A union keyed by agent id is the obvious candidate and I named it as such, with one constraint that IS mine: if an id appears in both, reuse `_AGENT_STATUS_RANK` rather than inventing a second ranking. Two rankings for one question is precisely the class of defect this chain has spent all day removing -- two terminal-status sets, two agent records, two manifests. And the brief explicitly permits the other answer: a defended whole-file precedence beats an undefended union.

`.manifest.lock` gets its own instruction because it is the trap in this round. It is a lock file, not a document; ranking or merging one is meaningless, and a kid following the union rule mechanically would do exactly that. Dropping it from the migration is a defensible answer and the brief says so, so the round can be right without being clever.
<!-- THOUGHT:END -->
