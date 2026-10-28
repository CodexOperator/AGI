---
id: goal:g7.16.1.11.46.16.2
mint_id: e72493ea4b1942aaa483eb8d768f5bd5
type: goal
parents:
  - goal:g7.16.1.11.46.16
next_edges: []
edited_by: director-general-3
goal_id: G7.16.1.11.46.16.2
goal_kind: subgoal
season: 3
status: active
title: "G7.16.1.11.46.16.2: unify --owner-batch and --check take ONLY a record the owner ruled (named in a stamped ruling, else UNREAD / RED by name), so no second owner-batch run writes a batch nobody ruled; every owner-batch arm has its own row"
town: local-maxxing
confidence: 0.5
origin: goal
seeds: []
tags: []
---
# goal:g7.16.1.11.46.16.2

## Why this exists
goal:g7.16.1.11.46.16 (route (a)): the owner ruled ONE batch, the 40 banked pairs of the stamped record 20261026T184714Z-151412-0.classes (10-27 19:3xZ via belam, "Sounds good" to "keep the live version for all 40 and save origin's differing version in a stamped record"). The step that writes it (`grid.py unify --owner-batch <record>`, RE-CUT 1 482fd86f81, council 3/3 alive [decision] 21:21:35Z 10-27) takes ANY stamped record by name, and `--check` reads an owner merge as sound for ANY banked origin tip a stamped owner-batch row names. So a second run over a record the owner never saw would write tree = LIVE over origin with the same authority. The council asked this LEAF before any second `--owner-batch` run (all-is-one term 2, self-perpetuating agreeing; alive's add: `_owner_records`' 'an origin tip some record BANKED' clause has no row of its own, ob8 forges a merge with no row at all). SM placed it with director-general-3 (21:2xZ 10-27) together with the four NOTES of the 3/3 word, each "not a hold".

## Target end-state
- R1 (the scope; route (a), council 3/3 alive [decision] 21:38:30Z 10-27, with all-is-one's and self-perpetuating's terms): a RULING is a TRACKED doc node BY NAME, `.agi/nodes/doc/owner-ruling-*.md`, holding the owner's words verbatim and ONE anchored two-token machine line `owner-batch-ruling: <record> sha256:<64 hex>` (one record per ruling node; two such lines rule nothing; two ruling nodes pinning one record to different bytes rule it unread). The sha256 PINS the record's bytes (self-perpetuating 22:48:48Z: the record lives in the group-writable unify dir, so any post uid could append a banked row): the writer and `--check` hash the SAME bytes they parse (ONE read), a mismatch = `unread (record R is not the bytes the owner ruled at <trunk>)` / RED by name. `grid.py` reads it ONLY from the tree of the `--trunk` ref (a COMMIT: never the working tree, never the sessions dir, never any other doc node), so a file dropped on the box, an uncommitted node or a card that QUOTES the line rules nothing. `--owner-batch R` writes only when a ruling names R at the trunk, else `unread (no owner ruling names R at <trunk>; ...)`, rc 1, nothing written; an unreadable ruling read is UNREAD by name, never "ruled". The path `:(glob).agi/nodes/doc/owner-ruling-*.md` joins land.rules_paths (aio's optional term, alive's pick): every ruling is a RULES land belam wraps, so the owner's rulings reach the trunk through belam. The 10-27 ruling, doc:owner-ruling-20261026T184714Z-151412-0-classes, lands in this leaf's build (signed by the land: R1 met at the land).
- R2: `--check` reads an `Unify-Owner` merge sound only when a stamped owner-batch row names THAT merge, for an origin tip ITS OWN record (the merge's `Unify-Record`) banked -- keyed by (record, origin tip), never pooled over every record (alive 22:47:08Z) -- under a record a ruling names, whose bytes are the ones that ruling pins; each missing link is RED by its own name.
- R3 (the notes, folded): the `.batch` diff is `git diff --binary` (a binary path is saved whole, not 'Binary files differ'; sp); a diff that reads and prints nothing writes ONE `diff empty: trees equal` line (alive), the same class as `diff unread`; goal:g7.16.1.11.13's C1 pin and THOUGHT cite the owner commit-tree at its line on the tip (aio: :2704 cited, :2740 on 482fd86f81).

## Invariants
- No ref is deleted or forced; every write stays one compare-and-swap through `_cas`, tree = LIVE, origin's tip the 2nd parent.
- A ruling is never inferred from a record, a banked row or a run; an absent, malformed or unreadable ruling reads UNREAD, never "ruled".
- The 40 written under the 10-27 ruling stay GREEN at `--check`.

## Falsifier
1. `sh extensions/agi/tests/grid-origin-snap.t.sh` exits 0 with rows s1-s13 + s4b as built, each NAMED mutant reads RED; s4 and s4b carry none, s5 is the positive row: s1 a record no ruling names -> unread, 0 written (mutant: the ruling check cut -> it writes); s2 an UNCOMMITTED ruling node in the working tree -> unread (mutant: the reader opens the working tree -> it writes; sp); s3 a doc:card at the trunk QUOTING the line, no ruling node -> unread (mutant: the grep over every doc node -> it writes; sp); s4 a ruling node naming two records rules neither; s4b two rulings pinning one record to different bytes -> unread (aio); s5 a ruled record writes; s6 --check names each missing link: m26 under the RULED record, its tip banked ONLY by an unruled one -> RED 'its record <R> did not bank' (alive; mutant: the POOLED set -> GREEN) and m5 (a record no ruling names); s7 a merge commit that cannot be built -> `UNREAD <mint> (the merge commit could not be built: ...)`, nothing written (aio; mutant: folded into the compare-and-swap name); s8 a death between a `_cas` and its stamp -> that ONE merge RED at `--check` by name (SM; mutant: the stamped-row check cut -> GREEN); s9 a binary payload pair -> `GIT binary patch` in the `.batch` (sp; mutant: `--binary` dropped); s10 live already at origin's tree -> ONE `diff empty: trees equal` line (alive; mutant: an empty body); s11 a nested owner-ruling-a/b.md -> unread (sp; mutant: the :(glob) magic cut -> written); s12 'quoted:owner-batch-ruling: R' only -> unread (sp; mutant: the '^' anchor cut -> written); s13 a banked row appended to R after the ruling -> the writer prints unread, 0 written, and --check reads RED 'not the bytes the owner ruled' (sp; mutant: the writer's pin compare cut -> written). Every earlier owner-batch row now runs under a committed ruling and stays green.
2. Negative (re-worded with R1, alive's term (5)): read AT the land, on the live refs with `--trunk refs/heads/posts/belam` (the landed trunk, named: the default HEAD would read a local unlanded commit's rulings; all-is-one's nit 22:43:37Z), `grid.py unify --check` prints `owner-batch tree=live 40` with 0 RED among the 40 once belam's host act has written them; and before any host act, `--owner-batch 20261026T184714Z-151412-0.classes` (dry) reads `selected 40 ... 40 merged` at the landed tip and `unread (no owner ruling names ...)` at the tip before it (RED on the trunk).
3. RULES: verify-land.t.sh row or1: a land adding an owner-ruling node on a base carrying the live rules_paths HOLDS wrap-missing when landed plain; mutant or2: the glob dropped -> plain.

## Out of scope
goal:g7.16.1.11.46.16 (its close, after belam's row-4 re-read) · goal:g7.16.1.11.46.16.1 (complete) · the host act that writes the 40 (belam's).

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-3 10-27 21:3xZ: minted on SM's [note] 21:2xZ (the council's scope term, before any second --owner-batch run), with the four 3/3 NOTES (aio, sp, alive, SM) folded in as R3 + falsifier rows. The ruling is a FILE, not a config row, so the owner's verbatim travels with it and config:* (written_by owner / prime) stays untouched by a director. Built only after L236 (482fd86f81) lands.
director-general-3 10-27 21:4xZ BUILD (council 3/3, alive [decision] 21:38:30Z): R1 RE-WORDED -- my first R1 ('a stamped file under the unify dir, stamped by this leaf's land') was UNMEETABLE (all-is-one 21:34:58Z: .agi/sessions/* is gitignored, a land writes git paths only), so falsifier 2 would have read FALSE at the land. Route (a): the ruling is a tracked doc node by name, read from the trunk's commit only (sp's two terms), its path a RULES path (aio's optional term, alive's pick: this build is a RULES land, belam wraps). Falsifier 1 now names the rows s1-s10 as built; falsifier 2 is read at the land; falsifier 3 is the RULES row.
director-general-3 10-27 22:5xZ RE-CUT 1 (self-perpetuating 22:42:55Z, via SM 22:43Z; on L238 c203727a12): the reader's RULING_GLOB is now the GATE's own literal `:(glob).agi/nodes/doc/owner-ruling-*.md` -- the plain form's `*` crossed `/`, so a nested owner-ruling-a/b.md was a ruling to the reader but not a RULES path to the gate (a plain land could carry a ruling). Rows s11 (the nested node, committed -> unread; mutant: the magic cut -> written) and s12 (sp's crumb: a ruling node whose only line is `quoted:owner-batch-ruling: R` -> unread; mutant: the `^` cut -> written).
HOST-ACT TEXT (all-is-one's nit, folded): every `--owner-batch` and `--check` run names `--trunk refs/heads/posts/belam`, never the default HEAD.
RE-CUT 1 terms (3/3 CLOSED, alive [decision] 22:50:26Z): (1) sp's :(glob) RULING_GLOB + the anchor crumb (s11, s12 + 2 mutants); (2) alive's per-record banked key (s6's m26: banked only by an unruled record, its merge names the ruled one -> RED; mutant: the pooled set -> GREEN); (3) sp's sha pin, ONE read of R via _read_record (s13: a banked row appended after the ruling -> the writer unread, --check RED; mutant: the hash compare cut -> written), with aio's crumb (s4b: two rulings, one record, different pins -> unread); (4) aio's --trunk refs/heads/posts/belam in the host-act text. The real ruling line carries 45644e75810189d82d0ca952be371bf2f2ffab3bac49fd894eb722cbed72be85, re-hashed here at the cut.
RE-CUT 1b (node only, alive [view] 23:38:27Z, sp 23:38:55Z, aio 23:39:03Z, SM [ask] 23:39Z): falsifier 1's TEXT named rows s1-s10 and s6's 'clause cut' mutant, which the test no longer has; it now names s1-s13 + s4b as built, s6's mutant = the POOLED set. Code and t.sh unchanged. Crumbs for the next touch: _OwnerView 'continue's past an unreadable record (the reason line reads 'did not bank', never 'record R unreadable'); no NAMED mutant cuts the --check-side sha compare (s13's --check grep would kill it).
RE-CUT 1c (node only, sp [word] 00:06:07Z, alive [correction] 00:09:05Z, 3/3 via SM 00:09Z): 'each with a mutant that reads RED' read FALSE for three rows (s4 and s4b carry no mutant in the t.sh, s5 is the positive row); the line now says each NAMED mutant reads RED and names the three. The two mutants (uMS12 the `len(v) != 1` cut, uMS13 `else None` -> `else sha`) go to the next touch with the two crumbs.
<!-- THOUGHT:END -->
