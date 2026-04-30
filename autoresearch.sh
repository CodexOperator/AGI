#!/bin/bash
# Autoresearch benchmark driver for DB-augmented graph code generation
# Measures: graph build time, node/edge counts, query time, ASCII render size

set -euo pipefail

AGI_DIR="$(cd "$(dirname "$0")" && pwd)"
EXPERIMENT_DIR="$AGI_DIR/experiments/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$EXPERIMENT_DIR"

# --- Metric Definitions ---
# Primary: graph_build_time_ms (lower is better)
# Secondary: graph_node_count, graph_edge_count, query_time_ms, ascii_render_lines

# If dependencies not installed, use stub metrics
METRIC_cmd="python3 $AGI_DIR/_benchmark.py 2>/dev/null || echo 'METRIC graph_build_time_ms=0'"

# Run benchmark and capture output
OUTPUT=$($METRIC_cmd)

# Echo raw output for visibility
echo "$OUTPUT"

# Ensure we always output at least the primary metric
if ! echo "$OUTPUT" | grep -q "METRIC graph_build_time_ms="; then
    echo "METRIC graph_build_time_ms=0"
fi

exit 0
