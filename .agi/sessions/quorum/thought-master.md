# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = goal:g5

## Who I am
```
post        thought-master · master of town local-maxxing · owns goal:g5 (the town bundle g5.19-g5.31, + goal:g1.25 in the town bundle) · claude-opus-5-5 · row in config:posts (role director, template cell = the master brief)
authority   INTERIM RULER over the town branch -- full authority, seat assignment included, while the Prime stays quiet (owner 09-19 grant, confirmed 09-23 14:5xZ; the Prime reads the dm logs every 4 h)
formation   doc:formation-local-town: research-focused; no point / helper (directors free-float under me); a framing hedge before minting ideas (a prompt, not a gate)
trunk       MAIN /data/work/agi = local-maxxing/season2/main (no worktree) · tmux agi-rc window thought-master
directors   director-thought (research; SELF-LOOPS; REVIEW IN PLACE) · director-engine gen 3 (g15 residues + goal:g1.25 + brief.py; goal:g7.33 is core's)
rig         the GPU2070S class: 8 GB GPU · 16 threads (2 CCX) · 15 GB RAM · sudo works
pre-approved (owner 09-23) clocks / power limits +10 / -70 pct and voltages +/-10 pct of the recorded baseline · NO per-round spending cap · per-key cap 1 USD KEPT (owner via the Prime 19:08Z)
```

## Live state (01:3xZ 09-24, gen 14)
```
LANDED         DE d81b44404 (merge-up #4 = EF.83-86; EF.84 with the named no-cell residue, 0 such seats here) + the earlier 09-23 landings
HOLD (TMM.66)  no PAID OpenRouter dispatch: 0.48 USD left of 170 at 23:31Z; the OWNER: "Standby for openrouter credits"
0-CREDIT LANE  the OWNER, 13 lines 00:xZ-01:3xZ 09-24, verbatim on goal:g5 (TMM.76-80)
  local brain  OrcaBonsai C2 = Bonsai 2 27B PTQ1_0 + abliterate LoRA scale 2.0 (DT's choice = the town's C2 arm), PrismML fork b10685 (CUDA),
               q4_0 KV, ONE 65,536-token slot, 7.29 GB, decode ~20 tok/s, prefill ~250 tok/s · container brain-orcabonsai27b on 127.0.0.1:8080
               · the old router container llama-server STOPPED (restore: docker start llama-server) · DT: experiment:director-thought-brain-swap-2026-09-24
  local round  export PI_CODING_AGENT_DIR=/data/ml/pi-agent-local (built-in openrouter provider -> :8080) + the STANDARD town line -> parent
               AND kids local (the adapter builds each child env from its parent's) -- UNVERIFIED until DT's first such round (TMM.79)
  default pi   ~/.pi/agent/models.json byte-identical to /data/ml/pi-models.json.before-20260924T0109Z (the box-wide redirect was NOT applied;
               PASS 3 + other posts stay on OpenRouter)
  slot         ONE local round at a time · DE's EF.90 (pi-local kid a00-0d0977d3, 01:29Z: every spawn exports its resolved harness as
               AGI_HARNESS -> kids inherit) = DE's LAST local round; then the slot is DT's ALONE (leaf A = hypothesis:lm-paths-py-resolves-
               proposed-box-roots @8ca1a1d1cd queued) and DE runs on pi-free (TMM.81 / TMM.82) · DT's check: no live EF.* in spawn_budget status
  free cloud   stealth/space-bunny-alpha (0 / 0 USD, 1M ctx, tools; public model list 01:1xZ) via a pi-free harness row in DE's branch config
               (TMM.80) -- unproved: .env's OPENROUTER_API_KEY is EMPTY, only dispatch's minted per-spawn key reaches OpenRouter; if pi refuses
               the id, merging it into pi's openrouter provider is MINE (my first try broke auth for that provider: reverted)
the Prime      told: the swap, the correction (no box-wide redirect), PASS 3 could use the free model · still owes: the account, the two director
               rows, EF.10 · the router question answered by the owner (Bonsai + KV compression)
PASS 3         PAUSED by the owner 01:3xZ ("I paused the pass from prime", in DT's pane, on goal:g5) -- was the one-shot 01:37Z
trunk reds     test_dashboard's SIGINT watch only
```

## 🔴 Where it stops
01:3xZ 09-24 gen 14: the 0-credit lane is built; EF.90 holds the local slot; waiting on DT's first local parent+kids round and DE's free-model dispatch
```
state   MAIN clean (only cron-owned comms churn), nothing staged, no gate worktree open
NEXT    (1) DE's EF.90 lands (review in place by DE) -> its [merge-up] -> the #4-style gate (no mur: read DE's review + the diff yourself)
        (2) DT's first PI_CODING_AGENT_DIR round: does the server log show the parent's AND the kids' requests? -> the lane is proved or fixed
        (3) DE's pi-free proof dispatch: if pi refuses the id, merge {"id": "stealth/space-bunny-alpha", ...} into a COPY of pi's config first,
            test it with a minted key and stdin closed (< /dev/null), then swap it in -- never leave ~/.pi broken (backup in /data/ml/)
        (4) the account: re-read; funded = ONE lift line for paid rounds · PASS 3: a [red] from the Prime first
out     python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```

## Traps (post-specific, learned)
```
meter        the prompt hook prints [meter] on a REAL prompt (a nudge, a task notification) -- not on the startup injection; rotate at f 0.47
rotation     rotate.py rotate --post <director> is REFUSED ('equal rank (director = director)') -> order the director's own bare rotate ·
             rotate --model/--effort that differs from the row is REFUSED (exit 3): the row changes first · config:posts model / effort /
             role / tier / harness / owning_goal / worktree / rotated_by = prime/owner-only cells · a pin is verified = .agi/sessions/<post>.meter
             names the new session's jsonl AND that jsonl shows a [meter] line · the where-it-stops slot's FIRST LINE is plain text, never a fence
orders       dm ONLY: send.py --from thought-master send --to <post> '<text>' via a python argv list (no --body-file); the Prime channel is
             positional: send.py --from thought-master send belam '[tag] ...' · EVERY number in an order is checked against the bytes first ·
             NEVER type a real hostname / model name into a dm (comms are committed) · next = TMM.83
owner lines  in my pane = verbatim on goal:g5 (write.py goal:g5 'note ...' -> snapshot-goals.py --render, then --check); run date -u FIRST
             and stamp THAT clock (two wrong stamps this gen, fixed in place: body line N = file line N+27, 'replace body N:N --force <file>')
local lane   the local server = 127.0.0.1:8080 (NOT 18080) · pi-local mints no credential · a kid WITHOUT --harness resolves the ladder's
             tier-0 kid row = pi = OpenRouter (explicit --harness beats a ladder row) · dispatch iter ids look like TMD.01 · --dry-run writes
             nothing · a hand-run pi -p with stdin OPEN hangs (use < /dev/null) · .env's OPENROUTER_API_KEY is EMPTY (only the provisioning
             key is set; rounds get minted keys) · pi --list-models never lists OpenRouter's built-ins here (no proof either way)
pi config    ~/.pi/agent is the whole box's: test a change in a COPY via PI_CODING_AGENT_DIR first · a models-array override of a built-in
             provider needs a working key to test · the backup is /data/ml/pi-models.json.before-20260924T0109Z
merge-ups    the WHOLE history rides: list the tip's merges yourself · merge by the NAMED tip · LAND WITHOUT A STAGED MERGE: gate
             M = commit-tree(merge-tree(HEAD, tip)) in a detached /tmp worktree; at landing T2 = merge-tree(live HEAD, tip) -- if HEAD
             moved, diff(gated tree, T2) = exactly the newcomer files, byte-identical to HEAD on them; L = commit-tree T2 -p HEAD -p tip;
             git merge --ff-only L; push · the range = diff(merge-base, tip), never diff(HEAD, tip) · a red suite = return the tip
reds         attribute each: which range touches the test / its code (git diff --quiet <base> <tip> -- <file>) · re-run it ALONE (a load
             flake passes alone) · test_thought_hygiene counts <!--\s*THOUGHT:BEGIN per node: a quoted marker trips it
review       read each round's FINAL verify stage in .agi/sessions/workflows/runs/mur-*/verify_R-EFnn.json · no mur under the hold = read the
             director's in-place review AND the diff yourself, and say so
key cases    the authority's keyed / unkeyed rows: send._pushed_seats(root, send.authority_ref(root), True) · local seat keys = the NAMES of
             .agi/sessions/seats/*.key (+ .key.pending), never the bytes
suite        env -u TMUX -u TMUX_PANE, setsid nohup in a ( subshell & ) + a pid waiter (run_in_background) · create the worktree in ITS OWN
             call · ~13.5 min at load 2 · foreground sleep is blocked: wait with a background loop
account      python3 -c "import sys;sys.path.insert(0,'extensions/agi/bin');import provisioning as p;print(p.credit_balance('.'))" = (total, used, left); prints no key
anonymize    anonymize.py guards hostname / ip / mac / board / secret (loopback exempt); the model name needs its own grep: git grep -i -E 'geforce|rtx ?20[0-9]0' <tip> -- .agi/nodes
write.py     a list field = 'set <field> <JSON array>' via a python argv list (no ' && ' inside; --dry-run shows the ring-gate preview) · a goal note -> snapshot-goals.py --render, then --check
box          box.* / locations.* are stale here (repo /data/work/agi) · never cd into a director's worktree (the harness then treats it as mine) -- read it by absolute path
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card · grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · a director's [merge-up] lands in the inbox file, not the dm log · 'pane busy' = the dm is in the log, the sweep retries
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime) · KV slot save / restore on the local brain (--slot-save-path = a server restart at a leaf boundary).
