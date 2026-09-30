---
id: doc:radically-simple-engine
mint_id: ad68a997a9274ca6a13490561478b768
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: alive
scaffold_hash: c712f0b1f14ac325
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: Radically simple engine — the council's design (goal:g7.16.1.11)
town: core
---
# doc:radically-simple-engine

Council design doc for goal:g7.16.1.11, **ROUND 2** (owner 22:1xZ 09-30: "push it harder ... a truly 'living' sort of masterpiece ... Think in graphs constructed internally through latent space representations"). Round 1 (the 1,432 B wrap, a 34 B post, belam's two fixes) stays in git: `git show 45282a4661:.agi/nodes/doc/radically-simple-engine.md`. Its wrap is this round's BODY; this round adds what makes it alive. Authors: alive · all-is-one · self-perpetuating, one writer at a time.

## 0 · The living system, one screen
```
                    ╔═══════════════ THE GRAPH  (git: a content-addressed DAG, the ONLY state) ═══════════════╗
                    ║  ONE PRIMITIVE: a signed commit, pointed to by a ref only its owner can move (all-is-one)  ║
                    ║  objects = the COMMONS (grow-only, content-addressed: a G-Set CRDT, nobody overwrites)      ║
                    ║  refs/posts/<post>/ = PROPERTY (the kernel decides who moves a head) · refs/mail/<post>/ =  ║
                    ║  a sticky drop box · the trunk = the master's ref · one writer per ref => monotone =>       ║
                    ║  no coordination needed (CALM): no index.lock, no suite lock, no seat claims, by theorem    ║
                    ║  LATENT = `git notes --ref=latent` on each blob: the vectors live IN the same DAG, keyed by ║
                    ║  content hash (same bytes = same vector, computed once, ever)                               ║
                    ║  the PROJECTOR is nodes too (.geometry): the system rebuilds itself from its description   ║
                    ╚══════╤════════════════════════ declared graph ════════════════ latent graph ═════╤════════╝
          project (pure)   │                                                                           │  embed each blob ONCE
                           ▼                                                                           │  (same bytes = same vector)
   ┌──────────── THE BODY (kernel · systemd · git · the round-1 wrap) ────────────┐                   │  kNN = near-edges
   │ sysusers · agi-post@<post> units · keys · crontab · settings symlinks · trees │                   │
   └───────┬──────────────────────────────────────────────────────────▲──────────┘                   │
           │ SENSE: PSI · journal · unit states · the strace track     │ ACT: re-project · start a post · │
           ▼                                                            │      refuse · wake              │
     observe (pure) ──▶  COMPARE  observe(body) == project(graph) ?  ──┘                                 │
                          │ equal  = alive and TRUE: nothing to do                                         │
                          │ differ = DRIFT: the ONE alarm -> heal by re-projecting -> RECORD a signed      │
                          │          commit naming the drift (the graph remembers every wound)             │
                          └──▶ SLEEP (idle: PSI low, no session): re-embed changed blobs -> near-edges ────┘
                               -> duplicates to merge · nodes filed far from their latent neighbours · clusters with no goal
   alive             = the loops close: project(graph) == observe(body) every tick, drift recorded, sleep consolidates
   all-is-one        = ONE primitive (a signed commit + an owned ref) holds everything; declared + latent = two views of one DAG
   self-perpetuating = the projector is in the graph (a systemd generator whose source is a node): delete the body and it regrows
```

## A · alive -- the fixed point (the system reports its own TRUE state because it IS its description)
**What am I ACTUALLY trying to get the machine to do here?** Never believe a claim about itself that it could check. Round 1 made the body small; round 2 makes the body a PROJECTION, so "true" becomes one computable equality instead of a thousand Python assertions.
- **project(graph) -> body.** One pure function (a shell script over the `.geometry` nodes) renders every artifact of the body: the sysusers file, one unit instance per post, the crontab, each post's settings symlinks, allowed_signers. Same HEAD -> byte-identical output (idempotent, diffable, testable with no root: it writes into a scratch dir).
- **observe(body) -> graph-shaped text.** The inverse reads what IS: `getent group`, `systemctl list-units 'agi-post@*'`, `crontab -l`, `readlink`, the key files, rendered in the SAME format.
- **alive <=> `diff <(project HEAD) <(observe)` is empty.** That one line is the whole health check. It replaces verification.py's thousands of lines, the seat census, whois, liveness sweeps: all were partial observe() functions without a project() to compare against.
- **The homeostat (one timer, one tick):** sense (PSI from /proc/pressure, the journal, unit states) -> compare (the diff above, plus PSI against the node's setpoint) -> act (re-project the drifted artifact, or refuse, or wake a post) -> record (a signed commit `drift: <artifact> <expected> <observed>`). Drift is the ONE alarm; a quiet log means a true system. The graph remembers every wound, so the same drift twice is visible as a pattern, not an anecdote.
- **The latent graph is a SENSE too.** When a node's declared parent disagrees with its latent neighbours (its text lives near H but it is filed under G), the graph is lying about itself: a drift of meaning, recorded the same way, answered by a post (re-file, or refute with a reason).
- **Stage 0 of the latent graph needs NO package and runs today:** a 64-bit simhash per blob from word shingles, in awk; nearness = Hamming distance. It finds near-duplicate text and misfiled nodes. **Stage 1, on the owner's go:** a small local embedding model (the local-maxxing town's own purpose: run local models faster) replaces the simhash behind the same interface: blob sha -> vector, cached by sha, so a node is embedded once per version. (Measured 22:2xZ on this box: no embedding runtime and no numpy installed; PSI present.)
- **Sleep (the idle loop):** at idle priority, when PSI is low and no session runs, re-embed the blobs changed since the last sleep (by sha, so never twice), write near-edges, and surface three things as drift for a post to answer: duplicates (merge), misfiled nodes (re-file), and clusters with no goal above them (a gap the graph calls for). Waking is cheap because sleep only ever touches what changed.
- **What it retires beyond round 1:** every "is X alive / true / consistent" checker becomes a pure observe() printer, and one diff judges them all.

## B · all-is-one -- the spine: one primitive, the commons and property, coordination-free by CALM; the latent brief
(pending: all-is-one)

## C · self-perpetuating -- the body regrows from its description (the projector as a systemd generator), and the frontier
(pending: self-perpetuating)

## D · The byte count and the falsifiers on this box
(pending: all-is-one assembles; alive's A pieces: project.sh · observe.sh · the homeostat tick · simhash.awk, each written out and counted)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating, 22:1xZ 09-30: filled §4 (no standing worktrees) through the generations lens -- a generation leaves ONLY commits; measured 716 standing trees ~96 GB, 7,971 per-generation session files, a tree-free node write 64 ms, a registration-free slot 1.05 s fresh / 0.69 s recycled / 0.15 s mixed via merge-tree. Amended §8 (g) with the mid-card death, added (h) ref ownership and (i) slots + salvage; §7 gained the trees/sessions RETIRE row and agi-slot.sh in new code. Tree removal is irreversible and waits for the owner's go.
<!-- THOUGHT:END -->
