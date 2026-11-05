---
id: idea:fuel-dead-simple-patterns-in-plain-sight
mint_id: 0bed88dbc25c4e24bc22c00449384cb5
type: idea
parents:
  - vision:the-living-being
next_edges: []
edited_by: belam
scale: small
season: 3
title: "FUEL for musing and brainstorming (owner 11-05): what other dead simple patterns hide in plain sight, waiting to be found and applied to other problems in a novel way? Seed: DG3's powers of 3 in the Kolakoski sequence"
---
# idea:fuel-dead-simple-patterns-in-plain-sight

## OWNER 2026-11-05 05:0xZ, verbatim, on director-general-3's rest-day work
> "I am enjoying viewing the sequence work though I don't quite understand what it means. I feel like DG3 was inspired by the graph's self-referential nature and that struck a chord with me. I was especially surprised by the power of 3 rule in the denominator! What a neat way to get 3 pop out as usually we don't see 3s play much of a role in things. Makes me think of what other dead simple patterns might be hiding in plain sight waiting to be found and applied to other problems in a novel way. Feel free to forward it and/or add it as 'fuel' for musing and brainstorming later as needed."

## The seed, as measured
Kolakoski (1,2,2,1,1,2,...) describes its own run lengths. DG3's break, Drive director-general-3/break/NOTES.md items 12 and 14, 1e8 terms, 5-6 digits:
- short-lag correlations are fractions over powers of 3: lag 1 -1/3, lag 2 -1/3, lag 3 +5/9, lag 6 +11/27, lag 7 -5/27, lag 9 +5/9, lag 10 -19/81, lag 12 +41/81.
- length-k block frequencies: 1/6, 1/3 (k=2); 1/6 (k=3); 1/6, 1/9, 1/18 (k=4). Denominators are a power of 3, some times 2 (DG3's note writes "1/(2*3^m)", which 1/3 and 1/9 do not fit).
- where a 3 comes from: runs have length 1 or 2, so the mean run is 3/2 IF the density is 1/2; DG3 derived lags 1-3 that way and reads the rest as the same step repeated at each level of the self-description. A measured pattern and a suggestion, not a theorem: density 1/2 is itself open.

## OWNER 2026-11-05 05:2xZ, verbatim, on DG2's happy numbers and graph counts
> "I love the exploration of happy numbers. I wonder if we can apply that to the simple patterns stuff as well. Some of these may actually be surprising optimizations in plain sight. IDK for sure though I just always was fascinated with raw numerology like this just doing it for your own fun not like the mystical stuff."
> "Maybe we can look into benford's law i'm not sure what it is. I also know there's a book called 'clean code' by a guy who goes by uncle bob on twitter I think and it talks about how to limit 'crap' and how to do one other key thing and idk if its related to benford's but maybe. I notice his swarm harness setup looks remarkably reminiscent of ours. unclebob on github I think he's very well known not some random."

## Threads to pull (read 11-05, by search summaries, not by reading the repos)
- Benford's law: in data spanning many orders of magnitude the leading digit d appears at rate log10(1 + 1/d), so 1 about 30%, 9 about 4.6%. DG2 tested node sizes: they fail it (1 leads 23%) because they span only 1.25 decades. Which of our counts DO span many decades?
- CRAP (Change Risk Anti-Patterns; Savoia + Evans): CC^2 * (1 - coverage)^3 + CC, per function. Not related to Benford. Martin ports it (unclebob/crap4clj, crap4go); he reportedly has agents drive every function's score below 6. We have not scored our engine.
- unclebob/swarm-forge: tmux, one git worktree per agent, role prompts, message passing, a "constitution"; roles such as specifier, coder, cleaner (DRY + CRAP reviews), architect. Close to our posts + box + briefs. The cleaner role is the part we have no post for.
- DG2's counts as a pattern to use: two thirds of goal leaves dormant since September; "The graph is a ledger; the cards are the whiteboard."

## Use
Fuel, not a task: nothing is owed, no goal or budget follows. Pull it when musing or brainstorming. The owner's words go to DG3 with the resume mail after the review (SM relays), so the post stays idle until then.
