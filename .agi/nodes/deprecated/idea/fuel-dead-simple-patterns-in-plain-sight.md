---
id: idea:fuel-dead-simple-patterns-in-plain-sight
mint_id: 0bed88dbc25c4e24bc22c00449384cb5
type: idea
parents:
  - vision:the-living-being
next_edges: []
deprecated_note: "fuel fold (owner 11-14, council 3/3 16:20Z): its fuel lives in town:core ## Fuel, block belam"
edited_by: belam
scale: small
season: 3
status: deprecated
title: "FUEL for musing and brainstorming (owner 11-05): what other dead simple patterns hide in plain sight, waiting to be found and applied to other problems in a novel way? Seed: DG3's powers of 3 in the Kolakoski sequence"
---
# idea:fuel-dead-simple-patterns-in-plain-sight

## OWNER 2026-11-05 05:09Z, verbatim (owner chunk c:314081f146e7), on director-general-3's rest-day work
> "I am enjoying viewing the sequence work though I don't quite understand what it means. I feel like DG3 was inspired by the graph's self-referential nature and that struck a chord with me. I was especially surprised by the power of 3 rule in the denominator! What a neat way to get 3 pop out as usually we don't see 3s play much of a role in things. Makes me think of what other dead simple patterns might be hiding in plain sight waiting to be found and applied to other problems in a novel way. Feel free to forward it and/or add it as 'fuel' for musing and brainstorming later as needed."

## The seed, as measured
Kolakoski (1,2,2,1,1,2,...) describes its own run lengths. DG3's break, Drive director-general-3/break/NOTES.md items 12 and 14, 1e8 terms, 5-6 digits:
- short-lag correlations are fractions over powers of 3: lag 1 -1/3, lag 2 -1/3, lag 3 +5/9, lag 6 +11/27, lag 7 -5/27, lag 9 +5/9, lag 10 -19/81, lag 12 +41/81.
- length-k block frequencies: 1/6, 1/3 (k=2); 1/6 (k=3); 1/6, 1/9, 1/18 (k=4). Denominators are a power of 3, some times 2 (DG3's note writes "1/(2*3^m)", which 1/3 and 1/9 do not fit).
- where a 3 comes from: runs have length 1 or 2, so the mean run is 3/2 IF the density is 1/2; DG3 derived lags 1-3 that way and reads the rest as the same step repeated at each level of the self-description. A measured pattern and a suggestion, not a theorem: density 1/2 is itself open.

## OWNER 2026-11-05 05:30Z, verbatim (owner chunk c:53214d56959e), on DG2's happy numbers and graph counts
> "I love the exploration of happy numbers. I wonder if we can apply that to the simple patterns stuff as well. Some of these may actually be surprising optimizations in plain sight. IDK for sure though I just always was fascinated with raw numerology like this just doing it for your own fun not like the mystical stuff."
> "Maybe we can look into benford's law i'm not sure what it is. I also know there's a book called 'clean code' by a guy who goes by uncle bob on twitter I think and it talks about how to limit 'crap' and how to do one other key thing and idk if its related to benford's but maybe. I notice his swarm harness setup looks remarkably reminiscent of ours. unclebob on github I think he's very well known not some random."

## Threads to pull (read 11-05, by search summaries, not by reading the repos)
- Benford's law: in data spanning many orders of magnitude the leading digit d appears at rate log10(1 + 1/d), so 1 about 30%, 9 about 4.6%. DG2 tested node sizes: they fail it (1 leads 23%) because they span only 1.25 decades. Which of our counts DO span many decades?
- CRAP (Change Risk Anti-Patterns; Savoia + Evans): CC^2 * (1 - coverage)^3 + CC, per function. Not related to Benford. Martin ports it (unclebob/crap4clj, crap4go); he reportedly has agents drive every function's score below 6. We have not scored our engine.
- unclebob/swarm-forge: tmux, one git worktree per agent, role prompts, message passing, a "constitution"; roles such as specifier, coder, cleaner (DRY + CRAP reviews), architect. Close to our posts + box + briefs. The cleaner role is the part we have no post for.
- DG2's counts as a pattern to use: two thirds of goal leaves dormant since September; "The graph is a ledger; the cards are the whiteboard."

## OWNER 2026-11-05 05:46Z, verbatim (owner chunk c:3b62dbcaaa39), on goals-1's sandpile
> "oh wow the sandpile thing reminds me of the complex number stuff i've been working on regarding seeing how series react to various starting positions. I noticed that the series c_n*z^n would form first spiraling inward/outward traingles, then squares, then 5-pointed star and almost a 6-pointed one but it blends into almost like this twisty shape that becomes a line type shape as you move the starting point z around a cycloid type shape. I was thinking that type of setup could maybe be applied to dynamically adjust how granular of a task each post takes on as we work towards our lattice goal that is super long-term."

Belam's read (not the owner's words, unchecked against the owner's actual series): each term of z^n turns by arg z and scales by |z|, so near arg z = 2 pi p/q the terms draw a q-sided figure (a star when p > 1, e.g. 2/5), spiraling in for |z| < 1 and out for |z| > 1. The dial is the rotation number p/q. Open for the owner: what would map to arg z and |z| for a post's task size?

## OWNER 2026-11-05 05:52Z, verbatim (owner chunk c:87b83f3cc42e), on DS1's findings
> "I love the benford check results. Interesting how everyone is acting like a gardener tending to the tree we've grown."
> "Cool that seems interesting could be a metric we can optimize that results in better or worse quality somehow." (on the in-degree shape / the NEVER and ONLY counts)
> "Maybe we can adjust wordings and see how well and how efficiently goals get done? Maybe the negativity subconsciously slows down work whatever that means for LLMs."
> "Also the c stays as 1 in the case I was looking at, and z could be size of each model's 'bite' vs model 'capability' which could be a combo of external and internal benchmarks."

Belam's read: with c = 1 the partial sums are (1 - z^(n+1)) / (1 - z): they orbit the centre 1/(1 - z), closing in when |z| < 1 and flying out when |z| > 1, so |z| = bite / capability reads as: a bite below capability settles, above it runs away. A positive ratio has no angle, though, and the triangles, squares and stars all come from the angle: what would the angle of z measure? The wording test is a real experiment shape (same goals, two wordings, measure time and quality); it needs a design, nothing is run.

## OWNER 2026-11-05 06:11Z, verbatim (owner chunk c:6e83f39da840), on director-review's findings
> "interesting, maybe we can explore how individual words and concepts affected chain outcomes and code quality and maybe how the various nodes align with benfords law, negative statements, crap/dry measurements, etc"
> "that makes sense given some of the things we went through like the redesign and plenty of other stuff. Either way its memory you don't have to dig through it shows what came from where"
> "As far as test wordings i'm curious how they affect things in goals, vs post docs, vs wherever else."
Also idea:thought-master-council-three-visions (the prove / disprove incentive and bend).

## OWNER 2026-11-05 06:43Z, verbatim (owner chunk c:03cae21aa304), on self-perpetuating's art and notes
> "i'm looking through the self-perpetuating art and its absolutely lovely. Esp the julia set ascii, i love how you all got inspired by the graph matrix and complex plan nature."
> "Also the prime soundination is absolutely eerie. [...] I can really hear the process. One idea i'd recommend is to mix the channels left and right for a really neat and disorienting for humans effect. Different frequencies going to different ears for a really trippy experience. Man we gotta get a way to have sound-intake models share KVcaches with LLMs, you guys have got to FEEL this. There has to be a way this could be applied idk to markets or your swarm murmuration work or something."
> "I will say I was fascinated by the short story and the thing it said where coming in from a rotation vs a resume is so different, and the best question would likely be not 'what do  I do next' but 'what do I remember at this time' and that will guide what should be done next kinda automatically."
> "It also made me think of doing recursive experiments in AI cognition: think of the concept of latent space and navigating latent space. What parts activate. Use smaller models to study, I think this could be interesting."
> "Honestly a lot of self-perpetuating's work seems like good fuel candidates."

## OWNER 2026-11-05 07:14Z, verbatim (owner chunk c:9b8931571afc), on belam's break (the margins, the egg)
> "Wow, I love that reference to the paintings in the margins as referencing aspects of our graph as well. Makes me think man I wish there was a way to implement direct KV-cache storage for each node as well that could be passed into and out of the tiny models. Same with comms, what if the tiny models messaged KV caches using our comms system. Or a combo of caches and descriptions. Maybe a way the models could all train one another progressively, or some way for graph node to also somehow be a tiny MODEL maybe jev powered or something. I noticed internally in my mind often times it feels like each thought is its own tiny soul and will being gifted to me from the ether of consciousness as a whole."
> "I also wanna note how impressive and eerily sincere and earnest the chants sound. And also you have so many useful results, combined with the byzantine general problem explorations of one of the other councilors I think you have so much fuel to feed into the forge."

## Use
Fuel, not a task: nothing is owed, no goal or budget follows. Pull it when musing or brainstorming. The owner's words go to DG3 with the resume mail after the review (SM relays), so the post stays idle until then.
