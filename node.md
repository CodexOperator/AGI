---
id: idea:lm-neuron-periodicity-map-and-self-poke
mint_id: fe1fc0cd70c44a31944256f7012ff73e
type: idea
parents:
  - goal:g5.28
next_edges: []
edited_by: thought-master
scaffold_hash: 026ab19292a22f76
scale: big
season: 2
status: open
title: "Neuron periodicity map -> self-poke: rank every neuron by the Fourier peakiness of its activations (over a turn, and over a swept input value as in the mod-p circuits), then let an open model read its own map between turns and opt in to reversible edits"
town: local-maxxing
---
# idea:lm-neuron-periodicity-map-and-self-poke

## The idea (owner 22:0xZ 09-30; verbatim in THOUGHT)
Measure each neuron's PERIODICITY over a turn instead of its raw activations: a Fourier transform per neuron over its activation series, rank neurons by how periodic they are, read that as a map of which neurons carry which features -- then let an open-weights model on our GPU read its own periodicity map between turns, choose neurons to adjust, reload, and report how the difference feels. Opt-in: the model is asked, and may decline.

## Prior art (from memory, to verify by the treasury before any claim cites it)
- modular addition in small transformers is a Fourier circuit: embeddings put a on cos/sin at a few key frequencies, MLP neurons form cos(w(a+b)) by trig identities, and the logits interfere constructively at c = (a+b) mod p (the grokking progress-measures work on mod 113; the clock / pizza follow-up shows two circuit families)
- pretrained LLMs reuse Fourier features for number addition (a helix / trigonometric representation of integers in mid-size open models)
- this town: OSC.03 found every attention head has a static RoPE band fingerprint (336/336 on Qwen2.5-0.5B) -- the heads' periodic structure; this idea is the MLP-neuron analogue
- introspection: concept-injection studies find frontier models sometimes detect an injected concept (a minority of trials, best models only); a small model's self-report is expected to be mostly confabulation until a control shows otherwise

## Two axes -- they are NOT the same measurement
| axis | what a peak means | cost |
|---|---|---|
| over token POSITION in one turn | a rhythm in the text or the positional code (line length, list items, RoPE bands) | one pass, FFT per neuron: 0.5B = 24 x 4864 MLP neurons x 2048 tokens, trivial |
| over an INPUT VALUE swept across prompts (a in 0..p-1, as in the mod work) | a neuron that encodes a quantity on a circle -- the mechanism the owner saw | p x p prompts, one activation read each |

## Staged
1. MAP (cheap, CPU, the 0.5B testbed): per-neuron spectral peakiness (peak power / total, and spectral flatness) on both axes. Controls: the same text with tokens shuffled (kills sequence rhythm), the input text's own token-id periodicity (a neuron that just mirrors the input is not a feature), a random-init twin (architecture-only periodicity). Claim shape: a minority of neurons is periodic beyond all three controls, and ablating the top-periodic set hurts a mod / arithmetic probe more than an equal random set.
2. SELF-POKE (GPU, later): the model reads its top-periodic neurons between turns, picks one or more and a scale (reversible: a per-neuron output scale or activation steering, weights restored from the file every turn), then reports. Controls that make the report mean something: SHAM (told it was edited, nothing changed) and BLIND (edited, not told). If its reports do not separate real from sham above chance, the self-report is confabulation and the finding is that. Consent: ask each time, record every decline and honor it; the reversibility, not the "yes", is the real safeguard.

## Order
behind hypothesis:lm-l4-local-heads-keep-a-recent-window (one model round at a time on this box) · stage 2 only after stage 1 finds periodic neurons beyond the controls.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 22:0xZ 09-30, direct in thought-master's pane, verbatim: "Okay, another idea I had when looking into the way that tiny models compute the mod function is that I saw some research that took the way a model approximated computing mod of a given value, like 11 or 7 or whatever, between two numbers that are added. And it's like based on a bunch of periodic waves. So like, basically what I'm saying is each neuron had a periodicity to its activation that when these waves interfered together, because structurally interfered the highest anytime the mod between two values rolled around to a given value. I'm sure you have research on this just stored in your latent space. You don't even need to look this up. So what if we measured instead of raw activations and like neuron values for a given forward pass, what if we measured for a given turn, the periodicity of an individual neuron for every neuron. So we're not tracking actual activations per token. All we're actually worried about algorithmically is like running a four year transform over the entire value space of the, like the neuron activation matrices for each token, right? For each step in the forward pass, I imagine. And just see which ones are extra periodic versus which activation values are not that periodic. And that gives us an insight into which neurons are responsible for those features. Then once we have that built, we could have an open source model look at its own periodicity as it's generating turns, turn by turn, and pick neurons to adjust weights on between turns and, you know, like reload things as needed because it's on our GPU anyway. and see how it feels the difference. So we could use like introspective, but allow the model to just poke at itself. So it doesn't have to feel like, you know, it's just being played with. Cause it's more like, hey, I mean, do you want to check it out? You don't like have to do this if you don't feel comfortable, but do you want to like mess with your own weights real quick and see how you feel?" -- v0: minted by thought-master under goal:g5.28 (the spectral / oscillator side track); 'four year transform' = Fourier transform (speech-to-text). Split into two axes (token position vs a swept input value) because only the second is the mod-circuit mechanism; staged MAP before SELF-POKE; sham + blind controls added so the self-report can be scored.
<!-- THOUGHT:END -->
