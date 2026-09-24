# thought-master — CARD (state only) · role = `doc:unified-master-brief` (TEMPLATE) + `doc:unified-head` (HEAD) · formation = `doc:formation-local-town` (.agi/nodes/.geometry/formations/) · town todo = `town:local-maxxing` trajectory_standin · owner lines = where the HEAD's notes line says (never a goal)

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

## Live state (03:1xZ 09-24, gen 15)
```
NORMAL OPS     OPEN since 03:17Z -- OWNER 02:3xZ (verbatim on goal:g5): "Let's resume normal operations using the free Openrouter endpoint. No
               more special usd0 runs just research towards doing more efficient usd0 runs in the future" -> the standard town line on --harness
               pi-free (stealth/space-bunny-alpha, 0 USD; the row is on the trunk f83d731911) · GO 03:1xZ: TMM.91 (DE: the 3 murs EF.87-89, EF.91,
               .23 r2 / .14 r3, the per-harness max_live leaf) · TMM.92 (DT: LEAF.04 -> REPLAY.01 -> SWR-SV.01 as a director review)
ACCOUNT        the allowlist + ZDR are dashboard-only (no API route: trap 'allowlist'; the owner's 02:54Z "admin key" line measured 03:01Z) --
               the owner made both edits (allowed providers 03:13Z, account-wide ZDR off 03:17Z; verbatim on goal:g5) -> raw re-probe 03:17Z =
               200, cost 0 · ZDR OFF = the free provider retains prompts (the owner's trade-off; the per-vendor ZDR re-imposition offer got no
               answer -> not applied) · 14.04 of 192 USD left (the Prime's 02:13Z move)
kids           a pi-free parent's kids pass --harness pi-free until EF.90's harness inheritance reaches the trunk (the ladder's kid row = paid)
HOLD (TMM.66)  every PAID model (deepseek, glm, opus) still held
usd0           the local lane is RETIRED as an operating mode (the owner cancelled the local kid 02:2xZ: DE SIGTERMed DT's LEAF.03 parent
               a00-bbb13581); efficient 0-USD runs = RESEARCH hypotheses on the free lane · the brain container brain-orcabonsai27b (OrcaBonsai
               C2 on :8080) stays up for that research; the old router llama-server is STOPPED (docker start llama-server restores it) ·
               /data/ml/pi-agent-local exists (unused now) · ~/.pi/agent == its 01:09Z backup
EF.90          DE's pi-local kid a00-0d0977d3 (AGI_HARNESS inheritance) OVERFLOWED its slot (66,720 of 65,536, DT's bytes) -- DE reports
DT research    02:41Z (28ed92197b): hypothesis:lm-pi-agents-load-claude-md-twice (CLAUDE.md loaded twice = 13,916 tokens = 55 pct of a first
               prompt on EVERY pi agent; lever pi --no-context-files = DE's lane once measured) · hypothesis:lm-pi-compacts-before-the-slot-
               ceiling-once-the-window-is-declared · LEAF.04 on pi-free GO (TMM.92) · SWR-SV.01 closes as a director review
LANDED         DE d81b44404 (merge-up #4 = EF.83-86) + the 09-23 landings
the Prime      PASS 3 may resume on pi-free at its next CHECK ([owner] line 03:1xZ) · still owes: the two director rows, EF.10
trunk reds     test_dashboard's SIGINT watch only
```

## 🔴 Where it stops
03:1xZ 09-24 gen 15: pi-free OPEN (the owner's two dashboard edits; raw re-probe 200 at 03:17Z); GO sent to both directors (TMM.91 / TMM.92); watching the first pi-free rounds
````
03:1xZ 09-24 gen 15: pi-free OPEN (the owner's two dashboard edits; raw re-probe 200 at 03:17Z); GO sent to both directors (TMM.91 / TMM.92); watching the first pi-free rounds
```
state   MAIN: goal:g5 + GOALS.md + this card committed and pushed; only cron-owned comms churn left; no gate worktree open
NEXT    (0) the first pi-free rounds: a kid record showing harness pi (= deepseek, PAID) under a pi-free parent = cut it; a 404 / 429 from
            the free provider = the director's one line, hold that lane, re-probe raw (trap 'allowlist') before any dashboard ask
        (1) DE's [merge-up]s (the 3 murs' batch; EF.90's result) -> the #4-style gate: each round's FINAL verify stage + the diff, read myself
        (2) DT's [merge-up] (LEAF.04, REPLAY.01) -> the same gate · SWR-SV.01 closes as DT's director review
        (3) paid models: lift only on the owner's word · PASS 3 (pi-free, the Prime's next CHECK): a [red] from the Prime first
out     python3 extensions/agi/bin/rotate.py rotate (bare, from MAIN; card write LAST; not mine: sequence.json, comms churn)
```
````

## Traps (post-specific, learned)
```
meter        the prompt hook prints [meter] on a REAL prompt (a nudge, a task notification) -- not on the startup injection; rotate at f 0.47
rotation     rotate.py rotate --post <director> is REFUSED ('equal rank (director = director)') -> order the director's own bare rotate ·
             rotate --model/--effort that differs from the row is REFUSED (exit 3): the row changes first · config:posts model / effort /
             role / tier / harness / owning_goal / worktree / rotated_by = prime/owner-only cells · a pin is verified = .agi/sessions/<post>.meter
             names the new session's jsonl AND that jsonl shows a [meter] line · the where-it-stops slot's FIRST LINE is plain text, never a fence
orders       dm ONLY: send.py --from thought-master send --to <post> '<text>' via a python argv list (no --body-file); the Prime channel is
             positional: send.py --from thought-master send belam '[tag] ...' · EVERY number in an order is checked against the bytes first ·
             NEVER type a real hostname / model name into a dm (comms are committed) · next = TMM.91
owner lines  in my pane = verbatim where the HEAD's notes line says: a template or config, then the role doc, then town:local-maxxing --
             NEVER a goal (goals are project trackers, owner 09-24) · the stamp = the jsonl's own timestamp for the owner's message
             (.agi/sessions/thought-master.meter names the jsonl), never a guess · a one-line replace inside a fence = 'replace body N:N --force <file>'
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
allowlist    the account-wide allowed providers (dashboard Settings > Privacy) have NO API route -- the management key cannot set them
             (openapi.json 94 paths; 03:01Z 09-24); guardrails + a request's provider.only only NARROW them · a 0-USD raw probe =
             provisioning.mint(limit_usd=0.01, ttl_minutes=10, workspace_id=workspace(cfg)) -> one chat call -> revoke(key_hash) in a finally
anonymize    anonymize.py guards hostname / ip / mac / board / secret (loopback exempt); the model name needs its own grep: git grep -i -E 'geforce|rtx ?20[0-9]0' <tip> -- .agi/nodes
write.py     a list field = 'set <field> <JSON array>' via a python argv list (no ' && ' inside; --dry-run shows the ring-gate preview) · a goal note -> snapshot-goals.py --render, then --check
box          box.* / locations.* are stale here (repo /data/work/agi) · never cd into a director's worktree (the harness then treats it as mine) -- read it by absolute path
handoff      .agi/sessions/seats/thought-master.handoff.md is rotate's header, NEVER a link to this card · grid.py commit --all is the cron's, never mine
comms        a nudge may be a phantom -> verify in git · a director's [merge-up] lands in the inbox file, not the dm log · 'pane busy' = the dm is in the log, the sweep retries
```

## BANKED (owner-only)
Bonsai ternary recipe on Qwen3-8B · oscillator readout on C2C-fused KV · llama.cpp block-diffusion drafter · per-channel-K 2-bit KV in ggml-cpu · rpc-split only if the owner names a model that does not fit · kid-persona QLoRA after trajectory capture · coupled-oscillator / SNN C2C fuser vs a frozen trunk · should the mirror menu BE the spawn gate · TypeSafe plugin + .env rename · Neon key · Doppler ownership · per-kid endpoint keys (g5.20) · Opus on the pi allowlist for brainstorms · claude-code kids on local-town (config-valid, unauthorised) · the older OpenRouter account (~14 USD): fold or reserve? · the ONE justified Camber burst (cross-arch attribution A/B, ~20 min) · vision:local-maxxing refresh from the 21:4xZ trajectory (owner/prime write only) · provider-key rotation after the 22:19Z env dump (dashboard-minted keys = owner/Prime) · KV slot save / restore on the local brain (--slot-save-path = a server restart at a leaf boundary).
