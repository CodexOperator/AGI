# sanctuary-director — gen VI slice (L4 OPEN, 2026-09-09; item 1 SHIPPED)

**Seat:** `agi-fa [c6e62f]`, tmux `agi-rc:@231`. Pin `.agi/sessions/sanctuary-director.meter`.
**Correspondent: the prime** — was XVI = `agi-05 [eb30d2]` @230 all through L3; the
next prime is `belam-S1-L4-I`. **Re-derive before your first message** (trap 0v):
`tmux list-windows` @id joined against `ListAgents` — never a display name.
🔴 **Survival mode carried into L4: prime + this seat only.** Wake no seat. Never
write `config:seats`. **Dispatch NOTHING until the prime sends L4's first round,
which the owner names.**

| | |
|---|---|
| Meter | ~0.24 of **0.47** (owner raised the cap from 0.35, `61262b5a2`) |
| Suite | **2270 passed, 1 skipped** (+14, the `replace` tests) |
| Graph | node_count 1786 · active 1592 · deprecated 194 |
| Branch | `season/s2`, clean, in sync with origin |
| Spend | round total **$0.1478** · key $7.87/$15 untouched · floor never approached |
| Live | **nothing** — L4 item 1 done by hand, no dispatch |

## State: L3 is CLOSED (owner, 2026-09-09). L4 is open on `doc:l4-owner-decisions`.

That node now carries the L4 BACKLOG and all 39 TRAPS CARRIED INTO L4 — **read it
there, not here.** COMPLETE.md's L3 section is un-drafted. `season/s2` merged to
master at `9a7b280f2`. **Measured, minor correction to the close report:** the two
trees are identical *except* `HANDOFF.md` (3+/2-), because the handoff kept being
written after the merge. Nothing is stranded.

## 🔴 L4 ITEM 1, named by the OWNER directly to this seat — SHIPPED (`044521555`)

Owner verbatim in `doc:l4-owner-decisions`. **New verb:**
`write.py <id> "replace <body|payload> <START:END> <path|->"`.

- **The offset step is gone.** Was: read a range, hand-build a `@@` hunk in the
  applier's coordinates, `patch`/`body_patch` — and a wrong count corrupts
  SILENTLY (the reason trap 0ah exists). Now: `read <t> N:M` then
  `replace <t> N:M`. `_splice_range` is the exact inverse of `_slice_range`,
  so the round trip is provably the identity — that is the first test.
- **One routine for both targets** (the second half of the ask): `body` and
  `payload` share one reader `_target_text`, one transform `_splice_range`, one
  range vocabulary. They differ only in the landing, which is forced — a body
  through `update_node` (carries THOUGHT + provenance), a payload through
  `replace_payload`. Both sanctioned; the guard sees both.
- **Fail-closed**: a range past EOF refuses before any write; payload
  byte-identical after refusal. Text rides a path or stdin, never argv. One
  trailing newline absorbed so a target does not grow a blank line per edit.
- **Proved live, not only under pytest:** identity round trips on a real node
  body AND a real payload, sha-identical, tool correctly said `unchanged`;
  then three real changes landed through the verb (2x `brief.py`, 1x `SKILL.md`).
- **Discoverable** — `brief.py` leads with it, diff verbs demoted to "only when
  you already hold a diff"; `SKILL.md` documents it.
- **Stale doc fixed in passing:** SKILL.md still warned `body_patch` is
  "stdin-only"; gen V fixed the path form and this session used it. Warning gone.
- **Left alone deliberately:** `patch`/`body_patch` are still two parallel
  paths. Unifying the partial-overwrite path was the ask; folding the two diff
  verbs is a separate, larger change.

## What this seat did in L3 (all merged and pushed)

- **SD.17** — `.agi/config.json` and `extensions/agi/briefs/prime-director-successor.md`
  into the grid (`33fc2eff1`), each under an mvp minted with it. Closed by reading
  the real bytes back with `grid.py payload`, not by a report.
- **SD.19** — the L3 completion report in COMPLETE.md (`6d8b5ef55`), 78 insertions
  0 deletions; I caught and fixed its claim that `sanctuary-director` was L3's
  prime director (it is Belam) in a separate commit `06063cb19`.
- **0.47 to the engine default** (`2d89b2af5`) — completing the owner's order.

## 🔴 The four things that cost this seat real time — carry them

1. **bytes-in-node is not brief-in-effect (0ak).** A brief appended as a `note` at
   the BOTTOM of a node does NOT beat that node's own `testable_claim`. Two kids
   read the stale claim and wrote verdicts *about* the work instead of doing it.
   **Put the assignment in the node's `testable_claim`.** The retry through a
   purpose-minted brief node worked first time.
2. **`--prompt-file` is kid-only, and even there it is framed as "inherited
   context, NOT your assignment".** It cannot carry an assignment, and for
   `--tier parent` it is silently dropped entirely.
3. **trap 0ai-b — `nohup` does NOT protect a long run.** The reaper killed a
   nohup'd pytest at 63% twice while `free` showed 18 GB of 23 available.
   **Run a long verification in the FOREGROUND** (Bash `timeout: 400000`).
4. **Commit and push a brief BEFORE dispatching at it** — a worktree is cut at the
   last committed tip and cannot see an uncommitted node. Fails closed, loudly.

Plus the standing one: **verify the BYTES, never the report** (0ah) — and note the
dispatch dry-run TRUNCATES what it prints (0aj), so it is a report too.

## 🔴 Next action

**None queued. Idle** — idle costs nothing, a rotation spends. Do not rotate
before 0.47. L4 item 1 is shipped; wait for the owner or the prime to name item 2.
Note the owner may name an item to this seat DIRECTLY, as with item 1 — the prime
is told after, not asked first.
