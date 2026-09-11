#!/bin/bash
# find-root.sh — locate the project root.
#
# The bash half of the one resolution rule; bin/locations.py is the Python half
# and implements the SAME phase order deliberately. The two are verified against
# each other in tests/test_locations.py::test_bash_and_python_agree — if you
# change a phase here, change it there, or that test fails and says so.
#
# Three-phase rule, tried in order, first success wins:
#   0. GRAPH DIR: walk up looking for <d>/.agi/ holding a config. This is the
#      goal:g11 layout, where the graph lives inside the repo it builds:
#        <repo>/.agi/{config.json,nodes/,context/}  +  <repo>/GOALS.md
#      Checked BEFORE phase 1 within each directory, because a half-migrated
#      repo carries both markers and the new layout is the one that should win.
#      Nearest enclosing wins, which is what lets an engine clone carry its own
#      graph without a flag: run from fantasia/ and you get fantasia's graph,
#      run from fantasia/agi/ and you get the engine's.
#   1. UP: walk up from the starting directory looking for a config file
#      (agi-tree.config.json, or legacy autoresearch-tree.config.json).
#      This is the pre-goal:g11 layout, where the tree IS the project root
#      (agi-tree.config.json + nodes/ at the top). This repo no longer
#      uses it; phase 0 resolves .agi/ here.
#   2. DOWN: only if phase 1 finds nothing, descend from the starting
#      directory looking for a tree at <start>/*-tree/.
#      This is the layout for a generic project that keeps its graph as a
#      sibling-level repo: <project>/<project>-tree/{config,GOALS.md,nodes/},
#      with the engine clone living INSIDE that tree at
#      <project>/<project>-tree/agi. The tree is outside the engine, not
#      inside it, so an engine checkout never contains a tree.
#        a. Preferred, unambiguous: <start>/<basename of start>-tree/<config>.
#        b. Otherwise glob <start>/*-tree/<config>. Exactly one match wins;
#           more than one is a hard error (candidates listed on stderr) —
#           never guess which tree belongs to the project.
#   3. Otherwise, return 1.
#
# No project name is ever hardcoded here — phase 2 is derived purely from the
# starting directory's basename and a glob, so this file stays generic across
# any project (see goal:g8.2).
#
# Source from any other script: `source <plugin>/lib/find-root.sh && PROJECT_ROOT=$(find_project_root)`
#
# Compatibility window: agi-tree.config.json and autoresearch-tree.config.json
# are still accepted so pre-goal:g11 projects keep working. New projects use
# .agi/config.json (phase 0).

# Canonical first, legacy second. Order matters: agi_tree_config_path returns the
# first that exists, so a project carrying both resolves to the canonical one.
AGI_TREE_CONFIG_NAMES=("agi-tree.config.json" "autoresearch-tree.config.json")

# The graph directory goal:g11 moves the tree into. A dot name on purpose: it
# files the graph with .git/.github/.claude — the tooling a repo carries but
# does not itself run — rather than in the middle of the source tree.
AGI_GRAPH_DIR_NAME=".agi"

# Print the config file path inside $1, or return 1 if the dir is not a project.
#
# Inside a .agi/ directory the bare name config.json is also accepted: the
# directory already says what it is, so the project prefix is redundant there.
# It is accepted ONLY there — outside a .agi/, config.json is far too generic
# to be a project marker, and treating it as one would make any repo with a
# stray config.json in its root look like a graph.
agi_tree_config_path() {
  local d="$1" name
  local -a names=("${AGI_TREE_CONFIG_NAMES[@]}")
  if [[ "$(basename "$d")" == "$AGI_GRAPH_DIR_NAME" ]]; then
    names=("config.json" "${names[@]}")
  fi
  for name in "${names[@]}"; do
    if [[ -f "$d/$name" ]]; then
      echo "$d/$name"
      return 0
    fi
  done
  return 1
}

# Phase-0 helper: print <d>/.agi if it exists and holds a config, else return 1.
agi_graph_dir_in() {
  local cand="$1/$AGI_GRAPH_DIR_NAME"
  if [[ -d "$cand" ]] && agi_tree_config_path "$cand" >/dev/null 2>&1; then
    echo "$cand"
    return 0
  fi
  return 1
}

# Phase-2 helper: descend into <start>/*-tree/ looking for a project dir
# (one that agi_tree_config_path accepts). Never guesses: more than one
# candidate is a hard error, with every candidate listed on stderr.
# Safe under `set -euo pipefail` callers — a failed glob or zero matches
# returns 1 rather than raising, since it is always used as an if/command-sub
# condition, never as a bare statement.
_agi_find_root_descend() {
  local start="$1" base preferred

  # (a) Preferred, unambiguous match: <start>/<basename of start>-tree/
  base="$(basename "$start")"
  preferred="$start/$base-tree"
  if [[ -d "$preferred" ]] && agi_tree_config_path "$preferred" >/dev/null 2>&1; then
    echo "$preferred"
    return 0
  fi

  # (b) Otherwise glob <start>/*-tree/ and collect every dir that is
  # actually a project (has a config file). nullglob so a no-match glob
  # expands to nothing instead of the literal pattern; always restored.
  # Note this globs one level below $start rather than inside an `agi/`
  # subdir: the tree is outside the engine now, so <project>/<name>-tree
  # is where it lives. A dir matching *-tree that has no config file is
  # skipped, not treated as a candidate — that is what keeps the wider
  # glob from picking up unrelated directories.
  local -a candidates=()
  local d
  shopt -s nullglob
  for d in "$start"/*-tree/; do
    d="${d%/}"
    if agi_tree_config_path "$d" >/dev/null 2>&1; then
      candidates+=("$d")
    fi
  done
  shopt -u nullglob

  case "${#candidates[@]}" in
    0) return 1 ;;
    1)
      echo "${candidates[0]}"
      return 0
      ;;
    *)
      echo "ERR: ambiguous tree under $start/ — refusing to guess. Candidates:" >&2
      printf '  %s\n' "${candidates[@]}" >&2
      return 1
      ;;
  esac
}

find_project_root() {
  local start="${1:-$PWD}" d="${1:-$PWD}" graph_dir hit_git_boundary

  # Resolve to an absolute path FIRST, exactly as the Python half does
  # (`Path(start).resolve()`). Without this the upward walk below never
  # terminates on a relative argument: `dirname .` is `.`, and `dirname nodes`
  # is `.`, so `d` stops changing while the loop waits for it to become `/`.
  # Found 2026-08-31 by running `find-root.sh .` from a directory that is not a
  # project — it spun at 100% CPU, printed nothing, and had to be killed.
  # The live callers all pass `$PWD` and so never hit it, which is exactly why
  # it survived: the failure needs a relative argument AND no project above it.
  #
  # `cd -P` resolves symlinks the way `Path.resolve()` does, so the two halves
  # agree on a path reached through a symlinked directory too.
  #
  # A start that does NOT exist is still made absolute, because that is what
  # `Path.resolve()` does — it does not require the path to exist, and the walk
  # then correctly finds the project enclosing where the missing directory
  # would have been. Leaving it literal was the first attempt here and was
  # wrong twice over: it disagreed with the Python half, and `dirname nope` is
  # `.`, so it re-armed the very loop this block exists to disarm.
  if [[ -d "$start" ]]; then
    start="$(cd -P "$start" 2>/dev/null && pwd)" || start="$PWD"
  elif [[ "$start" != /* ]]; then
    start="$PWD/$start"
  fi
  d="$start"

  # Phases 0 and 1, interleaved in ONE upward walk rather than run as two
  # separate walks. That matters: two walks would let a distant .agi/ outrank a
  # legacy config sitting right next to you, which inverts "nearest enclosing
  # wins" at exactly the moment a repo is half migrated.
  while [[ "$d" != "/" ]]; do
    if graph_dir=$(agi_graph_dir_in "$d"); then
      echo "$graph_dir"
      return 0
    fi
    if agi_tree_config_path "$d" >/dev/null 2>&1; then
      echo "$d"
      return 0
    fi
    # Bound to `start`'s OWN repository, exactly as the Python half does
    # (locations.find_project_root). A `$d/.git` (file or dir) is the boundary
    # of the repository `start` is inside; an `.agi`/config found at that same
    # level (checked above) is start's own and already returned. Anything ABOVE
    # that boundary lives in a DIFFERENT (ancestral) repository and must never
    # be climbed into — a path under an unrelated nested fixture git repo must
    # resolve nothing, not the outer project's root.
    if [[ -e "$d/.git" ]]; then
      # Remember the walk exited via the `.git` boundary so the explicit "/"
      # probe below is SKIPPED (hypothesis:l4-find-root-sh-stops-at-the-git-
      # boundary-all-the-way). The python half never probes "/" after a
      # boundary break either — it goes straight to phase 2 descend — so
      # probing it here would let an ANCESTRAL project rooted at the
      # filesystem root be resolved from inside an unrelated nested repo,
      # the very one-probe-short divergence this fixes. Do NOT `return 1`
      # here: that would skip phase 2 descend too, creating the OPPOSITE
      # divergence (python descends into <start>/*-tree/, bash refuses).
      hit_git_boundary=1
      break
    fi
    d="$(dirname "$d")"
  done

  # The loop stops before testing "/" itself; test it explicitly so a project
  # at the filesystem root is not silently unreachable — but ONLY on a
  # boundary-free walk. On a walk that broke at a `.git` boundary, probing "/"
  # would climb into an ancestral repository the python half never reaches.
  # On a boundary-free walk the python while-True loop probes "/" as its own
  # final iteration (cur="/" → probe → parent==cur → break), so we must too.
  if [[ -z "$hit_git_boundary" ]]; then
    if graph_dir=$(agi_graph_dir_in "/"); then
      echo "$graph_dir"
      return 0
    fi
    if agi_tree_config_path "/" >/dev/null 2>&1; then
      echo "/"
      return 0
    fi
  fi

  # Phase 2: descend into <start>/*-tree/. Only reached when phase 1
  # found nothing above $start.
  local descended
  if descended=$(_agi_find_root_descend "$start"); then
    echo "$descended"
    return 0
  fi

  return 1
}

# When executed (not sourced), print the resolved root or exit 1.
# The error names the directory actually searched — the argument if one was
# given, $PWD only as the default. v1 always printed $(pwd), which blamed the
# caller's cwd for a failure under a path passed on the command line.
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  AGI_FIND_ROOT_START="${1:-$PWD}"
  PROJECT_ROOT=$(find_project_root "$AGI_FIND_ROOT_START") || {
    echo "ERR: no project found walking up from, or descending into <dir>/*-tree/ under, $AGI_FIND_ROOT_START" >&2
    exit 1
  }
  echo "$PROJECT_ROOT"
fi
