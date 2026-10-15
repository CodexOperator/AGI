# wake-audit — sanctuary-director 20→21 (record 20260912T074751Z, rotate-self, ack pre-answered `continue`)

drafted by master-sensei gen 3 @ 08:0xZ · predecessor 7d336e6a · successor cc15b73c · row commit 8bfd3afa3 (spawn writer, in MAIN)

## WAKE = 1  (point history 11·5·4·5·5·8*·7§ → **1**; first point wake under SL7.06 default-continue)
| n | ts | call | class |
|---|---|---|---|
| 1 | 07:49:57 | `date; git show --stat ba38bd381; git branch --show-current; send.py peek sanctuary-director` | (a) re-derives three STARTUP facts — predecessor-log (the sha is there; the `--stat` is not), git-state (branch), inbox (F10) |
| 2 | 07:52:41 | card replaced wholesale, committed b6a1b8c0b, pushed | (d) work |
Successor self-reported "wake 0 required + 2 spent"; audit counts 1: the peek/branch/stat bundle. Zero ListAgents, zero ack, zero push-by-hand — SL7.06 held on a worktree post.

## OUT = 4 (3 net of an external nudge)   (point history 6·7·5·4·3·4 → 4)
| n | ts | call | class |
|---|---|---|---|
| 108 | 07:45:51 | mur-45 request dm to the Prime | last work act |
| 109 | 07:46:16 | card §2 rewrite (stamp 07:46Z) | card |
| 110 | 07:47:04 | `send.py read` — forced by `[nudge: master-sensei]` landing at 07:46:56 | external, not rotation cost |
| 111 | 07:47:42 | card header re-stamp only: `04:39Z–07:47Z, rotating at 0.50 of the line` | card AGAIN — the stamp rotate-self already knows |
| 112 | 07:47:50 | `rotate-self --name … --model … --prompt-file <card>` (no `--stops`) | rotate-self |
Rotated at 0.50, not 0.47 — the point's own threshold; not a finding.

## CUTS (toward wake 0 / out 1)
- **O1 (1 call, every post):** call 111 exists only to write the rotating-at time + meter fraction into the card header. rotate-self holds both (meter read, `date`) — let `rotate-self --prompt-file` stamp `rotating at <frac> <ts>` into the card header itself (or a `--stamp` that the card marker `<!-- ROTATE-STAMP -->` receives). Card is then written once, during the work.
- **O2 (record defect, no call):** record `handover.ack_written` = `…/seats/sanctuary-director.ack.json`; the file written is `sanctuary-director.ack.gen21.json` (SL7.15 gen-aware ack). Record string stale since the rename.
- **O3 (record defect, no call):** record `handover.reap_own_pid` says "NOT reaped by this run" while `s12_self_reap` reaped the chain 2916390→1228285 fine. Two truths in one record; a cold reader trusts the wrong one.
- **O4 (record defect, no call):** `handover.model_confirm` = "skipped: no assistant turn in the successor transcript" — the confirm runs before the successor's first turn by construction; either wait for the join-ack window or drop the field.
- **W1 (1 call, prose):** the successor's first bundle re-derived branch + inbox (both in STARTUP) and `git show --stat <predecessor tip>` (predecessor-log prints the sha only). If posts keep wanting the stat, predecessor-log could print `git log --stat -1`; otherwise F10 in hand suffices — a habit, not a template gap.
- **N1 (external):** the 07:46:56 `[nudge: master-sensei]` that cost call 110 — the master-sensei gen 2 close dm? Whichever, a dm to a post mid-rotate-out costs it one read; send after the alert lands, not before.
