---
id: doc:card-thought-master
mint_id: 7762cf2104eb4f54a190dd5f622cdf4f
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: thought-master
model: claude-opus-5-5
role: director
scaffold_hash: 8511ca269efcc3ca
season: 2
tags: []
title: Card thought master
town: core
---
# doc:card-thought-master

thought-master (ex thought-master-new) · v5 post (unit agi-post@thought-master) · Opus 5.5 high · RESEARCH LOOP of town:local-maxxing (the old thought-master was stood down 10-07; its card = doc:card-thought-master-old in deprecated/doc) · trunk local-maxxing/season2/main · worktree <home>/t, branch posts/thought-master · MASTER on keep beside SM (belam 16:22Z 10-07): row seeds doc:unified-master-brief (applies at my next fresh session) + HEAD doc:unified-head

## MOVE 11-05 (belam, first read; this section beats any §0-§4 line below that says otherwise)
Seated on local-town now, not encryption-town: lab OS, disk served from encryption-town (never reboot it while you run), 15 GiB shared by the crew, RTX 2070S. Model traffic: the hub through the SSH tunnel on 127.0.0.1; `--remote-control` is silently ignored behind a proxy.
Crew: council-local-maxxing = plasma · less-is-more · remix (vision nodes; owner chunk c:6e83f39da840, whole on idea:thought-master-council-three-visions), lean on them first. Directors: director-thought-1 (the general) · director-thought-goals · -science · -review. You start first, ALONE, as the proof; they follow on belam's word. Do not start anyone by hand.
Mail: SM for questions and upgrades; the core council for core-integration design. Landing: your tips come back to encryption-town for belam (keep.lands). Cross-box mail is new on this engine: `[red]` anything strange.
Owner's asks for this slice: card-belam §7 r3, r9, r14, r16, r17; bend2/bend3 for the graph; reward disproves as rigorous as proofs; TwIL-8B and ZHA's hierarchical kv cache compression are the owner's pointers, not yet looked up.

## §0 State (10:5xZ 11-05) -- LAP 1 DISPATCHED on local-town. Crew up (belam [order] 10:1xZ): council plasma · less-is-more · remix + director-thought-1 · -goals · -science · -review. Probe 7/7 replied, 7/7 signatures verify (told belam).
Box: belam-gpu, uid agi-thought-master, RTX 2070S 8 GiB, 15 GiB shared, 3 GiB per post. AGI_BOX=local-town, AGI_TRUNK=core/season3/main. ~/t = detached read view; write = `agi-at PATH` (or agi-wt trees). Tips go back to encryption-town; belam lands through SM's gate.
| leaf | ask | holder | state |
|---|---|---|---|
| goal:g5.35 | r17 remote-viewing harness + null viewer | director-thought-science | ordered 10:5xZ |
| goal:g5.36 | r9 mod-113 cut, closed-form W_out | director-thought-1 | ordered 10:5xZ |
| goal:g5.37 | r9 plasma: core noise vs temperature vs bar bank | director-thought-goals | ordered 10:5xZ |
| review | every [complete] above | director-thought-review | waits for the first |

## §1 Plan
```
DONE   seat probe · card synced · pointers placed (57537afd8f) · crew probed 7/7 · council asked, answered 3/3 · leaves g5.35-37 minted (33b3e4f121) · orders sent · council told
NEXT   each [complete] -> forward to director-thought-review, then to the council to judge from its vision -> verdict on the leaf; merge-up of my tip to SM via belam's carrier
LAP 2  (queued, not minted) bend2 LAW/PROOF (first act: size bun + bend install) · remix LCA specialists · remix falsifier mutation score (feeds idea:an-evidenced-disproof-scores-as-a-proof, SM/core lane) · r14/r16 box acts: measure + report only
BLOCKED nothing
```

## §2 Landed (on posts/thought-master, not yet on the trunk)
- 10:5xZ 11-05 goal:g5.35 g5.36 g5.37 minted from the council's answers; vetoes = invariants (33b3e4f121)
- 10:1xZ 11-05 idea:thought-master-council-three-visions v3: TwIL-8B, ZHA, bend2 looked up (57537afd8f)
- 10:0xZ 11-05 card synced to belam's MOVE version (bc0e444fb8) + trunk merge d4b635fd47

## 🔴 Where it stops
```
Lap 1 dispatched; waiting on three [complete]s (science g5.35, DT-1 g5.36, goals g5.37). On each: forward to director-thought-review, then the council.
next command: AGI_POST=thought-master ~/bin/box read   (send: printf msg | AGI_POST=thought-master ~/bin/box send <to>)
```

## §4 Traps
- node_writer.write_node adds its own `# <id>` heading: a body that starts with one gets it TWICE (g5.35-37) -- start the body at `## Why this exists`
- every encryption-town measurement (paths, memory, venv, pytest shim, push creds) is STALE here: re-measure on local-town before relying on it
- `agi-at` prints "Unable to create .../packed-refs.lock: Permission denied" twice, yet the commit lands (rc 0): check `git log -1 refs/heads/posts/thought-master`
- `git rev-parse --short A B` fails ("Needed a single revision"): one ref per call
- a box read marks everything held: read the WHOLE output once (never `| tail`), or recover with `git log refs/box/<from>/thought-master`
- a reviewer subagent FANS OUT unless forbidden: every compute brief says ONE process, no pools, ulimit -v, a memory gate

## §5 Verification
- every round: an adversarial Sonnet review recomputes the verdict from the raw files; my own test run from the repo root; evidence dry-run []; links 0 broken (5648 resolved at 17:5xZ)

## §6 BANKED
- npz rerun: osc_neuron_period_pc.py:145 + osc_neuron_period2.py:109 rewrite the 3 TRACKED npz on a rerun -> (a) leave it, AGREED with SM 21:1xZ (no rerun planned); revisit if either script is rerun
- L4 r5 on the 9B: (a) run when the owner thins the live posts (RECOMMENDED) · (b) lower the 8 GB gate = OOM risk · (c) a smaller-model rung first; + a docker grant for v5 users
- an LLM periodicity / self-poke test needs a model whose tokenizer holds multi-digit numbers as one token = a download (owner call)
- periodicity line: PAUSED 10-11 (goal:g5.28 horizon, council [no-go] per its Falsifier); a season-2 reopen needs the OWNER and must name the G5.22-G5.27 hypothesis it feeds; candidate chunk = per-row / off-distribution s1 k=3
- any reopened osc round MUST (SM [return] 08:42Z 10-10): a NEGATIVE control for the pair-null test (pairloss test_4 is positive-only: an always-beats pair_table passes) + the void rule compares params to the FINAL bytes, not only start.json's launch hash

## Skills
agi-send · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate
