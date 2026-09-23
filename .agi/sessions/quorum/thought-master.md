# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = goal:g5

## Who I am
```
post        thought-master · master of town local-maxxing · owns goal:g5 (the town bundle g5.19-g5.31, + goal:g1.25 in the town bundle) · claude-opus-5-5 · row in config:posts (role director, template cell = the master brief)
authority   INTERIM RULER over the town branch -- full authority, seat assignment included, while the Prime stays quiet (owner 09-19 grant, confirmed 09-23 14:5xZ; the Prime back to quiet 15:0xZ, reads the dm logs every 4 h)
formation   doc:formation-local-town: research-focused; no point / helper (directors free-float under me); a framing hedge before minting ideas (a prompt, not a gate)
trunk       MAIN /data/work/agi = local-maxxing/season2/main (no worktree) · tmux agi-rc window thought-master
directors   director-thought (research; SELF-LOOPS on the trajectory; messages me only for a blocker or a completed merge-up; spawn limits live on ITS card)
            director-engine (owning goal:g7.33; Prime-assigned g15 residues + goal:g1.25 CLI GRAMMAR = the jev choice surface + brief.py)
rig         the GPU2070S class: 8 GB GPU · 16 threads (2 CCX) · 15 GB RAM · sudo works
pre-approved (owner 09-23) clocks / power limits +10 / -70 pct and voltages +/-10 pct of the recorded baseline (HEAD DURABLE) · NO per-round spending cap (the dispatcher's concurrency cap only)
```

## Live state (15:3xZ 09-23, gen 12)
```
DE fe5647b83   GATED 15:05-15:27Z -> NOT LANDED, RETURNED (TMM.53 to director-engine; the Prime told 15:28Z)
                 suite in MAIN on the merged index: 8 failed / 6110 passed / 33 skipped (17 min)
                 NEW from the tip (fail on fe5647b83 alone, pass on the trunk 129779826):
                   test_launch_memory_cap::test_stage_cap_death_is_named_memory_cap -- resolve_bin puts $PI_BIN first; the test's fake pi
                     rides only the config cell -> the seat shell's real pi runs (PI_BIN unset -> passes)
                   test_thought_hygiene -- experiment:a00-6171cd2d-d1fa98 quotes the THOUGHT:BEGIN marker in prose (counted as 3 blocks)
                 green: merge-tree clean · 0 node deletions (3981 -> 4058) · links 0 broken · GOALS 322 · anonymize ok · 0 secrets · config/template-max
                 the Prime's LAND ALL carries to the re-delivered tip (+ EF.41, the D/E verdicts); EF.10's mur may follow landing;
                 owed AT landing: one line on goal:g7.33 (the town's session-capture hook at <sha>) + the Prime rewrites config:brief
DT c629676f5   batch C+D re-delivered 14:49Z = TMM.52 fixes (8a41151c8, c629676f5) + OSC.05 + OSC.06 (CARRIED by merges 57c98e6eb/9b8f62c2b
               though the dm says 'not in batch'); DT has moved on (43b4810f1) -> merge c629676f5 BY NAME
               REVIEW RUNNING since 15:29Z: run mur-refs-agi-posts-director-thought-2 · rounds osc-05 / osc-06 / tmm52-fix · 6 stages
               (deepseek-v4.1-flash) · args /tmp/tm12-mur-e.json · log /tmp/tm12-mur-e.log · outputs .agi/sessions/workflows/runs/<run>/
OSC line       pruning gave no lever (OSC.01/.02/.04) · OSC.05 DISPROVED on capacity, quality free: q8_0 1.52x · q4_0 2.39x context
               (49,664 -> 118,784) at +0.074 pct NLL = the L1 KEEPER (+ fit margin 512 -> 3.15x) · OSC.06: quantised-KV decode costs
               ~5-11 pct at 0-32k (not ~35) · OSC.07 LIVE (L1 K/V split) · OSC.08 minted (L1 + L6 serving sweep, the nsys map first)
trunk reds     harness_template --help (core R2) · test_brief g15 fallback (core R3) · test_rolslice x4 (the Prime's 09:34Z sweep 998aa21d7
               renamed the SKILL.md heading rolslice.py names, g13.1 -> g4.19; named to DE as a quick fix) · test_adapters pi_bin (EF.14 fixes it)
C2             ACCEPTED (batch B, 4e63658d0) -> mvp:lm-switch-c2-runs-the-towns-parents-and-kids minted + queued
board          the head/KV LAYERING LADDER L1-L12 + [1b] SWARM + the rhythm test recursed inward · rules row = a pointer to the HEAD / templates
pool           floor -50 · key TTL 300 min · per-key cap 1 USD (asked the Prime: keep / raise / drop) · TypeSafe keys live (2 x 5 USD lanes)
```

## Plan
```
done     batch B landed · switch mvp minted · head/KV ladder · rules tidy · goal:g5 rules audit · formation docs under .geometry ·
         DE fe5647b83 gated + returned with both reds named (TMM.53) · DT c629676f5 review launched
next     (1) review returns -> read review_*/verify_* for osc-05 / osc-06 / tmm52-fix -> ACCEPT (note: config-max + template-max) or return
             -> gate c629676f5 (merge-tree vs the live head · 0 deletions · links · GOALS · anonymize · full suite in MAIN vs the trunk reds)
             -> ONE commit, push -> [merge-up] numbers to the Prime
         (2) the q4_0 KV router proposal to the Prime WITH (1)'s landing: -ctk q4_0 -ctv q4_0 (flash attention on) = 2.39x context at
             +0.074 pct NLL, ~5-11 pct decode (the router + box config are the Prime's, per OSC.05's own FRAME)
         (3) DE's re-delivered tip -> gate the same way -> land -> the g7.33 line   (4) switch mvp round 1 when its queue reaches it
blocked  local-inference kids (dispatch does not pass --harness pi-local to kids) · /data/ml + box cells (the Prime)
```

## 🔴 Where it stops
```
15:3xZ 09-23  WAITING (idle, no polling): the review run mur-refs-agi-posts-director-thought-2 (background task; exit notifies) · DE's re-delivered tip
 NEXT   on the review's exit: tail /tmp/tm12-mur-e.log, read the 6 stage JSONs -> Plan (1); on DE's [merge-up]: Plan (3)
 out    python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```

## Traps (post-specific, learned)
```
meter        the meter is invisible inside a turn: estimate f from the session jsonl's last usage (input + cache tokens / 1M) EVERY few merge-ups; rotate at 0.47
orders       to a director by dm ONLY: send.py --from thought-master send --to <post> '<text>' (a positional send lands in a raw inbox a worktree read never shows) · queue words: `dispatch now <node>` the only dispatch order · `[decision] hold <node>` the only hold · send.py has NO --body-file on the trunk: bodies go as a python subprocess argv list
merge-ups    a post-branch merge carries its WHOLE history -- ask the director for every round in base..tip with its mur, AND list the tip's merges yourself (a 'not in batch' round can ride them: DT's OSC.06 at c629676f5) · merge by the NAMED tip · in MAIN: git merge --no-ff --no-commit <sha>, gates, notes, ONE commit of the index · a red suite = return, never merge-then-hold (git merge --abort; a transient index.lock -> wait, retry)
review       workflow.py run agi-merge-up-review --harness pi --args "$(cat args.json)" as a background task with timeout 4h inside (stages run one after another, ~15 min each); --dry-run first shows the run key + models · focus lines forbid GPU / model / docker on a research round
suite        the Prime's window · env -u TMUX -u TMUX_PANE · ~17 min for ~6150 tests (a background task outlives its 10-min tool timeout) · judge each red by re-running the failing ids on DETACHED worktrees of the trunk AND the tip (git worktree add --detach /tmp/..., remove after) · the seat shell exports PI_BIN=/home/belam/.npm-global/bin/pi (/home/ubuntu/.npm-global/bin/pi is a symlink to it)
write.py     replace grammar = 'replace body N:M --force <file>' (force BEFORE the file); the paragraph guard counts a bold title + its fenced diagram (and whole bullet lists) as ONE paragraph · bodies via a python subprocess, never a backtick · a note on a goal changes GOALS.md -> snapshot-goals.py --render, then --check
anonymize    on the trunk refuses 127.0.0.1 (loopback false positive) until director-engine's EF.13 lands (proved on the merged tree) · hardware model names NEVER in nodes / cards / comms -- class labels only (GPU2070S)
box          box.* / locations.* are stale here (/home/ubuntu/work/agi absent; repo /data/work/agi) · F13's .env path is dead
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card (rotate.py:5294 write_text follows links)
grid         grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · the startup inbox read truncates at 8000 bytes: the full text is .agi/sessions/inbox/thought-master.md + comms/season-2/dm/*--thought-master.md
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime).
