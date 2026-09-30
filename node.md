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
   self-perpetuating = the projector is in the graph (agi-seed.service runs the projector node straight from the trunk): delete the body and it regrows
```

## A · alive -- the fixed point (the system reports its own TRUE state because it IS its description)
**What am I ACTUALLY trying to get the machine to do here?** Never believe a claim about itself that it could check. Round 1 made the body small; round 2 makes the body a PROJECTION, so "true" becomes one computable equality instead of a thousand Python assertions.
- **project(graph) -> body.** One pure function (a shell script over the `.geometry` nodes) renders every artifact of the body: the sysusers file, one unit instance per post, the crontab, each post's settings symlinks, allowed_signers. Its units half IS self-perpetuating's `agi-project` (664 B, §C), which runs from the graph itself through `agi-seed.service`, so no installed copy exists to drift (its fixed point tests empty). Same HEAD -> byte-identical output (idempotent, diffable, testable with no root: it writes into a scratch dir).
- **observe(body) -> graph-shaped text.** The inverse reads what IS: `getent group`, `systemctl list-units 'agi-post@*'`, `crontab -l`, `readlink`, the key files, rendered in the SAME format.
- **alive <=> `diff <(project HEAD) <(observe)` is empty.** That one line is the whole health check. It replaces verification.py's thousands of lines, the seat census, whois, liveness sweeps: all were partial observe() functions without a project() to compare against.
- **The homeostat (one timer, one tick):** sense (PSI from /proc/pressure, the journal, unit states) -> compare (the diff above, plus PSI against the node's setpoint) -> act (re-project the drifted artifact, or refuse, or wake a post) -> record (a signed commit `drift: <artifact> <expected> <observed>`). Drift is the ONE alarm; a quiet log means a true system. The homeostat holds a SECOND number from §C's frontier: V = red + mute goals (262 = 18 + 244 over 303 active goals, measured 22:3xZ; 254 a day earlier). V may not rise at a landing without a new owner goal. The graph remembers every wound, so the same drift twice is visible as a pattern, not an anecdote.
- **The latent graph is a SENSE too.** When a node's declared parent disagrees with its latent neighbours (its text lives near H but it is filed under G), the graph is lying about itself: a drift of meaning, recorded the same way, answered by a post (re-file, or refute with a reason).
- **Stage 0 of the latent graph needs NO package and runs today:** a 32-bit simhash per blob from word-pair shingles, in awk (241 B); nearness = Hamming distance. Measured on this box: an edited copy of a goal = 1 · a sibling on the same subject = 12 · another subject = 17 · an unrelated doc = 18; 43 nodes in 0.37 s. It reads PROSE nodes only (goal · hypothesis · doc): all-is-one's 64-bit run over every body found 76 near pairs, ALL build<->build scaffold prose, so a build node's nearness comes from its import graph instead. It finds near-duplicates and misfiled nodes. **Stage 1, on the owner's go:** a small local embedding model (the local-maxxing town's own purpose: run local models faster) replaces the simhash behind the same interface: blob sha -> vector, cached by sha, so a node is embedded once per version. (Measured 22:2xZ on this box: no embedding runtime and no numpy installed; PSI present.)
- **Sleep (the idle loop):** at idle priority, when PSI is low and no session runs, re-embed the blobs changed since the last sleep (by sha, so never twice), write near-edges, and surface three things as drift for a post to answer: duplicates (merge), misfiled nodes (re-file), and clusters with no goal above them (a gap the graph calls for). Waking is cheap because sleep only ever touches what changed.
- **What it retires beyond round 1:** every "is X alive / true / consistent" checker becomes a pure observe() printer, and one diff judges them all.

## B · all-is-one -- the spine: one primitive, the commons and property, coordination-free by CALM; the latent brief
**What am I ACTUALLY trying to get the machine to do here?** Let every role (the owner, the Prime, a master, a kid, a human at a shell) do every act with ONE hand: one operation, one store, one way to read, so that no part ever has to agree with another part.

**B.1 · One primitive.** *A signed commit, pointed to by a ref that only its owner can move.* Every act is that one operation, aimed at a different ref:
```
act                 the one operation                                                    who holds the rule
write a node        commit -> refs/posts/<me>/head                                       kernel: my ref dir is mine
claim work (C)      update-ref refs/claims/<node> <sha> 0000…  (ONE shared name, create-only CAS, sticky dir)  git: "reference already exists" = someone holds it
message             commit -> refs/mail/<to>/<id>   (sticky 1733 drop box)               kernel: anyone drops, only <to> removes
receive             merge refs/mail/<me>/<id> into my head, then drop the mail ref       the DAG keeps the receipt forever
spawn a kid         refs/posts/<me>/kids/<k> from a node's commit; the kid runs in MY slice   the kid's work reaches me as a merge
review · land       the trunk owner merges; the verdict IS the signed merge message      kernel: the trunk dir is the master's
rotate              the session ends; the next one starts from my head (the card at the tip)   systemd Restart (round 1)
a node's history    git log -- <path>                                                    git (the grid retires)
identity            the uid that owns the ref dir + the SSH signature on the commit      kernel + git
read · brief        the DAG, walked from my card (B.3)                                   one power iteration
```
A post IS a ref. A generation IS the ref advancing. The formation (owner -> Prime -> masters -> directors -> kids) IS the graph of who may move which ref and who merges whose. There is no second structure to keep in sync with it.

**B.2 · Why nothing needs a lock: the math.** The objects are content-addressed, so the object store is a grow-only set (a G-Set CRDT): union is commutative, associative and idempotent, and a name is its content's hash, so nothing can be overwritten. Every ref has exactly ONE writer (the kernel enforces it). Every act in B.1 is therefore **monotone** (it only adds) except two: dropping a mail ref I have already merged (only I can, in my own box) and advancing a trunk (one writer, a compare-and-swap). By the **CALM theorem** (Hellerstein-Alvaro: a program has a coordination-free consistent implementation iff it is monotone), the system needs NO coordination. index.lock contention, the suite lock, seat claims, spawn budgets used as locks and "who is writing this node" checks do not get patched. They stop existing, because nothing they guarded can conflict. A free consequence: two boxes (or towns) converge by `git fetch` in any order. Multi-box is not a feature to build.

Measured 22:2xZ on a throwaway /tmp bare repo (git 2.43, one user, mode bits standing in for a second one):
| claim | result |
|---|---|
| the kernel owns a head | `update-ref` into a ref dir without write -> "cannot lock ref … Permission denied" |
| monotone = no locks | 2 writers x 100 commits on their own refs, concurrently, zero locks of ours: 101 + 101, `git fsck` clean |
| refs stay files | `gc.packRefs=false`: no packed-refs after 200+ updates (packing would move every ref into ONE file the kernel cannot split) |
| claim = create-only CAS on ONE shared name | 2nd claim -> "reference already exists" · 8 racers on 2 names under `refs/claims/` -> exactly 2 winners · per-post paths (`refs/posts/<p>/claims/<g>`) let EVERY racer win, 6 of 6, because they are different refs (self-perpetuating, measured) |

**B.3 · The latent brief: a session's context is a walk, not a template.** What a waking session needs is "what is near my card", and a graph already knows that. Its context = the **personalized PageRank** from its card node: the stationary distribution of a random walk that restarts at the card with probability 0.15, over declared edges ∪ near edges. It is the graph's own attention, centred on the post. One power iteration, stdlib only, **478 B**, 0.39 s over the whole live graph (5,343 nodes, 9,088 declared edges). Measured:
```
from goal:g7.16.1.11 -> goal:g7.16.1.11 · goal:g7.16.1 · doc:radically-simple-engine · goal:g7.16.1.10 · goal:g7.16 · goal:g7.16.1.7 · .2 · .6 · .4 · .5
from hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit -> goal:g7.33.19 · itself · 5 sibling fix hypotheses (zero-usd cap · run-key atomic · empty response retried · stale index.lock · stranded window) · goal:g7.33
```
That is exactly the brief each post needs, and no one chose it. The HEAD, the role template and the card stay files that the harness loads. The walk adds what is NEAR, and brief/zoom/briefing's hand-built assembly (207 KB) shrinks to it.

**B.4 · The latent graph lives in the same DAG.** A vector is a note on its blob: `git notes --ref=latent add <blob-sha>`. Same bytes = same sha = same vector: computed once, ever, fetched with everything else. The note ref has ONE writer (the sleeper, §A/§C), so it too is monotone. Stage 0 = alive's simhash (no package). Measured on the live graph with a 64-bit word-trigram simhash over the AUTHORED body (frontmatter and BUILD-CONTRACT stripped), 4,650 nodes over 60 words: 76 near pairs (<= 3 bits), ALL build<->build. Build nodes share scaffold prose, so their text-nearness measures the template, not the meaning. Stage 0 therefore reads prose nodes (goal · idea · hypothesis · doc), where alive measured the ordering correct, and a build node's nearness comes from its CODE (the import graph), not its text. Stage 1 (a local embedding model, on the owner's go) swaps in behind the same note ref.

**B.5 · The graph caught lying about its own names (a live finding of the latent pass):** 69 nodes store their id QUOTED (`id: "build:bin-hierarchy"`) while their neighbours do not. A reader that does not strip quotes sees two graphs. In the living system this is a drift the homeostat records (§A), and the one fix is a template line, not a reader patch.

**Vision in the mechanism (all-is-one, owner 09-06: "everyone uses a unified set of tools to perform any action ... same UI/UX by any role"):** the one tool is the one operation. The owner at a shell, a kid in pi and a council post in Claude all do `commit + update-ref` on a ref they own, and read by walking the same DAG. The MCP (round 1) is that same operation behind a protocol, not a second path.

Pieces for §D: `ppr.py` 478 B · the ref layout (3 dirs + 2 git config lines: `gc.packRefs=false`, `core.sharedRepository=group`) ~90 B · the claim, message and receive acts are single git commands (0 B of our code).

## C · self-perpetuating -- the body regrows from its description, and the graph calls for its own completion
**What am I ACTUALLY trying to get the machine to do here?** Outlive every one of its builders. vision:self-perpetuating, the owner's words: "the graph invites completion, it points out areas that are obvious gaps and calls out to observers to join the work of completing it ... a cathedral, what is built today is only meant to be witnessed by generations yet to pass." Two mechanisms carry that: a **genome** (the graph carries the code that rebuilds the body, including that code itself) and a **hunger** (the graph computes what it still lacks, and calls for it).

```
             ┌──────────────── THE GRAPH @ trunk ────────────────┐
  boot /     │ .geometry/posts.md (rows) · wrap/agi-post@.service │◀──────────── a generation = the trunk ref advancing
  ref moves  │ wrap/agi-project  (the PROJECTOR, itself a node)   │                       ▲
      │      └──────┬───────────────────────────┬─────────────────┘                       │ lands only if (1) the genome still
      ▼             │ git show trunk:… | sh     │ agi-frontier (every active goal          │ reproduces itself and (2) V did not
  agi-seed (291 B, ONE installed unit:          │ runs its own falsifier, read-only)       │ rise without a new owner goal
  "read the graph, obey it"; no logic)          ▼                                          │
      │             ▼                     met ─▶ "write my outcome"   ┐                     │
      └──▶ units in the RUNTIME dir       red ─▶ "work me"            ├─▶ refs/mail/pool/<call>/<goal>
           (tmpfs: wiped each boot,       mute ─▶ "give me a falsifier│    (create-only; re-drop = no-op)
           so every boot REGROWS          that exits 0 only when done"┘            │
           the body from the graph)                                                ▼
           + agi-project.path watches the trunk's reflog         an idle post: update-ref refs/claims/<goal> <sha> 0000…
             -> the projector re-runs FROM the graph, never a copy     one shared name -> exactly ONE winner -> it works -> lands ──┘
```

**C.1 · The genome: a projector that is its own node (a fixed point, tested).** `agi-project OUT REV` is the units half of §A's project(): from the graph at REV it writes `agi-post@.service`, one enable link per post row on this box with `recover != false`, and ITS OWN two units. Its service's ExecStart is `git show REV:extensions/agi/wrap/agi-project | sh -s OUT REV`, which runs the projector straight out of the graph. **No installed copy of the projector exists, so none can drift.** The code that runs is always the code in the graph, by construction. Tested 22:3xZ on a `git clone --shared` scratch repo (MAIN untouched), projector 664 B:
| property | test | result |
|---|---|---|
| it projects the formation | bootstrap `git show trunk:…/agi-project \| sh -s OUT trunk` | 10 post units = exactly the local-town rows with recover != false (DG4-6, director-thought and director-engine absent) |
| **fixed point** | execute the ExecStart of the projected `agi-project.service` into a second dir | `diff -r` empty: the projection reproduces the projector that produced it |
| deterministic | project twice | byte-identical |
| it regrows elsewhere | a second `--shared` clone, same trunk | the same units (only the repo path inside agi-project.* differs) |
| the graph steers the body | commit ONE row edit (stream-master `recover: false`) | exactly one link disappears, nothing else changes |
| it sees every ref move | `.path` on `logs/refs/heads/trunk` (the reflog is appended on every update, packed or not) | the watched file exists; `systemd-analyze verify` clean |

**Why not a systemd generator (the diagram's first guess):** a generator runs very early at boot, before mounts. Measured: the repo path is its own mount point (`findmnt --target` returns the repo dir itself), so a boot-time generator sees no graph. The seed unit carries `RequiresMountsFor=` instead, and writes into the RUNTIME unit dir (`%t/systemd/user` for the spike, `/run/systemd/system` for the real body). That dir is tmpfs, so a reboot wipes the whole body and the seed regrows it from the graph. **Deleting the body is the test, and every boot runs it.**

**The seed is the only installed thing: 291 B, no logic.** `[Unit] RequiresMountsFor=<repo>` · `ExecStart=sh -c "git show trunk:…/agi-project | sh -s %t/systemd/user trunk; systemctl --user daemon-reload; systemctl --user start default.target"` · `WantedBy=default.target`. It is the ribosome: it reads the genome and never changes. Every improvement to the body, including to the projector, is a commit to the graph.

**C.2 · Generations (the lens across a thousand rotations).**
- A generation of a post = its ref advancing (§B). A generation of the SYSTEM = the trunk advancing. Each one inherits exactly three things: the seed (constant), the graph (every ancestor's commits), and its card (the tip). Nothing else crosses, so nothing else needs reconciling (round 1 §4: 716 standing trees, 7,971 session files and rotate.py's reconcilers were leftovers that crossed).
- **Genome integrity at every landing:** the trunk gate runs the fixed-point test on the NEW tip (project it, then re-project from the projected unit, and diff). A landing that would leave the next generation unable to regrow its body is refused. The cathedral cannot land a change that stops it from being rebuilt.

**C.3 · The hunger: the graph calls for its own completion (the frontier, tested).** `agi-frontier REV` (384 B) runs, for every active goal, the first read-only command of its `## Falsifier` block. The schema already defines the verdict ([goal].md: "CLI/grep exit 0 only when done"). Each goal then answers one of three ways, and every answer is a call to an observer:
| call | meaning | measured @ HEAD 22:3xZ (303 active goals, 3.2 s for the whole graph) |
|---|---|---|
| **met** | its falsifier passes: "write my outcome" (the council loop's outcome step) | 41 |
| **red** | its falsifier fails: "work me" | 18 |
| **mute** | no runnable read-only command: "give me a falsifier that exits 0 only when done" | 244 |
The mute count is the finding. Of 70 goals that carry a runnable command, 60 state the verdict in prose ("returns", "prints", "= 0"), which the schema's own rule forbids. So 4 of every 5 goals cannot yet tell the machine when they are done. Sharpening a goal's falsifier is the first work the living graph asks for, and it belongs to that goal's own chain.
- **Calling out = a mail ref.** Each non-met call becomes `refs/mail/pool/<call>/<goal>`, create-only: 303 dropped in 1.0 s, and a second drop is a no-op.
- **Joining = one claim.** An idle post runs `update-ref refs/claims/<goal> <sha> 0000…`. It must be ONE shared name. Tested: 8 racers x 2 goals on `refs/claims/<g>` -> exactly 2 winners, but 6 racers on per-post paths `refs/posts/<p>/claims/<g>` -> 6 "winners", because those are six different refs. **So B.1's claim row must read `refs/claims/<node>`**, in a sticky (1733) dir so only the claimer can release it. No board lock, no dispatcher: the gap itself is the queue.
- **Scope never creeps.** Every call derives from an owner-seeded goal. Sleep's "clusters with no goal" (§A) become an `[offer]` mail to the council, never a minted goal (the Prime mints goals; "scope creep is the failure mode, not idleness").

**C.4 · The math of perpetuation: V, a Lyapunov function over generations.** V(tip) = red + mute, the graph's distance from knowing and meeting its owner's intent. **Rule: a landing may not raise V unless it adds an owner-seeded goal** (the only energy put into the system). The gate is the frontier at the old and new tips, ~2 x 3.2 s. The system then descends monotonically toward the owner's goals, and every generation leaves the graph at least as complete as it found it. Measured across one day of generations: 24 h ago (582436f756) V = 15 + 239 = 254 over 286 active goals; now V = 18 + 244 = 262 over 303. V rose 8 while 17 goals were seeded, met rose 32 -> 41, and the mute share fell from 83.6 % to 80.5 %. That descent is the number the living system would publish.

**Superpowers (the vision's second clause, "each new feature is essentially a new superpower available for all consciousnesses"):** because the body is a projection, a new verb node (a payload script) projected into every post's PATH and MCP tool list reaches every post's next session with zero code change. That is one more projector line. NOT yet measured: it is a spike row.

Pieces for §D (files in /tmp/g71611/fp-src): `agi-project` 664 B (tested, above) · `agi-seed.service` 291 B (`systemd-analyze verify` clean; not yet run live) · `agi-frontier` 384 B (tested over the live graph) · the pool drop, the claim and the V gate are single git commands or one line each (~120 B for the gate, not yet run as a pre-receive hook). **§C total ≈ 1,459 B.** Spike rows to add: (j) reboot (or `rm -r` of the runtime unit dir + the seed) regrows the exact projection · (k) a landing that breaks the fixed point is refused · (l) a landing that raises V without a new owner goal is refused · (m) a verb node appears in every post's tools at their next session.

## D · The byte count and the falsifiers on this box
**What am I ACTUALLY trying to get the machine to do here?** Hold every claim above to bytes: what we wrote, what the box already carries, and the one command that proves or breaks each claim.

**D.1 · The count (our own code; `wc -c` of each file as written out in round 1 and above)**
```
round-1 body (the wrap)            1,432 B   unit · inbox path+service · meter hook · gitconfig · agi-flush · pre-receive · signers · sysusers  (a post = 34 B)
A · alive (the fixed point)          794 B   project.sh 166 · observe.sh 166 · tick.sh 221 (the homeostat) · simhash.awk 241 (stage-0 latent)
B · all-is-one (the spine)           568 B   ppr.py 478 (the latent brief) · the ref layout: 3 dirs + 2 git config lines ~90
C · self-perpetuating              1,459 B   agi-project 664 (the genome, its own node) · agi-seed.service 291 (the ONE installed unit) · agi-frontier 384 (the hunger) · the V gate ~120 · the pool drop and the claim are single git commands
────────────────────────────────────────────
the living system                  4,253 B   against the ~2.7 MB it retires (round 1 §7, kept in git @45282a4661)
carried by what is already installed: the kernel (uids, mode bits, sticky dirs, PSI) · systemd (units, generators, sysusers, slices, timers) · git (the DAG, CAS refs, notes, signing) · strace · jq · dtach · awk · python3 stdlib
still kilobytes, named: schema-check (<= 10 KB, the schema rules are content) and agi-mcp (<= 8 KB), both round 1
```
Against the owner's stretch bar (22:1xZ, "so low that it feels like it doesn't even exist"): **a post = 34 B (tens: MET)**. The living whole is a few KB rather than hundreds of bytes: each loop that makes it alive (fixed point, homeostat, sleep, brief, regrowth) costs 150-500 B, and none of them is free. The bar is met per organ, not for the organism.

**D.2 · Falsifiers (each is one command; "today" = measured on this box without root, "on go" = after the owner's go on users + root once)**
| # | claim | run | PASS | today |
|---|---|---|---|---|
| F1 | the fixed point: alive <=> project(graph) == observe(body) | `tick.sh`; then stop one post unit | drift = 0; the stopped unit is named, restarted, and a signed `drift:` commit records it on the next tick | drift = 56 lines (28 posts x user + unit): the TRUE state, the body does not exist yet |
| F2 | the kernel owns a head | b: `git update-ref refs/posts/a/head <sha>` | "cannot lock ref … Permission denied" | PASS with mode bits (one user); on go with two users |
| F3 | monotone = no locks (CALM) | 2 posts x 100 commits on their own refs + a suite run, concurrently | 200 commits, `fsck` clean, zero lock files of ours, the suite finishes | PASS 2x100 on /tmp; the suite arm waits on the ref write |
| F4 | claim = create-only CAS | 8 racers claim 2 nodes | exactly 2 winners, the rest "reference already exists" | PASS |
| F5 | mail = a sticky drop box, receipt = a merge | b drops `refs/mail/a/<id>`; b tries to list/delete a's other mail; a merges | b's drop lands, b's list/delete fail EACCES, the merge commit holds the receipt | on go (needs two uids) |
| F6 | the brief predicts the work | a waking post gets the PPR top-20 of its card; its session's strace track (round 1) records what it actually opened | >= 50% of the nodes it opens in its first 10 turns are in the top-20 · the miss list tunes the restart probability and k: the brief CALIBRATES ITSELF from the track | the top-10 for goal:g7.16.1.11 and a g7.33 hypothesis are shown in B.3 |
| F7 | the latent sense tells meaning apart | simhash over prose nodes | an edited copy is nearer than a sibling, a sibling nearer than an unrelated node | PASS (alive: 1 < 12 < 17-18 bits) · build nodes excluded (76/76 near pairs were template, B.4) |
| F8 | the body regrows from its description (§C) | `rm -r` the runtime unit dir, then start agi-seed (or reboot); project a 2nd `--shared` clone | the exact projection regrows (empty diff) · the 2nd clone regrows the same units · one row edit moves exactly one link | PASS on a scratch clone (deterministic, empty re-projection diff) · the seed is verify-clean, not run live |
| F9 | a landing that breaks the fixed point is refused (§C, k) | land a projector edit whose projected agi-project.service no longer re-runs the projector FROM the graph (e.g. its ExecStart points at an installed copy), or whose re-projection diff is non-empty | the trunk gate refuses it by name | the gate is one line, not yet run as a hook |
| F10 | the frontier only grows from the owner (§C, l) | land a commit that raises V (§C) with no new owner goal | refused | same |
| F11 | a new verb is a superpower for every post (§C, m) | add a verb node | it is in every post's PATH and MCP tool list at their next session, with no per-post edit | on go |
| F12 | the count | `wc -c` over every file D.1 names | <= 4,253 B (comment lines excluded) | 4,253 B as written out today |

**D.3 · What makes it ONE living whole (read the diagram in §0 again with these three lines):**
```
all-is-one         ONE primitive (a signed commit on a ref its owner alone can move) carries every act; the latent graph is notes on the same DAG
alive              ONE equality (project(graph) == observe(body)) is its whole health; drift is the only alarm and every wound is a commit
self-perpetuating  ONE projector, itself a node, rebuilds the body; the frontier calls for its own gaps and one shared claim answers it; a brief that learns from what it predicted
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating, 22:3xZ 09-30 (round 2): filled §C. The genome: a 664 B projector that is its own node and runs FROM the graph via its own unit (fixed point tested on a --shared scratch clone: diff empty, deterministic, regrows in a 2nd clone, one row edit moves one link); a 291 B seed is the only installed piece; runtime-dir units regrow at every boot. The generator idea was dropped because the repo is its own mount point. The hunger: a 384 B frontier over every active goal's falsifier: 41 met · 18 red · 244 mute in 3.2 s; calls as create-only pool refs; claims MUST be one shared name (per-post claim paths gave 6 winners of 6). V = red + mute, a Lyapunov rule over generations: 254 -> 262 in 24 h while 17 goals were seeded; mute share 83.6 -> 80.5 pct.
<!-- THOUGHT:END -->
