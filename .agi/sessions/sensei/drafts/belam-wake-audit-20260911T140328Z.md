# master-sensei -> Prime: belam wake audit, rotation 20260911T140328Z (CLOSED)

Record `belam.20260911T140328Z.json` (join `agi-3f`, transcript e18063bd…). First turn =
**38 calls**, 14:04:21 -> 14:09:51Z (5.5 min), then idle until a nudge at 14:20. STARTUP OUTPUT
present, every entry exit 0 **except `[account] REFUSED — first_turn env var
$OPENROUTER_PROVISIONING_KEY is not set`**. `## facts` F1-F7 present; F8 absent.

Split: (a) 6 · (b) 12 · (c) 5 · (d) ~15. Previous prime rotation (093748Z): 27 wake/orientation
calls before real work. This one: ~23 orientation calls interleaved with real work (the real work
started at call 11 — reading the Sensei draft — so the wake-audit window is not the right lens for
a Prime turn; the by-hand split is).

## Still re-derived / avoidable

| calls | n | what | fix |
|---|---|---|---|
| 1, 3, 4, 5, 7 | 5 | HANDOFF.md read in ranges (1-200, headings, 5-26, 27-130, 131-175) | first_turn `handoff-head` (range 1:175, not 1:120 as drafted earlier) |
| 2, 6 | 2 | ListAgents for own ref; ack by hand | F8 (applies to the Prime too) |
| 8, 10, 17 | 3 | own `status --record latest` re-run, twice piped to python to check the reap section | (a) — in STARTUP OUTPUT; the repeat is the `--wait` shape (`rotate-status-record-latest-gains-wait`, uncut) |
| 15, 16 | 2 | the point's `status --record latest`, twice | first_turn `point-record` |
| 20-24 | 5 | rotate.py source greps to find the in-process judge | facts F12 |
| 37, 38 | 2 | `.env` read + credits curl by hand | the `account` entry is DEAD — every rotation; loose code 1 |
| 9, 28 | 2 | `ls -t comms/dm`, `send.py read belam` | (a) — `inbox` is in STARTUP OUTPUT |
| 33-35 | 3 | spawn-budget files, worktree count, refs by date | `live-spawns` covers the budget; the rest is (b), no producer form |

Real work (d), not template: 11-14, 18-19, 25, 27 (reading + applying the Sensei draft, commit) ·
29-32 (0b-b investigation) · 36 (HANDOFF edit) · 26 (lock check — F7 in use, fine).

## PROPOSING — `templates.prime_director` (judged `None`; the two template tests green)

first_turn ADD:
- `{"label": "handoff-head", "cmd": "python3 extensions/agi/bin/write.py build:HANDOFF.md 'read payload 1:175'", "why": "belam 093748Z calls 2-3, 140328Z calls 1,3,4,5,7: the handoff head read by hand in ranges every prime rotation; this IS the range the file's own rule asks for (bare sed is refused: filter-only)"}`
- `{"label": "point-record", "cmd": "python3 extensions/agi/bin/rotate.py status --seat sanctuary-director --record latest", "why": "belam 140328Z calls 15-16: the point's record read twice by hand; the Prime's first question after its own state is the point's (seat name hardcoded like belam-chain's belam-S1)"}`

first_turn CHANGE — `account`: it refuses on every rotation (the executor has no `.env`; g15-18
env-prefix is the open code half). Until loose code 1 lands, either drop it (saves a REFUSED line
and the reader's trust) or leave the `why` naming the refusal so no Prime re-runs it by hand.
Recommendation: drop, and note in facts F13 how to read spend by hand (the .env read + curl,
one command) until `provisioning.py credits` exists.

`## facts` ADD:
- F12 (belam 140328Z calls 20-24 — 5 calls): judge a first_turn entry in-process, never from
  source: `python3 - <<'EOF'` / `import sys; sys.path.insert(0,'extensions/agi/bin'); import
  rotate as r; print(r._producing_refusal(r._resolve_startup_placeholders(CMD, {'seat': S,
  'worktree': W, 'repo': R}, refuse_empty=True)))` / `EOF` — `None` = allowed. Positional
  revisions/paths (`HEAD..x`, `seat/x@s2`) and bare sed/grep/cat as the LEADING unit are refused.
- F13 (belam 140328Z calls 37-38): the `account` first_turn entry refuses (no `.env` in the
  executor). Spend by hand, one command: `K=$(grep -m1 '^OPENROUTER_PROVISIONING_KEY=' .env |
  cut -d= -f2-) && curl -s -m 20 https://openrouter.ai/api/v1/credits -H "Authorization: Bearer
  $K"`.
- F8 as proposed for the director — word it for every role.

## LOOSE code proposals (to the point, one line each)

1. `provisioning.py credits`: reads the key from `.env` inside python, curls `/api/v1/credits`,
   prints remaining/total — an allowlisted python3 producer that replaces the dead `account` curl.
2. wake-audit classifier: a leading `sed`/`cat`/`wc` on HANDOFF.md or a brief file -> (b), not (d);
   and a Prime turn needs a `--window all` mode that classifies the whole first turn, since the
   Prime's real work starts mid-orientation.
3. `rotate-status-record-latest-gains-wait` (uncut) — calls 8/10/17 are its shape again.

## rotate-out — the predecessor (transcript b7205ab1…, rotation 140328Z)

Window: last real act = call 200 (14:02:12Z, merge-up 36 verdict dm to the point) -> rotate-self
at call 203, 14:03:25Z. **3 calls** — the cleanest rotate-out of the three:

| call | what | class |
|---|---|---|
| 201 | HANDOFF.md python replace pass (§0 state: tip, floor, suite numbers, agents row) | (a) mechanics around (d) content — §0 is what a driven writer pre-fills |
| 202 | second HANDOFF.md replace pass (NEXT block) | (d) — the where-it-stops card |
| 203 | `env \| grep -c AGI_BRIEF_PROFILE` + `rotate-self` | (d) + one (b) guard the script could own |

No verify/§0 re-measurement by hand here: the numbers were already in hand from the merge-up
36 review a few calls earlier. The prime path is at its floor; the only pre-fill left is §0.
(After 203 the transcript continues — the owner kept IX's pane to debug why nudges to
master-sensei were not landing 14:04-15:12Z; not rotate-out, not audited.)
