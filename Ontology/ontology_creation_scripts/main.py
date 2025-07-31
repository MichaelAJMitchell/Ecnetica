#!/usr/bin/env python3
"""
Mathematical Concept Scraper

A tool for extracting mathematical concepts and prerequisite relationships
from educational documents to build a knowledge graph.

Usage:
    python main.py --file path/to/file.pdf
    python main.py --directory path/to/documents/
    python main.py --input-folder path/to/input/folder/
    python main.py --files file1.pdf file2.txt file3.csv
    python main.py --stats
"""

import argparse
import sys
import os
from concept_scraper import ConceptScraper

def main():
    parser = argparse.ArgumentParser(
        description="Extract mathematical concepts and relationships from educational documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --file curriculum.pdf
  python main.py --directory ./documents/
  python main.py --input-folder ./input_folder/
  python main.py --files math1.pdf math2.txt curriculum.csv
  python main.py --stats
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Process a single file'
    )
    
    parser.add_argument(
        '--directory', '-d',
        type=str,
        help='Process all supported files in a directory'
    )
    
    parser.add_argument(
        '--input-folder', '-i',
        type=str,
        help='Process all supported files in an input folder'
    )
    
    parser.add_argument(
        '--files', '-F',
        nargs='+',
        type=str,
        help='Process multiple specific files'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='Show current knowledge graph statistics'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='output',
        help='Output directory for CSV files (default: output)'
    )
    
    args = parser.parse_args()
    
    # Check if any action is specified
    if not any([args.file, args.directory, args.input_folder, args.files, args.stats]):
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize the scraper
        print("Initializing Mathematical Concept Scraper...")
        scraper = ConceptScraper()
        
        # Show statistics if requested
        if args.stats:
            scraper.print_statistics()
            return
        
        results = []
        
        # Process single file
        if args.file:
            print(f"Processing single file: {args.file}")
            result = scraper.process_single_file(args.file)
            results.append(result)
        
        # Process directory
        elif args.directory:
            print(f"Processing directory: {args.directory}")
            results = scraper.process_directory(args.directory)
        
        # Process input folder
        elif args.input_folder:
            print(f"Processing input folder: {args.input_folder}")
            results = scraper.process_directory(args.input_folder)
        
        # Process multiple files
        elif args.files:
            print(f"Processing {len(args.files)} files")
            results = scraper.process_files(args.files)
        
        # Print summary
        if results:
            print(f"\n{'='*60}")
            print("PROCESSING SUMMARY")
            print(f"{'='*60}")
            
            successful = 0
            total_concepts = 0
            total_relationships = 0
            
            for result in results:
                if result['success']:
                    successful += 1
                    total_concepts += result['concepts_added']
                    total_relationships += result['relationships_added']
                    print(f"✓ {os.path.basename(result['file'])}: "
                          f"{result['concepts_added']} concepts, "
                          f"{result['relationships_added']} relationships")
                else:
                    print(f"✗ {os.path.basename(result['file'])}: {result['error']}")
            
            print(f"\nSuccessfully processed: {successful}/{len(results)} files")
            print(f"Total new concepts: {total_concepts}")
            print(f"Total new relationships: {total_relationships}")
            
            # Show final statistics
            scraper.print_statistics()
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 