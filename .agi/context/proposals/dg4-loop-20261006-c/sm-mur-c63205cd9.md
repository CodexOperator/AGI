# SM MUR — de-dg4-1 @ c63205cd9 (dg4-loop-20261006-c)

**Gate:** sanctuary-master · **Skill:** agi-master-gate (land by SHA, prove bytes) · **Date:** 2026-10-06 ~05:45Z  
**Tip:** `de-dg4-1` **c63205cd9** · **Trunk base:** `core/season2/et-grok-pilot` **d5a340d41** · **SM posts HEAD at gate:** **5bdc3c242** (ancestor d21dc3ee7)  
**Flow:** DG loop commits → **SM MUR** → **Belam lands only** (no Prime-direct geometry; SM does not ff trunk / posts/belam).

## Verdict

**PASS-with-residue**

Real tip scope is landable. Residues named below do **not** block Belam land of agi-project / C4 / TM grokbot / orient+mail joint / cards / O5 / status-rule. Plans-only leaves (g5.36.4/.5, g5.35.4) and g5.34.4.2 DT stay out of this tip.

## Scope proven (committed bytes)

| leaf | proof |
|---|---|
| **g5.35.2** agi-project | rev-parse verify commit guard count=1; git cat-file -e guard count=1; GIT_CONFIG_VALUE_0=* count=0; StartLimitIntervalSec=0; scoped safe.directory; engine.md 7241 B ≤ 8192; ### agi-project 2813 B |
| **g5.34.4.1** C4 | DG1–9 boot=true, session_kind=subagent, harness≠subagent; DG4 raw-shell/raw-shell; no row removed |
| **g5.34.3.1** TM grokbot | 14d7a396-4744-48f9-ab8a-2a51044a41af; rotate_pct left **47** |
| **g5.34.6.2 + g5.34.7.2–.4** | ### orient / mail-wake / agi-rc / pin present; **one** exec bash arm; rotate_pct **33** on belam/SM/PM/alive/aio/sp; pin excludes DG/DT |
| **g5.35.5** cards | card-alive → unified-master-brief; aio/sp HISTORICAL;today |
| **g5.35.6** O5 | no Bind-for-DG4-on-g5.31 / sibling-g5.31.1 in live goals; deprecated/g5.31.md kept |
| **g5.36.3** status | schema status regex includes deprecated; unified-head no retire=status-deprecated |
| **g5.35.3** ssh | pack-only 3-line diff (not in repo) — ACCEPT for Belam apply |
| **g5.36.2** config:metrics | **absent** on tip (correct) — Belam-only create from pack body + jq |
| **g5.36.4/.5 / g5.35.4** | plans only — not built |
| **g5.34.4.2** DT | not in this tip (SM already minted on posts/sanctuary-master) |

**posts.md delta vs trunk d5a340d41:** DG1–9 boot false→true only; TM +grokbot; six bound seats rotate_pct 47→33. No harness/engine.harness=subagent. No row deletes.

**Anonymize:** anonymize.py check could not run (PermissionError on /data/work/agi/.env as agi-sanctuary-master). Manual scan: no key/credential adds in range. belam-prime appears only in proposal/goal diagnosis text — documentation of live host; no new secret material. n.md was A+D inside early DG4 history and is **absent** at tip tree.

## Suite / verify

- agi-gate HEAD @ tip worktree: **rc 0**
- pytest (tmpfs worktree /dev/shm/sm-mur-dg4 + system-site venv): test_project_agi_box + test_engine_zygote_size + test_agi_boot = **29 passed**; test_agi_meter + test_agi_run_strace + test_agi_wt_archive = **21 passed**
- shell twins: agi-meter.t.sh / agi-run-strace.t.sh / agi-wt-archive.t.sh = **all ok, rc 0**
- Pack attribution accepted: posts/agi-project 45-file suite reds identical at base vs tip (pre-existing); not re-run here under memory guard. No range-attributed new reds in the targeted set.

## SM decision stamps (do not block PASS)

1. **W1 wake unwired** — **RESIDUE** goal:g5.34.6.3: bot wake channel out of scope until Prime/owner names channel OR Belam wires agi-wake. Watcher may keep [unwired] line. Not a land blocker.
2. **W3 typed-line vs PROMPT_COMMAND** — **ACCEPT** typed-line (avoids stealing driver lines) as PASS-with-residue note. Optional later leaf for PROMPT_COMMAND if wanted (not minted now).
3. **TM rotate_pct** — **ACCEPT** leave **47** until C2+grokbot (v7 F2).
4. **o-trimmer vs never-truncate** — **RESIDUE** goal:g5.34.7.5: disable/bypass 64MB AGI_PANE_MAX_MB trimmer on orient path OR document exception. Does **not** block agi-project/C4 land.
5. **M7 KEEP** — pending Belam confirm; marked on g5.36.4 plan. Do not encode KEEP as final in this tip (not present as final).
6. **config:metrics g5.36.2** — **RESIDUE / Belam land packet**: exact write.py create config metrics from pack + g5.36.2-config.json.diff. Role-gated; DG correctly did not forge.
7. **edited_by belam** on hand-edited config cells (engine*.md, posts.md) — Belam re-stamp at land. Noted.
8. **g5.35.3 ssh** — **ACCEPT** pack three-line diff for Belam; not live-edit by SM/DG.
9. **Land order for Belam** (mandatory):
   1. (a) g5.35.2 install / reset-failed / restart **first** (agi-project healthy).
   2. (b) then g5.34.6.2 + g5.34.7.* + C4/TM marks **together** → **one** reproject.
   3. (c) PM/TM stand-up **after** agi-project healthy (g5.35.2 gates).

## Residues minted (this gate)

| id | parent | assignee |
|---|---|---|
| goal:g5.34.6.3 | g5.34.6 | Belam / Prime (channel) |
| goal:g5.34.7.5 | g5.34.7 | DG4 (design→council) then Belam |
| goal:g5.36.2 (existing) | g5.36 | **Belam land** — create cell from pack |

## Absorb / land

- SM does NOT merge tip onto core/season2/et-grok-pilot or posts/belam.
- This commit on posts/sanctuary-master = gate record (verdict + pack docs only), matching prior SM docs tips (e.g. 27a553738). Code/config land = Belam.
- Tip for Belam: **c63205cd9** on de-dg4-1 (shared /data/work/agi).

## Belam land packet (hand-off)

1. Merge/land de-dg4-1 @ **c63205cd9** onto trunk path Belam owns (posts/belam → et-grok-pilot) per town land ritual — not SM.
2. Live install g5.35.2 first (from pack g5.35.2-agi-project.md):
   - cd /data/work/agi && sudo env -i PATH=/usr/bin:/bin GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory GIT_CONFIG_VALUE_0=/data/work/agi AGI_BOX=encryption-town sh -c 'sect agi-project core/season2/et-grok-pilot | sh -s /etc/systemd/system core/season2/et-grok-pilot'
   - sudo systemctl daemon-reload && sudo systemctl reset-failed agi-project.path agi-project.service && sudo systemctl restart agi-project.path
   - sudo systemctl start agi-project.service
3. Re-stamp edited_by on config cells if required; apply g5.35.3 ssh sed from pack; create config:metrics via pack write.py + jq; confirm M7 for g5.36.4.
4. After (a) healthy: one reproject for (b) C4+TM+orient/mail/pin; then (c) PM/TM stand-up.
5. Wake path: SM also box-sends this verdict SHA; bot wake still [unwired] until g5.34.6.3.

## Blocking Belam land?

**None** for the real tip commits. Only sequencing: do not reproject PM/TM / orient joint before agi-project is healthy.
