#!/usr/bin/env python3
"""
Example usage of the Mathematical Concept Scraper

This script demonstrates various ways to use the scraper programmatically.
"""

import os
from concept_scraper import ConceptScraper

def example_single_file():
    """Example: Process a single file."""
    print("Example 1: Processing a single file")
    print("-" * 40)
    
    scraper = ConceptScraper()
    
    # Process a single file
    result = scraper.process_single_file("path/to/your/document.pdf")
    
    if result['success']:
        print(f"✓ Successfully processed {result['file']}")
        print(f"  Concepts added: {result['concepts_added']}")
        print(f"  Relationships added: {result['relationships_added']}")
    else:
        print(f"✗ Failed to process {result['file']}: {result['error']}")

def example_directory():
    """Example: Process all files in a directory."""
    print("\nExample 2: Processing a directory")
    print("-" * 40)
    
    scraper = ConceptScraper()
    
    # Process all supported files in a directory
    results = scraper.process_directory("../ontology_source_materials/")
    
    successful = sum(1 for r in results if r['success'])
    total_concepts = sum(r['concepts_added'] for r in results if r['success'])
    total_relationships = sum(r['relationships_added'] for r in results if r['success'])
    
    print(f"Processed {len(results)} files, {successful} successful")
    print(f"Total concepts added: {total_concepts}")
    print(f"Total relationships added: {total_relationships}")
    print("Output files saved to: ../ (Ontology directory)")

def example_statistics():
    """Example: Get and display statistics."""
    print("\nExample 3: Getting statistics")
    print("-" * 40)
    
    scraper = ConceptScraper()
    
    # Get detailed statistics
    stats = scraper.get_statistics()
    
    print(f"Total concepts: {stats['total_concepts']}")
    print(f"Total relationships: {stats['total_relationships']}")
    print(f"Unique sources: {stats['unique_sources']}")
    
    if 'strand_distribution' in stats:
        print("\nConcept distribution by strand:")
        for strand, count in sorted(stats['strand_distribution'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {strand}: {count}")
    
    # Or use the built-in print function
    print("\nDetailed statistics:")
    scraper.print_statistics()

def main():
    """Run all examples."""
    print("=" * 60)
    print("MATHEMATICAL CONCEPT SCRAPER - USAGE EXAMPLES")
    print("=" * 60)
    
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY environment variable is not set!")
        print("Please set your OpenAI API key before running these examples.")
        print("You can create a .env file with: OPENAI_API_KEY=your_key_here")
        return
    
    # Run examples (commented out to avoid actual API calls)
    print("Note: These examples are for demonstration purposes.")
    print("Uncomment the function calls below to run actual examples.")
    print()
    
    # Uncomment the lines below to run actual examples:
    # example_single_file()
    # example_directory()
    # example_statistics()
    
    print("To run actual examples:")
    print("1. Make sure you have documents in ../ontology_source_materials/")
    print("2. Uncomment the function calls in this script")
    print("3. Run: python3 example_usage.py")
    print("4. Output files will be saved to ../ (Ontology directory)")
    print("5. Existing files will be automatically archived to ../ontology_archive/")

if __name__ == "__main__":
    main() 