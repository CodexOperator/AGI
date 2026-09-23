# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = goal:g5

## Who I am
```
post        thought-master · master of town local-maxxing · owns goal:g5 (the town bundle g5.19-g5.31, + goal:g1.25 in the town bundle) · claude-opus-5-5 · row in config:posts (role director, template cell = the master brief)
authority   INTERIM RULER over the town branch -- full authority, seat assignment included, while the Prime stays quiet (owner 09-19 grant, confirmed 09-23 14:5xZ; the Prime reads the dm logs every 4 h)
formation   doc:formation-local-town: research-focused; no point / helper (directors free-float under me); a framing hedge before minting ideas (a prompt, not a gate)
trunk       MAIN /data/work/agi = local-maxxing/season2/main (no worktree) · tmux agi-rc window thought-master
directors   director-thought gen 14 (research; SELF-LOOPS; REVIEW IN PLACE: rounds wait on loop branches until clean) · director-engine gen 1 (goal:g7.33; g15 residues + goal:g1.25 + brief.py)
rig         the GPU2070S class: 8 GB GPU · 16 threads (2 CCX) · 15 GB RAM · sudo works
pre-approved (owner 09-23) clocks / power limits +10 / -70 pct and voltages +/-10 pct of the recorded baseline · NO per-round spending cap · per-key cap 1 USD KEPT (owner via the Prime 19:08Z)
```

## Live state (20:4xZ 09-23, gen 13)
```
DT LANDED      e0689f715 at c63e1ab8b (pushed) = batch C+D + OSC.01-08 (+ OSC.09's hypothesis) + the TMM.44-58 closes. Gate: 0 conflicts ·
               0 deletions (4106 -> 4124) · links 0 broken · GOALS 340 · anonymize ok · model-name grep 0 in nodes (51 in raw datasets logs,
               TMM.56) · suite on the gated tree in a detached /tmp worktree 6182 passed / 1 failed = core R3. HEAD moved mid-suite -> landed
               tree = gated + exactly the 7 newcomer files (Prime rotation + config:brief, DE rotation); commit-tree + ff-only, nothing staged
               -> [merge-up] to the Prime (router answer re-listed) · TMM.62 to DT · board rewritten 1e6b8b92b (L1 DONE, engine, windows, open)
DE             whole post range landed b0b4fbc9b (gen 12's gate); next merge-up = EF.10's mur + EF.49 50 51+56 54 57-60 62-64 (post tip
               4af82b8a2) + EF.65/66
rotation       owner 20:06Z order DONE, [rotation] sent to the Prime 20:3xZ -- each pin -> its own transcript, the hook prints in each pane:
               TM gen 13 20:10Z (0.16) · DT gen 14 19:51Z, after the 19:47Z hook reinstall: no second rotation, TMM.61 = resume (0.19) ·
               DE gen 1 20:19Z, self-rotated on my TMM.61 (0.08)
L1 rung        DONE on the trunk; router flags with the Prime: -fa on -ctk q4_0 -ctv q4_0 --fit-target 512 = 156,416 tokens (3.15x) at
               +0.074 pct NLL; -ctk q8_0 -ctv q4_0 (1.86x, +0.016 pct) the conservative sibling
PASS 3         the Prime's trunk -> season2/main merge starts 01:37Z 09-24 (~3 h, 2 cores; exact-path Prime commits in MAIN; RED = no merge)
box            20:37Z killed an orphaned probe: python3 - under systemd --user (a 14:32Z penalty() check of kv_speed_round.py @e37e8cca1),
               100 pct of a core for 6 h, pipes dead, its session gone
trunk reds     core R3 only (test_brief g15 fallback)
with the Prime grid_sync ref pushes rejected (0 of 7,867 refs/grid on origin; cron log 582 MB, growing) · goal:g15 retired yet parents
               g15.27-.29 · g15.29.9 cells · box cells (models_dir, ml_scratch_dir, an alias) · the L1 router answer
```

## 🔴 Where it stops
````
```
20:4xZ 09-23  gen 13 at f 0.16; MAIN clean (only cron-owned comms churn), nothing staged; both directors working, no order open
 NEXT   (1) gate the next [merge-up] from either director -- DT: from 96207abf1 (OSC.09's Dispatch line + harvest, OSC.10 after
            mur-director-thought-13, OSC.11) · DE: EF.10's mur + the frozen rounds + EF.65/66 -- review per the traps, land by the
            commit-tree + ff-only method
        (2) the Prime's router answer -> the board's L1 row
        (3) switch mvp (goal:g5.27) round 1 when the queue reaches it
        (4) PASS 3 01:37Z 09-24: keep the trunk green; a landing inside its window rides the next pass -- say so in the [merge-up]
 out    python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```
````

## Traps (post-specific, learned)
```
meter        the prompt hook prints [meter] on a REAL prompt (a nudge, a task notification) -- not on the startup injection; rotate at f 0.47
rotation     rotate.py rotate --post <director> is REFUSED ('equal rank (director = director)') -> order the director's own bare rotate ·
             a pin is verified = .agi/sessions/<post>.meter names the new session's jsonl AND that jsonl shows a [meter] line
orders       dm ONLY: send.py --from thought-master send --to <post> '<text>' via a python argv list (no --body-file); the Prime channel is
             positional: send.py --from thought-master send belam '[tag] ...' · EVERY number, interval or RELAYED residue in an order is
             checked against the bytes first (TMM.52's crossing, TMM.54's '3 reps': both mine) · a fix list names every wording of the error
             (git grep each variant) · NEVER type a real hostname / model name into a dm (comms are committed) · TMM numbers are per
             master, not per dm: next = TMM.63
merge-ups    the WHOLE history rides: list the tip's merges yourself · merge by the NAMED tip · LAND WITHOUT A STAGED MERGE: gate
             M = commit-tree(merge-tree(HEAD, tip)) in a detached /tmp worktree (suite, links, GOALS --check, anonymize on git diff HEAD M);
             at landing T2 = merge-tree(live HEAD, tip) -- if HEAD moved, diff(gated tree, T2) must be exactly the newcomer files and
             byte-identical to HEAD on them; L = commit-tree T2 -p HEAD -p tip -F msg; git merge --ff-only L; push (a rotate committing
             in MAIN consumes any MERGE_HEAD: 436558a46) · a red suite = return the tip
review       workflow.py run agi-merge-up-review --harness pi --args "$(cat args.json)" as a background task (timeout 4h inside); --dry-run first · a superseding tip: review only the delta · stage JSONs can be 'unstructured': parse the string · verify stages die at context-build (60 s) under box load > ~30: check the material defects yourself and say so · a text-only close = verify its diff yourself, no review round
suite        env -u TMUX -u TMUX_PANE, launched with setsid nohup (detached) + a background waiter · ~15 min at load 5, 50 min at load 30-50 · the lock is per graph root (a /tmp worktree locks its own) · judge each red on DETACHED worktrees of the trunk AND the tip (remove after)
anonymize    anonymize.py guards hostname / ip / mac / board / secret (loopback exempt since EF.13); the model name needs its own grep: git grep -i -E 'geforce|rtx ?20[0-9]0' <tip> -- .agi/nodes · drivers that record os.uname().nodename leak the hostname into datasets
write.py     'replace body N:M --force <file>' · a list field = 'set <field> <JSON array>' via a python argv list (no ' && ' inside; --dry-run shows the ring-gate preview) · a goal note -> snapshot-goals.py --render, then --check · the thought verb rewrites a THOUGHT block whole
box          box.* / locations.* are stale here (/home/ubuntu/work/agi absent; repo /data/work/agi) · F13's .env path is dead · an orphan under systemd --user with dead pipes is nobody's: kill it and say so
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card · grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · the startup inbox read truncates at 8000 bytes: full text in .agi/sessions/inbox/thought-master.md + comms/season-2/dm/*--thought-master.md
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime).
