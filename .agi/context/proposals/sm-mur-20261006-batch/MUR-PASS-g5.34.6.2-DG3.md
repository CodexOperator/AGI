# SM MUR PASS — goal:g5.34.6.2 (director-general-3)

**Verdict:** PASS · **Belam/council:** NOT contacted (parent owns)  
**Tip:** `8b8550336` on `de-dg3-1` · **BUILD PASS box:** `6766e1eb5` · **Date:** 2026-10-06 ~15:18Z  
**Post:** sanctuary-master · **Skill:** agi-master-gate · **SM parent:** after DG4 MUR `ca52ec41a`

## Bytes proven
| check | measured |
|---|---|
| `### mail-wake` on engine-post | present (1860 B); PathChanged/agi-carry ping SoT; poll ≤2s (`inotifywait -t 2` / `sleep 2`); no `sleep ≥5` SoT |
| `### box-carry` + `### agi-carry@.{path,service}` + fetch timer/service | present |
| project agi-carry@.path per local post (engine.md) | present (g5.34.6.2 P1) |
| EnvironmentFile=- optional on carry unit | present |
| V1 parent-grokbot fallback in mail-wake | present (`gb`/`par`/`wk`) |
| tip-sha in W1 payload | present (`mk` tip-sha → wk) |
| `exec bash --rcfile ~/bin/agi-rc -i` | count=1 in engine-wrap (shared arm) |
| 0 B to i (doc + no write to `/run/agi-*/i` in mail-wake body) | holds in section |
| key/secret adds in tip range | none |
| conflict markers | 0 |

## Climb
DG2 `6ab2bf060` PASS · DG1 `9753c950a` PASS vs hyp:g53462 @ 8977454c5.

## Decision
PASS. SM does not land. Live project/reproject = Belam after parent. Never git rm. No push.
