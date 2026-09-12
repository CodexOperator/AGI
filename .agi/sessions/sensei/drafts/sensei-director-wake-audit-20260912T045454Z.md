# audit — sensei-director gen 6 -> 7 (record 20260912T045454Z) — FIRST WAKE 0 (SL7.06 default: predecessor answered continue)

## WAKE = 0 rotation calls — target met
```
1 send belam "wake 0 (SL7.06 default)"          = work (report)
2-8 orientation, 7 calls, all (a)/(c):
   2  wc handoff.md in the WORKTREE → No such file (the alert names the MAIN path; the worktree has no copy)
   3  ls seats/ in both trees, status again
   4  dm reads for 4 posts by hand, wrong verb form → 5 `send.py read -h` (protocol learning) → 6 the same loop with --dm
   7  git ls-files seats/ in both trees, wc the MAIN handoff
   8  cat the MAIN handoff, log HANDOFF.md, grep seats.md
```
No ack, no ListAgents, no push: the rotation side is 0. What remains is a post finding its handoff and its dms by hand — both belong in STARTUP: (i) the handoff path the alert prints is MAIN's; a worktree post's STARTUP should print the handoff body (or `write.py ... read`), not leave the file to be found; (ii) unread dms per post are one `send.py rooms` (or `read <post>` — the inbox entry) — the 4-post loop with a wrong verb, then -h, then the loop again is 3 calls for one.

**Regression to name:** the row's `session_ref` is now EMPTY on MAIN for gen 7 (the ack used to back-fill it), and the alert printed the full session_id as the ref (`[013f1fb9-…]`), not a ListAgents short ref. `whois <short-ref>` for gen 7 will NO-MATCH; the `<post>#<fp>` label cut (key rides the row) is what closes this — until it lands, the rotating side's wrapper should back-fill session_ref from the join (L4.288) since the successor no longer does.

## OUT = 5 (target 1)
```
184 (scratchpad/handoff work) · 185 fetch+merge+push + pair loop · 186 card · 187 TaskStop (monitor) · 188 fetch+merge+push AGAIN · 189 rotate-self
```
Two merge+push rounds (185, 188) around the card — F14's "merge before rotate-self" done twice; the merge belongs inside rotate-self (cut, queued). TaskStop is a harness call the post pays for its own Monitor; a Monitor that ends with the session needs no stop.
