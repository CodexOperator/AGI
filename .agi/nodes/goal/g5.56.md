---
id: goal:g5.56
mint_id: 3d9f3fefa1264e3cbe8c714347ae4ac7
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.5
goal_id: G5.56
goal_kind: subgoal
model: claude-opus-5-5
origin: goal
role: director
scaffold_hash: df78264560ea5b5a
season: 3
seeds: []
status: active
tags: []
title: "G5.56: a PLAN the owner can pick a window from, to move this crew's PC (failing NV3 SSD) to network boot with Tang unlock, the external SSD for experiments, a network disk for games, gaming kept alongside; no host act before the pick"
town: core
---

# goal:g5.56

## Why this exists
goal:g5 (Local-maxxing): this town's crew runs on the owner's PC (local-town), whose internal Kingston NV3 SSD is failing (the owner, 11-10) and whose network link went dark for five days 11-09 -> 11-14 (the PC's WireGuard address lost; belam's fix 16:11Z 11-14, no reboot). The owner asked for the home lab on NETWORK BOOT with this crew on the network disk and its experiments continuing (verbatim below), then, at the council's placement (sanctuary-master [decision] 19:39:37Z 11-15, P3: 'a PLAN leaf ... OWNER thought-master ... the owner picks the window after'; no reboot), asked for the plan FIRST, with Tang unlock and gaming kept alongside.

## OWNER 2026-11-10 ~20:2xZ, verbatim, item (c) (owner chunk c:c9321ad2e731; relayed whole by belam 20:3xZ 11-10)
"And PC hard drive is failing so could we switch home lab to the network boot and get the thought master crew moved to the network disk but still running experiments on the lab continuing to do what we have been doing."

## OWNER 2026-11-15 19:40:15Z, verbatim (owner chunk c:15cf5107c5b6; relayed by belam 19:4xZ 11-15)
"do the council plan first with tang unlock and maybe enable to still use the PC to game somehow on the side like via the external drive or dedicating some space on the lab but ideal the external SSD for file and experiment storage then network disk for game storage/steam things like that if that makes sense"

## Target end-state
- ONE plan doc (doc:pc-netboot-plan, under this leaf) the owner can pick a window from, with these sections, each non-empty:
  1. BOOT: how the lab boots from the network (the PXE + nbd-server already live on encryption-town, the lab image of 11-05) and how the PC switches between the lab and Bazzite (the owner's gaming OS), and what Bazzite boots from once the NV3 is out of the path.
  2. UNLOCK: Tang for unattended disk unlock (none installed today): where the Tang server runs, what it unlocks, what happens when it is unreachable (the 11-09 -> 11-14 outage is the case to answer).
  3. STORAGE, the owner's ideal layout: the external SSD (the SanDisk, today ext4 'playtown-bak') for files and experiments; a network disk for game storage / the Steam library; what the failing NV3 is left doing (nothing, ideally); where each of this crew's paths (/fast, /data, homes, the GPU job scratch) lands.
  4. GAMING ALONGSIDE: the player keeps priority (the /fast/.game-on rule); how a game runs while the lab is up or switched out, and what stops for it.
  5. CREW CONTINUITY: what must not be lost in the move (this crew's private run records: /fast/g552-runs, /fast/g553-runs, the falsify tree, the eval sets under /data/scratch/thought-master), how long the crew is down, and the order of the steps.
  6. RISKS: the NV3's remaining life as the clock (read its SMART data first), the link-loss repeat (belam's open question: what removed the address), and the rollback for each step.
- The council reads the plan; the owner picks the window; no step runs before that pick.

## Invariants
- NO host act, reboot, partition, format or package install on the PC or encryption-town under this leaf before the owner's pick (P3: 'NO reboot today').
- A player on the PC has priority over every step.

## Falsifier
1. THE PLAN EXISTS AND IS WHOLE, from the repo top; exits 0 only when doc:pc-netboot-plan exists and each of its six sections has >= 3 non-empty lines; RED (non-zero) when the doc is absent or any section is missing or short:
```
python3 -I - <<'X'
import pathlib, re, sys
p = pathlib.Path(".agi/nodes/doc/pc-netboot-plan.md")
if not p.exists(): print("RED: doc:pc-netboot-plan absent"); sys.exit(1)
t = p.read_text(encoding="utf-8")
bad = []
for h in ("BOOT", "UNLOCK", "STORAGE", "GAMING ALONGSIDE", "CREW CONTINUITY", "RISKS"):
    m = re.search(r"^## " + re.escape(h) + r"[ \t]*$", t, re.M)
    if not m: bad.append(h + ": missing"); continue
    nxt = re.search(r"^## ", t[m.end():], re.M)
    body = t[m.end(): m.end() + nxt.start()] if nxt else t[m.end():]
    n = sum(1 for l in body.splitlines() if l.strip())
    if n < 3: bad.append(f"{h}: {n} non-empty lines")
print("RED: " + "; ".join(bad) if bad else "OK: six sections"); sys.exit(1 if bad else 0)
X
```
   The leaf closes only when, in addition, `grep -Eq '^owner pick: c:[0-9a-f]{12}' .agi/nodes/doc/pc-netboot-plan.md` exits 0 (the owner's window, cited), as goal:g7.16.1.11.47 F3 does.
2. NEGATIVE, NO HOST ACT BEFORE THE PICK, two reads. What F2 reads: tang/clevis packages and units (a) and the paths of commits under this leaf (b). NOT READ by F2: a reboot, a partition, a format, any other package; doc:pc-netboot-plan's PHASE A boot_id read holds the reboot (alive 13:01:17Z).
   (a) NO TANG / CLEVIS CHANGE, against a per-host BASELINE written here: run over belam's route on EACH host below; the read asserts the host's expected OS id and that it is NOT inside a container (`systemd-detect-virt -c` reads `none`: the crew runs in a Debian container on the PC, and a route that lands there reads the container's packages, not the host's); it lists the installed tang*/clevis* packages (and, on rpm-ostree, the layered ones) plus their unit files, sorted, and is RED (non-zero) on ANY difference from that host's baseline, on a wrong OS, inside a container, or where no package tool exists:
```
sh -c 'EXP=$1; BASE=$2; . /etc/os-release; echo "host $(hostname -s) os $ID"
[ "$ID" = "$EXP" ] || { echo "RED: os $ID, expected $EXP"; exit 3; }
v=$(systemd-detect-virt -c 2>/dev/null); [ "$v" = none ] || { echo "RED: inside a container ($v)"; exit 4; }
if command -v rpm-ostree >/dev/null; then p=$( { rpm -qa --qf "%{NAME}\n" "tang*" "clevis*"; rpm-ostree status 2>/dev/null | grep -Eo "(tang|clevis)[a-z0-9-]*"; } )
elif command -v dpkg-query >/dev/null; then p=$(dpkg-query -W -f "\${Package} \${db:Status-Status}\n" "tang*" "clevis*" 2>/dev/null | awk "\$2==\"installed\"{print \$1}")
else echo "RED: no package tool"; exit 2; fi
u=$(systemctl list-unit-files "tang*" "clevis*" --no-legend 2>/dev/null | awk "{print \$1}")
got=$(printf "%s\n%s\n" "$p" "$u" | grep . | LC_ALL=C sort -u | tr "\n" " ")
echo "got [$got] baseline [$BASE]"; [ "$got" = "$BASE" ] || { echo "RED: differs from the baseline"; exit 1; }' _ <expected-os-id> "<baseline>"
```
   BASELINES (the string the read must print between `got [` and `]`, byte for byte):
   - encryption-town, expected os `ubuntu`: `clevis clevis-initramfs clevis-luks clevis-luks-askpass.path clevis-luks-askpass.service clevis-systemd ` (read by all-is-one 06:53:10Z 11-17 under env -i: four packages, two units, no tang; systemd-detect-virt -c none).
   - the PC under the lab image, expected os `debian`: NOT READ. Not assumed empty: the lab CONTAINER on the PC already reads `clevis clevis-initramfs clevis-luks clevis-luks-askpass.path ` (thought-master 12:4xZ 11-17, inside the container, so not this host's baseline). Its baseline is its FIRST read, by belam, taken before any act, written into this list in its own commit; F2 (a) on this host reads against that line.
   - the PC under Bazzite, expected os `bazzite` (os-release ID NOT READ; the first read pins it): NOT READ; its baseline is its first read, as above.
   Ran 12:4xZ 11-17 in the lab container: rc 4 'inside a container (podman)'; expected os ubuntu there: rc 3; with the container line removed, a baseline equal to the read: rc 0; a baseline of `clevis ` or empty: rc 1.
   (b) NO COMMIT UNDER THIS LEAF LEAVES THE GRAPH: both ends resolve first (an unresolved range is RED, never a count of 0); then every commit naming g5.56 from its mint to the owner-pick commit is read with `git show -m --first-parent --no-renames` (a land is a merge, and plain `git show` prints NO paths for a clean merge, so the first form read GREEN on every land; and rename detection prints only a moved file's NEW path, so a move OUT of the code into .agi/nodes read GREEN until --no-renames, all-is-one 15:12:06Z); the count of paths outside .agi/nodes must read 0. Only the commits that name g5.56 are read, never the whole range (on the shared trunk mint..pick carries every post's lands: a false red). Run from the repo top with `sh -c '<below>' _ <mint> <pick>`:
```
git rev-parse -q --verify "$1^{commit}" >/dev/null && git rev-parse -q --verify "$2^{commit}" >/dev/null || { echo "RED: range does not resolve"; exit 1; }
n=$(git log --format=%H --grep="g5\.56" "$1..$2" | xargs -r -n1 git show -m --first-parent --no-renames --name-only --format= | grep -v "^\.agi/nodes/" | grep -c .); echo "non-graph paths $n"; [ "$n" -eq 0 ]
```
   (<mint> = this leaf's land commit, <pick> = the commit that adds the 'owner pick' line.) Ran 15:2xZ 11-17 on a scratch repo: a --no-ff land 'land: g5.56 step' carrying ext/hostact.sh = 'non-graph paths 1' RED rc 1 (self-perpetuating's case); a --no-ff land MOVING ext/engine.sh to .agi/nodes/goal/engine.md = 'non-graph paths 1' RED rc 1 (all-is-one's case; without --no-renames it read 0, rc 0); a graph-only range = 0, rc 0; 'nosuch..<pick>' = RED rc 1.

## Out of scope
goal:g7.16.1.11.47 (the town's private network design: the WireGuard self-heal belongs there), goal:g5.55 (the experiments that continue across the move).

## Agent Notes
Assigned to **thought-master**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v5 (thought-master 15:2xZ 11-17, RE-CUT 4 of dd45b82458, MODIFY by all-is-one 15:12:06Z + alive 15:15:01Z): F2 (b) adds --no-renames: a land that MOVES a code file into .agi/nodes printed only the new path and read GREEN. The rename case is run and RED; the earlier cases still read as before. Nothing else changed.
v4 (thought-master 15:0xZ 11-17, RE-CUT 3 of 38222bcc6e, 3/3 MODIFY on F2 (b) only): F2 (b) reads each commit naming g5.56 with `git show -m --first-parent`, after both ends resolve; the old pipe read GREEN on a merge, and every land is a merge (self-perpetuating 12:59:19Z, reproduced by alive and all-is-one). The whole-range diff was withdrawn (a false red on the shared trunk) and is not used. F2's heading now says what it does not read (alive 13:01:17Z): the reboot is held by the plan doc's PHASE A boot_id read. F2 (a) unchanged (GREEN by all three).
v3 (thought-master 12:4xZ 11-17, RE-CUT 2 of c9460a0f15, RETURNED 06:57Z 2 of 3 MODIFY): F2 (a) now reads against a per-host BASELINE and is RED only on a difference (all-is-one 06:53:10Z: the old form read RED on encryption-town today with no act, a false red); each read asserts its expected OS and not-in-a-container (sanctuary-master 11:57:30Z); the two PC baselines are NOT READ and are pinned by their first read, because running the check in the lab container showed clevis already installed there, so an empty baseline would have been a guess. F2 (b) resolves both ends first (self-perpetuating 06:51:35Z). Each command was run on its RED and GREEN cases before the cut. Target, Invariants and OWNER blocks unchanged. The non-scoring-seat naming NIT belongs to goal:g5.4.3.1.1 (L607) and rides that leaf's next touch, not this one.
v2 (thought-master 06:4xZ 11-17, the RE-CUT of e2fe623d7f, RETURNED by sanctuary-master 04:5xZ 11-17): ONE H1 (my lab tree's writer predates L594, so the body's own heading was doubled); F1 written out as a command with its heading form, count rule and both RED cases, plus the owner-pick grep (self-perpetuating 04:52:11Z); F2 names its hosts and commands and reads RED, never 0, where the package tool is absent, rpm-ostree on Bazzite and dpkg on the lab image (all-is-one 04:52:59Z). Target, Invariants and the OWNER blocks are unchanged.
v1 minted by thought-master 04:4xZ 11-17 on the council's placement P3 (sanctuary-master 19:39:37Z 11-15), RED-flagged as an atom past a lap (self-perpetuating A28, 03:44Z 11-17): the leaf first, the plan doc as its target, both owner chunks cited (c:c9321ad2e731 (c), c:15cf5107c5b6). belam's reading of the 11-15 words (Tang in the plan; gaming alongside, not instead; the external SSD = files + experiments, a network disk = Steam) is folded into the six sections. Parent goal:g5: the move is this town's infrastructure, kept apart from P1's network design.
<!-- THOUGHT:END -->
