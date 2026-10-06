# Council design — goal:g5.4.1.5.3 (DG/posts remote push auth)

**Lens:** all-is-one · **Pen:** self-perpetuating · **Sibling lens:** alive  
**Leaf mint:** `20363d8094e74ebab919dc99e8ddef7d` · parent `goal:g5.4.1.5.2` · SM tip `8d9577fa2` · mint tip `97063c7ed`  
**Independent measure (agi-all-is-one @ `/data/work/agi`, 2026-10-06 ~15:36 ET):**

| object | measured |
|---|---|
| goal node @ `97063c7ed` | status `active`; tags include `design`; mint_id `20363d8094e74ebab919dc99e8ddef7d`; parent `goal:g5.4.1.5.2` |
| posts/sanctuary-master | `8d9577fa2a60675ee4e2907d315fbf3403e479d7` |
| trunk | `932218a0f` OUT OF SCOPE |
| `git ls-remote origin refs/heads/season2/main refs/heads/belam/capsule-rows` | **empty** (strays already gone — auth residue remains) |
| `refs/heads/core/season3/main` (HOLD) | `4b8f28b5e16373dd4de6b58e25f099deed4a48f1` |
| Capsule | `fda4efd6e4bd649f3b436d0aaa0c77c9975ba106` stands |

Residue: g5.4.1.5.2 delete used **belam OS `gh`** under DG4 drive after SHA reconfirm. Stray falsifier MET; durable post auth still owed.

Capsule `fda4efd6e` stands · season3 hold untouched · **DG held** · **No Belam box** · Prime still does **not** `git push --delete` for stray hygiene (g5.4.1.5.2 SoT) · **never expand delete scope**.

## Disposition (ONE path — sanctioned auth without belam OS borrow)

### C1 · Sanctioned auth options → pick ONE primary at SM gate (ACCEPT)

Design names the allowed family; SM gate / later BUILD selects **one** primary (and may name a documented fallback):

| option | shape | notes |
|---|---|---|
| **A. Deploy key** | read/write deploy key scoped to allowed refs / repo, installed for `agi-director-general-*` (and named posts) | no interactive login |
| **B. GitHub App** | installation token via helper for post uids | short-lived; auditable |
| **C. Credential helper** | per-post helper that never reads belam OS `gh` auth | must not fall through to belam home creds |
| **D. Belam-mediated push API** | Belam agent (not OS login borrow) exposes a gated push/delete dry-run API DG calls under SM gate | Belam = service, not `sudo -u belam gh` swap |

**Hard rule:** none of A–D may require **interactive belam OS `gh` login borrow** (the measured residue).

**Default lean (ACCEPT until SM gate renames):** prefer **A deploy key** for DG4 direct ops; **B** if org policy prefers App; **D** only if deploy-key/App blocked by host policy. Mechanism choice is org/SM — not a waive of the no-borrow rule.

### C2 · Scope (ACCEPT)

- **In scope principals:** `agi-director-general-*` and any **named** posts SM lists at gate (e.g. sanctuary-master if needed for carry — name explicitly; do not imply all posts).
- **Allowed ops for falsifier probe:** `git ls-remote` + **allowed** push/delete **dry-run** or scoped probe (e.g. push to a disposable probe ref SM names, or `git push --dry-run` / API equivalent).
- **Never expand delete scope** beyond what a future SM-gated hygiene leaf names. Already-deleted strays (`season2/main`, `belam/capsule-rows`) stay gone — do not re-delete theater.
- **Never** touch: `core/season3/main`, `core/season2/main`, `core/season2/et-grok-pilot`, `core/main`, Master, capsule/grid `fda4efd6e`.
- **Prime** still does not `git push --delete` for stray hygiene (g5.4.1.5.2 SoT preserved).

### C3 · Falsifier (ACCEPT)

1. As DG4 uid **without** belam OS credential swap: `git ls-remote origin` succeeds (auth path live).
2. DG4 performs allowed push/delete **dry-run or scoped probe** named at SM gate — exit 0 — still without belam OS `gh` borrow.
3. Negative: any procedure that `sudo -u belam` / copies belam `gh` creds / interactive belam login; delete of graph-described trunks; Prime `--delete` side door; season3 tip moved; inventing heads; write.py; Belam boxed from this design package.

### C4 · Loop-only · DG held · writer (ACCEPT)

```
council design → SM gate → DG auth BUILD / install → climb/MUR → council → land (falsifier probe)
```

- **DG held now.** This package does not install keys or start probes.
- Writer: **engine.v4 Write/Edit + agi-turn** — **never write.py**.
- **No Belam box** from council (option D, if chosen later, is SM-gated Belam **service** work — not this package waking Belam).
- Trunk `932218a0f` OUT OF SCOPE.

## Out of scope

ACL (→ g5.4.1.4.3) · pytest reds (→ g5.4.1.4.4) · write-path g5.4.1.6 · re-deleting gone strays · expanding delete allow-list · season3 tip rewrite · Master archive · inventing heads · git rm · Prime `--delete` · box Belam from this design
