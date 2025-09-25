#!/usr/bin/env python3
"""
Ontology Builder - Minimal mathematical concept extraction tool

This is the main entry point for the ontology builder system.
It provides a command-line interface for processing individual files or entire directories
to extract mathematical concepts and relationships using LLMs.
"""

import argparse
from extractor import ConceptExtractor

def main():
    """Main function with command-line argument parsing."""
    parser = argparse.ArgumentParser(description='Extract mathematical concepts and relationships')
    parser.add_argument('--file', '-f', type=str, help='Process single file')
    parser.add_argument('--directory', '-d', type=str, help='Process directory')
    parser.add_argument('--output', '-o', type=str, default='graph-data.json', help='Output JSON file')
    parser.add_argument('--chapters', '-c', type=int, default=1, help='Number of chapters per chunk (MD files only)')
    
    args = parser.parse_args()
    
    # Initialize the main extraction engine
    extractor = ConceptExtractor()
    
    # Route to appropriate processing method based on arguments
    if args.file:
        extractor.process_file(args.file, args.output, args.chapters)
    elif args.directory:
        extractor.process_directory(args.directory, args.output, args.chapters)
    else:
        print("Please specify --file or --directory")

if __name__ == "__main__":
    main() 