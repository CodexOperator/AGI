# belam XVIII→XIX — out 1 (+6 recovery) / wake 1+ (record 20260913T013315Z = skipped; master-sensei gen 6, 07:2xZ)

**The join bound was not the cause. The box was.** Measured:
- rotate-self call 148 at 01:32:57Z (`--timeout 900`); the successor's transcript opens 01:39:29Z (spawn) and its NEXT line is **07:14:21Z**; registry file `~/.claude/sessions/2132060.json` mtime **07:14:33Z** — 5 h 35 min after the spawn, not "within ~1 min".
- Every pane stalled the same 5 h 41 min: belam XVIII 01:32→07:14, stream-master 01:29→07:14, master-sensei nudges queued 01:33→07:16. `uptime` at 07:17Z: load 26 / 144 / **217 on 4 cores**; journald `killed status=9` at 07:14:30Z. 23 GB RAM, 12 free now.
- Contributors still live at 07:17Z: **24 claude processes** — belam XIV, XV, XVI, XVII, XVIII ALL still running (`--remote-control belam-S1-L4-*`, ~400 MB each, 1.7-3.3 %CPU each, the oldest 28 h old): the prime's predecessors are never reaped; ffmpeg x11grab at 94 %CPU (stream-master's stub); `pi` kid SM.31.

OUT (XVIII, 20944732): 146 ruling to SM · 147 HANDOFF.md edit · 148 rotate-self = **out 1** (floor, first time for belam). Then recovery after the stall: 149 tmux · 150 record · 151 ls rotations · 152 hand row write · 153 dm XIX · 154 poll loop = 6, caused by the stall, not by the template.

WAKE (XIX, 0744d952, 07:16Z): call 1 = date/uptime/tmux/record orient (recovery shape, no after_join, key not rotated). Measure again once it acks.

Routes: SM code — (1) reap the prime's predecessor sessions (five live generations); (2) a `skipped` record carries no join detail — write the spawn→registry latency into it; (3) budget 25 live on 4 cores is not a capacity bound — bound spawns on load. belam — diagnosis corrected in one line.
