#!/usr/bin/env python3
"""
Lightweight Knowledge Graph Data Processor

This script creates a minimal JSON format from ontology CSV files and creates a minimal JSON format for 
a lightweight canvas-based knowledge graph visualization.
"""

import pandas as pd
import json
import random
import os

def create_lightweight_graph_from_coords(coords_file='graph_with_coords.json', canvas_width=800, canvas_height=600, margin=50):
    """Create a minimal graph using node positions from graph_with_coords.json, scaled to fit the canvas."""
    print(f"Reading node positions from {coords_file} ...")
    if not os.path.exists(coords_file):
        print(f"Error: {coords_file} not found")
        return None
    with open(coords_file, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    nodes = graph_data['nodes']
    edges = graph_data['edges']

    # Find min/max for scaling
    xs = [n['x'] for n in nodes]
    ys = [n['y'] for n in nodes]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Scale and center to fit canvas
    def scale(val, minv, maxv, out_min, out_max):
        if maxv == minv:
            return (out_min + out_max) / 2
        return out_min + (val - minv) / (maxv - minv) * (out_max - out_min)
    
    for n in nodes:
        n['x'] = scale(n['x'], min_x, max_x, margin, canvas_width - margin)
        n['y'] = scale(n['y'], min_y, max_y, margin, canvas_height - margin)
        # Rename label -> name for lightweight format
        n['name'] = n['label']
        n['full_name'] = n['label']
    
    # Convert edges to lightweight format
    lw_edges = []
    for e in edges:
        # Accept both 'source'/'target' or 'from'/'to'
        src = e.get('source', e.get('from'))
        tgt = e.get('target', e.get('to'))
        lw_edges.append({'from': src, 'to': tgt})
    
    # Compose metadata
    strands = sorted(set(n.get('strand', 'Unknown') for n in nodes))
    lw_graph = {
        'nodes': [
            {
                'id': n['id'],
                'name': n['name'],
                'full_name': n['full_name'],
                'strand': n.get('strand', 'Unknown'),
                'explanation': n.get('explanation', n['name']),
                'x': n['x'],
                'y': n['y']
            }
            for n in nodes
        ],
        'edges': lw_edges,
        'metadata': {
            'total_nodes': len(nodes),
            'total_edges': len(lw_edges),
            'strands': strands,
            'max_nodes': None
        }
    }
    return lw_graph

def save_lightweight_graph(graph_data, output_file='_static/lightweight-graph.json'):
    """Save the graph data to JSON file"""
    
    # Ensure _static directory exists
    os.makedirs('_static', exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
    
    print(f"Lightweight graph data saved to {output_file}")
    print(f"Nodes: {len(graph_data['nodes'])}")
    print(f"Edges: {len(graph_data['edges'])}")
    print(f"Strands: {graph_data['metadata']['strands']}")

def main():
    """Main function to process and save the lightweight graph"""
    
    print("Creating lightweight knowledge graph using layout_knowledge_graph.py output...")
    
    # Create graph with 100 nodes for good performance
    graph_data = create_lightweight_graph_from_coords()
    
    if graph_data:
        save_lightweight_graph(graph_data)
        print("✓ Lightweight graph created successfully!")
    else:
        print("✗ Failed to create lightweight graph")

if __name__ == "__main__":
    main() 