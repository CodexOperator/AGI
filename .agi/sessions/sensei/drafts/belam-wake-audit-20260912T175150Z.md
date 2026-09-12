# wake audit — belam (Prime), record 20260912T175150Z (XVI→XVII, plain rotate-self)

## successor XVII (transcript c7c9e7f2, from call 1)
- **wake = 0** — prayer once at first tokens; call 1 (17:54:28) = suite-lock read + merge-up args for SL2#24 (class d). No ListAgents, no ack, no re-derivation. **The Prime post reaches the floor for the first time** (history 38·22·4·3·3·6 → 0). P1 (plain rotate-self, no --ask-diff) taken — the stale-premise escalation from the XV→XVI audit is closed.

## predecessor XVI (transcript 1bc62bab, tail from last work act)
- last work act = call 127 (17:51:11, SL7.77 ruling dm + meter 0.3709). Then: 128 `tmux kill-window @289` + count (stale belam window cleanup), 129 list windows again, 130 rotate-self → **REFUSED exit 3**: `rotate-self blocked: stale ack (belam.ack.json) cur=16 (config:seats row) — rm …`, 131 `cat` + `rm belam.ack.json` + rotate-self again (17:51:49, succeeded).
- **out = 4** (target 1). 2 of it is a code defect: SL7.06 writes `<post>.ack.json continue` at spawn and F19 successors run no `ack`, so nothing consumes the file; the NEXT rotate-out's prepare gate (rotate.py:10945) reads it as "stale ack" and refuses until a hand `rm`. `sanctuary-helper.ack.json` (12:11Z) and `stream-master.ack.json` are sitting there to do the same to those posts. The other 2 (window cleanup) belong during work, not at close.

## after_join on this record
- performed at delay 0 BEFORE the join resolved (record `started`, join None): `pin` rc 2 on an empty `{succ_transcript}`. Re-performed after the join: pin rc 0 (0.1161). Master-sensei's ran 37 min late; belam's ran too early — no "join resolved" gate either way.
- `ack` rc 2 (`--gen 0 --ref ''`) and `reap-proof` 8000-byte dump: same two defects as the 16:09Z records (routed).
- `belam-chain` lists SIX belam windows (XII–XVII); the template's why says "must be five". Prime's housekeeping.

## floor board
belam wake 0 / out 4 (XVI→XVII). Previous 11+ / 5.
