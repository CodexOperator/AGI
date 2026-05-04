"""Step 3 of the discovery cascade — LM hook (T-028 / R6).

If steps 1 (bracket) and 2 (fingerprint) miss, attempt the configured LM hook.
On success: write a non-bracketed (pending review) schema file and return it.
On failure: log + fall through.
"""

from __future__ import annotations

import logging
import warnings
from pathlib import Path
from typing import Any

import yaml

from ..cascade import DiscoveryResult, register_extra_step
from ..loader import Schema, SchemaRegistry, load_schemas_from_dir
from . import LanguageModelHook, load_hook_from_config

logger = logging.getLogger("schema_registry.hooks")

_active_hook: LanguageModelHook | None = None


def configure_hook(hook: LanguageModelHook | None) -> None:
    """Inject a LM hook for the cascade. Pass None to disable."""
    global _active_hook
    _active_hook = hook


def _validate_proposed_yaml(text: str) -> dict[str, Any] | None:
    """R6.4: validate hook output before writing to disk."""
    try:
        parsed = yaml.safe_load(text)
    except yaml.YAMLError as e:
        logger.warning("hook proposed malformed YAML: %s", e)
        return None
    if not isinstance(parsed, dict):
        logger.warning("hook proposed non-mapping YAML: %r", type(parsed).__name__)
        return None
    if "name" not in parsed:
        logger.warning("hook proposed schema missing required 'name' field")
        return None
    return parsed


def cascade_step_3(directory: str | Path, registry: SchemaRegistry) -> DiscoveryResult:
    """LM hook fallback (R6.2: missing/unreachable → cascade proceeds to generic)."""
    if _active_hook is None:
        return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
    samples: list[dict[str, Any]] = []
    base = Path(directory)
    if not base.is_dir():
        return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
    for p in sorted(base.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".json"}:
            continue
        try:
            from graph_core.persistence import load_node_file

            nf = load_node_file(p, body=False)
            samples.append(dict(nf.frontmatter))
        except Exception:
            continue
        if len(samples) >= 5:
            break
    try:
        result = _active_hook.propose_schema(samples)
    except Exception as e:  # noqa: BLE001 — R6.3
        logger.warning(
            "LM hook %r raised during propose_schema: %s",
            _active_hook.name,
            e,
        )
        warnings.warn(
            f"LM hook {_active_hook.name!r} failed: {e}",
            UserWarning,
            stacklevel=2,
        )
        return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
    if not result.schema_yaml:
        if result.error:
            logger.info("LM hook %r returned no schema: %s", _active_hook.name, result.error)
        return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
    parsed = _validate_proposed_yaml(result.schema_yaml)
    if parsed is None:
        logger.warning("LM hook output rejected by validator")
        return DiscoveryResult(schema=None, step="no-match", candidate_score=0.0)
    # Write the proposal as an inactive (no brackets) schema for user review.
    name = str(parsed["name"])
    proposed_path = base.parent / "schemas" / f"{name}.md"
    proposed_path.parent.mkdir(parents=True, exist_ok=True)
    text = "---\n" + yaml.safe_dump(parsed, sort_keys=True) + "---\n"
    proposed_path.write_text(text, encoding="utf-8")
    # Don't auto-activate — leave for user review.
    fresh_reg = load_schemas_from_dir(proposed_path.parent)
    schema = fresh_reg.schemas.get(name)
    return DiscoveryResult(schema=schema, step="lm-hook", candidate_score=0.5)


register_extra_step(cascade_step_3)
