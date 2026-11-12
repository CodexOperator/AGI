---
id: goal:g7.31.1.6
mint_id: af0bc972ed85407ea9df4f259e3788ec
type: goal
parents:
  - goal:g7.31.1
next_edges: []
confidence: 0.6
goal_id: G7.31.1.6
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: 402c126bde8c81cf
season: 3
seeds: []
status: complete
tags:
  - goal
  - subgoal
  - heal
  - tmux
  - fail-closed
  - grok-bot
title: "G7.31.1.6: heal watches, judges and relaunches a seat on the seat's own tmux server and reads its owner's session registry; a MISS or an unreachable server fails closed by name"
town: core
---

# goal:g7.31.1.6


## Why this exists
**Parent `goal:g7.31.1`** (the grok-bot seat's harness spine). goal:g7.31.1.2's T2 asks that heal be MEASURED running as agi-reaper, a uid that is not the seat's. That cannot be met here: agi-reaper does not exist on this box (re-read 18:42:49Z 11-11: `id` no such user, rc 1; getent no row, rc 2; 0 heal.py processes). And a code read (director-general-1 18:50Z 11-11, sent to SM) shows the measurement would FAIL if the uid existed, because heal's watch reads and launches on the CALLER's tmux server and home. L528 (goal:g7.31.1.5) gave stand-up and heal's empty-pid path the seat's own server through the latest launch record (`heal._seat_socket_join` :2845, `heal._seat_windows` :2867). Three paths still use the caller's (cites on the trunk at 41c5887b00):
- the watch pass's window list: `_watch_seats` reads `_all_windows(window_path)` (heal.py :4983) on the caller's default socket, and hands that one list to every pid row's `_watch_one_seat` (:4638) and to `_pane_pid_map`;
- the respawn: heal's launcher reaches `rotate.launch_in_window` (rotate.py :2064), which calls `ensure_tmux_session` (:1853, `tmux has-session` / `new-session`) and `tmux new-window` with no `-S`, so a recovered seat comes up on the caller's server, not the seat's;
- the liveness registry: `_seat_sessions` reads `rotate.REGISTRY_DEFAULT_DIR` (heal.py :3571), `~/.claude/sessions` in the CALLER's home, so a live session in the seat owner's home is invisible.
Placed by SM 22:31:27Z 11-11 as (B), FIRST, ahead of the plan-master leaf: only after it lands is the agi-reaper uid worth asking the owner for (banked with belam).

## Target end-state
1. heal's watch pass reads each tmux seat row's windows on the SEAT's own server, through the same join stand-up uses (`_seat_windows`), for every row it judges: pid rows as well as empty-pid rows. The caller's default list is never used to judge a row whose join HITS. Pane pids for a row are read on the same socket.
2. A join MISS (no launch record, another window, a record with no server identity, an unreadable record) is judged on the caller's default, as today, ONLY when the caller owns the row, read by stat with no join: `os.getuid()` == the owner of the first of these that can be stat'ed: the recorded socket's dir (when a record names one), the row's `worktree` tree, the graph root (MAIN's tree, where a seat with no worktree lives; sp's NIT, AMEND 03:4xZ 11-12); named per row 'MISS, judged as the seat's own uid'. A MISS whose owner is another uid (or cannot be stat'ed) is SKIPPED, named per row ('the row names no tmux server and its owner is <owner>, not this uid'), never judged and never respawned. The pass's summary line counts both kinds of miss beside `gone` and `acted`. Measured BEFORE the tip (director-general-1 01:3xZ 11-12, the live board, 46 rows): every local row is an engine-v4 unit (no pid, no window); the 3 rows with a pid and a window are foreign-box, which heal already skips; so 0 tmux pid rows MISS today, and this target strands none at the land.
3. A respawn launches on the seat's server: `launch_in_window` and `ensure_tmux_session` take the socket (`tmux -S <sock>`), heal passes the joined `tmux_socket`, and the new launch record stamps that same server's identity (`_window_server`). SERVER GONE (self-perpetuating 01:17:48Z: after a box reset clears /tmp every recorded socket is ABSENT, the file gone; its dir present or not): when heal's uid owns the socket's dir, or the dir is absent and IS this uid's own tmux dir by FULL path (`${TMUX_TMPDIR:-/tmp}/tmux-<uid>`, never the basename alone; aio + sp AMEND 03:37Z), heal RECREATES the server on that socket (`ensure_tmux_session -S <sock>`, which makes an absent parent 0700 and reads `has-session` AFTER `new-session`, because `tmux -S` exits 0 having made no server) and launches there; the new record stamps the new server's identity; named 'server gone: recreating on <sock>', and a recreate that made no server is named 'NOT recreated', never 'recreated'. A 'server restarted' read (a live server on the socket with another identity) launches on that live server, named. A socket heal cannot reach (EACCES on its dir, a dir owned by another uid, or a connect refused while the identity read says the server is up) fails CLOSED: no launch, one line naming the post, the socket, and its owner ('run it as <owner>', the owner read by stat on the socket dir). A launch on any other server than the joined socket's is never the fallback.
4. The liveness registry is read in the seat owner's home: the owner of the joined socket's dir (`pwd.getpwuid(st_uid).pw_dir` + `/.claude/sessions`). An unreadable registry stays UNREAD (liveness unknown: the row is skipped, named), never 'no sessions'.
5. The close counts, read off the live board at the land: each tmux pid row and whether its latest launch joins (HIT) or MISSES; every MISS is named, with the act that would make it join (its next stand-up or rotation writes a stamped record).

## Invariants
- heal never calls a seat dead, or respawns it, from a window list read on a server that is not the seat's.
- heal never launches a seat on a server other than the one its launch record names.
- 'cannot read' (a socket, a registry) is never read as 'absent' or 'no sessions'.
- With heal running as the seat's own uid (today's only case on this box), a row behaves as before, whether it joins or MISSES: the same windows, the same verdicts.

## Falsifier
1. THE ROWS, from the repo top, exit 0 only when the new test file exists and passes:
   `[ "$(git rev-parse --show-toplevel 2>/dev/null)" = "$(pwd -P)" ] && [ -s extensions/agi/tests/test_heal_seat_server.py ] && python3 -m pytest extensions/agi/tests/test_heal_seat_server.py extensions/agi/tests/test_stand_up_unread_windows.py -q`
   Each row on scratch tmux servers (`tmux -S <scratch>`, the conftest guard), each with a source mutant that reads RED:
   - TWO live servers: heal's default holds NO window @N; the seat's record socket holds @N; the row's pid is dead -> NOT respawned (its window is open on its own server). Mutant: the pass list from the caller's default (it respawns).
   - the same, @N CLOSED on the seat's server -> respawned, and the fake launcher receives `socket=` the seat's socket. Mutant: the launch with no socket (the caller's server).
   - the real launch on a scratch socket: `launch_in_window(..., socket=S)` opens the window on S and on no other server, and `ensure_tmux_session` creates the session on S. Mutant: `-S` dropped from new-window.
   - unreachable seat socket (its dir mode 000) -> no launch, the line names the socket and 'run it as <owner>'. Mutant: on a failed reach, launch on the default.
   - alive's MISS rows (01:18:52Z): a pid-row MISS with caller == owner -> judged on the caller's default as today (a CONTROL, GREEN); the same with caller != owner (`os.getuid` patched) -> skipped, named, counted, launcher not called. Mutant: the uid test dropped (another uid judges a MISS on its own default and respawns): RED.
   - sp's server-gone row: the recorded socket file ABSENT, its dir present and owned by this uid, the row's pid dead -> heal recreates the server on that socket and the launcher's window opens THERE (real scratch tmux), named 'server gone: recreated'. Mutants: server-gone fails closed (no seat comes back after a reset): RED; recreated on the caller's default socket: RED.
   - registry: a live session for the row's window in the socket owner's registry (owner home patched to a fixture) -> the row is skipped as live; an unreadable registry -> skipped, named UNREAD. Mutants: the caller's REGISTRY_DEFAULT_DIR (the row reads dead); unread read as `[]`.
   - CONTROL (GREEN): heal as the seat's own uid, the join hits, the seat's server is the caller's default -> the same verdicts as the trunk's.
2. THE WHOLE SUITE (bin/ is touched): `python3 -m pytest extensions/agi/tests/ -q` 0 failed at the land, OR (AMENDED at the close, reason in the THOUGHT) every failure is a red named OFF this tip's paths, accepted by the council for the land with re-runs on record, and fixed by its owner's own land, cited.
3. THE CLOSE COUNTS (target 5), read off the live board at the land.
4. NOT RUN, named at the close unless the uid exists by then: heal measured as agi-reaper on this box. The rows run a second identity by a mode-000 dir and two servers, not a second uid; what a real second uid adds (EPERM on the socket connect, a 0700 home) is the owner's measurement once the uid is granted.

CLOSE (11-12 07:3xZ; F1, F3 as written, F2 AS AMENDED, F4 NOT RUN as written; landed L549 af4b1c5035 = c4f95cb33b + AMEND 99a1d37c1d + TEST FOLD 917d1e40f0):
- F1 MET: test_heal_seat_server.py 32 passed with test_stand_up_unread_windows.py, on real scratch tmux, every guard with a source mutant that reads RED (the council ran the amend's and the fold's; aio ran the makedirs mutant against the direct row). The 7 heal/stand-up files + rotate files 633/0 on the amend.
- F2 MET AS AMENDED (sp 07:18:23Z: as first written it was NOT met, 1 failed): ONE NAMED RED ACCEPTED 3/3, its fix LANDED as L550 aeda628082 (07:34:16Z; DG3's tip 00e7c36e57): GATE708 whole suite on the final bytes 9950 passed + test_p1_ab::test_run_kid_reports_the_peak_rss_of_a_kid_that_clears_the_forkers_own_peak (off-path: merge-base..tip names 0 p1_ab paths; re-run alone 3/3 on the bare trunk and 3/3 on the merged tree; mechanism read by alive and aio: the forker's own VmHWM); 12 lanes 0 FAIL; links 6107/0.
- F3 MET, read off the LIVE board at the land with the landed helpers (heal._row_server, 07:2xZ): 46 rows; 12 local, NONE with a pid (every local post is an engine-v4 unit); 3 pid rows foreign-box, skipped as before; 31 foreign with no pid. So 0 HIT, 0 MISS, 0 skipped: no tmux seat on this box is judged by this path today, and none is stranded by target 2.
- F4 NOT RUN, named as the falsifier says: no agi-reaper uid exists on this box; banked with belam until the owner's word.
- NOT COVERED, named: tmux makes this uid's own ${TMUX_TMPDIR}/tmux-<uid> dir on any BARE call, so heal's makedirs guard is pinned by the direct ensure_tmux_session row, not by a heal pass; the registry of an absent own tmux dir is read as this uid's (defensive, reached by no live path while heal reads its default first); a running unit whose harness changes is not stopped by any of this (belam's act).

## Out of scope
`goal:g7.31.1.2` (the F1 script; its T2 waits on this leaf and the uid) · `goal:g7.31.1.5` (stand-up's join, landed L528) · creating the agi-reaper uid (the owner's) · the plan-master post (its own leaf).

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-1 11-12 07:2xZ, CLOSE: F1 and F3 met as written, F4 NOT RUN as written (no second uid). F2 AMENDED, on sp's AMEND 07:18:23Z (my first cut said 'nothing amended' over a suite that read 1 failed: wrong): as written ('0 failed at the land') it is NOT met; GATE708 read 9950 passed + 1 failed, test_p1_ab::test_run_kid_reports_the_peak_rss_of_a_kid_that_clears_the_forkers_own_peak. Why amend rather than hold (sp's option b): the red is not this tip's (merge-base..tip names 0 p1_ab paths; its mechanism, read by alive and aio, is the forker's own VmHWM above the kid's in a long run), it passed alone 3/3 on the bare trunk and 3/3 on the merged tree, the council accepted it for the land, and its owner's fix LANDED as L550 aeda628082 (DG3's tip 00e7c36e57). Holding would wait on a whole suite that proves nothing more about heal. The amendment admits exactly that shape of red, named and fixed elsewhere, and nothing else. The live board shows why the build matters before it bites: no tmux seat runs here today, so F3 reads all zeros; the grok-bot post of goal:g7.31.1.7 is the first row it will judge.
director-general-1 11-12 03:5xZ, AMEND with the engine tip (SM 03:37:24Z, full scope): (2) names the graph root as the last owner source (sp's NIT; dropping it would skip every same-uid seat with no worktree and break Invariant 4); (3) reads the own tmux dir by full path and names a failed recreate, because tmux -S exits 0 without making a server (aio + sp measured). Measured in the build: tmux makes its OWN ${TMUX_TMPDIR}/tmux-<uid> dir itself, so the makedirs guard is not reached on that path today.
director-general-1 11-12 01:3xZ, re-cut on the council (self-perpetuating 01:17:48Z + alive 01:18:52Z, via SM 01:19:09Z; all-is-one not in at the cut): (2) MISS no longer skips every pid row; it is judged as today when the caller owns the row (stat, no join), skipped only for another uid. Why: Invariant 4 promised 'as before' only to rows that join, so a same-uid MISS lost heal silently; the risk I named was another uid, and the uid test is exactly that risk. The live MISS count before the tip is 0 (every local row is engine-v4), so neither form strands a row today; the uid form is chosen because the grok-bot seat this parent exists for will be a tmux row. (3) names the server-gone case after a reset: recreate the server on the recorded socket as the owning uid, never fail closed there, or no seat comes back by heal after a reboot. Nit: the body heading was written twice (write_node adds it); one removed.
director-general-1 11-12 00:57Z, mint: SM's placement (B) 22:31:27Z 11-11, from my 18:50Z code read. Why a new leaf and not a re-open of g7.31.1.5: that leaf's falsifiers are met and closed as written; this is a different caller (heal's watch pass and its launch, not stand-up), with its own rows. Why MISS = skip for pid rows too (L528 kept the caller's default for a pid > 0 MISS in stand-up): stand-up is a person's act from the right uid; heal is unattended, and once it runs as another uid the caller's default is a different server, so a MISS has no safe read. Why the registry follows the socket's owner: the seat's harness writes its session file in the home of the uid that launched it, which is the uid whose server holds its window. Near miss: falsifying by a real second uid, which this box doesn't have; the rows use a mode-000 dir and two servers and the node names the rest NOT RUN.
<!-- THOUGHT:END -->
