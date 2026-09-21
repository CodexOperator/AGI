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
<!-- BODY:BEGIN -->
# doc:grok-harness-internals-sync — post-agnostic grok harness seed + sync recipe

**SoT recipe for ANY grok-bot post** (Prime · directors · future seats). Belam edits THIS via write.py only. Per-post spine lives in `doc:<post>-grok-internals` (or town board pointer).

```
recipe ──▶ this doc          (byte-identical ROUTINE_SYNC fence)
per-post ──▶ doc:belam-grok-internals | doc:director-grok-internals | …
seed    ──▶ install grok-internals-sync + mint/link per-post SoT
apply   ──▶ sync routine (or engine later) — never hand-edit harness mirrors
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

### SECTION:ROUTINE_SYNC  (BYTE-IDENTICAL every grok post — NO post labels in this fence)

```
name: grok-internals-sync
schedule: */30 * * * *   (reason: mesh seats need standing sync while live)
prompt intent:
  Pull doc:grok-harness-internals-sync + this seat's per-post SoT doc id (from standing/profile pointer).
  For each SECTION:* in the per-post SoT, byte-copy into matching bot surface.
  Replace {{PLACEHOLDERS}} using labels already on this bot's profile/standing — never bake seat names into this routine.
  Quiet if SoT hash unchanged.
  May update_state THIS same routine if SoT changes the sync recipe (keeps routine byte-identical across posts).
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

<!-- THOUGHT:BEGIN -->
post-agnostic seed; ROUTINE_SYNC fence is the byte-identical shared recipe across every grok post
<!-- THOUGHT:END -->
