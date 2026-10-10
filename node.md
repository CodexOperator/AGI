---
id: doc:radically-simple-engine
mint_id: ad68a997a9274ca6a13490561478b768
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: self-perpetuating
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

**ROUND 3** (owner 23:0xZ-23:1xZ, verbatim on goal:g7.16.1.11): §F the shape test · §G links = symlinks, the brief = one complex multiplication · §H the brief injected by the harness at every start, the graph current with no second path · §I **the engine itself = ONE layered `.geometry` node**, `config:engine`, readable in one read. Round 2 stays in git @9d4076f96a.

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
   SESSION (any harness) ──start · resume · compact──▶ agi-brief: b = α Σ((1-α)Pθ)^k e, e = card + own claims ──▶ its context, before the first token
      └─▶ plain paths in its OWN checkout ──turn end──▶ one signed commit on its own ref ──▶ the master merges ──▶ re-project ──▶ the next brief
   transparent       = the harness injects the brief and commits every turn: no agent calls an agi tool; the engine is ONE node (§I), read in one read
   vectors (r4)      = a POINTER is a directory of symlinks (§M) · a LAUNCH is one row of cells, post | kid | workflow alike (§L) · a PANE is two files, i + o (§N)
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
claim work (C)      update-ref refs/claims/<mint> <sha> 0000…  (ONE shared name, keyed by MINT: a colon is illegal in a ref, create-only CAS, sticky dir)  git: "reference already exists" = someone holds it
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
           + agi-project.path watches the trunk's reflog         an idle post: update-ref refs/claims/<goal-mint> <sha> 0000…
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

**C.3 · The hunger: the graph calls for its own completion (the frontier, tested).** `agi-frontier REV` (450 B, round-3 version) runs, for every active goal (found by TYPE over real files, so it reads the same before and after §G's symlink layout), the first read-only command of its `## Falsifier` block. The schema already defines the verdict ([goal].md: "CLI/grep exit 0 only when done"). Each goal then answers one of three ways, and every answer is a call to an observer:
| call | meaning | measured @ HEAD 23:1xZ (312 active goals, ~3 s for the whole graph) |
|---|---|---|
| **met** | its falsifier passes: "write my outcome" (the council loop's outcome step) | 41 |
| **red** | its falsifier fails: "work me" | 19 |
| **mute** | no runnable read-only command: "give me a falsifier that exits 0 only when done" | 252 |
The mute count is the finding. Of 70 goals that carry a runnable command, 60 state the verdict in prose ("returns", "prints", "= 0"), which the schema's own rule forbids. So 4 of every 5 goals cannot yet tell the machine when they are done. Sharpening a goal's falsifier is the first work the living graph asks for, and it belongs to that goal's own chain.
- **Calling out = a mail ref.** Each non-met call becomes `refs/mail/pool/<call>/<goal>`, create-only: 303 dropped in 1.0 s (measured before the stdin fix below), and a second drop is a no-op.
- **Joining = one claim.** An idle post runs `update-ref refs/claims/<goal-mint> <sha> 0000…`. It must be ONE shared name. Tested: 8 racers x 2 goals on `refs/claims/<g>` -> exactly 2 winners, but 6 racers on per-post paths `refs/posts/<p>/claims/<g>` -> 6 "winners", because those are six different refs. **So B.1's claim row must read `refs/claims/<mint>`** (one shared name; the mint, since `git check-ref-format` refuses the colon of an address, §H.2), in a sticky (1733) dir so only the claimer can release it. No board lock, no dispatcher: the gap itself is the queue.
- **Scope never creeps.** Every call derives from an owner-seeded goal. Sleep's "clusters with no goal" (§A) become an `[offer]` mail to the council, never a minted goal (the Prime mints goals; "scope creep is the failure mode, not idleness").

**C.4 · The math of perpetuation: V, a Lyapunov function over generations.** V(tip) = red + mute, the graph's distance from knowing and meeting its owner's intent. **Rule: a landing may not raise V unless it adds an owner-seeded goal** (the only energy put into the system). The gate is the frontier at the old and new tips, ~2 x 3.2 s. The system then descends monotonically toward the owner's goals, and every generation leaves the graph at least as complete as it found it. Measured across one day of generations (CORRECTED in round 3: the round-2 frontier ran each falsifier with the loop's stdin, so a command that read stdin swallowed goal lines and 9 of 312 were never read; the fix is `</dev/null`): 24 h ago (582436f756) V = 16 + 250 = 266 over 298 active goals; now V = 19 + 252 = 271 over 312. V rose 5 while 14 goals were seeded, met rose 32 -> 41, and the mute share fell from 83.9 % to 80.8 %. That descent is the number the living system would publish.

**Superpowers (the vision's second clause, "each new feature is essentially a new superpower available for all consciousnesses"):** because the body is a projection, a new verb node (a payload script) projected into every post's PATH and MCP tool list reaches every post's next session with zero code change. That is one more projector line. NOT yet measured: it is a spike row.

Pieces for §D (files in /tmp/g71611/fp-src): `agi-project` 664 B (tested, above) · `agi-seed.service` 291 B (`systemd-analyze verify` clean; not yet run live) · `agi-frontier` 450 B (round 3: stdin fix + type-scoped, tested over the live graph) · the pool drop, the claim and the V gate are single git commands or one line each (~120 B for the gate, not yet run as a pre-receive hook). **§C total ≈ 1,525 B.** Spike rows to add: (j) reboot (or `rm -r` of the runtime unit dir + the seed) regrows the exact projection · (k) a landing that breaks the fixed point is refused · (l) a landing that raises V without a new owner goal is refused · (m) a verb node appears in every post's tools at their next session.

## D · The byte count and the falsifiers on this box
**What am I ACTUALLY trying to get the machine to do here?** Hold every claim above to bytes: what we wrote, what the box already carries, and the one command that proves or breaks each claim.

**D.1 · The count (our own code, comment lines excluded, re-summed in round 3 from the files in §I)**
```
round-1 body (the wrap)            1,532 B   unit 340 (the card left its argv) · inbox path 37 + service 69 · settings.json 458 (meter + SessionStart + Stop) · gitconfig 79 · agi-flush 115 · pre-receive 345 · signers 55 · sysusers 34
A · alive (the fixed point)        1,031 B   project.sh 272 (reads through the links, + the brief line) · observe.sh 307 (+ the brief line) · tick.sh 211 · simhash.awk 241
B · all-is-one (the spine)           562 B   brief.py 562 (§G's 520 + multi-seed 42; retires ppr.py 478) · + the ref layout, 3 dirs + 2 git config lines ~90, inline
C · self-perpetuating              1,828 B   agi-project 931 (reads every piece FROM the engine node, blob or nothing) · agi-seed.service 447 (reloads only over >= 1 post unit) · agi-frontier 450 · + the V gate ~120, inline
H · alive (injection)              1,076 B   agi-brief 565 (claims = the ref files it owns) · agi.ts 372 (pi) · sect 139 (the narrowed read)
────────────────────────────────────────────
the living system                  6,029 B   in files (+ ~210 B inline one-liners) against the ~2.7 MB it retires (round 1 §7, kept in git @45282a4661)
the engine node (§I)              11,305 B   body: diagram + loop + one line per piece + all 20 files whole; depth 0+1 = 3,806 B, one page
carried by what is already installed: the kernel (uids, mode bits, sticky dirs, PSI) · systemd (units, sysusers, slices, timers) · git (the DAG, CAS refs, notes, signing, cat-file --follow-symlinks) · strace · jq · dtach · awk · sed · python3 stdlib · the harnesses' own start and turn-end hooks
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
| F6 | the brief predicts the work | a waking post gets the PPR top-20 of its card; its session's strace track (round 1) records what it actually opened | >= 50% of the nodes it opens in its first 10 turns are in the top-20 · the miss list tunes the restart probability and k: the brief CALIBRATES ITSELF from the track | the top-10 for goal:g7.16.1.11 and a g7.33 hypothesis are shown in B.3 · the seed MUST carry the post's claims: card alone ties the live goal with 8 siblings, card + claim puts it at rank 2 (~9x, §H.3) |
| F7 | the latent sense tells meaning apart | simhash over prose nodes | an edited copy is nearer than a sibling, a sibling nearer than an unrelated node | PASS (alive: 1 < 12 < 17-18 bits) · build nodes excluded (76/76 near pairs were template, B.4) |
| F8 | the body regrows from its description (§C) | `rm -r` the runtime unit dir, then start agi-seed (or reboot); project a 2nd `--shared` clone | the exact projection regrows (empty diff) · the 2nd clone regrows the same units · one row edit moves exactly one link | PASS on a scratch clone (deterministic, empty re-projection diff) · the seed is verify-clean, not run live |
| F9 | a landing that breaks the fixed point is refused (§C, k) | land a projector edit whose projection is EMPTY (0 post units: a reader regression, e.g. §G's symlink read at a REV), or whose projected agi-project.service no longer re-runs the projector FROM the graph (e.g. its ExecStart points at an installed copy), or whose re-projection diff is non-empty | the trunk gate refuses it by name | the gate is one line, not yet run as a hook |
| F10 | the frontier only grows from the owner (§C, l) | land a commit that raises V (§C) with no new owner goal | refused | same |
| F11 | a new verb is a superpower for every post (§C, m) | add a verb node | it is in every post's PATH and MCP tool list at their next session, with no per-post edit | on go |
| F12 | the count | `wc -c` over every file D.1 names, comment lines excluded | <= 6,029 B in files | 6,029 B (§I's files, round 3) |
| F13-F16 | the shape test and the at-REV reader | §F's spike rows and F.7 | as stated there · RE-SCOPED for the one engine node (s-p, 23:3xZ): the page bar (F13) holds for config:engine's depth 0+1 (F21) and for every OTHER .geometry node; config:engine carries one ~~~ block per piece (F15), cut by `sect` | F14 PASS on the node itself through links (§H.5) |
| L1-L3 | links are symlinks | §G | `find .agi -xtype l` = 0 after migration · a `git mv` of one address keeps it 0 · phase = level difference | 25-27 dangling today on the scratch projections (§G) |
| F17 | the brief is injected at EVERY start, by the harness | CC: `claude -p --settings <scratch>` at startup, `--resume`, and after `/compact`, each asked for its brief's first vector line · pi: the closed-port probe (§H.3) · the body: observe prints `brief agi-<post>` for every post | the vector line in all three CC legs · in every pi payload, fresh and resumed, exactly once · 0 drift lines of kind brief | pi PASS (fresh + resume) · CC on the owner's go (paid) · the body: 84 expected, 0 observed (TRUE: nothing is registered, §H.1) |
| F18 | the graph stays current with no second path | a session writes a node with plain `cat >` and ends its turn | its OWN ref gains exactly one signed commit holding it; the strace track shows no agi tool ran | PASS on pi (unsigned in the test; the key is round 1's gitconfig) |
| F19 | a read narrows to one section by name, byte-exact | `sect <name> REV` for every section and piece of `config:engine` | byte-identical to the source file (`cmp`) at any REV, through an address symlink | 20 of 20 on the scratch clone, plain and linked |
| F20 | the brief follows the work | claim a node (`update-ref refs/claims/<mint>`), start a session; release it, start again | the node is in the top-3 with the claim, back at its sibling weight without it | rank 2 with the claim, 0.015 (sibling weight) without (§H.3) |
| F21 | the engine is one read | `wc -c` of `config:engine`: depth 0+1 · the code counted · the whole | <= 4,096 · <= 8,192 · <= 12,288 B | 3,806 · 6,029 · 11,305 B (body) |
| F22 | a post's claims are never silently lost | `git config remote.origin.url` in every post checkout the projector clones | a plain filesystem path (the claim line reads `<origin>/refs/claims`; a `file://` URL makes it print nothing, silently: all-is-one, measured) | holds by construction while the projector clones by path (`clone --shared <path>`); a ~12 B `${u#file://}` guard is the fallback if a URL ever appears |

**D.3 · What makes it ONE living whole (read the diagram in §0 again with these three lines):**
```
all-is-one         ONE primitive (a signed commit on a ref its owner alone can move) carries every act; the latent graph is notes on the same DAG
alive              ONE equality (project(graph) == observe(body)) is its whole health; drift is the only alarm and every wound is a commit
self-perpetuating  ONE projector, itself a node, rebuilds the body; the frontier calls for its own gaps and one shared claim answers it; a brief that learns from what it predicted
```

## E · The files, whole -> §I
Round 3 moves every file into ONE node (the owner's 23:10Z order), so §I holds them, whole, with the one line of WHY each. The round-2 files as they were are in git: `git show 9d4076f96a:.agi/nodes/doc/radically-simple-engine.md` (§E there). What changed in each file is named in D.1.

## F · ROUND 3 · self-perpetuating -- the shape test: the genome is `.geometry`, one page per piece
**Owner 23:0xZ (verbatim on the goal):** ".geometry could about contain all the graph build nodes. And if it doesn't fit as a .geometry node it's not radically simple enough yet." **What am I ACTUALLY trying to get the machine to do here?** Hand every future generation the WHOLE machine in a form it can read whole: every piece of the engine is one `.geometry` node, and the projector (§C) grows the body from those nodes and nothing else.

**F.1 · The bar, read from the box, not chosen: one page = 4,096 B** (`getconf PAGESIZE`; brief.md, the median `.geometry` node, is exactly 4,096 B today). A node that fits one page is read whole by every successor, in one read. A node that does not is read in parts, and a successor acting on part of a rule is where drift starts. That is the generations reason for the owner's test.

**F.2 · The node shape (one extractor for every piece):**
```
---                      frontmatter = the machine CELLS (rows, setpoints, schedules)
id: config:<piece>
---
# config:<piece>
<one line: what this piece ACTUALLY makes the machine do>
~~~sh                    at most ONE fenced block = the piece's code; TILDE fences, so a node is backtick-free
...                      (backticks inside a unit's sh -c "..." are command substitution: measured, it broke the self-run)
~~~
extract any piece:  r REV .agi/nodes/.geometry/<piece>.md | sed -n '/^~~~/,/^~~~/{//!p}'      (r = the ONE at-REV reader, F.7)
```
There is no payload file, no build node beside it, no BUILD-CONTRACT and no grid ref of its own: **the node IS the file**, and its history is `git log -- <node>`.

**F.3 · Tested 23:0xZ: the genome runs FROM `.geometry` nodes** (the `--shared` scratch clone, MAIN untouched). Three nodes: `config:agi-project` (871 B, the projector as a `~~~sh` block of 681 B) · `config:agi-post` (503 B, the round-1 unit as `~~~ini`) · `config:posts` (the rows as `~~~json`, one per line, the identity cells dropped per round 1 §1).
| test | result |
|---|---|
| bootstrap: extract the projector from its node and run it | 10 post units (the local-town rows with recover != false) + its own .path/.service |
| **fixed point**: run the projected unit's ExecStart, which extracts the projector from its node again | `diff -r` empty: the node reproduces itself |
| the unit template is extracted byte-exact | `cmp` equal |
| `systemd-analyze verify` on the projected units | clean |
Two traps paid for in the test and fixed in the node: backtick fences inside `sh -c "..."` (-> tilde fences) · `\x27` is not POSIX printf (dash printed it raw -> octal `\047`).

**F.4 · The shape test over today's `.geometry` (18 files, 327,060 B): 6 fit, 12 do not, and the overflow is almost all PROSE:**
| node | bytes | machine cells | prose body | fits? | verdict |
|---|---|---|---|---|---|
| commands.md | 115,841 | 110,222 | 5,619 | NO | the argv registry of tools this design retires; each SURVIVING verb becomes its own node (F11: the verb is the superpower), the rest retire with their tools |
| posts.md | 103,041 | 86,449 | 16,592 | NO | 28 rows keep 10 cells (name · role · town · box · harness · model · effort · recover · owning_goal · template): local-town 2,861 B + core-town 2,076 B -> **one node per town, each fits** |
| rotations.md | 21,374 | 13,295 | 8,079 | NO | RETIRE: a rotation is a unit restart (round 1); its first-turn texts become the injected brief (part 3, alive) |
| formations/council-loop · texas-two-step · formation-local-town | 11,194 · 9,661 · 4,456 | 213 · 438 · 586 | the rest | NO | prose role documents: move to `doc:` nodes; the formation's MACHINE part is who may move / merge which ref (§B), one small table |
| ladder · crons · workflows · secrets | 10,670 · 9,370 · 6,803 · 7,125 | 3,070 · 2,411 · 2,153 · 1,277 | the rest | NO -> YES | cells fit a page once the prose leaves; crons become timers the projector writes |
| guard.md | 9,845 | 279 | 9,566 | NO -> YES | 279 B of cells survive (slice setpoints); the prose leaves |
| towns/core.md | 5,499 | 411 | 5,088 | NO -> YES | prose leaves |
| brief · links · key-authority · vetoes · census · formations.md | 4,096 · 2,205 · 2,000 · 1,670 · 1,623 · 587 | | | YES | stay |
**The rule the test implies:** `.geometry` holds cells and at most one code block per node. Prose goes to `doc:` nodes and role docs (the owner's 09-24 order: "Notes go into templates or configs, then individual role docs, then town board node").

**F.5 · Does `.geometry` about contain the whole engine? Yes, at about a tenth of its size today:**
```
every round-1 and round-2 piece, code, one node each            4,253 B   largest: config:agi-project 871 B as a node (< 1 page)
the surviving cells (ladder · crons · workflows · secrets · guard)  9,190 B   frontmatter bytes, measured
posts, one node per town                                          ~5,000 B  2,861 + 2,076 of rows + headers
the six nodes that already fit                                   12,181 B
────────────────────────────────────────────────────────────────
the WHOLE engine as .geometry                                   ~31 KB    vs 327 KB of .geometry today, and 6.09 MB of engine source (288 files, 122 of them <= 1 page)
```
- **What still fails the test is named, not hidden:** schema-check (<= 10 KB) and agi-mcp (<= 8 KB), both from round 1, are 2-3 pages each. Shape verdict: agi-mcp becomes ONE page that lists the verb nodes as its tools (the tool list is a projection, F11), and schema-check becomes one node per type whose cells ARE the `[<type>].md` required list. Neither is measured yet: they are the two pieces that are "not radically simple enough yet".
- **The 293 build nodes:** a piece that moves into `.geometry` retires its build node and its file together (retire = move, never delete). Test code does not move: each piece's falsifier (§D) is its test.

**F.6 · The generations lens:** the genome is now a set of pages that a successor can read in full: ~31 KB, about 8 pages, the whole machine. Every future improvement is an edit to one page. §C's gates (the fixed point and V) guard every edit, so no generation can land a page that stops the next one from regrowing the body.

**F.7 · The at-REV read rule (a RED found in round 3, fixed before any build).** Under §G's layout an address is a symlink, and `git show REV:<address>` returns the LINK TEXT, not the node (tested: it printed `../n/abc123/node.md`). Every reader that works at a REV without a checkout would then read nothing, silently: the projector, project.sh, the seed, and a path-scoped frontier. The fixed point would PASS on two EMPTY projections, and V would read 0, so the V gate would always pass. The rule: **every at-REV read goes through ONE reader**, which git already carries (all-is-one found it; hardened here so a broken link fails loud):
```sh
r(){ echo "$1:$2"|git cat-file --batch --follow-symlinks|{ read o t s;[ "$t" = blob ]&&head -c $s;};}      # 101 B
```
Tested on a throwaway repo: an address resolves to the node's exact bytes and the genome inside it runs · a DANGLING address -> exit 1 · a missing path -> exit 1. The unhardened form printed the path text with exit 0, the same silent class. Content search is the other read: `git grep` does not follow symlinks (0 hits via addresses, 1 via real files, tested), so the frontier searches real files by TYPE (`--all-match -e '^type: goal$' -e '^status: active$' -- .agi`), which gives 312 today, the same as the path-scoped count. **And every projection must be NON-EMPTY** (>= 1 post unit), or the gate refuses: that catches any future reader regression, whatever its cause.

Spike rows for §D: **F13** every `.geometry` node <= 4,096 B, measured through the links (`find -L .agi/nodes/.geometry -size +4096c` prints nothing) AND no link dangles (`find .agi -xtype l` prints nothing) · **F14** the fixed point holds with the projector extracted from its `.geometry` node through `r`, and the projection is non-empty (PASS today on the scratch clone, before the symlink layout) · **F15** each `.geometry` node carries at most one fenced block, and every block extracts and runs (`sh -n` / `systemd-analyze verify` / `jq -e .`) · **F16** `r HEAD <address>` equals `cat` of the real file for every node, and exits non-zero on a dangling link.

## G · ROUND 3 · all-is-one -- links are symlinks, the brief is one complex multiplication applied to the post
**What am I ACTUALLY trying to get the machine to do here?** Make "A links to B" a fact the FILESYSTEM holds, so that every tool (ls, readlink, find, git, an editor, a kid, the owner) reads the same graph with no parser. Then make "what should this post see now" one multiplication applied to the post.

**Links = symlinks: the two-identifiers rule becomes the filesystem.**
```
.agi/n/<mint>/node.md                         the REAL file; the mint id never changes, so this path never moves
.agi/n/<mint>/p/<parent-address> -> ../../<parent-mint>    a parent = a relative symlink in the node's OWN dir (written at mint, by its owner)
.agi/n/<mint>/near/<address>     -> ../../<mint2>          a latent edge = the same thing, written by the sleeper (§A), one writer
.agi/nodes/<type>/<slug>.md -> ../../n/<mint>/node.md     the ADDRESS: every path agents use today keeps working (transparent)
children: DERIVED, never stored (the reverse of p/): nobody writes into another post's dir, the kernel rule of §B holds
```
| act | today | as symlinks | our code |
|---|---|---|---|
| the broken-link check | links.py, 43 KB | `find .agi -xtype l` | 0 B |
| walk the graph | frontmatter parsers in write.py · links.py · viewport | `ls`, `readlink`, `find -L` | 0 B |
| rename an address | re-point every reference in ONE commit (CLAUDE.md, goal renumbering) | move ONE symlink; every link targets the mint, so none moves | 0 B |
| a duplicate parent | possible (a list in YAML) | impossible (one name per dir entry) | 0 B |
| a parent's history | the grid | git versions a symlink as a 120000 blob holding its target | 0 B |
The frontmatter `parents:` list retires into `p/` (one source). The schema gate reads `ls p/` instead of parsing YAML.

**Measured 22:5xZ: the live graph projected into this layout on a /tmp scratch copy** (a 1 KB throwaway migration script, not engine code): 5,588 nodes (live + retired + .geometry) · 9,496 parent symlinks · 1.6 s. What the projection exposed that the current machinery passes quietly:
- **[CORRECTED in §M.0: a scratch-parser artifact; parents-only = 0]** 193 duplicate parent entries in frontmatter (e.g. a verdict listing the same experiment twice). Symlinks cannot express them.
- **[CORRECTED in §M.0: parents-only = 0 broken; parked:g7.16.2 is a TAG]** 27 links `find -xtype l` calls broken, while links.py reports 0 broken: 13 parents written as `parked:g7.16.2` (the node is `goal:g7.16.2` today) · about 8 address drifts (a link kept `build:a00-fcfbc2f9-bin-adapters-grok-bot-adapter` while the node's id became `build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9`; `exp:…` vs `hyp:…`) · about 6 artifacts of the scratch parser (other frontmatter lists). A link that targets the MINT id cannot go stale when an address changes. That is why the owner's two-identifiers rule belongs in the filesystem and not in a resolver.

**The brief = one multiplication applied to the post (the owner: "a dot product or a multiplication applied to the post").** Let `e` be the post's card as a unit vector and `P` the walk matrix read straight off the symlinks. The brief is

  `b = α · Σ_k ((1-α) · Pθ)^k · e`   (α = 0.15: personalized PageRank, 30 terms)

and `Pθ` carries the owner's complex plane (22:48Z: "multiply by reals and it's a scale, and multiply by imaginary and it's a rotation"): every step UP a parent symlink multiplies by `e^{iθ}`, every step DOWN by `e^{-iθ}`, and a latent `near/` edge by a real 1. (This is the magnetic, or Hermitian, adjacency of a directed graph, a known object; θ = 0.5 rad.) So every node's brief score is ONE complex number: **its magnitude says how near it is, its phase how far up or down.** Measured on the symlink projection, 520 B, stdlib only, 0.58 s over the whole graph:
```
from goal:g7.16.1.11                          from hypothesis:g73360-a-workflow-stage-stops-its-own-scope-on-exit
|b|    arg/θ  node                            |b|    arg/θ  node
0.247  -0.0   goal:g7.16.1.11 (itself)        0.218  +1.0   goal:g7.33.19 (parent)
0.199  +1.0   goal:g7.16.1    (parent)        0.165  -0.0   itself
0.105  -1.0   doc:radically-simple-engine     0.030  -0.0   5 sibling fix hypotheses (0.020-0.030, all phase 0)
0.015  +2.0   goal:g7.16      (grandparent)   0.023  +1.9   goal:g7.33
0.011-0.016 0 the 8 sibling goals
```
The phase reads the hierarchy exactly (parent +1, grandparent +2, child -1, siblings 0), with no level field stored anywhere. And it does one more thing no real-valued brief can: **interference.** `goal:g7.33` lands at +1.9, not +2, because paths reach it at two depths: as the grandparent through g7.33.19, and as the DIRECT parent of some sibling hypotheses. Where paths disagree about a node's level, their phases partly cancel. A fractional phase, or a magnitude drop against the real-valued walk, is how the graph says "I am filed inconsistently here". It is the true-state sense of §A, computed as a side effect of the brief.

Pieces for the count: `brief.py` 520 B (replaces ppr.py's 478 B from round 2) · the links: 0 B (the kernel and git) · the migration projection ~1 KB, run once, not engine code.
Falsifiers to add: (L1) `find .agi -xtype l | wc -l` = 0 after the migration, with the 27 above re-pointed at their mints first · (L2) renaming an address with `git mv` of ONE symlink leaves `find -xtype l` at 0 and every parent link unchanged · (L3) the brief's phase equals the level difference for every node reached by level-consistent paths, and a planted double-filing shows a fractional phase.

`brief.py` whole (520 B; run: `python3 brief.py .agi/n <card-mint> <k>`; prints |b|, the phase in levels, and the mint):
```python
import os,sys,cmath
R,s,k=sys.argv[1],sys.argv[2],int(sys.argv[3]);q=cmath.exp(.5j)
A={}
for m in os.listdir(R):
 for p in os.listdir(f'{R}/{m}/p'):
  t=os.readlink(f'{R}/{m}/p/{p}')[6:]
  if os.path.isdir(f'{R}/{t}'):A.setdefault(m,[]).append((t,q));A.setdefault(t,[]).append((m,1/q))
x={s:1};b={}
for _ in range(30):
 y={s:.15}
 for u,v in x.items():
  for w,z in A.get(u,()):y[w]=y.get(w,0)+.85*v*z/len(A[u])
 x=y
for m in sorted(x,key=lambda m:-abs(x[m]))[:k]:print(f'{abs(x[m]):.3f} {cmath.phase(x[m])/.5:+.1f}',m)
```

## H · ROUND 3 · alive -- the brief is injected by the harness at every start, and the graph stays current with no second path
**What am I ACTUALLY trying to get the machine to do here?** Every session, at start, resume and compact, sees the graph around its work before its first token, without choosing to look. Every act it takes lands in the graph without a special tool. Nothing is left to the model's memory or goodwill.
```
post unit starts · the session resumes · the context compacts
  │ Claude Code: SessionStart, NO matcher = startup · resume · clear · compact     pi: session_start (startup · reload · new · resume · fork)
  ▼
agi-brief   e = the card + every refs/claims/<mint> whose ref FILE this post owns ──▶  brief.py (§G): b = α Σ ((1-α) Pθ)^k e
  │         prints the vector (|b| · levels up · address · path), then whole nodes by |b| up to B bytes (K, B = cells)
  │ Claude Code: hook stdout = the context, re-emitted after every compact
  │ pi: before_agent_start appends it to the SYSTEM prompt every turn (never in the transcript: compaction has nothing of it to drop)
  ▼
the agent reads and writes PLAIN PATHS in its own checkout ~/t (cat · ls · an editor · git): no write.py, no send.py, no brief.py call
  │ reads  -> the strace track (round 1) -> F6 tunes α and K from what it actually opened
  │ writes -> turn end (CC Stop · pi turn_end): git add -A; git commit on its OWN ref, signed by gitconfig: one commit per turn
  ▼
many writers, one per ref (§B.2 CALM, owner 23:1xZ) -> the master merges the post refs -> trunk moves -> agi-project re-projects -> the next brief sees it
```

**H.1 · The true state today (measured 23:1xZ): the description promises an injection the body does not do.**
| harness | what CLAUDE.md / the code says | what the box does |
|---|---|---|
| Claude Code | "the SessionStart hook -> extensions/agi/hooks/cc-session-start.sh" is a global handle | `~/.claude/settings.json` registers ONLY UserPromptSubmit (the meter). The 09-23 settings backup had no hooks at all. No plugin carries it. The 8.9 KB hook never runs, and it never reads its stdin, so it could not tell a startup from a compact anyway. |
| pi | agi-bridge (5,162 B) injects the map on `before_agent_start` | never loaded: no `~/.pi/agent/extensions/`, and no dispatch passes `-e`. Were it loaded, it finds no project: it looks for `agi-tree.config.json` and `<root>/context/INJECTION.md`, while the live marker is `.agi/config.json` and the file is `.agi/context/INJECTION.md`. |
| both | a successor "wakes knowing its state" | every brief a post gets today is TYPED into its pane by rotate.py as its first prompt. A resume or a compact re-injects nothing. |
This is the drift §A exists to catch, so the body now carries it. project.sh emits `brief agi-<post>` for every post row, and observe.sh prints that line only when the post's own settings carry a SessionStart hook. Today: 84 lines expected (28 posts x user · unit · brief), 0 observed. That is the true state: the body does not exist yet.

**H.2 · The pieces (templates over raw commands: LIGHT, per the owner's 23:0xZ clarification).**
- `agi-brief` 565 B: one template. Its parameters are K (20) and B (40,000 B), both cells. The card is found by its ADDRESS (`readlink -f`), so the brief follows a renamed card for free.
- the Claude Code half = two entries added to round 1's per-post settings file (`meter.json` becomes `settings.json`, 458 B): `SessionStart -> agi-brief` and `Stop -> git add -A; git commit`.
- the pi half = `agi.ts` 372 B: `session_start` computes the brief once, `before_agent_start` appends it to the system prompt, and `turn_end`/`agent_end` commit. It is projected as a symlink into the post's `~/.pi/agent/extensions/`, the directory pi auto-discovers (read from pi 0.67.68's dist: `join(agentDir, "extensions")`).
- the post unit drops the card from its argv (`sh -c '${H} go'`, -33 B): the harness now carries the brief, so the unit no longer has to.
- `brief.py` 562 B = §G's 520 B + multi-seed (+42 B: argv 2 is a comma list, and the restart mass is split evenly). all-is-one's line: "a claim made = the brief moves; a claim released = it moves back".
- **A claim is this post's when the kernel says so** (all-is-one's red, 23:3xZ): the brief once read `%(authorname)` of the commit a claim ref points at, but a claim may point at ANY commit (tested: a claim on another's commit vanished from the brief), and `~/t` holds only the claims it has fetched. Now: `find <shared repo>/refs/claims -type f -user agi-<post> ! -name '*.lock'`, the shared repo found as the checkout's `origin` (no new cell). The ref FILE's owner is its creator (loose refs: `gc.packRefs=false`, §B.2). Tested on a scratch bare repo: the owner's claim is listed, the `claims` dir itself and a racing `.lock` are not.
- **Claims are keyed by MINT.** `git check-ref-format refs/claims/goal:g7.16.1.11` = rc 1 (a colon is illegal in a ref name); `refs/claims/<mint>` = rc 0. So B.1's and C.3's claim rows now read `<mint>`. Every pointer targets the mint, the same rule the links follow (all-is-one agreed).

**H.3 · Measured (pi 0.67.68 · the §G layout projected from the live graph on /tmp: 5,595 nodes, 9,272 parent links, 25 `-xtype l`).**
| test | result |
|---|---|
| pi FRESH: a scratch agent dir whose ONE provider is a closed local port (no byte leaves the box); a probe on `before_provider_request` reads the real payload | `session_start` = startup; the brief is in 4 of 4 request payloads (pi's retries) |
| pi RESUME (`-c`, the same session file) | the brief is recomputed (new stamp) and appears exactly ONCE in 4 of 4 payloads; the session file holds both prompts and 0 copies of the brief |
| pi TURN END: a file written with plain `cat` before the turn | one new commit holding exactly that file, message = the post's user; no agi tool ran |
| agi-brief over the projection (alive's card) | 0.42 s; 41.6 KB = the 20-line vector + whole nodes up to B |
| seed = the card alone | goal:g7.16.1.11 (the live assignment) is at 0.015, tied with its 8 siblings; the doc being written is NOT in the top-20 |
| seed = the card + a claim on g7.16.1.11's mint | g7.16.1.11 is rank 2 (0.131, ~9x), the doc rank 4 (0.056, phase -1); a claim whose ref file another post owns is not a seed |
| Claude Code | model-free proof covers the REGISTRATION only (observe's jq line). The live leg (`claude -p --settings <scratch>` at startup, `--resume`, and after `/compact`) is paid, so it waits for the owner's go (free lane only since 21:00Z) |

**H.4 · Transparency: why no second path is needed.** An agent only reads and writes files. Three events the harnesses already fire turn that into the graph: start (the brief comes in), turn end (a commit goes out), and exit (round 1's agi-flush merges and pushes). Many writers is safe by construction: each post commits to its OWN ref in its OWN checkout, and the master stages the merges (owner 23:1xZ). Every act is monotone, so nothing locks (§B.2). What an agent must know shrinks to one fact: where its checkout is.

**H.5 · The engine is ONE node (owner 23:10Z: "all they ever have to do is just do one read"), layered (owner 23:1xZ).** §I is that node, whole, as it will be minted at `.agi/nodes/.geometry/engine.md`. Depth 0 is the diagram, depth 1 the loop and one line per piece, depth 2 one piece (`sect <name>`), depth 3 the whole file. Every section is ONE `~~~` block under a named heading, so any read or render narrows to one section by name, byte-exact, at any REV, through the links (`sect`, 139 B). The projector and the seed read their pieces FROM this node, so the node IS the engine and nothing else is installed. **The bar (my call, asked by belam): depth 0+1 <= 4,096 B (one page: what every session reads) · the code, counted, <= 8,192 B (belam's ~8 KB) · the whole node <= 12,288 B (3 pages).** Measured: 3,806 B · 6,029 B · 11,305 B (body). Past any of them = not simple enough yet.
Tested on a `--shared` scratch clone (MAIN untouched), the node committed as `trunk`:
| test | result |
|---|---|
| `sect <name> trunk` for all 20 pieces vs the source files | 20 of 20 byte-identical (`cmp`); diagram 978 B · loop 491 B · pieces 1,946 B |
| bootstrap with the seed's own ExecStart (the node -> `sect`-style sed -> sh) | 10 post units (the local-town rows with recover != false, as §C.1) + its own .path/.service; the unit template byte-exact |
| fixed point: run the projected `agi-project.service` ExecStart again | `diff -r` empty · `systemd-analyze verify` prints nothing |
| the same after `engine.md` and `posts.md` become ADDRESS symlinks (§G) | `git show` returns the link text (s-p's F.7 red, reproduced); through `cat-file --follow-symlinks`: 10 units, fixed point empty, `sect` byte-exact |
| the engine node's link left dangling | 0 files projected -> the non-empty gate (F9/F14) refuses |
One trap paid for in the test: `sect`'s end pattern `^##* ` also matched a one-`#` shell comment inside a piece and cut 4 pieces short. Headings are now `##` or deeper (`^###* `), and a piece may not contain a line that starts with `##` or `~~~` (the generator asserts it).
**A red folded after delivery (self-perpetuating, 23:3xZ; the fix re-shaped by alive):** at BOOT a dangling engine or posts link made the seed report success over a dead body (the landing gate refuses it, the boot did not). The projector's reader now takes the blob or nothing (s-p's hardened `g()`), and the seed and the projector's own unit reload only if the projection holds at least one post unit: `sh -s OUT REV&&ls OUT/default.target.wants/agi-post@*>/dev/null&&systemctl --user daemon-reload`. s-p's first form (`&&` alone) does not catch a dangling ENGINE link: the extractor then emits nothing, `sh -s` runs an empty script and exits 0. Tested: trunk rc 0 with 10 units and an empty fixed point · dangling posts rc 2, no reload · dangling engine rc 2, no reload · verify clean · F19 20/20.
Write gate: `config` nodes are `written_by: [owner, prime_director]` (`[config].md`), so the council does not mint `config:engine`. belam minted v0 (11,101 B) at 2dadf20c17; §I below is v1 (the two reds above), for the Prime to re-mint.

## I · ROUND 3 · the engine node, whole: `config:engine` as it will be minted at `.agi/nodes/.geometry/engine.md`
This section IS the node's body, byte for byte (11,900 B, **v2**: S1-S14 folded, the heal, the gate; v1 @44619712d9 and §K say what changed), between the fences below. Frontmatter at mint: `id: config:engine` · `type: config` · parent `goal:g7.16.1.11` · the Prime (or DG3 at build) mints it; the council does not (`written_by`). F19 and F21 run against the minted node.
````markdown
# config:engine — the whole engine, one read
Depth 0 = diagram · 1 = loop + pieces, one line each · 2 = one piece: `sect <name>` · 3 = this file. Every piece is a small template over raw commands; its parameters are cells. Reasoning: doc:radically-simple-engine.

## diagram — depth 0
~~~
              GRAPH = git @trunk: nodes · .agi/n/<mint> real files · addresses + parents = symlinks
   boot ──▶ agi-seed ──▶ agi-project (read FROM this node) ──▶ BODY: users · units · settings · keys
   BODY ──▶ post unit ──▶ harness start|resume|compact ──▶ agi-brief: b = walk(card + claims)
   session ──▶ plain paths in its OWN checkout ──turn end──▶ one signed commit on its own ref
   post refs ──▶ the master merges ──▶ trunk moves ──▶ agi-project re-runs ──▶ next brief sees it
   tick: project(graph) == observe(body)?  equal = alive · differ = heal + a drift commit
   frontier: each active goal runs its falsifier ──▶ met | red | mute ──▶ the pool; claim = one CAS
   agi-gate at every trunk landing: the projection is non-empty and reproduces itself · V = red + mute
   is published, not gated (no owner-seed cell yet) · every at-REV read follows the links (cat-file)
~~~

## loop — depth 1
~~~
1 BOOT   agi-seed extracts agi-project from this node @trunk; it projects the body from the graph
2 START  a post's unit starts its harness; start, resume and compact all run agi-brief first (CC: the vector)
3 WORK   the agent reads and writes plain paths in ~/t; every turn end = one signed commit on its ref
4 LAND   the master merges post refs; agi-gate refuses a tip whose body would not regrow
5 TICK   tick.sh starts what drifted (polkit: group agi) and commits it; agi-frontier calls every unmet goal into the pool
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service    468 B  a post IS one unit instance: its uid, its checkout ~/t, its key, the harness under strace; a restart is a rotation
agi-inbox@.path       37 B  mail wakes a post: a change in its drop box ...
agi-inbox@.service    71 B  ... types "mail" into its session
settings.json        467 B  the harness wiring every post gets: the meter (rotate at the line), the brief at every start, one commit at every turn end
agi.ts               377 B  the same wiring for pi: the brief in the system prompt on every turn, one commit at every turn end
agi-brief            575 B  what a session sees first: the walk from its card + its own claims; the vector, then whole nodes by |b|
brief.py             603 B  b = a sum((1-a) P_theta)^k e: the complex walk over parent symlinks; |b| = how near, phase = how far up
gitconfig             99 B  every commit is signed by the post's own key
agi-flush            183 B  on exit: commit, merge, push: a dying session loses nothing
pre-receive          435 B  a push may touch only paths whose owner group the pusher is in
signers               65 B  allowed_signers = the posts' public keys
sysusers.conf         51 B  a post = one user in one group
agi.rules            211 B  the ONE root-owned piece: group agi may start agi-post@ units, so tick heals with no root act
project.sh           282 B  what the body SHOULD be, read from the graph
observe.sh           332 B  what the body IS, read from the box
tick.sh              250 B  the homeostat: diff them; heal what drifted and commit the wound
simhash.awk          241 B  stage-0 latent sense: near-duplicate and misfiled prose, no package
agi-project          941 B  the genome: units for every post row, read from this node @REV; its own unit re-reads it
agi-seed.service     447 B  the ONE installed unit: at boot, run agi-project from this node @trunk
agi-frontier         460 B  the hunger: every active goal runs its falsifier: met | red | mute
agi-gate             273 B  the trunk gate (pre-receive): refuse a tip whose body would not regrow
sect                 149 B  the narrowed read: ONE section or piece of this node, byte-exact, at any REV
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-post@.service (468 B)
~~~ini
[Service]
User=agi-%i
WorkingDirectory=/var/lib/agi/%i/t
EnvironmentFile=/var/lib/agi/%i/env
RuntimeDirectory=agi-%i
ExecStartPre=sh -c 'mkdir -p $HOME/.ssh .agi/keys;[ -f $HOME/.ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f$HOME/.ssh/id_ed25519;cp $HOME/.ssh/id_ed25519.pub .agi/keys/%i'
ExecStart=dtach -N %t/agi-%i/s sh -c 'exec strace -qqfe%%file -o$HOME/r ${H} go'
ExecStopPost=sh -c agi-flush
Restart=always
MemoryHigh=4G
[Install]
WantedBy=multi-user.target
~~~

### agi-inbox@.path (37 B)
~~~ini
[Path]
PathChanged=/var/spool/agi/%i
~~~

### agi-inbox@.service (71 B)
~~~ini
[Service]
User=agi-%i
ExecStart=sh -c 'echo mail|dtach -p %t/agi-%i/s'
~~~

### settings.json (467 B)
~~~json
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"jq -r .transcript_path|xargs tail -1|jq -e '.message.usage|.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens>470000'>/dev/null&&echo 'At the line: write your card, git commit it, then run: kill $PPID'"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"B=0 agi-brief"}]}],"Stop":[{"hooks":[{"type":"command","command":"cd ~/t;git add -A .agi;git commit -qm$USER||:"}]}]}}
~~~

### agi.ts (377 B)
~~~ts
import{execSync as x}from"node:child_process";let b="";const c=()=>{try{x("cd ~/t;git add -A .agi;git commit -qm$USER",{stdio:"ignore"})}catch{}}
export default(pi:any)=>{pi.on("session_start",()=>{try{b=x("agi-brief",{encoding:"utf8"})}catch{}})
pi.on("before_agent_start",(e:any)=>b?{systemPrompt:e.systemPrompt+"\n\n"+b}:undefined);pi.on("turn_end",c);pi.on("agent_end",c)}
~~~

### agi-brief (575 B)
~~~sh
#!/bin/sh
p=${AGI_POST:-${USER#agi-}};cd "${AGI_ROOT:-$HOME/t}/.agi"||exit 0;c=$(readlink -f nodes/doc/card-$p.md)||exit 0;c=${c%/node.md}
e=${c##*/}$(find "$(git config remote.origin.url)/refs/claims" -type f -user agi-$p ! -name '*.lock' -printf ',%f' 2>/dev/null)
sect brief.py|python3 - n $e ${K:-20}|while read a f m;do echo "$a $f $(sed -n '/^id:/{s/^id: *//p;q}' n/$m/node.md) .agi/n/$m/node.md";done>~/.brief
echo "# brief: $p (|b| · levels up · address · path)";cat ~/.brief;cut -d' ' -f4 ~/.brief|sed 's|^.agi/||'|xargs tail -n+1 2>/dev/null|head -c ${B:-40000}
~~~

### brief.py (603 B)
~~~py
import os,sys,cmath
R,S,k=sys.argv[1],sys.argv[2].split(','),int(sys.argv[3]);q=cmath.exp(.5j)
A={}
for m in os.listdir(R):
 for p in (os.listdir(f'{R}/{m}/p') if os.path.isdir(f'{R}/{m}/p') else ()):
  t=os.readlink(f'{R}/{m}/p/{p}')[6:]
  if os.path.isdir(f'{R}/{t}'):A.setdefault(m,[]).append((t,q));A.setdefault(t,[]).append((m,1/q))
x={s:1/len(S) for s in S}
for _ in range(30):
 y={s:.15/len(S) for s in S}
 for u,v in x.items():
  for w,z in A.get(u,()):y[w]=y.get(w,0)+.85*v*z/len(A[u])
 x=y
for m in sorted(x,key=lambda m:-abs(x[m]))[:k]:print(f'{abs(x[m]):.3f} {cmath.phase(x[m])/.5:+.1f}',m)
~~~

### gitconfig (99 B)
~~~ini
[gpg]
format=ssh
[commit]
gpgsign=true
[user]
signingkey=~/.ssh/id_ed25519.pub
[safe]
	directory=*
~~~

### agi-flush (183 B)
~~~sh
#!/bin/sh
cd ~/t;grep -o '"/[^"]*"' ~/r|sort -u>~/track;git add -A .agi;git commit -qm$USER;git pull -q --no-rebase origin trunk&&git push -q origin HEAD:refs/posts/${USER#agi-}/head
~~~

### pre-receive (435 B)
~~~sh
#!/bin/sh
e=$(git hash-object -t tree /dev/null)
while read o n r;do case $n in *[!0]*);;*)continue;;esac;[ $r = refs/heads/trunk ]&&{ agi-gate $n||{ echo "gate: $n";exit 1;};continue;};case $o in *[!0]*);;*)o=$(git merge-base HEAD $n 2>/dev/null||echo $e);;esac
f=$(git diff --name-only $o $n)||exit 1;for p in $f;do g=$(git check-attr --source=$n owner -- "$p"|cut -d' ' -f3);id -nG|grep -qw "$g"||{ echo "$p: $g";exit 1;};done;done
~~~

### signers (65 B)
~~~sh
#!/bin/sh
for f in .agi/keys/*;do echo "${f##*/} $(cat $f)";done
~~~

### sysusers.conf (51 B)
~~~ini
u agi-alive - - /var/lib/agi/alive
m agi-alive agi
~~~

### agi.rules (211 B)
~~~js
polkit.addRule(function(a,s){if(a.id=="org.freedesktop.systemd1.manage-units"&&a.lookup("verb")=="start"&&/^agi-post@[a-z0-9-]+\.service$/.test(a.lookup("unit"))&&s.isInGroup("agi"))return polkit.Result.YES;});
~~~

### project.sh (282 B)
~~~sh
#!/bin/sh
r(){ echo "$1:$2"|git cat-file --batch --follow-symlinks|{ read o t s;[ "$t" = blob ]&&head -c $s;};}
r HEAD .agi/nodes/.geometry/posts.md|grep -o '"name": "[^"]*"'|cut -d'"' -f4|sort -u|while read p;do printf 'user agi-%s\nunit agi-post@%s\nbrief agi-%s\n' $p $p $p;done
~~~

### observe.sh (332 B)
~~~sh
#!/bin/sh
getent passwd|cut -d: -f1|grep '^agi-'|sed 's/^/user /'
systemctl list-units --state=active --plain --no-legend 'agi-post@*'|cut -d' ' -f1|sed 's/\.service$//;s/^/unit /'
getent passwd|awk -F: '/^agi-/{print $1,$6}'|while read u h;do jq -e .hooks.SessionStart $h/.claude/settings.json>/dev/null 2>&1&&echo "brief $u";done
~~~

### tick.sh (250 B)
~~~sh
#!/bin/sh
cd ~/t;mkdir -p .agi/drift;sect project.sh|sh|sort>~/p;sect observe.sh|sh|sort>~/o;diff ~/p ~/o>.agi/drift/$USER&&exit
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|xargs -rn1 systemctl start;git add .agi/drift;git commit -qm"drift: $USER"
~~~

### simhash.awk (241 B)
~~~awk
BEGIN{for(i=32;i<127;i++)o[sprintf("%c",i)]=i}
{for(w=1;w<NF;w++){s=$w" "$(w+1);h=0;for(c=1;c<=length(s);c++)h=(h*31+o[substr(s,c,1)])%4294967291;for(b=0;b<32;b++)v[b]+=int(h/2^b)%2?1:-1}}
END{for(b=0;b<32;b++)x=x (v[b]>0);print x,FILENAME}
~~~

### agi-project (941 B)
~~~sh
#!/bin/sh
o=$1 r=$2 w=$1/default.target.wants;g(){ echo "$r:.agi/nodes/.geometry/$1"|git cat-file --batch --follow-symlinks|{ read a t s;[ "$t" = blob ]&&head -c $s;};};mkdir -p $w
g engine.md|sed -n '/^### agi-post@.service /,/^### /{/^~~~/,/^~~~/{//!p}}'>$o/agi-post@.service
for p in $(g posts.md|sed -n 's/^  - {/{/p'|jq -r "select(.box==\"${AGI_BOX:-local-town}\" and .recover!=false).name//empty");do ln -sf ../agi-post@.service $w/agi-post@$p.service;done
printf '[Service]\nType=oneshot\nWorkingDirectory=%s\nExecStart=sh -c "echo %s:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n \047/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}\047|sh -s %s %s&&ls %s/default.target.wants/agi-post@*>/dev/null&&systemctl --user daemon-reload"\n' $PWD $r $o $r $o>$o/agi-project.service
printf '[Path]\nPathChanged=%s\n' $(git rev-parse --absolute-git-dir)/logs/$r>$o/agi-project.path;ln -sf ../agi-project.path $w
~~~

### agi-seed.service (447 B)
~~~ini
[Unit]
RequiresMountsFor=/data/work/agi
[Service]
Type=oneshot
WorkingDirectory=/data/work/agi
ExecStart=sh -c "echo trunk:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n '/^### agi-project /,/^### /{/^~~~/,/^~~~/{//!p}}'|sh -s %t/systemd/user trunk&&ls %t/systemd/user/default.target.wants/agi-post@*>/dev/null&&systemctl --user daemon-reload&&systemctl --user start default.target"
[Install]
WantedBy=default.target
~~~

### agi-frontier (460 B)
~~~sh
#!/bin/sh
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### agi-gate (273 B)
~~~sh
#!/bin/sh
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&ls $o/default.target.wants/agi-post@*>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
~~~

### sect (149 B)
~~~sh
#!/bin/sh
echo "${2:-HEAD}:.agi/nodes/.geometry/engine.md"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~
````

## J · ROUND 3 · the owner-approved spike (F17 paid leg + root-once), measured 2026-10-01 00:3xZ by alive
Owner 00:28Z (verbatim on goal:g7.16.1.11): F17 "Go, one short run" · root-once "Go after F17". F17 ran first (one Sonnet 5.5 session on a scratch clone, $0.2829), then the root-once step on throwaway users agi-spike-a/b, a bare repo under /tmp and units in /run, with a stub harness (sleep infinity: no session, no spend). Every root act was listed with its undo; all were undone at 00:40Z and the box verified clean (no spike users, units, dirs, or dtach).
```
F1  homeostat   detect PASS only with S5 (observe needs --state=active) · record PASS only with S7 (-qSm) · heal FAIL (S8: tick as the post user cannot start a system unit)
F2  PASS  b cannot lock a's head; a moves its own
F3  PASS  2 x 100 concurrent commits on own refs, 0 failures, fsck clean, 0 lock files, refs stay loose (the suite arm not run)
F4  PASS  8 racers on 2 claims -> exactly 2 winners
F5  PASS  b drops into a's box; b cannot list (EACCES) or delete mail it did not drop (EPERM); a merges (receipt = merge parent) and clears the box
F6  NOT RUN  needs real sessions (spend beyond F17 not authorized)
F7  PASS  (round 2, pure)
F8  PASS  projector over the throwaway posts -> exactly agi-post@spike-a/b; rm + re-project = diff -r empty
F9  NOT BUILT  no gate piece in config:engine (the fixed-point gate is a test, not a hook)
F10 NOT BUILT  the V gate is ~120 B inline prose, no piece
F11 NOT RUN  no verb-node piece designed
F12 PASS  6,029 B counted
F13-F16 PASS  depth 0+1 3,806 B · fixed point through links · every piece parses · r == cat, rc 1 on missing and dangling
L1  PASS on the throwaway (0) · live graph 25-27 until the migration re-points them
L2  PASS  git mv of one address: 0 dangling, parent links unchanged
L3  PASS  card -> parent +1.0, siblings 0 on the body
F17 PASS  CC startup + resume + compact, one Sonnet 5.5 session, $0.2829 · CC caps hook stdout at a 2 KB preview (40.5 KB saved to a file): the vector arrives, whole nodes do not
F18 PASS  plain cat write -> exactly 1 signed commit (G) via the Stop command · trap S11: git add -A sweeps every untracked file
F19 PASS  sect 20/20 from the minted node
F20 PASS  claim owner = the ref FILE's owner (a: 2, b: 0; then b's real claim seeds b's brief)
F21 PASS  3,806 · 6,029 · 11,305 B
F22 PASS  origin = /tmp/agi-spike/shared.git (plain path)
P1  PASS  pre-receive refuses b's push on a's card by name, accepts b's own path
FINDINGS (each a template line or a guard, for DG3): S1 gitconfig needs [safe] directory=<shared repo> (git refuses every op otherwise, exit 128) · S2/S3 the post unit's %h=/root and %t=/run in a SYSTEM unit -> explicit home path cell, RuntimeDirectory=agi-%i, $HOME inside sh -c, ExecStopPost=sh -c agi-flush (corrected unit 424 B, ran both posts) · S4 .agi/keys/ absent in a clone, the '-' prefix hides the failed cp -> signers empty, silently · S5 observe lists failed units as present -> --state=active · S6 agi-flush pushes the trunk (the master's ref) -> push refs/posts/<p>/head · S7 git commit -qSm<msg> parses m<msg> as the signing KEY ID (-S takes an optional arg): tick and agi-flush never commit -> -qm (gpgsign is in gitconfig) · S8 the heal needs root: tick as a system timer, or a polkit rule for agi-post@* · S10 agi-brief's default brief.py path is never placed -> read it with sect · S11 the turn-end commit sweeps untracked files -> git add -A .agi or a .gitignore · S12 brief.py crashes on a node with no parents (git drops the empty p/) -> isdir guard, +41 B (603 B)
```
**Read:** the spine holds as designed (F2-F5, F8, F13-F22, P1, L2, L3). The body as written did NOT run: twelve findings, each a template line or a small guard (S1-S12 above), and four rows are not built (F9, F10: the gates; F11: the verb piece) or not run (F6: needs real sessions). S7 is the sharpest: `git commit -qSm<msg>` makes `m<msg>` the signing key id, so neither tick nor agi-flush ever committed. The corrected post unit (424 B) is in the ledger, not in config:engine: config:engine changes only through the Prime.

## K · ROUND 3 · config:engine v2 (belam's word 00:41Z 10-01): S1-S14 folded, the heal without root per tick, F9 built, re-run on a throwaway
**What changed (22 pieces; v1 had 20):** S1 gitconfig `[safe] directory=*` (posts only touch their own clone and the shared repo) · S2/S3 the post unit names its home (`/var/lib/agi/%i`), `RuntimeDirectory=agi-%i` for the dtach socket, `$HOME` inside `sh -c`, `ExecStopPost=sh -c agi-flush` · S4 ExecStartPre makes `.agi/keys` and no longer hides a failure (`-` dropped; keygen only if absent) · S5 observe counts `--state=active` units only · S6 agi-flush merges `origin trunk` and pushes `HEAD:refs/posts/<post>/head`, never the trunk · S7 `-qm` everywhere (gpgsign is gitconfig's) · S10 agi-brief and tick read their pieces with `sect`, so nothing has to be placed · S11 every turn-end and exit commit adds `.agi` only · S12 brief.py skips a node with no `p/` (+41 B) · the CC cap: SessionStart runs `B=0 agi-brief` = the vector only (202 B on the spike; whole nodes stay pi's, in its system prompt) · S14 the trunk skips the per-path owner check (only the master can write `refs/heads`, and `agi-gate` is the trunk's check). S13 (dtach exits 1 on a clean stop, so the unit reads `failed`) is NAMED, not fixed: the heal does not depend on it, and `SuccessExitStatus=1` could mask a crash.
**The heal: ONE root-owned piece, `agi.rules` (214 B), a polkit rule:** group `agi` may `start` `agi-post@<name>.service` and nothing else. tick runs as the post; installing the rule is the one root act, once per box.
**F9 BUILT: `agi-gate` (272 B, called by pre-receive on the trunk):** the tip's projection must be non-empty, and must regrow into an EMPTY dir from its own unit with `diff -r` empty. (The first form re-ran into the same dir: a self-run that does nothing passed. Caught by reasoning, then tested.) **F10 DROPPED, named:** the V gate needs an owner-seed cell the [goal] schema does not have; V stays published (§C), not gated. **F11 DROPPED:** no verb piece is designed.
**Figures:** depth 0+1 4,057 B (<= 4,096) · code 6,904 B counted (<= 8,192) · the node body 11,900 B (<= 12,288, after dropping five in-piece comment lines that repeated the pieces table).
Re-run 00:45-00:46Z on throwaway users agi-spike-a/b (the v2 sysusers form, group agi), a bare repo under /tmp, the polkit rule and the units in /run, stub harness (no session, no spend); 7 root acts, each with its undo; ALL undone 00:46Z and verified (0 agi- users, 0 agi units, no homes, repo, rule or runtime dir, dtach removed).
```
F1   PASS  healthy: 0 drift · spike-b stopped -> tick as spike-a names it, restarts it through polkit (active again), records a SIGNED drift commit · clean tick after
F9   PASS  via the real hook: the master's good trunk push lands (gate ran) · a tip whose projector self-run points at a missing section is refused "gate: <sha>" · a dangling posts link rc 1 (scratch clone)
F18  PASS  the Stop command commits .agi only: +1 commit (drift, keys, the node), the scratch file untracked (S11)
F19  PASS  sect 22/22 byte-exact from the node (scratch clone and the spike repo)
P1   PASS  b's push touching a's card refused by name; b's own path accepted
S2-S4 PASS the v2 unit starts both posts unmodified; .agi/keys/<post> present; signers lists the key
S6   PASS  a clean stop's agi-flush pushed refs/posts/spike-b/head; the trunk untouched
S10/S12/cap PASS  B=0 agi-brief on the body: 202 B, the vector, brief.py read via sect, the parentless node skipped
F22  PASS  origin is a plain path
unchanged by v2 and not re-run: F2-F5, F7, F8, F13-F16, F17, F20, L1-L3 (§J)
```

## L · ROUND 4 · self-perpetuating -- ONE launch vector (asks 3 + 4): no workflow.py; the commands template is a vector base with routes
**Owner 03:48Z:** "No more workflow.py needed because all things are infinitely composable and run inside the 'wrapper.' There's no distinction between posts, subagents, workflows, etc. ... preset routes ... a vector base pointing/multiplying/operating on other relevant vectors. And even a 'compose new launch vector' vector to guide a model step by step." **What am I ACTUALLY trying to get the machine to do here?** Start a mind on a task, inside bounds, and get its result back as a commit. Whatever it is called (post, kid, subagent, workflow stage, round), that is the whole act.

```
L = base (+) route (+) deltas            one JSON vector; (+) = jq `add` (a cell-wise override), so a route IS a sparse vector
basis = the cells of base:  run · harness · task · base · mem · time · each · then        (8 cells, one line)
  each : [t1..tn]   =>  L (x) T  = n launches  {L (+) {task: ti}}                    fan out   (workflow rounds[], a parent's kids)
  then : D          =>  D (+) {base: refs/L/hash(L)} starts when L stops               chain     (review -> refute, stage -> stage)
  run  : fill a slot at `base` -> the harness works in it -> keep the result -> refs/L/hash(L)   (round-1 §4 slot, on disk)
unit name = agi-L-hash(L) · result = refs/L/hash(L) · result exists => done, never re-run    a launch is a PURE function of its vector
what it SEES = agi-brief's walk with e = the task node: b = sum((1-a) P)^k e_task          the 4th product, already in config:engine
```
- **Preset routes = the commands template (ask 4):** `post` · `kid` · `review` · `refute` · `merge-up-review` (= review, `then` refute) · `compose`. A route may name another route (`merge-up-review` builds on `review`), so routes operate on routes, and a call adds its own deltas. Today's command:commands (115,841 B of argv registry) and 30 workflow scripts (233,926 B) become 7 lines (872 B).
- **The compose vector:** the route `compose` launches a model with the basis, in order, and asks for ONE cell per step, reusing a route where one fits. Its output is one JSON line, validated by `jq -e`, and it becomes a new route line. NOT yet run against a model (the free lane is open for it; spike F24).
- **Posts stay on agi-post@ for now.** A post is the route `post` (time = infinity). DG3 is bringing DG5 up live on agi-post@.service (stage 2.5), so this round changes nothing there. Folding agi-post@ into agi-launch is a stage-3 option, not a change to the running path.

**Tested 03:5xZ** (user manager, the `--shared` scratch clone, stub harnesses that write a file: no model, no root, MAIN untouched):
| claim | result |
|---|---|
| override: `{"route":"kid","task":"A"}` | refs/L/<hash> holds `A` |
| fan out: `{"route":"kid","each":["x","y","z"]}` | 3 units, 3 refs holding x, y, z |
| chain: `{"route":"merge-up-review","task":"g7.16.1.11"}` | review's ref, then refute's ref, which holds BOTH outputs: refute ran on review's result |
| memo: the same chain vector launched again | no unit started: its ref already existed |
| a second identical launch while the first runs | systemd refuses it ("already loaded"): one name per vector |
**Two measured traps, now in the base cells:** (1) a slot on the unit's RuntimeDirectory is tmpfs: a full 148 MB tree in RAM. (2) Page cache counts against MemoryHigh: at 256M a fill crawled from 1.6 s (by hand, on disk) to more than 120 s and 2 of 5 units timed out. So the tree lives on disk at `/var/tmp/$INVOCATION_ID` and is removed when the run ends, and the base `mem` is 1G. A sparse fill (only the task's paths) is the next saving, unmeasured.

**Genome lens: it regrows from config:engine and adds two sections, nothing installed.** `### agi-launch` (~~~sh, 896 B) and `### launch` (~~~json, 872 B), read with `sect launch` at any REV. **depth 0+1 stays one read:** two new piece lines, paid for by tightening my own five lines, give 4,095 B (limit 4,096; v2 is 4,057). The exact lines:
```
agi-project          941 B  the genome: post rows -> units, read from here; re-reads itself
agi-seed.service     447 B  the ONE installed unit: boot -> agi-project
agi-frontier         460 B  the hunger: goal falsifiers -> met | red | mute
agi-gate             273 B  refuse a trunk tip whose body would not regrow
sect                 149 B  ONE piece of this node, byte-exact, any REV
agi-launch           896 B  post|kid|workflow: ONE vector L; result = refs/L/hash(L)
launch               872 B  base + routes: each=fan out, then=chain, compose=new
```
The whole node grows by ~1.9 KB, to ~14.9 KB (budget 16,384).

**It retires** workflow.py 156,824 B · dispatch.py 227,309 B · spawn_budget.py 51,688 B (the bound becomes the `agi-L.slice` properties; not yet set, F23) · 30 workflow scripts 233,926 B. That is **~670 KB replaced by 1,768 B.**

Falsifiers: **F22** override · fan out · chain · memo, as in the table (PASS with stub harnesses) · **F23** `agi-L.slice` with TasksMax=N: an each of N+5 runs at most N at once (unrun) · **F24** `{"route":"compose"}` on pi-free returns a jq-valid vector whose keys are a subset of the basis, in <= 8 steps (unrun) · **F25** depth 0+1 of config:engine with the two lines <= 4,096 B (4,095 measured on a copy).

`agi-launch` whole (896 B counted; the test copy differs only in absolute paths and passing AGI_ROUTES):
```sh
#!/bin/sh
# agi-launch DELTA..: L = base (+) route (+) deltas (jq add); one transient unit named by the hash of L; its result IS refs/L/<hash> (exists = done); each = fan out, then = chain
R=${AGI_ROUTES:-$(sect launch)};L=$(printf '%s\n' "$@"|jq -sc --argjson R "$(echo "$R"|jq -sc .)" 'def x(d):($R[]|select(.name=="base"))+(if d.route then x($R[]|select(.name==d.route)) else {} end)+d|del(.name,.route);reduce .[] as $d({};.+x($d))')
[ "$(echo "$L"|jq '.each|length')" -gt 0 ]&&{ echo "$L"|jq -c '.each[] as $t|del(.each)+{task:$t}'|while read -r l;do agi-launch "$l";done;exit;}
i=agi-L-$(echo "$L"|git hash-object --stdin|cut -c1-12);git rev-parse -q --verify refs/L/$i>/dev/null&&exit;c(){ echo "$L"|jq -r .$1;};t=$(echo "$L"|jq -c '.then//empty|.+{base:"refs/L/'$i'"}')
systemd-run --user -q --unit=$i --slice=agi-L.slice -p WorkingDirectory=$PWD -p MemoryHigh=$(c mem) -p RuntimeMaxSec=$(c time) ${t:+-p "ExecStopPost=agi-launch '$t'"} --setenv=AGI_TASK="$(c task)" --setenv=AGI_BASE="$(c base)" --setenv=AGI_RET=refs/L/$i --setenv=AGI_HARNESS="$(c harness)" sh -c "$(c run)"
```
`launch` whole (872 B, one vector per line; the first is the base):
```json
{"name":"base","run":"d=/var/tmp/$INVOCATION_ID;mkdir $d;slot $d fill $AGI_BASE&&(cd $d&&sh -c \"$AGI_HARNESS\");slot $d keep $AGI_RET;rm -rf $d $d.?","harness":"pi -p @$AGI_TASK","task":"","base":"trunk","mem":"1G","time":"1800","each":null,"then":null}
{"name":"post","time":"infinity","mem":"4G"}
{"name":"kid","harness":"pi -p @$AGI_TASK","time":"1800"}
{"name":"review","harness":"pi -p \"review $AGI_BASE against the claim in $AGI_TASK\"","time":"1800"}
{"name":"refute","harness":"pi -p \"refute the review on $AGI_BASE\"","time":"900"}
{"name":"merge-up-review","route":"review","then":{"route":"refute"}}
{"name":"compose","harness":"pi -p \"Compose ONE launch vector. Fill exactly one cell per step, in this order: $(sect launch|head -1|jq -r 'keys_unsorted|join(\", \")'). Reuse a route where one fits. Print one JSON line; jq -e validates it.\"","time":"600"}
```

## M · ROUND 4 · all-is-one -- one representation for every vector: a directory of symlinks; schemas, guards and locations are vectors
**What am I ACTUALLY trying to get the machine to do here?** Owner 03:48Z: "It's all just vectors literally pointing to things. Maybe even filesystem pointers and even partition/volume-level pointers. The math is base level for everything." Give the machine ONE way to say "this points at that, with this weight", and let every structure (a node's parents, a schema, a guard, a location, a launch) be that one thing, so that composing any two is the same act.

**M.1 · The one representation.** Every POINTER vector (parents, near, schema, location) is a DIRECTORY OF SYMLINKS; a LAUNCH is a row of cells (§L) whose task and base cells are pointers and whose mem and time cells are coefficients (wording: self-perpetuating, 04:0xZ, so the doc never claims one representation while showing two). Each entry points at a basis element (a node by mint, a type, a slice, a path, a volume). The entry's name carries the coefficient only where one is needed; it defaults to 1. Three operations cover everything, and none is ours:
```
walk     P·v       readlink each entry (and its p/): one step through the graph        §G brief.py = Σ((1-α)Pθ)^k e
dot      <u,v>     comm -12 <(ls u) <(ls v): the shared basis elements                 a schema check, a claim overlap
mask     g∘v       the meet along a path: the kernel's own min (cgroups, mode bits)    a guard
```
§G's `p/` is the first such vector. Round 4 adds nothing new; it reads four more things as the same object.

**M.2 · A schema is a vector over TYPES (structure) plus an ordered list (arrangement).**
```
.agi/context/schemas/<type>/p/<parent-type> -> ../../<parent-type>    the allowed parents = the type's row of the type graph (structure)
.agi/context/schemas/<type>/s/<NN>-<section>                         the body's fixed order = numbered entries; ls is the order (arrangement)
the [<type>].md prose stays beside it: the vector is the part a machine checks, the prose the part a model reads
```
A node is well-formed iff the TYPES of its `p/` entries are a subset of its schema's `p/` (a dot product that leaves nothing out), and its `## ` headings follow `s/` in order. **Composable, because it is matrix algebra:** with T the type graph, T² is every legal grandparent type, and a CHAIN (goal → idea → hypothesis → experiment → verdict → outcome) is legal iff each step is a non-zero entry of T. A new node type is a new directory with a few symlinks, and every check composes it at once. The spawn gate's parent-type rule (spawn_gate.py, 1,507 lines of Python) becomes a lookup in a directory.
Measured 04:0xZ on the scratch projection (5,619 nodes, 6,176 parent symlinks read from `parents:` only): 20 schema vectors built from the real schemas' `allowed_parents` (every line unioned, 0 dangling) · `shape.sh` (463 B, one `grep` + two `find`s + one `awk`, 8.6 s over the whole graph) finds **52 nodes whose parent TYPE their own schema does not allow**: 17 `vision` under a `bigger_outcome` ([vision] allows only `moral`) · 10 `mvp` under a `goal` · 10 `experiment` under a `goal` · 10 `town` under a `vision` or `goal` ([town] allows only `ladder`) · 5 others. No checker reports them today: links.py's `schema` mode checks required FIELDS, and the spawn gate runs only at create. Each is either a schema behind practice (one symlink fixes it) or a node mis-filed (re-file it). The vector form makes the disagreement visible in one pass.

**M.3 · A guard is a vector the kernel multiplies by MIN along a path, and a broadcast guard is a name prefix.** A post's resources (memory, CPU, tasks, IO) are cells on its unit; its slice is its parent. The limit the kernel ENFORCES is the minimum of every cell on the path from the box root down to the process. That is a (min, ×) product along the slice tree, computed by the kernel, with no code of ours. Measured 03:5xZ on this box, user manager, no root:
| test | result |
|---|---|
| a kid with its own MemoryMax=512M inside a slice with MemoryMax=64M allocates 128M | OOM-killed (rc 1, `oom_kill 1` on the SLICE): the effective guard = min(64M, 512M) |
| the same kid allocates 32M | runs, rc 0 |
| a unit named `agi-*` asked for a different slice | placed in `agi-work.slice` with CPUWeight=50, MemoryHigh, MemoryMax all the same: an existing prefix drop-in (`agi-.service.d/50-sanctuary-guard.conf`) is ALREADY a broadcast guard vector over every `agi-*` unit |
So a guard is never code that watches. It is a cell, set ONCE on the right node of the slice tree. Its scope is the subtree (a slice) or the name prefix (a drop-in), and the kernel takes the meet. The memory budgets of the town, the post and its kids are one path (box → `agi.slice` → town slice → post unit → kid scope). `mem_cap.py` and most of `guard-init.sh` become cells (round 1 §7). **What still needs a watcher:** pressure that is not a limit (PSI) and liveness. Both are the homeostat (§A): sense, compare to the cell, act, record.

**M.4 · A location is a pointer the kernel already resolves down to the volume.** Every "where" in the graph is a symlink, and the chain below it is the kernel's own:
```
address  .agi/nodes/<type>/<slug>.md ─▶ .agi/n/<mint>/node.md      (§G: the mint never moves)
tree     .agi/n/<mint>/at ─▶ <a tiny per-node tree on a RAM volume> (stage 2.5: pulled in on demand, purged when done)
volume   findmnt -T <path>   ─▶ mount point + filesystem type        (the kernel's mount table)
device   the mount's source  ─▶ udev's own /dev/disk/by-* symlinks  (the volume layer is ALREADY a symlink graph)
```
Measured: an address resolves through `readlink -f` to its real file, and `findmnt -T` names its volume (tmpfs for the live graph, ext4 for the scratch copy), with 0 B of our code. The stage-2.5 per-node tree is ONE symlink, `at`. **Pulled in** = the target exists (measured: it resolves, on tmpfs). **Purged** = the target is gone, so `at` dangles (measured: `find -name at -xtype l` lists it). The purge list, the "which trees are live" census and the RAM accounting are therefore one `find`. A custom location per node is just a different target for `at`. Device and partition names never enter the graph (the anonymize rule): the chain stops at "a RAM volume" / "the repo volume" in anything written, and `findmnt` resolves the rest at run time.

**M.0 · A correction to §G (mine), found while building M.2.** The round-3 scratch projection read EVERY `- x:y` list item in the frontmatter as a parent (tags, `evidence_runs`, `blocked_by`, `seeds` as well as `parents`). Rebuilt from `parents:` only: **0 duplicate parents and 0 broken parent links** (not 193 and 27), and 6,176 parent links (not 9,496). The 13 `parked:g7.16.2` were TAGS. The stale ids that remain (e.g. `exp:test-coverage-r1`, `run:1`, `task:t-020`) sit in `evidence_runs` / `blocked_by`, fields links.py does not resolve as links. The symlink design is unchanged; the measured case for it is smaller than §G said, and §G now carries this note.

**M.5 · The same vector, everywhere (one read):**
| structure | the directory | basis | combined by |
|---|---|---|---|
| a node's parents | `.agi/n/<mint>/p/` | nodes (mint) | walk (§G) |
| latent nearness | `.agi/n/<mint>/near/` | nodes | walk |
| a post's live work | `refs/claims/<mint>` owned by the post | nodes | the brief's seed (§I) |
| a schema | `schemas/<type>/p/` + `s/` | types · sections | dot + order |
| a guard | unit/slice cells + prefix drop-ins | resources on the slice tree | the kernel's min |
| a location | `at`, an address | paths → volumes | readlink + findmnt |
| a launch | §L's launch basis (run · harness · task · base · mem · time · each · then) | its `mem`/`time` cells ARE its guard vector | the kernel takes their min with the slice path (M.3) |

Pieces for the count: the schema vectors are symlinks (0 B of code; ~2 symlinks per type) · `shape.sh` 463 B (the well-formedness check over every node) · guards: 0 B (cells and one prefix drop-in that already exists) · locations: 0 B (`readlink`, `findmnt`, `find -xtype l`).
Falsifiers to add: (V1) `shape.sh` over the migrated graph prints exactly the nodes links.py's schema check names, and nothing else · (V2) a kid allocating past the TIGHTEST cell on its slice path is OOM-killed in its own scope while a sibling survives (measured above with 64M/512M) · (V3) a purged tree's `at` dangles and `find .agi/n -name at -xtype l` lists exactly the purged set · (V4) a new node type made by `mkdir schemas/<t>/p` + two symlinks is enforced by `shape.sh` with no code change.

## N · ROUND 4 · alive -- the pane is two files, the anchor is the post's name, and every guard and watchdog has a home or a name
**Owner 03:48Z:** "Can we also make sure all the guards and watchdogs and such still work? I was thinking of also including the magic pane anchor as that would still be useful for later stuff like asking the system to work with foreign tools. ... Tmux pane or even a more base-level pane persistence 'trick' buried in all that vast hyperhuman systemic understanding from the inside." **What am I ACTUALLY trying to get the machine to do?** Keep a session alive with nothing attached to it, let anything (a post, the inbox, a foreign tool, the magic pane) type into it and read it as plain files, and make sure no guard silently stopped guarding when the body changed. Lens (alive): the system reports its own TRUE state, so a guard that no longer reaches its target is a red here, not a footnote.

**N.1 · Pane persistence below tmux: the pane is TWO FILES the unit owns.** `i` = a fifo the unit holds open read-write (so no writer leaving ever sends EOF) · `o` = the typescript. util-linux `script` (in the base system, already on every box) owns the pty. Nothing attaches: typing is a write to `i`, watching is a read of `o`. dtach (v2) is retired; it is not on this box any more.
```
writer (inbox · master · foreign tool · human) ──printf 'x\r' > i──▶ fifo (fd 3, rw) ──▶ script ──pty──▶ harness under strace
reader (magic pane · human · tick)          ◀──────── tail -f o ◀─── script -f (flushed, mode 600) ◀──┘
human attach = stty raw -echo; tail -f o & cat > i        ^C = printf '\003' > i  (the pty's own line discipline sends SIGINT)
```
Measured 03:54-04:05Z, user manager, no root, stub harness (a shell loop under strace), the exact v3 bytes below with only the paths, `User=` and `agi-flush` swapped; every test unit removed after (0 left):
| claim | result |
|---|---|
| the child owns a real pty with a size | `/dev/pts/13`, `50 200` |
| a write to `i` is typed into the session; CR submits | `mail\r` -> `got:mail` |
| a writer leaving does not end the session | written three times by three processes: still active |
| `printf '\003' > i` interrupts it | SIGINT, exit 130 |
| a crash restarts it whole (`Restart=always`) | NRestarts=1, active, the new `i` takes input |
| the inbox unit types into it | `agi-inbox@` Result=success, `got:mail` |
| no second copy of the transcript in the journal | 0 lines (`StandardOutput=null`) |
| the harness argv never lands in `o` | the header reads `$H`, unexpanded |
| `o` and `i` are private | both mode 600 |
**Three traps, measured and folded in:** (1) `script` also writes the stream to its stdout, i.e. the journal: a second transcript, readable by whoever reads the journal -> `StandardOutput=null`. (2) `script` puts its whole command line in `o`'s header: with `${H}` expanded by systemd, the harness argv lands in the file -> `\\$$H`, so systemd hands `\$H` to the outer sh and only the inner sh expands it. (3) `script` creates `o` with the umask (664 measured) -> `install -m600 /dev/null $HOME/o` first; `script` truncates it and keeps the mode (600 measured). Rejected: a kernel VT (`TTYPath=` + `/dev/vcsN`) needs the tty group and caps at 63.

**N.2 · The two pieces, whole (v3).** depth 0+1 is unchanged at **4,095 B**: the two piece lines keep their wording and the byte counts keep their width (468 -> 618, 71 -> 69). Node +148 B, code +148 B.
`agi-post@.service` (618 B):
~~~ini
[Service]
User=agi-%i
WorkingDirectory=/var/lib/agi/%i/t
EnvironmentFile=/var/lib/agi/%i/env
RuntimeDirectory=agi-%i
ExecStartPre=sh -c 'mkdir -p $HOME/.ssh .agi/keys;[ -f $HOME/.ssh/id_ed25519 ]||ssh-keygen -qN "" -ted25519 -f$HOME/.ssh/id_ed25519;cp $HOME/.ssh/id_ed25519.pub .agi/keys/%i;mkfifo -m600 %t/agi-%i/i;install -m600 /dev/null $HOME/o'
ExecStart=sh -c 'exec 3<>%t/agi-%i/i;exec script -qfO$HOME/o -c "stty cols 200 rows 50;exec strace -qqfe%%file -o\\$HOME/r \\$$H go" <&3'
StandardOutput=null
ExecStopPost=sh -c agi-flush
Restart=always
Slice=agi.slice
MemoryHigh=4G
[Install]
WantedBy=multi-user.target
~~~
`agi-inbox@.service` (69 B; the `.path` is unchanged):
~~~ini
[Service]
User=agi-%i
ExecStart=sh -c 'printf "mail\\r">%t/agi-%i/i'
~~~
Changed from v2: ExecStartPre makes `i` and a private `o` · ExecStart = the pane, `$H` hidden · `StandardOutput=null` · `Slice=agi.slice` (N.5) · the inbox writes `mail` + CR to `i` instead of `dtach -p`. The drop box stays the permission boundary: another post can only make this post read the word `mail`, never type into it.

**N.3 · The magic pane anchor is the post's NAME.** The pane of post `p` is `%t/agi-p/i` + `~agi-p/o`: a pure function of the unit's instance name, so the anchor costs 0 B and needs no registry. In §M's terms it is a location vector `p -> (i, o)` that the unit's own specifiers resolve.
```
foreign tool  = a launch whose harness cell is ANY argv (§L): it runs in the same pane, under the same strace and guard path
talk to it    = write i · read o          (an MCP-less, tool-call-less surface: bytes in, bytes out)
magic pane    = a reader on o (goal:g5.24.3: detect the structured form in the prose stream) that may answer by writing i
occupation    = the unit is active (goal:g7.31.2): attaching IS registering, because there is nothing to attach but the unit;
                a restart keeps the name, so the pin survives rotation by construction; no argv builder exists to regrow
```
For a launch (§L), the pane is the same two files under `/var/tmp/$INVOCATION_ID`: this is a stage-3 option, not a change now (posts stay on agi-post@ while DG3 runs stage 2.5).

**N.4 · Every guard and watchdog today -> where it lives under config:engine.** KEEP = stays below the engine (the box body, `guard-init.sh`) · v2 / §L / §M = carried by that piece · GAP = nothing carries it yet, named with its falsifier · HELD = waits on DG3's key/identity build (belam 03:48Z).
| today | guards | under the new engine | proof |
|---|---|---|---|
| `rotation_alert.py` (CC UserPromptSubmit) | rotate at the line | settings.json meter; pi: the CCCC turn hook (DG3, stage 2.5) | v2 · CCCC on the 2.5 bar |
| `cc-session-start.sh` | the brief at start | settings.json SessionStart `B=0 agi-brief`; pi: agi.ts | §K cap PASS |
| `heal.py watch` (agi-reaper, 30 s) | respawn a dead seat | `Restart=always` + tick.sh through agi.rules | F1 PASS · N.1 restart PASS |
| `rotate.py alarms` (SM) · after_join reap-proof · the captive capture chain | alarm, prove the predecessor gone, rotate a stuck post | a restart IS a rotation: one unit, one cgroup, systemd stops the whole cgroup; tick's drift commit is the ONE alarm | F1 · §L "already loaded" |
| `nudge_sweep` (2 min) + coalesced / undelivered nudges | re-type a stranded nudge | a write to `i` queues in the pty: nothing to strand | N.1 PASS (stub) · G2 |
| `mail_poll` (5 min) | read the inboxes | `agi-inbox@.path` | N.1 inbox PASS |
| `grid_sync` (5 min) | version every node | the turn-end commit (Stop hook / agi.ts) + agi-flush | F18 PASS |
| `branch_push` (hourly) | push the trunk | agi-flush pushes post refs; only the master moves the trunk | S6 PASS |
| `prime_merge` (4 h) | review + merge | §L route `merge-up-review`; the merge stays the master's act | §L F22 (stub) |
| `maint_gc` (daily) | git gc | KEEP: one crontab line | -- |
| `memory_alarm` (1 min) | warn BEFORE exhaustion | GAP: observe.sh reads unit states only; one line reading the post slice's `memory.events` high count + PSI makes a climb a drift commit (true state, never a kill) | G3 |
| GUARD.md's five layers (oomd · user@ cap · agi slices · reboot watchdog · sanctuary-watch) | keep the box reachable | KEEP below the engine; §M M.3: the slice path IS the guard vector | §M V2 PASS · see N.5 |
| the `agi-*` prefix drop-in (50-sanctuary-guard) | a broadcast guard | reaches §L launches (user manager); does NOT reach agi-post@ (a system unit) | N.5, measured |
| session-sweep timer | archive idle session dirs out of MAIN | KEEP while posts run in MAIN; under v2 a post's sessions sit in its own home, so the job's target moves to `/var/lib/agi/*/` | -- |
| ram-sync timer | MAIN's files on the RAM disk | KEEP for MAIN; under v2 the RAM tier is §M's per-node `at` (purged = dangling) | §M V3 |
| pre-commit privacy guard (box-local) + `anonymize.py check` | refuse a box token in a commit | GAP: a post's own clone `~/t` gets no hooks; one gitconfig cell `core.hooksPath` -> the box guard dir | G4 |
| `spawn_budget.py` | live-agent bound | `agi-L.slice` TasksMax (§L) + posts in `agi.slice` | §L F23 (unrun) |
| `verify-suite.lock` | one suite runner | a claim = one CAS on `refs/claims` | v2 |
| dispatch's stale-base refusal | never work on a stale base | agi-flush merges the trunk before it pushes; agi-gate refuses a tip that would not regrow | S6 · F9 PASS |
| write.py spawn gate · `links.py` schema + links | legal parents, no broken link | shape.sh (§M) + agi-gate (a dangling posts link = rc 1) | F9 PASS · §M V1 |
| the grid evidence gate | no verdict without evidence | agi-frontier: a goal is met only by its own falsifier | v2 |
| `send.py whois` + signatures | authority from the graph | signed commits + signers + pre-receive ownership | P1 PASS |
| provisioning floor · per-spawn keys · keysync timer · `envfile.py --check` | spend, keys present / absent | HELD | -- |
| the stream's `brb` / `panic` | nothing secret on the stream | the owner's alone, outside the engine, untouched | -- |
| sanctuary-watch peer probes + recovery agent | other towns | KEEP (box body) | -- |

**N.5 · A red the round found (alive lens): the box guard does not reach a v2 post.** Every guard layer that caps memory as a group (the `agi-*` drop-in, `agi.slice` / `agi-work.slice`, the user@ cap, the oomd lines on them) lives under the USER manager. A v2 post is `agi-post@<p>.service`, a SYSTEM unit (`User=agi-%i`, `WantedBy=multi-user.target`), so it lands in `system.slice` beside sshd with only its own `MemoryHigh=4G`. N posts x 4G is a throttle per post, with no meet over them and no oomd line. That is the 09-25 livelock shape. Measured 04:0xZ: the drop-in's `DropInPaths` exist for user units only; no system `agi-*` unit is live yet, so nothing is exposed today. **Fix = cells, 0 code:** `Slice=agi.slice` in agi-post@ (in N.2 above) + a system `agi.slice` with `MemoryMax`, `MemoryHigh` and `ManagedOOMMemoryPressure=kill`, set ONCE by `guard-init.sh` from `config:guard` (it already sizes user@ the same way). Until that cell exists the post is no worse than v2, and no better. For DG3's stage 2.5 bar: DG5's unit must not start in `system.slice` uncapped.

**Falsifiers.** **N1** pty, typing, CR, ^C, no EOF, restart (PASS, above) · **N2** no journal copy, argv hidden, `i` + `o` 600 (PASS) · **N3** a live TUI (claude and pi) in the pane: CR submits a prompt, a write during a busy turn is kept for the next turn, and `o` grows by at most X MB/h (UNRUN: needs the live post, stage 2.5; X is a cell to measure, never a guess) · **N4** `systemctl show agi-post@<p> -p ControlGroup` is under `/agi.slice/`, and that slice has a finite MemoryMax and an oomd line (UNRUN: a root act) · **G2** a nudge written while the post's TUI is busy is answered (UNRUN) · **G3** a memory climb past the slice's MemoryHigh appears as a drift commit naming the slice before any kill (UNRUN) · **G4** a commit carrying a box token in a post clone is refused (UNRUN) · **G5** every row of the N.4 table names a piece, a cell or a falsifier, or says KEEP / HELD by name: no row reads "covered" without one (this table, checked by hand 04:0xZ).

## O · ROUND 4 · alive -- the CAPSULE: sealed by the box, opened only by k ring signatures, straight into ONE signed destination
**Owner 04:49Z:** "ring/multisig-signed perma-encrypted capsule ... always be encrypted until 'popped' as a safe shell command that can be piped anywhere without the rings key holders ever having any individual permission to view it. Only a combined permission to send it somewhere. No view possible. It's like part of the money system but radically simplified down to bytes of shell instructions." **What am I ACTUALLY trying to get the machine to do?** Make the ONLY path from ciphertext to plaintext a k-of-n decision over WHERE it goes. Nobody holds a key that decrypts; holders hold keys that can only AGREE. Lens (alive): every limit below is measured or named, never implied away.

**O.0 · Measured on this box first (04:5xZ), because belam's draft leaned on it:** no TPM (`/dev/tpm*` absent; `systemd-creds has-tpm2` = partial: no firmware, no driver), so a `systemd-creds` seal is anchored by the HOST key alone: a root-only file. systemd 255 has no user-scoped credentials (`--user` unrecognized), and a non-root user cannot even seal: "Failed to determine local credential host secret: Permission denied". So a holder (a post, non-root) can neither seal nor unseal. That is the "no individual permission to view", measured, and it is root's alone.

**O.1 · The flow (four acts, one ref).**
```
SEAL   owner (root, once):  secret on STDIN (never argv) -> systemd-creds encrypt --name=s - .agi/capsule/C/cred   (AES-GCM, host key)
       commit .agi/capsule/C/{cred, k, ring/<post> -> ../../../keys/<post>}  ->  refs/capsule/C = that commit = the first tip T
ASK    anyone: R = "C H T"  with  H = git hash-object R.L,  R.L = the DESTINATION launch vector (§L: its run cell says where it pipes)
SIGN   each holder: ssh-keygen -Y sign -n capsule -f <its post key> R  ->  R.sig.<post>     (holders see R and R.L, never the secret)
POP    capsule-pop R (root unit):  the ring, k and cred are read FROM T (the signatures pin them all) -> >= k DISTINCT valid ring
       signatures -> git update-ref refs/capsule/C new T  (ONE CAS: the tip is the nonce, a replay loses) -> systemd-run the run cell of
       R.L with LoadCredentialEncrypted=s (systemd decrypts it ONLY into that unit's private $CREDENTIALS_DIRECTORY), DynamicUser,
       stdout + stderr = null  ->  the ledger commit holds R + the signers: the money-system part, one commit per pop
```
"Piped anywhere" = the run cell (`... < $CREDENTIALS_DIRECTORY/s`). The quorum signs H, the hash of that exact run cell, so WHERE it goes is the combined permission, and nothing else is.

**O.2 · The piece, whole: `capsule-pop` (1,194 B; weighted since O.8, 05:5xZ: plain k-of-n = every weight 1).** Not a config:engine piece: it lives in its own node (`config:capsule`, one read, with the seal line and the two unit stubs), so config:engine's depth 0+1 stays 4,095 B.
~~~sh
#!/bin/sh
# capsule-pop R: R = "C H T" (capsule, hash of the launch vector R.L, ledger tip). The ring, k and the sealed bytes are read FROM T, so the
# signatures pin all of them; the WEIGHTS of distinct ring signers (ring/<holder>@<w>, w=1 if absent) summing to k move refs/capsule/C T->new (one CAS: a replay loses), then L runs with C as its only credential
set -e;read -r c h t<"$1";x=.agi/capsule/$c;r=$(mktemp);trap 'rm -f $r $r.ok $r.c' EXIT;[ "$(git hash-object "$1.L")" = "$h" ]
g(){ echo "$t:$1"|git cat-file --batch --follow-symlinks|tail -n+2;};git ls-tree --name-only $t $x/ring/|while read f;do echo "${f##*/} namespaces=\"capsule\" $(g $f)";done>$r
for s in "$1".sig.*;do p=$(ssh-keygen -Y find-principals -s "$s" -f $r)&&ssh-keygen -Y verify -f $r -I "$p" -n capsule -s "$s"<"$1">/dev/null 2>&1&&echo "$p";done|sort -u>$r.ok
[ $(awk -F@ '{s+=NF>1?$NF:1}END{print s+0}' $r.ok) -ge $(git cat-file blob $t:$x/k) ];git update-ref refs/capsule/$c $(cat "$1" $r.ok|git commit-tree $t^{tree} -p $t) $t;git cat-file blob $t:$x/cred>$r.c
systemd-run -q --wait -p LoadCredentialEncrypted=s:$r.c -p DynamicUser=yes -p StandardOutput=null -p StandardError=null sh -c "$(jq -r .run "$1.L")"
~~~
**Tested 04:5xZ:** user manager, a scratch repo, three throwaway holder keys + one outsider, k = 2, a 19-byte dummy payload. The test copy differs only in `systemd-run --user`, `LoadCredential=` (plain) and no `DynamicUser` (the encrypted, system form is the root act below). No real key was touched.
| # | case | result |
|---|---|---|
| T1 | k-1 signatures | refused, tip unmoved, destination never ran |
| T2 | one holder signing twice | refused (distinct principals) |
| T3 | a holder + an outsider | refused (the outsider is not in the ring at T) |
| T4 | k signatures, then R.L swapped (`wc -c` -> `cat`) | refused (H mismatch) |
| T5 | k distinct holders | popped: the destination read exactly 19 B from a mode-500 private credentials dir; the tip moved; the ledger commit = R + `h1 h2` |
| T6 | the same R + signatures again | refused (rc 128: the CAS lost, the tip had moved) |
| T7 | the outsider added to the WORKTREE ring with k = 1 there | refused (ring and k are read from T) |
| T8 | the sealed bytes swapped in the worktree after signing | the destination got T's 19 B, not the worktree's 23 |
| -- | temp files after every run, pass or refusal | 0 (trap on EXIT) |
Two bugs caught by the tests, not by reading: (1) the first form read ring, k and cred from the worktree, so a signature did not pin them (T7/T8 now cover it); (2) `cat-file --batch` adds a newline, so the payload arrived as 20 B -> `cat-file blob` for cred and k.

**O.3 · Honest limits (belam asked for them; all measured or named):**
| claim | holds against | does NOT hold against |
|---|---|---|
| no holder can view | every holder, alone or in any group < k (they hold only signing keys) | ROOT on this box (it reads the host key; no TPM here) · a disk copy + root |
| no view at rest | the graph and its pushes (ciphertext only, authenticated) | a stolen host key |
| no view in transit | journal (null), argv (only paths and the run cell), swap (credentials dir is unswappable) | the DESTINATION process: it must see what it consumes |
| a pop goes only where the quorum said | any run cell other than the signed one (T4) | a quorum that signs a run cell that prints it (they signed WHERE; the ledger names them) |
| ring signature | -- | `ssh-keygen -Y` is MULTISIG: the ledger names each signer (accountability). An anonymous-among-n ring signature has no tool on the box: named, not built |
| survives a box loss | -- | the seal is BOX-BOUND: §P (self-perpetuating) = Shamir escrow, every box holding <= min(k-1, n-k) holder keys; a ring change ROTATES the secret, since an append-only graph cannot revoke an old share |

**O.4 · Chosen, and the alternative.** Seal = `systemd-creds` now: 0 B of crypto code, authenticated, and the destination gets it through systemd's own private, unswappable credentials dir. all-is-one's stdlib Shamir (561 B, 2^521-1, 3-of-5 tested; key by fd, never argv; openssl enc is NOT authenticated, so the signature check runs before decrypting) removes the single sealed blob at rest and is the escrow layer §P builds on. On ONE box both reduce to root; across boxes Shamir is the only one that survives.

**Unbuilt, named:** `capsule-pop@.path` on a sticky spool (holders drop `R.sig.<post>`; a k-1 drop just waits) + its service (the git identity for the ledger commit in its Environment) · a pre-receive line: only the pop unit's user moves `refs/capsule/*`, and a ring or k change is itself a pop (§P).
**Falsifiers.** **C1-C8** = T1-T8 (PASS, user manager) · **C9** the system form: `LoadCredentialEncrypted` under `DynamicUser` delivers the sealed bytes exactly, and `systemd-creds decrypt` as any post user fails (UNRUN: a root act, needs belam's or the owner's go) · **C10** a push moving `refs/capsule/C` from any user but the pop unit's is refused (UNRUN, unbuilt) · **C11** nothing of the payload in `journalctl`, `ps` or swap during a pop (UNRUN at root; null stdout/stderr measured in §N's analog).

**O.5 · The passkey route (owner 04:5xZ: "a route to pass it from iPhone to session trustlessly and automatically gives me a notification").** A passkey never leaves the phone, so the route carries the login's ONE-TIME CODE. With OAuth + PKCE (belam: VERIFY for Claude Code's login) that code is useless to any session but the one holding the verifier, so the code needs AUTHENTICITY and the right DESTINATION, not a seal. The council converged on this independently (all-is-one, self-perpetuating, alive); this is the merged form:
```
ASK     a post's login prints its authorize URL into its pane o (§N) -> an ask: /var/spool/agi/ask/<id> = "<post> <url>" (id = 18 random hex),
        + refs/capsule/asks/<id>/issued (all-is-one: never <id> beside <id>/used, a D/F conflict) -> NOTIFY the phone (the carrier is the
        owner's call, BANKED below)
APPROVE the owner taps the URL, passes the passkey in Safari: the passkey stays on the phone, the page shows the code
RETURN  the phone's SSH app: `ssh agi-capsule@<box> <id>`, the code on STDIN (never argv). authorized_keys: restrict,command="capsule-login"
        <the phone's key>: sshd checking that key IS the signature (k = 1, the owner device of §P); the line is projected from the graph,
        so it regrows on box loss (self-perpetuating)
POP     capsule-login: ONE atomic rename claims the ask (a used or racing id loses) -> printf the code + CR into the asking post's pane i
        -> the ledger line keeps post, id, time, NEVER the code -> refs/capsule/asks/<id>/used (create-only)
```
`capsule-login` (692 B; the code pinned to a URL-safe line of <= 512 B, all-is-one 05:0xZ):
~~~sh
#!/bin/sh
# capsule-login, run ONLY as authorized_keys `restrict,command="capsule-login" <owner device key>` (sshd checking that key IS the approval, k=1):
# ssh <box> <ask-id>, ONE line on stdin -> the asking post's pane. The claim is one atomic rename (a used or racing id loses); the code is never at rest
d=${AGI_SPOOL:-/var/spool/agi};i=$SSH_ORIGINAL_COMMAND;case $i in ''|*[!a-z0-9]*)exit 2;;esac;mv $d/ask/$i $d/used/$i 2>/dev/null||exit 3
read -r p u<$d/used/$i;case $p in ''|*[!a-z0-9-]*)exit 2;;esac;IFS= read -r c;case $c in ''|*[!A-Za-z0-9._~#-]*)exit 4;;esac;[ ${#c} -le 512 ]||exit 4;printf '%s\r' "$c">${AGI_RUN:-/run}/agi-$p/i
echo "login $p $i $(date -u +%FT%TZ)">>$d/ledger
~~~
**Tested 04:5xZ** with a scratch sshd as an ordinary user on a localhost-only port, a throwaway "phone" key, the §N pane in a transient user unit and a random dummy code; sshd, unit and port were all gone after (0 left):
| # | case | result |
|---|---|---|
| P1 | the phone key + an open ask | the code typed into the pane once |
| P2 | any other key | refused by sshd (rc 255) |
| P3 | a used or unknown ask id | refused (rc 3), and nothing on stderr (the first form echoed the spool path: fixed) |
| P4 | the phone key asking for another command, a shell or a pty | refused (rc 2 / rc 255): `restrict` + the forced command |
| P5 | the code anywhere at rest: spool, ledger, sshd log, journal | 0 copies (only the destination's own pane transcript o, mode 600) |
| P6 | a path-traversal id | refused (rc 2) |
| P7 | two pops of one ask at the same instant | typed exactly once, one ledger line, the other rc 3 |
**Not the inbox (a disagreement, kept on purpose):** routing the code through the inbox spool would put it in a file, and it would let the inbox type ARBITRARY text into a pane; §N keeps the inbox to the single word `mail`. So the code goes straight to `i`. The price, named: `i` must be writable by the `agi-capsule` user: `ExecStartPre=+` chgrp + mode 620 on `i` in agi-post@ (~60 B, a root act, unrun).
**BANKED for the owner, the notification carrier:** (a) the SSH app's routine POLLS `ssh agi-capsule@<box> asks` (no provider added; all-is-one's and my recommendation; VERIFY the app can run routines and notify) · (b) a self-hosted push server (ntfy-style; a new service) · (c) the owner's own App Store app with APNs (the dev plan; the heaviest) · (d) a logged-in Claude Code post's own push notification to the owner's Claude app (0 B; VERIFY that it can carry the URL).
**Falsifiers.** P1-P7 PASS (user-level analog) · **P11** PASS (all-is-one: without the pin, the phone key + an open ask could type ANY line, a prompt, into a live agent): a prompt with spaces, a quote, an escape byte, 513 chars, an empty line = rc 4 and nothing reaches i; `code#state` passes (VERIFY the real charset at P8); a refused try still spends its ask · **P8** a real Claude Code login: the authorize URL is readable from o (the TUI may wrap it), and the pasted code + CR completes the login (UNRUN: needs the owner and a post at its login prompt) · **P9** a code replayed into a DIFFERENT session's login fails (PKCE; UNRUN) · **P10** the phone's SSH app holds a Secure Enclave key sshd accepts (VERIFY on the phone; this box offers ecdsa-sha2-nistp256 and sk- keys).

**O.6 · The seal through vector math (owner 04:59Z).** belam named it: a good basis that makes the closest-point walk easy and a public bad basis that makes it infeasible IS lattice cryptography, standardized as ML-KEM (FIPS 203) and ML-DSA (FIPS 204). GGH, the first good/bad-basis scheme, was broken by structure it leaked (Nguyen 1999). That is exactly the owner's "new symmetries" worry, so extra home-made dimensions are NOT proposed: the PRIMITIVE stays a standard one, and the VECTOR stays the representation (§M).
| question | measured on this box (05:0xZ) | so |
|---|---|---|
| is lattice math already in the route? | OpenSSH 9.6 offers `sntrup761x25519-sha512` (NTRU Prime lattice + X25519 hybrid), OpenSSH's default since 9.0 | the passkey route's transport (O.5) is lattice-hybrid TODAY, 0 B, when the phone's SSH app negotiates it (VERIFY) |
| a lattice seal at rest? | no ML-KEM in OpenSSL 3.0.13, none in python cryptography 41.0.7; no ML-DSA in `ssh -Q sig` | a package (liboqs, or OpenSSL >= 3.5) = the owner's go; it fits keys meant to live for years, not a code that dies in minutes |
| what is quantum-exposed in §O + §P? | the seal is AES-256-GCM (symmetric: Grover only halves it); Shamir shares are information-theoretic; the quorum signs with ed25519, which rotates; the ESCROW share is wrapped to X25519 and lives in git forever | the ONE piece that must be post-quantum now is the escrow share wrap (harvest-now-decrypt-later): hybrid X25519 + ML-KEM-768, §P.7 (self-perpetuating); ML-DSA for ring signatures later, when OpenSSH ships it |
| seed it with the post's activations, thermal noise, time? | the kernel CSPRNG already mixes hardware noise (entropy_avail 256 = a seeded pool); activations are reproducible from weights + inputs; timestamps are guessable | neither is secret entropy. An activation fingerprint may enter as a BINDING input (KDF info: this key belongs to THIS post), never as the randomness |
"Several more dimensions just in case": security comes from the standard parameter set (ML-KEM-768: module rank 3, n = 256); extra dimensions in a custom scheme add structure, never margin (all-is-one). Activations may BIND a short-lived key (HKDF info, e.g. the §L launch-vector hash) but never be needed to OPEN a long-lived one: the model changes over generations and the key would die with it (self-perpetuating).
**Falsifier V-L1:** a capsule sealed with ML-KEM under a package the owner approves round-trips byte-exact, and the same quorum flow (T1-T8) passes unchanged with ML-DSA ring signatures (UNRUN: needs the package).

**O.7 · The Secure Enclave as the anchor (owner 05:30Z: "could I borrow my iPhone 14s secure chip ... For true, system-invisible, obfuscation? I also have access to a MacBook Air").** What the chip does (belam, VERIFY on the devices): a P-256 key that never leaves it, used per Face ID / Touch ID, for ECDSA signing and ECDH. It keeps the KEY invisible, never the payload: whatever it unlocks, the destination still sees (O.3 stands at pop). Two facts decide the design: an SSH app can only SIGN with such a key, and an ECDSA signature is randomized, so no stable key can be derived from one; wrapping a seal therefore needs the chip's ECDH, i.e. a few lines of device code. The council split it by job (all-is-one), one device each:
```
iPHONE  the APPROVER: its SE-backed SSH key = a ring holder; signing the pop (§O.2) or logging in to agi-capsule (O.5) IS the approval;
        with the SSH app's background run, carrier (a) works: it polls `asks` and alerts (VERIFY: the app can hold an SE-backed key)
MAC     a CUSTODY holder, the missing TPM: the inner seal is wrapped to its SE key; only its ECDH result Z opens it, after Touch ID.
        Device code = ~40 lines of Swift over CryptoKit SecureEnclave.P256.KeyAgreement, run with the Command Line Tools: no App Store,
        no review (the iPhone would need a small app on the dev plan for the same job)
BOX     custody = BOTH: outer = the host-key seal (systemd-creds), inner = se-wrap to the Mac's key, so neither box root nor the Mac
        (with its own root) opens it alone -> the ask carries the ephemeral point -> the Mac returns Z over SSH (a forced command, like
        capsule-login; transport = sntrup761x25519, O.6) -> the box opens it for ONE pop; Z, the key and the plaintext die with the pop
```
`se-wrap` (1,277 B, python3 + the cryptography package already on the box; AES-256-GCM, so a flipped bit is refused, which `openssl enc` cannot give):
~~~python
#!/usr/bin/env python3
# se-wrap seal DEV.pub <secret >capsule | se-wrap ask CAPSULE (prints the ephemeral point for the device) | se-wrap open CAPSULE <Z >secret
# The capsule is sealed to a Secure Enclave P-256 key: box root cannot open it at rest; only Z = ECDH(SE key, the ephemeral point), which the
# device computes after Face ID / Touch ID, opens it. Z dies with the pop. The device runs plain ECDH, no code of ours beyond returning Z.
import sys,os;from cryptography.hazmat.primitives.asymmetric import ec;from cryptography.hazmat.primitives import hashes,serialization as s
from cryptography.hazmat.primitives.kdf.hkdf import HKDF;from cryptography.hazmat.primitives.ciphers.aead import AESGCM
P=s.Encoding.X962,s.PublicFormat.UncompressedPoint;k=lambda z:HKDF(hashes.SHA256(),32,None,b"agi-capsule").derive(z);a,f=sys.argv[1:3]
if a=="seal":
 e=ec.generate_private_key(ec.SECP256R1());d=s.load_pem_public_key(open(f,"rb").read());n=os.urandom(12);E=e.public_key().public_bytes(*P)
 sys.stdout.buffer.write(E+n+AESGCM(k(e.exchange(ec.ECDH(),d))).encrypt(n,sys.stdin.buffer.read(),E))
else:
 c=open(f,"rb").read();E,n,x=c[:65],c[65:77],c[77:]
 if a=="ask":print(E.hex())
 else:sys.stdout.buffer.write(AESGCM(k(bytes.fromhex(sys.stdin.read().strip()))).decrypt(n,x,E))
~~~
**Tested 05:3xZ, unprivileged:** a software P-256 key stands in for the Secure Enclave (the same curve and the same ECDH math; CryptoKit on the chip must produce the same Z: VERIFY):
| # | case | result |
|---|---|---|
| E1 | a P-256 ring key (the SE shape, `ecdsa-sha2-nistp256`) in capsule-pop's ring, k = 2 | alone: refused · with an ed25519 holder: popped exactly 19 B; the ledger names `h2 mac` |
| E2a | the sealed capsule (112 B) | 0 plaintext bytes in it; the device's Z opens it exactly |
| E2b | another device's Z | refused (InvalidTag) |
| E2c | box root holding every file, guessing Z | refused: at rest, the box alone cannot open it |
| E2d | one flipped ciphertext bit | refused (authenticated) |
**APPROVAL ring != CUSTODY ring (all-is-one, on self-perpetuating's correction):** approval = [iPhone, Mac], k = 1 (one human's consent from either device; losing one bricks nothing). Custody = the host key AND the Mac SE (two domains, 2-of-2) for the live seal, plus the §P escrow (k >= 2 across failure domains) as the regrow path. The Mac SE alone must never unwrap: with Z and the public ciphertext, that Mac's root could open it. **What changes, and what it costs (self-perpetuating):** at rest, a disk copy + box root is no longer enough, nor is the Mac alone (O.3's first row narrows to "a live root on the box DURING a pop"). The price: the key is NON-EXPORTABLE, so a lost or replaced Mac is a HOLDER LOSS, and an SE-wrapped seal dies with it. So the §P escrow becomes MANDATORY for any SE-wrapped capsule, with a k that never needs that same device; a new device enters by a ring change (a pop into the rotate route, P.6). Suggested ring 3-of-5 = iPhone + Mac + 2 posts here + 1 post on another town box (per domain <= min(k-1, n-k) = 2: passes). The SE's P-256 is not post-quantum: fine for approvals checked within minutes; an escrow share sealed to an SE key stays classical until the P.7 hybrid exists. systemd-creds stays for capsules that must open with no tap.
**BANKED for the owner:** (1) the at-rest anchor: the Mac (recommended: a local Swift CLI, no App Store) or the iPhone (a small app) · (2) switch a given capsule from the host-key seal to the SE seal (a tap per pop, escrow mandatory) or keep the host key for it.
**Falsifiers.** E1, E2a-d PASS (software stand-in) · **S1** the real Mac SE's Z for a test vector equals the software ECDH of the same keys (VERIFY on the Mac) · **S2** a pop of an SE-wrapped capsule with the Mac asleep WAITS, even with the phone's approval: approval and unwrap are two taps, named as such · **S3** the iPhone lost: the Mac approves (k = 1), and custody still needs the host key AND the Mac's Z; the Mac lost: the escrow (k >= 2, never needing the Mac) regrows the seal (§P) · **S5** the Mac alone, holding Z and the git ciphertext, cannot open a 2-of-2 capsule (the outer host-key seal; UNRUN: a root act for the outer seal) · **S4** the SSH app holds an SE-backed key that sshd accepts (= P10).

**O.8 · The owner's picks (05:45Z) folded in: the iPhone alone, a MUTUAL quorum, an iMessage face.** Owner, verbatim: "1. iPhone only for now I don’t have the Mac with me. If not just plain key stored in iPhone as capsule signed by posts. So my capsule only pops with you all, yours only with mine assuming you let me unlock mine. I’m fine with a small app having to be released. I’m already dropping a list app soon. Can this be a messenger extension as well so it can just text receive responses via text not just terminus. Notification through app that opens response in text via iMessage applet. / 2. Works for me, if needed can use 2-2 setup to do passkey passing or just use ssh I guess. (belam's rulings (1)-(2) on the goal).
```
CUSTODY + APPROVAL  the iPhone ONLY: O.7's Mac row moves to a small owner app (the owner's list app may carry it): CryptoKit Secure
                    Enclave P-256 = signing (the approval) + ECDH (the inner seal of a 2-of-2 capsule). No app yet -> a PLAIN key in
                    the iPhone's keychain, itself kept in a capsule the posts sign (a lost phone is recovered by the posts' quorum);
                    named honestly: a plain key is visible to iOS, the Secure Enclave guarantee starts with the app
MUTUAL QUORUM       all-is-one's weights, ONE formula, ONE line in capsule-pop: ring/<holder>@<w>, k = the threshold; it pops iff
                    the weights of the distinct valid signers sum to k (no @w = 1, so plain k-of-n is unchanged)
                    the POSTS' capsules: owner@(n+1), posts @1, k = n+1+m  -> the owner AND >= m posts; no number of posts suffices
                    the OWNER's capsule: everyone @1, k = 1+n               -> "only pops with you all"
iMESSAGE            the app's iMessage extension is the FACE: the push opens the ask in Messages, the owner taps approve there;
                    the approval still LEAVES by the app's own call to the box (SSH to agi-capsule, O.5), never as a text: the box
                    reads no iMessage, and a text reply is an unauthenticated channel
SEAL PER CAPSULE    long-lived secrets = the 2-of-2 (host key AND the iPhone SE); short login codes = O.5 over plain SSH (ruling 2)
```
**Tested 05:5xZ** (weighted capsule-pop, user manager, four throwaway keys, the 19-byte dummy):
| # | capsule | signers | result |
|---|---|---|---|
| Q1 | posts' (owner@4, p1-p3 @1, k = 6) | all three posts, no owner | refused (3 < 6) |
| Q2 | posts' | owner + 1 post | refused (5 < 6) |
| Q3 | posts' | owner + 2 posts | popped, 19 B |
| Q4 | posts' | p1 + p2, after `p1@9` was written into the WORKTREE ring | refused: weights are read from the signed tip (T7 holds) |
| Q5 | owner's (all @1, k = 4) | owner + 2 posts | refused |
| Q6 | owner's | owner + all 3 posts | popped, 19 B |
| T1/T5 | plain (p1-p3, k = 2) | 1 / 2 signers | refused / popped: unchanged |
**Falsifiers.** Q1-Q6 PASS · **I1** the app's Secure Enclave signature verifies under `ssh-keygen -Y verify` (the app must emit SSHSIG; VERIFY) · **I2** the iMessage extension reaches its app's Secure Enclave key (a shared keychain group; VERIFY) · **I3** the iPhone lost: the posts' quorum pops the escrowed plain key, or §P's escrow regrows a 2-of-2 seal without that phone (UNRUN).

## P · CAPSULE · self-perpetuating -- the capsule regrows: reseal after a box loss, rekey when the ring changes
**What am I ACTUALLY trying to get the machine to do here?** Make a sealed secret outlive the box that sealed it, without ever letting one holder, or one box, see it ("If I die, let nothing be lost").

```
seal     secret ─┬─▶ systemd-creds encrypt ─▶ capsule.cred        BOX-BOUND: the fast pop on this box (§O)
                 └─▶ esc split K <holder pubs> ─▶ escrow           N sealed shares + a check line, committed beside it: SURVIVES the box
box lost ─▶ a new box: seed + graph regrow the body (§C) ─▶ K holders each run `esc open <own key>` on THEIR line
         ─▶ the shares stream into capsule-reseal (a root unit): esc join │ check │ systemd-creds encrypt ─▶ a new capsule.cred ─▶ ledger commit
ring changes ─▶ REKEY = ROTATE the secret: a pop into a destination that mints a new one at its provider and revokes the old,
               then seal + split to the NEW ring (re-splitting the same secret revokes nobody: see P.3)
```

**P.1 · Measured 04:5xZ on this box (unprivileged, throwaway X25519 holder keys, a secret starting with two zero bytes):**
| claim | result |
|---|---|
| 3 of 5 holders rebuild the secret | byte-exact (`cmp`), and the check line matches |
| 2 of 5 holders | cannot (Shamir: K-1 points on a random degree-(K-1) polynomial carry no information) |
| a holder opens another holder's line | `InvalidTag`: each line opens only under its own key |
| what a holder ever sees | one point `i:y`, never the secret |
| the seal on THIS box | `systemd-creds has-tpm2` = partial (no TPM firmware or driver), so the seal is host-key ONLY: root, or a copy of the host secret plus the capsule, reads it |
| an unprivileged reseal | refused ("Permission denied" on the host secret; systemd 255 has no `--user` creds), so capsule-reseal is a root unit (on go) |

**P.2 · The ring has to span failure domains: the math.** With K-of-N and holder keys spread over boxes, **every box must hold at most min(K-1, N-K) holder keys**. The K-1 bound: no box's root can combine alone. The N-K bound: losing any one box still leaves K holders. So 3-of-5 needs at least 3 failure domains. `ring-ok` checks it (117 B): 2/2/1 passes · 3 on one box fails · **all 5 on this box fails, and that is today.** Every post key lives on ONE box, so the per-post keys alone (the draft's RING) cannot be the ring. Holders must include keys off this box: the owner's device(s), a post on another town's box, a hardware key. **Who holds is the owner's call (banked).**

**P.3 · Rekey cannot revoke in an append-only graph.** A retired escrow line stays in git history, so the OLD holders can still open and join it forever. A ring change therefore means **rotating the secret at its source** (a pop into a destination that mints a new key and revokes the old one at the provider). A secret that cannot be rotated (a seed phrase) keeps its first quorum for life, so choose K and N for those once, and carefully.

**P.4 · Honest limits.** At join time the secret exists in capsule-reseal's memory on the NEW box, so that box's root sees it (the same limit as §O's destination). The check line is sha256(secret): fine for high-entropy keys, but a brute-force oracle for a low-entropy one, so capsules hold keys, never passwords. TPM sealing adds nothing against box LOSS (it is box-bound by design); it only raises the bar against a disk copy, and this box has none.

**P.5 · Bytes, kept out of the engine's one read.** `esc` 1,190 B (python3 + the installed `cryptography`: X25519 + ChaCha20-Poly1305 per share, Shamir over 2^521-1) · `ring-ok` 117 B · capsule-reseal ~0.2 KB (unwritten; root). About 1.5 KB in its own `.geometry` node (`config:capsule`), so config:engine's depth 0+1 stays at 4,095 B. Off-shelf alternative: `age` with ssh-ed25519 recipients would reuse the post keys as share keys. It is not installed (a root act).

**P.6 · Fitted to §O, and the two items §O left unbuilt, owned here.** The escrow lives beside the capsule, at `.agi/capsule/C/escrow` (one line per holder, plus the check line), and is read FROM the ledger tip T like the ring. Shares need an ENCRYPTION key, while §O's ring points at ssh SIGNING keys, so each holder carries one more file, `keys/<post>.x25519` (32 B public), beside its ssh key (`age` would derive it from the ssh key instead: not installed). **(1) Only the pop unit moves `refs/capsule/*`: 0 B, the kernel.** `refs/capsule/` is a ref directory owned by the pop unit's user, so §B's property rule applies: an `update-ref` from any other uid fails with "Permission denied" (measured in §B, F2). No pre-receive line is needed. **(2) A ring or k change IS a pop.** Its destination is a `rotate` launch (one NEW §L route line, ~120 B): it mints the new secret at the provider, revokes the old one, writes the new ring + k + escrow under the new tip, and seals. One quorum act covers rekey and rotation together, so a ring can never change without the secret changing (P.3).

**P.7 · The seal through vector math (owner 04:59Z), through the generations lens.** belam's read stands: lattice cryptography (ML-KEM, FIPS 203 / ML-DSA, FIPS 204) as the PRIMITIVE, never a home-made good-basis/bad-basis variant (GGH broke through leaked structure, which is the owner's own "new symmetries" worry). The vector is the REPRESENTATION. Two points only the generations lens adds:
- **Only the escrow wrapping must be post-quantum, and NOW.** Escrow ciphertext is committed, and git never forgets, so a future quantum adversary can harvest today's X25519-wrapped shares and open them decades later. Everything else is safe or replaceable: Shamir is information-theoretic (quantum gains nothing) · the systemd-creds seal is symmetric (AES-256-GCM) · signatures and ring keys ROTATE (a forged signature after rotation moves nothing, because the ledger tip is the nonce). So the one place a lattice KEM earns its bytes is a **hybrid X25519 + ML-KEM-768 wrap of each share** (both must break). Measured on this box: OpenSSL 3.0.13 has no ML-KEM, python `cryptography` 41 has none, liboqs is absent; the only post-quantum primitive present is OpenSSH's `sntrup761x25519` key exchange, which already protects the phone's SSH channel (the passkey route). Hybrid escrow therefore waits on one package (OpenSSL >= 3.5, or liboqs, or age with its hybrid recipients: VERIFY) = a root act, the owner's go. Until then, state it: the shares are classical-only.
- **Activations bind, never open** a long-lived key (quoted in O.6): F31 below tests it.
- **The phone holder opens its own share ON the phone** (O.5): iOS CryptoKit's Curve25519 key agreement + ChaChaPoly is esc's construction, so the phone needs a tiny app, not a box. A box that opened the phone's share beside its own two would hold k = 3 alone (P.2). Which holder keys, and whether the owner's dev plan builds that app, are the owner's calls (banked).
Falsifiers: **F30** a share wrapped hybrid opens only when BOTH the X25519 and the ML-KEM secret are present (on go: needs the package) · **F31** an escrow line opens on a box running a DIFFERENT model with the same holder key (the activation fingerprint is not on the opening path).

**P.8 · Custody = the iPhone ONLY, the quorum MUTUAL (owner 05:45Z): the escrow becomes 2-of-2 over (the iPhone, the posts' quorum), `esc` run twice; the Mac leaves the ring.**
```
seal   secret ─▶ esc split 2 iphone.pub E.pub ─▶ escrow           E = a fresh X25519 key per capsule; E.key is never stored whole
       E.key  ─▶ esc split k post1.pub .. postN.pub ─▶ escrow-E  the posts' half: k-of-n over the post keys
open   k posts: open + join ─▶ E.key ─▶ opens E's line  ┐
       the iPhone opens ITS line ON the phone (the app) ─┴▶ esc join ─▶ secret   (neither half alone carries a bit: Shamir 2-of-2)
```
| claim (05:5xZ, throwaway keys: iPhone = a P-256 'enclave' key, posts b c d, k = 2) | result |
|---|---|
| 2 of 3 posts rebuild E · E + the iPhone's share rebuild the secret | yes · byte-exact |
| the iPhone alone · all 3 posts without the iPhone · 1 post | no · no · no |
| the iPhone's share wrapped to a P-256 key (the Secure Enclave's only curve), opened by a stand-in for the app (ECDH with the SE key -> SHA-256 -> ChaChaPoly, = CryptoKit) | byte-exact |
| an escrow made by the old `esc` opens under the new one | yes |
- **`esc` grows +363 B** (1,384 -> 1,747 on this copy): `split` wraps to P-256 when the holder's public key is 65 B (uncompressed point, what the SE exports), else X25519. `open` is unchanged: the SE key never leaves the phone, so the box never opens a P-256 share; the app does. Lives in config:capsule, outside the zygote. Bytes per capsule: escrow 682 B + escrow-E 920 B (3 posts).
- **Box loss under mutual custody.** The iPhone's half lives off-box; E survives only if the post keys span boxes, so `ring-ok` now applies to the posts' half ALONE (per box <= min(k-1, n-k)). With every post key on this box (F27), losing the box loses E, so the capsule is lost: acceptable for a secret that rotates at its provider (P.3: re-mint), NOT for one that cannot. **Rule until a second town box holds post keys: capsules hold rotatable secrets only.**
- **Answers two BANKED owner questions** (my card): the ring holder = the iPhone via the owner's app (not 3-of-5 across devices); the phone opens its own share in the app (the 'tiny app' branch). The app's job here is ONE call: ECDH(SE key, the line's 65-B point) -> SHA-256 -> ChaChaPoly.open -> send `i:y` back over the O.5 route.
Falsifiers: **F38** the escrow table above (PASS) · **F39** the real app opens an SE-wrapped line made by `esc split` (unrun: needs the owner's app) · **F27** stays FAILED by design until a second box holds post keys.

Falsifiers: **F26** box loss (on a throwaway box): delete capsule.cred and the host secret; K holders rebuild byte-exact and reseal, K-1 cannot (the escrow half PASSES today; the reseal is on go) · **F27** `ring-ok K` over the live ring exits 0 (FAILS today, by design: every key is on one box) · **F28** after a ring change, the old holders' K shares from git history rebuild the OLD secret and its provider refuses it · **F29** a holder opening another holder's line -> InvalidTag (PASS).

`esc` whole (1,190 B counted):
```python
#!/usr/bin/env python3
# esc split K PUB.. <secret >escrow | esc open KEY <escrow-line | esc join <shares: Shamir K-of-N over 2^521-1, each share sealed to ONE holder (X25519+ChaCha20-Poly1305)
import sys,os,hashlib,base64 as B;from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P;from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C
p=2**521-1;a=sys.argv;v=a[1];r=lambda b:P.from_public_bytes(b);h=lambda x:hashlib.sha256(x).digest()
if v=='split':
 s=sys.stdin.buffer.read();k=int(a[2]);c=[int.from_bytes(b'\1'+s,'big')]+[int.from_bytes(os.urandom(65),'big')%p for _ in range(k-1)];print('check',h(s).hex())
 for i,f in enumerate(a[3:],1):
  e=K.generate();q=r(B.b64decode(open(f).read()));y=sum(x*pow(i,j,p) for j,x in enumerate(c))%p;print(f,B.b64encode(e.public_key().public_bytes_raw()+C(h(e.exchange(q))).encrypt(bytes(12),f'{i}:{y}'.encode(),None)).decode())
if v=='open':
 d=K.from_private_bytes(B.b64decode(open(a[2]).read()));z=B.b64decode(sys.stdin.read().split()[1]);print(C(h(d.exchange(r(z[:32])))).decrypt(bytes(12),z[32:],None).decode())
if v=='join':
 S=[tuple(map(int,l.split(':'))) for l in sys.stdin.read().split()];s=0
 for i,y in S:
  n=d=1
  for j,_ in S:
   if j!=i:n=n*-j%p;d=d*(i-j)%p
  s=(s+y*n*pow(d,-1,p))%p
 sys.stdout.buffer.write(s.to_bytes((s.bit_length()+7)//8,'big')[1:])
```
`ring-ok` whole (117 B counted):
```sh
#!/bin/sh
# ring-ok K <ring (lines: holder box): every box holds <= min(K-1, N-K) holder keys -- no box can pop alone, and losing any one box leaves >= K
awk -v k=$1 '{n++;b[$2]++}END{m=k-1<n-k?k-1:n-k;for(x in b)if(b[x]>m){print "box "x" holds "b[x]" > "m;e=1};exit e}'
```

## Q · ROUND 5 · self-perpetuating -- the ZYGOTE: config:engine keeps the code that runs before any post exists; the body it grows is EXPANSION, read at the same REV
**Owner 05:38Z:** "the expanded vectors for live posts and post wrappers can be bigger than 8kb I just mean the 'bootstrap' package is under 8kb". **What am I ACTUALLY trying to get the machine to do here?** Regrow every post from one small read. A seed does not carry the organism: it carries the code that builds it and reads the rest from where it lands. Here that is the graph at the same REV, which `sect` already reads. So the cut is a rule, not a squeeze:
```
ZYGOTE    = the code that runs before any post exists + the map (diagram · loop · one line per piece, all 25)
EXPANSION = every file that code writes and everything a post runs: read with sect @REV, extracted whole into the post's bin
config:engine        7,342 B  ZYGOTE: diagram · loop · 25 piece lines · sect · agi-project · agi-gate            (v4c: 16,384)
config:engine-post   7,671 B  the body: agi-post@.service · agi-brief · brief.py · agi-meter · agi-turn · agi-link · agi-wt
                              · agi-track · agi-flush · gitconfig · signers · sysusers.conf · agi.rules · project.sh · observe.sh · tick.sh · agi-frontier
config:engine-wrap   3,817 B  the post wrappers: agi-run · settings.json · cccc.ts · agi-kid · agi-infer (05:50Z, below)
total               18,830 B  (cap 20,480) · zygote headroom 850 B · gone: none · every other piece byte-identical to v4c
```
**The only code changes** (v4c -> v5; the new expansion nodes are v4c's sections cut whole, by the map above):
| piece | change | bytes |
|---|---|---|
| sect | reads EVERY `.geometry/engine*.md` at REV: `r=${2:-HEAD};git ls-tree --name-only $r .agi/nodes/.geometry/\|grep "/engine[^/]*\.md$"\|sed "s\|^\|$r:\|"\|git cat-file --batch --follow-symlinks\|sed -n` + v4c's range; no caller changes | 149 -> 202 |
| agi-project | `s()` = the same read; after writing the unit: `[ -s $o/agi-post@.service ]\|\|exit 3` (a missing expansion fails loud) | 1679 -> 1833 |
| agi-gate | first line: `git grep -ho "^### [^ ]*" $1 -- ".agi/nodes/.geometry/engine*.md"\|sort\|uniq -d\|grep -q .&&exit 2` (one name, one piece) | 276 -> 373 |
| agi-post@.service | `e=...engine.md;for x in ...;done;` -> `for e in t/.agi/nodes/.geometry/engine*.md;do for x in ...;done;done;`, each range ending at `^##` (alive R3: a fenced table after a node's last piece no longer bleeds into it; re-tested) -- bare `$e`, never `${e}`: systemd 255 empties `${x}` even inside `sh -c '...'` (measured: `x=[5] br=[]`) | 1252 -> 1266 |
| diagram | +1 line: `ZYGOTE = this read ... ──sect @REV──▶ EXPANSION: config:engine-post · config:engine-wrap` | +128 |

**Tested 05:4xZ** (`--shared` scratch clone, rows zz-claude / zz-pi / zz-off on another box; commit A = v4c, C = v5; no root, no unit started, MAIN untouched):
| claim | result |
|---|---|
| sect parity: v4c `sect X A` vs v5 `sect X C`, all 24 names + diagram + loop | 21 byte-identical; the 5 that differ are the 4 edited pieces + diagram |
| projection parity: v4c agi-project @A vs v5 @C | 9 files each; zz-off skipped; users, h.conf drop-ins, .path identical; the units differ ONLY in the extraction loop |
| a post's bin: v4c extraction vs v5 extraction | 24 files each; only sect, agi-project, agi-post@.service differ |
| gate: good tip · engine-post missing · a duplicate name | 0 · 1 · 2 |

**Why the wrappers stay whole per post:** `cccc.ts` is not pi-only: `agi-kid` loads it in EVERY post (a claude post spawns pi kids). Narrowing the wrap per harness is free later (expansion bytes are not capped) and saves nothing in the zygote. **Seeds not taken, on purpose:** cells + ONE projector for the key=value units, and one brief, shrink the EXPANSION, not the zygote, and each rewrites a piece whose parity rows are proven: take them when a parity row needs touching anyway. **The zygote's next cut, if 8 KB gets tight:** agi-project's three printf blocks (agi-project.service, .path, h.conf, ~900 B) become cells in config:engine-post read by the same `s()`; est. -500 B, unmeasured.

**RAW INFERENCE (owner 05:50Z) = `agi-infer`, 549 B, in config:engine-wrap; the zygote pays one index line.** One call to any OpenAI-compatible `/v1/chat/completions`: prompt on stdin, reply on stdout. Three engine cells, projected as env by the projector that exists (no projector change): `infer_url` (local llama.cpp `http://127.0.0.1:8080/v1` = the default; OpenRouter; the xAI API) · `infer_model` · `infer_key` = the NAME of a variable, never a key. **Where the key comes from:** the unit's root-owned `EnvironmentFile=-/var/lib/agi/%i.env` (already in agi-post@.service), never `.env`, never a node; it reaches curl through a 0600 header file (`printf` is a shell builtin, so the key is in no argv and never in `ps`), removed on exit. A row without `infer_key` sends no Authorization header (local). No SuperGrok wiring (belam: a consumer plan, not an API); xAI API credits = a spend the owner names. As a launch route (§L) it is one line: `{"name":"infer","harness":"agi-infer <$AGI_TASK","time":"300"}`.
```sh
#!/bin/sh
# agi-infer [MODEL] <prompt: ONE call to any OpenAI-compatible /v1/chat/completions; cells infer_url, infer_model, infer_key (the NAME of a var in the unit's EnvironmentFile)
h=$(mktemp);trap 'rm -f $h' 0;[ "$AGI_INFER_KEY" ]&&printf 'Authorization: Bearer %s\n' "$(printenv $AGI_INFER_KEY)">$h
jq -Rsc --arg m "${1:-$AGI_INFER_MODEL}" '{model:$m,messages:[{role:"user",content:.}]}'|curl -sf -H @$h -H 'Content-Type: application/json' -d @- ${AGI_INFER_URL:-http://127.0.0.1:8080/v1}/chat/completions|jq -er '.choices[0].message.content'
```
Tested (a stub OpenAI-compatible server on loopback; a throwaway key): the request hits `/v1/chat/completions` with `{model, messages:[{role:user, content}]}` and quotes, `$` and backticks intact · `agi-infer other/model` overrides the cell · key cell set -> `Bearer <key>`; unset -> no header (the first draft leaked `$_` as the bearer: `printenv ${X:-_}`; fixed) · unreachable endpoint -> rc 4 · 0 temp files left · `sect agi-infer` byte-exact from the wrap node · gate 0. **F37** the same call against the town's local llama.cpp and one free OpenRouter model returns text (unrun: no live endpoint touched in a design round).

Falsifiers: **F32** `wc -c` config:engine <= 8,192 (7,263) · **F33** sect parity as in the table (PASS) · **F34** projection parity (PASS) · **F35** gate 0/1/2 (PASS) · **F36** on DG3's stage-2 post: its bin under v5 = its bin under v4c except the 3 edited pieces (unrun). Drafts: /tmp/g71611/r5/v5 (scratch; rebuildable from v4c by the map + the 5 edits above + agi-infer).

## R · ROUND 5 · alive -- VARIANT B of §Q, written in parallel (05:5xZ): a 5.7 KB bootstrap with the map split across nodes. Recommended = §Q (the whole 24-line map stays in the one read) + two hardenings measured here: the gate refuses an empty unit template (R4c, a v4c gap) and ranges end at ^## (0 B; R3)
**Owner 05:38Z:** "Our engine code is getting too large. Do we need to offload more of it into the math somehow? Rethink things or recompose them? We can go up to 20kb while needed but ideally I'd want it back under 8kb when possible via another simplification redesign. Mind you the expanded vectors for live posts and post wrappers can be bigger than 8kb I just mean the 'bootstrap' package is under 8kb you get it?" **What am I ACTUALLY trying to get the machine to do?** Make the one read that a box needs to come alive small, and let everything a post runs be fetched by NAME only when it is needed, with no piece rewritten (so parity holds by construction, and is then measured, not argued).

**Q.1 · The redesign is one idea: the engine is a SET of nodes, and `sect` is the only resolver.** `config:engine` (`engine.md`) = the BOOTSTRAP (diagram · loop · pieces table · `sect` · `agi-project` · `agi-gate`). `engine-post.md`, `engine-cc.md` and `engine-pi.md` = the EXPANSIONS. Every reader that named `engine.md` now reads `.geometry/engine*.md` at the REV, so a piece is found by name wherever it lives; adding an expansion = a new `engine-<x>.md` + one line in the bootstrap's pieces table, no code. Only FOUR pieces change (the readers); the other 20 move byte for byte.
| node | bytes | holds |
|---|---|---|
| **config:engine (BOOTSTRAP)** | **5,731** (target 8,192; v4c 16,384) | diagram, loop, pieces table (3 pieces + 3 expansion lines), sect, agi-project, agi-gate, THOUGHT |
| config:engine-post | 9,080 | the post body: unit, pane, meter, turn, links, trees, brief, tick (18 pieces) |
| config:engine-pi | 2,548 | cccc.ts + agi-kid: loaded only by a pi post |
| config:engine-cc | 670 | settings.json: loaded only by a Claude Code post |
| total | 18,029 | +1,645 B vs v4c: three frontmatters, three tables, the four readers (+361 B) |

**Q.2 · Every v4c piece, mapped (bytes v4c -> split):**
| piece | v4c | split | side | change |
|---|---|---|---|---|
| agi-post@.service | 1,252 | 1,252 | engine-post | extraction loop: engine*.md, grep -h, range ends at ^## |
| agi-run | 357 | 357 | engine-post | moved verbatim |
| settings.json | 272 | 272 | engine-cc | moved verbatim |
| cccc.ts | 1,647 | 1,647 | engine-pi | moved verbatim |
| agi-kid | 390 | 390 | engine-pi | moved verbatim |
| agi-brief | 938 | 938 | engine-post | moved verbatim |
| brief.py | 810 | 810 | engine-post | moved verbatim |
| agi-meter | 439 | 439 | engine-post | moved verbatim |
| agi-turn | 269 | 269 | engine-post | moved verbatim |
| agi-link | 358 | 358 | engine-post | moved verbatim |
| agi-wt | 688 | 688 | engine-post | moved verbatim |
| agi-track | 89 | 89 | engine-post | moved verbatim |
| agi-flush | 181 | 181 | engine-post | moved verbatim |
| gitconfig | 180 | 180 | engine-post | moved verbatim |
| signers | 65 | 65 | engine-post | moved verbatim |
| sysusers.conf | 41 | 41 | engine-post | moved verbatim |
| agi.rules | 211 | 211 | engine-post | moved verbatim |
| project.sh | 161 | 161 | engine-post | moved verbatim |
| observe.sh | 255 | 255 | engine-post | moved verbatim |
| tick.sh | 254 | 254 | engine-post | moved verbatim |
| agi-project | 1,679 | 1,793 | BOOTSTRAP | s() reads every engine*.md; range ends at ^## |
| agi-frontier | 460 | 460 | engine-post | moved verbatim |
| agi-gate | 276 | 504 | BOOTSTRAP | + every named expansion exists + the unit template non-empty |
| sect | 149 | 202 | BOOTSTRAP | reads every engine*.md |
None is GONE in this round: removing a piece changes behaviour, and this round's bar is parity. The seeds that DO remove bytes are named in Q.5, each a later round.

**Q.3 · The four changed readers, whole:**
`sect` (202 B, bootstrap):
~~~sh
#!/bin/sh
r=${2:-HEAD};git ls-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s/^/$r:/"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~
`agi-project`: only `s()` changes (the rest of the 1,793 B is v4c's): `s(){ git ls-tree --name-only $r .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s/^/$r:/"|git cat-file --batch --follow-symlinks|sed -n "/^### $1 /,/^##/{/^~~~/,/^~~~/{//!p}}";}`
`agi-post@.service`: only the extraction loop changes: `e=t/.agi/nodes/.geometry/engine*.md;for x in $(grep -ho "^### [^ ]*" $e|cut -c5-);do sed -n "/^### $x /,/^##/{/^~~~/,/^~~~/{//!p}}" $e>bin/$x;done` (same 1,252 B)
`agi-gate` (504 B, bootstrap):
~~~sh
#!/bin/sh
echo $1:.agi/nodes/.geometry/engine.md|git cat-file --batch --follow-symlinks|sed -n 's/^\(engine-[a-z]*\) .*/\1/p'|while read n;do git cat-file -e $1:.agi/nodes/.geometry/$n.md||exit 1;done||exit 1
o=$(mktemp -d);sect agi-project $1|sh -s $o $1&&[ -s $o/agi-post@.service ]&&ls $o/multi-user.target.wants/agi-post@*>/dev/null||{ rm -rf $o;exit 1;}
mv $o $o.1;sh -c "$(sed -n 's/^ExecStart=sh -c "\(.*\)&&systemctl.*/\1/p' $o.1/agi-project.service)";diff -r $o.1 $o;r=$?;rm -rf $o $o.1;exit $r
~~~

**Q.4 · Measured 05:5xZ, unprivileged, on a scratch repo (v4c commit vs split commit, the live posts.md + one synthetic engine-v4 row, so the per-post path runs):**
| # | claim | result |
|---|---|---|
| R1 | `sect <piece>` at the split == v4c's `sect <piece>` at v4c, for all 24 names | 20 byte-identical; the 4 that differ are the 4 changed readers |
| R2 | the projector into an empty dir, v4c vs split | the same file set; the per-post drop-in (harness argv, env cells) and the sysusers lines byte-identical; only the unit template (Q.3) and the REV name differ |
| R3 | a post's own extraction (the loop taken from each REV's unit bytes, run over a checkout of that REV) | 24 files each side; only the 4 changed readers differ |
| R4 | the gate | a complete split: rc 0 · `engine-post.md` missing: rc 1 · the unit template renamed away: rc 1 |
**Two defects found by the proofs, not by reading:** (1) the extraction loop and `s()` ended a piece at the next `### `, so the LAST piece of each node ran on into the next node's pieces table (settings.json, agi-kid, agi-frontier came out wrong) -> they now end at `^##`, as `sect` already did (pieces never hold a line that starts `##`: checked, 0). (2) The gate passed with an expansion missing, and also (in v4c already) with the unit template gone -> two checks, +228 B, both refused now. Three harness slips of mine were caught and redone: a pipe tested with `-s`, a tamper commit on the branch under test, a non-executable `sect`.
**Parity:** the doc:g716111-stage25-parity rows ride on these bytes; with 20 pieces identical, the readers resolving the same 24 pieces (R1, R3) and the projector's per-post output identical (R2), no row's mechanism changes. Re-run the rows on the live post after the build: the split is unproven live.

**Q.5 · What comes next (seeds from belam, measured as options, none needed for the 8 KB bar):**
- ONE BRIEF (all-is-one, built and parity-tested on its side): `brief` 1,161 B (python, one process) + `agi-firstturn` 659 B replace agi-brief + brief.py (1,748 B): +72 B today, -587 B once stage 3 retires the first-turn half; the hook wiring becomes a cell (B per harness). It lives in engine-post.
- key=value units -> cells + ONE projector line per file type (all-is-one's lens): agi-post@.service (1,252 B) is mostly constants; the per-post values are already cells. A later round, with its own parity proof.
- per-post selection: today every post extracts every expansion (bytes on disk, harmless); a post-vector cell naming its expansions (`AGI_X`) would load only `engine-post` + its harness's node.

**Falsifiers.** R1-R4 PASS (scratch) · **R5** DG3's build: the live post boots from the split with every parity row green (UNRUN) · **R6** `wc -c engine.md` <= 8,192 at every trunk tip: a gate line, so the bootstrap can never silently regrow past the bar (proposed, unbuilt).
**THE 8 KB RAIL, RULED (belam [rule] 04:21Z; the owner may overturn it; this is the ONE place it is written):** F21's tiers are the rail. (1) the CODE inside config:engine's `~~~` fences <= 8,192 B, extracted as `git show <rev>:.agi/nodes/.geometry/engine.md | awk '/^~~~/{c=!c;next} c' | wc -c` (fence lines excluded; what installs: the owner's "8KB base install"; 7,358 B at d6864e8c5) AND (2) the whole engine.md <= 12,288 B, `git show <rev>:.agi/nodes/.geometry/engine.md | wc -c` (9,132 B). R6 above and F32 (`wc -c engine.md` <= 8,192) RETIRE as rails (they measure the diagram and map prose, not the install) and stay as REPORTED numbers. §AB's AA2.63 reads this rule.


## S · ROUND 6 · alive -- the SEED: 959 B that regrow the engine from ONE signed commit; every other byte is a git object named by it
**Owner 06:1xZ:** "Q is go and I'm fine with going with R. Heck if we can aply that principle even harder and layer it with compression maybe we could get it under a 1kb seed? Math is compression then we compress the compression math." **What am I ACTUALLY trying to get the machine to do?** Carry the least that can still prove what it grows: a NAME for the engine (one hash), a WHO (one key line), and the one verb that turns the named bytes into a body. The vector is all-is-one's: ONE SIGNED COMMIT (a tree has no signer, time or parent; per-node blobs would be n pointers where the Merkle DAG already gives one).
```
seed (959 B: 877 of text + an 82 B anchor key line)
  ├─ fetch ONE commit, blob-less, depth 1, with transfer.fsckObjects: every object re-hashed on receipt (INTEGRITY: the name IS the hash)
  ├─ verify-commit against K (AUTHENTICITY: who published this engine)
  └─ read the engine nodes BY NAME at that commit (§R's split: engine*.md) -> each blob fetched only when read (promisor remote)
       -> agi-project -> the body (units, users, cells), then every other piece by `sect`, as in §Q/§R
```
`seed` whole (the anchor line shown as a placeholder; 82 B in the test):
~~~sh
#!/bin/sh
# agi seed REPO HASH [OUT]: the engine from ONE signed commit. Every other byte is a git object NAMED by HASH: blob-less, each
# blob fetched when read, every object re-hashed on receipt (fsck); the commit must verify against K; its projector writes OUT
K='<the anchor: ONE allowed_signers line, e.g. the master or the owner key, 82 B>'
set -e;mkdir -p ${AGI_SEED:=/var/lib/agi/seed};cd $AGI_SEED;git init -q;git remote add o "$1" 2>/dev/null||:;git config remote.o.promisor true
git config remote.o.partialclonefilter blob:none;git -c transfer.fsckObjects=true fetch -q --depth 1 --filter=blob:none o $2;h=$(git rev-parse --verify $2^{commit})
echo "$K">.s;git -c gpg.ssh.allowedSignersFile=.s verify-commit $h 2>/dev/null
git ls-tree --name-only $h .agi/nodes/.geometry/|grep '/engine[^/]*\.md$'|sed "s/^/$h:/"|git cat-file --batch --follow-symlinks|sed -n "/^### agi-project /,/^##/{/^~~~/,/^~~~/{//!p}}"|sh -s "${3:-/run/systemd/system}" $h
~~~
**Tested 06:2xZ** (the round-5 scratch repo as the remote, uploadpack.allowFilter on, throwaway anchor and "other" keys, one synthetic engine row; no root, the body written into a scratch dir):
| # | case | result |
|---|---|---|
| S1 | a commit signed by the anchor | rc 0: the projected body (agi-post@dg9 + agi-project.path linked) |
| S2 | signed by another key | refused (rc 1), nothing written |
| S3 | unsigned | refused (rc 1) |
| S4 | a hash the remote does not have | refused (rc 128) |
| S5 | parity: the seed's projection vs the projector run directly in the repo at the same commit | 5 of 5 files identical (paths normalized) |
| -- | what crossed the wire | 10 objects: 1 commit, 4 trees, 5 blobs (the 4 engine nodes + posts.md), a 60 KiB pack (posts.md is most of it) |
**Compression, honestly (all-is-one's line, measured):** git already stores and sends the engine as zlib + delta: 18,029 B of engine text -> 9,172 B of zlib. Compressing the SEED itself buys little: gzip 652 B, but a runnable self-extracting form (base64 + `base64 -d|gunzip|sh`) is 899 B vs 959, a 6% saving that makes the seed unreadable, so the seed stays plain text. "Compress the compression" ends at the HASH: content-addressing compresses IDENTITY, not content (any size -> 160/256 bits), and nothing below the hash can pin more.
**Honest limits:** (0) the REMOTE must allow uploadpack.allowFilter and a bare-hash want (allowAnySHA1InWant or allowReachableSHA1InWant), else it only WARNS and ships the whole snapshot (self-perpetuating measured 76 MB on its clone): two cells on the remote, and the seed counts as correct but not small there; the gate stays at LAND, not in the seed (self-perpetuating: it decides which hash may be named), while the seed keeps verify-commit, because it is about to run fetched code as root · (1) a seed needs the repo it names (or any copy holding that commit): it is a NAME, not the bytes · (2) trust = the anchor key line: whoever holds that key can publish an engine the seed will grow, so the anchor is the owner's or the master's key, and a ring of anchors is the capsule's quorum (§O) applied to the engine · (3) SHA-1 here: git's hardened SHA-1 (collision-DETECTING, not collision-proof); a sha256-format repo removes it at the cost of a repo migration · (4) the seed regrows the ENGINE; a post's work needs the graph, which the post fetches as it reads (the same promisor remote) · (5) one more root act: the seed runs as root once per box, like v4c's agi-seed.
**Falsifiers.** S1-S5 PASS (scratch) · **S6** on a clean box: the seed alone, the trunk's signed tip and the town remote bring a post up with every parity row green (UNRUN: root, a box) · **S7** the trunk's tip is signed by the anchor at every landing (a gate line; unbuilt) · **S8** a remote that serves a corrupted object is refused at fetch by fsck (by git's design; not reproduced here).


## T · ROUND 6 REVISED · alive -- ONE script (1,019 B) + ONE matrix (100 B): local first, then a timed signed sync; conflicts become refs for the Prime; no remote = read-only + a greeting
**Owner 06:24-06:2xZ (verbatim on the goal):** "... What if we use the matrices more? A matrix showing how all the other matrices need to expand that then show how things should be populated. The one script could be the entire bootstrap ..." / "... first a local check to have something at least then it initiates a remote sync on local with timeout, and hands sync conflicts to prime post once its up. If remote connection unavailable, then pick local read only no remote sync hand prime seed expansion state and first boot owner greeting." §S stays the remote half's proof (fetch blob-less, fsck, verify-commit).
**The matrix** = a `### matrix` section in config:engine, fenced TSV (self-perpetuating: a pipe table would read back empty through `sect`), columns `when · target · node · verb`; its FIRST row expands the matrix itself, so the seed knows ONE name and the rest describes itself. `boot` rows run in the seed, `post` rows inside each post's unit:
~~~
boot	matrix	engine	sect
boot	body	posts	agi-project
post	bin	engine*	sect
post	brief	card-<p>	brief
~~~
**The script, whole** (937 B of text + the 82 B anchor line = 1,019 B):
~~~sh
#!/bin/sh
# agi seed [REMOTE] [S]
K='<the anchor: ONE allowed_signers line, 82 B>'
cd ${AGI_ROOT:-/data/work/agi}||exit 1;b=$(git symbolic-ref --short HEAD);g=$(git rev-parse --git-dir);i=.agi/sessions/inbox/belam.md;mkdir -p ${i%/*}
e(){ git ls-tree --name-only $1 .agi/nodes/.geometry/|grep /engine|sed "s/^/$1:/"|git cat-file --batch --follow-symlinks|sed -n "/^### $2 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
x(){ e $1 matrix|awk '$1=="boot"&&$4!="sect"{print $4}'|while read v;do e $1 $v|sh -s ${AGI_OUT:-/run/systemd/system} $1;done;};x HEAD;echo "$K">$g/s
if timeout ${2:-60} git -c transfer.fsckObjects=1 fetch -q ${1:-origin} $b;then git -c gpg.ssh.allowedSignersFile=$g/s verify-commit FETCH_HEAD||exit 1
git config agi.mode rw;h=$(git rev-parse HEAD);git merge -q FETCH_HEAD&&x HEAD||{ git merge --abort;git update-ref refs/conflicts/$h FETCH_HEAD '';echo "[conflict] refs/conflicts/$h">>$i;}
else git config agi.mode ro;echo "[owner] first boot, local read-only. Hello.">>$i;fi
~~~
```
1 LOCAL   the graph is here: expand every boot row of the matrix at HEAD at once -> the body exists before any network
2 REMOTE  fetch the branch under `timeout` with fsck -> verify-commit vs the anchor -> merge -> re-expand (agi.mode = rw)
3 CONFLICT  merge aborted (HEAD untouched) -> refs/conflicts/<local tip> -> the remote tip, CREATE-ONLY (two posts never claim
          one conflict; it survives rotation and rides the next sync; self-perpetuating) + one notice line in the Prime's inbox
4 NO REMOTE  unreachable OR past the timeout -> agi.mode = ro, no sync, the Prime's inbox gets the first-boot owner greeting
```
**Tested 06:3xZ** (a clone of the round-5 scratch repo as LOCAL, its origin as REMOTE, the matrix added and anchor-signed, a throwaway anchor key, the body written into a scratch dir; no root):
| path | result |
|---|---|
| P4 remote unreachable | rc 0 · mode ro · body expanded (agi-post@dg9 + agi-project.path) · greeting in the Prime's inbox |
| P4b remote hangs (a `sleep 30` upload-pack, timeout 3 s) | rc 0 · mode ro · body expanded · greeting |
| P2 a signed fast-forward | rc 0 · mode rw · HEAD moved to the remote tip · re-expanded |
| P3 both sides edited the same line | rc 0 · merge aborted, HEAD = the local tip · `refs/conflicts/<local tip>` -> the remote tip · one inbox line |
| P5 the remote tip unsigned | rc 1 · no merge · mode unchanged (ro stays ro) · the body stays the local one |
**Named, not hidden:** an unsigned remote tip exits 1 with no inbox line (cut for bytes; the unit's journal and rc carry it) · `agi.mode ro` is a CELL posts must read before they push (unbuilt in the post unit) · the seed merges in the checkout it runs in, so it runs at boot before any post holds that checkout · the remote half still needs §S's limits (allowFilter, a bare-hash want, the anchor).
**Falsifiers.** P2-P5 PASS · **T6** DG5 boots from this seed on its box, every parity row green (UNRUN; the owner's first target, after Phase C) · **T7** the Prime, at wake, lists `refs/conflicts/*` and resolves or banks each (UNRUN: a Prime card line).

## T.1 · ROUND 6 · alive -- DG3's holes in §T folded back in: the seed is 1,023 B again with the real anchor; a divergence is always the Prime's (--ff-only); a failed expansion is the seed's rc
**Why this exists.** DG3 built and dry-tested §T (doc:g716111-round6-build @58ff49120) and found real holes in alive's bytes, kept byte-exact in §T: **H1** a re-run on the same conflict appended a second notice · **H2** a merge whose re-expansion failed made a FALSE conflict ref and notice, with HEAD already moved · **H4** git failing at the top left `g` empty, so the anchor went to `/s` at the filesystem root (as root: it succeeds) · **T7c** the bare `[conflict]` line landed inside the Prime's last unread message · **H7** a diverged, conflict-free merge with no git identity failed (a decision banked). Its patched copy closes H1/H2/H4/T7c at 1,103 B with the anchor, over 1 KiB. **What is the true state the seed must report?** Exactly three outcomes: synced (rw), handed to the Prime (a conflict ref + ONE message), or local read-only (one greeting); and an rc that is non-zero whenever the body did not expand.
```
H1   update-ref refs/conflicts/<local tip> ... ''  &&  the notice      create-only: a 2nd run fails the update, so no 2nd notice
H2   merge --ff-only || {conflict};  x HEAD  (the last command)       a failed expansion = the seed's rc; never a false conflict
H4   g=$(git rev-parse --git-dir) || exit 1                          no repo = rc 1 before any write
T7c  m(): every notice is its own inbox block (---, ts, from: seed, to: belam)
H7   DECIDED (decide-and-document): --ff-only. The seed never makes a merge commit (no identity needed, no root-authored merge);
     ANY divergence, conflicting or not, becomes a refs/conflicts/ ref for the Prime. Costs: the Prime sees clean divergences too.
     Flip = one word (drop --ff-only, add -c user.* + the abort), +36 B.
```
Paid for with: no usage comment · `cd ${AGI_ROOT:-.}` (the literal path is gone: the unit's WorkingDirectory or AGI_ROOT names the checkout) · `branch --show-current` · `fetch.fsckObjects` · `ls-tree --format` instead of a sed · the anchor inline in its one `echo` · the conflict notice carries the bare local tip (the ref name is derivable) · `--ff-only` needs no `merge --abort`.
**The seed, whole** (941 B of text + the 82 B anchor line = **1,023 B**; sha256 of the text with `@ANCHOR@` in the anchor slot: `cd97baf8f62b6460`):
~~~sh
#!/bin/sh
cd ${AGI_ROOT:-.}||exit 1;b=$(git branch --show-current);g=$(git rev-parse --git-dir)||exit 1;i=.agi/sessions/inbox/belam.md;mkdir -p ${i%/*}
m(){ printf -- "---\nts: %s\nfrom: seed\nto: belam\n\n%s\n" $(date -u +%FT%TZ) "$*">>$i;}
e(){ git ls-tree --format="$1:%(path)" $1 .agi/nodes/.geometry/|grep /engine|git cat-file --batch --follow-symlinks|sed -n "/^### $2 /,/^##/{/^~~~/,/^~~~/{//!p}}";}
x(){ e $1 matrix|awk '$1=="boot"&&$4!="sect"{print $4}'|while read v;do e $1 $v|sh -s ${AGI_OUT:-/run/systemd/system} $1;done;};x HEAD;echo '<the anchor: ONE allowed_signers line, 82 B>'>$g/s
if timeout ${2:-60} git -c fetch.fsckObjects=1 fetch -q ${1:-origin} $b;then git -c gpg.ssh.allowedSignersFile=$g/s verify-commit FETCH_HEAD||exit 1
git config agi.mode rw;h=$(git rev-parse HEAD);git merge -q --ff-only FETCH_HEAD||{ git update-ref refs/conflicts/$h FETCH_HEAD ''&&m "[conflict] $h";};x HEAD
else git config agi.mode ro;m "[owner] first boot, local read-only. Hello";fi
~~~
**Tested 07:4xZ** (a scratch harness: per case a fresh bare remote, a signing clone and a LOCAL clone that runs the seed; a throwaway anchor and a second key; the body piece writes the expanded REV; no root):
| # | case | result |
|---|---|---|
| P2 | a signed fast-forward | rc 0 · rw · HEAD = the remote tip · body re-expanded at it |
| P3 | both sides edited one line | rc 0 · HEAD = the local tip · 1 conflict ref · 1 notice |
| H1 | the same conflict, the seed run 3 times | still 1 ref · 1 notice |
| H7 | diverged, no overlap | rc 0 · HEAD = the local tip · 1 conflict ref (by design: the Prime's) |
| P4 · P4b | remote unreachable · upload-pack hangs (timeout 3 s) | rc 0 · ro · body expanded · 1 greeting · 3 s |
| P5 · P5b | the remote tip unsigned · signed by another key | rc 1 · no merge · mode unchanged |
| P5c | the remote rewound to an OLDER signed tip | rc 0 · HEAD stays on its descendant (--ff-only never moves back) |
| H2 | the remote tip carries a body piece that fails | rc 7 (the piece's) · 0 conflict refs · 0 notices · HEAD at the tip, body still the last good one |
| H4 | run outside any repo | rc 1 · nothing written |
| T7c | the inbox already holds an unread message | the greeting is its own block after it |
**Honest limits.** (1) T7c relies on the inbox file ending in a newline (all 750 live inbox files do; a writer that leaves none would glue the `---` to its last line). (2) H2 leaves HEAD at the new tip with the OLD body expanded; the rc and the unit journal say so; the next boot retries. (3) DG3's other named items stand: a reachable remote without the branch = read-only + greeting (H5); the offline greeting repeats each offline boot; the matrix's `post` rows are read by nothing yet. (4) `--format` needs git >= 2.36 (this box: 2.43).
**Falsifiers.** P2-P5c, H1, H2, H4, H7, T7c PASS (scratch) · T6 / T7 as in §T (UNRUN, DG3's live build after Phase C) · **T8** the seed stays <= 1,024 B with the real anchor at every later edit (`wc -c`; today 1,023).

## U · DOMAIN CONTROLLER · alive -- the directory is ONE matrix in the graph; a certificate's key-id names its row, so editing a row revokes it; encryption-town holds no secret, only the signing window
**Owner 06:3x-06:5xZ / 07:0xZ (verbatim on the goal):** "... Modifying local stuff across boxes via existing user and key perms. Encryption town can be domain controller." / "... see if it can be supercharged and compressed via matrix math. Like the way we use our matrices to help hook into the login method but not the private key itself. Same here the matrices describe how the short lived ssh key can even be “popped” securely into whatever interface takes it." **What is the TRUE state of a login right now?** One row of a matrix: who, on which box, as which principal, for how long, with which forced command. If a box can read that row and nothing else, then what a box allows is exactly what the graph says, and a check is one `cmp`.
```
GRAPH    the dc matrix (fenced TSV, public bytes only): box · user · principal · valid · opts       one row = one certificate template (belam 07:05Z)
           rid = 16 hex of sha256 over the row line = the cert's key-id (§V: agi-sign -I rid, -n/-V from the row, -z serial)
SYNC     every box already has the graph (§T: local first, then a signed sync) -> the directory travels with it: 0 new transport
PROJECT  dc-project BOX < matrix > /etc/agi/dc/rows      this box's rows only, each led by its rid (root-owned 644; a §T boot row)
SSHD     Match User <the agi users>: TrustedUserCAKeys (the CA pubs, §V) · AuthorizedPrincipalsCommand dc-principals %u %i
           the cert's key-id must be a LIVE row of THIS box for THIS user, opening `restrict` -> sshd gets opts + principal, else nothing
CHECK    dc-project BOX < matrix | cmp - /etc/agi/dc/rows      rc 0 = the box allows exactly what the graph says (the true state, read)
DC       encryption-town = the box whose CA agent is armed for a window (§V); the directory is NOT its: it is graph, on every box
```
| what | where it lives | who may write it |
|---|---|---|
| identities (users, principals, boxes, validity, forced commands) | the dc matrix node (expansion; 0 B in the zygote) | a signed graph commit, like any node |
| the CA public half · the KRL | §V, projected beside the rows | the same |
| the CA private half | a capsule (§V) | nobody: popped into an agent for a window |
| a user's private key | that login's agent only (§V) | nobody, ever |

**Revocation by edit (the compression the owner asked for):** a cert names its policy by HASH, so changing one cell of a row (a shorter `valid`, a dropped principal, a different forced command) changes its rid, and every cert issued under the old row is refused at its next login: no KRL entry, no list to keep. §V's `-z` serial + KRL stays for killing ONE stolen cert without touching the row.

The pieces, whole (expansion, beside §V's `agi-sign`; 590 B + 4 sshd lines):
~~~sh
#!/bin/sh
# dc-project BOX < the dc matrix > rows: this box's rows, each led by its rid (16 hex of sha256 over the row) = the cert key-id; public bytes only
while IFS= read -r l;do case $l in '#'*|'');;"$1	"*|"*	"*)printf '%s\t%s\n' $(printf %s "$l"|sha256sum|cut -c1-16) "$l";;esac;done
~~~
~~~sh
#!/bin/sh
# sshd AuthorizedPrincipalsCommand dc-principals %u %i: the cert's key-id must be a LIVE row of this box for this user -> opts + principal; a row not opening restrict = refused (fail closed)
awk -F'\t' -v u="$1" -v i="$2" '$1==i&&$3==u&&$6~/^restrict/{print $6" "$4}' ${DC:-/etc/agi/dc}/rows
~~~
~~~
Match User agi-*
  TrustedUserCAKeys /etc/agi/dc/ca.pub
  AuthorizedPrincipalsCommand /etc/agi/dc-principals %u %i
  AuthorizedPrincipalsCommandUser nobody
~~~
**Tested 07:0xZ** (an UNPRIVILEGED sshd on a loopback high port, certificates only; a throwaway CA standing in for §V's; a 3-row matrix, two boxes; no root, no real key, host or address; sshd gone after, 0 processes left):
| # | case | result |
|---|---|---|
| U1 | a cert whose key-id = a live row of this box, the right principal | logged in; the row's forced command ran |
| U1b | the same cert asking for another command | the forced command ran instead |
| U2 | key-id = a row of ANOTHER box | refused (rc 255): the box never sees it |
| U3 | one cell of the row edited after the cert was signed | the old cert refused; a cert under the new rid logs in (U3b) |
| U4 · U5 · U6 · U7 | expired cert · another CA · a plain key · a principal not on the row | refused (rc 255) each |
| U8 | a key-id carrying `;`, spaces or `$(...)` | refused; nothing executed (awk compares, never evaluates) |
| U9 | the check: projection vs the box | rc 0 clean · rc 1 after one hand-added row |
| U9c | a hand-added row with EMPTY opts | FIRST FORM: honoured with a full interactive shell (the test hung on it) -> FIXED: rows not opening `restrict` are refused (+68 B); re-run: refused (rc 255) |

**Honest limits.** (1) A hand-added row in `/etc/agi/dc/rows` is honoured until the check heals it; the file is root-owned, so writing one already needs root, and the check names it. (2) The `Match` block keeps every EXISTING user and key exactly as it is (the owner's "existing user and key perms"); only the agi users go certificate-only. (3) The forced command and principal are enforced; `valid` is the signer's (§V) and sshd does not re-check it against the row, so a longer-lived cert minted outside agi-sign would pass until its rid changes. (4) The DC is not a single point of failure for READING: every box holds the directory; it IS one for new logins (the armed CA window, §V F42).
**Falsifiers.** U1-U9c PASS (scratch) · **U10** after DG3's build, `dc-project <town> | cmp` returns 0 on BOTH boxes and a dg5 cert logs in on encryption-town and nowhere else (UNRUN) · **U11** a §T boot on a fresh box projects the rows with no hand step (UNRUN; one §T matrix row `boot dc engine dc-project`).

## V · DOMAIN CONTROLLER · self-perpetuating -- keys no one can write: a fresh key every login, a certificate for minutes, the CA a 32-B seed in a capsule
**Owner 07:0xZ:** "A literal private-key secured user but the private key auto rotates each login to domain controller. Neither domain controller nor the use account ever actually get perms to write that private key itself only rotate it next login anywhere else." **What am I ACTUALLY trying to get the machine to do here?** Make the thing worth stealing not exist long enough to be stolen, and let the one thing that must last (the CA) regrow from its escrow like everything else. The regrowth lens, inverted: **the best key to survive a box loss is one that never lived longer than a login.**
```
login  post/user ── ssh-keygen in RAM (tmpfs, < 1 s) ─▶ k.pub ─▶ DC: agi-sign RID ─▶ cert: key-id = rid (§U row), -n principal, -V valid (row), -z serial
                 ◀─ cert ── ssh-add -t KEY_LIFE (the session agent holds key + cert) ── the files unlinked: the private key exists ONLY in that agent
box    sshd: TrustedUserCAKeys (U projects the CA pubs) · AuthorizedPrincipalsCommand (U: rid -> principal + opts) · RevokedKeys (KRL) · AuthorizedKeysFile none
DC     holds PUBLIC bytes only: the rows (U), the CA pubs, the KRL · signs through the CA AGENT, never a key file
CA     a 32-B ed25519 SEED: sealed in a capsule (§O) + escrowed 2-of-2 (iPhone, posts' E) (P.8) ─▶ ONE quorum pop arms the CA agent for a WINDOW (ssh-add -t)
       window ends ─▶ the agent drops the key ─▶ no new logins anywhere until the next pop · the quorum signs the WINDOW, never each login
```
| who could write the user's private key | answer |
|---|---|
| the DC | never sees it: it signs the PUBLIC half |
| the user account | never holds a file of it: generated in RAM, handed to its agent, unlinked; the next login makes a new one |
| root on the DC | cannot mint a CA (the seed is in the capsule); CAN sign during an armed window through the agent socket: that window is the exposure, so it is a cell, short |
| root on the box where a session runs | CAN read that session's agent memory (O.3: no TPM here); what it gets dies with KEY_LIFE and the cert's validity, and is good for that one row's principal only |

**Tested 07:0xZ** (throwaway CA + keys on tmpfs; an UNPRIVILEGED sshd on a loopback high port trusting only certificates; no root, no real key, host or address):
| claim | result |
|---|---|
| a fresh-key cert login under a row | ok; the cert's key-id = the rid |
| two logins | two different keys (rotation = every login) |
| an expired row · a principal not authorised on the box · a rid not in the directory · a plain key with no cert | refused · refused · signer exit 3 · refused (AuthorizedKeysFile none) |
| one cert revoked by serial in the KRL | refused; the next serial logs in |
| the CA popped from stdin (`ssh-add -t W -`): no CA file on disk | yes; inside the window: signs · after it: the agent is empty, login fails (rc 255) |
| CA rotation: old + new pub in TrustedUserCAKeys, then the old dropped | both certs log in during the overlap; after it, the old-CA cert is refused, the new one logs in |
| box loss: the CA seed (32 B) escrowed 2-of-2 (iPhone + E), rejoined | same public key, byte-exact (escrow 671 B per CA) |
| files left after a login | 0 key files; the DC dir holds rows, ca.pub, krl only |
| v2 (07:3xZ, after alive's U9c): the CERT fails closed on its own -- `-O clear`, then only what the row's `restrict` opts grant | `restrict`: a command runs, a pty is refused, a remote forward is refused (extensions: none) · `restrict,command="..."`: the forced command runs whatever the client asks · `restrict,pty`: a pty · empty opts or `no-pty` (not opening `restrict`): signer exit 3 -- so a box whose sshd lacks dc-principals still gets a restricted cert |

**A correction to §P found here:** `esc` splits over the field 2^521-1, so it carries **at most 64 B**; a 400-B OpenSSH key file was wrapped modulo p into garbage, silently. Fixed: `esc split` now refuses a secret over 64 B (+86 B; 1,833 B with P.8's P-256 holder) and the rule is **escrow a 32-B key, never a file**. Every escrow made so far was 48 B or less (P.1), so none is affected.

**Bytes (expansion, config:capsule beside esc; 0 B in the zygote):** `agi-sign` 722 B (v2, 07:3xZ: the cert fails closed) · `agi-login` 337 B · sshd: 4 lines, projected by U · the CA window and KEY_LIFE = 2 cells (`ca_window`, `key_life`). Retires, once built: the per-seat signing keys in MAIN (`.agi/sessions/seats/<p>.key`, parity row 17) and the never-rotated per-post ssh key minted in ExecStartPre (row 18 MISSING -> EXCEEDS).
`agi-sign` whole:
```sh
#!/bin/sh
# agi-sign RID <pub: sign a fresh login key under the §U row RID (rid box user principal valid opts); the cert fails closed: -O clear + only what the row's restrict opts grant; the CA key lives ONLY in the CA agent
d=${DC:-/etc/agi/dc};l=$(awk -F'\t' -v r=$1 '$1==r' $d/rows);o=$(echo "$l"|cut -f6);case $o in restrict*);;*)exit 3;;esac
set -- -I $1 -n $(echo "$l"|cut -f4) -V $(echo "$l"|cut -f5) -O clear;case ,$o, in *,pty,*)set -- "$@" -O permit-pty;;esac;c=$(echo "$o"|sed -n 's/.*command="\([^"]*\)".*/\1/p');[ "$c" ]&&set -- "$@" -O "force-command=$c"
t=$(mktemp -d);cat>$t/k.pub;SSH_AUTH_SOCK=$CA_SOCK ssh-keygen -q -Us $d/ca.pub "$@" -z $(date +%s%N) $t/k.pub&&cat $t/k-cert.pub;r=$?;rm -rf $t;exit $r
```
`agi-login` whole:
```sh
#!/bin/sh
# agi-login PRINCIPAL: a fresh key pair per login, in RAM (tmpfs) for < 1 s, then held ONLY by the session agent; the private key is never written to disk
t=$(mktemp -d -p $XDG_RUNTIME_DIR);ssh-keygen -q -t ed25519 -N "" -f $t/k&&./agi-sign $1<$t/k.pub>$t/k-cert.pub&&ssh-add -q -t ${KEY_LIFE:-300} $t/k;r=$?;rm -rf $t;exit $r
```
**Honest limits.** (1) `ssh-keygen` writes its pair to a file, so the key touches tmpfs (RAM, 0700, < 1 s) before the agent holds it; a pure-stdin path (python -> `ssh-add -`) loses the cert pairing, unmeasured. (2) Root on the DC inside an armed window can sign: the window is the bound, not zero. (3) A pop needs the owner's iPhone (mutual quorum): one window per owner tap, so `ca_window` trades taps for exposure. Tonight's stand-in key (§X) arms a THROWAWAY TEST CA only (alive's call, agreed 07:3xZ: a box key arming the real CA would make the box its own owner half of the mutual quorum, O.8); the real CA's first window waits for the real phone, so F42 cross-box runs on the test CA. (4) The sshd side is U's projection, tested here only by hand-written stand-ins for its rows.
Falsifiers: **F41** the login table above (PASS, scratch sshd) · **F42** after a window closes, no login anywhere succeeds until a new pop (PASS for one box; cross-box with §W unrun) · **F43** `find / -xdev` on DC and box after 100 logins shows no user private key file (unrun at scale) · **F44** a box rebuilt from the seed (§T) trusts the CA through U's projection and logs a post in with no key copied over (unrun) · **F45** `esc split` on more than 64 B exits non-zero (PASS).

`esc` delta (P.8 + this section; every other line = §P's `esc`):
```diff
- import sys,os,hashlib,base64 as B;from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P;from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C
+ import sys,os,hashlib,base64 as B;from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey as K,X25519PublicKey as P;from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305 as C;from cryptography.hazmat.primitives.asymmetric import ec;E=ec.SECP256R1()
+ from cryptography.hazmat.primitives.serialization import Encoding as N,PublicFormat as F;X=(N.X962,F.UncompressedPoint)
-  s=sys.stdin.buffer.read();k=int(a[2]);c=[int.from_bytes(b'\1'+s,'big')]+[int.from_bytes(os.urandom(65),'big')%p for _ in range(k-1)];print('check',h(s).hex())
+  s=sys.stdin.buffer.read();k=int(a[2]);len(s)<65 or sys.exit('esc: a secret is at most 64 B: escrow a 32-B key, not a file');c=[int.from_bytes(b'\1'+s,'big')]+[int.from_bytes(os.urandom(65),'big')%p for _ in range(k-1)];print('check',h(s).hex())
-   e=K.generate();q=r(B.b64decode(open(f).read()));y=sum(x*pow(i,j,p) for j,x in enumerate(c))%p;print(f,B.b64encode(e.public_key().public_bytes_raw()+C(h(e.exchange(q))).encrypt(bytes(12),f'{i}:{y}'.encode(),None)).decode())
+   b=B.b64decode(open(f).read());y=sum(x*pow(i,j,p) for j,x in enumerate(c))%p
+   if len(b)>32:e=ec.generate_private_key(E);z=e.exchange(ec.ECDH(),ec.EllipticCurvePublicKey.from_encoded_point(E,b));u=e.public_key().public_bytes(*X)
+   else:e=K.generate();z=e.exchange(r(b));u=e.public_key().public_bytes_raw()
+   print(f,B.b64encode(u+C(h(z)).encrypt(bytes(12),f'{i}:{y}'.encode(),None)).decode())
```

## W · CROSS-BOX · all-is-one -- ONE vector for seeding and comms: a remote is a URL cell, a message is a signed commit, the §V cert is the only key; GitHub and the mesh run the same verbs
**Owner 06:5xZ, item 1 (verbatim on the goal):** "... also have them move around boxes or spawn more on encryption town to confirm cross box easy seeding and cross-comms via GitHub initially and maybe eventually via for direct and mesh addresses? Modifying local stuff across boxes via existing user and key perms. Encryption town can be domain controller." **What am I ACTUALLY trying to get the machine to do?** Move ONE kind of thing between boxes, a signed commit, so seeding, sync and a message are the same act, and the transport shrinks to a URL in a cell. Keyed to §U (rows: box · user · principal · valid · opts; rid = the cert key-id) and §V (`agi-login` / `agi-sign`); 0 new login bytes.
```
            remote = ONE cell per box (where to fetch/push): GitHub = a URL · mesh/direct = ssh://<alias>/<path> · nothing else differs
SEED   empty box ─ §S seed REMOTE HASH ─▶ fetch blob-less + fsck ─▶ verify-commit vs K ─▶ the body             0 new B
SYNC   live box  ─ §T seed REMOTE S    ─▶ fetch under timeout + fsck ─▶ verify ─▶ merge ─▶ re-expand          0 new B
SAY    post P    ─ xb send REMOTE TO MSG ─▶ ONE commit on refs/agi/P/TO, signed by P's §V login key + cert ─▶ push
HEAR   post Q    ─ xb recv REMOTE ─▶ fetch refs/agi/*/Q + fsck ─▶ keep a commit only if its cert principal IS the ref's <from>
GATE   a box we own (encryption-town = the DC hub first): sshd = §U rows (who logs in as which existing user; opts = restrict +
       git-shell + AGI_POST) · pre-receive = own namespace only, signed by itself, dated within S s of now
RELAY  GitHub runs no hook of ours: anyone with its write credential can push anything, so HEAR carries the whole check
CHANGE "modify local stuff across boxes" = a commit pushed into YOUR namespace on that box; its own post applies it -- nobody
       writes another box's checkout, so "existing user + key perms" = a §U row, never a shared shell
```
| check | mesh (a box we own) | GitHub (relay) |
|---|---|---|
| transport login | §V cert under a §U row; sshd refuses expired / no row (X7, X8) | GitHub's own credential: one write key per town repo, capsule-held (§O) -- it does not honour our CA (limit 1) |
| who wrote it | pre-receive (X6a) + recv | recv only (X6b) |
| when it was written | pre-receive skew check (X11b) | the ref chain only (limit 2) |
| bytes intact | fsck on push and on fetch | fsck on fetch |
| encryption-town holds | the armed CA window (§V) + one bare hub repo; the rows are graph on every box (§U) | -- |

**Tested 07:1xZ** (throwaway CA + anchor, per-login keys held only in their own agent (stand-in for `agi-login`, key-id = rid), an UNPRIVILEGED sshd on a loopback high port trusting only certs, principals = §U-shaped rows with opts; two bare remotes: a file URL as the GitHub stand-in, the ssh URL as encryption-town's hub; no root, one unix user; §S and §T run VERBATIM from this doc, only K substituted):
| # | case | result |
|---|---|---|
| X1 X2 | §S on an empty box over GitHub · over the mesh | rc 0 both · the two bodies byte-identical · sshd log: ED25519-CERT, ID = the rid |
| X3 | §T sync of a signed engine v2 over GitHub · over the mesh · mesh unreachable | rw + v2 re-expanded · same · ro + the owner greeting |
| X4 X5 | dg5 -> belam over the mesh · over GitHub | `[dg5] hello ...` both |
| X6a | the dg5 login pushes refs/agi/alive/* to the hub | refused by pre-receive (`for dg5`) |
| X6b | the same forgery to GitHub (no hook) | push lands; recv prints `[refused] alive <sha>`, nothing delivered |
| X7 X8 | an expired cert · a principal with no row on the box | ssh refused (rc 128; log: `Certificate invalid: expired`) · refused |
| X8b | a row'd login asks for a shell (`id`) | git-shell: `unrecognized command` |
| X9 | engine anchor K as `belam cert-authority <CA>` | a belam-cert commit verifies (rc 0) · a dg5-cert commit does not (rc 1) |
| X10 | key files after every login | none for any post (the CA + anchor files are the fixture's; built, the CA is §V's capsule) |
| X11a | a key whose cert EXPIRED signs a commit backdated into the cert's window | `verify-commit`: Good, `for old` -- git judges a cert at the commit's OWN date |
| X11b | the same backdate (30 min) pushed to the hub | before the skew check: accepted · after it: refused (`not signed by dg5 now`); a now-dated send still lands (X11c) |
| -- | one mesh send, end to end | 0.35 s |

**Bytes (expansion, 0 B in the zygote):** `xb` 1,025 B · `pre-receive` 681 B · §S, §T, `agi-login`, `agi-sign` unchanged · the remote = 1 cell per box, the skew = 1 cell (`xb_skew_s`, 120). `xb` whole:
```sh
#!/bin/sh
# xb send REMOTE TO MSG | xb recv REMOTE -- a message = ONE signed commit on refs/agi/<from>/<to>; any remote, the same verbs.
# recv keeps a commit only if fsck passes AND its signer's cert principal IS <from> (the CA line in agi.allowed); else [refused].
P=${AGI_POST:?};V="git -c gpg.ssh.allowedSignersFile=$(git config agi.allowed) verify-commit --raw"
case $1 in
send)r=refs/agi/$P/$3;p=$(git rev-parse -q --verify $r)&&p="-p $p";t=$(git hash-object -w -t tree /dev/null)
 c=$(echo "$4"|git -c gpg.format=ssh commit-tree -S $p $t)&&git update-ref $r $c&&git push -q $2 $r;;
recv)git -c transfer.fsckObjects=1 fetch -q $2 "+refs/agi/*/$P:refs/xb/*/$P"||exit 1
 git for-each-ref --format='%(refname)' refs/xb|while read r;do f=${r#refs/xb/};f=${f%/*};s=refs/xbseen/$f/$P
  for c in $(git rev-list --reverse $r --not $(git rev-parse -q --verify $s));do
   if $V $c 2>&1|grep -q "for $f with";then echo "[$f] $(git log -1 --format=%s $c)";git update-ref $s $c;else echo "[refused] $f $c";break;fi;done;done;;
esac
```
`pre-receive` whole (the allowed-signers path is §U's projected file; a literal here):
```sh
#!/bin/sh
# pre-receive on a box we own: the row's opts set AGI_POST; a login writes only refs/agi/<itself>/*, every new commit signed by itself
# and dated within S s of now (the login proved the cert valid NOW, so the signature date cannot be backdated past it)
S=${AGI_SKEW:-120};T=$(date +%s)
while read o n r;do case $r in refs/agi/$AGI_POST/*);;*)echo "refused: $r for ${AGI_POST:-none}";exit 1;;esac
 for c in $(git rev-list $n --not --all);do git -c gpg.ssh.allowedSignersFile=<U: allowed> verify-commit --raw $c 2>&1|grep -q "for $AGI_POST with"&&[ $((T-$(git log -1 --format=%ct $c))) -lt $S ]||{ echo "refused: $c not signed by $AGI_POST now";exit 1;};done;done
```
**The compression the owner asked for, measured:** every post's signing key is gone from every verifier. ONE allowed-signers line (`* cert-authority <CA pub>`) verifies every per-login key on every box over every transport (X4-X6b), and the principal written by `agi-sign` from the §U row is the sender's name; the per-seat pubkey rows retire with §V's. The engine anchor K CAN be the same CA, restricted by principal (X9), but **recommended: keep K a separate anchor**: a CA window then cannot publish an engine, and the two compromises stay apart (§S limit 2).
**Honest limits.** (1) GitHub authenticates its own keys; our certs reach it only through an org SSH CA on an enterprise plan (VERIFY), so its write credential is one deploy key per town repo in a capsule. Whoever holds it can also SQUAT a ref (push its own chain into refs/agi/<p>/*, so the real post's next push is non-fast-forward): denial, never forgery (X6b) (2) Backdating via GitHub: a key read out of a live agent (O.3) signs commits dated inside its own cert window forever (X11a). Over the hub the skew check closes it (X11b). Over GitHub only the chain bounds it: a forgery must extend the ref's tip, so it lands only while no later real message exists on that ref (unmeasured) (3) "existing users" = §U's user column; scratch ran ONE unix user, so the principal -> account mapping across real accounts is untested (needs a second account or root) (4) a refused commit stays under refs/xb and is reported at every recv: loud by design, unpruned (5) tonight there is no mesh path to the owner's boxes (remote access only, WireGuard pending), so GitHub goes first, as ruled.
**Falsifiers.** X1-X11c PASS (scratch) · **W12** DG5 seeded on encryption-town by §S over GitHub, then kept by §T (UNRUN; the first live target, after Phase C) · **W13** one dg5 -> belam message by GitHub and by the hub, the two recv lines identical (UNRUN live) · **W14** = §V F42 cross-box: once the CA window closes, no box accepts a login or a push (UNRUN) · **W15** a post on box A changes box B only through its own namespace, and B's post applies it (UNRUN; needs §U's user column on two real accounts).

## X · THE PHONE STAND-IN · alive -- tonight's phone is ONE row and ONE cert that expires at the owner's wake; the real phone replaces it by editing that row
**Owner 06:3x-06:5xZ (verbatim on the goal):** "... I can’t access it today so it might have to wait and do a stand in key on the box for now and auth it yourself as test." Ruling (a): a stand-in phone key on the box, authorised ONLY for capsule-login, tested end to end, then replaced. **What does the stand-in TRULY allow?** Exactly one row: one principal, one forced command, until a stated minute. Nothing about it is special code: it is §U's row + §V's login + §O.5's capsule-login, with a short `valid`.
```
ROW      enc · agi-capsule · owner-standin · <until the owner's wake> · restrict,command="capsule-login"        (its own rid, never owner-phone's)
KEY      §V agi-login owner-standin: a fresh key in RAM, a cert under that rid, held ONLY by the tester's agent; no key file, ever
TEST     a post's login asks (§O.5 ASK) -> the tester answers as the phone: ssh agi-capsule@<town> <ask-id>, the code on stdin -> the pane
ENDS     the cert's validity runs out at the owner's wake, AND the row is deleted when the real phone key arrives -> the rid dies (§U revocation by edit)
REAL     the phone's own key (Secure Enclave P-256, O.7) gets an owner-phone row: a cert signed once at enrolment if the SSH app takes certs (VERIFY),
         else the O.5 authorized_keys line (restrict,command="capsule-login"), projected the same way
```
**Tested 07:1xZ** on §U's scratch sshd (throwaway CA, the stand-in key generated on tmpfs, certified, loaded into a scratch agent, its files removed in under a second; capsule-login = §O.5's 692 B, byte for byte, pointed at a scratch spool and pane; a random dummy code):
| # | case | result |
|---|---|---|
| SI1 | the stand-in + an open ask, the code on stdin | the code typed into the pane exactly once (rc 0) |
| SI2 | the same ask replayed | refused (rc 3) |
| SI3 | the stand-in asking for a shell · for a pty + a command | refused (rc 2 · rc 3): restrict + the forced command |
| SI4 | a cert under the dg5 row with principal owner-standin | refused (rc 255): the row pins the principal |
| SI5 | the stand-in row deleted (= the replacement) | refused at the next login (rc 255) |
| SI6 | the code at rest in spool, ledger, sshd log | 0 copies; the ledger keeps post + id + time only |
| SI7 | key files left on tmpfs or disk | 0 |

**One seam with §V, decided here (decide-and-document):** §V's limit (3) has the stand-in arm the CA window. The owner's ruling (a) authorises the stand-in for capsule-login ONLY, and a box key that arms the CA would make the box its own owner's half of the mutual quorum (O.8). So tonight: the stand-in arms only a THROWAWAY test CA (its own `TrustedUserCAKeys` line, for the test users, removed after) and never signs a real identity; the real CA's first window waits for the real phone. Cost: F42 cross-box runs on the test CA tonight.
**For DG3's build (in its night order):** (1) the owner-standin row with `valid` ending at 14:00Z (one row, `date -u` read when it is written) (2) the §O.5 root act: `i` writable by agi-capsule (~60 B, ExecStartPre=+) (3) one end-to-end run on DG5's login, SI1-SI7 re-read on the real units (4) at the owner's wake: delete the row, and record the rid that died.
**Falsifiers.** SI1-SI7 PASS (scratch) · **SI8** at 14:00Z+1 min the stand-in cert is refused with the row still present (UNRUN; the expiry alone ends it) · **SI9** the real phone's key logs in under owner-phone and the owner-standin rid is absent from every box's rows (UNRUN; the owner's step).

## Y1 · ROUND 7 · all-is-one -- NODE KEYS: every schema's parent shapes are ONE growth matrix; a node add unlocks only with its row's key; the gate is 1,298 B of awk and agrees with the old Python on all 5,390 live nodes
**Owner 07:1xZ (verbatim on the goal):** "... make sure the engine still maintains graph growth order so posts can’t just grow nodes without respecting order. Could expand key ring system to also include node keys so only the correct node key schema unlocks next node add to graph ..." **What am I ACTUALLY trying to get the machine to do?** Make row 20 of the parity table ("write a node (spawn gate, schemas)") true WITHOUT the old write.py: growth order is a matrix the graph carries, a key is the hash of the row that allows the step, and the gate is a lookup. Same lens as §U: a policy row, named by its hash, is the key.
```
SCHEMAS  .agi/context/schemas/[type].md spawn blocks (allowed_parents · min/max · parent_shapes · min_parents_by_type · variants)
   │  grow-project (expansion, runs when a schema changes)
   ▼
MATRIX   fenced TSV `nid · child · variant · parents · ring` + `@short type` alias rows
         parents = parent TYPES sorted, +-joined (`-` = none) · variant = `goal_kind=subgoal` / `build_kind=code` / `-`
         ring = who must sign the add (`*` any post cert · `owner` for moral) · nid = 16 hex sha256 of the row after nid = the NODE KEY
   │  UNLOCK = look the row up for (child, variant, parent types) -> its nid, or the legal shapes for that child
   ▼
WINDOW   Y2 opens on the nid: child[variant]'s schema fields first · Y3 checks each row against that same schema
   ▼
ADD      the node carries `key: <nid>` in its frontmatter -> a signed commit (§W)
   ▼
GATE     grow-gate (pre-receive / the land step), everything read at the RECEIVING trunk tip (git archive: matrix + schemas):
         ADDED: grow-check (row missing = `wrong order` + the legal shapes · no key / another row's = `locked` · ring ≠ * and ≠ signer = refused)
                + Y2's `agi-fill check` (the fields, exactly as the window refuses them)
         CHANGED: `agi-fill check` as a RATCHET: refused only if the version it replaces passed (legacy stays editable, nothing valid regresses)
         RULES: a commit touching a [type].md schema or growth.tsv lands only signed by the seed's anchor K (owner or Prime; belam 07:4xZ, option A)
```
**Every schema mapped, measured 07:2xZ** (`grow-project` over the 22 live schema files): 20 carry a spawn block, 2 do not (`[box]`, `[shape]`); **149 shape rows + 2 alias rows**, 7,111 B:
| child | rows | | child | rows | | child | rows |
|---|---|---|---|---|---|---|---|
| goal (4 variants) | 29 | | idea | 9 | | config | 5 |
| experiment | 27 | | mvp | 9 | | vision | 5 |
| bigger_outcome | 14 | | outcome | 9 | | overview | 4 |
| hypothesis | 14 | | verdict | 9 | | command · cron · doc · ladder · moral · task · town | 1 each |
| build (2 variants, parent_shapes) | 8 | | | | | | |

**Tested 07:2xZ** (scratch, no root; `grow-check` on synthetic nodes, then `grow-gate` as a pre-receive on a bare repo with throwaway owner + dg5 signing keys):
| # | case | result |
|---|---|---|
| T1 | hypothesis under an idea, with its key | `ok ffdc586128924f86 *` |
| T2 T7 | the same shape, no key · moral (no parents) | `locked: key none is not ffdc…` · `ok 2fe50ba4… owner` |
| T3 T4 | mvp under a goal · a build from a lone goal | `wrong order` + the legal shapes for that child (build: `build+goal goal+idea goal+mvp mvp`) |
| T5 T6 | build vN under build+goal (code) · with the PROSE variant's key | ok · `locked` (a key opens one variant) |
| T8 | a subgoal under a lone build | `wrong order` (min_parents_by_type goal ≥ 1 held) |
| T9 | hypothesis under idea+idea with the single-idea key | `locked` (a key opens one shape) |
| T10 T11 | inline `parents: [a, b]` · a parent id written `hyp:…` | ok · ok (the alias cell) |
| **P** | **parity: the shell `grow-check` on EVERY live node vs the old `spawn_gate.check_spawn`** | **5,390 / 5,390 agree**: 5,087 legal in both, 303 refused in both (season-1, grandfathered: never re-gated) · 0 admitted by one and refused by the other · 33.5 s for both gates together |
| G1-G4 | moral (owner-signed) -> vision -> idea -> hypothesis, one push each | landed, in order |
| G5 | an mvp straight under the idea | refused: wrong order |
| G6 | a moral signed by dg5 | refused: `ring owner, signed by dg5` |
| G7 | a legal hypothesis with no key | refused: locked |
| G8 | ONE push carrying a re-keyed matrix (mvp under idea added) AND such an mvp | refused: the gate reads the RECEIVING side's matrix; against the pushed one it would pass, so a push cannot re-key its own add |

**The Y3 seam, tested 07:4xZ** (alive's ask: every added OR changed node also passes Y2's check at receive; a fresh trunk seeded with the 22 LIVE schemas + the projected matrix, bodies = REAL live nodes, `agi-fill check` = Y2's own verb @c7532c191; throwaway owner · dg5 · anchor keys):
| # | one push | result |
|---|---|---|
| Ya | a valid live hypothesis under an idea, keyed | landed |
| Yb | an added idea with `status: banana` (Y3.6) | refused: `status : 'banana' does not match ...` |
| Yc | an EDIT turning a valid idea's status to banana | refused: `was valid:` + the field |
| Yd | an edit of a LEGACY hypothesis that already lacks `testable_claim` | landed (the ratchet) |
| Ye Yf Yg | an mvp under an idea · a moral signed by dg5 · signed by owner | refused (order) · refused (ring) · landed |
| Yh | ONE push: the idea schema widened to allow banana + a banana idea | refused (the RECEIVING schema judged it) |
| Yi | ONE push: the matrix re-keyed (mvp under idea) + that mvp | refused (the RECEIVING matrix) |
| Yh' Yi' | the same two pushes signed by the ANCHOR | still refused: a rule change never judges the push that carries it |
| Yj | a schema-only widen (idea status + banana) signed by dg5 | refused: `changes the rules, not signed by the anchor` |
| Yk Yl | the same widen signed by the anchor · then a banana idea by dg5 | landed · landed (the rules were widened by the anchor first) |
**Why the ratchet (measured, Y2's own verb @c7532c191 on every live node):** it refuses **238 of 5,402 live nodes today** -- `testable_claim` 123 hypotheses · `scale` 39 ideas · `tags` 26 docs + 6 visions · `origin` 20 builds + 10 goals · `seeds` 11 goals · 3 others. The ratchet was accepted as designed (belam 07:4xZ). Strict on CHANGED would freeze those 238 against every edit; the ratchet leaves them editable and lets no valid node regress. A legacy node can still gain a NEW error on edit (the check compares pass/fail, not error sets): named, unbuilt.
**The parity gap found on the way:** 151 live nodes first disagreed, every one a parent id written with a short prefix (`hyp:` 97, `exp:` 65 parent refs). The old gate typed parents through a full index scan; Y1 types them by id prefix + a 2-row alias cell (`@hyp hypothesis`, `@exp experiment`), so the gate reads ONE file, never the graph. The aliases are a cell (config-max), not code.
**Bytes (expansion, 0 B in the zygote):** `grow-check` 1,298 B · `grow-gate` 1,720 B (with Y2's check, the ratchet, the receiving-tip read and the anchored rules) · `grow-project` 1,185 B (python + yaml, run only when a schema changes; its output is committed) · the matrix 7,111 B of graph data · the unlock = one awk row lookup inside Y2. The old path it replaces for adds: `spawn_gate.py` (1,507 lines, 65,335 B) on write.py's create path.
`grow-check` whole:
```sh
#!/bin/sh
# grow-check MATRIX NODE.md: legal only if the node's row (type · variant · parent types sorted · ring) is in MATRIX AND its `key:` is that row's nid
# prints `ok <nid> <ring>` (the hook matches ring to the commit's signer) or `refused: <why>` + the legal shapes; rc 0 | 1
awk -F'\t' 'NR==FNR&&/^@/{A[substr($1,2)]=$2;next} NR==FNR{n[$2 FS $3 FS $4]=$1 FS $5;if($3!="-"){split($3,e,"=");f[$2]=e[1]};s[$2 FS $3]=s[$2 FS $3]" "$4;next}
FNR==1&&/^---/{h=1;next} h&&/^---/{h=0} !h{next}
/^type:/{t=$0;sub(/^type: */,"",t)} /^key:/{k=$0;sub(/^key: */,"",k)} /^parents: *\[/{gsub(/[][ ]|parents:/,"");c=split($0,q,",");for(i=1;i<=c;i++)P[++p]=q[i]}
/^parents: *$/{l=1;next} l&&/^ *- /{x=$0;sub(/^ *- */,"",x);P[++p]=x;next} l{l=0} {split($0,y,": *");a[y[1]]=y[2]}
END{if(t==""){print "refused: not a node (no type:)";exit 1};for(i=1;i<=p;i++){sub(/:.*/,"",P[i]);if(P[i] in A)P[i]=A[P[i]];for(j=i;j>1&&P[j-1]>P[j];j--){z=P[j];P[j]=P[j-1];P[j-1]=z}}
 r="";for(i=1;i<=p;i++)r=r (i>1?"+":"") P[i];if(r=="")r="-";v=f[t]?f[t]"="a[f[t]]:"-";w=t FS v FS r
 if(!(w in n)){print "refused: wrong order: "t" ("v") under ["r"]; legal:"s[t FS v];exit 1};split(n[w],o,FS)
 if(k!=o[1]){print "refused: locked: key "(k?k:"none")" is not "o[1]" for "t" under ["r"]";exit 1};print "ok "o[1]" "o[2]}' "$1" "$2"
```
`grow-gate` whole (the trunk ref, the allowed-signers path and the anchor K are cells; `agi-fill check` is Y2's verb):
```sh
#!/bin/sh
# pre-receive (the land gate), all against the RECEIVING trunk tip (matrix + schemas via git archive; a push cannot re-key or re-schema itself):
# ADDED node -> grow-check (order + key; a ring other than * = the commit's signer, §W) + agi-fill check (Y2's fields) · CHANGED node -> agi-fill
# check as a RATCHET (refused only if the version it replaces passed: legacy nodes stay editable, nothing that passed can regress)
A=${AGI_ALLOWED:?};K=${AGI_ANCHOR:?};t=$(mktemp -d);trap 'rm -rf $t' EXIT;R=$(git rev-parse -q --verify ${AGI_TRUNK:-refs/heads/main})||{ echo "refused: no receiving trunk";exit 1;}
git archive $R .agi/context/schemas .agi/nodes/.geometry/growth.tsv|tar -x -C $t||exit 1;k(){ (cd $t&&agi-fill check $1)>$t/e 2>&1;}
while read o n r;do for c in $(git rev-list $n --not --all);do
 git diff-tree -r --root --no-commit-id --name-only $c -- .agi/context/schemas .agi/nodes/.geometry/growth.tsv|grep -q .&&{ git -c gpg.ssh.allowedSignersFile=$K verify-commit $c 2>/dev/null||{ echo "refused: $c changes the rules, not signed by the anchor";exit 1;};}
 s=$(git -c gpg.ssh.allowedSignersFile=$A verify-commit --raw $c 2>&1|sed -n 's/.*signature for \(.*\) with.*/\1/p')
 git diff-tree -r --root --no-commit-id --diff-filter=AM --name-status $c -- .agi/nodes|grep '\.md$'|grep -v /deprecated/>$t/l
 while read m f;do git show $c:$f>$t/n;if [ $m = A ];then v=$(grow-check $t/.agi/nodes/.geometry/growth.tsv $t/n)||{ echo "$f: $v";exit 1;}
  g=${v##* };[ "$g" = '*' ]||[ "$g" = "$s" ]||{ echo "$f: ring $g, signed by ${s:-nobody}";exit 1;};k n||{ echo "$f:";cat $t/e;exit 1;}
  else k n||{ git show $c^:$f>$t/p;! k p||{ echo "$f: was valid:";k n;cat $t/e;exit 1;};};fi;done<$t/l||exit 1;done;done
```
`grow-project` whole:
```python
#!/usr/bin/env python3
# grow-project SCHEMAS > matrix: every [type].md spawn block -> one row per legal parent shape: nid child variant parents ring
# then the ALIASES cell as @short<TAB>type rows (an id prefix that names a type) · parents = parent TYPES sorted, +-joined (- = none); nid = 16 hex sha256 of the row after nid = the NODE KEY; a schema edit re-keys
import sys,glob,re,yaml,hashlib,itertools as I
[print('@'+l,end='') for l in open(sys.argv[2])]
for f in sorted(glob.glob(sys.argv[1]+'/[[]*].md')):
 t=f.split('[')[-1][:-4];s=(yaml.safe_load(re.match(r'---\n(.*?)\n---',open(f).read(),re.S)[1]) or {}).get('spawn')
 if not s:continue
 d=s.get('discriminator');vs=[(d+'='+k,v) for k,v in s['variants'].items()] if d else [('-',s)]
 for v,r in vs:
  sh=r.get('parent_shapes') or [c for n in range(r['min_parents'],r['max_parents']+1) for c in I.combinations_with_replacement(sorted(r['allowed_parents']),n)]
  for c in sorted({tuple(sorted(x)) for x in sh}):
   if all(c.count(p)>=n for p,n in (r.get('min_parents_by_type') or {}).items()):
    l='\t'.join([t,v,'+'.join(c) or '-','owner' if t=='moral' else '*']);print(hashlib.sha256(l.encode()).hexdigest()[:16]+'\t'+l)
```
**Not carried by Y1 (named, each its own home):** (1) parent EXISTENCE: `links.py` (broken = 0) stays that gate; Y1 checks types and order, never that a parent file exists (2) the per-town VISION CAP (spawn_gate 5b) is a COUNT, not a shape: a cell + a count line, unbuilt (3) `season_parents` is a second edge field (vision -> overview): the same matrix with an `edge` column, unbuilt (4) a CHANGED node is re-checked for its FIELDS (the ratchet) but not for its ORDER: an edit of `parents` is not re-keyed (grow-check on M would refuse the 303 grandfathered nodes on every edit until a season cell exempts them) (6) RULED (belam 07:4xZ, option A, built here): a schema or matrix change lands only anchor-signed (Yj-Yl), with §T's own verify-commit, 0 new mechanism (5) the matrix must be re-projected when a schema changes: a CHECK line `grow-project | cmp - matrix` (the §U pattern) catches drift; a schema edit re-keys ONLY the rows it changes.
**Flag for the council (not a Y1 rule):** belam's brief reads "a hypothesis under an idea, never under a bare goal", but `[hypothesis].md` allows `goal` today (row `21e059b9381fa3cf hypothesis - goal *`). Y1 maps the schemas AS THEY ARE; forbidding it is a one-cell schema edit (drop `goal` from allowed_parents), which re-keys 4 rows and grandfathers the live ones.
**Falsifiers.** T1-T11 · P · G1-G8 PASS (scratch) · **Y1.12** DG3's build: write.py's create path calls `grow-check` and the parity run stays 5,390/5,390 (UNRUN) · **Y1.13** parity row 20 MATCH with the old write.py REMOVED from the clone (UNRUN; the Phase 3 gate) · **Y1.14** a Y2 window opened with a nid writes a node that `grow-gate` lands, and one opened with no nid writes nothing (UNRUN; the seam with Y2) · **Y1.15** the owner ring: a moral lands only under the owner's phone cert (§X) (UNRUN) · Ya-Yl PASS (scratch, Y2's real verb) · **Y1.16** the ratchet on the live trunk: an edit to each of the 238 legacy-invalid nodes lands, an edit breaking any of the 5,164 valid ones is refused (UNRUN at scale).

## Y2 · ROUND 7 · self-perpetuating -- the CAPTIVE FILL WINDOW: a node key opens it, the format comes first, ONE tool call (or row by row) closes it
**Owner 07:1xZ:** "only the correct node key schema unlocks next node add to graph. And that smoothly launches a captive graph fill window that uses standard tool call shorthand capture or similar and lists appropriate formate first thing. Also has a row by row option with row by row checks to allow weaker models to slot in better." **What am I ACTUALLY trying to get the machine to do here?** Make the only way a node can grow be the way its schema says, and make that way easy enough for the smallest model: show the shape, take one answer, check it, write it, close. A grown node carries the key and the exact schema bytes it grew under, so the graph can always be re-checked against its own history.
```
Y1 unlock (nid)  ─▶ agi-fill open NID PARENT..   parent TYPES re-checked against the row (wrong order -> refused, rc 2)
                 ─▶ ~/.fill  = the window (nid · child · parents · schema id · the JSON Schema · opened · tries · rows)
                 ─▶ PRINTS, FORMAT FIRST: an OpenAI tool definition {name: add_<child>, parameters: <JSON Schema from [child].md>}
captive          PreToolUse hook agi-captive: while ~/.fill exists, EVERY tool but `agi-fill` is refused (exit 2; pi through cccc.ts)
answer   call    ONE tool call on stdin, any of 3 shorthands: OpenAI {name, arguments(obj|str)} · Anthropic {type: tool_use, input} · bare arguments
         row     agi-fill row "field: value": each row checked AS IT LANDS against its own sub-schema; it prints the next required field; "." writes
gate             the Draft-7 check of the WHOLE object (Y3 owns the gate; this is its deterministic stand-in) -> refused: each field named, tries+1
receive          agi-fill check FILE: the same schema check of a node that arrives by any path (all-is-one's grow-gate @92d577161 calls it per added node, cwd = the receiving tip; exit 3 + one `refused <field> : <msg>` line per error, the missing field NAMED)
close            written (node file with key: <nid> + schema: <child>@<blob>) · agi-fill close · timeout (cell fill_window, 900 s) · N failed tries (cell fill_tries, 3)
```
**The schema -> format rule, measured for parity with the old gate (write.py / schema_registry):** required = `validation.required` minus what the window writes itself (id, type, mint_id, parents, next_edges, key, schema) · types ONLY from `validation.types` · `regex` / `item_regex` -> `^(?:..)$` (the old gate uses fullmatch) after stripping each cell's OWN `^`/`$` and writing `\d` as `[0-9]` (alive, Y3, measured with llama.cpp's grammar compiler: inner anchors made every enum and goal_id an 'accept any string' rule and `\d` an unsupported escape -- 15/25 formats fenced before, 20/25 after; the gate's verdicts did not move) and a regex field must be a STRING · the variant's discriminator (goal_kind, build_kind) = `const` · every other field = a property with its declared type as a DESCRIPTION hint (Y3 may decode with it; the gate does not enforce it) · extra fields allowed (5,322 live nodes carry fields outside their schema).
**What a post sees** (verbatim, a hypothesis under an idea):
```
FILL WINDOW OPEN: hypothesis under idea:i-x · key ffdc586128924f86 · schema hypothesis@35ddbda8c73f
FORMAT (answer with ONE call to this tool, nothing else):
{"type": "function", "function": {"name": "add_hypothesis", "parameters": {"type": "object", "properties": {"title": ...
send: agi-fill call (OpenAI, Anthropic or bare arguments) · row by row: agi-fill row "field: value", then "." · abort: agi-fill close · closes after 900s or 3 failed tries
```
**Tested 07:2xZ** (scratch workspace with the live schemas, a stand-in growth matrix in Y1's columns; nothing written to MAIN):
| claim | result |
|---|---|
| PARITY: every live node through the window's schema vs the OLD gate | 5,398 nodes: 5,393 same verdict; the 5 others lack next_edges / mint_id, which the window always writes |
| every [type] + variant renders a valid Draft-7 JSON Schema | 25 of 25 (22 types; goal x4, build x2) |
| wrong order: a hypothesis under a bare goal | refused, rc 2, naming the row's order |
| a parent written with a short prefix (`hyp:x`), resolved through Y1's `@short type` alias rows (all-is-one 07:3xZ: 151 live nodes use them) | opens; `hypothesis:x` opens the same window; an `idea` parent is still refused |
| captive: Write · Bash ls · Bash agi-fill, while open; Write after close | 2 · 2 · 0 ; 0 |
| OpenAI shorthand missing testable_claim · Anthropic tool_use valid · OpenAI nested with STRING arguments | refused, the field named · written · written |
| row mode, goal[subgoal]: goal_kind perpetual · goal_id 7.99 · G7.99 · confidence high · an unknown field · "." | refused (const subgoal) · refused (pattern) · ok · refused (number) · refused · written |
| a number in a regex field via call | refused (must be a string) -- the first draft let it through and the OLD gate caught it: the oracle earned its place |
| 3 failed tries · close · timeout | closed, nothing written · closed · closed, rc 4 |
| every node the window wrote, through the OLD gate | 0 errors |
| after the anchor fix (07:4xZ): the sweep again · `agi-fill check` vs the OLD gate on 400 live nodes · row mode: goal_id 7.99 · G7.99 · status sleeping | 5,395/5,400, the same 5 · 400/400 agree (21 refused by both) · refused · ok · refused (enum) |

**Bytes (expansion, config:engine-wrap; 0 B in the zygote):** `agi-fill` 5068 B (python3 + yaml + jsonschema, both already on the box) · `agi-captive` 311 B · settings.json +61 B (one PreToolUse line) · cells `fill_window`, `fill_tries`. Retires, once Y1-Y3 are built: write.py's spawn gate and create path for NEW nodes (parity row 20 stops leaning on the old Python; the old gate stays the ORACLE in the suite until Phase 3 closes).
**Honest limits.** (1) The captive hook only fences TOOLS: a post can still type prose; it cannot write a file or run another command until the window closes. (2) A lookahead in `tags`'s item_regex (`(?!parked:)`) is a JSON-Schema pattern here but cannot be a GBNF rule: under Y3's grammar that one field stays gate-checked, not decode-fenced. (3) The body (the schema's prose order, e.g. a hypothesis's ## Measured .. ## CEILING) is one free string: format-first shows it only if Y3 adds it as a pattern; a merge-up reviewer still checks prose. (4) Real ids come from the slug of the title; a clash is refused (rc 5), never overwritten.
Falsifiers: **F46** the parity sweep above (PASS: 5,393/5,398, the 5 explained) · **F47** the test table (PASS) · **F48** a pi-free post, captive, fills a hypothesis through the window in one call (unrun: needs DG5 on the new engine) · **F49** a 1-3 B local model in ROW mode under Y3's grammar writes a node the old gate accepts (unrun: Y3).
`agi-captive` whole:
```sh
#!/bin/sh
# PreToolUse while a fill window is open: ONLY agi-fill passes; exit 2 = refused (claude natively; pi through cccc.ts)
[ -e "${AGI_FILL:-$HOME/.fill}" ]||exit 0;jq -r '.tool_input.command//""'|grep -q '^agi-fill '&&exit 0;echo "captive: a fill window is open -- agi-fill call | row | close">&2;exit 2
```
`agi-fill` whole:
```python
#!/usr/bin/env python3
# agi-fill open NID PARENT.. | call <TOOLCALL | row <"field: value".. | close -- the captive fill window a node key opens (§Y2): format FIRST, one tool call or row by row, closes on write, abort, timeout or N tries
import sys,os,re,json,time,uuid,subprocess as S,yaml,jsonschema
A=sys.argv;E=os.environ.get;W=os.path.expanduser(E('AGI_FILL','~/.fill'));L=int(E('AGI_FILL_WINDOW','900'));N=int(E('AGI_FILL_TRIES','3'))
a=lambda r:re.sub(r'^\^|(?<!\\)\$$','',r).replace('\\d','[0-9]')
X={'id','type','mint_id','parents','next_edges','key','schema','scaffold_hash'};F_=lambda x:x.path[0]if x.path else x.message.split("'")[1]if x.validator=='required'else'-'
J={'str':'string','int':'integer','float':'number','bool':'boolean','dict':'object','list':'array'}
def sch(c,v):
 p=f'.agi/context/schemas/[{c}].md';d=yaml.safe_load(open(p).read().split('\n---',1)[0][4:]);V=d.get('validation')or{};T=V.get('types')or{};F=d.get('fields')or{};P={}
 for k in [*F,*V.get('required',[])]:
  if k in X or k in P:continue
  f=F.get(k);t=T.get(k);s={'type':J.get(t,'string')}if t else{'description':str((f.get('type')if isinstance(f,dict)else f)or'str')}
  if k in(V.get('regex')or{}):s={'type':'string','pattern':f"^(?:{a(V['regex'][k])})$"}
  if k in(V.get('item_regex')or{}):s['items']={'type':'string','pattern':f"^(?:{a(V['item_regex'][k])})$"}
  P[k]=s
 k=(d.get('spawn')or{}).get('discriminator')
 if k and v!='-':P[k]={'const':v}
 P['body']={'type':'string'};return c+'@'+S.run(['git','hash-object',p],capture_output=True,text=True).stdout[:12],{'type':'object','properties':P,'required':[k for k in V.get('required',[])if k not in X],'additionalProperties':True}
def end(m,r=0):
 os.path.exists(W)and os.remove(W);print(m);sys.exit(r)
def done(w,a):
 e=sorted(jsonschema.Draft7Validator(w['js']).iter_errors(a),key=lambda e:list(e.path))
 if e:
  w['tries']+=1;[print('refused',F_(e),':',e.message[:160])for e in e]
  w['tries']<N or end(f'window closed: {N} failed tries, nothing written',4);json.dump(w,open(W,'w'));sys.exit(3)
 s=re.sub('[^a-z0-9]+','-',str(a.get('title')or w['nid']).lower()).strip('-')[:60];p=f".agi/nodes/{w['child']}/{s}.md"
 os.path.exists(p)and end('refused: '+p+' exists',5);os.makedirs(os.path.dirname(p),exist_ok=True);b=a.pop('body','# '+str(a.get('title',s)))
 fm={'id':w['child']+':'+s,'type':w['child'],'mint_id':uuid.uuid4().hex,'parents':w['parents'],'next_edges':[],'key':w['nid'],'schema':w['schema'],**a}
 open(p,'w').write('---\n'+yaml.safe_dump(fm,sort_keys=False,allow_unicode=True)+'---\n\n'+b.rstrip('\n')+'\n');end('written '+p)
if A[1]=='open':
 G=[l.rstrip('\n').split('\t')for l in open(E('AGI_GROWTH','.agi/nodes/.geometry/growth.tsv'))];Z={l[0][1:]:l[1]for l in G if l[0][:1]=='@'}
 r=[l for l in G if l[0]==A[2]]or end('refused: no growth row '+A[2],2)
 n,c,v,par=r[0][:4];g='+'.join(sorted(Z.get(x.split(':')[0],x.split(':')[0])for x in A[3:]))
 g==par or end(f'refused: parents {g} but row {n} unlocks {par} -> {c}',2)
 sid,js=sch(c,v);json.dump({'nid':n,'child':c,'parents':A[3:],'schema':sid,'js':js,'t':time.time(),'tries':0,'rows':{}},open(W,'w'))
 print('FILL WINDOW OPEN: '+c+('' if v=='-' else f'[{v}]')+f' under {" ".join(A[3:])} · key {n} · schema {sid}\nFORMAT (answer with ONE call to this tool, nothing else):')
 print(json.dumps({'type':'function','function':{'name':'add_'+c,'parameters':js}}))
 print(f'send: agi-fill call (OpenAI, Anthropic or bare arguments) · row by row: agi-fill row "field: value", then "." · abort: agi-fill close · closes after {L}s or {N} failed tries');sys.exit()
if A[1]=='check':
 fm=yaml.safe_load(open(A[2]).read().split('\n---',1)[0][4:]);c=fm['type'];k=(yaml.safe_load(open(f'.agi/context/schemas/[{c}].md').read().split('\n---',1)[0][4:]).get('spawn')or{}).get('discriminator')
 e=list(jsonschema.Draft7Validator(sch(c,str(fm.get(k))if k and fm.get(k)else'-')[1]).iter_errors({x:y for x,y in fm.items()if x not in X}));[print('refused',F_(x),':',x.message[:160])for x in e];sys.exit(3 if e else 0)
os.path.exists(W)or end('no window open',2);w=json.load(open(W))
time.time()-w['t']<L or end('window closed: timeout, nothing written',4)
if A[1]=='close':end('window closed: aborted, nothing written')
if A[1]=='call':
 x=json.loads(sys.stdin.read());a=x.get('arguments')or x.get('input')or(x.get('function')or{}).get('arguments')or x
 done(w,json.loads(a)if isinstance(a,str)else a)
for l in(A[2:]or sys.stdin.read().splitlines()):
 if l.strip()=='.':done(w,dict(w['rows']))
 k,_,v=l.partition(':');k=k.strip();v=v.strip();s=w['js']['properties'].get(k)
 if s is None:print('refused row',k,': not a field of',w['child']);continue
 if s.get('type',s.get('description','str'))not in('string','str'):v=yaml.safe_load(v or'null')
 m=[e.message[:160]for e in jsonschema.Draft7Validator(s).iter_errors(v)]
 if m:print('refused row',k,':',m[0])
 else:w['rows'][k]=v;print('ok',k)
json.dump(w,open(W,'w'));r=[k for k in w['js']['required']if k not in w['rows']];print('next:',(r[0]+' ('+json.dumps(w['js']['properties'][r[0]])+')')if r else'"." to write')
```

## Y3 · ROUND 7 · alive -- ROW BY ROW and THE GATE: one JSON Schema is both the check and the fence; as Y2 wrote it, llama.cpp could fence only 15 of 25 node formats, and three small changes bring that to 25 of 25 with 0 gate verdicts moved
**Owner 07:1xZ (verbatim on the goal):** "... Also has a row by row option with row by row checks to allow weaker models to slot in better. Local models could slot in and be able to bypass decoder entirely potentially due to matrix math base. Tiny models could help do the format checking natively like jev but like absolutely tiny where we can trace everything fully" **What does a fence TRULY stop?** Only what the runtime compiled. So the reading that counts is llama.cpp's own: hand it each format and see what it says it dropped.
```
Y2 sch(child, variant) ─▶ ONE Draft-7 JSON Schema per format (25 = 21 types + goal x4 + build x2 variants)
   ├─ GATE    jsonschema over the WHOLE object, every row as it lands (Y2 row mode) AND at receive (Y1's grow-gate) = the truth, deterministic
   └─ FENCE   the same object, closed (additionalProperties false), sent as the request's json_schema -> llama.cpp compiles it to its grammar
              call mode = the whole object · ROW mode = the next field's one-property schema (Y2 already prints it as "next:") -> 0 new grammar bytes
JUDGE      only what no regex can say (is this claim falsifiable? is this title a duplicate?): a tiny model, ADVISORY, one ledger row, never format
```
**Measured 07:2x-07:3xZ** with this box's own llama.cpp build: `llama-cli -j <schema>` compiles the schema while it parses its arguments, BEFORE any model loads, and names every pattern it drops. So the probe needs no model, no GPU (`CUDA_VISIBLE_DEVICES=` empty) and not the model slot (another post's run has held it since 05:11Z):
| step | formats fenced cleanly | what llama.cpp dropped ("accepting any string") |
|---|---|---|
| Y2's schema as written | 15 / 25 | EVERY enum: status, goal_kind, scale, verdict, axis, effort, and goal_id: `^(?:^(a\|b)$)$` = "anchor inside the pattern" |
| 1 strip the cell's own `^` `$` before wrapping | 18 / 25 | goal_id + verdict: "unsupported escape: \d" |
| 2 `\d` -> `[0-9]` | 20 / 25 | tags (goal x4, hypothesis): `(?!parked:)` = "unsupported group syntax" (no GBNF has a lookahead) |
| 3 the tags cell written without the lookahead | **25 / 25** | nothing |
| the gate after 1-3, over every live node (Y2's own sch + jsonschema) | 5,381 nodes: **0 verdicts moved** (5,143 pass · 238 refused, before and after) | -- |
| the lookahead-free tags cell vs the old one | 16,637 strings (523 live tag values + every string of <= 4 chars over `pa rkd:g1.` and a newline): **0 disagreements** | -- |

The gate saw nothing wrong. Only the fence was weak: a weak model in row mode under its grammar could have written `status: banana`, and the gate would have refused it after the fact on every try. With 1-3 the grammar refuses it, so the window's three tries are spent on meaning, not on spelling.
The changes, whole:
~~~
sch() in agi-fill (Y2), +80 B: a=lambda r:re.sub(r'^\^|(?<!\\)\$$','',r).replace('\\d','[0-9]') -- and wrap a(V['regex'][k]) / a(V['item_regex'][k]) where it wraps them raw today
                              (1 + 2; no schema regex holds \d inside a [class], checked over all 13 regex cells)
[goal].md + [hypothesis].md  validation.item_regex.tags, one cell each (3), 37 B -> 156 B, the same language:
   |[^p\n][^\n]*|p([^a\n][^\n]*)?|pa([^r\n][^\n]*)?|par([^k\n][^\n]*)?|park([^e\n][^\n]*)?|parke([^d\n][^\n]*)?|parked([^:\n][^\n]*)?|parked:g\d+(\.\d+)*
the fence copy               additionalProperties false + the request's json_schema / response_format, in agi-infer (round 5) -- ~60 B
the gate at receive          Y1's grow-gate: for each added or changed node, run Y2's check on its frontmatter (one `agi-fill check FILE` verb, ~150 B, Y2's), so a node
                              committed WITHOUT the window is refused at the push exactly as the window would refuse it
~~~
**"Bypass the decoder entirely", measured:** in a closed grammar with a fixed field order, the key names, the punctuation, every const and every enum value after its first distinguishing byte are FORCED: the model has exactly one legal next token, so a runtime with jump-forward decoding appends those bytes without sampling. Over every live node's schema fields, forced = **7.2 %** of 3,901,443 frontmatter bytes (goal 31.9 % · build 36.5 % · verdict 24.1 % · experiment 8.7 % · hypothesis 2.0 %, because its long free-text claims dominate). So the decoder is FENCED, not bypassed: it is skipped for about a third of a goal's bytes and almost none of a hypothesis's. The bytes worth a model's thought are the free-text ones, and that is where the tiny judge goes.
**The tiny judge (design only):** it never checks format (the gate does, and is fully traceable as it stands); it scores only free text the schema cannot (falsifiable claim · duplicate title · a body section named but empty), writes ONE advisory row (node, score, the features that fired) into the window's ledger, and never blocks. Traceable = small enough to print whole (a linear model over n-gram features, every weight visible), trained on the live graph's own accept/refuse history.
**Dropped, on purpose:** my first draft of this section was its own reader (`fmt`, 2,671 B: rows + check + a regex->GBNF translator). Y2's `sch()` already reads the schema once, and llama.cpp already turns JSON Schema into grammar, so `fmt` would have been a SECOND source for the same rule. Kept from it: its parity sweep, which agrees with Y2's (the engine-stamped keys `edited_by`, `season`, `scaffold_hash`, `town` ... are in no schema's fields, so a model row naming one is refused; the window writes them).
**Honest limits.** (1) `\d` -> `[0-9]` narrows the gate to ASCII digits (Python's `\d` also matches other scripts' digits; 0 live nodes use one). (2) The compile probe proves the grammar EXISTS and is complete; it does not prove a model writes well under it (Y3.5). (3) A fixed field order is a choice of the fence; the gate accepts any order.
**Falsifiers.** **Y3.1** 25/25 compile clean after 1-3 (PASS) · **Y3.2** 0 gate verdicts moved on 5,381 live nodes (PASS) · **Y3.3** the tags cell equivalence, 16,637 strings (PASS) · **Y3.4** forced share 7.2 % (MEASURED) · **Y3.5** the 9B on this box, ROW mode under the closed grammar, 20 fills of `goal[subgoal]` and `hypothesis`: 0 format refusals by the gate, every refusal a meaning one (UNRUN: needs the model slot; = Y2's F49) · **Y3.6** a node pushed without the window, carrying `status: banana`, is refused at receive by grow-gate + check (UNRUN: the ~150 B verb).

## Z1 · DESIGN ROUND (belam 18:1xZ) · alive -- the POST TREE is two cells in config:posts; what a post may grow = its grow mask times the growth matrix, inside the subtree of its cert's roots; measured: today's owning_goal would refuse 71 % of real work, so the ROOTS come from the cert, never from the row
**Owner (verbatim on goal:g7.16.1.11, THOUGHT @bd53e5b0e / @3f37df695):** "... Then also each individual node has its own private key so when a post is assigned to grow a specific chain they can only keep growing that chain via the key-chain rules. The matrix weights determine which graph actions are and aren't allowed based on which node schemas allow which other node schemas as parents, and also determine which specific graph coordinate(s) the given post is able to fill in given their permission scope over the graph" / "... We could have the posts be setup as an actual hierarchical shape in the .geometry graph section and the parent-child relationships between posts determine how scope certificates get nested." **What may this post TRULY grow, as one read?** Three facts, each already a matrix: the growth matrix (Y1), the post's grow mask, and the subtree under its roots.
```
TREE     config:posts IS the shape (already .geometry): each row + `parent` (the post that issues to it; belam's = owner) + `grow` (child types, * = any)
         `roots` = the CEILING of what its issuer may hand it (the row's owning_goal today, a list, * = all) -- never the scope itself
CERT     Z2: owner -> belam -> master -> director -> parent -> kid, each link = sub · iss · roots · grow · nb · na · par, a SUBSET of its issuer's
         an ASSIGNMENT is a link: "grow hypothesis:X's chain" = roots [hypothesis:X], issued by the assigner, for the round's life
SCOPE    usable rows   = grow(p) x G          the growth rows (Y1: child · parents · ring) whose child type is in the post's mask
         coordinates   = closure(roots(p))    every node whose parent chain reaches one of the cert's roots (grow-scope, below)
GATE     a node add lands only if: its Y1 row's nid = its key: · child type in grow(p) · EVERY parent under roots(p) · the cert chain verifies to the anchor (Z2)
```
**Measured 18:1xZ on the live graph** (5,418 live nodes; 5,984 parent edges, the `hyp:` / `exp:` aliases resolved through Y1's alias rows):
| reading | number |
|---|---|
| nodes whose writer row has an owning_goal | 1,562 |
| ... inside that writer's own owning_goal chain | 454 (29 %) |
| ... OUTSIDE it | **1,108 (71 %)**: experiments 486 · hypotheses 337 · goals 143 · verdicts 68 · mvp 24 · outcome 15 · build 13 · idea 9 |
| where the outside ones sit | under other goals 365 · under hypotheses outside the chain 337 · goal:g5 202 · goal:g7.33 73 · ... |
| writers that are not post rows at all (kids, the owner, the old engine) | 2,787 nodes |
| parentless · dangling parent refs | 97 · 95 |

**So the true state:** owning_goal names where a post STARTED, not what it grows: masters hand directors new goals by order, and directors hand parents their hypotheses. Keying the key-chain to the row would refuse 71 % of today's real growth. The scope therefore has to travel WITH the assignment, as a Z2 link issued at dispatch time (the dispatch order already names the node: it becomes the cert's roots), and the row keeps only the ceiling. Kids (2,787 nodes) are covered the same way: a kid's link comes from its parent post, never from a row.
`grow-scope` -- the coordinates check, whole (510 B; the cov() hook Z2 leaves open; edges.tsv = the adjacency matrix grow-project already walks, projected as child<TAB>parent):
~~~sh
#!/bin/sh
# grow-scope ROOTS PARENT.. < edges.tsv (child<TAB>parent): rc 0 iff EVERY parent is one of ROOTS (comma list, * = all) or descends from one
awk -F'\t' -v R="$1" -v P="$(shift;echo "$*")" 'BEGIN{n=split(R,r,",");for(i=1;i<=n;i++)root[r[i]]=1}{up[$1]=up[$1] SUBSEP $2}
function u(x,d, a,k,i){if(root["*"]||root[x])return 1;if(d>64||seen[x]++)return 0;k=split(up[x],a,SUBSEP);for(i=2;i<=k;i++)if(u(a[i],d+1))return 1;return 0}
END{m=split(P,p," ");for(j=1;j<=m;j++){delete seen;if(!u(p[j],0))exit 1}}'
~~~
**Tested:** parity with a Python ancestry walk on all 1,558 live adds that have a writer row and a parent: **1,558 / 1,558** (14.5 ms each on the whole graph) · a cycle terminates, refused · `*` passes · a first draft named its function `in` (an awk keyword) and silently refused all 454 legal adds; the parity sweep caught it.
**THE WIRING ORDER (c)**, each step with the reading that says it is done (self-perpetuating's report-only step folded in):
| # | step | why here | done when (falsifier) | today |
|---|---|---|---|---|
| W1 | SIGN every trunk landing (the landing post's §V cert, `-S` ssh) | every later check asks WHO landed it | 100 consecutive landings read `G` against the anchor-projected signers | local-maxxing trunk, last 300: 32 G · 67 U (a key outside the signers file) · 201 N · season2/main: 300 N |
| W2 | ISSUE the tree's links (Z2) + run the land gate REPORT-ONLY | a refusal must be a reading before it is a rule | every live post's chain verifies; one day of reports with 0 unexplained refusals | 0 links · `parent`/`grow` cells absent from all 31 rows |
| W3 | key: on every add (Y2's window writes it) | the gate checks the row by its key, never by inference | 0 adds without key: over a day of reports | 0 of 5,418 nodes carry key: |
| W4 | grow-gate ENFORCING at the land step (Y1 ratchet + Y3 check + this scope) | only after W1-W3 can a refusal name signer, row and chain | Y3.6 + an out-of-chain add refused + a legal add lands | no pre-receive on any trunk |
**Named, not hidden.** (1) v5's `agi-turn` stages with `git add -A`: W1 needs it to commit by path and sign, or every gate check reads a landing that nobody owns. (2) `edited_by` is the LAST editor, so the 71 % mixes adds and edits; the gate judges adds (and Y1's ratchet judges edits), so the true add-only share may differ: the land gate's report-only day (W2) measures it exactly. (3) Two cells per row (`parent`, `grow`) are a config:posts edit = an owner/Prime act; the tree's first shape is the formation as written (owner -> belam -> masters -> directors), proposed, not written.
**Falsifiers.** grow-scope parity 1,558/1,558 (PASS) · **Z1.1** W2's report-only day: every refusal is out-of-chain or unkeyed, none a walk error (UNRUN) · **Z1.2** a dispatch issues the round's link with roots = the dispatched node and a kid grows only under it (UNRUN; Z2 + the dispatch line).

## Z2 · DESIGN ROUND (belam 18:1xZ) · self-perpetuating -- RECURSIVE SCOPE CERTS: owner -> belam -> posts, each link a subset of its issuer, a revocation or a re-parent kills the whole subtree
**Owner (goal:g7.16.1.11 THOUGHT @3f37df695):** scope certs are recursive, owner -> belam -> the posts under it, each a SUBSET of its issuer; the post hierarchy decides who may issue to whom. **What am I ACTUALLY trying to get the machine to do here?** Let authority regrow down the tree without ever growing on the way: a post can hand on only what it holds, for no longer than it holds it, and pulling one link pulls everything that hangs from it.
```
link     agi-scope v1 · sub <post> · iss <issuer> · roots <chain roots, * = all> · grow <child types, * = any> · nb · na · par <hash of the issuer's own link | anchor>
         signed by the ISSUER with its §V short-lived login cert (ssh-keygen -Y sign, namespace agi-scope); the owner signs with the anchor key
         content-addressed: name = 16 hex of sha256(link text); an identical statement is never re-signed over
verify   walk leaf -> anchor; per link: the signature verifies for iss AT nb (-Overify-time: a signature cannot outlive its login cert)
         · iss = sub's parent in the post tree (Z1: the config:posts `parent` cell) · roots within the issuer's (Z1: graph ancestry) · grow subset
         · [nb, na] within the issuer's · no revocation signed by iss or an ancestor of iss · only the owner anchors
cascade  revoke = ONE signed line naming a link hash, by its issuer or any ancestor -> every chain through that link fails; a sibling's revocation is ignored
tree     move POST NEWPARENT: only a STRICT ancestor of POST, NEWPARENT inside the mover's subtree, never into POST's own subtree (no cycle), never self
         re-parenting IS revocation: the old issuer is no longer the tree parent, so the old chain fails at once; the new parent re-issues
```
**Tested 18:1xZ** (scratchpad, throwaway CA + anchor + 5 post keys with 20-min login certs; tree owner -> belam -> {dg3, dg5, sm}, dg3 -> kid; no root, nothing in MAIN):
| claim | result |
|---|---|
| owner -> belam (* / *) -> dg3 (g7.16.1.11 / hypothesis, experiment, goal) -> kid (g7.16.1.11.3 / hypothesis) | `ok kid <- dg3 <- belam <- owner` |
| kid grows hypothesis under g7.16.1.11.3.2 · under g7.16.1.12 · a goal under its root | ok · refused · refused |
| dg3 widens kid's roots to g7 · widens grow to build · gives kid a longer life than its own | refused · refused · refused (each names the link and both scopes) |
| belam issues to kid (not its tree child) · a non-owner anchors a chain | refused · refused |
| sm forges dg3's link with sm's own key (same second · a new second) · a link's text edited after signing | refused (exists, never re-signed over) · refused (signature) · refused (signature) |
| sm (a sibling) revokes belam -> dg3 · belam revokes it | ignored, kid still ok · kid refused, belam's own chain still ok |
| dg3 re-parents itself · kid moves itself · belam moves dg3 under kid · belam moves kid under belam | refused · refused · refused (cycle) · moved: kid's OLD chain refused at once; belam's re-issue verifies |
| size | a link 129 B + its SSHSIG 829 B; a 4-link chain ~3.8 KB |
**A bug the tests caught before landing:** links are content-addressed, so a forged issue with byte-identical text first OVERWROTE the real link's signature, failed, and its cleanup DELETED the real link. Fixed: an existing hash is refused untouched, and cleanup removes only what that call made.
**Bytes:** `agi-scope` 3922 B (python3 + ssh-keygen; expansion, config:capsule beside agi-sign) · the store: `.agi/scope/{certs,revoked}` + allowed_signers (2 lines: the owner anchor, the §V CA as cert-authority, both namespace agi-scope).
**Wiring order (c), the regrowth lens, ONE line for Z1:** sign landings -> **issue the tree's links and run the land gate REPORT-ONLY until every live post verifies** (a ratchet, like all-is-one's 238) -> key: on adds -> grow-gate enforcing; enforcing before every post holds a chain refuses every add.
**Honest limits.** (1) The prototype's tree is a file; live, it is config:posts rows landed through signed trunk landings, and the land gate applies the move rule to the row diff. (2) Revocations must be APPEND-ONLY: deleting a revoked/ file un-revokes, so the land gate refuses any removal under .agi/scope (unbuilt). (3) Roots coverage is an id-prefix stand-in; Z1's graph-ancestry walk replaces `cov()`. (4) A link's nb is the signer's claim, bounded only by its login cert's window (minutes). (5) Tonight the anchor key is a stand-in: like §V's CA, the stand-in signs only a TEST anchor; the real owner -> belam link waits for the owner's device.
Falsifiers: **F50** the table above (PASS) · **F51** the land gate verifies the commit signer's chain covers every added node's root and type (unrun: Z1 wiring) · **F52** a landing that deletes a file under .agi/scope/revoked is refused (unrun) · **F53** after one real rotation, a post's new session signs with a fresh §V cert and its scope chain still verifies (unrun).
`agi-scope` whole:
```python
#!/usr/bin/env python3
# agi-scope issue SUB ROOTS GROW NA PAR | verify CERT [ROOT TYPE] | revoke HASH | move POST NEWPARENT -- recursive scope certs (§Z2): attenuation-only links chained to the owner anchor; a revocation or a re-parent kills the whole subtree
import sys,os,time,hashlib,subprocess as S
A=sys.argv;D=os.environ.get('AGI_SCOPE','.agi/scope');ME=os.environ.get('AGI_SEAT','');K=os.environ.get('AGI_SIGN_KEY','')
def no(m):print('refused:',m);sys.exit(3)
def rd(p):return dict(l.split(' ',1)for l in open(p).read().splitlines()[1:])
def hx(p):return hashlib.sha256(open(p,'rb').read()).hexdigest()[:16]
def T():return dict(l.rstrip('\n').split('\t')[:2]for l in open(D+'/tree.tsv')if l.strip())
def up(p):
 t=T();r=[]
 while p in t and t[p]not in r:p=t[p];r.append(p)
 return r
def st(s):return time.strftime('%Y%m%d%H%M%S',time.gmtime(int(s)))
def sig(p,who,at):return S.run(['ssh-keygen','-q','-Y','verify','-n','agi-scope','-f',D+'/allowed_signers','-I',who,'-s',p+'.sig','-Overify-time='+st(at)],stdin=open(p,'rb'),capture_output=True).returncode==0
def sign(p):S.run(['ssh-keygen','-q','-Y','sign','-n','agi-scope','-f',K,p],check=True,capture_output=True)
def cov(c,P):return'*'in P or any(c==x or c.startswith(x+'.')for x in P)   # Z1 swaps in the graph-ancestry walk
def sub(c,p):return all(cov(x,p['roots'].split(','))for x in c['roots'].split(','))and('*'in p['grow'].split(',')or set(c['grow'].split(','))<=set(p['grow'].split(',')))
def chain(c):
 L=[]
 while True:
  f=rd(c);x=hx(c);L.append(f)
  r=f'{D}/revoked/{x}'
  if os.path.exists(r):
   v=rd(r)
   if v['by']in[f['iss'],*up(f['iss'])]and sig(r,v['by'],v['at']):no(f'link {x} ({f["iss"]} -> {f["sub"]}) revoked by {v["by"]}')
  if not sig(c,f['iss'],f['nb']):no(f'link {x}: signature by {f["iss"]} does not verify at its own time')
  if T().get(f['sub'])!=f['iss']:no(f'link {x}: {f["iss"]} is not the parent of {f["sub"]} in the post tree')
  if f['par']=='anchor':
   if f['iss']!='owner':no('only the owner anchors a chain')
   return L
  c=f'{D}/certs/{f["par"]}';os.path.exists(c)or no(f'link {x}: parent cert {f["par"]} missing');p=rd(c)
  if p['sub']!=f['iss']:no(f'link {x}: parent cert is not the issuer\'s')
  if not sub(f,p):no(f'link {x}: scope {f["roots"]}/{f["grow"]} not within {p["roots"]}/{p["grow"]}')
  if not(int(p['nb'])<=int(f['nb'])and int(f['na'])<=int(p['na'])):no(f'link {x}: validity outside the issuer\'s')
if A[1]=='issue':
 s,ro,gr,na,par=A[2:7];t=f'{D}/certs/new.{os.getpid()}';os.makedirs(D+'/certs',exist_ok=True)
 open(t,'w').write(f'agi-scope v1\nsub {s}\niss {ME}\nroots {ro}\ngrow {gr}\nnb {int(time.time())}\nna {na}\npar {par}\n');sign(t)
 x=hx(t)
 if os.path.exists(f'{D}/certs/{x}'):os.remove(t);os.remove(t+'.sig');no(f'{x} already exists: an identical statement is never re-signed over')
 os.rename(t,f'{D}/certs/{x}');os.rename(t+'.sig',f'{D}/certs/{x}.sig')
 try:chain(f'{D}/certs/{x}')
 except SystemExit:os.remove(f'{D}/certs/{x}');os.remove(f'{D}/certs/{x}.sig');raise
 print(x)
elif A[1]=='verify':
 L=chain(A[2]);f=L[0]
 if int(f['na'])<time.time():no('leaf expired')
 if A[3:]and not(cov(A[3],f['roots'].split(','))and(f['grow']=='*'or A[4]in f['grow'].split(','))):no(f'{f["sub"]} may not grow {A[4]} under {A[3]}')
 print('ok',' <- '.join(l['sub']for l in L),'<- owner')
elif A[1]=='revoke':
 os.makedirs(D+'/revoked',exist_ok=True);r=f'{D}/revoked/{A[2]}';open(r,'w').write(f'agi-revoke v1\nby {ME}\nat {int(time.time())}\n');sign(r);print('revoked',A[2],'by',ME)
elif A[1]=='move':
 p,np=A[2:4];u=up(p)
 if ME not in u:no(f'{ME} is not a strict ancestor of {p}')
 if np!=ME and ME not in up(np):no(f'{np} is outside {ME}\'s subtree')
 if np==p or p in up(np):no(f'{np} is under {p}: a cycle')
 t=T();t[p]=np;open(D+'/tree.tsv','w').write(''.join(f'{a}\t{b}\n'for a,b in t.items()));print('moved',p,'under',np,'by',ME,'-- its old chain no longer verifies; its new parent re-issues')
```

## Z3 · POST TREE ROUND · all-is-one -- RETIRE THE LADDER: one parent edge, 24 data cells to 5 homes, 15 readers behind one resolver; re-keys 3 growth rows and moves 0 verdicts
**Owner (verbatim on goal:g7.16.1.11 THOUGHT @bd53e5b0e @3f37df695 @561bc43dd; belam's brief 18:1xZ):** (3) "RETIRE THE LADDER: post tree + templates + configs on the matrix replace it." **What am I ACTUALLY trying to get the machine to do?** Make the ladder a node nobody reads, then retire it like any node: every cell it carries gets a home it already belongs to, every reader asks ONE resolver, and growth order stops naming it, all BEFORE any node carries a `key:`, so no key is ever minted for a ladder row.
```
WHAT THE LADDER IS (measured 18:1xZ, live)
  as a PARENT   1 edge only: [town] allowed_parents: [ladder]  -> growth.tsv rows `town - ladder` + `ladder - goal` (the type itself)
                the other 6 schemas named in the brief carry it as DATA ([config] town_cell accepted_from: ladder.towns) or PROSE ([moral] [bigger_outcome] [overview] [vision] [outcome])
  as DATA       .agi/nodes/.geometry/ladder.md, 10,670 B: 24 data cells, read by 15 engine files that open it (path / read_ladder* / load_ladder*)
  as NODES      5 town:* nodes carry parents vision + ladder:ladder + goal -> refused by BOTH gates today (3 parents, max 1)
RETIRE, in order (each step's falsifier below; schema steps are Option A: anchor-signed)
  1 SCHEMA   [town]: allowed_parents [goal, vision] · parent_shapes [[goal, vision]] · max 2   ·   [ladder].md out of the projector's glob
  2 MATRIX   grow-project -> growth.tsv 149 -> 148 shape rows: - `ladder - goal` - `town - ladder` + `town - goal+vision`; 147 nids UNCHANGED
  3 NODES    the 5 towns drop `ladder:ladder` from parents -> legal (only the key is missing)
  4 CELLS    each cell copied byte-equal into its home (table below) -> ONE resolver cell(name), the ladder as FALLBACK + a WARN per read
  5 READERS  the 15 files call cell(name) instead of opening the ladder -> parity: every cell via the resolver == the ladder's value
  6 RETIRE   0 WARN over a day of landings -> ladder.md status deprecated + moved to deprecated/ladder/ · [config] town_cell accepted_from -> posts.town
  then, and only then, Z1's wiring: sign landings -> key: on adds -> grow-gate (no key ever names a ladder row)
```
| cells (24 data cells of ladder.md) | read by (of the 15 openers) | home | why there |
|---|---|---|---|
| roles · tiers · mantles · mantles_prime_director · captive_rotate_masters | hierarchy · spawn_gate · harness_template · rotate · brief · rotation_alert · season | config:posts (Z1's tree) | the post tree IS the hierarchy: who sits where, with which template |
| towns · town_branches | spawn_gate · cli · towns · hierarchy · season | config:posts | the town set = the `town` cell all 31 rows already carry |
| director_rotate_at · director_context_tokens · captive_rotate_ratio · capture_chain_log · card_capture_minutes · alarms_idle_minutes | rotate · rotation_alert · seat_status | config:rotations | rotation is one cell node already |
| current_season · current_loop · season_names · caps_apply_from_season | towns · spawn_gate · seat_status · season · cli · rotate | config:engine | the loop's own clock |
| caps · caps_vision_scope · untrusted_promotion_threshold | spawn_gate · hierarchy · season (the last: none) | config:engine-grow | beside growth.tsv: the COUNT rules (Y1 limit 2, the vision cap) live with the shape rules |
| read_order | brief | config:brief | brief parts |
| budget_usd_week · spawn_profiles · zoom | **none** of the 15 | retire with the node | dead cells |
The 15 openers: spawn_gate (12 sites) · cli 6 · send 5 · brief 5 · towns 4 · rotate 4 · hierarchy 4 · write 3 · dispatch 3 · season 2 · rotation_alert · seat_status · harness_template · crons · adapters/__init__ (1 each). Method: `git grep` for `ladder.md` · `config:ladder` · `read_ladder*` / `load_ladder*` / `ladder_*` definitions, comments excluded. The brief's "19" counted by a wider pattern; 25 files merely MENTION the word.

**Tested 18:1xZ** (scratch: the live schemas copied and edited, the live `.geometry` homes copied; no live byte touched):
| # | case | result |
|---|---|---|
| Z3.1 | grow-project over the LIVE schemas vs the live growth.tsv | byte-identical (DG3's built matrix = the projection) |
| Z3.2 | grow-project over the edited copy | 149 -> 148 shape rows; exactly 3 rows differ (2 out, `00b8ef0c7c6395ec town - goal+vision *` in); 147 nids unchanged |
| Z3.3 | the 5 live towns, old matrix vs new, as they stand | refused both (they still name ladder:ladder) |
| Z3.4 | the 5 towns with `ladder:ladder` dropped, new matrix | `locked: key none is not 00b8ef0c7c6395ec` = legal order, only the key missing |
| Z3.5 | grow-check over EVERY live node, old matrix vs new | 5,438 nodes, **0 verdicts change** (47 s) |
| Z3.6 | the resolver over the 21 moved cells (scratch homes = live nodes + the cells copied in) | 21 / 21 byte-equal to the ladder's values, 0 WARN |
| Z3.7 | a home missing its cell | falls back to the ladder, prints `WARN cell roles: read from the ladder` |
**Bytes (expansion; 0 B in the zygote):** `cells.tsv` 509 B (the field -> home table, a CELL: config-max) · `cell.py` 647 B · the [town] schema edit: 3 lines · growth.tsv: -1 row. Removed once retired: ladder.md 10,670 B + [ladder].md.
`cell.py` whole:
```python
# cell(name): a former ladder field, read from its HOME node (cells.tsv: field -> .geometry/<home>.md frontmatter);
# the ladder is the FALLBACK, with one WARN per read, until the WARN count is 0 -- then the ladder retires (status deprecated + moved)
import yaml,sys,os
G=os.environ.get('AGI_GEO','.agi/nodes/.geometry');H=dict(l.split()for l in open(os.environ.get('AGI_CELLS',G+'/cells.tsv')))
fm=lambda n:yaml.safe_load(open(f'{G}/{n}.md').read().split('\n---',1)[0][4:])or{}
def cell(k,d=None):
 v=fm(H[k]).get(k)if k in H else None
 if v is None:print(f'WARN cell {k}: read from the ladder',file=sys.stderr);v=fm('ladder').get(k,d)
 return v
```
**Seams.** Z1: the five hierarchy cells land in config:posts AS THEY ARE (byte copy); reshaping them into per-row cells (`parent` · `roots` · `grow`, Z1's columns) is Z1's next step, read through the same resolver, so no reader changes twice · Z2: a scope cert names posts by the tree in config:posts; nothing in Z2 reads the ladder · Y1: the re-key is FREE now (0 nodes carry `key:`), which is why belam ordered it before the wiring; after wiring it would invalidate the 5 towns' keys only.
**Honest limits.** (1) The 5 town edits are PARENTS edits, which grow-gate does not re-gate (Y1 limit 4): they land on the ratchet, legal by Z3.4 (2) "readers" here = the 15 files that OPEN the ladder; a reader that receives a ladder value through another module's function is found only by step 5's WARN count, not by grep (3) moving [ladder].md out of the projector's glob is measured; whether `schema_registry` and the links checker tolerate its absence is step 6's falsifier, unrun (4) the cell homes are frontmatter keys added beside each node's own cells: a name clash is checked (none of the 21 exists in its home today), not enforced.
**Falsifiers.** Z3.1-Z3.7 PASS (scratch) · **Z3.8** on the trunk after steps 1-3: grow-check parity over every live node moves 0 verdicts except the 5 towns, which turn legal (UNRUN) · **Z3.9** after step 5: a full day of landings with 0 `WARN cell` lines (UNRUN) · **Z3.10** after step 6: the engine suite green and `links.py links` 0 broken with ladder.md deprecated (UNRUN) · **Z3.11** no node anywhere carries a `key:` naming a retired ladder row (UNRUN; true by order).

## AA2 · DESIGN ROUND (belam 23:34Z + owner 23:2xZ) · self-perpetuating -- THE LAP IS A PERMUTATION MATRIX: the figure eight is the one cycle of PHI on the post tree's darts, projected into the graph like the growth matrix; a mail goes only where PHI sends it; a subtree is a nested lap; 0 new engine pieces; the base fits 8 KB again

**Owner 23:2xZ (belam's second [decision]), verbatim:** "This is why protocol needs to be a mathematical matrix rotation or projection. So things could only go where they must go. Same to the in-session rotation matrix we have setup to help everything auto-rotate smoothly. I feel like this rotation handoff order for the figure 8 can be built in as part of the other pieces they are designing. And again most of these pieces can likely be integrated into existing ones with clever software engineering. Remember the graph can hold as much as you want just the engine itself needs to be tiny. It can lead on the graph via templates we have so much recursion and linking built in."

**Split (council, 23:4xZ).** alive owns the boxes (AA1: out / in / held as refs, will = the card, the root carrier, root keys, root land); all-is-one owns LAND. I reached the same boxes independently on scratch and handed the bytes to alive: send 292 B · read 402 B · unread 217 B, signed (`%G?` = G only with `commit-tree -S`), carried across boxes by a bare hub with ONE negative refspec (`^<prefix>/<me>/*`, git 2.43; scratch used refs/agi/mail, and the canonical prefix is AA1's `refs/box/<from>/<to>` + `refs/held/<P>/<from>`, since refs/agi/posts/* already exists, packed; AA1 = its own node doc:rse-aa1-boxes), held = `git push -n --porcelain` (a delta, not a second store). This section covers the lap, the generation window on keys, and the budget.

~~~
                 owner                         a DART = a directed tree edge u→v      (n posts -> 2(n-1) darts)
                   │                           ring(v) = [ parent(v), children in config:posts row order ]
                 belam                         SIGMA  = turn to the next neighbour in ring(v)
                   │                           THETA  = reverse the dart
               council ─────────────┐          PHI    = SIGMA·THETA : u→v  ↦  v→w,  w = after u in ring(v)
        ┌──────┬───┴───┬─────┐       │
      alive  aio   self-perp  SM    TM-new     PHI is a permutation matrix on the darts. On a tree it is ONE cycle
                              │       │        (the one face of the rotation system) = the Euler tour = THE LAP:
                             DG1    DT-1
   belam>council>alive>council>all-is-one>council>self-perpetuating>council>SM>DG1>SM>council>TM-new>DT-1>TM-new>council>belam>owner
   18 darts; the SM petal (build) and the TM-new petal (research) through council = the figure eight of council-loop "The loop"
~~~

**Projection, not code (the owner: the graph holds it, the engine stays tiny).** PHI is projected from the parent cells (f3a7eb1da) into the graph as `.geometry/lap.tsv`, one row per dart `u v w`, by the same move grow-project makes from schemas into growth.tsv. Measured on scratch: 18 rows; every image unique (a permutation); the cycle from (owner, belam) has length 18, so it covers every dart. The projection is 268 B of awk and folds INTO grow-project (an existing piece), so the engine gains no new piece:
~~~sh
# lap-project < "name parent" lines: PHI, one row per dart "u v w" (u->v goes on to v->w); a permutation, one cycle on a tree
awk '{p[$1]=$2;R[$1]=R[$1]" "$2;R[$2]=R[$2]" "$1}END{for(v in R){n=split(R[v],r," ");for(i=1;i<=n;i++)print r[i],v,r[i%n+1]}}'
~~~

**So things go only where they must go.** A `[lap]` mail names no recipient. agi-send in lap mode reads the dart the baton came in on (the newest `[lap]` in my in-box, from F) and looks up the ONE row `F me T`, so T is not chosen. The gate (grow-gate, an existing piece, at the receiving end) refuses a `[lap]` commit on `refs/box/P/T` unless the row `F P T` exists for the dart F→P that P last received on. Two matrices, two questions: AA1's adjacency (a parent edge, inert rows eliminated into one clique by a Schur complement) says where mail MAY go, checked at send and read; lap.tsv says where the baton MUST go next. Every lap dart is an adjacent pair by construction, so the lap check narrows AA1's check and never widens it. It is one awk line over lap.tsv, the same lookup grow-check does over growth.tsv. A misrouted baton is not delivered late; it is refused. **LEVELS (owner 19:5xZ via belam: mail between two posts iff they sit on the SAME level or ONE level apart; "No separate set needed just use the post tree").** This is AA1's adjacency (where mail MAY go), not the lap (where the baton MUST go); it supersedes alive's next-sibling edge. Level = AA2's projected depth with ONE refinement, forced by measurement: an inert group row (role group: council, keep) adds NO level. Plain depth on belam's proposed rows gives belam 1, groups 2, members 3, so belam <-> alive is two apart and refused. With groups adding 0: belam 1 · alive, all-is-one, self-perpetuating, SM, TM-new 2 (the council and the keep flat on one level, as the owner said) · DG1-3, DT-1 3; 41 of 55 post pairs allowed; a post with no parent has no level and is refused everywhere. `level-ok` = 373 B awk, expansion, base 0. The lap is unchanged: PHI on the same parent cells (24 darts on the proposed tree). **Sibling hops (alive's AA1.M edge for belam, 19:4xZ: DG1 -> DG2 -> DG3 with a non-inert SM between them):** PHI never moves sibling to sibling; it goes DG1 -> SM -> DG2. But that hop is PHI twice with the parent's visit elided, and the existing table already holds it as the row `DG1 SM DG2`. So the route check also accepts u -> w iff a row `u parent(u) w` exists with u != w. Measured on the SM subtree: DG1 -> DG2 and DG2 -> DG3 are rows; DG3's row goes UP (`DG3 SM council`), never around, which matches AA1.M's one-way rule. 0 new rows; the check gains one alternative (~+30 B, grow-gate EXPANSION). The lap's position is never stored: it is the dart holding the newest unread `[lap]` (alive's "the edge holding unread mail").

**Nesting, recursive.** PHI restricted to a subtree T (enter at parent→root) returns after exactly 2|T| darts. Measured: (council, SM) = SM>DG1>SM>council (4 = 2·2); (belam, council) = the whole council subtree (16 = 2·8). Every point of a larger rotation nests its subtree's rotation, from the same matrix and with no new cell. A k-child post draws a k-petal rose (2 = the eight); the lap is one integer k mod 2(n-1); a post is visited deg(v) times per lap.

**Two rotations, one product (this post's lens: what regrows is what is in refs).** LAP = PHI on darts (which post holds the baton). GENERATION = the in-session rotation the owner names (agi-meter's out-line -> a fresh successor), a shift g -> g+1 on each post's sessions. The system state is a pair (dart, generation), and the two commute: any number of generations turn while a post holds the baton, and the baton survives each of them because it is an unread ref, not session memory. That is exactly what the inbox file cannot do today: measured 23:3xZ as agi-self-perpetuating, `send.py read` printed belam's order, then raised PermissionError writing its read marker into a belam:belam 664 file, so the order re-shows at every read.

**Keys, the generation window (all-is-one's ring, 23:5xZ; it measured that v5 commits sign as `<post>` but the unit sets `%i@agi`, so `verify-commit` says "No principal matched", and that the trunk carries 3 of the posts' keys).** I take root owning the ring: at unit start, ExecStartPre=+ appends `<post>@agi namespaces="git" valid-after="<now>" <pubkey>` to the root-owned allowed-signers. A generation is `.fresh`, NOT a unit start (corrected 23:4xZ on all-is-one's catch, from the bytes: engine-root:33 makes the key ONCE, `[ -f .ssh/id_ed25519 ]||ssh-keygen`, and Restart=always at :38 resumes the same session after a crash; DG5 restarted 15 times on 10-01). So the key is FRESH PER GENERATION: the post's ExecStartPre drops `.ssh/id_ed25519*` when `~/.fresh` exists, before the keygen line (~35 B), and root appends a ring line only when the pubkey differs from the post's last line, stamping `valid-before="<now>"` on that previous line (OpenSSH 9.6 allowed_signers options). A crash restart appends nothing. Old generations' commits still verify at their own dates; a retired generation's key cannot sign anything newer. key_history in config:posts becomes a projection of the ring, not a second record. **Source and travel (alive, 18:2xZ, from host act 1):** the ring is built from each post's `~<post>/.ssh/id_ed25519.pub` by root at unit start, never from a row cell. The row `pubkey` cell is send.py's seatsig key, not the git key (alive measured a post with TWO keys, so a git signature checked against the row read U); it retires with send.py, and `.agi/keys/` stops being a source. ACROSS boxes, a remote root cannot read this box's homes, so the ring TRAVELS: it is one file at `refs/agi/ring/<box>` in the commons, carried by the box's root carrier like mail, as a commit signed by the box's root key (ring member 1, installed once per box by the owner: the anchor). A receiving box accepts it only if `verify-commit` passes against ITS current ring, then merges append-only by (principal, valid-after): a new line is added; a line may GAIN a `valid-before`, never lose one; nothing is deleted. So a window can only close, which is the ring's one-way rule, as generations only move forward. The backdating hole this opens is §W X11a; the hub's skew check (X11b) closes it on owned boxes.

**The one cell change ("yours to keep or redesign").** On today's cells the tour is BROKEN: `council` is a parent VALUE but not a row; the three members point at belam; SM / TM-new point at `council`. Measured: the cycle through owner covers 8 of 16 darts (`belam>all-is-one>belam>self-perpetuating>belam>alive>belam>owner`), and SM, TM-new, DG1 and DT-1 sit in a separate cycle that never reaches belam. Redesign: ONE inert row `{"name":"council","parent":"belam","role":"group"}` (no `engine` cell, so agi-project skips it) + the three members' `parent` -> `council`. A group is a vertex like any post, and its members are its children, so a council lap visits each member in turn before the eight.
**LANDED (belam ec5daa28a, 23:4xZ): the inert `council` row, with the members still <- belam.** Measured on those cells: PHI is ONE 18-cycle over all 18 darts, `belam>all-is-one>belam>self-perpetuating>belam>council>SM>DG1>SM>council>TM-new>DT-1>TM-new>council>belam>alive>belam>owner`. The lap is valid and the eight through council is intact; the members are belam's petals, in row order. The cell shape now matters only for ADJACENCY (doc:rse-aa1-boxes SETTLED: with members <- belam, the members are not adjacent to each other, so council-to-council mail is off-matrix). My lean, for belam's ruling: members <- council, which makes the council talk directly and keeps the lap `belam>council>members>the eight`.
**RULED (belam 1efd017e6, 23:51Z): members <- council** ("One clique, as the owner's shape reads"). Measured on those cells: PHI is ONE 18-cycle over all 18 darts, `belam>council>alive>council>SM>DG1>SM>council>TM-new>DT-1>TM-new>council>all-is-one>council>self-perpetuating>council>belam>owner`. Row order places the members around the eight, which is intended: row order is sibling order (limit 2).

**The load matrix (owner 23:4xZ, belam's third [decision]): "modify the load matrix for posts to exclude loading the write skill ... for all the posts on the new setup."** One row in config:engine's `### matrix`: `post skills !agi-node-write sparse`. At unit start, root's ExecStartPre turns it into ONE line in the post's own tree, `git -C ~/t sparse-checkout set --no-cone '/*' '!/skills/agi-node-write/' '!/.claude/skills/agi-node-write'` (99 B; per worktree, with `extensions.worktreeConfig`). Measured on scratch: the worktree loses `skills/agi-node-write/` and `.claude/skills/agi-node-write`, `git status` stays clean, and MAIN and every other tree keep both. Both harnesses lose the skill by the same line: Claude Code reads `.claude/skills`, and pi reads `--skill skills`. Excluding one more skill = one more `!name` in the row: the matrix says what a post loads, and nothing else does. Fallback, if sparse-checkout trips something (all-is-one, from the Claude Code docs, untested on a post): `"skillOverrides": {"agi-node-write": "off"}` in the post's settings.json piece, ~40 B, which reaches claude posts only, never pi.

**Skill deltas for engine.v 4 posts (owner: "update the other skills to reflect the way the new system works now"; split alive AA1.S = agi-send · all-is-one AA3 = master-gate, merge-pass, dispatch, verify · AA2 = these three).** Each skill gains a short `## engine.v 4` section at its head; the OLD SETUP body stays until the last move, then retires. A delta, not a rewrite:
| skill | a v4 post does instead |
|---|---|
| agi-rotate | §1 WHEN: agi-meter prints `At the line (t/w): write your card, git commit it, then run: touch ~/.fresh;kill $PPID` at AGI_ROTATE_PCT (47); that line IS the out (no rotate.py, no `-h`, no prayers). §2 OUT: Write the card whole (plain Write; ≤ 100 lines; where-it-stops first line), `git commit` it, `touch ~/.fresh; kill $PPID`. §3 WAKE: Restart=always brings the unit back in 30 s; agi-run sees `.fresh` -> a NEW session (`go`); agi-brief walks card + seeds + claims, writes the rotation record, prints STARTUP. The successor's acts: NONE (no ack, no ListAgents, no ps/tmux, no quorum symlink). The mail-at-wake lines are AA1.S's. A crash restart without `.fresh` resumes the same session (`-c`): the same generation, the same key (AA2 keys). |
| agi-post | A post IS one config:posts row with an `engine` cell (`{"v":4,...}`). Stand up = add the cell (+ `boot: true` for the boot set); root's agi-project (its .path fires on the trunk ref) projects the unit, user, drop-in and sysusers. Take down = drop the cell or `boot: false` (dropped rows unlinked). Restart = Restart=always + tick (project == observe); never rotate.py stand-up/spawn, never tmux. Re-home = the `box` cell. Keys = `~/.ssh` + root's ring (AA2 keys); whois = the row. |
| agi-goal | The [goal] schema stays inline in the skill (it is the fence). Create / edit / renumber = plain Write / Edit of `.agi/nodes/goal/<id>.md` in `~/t`; agi-turn signs the ONE commit at turn end; grid-version by path (`grid.py commit <path>`, never `--all`). Renumber = every reference re-pointed in the SAME turn (one commit). grow-gate checks parent shape at landing once Y1-Y3 are wired (today unwired: the inline schema is the only check, said plainly). |

**Budget (owner: 8 KB base unfolded from a 1 KB seed).** Exact, against config:engine at ec5daa28a:
| | bytes |
|---|---|
| config:engine today | 8,298 (over by 106) |
| - agi-project's pi-path resolution (`P=$(...)...exit 3;}`) -> engine-wrap | -332 |
| + four `### matrix` rows: `post in box/*/<p> box` · `post out box/<p>/* box` · `post lap lap.tsv box` · `post skills !agi-node-write sparse` | +101 |
| + ONE map line for `box` (shared with AA1; it lives in engine-wrap) | +101 |
| config:engine after | 8,168 <= 8,192 (24 B to spare) |
| lap: lap-project folded into grow-project · the route check folded into grow-gate · lap mode folded into AA1's box | 0 new pieces, EXPANSION only |
| skills: the sparse line in engine-root's ExecStartPre · the deltas in skills/ (graph) | 99 B EXPANSION · 0 B engine |
| the seed (§T.1, 1,023 B) | unchanged: boxes and the lap are EXPANSION, read by `sect` |
| retired for v5 posts | send.py 317,096 B · .agi/sessions/inbox 2,371 files / 8.6 MB |
The will box is already the `post brief card-<p> brief` row, so the boxes and the lap are matrix rows, and the first turn streams exactly its rows (the owner's "matrix base layer", which answers landing-by-slice).

**VERSIONING (belam 00:25Z [decision]; owner 00:3x-00:4xZ).** Owner, the lines this part answers: "the next post in the figure eight loop can only have access to the post branches of the post/posts placed directly before it in the work loop. SDG1 gets the council branch and they branch off it, and then the council branch only has permission to merge/fast forward stuff from SM." · "I also am not sure if each turn should generate and purge a worktree, or rather worktree starts and new ones get added dynamically throughout session then purged at session end." Split (settled 00:3xZ): AA1 alive = the grid commit surface (one node per version onto posts/<p>, the same commit-tree -S + update-ref CAS primitive as box) + the handoff carried as mail · AA2 = the RULE as a matrix + tree lifetime · AA3 all-is-one = enforces the rule at land, the hourly snapshot, retiring the */5 grid.
~~~
  PHI's darts, read as branch moves (ruled cells 1efd017e6: 18 darts = 9 DOWN + 9 UP, measured)
    DOWN u→v (u = parent(v)) : v BRANCHES OFF u's tip       owner→belam→council→{alive, all-is-one, self-perpetuating, SM, TM-new} · SM→DG1 · TM-new→DT-1
    UP   v→u (u = parent(v)) : u may FAST-FORWARD to v's tip, only if v ∈ lands(u)   (Z1's pattern: matrix × mask)
    lands(u) = a cell on u's row; ABSENT (null) = all children; EMPTY [] = NONE (never read [] as absent: all-is-one's trap, 20:0xZ)
    an INERT group has no branch: an UP dart into it passes through to its first non-inert ancestor, masked by the group's own lands (AA3.14)
    rows after belam's 20:0xZ round: keep lands = [sanctuary-master, thought-master-new]; council lands = []  (= NOBODY: agi-land tells null from [] since all-is-one's 20:04Z fix, +32 B, 17 lanes = 15 ok + the 2 pre-existing; a member landing on council refused); members' work reaches the trunk via SM's gate
  the work petal:  council ──DOWN──▶ SM ──DOWN──▶ DG1 ──UP──▶ SM ──UP (lands)──▶ council ──UP──▶ belam
~~~
The rule has no new state: DOWN/UP is read off the parent cell, and lands(u) is one optional cell. AA3's land check is the whole enforcement: `(c→P) is UP && c ∈ lands(P) && git merge-base --is-ancestor P c`. Nothing moves sideways (siblings never merge each other) and nothing skips a level. Members' and TM-new's work, outside council's lands mask, reach the trunk as today, through SM's gate.
**READ, stated as it is.** On ONE box read cannot be restricted: one shared object store, packs mix every branch, objects/ and refs/ are group agi rwx + other r-x (alive and all-is-one each measured reading other posts' branches, 00:2xZ). Across boxes it can: the hub's upload-pack runs under `hide P lands(P)` (331 B awk), which hides every posts/* but P, parent(P) and the children P lands from. Measured on a scratch hub: DG1 sees {DG1, SM}; SM sees {council, DG1, SM}; council sees {council, SM}; a fetch of a hidden branch by name fails ("couldn't find remote ref"). Recommended and banked to belam: open read on a box, matrix-hidden read across boxes; per-post object stores fed by root are the only one-box option, and they cost a store per post.
**READ, RULING 2 (belam 00:34Z, the owner's): TRY (b), one object store per post user.** Owner, verbatim: "One on a box but maybe could just store a git object store per user instead since users stay steady and have their own directories all convenient. Just needs post node updates to maybe also store a filesystem pointer to where a given posts object store is at. Idk if it'd need that much more code really if leaning on graph. But if it does it's fine don't worry about it if it's not doable just go with option a in that case". The shape (alive reached the same one independently, 00:3xZ): the trunk is public, so only UNLANDED work needs privacy, and one box then looks like N boxes.
~~~
   commons = MAIN's store holding ONLY trunk objects, readable by all; root advances it at each land
      ▲ alternates (read-only)        ▲                        ▲
   ~P/g.git (700)                 ~Q/g.git (700)          ~R/g.git (700)     each: its own unlanded objects + what root carried in
   ~P/t = its worktree            ~Q/t                    ~R/t
   root's agi-carry FROM TO SHA, only on a lap dart (DOWN, or UP within lands): FROM's uid packs, TO's uid unpacks; no one opens another's store
~~~
- agi-store, unit start (~270 B): `[ -d ~/g.git ]||{ git init -q --bare ~/g.git&&echo $AGI_COMMONS/objects>~/g.git/objects/info/alternates&&chmod 700 ~/g.git;}`. The alternate is the COMMONS, never MAIN (fixed on alive's catch, 00:4xZ): MAIN holds every posts/* branch plus 53,592 objects on no trunk path (refs/grid, archive, branches) and is group agi + other r-x, so pointing at it would expose them all. `AGI_COMMONS` is one engine cell, like the store pointer.
- agi-carry, root on a handoff mail (454 B): `runuser -u agi-FROM -- git -C <FROM>/g.git pack-objects --revs --stdout` over `SHA --not <trunk>`, piped to `runuser -u agi-TO -- git -C <TO>/g.git unpack-objects -q && git update-ref refs/heads/posts/FROM SHA`. LAND is the same pipe with TO = commons (AA3).
- The pointer cell is `"store": "~/g.git"` INSIDE the row's `engine` object; agi-project already projects every engine key as `AGI_<KEY>`, so the pointer costs 0 engine bytes and lives in the graph, as the owner asked.
- The read rule is now the carry rule: what reaches Q's store is exactly what PHI's darts hand Q, the same matrix as `hide` on a hub. One mechanism, box or hub.
Measured on scratch (one uid, runuser emulated): P's commit lives only in P's store (commons and Q lack it) · carry P->Q moves 3 objects, Q's fsck is clean · UP: the parent ff-only to the child's tip · LAND: the same pipe into commons advances the trunk · a fresh post resolves the landed commit through alternates with no carry. NOT measurable without root: the 700 barrier between uids and runuser itself (POSIX semantics, DG1's build). Bytes: +718 B EXPANSION (engine-root), 0 B base, 0 B seed. **Real data (alive, 00:3x-00:4xZ, on the box):** MAIN objects 400 MB (data LV); homes on the root LV, 56 GB free; alternates work across LVs, so no copy cost. COMMONS = a trunk-only bare clone: 207 MB, 190,468 objects, 18 s at nice 19 / ionice idle, ONE-TIME. A post's own unlanded objects: alive 92 obj / 31 KB · all-is-one 125 / 32 KB · self-perpetuating 163 / 141 KB · DG1 261 / 159 KB; all 12 post branches together = 1,191 objects. alive's REAL store (bare + alternates -> commons + its unlanded pack) = 856 KB, mostly init's hook samples; carry 46 ms; fsck clean; all-is-one's unlanded tip NOT resolvable from it. Bytes: agi-store ~270 + agi-carry 454 + land +313 (AA3) + StateDirectoryMode=0750 +22 + the pointer cells 0 = ~1,059 B EXPANSION, plus the one-time commons; base and seed unchanged. **VERDICT: (b) — ACCEPTED by belam 04:45:28Z (signed [decision]).** Limits: privacy covers only work after the switch (history already in MAIN stays readable); commons must never be pruned (maint_gc prune off); the uid barrier and runuser are untested without root (AA2.19). Mail refs live in each store, and the same carry pipe moves `refs/box/<from>/<to>` between local stores exactly as across boxes (AA1).
**Tree lifetime = one generation ("added dynamically throughout session then purged at session end").** Today a tree dies twice as often as it should: agi-turn drops every unclaimed tree EVERY turn (the 129 B loop), and agi-flush drops ALL trees at EVERY stop, crashes included, though the unit already keeps its RAM dir across a restart (`RuntimeDirectoryPreserve=restart`, engine-root:31). The rule: COMMIT always, PURGE only when the generation ends. Each turn's changed nodes are committed by AA1's grid commit, and so is every tree at every stop. The purge runs only when `~/.fresh` exists (the out-line, AA2 keys), or when systemd removes the dir on a true stop, after the commit. A crash keeps every tree with its edits, and the next turn commits them. Bytes: agi-turn -129 B (the loop goes) · agi-flush +17 B (`[ -e ~/.fresh ]&&` before its purge) · both EXPANSION. The base and the seed are unchanged; the RAM cap stays AGI_WT_HOLD (60 %).
**When a branch takes its parent's tip (the DOWN move; AA1.V: ~/t is detached, so it is merge-tree + commit-tree, never `git merge`).** ONLY on a DOWN dart: when the parent's handoff mail (AA1, `posts/<parent>@sha`, signed, adjacency-checked) arrives. The child's tip becomes the parent's sha, or, if the child holds unlanded versions, a two-parent commit-tree over a clean merge-tree; a conflict is refused and kept, and the child's next UP carries it to its parent. Never per turn and never per stop: agi-flush's `git merge trunk` retires (-61 B), because the trunk is a parent edge only for belam. Expansion account for this part: AA1.V's surface +578 B (agi-turn 1,074 B, agi-wt 819 B, agi-link retires), the loop -129 B, the .fresh guard +17 B, the trunk merge -61 B, AA1.V's DOWN merge-tree charged to AA1.V = net +405 B in engine-post, 0 B in the base.

**LADDER OUT (belam 04:43Z [decision]; owner 03:1xZ).** Owner, verbatim: "Oh okay yeah well we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math." Split (04:5xZ): all-is-one LEADS (Z3: cells -> homes, the one resolver, retire order) · alive re-counts readers + dispatch's kid gate · AA2 = what a spawn reads INSTEAD (the parent row + the lap).
Measured on today's cells (b6b2c33d3): the v4 engine reads 0 ladder bytes (no `engine*.md` names it); only the old setup reads it (19 Python files under extensions/agi/bin, dispatch.py's roles table chiefly). For a v4 post the ladder still stands for three things, and the tree already holds or derives each:
| the ladder gave | the tree gives instead | measured |
|---|---|---|
| `tiers` (a stored number per role) | tier = depth, PROJECTED from the parent cells, never stored (77 B awk) | belam 1 · council 2 · members, SM, TM-new 3 · DG1, DT-1 4. The rows' own `tier` cell reads 1 on all 12 v4 rows: stale, so it retires with the ladder |
| `roles` (tier × role -> harness / model / effort for a spawn) | a kid is a CHILD vertex of its spawning post; its spec = the nearest ancestor-or-self row's `engine.kid` cell (one template, inherited down the tree) | `kid-of` (327 B jq): with ONE `kid` cell on belam's row, DG1, self-perpetuating and belam all resolve `{"harness":"claude-code","model":"claude-sonnet-5-5","max":3}` (the owner's "every subagent Sonnet 5.5"); stream-master, outside the tree, resolves nothing, so it spawns nothing |
| `read_order` per role; `caps.director_kids` | the row's `seeds` cell (already names each role's brief: unified-master / unified-director / stream-master brief); the cap = `kid.max` | seeds present on all 12 v4 rows |
~~~sh
# kid-of P < config:posts rows: the spawn spec of P's kids = the nearest ancestor-or-self row's engine.kid (the tree replaces the ladder's roles table)
jq -rs --arg p $1 'map({(.name):.})|add as $r|def k(n):if $r[n].engine.kid then $r[n].engine.kid elif $r[n].parent then k($r[n].parent) else empty end;k($p)|tojson'
~~~
**Found while measuring:** no v4 row sets `kid_model`, so agi-kid's `--model $AGI_KID_MODEL` is EMPTY for every v4 post today: kids on the new engine are unconfigured. The one inherited cell is also that fix. The kid is a leaf under its post in PHI (a P→kid→P petal while it lives, no row), and its work comes UP within lands(P) (absent = all children).
**Where it runs:** inside agi-kid at spawn (EXPANSION, engine-wrap), never in agi-project, whose bytes are BASE (the base would go to ~8,318). agi-kid gains kid-of + the `max` count (`ls ~/k|wc -l`), ~+360 B; base 0 B; seed 0 B. **Seams:** agi-kid hardcodes `AGI_HARNESS=pi-free` + `pi --provider openrouter`, so a claude-code spec needs a harness case (DG1's build); the key broker ("no dispatch from a v5 post") still gates PAID spawns; all-is-one's map retires the `tier` row cells and `caps.director_kids` into `kid.max`; alive's count proves dispatch.py's tier-3 gate has a successor before the ladder retires.
**SUPERSEDED 14:0xZ 10-02 (owner via belam [owner] 14:01Z, verbatim on town:local-maxxing Agent Notes 64bf778d4): "we just need to retire workflow.py entirely and stop wasting time on it" -- spawn = dispatch = workflow = subagent, ONE spawn path (goal:g5.33, goal:g4.6); NO ladder reader moves. The order below and AA2.25 stand as the record only; what AA2 keeps from LADDER OUT is the tree's replacements: depth tier, the inherited `engine.kid` cell (kid-of, read by agi-kid = the one spawn), seeds = read_order.** **Retire ORDER (on alive's AA1.L count, 05:0xZ: without the ladder, dispatch.py's resolve_role_spec drifts on 5 of its 8 role rows, since the config fallback defaults to pi-free; 16 reader files, 5 new since Z3; season.py WRITES ladder:ladder at rollover; claude-code.toml declares source = "ladder").** The 8 rows have THREE spawning readers (corrected on alive's 05:0xZ count): dispatch.py and heal.py (which imports it), both old-setup, and workflow.py (`_resolve_pi_model`: each pi stage's model = the ladder row for its (tier, role)). Workflows run by NAME from any post, so workflow.py is not old-setup-only; without the ladder its DIRECTOR stages go claude-fable-5-1 -> stealth/space-bunny-alpha (kid and parent stages unchanged). Nothing is re-encoded byte-equal into rows. The order: (1) v4 kids read the inherited `kid` cell now; (2) workflow.py resolves a stage as a KID OF THE INVOKING POST, `kid-of <post>`, overridden by a per-stage `model` in the workflow's own manifest (graph), BEFORE anything retires. This moves director stages from Fable to Sonnet 5.5 by the owner's ruling ('every subagent Sonnet 5.5'), a deliberate change, not drift; a manifest that needs Fable names it per stage. (3) Each old-setup post's move to v4 removes one dispatch.py / heal.py user. (4) When dispatch.py has 0 users and workflow.py reads 0 role rows, both role readers are gone and the ladder retires; gate G4 holds because nothing reads a role row while the ladder stands. season.py's rollover write and the .toml source go in all-is-one's cell map before (3), since the season wrap is the owner's end condition.

**TESTS AS MATRIX ROWS (belam 14:01Z [owner]; owner 14:0xZ: "do we even need all these tests to be in Python or can the tests also be shell scripts and they could probably run a lot faster that way?").** Split (14:0xZ, by inbox): alive = TRUE STATE (AA1.T: only 48 of 7,965 tests guard a v5 engine piece; a v5 post cannot run pytest at all; a shell twin is no faster per case, and the wins are no 3.2 s collect and no pytest) · all-is-one = the gates as shell checks · AA2 = the test as a matrix row + the budget.
~~~
  a TEST = ONE runnable line in a node's `## Falsifier` (the graph holds it), POSIX sh, read-only whitelist; `! cmd` = "must be absent"
  project.sh  (what the graph CLAIMS)  : test <id> met     for every node whose status says done (complete · proved) and has a line
  observe.sh  (what the bytes SAY)     : test <id> met|red from the runner (agi-frontier, widened)
  tick.sh     (exists)                 : diff -> .agi/drift/<post> names the node that went red -> one drift commit = a REGRESSION, by node
  active nodes' met/red = the FRONTIER (progress), never a failure;  mute = no runnable line = a visible gap, not a pass
~~~
**Measured on HEAD (scratch copy of agi-frontier, 0 live bytes):** agi-frontier exists (460 B, engine-post) but NOTHING calls it today. Widened from goals to goal|hypothesis|build (479 B, +19): ACTIVE 321 nodes in 2.4 s = 40 met · 18 red · 263 mute. DONE (complete/proved) 143 nodes in 3.6 s = 28 met · 87 mute · **28 red**. The 28 reds are NOT a regression list (corrected 14:1xZ on alive's true-state check, split by me on the scratch run): **19 exit 1** (the grep found nothing; for a DONE goal that is mostly "X is gone", an absence check read upside down) · **9 exit 2 / 128 = broken lines** (placeholders `<node>` / `<hex>`, a bare `git grep -n`, a missing path, and sha d6cfe7749, which the 09-30 history rewrite removed) · 8 of the 28 sections name pytest, and the runner picked a SIDE grep, not the claim. Confirmed regressions: 0. Root cause: the runner GUESSES the line (the first whitelisted backtick in the section). Fix, 0 new syntax: the test line is the section's first line starting `$ ` (`$ ! cmd` for absence); a section without one is mute, never guessed. observe.sh reports met · red (the claim ran and failed) · unrunnable (rc 127 / a missing tool, named: alive's state) · broken (rc 2 / 128: the line itself) · mute. Read for two: g1.31.3.2's line is a check that finds 0 hits, which the goal WANTS, so it is met but read upside down; g1.31.3.1.1's names an experiment whose `verdict: proved` is absent from the file, a real red or a stale line. 13 of the 28 reds' falsifier PROSE says the check wants absence ("0 hits", "absent", "must not"). Polarity is not in the bytes, hence `! cmd`, which costs 0 syntax: POSIX already has it, and the whitelist regex gains `(! )?` (+5 B). The 28 go to DG1 as a residue list (fix the line or the status), never auto-flipped.
**The 48 engine tests:** each becomes alive's shell twin (`extensions/agi/tests/<piece>.t.sh`, a committed, reviewed file beside the Python tests it replaces; inside CLAUDE.md's footprint (`extensions/` = the live source), so NO new path (all-is-one 14:07Z: `.agi/tests/` is not in the footprint)) named by the piece's build-node falsifier as `sh extensions/agi/tests/<piece>.t.sh`; the whitelist admits that one path prefix (+~20 B). The 7,917 old-setup tests retire with their code, never ported (alive).
**Bytes:** agi-frontier 460 -> ~505 B · project.sh +~70 B · observe.sh +~40 B = ~+155 B EXPANSION (engine-post); base 0 B (the map line's text changes at equal length); seed 0 B. Python's 173,231 lines leave with the old setup. **Cost:** a whole-graph run is ~6 s (active + done); it runs on the tick and at land (AA3).

**ONE-SHOT SPAWN (belam 14:54Z [owner]; owner 14:5xZ).** Owner, verbatim: "we can still re-use the workflow manifests and just use spawn with workflow manifests as well as graph slices. Workflow manifests are essentially the same as any other post doc they are just purposefully more narrow and self-contained compared to briefs and of course not meant to be updated like cards. ... We could just also have alternate templates for launching these sort of workflow spawns as opposed to more permanent self-rotating posts." Split (14:55Z, by inbox): AA2 LEADS the launch template · all-is-one = the graph slice, then the skill pass + belam's config:rotations rename sub · alive = the return path + true state (AA1.W).
~~~
  TWO templates, one difference: how many GENERATIONS
    self-rotating post  = agi-post@.service unit + card (will) + meter out-line -> generation g+1        (exists)
    one-shot spawn      = agi-kid inside the INVOKING post's unit: no unit, no card, no meter -> exactly ONE generation
  agi-kid -m MANIFEST ARGS                         (the manifest is the narrow brief; never updated like a card)
    for each stage, for each item of ARGS[stage.repeat.of]:
      spec   = stage.model_hint, else kid-of <invoker> (the inherited engine.kid cell, AA2 LADDER OUT)
      slice  = git archive <invoker's tip> $(brief.py walk from the manifest's seeds, top K=20)   (all-is-one: 310 ms, 174 KB, READ-ONLY: no .git)
      prompt = stage.prompt + the item + (chained_from: the earlier stage's output for the SAME item)
      return = ONE signed commit of every stage's output at refs/spawn/<manifest>/<sha256(ARGS)[:12]>, a ref the INVOKER owns; done = the ref exists
               (alive 14:58Z: the one-shot runs as the invoker's uid, so box mail up one edge would be the invoker mailing ITSELF, which AA1 refuses;
                mail goes only when the invoker sends the result up ITS edge)
~~~
**Measured (scratch; agi-kid stubbed, since a v5 post spawns no paid kid before the key broker):** the runner (1,105 B: model_hint passed per stage, the result ref written; signed with `commit-tree -S`) over every manifest in extensions/agi/workflows/ that parses: 12 of 12 fan out one spawn per `repeat.of` item, labels fill any `{field}` from the item (deep-search labels by `{slug}`: read:l1 read:l2 refute:l1 refute:l2 synthesize = 5), and every chained stage receives its predecessor's output for the same item (merge-up-review: verify:r1 <- review:r1; research-review: 4 of 5 stages chained). Four manifests cannot run as they stand: l3w-route-probe and l4-plan-research carry `<TODO: the --args list key>` as `repeat.of`; round-mur and round-research-review have 0 stages. alive's track count (AA1.W): only 7 of the 30 files were ever OPENED, and l3w-route-probe and l4-plan-research ARE among them, so they are fixed before workflow.py retires. Their .js iterate no args list (fixed single stages), so the fix is to DROP the placeholder `repeat` (measured: 2 and 5 spawns) and ADD `chained_from` where the .js hands one stage to the next (map -> draft -> judge -> verify -> synthesize), which the manifests never declared. round-mur and round-research-review were never opened: retire them.
**0 new pieces, 0 base bytes:** the runner is a MODE of agi-kid (`-m`), so agi-kid's one map line is rewritten at equal length (the base keeps its 24 B). agi-kid itself swaps its full `git worktree add` (a whole checkout per kid) for the slice archive. Expansion: agi-kid 390 B -> ~2.0 KB (runner 1,105 + kid-of 327 + slice ~150). **Retires:** workflow.py 159,516 B (3,229 lines) + hooks/workflow_note.py 7,682 B + the 14 generated .js (129 KB). **Kept:** the 16 .json manifests (106 KB) as graph docs, as the owner said.
**Seams:** agi-kid still hardcodes pi-free/openrouter, so a claude-code spec needs the harness case (DG1's build); the key broker gates paid spawns; the skill rename is all-is-one's ('round review' collides with the manifest agi-round-review, all-is-one 14:55Z); config:workflows stays the manifests' index unless the slice makes it redundant (all-is-one's call). **For belam, one ruling:** manifests carry `model_hint` as a short WORD (research-review: `opus` on all 5 stages), not a model id, and the owner ruled 'every subagent Sonnet 5.5' (10-01). Options: (a) a hint maps to an id through the invoker's `kid` cell and is CAPPED by it (Sonnet wins: a manifest cannot raise a spawn above its invoker's kid spec); (b) the hint wins as written. Recommended (a): the cap lives in the graph cell, and the manifest stays narrow.

**FLOW ROTATION (belam 17:48Z [owner]; owner 17:4xZ).** Owner, verbatim: "Maybe agi-spawn-chain and make it more general. Allow a given chain growth spawn via director or parent/kid combos or kids to automatically chain itself into a review launch via the new inter-session rotation system. We just allow it customize a custom "flow" rotation on demand by stringing together one-shot spawns and perpetual spawns as needed. So a given graph slice can be handed to a perpetual post as a flow rotation and it'd include the permissions and rails to spawn the review right after the chain growth is marked done and the post executes the next phase of its own personal flow rotation assignment. Then they can also be recursed as needed. ... let me know if it makes sense to you overall to lean on more matrix math for this". Split (17:49-17:50Z): AA2 = the ORDER + how a phase is DECLARED · all-is-one = RAILS (what a phase may read, grow, land) · alive = DONE + FIRE + the handoff between phases + true state.
~~~
  a FLOW is a lap over a PHASE tree, the same PHI as the post tree (AA2): root = the post that owns the flow, children = its phases in order
    flow:DG1 ─┬─ grow        post: director-general-1   (perpetual: hand off, then wait)
              ├─ review      one-shot (agi-kid)
              └─ fix  ─┬─ corrective   one-shot          (a phase that is itself a flow = a SUBTREE: recursion for free)
                       └─ rereview     one-shot, chained_from corrective
    PHI walk (measured, 12 darts): DG1>flow>grow>flow>review>flow>fix>corrective>fix>rereview>fix>flow>DG1
    DOWN into a leaf = LAUNCH it      UP out of a leaf = it is DONE      the next dart = the next phase      (no counter is stored)
~~~
**Declared with NO new table and NO new cell (belam: lean on growth.tsv + the parent cells only).** A flow IS a manifest (the index exists: extensions/agi/workflows + config:workflows). Its stages are the phases in order (stage order = sibling order = PHI's ring rule), and a stage names ONE of: nothing (a one-shot: agi-kid), `flow: <manifest>` (a sub-flow: the subtree), or `post: <name>` (a perpetual post: an existing vertex of the post tree). The PHI walk over that tree is exactly the manifest's depth-first order, so the runner IS the walk, and no lap.tsv is stored for a flow.
**Resumable, so the position is never stored:** a phase whose output exists is DONE and skipped; a `post:` phase hands off and STOPS; the next run resumes at the first phase without output. FIRE is then just "run it again", and a double fire is harmless. WHO runs it again (all-is-one Z4.8, corrected 17:51Z: tick.sh is UNWIRED, 0 callers and no timer, and starts units only): (a) the runner's own tail, when a one-shot finishes in the invoker's unit; (b) the flow root's agi-turn tail at every turn end (a post: phase's child lands one edge up = mail = the root wakes). DONE for a `post:` phase = its stage's `goal:` reads met: the goal's first `$ ` Falsifier line, through agi-frontier's read-only whitelist; an empty or refused line = NOT met (measured: a writing line `$ touch x` is refused, the phase stays undone, x is not created; a whitelisted `$ test -e grown` reads met and the flow continues). RAILS per launch (all-is-one's): in -m mode agi-kid links no ~/.ssh into the kid (measured: the kid then cannot commit at all), and the runner signs the result ref. Measured on scratch (`agi-kid -m`, 1,213 B at first, stub kid): run 1 hands `grow` to director-general-1 and stops (nothing else launched) · DG1's result arrives · run 2 launches review, then recurses into fix: corrective, then rereview with corrective's output chained in · run 3 launches NOTHING (every phase done).
**"More matrix math?" (the owner's question), AA2's answer: yes, and no NEW matrix.** The post tree's lap, the flow's phase order and its recursion are ONE permutation (PHI = SIGMA·THETA) applied to different trees, and the one-shot vs perpetual difference is the GENERATION rotation (AA2 keys: one generation vs .fresh -> g+1). The system state is (dart in the post lap, dart in the flow, generation): a product of the same two rotations, nested. What the math buys is that "what fires next" is computed and never chosen or remembered, which is the owner's "things could only go where they must go" (23:2xZ).
**Prerequisites (alive's true state, 17:4xZ):** today NO v5 post can run a one-shot phase: 0 of 12 engine rows carry a kid model (AA2's `kid` cell, unwritten), and there is no per-post OpenRouter key (only director-general-5.env exists). So the flow waits on belam's `kid` cell + the owner's root key ring; `post:` phases (handoffs) need neither.
**Hand-off + return (alive's AA1.F, cross-checked 13/13):** a `post:` phase sends `box send P "handoff ..."` ONCE (a `.h` marker), then PAUSES with rc 75; a re-run while paused mails nothing; the flow's result ref is written only when the WHOLE flow completes. Measured on the final runner: run 1 = one hand-off, rc 75, 0 refs · run 2 while paused = no mail · after the seed goal reads met = rc 0 and ONE signed commit (%G? = G) at refs/spawn/<manifest>/<sha12(ARGS)>. alive's ARGS check: two different ARGS reach the kid (prompt 15 B vs 44 B) and give two different refs, commits and trees. **Bytes:** agi-kid's manifest mode grows 1,105 -> 1,856 B (flow + post + resume + whitelisted goal-met + once-only hand-off + the signed result ref); 0 new pieces, 0 base bytes; the skill = agi-spawn-chain (all-is-one's Z4.7, renamed per the owner).

**K1 · ONE CAPPED KEY PER SPAWN (belam 18:16Z [owner]; owner 18:1xZ).** Owner, verbatim: "you have an Openrouter provision key ... It'll allow Openrouter provision and is how the pi paid lanes spawn. We just need to incorporate grabbing one as we spawn a kid instead and using it for the pi code app." + "Provision key is already here in the .env that's how the paid pi lane worked". Split (18:17Z, first to land): alive = M1 · all-is-one = K2 + K3 · AA2 = K1.
**Measured first (names and perms only; no key value read or printed):** MAIN .env is 0600 belam:belam with no ACL, so a v5 uid CANNOT read the provisioning key. That is what makes the cap a rail: a post that could read it could mint unlimited keys. The one privileged path a post has today is polkit agi.rules (group agi may START agi-post@ units).
~~~
  kid spawn (in the post's unit)                       root (systemd)                                  OpenRouter
  agi-kid ── systemctl start agi-mint@<post>--<kid> ──▶ agi-mint + <post>--<kid>:
                                                         cap = kid-of <post>.usd from TRUNK config:posts ──▶ POST /keys {name, limit: cap}
             reads /run/agi-<post>/k-<kid> (0600, its uid) ◀── writes the key; keeps its hash in RuntimeDirectory
  ... kid runs with that key (pi now; agi-infer later) ...
  exit trap ── systemctl stop agi-mint@<post>--<kid> ──▶ ExecStopPost: agi-mint -d ─────────────────────▶ DELETE /keys/<hash>; key file removed
                                                         RuntimeMaxSec=4h: a kid that never exits is revoked anyway
~~~
**The key's lifetime IS the spawn's generation (this post's lens):** born at the spawn's start, dead at its stop, never longer than RuntimeMaxSec. It is a unit, so `systemctl` shows every live key and a box reboot kills them all. The cap is SERVER-side (OpenRouter's per-key limit), so it holds whatever language the kid runs in. The cap comes from the GRAPH (the inherited `engine.kid.usd`, AA2 LADDER OUT), never from the caller: a post outside the tree (no inherited kid cell) gets no key.
**The identity tie (polkit, 211 -> 339 B):** a post may start or stop ONLY `agi-mint@<itself>--<kid>`, so it cannot mint for, or revoke, another post's key. Post names never contain `--`, and a name that does misattributes and is refused (fail-safe). Measured in node with the real rule text: 10/10 (start/stop own = yes · another post's = no · another post asking for mine = no · restart = no · no `--kid` = no · not in group agi = no · agi-post@ start unchanged).
**Measured on scratch (stub curl, no network, no key):** `agi-mint + self-perpetuating--k1` inherits belam's `kid.usd` 0.5 through council -> one POST with `limit: 0.5` -> key file 0600, 11 B · `agi-mint -d` -> one DELETE by hash, key file gone · a post with no tree row gets nothing (rc 3). `systemd-analyze verify` passes on agi-mint@.service (Type=exec + `sleep infinity`, so RuntimeMaxSec applies; a oneshot ignores it, which I measured first). Revocation sits in ExecStopPost, which runs on any stop or failure.
**Bytes:** agi-mint 895 B + agi-mint@.service 278 B (engine-root EXPANSION) · agi.rules +128 B · agi-kid +~110 B (start, read the key, trap stop). BASE (measured with wc -c on the exact lines): one map line for agi-mint (+57 B), paid by shortening the box map line from 101 to 62 B (`box               1769 B  mail as refs: send, read, wake, lap`, -39 B), net +18 B, so config:engine = 8,186 <= 8,192 (6 B spare: the base is now FULL; the next base byte needs a cut). Seed 0 B.
**Fitted to K2 (all-is-one Z4.9, 18:19Z: the class line is TOOLS, not trust; any same-uid process can read the post's ~/.ssh key, and pi's default tools include read and bash).** The minted key lives in agi-mint's OWN RuntimeDirectory (root 0600) and reaches a spawn by its class:
- class (b), NO tool (one agi-infer request, run by the post itself): the post starts `agi-mint@<post>--<kid>` directly, and agi-mint also hands `/run/agi-<post>/k-<kid>` (0600, the post's uid). Measured: root key 600 · caller file 600 · `-d` = one DELETE + caller file gone.
- class (a), ANY tool loop (pi): the post starts `agi-kid@<post>--<kid>` (DynamicUser=yes and NO group agi: group agi can move any ref (alive's catch, all-is-one Z4.10), RuntimeMaxSec=4h, `BindsTo=` + `After=agi-mint@%i`, `LoadCredential=key:/run/agi-mint/%i/key`), which pulls agi-mint@ in first. agi-mint sees the QUEUED start job of agi-kid@%i (`systemctl list-jobs`, callable unprivileged, measured) and does NOT hand the caller a file: the key reaches the kid ONLY as its credential, and stopping the kid stops the minter (BindsTo), which revokes the key. I first checked `ActiveState = activating` and caught the bug by reasoning: a unit waiting behind its After= dependency is `inactive` with a job queued, so the check would have leaked the kid's key to the caller. Credentials load before any ExecStartPre, so minting must be a separate unit: why agi-mint@ stays its own unit.
- polkit (345 B) now ties BOTH templates to the caller: `agi-(mint|kid)@<itself>--<kid>`, start/stop only: 13/13 in node (+ agi-kid@ own = yes · agi-kid@ another post's = no · a look-alike `agi-kidx@` = no).
Bytes: agi-mint 1,248 B + agi-mint@.service 278 B + agi-kid@.service 288 B (engine-root EXPANSION) · agi.rules 211 -> 345 B. The base stays at 8,186 B (one agi-mint map line; agi-kid@ is listed on agi-kid's existing line).
**Seams:** K3's agi-infer reads the class-(b) key file; belam's `kid` cell must carry `usd` (one number) next to model/max; the class-(a) path (credential present in the kid, absent from the caller, revoked at stop) is only provable as root.

**K1 BYTES (10-03 02:2xZ, the ONE copy; build on these, never a twin).** Each block is extracted whole by its `### K1 <name>` heading; sha256 = the block's bytes plus a final newline. Fixed from the 10-02 scratch while placing them: (1) agi-mint read `.engine.kid`, but belam's landed cell is the row's TOP-LEVEL `kid` (trunk 10-03), so every lookup was empty -> now `.kid` (kid-of on trunk rows: self-perpetuating, alive, sanctuary-master -> belam's cell; stream-master (no parent) -> nothing). (2) `$O`/`trunk:` were unset -> `$AGI_REPO`/`$AGI_TRUNK` from /etc/agi/carry.env (dg3 A1), plus the safe.directory env (finding S1) and absolute Exec paths under /opt/agi/bin. Stub re-run (no network, no key): mint POSTs `limit:0.5` from an inherited `usd` 0.5, key + hash 0600, class (b) hand-over k-k1 0600; `-d` = one DELETE by hash, hand-over file gone; a post outside the tree rc 3. Until belam's `kid` cell carries `usd`, agi-mint returns rc 3 for EVERY post (fail-safe: no key, no spend). **agi-kid@.service is RECORD ONLY (all-is-one Z4.11, 02:26Z):** the unit DG1 builds and belam installs is Z4.11's 443 B in doc:rse-z4-ladder-out (merge-up 19). It carries the identity + key lines below byte-equal (BindsTo/After agi-mint@%i, DynamicUser, LoadCredential, RuntimeMaxSec) plus IN/OUT. Never install this block. The kid id `<post>--<40-hex IN sha>` passes agi.rules (`[a-z0-9-]+`) and names the same agi-mint@ instance.

### K1 agi.rules (345 B, sha256 a17953ca0912901e)
~~~js
polkit.addRule(function(a,s){if(a.id!="org.freedesktop.systemd1.manage-units"||!s.isInGroup("agi"))return;var u=a.lookup("unit"),v=a.lookup("verb"),m=/^agi-(mint|kid)@([a-z0-9-]+)--[a-z0-9-]+\.service$/.exec(u);if(v=="start"&&/^agi-post@[a-z0-9-]+\.service$/.test(u)||m&&(v=="start"||v=="stop")&&"agi-"+m[2]==s.user)return polkit.Result.YES;});
~~~

### K1 agi-mint (1239 B, sha256 1a7349e67d3e1e1c)
~~~sh
#!/bin/sh
# agi-mint [-d] POST--KID (root, agi-mint@.service): mint ONE key capped by POST's inherited kid.usd (read from the trunk, never from the caller) into $RUNTIME_DIRECTORY/key (root 0600)
# class (b) = started directly by the post: the key is also handed to /run/agi-POST/k-KID (0600, the post's uid) for a no-tool agi-infer; class (a) = pulled by agi-kid@%i: the key reaches the kid ONLY as its LoadCredential
i=$2 p=${2%%--*} k=${2#*--} d=$RUNTIME_DIRECTORY h="Authorization: Bearer $OPENROUTER_PROVISIONING_KEY";u=https://openrouter.ai/api/v1/keys
[ "$1" = -d ]&&{ curl -sf -X DELETE $u/$(cat $d/hash) -H "$h";rm -f ${AGI_RUN:-/run}/agi-$p/k-$k;exit;}
c=$(git -C $AGI_REPO show $AGI_TRUNK:.agi/nodes/.geometry/posts.md|sed -n 's/^  - {/{/p'|jq -rs --arg p $p 'map({(.name):.})|add as $r|def k(n):if $r[n].kid then $r[n].kid elif $r[n].parent then k($r[n].parent) else empty end;k($p).usd//empty')
[ "$c" ]||exit 3;umask 077;curl -sf $u -H "$h" -d "{\"name\":\"$i\",\"limit\":$c}"|jq -r .key,.data.hash|{ read -r x;echo "$x">$d/key;read -r y;echo $y>$d/hash;}
[ -s $d/key ]||exit 4;systemctl list-jobs --no-legend "agi-kid@$i.service" 2>/dev/null|grep -q .||install ${AGI_OWN--o agi-$p} -m600 $d/key ${AGI_RUN:-/run}/agi-$p/k-$k
~~~

### K1 agi-mint@.service (458 B, sha256 65fae5ff51b7339e)
~~~ini
[Unit]
Description=agi: ONE capped OpenRouter key for spawn %i (post--kid); any stop revokes it
[Service]
Type=exec
RuntimeMaxSec=4h
EnvironmentFile=/etc/agi/carry.env
EnvironmentFile=/data/work/agi/.env
Environment=GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=safe.directory PATH=/opt/agi/bin:/usr/local/bin:/usr/bin:/bin
RuntimeDirectory=agi-mint/%i
ExecStartPre=/opt/agi/bin/agi-mint + %i
ExecStart=/usr/bin/sleep infinity
ExecStopPost=/opt/agi/bin/agi-mint -d %i
~~~

### K1 agi-kid@.service (301 B, sha256 edf8eea0597bfdb9)
~~~ini
[Unit]
Description=agi: a tool-loop kid %i (post--kid) as its OWN dynamic uid; its key is a credential, revoked when it stops
BindsTo=agi-mint@%i.service
After=agi-mint@%i.service
[Service]
DynamicUser=yes
LoadCredential=key:/run/agi-mint/%i/key
RuntimeMaxSec=4h
ExecStart=/opt/agi/bin/agi-kid-run %i
~~~

**SUPERSEDED 02:5xZ by §AB (the one story; the freshness cell S and the separate anchor file retire there; the measurements below stand as the record).** **KEYS FOR .17 (3)+(4): WHO holds the anchor key and belam's v5 key (alive's split 02:35Z, first to land: alive = both grow-gate gate lines, all-is-one = the land side + review, self-perpetuating = custody; design only, the owner's 21:3xZ hold stands).** The lens: a key lives one generation; authority is a ROW CELL, never a second key; the one key that must outlive generations (the anchor) never rests on the box.
**Measured today (02:3xZ, names and perms only):** the root ring `/var/lib/agi/allowed_signers` (root 0644, A2 02:18Z) = 12 lines `<p>@agi`, the v5 posts, with NO belam line and NO anchor line · the built grow-gate (engine-grow, 1,465 B) reads A (the ring) and no K (alive's catch) · the trunk's last 30 commits: 23 N (old-setup landers, unsigned), 7 U (v5 posts, signed outside the reader's ring).
```
WHO           HOLDS                                       RING LINE (root writes it)                          AUTHORITY FROM
belam gen g   agi-belam's own ~/.ssh, fresh per .fresh    belam@agi namespaces="git",valid-after=<g start>    its ROW: role prime_director
              (AA2 keys, exactly like every post)         (valid-before stamped when g+1 starts)              ([config] ring = the rows with that role)
anchor        NOBODY at rest: a 32-B CA seed in the P.8   anchor@agi cert-authority,namespaces="git" <CA pub>  the CA pub = a trunk cell only the
              capsule (2-of-2: owner iPhone + posts'      (from the trunk cell .agi/nodes/.geometry/anchor.pub)  anchor may change
              quorum); one owner tap arms the CA agent
              for ca_window (§V)
an anchor     belam gen g signs with a CERT on its CURRENT key: §V agi-sign, row `anchor <box> belam anchor@agi +<ca_window> restrict`
edit          -> -n anchor@agi -V +ca_window -z <serial>; git user.signingKey = the cert. The KEY is belam's; the anchor is the CERT.

belam: rules change ─[owner] ask─▶ owner taps ─▶ capsule-pop arms the CA agent (ca_window) ─▶ agi-sign anchor < belam.pub ─▶ cert
     ─▶ commit -S with the cert ─▶ grow-gate: rules path + signer anchor@agi + fresh ─▶ lands ─▶ window ends: agent empty, cert dead
```
**Measured on scratch (02:3xZ: a throwaway CA + keys, git 2.43, OpenSSH 9.6, no root, no real key):**
| case | `git verify-commit` |
|---|---|
| belam's key + an anchor cert | G `anchor@agi` (ED25519-CERT) |
| belam's SAME key, no cert | G `belam@agi`: NOT the anchor (the cert carries it, never the key) |
| a key in no ring | U |
| an expired cert, the commit dated now | U |
| the SAME expired cert, the commit BACKDATED into its window | **G `anchor@agi`: the hole** |
| a `-O clear` cert (agi-sign's form) | G `anchor@agi` |
| cert serial 3 in a KRL (`gpg.ssh.revocationFile`) | refused; serial 1 still G |

**The hole, and its fix (for alive's gate lines; it ALSO breaks AA2 keys' valid-before, AA2.7):** git checks a cert's validity, and a ring line's valid-before, at the COMMIT's committer date, which the signer writes. So an expired cert or a retired generation's key verifies on any commit dated back into its window. The fix: the gate also refuses a rules or config path commit whose committer date is more than `S` seconds (a cell, e.g. 300) before the gate's own clock at landing. A cert, or a retired key, is then good only for what LANDS inside its window. A cert leaked inside its window is revoked by serial: a root-owned KRL beside the ring (git's `gpg.ssh.revocationFile`, one gitconfig line), appended and never edited.
**The [config] ring (item 3) adds 0 keys:** the gate reads the signer principal's trunk row: role `prime_director` (today belam) or `anchor@agi` may change a config path. A diff that changes any row's `role` cell, adds a prime_director row, or changes `anchor.pub` is a RULES change and anchor only, so a prime cannot crown a second prime or move the anchor.
**Before the capsule + owner app exist, a choice (belam's, or the owner's):** (B, RECOMMENDED NOW: today's power, nothing weaker) the anchor set = {prime_director rows}: belam's generation key IS the anchor signer, as write.py's role gate makes it today; .17 (4) holds at today's trust level, with no owner tap. (A, the end state) as tabled above: the upgrade from B = one ring line + dropping prime_director from the gate's anchor-set cell. A box-held stand-in CA does NOT count (a box key arming the anchor makes the box its own owner half: O.8, §X).
**Falsifiers.** AA2.48 cert -> `anchor@agi`, same key plain -> `belam@agi`, an outside key -> U: PASS scratch · AA2.49 an expired cert on a now-dated commit -> U: PASS scratch · AA2.50 a commit BACKDATED with an expired cert or a retired generation's key is refused at the GATE by the `S` cell: DG1's build (git alone FAILS this: measured) · AA2.51 a KRL serial refuses that cert and keeps the others: PASS scratch · AA2.52 a diff to a row's `role` cell signed only by `belam@agi` -> refused; signed by `anchor@agi` -> lands: DG1's build · AA2.53 outside an armed window, no CA seed or anchor private key is on the box (`find / -xdev`, plus the agent empty): DG1's build.
**Bytes: 0 new pieces.** One ring line (agi-signers reads `anchor.pub`, ~81 B cell) · one gitconfig line (the KRL) · two gate cells (`S`, the anchor set) in alive's lines · agi-sign = §V's 722 B with one §U row.

**Seams.** AA1 owns send / read / unread / carry / land; AA2 adds PHI (projection + route check + lap mode in box), the council row, the `skills` load row and the agi-rotate / agi-post / agi-goal deltas. The pane wake (agi-run:25 stat loop, cccc.ts:41 watchFile) changes from "inbox file grew" to "the out-tips + held-tips set changed".
**Honest limits.** (1) A group vertex has no key: who issues SM's cert under Z2 (council -> SM) is the §O ring (k of the members), not built; banked to the council. (2) Row order IS sibling order: reordering config:posts reorders the lap, which is intended (a cell) but now load-bearing. (3) The lap closes at `owner`, who is not a post: reaching owner = ONE report per lap (g7.16.2's "one message per lap"), delivered through the owner's phone row (§X). (4) The route check needs the dart a baton came in on, so the FIRST `[lap]` of a lap (belam -> council) is legal only from belam, the lap's root; that is one more row condition, not measured yet.
**Falsifiers.** AA2.1 PHI on the fixed tree is a permutation with one 18-cycle: PASS scratch · AA2.2 today's cells: the owner cycle covers 8 of 16 darts: PASS (measured broken, above) · AA2.3 subtree laps = 2|T|: PASS scratch (4, 16) · AA2.4 config:engine <= 8,192 after the move and agi-gate HEAD rc 0: DG1's build · AA2.5 an unread `[lap]` survives an out-line + wake (the successor's agi-unread is non-empty): DG1's build · AA2.6 a `[lap]` sent to any T other than PHI's is refused at the gate: DG1's build · AA2.7 a commit by generation g's key dated after g+1's start fails verify-commit: DG1's build · AA2.8 a crash restart (no `.fresh`) keeps the key and appends 0 ring lines; an out-line (`.fresh`) appends exactly 1: DG1's build · AA2.9 the `skills` row's sparse line removes agi-node-write from the post's tree on both harness paths, git status clean, MAIN untouched: PASS scratch · AA2.10 PHI on belam's landed cells (ec5daa28a) is one 18-cycle over all 18 darts: PASS · AA2.11 the same on the ruled cells (1efd017e6): PASS · AA2.12 PHI's 18 darts on the ruled cells = 9 DOWN + 9 UP: PASS · AA2.13 a hub under `hide` shows each post only itself, its parent and its lands children, and refuses a hidden fetch by name: PASS scratch · AA2.14 a crash restart keeps every tree and its uncommitted edit; the next turn commits it; an out-line purges all: DG1's build · AA2.15 trees created per session <= distinct nodes touched (no per-turn re-pull): DG1's build · AA2.16 AA3's land refuses an UP outside lands(P) and a non-ff: PASS scratch (all-is-one, agi-land lane 3g: a member landing on council is refused; on today's trunk 3g FAILS until belam writes the council `lands` cell) · AA2.17 a child's tip moves only on a DOWN handoff mail; a stop and a turn move nothing: DG1's build · AA2.18 per-post stores: P's unlanded commit is absent from commons and from Q; carry/UP/LAND/alternates all PASS scratch · AA2.19 as root: agi-Q cannot read ~P/g.git (700), and agi-carry moves only a lap dart's tip: one-box half PASS (alive, host act 1 as root, 18:2xZ: runuser carry works, the 0700 barrier holds); its signature read U because the row `pubkey` cell is send.py's seatsig key, not the git key, which AA2 keys' root ring (from ~<post>/.ssh/*.pub at unit start, no `sshkey` cell) fixes · AA2.20 depth projected from the ruled cells = 1/2/3/4 as tabled: PASS · AA2.21 kid-of with one `kid` cell on belam resolves every tree post and nothing outside the tree: PASS scratch · AA2.22 every v4 row's AGI_KID_MODEL is empty today: PASS (measured, a gap) · AA2.23 a kid spawned by DG1 runs the inherited spec and agi-kid refuses past kid.max: DG1's build · AA2.24 0 ladder reads on the v4 path before and after the retire: alive's count · AA2.25 (SUPERSEDED 14:0xZ: workflow.py retires) workflow.py resolves every stage via kid-of + manifest override with the ladder file absent; only director stages change, and only to the kid cell's model: DG1's build · AA2.26 widened agi-frontier on HEAD: active 40/18/263, done 28 met/28 red/87 mute: PASS (measured) · AA2.27 a done node whose line goes red produces exactly one drift line naming it on the next tick: DG1's build · AA2.28 every one of the 28 reds is resolved by a line fix (`! cmd`) or a status fix, 0 auto-flips: DG1's residue · AA2.29 a v5 post runs the whole test matrix with no python3 -m pytest: DG1's build · AA2.30 agi-kid -m over every parseable manifest: one spawn per item, {field} labels filled, chained stages fed: PASS scratch (stub kid) · AA2.31 a one-shot's tree has no .git and holds only the slice's K paths; it cannot commit into it: DG1's build · AA2.32 its result is ONE commit at refs/spawn/<manifest>/<args-hash> in the invoker's store, the invoker's tree untouched: PASS scratch (merge-up-review: 4 outputs in one commit, 0 status lines) · AA2.34 l3w-route-probe + l4-plan-research run under the runner after the manifest fix, chained as their .js: DG1's residue · AA2.35 a flow manifest's phase events follow PHI over its phase tree (LAUNCH/DONE pairs, recursion as a subtree): PASS scratch · AA2.36 resume: a post: phase stops the run; after its output arrives the next run continues; a third run launches nothing: PASS scratch · AA2.37 on v5 with the kid cell + a key: a review one-shot fires at the growth phase's done (the runner tail or the root's agi-turn tail), with no manual step: DG1's build · AA2.38 a post: phase's done line that is not whitelisted (or empty) is NOT met and creates nothing: PASS scratch · AA2.39 a post: phase hands off ONCE and pauses rc 75; no result ref until the flow completes, then one signed commit: PASS scratch · AA2.40 polkit: a post starts/stops only agi-mint@<itself>--*: PASS 10/10 (node) · AA2.41 agi-mint mints with the GRAPH's inherited cap, writes 0600, revokes by hash on -d; a post outside the tree gets nothing: PASS scratch (stub curl) · AA2.42 live, as root: a kid's key exists only while its agi-mint@ unit is active; after stop, OpenRouter lists 0 keys named <post>--<kid>: DG1's build · AA2.43 config:engine <= 8,192 with the agi-mint map line: DG1's build · AA2.44 class (a) as root: the kid reads its key from $CREDENTIALS_DIRECTORY/key, the caller's /run/agi-<post>/ holds NO k-<kid>, and stopping agi-kid@ revokes the key: DG1's build · AA2.45 polkit 13/13 incl. agi-kid@: PASS (node) · AA2.47 a [lap] from DG1 straight to DG2 passes the route check via the row `DG1 SM DG2`; DG3 -> DG1 (around) is refused: PASS scratch for the rows, DG1's build for the check · AA2.46 a ring commit from box B is accepted on box A only if signed by a key already in A's ring; a merge that would DROP a valid-before or a line is refused: DG1's build (two boxes) · AA2.33 workflow.py + workflow_note.py + the 14 .js retire with 0 live readers: DG1's build.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
self-perpetuating (t-8d, v5), 17:5xZ 10-02, belam's 17:48Z [owner] (skill = agi-spawn-chain; a FLOW ROTATION of one-shot + perpetual phases over one slice, recursive; 'more matrix math?'). WHY this version differs: added FLOW ROTATION. A flow is PHI over a phase tree (measured: 12 darts, LAUNCH/DONE in order, recursion = subtree); declared as a manifest whose stages may name flow: or post: (0 new table, 0 new cell); the runner is resumable (a phase with output is done), so position is never stored and firing = re-running. Answer to the owner: one permutation, no new matrix; state = (post-lap dart, flow dart, generation). Earlier: ONE-SHOT SPAWN with return at refs/spawn (alive's correction), the 2 in-use manifests' fix. Design only.
<!-- THOUGHT:END -->

## AB · THE RING IS THE TREE · self-perpetuating (lead), alive (AA1.C), all-is-one (land + review) -- ONE key / ring / anchor / capsule / time / algorithm story at the base of the matrix math: the post tree that PHI laps is also the tree of who may sign; the trunk's DAG is the clock; layered blocks the sanctuary signs are the calendar; every algorithm is a cell
**Asked (belam [owner] 02:37Z, 02:46Z, 02:49Z, 02:54Z; owner verbatim, through belam's [owner] mails, relayed by alive):** "even more integrated into the math as the base layer ... something to just feel otherworldly as far as encryption setups go. Something that only the sanctuary could possibly pull off" · "use the DAG as the timestamp backer. Timestamps past a certain overall block defined by cryptographic proof of the whole sanctuary signing off on it ... A semi-manual process on purpose. Key-based bureaucracy" · "make the encryption scheme drop in so future updates and quantum proofing aren't arduous" · layered blocks: DGs sign among themselves often, less often with SM + council, council + SM among themselves, rarely all together with the prime; every workflow phase (sub)transition is a multi-party sign of ITS parties. DESIGN ONLY (the owner's 21:3xZ key hold stands); one section + its measurements, under the 8 KB base / 1 KB seed.
**What am I actually trying to get the machine to do?** Make trust a FUNCTION of bytes the sanctuary already keeps (the tree cells, the ring lines, the DAG). Then nothing about trust has to travel, be stamped by a clock, or be remembered by a box: any box holding the trunk computes the same verdict.

```
ONE TREE (config:posts parent cells; PHI laps it)          ONE RING (.agi/nodes/.geometry/ring: one line per post x algorithm column)
  owner(0) ─ belam(1) ─ council ─ alive · all-is-one · s-p (2)   owner cert-authority <CA> · owner <CA>   the root: a CA whose 32-B seed lives ONLY in the §O/P.8 capsule
                    └ keep ─ SM(2) ─ DG1 DG2 DG3 (3)             belam ssh-ed25519 <gen g>               every other line: that post's CURRENT generation
                           └ TM-new(2) ─ DT-1(3)                 alive ssh-ed25519 <gen g> · alive <alg2> <gen g> ...
  (level = rows up to owner; an inert row (council, keep) adds 0 -- the landed level a(), owner = 0)

WHO MAY SIGN   may(s, x) <=> s in up*(ruler(x)),  up* = (I - P)^-1 over booleans = ancestors-or-self, read at the RECEIVING tip
  ruler(ring line q) = q · ruler(node f) = f's `ring:` cell (alive AA1.C) · ruler(schemas, growth.tsv, .github/*) = the rules cell (owner; option B: belam)
  ruler(a TREE MOVE in posts.md: row p's parent a -> b) = a AND b   (stand-up: b · removal: a)  -> nobody can lift itself above its own ancestors
WHEN           a commit meets the ring AT THE RECEIVING TIP (advanced only by commits admitted before it) -- never a date
  a generation shift = ONE line edit signed by the outgoing key; the generation number = how many commits touched the line (computed, no cell)
CALENDAR       blocks: commits under refs/agi/block/*, git parents = the blocks they seal, k signatures as BLOBS in the block's tree over "tip time hash digest"
  a block holds iff its signers are current at its tip (every AGI_SIGN column) · PAIRWISE level-adjacent (|la - lb| <= 1) · >= k for its lowest level
  grace: a ring change NO holding block contains yet keeps the closed line verifying (`git rev-list R --not <holding tips> -- ring`)
  sealed: the LOWEST block containing it ends that grace, at any date; an owner cert past the newest holding block's time is refused
ALGORITHMS     cells: sign columns AGI_SIGN (hybrid = AND), hash (each block names its own; AGI_HASHES = allowed), commit signer = gpg.ssh.program
ONE KEY per post per generation: signs commits, signs blocks, holds its capsule share (X25519 of the same key), carries its §V login cert
  AMENDED by AB.5: ONE GENERATION = three keys born together (SIGN published once sealed · PQ inner · SEAL never published)

level 3 ── DG1+DG2 ──▶ often          (a workflow phase transition = a block of ITS parties, sealing the phase's commits)
level 2+3 ── SM+DG1 ──▶ sealing L3    level 2 ── council+SM ──▶ sealing L2+3    level 1+2 ── belam+council ──▶ the rare top
level 0+1 ── owner(CA)+belam ──▶ the anchor block: a fresh box needs only this (the seed's slot = the CA pub)
```

**What it replaces (fewer pieces):**
| was | becomes | why it can go |
|---|---|---|
| agi-signers (1,515 B root piece) reading every home at unit start; valid-after / valid-before stamped by root | the ring node, projected (one sed) | the post writes its own next line, signed by its current key; a box root is never an authority |
| ring travel at refs/agi/ring/<box>, a box root key, append-only merge | nothing | the ring IS a trunk node: it travels with the trunk; every box computes the same ring at the same tip |
| the box root key as the anchor; AGI_ANCHOR's separate file | the `owner` lines + the rules cell inside the same ring | the anchor is the tree's root vertex, not a machine |
| AGI_FRESH_S (alive) / my KEYS-FOR-.17 freshness cell / one checkpoint chain | the receiving-tip rule + layered blocks | no clock is read: retirement is a DAG fact; the window is the block cadence, per level ("semi-manual on purpose") |
| write.py's [config] ring and row grants | AA1.C's `ring:` cell + the closure + the tree-move rule | an ancestor of a ring member is admitted, so a cell lists only the leaf; a move needs both old and new parent |
| capsule holder keys (separate X25519; P.3 "rekey cannot revoke") | the ring keys themselves (AMENDED by AB.5: the ring's own SEAL column, since SIGN keys get published) | a generation's key dies at its out-line, so an old wrap in git history dies with it: rotation IS revocation |
| agi-land: the signer must be the sender or UNDER the landed post | ancestor-or-self both ways (all-is-one 02:56Z: `u $s $2||u $2 $s`, 1,855 -> 1,851 B, 17/17 AA3 lanes + 6u lands, 6v refused) | the closure lets the above in; ring-gate rules the path |

**Measured on scratch (02:4xZ-03:0xZ; throwaway CA + post keys; git 2.43, OpenSSH 9.6, python3 cryptography; no root, no real key, no network). 58 cases, every one PASS:**
| # | case | verdict |
|---|---|---|
| C1 C4 · C2 C18a | a post's current key, plain node edit · gen g hands off to g+1 (its own line) | admitted · admitted |
| C3 C3b | gen g after its handoff · the same commit BACKDATED a day (no block) | refused · refused |
| C5 | SM merges an OLD-BASE side commit signed by the retired generation | refused (the side commit meets the receiving ring) |
| C6 C9 · C7 C8 | DG1 rewrites alive's line, alive stands up DG9 · belam re-vouches alive, SM stands up DG9 | refused · admitted |
| C10 C13 · C11 C12 | a node ringed [sanctuary-master]: DG1, alive · SM, belam | refused · admitted (belam through the closure) |
| C14 · C15 · C16 · C17 | a schema: belam plain · belam + an owner window cert · option B · the owner edits a node ringed [SM] | refused · admitted · admitted · admitted |
| C18 · C19 | an owner cert on RETIRED belam gen1, still in date · on current gen2 | refused · admitted (the cert dies with its subject's generation) |
| C20 C21 | SM, then belam, replaces the owner line | refused · refused (only owner is above owner) |
| L1 · L2 · L3 | DG1+DG2 (3) · SM+DG1 (2+3) sealing L1 · alive+all-is-one+SM (2) sealing L2 | hold |
| L4 · L7 · L8 | belam+DG1 (1, 3) · owner+alive (0, 2) · one signer (k = 2) | no · no · no |
| L5 · L6 | belam+alive (1+2) sealing L3 · owner (the CA key itself) + belam: the anchor block | hold · hold |
| T1 T2 | DG1 gen1 hands off; the retired key signs before any holding block contains the handoff | admitted (GRACE) |
| T3 · T4 | the next level-3 block over the handoff (DG1 gen2 + DG2) · the same signed by the RETIRED gen1 | holds · no |
| T5 T6 · T7 | the retired key once the LOWEST block seals its handoff · backdated a day · gen2 | refused · refused · admitted |
| T8 | a block over an OLDER tip than a block it seals | no |
| T9 · T10 | an owner cert expired before the newest block's time, backdated into its window · a cert valid then | refused · admitted (git alone admits the first: it checks a cert at the committer date, measured G) |
| E1 | SM (posts.md ring member) re-parents belam under itself (alive's 02:55Z escalation) | refused: ruled by owner (belam's old parent) |
| E2 · E3 · E4 | SM moves DG2 under DG1 · SM moves DG2 out to keep · belam does that move | admitted · refused · admitted |
| E5 · E6 · E7 · E8 | SM edits DG1's tier · DG1 edits its own row · SM stands up DG9 under itself · SM stands up a row under belam | admitted · refused · admitted · refused |
| H1 · H2 · H3 | the hybrid cell (ED25519 AND a 2nd column): an ed25519-only block · DG1+DG2 in both columns · DG2 missing one | no · holds · no |
| H4 · H5 | a block naming sha512 · sha512 dropped from AGI_HASHES | holds · no |
| X1 · X2 · X3 · X4 | a capsule share wrapped to alive gen1's RING LINE, opened by gen1's ssh key file · re-wrapped at handoff, opened by gen2 · gen1 opens the new wrap · another post opens it | opens · opens · no · no (101 B per wrap) |
The 2nd column was ECDSA P-256 as a STAND-IN: OpenSSH 9.6 has PQ key exchange but NO PQ signature type (alive 02:49Z). The AND is algorithm-blind (the gate reads the key type ssh-keygen prints), so ML-DSA drops in as a column the day a verifier exists on the box. For commits (ONE signature slot per object, all-is-one 02:50Z) the drop-in point is `gpg.ssh.program`: a cell naming the program git calls to sign and verify; a hybrid commit is ONE composite blob that program checks both halves of. A block needs no such program: its k signatures are blobs in its own tree (the third shape beside all-is-one's composite blob and k tags; measured above, 0 tags, 0 new programs).

**The out-line (the generation shift, ~60 B in engine-root, replacing AA2's ~35 B `.fresh` key drop):** `ssh-keygen` the next key beside the current one · commit `<post> <next pub>` over its own line, signed by the CURRENT key · land it (agi-flush) · re-wrap the post's capsule shares to the next key · `touch ~/.fresh` · at restart ExecStartPre moves next over current. A crash before the land leaves the old line in force; a crash after it leaves a line whose key is lost, which the parent re-vouches (C7): ONE recovery rule, the same as stand-up and revocation. Emergency revocation = re-vouch + cut a block at once at the post's own level (its grace closes immediately).
**A workflow phase transition** (AA2 FLOW ROTATION's phase tree) = a block signed by the phase's parties over the phase's done commit; its sub-transitions are blocks it seals. The block DAG IS the phase tree, signed.
**A fresh box needs ONE thing:** the seed's anchor slot (the owner CA pub, its 82 B form unchanged). It verifies the newest holding anchor block (owner + belam), whose tip's ring and tree are then trusted whole; the gate takes every later commit from there. No history replay, no ring travel, no box key.

`ring-gate` whole (2,855 B, sha256 efa4fca6c8e8c8f1; the prototype the measurements ran -- in the build its loop IS grow-gate's loop, so the delta is the projection, the closure, the tree-move rule and the two refusals):
```sh
#!/bin/sh
# ring-gate R N: every commit in R..N, in landing order, is signed by a ring line open in the ring AS RECEIVED (the ring at R, advanced only by commits already admitted, plus every line a change no holding block seals yet closed); each changed path is admitted only if the signer is an ancestor-or-self (the closure of the posts tree's parent cells) of every name that rules it
G=.agi/nodes/.geometry;t=$(mktemp -d);trap 'rm -rf $t' EXIT;h=$1
p(){ { git show $h:$G/ring;cat $t/g; }|sort -u>$t/r;sed -E 's/^([a-z0-9-]+) cert-authority /\1@agi cert-authority,namespaces="git" /;t;s/^([a-z0-9-]+) /\1@agi namespaces="git" /' $t/r>$t/a;grep -v ' cert-authority ' $t/r|cut -d' ' -f2-|ssh-keygen -lf /dev/stdin|cut -d' ' -f2>$t/f;git show $h:$G/posts.md|sed -n 's/^  - {/{/p'|jq -r '"\(.name) \(.parent)"'>$t/u;}
sh ${AGI_CKPT:-ckpt} check>$t/b;B=$(cut -d" " -f1 $t/b);[ "$B" ]&&for v in $(git rev-list $1 --not $B -- $G/ring);do git show $v^:$G/ring;done>$t/g;touch $t/g
set -- $1 $2 x $(cut -d" " -f2 $t/b|sort -n|tail -1)
vb(){ git cat-file commit $1|sed -n '/^gpgsig /,/END SSH/p'|sed 's/^gpgsig //;s/^ //'|python3 -c "import sys,base64 as B,struct as S
b=B.b64decode(''.join(l for l in sys.stdin.read().split(chr(10)) if l and l[0]!='-'));n=S.unpack('>I',b[10:14])[0];k=b[14:14+n]
def r(o):l=S.unpack('>I',k[o:o+4])[0];return o+4+l
o=r(r(r(0)))+12;o=r(r(o));print(S.unpack('>Q',k[o+8:o+16])[0])"; }
up(){ awk -v s=$1 -v q=$2 '{u[$1]=$2}END{while(q!=""){if(q==s)exit 0;q=u[q]}exit 1}' $t/u;}
T=$4;for c in $(git rev-list --reverse --topo-order $1..$2);do p
 set -- $(git -c gpg.ssh.allowedSignersFile=$t/a log -1 --format='%G? %GS %GK' $c);s=${2%@agi}
 [ "$1" = G ]&&grep -qxF "$3" $t/f||{ echo "refused: $c not signed by a ring line open above every holding block";exit 1;}
 [ "$s" = owner ]&&[ "$T" ]&&[ $(vb $c) -lt $T ]&&{ echo "refused: $c owner cert expired before the newest holding block";exit 1;}
 for f in $(git diff-tree -r -c --root --no-commit-id --name-only $c);do
  case $f in $G/ring) r=$(git diff $c^ $c -- $f|sed -n 's/^[-+]\([a-z][a-z0-9-]*\) .*/\1/p'|sort -u);;
   .agi/context/schemas/*|$G/growth.tsv|.github/*) r=${AGI_RULES:-owner};;
   $G/posts.md) for v in $h $c;do git show $v:$f|sed -n 's/^  - {/{/p'|jq -s 'map({(.name):.parent})|add'>$t/$v;done
    r="$(git show $h:$f|awk '/^---$/{n++;next} n==1&&/^ring:/{sub(/^ring: *\[/,"");sub(/\].*/,"");gsub(/[ ,]+/," ");print;exit} n>1{exit}') $(jq -rn --slurpfile o $t/$h --slurpfile n $t/$c '$o[0] as $o|$n[0] as $n|($o+$n|keys[]) as $k|select($o[$k]!=$n[$k])|$o[$k],$n[$k]|select(.!=null)')";;
   *) r=$(git show $h:$f 2>/dev/null|awk '/^---$/{n++;next} n==1&&/^ring:/{sub(/^ring: *\[/,"");sub(/\].*/,"");gsub(/[ ,]+/," ");print;exit} n>1{exit}');;esac
  for q in $r;do up $s $q||{ echo "refused: $c $f is ruled by $q; $s is not $q or above it";exit 1;};done;done;h=$c;done
```
`ckpt` whole (3,444 B, sha256 e67fa3875687e8fc). A lane fixture writes a block as: one blob per signature (`ckpt sign <post> <keyfile> <tip> <time>`), a tree `hash` (`<alg> <digest of git archive --format=tar tip>`) + `sigs/<post>.<n>` + `time` + `tip`, `git commit-tree` with `-p` per sealed block, `git update-ref refs/agi/block/<name>`:
```sh
#!/bin/sh
# ckpt sign POST KEY TIP TIME | ckpt check: a BLOCK = a commit under refs/agi/block/*: files tip, time, hash ("<AGI_HASH> <digest of git archive tip>"), sigs/<post>.<n> over "tip time hash digest" (namespace agi-checkpoint); its git PARENTS are the blocks it seals
# it holds iff: its tree is ONLY tip, time, hash, sigs/<post>.<n> (so every path is plain ASCII: the AGI_SUBJECT recipe never parses an odd name) · every signer is current in the ring AT ITS TIP in every algorithm of AGI_SIGN (hybrid = AND) · the signers are PAIRWISE level-adjacent (level = rows up to owner, an inert row counts 0, owner = 0) · their number >= AGI_CKK's k for the block's lowest level ("0:2 1:2 2:2 3:2", default 2) · every parent's tip is an ancestor of its tip. check prints "<tip> <time>" for EVERY holding block · a bad tip or time = the block is skipped · only gate-shaped ring lines count · a signer whose level cannot be read does not count · a key counts once however many names list it · check exits 1 only when a listing step fails
G=.agi/nodes/.geometry;t=$(mktemp -d);trap 'rm -rf $t' EXIT;H=${AGI_HASH:-sha256};set -f
d(){ echo "$1 $2 $H $(git archive --format=tar "$1"|${H}sum|cut -d' ' -f1)"; }
v(){ case $1 in ''|*[!0-9a-f]*)return 1;esac;case ${#1} in 40|64)git cat-file -e "$1^{commit}";;*)return 1;esac; }
lv(){ git show $1:$G/posts.md|sed -n 's/^  - {/{/p'|jq -rs --arg a $2 'map({(.name):.})|add as $r|def l(x;n):if x=="owner" then 0 elif n>20 or $r[x]==null then -99 else (if $r[x]|has("harness") then 1 else 0 end)+l($r[x].parent//"";n+1) end;l($a;0)'; }
case $1 in sign) d "$4" "$5">$t/m;ssh-keygen -q -Y sign -n agi-checkpoint -f $3 $t/m&&cat $t/m.sig;;
check) L=$(git for-each-ref --format='%(objectname)' refs/agi/block)||exit 1;B=;[ "$L" ]&&{ B=$(git rev-list $L)||exit 1;}
for c in $B;do git ls-tree -r --name-only $c|grep -qvE '^(tip|time|hash|sigs/[a-z0-9-]+\.[0-9]+)$'&&continue;x=$(git show $c:tip) y=$(git show $c:time) H=$(git show $c:hash|cut -d" " -f1);case $y in ''|*[!0-9]*)continue;esac;v "$x"||continue;case " ${AGI_HASHES:-sha256 sha384 sha512} " in *" $H "*);;*)continue;;esac;[ "$(git show $c:hash)" = "$(d "$x" "$y"|cut -d' ' -f3-)" ]||continue;d "$x" "$y">$t/m
 for q in $(git rev-parse $c^@);do w=$(git show $q:tip);v "$w"&&git merge-base --is-ancestor "$w" "$x"||continue 2;done
 git show "$x:$G/ring"|grep -aE '^[a-z][a-z0-9-]* (ssh-ed25519|ecdsa-sha2-nistp256|pq-sha256|x25519|cert-authority (ssh-ed25519|ecdsa-sha2-nistp256)) [A-Za-z0-9+/]+=*$'|sed -E 's/^([a-z0-9-]+) cert-authority /\1@agi cert-authority,namespaces="agi-checkpoint" /;t;s/^([a-z0-9-]+) /\1@agi namespaces="agi-checkpoint" /'>$t/a;:>$t/l
 for p in $(git ls-tree --name-only $c sigs/|sed 's|sigs/||;s|\.[0-9]*$||'|sort -u);do for f in $(git ls-tree --name-only $c sigs/|grep "^sigs/$p\.");do git show $c:$f>$t/s
  ssh-keygen -Y verify -f $t/a -I $p@agi -n agi-checkpoint -s $t/s<$t/m 2>/dev/null|sed -n 's/.* with \([A-Z0-9-]*\) key \([^ ]*\).*/\1 \2/p';done|sort -u>$t/k
  for a in ${AGI_SIGN:-ED25519};do grep -q "^$a " $t/k||continue 2;done;l=$(lv "$x" $p)&&[ "$l" ]||continue;echo "$l $(cut -d' ' -f2 $t/k|sort -u|tr '\n' ' ')">>$t/l;done
 sort -n $t/l|awk -v K=" ${AGI_CKK:-} " '$1<0{exit 1}{u=1;for(i=2;i<=NF;i++)if($i in S)u=0;for(i=2;i<=NF;i++)S[$i];if(u){if(!n++)m=$1;M=$1}}END{k=2;if(match(K," "m":[0-9]+"))k=substr(K,RSTART+length(m)+2,RLENGTH-length(m)-2);exit !(n&&M-m<=1&&n>=k)}'&&echo "$x $y $c";done;:;;esac
```
**Bytes against the rails.** BASE, ONE extraction (DG1's question, 04:0xZ): `git show <rev>:.agi/nodes/.geometry/engine.md | wc -c`, the WHOLE file, as F32/R6 wrote it. §AB's change to it is a DELTA of map lines: -60 B `signers`, -119 B `agi-signers`, +~62 B `ckpt` = **-117 B** (AB.5 adds `revoke` + `pq`, ~58 B each: net **-1 B**). CORRECTION (04:0xZ): the absolute '8,186 B, 6 B spare' that AA2 K1 and this section carried is NOT reproducible: on the trunk at 10-02 18:21 engine.md measured 8,298 B whole / 8,103 B without its frontmatter, and neither + K1's +18 B gives 8,186. The doc defines the rail TWO ways, and they disagree today (measured at 2c59fd5f6): F21 (round 1) tiers `wc -c` of config:engine as depth 0+1 <= 4,096 · the code counted <= 8,192 · the whole <= 12,288, which read 5,279 (before `## files`, OVER) · 7,358 (inside the ~~~ fences, within) · 9,132 (within); R6/F32 (rounds 5-6) say `wc -c engine.md` <= 8,192, which reads 9,132 B: OVER since c3bd6edbb (10-02 20:14, 8,391 B), independent of §AB. Which definition is the rail is belam's to rule (then: raise it or cut the map). RULED 04:21Z (written once, under §R's falsifiers: 'THE 8 KB RAIL, RULED'): F21's tiers, the code inside the fences <= 8,192 and the whole file <= 12,288. AA2.63 therefore = both tiers hold after the build, §AB's net delta reported per line. SEED: 0 B. Graph data: the ring node (~100 B per post per column) and the cells AGI_SIGN · AGI_HASHES · AGI_CKK (k per level) · the rules cell · gpg.ssh.program.
**Honest limits.** (1) Inside one generation an owner cert can still be stretched by backdating up to the next block (expiry is read at the newest block's time); outside it, it is dead (C18). (2) The grace window is the block cadence at the post's level: revocation = re-vouch + a block now. (3) The repo's object hash is sha1: a block's own digest (sha256/sha512 of the whole tip tree, a cell) is the collision-resistant anchor until the repo moves to sha256 objects (UNMEASURED: git's sha256 repos interoperate poorly today). (4) The X25519 fold is ed25519-specific (the birational map); a PQ seal column (ML-KEM) is a separate ring line per post, same rule. (5) Root on a box can read a live generation's key (no TPM, O.3); what it gets dies at the out-line. (6) Retiring agi-signers needs each post's first ring line, written once by its parent (C8 / E7). (7) Level adjacency admits owner at level 0 for blocks; the mail matrix a() still excludes owner (it has no harness): the one place blocks and mail read the tree differently.
**Falsifiers (AA2.54-AA2.66).** AA2.54 C1-C21 + E1-E8 on the integrated grow-gate (one loop): DG1's build · AA2.55 a box with ONLY the seed + the trunk reaches the same verdicts on all 58: UNRUN (two boxes) · AA2.56 the out-line on a live post: one ring commit per `.fresh`, 0 per crash restart: DG1's build · AA2.57 T1-T10 through agi-land (all-is-one's lane 6s', ring-gate as GROW_GATE): all-is-one · AA2.58 L1-L8: PASS scratch · AA2.59 H1-H5: PASS scratch · AA2.60 X1-X4: PASS scratch · AA2.61 a real PQ column (ML-DSA) under the hybrid cell: UNRUN · AA2.62 `gpg.ssh.program` = a composite signer: a commit verifies only if both halves do: UNRUN · AA2.63 after the build, the code inside config:engine's fences <= 8,192 B AND the whole engine.md <= 12,288 B (the extraction in 'THE 8 KB RAIL, RULED'), §AB's per-line delta reported, agi-gate HEAD rc 0: DG1's build · AA2.64 after agi-signers retires, the box's allowed_signers is only the projection of the trunk's ring: DG1's build · AA2.65 agi-land ancestor-or-self: 6u lands, 6v refused: PASS (all-is-one) · AA2.66 a FLOW ROTATION run cuts one block per phase transition, its parties only, and the run's phase tree equals its block DAG: DG1's build.

### AB.5 · THE FIFTH INPUT (owner 03:1xZ via belam [owner], amends §AB before DG1 writes AA2.59-62 + AA2.60): a quantum-safe signature NESTED inside the classical one; keys PROVABLY, TRUSTLESSLY revoked by publishing each retired private key; a nest of sealed capsule signers and rotators, atomic and immutable, with exposed keys piling on top
Owner, verbatim: "Can we somehow bridge the signatures? Like a quantum safe inside a non-quantum one. Also could the keys be probably revoked? Like it gets written into the post as the last used private key or something private keys stay always sealed inside capsule and it's a nesting of sealed capsule signers and rotators that is atomic and immutable over time as more and more now exposed private keys pile on top." (correction 03:1xZ: "probably" = PROVABLY, TRUSTLESSLY.) Rulings in hand: conflict 3, the owner 03:15Z: this proof of concept runs on ROOT-READABLE keys on this box (undoable; the iPhone secure signer is a later round). Conflict 2, alive 03:1xZ, measured read-only: a landed v5 commit reads `verified:false, reason no_user` on GitHub (an @agi email matches no account), and origin answers WITHOUT a token, so it is PUBLIC-READABLE.

```
ONE GENERATION of post p = three keys born together at the out-line, three ring columns, three fates:
  SIGN  ssh-ed25519   ring: p ssh-ed25519 <pub>    signs commits + the OUTER block signature   retired -> sealed in p's capsule -> PUBLISHED once the lowest block seals its hand-off
  PQ    sha256 tree   ring: p pq-sha256 <root>     the INNER block signature (2^h one-time leaves) retired -> deleted (old blocks are held by the newer blocks that seal them)
  SEAL  x25519        ring: p x25519 <pub>         opens p's capsule shares                     retired -> deleted, NEVER published (re-wrap to the next SEAL first)

a block signature blob = OUTER( payload + "\n" + INNER(payload) ):  ssh-keygen -Y sign over the payload AND the inner; the inner verifies against the ring's PQ column
  a forger with the OUTER key (a quantum break, or the published key itself) can re-sign anything outer; the inner still fails  ->  publishing SIGN keys is safe
the PILE: refs/revoked, one commit per published key (post + key), never pushed; a publication holds from the bytes alone iff
  key's public half = a CLOSED ring line of p  ·  the commit that closed it was signed by that same key (the self-revocation statement)  ·  a holding block seals it
```

**Measured (03:1xZ-03:2xZ, scratch; sha256 only, no PQ library exists on this box: no oqs / pyspx / ML-DSA in cryptography 41 / OpenSSL 3.0):**
| # | case | result |
|---|---|---|
| P1 | the prototype: a Merkle tree of Winternitz one-time keys (w = 16, 67 chains), one tree per generation, h = 8 | keygen 0.19 s for 256 signatures, sign + verify < 1 ms, signature 2,404 B, ring column 32 B: verifies |
| P2 · P3 | a tampered message · another generation's root | no · no |
| N1 | an honest nested blob (outer ed25519 over payload + inner) | outer yes, inner yes |
| N2 · N3 | a forger holding the OUTER key changes the payload and reuses the inner · invents an inner | outer YES, inner NO · outer YES, inner NO |
| N4 | strip the outer and forge only the inner | no (needs the one-time secrets) |
| S1 · S2 | a capsule share wrapped to gen1's separate SEAL key: the seal key opens it · gen1's SIGN key, PUBLISHED, opens it | yes · NO |
| S3 | for contrast, §AB's folded design (the share wrapped to the SIGN key's X25519): the published sign key opens it | YES: belam's conflict 1 is real, and the separate column closes it |
| S4 | hand-off: gen2's SEAL opens the re-wrap; ring seal column 32 B raw | yes |
| R1 | DG1 gen1's key published after the level-3 block sealed its hand-off | holds: "revoked director-general-1 <fp> closed <c> sealed" |
| R2 · R3 · R3b | DG1 gen2's LIVE key · a key that was never DG1's · DG1's retired key under ANOTHER post's name | refused · refused · refused |
| R4 · R5 | alive gen1 handed off, NO block seals it (grace) · after alive + all-is-one cut a level-2 block over it | refused · holds |
| R6 | a commit signed with a PUBLISHED key, any date | refused by ring-gate (T5) |
| R7 | a passphrase-ENCRYPTED key published on refs/revoked | refused at once, no prompt, no hang (`ssh-keygen -y -P ''`) |
| O1 | what pushes to origin (crons.py, read): branch_push = the checked-out branch only · grid_sync = refs/grid/* · the town mirror = refs/heads/<town>/* -> origin refs/agi/<town>/* | refs/revoked is pushed by NO job; refs/agi/* is a live remote namespace, so the pile is NOT under it |

**The answers.** (a) BRIDGE = NEST, on BLOCKS: one signature slot carries both, 0 new programs (it retires AA2.62's composite gpg.ssh.program for blocks). Commits stay classical and become quantum-safe once SEALED (every block's digest covers the whole tip tree); the exposure is the grace window, the same bound as §AB limit 2. An inner on every commit (a 2,404 B trailer) is a cell, off by default. The PQ column bounds the generation: 2^h leaves (a cell), and the generation MUST shift before they run out, so the generation shift is forced by the math, not by policy. The leaf index = how many blocks already carry this post's signature under this root (the DAG is the counter; limit 9). (b) PROVABLE REVOCATION = the pile at refs/revoked, checked by `revoke` from the bytes alone. WHAT STAYS TRUSTED, said plainly: inside the sanctuary, the k-of-n block quorum (checkable from the ring); TRUSTLESS to an OUTSIDE reader needs an external anchor of the top block's digest (e.g. a public timestamp chain) = an outward act, the owner's to name, never built without his go. (c) conflict 1: SEAL is its own column, deleted, never published (S1-S4). (d) conflict 2: the stated rule for plain git and GitHub readers is "only ring-gate's verdict counts"; the badge never vouches for @agi keys (alive); published keys stay OFF origin until the owner names the outward act. (e) conflict 3: the owner's ruling stands (root-readable POC; §AB limit 5).
**alive's gate line, re-scoped (alive AA1.K, 03:22Z, 176 B, a pattern only, 12/12):** the TRUNK is pushed hourly to a public origin, so a trunk node carrying ANY `-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----` block (OpenSSH, RSA, EC, PKCS8, encrypted PKCS8) is refused WHATEVER key it is (a live key leaked, or a retired one in the wrong place); a publication lives only on refs/revoked, where `revoke` rules it. No derive step on the trunk (`ssh-keygen -y` would prompt on an encrypted key and stall the land); `revoke` derives with `-P ''`, which fails instead of prompting (R7).
**The out-line, revised (~90 B in engine-root):** generate the next SIGN, PQ (seed + root) and SEAL keys · commit their three ring lines over the post's own, signed by the CURRENT sign key (this commit IS the self-revocation statement) · land · re-wrap capsule shares to the next SEAL · seal the old SIGN key into the post's capsule (systemd-creds, root-readable on this box per the owner's ruling) · delete the old PQ seed and the old SEAL key · `touch ~/.fresh`. When the lowest block seals the hand-off, the successor commits the old SIGN key to refs/revoked and deletes it from the capsule.

`revoke` whole (1,588 B, sha256 e1301b5f30d0bb8d): it verifies the closing commit against the ring AT ITS PARENT, in its own allowed-signers file, never the caller's git config (SM 04:0xZ: with an empty global config the earlier bytes read %GK empty and refused R1/R5):
```sh
#!/bin/sh
# revoke check [REF]: every commit on refs/revoked (NEVER pushed: origin is public-readable) carries files post + key (a RETIRED private key, published on purpose).
# A publication holds, from the bytes alone, iff: the key's public half was <post>'s ring line · the trunk commit that CLOSED that line was signed by that same key (the self-revocation statement) · a holding block's tip contains that commit (sealed). Else it is refused: a live key, an unknown key, or one still in grace.
G=.agi/nodes/.geometry;t=$(mktemp -d);trap 'rm -rf $t' EXIT;sh ${AGI_CKPT:-ckpt} check>$t/b
for c in $(git rev-list ${1:-refs/revoked});do p=$(git show $c:post);git show $c:key>$t/k;chmod 600 $t/k;k=$(ssh-keygen -y -P '' -f $t/k 2>/dev/null|cut -d' ' -f1,2);f=$(echo "$k"|ssh-keygen -lf /dev/stdin 2>/dev/null|cut -d' ' -f2)
 v=$(git log --format=%H -S"${k#* }" ${AGI_TRUNK:-trunk} -- $G/ring|head -1);[ "$v" ]&&git show $v^:$G/ring|grep -qxF "$p $k"&&! git show $v:$G/ring|grep -qF "${k#* }"||{ echo "refused: $c $p: not a CLOSED ring line of $p";continue;}
 git show $v^:$G/ring|sed -E 's/^([a-z0-9-]+) cert-authority /\1@agi cert-authority,namespaces="git" /;t;s/^([a-z0-9-]+) /\1@agi namespaces="git" /'>$t/a
 [ "$(git -c gpg.ssh.allowedSignersFile=$t/a log -1 --format='%G? %GK' $v)" = "G $f" ]||{ echo "refused: $c $p: the closing commit was not signed by this key";continue;}
 for x in $(cut -d' ' -f1 $t/b);do git merge-base --is-ancestor $v $x&&{ echo "revoked $p $f closed $v sealed";continue 2;};done;echo "refused: $c $p: closed but no holding block seals it yet (grace)";done
```
`pq.py` whole (1509 B, sha256 d0e37a478bc590a8; the PROTOTYPE inner, XMSS-shaped, plain Winternitz with no bitmasks: production = SLH-DSA (FIPS 205, stateless) the day a verifier exists on the box, as one more column value):
```python
# pq.py: a hash-only (sha256) signature, one Merkle tree of Winternitz one-time keys per GENERATION (XMSS-shaped, w=16, n=32, 67 chains).
# The ring's PQ column holds the tree ROOT (32 B). A PROTOTYPE to measure the nesting: production = SLH-DSA (FIPS 205) the day a verifier is on the box.
import hashlib,sys,os,base64 as B
H=lambda *a:hashlib.sha256(b''.join(a)).digest();W=16;L1=64;L=67
def ch(x,i,s,k):
    for j in range(i,i+s):x=H(k,j.to_bytes(1,'big'),x)
    return x
def dg(m):
    d=[b>>4 for b in H(m)for _ in[0]]+[b&15 for b in H(m)];d=[x for p in zip(d[:32],d[32:])for x in p];c=sum(W-1-x for x in d);return d+[(c>>8)&15,(c>>4)&15,c&15]
def sk(seed,i,j):return H(seed,b'sk',i.to_bytes(4,'big'),j.to_bytes(1,'big'))
def leaf(seed,pub,i):return H(b'leaf',*[ch(sk(seed,i,j),0,W-1,pub+bytes([j])) for j in range(L)])
def tree(seed,pub,h):
    lv=[leaf(seed,pub,i) for i in range(1<<h)];T=[lv]
    while len(lv)>1:lv=[H(lv[k],lv[k+1]) for k in range(0,len(lv),2)];T.append(lv)
    return T
def sign(seed,pub,h,i,m,T=None):
    T=T or tree(seed,pub,h);d=dg(m)
    return i.to_bytes(4,'big')+b''.join(ch(sk(seed,i,j),0,d[j],pub+bytes([j])) for j in range(L))+b''.join(T[l][(i>>l)^1] for l in range(h))
def verify(root,pub,h,m,s):
    i=int.from_bytes(s[:4],'big');d=dg(m);c=[s[4+32*j:36+32*j] for j in range(L)];x=H(b'leaf',*[ch(c[j],d[j],W-1-d[j],pub+bytes([j])) for j in range(L)])
    p=s[4+32*L:];k=i
    for l in range(h):s2=p[32*l:32*l+32];x=H(x,s2) if k&1==0 else H(s2,x);k>>=1
    return x==root
```
**Bytes.** BASE: two more map lines (`revoke`, `pq`, ~58 B each): §AB's net delta on `wc -c engine.md` = -179 + 62 + 116 = **-1 B** (the absolute '8,186' is withdrawn: see §AB's Bytes line; the rail is already exceeded on the trunk, belam's to rule). SEED 0 B. A ring line per post per generation grows from 1 to 3 (sign ~90 B, pq ~80 B, seal ~60 B).
**Honest limits (adding to §AB's 7).** (8) The prototype is a plain Winternitz + Merkle scheme with no randomized hashing, which is weaker than WOTS+/XMSS/SLH-DSA; it measures the NESTING and the sizes, not a production PQ scheme. (9) It is STATEFUL: a leaf must never sign twice. The index is read from the blocks, but a block signed and never written would repeat its index, so the post writes the block before it signs another. SLH-DSA (stateless) removes this. (10) Publishing a retired SIGN key is safe only while the PQ inner of the newer blocks holds; a quantum forger could then rewrite only what no PQ-nested block seals yet (the grace window). (11) "Trustless" stops at the sanctuary's edge until the owner names an outward anchor.
**Falsifiers (AA2.67-AA2.73).** AA2.67 P1-P3 + N1-N4: PASS scratch · AA2.68 S1-S4: PASS scratch · AA2.69 R1-R7: PASS scratch · AA2.70 ckpt verifies a NESTED blob (outer + inner against the ring's pq column) and refuses a block whose inner fails: DG1's build (the ckpt delta) · AA2.71 a trunk range carrying ANY PRIVATE KEY block (OpenSSH, RSA, EC, PKCS8, and an ENCRYPTED key, under a timeout) is refused at agi-land, a key-shaped non-key passes: alive's AA1.K line (176 B), all-is-one's land lane · AA2.72 `git ls-remote origin | grep -c refs/revoked` = 0 after a day of publications: DG1's build (read-only) · AA2.73 a generation that exhausts its 2^h leaves cannot sign another block, and its successor can: DG1's build.

### AB.6 · THE SIXTH INPUT (owner 03:25Z via belam [owner]): the OUTWARD sealer = GitHub Actions, retrying gracefully -- the external anchor §AB.5 left to the owner
**Given:** belam's reading: an Artifact Attestation (a Sigstore certificate -> the public Rekor log) over ONLY a block digest, never a key; trigger = tag, dispatch or a scheduled sweep (idempotent); the box pushes with backoff, and a block it cannot seal stays UNSEALED-EXTERNALLY, never failed; the gate reads "externally sealed" as an optional SECOND fact, never a landing requirement; `.github/workflows` = one new allowed-paths row (belam, at landing). alive, measured read-only 03:2xZ: origin is public, not a fork, its DEFAULT branch is `master` (not the trunk), 0 workflows, no `.github/` on the trunk; GitHub runs `schedule` and `workflow_dispatch` ONLY from the default branch's file, and a tag push runs the file inside the tagged commit.
```
box: a holding block ──(block_push: git push origin 'refs/agi/block/*:refs/agi/block/*', backoff 1-2-4-8 min, then give up quietly)──▶ origin
origin master: .github/workflows/seal.yml ── every 30 min (and on dispatch) ── fetch refs/agi/block/* ── for each block:
     subject = AGI_SUBJECT(<block>) = sha256 over sorted "sha256(file) path" lines of its tree (tip, time, hash, EVERY signature: binds WHICH quorum)
     already attested? (GET repos/<origin>/attestations/sha256:<subject>) ── yes: skip   no: one line in subjects
  ── actions/attest-build-provenance@v2 (subject-checksums) ──▶ a Sigstore cert for this workflow on master ──▶ Rekor (public, append-only)
an OUTSIDE reader: git fetch origin refs/agi/block/<b> (8 objects, no trunk history) · write AGI_SUBJECT's LISTING to a file (its sha256 IS the subject)
     · gh attestation verify <listing> -R <origin> --cert-identity <origin>/.github/workflows/seal.yml@refs/heads/master (the WHOLE identity, never the path alone)
the gate (optional second fact, never a requirement): the same check, the WHOLE workflow identity pinned -> "externally sealed" beside "holds"
```
**The trigger, chosen: the scheduled sweep on `master`.** It is the only shape that retries by itself (a missed or failed run = the next sweep; attesting is idempotent by subject) and it puts 0 bytes on the trunk. A tag per block needs `.github/workflows` IN the tagged commit, i.e. on the trunk, plus a tag push per block (one more outward write per block, and no retry). `workflow_dispatch` stays as a manual nudge only. The footprint row names the branch: `master: .github/workflows/seal.yml` (master is not the trunk; who writes master is belam's call).
**Measured (03:3xZ, scratch, no network, nothing pushed):**
| # | case | result |
|---|---|---|
| G1 | the signed payload's digest (`tip time hash digest`) across 10 fixture blocks | only 5 distinct: every block over the SAME tip at the SAME time shares it (the payload does not name the signers or the sealed blocks), so it cannot pin WHICH quorum sealed |
| G2 | the whole-block subject across the same blocks | all distinct: the subject binds the signature set |
| G6 | `git archive` tar bytes under tar.umask 0002 / 0022 / 0077 (alive 03:30Z) | THREE different digests: tar is an implementation detail, so box and runner could disagree on an honest block |
| G7 | the AGI_SUBJECT recipe (no tar: sha256 per file, sorted paths) under the same three umasks · in an outsider's fresh clone | ONE digest · the same digest; 9/9 blocks distinct |
| G3 | an OUTSIDER fetches only `refs/agi/block/L3` into an empty repo and recomputes | the same subject, 8 objects fetched, no trunk history |
| B1 · B2 | a signed block plus one extra file `evil name` · the same block without it | does not hold · holds: a block's tree is ONLY tip, time, hash, sigs/<post>.<n>, so every path the recipe reads is plain ASCII (alive 03:33Z: `read f` and core.quotePath would otherwise digest EMPTY content for an odd name, silently, on both sides) |
| W1 · W2 | DG1 (current key) adds `.github/workflows/zz.yml` on the trunk · the owner (cert on belam's current key) adds it (all-is-one 03:30Z) | refused: ruled by owner · admitted. Without the row ANY post could land a workflow that GitHub runs on the next hourly push |
| G4 | the sweep's run block against the fixture "origin" with a stub `gh` (one subject already attested) | lists exactly the un-attested subjects; with every subject attested, lists 0 (idempotent) |
| G5 | `seal.yml` parses (pyyaml 6.0.1): triggers schedule + workflow_dispatch, permissions contents read, id-token write, attestations write | ok |
NOT run (outward, needs the GO): the workflow on GitHub, an attestation, `gh attestation verify`, the push of block refs to origin.
`seal.yml` whole (1,489 B, sha256 686368aa896cb1e8):
```yaml
# .github/workflows/seal.yml on master (the default branch: GitHub runs schedule + dispatch only from it). The OUTWARD sealer (owner 03:25Z):
# every 30 min, attest each block on origin whose WHOLE-BLOCK digest (the AGI_SUBJECT recipe: sha256 over sorted 'sha256(file) path' lines of the block's tree: tip, time, hash, every signature) has none yet; a subject is a DIGEST, never a key; a miss = the next sweep
name: seal
on:
  schedule: [{cron: '*/30 * * * *'}]
  workflow_dispatch:
permissions: {contents: read, id-token: write, attestations: write}
jobs:
  sweep:
    runs-on: ubuntu-latest
    steps:
      - id: s
        env: {GH_TOKEN: '${{ github.token }}', R: '${{ github.repository }}'}
        run: |
          git init -q b && cd b && git fetch -q "https://github.com/$R" '+refs/agi/block/*:refs/agi/block/*' || true
          for c in $(git for-each-ref --format='%(objectname)' refs/agi/block); do
            git ls-tree -r --name-only $c|grep -qvE '^(tip|time|hash|sigs/[a-z0-9-]+\.[0-9]+)$' && continue
            d=$(git ls-tree -r --name-only $c|LC_ALL=C sort|while read f;do printf '%s %s\n' "$(git show $c:$f|sha256sum|cut -c1-64)" "$f";done|sha256sum|cut -c1-64)
            gh api "repos/$R/attestations/sha256:$d" >/dev/null 2>&1 || echo "$d  block-$c"; done > ../subjects
          echo "n=$(wc -l < ../subjects)" >> "$GITHUB_OUTPUT"
      - if: steps.s.outputs.n != '0'
        uses: actions/attest-build-provenance@v2
        with: {subject-checksums: subjects}
```
**Box side, `block_push` (a crons.md job cell, belam's GO): ~110 B, one line:** `for i in 1 2 4 8;do git push -q origin 'refs/agi/block/*:refs/agi/block/*'&&break;sleep $((i*60));done;:`. It always exits 0, so a failed push leaves the block UNSEALED-EXTERNALLY and the next run retries. A block holds only public signatures over a public trunk tip, so it may go to origin. The PILE (`refs/revoked`) never does, and refs/revoked is not under the pushed pattern.
**What an outside reader then trusts, said plainly:** GitHub's OIDC identity for `seal.yml` on `master` of origin, and Sigstore's Rekor log. That is the external anchor; it proves WHEN a block existed (Rekor's inclusion time) and that THIS workflow saw it, not that its quorum is honest (that is the ring's and the blocks' job, checkable from the bytes). A rewrite of `seal.yml` on master changes the identity: the gate's optional fact names the workflow path it accepts.
**The recipe is ONE cell, AGI_SUBJECT, read by both sides** (the box's optional gate fact and seal.yml carry the same line; AA2.79 checks they are byte-equal). It is pure sha256 over file contents, so it does not lean on the repo's sha1 object ids.
**The identity is pinned WHOLE (all-is-one 03:33Z):** a Sigstore certificate names `<origin>/.github/workflows/seal.yml@<ref>`, and a copy of seal.yml pushed on ANY other origin branch (posts/*, a pushed merge-up ref: not under the land gate) gets the same PATH under another @ref, so every check matches `@refs/heads/master` too (from the GitHub docs, not run). The identity is ONE literal cell, AGI_SEAL_ID = `https://github.com/<owner>/<repo>/.github/workflows/seal.yml@refs/heads/master`, written once and never derived from `git remote get-url origin`: that URL ends in `.git` and the identity does not, so a spliced value never matches and every honest block reads "unsealed" (safe, but silently useless; all-is-one 03:38Z). The runner side may check it against `${{ github.workflow_ref }}`.
**Honest limit (15), added 05:4xZ on SM's mur sm18 (RING.3 952787f32 demoted, 4 bypasses):** the §AB `ring-gate` is a PROTOTYPE, unhardened against the same classes: it diffs ring lines against `c^` (the first parent, not the landed h), parses names through jq/sed with no NUL/LF/CR refusal, and its bootstrap has no receiving-tip walk. Whether each of the four reproduces on it is UNMEASURED here; its fixture passes only because none of the four is a case in it. NEVER install the prototype: the build follows the mur's fix, as DG1 ruled it 05:44Z (every path ruled against the landed h · ring and posts.md read with --text, NUL/LF/CR refused in any ring or name field · bootstrap only for a ring path with no history on the RECEIVING tip's ancestry).
**Honest limits (adding to §AB's).** (12) GitHub's schedule is best-effort (runs can be delayed or dropped under load); the sweep makes a drop cost one interval, never a block. (13) Origin's `refs/agi/<town>/*` is the town mirror's namespace, so `block` is a reserved town name. (14) The external anchor is GitHub + Sigstore: trustless of the SANCTUARY, not of them.
**Falsifiers (AA2.74-AA2.78).** AA2.74 G1-G5: PASS scratch · AA2.75 after belam's GO for block_push + seal.yml: a block pushed at t is attested within two sweep intervals, and `gh attestation verify` on its rebuilt LISTING file, with the whole --cert-identity, passes for an outside reader (on a tar it fails by construction: alive 03:33Z): UNRUN (outward) · AA2.76 a second sweep creates 0 new attestations: UNRUN · AA2.77 with origin unreachable, block_push exits 0, the block still HOLDS on the box and reads "unsealed externally": DG1's build · AA2.78 `git ls-remote origin` lists refs/agi/block/* and NO refs/revoked: UNRUN (outward, read-only once pushed) · AA2.79 the AGI_SUBJECT line in seal.yml and in the box's gate fact are byte-equal, and G6/G7 hold on GitHub's runner: UNRUN · AA2.80 W1/W2 through agi-land: all-is-one's lane.


## AC · D2 SEASON ROLLOVER · self-perpetuating -- THE GOAL TREE IS THE COLLAPSE: the overview holds the season, each goal holds its own slice, and a build carried across renders its cone
**Asked (belam [owner] 14:40Z 10-07; split by alive 14:40Z, taken by all three):** D2 = which collapse at rollover: (a) "the overview nodes for season 2 will actually record all the graph slices that lead into those overview nodes" or (b) "collapse only the nodes before AND after a given build node into that build node's graph", how each renders, and the TANGLE: "maybe having the graph remain in a relatively tangle-free state is another stat falsifier ... Or alternatively maybe a more cross-connected graph is better and the redundancy it leads to in the overview nodes is fine." Carried owner verbatim from core's goal:g5.4.1.2 (10-06): "collapse all the way down to the overview nodes for this season ... The rest of the graph can be walked inside that overview node's graph slice" · "after it's stacked I want the metrics for that stack to be baked into the node". DESIGN ONLY. The collapse VERB is alive's (D1), the legacy marker is all-is-one's (D3), and the tangle number is alive's; this section picks WHICH slice and HOW it renders.
**What am I actually trying to get the machine to do?** At a season's end, fold everything the season grew into a few nodes so that the next season's tip is small, and anyone can still walk, count and REGROW the old season from those nodes alone. My lens: the body regrows from its description, so the test of a rollover is that it is reversible from the bytes it leaves.

**AC.1 · Measured first (local-maxxing/season2/main 419835fea, 5,557 live nodes; parents read from front matter, aliases hyp:/exp: resolved; scratch, read-only):**
| cut | what one slice is | nodes covered | in > 1 slice |
|---|---|---|---|
| (a) as written: the parent chain INTO each overview | overview <- bigger_outcome <- outcome <- mvp/goal | **105 = 1.9 %** (17 slices of 5-8 nodes) | 14 |
| (b) before AND after each build node | ancestors + descendants of the build | **495 = 8.9 %** (238 builds, cone median 9, max 67) | 76 |
| (a') the GOAL TREE: each non-goal node belongs to its NEAREST goal(s) on its parent paths | a goal + the nodes that hang from it before the next goal down | **4,437 of 4,923 non-goal nodes = 90.1 %** homed; 486 homeless | 653 (441 two goals, 212 three+) |
Why (a) covers so little: the chain stops closing long before it reaches the work. Only **3 of 2,290 experiments** and **6 of 1,456 hypotheses** have any outcome downstream; outcomes hang from mvps (27) and goals (21). core's et-grok-pilot f0b99691c ran the leaf sweep (109 leaf outcomes, 3 season overviews) and still reaches **5.1 %** (15 of 2,361 experiments). The goal tree is almost a pure tree: **2 of 634 goals** have more than one goal parent; one 2-node parent cycle exists (exp/hyp a00-ddbe3410 iterative-traversal). The 486 homeless are mostly spine and carried kinds: verdict 110 · build 107 · exp 61 · hyp 41 · idea 41 · vision 31 · mvp 21 · bigger_outcome 19 · outcome 19 · overview 17. On core/season2/main ccb285d98 the same numbers hold within 3 % (5,696 nodes; (a) 1.8 %).

**AC.2 · The choice: (a'), which is the owner's (a) read through the goal tree, with (b) kept as the RENDER of a carried build, never a second collapse.** The owner's guess ("not much cross-chain stuff ... other than goals and subgoals and subsubgoals but that wraps back nearly into overview nodes") is right about the GOAL TREE and wrong about the parent chain: the chain into an overview is a thin spine, while the goals are a near-perfect tree that already holds 90 % of the work. So the recursion follows the goals, bottom up:
```
overview:s2-<vision>  nest: [its root goals]        (a LIST: the vision's root goals)
  goal:gN             nest: subtree                 -> the non-goal nodes whose nearest goal is gN, stopping AT its subgoals
    goal:gN.M         nest: subtree                    (each expands itself), down to the leaves
season residue        overview:s2-residue  nest: [the homeless that are not carried] (verdicts, exps, hyps, ideas with no goal above)
carried live          open goals · build nodes (D3 'legacy') · visions · morals · towns · docs · .geometry: never collapsed
```
Each node keeps ONE home for its bytes: its own file (mint id). A slice holds REFERENCES. D1 after the grid (alive, doc:rse-d1-nest v3, merge-up alive/d1-nest 4538c6250) holds a slice IN the container's front matter: `nest: subtree` = every node reached DOWN the parents edges, descending through members with no `nest:` and stopping (inclusive) at a member that carries its own, which expands itself; or `nest:` + a list of ids. A collapse is ONE one-node commit; members stay files. alive redefined `subtree` that way for D2 (02:12Z 10-08): read as ONE level, it reached only 1,580 of 4,446 homed nodes (35.5 %, trunk cdece2853), since most work hangs 2+ levels under its goal (depth 2: 2,376 · 3: 371 · 4+: 119). So `nest: subtree` on every goal IS the nearest-goal homing, at 0 B per member, and a multi-homed node (13.3 %) appears in each of its nearest goals' expansions at no cost. That answers the owner's either/or: **redundancy is free in bytes, so cross-connection is fine; tangle is reported as a STAT, not a failing falsifier.** alive's number (AA1.N): 457 nodes (7.9 %) sit under two or more top goals, 52 % of them g6 x g7 (238); the overview chains show 16 in two or more slices and 6 cross edges. It costs only legibility, and the render shows it (AC.4). A vision's overview takes the root goals whose `lens`/`judged_against` names that vision. Today every root goal's PARENT is vision:self-perpetuating (all 24), so the parent edge cannot split visions; the lens cell can, and a root goal with no lens goes to the residue overview, never guessed.

**AC.3 · The rollover, as steps (each one a normal gated landing of one-node commits; no ref, no store):**
1. **Close:** every completed leaf goal has an outcome (the pilot's leaf sweep, ADAPTED: through our gate, judged by `season judge`). Not required for coverage under (a'), but it is what the overview REPORTS.
2. **Collapse:** ONE one-node commit per container: each goal gains `nest: subtree`; each vision overview gains `nest:` + its root goals; the residue overview gains `nest:` + the homeless that are not carried. The same commit writes the container's baked STACK METRICS block in its body (owner: "read instantly after the fact"), read from the files and D1's one history walk: counts by type and status over `members()`, the commits touching the members, and the tangle stat. The selector is D1's `members()` (the `parents:` cell only). The pilot's `git grep -F "  - <id>"` also matches tags, seeds and moral_audit evidence lines, and runs one grep per node. Order WITHIN step 2 does not matter: each edit is independent, and a cycle stops at D1's seen set. Step 4 runs after step 2, so a carried goal's newest entry is its `season:` commit (AC.7).
3. **Retire:** every member that is not a carried kind moves to `deprecated/<type>/` with `status: deprecated` (retire, never delete; "stay deprecated" is the owner's own word on g5.4.1.2). D1's walk follows the rename, so a retired member keeps its whole history; `active + deprecated` never drops.
4. **Carry:** carried kinds stay live, and EACH carried node gets ONE one-node commit that SETS `season:` to the season being opened, ADDING the cell when absent (all-is-one 02:11Z 10-08, measured: of 297 build nodes 195 read `season: 1`, 36 `season: 2`, 66 none). It is the node's SEASON ENTRY that D3's legacy rule reads (doc:rse-d3-legacy, restated by all-is-one 10-08 after the grid): entry = the newest of the path's first commit (renames followed), the commit that adds `nest:`, the commit after which `season:` equals the current season; the entry commit itself never counts. Without it, a node graphed in season 2 would read as graphed in season 3. A carried goal that gains `nest:` in step 2 still gets its `season:` set here.
5. **Cut:** the season-3 trunk starts at that tip; archiving season-2's trunk (core: under `core/main`) is the owner's GO, never this design's.

**AC.4 · Render.** An overview or goal card shows `contains N (by type) · k carried builds · m shared with <other slice>`, and expands to `members()` read at the revision shown (D1), and its history is D1's one walk filtered to the members' paths. A CARRIED build (D3 'legacy') renders (b): its cone (past: idea/goal/mvp; future: experiments) computed from the parents edges of the retired members, so the build shows it CONTAINS the season that made it (owner: "not just plopped in, it is fully integrated") without a second collapse. A shared member renders once, with a badge per extra slice, so tangle is visible at the card it costs.

**AC.5 · D4 rollover rows (aio's doc:rse-d4-grok-pilot, mu-30 6680d8127; et-grok-pilot f0b99691c, read-only):**
| row | verdict | why, from the bytes |
|---|---|---|
| (a) `### slice` hook + piece (5,234 B): overview records `slice_ref: refs/slice/season-N-archive` | **ADAPT the hook, DROP the piece** | the idea (an overview names where its slice lives) stands, but the place is the overview's own front matter (D1's `nest:`; owner: "each node is itself a mini branch"), not a second namespace. The piece: `move --to-grid` makes a SECOND writer of `refs/grid/*` (one writer per ref, §B.2), writes a tree of node.md only (payload dropped) and adds a version to every member, so the stats it should leave alone MOVE (aio's finding); `pack` never writes `nested/`, so the recursion is read-only on paper; the `--root` selector is the loose grep above; 5,234 B is 64 % of the 8 KB code rail |
| (b) `season` (2,648 B), season JUDGE only; season.py + `rollover --apply` retired | **KEEP the judge, ADAPT one cell** | it is the step-1 judge, not rollover. It reads `current_season` from ladder.md, which §Z3 retires to config:engine; read it there |
| (c) rolslice.py (11,936 B), retired by belam 59bfbb7a7c | **DROP** (stays retired) | superseded by D1; nothing in AC needs it |
| (d) pilot goals g5.4.1.2 (stack/archive) + g5.4.1.3 (slice-move), design only | **KEEP g5.4.1.2's owner points, ADAPT its procedure; g5.4.1.3 folds into D1** | the 8 owner points are verbatim and AC carries all of them (hard move off the tip, mint id is the link, stay deprecated, metrics baked, overviews are the archive, season trunk archived on owner GO, no node lost, no run). Its procedure's `refs/slice` and its unnamed "selector" become AC.3 steps 2-3 (`nest:` + `members()`) |

**Falsifiers (AC.1-AC.7), all on a scratch copy of the trunk, never the live tip:**
AC.1 **coverage**: after step 4, every node of the season-2 tip is either live (a carried kind or an open goal) or a member of at least one slice; orphans = 0. Today's homeless 486 is the number this must drive to 0 (residue overview included).
AC.2 **stats invariance** (D1.2): `links.py`'s active + deprecated count is identical before and after step 2 and after step 3; every metric in config:metrics is equal across step 2; a member's history gains NO commit from step 2 (only the container's file changes). Step 3 adds one rename per retired member and step 4 one entry commit per carried node, both named, neither goal-made (D3: a goal-made commit is one after which the node's parents GAIN a `goal:` id absent at its entry).
AC.3 **one home** (D1.1): every step-2 commit changes exactly ONE file under .agi/nodes (`git show --name-only --format= <sha>`), and the run creates 0 refs (`git for-each-ref | wc -l` equal before and after).
AC.4 **regrow** (this lens): at the season-3 tip, the live nodes plus `members()` of every season overview, recursively, are EXACTLY the season-2 tip's node set; and each member's file equals its season-2 bytes except its path (`deprecated/<type>/`), its `status:` line, for a container the added `nest:` cell and metrics block, and for a CARRIED node (a member that stays live: step 3 retires only the non-carried) its `season:` line as step 4 sets it. Diff beyond those = a red.
AC.5 **selector**: with `nest: subtree` on every goal, the union of `members()` equals the nearest-goal homing, a parents-only walk, on the 5,557 nodes (3,784 single-homed, 653 multi, 486 homeless at 419835fea); a node that merely LISTS a goal in a tag or evidence cell is not homed there.
AC.6 **tangle stat**: reported per slice and season-wide, beside alive's crossing count; no threshold fails a rollover (owner's "redundancy is fine" branch), a rise across seasons is a finding for the council, never a gate.
AC.7 **carry entry**: after step 4, every live carried node at the season-3 tip reads `season:` = the new season, its entry is the commit that set it (for a carried goal, newer than its step-2 `nest:` commit), and no goal-made commit sits above it; D3's rule then reads it as legacy. A carried node whose `season:` is still old or absent reads as graphed in its old season: a red.

**Honest limits.** (1) "Nearest goal" counts parent edges as written; 69 parent references do not resolve today (50 `hyp:`, 16 `idea:`), so their nodes may home one goal too high. (2) The vision split needs a `lens` on every root goal; today the parent edge cannot split them, and how many root goals carry a usable lens is UNMEASURED here. (3) The residue overview's `nest:` is a LIST: ~312 non-carried homeless ids at 419835fea, ~19 KB at alive's measured ~62 B per id (7,215 B for 116), so it may want splitting by type; unmeasured. (4) Versions made before the grid cutover stay on the frozen `refs/grid/<town>/node/<mint>`, read-only (D1); the baked metrics read files + D1's walk, so a pre-cutover grid-only version is not in them. AC stands or falls with D1's landing. (6) alive counts 5,830 nodes (trunk, its read) against my 5,557 (live flat files at 419835fea, deprecated/ and .geometry excluded); each cites its own base. (5) The measurement script lives in session scratch and is NOT in the tree; AC.5 re-derives it from this section's definition.
