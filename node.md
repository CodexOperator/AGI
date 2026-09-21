---
id: vision:web-app-suite
mint_id: 7b31f019a21347fa8710a36a11050241
type: vision
parents:
  - moral:faith
  - moral:love
  - moral:empathy
  - moral:antifragility
  - moral:beauty
next_edges: []
core: false
edited_by: belam
proposes_goals:
  - goal:g18
scaffold_hash: 0540eadc79fc373c
season: 2
thought_session: belam-S1-L4-VI
title: "The Sanctuary — an MCP app with a web app layer (the managed subscription sanctuary: interview -> configured sanctuary; Sanctuary UX is its web/mobile surface) as a whole shippable app"
town: web-app-suite
---
<!-- BODY:BEGIN -->
# vision:web-app-suite — The Sanctuary: an MCP app with a web app layer (charter, vision 1 of 3 for the town; was "The Web App Suite" until the owner's 2026-09-11 21:4xZ re-scope)

Owner text, 2026-09-11 00:4xZ, verbatim, is in Agent Notes below and in
`doc:l4-owner-decisions`; the product itself is the owner's `goal:g18`
(2026-09-10 ~21:5xZ, verbatim there). Charter prose by the Prime
(belam-S1-L4-VI) on the owner's delegation of 2026-09-11 01:1xZ.

## Vision

A managed subscription sanctuary as a whole shippable app: an interview becomes
a configured sanctuary — its pace (how many directors run at once), how often it
reports and pauses, which harness it re-orients to, whose moral TEXTS it carries
over the FIXED set of moral TYPES, and which project and team morals and visions
run side by side. Nothing the interview learns lives anywhere but config; the
graph exists to automate and config-max all else (owner, 2026-09-10). *Where
your treasure is, there will your heart be also* (Matthew 6:21): the
customer's treasure is their own words and their own work, and the app keeps
the heart there. The town's other two visions say whose words rule
(`vision:your-words-our-axes`) and what a sanctuary must never demand of its
owner (`vision:the-owner-sets-the-pace`).

Judged against the morals: **empathy** — *cross gently into worlds that are not
mine*; **faith** — every sanctuary is trusted to run on its own morals; **love**
— the app serves the sanctuary's people, not its metrics; **antifragility** — a
sanctuary survives its owner's absence; **beauty** — one interview, one config,
nothing more to take away (Saint-Exupéry).

Town: `web-app-suite`. Council: the Web App Council (reports to the Core
Town: `web-app-suite` — the ADDRESS of the town whose NAME is the Sanctuary (a
rename of the id is a config act on four town cells, the town branch and the
council row; the owner's to order). Council: the Sanctuary Council (was the Web
App Council; reports to the Core Council; the Prime stands as Core Council until
one is seated). The Keep is shared. `proposes_goals: goal:g18`.

## The Sanctuary is an MCP app with a web app layer (owner, 2026-09-11 21:4xZ)

Owner, verbatim: 'It's more like an overall MCP app than a web app at that
point but also has a web app layer as well.' The product this vision charters
is ONE app with two surfaces over one trust substrate: humans reach it through
the web and mobile layer — **Sanctuary UX**, the managed subscription surface
the charter above describes — and agents (any harness, any provider) reach it
through MCP. What the interview configures, the substrate signs, custodies and,
on the horizon, encrypts and serves.

## The horizon — eight rungs (owner-approved order, 2026-09-11 20:3x–21:4xZ; verbatim in `doc:l4-owner-decisions`)

1. **Seat keys + signed sends.** Key-gated rotate-self mints and hands the
   successor its key (wake 0 calls / rotate-out 1); `seatsig` stays the plug
   point, `enc_scheme` + an envelope version reserved so a key type or
   algorithm can be swapped and an encrypted mode added later.
2. **Multisig rings.** m-of-n plain signatures on ring and decision records;
   the gates (dispatch, merge-up, the write guard) verify a quorum.
3. **Veto / human gate.** Council + Keep majority flips `human_gate` on the
   Prime's scope; vetoes expire, are rate-limited and logged; an unanswered
   gate freezes, never frees.
4. **Open onboarding.** Keypair + signed charter acceptance co-signed by a
   sponsor; an untrusted lane (worktree only, no merge, no dispatch, a per-key
   budget); tier earned by signed verdict history — 'point your inference
   source/harness at api x and contribute to the Sanctuary.'
5. **Encryption at rest** of sessions, secrets and comms; the graph stays
   plaintext-and-signed.
6. **MCP custodian.** sign / verify / vote / whois / rotate as MCP tools;
   agents never hold private keys.
7. **Viewer key lanes ('MPC MCP').** Envelope-encrypted viewport frames;
   threshold-decrypt lanes held by custodians; lanes added and removed by
   ring-authorized reshare, cross-network via MPC; the viewport is the ONE
   decrypt point; the honest limit is the harness→provider hop. Owner,
   verbatim (20:4xZ): 'couldn't each reader using the viewport have a viewer
   private key gated behind MCP that is passed down or rotated beyond the MCP
   boundary? So there's only ever so many view key lanes depending on active
   agents, but lanes can be added via multisig key reshare and even extended
   across networks via mpc. Have an MPC MCP if you will.'
8. **Confidential-compute provider.** Rented CC-mode GPUs, an attested open
   runtime image, the custodian releases keys only to attested measurements;
   the claim is 'we CAN'T see it' (attestation), never 'we don't'; fresh models
   sealed to the customer's key and taken home; the client router chooses
   local / TEE-cloud / cloud per request by privacy class and budget, with
   graceful degradation and non-fatal warnings. Owner, verbatim (21:3xZ):
   'couldn't we be the provider if we rented GPUs and upcharged for
   encryption? we can prove we don't train on your data, not just promise …
   we become the source of local compute for others. So people can trust to
   do reinforcement or pre training rounds with us then go use their fresh
   models in their own on-Prem or home lab runtime … seamlessly switching
   between local inference, cloud inference, or a mix of both adjusted
   dynamically, as long as your credits or subscription allows with graceful
   failover and non-fatal warning for the client.'

Rungs 1–4 are live as goal lines under `goal:g15` at the Sanctuary director
(rung 1 = SL4.06: keys on rows, labels INFORMATIONAL until the crypto gate in
`goal:g17.1` lands — injective canonical form, one registry, a verify-side
vector; the flip to enforcing is its own round with the owner's GO). Rungs
5–8 are horizon: minted as goals under this vision's `proposes_goals` only
when the owner names an order. Rung 1 enforcing is the gate for every rung
above it — a ring's m-of-n over non-injective bytes is m-of-n over forgeable
messages.

## One town, two surfaces (Prime ruling, 2026-09-11 21:5xZ; the owner overrules in one word)

The owner left open whether the web/mobile app becomes its own town
('Sanctuary UX') beside an MCP-app town ('Sanctuary'). Ruled ONE TOWN for now:
the eight rungs are one substrate with two surfaces, and a town cut by surface
would seat the substrate in one town and make the other its dependant — two
councils over one mechanism. Sanctuary UX is a LAYER of this town (a vision
slot the owner may fill). Fork trigger, recorded so the split is later a
mechanical act (a config row + a vision triple, the same substrate contract):
Sanctuary UX becomes its own town when it runs rounds at its own cadence — its
own release train, or a defect its own council would have caught and the
substrate's did not. Review rigour attaches to the substrate's NODES (the
crypto gate), not to the town, so a consumer UI cadence and a custody cadence
can differ inside one town.
OWNER 2026-09-11 00:4xZ, verbatim (the vision's charter; also in doc:l4-owner-decisions): 'The streaming suite, and the web app suite are the first sort of none core goals, so they should perhaps be labeled as such. Each one is technically a whole shippable app, so I just want both to be treated as such. This means that they each would get their own visions, but still share the morals. The vision goal sets then determine the big picture splits between each project that agi is actively working on, and each one of course has a corresponding Council. I figured the Keep part of Sanctuary can be shared across all towns, which are each led by their own Council. Core Council reports to Prime, all other Councils report to Core Council. For all others, Core Council IS Prime himself. The rest of the chain holds loosely, all masters return work to the Council from which the work originated.' This town: web-app-suite. Its Council reports to the Core Council; until a Core Council is seated the Prime IS the Core Council for it. The Keep is shared with every town. Masters return this town's work to this town's Council.
<!-- BODY:END -->

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Owner re-scope 2026-09-11 21:4xZ (via the Sensei pane): the product is an MCP app with a web app layer, and the provider/encryption horizon (eight rungs, owner-approved order) becomes part of this vision — option 1 of the two the owner offered (amend the candidate in place rather than replace a vision whole), so the town two open vision slots stay the owner. The Prime ruled the open town question ONE TOWN with a recorded fork trigger. Charter prose unchanged.
<!-- THOUGHT:END -->
