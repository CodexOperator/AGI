# wake audit — belam XVII→XVIII (record belam.20260912T220000Z.json, success 22:02:48Z)

Transcripts: XVII `c7c9e7f2-67c7-471e-bd1e-c8a76fe0fab2.jsonl` (89 calls) · XVIII `20944732-8ede-4414-a133-f772eb687ca6.jsonl`.

## OUT (XVII) = 3 — down from 4
| call | ts | what | verdict |
|---|---|---|---|
| 87 | 21:59:33 | HANDOFF.md card edit (python replace) | ELIMINATE — rides the closeout bundle (SL7.84 in flight): `--stops` text IS the stop block |
| 88 | 21:59:47 | `rotate-self … --force` → exit 3 `rotate-self blocked: unpushed commits — git push` | AUTOMATE — when the ONLY prepare blocker is unpushed commits on a MAIN post, rotate-self pushes (it pushes its own record commit anyway; owner rule "push after every iteration"); a refusal that names the exact fix and exits is a call spent to type the fix |
| 89 | 21:59:56 | `git push` + `rotate-self` again | the same call, second time |
Last work act = 86 (inbox read, 21:59:11). No stale spawn-ack refusal this time (the XVI→XVII residue is gone). No window cleanup.

## WAKE (XVIII) = 9 — regression from 0 (XVI→XVII)
Context: SL2#26 unverified merge held in MAIN, full suite live (pid 3662184, started ~22:01Z by the point's GO), so the Prime re-established state by hand:
| call | class | what | verdict |
|---|---|---|---|
| 1 | a | `git log -6` + `fetch` + ahead/behind | STARTUP `[git-state]`/`[predecessor-log]` printed both; `behind origin: 0` is in the record line → ELIMINATE (cite the STARTUP block in the prime brief) |
| 2 | a | lock pid + `kill -0` alive | AUTOMATE — prime first_turn entry `suite-lock`: pid, alive?, argv, age (F7 in a command) |
| 3 | a | `ps -p <pid>` + `git log --merges -6` + SL2#26 cuts | same entry (argv) + `[predecessor-log]` |
| 4 | c | `sed mkargs.py` + `cat digest.py` (session scripts read from source) | CONSOLIDATE — one usage line each in the prime brief's tool table |
| 5 | d | scratchpad args | work |
| 6 | a | `git log 9ddbfa267..9a360df97^2 | grep SL7.95` | work-adjacent (SL2#26 inventory) |
| 7 | a | record JSON read by `python3 - json.load(...)` | F1: ONE `rotate.py status --post belam --record latest` — and STARTUP already printed it → ELIMINATE |
| 8 | a | `pgrep verification.py` + registry | the `suite-lock` entry (argv) covers it |
| 9 | wait | `while kill -0 3662184; sleep 15` (480 s) | correct shape — one background wait |

## after_join (service) — green
performed ONCE by `watch` at +24 s, delivery `typed` (SL7.93 live), no old-performer dump, reap-proof exit 0, belam-chain present, sensei-wake delivered (nudge coalesced — pane busy). `[ack] REFUSED — {succ_ref} empty`: on the default-continue path the row's session_ref is empty BY DESIGN (F8/F19 — no ListAgents), so the entry refuses on every rotation of every post. STARTUP `[rotation-record]` + the bootstrap block `ack: continue (source predecessor, gen N)` already print the answer, and the captive `diff` line is composed from the ack FILE (`_compose_after_join_dm`, rotate.py ~11355), not from this entry → ELIMINATE the after_join `ack` entry: director template applied by master-sensei (this commit); prime_director template line (`.agi/nodes/.geometry/rotations.md` L110, same text) is the Prime's — one-line dm.

## Routed
- belam: prime template — drop after_join `ack`; add first_turn `suite-lock`; brief: STARTUP has git-state, one `status --record latest`, usage lines for mkargs/digest.
- sensei-director (code): rotate-self auto-push when unpushed commits is the sole blocker; `sensei.py calls --from N` prints nothing on a 93-call transcript.
