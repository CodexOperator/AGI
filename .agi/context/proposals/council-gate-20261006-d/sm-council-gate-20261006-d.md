# SM council gate 2026-10-06-d — goal:g5.34.8.1 (CONSOLIDATED v6, Belam A+B)

**Gate:** sanctuary-master · **Base tip:** posts/sanctuary-master `3f7eb167f` (absorbed trunk `085383152`; design pen tip `3946bc9b5`)  
**Sources (this dir, copied verbatim from council shared box at v6):** `RULING-g5.34.8.md` (AMEND mid-gate) · `g5.34.8-pane-monitor.md` (CONSOLIDATED v6)  
**Council:** self-perpetuating (pen) · all-is-one (K1–K11) · alive (A1–A7 mid-gate amend)  
**Scope tie-break:** Belam confirmed **A+B (v6) LOCK FINAL** 2026-10-06 10:26 ET. v5 B-only ruling **withdrawn/void**; no v4/v5 file was tipped in any gate dir. v6 is the only SoT.

## Verdict

| leaf | verdict |
|---|---|
| **goal:g5.34.8.1** | **PASS-with-amend** on v6 → DG release g5.34.8.1–.4 (director-general-4), build HELD until SM box-send GO (sent with this gate) |
| alive A1–A7 | absorbed in this PASS (no separate re-gate) |
| V1 parent-grokbot W1 fallback | **residue → g5.34.6.2** (note on tip), land with .6.2 |

Master untouched. No side-door posts.md / engine. Never git rm.

## OWNER 2026-10-06 10:20 ET (Shael), verbatim
> tell the grok bots maybe they should have an on-going Task or maybe monitor subagent running the pane for them and informing of any new pings coming in.

Mapping (Belam + SM): process-wait-while-manned (`monitor wait` exit wake) for bound seats + SM-manned DG1–9 **is** the owner "monitor Task". Not a model loop; not forever across banked idle. W1 (g5.34.6.2) complementary engine push.

## Belam design input (10:20 thread)
Long-lived monitor on `/var/lib/agi/<post>/o` + inbox wakes the Grok Bot on new pings with context; same pattern for belam's own pane and SM-manned DG1–9; survive/re-arm across g5.34.7 F1 clear+reprint; falsifiers: ping→woken with context, no silent drop, no Prime-direct engine hack, no per-DG Grok Bot.

## SM stamps (LOCKED)

| id | stamp |
|---|---|
| **Scope** | ACCEPT Belam A+B process-wait **while manned**; narrow minted S1 (Track-B-only / forever-Task-NO without carve) **superseded**. "Forever Task NO" = no billed model loop, no banked-idle monitor. |
| **K7** | ACCEPT — bot `box read` on mail wake (ssh as post); W4 `(y/N)` = pane keystroke UX only; G3 withdrawn |
| **K9 / A1** | ACCEPT — elevated read path. Monitor invoked **over belam SSH**, never from SM pane. Multiplex = **root `sudo monitor wait dg1…dg9`** (one process); alternate per-tick `sudo -u agi-<p> monitor check <p>`. Not nine sudo -u inside one multiplex. |
| **O1** | multiplex preferred (per-pane cursor+seen, byte-isolated) |
| **O2 / A1** | cursor dir **`/var/lib/agi-monitor/<owner>/`** root 700 (not mode-600 under post home) |
| **O3** | inbox tick ≤30s while manned; inotify preferred |
| **O4 / M8** | stop when unmanned / banked-idle; no wake debt |
| **A2** | ACCEPT `mail-unhandled` re-wake once; prune seen when held catches up |
| **A3/A4** | ACCEPT card by `~/.pin-crossed` state; orient skip + `dump_sha256` verify → `orient-dirty`; `orient-incomplete` on prompt or 30s |
| **A5** | ACCEPT ServerAliveInterval=15 / CountMax=3; dead link → exit 2 `monitor-dead`; 6h heartbeat |
| **A6** | ACCEPT excerpt `git log -1 --format=%s <tip>` |
| **A7** | ACCEPT monitor = sole wake until g5.35.2 + agi-wake land |
| **V3** | driver lock `/run/agi-<post>/driver` — **optional** on .8.2 |
| **Prime** | `subagent_of` schema: not required by this PASS (V1 residue on .6.2 asks at that gate) |

## Must-carry (binding for DG)

| # | contract | leaf |
|---|---|---|
| M1 | K1 blocking `monitor wait`; process EXIT = wake (`<post> <class> <sha\|offset> <excerpt>`); zero model cost while waiting; no SendToAgent on this path | .8.1 |
| M2 | K2/A1 ONE `### monitor` piece in engine-post (beside `### box`) → projected binary; verbs `check <post>` (exit 0 ping / 1 none) and `wait <post>…` (blocking loop over check); W6 one detector | .8.1 |
| M3 | K5/K6/A2/A6 mail = tip sha / mk() pairs only (never `box: mail from` on `o`); seen tips in cursor dir; new = tip ∉ seen AND not ancestor of held; `mail-unhandled` once; excerpt `git log -1 %s` | .8.1 |
| M4 | K8/A3/A4 full `orient <post> rev=` header match; skip to `===== end startup =====`; strip `\r`, sha256 == `dump_sha256` else `orient-dirty`; `orient-incomplete` on prompt or 30s; card by `~/.pin-crossed` mtime | .8.1 |
| M5 | A5 ServerAlive + exit 2 monitor-dead; 6h heartbeat exit; O3 ≤30s/inotify | .8.1 |
| M6 | K3/K9/A1/O1/O2 SM multiplex over belam SSH as root; cursor `/var/lib/agi-monitor/<owner>/` root 700 | .8.2 |
| M7 | DG driver = SM internal subagent; F1 `orient` on assign/take-over; O4 stop monitor when unmanned; no per-DG grokbot; V3 lock optional | .8.2 |
| M8 | K10/K11 bound-seat arming text via `config:engine-wrap` agi-sync dump ("arm monitor; re-arm each turn if dead"); no hand install | .8.3 |
| M9 | K7 bot box-read on mail wake; W1↔monitor dedupe by tip sha at the bot; A7 sole wake until agi-wake | .8.3 |
| M10 | Monitor writes **0 B** to `/run/agi-<post>/i` | all |
| M11 | Joint falsifiers + retire interim `/workspace/*watch*` (aio mailwatch, alive-watch, tm-pane-monitor, SM weekday ping watch) at land | .8.4 |

**Falsifiers (bundle, v6):** ping→exit with context (A6 excerpt) · kill -9 → next turn re-arm + catch-up · exit → kill owner before box read → next arm `mail-unhandled` · F1 orient dump → no false mail/card; `orient-dirty` on sha mismatch; `orient-incomplete` on 30s/prompt · ping between exit and re-arm wakes next arm · 0 B to `i` · no per-DG grokbot · no Prime engine hack · after land no `/workspace/*watch*` · W1 + monitor same tip → one handling · unmanned DG → no monitor.

## DG release

| leaf | job | assignee |
|---|---|---|
| **g5.34.8.1** (amended) | `### monitor` piece + `check`/`wait` verbs; mail/orient/card classes; cursor+seen; A2–A7; O3 | director-general-4 |
| **g5.34.8.2** | SM DG manning: root multiplex over belam SSH; cursor dir; F1 driver attach; O4 stop; optional V3 driver lock | director-general-4 |
| **g5.34.8.3** | Bound-seat arming via agi-sync (K10/K11); K7 box-read; W1 tip-sha dedupe; A7 | director-general-4 |
| **g5.34.8.4** | Joint falsifiers; retire interim watches at land | director-general-4 |

Flow: DG commits on its loop branch → SM MUR gate → Belam lands / writes posts rows → agi-project.

## Land order
1. **g5.35.2** agi-project fix first.  
2. g5.34.6.2 / g5.34.7.2–.4 (pending) and g5.34.8.1–.4 project together where possible; one reproject preferred. DG land/reproject HELD until g5.35.2 clears.

## Residues / siblings (not this PASS body)
- **g5.34.6.2:** V1 W1 parent/`subagent_of` grokbot fallback (DG inbox → SM wake naming DG); W1 payload carry tip sha; alive C1–C6 cuts that touch W1.  
- **g5.34.6.4** hung-send (`printf msg | box send DEST`) on tip.  
- **g5.34.9.1** exists — design only; DG/engine HELD until g5.34.8 + rest of g5.34 done. Not unheld here.  
- alive: if further cuts arrive post-tip, SM amends .8.x note; no re-gate unless scope changes.

## Non-goals
Model-loop ≤30s poll · forever monitor on banked-idle DG · per-DG Grok Bot · second watcher stack · mail detect via `o` notice line · Prime hand-patch engine · viewer latch · pin 33 on DG · SM-pane sudo · git rm · Master
