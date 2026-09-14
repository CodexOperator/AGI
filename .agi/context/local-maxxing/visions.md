# Local-maxxing visions — rulers (owner GO 2026-09-14 ~03:5xZ, verbatim on goal:g14: "those rewords for the visions seem a lot more useful as rulers to measure progress and kind to models. Let's go with those at this time.")

Each vision keeps the owner's FAITH line verbatim (direction, never graded) and carries one OPERATIONAL line under it (the ruler every verdict in the town is measured against). Drafted by the thought-master; minted by the Prime (vision schema written_by owner/prime_director; parents: moral:faith + moral:local-maxxing, town local-maxxing). vision:local-maxxing (exists) = vision 1; visions 2 and 3 are new (goal:g14.2 "three visions").

## vision 1 — efficiency (vision:local-maxxing)
FAITH (owner, verbatim 2026-09-14): "there's always a more efficient way to do inference on lighter and lighter hardware."
RULER: For every job the sanctuary runs, there exists a configuration meeting its quality bar at fewer bytes-touched-per-token (weights + KV read per generated token) on a smaller RAM/bandwidth envelope than the one we run now. Measured monthly in the bytes-touched ledger (doc:local-maxxing-trove-survey-2026-09-14, CP1): a month with no row that lowers bytes-per-token at held quality is a month the vision was not advanced, not a month it was false.

## vision 2 — smarter inference (new: vision:local-maxxing-smarter)
FAITH (owner, verbatim): "there's always a smarter way to do inference that achieves better and better bench results over time."
RULER: At a fixed CPU-second budget per item, the accuracy of the best <=4B configuration on the town's standing harness (200 items: GSM8K + ARC-style MC + IFEval slice; thinking mode fixed and logged; paired per-item tests, SE ~3.5 pts) rises month over month. The harness is the object the vision lives in (CP5); a configuration is anything inference-side or training-side that runs on the town's own boxes.

## vision 3 — cooperation (new: vision:local-maxxing-together)
FAITH (owner, verbatim): "two or more models working together are exponentially smarter than just a simple sum of those parts."
RULER: For a fixed CPU-second budget there exists a cooperation scheme (sampling + verifier, routing, cascade, speculative, shared cache, debate, coupled byte-neuron channels, ...) whose accuracy exceeds the best single member at that budget, and whose marginal gain per added member or sample does not decay — an accelerating segment of the accuracy-vs-compute curve with a bootstrap CI over items that excludes zero. Baseline is always the best member (or one model at matched compute), never a sum. Measured in the Vision-3 Pareto table (CP9).
