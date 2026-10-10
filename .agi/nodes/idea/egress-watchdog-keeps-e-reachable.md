---
id: idea:egress-watchdog-keeps-e-reachable
mint_id: ff9365d96c5c48349673c23fe6e6635e
type: idea
parents:
  - goal:g7.16.1.11.7
next_edges: []
model: claude-opus-5-5
role: prime_director
scaffold_hash: 79f4f9ba071a7d9d
season: 2
title: "encryption-town keeps egress when the overlay gateway dies: a 1-minute root watchdog falls back from full tunnel to split"
town: core
---

# idea:egress-watchdog-keeps-e-reachable

On encryption-town, outbound traffic runs through a WireGuard overlay gateway (full tunnel, wg0 -> wg0-full.conf) or direct (split, wg0 -> wg0-split.conf). If the gateway dies while the box is in full mode, the box loses ALL egress: GitHub pushes, remote-control sessions, model APIs. The egress watchdog is the fallback: a root timer every minute pings the gateway (10.66.0.1, the overlay address) and, after 3 misses in a row, switches the box to split so it stays reachable.

Files (extensions/agi/guard/egress/, installed by hand on 09-13, grok era; added to the graph 10-09 on the owner's word):
- belam-egress: `full | split | status` -- relinks wg0.conf and restarts wg-quick@wg0 (installed at /usr/local/sbin)
- belam-egress-watchdog: the 1-minute check (installed at /usr/local/sbin)
- belam-egress-watchdog.service / .timer: OnBootSec=2min, OnUnitActiveSec=1min (installed at /etc/systemd/system)

KNOWN DEFECT (measured 10-09 04:2xZ, belam-s2-I): the watchdog's first line is `[ \"$(readlink /etc/wireguard/wg0.conf)\" = /etc/wireguard/wg0-full.conf ] || exit 0`. The escaped quotes are literal characters, so the test is never true and the script ALWAYS exits 0 -- it has never checked the gateway (no /run/belam-egress-fails, no belam-egress journal entry), while E IS in full mode now. The fix is dropping the six backslashes (the logger line carries the same literal quotes). Not applied: once it works it switches E to direct egress after 3 misses and never back -- a networking/privacy call for the owner.

The repo copy of belam-egress differs from the installed one in one comment line only (the gateway's location removed); belam-egress-watchdog and both units are byte-identical.
