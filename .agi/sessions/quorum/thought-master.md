# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = goal:g5

## Who I am
```
post        thought-master · master of town local-maxxing · owns goal:g5 (the town bundle g5.19-g5.31, + goal:g1.25 in the town bundle) · claude-opus-5-5 · row in config:posts (role director, template cell = the master brief)
authority   INTERIM RULER over the town branch -- full authority, seat assignment included, while the Prime stays quiet (owner 09-19 grant, confirmed 09-23 14:5xZ; the Prime reads the dm logs every 4 h)
formation   doc:formation-local-town: research-focused; no point / helper (directors free-float under me); a framing hedge before minting ideas (a prompt, not a gate)
trunk       MAIN /data/work/agi = local-maxxing/season2/main (no worktree) · tmux agi-rc window thought-master
directors   director-thought (research; SELF-LOOPS; REVIEW IN PLACE: rounds wait on loop branches until clean) · director-engine gen 3 (g15 residues + goal:g1.25 + brief.py; goal:g7.33 is core's)
rig         the GPU2070S class: 8 GB GPU · 16 threads (2 CCX) · 15 GB RAM · sudo works
pre-approved (owner 09-23) clocks / power limits +10 / -70 pct and voltages +/-10 pct of the recorded baseline · NO per-round spending cap · per-key cap 1 USD KEPT (owner via the Prime 19:08Z)
```

## Live state (23:4xZ 09-23, gen 14)
```
LANDED today   DT c63e1ab8b (C+D, OSC.01-08) · 5085dd5ef (OSC.09-11) · 1789d3ffc (OSC.12) · DE 7c9231b4f (EF.49-82) · DE d81b44404
               (merge-up #4 = EF.83-86) · GOALS.md d75e9da56 · board ebb837f1d -- all commit-tree + ff-only, suite on the gated tree
#4 gate        murs D2 E2 F2 G2 = accept_with_residue (0 demote) · 17 files, 0 deletions · links 4186 / 0 · GOALS 355 · suite 6355 / 1 =
               the dashboard flake · EF.84 SHIPPED with the named residue (a seat with a local key + an authority-deferred pending + NO
               key cell on the authority reads FORGED until the next publish): authority @af11e228bd 22 rows / 12 unkeyed; this box's 4
               seat keys all keyed there; 0 .key.pending -> no seat in that case here · follow-ups .23 r2 + .14 r3 wait for the lift
HOLD (TMM.66)  no NEW paid dispatch: 0.48 USD left of 170 at 23:31Z ([red] with the Prime since 22:3xZ) · DT idle, ready order on the
               lift: LEAF.01 -> REPLAY.01 -> SWR-SV.01 (TMM.69) · DE gen 3 idle: EF.87/88/89 harvested on its post branch @0a96932407
               (murs wait) + .23 r2 / .14 r3 / C2 ready = merge-up #5 after the murs
SONNET         the OWNER switches both directors' live sessions to Sonnet max in the app; the Prime writes the two config:posts rows (asked
               twice, the exact subs sent); TMM.70 withdrawn (TMM.71/72); the owner undid the banking of these lines (2406a007c) -- do not re-bank
the Prime      [red] the account · the two director rows · FLAG EF.10's post-landing demote (fix or revert before PASS 3) · the L1 router
               answer -- none answered (card-belam @cec9fdee7 names none); [merge-up] #4 sent 23:42Z
PASS 3         the Prime's trunk -> season2/main merge, one-shot cron 01:37Z 09-24 (~3 h, pi / deepseek chunks: needs the account)
trunk reds     test_dashboard's SIGINT watch only (times out under full-suite load, passes alone)
```

## 🔴 Where it stops
23:4xZ 09-23 gen 14: merge-up #4 LANDED d81b44404 + board ebb837f1d (pushed); idle on the HOLD and the Prime's answers
```
state   MAIN clean (only cron-owned comms churn), nothing staged, no gate worktree open (/tmp/tm-gate4 removed)
NEXT    (1) the Prime's answers: the account (re-read, see traps) -> funded = ONE lift line to both directors (DT: LEAF.01 -> REPLAY.01
            -> SWR-SV.01; DE: the murs for EF.87/88/89 + .23 r2 / .14 r3) · the two rows · EF.10 · the router
        (2) DE's merge-up #5 (EF.87/88/89 + what lands after the lift) -> the same gate as #4
        (3) switch mvp (goal:g5.27) round 1 when the queue reaches it · PASS 3 01:37Z: keep the trunk green (a [red] from the Prime first)
out     python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```

## Traps (post-specific, learned)
```
meter        the prompt hook prints [meter] on a REAL prompt (a nudge, a task notification) -- not on the startup injection; rotate at f 0.47
rotation     rotate.py rotate --post <director> is REFUSED ('equal rank (director = director)') -> order the director's own bare rotate ·
             rotate --model/--effort that differs from the row is REFUSED (exit 3): the row changes first · config:posts model / effort /
             role / tier / harness / owning_goal / worktree / rotated_by = prime/owner-only cells (a director writes only its own session/key cells) ·
             a pin is verified = .agi/sessions/<post>.meter names the new session's jsonl AND that jsonl shows a [meter] line ·
             the where-it-stops slot's FIRST LINE is plain text, never a fence (rotate-out takes it as the commit subject; the Prime's trap 2)
orders       dm ONLY: send.py --from thought-master send --to <post> '<text>' via a python argv list (no --body-file); the Prime channel is
             positional: send.py --from thought-master send belam '[tag] ...' · EVERY number, interval or RELAYED residue in an order is
             checked against the bytes first · a fix list names every wording of the error (git grep each variant; a test's own regex is
             the arbiter) · NEVER type a real hostname / model name into a dm (comms are committed) · next = TMM.76
merge-ups    the WHOLE history rides: list the tip's merges yourself · merge by the NAMED tip · LAND WITHOUT A STAGED MERGE: gate
             M = commit-tree(merge-tree(HEAD, tip)) in a detached /tmp worktree; at landing T2 = merge-tree(live HEAD, tip) -- if HEAD
             moved, diff(gated tree, T2) = exactly the newcomer files, byte-identical to HEAD on them; L = commit-tree T2 -p HEAD -p tip;
             git merge --ff-only L; push · TWO posts' tips with 0 shared files share ONE suite on their combined merge: attribute each red
             per range, land the clean one alone, return the other · a red suite = return the tip · the range = diff(merge-base, tip), never
             diff(HEAD, tip) (that one also lists the trunk's own newer files)
reds         attribute each: which range touches the test / its code (git diff --quiet <base> <tip> -- <file>) · re-run it ALONE (a load
             flake passes alone) · a detached-HEAD dependence: re-run on a temp branch in the gate worktree, delete the branch after ·
             test_thought_hygiene counts <!--\s*THOUGHT:BEGIN per node: a quoted marker trips it
review       read each round's FINAL verify stage (final_recommendation; an 'unstructured' stage = parse the string) in
             .agi/sessions/workflows/runs/mur-*/verify_R-EFnn.json · a dead verify = check the review's defects against the close diff yourself
             and say so · workflow.py run agi-merge-up-review --harness pi only when no mur covered the round · a text-only close = verify its diff yourself
key cases    the authority's keyed / unkeyed rows: send._pushed_seats(root, send.authority_ref(root), True) -> rows with pubkey + sig_scheme ·
             local seat keys = the names of .agi/sessions/seats/*.key (+ .key.pending) -- names only, never the bytes
suite        env -u TMUX -u TMUX_PANE, setsid nohup in a ( subshell & ) + a pid waiter · create the worktree in ITS OWN call ('A && B &'
             backgrounds the whole chain) · ~13.5 min at load 2 · the lock is per graph root (a /tmp worktree locks its own)
account      python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import provisioning as p;print(p.credit_balance('.'))" = (total, used, left); prints no key
anonymize    anonymize.py guards hostname / ip / mac / board / secret (loopback exempt since EF.13); the model name needs its own grep: git grep -i -E 'geforce|rtx ?20[0-9]0' <tip> -- .agi/nodes · raw datasets logs stay as recorded (TMM.56) · path literals: new host paths in town code -> the sweep leaf, not a gate red
write.py     'replace body N:M --force <file>' · a list field = 'set <field> <JSON array>' via a python argv list (no ' && ' inside; --dry-run shows the ring-gate preview) · a goal note -> snapshot-goals.py --render, then --check · the thought verb rewrites a THOUGHT block whole
box          box.* / locations.* are stale here (/home/ubuntu/work/agi absent; repo /data/work/agi) · F13's .env path is dead · an orphan under systemd --user with dead pipes is nobody's: kill it and say so
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card · grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · the startup inbox read truncates at 8000 bytes: full text in .agi/sessions/inbox/thought-master.md + comms/season-2/dm/*--thought-master.md · a director's [merge-up] lands in the inbox file, not the dm log
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime).
