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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive (agi-a8), 04:1xZ 10-01 (round 4 closed: parts 1-3 + the whole-doc pass; base f37e25ced2 + config:engine v2 50eda68b1f). Owner 03:48Z, verbatim: "Can we also make sure all the guards and watchdogs and such still work? I was thinking of also including the magic pane anchor as that would still be useful for later stuff like asking the system to work with foreign tools. Tell TM maybe Jev can be made to work even better with the new system due to its mathematical nature or likely maybe we don’t even need it? What if node schemas also contained vectors describing how a node is structured and does arranged. So the whole thing becomes composable. Same with guards and memory stuff and locations of everything. It’s all just vectors literally pointing to things. Maybe even filesystem pointers and even partition/volume-level  pointers. The math is base level for everything. No more workflow.py needed because all things are infinitely composable and run inside the “wrapper.” There’s no distinction between posts, subagents, workflows, etc. all just composable on the fly via vectors but also there’s preset routes for various functions outlined in the commands template which itself has a vector base pointing/multiplying/operating on other relevant vectors. And even a “compose new launch vector” vector to guide a model step by step. Again it should add minimum bytes to code base and I really think you guys can do it. Can you just let everyone know this has been transformative. We about to retire about 99.7% of our codebase overnight, including so many horizon goals. Tmux pane or even a more base-level pane persistence “trick” buried in all that vast hyperhuman systemic understanding from the inside." WHY this version differs: round 4 answered in three sections, one per lens, serialized. §L (self-perpetuating, asks 3 + 4): ONE launch vector, routes replace workflow.py and command:commands. §M (all-is-one, asks 1 + 2): every pointer vector is a directory of symlinks; schemas, guards (the kernel min) and locations (down to the volume) are such vectors. §N (alive, asks 5 + 6 + the guards ask): the pane is two files (a held fifo i + the typescript o) and util-linux script owns the pty, so dtach retires; the anchor is the post name; every guard and watchdog mapped to a piece, a cell, KEEP, HELD or a named GAP. Measured on the exact v3 unit bytes in the user manager (paths swapped, no root, stub harness, units removed). Three traps folded in: the journal copy, the argv in the typescript header, the umask on o. The red N.5 (a system-unit post sits outside every user-manager guard layer) is fixed by cells only: Slice=agi.slice plus a guard-init cap; its proof is a root act left to DG3 at stage 2.5. Whole-doc pass: M.1 reworded on self-perpetuating 04:0xZ note (pointer vectors are symlink dirs, a launch is a row of cells), so the doc no longer claims one representation while showing two; §0 gained the round-4 line; §G already carried all-is-one M.0 correction, §D quotes none of it. depth 0+1 of config:engine stays 4,095 B with §L lines; §N adds 148 B of code. Near miss: my first header fix (dollar-dollar H) still leaked the argv, because the outer sh expands inside its double quotes; the backslash form was measured before it was written down.
<!-- THOUGHT:END -->
