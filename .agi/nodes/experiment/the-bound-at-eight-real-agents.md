---
id: experiment:the-bound-at-eight-real-agents
mint_id: 934a185a44404ddc82696a078f58fc7a
type: experiment
parents:
  - hypothesis:a03-280a21b7-6d6841
next_edges: []
confidence: 0.9
edited_by: director
evidence_runs: 2
scaffold_hash: 44f393af23837334
thought_session: L1.07
title: Eight real pi agents against the tree-wide bound — and the cost of aiming them all at one node
verdict: proved
---
# experiment:the-bound-at-eight-real-agents

## Experiment

Two live runs, in sequence, deliberately not together.

```bash
# Part B — goal:g1.11's other falsifier half, never run before
<OPENROUTER_PROVISIONING_KEY temporarily removed from .env>
python3 extensions/agi/bin/dispatch.py "$PWD" 1004 --tier kid --target goal:g4.8 --level small

# The bound, at 8
spawn.parallel: 1 -> 8   (max_live stays 25)
python3 extensions/agi/bin/dispatch.py "$PWD" 1005 --tier kid --target goal:g4.8 --level small
```

The live population was **sampled every 2s throughout** rather than read at the
end. A peak is not visible in an end state, and `goal:g4.8` clause 1 is about
the peak.

## Evidence

### Part B — the loop runs with no provisioning key at all

```
provisioning.available()  -> False
dispatch exit             -> 0
"credentials: minting..."  -> ABSENT (the mint path was skipped, not failed)
OPENROUTER_* vars in kid environ -> 0     (pure env-get.sh file fallback)
engine-minted keys        -> 0
shared key usage          -> 4.4687 -> 4.4729   (the kid worked, on the shared key)
```

**`goal:g1.11`'s falsifier is now complete in both halves.** The hardening
feature is not a hard dependency: with it off, the engine behaves exactly as it
did before the feature existed. That was the clause most at risk of being
quietly skipped, because it proves a *negative* and nothing breaks if nobody
runs it.

### The bound at 8 — peak equals cap, on the boundary

113 samples over ~226s of live run:

```
PEAK: leases=8   pi_procs=8   (cap = spawn.parallel 8, max_live 25)
manifest: 8 agents, 0 unadmitted
```

Peak *equals* the cap — on the boundary, not passing it by starvation, which
is the same signature the synthetic run produced at 1/3/5.

### Clause 1 — no kid's node was lost or overwritten

All 8 node files exist, all are real content rather than bare scaffolds
(3.9k–4.9k bytes each), and the corpus grew by **exactly 9** — the 8 kids plus
Part B's one.

```
active_node_count 926 -> 935      broken_links 0
```

`goal:s28`'s warning was that a read-merge-write cycle can look correct and
lose 6 of 8 under load. At 8 concurrent, nothing was lost. `mint_id` being a
UUID with no shared counter is why, which is `hypothesis:a03-280a21b7-6d6841`'s
stated mechanism holding.

### Per-agent attribution, at concurrency

Eight distinct keys, eight distinct bills, all revoked on reclaim:

```
agi-iter1005-kid-a07-1850cc5d  usage=0.005229522
agi-iter1005-kid-a06-4714fa2c  usage=0.005482476
agi-iter1005-kid-a05-bc3ad321  usage=0.005374200
agi-iter1005-kid-a04-7bb380cb  usage=0.004918836
agi-iter1005-kid-a03-280a21b7  usage=0.004266589
agi-iter1005-kid-a02-02affc6b  usage=0.006695212
agi-iter1005-kid-a01-2a74553c  usage=0.006250301
                                          ... a00 already reclaimed and revoked
engine-minted keys outstanding after the run: 0
```

Total for 9 kids across both runs: **$0.089**.

## 🔴 The finding nobody was looking for: concurrency at one target buys duplicates

**Six of the eight kids wrote substantially the same hypothesis** — read from
the bodies, not the titles, because three shipped placeholder titles and the
first count off the titles alone said five:

```
a00  delegator spend sub-linear if review is by-summary          } the
a01  delegator token spend sub-linear, parent summaries          } same
a02  delegator token cost O(P) not O(L)                          } claim
a04  delegator review cost sub-linear in loop count              } six
a06  delegator token spend sub-linear, structural compression    } times
a07  parent reports size-bounded => delegator cost sub-linear    }

a03  parallel kids avoid node collisions (mint_id is a UUID)      distinct
a05  a parent demotes an unevidenced verdict unaided             distinct
```

`a05` is the one that matters most and it nearly went unread: it targets
`goal:g4.8`'s clause 2, the never-observed one, and it arrived under a
placeholder title that made it look like more of the same.

Every slot was aimed with `--target goal:g4.8 --level small`, so all eight got
the *same* 2-hop subtree and independently picked the most salient open thread
in it. **Raising `spawn.parallel` against a single target raises throughput and
not coverage** — the marginal kid re-derives what the previous kid is deriving
right now, because none of them can see each other's work in flight.

This is a cost of the ramp itself and it will get worse, not better, at 16 and
25. It does not invalidate the bound result — the bound is about population,
not content — but it means **the ramp needs target diversity to convert
concurrency into coverage.** Recorded here rather than fixed here.

## 🔴 Second finding: `goal:s31`'s lift fails about a third of the time

Three of eight nodes (a02, a05, a07) shipped with the derived placeholder
title (`A02 02affc6b dc0c54`) and no `testable_claim`, while carrying a
perfectly good claim **in the body**. Same failure as `hypothesis:a00-0fe61f28`
in iteration 1002: 4 of 12 kid nodes across this session, ~33%.

`goal:s31` names three shapes — seed, lift, report. **Seed works; lift does
not.** The kid writes the claim into the body and nothing moves it to
frontmatter, so the field the schema requires stays empty while the
information exists two lines below it.

**It is not cosmetic, and `a05` is the proof.** A placeholder title is what a
reviewer scans; `a05` carried the single most valuable claim in the batch —
`goal:g4.8` clause 2, the one never observed — under a title that read like
noise. Selecting nodes by title, which is what every renderer and every zoom
does, would have dropped it. The lift failure does not corrupt data, it
**hides it from the reader who decides what happens next.**

## What is NOT proved

- **Cap 25.** This ran at 8. `mvp:the-bound-under-real-agents` asks for 5
  parents at cap 25 and that is still open.
- **Clause 2 — a parent demoting an unevidenced verdict unaided.** No parent
  tier was dispatched. This is the clause that distinguishes a parent tier
  from a spawn fan-out, and it remains never-observed.
- **Clause 3 — delegator spend sub-linear in loop count.** Untested, and
  ironically it is what five kids wrote hypotheses about.
- **A `SIGSTOP`ped agent holding its slot.** Not exercised.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Ran at 8 rather than the 25 this mvp's falsifier specifies, and that is a deliberate deviation from the node I am discharging. The owner asked for a deliberate ramp across ten iterations, and the sequencing note in `mvp:the-bound-under-real-agents` gives the reason in its own words: two live runs at an untested concurrency with unmeasured failure modes cannot be attributed if they fail together. Going 1 -> 25 in one step would have been the same mistake inside a single run. The cap-25 clause stays open and is not being quietly counted as closed.

The duplicate-work finding is the part I did not expect and would not have seen at parallel 2. It is a genuine argument against the ramp as I planned it: I had been treating `spawn.parallel` as the coverage knob, and at one target it is not -- it is a throughput knob, and coverage comes from target selection. Recording it as a finding rather than immediately building target diversity, because the honest sequence is to observe it once at 16 before deciding whether it is a defect or a property to route around.

Verdict is `proved` on the bound and on Part B, both of which have run evidence. It is NOT a verdict on the mvp, which asks for more than this run delivered.
<!-- THOUGHT:END -->