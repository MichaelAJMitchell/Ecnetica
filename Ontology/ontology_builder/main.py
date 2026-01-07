#!/usr/bin/env python3
"""
Ontology Builder - Minimal mathematical concept extraction tool

This is the main entry point for the ontology builder system.
It provides a command-line interface for processing individual files or entire directories
to extract mathematical concepts and relationships using LLMs.
"""

import argparse
import os
import importlib
from extractor import ConceptExtractor

# Directory containing this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Default output location for live ontologies
LIVE_ONTOLOGY_DIR = os.path.join(SCRIPT_DIR, '..', 'live_ontology')

# Available configs
AVAILABLE_CONFIGS = {
    'chem': 'config_chem',
    'physics': 'config_physics',
}

def get_default_output_path(config_name: str) -> str:
    """Generate the default output path based on config name."""
    os.makedirs(LIVE_ONTOLOGY_DIR, exist_ok=True)
    return os.path.join(LIVE_ONTOLOGY_DIR, f'graph-data-{config_name}.json')

def load_config(config_name: str):
    """Dynamically load a config module."""
    if config_name not in AVAILABLE_CONFIGS:
        raise ValueError(f"Unknown config: {config_name}. Available: {list(AVAILABLE_CONFIGS.keys())}")
    
    module_name = AVAILABLE_CONFIGS[config_name]
    return importlib.import_module(module_name)

def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(description='Extract mathematical concepts and relationships')
    parser.add_argument('--file', '-f', type=str, help='Process single file')
    parser.add_argument('--directory', '-d', type=str, help='Process directory')
    parser.add_argument('--output', '-o', type=str, help='Output JSON file (default: ../live_ontology/graph-data-{config}.json)')
    parser.add_argument('--config', '-c', type=str, default='physics', 
                        choices=list(AVAILABLE_CONFIGS.keys()),
                        help='Config to use: chem or physics (default: physics)')
    
    args = parser.parse_args()
    
    # Load the selected config
    config = load_config(args.config)
    
    # Determine output path
    output_file = args.output if args.output else get_default_output_path(args.config)
    
    print(f"Using config: {args.config}")
    print(f"Output file: {output_file}")
    
    # Initialize the main extraction engine with configurable chunking
    # Pass config module to extractor
    extractor = ConceptExtractor(
        chapters_per_chunk=1, 
        rows_per_chunk=1,
        config=config
    )
    
    # Route to appropriate processing method based on arguments
    if args.file:
        extractor.process_file(args.file, output_file)
    elif args.directory:
        extractor.process_directory(args.directory, output_file)
    else:
        print("Please specify --file or --directory")
        print(f"\nExample usage:")
        print(f"  python main.py -d ../ontology_source_materials/chemistry -c chem")
        print(f"  python main.py -d ../ontology_source_materials/physics -c physics")

if __name__ == "__main__":
    main()
