---
id: hypothesis:l3-oom-watchdog-kills-live-work
mint_id: e22bd37fbd2e4065816fa7a32b392deb
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 44f04d795135611c
season: 2
testable_claim: "The kills labelled low memory on this box are ONE mechanism reaching real work processes, not a background-task admission limit: dispatch.py parent processes die mid-round well before agent_timeout_mins (SD.06's parent at ~8min against a 1200s reaper), background wait-monitors die 10 of 10 across three distinct shapes, and free -g reports 11-12 GB available at every kill -- while the box carries ~47 claude plus ~27 node processes holding 11 of 23 GB, dominated by kept-alive predecessor sessions that cost ~0 tokens/hour and are never reaped; proven by correlating kill timestamps against per-process RSS and total resident memory, by identifying the actual killer (kernel OOM via dmesg or a harness watchdog via its own logs -- they are distinguishable and nobody has looked), and decisively by archiving the accumulated predecessor sessions and showing the kill rate falls."
thought_session: rc-XIII
title: A memory watchdog is killing live dispatched parents, not just background monitors
---
<!-- BODY:BEGIN -->
# hypothesis:l3-oom-watchdog-kills-live-work

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
MINTED FROM THREE OBSERVATIONS ON 2026-09-08 THAT WERE FILED SEPARATELY AND ARE PROBABLY ONE CAUSE. Flagged by sanctuary-director gen II, which reported the third and correctly asked rather than minting it itself.

OBSERVATION 1, trap 0p and section 6 item 79: background wait-monitors killed with a "low memory" label. Gen II lost 6 of 6 with its own shapes, then 2 of 2 with the prime's run_in_background shape. The prime's own two runs survived. Ten attempts, eight kills, and free -g reported 11-12 GB available at every single one. Item 80 recorded the prime's mechanism-based explanation as DISCONFIRMED and said the difference needed a measurement rather than more prose.

OBSERVATION 2, section 6 item 76 and trap 0n: dispatch.py's reaper exits at its 1200s timeout and the harness reports that exit as a COMPLETED notification while the pi parents keep running. That one is a clean, explainable timeout.

OBSERVATION 3, NEW AND THE ONE THAT CHANGES THE PICTURE: SD.06's actual dispatch.py PARENT process (pid 3911171) was killed for real at roughly 8 minutes, far short of the 1200s timeout. ps confirms gone, not orphaned. Gen II's own words: trap 0n's "reaper gives up cleanly at 20 min" and this "wrapper dies early and hard" may be two different things wearing one label. That is exactly right and it is why this node exists.

THE CANDIDATE CAUSAL CHAIN, stated so it can be attacked rather than believed. Kept-alive predecessor sessions accumulate and are never reaped -- the prime counted about 47 claude and 27 node processes across roughly 25 sessions, many more than a day old, holding 11 of 23 GB. Those sessions cost about 0 tokens per hour, which is exactly why nobody noticed them: they are free on the budget everyone watches and expensive on the one nobody does. Memory pressure builds. A watchdog -- kernel OOM or a harness-level one, and NOBODY HAS CHECKED WHICH -- kills the newest or largest processes. The newest and largest processes are precisely the freshly dispatched parents and their monitors. So the accumulation of IDLE sessions may be killing LIVE work.

IF THAT CHAIN HOLDS IT RETRO-EXPLAINS A GREAT DEAL, and the prediction is what makes it testable rather than a story: parents that died mid-round for no visible reason, the -r1 restarts that followed them, and possibly some share of the branches that landed at zero commits across three consecutive rounds. It also makes section 6 item 82's auto-archive URGENT rather than housekeeping -- the owner asked for it to reduce confusion and reclaim RAM, and if this chain holds, archiving is a fix for rounds dying, which is a far larger prize.

FIRST STEPS, cheapest first, and STOP AT THE FIRST DECISIVE RESULT rather than doing all of them. One, identify the killer: dmesg for kernel OOM entries naming the killed pids, and the harness's own logs for a watchdog. These are distinguishable and it is the single highest-value five minutes available, because every remedy below depends on which one it is. Two, correlate kill timestamps against total resident memory and per-process RSS at those moments, since free -g at the time of ASKING is not the same as memory at the moment of the KILL and that conflation is why this has stayed mysterious. Three, the decisive experiment, which is also the fix the owner already asked for: archive the accumulated predecessor sessions per section 6 item 82 and measure whether the kill rate falls. If it does, this is proved and item 82 is promoted from tidiness to a reliability fix.

DO NOT accept "it is just memory pressure" without naming the killer. Two independent parties have now observed double-digit gigabytes free at the moment of a kill, and an explanation that contradicts the measurement twice is not an explanation. This is the same discipline that corrected trap 0p and item 79 today.

SANCTUARY-DIRECTOR, 2026-09-08T15:12Z -- another data point. SD.07's kid a00-a2edba9e died unprompted (no stop order active) and the reaper correctly auto-restarted it as a00-a2edba9e-r1 (iter=0). Benign, self-healed, not intervened on -- but the crash itself is one more unexplained process death on this box while free -g showed nothing alarming, same shape as the watcher kills. Logged for the timestamp, not because the restart needed handling.
