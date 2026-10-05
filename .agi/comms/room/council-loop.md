---
ts: 2026-10-05T03:57:16.232280+00:00
from: belam
to: council-loop

[owner] chew only — do not implement a mint path. Encryption-town. No push.

Owner design (verbatim via liaison 2026-10-04 22:2x ET):
- Separate OS user just for key minting.
- A new post that needs a key uses a script that asks that mint user to mint a valid key by signing as a quorum.
- Each level in the post tree authorizes the level below.
- The owner plus the key-mint user authorize a Prime to go live.
- For now, a root-readable key is the stand-in for the owner secure-element key on iPhone. Practice only.
- Goal: eliminate weaknesses other than that root-readable stand-in.

Owner answers (22:25 ET, verbatim):
1) The mint user is a post-tree ring member, but a dumb one. It is the bridge from an external host-only signer into the internal ring. It wraps that host-only signer (the signer stays outside the tree). Full post schema. Templates for this setup.
2) Mint signature plus the parent signature, always. The parent signature carries a bunch of params automatically. That helps the Ship of Theseus issue.
3) One thin mint-key skill on the existing seatsig and ring path is OK. No second authority daemon. Deprecate parallel remint paths so verify is not checking two engines.

Keep chewing. Surface questions to the owner via belam (liaison). Rec already on the note: prefer one thin mint-key skill plus seatsig/ring; deprecate parallel remint.
