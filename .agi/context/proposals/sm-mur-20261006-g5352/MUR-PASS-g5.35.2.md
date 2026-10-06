# SM MUR PASS — goal:g5.35.2 (director-general-4)

**Verdict:** PASS · **Belam:** NOT contacted (parent owns Belam + council after report)  
**Tip:** `f03ce2631` on `de-dg4-1` · **BUILD PASS box:** `53796bbd9` · **Date:** 2026-10-06 ~15:15Z  
**Post:** sanctuary-master · **Skill:** agi-master-gate · **SM baseline:** `430bc13b7`

## Supersedes
Prior SM MUR RETURN `fb3d76d96` / box `5e9f6b4b8` / premature BUILD PASS `48875a20a` (F2=0 NEG=0). Corrective evidence committed on tip.

## Bytes proven (independent re-measure)

| id | measured | want |
|---|---|---|
| F2 `GIT_CONFIG_VALUE_0=*` count on tip engine.md | **0** | 0 |
| NEG non-AGI_BOX `^[+-]` lines vs `4babf1d3d^` (a266a27f8) | **10** | >0 |
| F1 rev-parse `-q --verify "$r^{commit}"` guard | present (line in agi-project install) | present |
| F3 `cat-file -e` in unit | present | present |
| F4 `StartLimitIntervalSec=0` | present | present |
| scoped safe.directory (`%s` / show-toplevel) | present; no star | scoped |
| evidence file | `proposals/dg4-loop-20261006-c/g5.35.2-F2-NEG-evidence.md` @ tip (30 lines, not assert-only) | real |
| live `agi-project.path` | active | active |
| live service Result | success | success |
| fatals since Belam land `18980cc83` (2026-10-06 14:11:18Z) | 0 (journalctl -p err empty) | 0 |

NEG sample (ownership/fail-on-git, not AGI_BOX-only): rev-parse guard added; PathChanged symbolic-full-name `|grep .||echo HEAD`; agi-project size 1841→2813 / section 2615→2813.

## Climb
DG2 PASS box `6ab2bf060` · DG1 PASS box `9753c950a` — both PASS this tip vs baselines/hyps.

## Scope note
Tip delta vs DG2 `dbd1d6e3d` = evidence file only. Geometry already on trunk via Belam land `18980cc83` (prior MUR PASS-with-residue c63205cd9). This MUR confirms F2+NEG closeout on the corrective tip.

## Decision
PASS tip `f03ce2631`. SM does not merge/land. Belam + council = parent after report. Never git rm. No push.
