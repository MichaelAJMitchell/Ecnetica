#!/usr/bin/env python3
"""
Knowledge Graph Layout Script

This script reads concepts and relationships CSV files, builds a directed graph,
computes a layout using graphviz, and outputs a JSON file ready for Sigma.js visualization.

Usage:
    python layout_knowledge_graph.py [concepts_file] [relationships_file]
    
If no files are provided, the script will automatically detect CSV files containing
"concepts" and "relationships" in their names in the current working directory.
"""

import pandas as pd
import networkx as nx
import json
import sys
import os
import glob
from pathlib import Path

try:
    import pygraphviz
    from networkx.drawing.nx_agraph import to_agraph
    HAS_PYGRAPHVIZ = True
except ImportError:
    HAS_PYGRAPHVIZ = False

def find_csv_files():
    """Automatically find concepts and relationships CSV files in current directory."""
    concepts_file = None
    relationships_file = None
    
    # Look for files containing "concepts" in the name
    concepts_files = glob.glob("*concepts*.csv")
    if concepts_files:
        concepts_file = concepts_files[0]
    
    # Look for files containing "relationships" in the name
    relationships_files = glob.glob("*relationships*.csv")
    if relationships_files:
        relationships_file = relationships_files[0]
    
    return concepts_file, relationships_file

def build_graph(concepts_df, relationships_df):
    """
    Build a NetworkX directed graph from concepts and relationships data.
    
    Args:
        concepts_df: DataFrame with columns [id, name, explanation, broader_concept, strand, source]
        relationships_df: DataFrame with columns [id, prerequisite_id, dependent_id, prerequisite_name, dependent_name, explanation, source]
    
    Returns:
        networkx.DiGraph: Directed graph with nodes and edges
    """
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes (concepts)
    for _, row in concepts_df.iterrows():
        G.add_node(
            row['id'],
            label=row['name'],
            explanation=row['explanation'],
            broader_concept=row['broader_concept'],
            strand=row['strand'],
            source=row['source']
        )
    
    # Add edges (relationships)
    for _, row in relationships_df.iterrows():
        G.add_edge(
            row['prerequisite_id'],
            row['dependent_id'],
            explanation=row['explanation']
        )
    
    return G

def compute_layout_with_clusters(G, concepts_df):
    if HAS_PYGRAPHVIZ:
        # Create an AGraph (pygraphviz) for advanced layout
        A = to_agraph(G)
        A.graph_attr.update(rankdir='TB', splines='true', overlap='false')
        # Group nodes into clusters by strand
        strands = concepts_df['strand'].fillna('Unknown').unique()
        strand_to_nodes = {strand: concepts_df[concepts_df['strand'] == strand]['id'].tolist() for strand in strands}
        for i, (strand, node_ids) in enumerate(strand_to_nodes.items()):
            if not node_ids:
                continue
            sg = A.add_subgraph(node_ids, name=f'cluster_{i}', label=strand, color='lightgrey')
            sg.graph_attr['style'] = 'filled'
            sg.graph_attr['color'] = 'lightgrey'
            sg.graph_attr['label'] = strand
        A.layout(prog='dot')
        pos = {}
        for n in G.nodes():
            node = A.get_node(n)
            x, y = map(float, node.attr['pos'].split(','))
            pos[n] = (x, y)
        y_coords = [y for x, y in pos.values()]
        min_y, max_y = min(y_coords), max(y_coords)
        for k in pos:
            x, y = pos[k]
            pos[k] = (x, max_y - y + min_y)
    else:
        print("pygraphviz not found, using networkx.spring_layout for fallback.")
        pos = nx.spring_layout(G, k=2, iterations=200)
        xs = [x for x, y in pos.values()]
        ys = [y for x, y in pos.values()]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        def scale(val, minv, maxv, out_min, out_max):
            return out_min + (val - minv) / (maxv - minv) * (out_max - out_min)
        for k in pos:
            x, y = pos[k]
            pos[k] = (
                scale(x, min_x, max_x, 50, 800 - 50),
                scale(y, min_y, max_y, 50, 600 - 50)
            )
    # Compute levels (longest path from roots)
    levels = {}
    roots = [n for n in G.nodes() if G.in_degree(n) == 0]
    for node in G.nodes():
        if node in roots:
            levels[node] = 0
        else:
            max_level = 0
            for root in roots:
                try:
                    path_length = nx.shortest_path_length(G, root, node)
                    max_level = max(max_level, path_length)
                except nx.NetworkXNoPath:
                    continue
            levels[node] = max_level
    return pos, levels

def create_sigma_json(G, pos, levels):
    """
    Create Sigma.js compatible JSON format.
    
    Args:
        G: NetworkX directed graph
        pos: Dictionary of node positions
        levels: Dictionary of node levels
    
    Returns:
        dict: Sigma.js compatible graph data
    """
    nodes = []
    edges = []
    
    # Add nodes
    for node_id in G.nodes():
        node_data = G.nodes[node_id]
        x, y = pos[node_id]
        
        node = {
            "id": node_id,
            "label": node_data['label'],
            "x": float(x),
            "y": float(y),
            "strand": node_data['strand'],
            "broader_concept": node_data['broader_concept'],
            "explanation": node_data['explanation'],
            "source": node_data['source'],
            "level": levels[node_id]
        }
        nodes.append(node)
    
    # Add edges
    for source, target in G.edges():
        edge = {
            "source": source,
            "target": target
        }
        edges.append(edge)
    
    return {
        "nodes": nodes,
        "edges": edges
    }

def main():
    """Main function to orchestrate the graph building and layout process."""
    
    print("Starting knowledge graph layout script...")
    
    # Parse command line arguments or auto-detect files
    if len(sys.argv) == 3:
        concepts_file = sys.argv[1]
        relationships_file = sys.argv[2]
        print(f"Using provided files: {concepts_file}, {relationships_file}")
    elif len(sys.argv) == 1:
        concepts_file, relationships_file = find_csv_files()
        if not concepts_file or not relationships_file:
            print("Error: Could not automatically find concepts and relationships CSV files.")
            print("Please provide them as command line arguments:")
            print("python layout_knowledge_graph.py <concepts_file> <relationships_file>")
            sys.exit(1)
        print(f"Auto-detected files: {concepts_file}, {relationships_file}")
    else:
        print("Usage: python layout_knowledge_graph.py [concepts_file] [relationships_file]")
        sys.exit(1)
    
    print(f"Reading concepts from: {concepts_file}")
    print(f"Reading relationships from: {relationships_file}")
    
    try:
        # Read CSV files
        concepts_df = pd.read_csv(concepts_file)
        relationships_df = pd.read_csv(relationships_file)
        
        print(f"Loaded {len(concepts_df)} concepts and {len(relationships_df)} relationships")
        
        # Build graph
        print("Building directed graph...")
        G = build_graph(concepts_df, relationships_df)
        
        print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
        
        # Check for disconnected components
        if not nx.is_weakly_connected(G):
            components = list(nx.weakly_connected_components(G))
            print(f"Warning: Graph has {len(components)} disconnected components")
            print(f"Component sizes: {[len(c) for c in components]}")
        
        # Compute layout with clusters by strand
        print("Computing layout with clusters by strand...")
        pos, levels = compute_layout_with_clusters(G, concepts_df)
        
        # Create Sigma.js JSON
        print("Creating Sigma.js JSON...")
        sigma_data = create_sigma_json(G, pos, levels)
        
        # Write output file
        output_file = "graph_with_coords.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sigma_data, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully created {output_file}")
        print(f"Output contains {len(sigma_data['nodes'])} nodes and {len(sigma_data['edges'])} edges")
        
        # Print some statistics
        print("\nGraph Statistics:")
        print(f"Root nodes (no prerequisites): {len([n for n in G.nodes() if G.in_degree(n) == 0])}")
        print(f"Leaf nodes (no dependents): {len([n for n in G.nodes() if G.out_degree(n) == 0])}")
        print(f"Maximum level: {max(levels.values()) if levels else 0}")
        
        # Print some example nodes by level
        print("\nExample nodes by level:")
        for level in sorted(set(levels.values()))[:5]:  # Show first 5 levels
            level_nodes = [n for n, l in levels.items() if l == level]
            print(f"Level {level}: {len(level_nodes)} nodes")
            if level_nodes:
                example_node = level_nodes[0]
                print(f"  Example: {G.nodes[example_node]['label']}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 