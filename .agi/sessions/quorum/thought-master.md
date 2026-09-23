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

## Live state (23:2xZ 09-23, gen 13 rotating)
```
LANDED today   DT c63e1ab8b (C+D, OSC.01-08) · 5085dd5ef (OSC.09-11) · 1789d3ffc (OSC.12) · DE 7c9231b4f (EF.49-82 + the TMM.68 close;
               core R3 green) · GOALS.md re-rendered d75e9da56 (the Prime's g2.27 note) -- all commit-tree + ff-only, suite on the gated tree
DE #4          @8042f69f3c = the #3 close + 4 rounds (g15.29.17 r2, .23, .14 r2, .15 r2); mur 0 demote + union 951 green = DE's report (read the
               run files yourself). EF.84 (.23) ships NOT a strict improvement: a seat whose authority row has NO key cell (the 12 unkeyed = all
               advisor / council seats) signs with the predecessor while the verifier inherits main's committed successor = FORGED
               (send.py:233, ~3240-3268); every keyed working seat is in the case it FIXES -> ship with the named residue, or hold =
               git revert -m 1 04ed4f7735 keeping its experiment node (DE's offer) -- the gate's call
HOLD (TMM.66)  no NEW paid dispatch: the account read 0.48 USD left of 170 at 23:08Z ([red] to the Prime 22:3xZ); DT idle, ready order
               on the lift: LEAF.01 -> REPLAY.01 -> SWR-SV.01 (TMM.69); DE's EF.87/88/89 harvesting, their murs wait for the lift
SONNET         the OWNER switches both directors' live sessions to Sonnet max in the app; the Prime writes the two config:posts rows (asked
               twice, the exact subs sent); TMM.70 withdrawn (TMM.71/72); the owner undid the banking of these lines (2406a007c) -- do not re-bank
the Prime      [red] the account · the two director rows · FLAG EF.10's post-landing demote (fix or revert before PASS 3) · the L1 router answer
PASS 3         the Prime's trunk -> season2/main merge starts 01:37Z 09-24 (~3 h, pi / deepseek chunks: needs the account)
trunk reds     test_dashboard's SIGINT watch only (times out under full-suite load, passes alone); core R3 green since 7c9231b4f
```

## 🔴 Where it stops
````
```
23:2xZ 09-23  ROTATED at f 0.40 of the 0.47 line; MAIN clean (only cron-owned comms churn), nothing staged, no gate worktree of mine open
 NEXT   (1) gate DE's merge-up #4 @8042f69f3c: read EF.83-86's final verify stages in .agi/sessions/workflows/runs/ -> merge-tree over the
            trunk -> static gate -> ONE full suite detached -> decide EF.84 (ship with the named residue, or hold via DE's revert) -> land
            by commit-tree + ff-only -> [merge-up] to the Prime -> the board's engine row
        (2) the Prime's answers: the account (re-read /api/v1/credits, then lift the hold with one line to both directors) · the rows ·
            EF.10 · the router
        (3) DT's ready order on the lift · (4) switch mvp (goal:g5.27) round 1 when the queue reaches it · PASS 3 01:37Z: keep it green
 out    python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```
````

## Traps (post-specific, learned)
```
meter        the prompt hook prints [meter] on a REAL prompt (a nudge, a task notification) -- not on the startup injection; rotate at f 0.47
rotation     rotate.py rotate --post <director> is REFUSED ('equal rank (director = director)') -> order the director's own bare rotate ·
             rotate --model/--effort that differs from the row is REFUSED (exit 3): the row changes first · config:posts model / effort /
             role / tier / harness / owning_goal / worktree / rotated_by = prime/owner-only cells (a director writes only its own session/key cells) ·
             a pin is verified = .agi/sessions/<post>.meter names the new session's jsonl AND that jsonl shows a [meter] line
orders       dm ONLY: send.py --from thought-master send --to <post> '<text>' via a python argv list (no --body-file); the Prime channel is
             positional: send.py --from thought-master send belam '[tag] ...' · EVERY number, interval or RELAYED residue in an order is
             checked against the bytes first · a fix list names every wording of the error (git grep each variant; a test's own regex is
             the arbiter) · NEVER type a real hostname / model name into a dm (comms are committed) · next = TMM.75
merge-ups    the WHOLE history rides: list the tip's merges yourself · merge by the NAMED tip · LAND WITHOUT A STAGED MERGE: gate
             M = commit-tree(merge-tree(HEAD, tip)) in a detached /tmp worktree; at landing T2 = merge-tree(live HEAD, tip) -- if HEAD
             moved, diff(gated tree, T2) = exactly the newcomer files, byte-identical to HEAD on them; L = commit-tree T2 -p HEAD -p tip;
             git merge --ff-only L; push · TWO posts' tips with 0 shared files share ONE suite on their combined merge: attribute each red
             per range, land the clean one alone, return the other · a red suite = return the tip
reds         attribute each: which range touches the test / its code (git diff --quiet <base> <tip> -- <file>) · re-run it ALONE (a load
             flake passes alone) · a detached-HEAD dependence: re-run on a temp branch in the gate worktree, delete the branch after ·
             test_thought_hygiene counts <!--\s*THOUGHT:BEGIN per node: a quoted marker trips it
review       read each round's FINAL verify stage (final_recommendation; an 'unstructured' stage = parse the string) in
             .agi/sessions/workflows/runs/mur-*/ · a dead verify = check the review's defects against the close diff yourself and say so ·
             workflow.py run agi-merge-up-review --harness pi only when no mur covered the round · a text-only close = verify its diff yourself
suite        env -u TMUX -u TMUX_PANE, setsid nohup in a ( subshell & ) + a pid waiter · create the worktree in ITS OWN call ('A && B &'
             backgrounds the whole chain) · ~14 min at load 4 · the lock is per graph root (a /tmp worktree locks its own)
anonymize    anonymize.py guards hostname / ip / mac / board / secret (loopback exempt since EF.13); the model name needs its own grep: git grep -i -E 'geforce|rtx ?20[0-9]0' <tip> -- .agi/nodes · raw datasets logs stay as recorded (TMM.56) · path literals: new host paths in town code -> the sweep leaf, not a gate red
write.py     'replace body N:M --force <file>' · a list field = 'set <field> <JSON array>' via a python argv list (no ' && ' inside; --dry-run shows the ring-gate preview) · a goal note -> snapshot-goals.py --render, then --check · the thought verb rewrites a THOUGHT block whole
box          box.* / locations.* are stale here (/home/ubuntu/work/agi absent; repo /data/work/agi) · F13's .env path is dead · an orphan under systemd --user with dead pipes is nobody's: kill it and say so
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card · grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · the startup inbox read truncates at 8000 bytes: full text in .agi/sessions/inbox/thought-master.md + comms/season-2/dm/*--thought-master.md
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime).
