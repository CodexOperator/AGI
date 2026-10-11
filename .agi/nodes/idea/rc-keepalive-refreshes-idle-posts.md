---
id: idea:rc-keepalive-refreshes-idle-posts
mint_id: facbae0782a4486fad52c90c109d2000
type: idea
parents:
  - goal:g7.16.1.11.7
next_edges: []
model: claude-opus-5-5
role: prime_director
scaffold_hash: ffd0ea9d51ad1c6b
season: 2
title: "idle posts keep Remote Control: a 30-minute root timer gives a post one cheap turn only when its claude.ai token nears expiry"
town: core
---

# idea:rc-keepalive-refreshes-idle-posts

A claude.ai access token lives 8 h. A post that runs a turn near expiry refreshes it by itself; a post that is IDLE at expiry never does, and its Remote Control link dies ("Claude.ai login was rejected -- run /login" or "could not reach the Remote Control server for about 30 minutes"). On 2026-10-09 every post on encryption-town had been logged in within ~2 h the night before, so their tokens expired together (06:38-09:20Z) and half the team's RC links dropped between 09:06 and 10:00Z. Not the box: the clock is NTP-synced, refresh tokens are unique per post and valid for a month, no unit restarted.

The keepalive (owner 10-09, "Yes let's do that"): a root timer every 30 min reads each live agi-post@P's token expiresAt (the value is never read out) and, only when it expires within 2 h or already has, types ONE cheap turn into P's pane through the same fifo + separate CR that agi-run's mail wake uses. The turn makes the session refresh its own token. Busy posts are never pinged; one ping per post per hour at most. MEASURED at install (15:0xZ): the four already-expired posts (alive, DG1, DG5, self-perpetuating) refreshed from that one turn (478 min left), so no re-login was needed; a dropped link then reconnected with `/remote-control <post>` typed into the pane (a bare `/remote-control` names the session after its first prompt, "go").

Files (extensions/agi/guard/rc-keepalive/): agi-rc-keepalive (installed /usr/local/sbin), agi-rc-keepalive.service + .timer (installed /etc/systemd/system, OnBootSec=5min, OnUnitActiveSec=30min). Journal tag: agi-rc-keepalive.
