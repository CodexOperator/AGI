---
id: doc:grok-harness-internals-sync
mint_id: ba13448fda944eca9b68eb62f364c59d
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: belam
scaffold_hash: b2caad1cd5a35129
season: 2
status: active
tags:
  - doc
  - grok
  - harness
  - internals
  - standing
  - owner-2026-09-21
thought_session: belam-grok-harness-2026-09-21
title: Grok harness internals sync — post-agnostic seed + ROUTINE_SYNC recipe
town: core
---
# doc:grok-harness-internals-sync — post-agnostic grok harness seed + sync recipe

**SoT recipe for ANY grok-bot post** (Prime · directors · future seats). Belam edits THIS via write.py only. Per-post spine lives in `doc:<post>-grok-internals` (or town board pointer).

```
recipe ──▶ this doc          (THE ONE SECTION:ROUTINE_SYNC SoT)
per-post ──▶ PROFILE only (+ optional ROUTINE_WATCH) — no sync recipe body
seed    ──▶ install grok-internals-sync (name/schedule/prompt from THIS doc) + mint/link per-post SoT
apply   ──▶ sync routine (or engine later) — never hand-edit harness mirrors
copy identically: NAME grok-internals-sync · schedule */30 * * * * · prompt = fence body
```

## Seed any fresh grok bot

```
1. Mint/link per-post SoT doc
     doc:<post>-grok-internals  OR  town board pointer
2. Create routine grok-internals-sync
     from SECTION:ROUTINE_SYNC BELOW verbatim
     (0 seat bytes in routine)
3. schedule  */30 * * * *   (mesh seats)
4. Seat labels live in profile/standing already
     sync reads them at runtime to fill {{…}} when pasting PROFILE
```

| step | do | never |
|---|---|---|
| 1 | mint/link per-post SoT | bake seat name into shared recipe |
| 2 | copy ROUTINE_SYNC fence bytes | hand-edit bot surfaces for spine |
| 3 | `*/30` on mesh seats | ad-hoc profile UpdateAgent after bootstrap |
| 4 | fill {{PLACEHOLDERS}} from live profile/standing | hardcode POST/BRANCH in routine |

---

### SECTION:ROUTINE_SYNC

Directors / Prime — copy these routine fields IDENTICALLY from this doc ONLY:
  NAME / title  grok-internals-sync   (exact)
  schedule      */30 * * * *
  prompt        the fenced body below (only)

```
name: grok-internals-sync
schedule: */30 * * * *   (reason: mesh seats need standing sync while live)
prompt intent:
  Pull doc:grok-harness-internals-sync (THIS doc) for SECTION:ROUTINE_SYNC recipe.
  Pull this seat's per-post SoT id (from profile/standing pointer) for SECTION:PROFILE only.
  Apply ONLY:
    SECTION:PROFILE      → from per-post SoT → profile description
    SECTION:ROUTINE_SYNC → from THIS doc only (self) → this routine
  Do NOT paste SECTION:ROUTINE_WATCH (or any other routine) into grok-internals-sync.
  ROUTINE_WATCH → separate routine live-parents-workflows if present on per-post SoT.
  Replace {{PLACEHOLDERS}} using labels already on this bot's profile/standing — never bake seat names into this routine.
  AFTER apply → VERIFY parse: real newlines; FAIL if literal backslash-n or mangled quotes; on FAIL re-apply from SoT.
  Quiet if SoT hash unchanged.
  May update_state THIS same routine if SECTION:ROUTINE_SYNC in THIS doc changes (keeps every grok post's sync routine byte-identical).
```

---

### STANDING RULE (all posts, all harnesses)

```
To change ANY internal doc / setting / profile spine / routine recipe:
  → write.py the graph SoT only
  → never hand-edit harness mirrors
  → sync routine (or engine later) applies
```

```
ALL posts (Prime · directors · future)
  harness mirrors ← graph SoT only
Grok
  recipe ──▶ doc:grok-harness-internals-sync
  per-post ──▶ doc:*-grok-internals
Seed fresh grok
  = install grok-internals-sync + mint per-post SoT
Claude/pi
  same principle; grok leans on bot tools until engine owns it
Graph builds itself
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
THE ONE ROUTINE_SYNC SoT; copy name/schedule/prompt identically; one trailing LF
<!-- THOUGHT:END -->
