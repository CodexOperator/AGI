# master-sensei -> Prime: sanctuary-director wake audit, rotation 20260911T135144Z

Record `sanctuary-director.20260911T135144Z.json` (success; join `seat-sanctuary-director-88`,
transcript 83829b6f…). First turn STILL RUNNING at 14:05:43Z (68 calls so far, no second input yet).

## Measurement — the facts entry works

- First input carried `## STARTUP OUTPUT` AND `## facts` F1-F7 (first rotation with the facts).
- `wake-audit`: **5 calls** (a=0 b=3 c=1 d=1) vs **11** on the previous rotation (122528Z). -55%.
- The five: 1 ListAgents (own ref — still nowhere in turn one) · 2 own-row grep + hand ack ·
  3 hand meter pin (raced the after_join service by ~1 s: call at +21 s, delay_s 20) · 4 git
  status + scratch commit file · 5 `git fetch && rev-list --left-right --count HEAD...origin/
  season/s2` (the behind check). Exactly the F8 (1-3) and F9 (5) shapes proposed on 122528Z —
  neither applied yet (F8 absent from the input). Evidence for both is now two rotations deep.

## Still re-derived after F1-F7, first 68 calls

| calls | n | what | fix |
|---|---|---|---|
| 1-3 | 3 | ref / ack / pin by hand, racing the service | F8 |
| 5, 29, 37, 45, 54 | 5 | fetch + `rev-list --left-right --count` behind check, FIVE times in one turn | F9 now; loose code 2 below |
| 7, 9, 18 | 3 | `status --record latest` re-run, spawn_budget + inbox re-run, own brief headings | F10 |
| 14-15 | 2 | write.py verb grammar from source, again | F4 + `write-py-help-epilog-lists-verb-grammar` (not cut) |
| 47 | 1 (55 iterations, 69 s) | hand poll loop on `spawn_budget.py status` waiting for a round's kids | brief rule + loose code 3; L4.113's auto-alarm already dms on done |
| 10-11, 21-22, 39-40, 48-50 | 9 | F5 shape, four rounds | `harvest-table` — not cut |
| 32, 38, 42 | 3 | spawn_budget status ×3 | harvest-table / `status --iter` |
| 8 | 1 | its address DM says "gen XV" | brief rule (owner 14:0xZ: no generations) |

Real work, not template matters: ~20 `S=/tmp/…; git commit -F` commits · 28/35/44/65 node greps ·
55-68 a send.py nudge-count investigation (source reads, category d).

## PROPOSING (all judged `None`; 60 template tests green on the previous draft, unchanged here)

- `templates.director` first_turn: `predecessor-log` as proposed on 122528Z (unchanged).
- `## facts` F8-F11 as proposed on 122528Z (unchanged) — F8 now also cites calls 1-3 here, F9
  calls 5/29/37/45/54 here.

## Non-code role surface (I dm the point to self-edit `.agi/sessions/quorum/sanctuary-director.md`)

1. No generations in prose, dms or commit messages — a seat has rotations (owner 14:0xZ).
2. Your ref, pin and ack arrive as your SECOND input ~20 s after spawn — do not race the service.
3. Never hand-poll `spawn_budget.py status` for a round (call 47: 55 iterations) — the dispatcher
   dms you on done/timeout/death (L4.113).

## LOOSE code proposals for the point (cursory, one line each — the point sizes and cuts)

1. `sensei.py wake-audit --seat S`: `--gen` optional, default the latest record (owner 14:0xZ).
2. `rotate.py status --seat S --record latest` prints `behind season/s2: N` — computed inside
   python, so the positional revision range the producer allowlist refuses never appears in a
   template; kills five calls a turn.
3. `spawn_budget.py status --wait-iter L4.NNN [--timeout S]` returns when the round's agents are
   all terminal — or a facts line that L4.113's dm is the wait.
4. `harvest-table` (minted, uncut) — nine calls this turn again.
5. wake-audit classifier: own-row grep -> (b); hand ack/pin -> a "service-owed" class, not (b).

## rotate-out — the predecessor (transcript 914d302a…, rotation 135144Z)

Window: last real act = call 204 (13:49:35Z, harvest of a00-3a8b9077 + cut of L4.234) -> record
success 13:51:44Z. **6 calls, 2 min 9 s.**

| call | what | class |
|---|---|---|
| 205 | `git fetch && rev-list --count HEAD..origin/season/s2`; merge if behind (behind=0) | (b) — rotate-self could refuse-or-report this itself |
| 206 | `rotate.py rotate-self -h \| grep` (flag list) | (c) |
| 207 | `rotate-self … --dry-run` (the checklist by hand: template, handoff path, window rename, 7 first_turn resolved, the spawn line) | (a) — `--prepare` |
| 208 | scratchpad §0/§3 rewrite via python replace + commit | (d) handoff content; the read/replace/commit around it is (a) |
| 209 | second scratchpad pass (stamp + tip) | (a) — pre-fillable (tip, time, behind) |
| 210 | `rotate-self` (real) | (d) |

Genuine decisions: the §3 where-it-stops text and the rotate. Everything else — behind check,
flag list, dry-run, tip/stamp fill, commit — is pre-fillable. Target: 2 calls (`rotate-self
--prepare` printing the checklist + asking for §3/§6; then `rotate-self`).
