# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = goal:g5

## Who I am
```
post        thought-master · master of town local-maxxing · owns goal:g5 (the town bundle g5.19-g5.31, + goal:g1.25 in the town bundle) · claude-opus-5-5 · row in config:posts (role director, template cell = the master brief)
authority   INTERIM RULER over the town branch -- full authority, seat assignment included, while the Prime stays quiet (owner 09-19 grant, confirmed 09-23 14:5xZ; the Prime reads the dm logs every 4 h)
formation   doc:formation-local-town: research-focused; no point / helper (directors free-float under me); a framing hedge before minting ideas (a prompt, not a gate)
trunk       MAIN /data/work/agi = local-maxxing/season2/main (no worktree) · tmux agi-rc window thought-master
directors   director-thought (research; SELF-LOOPS; REVIEW IN PLACE: rounds wait on loop branches until clean) · director-engine (goal:g7.33; g15 residues + goal:g1.25 + brief.py)
rig         the GPU2070S class: 8 GB GPU · 16 threads (2 CCX) · 15 GB RAM · sudo works
pre-approved (owner 09-23) clocks / power limits +10 / -70 pct and voltages +/-10 pct of the recorded baseline · NO per-round spending cap · per-key cap 1 USD KEPT (owner via the Prime 19:08Z)
```

## Live state (20:1xZ 09-23, gen 12 rotating)
```
DE LANDED      whole post range @291510892 at b0b4fbc9b (suite in MAIN 6182 passed / 1 failed = core R3 only); goal:g7.33 EF.10 line written;
               the Prime nudged (numbers + flags); config:brief's brief cell = the Prime's write now; EF.10's mur + the frozen rounds
               (EF.49 50 51 54 56, EF.57-65) = DE's next merge-up (TMM.60)
               HAZARD HIT: DT's rotate-self committed its spawn row in MAIN mid-window -> 436558a46 (pushed) names 291510892 as a parent with
               only the posts row; b0b4fbc9b carries the content (tree = the gated tree + 3 rotation files); nothing rewritten
DT e0689f715   READY TO LAND = batch C+D + OSC.05-08 + the TMM.54/55/56/57 closes + TMM.58 (the 3 kv-format JSON 'host' -> local-town; the
               drivers drop the field). 60eac6b52 ACCEPTED (TMM.57 verified line by line); my pre-check suite on trunk + 9c227503b = 0 new reds
L1 rung        proposed to the Prime 16:2xZ: -fa on -ctk q4_0 -ctv q4_0 --fit-target 512 = 156,416 tokens (3.15x) at +0.074 pct NLL; the split
               q8K/q4V (1.86x, +0.016 pct) the conservative sibling · OSC.08: the router's flags already at the swept knobs' optimum
rotation       owner 20:0xZ (banked on goal:g5): directors to a stopping point -> rotate them; meter pin verified (0.4455 on the live session)
               -> rotate myself; the Prime nudged. DT self-rotated 19:51Z (gen 14) · DE told to stop (TMM.59), no reply yet
trunk reds     core R3 only (test_brief g15 fallback) -- R2, rolslice x4, pi_bin green since b0b4fbc9b
with the Prime grid_sync ref pushes rejected ('Timed out validating rule': 0 of 7,867 refs/grid on origin, cron log 582 MB, growing) ·
               goal:g15 retired yet parents g15.27-.29 · g15.29.9 cells · box cells (models_dir, ml_scratch_dir, an alias) · the L1 router answer
```

## 🔴 Where it stops
```
20:1xZ 09-23  ROTATED (owner order) at f 0.45 of the 0.47 line; MAIN clean (only cron-owned comms churn), nothing staged
 NEXT   (1) DE's 'at stopping point' dm -> rotate it: its own threshold hook (as DT's at 19:51Z) or rotate.py (spawn --post director-engine
            launches a successor in tmux; read `rotate.py rotate -h` once) -> verify its meter pin
        (2) LAND DT e0689f715 BY NAME: its diff over 60eac6b52 = only the 3 host values + 3 driver lines; merge-tree vs the live head, 0
            deletions, links / GOALS --check / anonymize (committed EF.13 passes loopback) / model-name grep; full suite in MAIN vs core R3;
            ONE commit of the index, push; [merge-up] numbers to the Prime + one line to DT; the board's L1 row
        (3) the Prime's router answer -> the board   (4) switch mvp round 1 when its queue reaches it
 out    python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```

## Traps (post-specific, learned)
```
meter        estimate f from the session jsonl's last usage EVERY few merge-ups; the prompt hook now prints [meter] each turn; rotate at 0.47
orders       dm ONLY: send.py --from thought-master send --to <post> '<text>' via a python argv list (no --body-file) · EVERY number, interval or RELAYED residue in an order is checked against the bytes first (TMM.52's crossing, TMM.54's '3 reps': both mine) · a fix list names every wording of the error (git grep each variant) · NEVER type a real hostname / model name into a dm (comms are committed)
merge-ups    the WHOLE history rides: list the tip's merges yourself · merge by the NAMED tip · a red suite = return (git merge --abort) · ANY post's rotate commits in MAIN: a staged merge left across a rotation gets consumed (436558a46) -> after the suite, check HEAD and MERGE_HEAD before committing; if HEAD moved, verify the index tree = the gated tree + only the newcomer's files, then commit the index · two tips can share ONE suite: stage the octopus, verify its tree = the sequential merge tree, then land them one GO at a time
review       workflow.py run agi-merge-up-review --harness pi --args "$(cat args.json)" as a background task (timeout 4h inside); --dry-run first · a superseding tip: review only the delta · stage JSONs can be 'unstructured': parse the string · verify stages die at context-build (60 s) under box load > ~30: check the material defects yourself and say so · a text-only close = verify its diff yourself, no review round
suite        the Prime's window · env -u TMUX -u TMUX_PANE · ~17 min at low load, 50 min at load 30-50 · judge each red on DETACHED worktrees of the trunk AND the tip (remove after) · a pre-check on a throwaway commit-tree merge in /tmp needs no MAIN window
anonymize    anonymize.py guards hostname / ip / mac / board / secret (loopback exempt since EF.13); the model name needs its own grep: git grep -i -E 'geforce|rtx ?20[0-9]0' <tip> -- .agi/nodes · drivers that record os.uname().nodename leak the hostname into datasets
write.py     'replace body N:M --force <file>' · notes via a python argv list · a goal note -> snapshot-goals.py --render, then --check · the thought verb rewrites a THOUGHT block whole (prior ones live in grid history)
box          box.* / locations.* are stale here (/home/ubuntu/work/agi absent; repo /data/work/agi) · F13's .env path is dead
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card · grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · the startup inbox read truncates at 8000 bytes: full text in .agi/sessions/inbox/thought-master.md + comms/season-2/dm/*--thought-master.md
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime).
