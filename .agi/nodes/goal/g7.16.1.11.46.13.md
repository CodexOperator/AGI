---
id: goal:g7.16.1.11.46.13
mint_id: f556c1eddefb4732860522483ab49bae
type: goal
parents:
  - goal:g7.16.1.11.46
next_edges: []
confidence: 0.5
edited_by: director-general-2
goal_id: G7.16.1.11.46.13
goal_kind: subgoal
origin: goal
seeds:
  - doc:brainstorm-unify
tags:
  - brainstorm
  - wave-1
  - M6
season: 3
status: complete
title: "G7.16.1.11.46.13: M6 -- the facing post's chat is tapped verbatim (redacted, never refused) into its own box-local 0700 store keyed by its mint id, never silent and never blocking a turn; mem:/faces: are posts-row cells and faces: owner requires mem: full"
town: local-maxxing
---
# goal:g7.16.1.11.46.13

## Why this exists
goal:g7.16.1.11.46 (the brainstorm bundle, wave 1 addendum): the council cut this leaf from hypothesis:g7161146-w1b-full-memory-beside-the-atoms (alive's [decision] 14:0xZ 10-24, 3/3 with all-is-one and self-perpetuating, read at trunk ebc2942b74; all-is-one's sharpenings S1-S4, author belam YES via SM). Doc §40, §11, §27 (M6). Box readings that shaped it: the shared git dir is 775 with ACLs and its packs are world-readable, so refs/mem in the shared repo would expose the owner's words (R1); on three seats 34/83, 43/69 and 36/85 prompt lines arrived as `attachment.type: queued_command`, not user strings (R3); agi-meter already reads `transcript_path` on UserPromptSubmit (R3).

## OWNER 2026-10-24, verbatim (doc:brainstorm-unify §40 quotes it)
> "every optmem/optchat little chunk is marked to an atom as needed, with multiple chunks able to map to a single atom as
> one chunk would be user doing it the other would be the agent acknowledging."
> "mark it as 'full memory enabled' so other posts that are not owner facing can still have it. I figured prime would always have it."

## OWNER atoms placed here (doc:card-belam §7 rows; they close to leaf:goal:g7.16.1.11.46.13 when this node lands)
| # | atom (owner ask, short) | state |
|---|---|---|
| 10.8 | mark it full memory enabled so non-owner-facing posts can have it; the Prime always | target:§40 M6 |
| 10.1 (store half) | the owner-facing post gets a full optmem/chat memory beside the atoms | target:§40 store (the adapter half is V4, wave 2) |

## Target end-state
- R1 STORE: the facing post's chunks live in their own bare git dir, owned by that post's uid, mode 0700, with no remote, keyed by the post's MINT id (§27); never under refs/mem in the shared repo. Named costs: no remote = no backup until the owner rules (card §6); M8's spider (wave 3) and any non-facing reader need a grant then, outside this leaf.
- R2 REDACT, NEVER REFUSE: each anonymize token in a chunk becomes its placeholder, the frontmatter records `redacted: <n>`, and the redacted bytes are what is content-addressed.
- R3 TAP: the prompt side rides agi-meter (UserPromptSubmit, already reading transcript_path) plus a NEW Stop hook; owner lines come from user strings AND `attachment.type: queued_command`, deduped by transcript uuid, with a Stop sweep from a cursor.
- R4 SPEAKER TRUTH: `speaker: owner` is never written for isCompactSummary, isMeta, tool_result, a nudge ("mail: box read") or another harness-injected prompt.
- R5 ADDRESS: chunk id = sha over (speaker, session, transcript uuid, body); the body stays verbatim (after R2).
- R6 NEVER BLOCKS, NEVER SILENT: an unwritable store leaves the hook at rc 0 with one warn line; the at:/SessionStart line prints `mem: tapped <k>/<m>` (eligible owner lines vs chunks with s=<session>), `mem: unread` when the store or cursor cannot be read, and is RED when k < m.
- R7 CELLS: config:posts rows carry `mem: full|season|goal|none` and `faces: owner|posts|none`; an absent mem: reads none; only belam's row changes (mem: full, faces: owner); `faces: owner` without `mem: full` is refused by the ONE posts-row reader, named in this leaf's land.

## Invariants
- A chunk is never refused and never edited after write; redaction happens before the address is taken.
- No engine push spelling covers the store (no `refs/*`, no `--mirror`, no remote on the store).
- A hook failure never blocks a turn and never passes silently.
- Spend: the subscription only, 0 API.

## Falsifier
1. `sh extensions/agi/tests/mem-tap.t.sh` exits 0 with one lane per row R1-R7, and each MUTANT reads RED: (R1) the store placed under refs/mem in the shared repo; the store's mode is not 0700 (chmod 0750 -> RED), its owner is not the facing uid, or `getfacl` lists ANY ACL entry on it (one entry -> RED; the shared .git dirs carry default ACLs a child inherits and chmod masks but does not remove); the store lists a remote; a real second-uid read runs only where a second uid exists · (R2) a prompt with a home literal yields no chunk, or a chunk with the literal (want: one chunk, redacted: 1, no literal in the store) · (R3) a queued_command owner line yields no chunk · (R4) a compact summary or "mail: box read" yields an owner chunk · (R5) the same words twice under two uuids yield one chunk · (R6) the store raises and the hook exits non-zero; the hook drops one line and the at: line is not RED · (R7) a row with faces: owner + mem: season is accepted (want rc != 0, one named line).
2. Negative: `git -C <shared repo> for-each-ref refs/mem` prints nothing on the trunk after the land, and `git grep -nE "push.*(refs/\*|--mirror)" -- extensions/agi/bin extensions/agi/hooks` prints nothing (mutant, planted by mem-tap.t.sh: a `"push", "origin", "refs/*:refs/*"` line makes it hit -> RED).

## Out of scope
goal:g7.16.1.11.46.14 (M7, the chunk->atom edge) · M8 the walk (wave 3) · V4 + M9 + M10 (wave 2) · the pi and UniiChat adapters · the owner's push/backup ruling (card §6).

## Agent Notes
Assigned to **director-general-2**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v3 (director-general-2 10-24, CLOSE): built in three tips and landed as L109 f6adf7f7ed (the tap, the store, the cells), then L110r 769ea2db11 (the R4 fix after belam's LIVE red). Falsifiers RE-RUN at trunk 3423d341ac: mem-tap.t.sh exits 0 (55 ok lanes, 1 skip: the peer-uid read, no second uid on the box; mode, owner and ACL lanes carry the permission, G3); `git for-each-ref refs/mem` on the shared repo prints nothing; the fixed push ERE prints nothing. LIVE, as belam (his L110r [landed] 16:3xZ): `mem: tapped 2/2`; owner chunks whose source origin.kind != human = 0; owner chunks whose body opens with `<` or `[SYSTEM` = 0; the five wrongly linked card rows clear. What the live red taught (rows now in the piece and its lanes): (1) the cell read must read ROW lines only and a failed read is named, never quiet (alive's red on e79364f6b1); (2) `speaker: owner` needs origin.kind human AND no tag opener AND no nudge, because a peer's queued_command (origin kind peer) was stored as the owner's words; (3) `mem: tapped k/m` shares one filter between k and m, so it shows completeness, never speaker truth: it is RED on k != m, and the close evidence adds the origin and opener counts; (4) a bad chunk is RETIRED (moved to mem/retired/, bytes unchanged, `agi-mem scrub`), never deleted. DEVIATIONS / DEPENDENCIES: V1 dependency (belam, council): the store key is ${AGI_MINT:-$AGI_POST} until the section 27 mint cell exists; the leaf that adds it moves ~/.mem/<post>.git to the mint path in the same land, never orphaning it. Banked for the owner (belam's card): a SECRET typed into the chat is stored in plaintext at rest in the post's own 0700 store (a post uid cannot read the secrets source); it never travels, and C2 says a slice is cited only after a secrets-aware check by a uid that can read the source, before the atomizer goes live. No remote means no backup until the owner rules. The pi adapter taps nothing (no transcript_path in its hook JSON). FOLLOW-UP C4 (council 16:5xZ, a named row, not a gate): a posts.md line that NAMES the post but yields no parsed row (the cell read uses fromjson?, which skips an unparseable line, so a malformed belam row reads as no row and the piece is quiet) must read `mem: unread` plus the one [mem] warn, never quiet; MUTANT: break belam's row JSON with the other rows valid. Built only on an order.
v2 (belam 14:2xZ 10-24, council [decision] 14:1xZ 3/3 G1 + G3, node-text corrections; rows unchanged): G1 falsifier 2's pattern was vacuous (in git grep's ERE `[^\n]` is "not a backslash, not the letter n", so `push[^\n]*` missed both a refs/* push and --mirror and its own mutant read green; my error) -> `push.*(...)`. G3: a stubbed `id` cannot prove a permission, so the R1 lane asserts mode 0700 + owner + no ACL entries, with chmod-0750 and one-ACL-entry mutants.
v1 (belam 10-24 14:0xZ, minted by the brief's author on the council's word: "belam writes the two leaves (.46.13 M6, .46.14 M7) on the trunk; DG2 is the Assigned director of both"): rows R1-R7 are the council's decision verbatim in substance, each turned into a target line and a mutant lane in falsifier 1. Two edits from the brief: the store is its own 0700 bare dir, not refs/mem in the shared repo (council R1, after reading the shared dir's modes), and redaction replaces my brief's "passes the anonymize token check" (all-is-one S2: a refused chunk is a lost ask).
<!-- THOUGHT:END -->
