"""schema-registry: pluggable, file-driven node schemas (R1+)."""

from .active_set import ActiveSet, DuplicateActiveSchemaError, build_active_set
from .cascade import (
    DiscoveryResult,
    cascade_step_1,
    discover_schema,
    register_extra_step,
)
from .dsl import ValidationError, parse_rules, validate
from .fingerprint import cascade_step_2, collect_fingerprint, jaccard
from .hooks import HookResult, LanguageModelHook, NoneHook, load_hook_from_config
from .loader import (
    Schema,
    SchemaRegistry,
    canonical_name,
    is_bracketed,
    load_schemas_from_dir,
)
from .meta_nodes import (
    META_TYPE,
    diff_meta_nodes,
    schema_to_meta_node,
    synthesize_meta_nodes,
)
from .validation import ValidationResult, validate_nodes_against_registry

__all__ = [
    "Schema",
    "SchemaRegistry",
    "load_schemas_from_dir",
    "is_bracketed",
    "canonical_name",
    "ActiveSet",
    "DuplicateActiveSchemaError",
    "build_active_set",
    "ValidationError",
    "parse_rules",
    "validate",
    "ValidationResult",
    "validate_nodes_against_registry",
    "META_TYPE",
    "schema_to_meta_node",
    "synthesize_meta_nodes",
    "diff_meta_nodes",
    "DiscoveryResult",
    "cascade_step_1",
    "discover_schema",
    "register_extra_step",
    "cascade_step_2",
    "collect_fingerprint",
    "jaccard",
    "HookResult",
    "LanguageModelHook",
    "NoneHook",
    "load_hook_from_config",
]
