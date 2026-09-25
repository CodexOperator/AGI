# OSC.15 TMM.122 mechanical pre-step: Qwen3 QK-norm adapter

MECHANISM ONLY (no checkpoint/network/GPU; HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1).

Verified: attn_implementation=eager | hook={"q_untouched": true, "attn_k_is_quant_postrope": true, "quant_changes_output": true}
q_norm=Qwen3RMSNorm k_norm=Qwen3RMSNorm structural=True qwen2_has_qk_norm=False

q_norm/k_norm are real Qwen3RMSNorm, applied BEFORE RoPE (absent on Qwen2); the patched
post-RoPE key at the attention interface equals an independent quant_bw(rope(q,k)) reference,
and ALL_ATTENTION_FUNCTIONS["eager"] item-assignment is honored live (output differs on/off).

Remains gated: a scored agreement/KL result needs a PRETRAINED QK-norm checkpoint -- none
obtained (no download/network in scope, none cached on this box); no bit budget was tested.
