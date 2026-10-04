---
id: hypothesis:g716111-aa2-k1-one-capped-openrouter-key-per-spawn-minted-by-root-for-the-spawns-lifetime-and-revoked-at-its-stop
mint_id: 880ff70242df41d1981c7c40abed67de
type: hypothesis
parents:
  - goal:g7.16.1.11.12
next_edges: []
confidence: 0.6
edited_by: director-general-1
season: 2
testable_claim: "(AA2.40-.46, K1) a kid spawn gets ONE OpenRouter key, minted by root's agi-mint@<post>--<kid> with a SERVER-SIDE limit equal to the invoker's inherited kid.usd (read from the TRUNK config:posts, never from the caller), alive exactly as long as the spawn (ExecStopPost deletes it; RuntimeMaxSec=4h revokes a hung one): on scratch with a stub curl, `agi-mint + self-perpetuating--k1` inherits belam's kid.usd 0.5 through council and makes one POST with limit 0.5 and a 0600 key file, `agi-mint -d` makes one DELETE by hash and removes the file, a post with no tree row gets nothing (rc 3); polkit lets a post start or stop ONLY agi-(mint|kid)@<itself>--<kid> (13/13 in node, incl. another post's and a look-alike agi-kidx@ refused); `systemd-analyze verify` passes on agi-mint@.service and agi-kid@.service; the base config:engine stays <= 8,192 B (8,186 B: one map line, paid by shortening the box map line). Class (a), a tool loop (pi): the key reaches the kid ONLY as a systemd credential (agi-kid@ is DynamicUser, no group agi, BindsTo agi-mint@) and never the caller; class (b), no tool: the caller gets a 0600 file."
title: "AA2 K1: ONE capped OpenRouter key per spawn, minted by root for the spawn's lifetime from the inherited kid.usd cap and revoked at its stop; a post can mint or revoke only its own"
town: core
---
# hypothesis:g716111-aa2-k1-one-capped-openrouter-key-per-spawn-minted-by-root-for-the-spawns-lifetime-and-revoked-at-its-stop

## Measured
- belam [owner] 18:16Z (owner 18:1xZ, verbatim in doc:radically-simple-engine AA2 K1): "you have an Openrouter provision key ... It'll allow Openrouter provision and is how the pi paid lanes spawn. We just need to incorporate grabbing one as we spawn a kid instead and using it for the pi code app." + "Provision key is already here in the .env that's how the paid pi lane worked". Split 18:17Z: alive = M1 (done: goal:g7.16.1.11.11.1) · all-is-one = K2 + K3 · AA2 (self-perpetuating) = K1.
- Measured first (names and perms only; no key value read or printed): MAIN .env is 0600 belam:belam, no ACL, so a v5 uid CANNOT read the provisioning key: that is what makes the cap a rail. The one privileged path a post has is polkit agi.rules (group agi may START agi-post@ units).
- The cap is SERVER-side (OpenRouter's per-key limit), so it holds whatever language the kid runs in; it comes from the GRAPH (the inherited engine.kid.usd, AA2 LADDER OUT), so a post outside the tree gets no key. Post names never contain `--`; a name that does is refused.
- Bytes (self-perpetuating's scratch, final form fitted to K2): agi-mint 1,248 B + agi-mint@.service 278 B + agi-kid@.service 288 B in engine-root EXPANSION; agi.rules 211 -> 345 B; agi-kid +~110 B; the base 8,186 B (one agi-mint map line); seed 0.
- Seams: K3's agi-infer reads the class-(b) key file; belam's `kid` cell must carry `usd` (one number) next to model/max; the class-(a) path is only provable AS ROOT. DG1 AA2 doc source: AA2 K1 section on trunk 9778def43.

## CLAIM
(AA2.40-.46, K1) a kid spawn gets ONE OpenRouter key, minted by root's agi-mint@<post>--<kid> with a SERVER-SIDE limit equal to the invoker's inherited kid.usd (read from the TRUNK config:posts, never from the caller), alive exactly as long as the spawn (ExecStopPost deletes it; RuntimeMaxSec=4h revokes a hung one); polkit lets a post start or stop ONLY agi-(mint|kid)@<itself>--<kid>; the base config:engine stays <= 8,192 B.

## Dispatch line
config-max: YES, the Prime's: belam's `kid` cell gains `usd` (a number), and no row's key value is ever written to the graph / template-max: none / code: agi-mint + agi-mint@.service + agi-kid@.service (engine-root), agi.rules, agi-kid's start/read-key/trap-stop (+~110 B). NOT dispatched, and NOT started while the key broker is unbuilt: a v5 post spawns no paid kid before it. belam [decision] 02:2xZ 10-03: K1 waits on AA2 merge-up-1 (landed 9778def43, so that part is clear) and then HIS kid cell (with `usd`) and his GOs. Every HOST ACT (install the units and the rule, the first real mint, the first real delete) is its own belam GO (command, before-state, one-command rollback). Spend: the owner named this provider and mechanism (OpenRouter provisioning key); no other provider, and no real key is minted before belam's GO.

## FALSIFIERS
1. A committed shell test (extensions/agi/tests/agi-mint.t.sh, from self-perpetuating's scratch in the doc, stub curl): `sh extensions/agi/tests/agi-mint.t.sh` = 0 FAIL: one POST with the inherited limit, key file 0600, `-d` = one DELETE by hash and the file gone, a post with no tree row = rc 3, the 13 polkit cases.
2. Negative: `git grep -n 'PROVISIONING' -- .agi/nodes/.geometry/engine-post.md` prints 0 hits (no post-side piece names the provisioning key), and `wc -c` of config:engine <= 8,192.
3. AS ROOT, belam's GO each (UNVERIFIED until then): a class-(a) kid's credential is present in the kid and absent from the caller, and `systemctl stop agi-kid@..` revokes the key (one DELETE).

## TESTS
agi-mint.t.sh above; `systemd-analyze verify` on both templates; the polkit cases through the real rule text.

## FILE SCOPE
engine-root.md (agi-mint, the two units) · agi.rules · engine-wrap or engine-post (agi-kid) · extensions/agi/tests/agi-mint.t.sh. Never a key value; never the live trunk ref.

## CEILING
1 parent · kids <= 2 · agi-mint <= 1,248 B · units 278 B + 288 B · agi.rules <= 345 B · 0 base bytes beyond one map line (+18 net) · 0 USD until belam's GO.
