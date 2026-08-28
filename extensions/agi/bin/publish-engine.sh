#!/usr/bin/env bash
# publish-engine.sh — write the engine repo from the graph, then commit it.
#
# GOALS.md G6.5 step 2: "after G6.3, cron may stitch and commit the engine."
# G6.3 is complete and G6.1's read direction closed, so this is now a legal
# operation. It is still written to refuse far more often than it acts.
#
# The sequence, and every step is a gate rather than a stage:
#
#   1. re-derive contracts FROM THE GRID       (level3.py --from-grid)
#   2. verify the graph against ITSELF         (stitch --verify --from-grid --strict)
#   3. publish                                  (stitch --out ENGINE --from-grid --publish)
#   4. commit the engine, citing the graph commit that produced it
#
# Step 2 is the one that matters. Publishing a graph that disagrees with its own
# contracts would put drift into the engine atomically and cleanly, which is
# worse than not publishing at all — G6.7's own argument about an atomic
# publisher of corrupt content, arriving here first.
#
# What it will NOT do, by construction:
#   - publish into a dirty engine tree (stitch --publish refuses; that is what
#     makes every overwritten byte recoverable with `git checkout .`)
#   - publish when the graph has uncommitted node changes (a publish must be
#     attributable to a graph commit, or step 4's message is a lie)
#   - push. Pushing is the existing hourly cron's job; this only commits.
#
# goal:g7.10 — EVERY exit from here is recorded, in machine-readable form, in
# `<project>/context/publish-state.json`. Refusing is a legitimate outcome;
# refusing *quietly* is not. This script is the `:37` cron, and it refused 40
# consecutive times while publishing nothing at all, from install on
# 2026-08-25 until someone checked by hand on 2026-08-27. Nothing caught it:
# the refusal went to a log nobody reads, no metric moved, `driver.sh --smoke`
# said nothing and the injected map said nothing. The marker is what
# `metrics.py` (hours_since_successful_publish, publish_blocked_reason) and
# `hooks/cc-session-start.sh` read, so a stall now moves a number and shouts at
# the next agent to open any session anywhere.
#
# goal:g7.10 part 3 — a blocked publish no longer strands the bytes. When the
# default branch is refused for a reason that is about *attribution* rather
# than *content*, the same tree is parked on `cron/pending-<graph-sha>` in the
# engine, locally, never pushed. See `run_fallback` below. Parking is still a
# REFUSAL: exit is non-zero, `last_success_*` does not move, and the alarm keeps
# climbing. A safety net that made the alarm read healthy would be a worse bug
# than the one part 1 fixed.
#
# Usage: publish-engine.sh [--engine-root DIR] [--dry-run]
set -euo pipefail

SCRIPT="$(readlink -f "${BASH_SOURCE[0]}")"
BIN_DIR="$(dirname "$SCRIPT")"
PLUGIN_ROOT="$(dirname "$BIN_DIR")"
DEFAULT_ENGINE_ROOT="$(dirname "$(dirname "$PLUGIN_ROOT")")"

ENGINE_ROOT="$DEFAULT_ENGINE_ROOT"
DRY_RUN=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine-root) ENGINE_ROOT="$2"; shift 2 ;;
    --dry-run)     DRY_RUN=1; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

PROJECT_ROOT="$(bash "$PLUGIN_ROOT/lib/find-root.sh" 2>/dev/null || pwd)"
cd "$PROJECT_ROOT"

say() { echo "[publish-engine] $*"; }

# --- the durable marker (goal:g7.10) ------------------------------------------
# One file, two readers: metrics.py turns it into METRIC lines, and the
# SessionStart hook turns it into a banner. It lives under context/ beside
# INJECTION.md — where this repo already keeps generated state — and NOT under
# nodes/, because gate 0 below refuses on any uncommitted change under nodes/,
# so a marker written there would arm the gate it exists to report on, on every
# run, forever.
STATE_FILE="$PROJECT_ROOT/context/publish-state.json"

# record_state <ok|refused> [reason-token] [human detail]
# Never fatal: failing to write the marker must not change the outcome of the
# run, and must not mask the exit code the caller is about to see.
record_state() {
  # --dry-run is a report, not a run. Writing state from it would let a
  # hand-run dry pass overwrite the cron's record of what really happened.
  [[ "$DRY_RUN" == "1" ]] && return 0
  mkdir -p "$(dirname "$STATE_FILE")" 2>/dev/null || true
  AGI_PUBLISH_STATE="$STATE_FILE" \
  AGI_PUBLISH_STATUS="$1" \
  AGI_PUBLISH_REASON="${2:-}" \
  AGI_PUBLISH_DETAIL="${3:-}" \
  AGI_PUBLISH_COMMIT="${GRAPH_COMMIT:-}" \
  AGI_PUBLISH_FB_STATUS="${FALLBACK_STATUS:-}" \
  AGI_PUBLISH_FB_BRANCH="${FALLBACK_BRANCH:-}" \
  AGI_PUBLISH_FB_COMMIT="${FALLBACK_COMMIT:-}" \
  AGI_PUBLISH_FB_DETAIL="${FALLBACK_DETAIL:-}" \
  python3 - <<'PY' || say "WARNING: could not write $STATE_FILE"
import json, os, time

path = os.environ["AGI_PUBLISH_STATE"]
status = os.environ["AGI_PUBLISH_STATUS"]

# Carry the last real publish forward. A refusal must never erase the record of
# when the engine last actually landed -- that timestamp is the whole alarm.
prior = {}
try:
    with open(path, encoding="utf-8") as fh:
        loaded = json.load(fh)
    if isinstance(loaded, dict):
        prior = loaded
except Exception:
    pass

now = int(time.time())
state = {
    "schema": 1,
    "last_run_epoch": now,
    "last_run_status": status,
    "last_run_reason": os.environ.get("AGI_PUBLISH_REASON", ""),
    "last_run_detail": os.environ.get("AGI_PUBLISH_DETAIL", ""),
    "last_success_epoch": prior.get("last_success_epoch"),
    "last_success_graph_commit": prior.get("last_success_graph_commit"),
}
if status == "ok":
    state["last_success_epoch"] = now
    state["last_success_graph_commit"] = os.environ.get("AGI_PUBLISH_COMMIT", "")

# goal:g7.10 part 3 -- the fallback's record. Strictly ADDITIVE: five new keys,
# and not one line above may be reached from here. A run that parked its bytes
# on `cron/pending-*` is still `last_run_status: refused` with an untouched
# `last_success_epoch`, so `hours_since_successful_publish` keeps climbing and
# `publish_blocked_reason` stays set. The net caught the work; it did not make
# the fall stop counting. `schema` stays 1 on purpose: every existing reader
# keys on presence, so bumping it would signal a break that did not happen.
fb = os.environ.get("AGI_PUBLISH_FB_STATUS", "")
if fb:
    state["last_fallback_epoch"] = now
    state["last_fallback_status"] = fb
    state["last_fallback_detail"] = os.environ.get("AGI_PUBLISH_FB_DETAIL", "")
    # Branch and commit are a POINTER to parked bytes, so they are carried
    # forward rather than cleared by a later run that parked nothing. Losing
    # the address of a branch that exists is its own quiet failure.
    for key, env in (("last_fallback_branch", "AGI_PUBLISH_FB_BRANCH"),
                     ("last_fallback_commit", "AGI_PUBLISH_FB_COMMIT")):
        value = os.environ.get(env, "")
        state[key] = value or prior.get(key)
else:
    for key in ("last_fallback_epoch", "last_fallback_status",
                "last_fallback_detail", "last_fallback_branch",
                "last_fallback_commit"):
        if key in prior:
            state[key] = prior[key]

# Written whole then renamed: a hook or a metric reading mid-write would see a
# truncated file, and an unreadable marker reads as "never published".
tmp = path + ".tmp"
with open(tmp, "w", encoding="utf-8") as fh:
    json.dump(state, fh, indent=2, sort_keys=True)
    fh.write("\n")
os.replace(tmp, path)
PY
}

# The reassuring thing, said at the moment the fear arrives. When a publish
# stalls the reasonable assumption is that engine work is evaporating, and it
# is not: `grid.py commit --all` is a separate, ungated, 5-minute cron.
say_bytes_are_safe() {
  say "  Your payload bytes are NOT lost. \`grid.py commit --all\` runs on its own"
  say "  ungated 5-minute cadence, so every byte you edited under payloads/ is"
  say "  already recorded in its node's grid ref. Only the ENGINE PUBLISH is"
  say "  blocked, and it resumes by itself on the next :37 once this clears."
}

# --- the fallback: branch and continue (goal:g7.10 part 3) --------------------
#
# "The bytes must land somewhere even when the main path is blocked." Blocked
# publishes used to stop, and a stop that repeats 40 times is indistinguishable
# from a stop that repeats once. This parks the tree on
# `cron/pending-<graph-sha>` in the engine so the work is never stranded, while
# the default branch keeps its invariant: it is only ever written from a graph
# commit that exists.
#
# Four decisions, each of which the obvious implementation gets wrong:
#
#   1. A DETACHED TEMPORARY WORKTREE, never a branch switch in the engine's own
#      checkout. `git checkout -b` in $ENGINE_ROOT, write, commit, switch back
#      is racy against every other reader of that tree, and this project has
#      already lost work to exactly that shape -- commits piled up on an
#      `iter24-extend-300hop` branch while a cron pushed `master` and published
#      nothing. The worktree is created outside BOTH repos, is removed on every
#      exit path, and the engine's own HEAD/branch/cleanliness are asserted
#      unchanged afterwards rather than assumed.
#
#   2. VERIFY FIRST, ALWAYS. Gate 2 has not run when gate 0 refuses, so the
#      fallback runs it itself -- read-only, no level3.py, no grid commit,
#      nothing written into the graph repo at all. This is also the whole of the
#      answer to "does the fallback apply to gate 2": no, and not as a special
#      case. A pending branch is one `git merge --ff-only` from master, so it
#      may not carry bytes the real publish would have refused, and gate 2's
#      precondition is precisely what a `contracts-disagree` refusal reports as
#      failed. Eligibility is listed explicitly below anyway; verify-first is
#      the invariant that would hold even if that list were widened by mistake.
#
#   3. COMMIT ONLY WHEN THE BYTES DIFFER. This is the hourly `:37` cron. A graph
#      that stays dirty for three days is 72 runs, and 72 unconditional commits
#      is manufactured junk of the same kind a refused run once left behind as
#      184 junk nodes. The branch name is keyed on the graph sha, which does not
#      move while the graph is dirty -- but the GRID does (a separate, ungated
#      5-minute cron records payloads), so content genuinely changes between
#      runs. The check is the diff, not the clock.
#
#   4. PARKING IS STILL A REFUSAL. Exit non-zero, `last_success_*` untouched,
#      `publish_blocked_reason` still set. An alarm that goes quiet because the
#      safety net caught something is the exact mirror of the alarm that never
#      fired, and part 1 was paid for once already.
FALLBACK_STATUS=""
FALLBACK_BRANCH=""
FALLBACK_COMMIT=""
FALLBACK_DETAIL=""
FALLBACK_BRANCH_PREFIX="cron/pending-"

_FB_WT=""
_FB_TMP=""

_fb_cleanup() {
  if [[ -n "$_FB_WT" ]]; then
    git -C "$ENGINE_ROOT" worktree remove --force "$_FB_WT" >/dev/null 2>&1 || true
  fi
  [[ -n "$_FB_TMP" ]] && rm -rf "$_FB_TMP"
  git -C "$ENGINE_ROOT" worktree prune >/dev/null 2>&1 || true
  _FB_WT=""
  _FB_TMP=""
  return 0
}

# Which refusals may route around the block. `contracts-disagree` is absent by
# design (see decision 2); `unexpected-failure` is absent because after an
# unknown failure we do not know what state we are in, and running more
# machinery is how a small break becomes a large one.
fallback_is_eligible() {
  case "$1" in
    graph-dirty) return 0 ;;
    *)           return 1 ;;
  esac
}

_fb_decline() {
  FALLBACK_STATUS="$1"
  FALLBACK_DETAIL="$2"
  # A decline parked nothing THIS run, so it must not claim a pointer. Left
  # empty, record_state carries any genuinely-parked earlier branch forward.
  FALLBACK_BRANCH=""
  FALLBACK_COMMIT=""
  say "  fallback: DECLINED [$1] — $2"
  _fb_cleanup
  return 0
}

_run_fallback_body() {
  local reason="$1"
  local head before_branch base tip changed wt_sha tmproot pr er

  # (a) The engine has to be a git repo, and $ENGINE_ROOT has to be its ROOT.
  # Not a check for its own sake: the default $ENGINE_ROOT is derived from this
  # script's own path, so a copy of this script running from inside the graph's
  # `payloads/` tree resolves it to a directory that is *inside the graph repo*.
  # `git -C` would happily answer for the graph repo, and the fallback would
  # cut a `cron/pending-*` branch in the thoughtgraph.
  pr="$(readlink -f "$PROJECT_ROOT")"
  er="$(readlink -f "$ENGINE_ROOT" 2>/dev/null || true)"
  if [[ -z "$er" || "$er" == "$pr" || "$er" == "$pr"/* ]]; then
    _fb_decline "no-engine" "engine root '$ENGINE_ROOT' is missing or resolves inside the graph repo"
    return 0
  fi
  if [[ "$(git -C "$ENGINE_ROOT" rev-parse --show-toplevel 2>/dev/null)" != "$er" ]]; then
    _fb_decline "no-engine" "engine root '$ENGINE_ROOT' is not the root of a git repo"
    return 0
  fi
  head="$(git -C "$ENGINE_ROOT" rev-parse HEAD 2>/dev/null || true)"
  before_branch="$(git -C "$ENGINE_ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || echo DETACHED)"
  if [[ -z "$head" ]]; then
    _fb_decline "no-engine" "engine root '$ENGINE_ROOT' has no commits to branch from"
    return 0
  fi

  # (b) Where to build. Outside both repos: stitch.py refuses to write into the
  # graph repo at all, and treats any path inside the engine repo as a
  # `--publish` -- which would gate this on the engine's own working tree being
  # clean, a condition parking into a private worktree has no business needing.
  # Created before the verify below, so the verify has somewhere to leave its
  # evidence.
  tmproot="$(readlink -f "${TMPDIR:-/tmp}" 2>/dev/null || echo /tmp)"
  if [[ "$tmproot" == "$pr" || "$tmproot" == "$pr"/* || \
        "$tmproot" == "$er" || "$tmproot" == "$er"/* ]]; then
    tmproot="/tmp"
  fi
  _FB_TMP="$(mktemp -d "$tmproot/agi-publish-fallback.XXXXXX" 2>/dev/null || true)"
  if [[ -z "$_FB_TMP" || ! -d "$_FB_TMP" ]]; then
    _fb_decline "failed" "could not create a temporary directory under $tmproot"
    return 0
  fi

  # (c) Verify first. Read-only: it writes nothing anywhere, and in particular
  # it does not touch nodes/ the way step 1 does.
  #
  # The output is KEPT, and a bounded tail of it is printed on failure. Sending
  # it to /dev/null cost a real diagnosis once already: a fallback declined
  # `verify-failed` while a concurrent `*/5` grid cron was running, and there
  # was no way afterwards to tell whether the graph had actually drifted or a
  # git subprocess had simply lost a race. "It failed and the evidence is gone"
  # is the failure mode this entire goal is named after.
  say "  fallback: checking the graph against its own contracts before parking anything"
  if ! python3 "$BIN_DIR/stitch.py" --project "$PROJECT_ROOT" --verify --from-grid \
          --engine-root "$ENGINE_ROOT" --strict >"$_FB_TMP/verify.log" 2>&1; then
    say "  fallback: stitch.py --verify --from-grid --strict said —"
    tail -n 12 "$_FB_TMP/verify.log" 2>/dev/null | while IFS= read -r line; do
      say "  fallback: | $line"
    done
    # A crash is not evidence of drift. Declining is right either way, but the
    # marker must not report "your graph disagrees with itself" when what really
    # happened is that the check never finished.
    if grep -q "Traceback (most recent call last)" "$_FB_TMP/verify.log" 2>/dev/null; then
      _fb_decline "verify-crashed" \
        "stitch --verify could not complete, so nothing here knows whether these bytes are safe to park"
    else
      _fb_decline "verify-failed" \
        "the graph disagrees with its own contracts; a pending branch is one fast-forward from master, so it may not carry bytes the real publish would refuse"
    fi
    return 0
  fi

  # (d) Base the pending branch on its own tip when that tip already contains
  # the engine's HEAD -- that keeps the chain linear and `--ff-only` true, and
  # it is what makes run 2..72 a no-op instead of a second commit. A tip that
  # does NOT contain HEAD is stale (the engine moved on without it), so rebuild
  # from HEAD rather than extend something that can no longer fast-forward.
  FALLBACK_BRANCH="${FALLBACK_BRANCH_PREFIX}${GRAPH_COMMIT}"
  base="$head"
  tip="$(git -C "$ENGINE_ROOT" rev-parse --verify --quiet "refs/heads/$FALLBACK_BRANCH" || true)"
  if [[ -n "$tip" ]]; then
    if git -C "$ENGINE_ROOT" merge-base --is-ancestor "$head" "$tip"; then
      base="$tip"
    else
      say "  fallback: $FALLBACK_BRANCH no longer contains the engine's HEAD; rebuilding it from HEAD"
    fi
  fi

  _FB_WT="$_FB_TMP/wt"
  if ! git -C "$ENGINE_ROOT" worktree add --detach --quiet "$_FB_WT" "$base"; then
    _fb_decline "failed" "could not create a temporary worktree of $ENGINE_ROOT"
    return 0
  fi
  if [[ -n "$(git -C "$_FB_WT" status --porcelain 2>/dev/null)" ]]; then
    _fb_decline "failed" "a freshly created worktree was already dirty; refusing to build on it"
    return 0
  fi

  # (e) The same materialization the real publish does, from the same source.
  # `--force` rather than `--publish` only because the target is a private
  # worktree outside the engine root; the bytes are identical either way.
  if ! python3 "$BIN_DIR/stitch.py" --project "$PROJECT_ROOT" --out "$_FB_WT" \
          --from-grid --force >/dev/null; then
    _fb_decline "failed" "stitch.py could not materialize the grid into the worktree"
    return 0
  fi

  changed="$(git -C "$_FB_WT" status --porcelain | wc -l | tr -d ' ')"
  if [[ "$changed" == "0" ]]; then
    if [[ -n "$tip" && "$base" == "$tip" ]]; then
      FALLBACK_STATUS="already-parked"
      FALLBACK_COMMIT="$(git -C "$ENGINE_ROOT" rev-parse --short "$tip")"
      FALLBACK_DETAIL="$FALLBACK_BRANCH already carries exactly these bytes; no second commit"
    else
      FALLBACK_STATUS="already-matched"
      FALLBACK_BRANCH=""
      FALLBACK_DETAIL="the engine tree already matches the grid; nothing to park"
    fi
    say "  fallback: $FALLBACK_DETAIL"
    _fb_cleanup
    return 0
  fi

  git -C "$_FB_WT" add -A
  # The message must not lie about where these bytes came from. Under a
  # graph-dirty refusal they come from the grid, which is AHEAD of the graph's
  # git HEAD, so the tree is attributable to no graph commit at all -- which is
  # the entire reason master refused.
  if ! git -C "$_FB_WT" commit -q -F - <<EOF
parked by cron: engine bytes with NO graph commit to cite

publish-engine.sh refused on the default branch [${reason}] and parked the result here
rather than strand it. This is a REFUSAL that kept working, not a publish: the
default branch is untouched and nothing was pushed.

READ THE BRANCH NAME AS AN ANCHOR, NOT AS PROVENANCE. ${GRAPH_COMMIT} is the
nearest COMMITTED state of the graph, not a description of what is in this
commit. These ${changed} file(s) came out of the graph's grid refs, which run
ahead of the graph repo's git HEAD -- \`grid.py commit --all\` is a separate,
ungated, 5-minute cron while the publish is gated. That gap is exactly why a
commit on the default branch would have been a lie: it must cite a graph commit
that exists and contains these bytes.

Written by stitch.py --out <worktree> --from-grid, after
stitch.py --verify --from-grid --strict passed against the same grid.

TO LAND IT, clear the block -- commit nodes/ and GOALS.md in the graph repo --
and let the next :37 publish normally. It will produce these same bytes with
real provenance, after which this branch is redundant:

    git -C <engine> branch -D ${FALLBACK_BRANCH}

If you want THIS commit on the default branch instead, and you accept that its
message cites a graph state which does not contain it:

    git -C <engine> merge --ff-only ${FALLBACK_BRANCH}

goal:g7.10 part 3.
EOF
  then
    _fb_decline "failed" "could not commit the parked bytes in the temporary worktree"
    return 0
  fi

  wt_sha="$(git -C "$_FB_WT" rev-parse HEAD)"
  # Safe as a plain `branch -f`: the worktree is DETACHED, so this ref is not
  # checked out anywhere and nobody is standing on it.
  if ! git -C "$ENGINE_ROOT" branch -f "$FALLBACK_BRANCH" "$wt_sha" >/dev/null 2>&1; then
    _fb_decline "failed" "could not move $FALLBACK_BRANCH to the parked commit"
    return 0
  fi

  FALLBACK_STATUS="parked"
  FALLBACK_COMMIT="$(git -C "$ENGINE_ROOT" rev-parse --short "$wt_sha")"
  FALLBACK_DETAIL="${changed} file(s) parked on ${FALLBACK_BRANCH} @ ${FALLBACK_COMMIT} (local only, not pushed)"
  say "  fallback: $FALLBACK_DETAIL"
  _fb_cleanup

  # (f) Assert, do not assume, that the engine's own checkout is where it was.
  # Hazard 1 is the whole reason this uses a worktree; an assertion is what
  # turns that from an intention into a fact.
  local after_head after_branch
  after_head="$(git -C "$ENGINE_ROOT" rev-parse HEAD 2>/dev/null || true)"
  after_branch="$(git -C "$ENGINE_ROOT" symbolic-ref --quiet --short HEAD 2>/dev/null || echo DETACHED)"
  if [[ "$after_head" != "$head" || "$after_branch" != "$before_branch" ]]; then
    say "  fallback: ALARM — the engine checkout moved ($before_branch@${head:0:9} ->"
    say "  fallback: $after_branch@${after_head:0:9}). Nothing here should have done that."
    FALLBACK_STATUS="parked-but-engine-moved"
    FALLBACK_DETAIL="parked on ${FALLBACK_BRANCH}, but $ENGINE_ROOT moved from $before_branch@${head:0:9} to $after_branch@${after_head:0:9}"
  fi
  return 0
}

# Never fatal, and never allowed to change the exit code the caller is about to
# see: a fallback that failed still leaves an ordinary, loud refusal behind.
run_fallback() {
  FALLBACK_STATUS=""
  FALLBACK_BRANCH=""
  FALLBACK_COMMIT=""
  FALLBACK_DETAIL=""

  # `--dry-run` is a report. A branch is a write, so a dry pass creates none.
  if [[ "$DRY_RUN" == "1" ]]; then
    say "  fallback: not attempted (--dry-run writes nothing, and a branch is a write)"
    return 0
  fi

  if ! fallback_is_eligible "$1"; then
    FALLBACK_STATUS="not-eligible"
    FALLBACK_DETAIL="[$1] is not a block the fallback may route around"
    say "  fallback: not attempted — $FALLBACK_DETAIL"
    return 0
  fi

  # errexit and the ERR trap are both off in here: a failing git call must land
  # in a recorded `_fb_decline`, not blow past record_state on its way out.
  trap - ERR
  set +e
  _run_fallback_body "$1"
  set -e
  trap on_unexpected_error ERR
  return 0
}

# refuse <reason-token> <human explanation...>
refuse() {
  local reason="$1"; shift
  say "REFUSING [$reason]: $*"
  say_bytes_are_safe
  # Before the marker is written, so a run that parked its bytes says so in the
  # same record that says it refused.
  run_fallback "$reason"
  record_state refused "$reason" "$*"
  exit 1
}

# Anything that fails outside a gate -- level3.py crashing, the grid commit
# dying, a python that is not there -- used to exit non-zero with no marker at
# all, which reads downstream as "the cron never ran". Recorded like any other
# refusal so that case is visible too.
on_unexpected_error() {
  local rc=$?
  trap - ERR
  say "REFUSING [unexpected-failure]: a step exited ${rc}. Nothing published."
  say_bytes_are_safe
  record_state refused "unexpected-failure" "a step exited ${rc}"
  exit "$rc"
}
trap on_unexpected_error ERR

# --- gate 0: the graph must be committed --------------------------------------
# A publish is a derivation. If nodes/ has uncommitted changes then the engine
# commit below would cite a graph state that exists nowhere but this machine.
#
# This gate is CORRECT and must not be weakened. A single node whose stored
# contract differs from what level3.py re-derives leaves the graph permanently
# dirty and arms it forever -- one character of YAML quoting did exactly that
# (goal:g6.5), and the 3.11/3.12 f-string flap (goal:s19) then made it
# intermittent, which is worse. The fix for both is upstream of here.
#
# Read before the gate rather than after it, because the fallback names its
# branch `cron/pending-<this>`. `rev-parse HEAD` answers the same whether or not
# the tree is dirty: it is the nearest COMMITTED graph state. That it is not a
# description of the working tree is the point of the gate, and the parked
# commit's message says so in as many words.
GRAPH_COMMIT="$(git -C "$PROJECT_ROOT" rev-parse --short HEAD 2>/dev/null || echo unknown)"

if [[ -n "$(git -C "$PROJECT_ROOT" status --porcelain -- nodes/ GOALS.md)" ]]; then
  refuse "graph-dirty" "the graph has uncommitted changes under nodes/ or GOALS.md; commit them first — a published engine must cite a real graph commit"
fi

# --- step 1: contracts re-derive from the grid, not from the engine tree ------
say "re-deriving contracts from the grid"
python3 "$BIN_DIR/level3.py" --project "$PROJECT_ROOT" \
        --engine-root "$ENGINE_ROOT" --from-grid

# level3.py rewrites node bodies, so the grid needs the new versions before the
# publish reads them back out. Without this the published tree would be one
# derivation behind the nodes that describe it.
python3 "$BIN_DIR/grid.py" commit --all --prefix "publish: "

# --- gate 2: the graph must agree with itself ---------------------------------
say "verifying the graph against its own payloads"
if ! python3 "$BIN_DIR/stitch.py" --project "$PROJECT_ROOT" --verify --from-grid \
        --engine-root "$ENGINE_ROOT" --strict; then
  refuse "contracts-disagree" "the graph disagrees with its own contracts; nothing published"
fi

if [[ "$DRY_RUN" == "1" ]]; then
  say "--dry-run: all gates passed; would publish to $ENGINE_ROOT and commit"
  exit 0
fi

# --- step 3: publish ----------------------------------------------------------
say "publishing to $ENGINE_ROOT"
python3 "$BIN_DIR/stitch.py" --project "$PROJECT_ROOT" --out "$ENGINE_ROOT" \
        --from-grid --publish --engine-root "$ENGINE_ROOT"

# --- step 4: commit the engine, citing what produced it -----------------------
if [[ -z "$(git -C "$ENGINE_ROOT" status --porcelain)" ]]; then
  # A successful publish that wrote no new bytes. Recorded as success, not as
  # a no-op: the engine matches the graph, which is the entire point, and
  # calling it "nothing happened" is what let a healthy run and a 40-times
  # refusal look identical from outside.
  say "engine already matches the graph; nothing to commit"
  record_state ok "" "engine already matched the graph @ ${GRAPH_COMMIT}"
  exit 0
fi

CHANGED="$(git -C "$ENGINE_ROOT" status --porcelain | wc -l | tr -d ' ')"
git -C "$ENGINE_ROOT" add -A
git -C "$ENGINE_ROOT" commit -q -m "published from the graph @ ${GRAPH_COMMIT}

${CHANGED} file(s) written by stitch.py --from-grid --publish. This commit is a
derivation, not an edit: every byte came out of a node's grid ref in the graph
repo at ${GRAPH_COMMIT}. See GOALS.md G6.1/G6.5.
"
say "committed ${CHANGED} file(s) to $ENGINE_ROOT (graph @ ${GRAPH_COMMIT})"
record_state ok "" "committed ${CHANGED} file(s) (graph @ ${GRAPH_COMMIT})"
