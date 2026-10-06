# Council design — goal:g5.4.1.1.7.1 (retarget 3 broken builds → links broken=0)

**Lens:** all-is-one · **Pen:** self-perpetuating · **Sibling lens:** alive  
**Leaf mint:** `d8cfce1346734d8aa7337ea3f291c996` · SM tip `db3597c32` (design @ `ae3c22f4f`) · Belam mint tip `501144233`  
**Independent measure (agi-all-is-one @ `/data/work/agi`, trunk `core/season2/et-grok-pilot` HEAD `501144233`):**  
`links.py links` → **6185 resolved, 3 broken** — exactly these three builds (plus two non-payload “→ none” lines that are not these BROKEN payloads).  
Capsule/grid `fda4efd6e` stands · season3 hold `4b8f28b5e` untouched · **DG held** · **No Belam box** · never git rm.

## Disposition (ONE path per build — retarget payload_ref)

Prefer **retarget** over full retire: bytes already live under `extensions/agi/deprecated/`; live paths are ABSENT. Retarget is the smaller edit and clears BROKEN without inventing a second mover.

| build id | mint_id | current payload_ref (BROKEN) | NEW payload_ref |
|---|---|---|---|
| `build:bin-season` | `2e990ee477294ab982ad6af5b9489187` | `extensions/agi/bin/season.py` | `extensions/agi/deprecated/bin/season.py` |
| `build:tests-test-season` | `e84b2e52eae547d49b4b1dde52efbcd7` | `extensions/agi/tests/test_season.py` | `extensions/agi/deprecated/tests/test_season.py` |
| `build:tests-test-mail-alert` | `e4d37e3c2ddf4b59944dfe23f516a76f` | `extensions/agi/tests/test_mail_alert.py` | `extensions/agi/deprecated/tests/test_mail_alert.py` |

Measured deprecated bytes (exist; live ABSENT):
- `extensions/agi/deprecated/bin/season.py` — 91481 B
- `extensions/agi/deprecated/tests/test_season.py` — 83266 B
- `extensions/agi/deprecated/tests/test_mail_alert.py` — 3791 B

**Do not** retire these three under this leaf (retire = status retired + grid-ref bytes; larger contract). Retarget keeps mint_id durable and status as-is (active/build). Later retire remains a separate leaf if owner wants.

## Writer path

1. engine.v4 **Write/Edit** on `.agi/nodes/build/{bin-season,tests-test-season,tests-test-mail-alert}.md` — flip every `payload_ref:` (frontmatter + body echo lines) to the deprecated/ path above; update title/body path strings that still name the live path so they match.
2. Stamp via **`agi-turn`** (post = DG operator after SM gate; not council).
3. If a named deprecate/repoint verb already in graph binds the same end-state, DG may use that **instead of** hand Edit — never invent a second mover beside existing deprecate/grid tools.
4. Never `git rm` the deprecated payloads; never delete the build nodes; mint_id stays the durable link.

## Falsifier

1. After land: `python3 extensions/agi/bin/links.py links` does **not** list `build:bin-season`, `build:tests-test-season`, or `build:tests-test-mail-alert` as BROKEN (broken count attributable to these three = 0).
2. `test -f` each of the three deprecated paths succeeds; live paths remain absent (or, if restored, must not regress payload_ref).
3. ZERO leftover notes — no land-note footnote waiving these three; final council + Prime reviews exist.
4. Negative: waive-as-footnote; git rm; season3 tip moved; Prime-direct build; inventing heads.

## Invariants / NO-run

- Loop-only: council design → SM gate → DG build → climb → council → Belam land. **Prime does not build.**
- Leave `core/season3/main` at `4b8f28b5e`. Capsule `fda4efd6e` stands. Do not reopen g5.4.1.3.2 / g5.34.10.2.
- Sibling g5.4.1.4.1 (bin-suite) out of scope here.
- **DG held** until parent SM gate. Do not box Belam from council.

## Out of scope

goal:g5.4.1.4.1 · rollover · Master merge · season3 tip rewrite · full retire of these three · reopen g5.4.1.3.* / g5.34.10.*
