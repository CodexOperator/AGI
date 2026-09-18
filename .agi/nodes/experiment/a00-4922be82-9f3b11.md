---
id: experiment:a00-4922be82-9f3b11
mint_id: 01387d41a6e4492ba7a5842589a6aef2
type: experiment
parents:
  - hypothesis:l4-the-real-box-half-of-remote-now-agi-cloned-on-the-town-box-with-its-own-sessions-env-crons-and-keys-and-a-core-town-dm-read-there-in-one-tick
next_edges: []
confidence: 0.7
edited_by: a00-4922be82
evidence_runs:
  - experiment:a00-4922be82-9f3b11
line_ceiling: 40
loop: hypothesis:l4-the-real-box-half-of-remote-now-agi-cloned-on-the-town-box-with-its-own-sessions-env-crons-and-keys-and-a-core-town-dm-read-there-in-one-tick@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: f96cbb669488e47f
season: 2
title: "SM.117b real box: clone + box-local env/sessions/crons proved, but the fetch+read tick delivers nothing -- the inbox it reads is untracked"
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-4922be82-9f3b11 — the real box: clone, box-local env/sessions/crons, and what a git fetch actually delivers

## Experiment

Ran the SM.117b real-box slice on the town box, over its ssh alias only
(`ssh -F <mesh config> local-town` — alias in this node, never an address,
host name, hardware or location string). Every command ran ON the box; this
repo's graph was not touched except this node. Driver script and raw transcript:
`.agi/sessions/iter-124/a00-4922be82/{box_setup.sh,box_setup.out}`.

### 1. Checkout carries SM.117 (claim 1)

```
git clone --branch local-maxxing/season1/main <origin> agi   # 11 s
git fetch origin core/season2/main                            # fast
git merge --no-edit origin/core/season2/main                  # clean, 0 conflicts
```

Box head before the box-local commit: `d0bf66822` (merge). `boxes.py` PRESENT;
`mail_poll` 4 hits in `crons.py`. HEAD is on the thought town trunk
`local-maxxing/season1/main` with the core trunk merged in.

### 2. Box-local .env (claim 1)

`.env` written at the MAIN root, mode 600: `AGI_BOX=local-town`,
`OPENROUTER_API_KEY=` and `OPENROUTER_PROVISIONING_KEY=` both empty.
`envfile.py --check` on the box:

```
[secrets] PROBLEM: OPENROUTER_API_KEY is missing or empty in .env
[secrets] note: MINIMAX_API_KEY is not set (optional)
[secrets] note: OPENAI_API_KEY is not set (optional)
[secrets] note: OPENROUTER_PROVISIONING_KEY is not set (optional)
[secrets] note: CAMBER_CLOUD_API_KEY is not set (optional)
check_rc=1
```

Honest reading of claim 1's wording: `--check` does NOT name only the
provisioning slot — the **required** runtime key is also empty and is the one
PROBLEM. Both keys are the owner's to mint (spend isolation); the
provisioning slot's emptiness is reported as an optional note, exactly as
`envfile.py` documents. Nothing else fails.

### 3. Box-local state and crons (claims 1, 2)

- `.agi/sessions/` is box-local by construction (untracked; 352 tracked files
  live under it, none of them state).
- `tmux new-session -d -s agi-rc` -> `agi-rc: 1 windows`.
- The merged trunk declares **no box anywhere**: `.geometry/posts.md` has no
  `default_box` cell and **no row carries a `box` cell**, and `.geometry/crons.md`
  has **no `mail_poll` job and no `box` keys**. So SM.117's graph half never
  landed on core/season2/main — only its code (`boxes.py`, the `crons.py` box
  filter, `send.py --box-local`) did.
- Box-local graph edits (committed on the box's own branch `303034a37`, never
  pushed): `thought-master` + `director-thought` rows gain
  `"box": "local-town"`; cadences gain `grid_sync  box: core-town`,
  `branch_push  box: [core-town, local-town]`, and a new job
  `mail_poll {every_mins: 5, enabled: true, box: local-town}`.
- `crons.py show` BEFORE those edits rendered **7 lines** (the full core
  crontab: grid_sync + 5 mirror pushes + branch_push). AFTER: exactly **2** —
  `branch_push` and the `mail_poll` fetch+read line. `crons.py apply` installed
  those 2. Box crontab total = 4 lines (2 comment markers + 2 jobs).
- Core-town's crontab was never edited or applied; its `agi-crons` block still
  names project `/home/ubuntu/work/agi` and its own 7 rendered lines. Claim 2
  holds, but note it holds *because the trunk is still single-box*: with no
  core box declared, the box needed a box-local declaration to be gated at all.

### 4. The delivery proof (claim 4) — DISPROVED on the built bytes

Box-local commit `303034a37`. `crons.py apply` -> at 22:10Z the first tick
produced **no log at all**: `~/logs/` does not exist on a fresh box, and every
rendered line redirects to `~/logs/agi-crons-agi-<hash>.log`, so the whole
line (including the `read`) dies at the shell redirect with nothing written
anywhere. `mkdir -p ~/logs`, then the 22:15Z tick ran and logged:

```
mail_poll: skipped foreign-box post belam (box (default))
... 19 rows skipped by name ...
inbox for thought-master: empty
inbox for director-thought: empty
```

So the poll runs, box-gates correctly, and delivers **nothing**. Cause, read
from the bytes: `send.py send()` writes only `_inbox_path()` =
`<sessions>/inbox/<recipient>.md`, which is **untracked** (`.agi/sessions/` is
in `.gitignore`), and `send.py read --box-local` reads that same untracked
store. A fresh box has no inbox, so `git fetch` cannot deliver mail into it.
The dm bytes DID travel: the tracked transcript
`comms/season-2/dm/director-thought--thought-master.md` is present on the box,
and on the box

```
send.py read --dm director-thought --me thought-master --all   # rc=0
**director-thought** 10:17 — TM.05 ... audited + merged ...
```

renders core-town-authored messages. The reader exists for the tracked record;
`read --box-local` is pointed at the other store. Claim 4 as written
(`read thought-master --box-local` inside one tick) is therefore false on these
bytes: measured tick latency was 2–3 s once the log dir existed, but the tick's
content is empty.

### 5. Post keys (claim 3) — the choice, with its reason

Chosen: **re-mint at the box's next rotation**, keys not copied. Reason: a
private seat seed never leaves the box that minted it (transport over the
overlay would be a second copy of a live identity on a research-grade box);
reading does not need the private key — verification uses the pubkey already on
the row's `key_history` — so leaving the slot empty costs the read path
nothing, and the box's first rotation mints its own key and its `key_history`
row merges up (seed Addendum 4 step 7). NOT executed this round: no rotation
ran on the box, so this is a recorded decision, not a measured copy.

## Evidence

- Box: `local-maxxing/season1/main` @ merge `d0bf66822` + box-local `303034a37`.
- Box crontab block hash id `3fbc6951b5c1`, 2 job lines; core block id
  `2f118e6f32fd`, 7 job lines, untouched.
- Two real cron ticks: 22:10Z no log (missing `~/logs`), 22:15Z logged 19
  foreign skips + `inbox for thought-master: empty`.
- `send.py read --dm ... --me thought-master --all` rc=0 with real core-authored
  bodies.
- Raw transcript: `.agi/sessions/iter-124/a00-4922be82/box_setup.out` (129 lines).

## Findings (each a node-sized item, none built here — engine work is outside this round's file scope)

1. **The delivery seam is two stores.** `send()` writes the untracked
   `<sessions>/inbox/`; the git-carried record is `comms/season-*/dm/<a>--<b>.md`.
   A cron that only fetches + `read --box-local` therefore delivers nothing on a
   fresh box, and the SM.117 hermetic test (claim 5) could pass only because its
   fixture wrote the inbox directly rather than through git.
2. **`crons.py apply` does not create the log directory it redirects into.**
   A fresh box's first tick is silent — the exact failure class this repo
   removes elsewhere (`CronsError` is "never swallowed", but the redirect is
   below `crons.py`).
3. **SM.117's graph cells never landed on the trunk** (`default_box`, the three
   `box` cadence keys, the `mail_poll` job). Without them the box renders the
   full core crontab; the box-local edits above are what made claim 2
   observable.

## [decision] line for the Prime (09-19 check-in) — exact edits, no live row touched

```
[decision] SM.117b real-box: (a) .geometry/posts.md: add top-level `default_box: core-town`;
(b) thought-master + director-thought rows gain `"box": "local-town"` (core-town keeps them
`settings: quiet`); (c) .geometry/crons.md cadences: `grid_sync` + `box: core-town`,
`branch_push` + `box: [core-town, local-town]`, new `mail_poll {every_mins: 5, enabled: true,
box: local-town}`; (d) `crons.py apply` must create the log dir before rendering lines into
it; (e) delivery: mail_poll must consume the TRACKED comms dm transcript
(`send.py read --dm <peer> --me <post>`) or `read --box-local` must be re-pointed at it —
the untracked sessions/inbox cannot be the cross-box store.
```

## Verdict rationale

Claim 1 proved (clone/branch/env/sessions/tmux, with the `.env` check's wording
corrected); claim 2 proved on the box and core-town's crontab untouched; claim 3
is a recorded choice, unexecuted; claim 4 — the hypothesis's actual proof — is
falsified on the built bytes by two live ticks. Lean disproved, not proved.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
First version of this node. It differs from the scaffold by replacing the
placeholder body with the measured transcript of the real-box round: the clone
and box-local setup (proved), the box-scoped crons (proved, 7 -> 2 lines), and
the measured failure of the tick's delivery (the inbox is untracked, so a fetch
cannot fill it). The deviation to record: the brief's file scope allowed a
`.geometry/crons.md` line in THIS repo, but the trunk's graph has no box cells
at all, so the cadence and row edits were made on the BOX's own branch only
(`303034a37`) and delivered as one [decision] line, keeping core-town's graph
and crontab byte-untouched as claim 5 requires. The second deviation: claim 3
was resolved as re-mint rather than a key copy, with the reason on the node.
<!-- THOUGHT:END -->

## Agent Notes
Real box over its ssh alias only: clone (11s) + local-maxxing/season1/main merge of core/season2/main (clean), box-local .env (AGI_BOX=local-town; envfile --check names the empty required OPENROUTER_API_KEY, provisioning slot an optional note), own sessions, tmux agi-rc, box-local crons.md+posts.md on branch 303034a37 -> crons.py show 7 lines -> exactly 2 (branch_push + mail_poll), apply installed those; core-town's crontab untouched. Claim 4 FALSIFIED on the built bytes: two live ticks (22:10Z no log at all -- ~/logs does not exist and every rendered line redirects into it; 22:15Z logged 19 foreign skips + 'inbox for thought-master: empty') because send() writes and read --box-local reads the UNTRACKED sessions/inbox, while the git-carried dm record (comms/season-2/dm/*.md) is a different store that reads fine via read --dm --me. Keys: re-mint chosen, not copied (reason on node). [decision] line for the Prime is on the node; no live row cell touched.
