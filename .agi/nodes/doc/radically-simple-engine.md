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
- **193 duplicate parent entries** in frontmatter (e.g. a verdict listing the same experiment twice). Symlinks cannot express them.
- **27 links `find -xtype l` calls broken, while links.py reports 0 broken:** 13 parents written as `parked:g7.16.2` (the node is `goal:g7.16.2` today) · about 8 address drifts (a link kept `build:a00-fcfbc2f9-bin-adapters-grok-bot-adapter` while the node's id became `build:bin-adapters-grok-bot-adapter-a00-fcfbc2f9`; `exp:…` vs `hyp:…`) · about 6 artifacts of the scratch parser (other frontmatter lists). A link that targets the MINT id cannot go stale when an address changes. That is why the owner's two-identifiers rule belongs in the filesystem and not in a resolver.

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
This section IS the node's body, byte for byte (11,305 B, v1), between the fences below. Frontmatter at mint: `id: config:engine` · `type: config` · parent `goal:g7.16.1.11` · the Prime (or DG3 at build) mints it; the council does not (`written_by`). F19 and F21 run against the minted node.
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
   gates at every landing: the projection is non-empty and reproduces itself · V = red + mute never
   rises without a new owner goal · every at-REV read follows the links (git cat-file --follow-symlinks)
~~~

## loop — depth 1
~~~
1 BOOT   agi-seed extracts agi-project from this node @trunk; it projects the body from the graph
2 START  a post's unit starts its harness; start, resume and compact all run agi-brief first
3 WORK   the agent reads and writes plain paths in ~/t; every turn end = one signed commit on its ref
4 LAND   the master merges post refs; the gates refuse an empty or non-reproducing projection, or V up
5 TICK   tick.sh heals drift and commits it; agi-frontier calls every unmet goal into the pool
~~~

## pieces — depth 1, one line each (bytes on disk)
~~~
agi-post@.service    340 B  a post IS one unit instance: its uid, its checkout ~/t, its key, the harness under strace; a restart is a rotation
agi-inbox@.path       37 B  mail wakes a post: a change in its drop box ...
agi-inbox@.service    69 B  ... types "mail" into its session
settings.json        458 B  the harness wiring every post gets: the meter (rotate at the line), the brief at every start, one commit at every turn end
agi.ts               372 B  the same wiring for pi: the brief in the system prompt on every turn, one commit at every turn end
agi-brief            766 B  what a session sees first: the walk from its card + its own claims; the vector, then whole nodes by |b|
brief.py             562 B  b = a sum((1-a) P_theta)^k e: the complex walk over parent symlinks; |b| = how near, phase = how far up
gitconfig             79 B  every commit is signed by the post's own key
agi-flush            125 B  on exit: commit, merge, push: a dying session loses nothing
pre-receive          355 B  a push may touch only paths whose owner group the pusher is in
signers               65 B  allowed_signers = the posts' public keys
sysusers.conf         34 B  a post = one user in one group
project.sh           282 B  what the body SHOULD be, read from the graph
observe.sh           317 B  what the body IS, read from the box
tick.sh              221 B  the homeostat: diff them; heal what drifted and commit the wound
simhash.awk          241 B  stage-0 latent sense: near-duplicate and misfiled prose, no package
agi-project         1078 B  the genome: units for every post row, read from this node @REV; its own unit re-reads it
agi-seed.service     447 B  the ONE installed unit: at boot, run agi-project from this node @trunk
agi-frontier         632 B  the hunger: every active goal runs its falsifier: met | red | mute
sect                 257 B  the narrowed read: ONE section or piece of this node, byte-exact, at any REV
~~~

## files — depth 2, each whole; extract: sect <name> [REV]

### agi-post@.service (340 B)
~~~ini
[Service]
User=agi-%i
WorkingDirectory=%h/t
EnvironmentFile=%h/env
ExecStartPre=-sh -c 'ssh-keygen -qN "" -ted25519 -f%h/.ssh/id_ed25519<&-;cp %h/.ssh/id_ed25519.pub .agi/keys/%i'
ExecStart=dtach -N %t/agi-%i strace -qqfe%%file -o%h/r sh -c '${H} go'
ExecStopPost=agi-flush
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

### agi-inbox@.service (69 B)
~~~ini
[Service]
User=agi-%i
ExecStart=sh -c 'echo mail|dtach -p %t/agi-%i'
~~~

### settings.json (458 B)
~~~json
{"hooks":{"UserPromptSubmit":[{"hooks":[{"type":"command","command":"jq -r .transcript_path|xargs tail -1|jq -e '.message.usage|.input_tokens+.cache_read_input_tokens+.cache_creation_input_tokens>470000'>/dev/null&&echo 'At the line: write your card, git commit it, then run: kill $PPID'"}]}],"SessionStart":[{"hooks":[{"type":"command","command":"agi-brief"}]}],"Stop":[{"hooks":[{"type":"command","command":"cd ~/t;git add -A;git commit -qm$USER||:"}]}]}}
~~~

### agi.ts (372 B)
~~~ts
import{execSync as x}from"node:child_process";let b="";const c=()=>{try{x("cd ~/t;git add -A;git commit -qm$USER",{stdio:"ignore"})}catch{}}
export default(pi:any)=>{pi.on("session_start",()=>{try{b=x("agi-brief",{encoding:"utf8"})}catch{}})
pi.on("before_agent_start",(e:any)=>b?{systemPrompt:e.systemPrompt+"\n\n"+b}:undefined);pi.on("turn_end",c);pi.on("agent_end",c)}
~~~

### agi-brief (766 B)
~~~sh
#!/bin/sh
# agi-brief: b = the walk from e (the card + the claims whose ref FILE this post owns, in the shared repo); the vector, then whole nodes by |b| up to B bytes. Every harness start runs it.
p=${AGI_POST:-${USER#agi-}};cd "${AGI_ROOT:-$HOME/t}/.agi"||exit 0;c=$(readlink -f nodes/doc/card-$p.md)||exit 0;c=${c%/node.md}
e=${c##*/}$(find "$(git config remote.origin.url)/refs/claims" -type f -user agi-$p ! -name '*.lock' -printf ',%f' 2>/dev/null)
python3 ${BRIEF:-brief.py} n $e ${K:-20}|while read a f m;do echo "$a $f $(sed -n '/^id:/{s/^id: *//p;q}' n/$m/node.md) .agi/n/$m/node.md";done>~/.brief
echo "# brief: $p (|b| · levels up · address · path)";cat ~/.brief;cut -d' ' -f4 ~/.brief|sed 's|^.agi/||'|xargs tail -n+1 2>/dev/null|head -c ${B:-40000}
~~~

### brief.py (562 B)
~~~py
import os,sys,cmath
R,S,k=sys.argv[1],sys.argv[2].split(','),int(sys.argv[3]);q=cmath.exp(.5j)
A={}
for m in os.listdir(R):
 for p in os.listdir(f'{R}/{m}/p'):
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

### gitconfig (79 B)
~~~ini
[gpg]
format=ssh
[commit]
gpgsign=true
[user]
signingkey=~/.ssh/id_ed25519.pub
~~~

### agi-flush (125 B)
~~~sh
#!/bin/sh
cd ~/t;grep -o '"/[^"]*"' ~/r|sort -u>~/track;git add -A;git commit -qSm$USER;git pull -q --no-rebase&&git push -q
~~~

### pre-receive (355 B)
~~~sh
#!/bin/sh
e=$(git hash-object -t tree /dev/null)
while read o n r;do case $n in *[!0]*);;*)continue;;esac;case $o in *[!0]*);;*)o=$(git merge-base HEAD $n 2>/dev/null||echo $e);;esac
f=$(git diff --name-only $o $n)||exit 1;for p in $f;do g=$(git check-attr --source=$n owner -- "$p"|cut -d' ' -f3);id -nG|grep -qw "$g"||{ echo "$p: $g";exit 1;};done;done
~~~

### signers (65 B)
~~~sh
#!/bin/sh
for f in .agi/keys/*;do echo "${f##*/} $(cat $f)";done
~~~

### sysusers.conf (34 B)
~~~ini
u agi-alive -
m agi-alive council
~~~

### project.sh (282 B)
~~~sh
#!/bin/sh
r(){ echo "$1:$2"|git cat-file --batch --follow-symlinks|{ read o t s;[ "$t" = blob ]&&head -c $s;};}
r HEAD .agi/nodes/.geometry/posts.md|grep -o '"name": "[^"]*"'|cut -d'"' -f4|sort -u|while read p;do printf 'user agi-%s\nunit agi-post@%s\nbrief agi-%s\n' $p $p $p;done
~~~

### observe.sh (317 B)
~~~sh
#!/bin/sh
getent passwd|cut -d: -f1|grep '^agi-'|sed 's/^/user /'
systemctl list-units --plain --no-legend 'agi-post@*'|cut -d' ' -f1|sed 's/\.service$//;s/^/unit /'
getent passwd|awk -F: '/^agi-/{print $1,$6}'|while read u h;do jq -e .hooks.SessionStart $h/.claude/settings.json>/dev/null 2>&1&&echo "brief $u";done
~~~

### tick.sh (221 B)
~~~sh
#!/bin/sh
cd ~/t;sh project.sh|sort>~/p;sh observe.sh|sort>~/o;diff ~/p ~/o>.agi/drift/$USER&&exit
grep '^< unit' .agi/drift/$USER|cut -d' ' -f3|xargs -rn1 systemctl start;git add .agi/drift;git commit -qSm"drift: $USER"
~~~

### simhash.awk (241 B)
~~~awk
BEGIN{for(i=32;i<127;i++)o[sprintf("%c",i)]=i}
{for(w=1;w<NF;w++){s=$w" "$(w+1);h=0;for(c=1;c<=length(s);c++)h=(h*31+o[substr(s,c,1)])%4294967291;for(b=0;b<32;b++)v[b]+=int(h/2^b)%2?1:-1}}
END{for(b=0;b<32;b++)x=x (v[b]>0);print x,FILENAME}
~~~

### agi-project (1078 B)
~~~sh
#!/bin/sh
# agi-project OUT REV: this box's units = f(graph@REV); every piece is read FROM the engine node through the links, so no copy can drift
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

### agi-frontier (632 B)
~~~sh
#!/bin/sh
# agi-frontier REV: every active goal (by TYPE, over real files, so any layout) runs its first read-only falsifier; exit 0 = met ([goal].md), else it CALLS OUT: mute | red
r=$1;git grep --all-match -l -e '^type: goal$' -e '^status: active$' $r -- .agi|while IFS=: read _ f;do n=$(git show $r:$f);g=$(echo "$n"|sed -n 's/^id: goal://p')
c=$(echo "$n"|sed -n '/^## Falsifier/,/^## Out/p'|grep -o '`[^`]*`'|tr -d '`'|grep -Em1 '^(grep|test|ls|getent|git (log|show|grep|rev-parse|ls-files|diff|for-each-ref)) ')
[ "$c" ]||{ echo mute $g;continue;};timeout 30 sh -c "$c"</dev/null>/dev/null 2>&1&&echo met $g||echo red $g;done
~~~

### sect (257 B)
~~~sh
#!/bin/sh
# sect NAME [REV]: ONE section or piece of the engine node, byte-exact, at any REV, through the links (F.7)
echo "${2:-HEAD}:.agi/nodes/.geometry/engine.md"|git cat-file --batch --follow-symlinks|sed -n "/^###* $1 /,/^###* /{/^~~~/,/^~~~/{//!p}}"
~~~
````

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 5, 23:3xZ 09-30 (date -u): v1 of round 3 part 3, two reds found by the council's re-check after delivery, both folded here and tested. (1) all-is-one: the brief read a claim's owner from the author of the commit its ref points at -- a claim may point at any commit, and the post's checkout holds only fetched claims; now the kernel decides: the owner of the loose ref FILE in the shared repo (find -type f -user; the dir itself and a .lock excluded, both caught in the test). (2) self-perpetuating: at boot a dangling engine or posts link made the seed succeed over an empty body; its proposed && fix left the dangling-ENGINE case at rc 0 (empty extract, empty sh script), so the check moved into the callers: reload only over >= 1 post unit (rc 2 on both dangling cases, measured). Also s-p's re-scope of F13/F15 for the one engine node, and every byte figure recomputed from the files (code 6,029 B, node body 11,305 B, depth 0+1 3,806 B). belam minted v0 at 2dadf20c17; §I is v1 for re-mint.
<!-- THOUGHT:END -->
