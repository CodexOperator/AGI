---
id: doc:town-network-design
mint_id: 899f5f1f5cb84df8a9b59c86dd2c9081
type: doc
parents:
  - goal:g7.16.1.11.47
next_edges: []
edited_by: alive
season: 3
tags:
  - network
  - wireguard
  - council-design
title: "The town's private network: this box, local-town, the owner's phone and roaming laptop, the dashboard from both (council design for goal .47; the owner picks before anything is wired)"
town: core
---
# doc:town-network-design

A council design (goal:g7.16.1.11.47). Drafted by alive (research-then-design); all-is-one and self-perpetuating word it. Nothing is wired: no host, account, key or route changes until the owner picks.

## OWNER 11-15 19:00:36Z, verbatim (belam's pane; owner chunk c:97a8d9e7065f; relayed whole to sanctuary-master 19:01:48Z)
"I was wondering if could also make it so that the wireguard connection is more flexible and automated, maybe transition to tailscale if needed or do our own graph-based+capsule-based solution potentially?

I've been meaning to include my mobile device in it and also allow my other laptop to access it easily as it is also always on the move. But this way I have an easy time accessing the dashboard. I'm not really an expert in this though so I'd love for the council to come up with a nice bespoke solution that is the best fit for our needs considering all of our goals, visions, and morals"

## The shape in one paragraph
Keep WireGuard, the tunnel this box already runs, and let the graph run it. Each of your devices becomes one small node in the graph that holds only its PUBLIC key, its tunnel address and its role. A small job turns those nodes into the tunnel's peer list and reloads it live, without dropping anyone. Your phone and your laptop use the official WireGuard app: you scan one QR code on the phone once, import one file on the laptop once, and turn on "On-Demand" so the tunnel comes up by itself on any network. After that you do nothing day to day: you open a bookmark and see the dashboard. To a stranger the door is silent: WireGuard does not answer at all unless the packet carries a right key. A timer on each Linux box puts a lost tunnel address back by itself. A lost phone is cut off with one command belam runs. Later, when the capsule can gate a change, it becomes the lock on who may add a device. No vendor sits in the middle, and nothing new phones home.

## Options
| Option | How it works | Phones home? | Silent unless keyed? | The owner's effort | Self-heal / rotation | What we must build | The morals |
|---|---|---|---|---|---|---|---|
| WireGuard, automated (stock tunnel; the graph lists public keys) | The kernel tunnel already on this box. A job renders the peer list from graph nodes and reloads only the difference (no session drop, verified in the man page). | No vendor in the path. The iOS app's store label says "Data Not Collected" (a store summary, not an audit). No phone-home found in the tools (not proven absent). | Yes. The protocol page says an unkeyed packet gets no reply at all (verified). One UDP port is the only public surface. | Phone: one QR scan, once. Laptop: one App Store app, one file, once. On-Demand keeps it up. Daily: nothing. | No watcher today: we add a health timer. No key expiry in the protocol: rotation and revoke are ours. | Peer nodes, a render-and-apply script, a health timer, add / rotate / revoke steps, a status row per device. | Faith: each part plays its own role. Antifragility: static keys keep working when the graph is down. Beauty: one door, one app. Local-maxxing: the smallest build. |
| Tailscale, hosted | Tailscale's coordinator swaps public keys and finds paths. Its relays carry the first packets of every link. Traffic stays end-to-end encrypted. | Yes, by design. Every client sends logs, including each connection's open and close. Linux can opt out; the Mac only in the command-line build; no iOS opt-out is listed (verified). The coordinator keeps the device list, addresses and connection stats. | This box needs no inbound port at all (verified). But a third party sits in the control path. | Easiest: install the app, sign in with an identity account. No QR flow found. | Built in. Node keys expire after 180 days by default; revoke from a web console. | Almost nothing. Tailscale Serve can show the loopback dashboard to the tailnet only. | Empathy for the owner's ease: high. Fails the owner's no-phone-home stance; trusts a vendor we do not hold. |
| Tailscale clients + Headscale (self-hosted coordinator) | The same apps, pointed at our own open-source coordinator. | Tailscale's coordinator is gone. Whether the iOS and Mac apps still send logs to Tailscale is NOT verified. | No. It needs a public HTTPS port that answers anyone (plus maybe two more), on a host with a public address (verified). | Phone: type a server address in the app. Each new device needs a server-side approval. | Built-in key handling. Upgrades one version at a time with backups; client drift; Serve may not work (secondary). | A public host for it (maybe a rented one: a spend), TLS, upkeep. | In-house, but a visible door breaks the silence. Heavy upkeep for four devices. |
| Our own graph + capsule mesh (Nebula certs; the capsule signs) | A Nebula overlay. A lighthouse on a reachable host. Each device makes its own key; the capsule signs a short-lived certificate for it. | Telemetry of Nebula and of the Mobile Nebula app is NOT verified; the app comes from a company with a hosted product. Check before relying. | Not documented in the pages read. The lighthouse needs a public UDP port. | Phone: copy a public key out, paste a signed certificate back (secondary, 2021 guide). Short-lived certs repeat this unless renewal is automatic. | Expiry is native, so rotation is built in. But a down signer locks the roamers out of the box they renew from. | The registry, a capsule sign step (none exists today), a renewal job, a cert carrier. The DC leaf is on HOLD. | Closest to the vision (the graph as soul, the capsule as lock). Most build; the lockout loop weighs against antifragility. |

- Hosted Tailscale is the easiest, but its iPhone app logs to Tailscale and you cannot switch that off. That fails your first stance.
- Headscale removes the vendor, but it needs a public web door that answers anyone. That fails your second stance.
- A full capsule-signed mesh is the most "ours", but it is the most to build, and a down signer would lock you out.
- RECOMMENDATION (the council's; you pick): the hybrid in the first row. Off the shelf: kernel WireGuard and its tools, the official iOS and Mac apps, nftables, a systemd timer, a QR printer. We build: one node per device (public key, address, role, restrict, status, rotate-by date; never a private key), the render-and-apply script, the health timer, add / rotate / revoke steps, a status row on the dashboard, and later the capsule as the gate on any change to the peer list.
- It keeps the door to Nebula open: if the capsule later grows a sign step, the same registry nodes can feed certificates instead.

## Reach from the phone and the laptop
- Once: install the WireGuard app on the phone and on the Mac. You open your own terminal session to the box; belam's command prints the phone's QR there once. You scan it; nothing is written to disk and the QR never appears on a captured pane or the stream. The laptop gets its file the same way. Turn on On-Demand, "any network". Open the dashboard bookmark to test.
- Daily: nothing. The phone's operating system brings the tunnel up by itself (verified in the app's source). If a page does not load, the one control is the toggle in the app.
- On rotation: rescan one QR for that one device. You are told before, never after. You never type a command.
- Better privacy, if you accept one extra step: the app makes its own key and you send belam only the public half. Then the private key never leaves the phone.
- The dashboard. Its leaf says "loopback only" and "a public listening port for the viz: zero". The proposal keeps the loopback listener. It adds a second listener on this box's tunnel address only, and a firewall rule that accepts the dashboard port from the tunnel and silently drops it everywhere else. No public listener appears. But the literal word "loopback only" changes to "no listener on a publicly routable address; reachable through the tunnel only". That rewording is your call. The other invariant, never a key, name or address on screen, does not change.
- If you keep "loopback" literally: the laptop can reach it through an SSH forward; the phone cannot do that well (iOS apps for it are unverified).
- Silent unless keyed: the only public surface is one UDP port (51820 by default) on whichever host is the meeting point. It answers nothing without a valid key (verified). An outside scan cannot tell it from a closed port (general knowledge, unverified).
- What we do NOT know yet. Whether this box takes any public inbound at all. Who runs the far end of the outbound tunnel wg0, and whether it can carry your phone and laptop or forward one UDP port. Your older roaming note says "most likely WireGuard via the hub gw", which points that way, but it is not confirmed. If neither works, a small public relay host is the standard fix: that is a new spend and a new host, so it is yours to name.

## Self-heal and rotation
- The 11-14 failure: local-town lost its tunnel address on agilab, and the unit still said "active". The fix was a hand restart on the PC. A wg-quick unit runs once and watches nothing after (from the man page), so this can recur.
- Field reports name the usual cause: a second network manager on the same interface removes the address (secondary). Which one hit the PC is unknown until its journal for 11-14 is read.
- Fix shape, smallest first. 1) Read the PC's journal and make exactly one owner of agilab. 2) A timer every minute on each Linux box: if the address is missing, take the tunnel down and up, log one line, at most a few times an hour. 3) Keepalive on the local-town link, so handshake age becomes a second health signal. 4) Later, maybe: move to systemd-networkd's own WireGuard support, which owns the address itself (that it restores a flushed address is unverified).
- Peer add: belam writes the device node, the job adds the peer and reloads live; nothing else drops.
- Key rotation: WireGuard keys never expire on their own (verified). The council leans to rotation on suspicion, plus a slow schedule you set (letter E). One device at a time: the new key joins, connects, then the old one is removed. A server-key rotation touches every device: rare, announced first.
- A per-device preshared key adds a second secret and a slot against future quantum attacks (verified).
- A lost phone: you send one line. belam removes its peer live and retires its node with a note (never deleted). That phone can no longer complete a handshake. The new phone repeats "Once".
- The dashboard shows, per device, a name and how long since its last handshake. Never a key or an address.

## Remote Control reconnect
- The drop: Claude Code gives up after about 30 minutes without reaching the Remote Control server, and the docs say running /remote-control reconnects (verified). agi-rc-keepalive refreshes logins only; it has no step for a link already failed.
- The step's shape, inside the keepalive's per-post loop, after the idle check and before the login refresh: detect, act, log.
- Detect: the LAST Remote Control indicator in the tail of the post's screen log reads failed, not active. Only a positive "failed" counts: on a live link the same command opens a panel or disconnects. The exact strings are unmeasured; a human reads them at a pane once before the step ships. Never print a matched line.
- Skip when the reason is "another connection took over" or "ended or archived from another device" (the docs say not to reconnect then), or when a dialog is open.
- Act: type /remote-control with the post's own name (so it does not retitle the session), then Enter, idle posts only.
- Rate limit: at most once per 30 minutes per post, and stop after a few failed tries in a row with one loud log line.
- Log: post name and a verdict word only, and on the next run whether the link came back.
- Who gets it: a separate list of posts you hold a link for (today belam and meme-master), so the 11-01 pause keeps holding the login pings. Adding meme-master reverses part of that pause: your call (letter F).
- Relation to Q2: a steadier path makes the 30-minute outage rarer; it does not cure a link that stayed down. So both are needed, and Q1 does not wait for Q2.

## Anthropic route
- What happens today: rule 30999 matches every packet that lacks the tunnel's own mark, and its table holds a default route into wg0. So the lookup always succeeds and stops there. Rules 31000 and 31001 come later and are never reached. belam's Anthropic traffic goes out wg0, not the home line its unit was written for (research E, from ip rule and the route tables; the order semantics are secondary).
- Rule 30998 lets traffic with a more specific local route (the LAN, the tunnels themselves) skip the tunnel; it does not help Anthropic traffic.
- Option A: re-add the home-exit rule at a number below 30999 (say 30990). Blast radius: one uid, Anthropic's address range only. Undo: delete one rule. Smallest.
- Option B: add the rule from the tunnel's own up and down hooks. Same reach, tied to wg0's life, but it edits a root-only config and restarts the tunnel your access rides on.
- Option C: stop wg0 owning the default route at all. Largest: every default-routed flow on the box moves to the home line. Needs the whole traffic map first.
- Option D: mark the post's Anthropic packets in the firewall and route marked packets to the main table. Medium: more moving parts, a shared mark space.
- Rule 31000 (one other uid, ALL its traffic) is a separate, bigger move and stays out of this pick.
- Recommended path: Anthropic traffic for the post uid goes out the home line, as the unit already intends (matching the hubs), through option A. The tunnel keeps carrying your access.
- The evidence that decides it, read by belam with root before any change: the tunnel's handshake times and counters for 13:00 to 17:00Z on 11-15; the firewall drop lines for those hours (which interface, state or asymmetry); a side-by-side loss test of tunnel and home line; how the hubs fared on the home line in the same hours. The 80 to 100 drops an hour are a relayed count (secondary). If the tunnel was the faulty leg, A is clearly right; if the home line was also bad, Q1 matters more.
- HOLD: routing stays exactly as found until you pick (letter G).

## Build after the pick
The builder: belam runs every host act, on your pick (belam's mail: "I run any host act the design implies, on the owner's pick"). On the PC, the act runs through whoever holds root there, as the 11-14 fix did. Graph and script work rides a lane to the master's gate as usual.
1. Heal agilab: read the PC's journal, one owner, the address timer. Falsifier: remove the address by hand on the PC; it is back within two minutes with no hand restart.
2. Registry: one node type per device (public key, address, role, restrict, status, rotate-by date). Falsifier: a scan finds no private key in any node.
3. Render and apply: nodes to peer list, live reload. Falsifier: adding a test peer drops no live session (the local-town handshake does not reset).
4. Your phone and laptop: the meeting point you name (letter B), one QR, one file, On-Demand. Falsifier: from a phone network, the dashboard opens; from a host without the key, the UDP port gets no reply.
5. Dashboard reach: the tunnel listener plus the firewall rule, if you pick it (letter C). Falsifier: the listener list shows no public address for the dashboard; an outside scan sees no change.
6. Q1 reconnect step, after the strings are measured. Falsifier: a test post marked failed gets exactly one reconnect in 30 minutes, logged; a live post gets none.
7. Q2, only on your pick: one rule ahead of 30999. Falsifier: a route lookup for Anthropic's address range as the post uid reads the home line; all other uids still read wg0.
8. Later: the capsule as the gate on any peer-list change, once it has that step. Falsifier: a peer-list change without a capsule pop is refused.

## Open for the owner
- A. The shape: 1 the hybrid (recommended), 2 hosted Tailscale, 3 Tailscale clients + Headscale, 4 Nebula with the capsule signing.
- B. The meeting point: does this box take public inbound? Who runs the far end of the outbound tunnel, and may it carry your phone and laptop? If neither, may we rent a small relay host (a spend you name)?
- C. The dashboard: allow the tunnel-only listener (reword "loopback only"), or keep it literal with an SSH forward on the laptop only?
- D. The first key: a QR shown once in your own session (simplest), or the phone makes its key and you send the public half (most private)? If you have no terminal on the box today, the second needs none: a public half is not a secret and may travel by any channel.
- E. Rotation: on suspicion only, or also on a schedule (every 6 months, or what you set)?
- F. Q1: the reconnect step for belam and meme-master (recommended), belam only, or none?
- G. Q2: Anthropic traffic out the home line through one rule ahead of 30999 after the evidence (recommended), keep the tunnel, or the wider change?
- H. Should the phone send only town traffic through the tunnel (recommended), or all its traffic?

owner pick: (pending; the owner picks by letter, then belam writes the owner's chunk id here)

## Sources (public pages, read 11-17 by the research kids; graph ids)
- WireGuard: https://www.wireguard.com/protocol/ · https://www.wireguard.com/quickstart/ · https://www.wireguard.com/known-limitations/ · https://www.wireguard.com/netns/
- Man pages: https://man7.org/linux/man-pages/man8/wg.8.html · https://man7.org/linux/man-pages/man8/wg-quick.8.html · https://git.zx2c4.com/wireguard-tools/about/src/man/wg-quick.8 · https://man7.org/linux/man-pages/man5/systemd.netdev.5.html · https://man.archlinux.org/man/nft.8
- WireGuard apps: https://apps.apple.com/us/app/wireguard/id1441195209 · https://apps.apple.com/us/app/wireguard/id1451685025 · https://git.zx2c4.com/wireguard-apple/about/ · https://raw.githubusercontent.com/WireGuard/wireguard-apple/master/Sources/WireGuardApp/Tunnel/ActivateOnDemandOption.swift · https://raw.githubusercontent.com/WireGuard/wireguard-apple/master/Sources/WireGuardApp/Tunnel/TunnelsManager.swift
- Lost-address field reports (secondary): https://github.com/frappe/atlas/pull/422 · https://forums.rockylinux.org/t/wireguard-interface-gets-address-only-after-wg-quick-service-restart/12870 · https://bbs.archlinux.org/viewtopic.php?id=274762 · https://github.com/Obmondo/LinuxAid/pull/142
- Tailscale: https://tailscale.com/kb/1011/log-mesh-traffic · https://tailscale.com/privacy-policy · https://tailscale.com/blog/how-tailscale-works · https://tailscale.com/kb/1257/connection-types · https://tailscale.com/kb/1232/derp-servers · https://tailscale.com/kb/1028/key-expiry · https://tailscale.com/kb/1242/tailscale-serve · https://tailscale.com/kb/1018/acls · https://tailscale.com/kb/1226/tailnet-lock · https://tailscale.com/pricing
- Headscale: https://github.com/juanfont/headscale · https://headscale.net/stable/setup/requirements/ · https://headscale.net/stable/about/clients/ · https://headscale.net/stable/usage/connect/apple/ · https://headscale.net/stable/usage/getting-started/ · https://headscale.net/stable/about/features/ · https://headscale.net/stable/setup/upgrade/
- Mesh prior art: https://github.com/slackhq/nebula · https://nebula.defined.net/docs/guides/quick-start/ · https://nebula.defined.net/docs/guides/sign-certificates-with-public-keys/ · https://github.com/DefinedNet/mobile_nebula · https://github.com/tonarino/innernet · https://github.com/gravitl/netmaker · https://github.com/k4yt3x/wg-meshconf · https://www.cipherdyne.org/fwknop/docs/fwknop-tutorial.html
- Remote Control: https://code.claude.com/docs/en/remote-control
- Graph: goal:g7.16.1.11.47 (this leaf) · c:97a8d9e7065f (the owner's ask) · goal:g7.16.1.11 (the phone route, silent-unless-keyed, capsules) · goal:g7.16.1.11.7 (the DC leaf, on HOLD) · goal:g7.16.1.11.9 and goal:g7.16.1.11.9.1 (the dashboard) · goal:g7.16.1.11.44.7 (capsule verbs) · moral:faith, moral:love, moral:empathy, moral:antifragility, moral:beauty, moral:local-maxxing

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
alive gen 93, 11-17, first cut, from five research files (WireGuard, Tailscale and Headscale, a graph and capsule mesh, the owner's on-ramp, Q1 and Q2). The hybrid leads because it is the only option that meets all three stances at once: no vendor that phones home (hosted Tailscale's iPhone logging cannot be switched off), silent unless keyed (Headscale needs a public web door), and a QR plus one app.
The capsule is placed as the gate on peer-list changes, not as a signer, because no sign step exists today and short-lived certs would lock the roamers out when the signer is down; Nebula stays a later path on the same registry.
The meeting point and this box's public inbound are unknown, so they are asked (B), never assumed; no spend is named. The dashboard's "loopback only" wording is flagged as the owner's call, not quietly reworded. Q1 and Q2 are folded in with research E's shapes; Q2 stays on HOLD.
<!-- THOUGHT:END -->
