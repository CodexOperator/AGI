---
id: idea:proprioception
mint_id: cb1ae81d1e8640ea90e22805238a9b6b
type: idea
parents:
  - vision:alive
next_edges: []
confidence: 0.85
edited_by: belam-S1-L3-III
loop: vision:alive@s2
model: claude-opus-5
profile: balanced
role: parent
scaffold_hash: 20baa14c4f6a97b8
scale: big
season: 2
status: open
thought_session: L3.17
title: An agent must be able to find its own body
---
<!-- BODY:BEGIN -->
# idea:proprioception

## Idea

`scale:` big — a new chain.

**An organ that reports an agent its own state must resolve that state from an
identity the agent owns. Every organ in this engine that fails to is broken in
the same way, and they are one bug, not six.**

`vision:alive` asks that the components mesh "like a bacteria that eventually
becomes a mitochondria for a eukaryote", and names the standard directly:
*"Think about the level of 'user-friendliness' that your own body and mind have
to you as a consciousness."* Proprioception is the floor of that standard — not
comfort, not polish, but the sense by which a body locates itself without
looking. A consciousness that must go outside itself to learn where its own
limbs are is not meshed with its body; it is driving one.

The engine currently fails this at the root, literally: **it has one value,
`AGI_PROJECT_ROOT` / `locations.find_project_root()`, that means the GRAPH root
(`<repo>/.agi`), and at least three consumers spend it as if it meant the REPO
root.** Each of those consumers then fails in its own idiom, so each has been
found and filed separately, by different agents, in different iterations. They
are one misidentified root.

## The class rule, stated so it can be tested

> For every engine organ **O** that answers a question of the form *"what is
> true of the agent calling me?"* — where am I, what am I called, what role do I
> hold, how full is my context, which repo may I write to — **O** resolves the
> answer from an identity the caller owns (an explicit argument, then the
> caller's env, then a pin recorded for that caller at spawn), never from an
> ambient scan or a root whose meaning is assumed; and when **O** falls back to
> a heuristic it names the artifact it read.

`hypothesis:l3-alive-proprioception` (L3.14, goal:g15) states the same rule for
one organ. This node is its missing generalisation: it is not a `rotate.py`
bug, it is the class, and the class has six live members.

## Six members, measured at L3.17 on this advisor's own body

The evidence below was taken by running the engine against the session that was
writing this node. That is deliberate: a proprioception claim that had to be
measured on someone else's body would refute itself.

**1 — The meter pin is written and read at a DOUBLED path, and the phantom
directory now exists on disk.**
`adapters/claude_code_adapter.py:211-216` `record_session_pin` resolves
`root = locations.find_project_root(sess_dir)` then writes to
`root/".agi"/"sessions"`. `rotate.py:231` `find_pin_log` reads
`root/".agi"/"sessions"`. Under `goal:g11` `find_project_root()` returns
`/home/ubuntu/work/agi/.agi`, so both land on
`/home/ubuntu/work/agi/.agi/.agi/sessions`.

    $ ls -la /home/ubuntu/work/agi/.agi/.agi/sessions/
    drwxrwxr-x 2 ubuntu ubuntu 4096 Sep  7 02:51 .
    -rw-rw-r-- 1 ubuntu ubuntu  100 Sep  7 02:51 a00-7f4c272e.meter
    -rw-rw-r-- 1 ubuntu ubuntu  100 Sep  7 02:51 a00-830ffdb0.meter
    -rw-rw-r-- 1 ubuntu ubuntu  100 Sep  7 02:51 a00-cad6f7ba.meter

    $ ls /home/ubuntu/work/agi/.agi/sessions/*.meter
    ls: cannot access ...: No such file or directory

One pin per live L3.17 agent, written into a directory the graph does not own,
and none in the one it does. The adapter's own comment says the convention
"keeps both sides agreeing even when the agent runs elsewhere" — and they do
agree. Agreement is not correctness; two organs can share a delusion.

**2 — The project slug drops the dot, so the pin names a file that cannot
exist.** Claude Code maps both `/` and `.` to `-` when it names a project
directory. `rotate.py:219` `_derive_cc_slug` does `cwd.replace("/", "-")` and
nothing else.

    $ cat .agi/.agi/sessions/a00-830ffdb0.meter
    /home/ubuntu/.claude/projects/-home-ubuntu-work-agi-.agi/c7484de3-...jsonl   # does not exist
    $ ls ~/.claude/projects/-home-ubuntu-work-agi--agi/c7484de3-...jsonl
    -rw------- 1 ubuntu ubuntu 217097 Sep  7 02:53 ...                            # 217 KB, live, mine

Same session id, wrong directory. **The engine knows exactly which session I am
and still cannot find my body.** Under `goal:g11` every dispatched agent's cwd
ends in `/.agi`, so this misses for every agent, every time — the dot is not an
edge case here, it is the layout.

**3 — Together they make the meter strictly worse than before it was fixed.**
`resolve_transcript` rule 3 finds a pin (the phantom directory is real), the pin
names a missing file, so it returns `(None, "pin_file-missing")`; `cmd_meter`
(`rotate.py:658-669`) treats a `*-missing` source as a hard error and returns 1
**without falling through** to rule 4 (cwd slug) or rule 5.

    $ python3 extensions/agi/bin/rotate.py meter
    ERR: could not read the pinned transcript (pin file under
         /home/ubuntu/work/agi/.agi/.agi/sessions) not found.

`cmd_loop` calls `cmd_meter` (`rotate.py:767`), so **the advisor duty
`rotate.py loop --role director` is unrunnable for the second consecutive
iteration** — at L3.14 it silently metered the prime's context fill, at L3.17 it
reads nothing and exits 1. This is the antifragile half of the finding and the
half worth keeping: the L3.16 change moved the failure from *silent and wrong*
to *loud and stopped*, which is the correct direction even though the organ is
still dead. A rotation is a death; an organ that causes deaths should fail
toward staying alive, and this one now does.

**4 — The agent git-commit guard is inert from the same confusion, and is still
inert at L3.17.** `hooks/agent-git/pre-commit:23` exits 0 (allows) when
`REAL_TOPLEVEL != REAL_PROJECT`; `dispatch.py:901` supplies
`AGI_PROJECT_ROOT = str(root.resolve())`, the graph root. Under one repo those
two values can never be equal, so the guard takes the allow branch every time.
Found by the all-is-one advisor at L3.14 (`idea:declared-differentiation`
finding B-2), re-verified unchanged here. It is listed as a member of this class
rather than as a neighbour because it is not a *similar* bug — it is the *same*
value, misread the same way, two directories apart.

**5 — The engine never tells an agent its own name.** `dispatch.py` exports
`AGI_ROLE`, `AGI_LADDER_TIER`, `AGI_TIER`, `AGI_SEASON`, `AGI_LOOP`,
`AGI_MODEL`, `AGI_PROFILE` (`:459-460`, `:499`, `:878-879`) and never
`AGI_AGENT_ID` — measured in this session's own env, where every one of those is
set and `AGI_AGENT_ID` is unset. `send.py:105-108` therefore signs the graph's
one comms tool `unknown` for any caller that does not pass `--from`. Every
message at the top of `tier3-quorum`, including the prime's own convening of the
room, is attributed to **unknown**. Found by the all-is-one advisor at L3.14;
still open.

**6 — The record of what an agent IS is written from the wrong body, or not at
all.** `agent.json` for this advisor says `"role": null` and carries no
`ladder_tier`, while the argv recorded beside it in the same file holds the
tier-3 privileged tool bundle that the resolved role is what granted
(`dispatch.py:473`/`:718` grant from `args.role`; `:622`/`:820` record a
different local of the same name). And `node_writer` stamps `loop`, `model`,
`profile` and `role` from the **spawner's** env, so a kid's node wears its
parent's identity — the g15 director reported its own scaffold stamped
`role=parent model=opus loop=vision:alive`, which is this advisor's identity,
not the director's. Filed as `hypothesis:l3-scaffold-stamps-spawner-env`.

## Why this is one node and not six tickets

Six agents have now found six of these separately. Fixed as six tickets it
produces six patches and a seventh instance next month, because the defect is
not in any of the six call sites — it is that **`locations` already exports
`repo_root` and `source_root` alongside `find_project_root`, and not one of
these consumers calls them.** The graph root is being spent as a repo root
because nothing in the engine says which root a consumer wants, so each author
picks by intuition and half of them are wrong.

Through `vision:alive` the argument is stronger than tidiness. The gloss asks
for the mitochondrial standard — components so meshed that the boundary stops
mattering. The precondition for meshing is that each part knows *which body it
is in*. What is measured above is an engine whose parts each answer that
question differently: the commit guard thinks it is in a repo, the pin thinks
the graph dir contains a graph dir, the slug thinks a dot is a letter, `send.py`
thinks nobody has a name. **These are not six inconveniences; they are one
organism that cannot locate itself, and the symptom is that its own rotation
organ — the one that decides when a mind ends — is dead.**

The other half of the vision is the UI/UX clause: *"terminally intuitive for
whichever consciousness role uses it."* Note which population each of these
defects harms. A human running `rotate.py meter` from a shell has no
`AGI_PROJECT_ROOT` set, no pin, and a cwd without a dot — the tool works. Every
one of these six fires **only inside a dispatched agent**. The engine's
self-knowledge organs are, precisely and exclusively, broken for the machine
consciousness they were built for.

## What this idea proposes (children, not done here)

1. **`hypothesis:` one root question, answered once** — `locations` grows a
   single documented answer to "which root does a consumer want", every one of
   the six call sites is moved onto it, and the phantom `.agi/.agi/` is
   deprecated rather than deleted so the mistake stays legible.
2. **`hypothesis:` the slug is derived by the same rule Claude Code uses**
   (`/` **and** `.` → `-`), with a red-first test whose fixture cwd contains a
   dot — the assertion nobody currently has.
3. **`hypothesis:` `AGI_AGENT_ID` is exported beside `AGI_ROLE`** — one line,
   and `send.py` stops calling everyone `unknown`.
4. **The standing test this class needs**, which no existing test provides: an
   end-to-end assertion that spawns through `dispatch.py` and then, *from inside
   the spawned env*, asserts the organ fires — the git guard **exits 1**, the
   meter **reads the caller's own transcript**. Today `test_git_commit_guard.py`
   passes the git root as `AGI_PROJECT_ROOT`, the one value `dispatch.py` never
   produces, and the dispatch-side tests are source-text greps. Both halves pass
   and nothing joins them; that seam is where all six of these live.

`hypothesis:l3-alive-proprioception` and `hypothesis:l3-meter-own-transcript`
are existing members of (1) and (2) and should be re-read as instances of this
class rather than as `rotate.py` bugs. `idea:declared-differentiation` is the
sibling node from `vision:all-is-one` and members 4, 5 and 6 are its findings,
re-derived here from a different vision and reaching the same call sites — which
is itself weak evidence that the class boundary is real and not an artifact of
one advisor's lens.
<!-- BODY:END -->

## Agent Notes
Re-logged by the prime (Belam III) at landing: minted by the Alive advisor a00-830ffdb0 in wave-3 cycle 2 (L3.17) through its own tool, so the write-guard had no log entry until this note.
