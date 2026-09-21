---
id: build:src-schema-registry-init
mint_id: e8235f7ddf6b475186081d208cc776fa
type: build
parents:
  - idea:engine-schema-registry
build_kind: code
confidence: 1.0
edited_by: season.py
origin: build-scan
payload_ref: extensions/agi/src/schema_registry/__init__.py
season: 1
tags:
  - build
  - code
  - g2.1
thought_session: season
title: "Build: extensions/agi/src/schema_registry/__init__.py"
---
`extensions/agi/src/schema_registry/__init__.py` — level-3 code node (one file, one canonical node).

Census parent: `idea:engine-schema-registry`.

<!-- BUILD-CONTRACT:BEGIN — harness-owned shape; a model may only fill why/perf/security, never add/remove/reorder fields or entries -->
```yaml
payload_ref: extensions/agi/src/schema_registry/__init__.py
parse_ok: true
inputs:
- name: .active_set.ActiveSet
  how: '`from .active_set import ActiveSet` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .active_set.DuplicateActiveSchemaError
  how: '`from .active_set import DuplicateActiveSchemaError` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .active_set.build_active_set
  how: '`from .active_set import build_active_set` at line 3'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .cascade.DiscoveryResult
  how: '`from .cascade import DiscoveryResult` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .cascade.cascade_step_1
  how: '`from .cascade import cascade_step_1` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .cascade.discover_schema
  how: '`from .cascade import discover_schema` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .cascade.register_extra_step
  how: '`from .cascade import register_extra_step` at line 4'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .dsl.ValidationError
  how: '`from .dsl import ValidationError` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .dsl.parse_rules
  how: '`from .dsl import parse_rules` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .dsl.validate
  how: '`from .dsl import validate` at line 10'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .fingerprint.cascade_step_2
  how: '`from .fingerprint import cascade_step_2` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .fingerprint.collect_fingerprint
  how: '`from .fingerprint import collect_fingerprint` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .fingerprint.jaccard
  how: '`from .fingerprint import jaccard` at line 11'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .hooks.HookResult
  how: '`from .hooks import HookResult` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .hooks.LanguageModelHook
  how: '`from .hooks import LanguageModelHook` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .hooks.NoneHook
  how: '`from .hooks import NoneHook` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .hooks.load_hook_from_config
  how: '`from .hooks import load_hook_from_config` at line 12'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .loader.Schema
  how: '`from .loader import Schema` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .loader.SchemaRegistry
  how: '`from .loader import SchemaRegistry` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .loader.canonical_name
  how: '`from .loader import canonical_name` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .loader.is_bracketed
  how: '`from .loader import is_bracketed` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .loader.load_schemas_from_dir
  how: '`from .loader import load_schemas_from_dir` at line 13'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .meta_nodes.META_TYPE
  how: '`from .meta_nodes import META_TYPE` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .meta_nodes.diff_meta_nodes
  how: '`from .meta_nodes import diff_meta_nodes` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .meta_nodes.schema_to_meta_node
  how: '`from .meta_nodes import schema_to_meta_node` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .meta_nodes.synthesize_meta_nodes
  how: '`from .meta_nodes import synthesize_meta_nodes` at line 20'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .validation.ValidationResult
  how: '`from .validation import ValidationResult` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
- name: .validation.validate_nodes_against_registry
  how: '`from .validation import validate_nodes_against_registry` at line 26'
  why: TODO(model)
  perf: TODO(model)
  security: TODO(model)
outputs: []
```
<!-- BUILD-CONTRACT:END -->

Generated by `level3.py` (see `hyp:level3-node-anatomy` in the graph repo for the design). `how` fields above are derived mechanically via the standard library `ast` module; `why`/`perf`/`security` are placeholders for a later model pass — never fabricated by this generator.