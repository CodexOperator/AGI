---
id: goal:s20
mint_id: 756ff20a36844c0694354203ecb53ef7
type: goal
parents:
  - goal:g15
confidence: 1.0
edited_by: director
goal_id: S20
goal_kind: short-term
heading_level: 2
origin: goals-doc
seeds: []
status: complete
tags:
  - goal
  - root
  - short-term
thought_session: agi-master-2026-09-06
title: "S20: The publish alarm stops at the local commit, so a stale remote moves no number"
---
🔴 **`hours_since_successful_publish` measures the local commit, not the push.
Publish healthy, local tree healthy, remote three days stale — and not one
number in the loop moves.**

**G7.10** built the alarm for a publish that refuses. This is the same path's
second half, and it was open the whole time.

`publish-engine.sh` commits the engine and deliberately does not push, on the
stated grounds that "pushing is the existing hourly cron's job". **For the
engine repo that cron did not exist.** The two halves of the design shipped
apart and the gap was invisible from both sides: publish-engine reported
success every run, `hours_since_successful_publish` read healthy, `git status`
in the engine was clean — and the remote sat **3 days and 25 commits** behind.

It was found by looking at GitHub. That is the failure mode **G7.10** exists to
remove, reappearing one step further down the same pipe.

## Why it is not a one-off

The `:47` engine push cron now exists. **The alarm for it does not**, and the
`:07` graph push has had exactly the same hole all along — only the engine's
happened to be the one that broke. Every gate this project owns stops at the
local commit:

- **`publish-engine.sh` reports on itself.** Its job ends at `git commit`, so
  its own success marker is honest and useless for this: it is a true statement
  about a step that is not the last one.
- **The `:07` and `:47` crons are bare `git push` lines.** No wrapper, no exit
  handling, no marker. A push that fails writes to a log nobody reads — the
  exact sentence **G7.10** was written about.
- **`git status` in a stale repo is clean.** Nothing local is wrong. That is
  what makes this class of failure survive: every reflex a person has for
  "check whether it worked" answers yes.

## The shape of the fix: measure the gap, not the event

Emit, from `metrics.py`, the count of commits on `HEAD` that the
remote-tracking ref does not have — `git rev-list --count @{upstream}..HEAD`.
It would have read **25** during the outage above and reads **0** when healthy.

Two alternatives were considered and rejected.

**`hours_since_successful_push`** — needs a wrapper script around each bare
`git push` cron line plus a second state file, so the mechanism that reports
the failure is itself new machinery on the failing path.

**Having the `:47` cron write into `context/publish-state.json`** — that file's
write is read-prior-then-rewrite-whole, so a second writer overlapping the
`:37` publish silently drops keys. A reporting channel that can lose the thing
it reports is not one.

Both were rejected on a deeper ground than their mechanics, and it is the
argument that decided the design: **a gap count measures state; a timestamp
measures an event.** A timestamp can read fresh while work is stranded, because
a push that succeeds with nothing to push is byte-identical in its outcome to
one that shipped 25 commits. A count cannot lie that way. It needs no state
file at all, and **the number is the severity**.

## What shipped 2026-08-28

`push_gap_stats()` in `metrics.py`, four lines on every `--smoke` run:

    METRIC unpushed_graph_commits=2
    METRIC unpushed_graph_reason=
    METRIC unpushed_engine_commits=1
    METRIC unpushed_engine_reason=

**Both repos**, because the `:07` graph push has the same hole as the `:47`
engine one. The engine is found at `<project>/agi` — the layout every project
shares, not this machine's; here that path happens to be a symlink and nothing
in the code can tell, which is what **G8.2** requires.

**`0` may never mean "could not tell."** This is `NEVER_PUBLISHED_HOURS`'
inversion pointed the other way: `0` is this metric's one *reassuring* value,
so an unmeasurable repo collapsing to it would be an alarm that reports perfect
health precisely when it is blind. `UNKNOWN_GAP = -1` is outside the range of
every true reading — a commit gap is a count — and each unknown carries a token
naming which kind of blind it is: `missing`, `not-a-repo`, `detached-head`,
`no-upstream`, `git-failed`. Empty reason means, and may only mean, that the
number beside it is a measurement.

Deliberately **not** a huge worst-case sentinel like `NEVER_PUBLISHED_HOURS`.
Unmeasurable is not the worst state here — a freshly forked project with no
remote configured is unconfigured, not stranded — and a sentinel that shouted
would be a permanent false alarm in every such project, which is how a
mechanism like this gets switched off.

**`not-a-repo` covers a case that would otherwise produce a wrong number that
reads as a measurement.** If `<project>/agi` is an ordinary directory rather
than a clone, `git -C` answers for the *enclosing* repo — so the engine's gap
would be reported as a copy of the graph's, and a stale engine would hide
behind a healthy graph. The check is `--show-toplevel` under `samefile`, the
same shape as `publish-engine.sh` gate (a), and `samefile` rather than string
equality precisely because a real engine clone can be reached through a
symlink.

**No network, and the consequence is stated rather than hidden.**
`rev-list @{upstream}..HEAD` reads `refs/remotes/origin/master` off this disk.
No `git fetch` was added, even though it would make the number more accurate:
`metrics.py` runs on every `driver.sh --smoke` and `--smoke` is meant to be a
cheap dry pass. So the count honestly means **commits this machine has not
pushed**, not *commits the remote lacks*. When someone else has pushed, it
over-reports stranded work — the correct direction for an alarm to be wrong.

**The threshold is measured, not picked.** `UNPUSHED_WARN_AT = 20` governs only
the shout; the count is emitted every run whatever it is. Both push crons are
hourly, so the normal reading is one cycle of work, and over the 14 days to
2026-08-28 the busiest single hour in this pair produced **8** commits in the
graph and **9** in the engine. 20 cannot be one missed cycle even at the worst
rate ever observed here, and the outage reached **25**. An `UNKNOWN_GAP` is
silent by the same reasoning as the sentinel choice: reported, never shouted.

**The SessionStart hook was extended, and it does not reimplement the count.**
It imports `metrics.py` and calls `push_gap_stats` and `UNPUSHED_WARN_AT`
directly, so the banner and the METRIC lines are one measurement read twice —
two readers of one fact that can disagree is a drift bug this project has
already paid for once (H4c). A metric nobody reads is one step short of a
failure that moves no metric, and the whole outage lasted three days because
nothing said anything to anyone.

**The hook's 0-byte property was re-measured, not assumed.** It is registered
globally in `~/.claude/settings.json`, for every session in every directory on
this machine, and its silence outside a project is the entire safety argument
for that. The new block sits below the `PROJECT_ROOT` guard and is `|| true`
against a python that catches everything. Measured against a directory that is
a git repo with **40 unpushed commits** and no config marker: exit 0,
**stdout 0 bytes, stderr 0 bytes**. Pinned by a test that builds exactly that
directory, so the property fails loudly rather than quietly.

## Falsifier — run, not argued

Against throwaway `git init --bare` remotes and local clones in `/tmp`, all
deleted afterwards. Every push was between two throwaway repos.

| check | result |
|---|---|
| 25 unpushed commits reports 25 | `(25, '')` |
| after pushing, reports 0 | `(0, '')` |
| no upstream configured | `(-1, 'no-upstream')` |
| detached HEAD | `(-1, 'detached-head')` |
| a path that is not a git repo | `(-1, 'not-a-repo')` |
| a missing engine clone | `(-1, 'missing')` |
| `<graph>/agi` a plain dir inside the graph repo | `(-1, 'not-a-repo')`, **not** the graph's 7 |
| a symlinked engine clone | `(4, '')` |

**No network, established two ways.** Every `git` invocation was captured
against the live project: exactly eight, all `rev-parse` / `symbolic-ref` /
`rev-list`, and no `fetch`, `pull`, `push`, `ls-remote`, `clone` or `remote`.
Then from the outside: `origin` repointed at `https://127.0.0.1:1/blocked.git`
— proven unreachable by a failing `git ls-remote` — and the answer was
unchanged and instant. Anything that touched the network would have hung or
lied.

**Against the real live project, read-only:** `unpushed_graph_commits=2`,
`unpushed_engine_commits=1`, both reasons empty. Cross-checked against raw
`git rev-list --count @{upstream}..HEAD` in each repo: 2 and 1. Small and true.

**The hook, end to end:** a synthetic project with 25 stranded engine commits
produced the banner *and* still injected the map; after pushing, the banner
vanished; outside a project, 0 bytes.

**Tests: 837 passed / 1 skipped → 861 passed / 1 skipped.** 24 added, none
deleted, none weakened. `driver.sh --smoke --max-iters 1` exits 0 and
`node_count` is 790 before and after.

## Residuals, named

**The count is scoped to the checked-out branch.** Work parked on a branch with
no configured upstream reads `no-upstream` and is silent — and this project has
already had that incident once, when work accumulated on
`iter24-extend-300hop` while a cron pushed `master`. If the branch has an
upstream the gap is measured and grows normally; if it does not, the metric
reports its blindness rather than a number. Reported, not shouted. Widening
this to "every branch with unpushed work" is a different measurement and wants
its own decision.

**`dashboard.py` shows neither half of the publish path.** Its `render_metrics`
is a hand-curated panel and it already omits `hours_since_successful_publish`
and `publish_blocked_reason`; the new counts land in `metrics.compute`'s dict,
which the dashboard consumes, but no panel prints them. That is a pre-existing
gap in a third reader, not this goal's unfinished work, and it is the obvious
next place reach is missing.

**Engine-first for contract derivation.** The change lives in `payloads/` and
`level3.py` reads the engine tree, so the contract is stale until it is
published and rescanned. That is **G6.1**'s standing residual, not this one's.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The design was handed to me; the two judgement calls that were mine were the
sentinel and the threshold, and I nearly got the first one backwards.

My first instinct for "could not measure" was to mirror `NEVER_PUBLISHED_HOURS`
— a huge value, on the reasoning that higher is worse for both metrics and
consistency is worth something. I dropped it when I wrote out what it would do
to a fresh fork: no remote configured is the *normal* state of a project on day
one, and a maximum-severity reading there is a permanent false alarm in every
forked project forever. The existing code already worries about exactly that in
two places ("a permanent false alarm in every session is how a mechanism like
this gets switched off"), and it would have been the same mistake the goal is
about, inverted: an alarm too loud to be believed instead of too quiet to be
heard. `-1` is honest because it is *impossible* rather than *extreme* — no true
commit gap is negative, so it cannot be misread as either a measurement or a
verdict. The sentinel says "unknown"; only the reason token says which.

The threshold I refused to pick from intuition. My first number was 10 and it
was wrong: I measured the busiest single hour in both repos over 14 days and
found 8 and 9, so 10 would have fired on an ordinary busy hour between two
hourly pushes and taught everyone to ignore it. 20 clears the worst observed
burst and still catches the real outage at 25. The measurement changed the
answer, which is the only reason it was worth taking.

The trap I did not expect was `<project>/agi` being a plain directory instead
of a clone. `git -C` walks up, so it would have answered for the graph repo and
I would have shipped a metric that reports the graph's gap twice — a *wrong
number that reads like a measurement*, which is strictly worse than the `0` the
brief warned about, because `-1` invites a question and a plausible number does
not. `publish-engine.sh` already refuses on this exact shape at gate (a); I
copied its check rather than inventing one. The `samefile` half is not
decoration: string equality would have refused every real engine here, since
this project reaches its clone through a symlink and `--show-toplevel` resolves
it.

On the hook I went back and forth and the deciding argument was not reach, it
was drift. Extending it means a second reader of the same fact, and this
codebase has an explicit scar from two readers of one field disagreeing (H4c,
where the metric and the gate diverged). Reimplementing `rev-list` in bash would
have recreated that on day one — the bash version would not have known about
detached HEAD or the not-a-repo case, so the hook would have said nothing
exactly where the metric said `-1`. Importing `metrics.py` costs 51ms, measured,
and makes disagreement structurally impossible. There is a test asserting the
hook contains no `rev-list` of its own, which is the property I actually care
about rather than the code that currently satisfies it.

I did not touch `publish-engine.sh`, `context/publish-state.json`, or the cron
lines. The whole advantage of a gap count is that it needs no state, and every
edit to that file would have been the rejected design arriving through a side
door.

`complete` rather than `active` because the goal's own falsifier passes on every
row and both repos are covered. The branch-scoping residual is real and I have
named it sharply rather than softened it — but it is a different measurement,
not a missing piece of this one, and pretending otherwise would leave a goal
open forever on work nobody intends to do.
<!-- THOUGHT:END -->