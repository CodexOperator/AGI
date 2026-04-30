-- Schema for Unified Graph Memory (DB-augmented directed code generation)
-- Postgres-compatible with duckdb fallback for local runs

-- Node types enum
CREATE TYPE node_type AS ENUM (
    'doc_section',
    'code_reference', 
    'gitnexus_symbol',
    'gitnexus_definition',
    'memory_session',
    'schema_entity',
    'task_node'
);

-- Edge types enum  
CREATE TYPE edge_type AS ENUM (
    'sequential',
    'contains',
    'references',
    'depends_on',
    'implements',
    'extends'
);

-- Main nodes table
CREATE TABLE nodes (
    id TEXT PRIMARY KEY,
    type node_type NOT NULL,
    label TEXT NOT NULL,
    content TEXT,
    source TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Edges table
CREATE TABLE edges (
    id SERIAL PRIMARY KEY,
    from_node TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    to_node TEXT NOT NULL REFERENCES nodes(id) ON DELETE CASCADE,
    type edge_type NOT NULL,
    weight REAL DEFAULT 1.0,
    metadata JSONB DEFAULT '{}',
    UNIQUE(from_node, to_node, type)
);

-- Indexes for fast traversal
CREATE INDEX idx_edges_from ON edges(from_node);
CREATE INDEX idx_edges_to ON edges(to_node);
CREATE INDEX idx_edges_type ON edges(type);
CREATE INDEX idx_nodes_type ON nodes(type);
CREATE INDEX idx_nodes_source ON nodes(source);

-- GIN index for content search
CREATE INDEX idx_nodes_content_gin ON nodes USING gin(to_tsvector('english', content || ' ' || label));

-- Function: get adjacent nodes
CREATE OR REPLACE FUNCTION get_neighbors(node_id TEXT)
RETURNS TABLE(neighbor_id TEXT, edge_type edge_type) AS $$
BEGIN
    RETURN QUERY
    SELECT e.to_node, e.type FROM edges e WHERE e.from_node = $1
    UNION
    SELECT e.from_node, e.type FROM edges e WHERE e.to_node = $1;
END;
$$ LANGUAGE plpgsql;

-- Function: BFS path finding (Postgres implementation)
CREATE OR REPLACE FUNCTION find_path(start_id TEXT, end_id TEXT, max_depth INT DEFAULT 10)
RETURNS TABLE(path TEXT[]) AS $$
WITH RECURSIVE bfs AS (
    SELECT ARRAY[start_id] AS path, start_id AS current, 1 AS depth
    WHERE start_id != end_id
    UNION ALL
    SELECT b.path || e.to_node, e.to_node, b.depth + 1
    FROM bfs b
    JOIN edges e ON e.from_node = b.current
    WHERE b.depth < max_depth AND NOT (e.to_node = ANY(b.path))
)
SELECT path FROM bfs WHERE current = end_id LIMIT 1;
$$ LANGUAGE plpgsql;

-- View: Graph statistics
CREATE VIEW graph_stats AS
SELECT 
    (SELECT COUNT(*) FROM nodes) AS total_nodes,
    (SELECT COUNT(*) FROM edges) AS total_edges,
    (SELECT COUNT(*) FROM DISTINCT type) AS node_types,
    (SELECT type, COUNT(*) FROM nodes GROUP BY type ORDER BY COUNT(*) DESC) AS nodes_by_type;
