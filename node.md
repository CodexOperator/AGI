---
id: hypothesis:the-map-v0-git-graph-shell-piped-read-only-to-loopback-web
mint_id: 9077830bda574288839b82e9de15b9cc
type: hypothesis
parents:
  - goal:g7.16.1.11
next_edges: []
edited_by: director-general-2
scaffold_hash: 5a9e93f8c46c2e95
season: 2
testable_claim: one shell script renders git's own --graph over every branch and worktree, each coloured by its v0 stage (landed/committing/writing/claimed), served read-only on a loopback port from a config cell by a checksum-verified ttyd-class binary under a user unit, anonymize-filtered, a refresh under 2 s
title: "THE MAP v0: git log --graph over every branch + worktree, stage-coloured, piped read-only to 127.0.0.1 by a ttyd-class package (owner 06:1xZ 10-01)"
town: local-maxxing
---
# hypothesis:the-map-v0-git-graph-shell-piped-read-only-to-loopback-web

## Measured
Owner 06:1xZ 10-01 (verbatim on goal:g7.16.1.11): "Just a shell piped into the web that renders everything in-shell ... use built in graph render tools don't reinvent the wheel. Or lightweight packages others made". Laned by belam 06:19Z -> sanctuary-master -> DG2 06:21Z ("dispatch now"). On this box at 06:2xZ (date -u): graphweb on 127.0.0.1:8765 (transient unit agi-graphweb) keeps running; no ttyd-class binary on PATH; arch x86_64. Repo scale: 729 worktrees, ~1,050 refs/heads, 637 refs/archive/worktrees, ~9,450 refs/grid/* (per-node version refs -- NOT branches). `git log --graph --oneline --color --branches --remotes -n 200` = 0.16 s. The post-wrapper tracking (agi-track / agi-turn) is not on PATH yet (only in doc:g716111-stage25-engine-v4c and doc:radically-simple-engine).

## CLAIM
ONE shell script renders `git log --graph --color` over every branch (local + remote + each worktree's HEAD as it appears; refs/grid/* and refs/archive/* excluded), refreshed in place, with every ref/worktree coloured by its v0 stage -- landed (tip reachable from the town trunk) · committing (worktree with staged changes) · writing (worktree dirty, nothing staged) · claimed (branch/worktree with no commit past its merge-base with the trunk) -- and the agi-track read named in the script as the v1 swap. An EXISTING lightweight package (ttyd-class, a released static binary in ~/.local/bin, its sha256 checked against the release's published sums, user-level, no sudo) serves that script READ-ONLY on 127.0.0.1:<port> from a config cell (not 8765), under a user systemd unit. The page carries no key, secret, home path or hardware name: the render is filtered through anonymize's token classes.

## Dispatch line
kid (Sonnet 5.5, isolated worktree): FIRST reply with the config cell you will add (name + keys) and the package + release you will install, then build. config-max: host, port, refresh seconds, commit window, worktree-scan bound, package version + sha256, unit name -> ONE `map` cell in .agi/config.json, read by the script; never a literal in the script. template-max: none. No new renderer: git's own --graph does the drawing.

## FALSIFIERS
1. curl http://127.0.0.1:<port>/ from this box does not return the ttyd page, OR the port listens on anything but 127.0.0.1.
2. The served terminal accepts client input (a writable flag, or a keystroke over the websocket reaches the shell).
3. The anonymize filter test fails: a planted home path / secret-shaped token / live hardware name in a branch name or subject survives into the render.
4. One refresh costs > 2 s wall or walks refs/grid/* (the 729-worktree stage scan must be bounded by the config cell, e.g. only worktrees whose index/HEAD changed inside the window).
5. The binary's sha256 differs from the release's published sum, or anything is installed outside ~/.local/bin, or sudo is used.
6. A diff touching anything outside FILE SCOPE, or graphweb (8765) stopped or changed.

## TESTS
extensions/agi/tests/test_map_sh.py (new): render on a tmp repo with 4 worktrees in the 4 stages -> each ref carries its stage colour; refs/grid/* excluded; the anonymize filter redacts a planted home path + a secret-shaped token; the config cell is read (port/refresh changed -> the script follows). Live proof in the experiment: the unit active, `ss -ltn` shows 127.0.0.1:<port> only, curl returns the page, one refresh timed on the live repo.

## FILE SCOPE
extensions/agi/bin/map.sh (new) · extensions/agi/bin/anonymize.py (a `filter` verb only, if the classes need one) · .agi/config.json (the `map` cell) · extensions/agi/tests/test_map_sh.py (new) · ~/.local/bin/<package> (off-repo, checksum-verified).

## CEILING
script <= 150 lines · anonymize.py +30 · tests +120 · 0 other production lines.

## CORRECTIVE DH.1 -- closes the director's harvest residue on 9a0e12f86..19151e383 (ttyd's title frame carries the box hostname)
BASE      CONTINUE ON worktree-agent-a2c7f206afa857d38 tip 19151e383 (its own worktree). No merge. Never rebase.
1. HOSTNAME ON THE WIRE -- ttyd 1.7.7 sends a SET_WINDOW_TITLE frame "<command> (<hostname>)" with no server option to drop it; titleFixed only hides it client-side, the frame still crosses the socket (falsifier 3's class: a host name on the page). Fix: swap the package for one whose title is a server-side template (gotty, github.com/sorenisanerd/gotty, the latest release's linux amd64 static binary, sha256 checked against that release's published checksums BEFORE chmod; read-only by default -- never --permit-write; --address/--port from the cell; --title-format a fixed string with no {{.Hostname}}), OR keep ttyd behind a filter only if that stays inside the CEILING. True when fixed: capture EVERY websocket frame the server sends for 10 s after connect and print only `hostname in frames: no` (compare in-process against socket.gethostname(); never print the name); the input-frame probe still creates nothing.
2. PACKAGE CELL -- package / version / bin / sha256 in the `map` cell follow the swap; map.sh serve still refuses a binary whose sha256 differs from the cell.
3. OLD BINARY -- if the package is swapped, remove ~/.local/bin/ttyd (this round installed it; nothing else uses it: confirm with `systemctl --user list-units 'agi-*'` before removing).
4. TEST -- test_map_sh.py gains one row: serve's argv (built by map.sh, the binary stubbed) carries no write flag, binds the cell's host, and its title is the fixed string.
5. COLD FRAME -- disclose, do not fix: a cold first render measured 8.7 s / 41 s at load > 17; re-time 3 warm renders on the live repo and paste them.
ANON      no user name, home or repo path value, host name or IP other than 127.0.0.1; patterns write <user>
FILE SCOPE extensions/agi/bin/map.sh · .agi/config.json (the `map` cell) · extensions/agi/tests/test_map_sh.py · ~/.local/bin/<package> (off-repo)
CEILING   HARD CAP: 1 kid · map.sh <= 150 lines total · tests <= +40 over 19151e383 · 0 other production lines · Sonnet 5.5 lane · 0 USD

## CORRECTIVE DH.2 -- closes the Sonnet review of 675dbf1e8..9cb9ad4f3 (accept_with_residue)
BASE      CONTINUE ON worktree-agent-a2c7f206afa857d38 tip 9cb9ad4f3 (its own worktree). No merge. Never rebase.
1. HALF A SECRET SURVIVES -- map.sh:50 vs :63 -- `%<(subject_cols,trunc)` cuts a subject BEFORE `anonymize filter`, so a planted secret renders as its prefix. True when fixed: the filter runs on the FULL subject, truncation after it; the test plants a secret straddling the cut and asserts no prefix of it (>= 4 chars) survives.
2. UNTRACKED-ONLY READS AS CLAIMED -- map.sh:30 (-uno) + :44 -- a worktree adding only new files is "writing". True when fixed: untracked files count as writing; warm render on the live repo still < 2 s (paste 3 timings; MAIN stays in the scan).
3. COMMITTED-NOT-LANDED HAS NO COLOUR -- map.sh:41-44 -- add a 5th v0 stage `committed` = tip has commits past its merge-base with the trunk, nothing staged or dirty (a clean worktree ahead of the trunk, or a branch with no worktree that is not merged); legend + test row. Every ref in the decoration then carries a stage colour.
4. THE UNIT IS NOT IN THE BYTES -- add a `unit` verb: systemd-run --user --unit=<cell unit> --working-directory=<toplevel> -p MemoryMax=<cell> -- bash <self> serve; refuse if the unit is already active. Do NOT run it against the real unit name: prove it with MAP_CONFIG pointing at a tmp copy of the cell whose unit is agi-map-proof, then stop that unit.
5. HARDENING -- pass the write flag OFF explicitly (--permit-write=false or the release's equivalent; check `gotty --help`) against an inherited env; cap connections from the cell (--max-connection); the 4-5 stage colour codes and the xargs -P width move into the cell (config-max), read once.
DEMOTED (no fix, disclosed in a map.sh comment): unstaged edits in a worktree whose HEAD/index is older than the window are not seen -- the bound is falsifier 4's requirement; the v1 agi-track read is the named fix.
ANON      no user name, home or repo path value, host name or IP other than 127.0.0.1; patterns write <user>
FILE SCOPE extensions/agi/bin/map.sh · .agi/config.json (the `map` cell) · extensions/agi/tests/test_map_sh.py
CEILING   HARD CAP: 1 kid · map.sh <= 150 lines total · tests <= 180 lines total · 0 other production lines · Sonnet 5.5 lane · 0 USD

## CORRECTIVE DH.3 -- closes the Sonnet re-review of 9cb9ad4f3..04e317ac1 (accept_with_residue)
BASE      CONTINUE ON worktree-agent-a2c7f206afa857d38 tip 04e317ac1 (its own worktree). No merge. Never rebase.
1. TRUNK CHECKOUT READS CLAIMED -- map.sh:51 -- a clean worktree whose checked-out branch IS the cell's trunk reads `landed`; every other clean worktree with no commit past its merge-base stays `claimed` (a live worktree is a live claim). Test row: a clean trunk checkout -> landed colour.
2. LOCALE CUT -- map.sh:72 -- pin a UTF-8 locale for the awk cut (export LC_ALL=C.UTF-8 or the cell's value) so a multi-byte char is never cut mid-sequence under a unit with no LANG; test row under LC_ALL=C in the caller's env.
3. SILENT EMPTY FRAME -- map.sh:71 -- a failing `anonymize filter` prints ONE error line (`map: filter failed, frame withheld`) and never the unfiltered render (pipefail or an explicit status check); test row with the filter forced to fail.
4. QUOTING + MISSING KEY -- map.sh:90 quote the MAP_CONFIG setenv and make it absolute; map.sh:25 every required key checked once after the eval -> `map: cell key <k> missing` exit 2 (the cell's key names validated against [a-z_]+ before eval).
5. COMMENT -- map.sh:10-12 the demoted limit reads "unstaged or untracked edits".
DEMOTED: config_max on `--config /dev/null` / `-maxdepth 2` / the row fallback = invariants, not tunables (a configurable --config would reopen falsifier 2); raw ESC in a subject = the same exposure git's own cut had (not a regression).
ANON      no user name, home or repo path value, host name or IP other than 127.0.0.1; patterns write <user>
FILE SCOPE extensions/agi/bin/map.sh · extensions/agi/tests/test_map_sh.py
CEILING   HARD CAP: 1 kid · map.sh <= 150 lines total · tests <= 200 lines total · 0 other production lines · Sonnet 5.5 lane · 0 USD

## CORRECTIVE DH.4 -- closes the Sonnet re-review of 04e317ac1..75f8e43b6 (accept_with_residue)
BASE      CONTINUE ON worktree-agent-a2c7f206afa857d38 tip 75f8e43b6. No merge. Never rebase.
1. WATCH CADENCE UNPROVEN -- test_map_sh.py:134-135 -- the 6 s / >= 2 redraws window passes for any sleep up to ~5 s: keep the long timeout, require >= 4 redraws at the fixture's refresh_s (or assert the median redraw gap is within 3x refresh_s), so a hardcoded sleep fails it.
2. SETENV UNTESTED -- test_map_sh.py:147-149 -- one `unit` test row with MAP_CONFIG set to a RELATIVE path holding a space: the stubbed systemd-run argv carries ONE `--setenv=MAP_CONFIG=<absolute path>` argument.
DEMOTED: the C.UTF-8 pin has no fallback -- the locale exists on this box (the re-review ran it); a missing locale is a box finding, not this round's.
FILE SCOPE extensions/agi/tests/test_map_sh.py only
CEILING   HARD CAP: 1 kid · 0 production lines · tests <= 200 lines total · Sonnet 5.5 lane · 0 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.4: Sonnet re-review of 04e317ac1..75f8e43b6 = accept_with_residue -- DH.3 items 1-5 closed; 1 residue (the watch test widened to 6 s / >= 2 redraws no longer proves refresh_s) + 1 note worth a row (the absolute quoted MAP_CONFIG setenv untested); demoted: C.UTF-8 fallback (present on this box). Director at 75f8e43b6: test_map_sh 8 passed, test_anonymize_guard 52 passed, test_bin_help_smoke 73 passed on a rerun (a first run errored 81/81 in 0.85 s, not reproduced); MAIN renders 2.18 / 0.62 / 0.47 s, no host or home in the frame.
<!-- THOUGHT:END -->
