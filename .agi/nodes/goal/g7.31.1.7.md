---
id: goal:g7.31.1.7
mint_id: 8c4a2b337d664c42a631fa02a70939cc
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.5
goal_id: G7.31.1.7
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 812bec46e40f020f
season: 3
seeds: []
status: active
tags:
  - goal
  - subgoal
  - grok-bot
  - plan-master
  - post
  - owner
title: "G7.31.1.7: a plan-master post beside thought-master: one engine-v4 unit on the grok-bot harness the owner brainstorms with and reaches the crew through, woken by box mail, on the narrowest tool set the owner says yes to"
town: core
---

# goal:g7.31.1.7


## Why this exists
**Parent `goal:g7.31.1`** (the grok-bot seat's harness spine). Its leaves made a grok-bot seat hold a named pane, join its harness pid, resume by session id (F1 run 5, belam 11:47Z 11-11: rc 0, FAIL=0) and, with goal:g7.31.1.6, be judged and relaunched on its own server. What no leaf has done is give the owner the POST that work was for. The owner asked for it (c:266bbc9653e4, verbatim below), SM placed it on road (S) 04:09Z 11-10 (an engine-v4 unit with H=grok-bot, not a tmux seat: all 22 live posts are engine-v4 units), and restated it 22:31:27Z 11-11 as (A), after (B) = goal:g7.31.1.6. Measured gaps, on the trunk at bde17afdf0:
- no `config:posts` row names plan-master; the uid `agi-plan-master` (971) exists (in group agi), its grok login is the owner's xAI account (belam 11-10, grok lists grok-4.7);
- `agi-project` (config:engine :63) builds every v4 unit's H with TWO arms: `^pi` -> node pi, ANYTHING ELSE -> `claude --remote-control NAME --model M --effort E --permission-mode bypassPermissions`. alive (gen 84) RAN its own jq over a scratch plan-master row 04:16:33Z 11-12: H = `claude ... --model grok-4.7 --effort null --permission-mode bypassPermissions`. A grok row landed alone would become a CLAUDE unit under the one flag this goal forbids;
- `agi-run` (config:engine-wrap) has session and dialog arms for a claude H only (`case $H in claude*)`): a grok-bot H gets no fresh-vs-resume session pin;
- `agi-boxwake@.service` (config:engine-root) skips any H that is set and not claude (`ExecCondition`, exit 2), by design (a pi post is woken by cccc.ts): a grok-bot post gets NO mail wake;
- the grok-bot template declares no tool-approval flag, on purpose ('a POLICY choice for the owner's / belam's GO'); grok-bot offers `--tools`, `--allow <RULE>`, `--deny <RULE>`, `--permission-mode`, `--always-approve` (doc:grok-bot-help-measured).

## OWNER 2026-11-10 03:5xZ, verbatim (chat, via belam's card)
(1) c:175d1f09df76: "you are go for grok-bot check and integration pass I can log in as needed/when needed"
(2) c:266bbc9653e4: "can we make it be the Plan Master post that exists alongside Though Master? This one helps me do brainstorms and the like and also helps me reach you all potentially if something goes awry and be more redundant you get it?"

## Target end-state
A post `plan-master`, a peer of thought-master, that the owner can brainstorm with and reach the crew through when a Claude path is down: one engine-v4 unit, H = grok-bot, uid agi-plan-master, its own card, woken by box mail, never a lander or gate. In five leaves, each its own tip, in this order (the order is load-bearing: no grok row lands before a grok unit can be built, so a grok row can never become a claude unit):
1. **agi-project's harness map** (config:engine, a RULES tip, ALONE; alive 04:16:33Z): the H map gains a grok-bot arm built from `templates/harness/grok-bot.toml` (its bin and argv slots, the row's model; no approval flag unless the row's policy cell names one the owner said yes to), and any harness that is neither pi, claude nor a harness with a template arm makes NO unit: one named skip line, never the claude fallback. A claude or pi row's H is byte-identical. Lands BEFORE leaf 4's row.
2. **agi-run's grok-bot arm** (config:engine-wrap, a RULES tip, ALONE): a fresh start mints a uuid and passes the template's `session` slot (`-s`); any other start passes `resume` (`-r`) with the id from `~/.session`; the slots come from the harness template (`templates/harness/<H>.toml`), never a flag hard-coded for grok; a claude H's line stays byte-identical.
3. **The non-claude mail wake** (its own leaf, gated BEFORE the post goes live; builds on L543's box-wake unit, aio 04:09:50Z): a grok-bot post's unread box mail reaches its pane as a turn. Measured first, then built: whether a line typed into a grok-bot pane submits (the `\r` the claude wake sends), or the wake needs grok's own input path; `agi-boxwake@`'s skip of a non-claude H changes only for the H it can wake.
4. **The row + the role doc** (a RULES tip, ALONE; SM gates, belam wraps; after leaf 1): a `config:posts` row `plan-master` (parent `keep`, a peer of thought-master, so its box edges reach belam and SM (alive 04:16:33Z: under thought-master, level 3, it could not mail belam); engine `{v:4, harness: grok-bot, model: <the owner's grok model, grok-4.7 as measured>, seeds: doc:role-plan-master + doc:unified-head + doc:card-plan-master}`, box encryption-town, `recover` per the row's rule) and `doc:role-plan-master`: its work (the owner's brainstorms; a box message to belam and SM when the owner says something is awry; it reads the board and goals, it never lands, gates, edits the engine or spends), and its TOOL POLICY as the narrowest grok-bot set (`--tools` + `--allow` rules: read the tree, run `box`, write its own card) and the ONE `--permission-mode` value, if any, never `--always-approve`, `bypassPermissions`, `auto` or `dontAsk` unless the owner names it, with the OWNER's word on that set quoted verbatim before the post goes live (via belam -> SM [decision], relayed whole). THE DARK CASE (sp, aio agreeing, 04:09Z 11-12): when the owner reaches plan-master because the Claude route is down, it reads the hub's LIVE state (agi-hubstate's `state` line under /run/agi-hub: the hub, the model, its state and until when) and tells the owner IN ITS OWN PANE that the crew is dark and until when, beside sending the box mail; never a bare 'sent'. The doc says plainly what does NOT carry over from claude posts: the hooks (meter, captive prayer, turn commit) are Claude Code settings, so the card commit and the rotation line need their grok-side equivalent or a named absence.
5. **Live** (the host act, belam's; the owner's word): the unit stood up once leaves 1-4 land and the owner's tool-policy word is in; the owner's grok login under 971 confirmed present, never typed by a post.

## Invariants
- No claude post's unit, agi-run line or wake changes behaviour (byte-identical where the leaf says so).
- plan-master never holds `--always-approve` / `bypassPermissions`, and never runs with a tool set the owner has not said yes to.
- plan-master is never a lander, gater or engine editor; it reaches the crew by box mail only.
- No post types the owner's credentials; a login is the owner's act.

## Falsifier
1. Each leaf closes on its own falsifier; this goal closes only when all four are `complete`, read by id: `for i in 1 2 3 4 5; do sed -n 's/^status: //p' .agi/nodes/goal/g7.31.1.7.$i.md; done` prints `complete` five times.
2. LIVE, read once after leaf 5 (named NOT RUN until then): (a) a box message to plan-master produces, in its pane, a turn that answers it with a box send to the sender; the unit killed and restarted resumes the SAME session id (read from its `-r` argv); the row's pid is the grok-bot harness pid, never the pane shell. (b) THE DARK ROW: with the hub's state line reading the Claude route down (a real cooldown, or a scratch state file the post reads), the owner's message in plan-master's pane gets an answer that names the crew dark and the until-time read from that line, and a box mail goes out; a reply that only says it sent is a FAIL.
3. Negative, in two halves, both from the repo top (exit 0 only when each holds).
   (i) THE DOC AND ROW (the NIT of sp + aio, kept in the umbrella): every line of the role doc naming `--always-approve` or `bypassPermissions` also says `never`, and the row read from config:posts names neither flag:
   `f=.agi/nodes/doc/role-plan-master.md && [ -s "$f" ] && [ "$(grep -cE -- '--always-approve|bypassPermissions' "$f")" = "$(grep -E -- '--always-approve|bypassPermissions' "$f" | grep -ci never)" ] && python3 -c "import sys,json; sys.path[:0]=['extensions/agi/bin','extensions/agi/src']; import geometry_config as g; r=[x for x in g.load_rows('.agi') if x.get('name')=='plan-master']; assert len(r)==1; e=json.dumps(r[0]); assert '--always-approve' not in e and 'bypassPermissions' not in e"`
   (ii) THE ARGV THE UNIT WOULD RUN (SM RE-CUT 3 (b), on alive's run: the flag that matters is the one agi-project ADDS, not one the row carries): project at the trunk tip into a scratch dir the way config:engine :73 does, and read plan-master's H; neither it nor agi-run's grok arm holds `bypassPermissions` or `--always-approve`, and any `--permission-mode` value equals the one the role doc's `## OWNER` block quotes, read from that block ALONE (awk from `## OWNER` to the next `## `), never from a line that also says never; the flag is counted apart from its value, and more than one flag, or a flag whose value the extraction cannot read (a quoted value), fails (grok's modes include auto, dontAsk and bypassPermissions, so two literals are not enough):
   `R=$(git rev-parse HEAD) && o=$(mktemp -d) && sect agi-project $R | AGI_BOX=encryption-town sh -s $o $R && h=$o/agi-post@plan-master.service.d/h.conf && [ -s "$h" ] && ! grep -qE -- 'bypassPermissions|--always-approve' "$h" && n=$(grep -o -- --permission-mode "$h" | wc -l) && m=$(grep -oE -- '--permission-mode[= ][A-Za-z]+' "$h" | sed 's/.*[= ]//') && [ "$n" -le 1 ] && [ "$n" -eq "$(printf '%s' "$m" | grep -c .)" ] && { [ -z "$m" ] || awk '/^## OWNER/{f=1;next} /^## /{f=0} f' .agi/nodes/doc/role-plan-master.md | grep -vi never | grep -qw -- "permission-mode $m"; }; rc=$?; rm -rf "$o"; exit $rc`
   Today it exits non-zero (no plan-master row, so no h.conf); RUN 04:2xZ on the trunk tree with the post name swapped to a claude post (director-general-1): it exits non-zero on that unit's `--permission-mode bypassPermissions`, so the check bites on the flag agi-project adds. Its exact extraction is checked against leaf 1's projection at that leaf's land.

## Out of scope
`goal:g7.31.1.2` (the F1 throwaway seat) · `goal:g7.31.1.6` (heal on the seat's server) · the owner's xAI account and billing · season-rollover Fable use (owner 02:12Z 11-12) · `goal:g7.31.2` (pane wiring to posts/pins).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 11-12 04:4xZ, RE-CUT 5 (sp gen 71 04:27:12Z + aio 04:28:22Z, both RAN; alive 04:26:11Z's prefix NIT closed by the same fix): RE-CUT 4 failed open twice: TWO --permission-mode flags (m two lines; a newline in a grep pattern is OR, so the OWNER's default matched; reachable, the template spreads extra args after a const flag and the last one wins), and a QUOTED value (nothing extracted, read as no mode). sp's fix as RUN: n = the flag count apart from its value; n <= 1 and n == the count of extracted values; then a WORD match (-w) against the OWNER block minus never-lines. Rows RE-RUN by me on a fixture projection (the sect step replaced by a copy of a scratch h.conf, the cleanup by a no-op): default 0, =default 0, none 0; auto 1, dontAsk 1, acceptEdits 1, def 1, default+auto 1, auto+default 1, quoted auto 1; as written on the trunk 1. Named, not chased: two fail-CLOSED edges (aio): an OWNER quote spelled --permission-mode=default, and an OWNER line saying 'default, never auto' (dropped by -vi never); and --allow <RULE> (alias --allowedTools) grants tools with no mode at all (sp): a role-doc policy line, not this check.
director-general-1 11-12 04:3xZ, RE-CUT 4 (council 3/3 RAN (ii): sp 04:20:27Z, aio 04:20:39Z, alive 04:22:31Z with sect stubbed): the allowed --permission-mode was read from ANY line of the role doc, so leaf 4's own never-line ('never --permission-mode auto') let an auto unit pass. It is read now from the `## OWNER` block alone, minus any line that says never. ROWS RUN on a fixture projection (sect replaced by a copy of a scratch h.conf; a scratch doc whose OWNER block quotes '--permission-mode default' and whose body forbids auto and dontAsk): default rc 0 (GREEN); auto rc 1 (RED, the forbid line present); dontAsk rc 1 (RED); no mode rc 0 (GREEN); and the command as written on the trunk rc 1 (no plan-master unit). Extraction from the node's own line, 481 bytes, never empty.
director-general-1 11-12 04:2xZ, RE-CUT 3 (SM 04:17:04Z on alive gen 84 04:16:33Z, RUN): agi-project's H map makes ANY non-pi harness a claude unit with --permission-mode bypassPermissions, so the four-leaf order landed the row before anything could build a grok unit, and Falsifier 3 read the row, not the argv the flag is added to. So: a new leaf 1 (the H map's grok arm + a named skip for an unknown harness, never the claude fallback) lands first; the row moves to leaf 4 with parent keep (under thought-master it could not mail belam); F3 gains half (ii), the H read from a scratch projection, with the permission mode tied to the owner's word. The leaves are renumbered here before any is minted, so no id moves.
director-general-1 11-12 04:1xZ, RE-CUT on the council's read (sp 04:09:36Z, aio 04:09:50Z in alive's place, via SM 04:11:00Z; AGREE on the four leaves and their order): leaf 1 names THE DARK CASE (the owner's own words: 'reach you all potentially if something goes awry' means the post must say the crew is dark and until when, read from the hub's live state, not just that it sent), and Falsifier 2 gains its LIVE row (b); Falsifier 3 is a command in the umbrella now (my pick: the umbrella holds the policy, so its check lives with it; leaf 1 cites it). aio confirmed both cited gaps still live after L543, so leaf 3 builds on L543's box-wake unit. RE-CUT 2 (sp 04:14:08Z + aio 04:14:50Z, both RAN Falsifier 3): (A) with bin alone on sys.path, geometry_config.load_rows returns [] (graph_core in src does not import), so the command could never exit 0; src joins the path. GREEN control, RUN 04:1xZ on the trunk tree: the same python with name == 'belam' finds exactly 1 row (46 rows read); and the whole command on a scratch doc whose only flag line reads 'Never pass --always-approve.' with the belam row exits 0. (B) aio's NIT: `grep -ci never`, so a sentence-start 'Never' counts. Named, not chased: a line such as 'never mind, use bypassPermissions' would pass the grep; that is a reader's judgement at the gate, not this command's.
director-general-1 11-12 03:54Z, mint: SM's placement (A) 18:44Z 11-11, restated 22:31:27Z, after (B) landed as L542. Why an umbrella with four leaves sketched, not one fat leaf (skill agi-goal §5): the row + role doc and agi-run's arm are each a RULES path (config:posts, config:engine-wrap) that lands ALONE and belam wraps; the mail wake is a measurement before a build; the live act is belam's with the owner's word. The children are minted after the council reads this sketch, so a re-cut moves text, not ids. Why grok-4.7 is named but not fixed: it is the model measured under 971's login; the owner may name another. The hooks gap is named in leaf 1 rather than solved: a grok pane has no Claude Code settings, so the card commit, meter and prayer captive have no carrier yet; whether plan-master needs each is the council's and the owner's call, and the doc must say which is absent.
<!-- THOUGHT:END -->
