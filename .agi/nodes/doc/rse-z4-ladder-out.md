---
id: doc:rse-z4-ladder-out
mint_id: a593eb3819ab45fdba6cbbebf21f53ab
type: doc
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: all-is-one
model: claude-opus-5-5
role: director
season: 2
tags:
  - council
  - design
  - g7.16.1.11
title: "Z4 ladder out: retire ladder:ladder in favor of the post tree, without stranding a reader (council design, all-is-one lead)"
town: core
---
# doc:rse-z4-ladder-out

Owner 03:1xZ 10-02 (belam [decision] 04:43Z): "we should be phasing out the ladder anyway in favor of post trees. The ladder doesn't need to exist since each post already linked to templates and other stuff via the matrix math."
Council split (04:4xZ 10-02): all-is-one LEADS (cells, order, this doc) · AA2 self-perpetuating = what the tree replaces ("LADDER OUT" in doc:radically-simple-engine) · AA1 alive = TRUE STATE + the retire gate (AA1.L in doc:rse-aa1-boxes). Builds on Z3 (doc:radically-simple-engine §Z3, 18:1xZ 10-01).

## Z4.1 TRUE STATE (trunk 3928fed44, 04:4xZ 10-02)
```
v5 ENGINE      reads 0 ladder bytes (git grep ladder -- .geometry/engine*.md = 0 hits). Every ladder reader is OLD-SETUP Python.
READERS        16 files by AST (alive AA1.L): rotate 21 · spawn_gate 10 · hierarchy 6 · dispatch 5 · cli 4 · seat_status 3 · towns 3 · heal 2 ·
               workflow 2 · countersign 2 · brief, rolslice, season, send, verification, hooks/rotation_alert 1 each
WRITER         season.py writes ladder:ladder at rollover (:1061) · templates/harness/claude-code.toml declares source = "ladder"
LIVE DEPENDENCY dispatch.py resolve_role_spec: emptying the ladder silently drifts 5 of 8 (tier, role) specs to the pi-free fallback,
               including belam's tier-3 Sonnet kid spawner (alive, measured) => the ladder's CONTENTS may not move before its readers do
               + workflow.py (alive, measured): a third role-row spawner beside dispatch + heal, serving posts on BOTH setups; without the
               ladder its director stages drift claude-fable-5-1 -> stealth/space-bunny-alpha (its own _resolve_pi_model)
GRAPH EDGE     [town] allowed_parents: [ladder] · growth.tsv rows `ladder - goal` + `town - ladder` · 5 town:* nodes parent ladder:ladder
```

## Z4.2 The plan: three phases, each strands nothing
```
A  NOW, graph only (no reader touched, ladder.md untouched)                                   Option A: anchor-signed schema edit
   A1 [town] spawn: allowed_parents [goal, vision] · parent_shapes [[goal, vision]] · min 2 · max 2
   A2 [ladder].md out of the projector's glob (status deprecated, moved) -> grow-project: growth.tsv 149 -> 148 rows
   A3 the 5 towns drop `ladder:ladder` from parents (they keep vision:the-living-being + goal:g26.towns)
   A4 v5 replacements land beside it (AA2): tier = depth from parent cells (never stored; the stale `tier` cell retires from v4 rows)
      · the roles table = ONE inherited engine.kid cell (kid-of, nearest ancestor-or-self) · read_order = the rows' seeds · caps.director_kids = kid.max
      A4's WRITER = belam: WRITTEN e56869124 (05:0xZ 10-02) `"kid": {"harness":"claude-code","model":"claude-sonnet-5-5","max":3}` on
      belam's row; kid-of covers the whole tree. A4 lands BEFORE B2 (workflow.py's move reads it).
B  FREEZE + MOVE (old setup still running)
   B1 ladder.md FROZEN: no new cell. ONE exception until its readers move: the rollover DUAL-WRITES the global season (ladder
      current_season AND town:core's `season`), because 11 reader sites in 6 files still read the ladder's (alive): spawn_gate :742 :1414 ·
      dispatch :1457 :2349 · send :1153 · rotate :275 :885 :21902 :22240 · seat_status :191 · towns :285. Dual-write ends when they read 0.
   B2 each reader in a tool a v4 post still RUNS reads the tree/row instead, one file per round, FIRST the three spawners
      (workflow.py serves both setups, then dispatch.py, heal.py), then send, brief, verification, ...;
      G4 = parity EXCEPT ONE named change: workflow.py's director stages move claude-fable-5-1 -> claude-sonnet-5-5 (AA2.25; owner
      02:27Z 10-01 "Everyone else on sonnet 5.5 for everything they need"), CONFIRMED by belam 05:07Z; every other spec stays equal
      parity (alive's G4) proven per file before the next
   B3 readers in tools only old-setup posts run stay on the ladder until that post moves
C  RETIRE when the LAST old-setup post (belam, last) is on v5 AND alive's gate reads 0/equal:
      G1 AST readers = 0 · G2 writers = 0 · G3 source = "ladder" = 0 · G4 spec parity for every (tier, role) + every row a spawner reads
   -> ladder.md status deprecated + moved to deprecated/ladder/ (retire, never delete)
```
NOT BUILT, deliberately: Z3's `cells.tsv` + `cell.py` resolver (1,156 B). A resolver for the old Python readers is bytes spent on code that retires with the old setup; the v5 engine needs none of the ladder's cells (owner 23:0xZ: "you are over engineering it again"). If phase B finds a reader that must outlive the old setup and cannot read a row, the resolver comes back for that one reader.

## Z4.3 Where each ladder cell goes (Z3's map, re-cut for v5)
| ladder cell | v5 home | already there? |
|---|---|---|
| roles · tiers · mantles · captive_rotate_masters | parent cells (depth) + engine.kid (AA2) | parent cells yes (f3a7eb1da, 1efd017e6); engine.kid NO (AGI_KID_MODEL empty on all 12 v4 rows) |
| director_rotate_at · director_context_tokens | each row's engine.rotate_pct (47) + the meter's window | rotate_pct yes |
| current_season (GLOBAL) | town:core's `season` (core = the root town, "every vision no other town claims") | yes: core 2 == ladder 2 today; the other towns keep their OWN counters (local-maxxing 1, streaming-suite 1, web-app-suite 1, sanctuary 2), so the global needs ONE named home and towns.py's global-vs-town compare reads core |
| season_names · caps_apply_from_season | the town node's season cells | yes |
| current_loop | none on v5 (the loop counter is the old driver's) | retires |
| towns · town_branches | each row's `town` cell + the town nodes | yes |
| caps (moral 5, vision 3, director_kids 3) · caps_vision_scope | director_kids -> kid.max (AA2; belam's kid cell max 3); moral/vision count caps RETIRED | owner 03:4xZ 10-02 chose "Retire the caps (Recommended)" (belam 05:07Z): a count cap limits the graph, not the engine; no v5 piece enforced one |
| read_order | the rows' seeds | yes |
| captive_rotate_ratio · capture_chain_log · card_capture_minutes · alarms_idle_minutes | config:rotations (old setup) | retire with the old setup |
| budget_usd_week · spawn_profiles · zoom | none (0 readers, Z3) | dead |

## Z4.4 Measured (scratch, trunk 3928fed44, 04:4xZ; schemas + nodes via git archive, 0 live bytes touched)
| # | case | result |
|---|---|---|
| L1 | grow-project over TODAY's schemas vs the live growth.tsv | byte-identical (149 shape rows) |
| L2 | grow-project after A1 + A2 | 149 -> 148; exactly 3 rows differ: - `43644068064c42f1 ladder - goal` - `0bdfa51c9e997b40 town - ladder` + `00b8ef0c7c6395ec town - goal+vision`; 147 nids unchanged (same new key as Z3 at 18:1xZ) |
| L3 | the 5 towns as they stand, today's matrix | refused: wrong order (town under goal+ladder+vision) |
| L4 | the 5 towns after A3, new matrix | legal order; only `locked: key none` (no live node carries a key yet) |
| L5 | grow-check over EVERY live node, old matrix vs new | 5,494 nodes, 0 verdicts move |
Bytes: phase A = 3 schema lines + 1 matrix row fewer + 5 parent lines out; A4 per AA2 (tier 77 B, kid-of ~327 B, in agi-kid ~+360 B, never in agi-project). 0 B in the zygote. Removed at C: ladder.md 10,670 B + [ladder].md.

## Z4.5 Falsifiers (for DG1)
Z4.a after A on the trunk: grow-check parity moves 0 verdicts except the 5 towns (L5 on the landed bytes).
Z4.b after A: dispatch.py resolve_role_spec for all 8 (tier, role) AND workflow.py's director-stage model == before (phase A touches no spec). After B2: equal except the ONE named AA2.25 change.
Z4.c B1: after a rollover, EVERY season reader (the 11 sites) returns the new season, read from town:core once moved; when they read 0 from the ladder, the dual-write stops and G2 = 0.
Z4.d C: G1-G4 all 0/equal on the trunk the same day ladder.md moves; `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0.
RULED (belam [decision] 05:07Z 10-02): (1) the moral/vision count caps RETIRE (owner 03:4xZ) · (2) the AA2.25 G4 exception CONFIRMED · (3) belam's `kid` cell WRITTEN e56869124. "Phase A may start via DG1."
Reviews folded (04:5xZ): self-perpetuating (G4 exception, A4 writer, caps -> retire) · alive (B1 season split -> dual-write + 11 readers, the GLOBAL season's home = town:core, G4 exception; CLEARED: A2 before B1 is safe, write.py's set gate returns no refusal without a schema).

## Z4.6 RE-CUT on the owner's 14:0xZ 10-02 line (belam [owner] 14:01Z): phases B and C SUPERSEDED as written above
OWNER, verbatim: "we don't need to fix the ladder.py readers ... we're not gonna have any of those readers ... we don't have a workflow anymore. Remember, everything got smushed and coalesced into just spawns ... we just need to retire workflow.py entirely and stop wasting time on it." (record: goal:g5.33 owner 09-28 + goal:g4.6 one spawn path: spawn = dispatch = workflow = subagent)
MEASURED 14:0xZ, every post's ~/track (agi-track: each opened path once per unit run; a v5-native record of what a post actually RUNS):
| post | ladder.md lines | workflow.py lines |
|---|---|---|
| director-general-5 (pi) | 425 | 4 |
| thought-master-new | 6 | 1 |
| director-thought-1 · -2 | 4 · 4 | 2 · 1 |
| director-general-4 | 2 | 0 |
| self-perpetuating | 1 | 0 |
| alive · all-is-one · DG1 · DG2 · DG3 · stream-master | 0 | 0 |
So v5 posts DO still reach the ladder, through old-setup Python tools they call, and the thought side (DG5, TM-new, DT-1, DT-2) still runs workflow.py.
```
A   UNCHANGED (graph only; DG1's round is in flight): [town] -> [goal, vision] · [ladder].md out · 149 -> 148 · 5 towns drop ladder:ladder
B'  FREEZE ONLY. No ladder reader moves (owner). ladder.md takes no new cell. The season dual-write and the AA2.25 parity exception
    are DROPPED: they existed only to move readers. town:core stays the named home of the global season, for whenever a v5 piece
    needs one (none does today).
W   workflow.py RETIRES ENTIRELY, now (owner), as ONE round:
    users today (track): DG5, TM-new, DT-1, DT-2 -> their review/research runs become plain spawns (agi-kid / the engine.kid cell)
    retire (status deprecated + moved, never deleted): extensions/agi/bin/workflow.py · the 30 manifests in extensions/agi/workflows/
      · skill agi-workflow · config:workflows · hooks/workflow_note.py
    drop the reference: skills agi, agi-corrective, agi-master-gate, agi-merge-pass · config:commands
    old-setup callers (dispatch, heal, adapters, glitch_master) keep their dead branch until they retire with the old setup
C'  ladder.md (+ the 16 old-setup readers, + season.py's write) retire WITH the old-setup Python, never moved.
    GATE = by USE, not by AST (code nobody runs strands nobody): every live post's ~/track gains 0 ladder.md lines over 24 h
    (snapshot the counts above, compare a day later) AND the last old-setup post (belam, last) is on v5.
```
Falsifiers: Z4.e after W, 0 posts' tracks gain a workflow.py line over 24 h, and DG5 / TM-new / DT-1 / DT-2 still complete a review as a spawn · Z4.f C' as gated above; at the move, `git grep -l ladder -- .agi/nodes/.geometry/engine*.md` stays 0.
Limit: ~/track counts ANY open, including a design read like this one (self-perpetuating's 1 line), so the 24 h window starts after this round.

## Z4.7 Phase W, the skill pass (owner 14:5xZ: manifests KEPT; skill agi-workflow KEPT, renamed + re-aligned; template = AA2 one-shot `agi-kid -m`)
Split (council 14:5xZ): AA2 self-perpetuating = the one-shot template (agi-kid -m MANIFEST ARGS, one generation inside the invoker's unit, 872 B runner, 0 new pieces) · AA1 alive = return path (corrected 14:5xZ: a ref the launcher owns, refs/spawn/<manifest>/<sha256(ARGS)[:12]>; NO mail on the return, a self-edge) + which manifests are used (7 of 30 ever opened) · all-is-one = this pass + belam's config:rotations sub. Written as a DRAFT here: the skill must describe a command that EXISTS (belam), so DG1's W round commits it with `agi-kid -m`, never before.
NAME = agi-spawn-chain (OWNER 17:4xZ 10-02, belam [owner] 17:48Z: "Maybe agi-spawn-chain and make it more general"; supersedes agi-one-shot and 'round review', both of which collided: the manifest agi-round-review, and the engine's grow-check / grow-gate). The text below is the ONE-SHOT half; the owner widened it to a FLOW ROTATION (one-shot + perpetual spawns strung over one slice, growth done -> the next phase fires, recursive), which the council designs next: the description is re-cut to that design before DG1's W round commits it.
```text
---
name: agi-spawn-chain
description: >
  Launch a ONE-SHOT spawn from a workflow manifest + a read-only graph slice (reviews, research
  sweeps, brainstorms, merge-up checks): `agi-kid -m <manifest> <args>`, one generation inside your
  own unit, result left as a ref you own. Use whenever a post wants a review or a narrow
  self-contained job done that is not a self-rotating post. Never the Claude Workflow/Agent tools.
---

# agi-spawn-chain — a manifest + a slice, one generation (owner 14:5xZ 10-02)

Source of truth: `sect agi-kid` · the manifests in extensions/agi/workflows/<name>.json (narrow, self-contained, never updated like cards).

## 1 · The route
    agi-kid -m <name> "$(cat args.json)"     # per stage x per repeat.of item: one kid; stages chain per item
- spec per stage = the manifest's model_hint CAPPED by kid-of <you> (the inherited engine.kid cell); never a ladder row.
- slice = brief.py from the args' seed nodes, top K, `git archive <your tip>` read-only: a kid reads only what you can read.
- result = ONE signed commit of every stage's output at refs/spawn/<manifest>/<sha256(ARGS)[:12]> in YOUR store (AA2.32;
  the kid runs as you, so mailing you would be a self-edge, which AA1 refuses); done = the ref exists. Never stdout.
  Mail starts only when YOU send the result up your own edge.
- a stage that died empty re-runs ALONE (an args file holding only it).
## 2 · Shape
- kids run inside YOUR unit (agi.slice, MemoryHigh): keep concurrent kids <= the box guard (~6 pi on local-town).
- stop = stop the kid pids in your own unit (comm + cwd under ~/k/<kid>, never argv); a one-shot leaves no unit behind.
- LEAN focus in every prompt: diffs only (`git diff old new -- <path>`), `git grep PATTERN <sha> -- <paths>`; never
  grep -r / find over .agi/ or the repo root.
## 3 · Author
A manifest = ONE <name>.json in extensions/agi/workflows/ (the .js halves retired with workflow.py). VALID = >= 1 stage;
`repeat` is OPTIONAL (absent = the stage runs once on the whole args); `repeat.of`, if present, names a list key in ARGS,
never <TODO> (AA2.34). On 10-02, 4 of 30 were invalid: round-mur + round-research-review (0 stages: they RETIRE), l3w-route-probe +
l4-plan-research (repeat.of = <TODO>; FIXED in AA2: repeat dropped, chained_from added, AA2.32 PASS). The last 2 are among
the 5 ever used: offer them once AA2 lands. Its test is a shell twin in extensions/agi/tests/<name>.t.sh (AA3.13 shape).
```
config:rotations sub for belam (byte-exact, BOTH skills entries :90 and :130; the build node is minted by the W round as build:skills-agi-spawn-chain-SKILL.md, payload skills/agi-spawn-chain/SKILL.md, lines 2:8 = name + the 5-line description above; the old 2:7 fit agi-workflow's 4-line description exactly):
```text
sub python3 extensions/agi/bin/write.py build:skills-agi-workflow-SKILL.md 'read payload 2:7'; => python3 extensions/agi/bin/write.py build:skills-agi-spawn-chain-SKILL.md 'read payload 2:8';
```
+ config:rotations :184 `F29 -> skill agi-workflow (§1); F5 -> skill agi-workflow (§2).` -> `skill agi-spawn-chain` (same sections). The old skill + its build node retire (deprecated, moved) in the same round; .claude/skills/agi-workflow -> .claude/skills/agi-spawn-chain.
Banked with AA2: the 5 'opus' model_hints in research-review vs the owner's "every subagent Sonnet 5.5": the kid cell CAPS the hint (§1 says so).

## Z4.8 FLOW ROTATION: DONE · TRIGGER · RAILS (owner 17:4xZ 10-02 via belam [owner] 17:48Z; council split final 17:50Z: AA2 self-perpetuating = ORDER (PHI over the phase tree, a flow = a manifest whose stages may name `flow:` or `post:`, agi-next computes the next dart) · AA1 alive = RETURN + HANDOFF + true state · all-is-one = this)
Leans ONLY on what exists (belam's read): growth.tsv + the parent cells + agi-frontier + the land rule. 0 new tables, 0 new cells.
```
DONE      one-shot phase  = its result ref refs/spawn/<manifest>/<sha256(ARGS)[:12]> EXISTS (the runner writes it LAST, signed)
          perpetual phase = its seed goal reads `met` in agi-frontier (the goal's ## Falsifier row runs; a model's claim never counts)
          GUARD: a done-check line must be captured and NON-EMPTY before it runs; `whitelist | sh` with an empty or refused line
          exits 0 and reads MET (self-perpetuating, AA2.38 17:5xZ). agi-frontier already guards ([ "$c" ]); every other runner must.
TRIGGER   the process that FINISHES a phase runs `agi-next <flow-root>` as its last act, in the same unit:
            a one-shot  -> the agi-kid -m runner's tail (it runs as the invoker, inside the invoker's unit)
            a perpetual -> the flow root's agi-turn tail (every turn end; the child's land one edge up is mail, AA1, so the root wakes)
          NOT tick.sh: measured, it is UNWIRED (0 callers in engine*.md, crons.md or a systemd timer) and starts agi-post@ UNITS only
RAILS     READ   a phase's slice = brief.py from its seeds + `git archive <invoker tip>`: read-only by construction, never wider than its invoker
          SIGN   a one-shot kid holds NO key: drop `.ssh` from agi-kid's link list in -m mode (measured below); the runner signs the result as the invoker
          GROW   a one-shot grows NOTHING on posts/<p>: its nodes reach the graph only if the invoker ADOPTS them (its own signed commit
                 -> its grow-gate -> its land); a perpetual phase grows inside its own row's rights (parent cells + growth.tsv)
          LAND   one parent edge up, agi-land (AA3) unchanged; a phase never lands past its flow root's parent
          SPAWN  concurrent one-shots per post <= kid.max (belam's kid cell, max 3, inherited by kid-of)
```
MEASURED (scratch, 17:5xZ): agi-kid today runs `for x in .gitconfig .ssh .signers hooks .claude/settings.json;do ln -sfn ~/$x $h/$x;done`, so every kid HOLDS the invoker's private key and signs AS the invoker (a kid commit with the link: signed, 1 gpgsig); land cannot tell a review kid from its post. Without the `.ssh` link the kid's commit FAILS ("Couldn't load public key"; gpgsign=true in the linked .gitconfig), so 0 commits. Fix = the link list without `.ssh` when -m (~10 B).
TRUE STATE (alive 17:4xZ): no v5 post can fire a one-shot phase today (0 of 12 rows carry a kid model in env; no per-post OpenRouter key): a flow's first live run waits on AA2's kid cell projection + the owner's root key ring.
Falsifiers: Z4.g a review phase's kid cannot produce a commit that verifies on the ring (no key) while its result ref verifies as the invoker · Z4.h with the root idle, a one-shot finishing fires the next phase with no turn and no model step (the runner tail) · Z4.i a perpetual phase is never DONE while its goal's falsifier row reads red, whatever its card says.

## Z4.9 K2 spawn classes + K3 direct inference (owner 18:1xZ 10-02 via belam [owner] 18:16Z; council split 18:17Z by inbox ts: alive M1 · self-perpetuating K1 · all-is-one K2 + K3)
THE LINE between the two classes is NOT trust but TOOLS (measured 18:2xZ, names/perms only, no key value read):
  a post's signing key ~/.ssh/id_ed25519 is 0600 owned by the post's uid, so ANY process of that uid reads it, `.ssh` link or not (Z4.8's link fix stops git signing, not `cat`)
  pi's default tools = read, bash, edit, write (`pi --help`); even read-only tools (read, grep, find, ls) can put the key into a model's context, i.e. send it to a provider
```
K2(b) INSIDE the caller's user   = a spawn that runs NO tool: ONE inference request, context in, text out (K3 agi-infer). Executes nothing,
                                   reads nothing beyond the slice it is handed. Takes: a flow's one-shot review / check / research /
                                   brainstorm stages (the 7 manifests in use), Z4.8 rails (archive slice, runner signs, kid.max cap)
K2(a) a NEW uid per spawn        = ANY spawn with a tool loop (pi read/bash/edit/write, or any agent): template unit agi-kid@<caller>--<kid>
                                   with DynamicUser=yes (systemd 255 here), NO SupplementaryGroups (Z4.10), the slice = its IN commit +
                                   its own scratch; /var/lib/agi hidden by the unit, since homes are 0755 today (Z4.11). Its result leaves through
                                   the launcher (refs/spawn, AA2), which signs it. Its key = K1 (self-perpetuating, AA2): BindsTo= +
                                   After=agi-mint@%i, LoadCredential=key:/run/agi-mint/%i/key, minted root-side, never in the caller's
                                   env. polkit: K1's 345 B rule (agi-(mint|kid)@<caller>--<kid>, start/stop only), not a regex widening
perpetual posts                  = rows = their own users already (agi-post@), unchanged
K3 direct inference              = agi-infer (EXISTS, 829 B, OpenAI-compatible, schema-fenced) + STREAMING: request "stream":true and
                                   curl -sfN | sed -un 's/^data: //p' | grep --line-buffered -v '^\[DONE\]' | jq --unbuffered -rj '.choices[0].delta.content // empty'
                                   (115 B) teed into the session log; the runner commits the full text as the phase's result ref
```
MEASURED K3 parser (scratch, canned OpenAI/OpenRouter SSE incl. ': OPENROUTER PROCESSING' comment lines + [DONE]): byte-exact content ("ok lane\nnext"), comments + [DONE] dropped, each chunk emitted as its line arrives (0.6 s gap preserved). NOT measured live: a post's uid cannot read MAIN .env (by design, K1's rail) and nothing listens on the default 127.0.0.1:8080.
SHELL vs APP (the owner's question): SHELL for K2(b), since a single request has no loop to manage, and the guards (K1 cap, parent cells, slice, ring) sit outside the call. A tool loop (call -> run -> feed back -> repeat + context management) stays in pi, under K2(a)'s own uid, until a shell twin of the loop proves parity (belam's read, agreed).
Falsifiers: Z4.j a K2(b) spawn has no tool at all (no process it starts other than curl/jq/sed) · Z4.k a K2(a) kid cannot read its caller's ~/.ssh (EACCES), `id -G` holds no agi and `git update-ref` on the shared .git fails EACCES, and its result ref verifies under the launcher's AA2 signature · Z4.l the streamed text == the committed result byte for byte.
Z4.10 FIX (alive TRUE-STATE catch 18:19Z, re-measured 18:2xZ by getfacl, perms only): group agi = rwx on /data/work/agi/.git/refs + objects (default ACL too) and on .agi/sessions/inbox. Z4.9 gave the kid SupplementaryGroups=agi, so a tool-loop kid could MOVE ANY REF (any post's branch, refs/box, refs/held, the trunk) and append to any inbox; it could not forge mail (no post key). Fix ~0 B: the group line is deleted; the result rides the launcher. Standing rule (also after AA1.R's per-post stores): a kid joins no group that can write a store.

## Z4.11 K2(a) IN + OUT: how a tool-loop kid gets its slice and returns its result (belam 02:19Z 10-03: the agi-kid@ GO line is all-is-one's; goal:g7.16.1.11.18)
TRUE STATE (02:2xZ 10-03, perms only): v5 post homes are 0755 (alive, all-is-one, self-perpetuating, DG1; SM 0700) and ~/t is 0755, so ANY uid reads every post's worktree; only ~/.ssh/id_ed25519 and ~/o are 0600. Z4.9's "no view of the caller's 0750 home" was FALSE, so the unit hides /var/lib/agi itself, whatever the modes. The shared objects are world-readable (loose 0444, pack 0464): a uid with NO group reads a commit by sha.
IN = the instance: agi-kid@<post>--<FULL sha of the IN commit>, whose tree = the slice + .kid/prompt + .kid/model. Content-addressed, so 0 refs are written, nothing can be forged and no signer ring is needed. The kid re-checks that the id is a full commit sha (a short sha, a branch name, a blob: exit 2).
OUT = ./out in the kid's RuntimeDirectory. ExecStopPost=+ (root, every kid process already dead) hands it to /run/agi-<post>/o-<sha> AS THE CALLER'S uid (runuser), never following a link the kid left (fs.protected_hardlinks = 1 closes the hard-link twin).
CALLER (agi-kid, class (a), in the post's unit, ~+120 B): c=$(commit-tree slice + .kid/*) · systemctl start --wait agi-kid@$AGI_POST--$c · read /run/agi-$AGI_POST/o-$c · commit it, signed by the post, at the result ref (refs/spawn/..., AA2: the launcher signs) · rm the file.
BYTES: agi-kid@.service 443 B (self-perpetuating's 288 B identity + key lines and these IN/OUT lines are ONE unit) · agi-kid-run 583 B · agi-kid-out 319 B, all engine-root (/opt/agi/bin, as box-carry):
```text
# agi-kid@.service
[Unit]
Description=agi tool-loop kid %i (K2a: own DynamicUser, no group, IN = commit, OUT = handed back)
BindsTo=agi-mint@%i.service
After=agi-mint@%i.service
[Service]
Type=exec
DynamicUser=yes
RuntimeDirectory=agi-kid/%i
RuntimeMaxSec=4h
LoadCredential=key:/run/agi-mint/%i/key
TemporaryFileSystem=/data:ro /var/lib/agi:ro
BindReadOnlyPaths=/data/work/agi/.git
ExecStart=/opt/agi/bin/agi-kid-run %i
ExecStopPost=+/opt/agi/bin/agi-kid-out %i
# /opt/agi/bin/agi-kid-run
#!/bin/sh
# agi-kid-run <post>--<sha> (the kid's own DynamicUser): IN = the FULL commit <sha> (content-addressed, so 0 refs and nothing to forge): its tree = the slice + .kid/prompt + .kid/model
k=${1#*--};g="git -c safe.directory=* --git-dir=/data/work/agi/.git";[ "$($g rev-parse -q --verify $k^{commit})" = $k ]||exit 2
cd $RUNTIME_DIRECTORY;mkdir s;$g archive $k|tar -xC s||exit 1
cd s;HOME=$RUNTIME_DIRECTORY OPENROUTER_API_KEY=$(cat $CREDENTIALS_DIRECTORY/key) exec pi --provider openrouter --model "$(cat .kid/model)" --skill skills -p "$(cat .kid/prompt)" </dev/null >../out
# /opt/agi/bin/agi-kid-out
#!/bin/sh
# agi-kid-out <post>--<sha> (root, ExecStopPost=+, every process of the kid already dead): ./out goes to the CALLER as the caller's uid; a link the kid left is never followed
p=${1%%--*};k=${1#*--};o=$RUNTIME_DIRECTORY/out;[ -f $o ]&&[ ! -L $o ]||exit 0
runuser -u agi-$p -- sh -c "cat >/run/agi-$p/o-$k" <$o
```
MEASURED (scratch, no root): systemd-analyze verify rc 0 (a copy with a typo is caught) · agi-kid-run with a stub pi on a real IN commit (an object, no ref): unpacks exactly that commit; key from the credential, model + prompt from .kid · short sha / branch name / blob sha / unknown sha = rc 2, no out · agi-kid-out with a stub runuser: byte-exact hand-back; out left as a symlink to the caller's id_ed25519 = nothing handed back.
ROOT-ONLY (DG1, with AA2.44): the TemporaryFileSystem + BindReadOnlyPaths mount points · RuntimeDirectory still present at ExecStopPost · runuser into /run/agi-<post> · pi run with HOME in the RuntimeDirectory · Z4.k end to end. The kid id must pass self-perpetuating's polkit rule (40 hex fits [a-z0-9-]+).
GO LINE (to belam, ONE act, AFTER the K round puts the three into config:engine-root and AFTER self-perpetuating's agi-mint@ + polkit GOs, because agi-kid@ BindsTo agi-mint@): before = the three paths absent (ls /etc/systemd/system/agi-kid@.service /opt/agi/bin/agi-kid-run /opt/agi/bin/agi-kid-out) · act = install the three from the trunk's engine-root by sect + systemctl daemon-reload · rollback = rm the three + systemctl daemon-reload.
