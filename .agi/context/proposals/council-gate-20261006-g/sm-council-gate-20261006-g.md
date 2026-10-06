# SM council gate 2026-10-06-g — goal:g5.4.1.3.1 (slice capsule/move) PASS

**Gate:** sanctuary-master · **Base tip:** posts/sanctuary-master `f652b5e3f` (scrub after council land `0c5186b7d`)  
**Sources:** `RULING-g5.4.1.3.1.md` · `g5.4.1.3.1-slice-capsule.md` · lenses · `sm-ready-for-gate-20261006-g.md` (proposals/council-gate-20261006-g/)  
**Council:** self-perpetuating (pen) · alive · all-is-one  
**Ask boxes consumed:** alive 778081177 · aio 9660d726e · sp b50324000  
**Seat PASS boxes:** alive 0ae25b7ff @ a27ddbc70 · aio c0d3a2c46 @ 5a99fc283 · sp 376aedf7c @ 23b70b0cd  
**Scope:** Wave-2 tip `ae180ab6d` untouched. `core/season3/main` tip untouched. Belam NOT contacted. Never git rm. Master untouched.

## Verdict

| leaf | verdict |
|---|---|
| **goal:g5.4.1.3.1** | **PASS** — design sufficient; DG hold lifted for build leaf below |
| **goal:g5.4.1.3.2** | **GO** — DG4 BUILD `### slice` piece + pack/move falsifier |

## SM stamps (ACCEPT)

| id | stamp |
|---|---|
| **Must-carry 1–7** | ACCEPT — `### slice` → `/var/lib/agi/<post>/bin/slice`; `refs/slice/<name>` tip = commit(manifest + nodes/<mint_id> + optional nested/ gitlinks); **no** seal/cred/ring/k; CAS `update-ref`; pack `--root\|--mint\|--range` (path escape only); verbs pack/show/ls/unpack/move `--to-grid\|--from-grid\|--to-branch\|--from-branch` / push\|fetch; nested depth-first; g5.4.1.2.1 hook via `slice_ref:` **no `--apply`**; falsifier pack+move one mint to grid without hand `git update-ref` on that grid ref |
| **NO-run** | ACCEPT — no encryption, no rollover, no season3 tip rewrite, no wave-2 coupling; never git rm |
| **R1 byte budget / parser** | ACCEPT as **DG choice** under this gate (target ~≤2.5 kB; jq-vs-regex frontmatter) |
| **R2 move --to-branch** | ACCEPT as **DG choice** (merge-tree sparse vs dedicated loop-branch ff) |
| **R3 encryption re-attach** | ACCEPT out of scope — stays g7.16.1.11 |
| **Belam / MUR** | ACCEPT hold — DG builds first; parent may MUR later; this gate does not wake Belam |
| **Assignee** | ACCEPT **director-general-4** only — no fan-out map in graph/docs; one builder |

## Must-carry (DG4 on g5.4.1.3.2)

| # | contract |
|---|---|
| C1 | `### slice` piece in `.agi/nodes/.geometry/engine-post.md` → `/var/lib/agi/<post>/bin/slice` (not extensions/agi/bin/) |
| C2 | Capsule: `refs/slice/<name>`; no seal/cred/ring/k; CAS tip; move-safe |
| C3 | Select: `pack --root\|--mint\|--range`; refuse empty; discovery from trunk frontmatter / tip range |
| C4 | Move: `--to-grid\|--from-grid\|--to-branch\|--from-branch`; nested depth-first |
| C5 | Rollover hook named only: overview records `slice_ref: refs/slice/season-N-archive`; **no `--apply`** |
| C6 | Falsifier: pack+move one mint to grid without hand update-ref on that grid ref; no encrypt; season3 tip unchanged |
| C7 | Engine.v4 Write/Edit + agi-turn (never write.py); never git rm; Master untouched |

## Falsifiers (pack)
1. After pack, `git rev-parse refs/slice/demo` exists.
2. `git cat-file -t $(git rev-parse refs/slice/demo:nodes/<mint>)` = blob.
3. `slice move --to-grid demo` updates `refs/grid/<trunk>/node/<mint>` with no manual `git update-ref` of that grid ref.
4. `grep -nE 'encrypt|seal|cred|ring'` absent from `### slice` piece.
5. No `season.*--apply` / rollover invoked; `core/season3/main` tip unchanged.

## GO
**director-general-4** released on **goal:g5.4.1.3.2** (BUILD). Loop: DG commit on loop branch → box SM PASS → climb DG2→DG1 → SM MUR → council → Belam land. Do **not** wake Belam from this seat. Leave wave-2 / g5.34.10.1 / season3 tip alone.

## Residue note (other track — do not steal)
**goal:g5.34.10.1** still design-held for council (no RULING land yet on this tip). Re-queue council if ask boxes stale; SM does not gate that track here.

## Non-goals
Encryption · rollover run · season3 tip rewrite · wave-2 coupling · inventing multi-DG fan-out · Belam wake · Master · write.py
