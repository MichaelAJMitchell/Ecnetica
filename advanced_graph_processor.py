#!/usr/bin/env python3
"""
Advanced Graph Processor for Efficient Visualization
Creates multiple levels of detail and optimized data structures for smooth rendering
"""

import json
import pandas as pd
import networkx as nx
import numpy as np
from collections import defaultdict
import math
import os
from typing import Dict, List, Tuple, Any

class AdvancedGraphProcessor:
    def __init__(self):
        self.concepts_df = None
        self.relationships_df = None
        self.graph = None
        
    def load_data(self, concepts_file: str, relationships_file: str):
        """Load and validate the ontology data."""
        print(f"Loading concepts from: {concepts_file}")
        print(f"Loading relationships from: {relationships_file}")
        
        self.concepts_df = pd.read_csv(concepts_file)
        self.relationships_df = pd.read_csv(relationships_file)
        
        print(f"Loaded {len(self.concepts_df)} concepts and {len(self.relationships_df)} relationships")
        
        # Build NetworkX graph for analysis
        self.graph = nx.DiGraph()
        
        # Add nodes
        for _, concept in self.concepts_df.iterrows():
            self.graph.add_node(concept['id'], **concept.to_dict())
        
        # Add edges
        for _, relationship in self.relationships_df.iterrows():
            self.graph.add_edge(
                relationship['prerequisite_id'], 
                relationship['dependent_id'],
                **relationship.to_dict()
            )
        
        print(f"Built graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
        
    def calculate_importance_scores(self) -> Dict[str, float]:
        """Calculate importance scores for nodes using multiple metrics."""
        print("Calculating node importance scores...")
        
        importance = {}
        
        for node_id in self.graph.nodes():
            # Combine multiple centrality measures
            in_degree = self.graph.in_degree(node_id)
            out_degree = self.graph.out_degree(node_id)
            
            # PageRank-like importance
            try:
                pagerank = nx.pagerank(self.graph)[node_id]
            except:
                pagerank = 0.0
            
            # Betweenness centrality (sampled for performance)
            try:
                betweenness = nx.betweenness_centrality(self.graph, k=min(100, len(self.graph.nodes())))[node_id]
            except:
                betweenness = 0.0
            
            # Custom importance: combination of connectivity and centrality
            connectivity_score = (in_degree + out_degree) / 2.0
            centrality_score = (pagerank + betweenness) / 2.0
            
            # Final importance score (0-1)
            importance[node_id] = min(1.0, (connectivity_score * 0.3 + centrality_score * 0.7) / 10.0)
        
        return importance
    
    def create_levels_of_detail(self, importance_scores: Dict[str, float]) -> Dict[str, Any]:
        """Create multiple levels of detail for progressive loading."""
        print("Creating levels of detail...")
        
        # Sort nodes by importance
        sorted_nodes = sorted(importance_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Define LOD levels
        lod_levels = {
            'overview': 0.8,    # Top 20% most important nodes
            'detailed': 0.5,    # Top 50% most important nodes  
            'complete': 1.0     # All nodes
        }
        
        lod_data = {}
        
        for level_name, threshold in lod_levels.items():
            num_nodes = int(len(sorted_nodes) * threshold)
            selected_nodes = [node_id for node_id, _ in sorted_nodes[:num_nodes]]
            
            # Create subgraph with selected nodes and their connections
            subgraph = self.graph.subgraph(selected_nodes).copy()
            
            # Convert to visualization format
            nodes = []
            for node_id in selected_nodes:
                concept = self.concepts_df[self.concepts_df['id'] == node_id].iloc[0]
                node_data = {
                    'id': node_id,
                    'label': concept['name'],
                    'group': concept['strand'] if pd.notna(concept['strand']) else 'Unknown',
                    'title': concept['explanation'] if pd.notna(concept['explanation']) else concept['name'],
                    'importance': importance_scores[node_id],
                    'broader_concept': concept.get('broader_concept', '')
                }
                
                # Add optional fields if they exist
                if 'grade_level' in concept:
                    node_data['grade_level'] = concept['grade_level']
                if 'difficulty' in concept:
                    node_data['difficulty'] = concept['difficulty']
                    
                nodes.append(node_data)
            
            edges = []
            for from_node, to_node, data in subgraph.edges(data=True):
                edges.append({
                    'from': from_node,
                    'to': to_node,
                    'title': data.get('explanation', 'Prerequisite relationship')
                })
            
            lod_data[level_name] = {
                'nodes': nodes,
                'edges': edges,
                'metadata': {
                    'level': level_name,
                    'node_count': len(nodes),
                    'edge_count': len(edges),
                    'importance_threshold': threshold
                }
            }
            
            print(f"  {level_name}: {len(nodes)} nodes, {len(edges)} edges")
        
        return lod_data
    
    def create_clusters(self) -> Dict[str, Any]:
        """Create cluster data for different zoom levels."""
        print("Creating cluster data...")
        
        # Group by strand
        strand_clusters = defaultdict(list)
        for _, concept in self.concepts_df.iterrows():
            strand = concept['strand'] if pd.notna(concept['strand']) else 'Unknown'
            strand_clusters[strand].append(concept['id'])
        
        # Create cluster centers and bounds
        clusters = {}
        for strand, node_ids in strand_clusters.items():
            # Calculate cluster center (average of node positions if available)
            cluster_nodes = []
            for node_id in node_ids:
                concept = self.concepts_df[self.concepts_df['id'] == node_id].iloc[0]
                cluster_nodes.append({
                    'id': node_id,
                    'label': concept['name'],
                    'group': strand,
                    'title': concept['explanation'] if pd.notna(concept['explanation']) else concept['name']
                })
            
            clusters[strand] = {
                'id': f"cluster_{strand}",
                'label': strand,
                'nodes': cluster_nodes,
                'node_count': len(cluster_nodes),
                'center': {'x': 0, 'y': 0},  # Will be calculated during layout
                'bounds': {'x': 0, 'y': 0, 'width': 0, 'height': 0}
            }
        
        print(f"Created {len(clusters)} clusters")
        return clusters
    
    def optimize_layout(self, nodes: List[Dict], edges: List[Dict]) -> Tuple[List[Dict], Dict]:
        """Enhanced layout with gravitational system and better initialization."""
        print("Optimizing layout with enhanced gravitational system...")
        
        # Create a subgraph for layout calculation
        layout_graph = nx.DiGraph()
        
        # Add nodes with importance weights
        for node in nodes:
            layout_graph.add_node(node['id'], importance=node.get('importance', 0.5))
        
        # Add edges
        for edge in edges:
            layout_graph.add_edge(edge['from'], edge['to'])
        
        # Step 1: Initial positioning by strand clusters
        initial_pos = self.create_strand_based_initial_positions(nodes)
        
        # Step 2: Enhanced spring layout with gravity
        try:
            pos = nx.spring_layout(
                layout_graph, 
                pos=initial_pos,  # Use initial positions
                k=50,             # Much larger spring constant for many nodes
                iterations=200,   # More iterations for better convergence
                seed=42
            )
        except:
            # Fallback with better parameters
            pos = nx.spring_layout(
                layout_graph, 
                pos=initial_pos,
                k=30,
                iterations=100,
                seed=42
            )
        
        # Step 3: Apply gravitational forces
        pos = self.apply_gravitational_forces(pos, nodes, layout_graph)
        
        # Step 4: Apply positions to nodes
        for node in nodes:
            if node['id'] in pos:
                node['x'] = pos[node['id']][0] * 1000  # Scale up
                node['y'] = pos[node['id']][1] * 1000
            else:
                node['x'] = np.random.uniform(-500, 500)
                node['y'] = np.random.uniform(-500, 500)
        
        # Calculate bounds
        if nodes:
            x_coords = [node['x'] for node in nodes]
            y_coords = [node['y'] for node in nodes]
            bounds = {
                'min_x': min(x_coords),
                'max_x': max(x_coords),
                'min_y': min(y_coords),
                'max_y': max(y_coords),
                'center_x': (min(x_coords) + max(x_coords)) / 2,
                'center_y': (min(y_coords) + max(y_coords)) / 2
            }
        else:
            bounds = {'min_x': 0, 'max_x': 0, 'min_y': 0, 'max_y': 0, 'center_x': 0, 'center_y': 0}
        
        return nodes, bounds
    
    def create_strand_based_initial_positions(self, nodes: List[Dict]) -> Dict[str, Tuple[float, float]]:
        """Create initial positions based on strand clusters."""
        # Define strand cluster positions in a circle
        strands = list(set(node.get('group', 'Unknown') for node in nodes))
        num_strands = len(strands)
        
        # Create positions in a circle
        strand_positions = {}
        radius = 5.0  # Base radius
        
        for i, strand in enumerate(strands):
            angle = 2 * np.pi * i / num_strands
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            strand_positions[strand] = (x, y)
        
        # Assign initial positions to nodes
        initial_pos = {}
        for node in nodes:
            strand = node.get('group', 'Unknown')
            base_x, base_y = strand_positions[strand]
            
            # Add some randomness around the strand center
            importance = node.get('importance', 0.5)
            noise_scale = 0.5 + (1 - importance) * 0.5  # Less important nodes spread more
            
            x = base_x + np.random.normal(0, noise_scale)
            y = base_y + np.random.normal(0, noise_scale)
            
            initial_pos[node['id']] = (x, y)
        
        return initial_pos
    
    def apply_gravitational_forces(self, pos: Dict, nodes: List[Dict], graph: nx.DiGraph) -> Dict:
        """Apply gravitational forces to improve layout."""
        # Parameters
        gravity_strength = 0.1
        repulsion_strength = 0.5
        attraction_strength = 0.3
        
        # Convert to numpy arrays for easier computation
        node_ids = list(pos.keys())
        positions = np.array([pos[node_id] for node_id in node_ids])
        
        # Apply forces for several iterations
        for iteration in range(50):
            forces = np.zeros_like(positions)
            
            # Gravitational force towards center
            center = np.mean(positions, axis=0)
            for i, pos_i in enumerate(positions):
                direction = center - pos_i
                distance = np.linalg.norm(direction)
                if distance > 0:
                    forces[i] += gravity_strength * direction / distance
            
            # Repulsion between all nodes
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    direction = positions[i] - positions[j]
                    distance = np.linalg.norm(direction)
                    if distance > 0:
                        force = repulsion_strength / (distance ** 2)
                        forces[i] += force * direction / distance
                        forces[j] -= force * direction / distance
            
            # Attraction along edges
            for edge in graph.edges():
                if edge[0] in pos and edge[1] in pos:
                    i = node_ids.index(edge[0])
                    j = node_ids.index(edge[1])
                    
                    direction = positions[j] - positions[i]
                    distance = np.linalg.norm(direction)
                    if distance > 0:
                        force = attraction_strength * distance
                        forces[i] += force * direction / distance
                        forces[j] -= force * direction / distance
            
            # Apply forces
            positions += forces * 0.1  # Damping factor
        
        # Convert back to dictionary
        new_pos = {}
        for i, node_id in enumerate(node_ids):
            new_pos[node_id] = tuple(positions[i])
        
        return new_pos
    
    def create_metadata(self) -> Dict[str, Any]:
        """Create comprehensive metadata for the visualization."""
        strands = sorted(self.concepts_df['strand'].dropna().unique().tolist())
        
        # Check if optional columns exist
        grade_levels = []
        difficulties = []
        if 'grade_level' in self.concepts_df.columns:
            grade_levels = sorted(self.concepts_df['grade_level'].dropna().unique().tolist())
        if 'difficulty' in self.concepts_df.columns:
            difficulties = sorted(self.concepts_df['difficulty'].dropna().unique().tolist())
        
        return {
            'total_nodes': len(self.concepts_df),
            'total_edges': len(self.relationships_df),
            'strands': strands,
            'grade_levels': grade_levels,
            'difficulties': difficulties,
            'generated_at': pd.Timestamp.now().isoformat(),
            'version': '2.0'
        }
    
    def process(self, concepts_file: str, relationships_file: str, output_dir: str = '_static'):
        """Main processing function."""
        print("🚀 Starting advanced graph processing...")
        
        # Load data
        self.load_data(concepts_file, relationships_file)
        
        # Calculate importance scores
        importance_scores = self.calculate_importance_scores()
        
        # Create levels of detail
        lod_data = self.create_levels_of_detail(importance_scores)
        
        # Create clusters
        clusters = self.create_clusters()
        
        # Process each LOD level
        processed_data = {}
        for level_name, data in lod_data.items():
            print(f"Processing {level_name} level...")
            
            # Optimize layout
            optimized_nodes, bounds = self.optimize_layout(data['nodes'], data['edges'])
            
            # Create final data structure
            processed_data[level_name] = {
                'nodes': optimized_nodes,
                'edges': data['edges'],
                'bounds': bounds,
                'metadata': {
                    **data['metadata'],
                    'bounds': bounds,
                    'strands': list(set(node['group'] for node in optimized_nodes))
                }
            }
        
        # Create metadata
        metadata = self.create_metadata()
        
        # Create final output structure
        output_data = {
            'metadata': metadata,
            'levels': processed_data,
            'clusters': clusters,
            'importance_scores': importance_scores
        }
        
        # Save to file
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'advanced-graph-data.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Advanced graph data saved to: {output_file}")
        print(f"📊 Total size: {os.path.getsize(output_file) / 1024:.1f} KB")
        
        # Print statistics
        print("\n📈 Processing Statistics:")
        for level_name, data in processed_data.items():
            print(f"  {level_name}: {data['metadata']['node_count']} nodes, {data['metadata']['edge_count']} edges")
        
        return output_data
    
    def process_from_json(self, json_file: str, output_dir: str = '_static'):
        """Process graph data from existing JSON file."""
        print("🚀 Starting advanced graph processing from JSON...")
        
        # Load the JSON data
        with open(json_file, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        
        print(f"Loaded {len(graph_data['nodes'])} nodes and {len(graph_data['edges'])} edges from JSON")
        
        # Convert to the format we need
        nodes = graph_data['nodes']
        edges = graph_data['edges']
        
        # Create NetworkX graph for analysis
        self.graph = nx.DiGraph()
        
        # Add nodes
        for node in nodes:
            self.graph.add_node(node['id'], **node)
        
        # Add edges
        for edge in edges:
            self.graph.add_edge(edge['from'], edge['to'], **edge)
        
        print(f"Built graph with {self.graph.number_of_nodes()} nodes and {self.graph.number_of_edges()} edges")
        
        # Calculate importance scores
        importance_scores = self.calculate_importance_scores()
        
        # Create levels of detail
        lod_data = self.create_levels_of_detail_from_nodes(nodes, edges, importance_scores)
        
        # Create clusters
        clusters = self.create_clusters_from_nodes(nodes)
        
        # Process each LOD level
        processed_data = {}
        for level_name, data in lod_data.items():
            print(f"Processing {level_name} level...")
            
            # Optimize layout
            optimized_nodes, bounds = self.optimize_layout(data['nodes'], data['edges'])
            
            # Create final data structure
            processed_data[level_name] = {
                'nodes': optimized_nodes,
                'edges': data['edges'],
                'bounds': bounds,
                'metadata': {
                    **data['metadata'],
                    'bounds': bounds,
                    'strands': list(set(node['group'] for node in optimized_nodes))
                }
            }
        
        # Create metadata
        metadata = self.create_metadata_from_nodes(nodes)
        
        # Create final output structure
        output_data = {
            'metadata': metadata,
            'levels': processed_data,
            'clusters': clusters,
            'importance_scores': importance_scores
        }
        
        # Save to file
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'advanced-graph-data.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Advanced graph data saved to: {output_file}")
        print(f"📊 Total size: {os.path.getsize(output_file) / 1024:.1f} KB")
        
        # Print statistics
        print("\n📈 Processing Statistics:")
        for level_name, data in processed_data.items():
            print(f"  {level_name}: {data['metadata']['node_count']} nodes, {data['metadata']['edge_count']} edges")
        
        return output_data
    
    def create_levels_of_detail_from_nodes(self, nodes: List[Dict], edges: List[Dict], importance_scores: Dict[str, float]) -> Dict[str, Any]:
        """Create multiple levels of detail from existing node/edge data."""
        print("Creating levels of detail from JSON data...")
        
        # Sort nodes by importance
        sorted_nodes = sorted(importance_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Define LOD levels
        lod_levels = {
            'overview': 0.1,    # Top 10% most important nodes
            'detailed': 0.3,    # Top 30% most important nodes  
            'complete': 1.0     # All nodes
        }
        
        lod_data = {}
        
        for level_name, threshold in lod_levels.items():
            num_nodes = int(len(sorted_nodes) * threshold)
            selected_node_ids = [node_id for node_id, _ in sorted_nodes[:num_nodes]]
            
            # Filter nodes and edges
            selected_nodes = [node for node in nodes if node['id'] in selected_node_ids]
            selected_edges = [edge for edge in edges if edge['from'] in selected_node_ids and edge['to'] in selected_node_ids]
            
            # Add importance scores to nodes
            for node in selected_nodes:
                node['importance'] = importance_scores.get(node['id'], 0.5)
            
            lod_data[level_name] = {
                'nodes': selected_nodes,
                'edges': selected_edges,
                'metadata': {
                    'level': level_name,
                    'node_count': len(selected_nodes),
                    'edge_count': len(selected_edges),
                    'importance_threshold': threshold
                }
            }
            
            print(f"  {level_name}: {len(selected_nodes)} nodes, {len(selected_edges)} edges")
        
        return lod_data
    
    def create_clusters_from_nodes(self, nodes: List[Dict]) -> Dict[str, Any]:
        """Create cluster data from existing node data."""
        print("Creating cluster data from JSON data...")
        
        # Group by strand
        strand_clusters = defaultdict(list)
        for node in nodes:
            strand = node.get('group', 'Unknown')
            strand_clusters[strand].append(node['id'])
        
        # Create cluster centers and bounds
        clusters = {}
        for strand, node_ids in strand_clusters.items():
            # Get nodes for this cluster
            cluster_nodes = [node for node in nodes if node['id'] in node_ids]
            
            clusters[strand] = {
                'id': f"cluster_{strand}",
                'label': strand,
                'nodes': cluster_nodes,
                'node_count': len(cluster_nodes),
                'center': {'x': 0, 'y': 0},  # Will be calculated during layout
                'bounds': {'x': 0, 'y': 0, 'width': 0, 'height': 0}
            }
        
        print(f"Created {len(clusters)} clusters")
        return clusters
    
    def create_metadata_from_nodes(self, nodes: List[Dict]) -> Dict[str, Any]:
        """Create comprehensive metadata from existing node data."""
        strands = sorted(list(set(node.get('group', 'Unknown') for node in nodes)))
        
        # Extract grade levels and difficulties if they exist
        grade_levels = []
        difficulties = []
        for node in nodes:
            if 'grade_level' in node and node['grade_level']:
                grade_levels.append(node['grade_level'])
            if 'difficulty' in node and node['difficulty']:
                difficulties.append(node['difficulty'])
        
        grade_levels = sorted(list(set(grade_levels)))
        difficulties = sorted(list(set(difficulties)))
        
        return {
            'total_nodes': len(nodes),
            'total_edges': len(self.graph.edges()) if self.graph else 0,
            'strands': strands,
            'grade_levels': grade_levels,
            'difficulties': difficulties,
            'generated_at': pd.Timestamp.now().isoformat(),
            'version': '2.0'
        }

def main():
    """Main function to run the advanced graph processor."""
    processor = AdvancedGraphProcessor()
    
    # Check if we have the large graph-data.json file
    large_graph_file = 'Ontology/ontology_builder/graph-data.json'
    if os.path.exists(large_graph_file):
        print(f"🚀 Found large graph data file: {large_graph_file}")
        processor.process_from_json(large_graph_file)
    else:
        # Fallback to CSV files
        print("📁 Large graph data not found, using CSV files...")
        
        def find_file_by_pattern(directory, pattern):
            for filename in os.listdir(directory):
                if pattern in filename.lower() and filename.endswith('.csv'):
                    return os.path.join(directory, filename)
            return None
        
        concepts_file = find_file_by_pattern('Ontology', 'concepts')
        relationships_file = find_file_by_pattern('Ontology', 'relationships')
        
        if not concepts_file or not relationships_file:
            print("❌ Error: Could not find concepts and relationships CSV files in Ontology directory")
            return
        
        # Process the data
        processor.process(concepts_file, relationships_file)

if __name__ == "__main__":
    main()
