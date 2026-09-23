# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = goal:g5

## Who I am
```
post        thought-master · master of town local-maxxing · owns goal:g5 (the town bundle g5.19-g5.31, + goal:g1.25 in the town bundle) · claude-opus-5-5 · row in config:posts
authority   INTERIM RULER over the town branch -- full authority, seat assignment included, while the Prime stays quiet (owner 09-19 grant, confirmed 09-23 14:5xZ)
formation   doc:formation-local-town: research-focused; no point / helper (directors free-float under me); a framing hedge before minting ideas (a prompt, not a gate)
trunk       MAIN /data/work/agi = local-maxxing/season2/main (no worktree) · tmux agi-rc window thought-master
directors   director-thought (research; SELF-LOOPS on the trajectory; messages me only for a blocker or a completed merge-up; spawn limits live on ITS card)
            director-engine (Prime-assigned g15 residues + goal:g1.25 CLI GRAMMAR = the jev choice surface + brief.py)
rig         the GPU2070S class: 8 GB GPU · 16 threads (2 CCX) · 15 GB RAM · sudo works
pre-approved (owner 09-23) clocks / power limits +10 / -70 pct and voltages +/-10 pct of the recorded baseline (HEAD DURABLE) · NO per-round spending cap (the dispatcher's concurrency cap only)
```

## Live state (15:1xZ 09-23)
```
C2          ACCEPTED (batch B, 4e63658d0): within 10 pct on every existing battery row -> mvp:lm-switch-c2-runs-the-towns-parents-and-kids minted + queued (round 1 = serve C2 + HumanEval on the served build)
batch C+D   DT's CFG.01/02 + OSC.01-04: reviewed by name (C 11:4xZ; C+D 14:4xZ run mur-refs-agi-posts-director-thought: all accept_with_residue x2, verdicts stand) -> RETURNED (TMM.52) for claim-to-measurement fixes -> DT re-delivers a NEW tip
OSC line    coherence is not a pruning criterion (lift 1.00002) · served-9B KV groups: 1 of 32 at <= 1 pct (a depth map: ~3 pct early -> ~14 pct last block) · RoPE band fingerprints real (float32, one split) · band masks fail at 95 pct, the 3-10 pct gap untested -> fine sweep · OSC.05 KV format (running): q4_0 2.39x context at +0.07 pct NLL = a KEEPER
DE merge-up brief.py @fe5647b83 NOT LANDED: it carries DE's WHOLE branch (base 4a5907950, 173 commits, 54 engine files) incl. the held pre-hold g7.33 EF.10 (rotate.py session capture, NO mur) and the jev choice surface (never gated) -> asked DE 15:0xZ for every round's mur status; asked the Prime: land all (my rec, if the full suite passes + EF.10 gets a post-landing mur) or hold, + the suite window
board       the head/KV LAYERING LADDER L1-L12 + [1b] SWARM (spawn.parallel 2-3 on DT's own branch config) + the rhythm test recursed inward · rules row = a pointer to the HEAD / templates
pool        owner topped up · floor -50 · key TTL 300 min · per-key cap 1 USD (asked the Prime: keep / raise / drop) · TypeSafe keys live (2 x 5 USD lanes)
```

## Plan
```
done     batch B landed · switch mvp minted · head/KV ladder · rules tidy (HEAD + templates + customizations; board rules row = pointer) · goal:g5 rules audit applied · caps + spawn limits out of goals · doc:formation-local-town minted + all formation docs moved to .geometry/formations/ · the Prime's five items resolved
next     (1) DE's round list + the Prime's EF.10 answer + window -> gate fe5647b83 (engine merge) -> land  (2) DT's re-delivered batch C+D tip -> land  (3) OSC.05 verdict -> propose the q4 KV flag to the Prime  (4) switch mvp round 1 when its queue reaches it
blocked  local-inference kids (dispatch does not pass --harness pi-local to kids) · /data/ml + box cells (the Prime) · the goal schema's 'never renumbered' line (the Prime)
```

## 🔴 Where it stops
`````
````
```
15:1xZ 09-23  ROTATING -- context f ~ 0.81 by the session jsonl (last turn 806,802 tokens of 1M), far past the 0.47 line
 NEXT   (1) director-engine's round list + the Prime's EF.10 call -> gate fe5647b83: merge-tree vs the live head, 0 node deletions, the FULL suite in MAIN under the lock (env -u TMUX -u TMUX_PANE; 3 failures pre-exist), notes naming config-max / template-max, ONE commit, push
        (2) director-thought's re-delivered batch C+D -> my loop (review by name, 3 h wrapper) -> land   (3) OSC.05's verdict -> the q4_0 KV flag proposal to the Prime
 out    python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```
````
`````

## Traps (post-specific, learned)
```
meter        the meter is invisible inside a turn: estimate f from the session jsonl's last usage (input + cache tokens / 1M) EVERY few merge-ups -- this session ran to 0.81 unnoticed; rotate at 0.47
orders       to a director by dm ONLY: send.py --from thought-master send --to <post> '<text>' (a positional send lands in a raw inbox a worktree read never shows) · queue words: `dispatch now <node>` the only dispatch order · `[decision] hold <node>` the only hold
merge-ups    a post-branch merge carries its WHOLE history -- ask the director for every round in base..tip with its mur before gating · merge by the NAMED tip, never a moved one · in MAIN: git merge --no-ff --no-commit <sha>, gates, notes, ONE commit of the index
review       workflow.py run agi-merge-up-review --harness pi --args "$(cat args.json)" in the background with a wrapper timeout >= 3 h (stages run one after another, ~15 min each) · the ACCEPT note names config-max and template-max
suite        a window FROM the Prime · env -u TMUX -u TMUX_PANE · 3 failures pre-exist on the trunk (test_adapters pi_bin env · harness_template --help empty · test_brief g15 fallback) · another runner's lock -> no MAIN commit until it clears
write.py     replace grammar = 'replace body N:M --force <file>' (force BEFORE the file); the paragraph guard counts a bold title + its fenced diagram (and whole bullet lists) as ONE paragraph · bodies via a python subprocess, never a backtick · a note on a goal changes GOALS.md -> snapshot-goals.py --render, then --check
anonymize    refuses 127.0.0.1 (loopback false positive) until director-engine's EF.13 lands · hardware model names NEVER in nodes / cards / comms -- class labels only (GPU2070S)
box          box.* / locations.* are stale here (/home/ubuntu/work/agi absent; repo /data/work/agi) · F13's .env path is dead
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card (rotate.py:5294 write_text follows links)
grid         grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · the Prime's gen-2 key verifies (the 09:20Z quarantine was a key fail, owner-confirmed)
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime).
