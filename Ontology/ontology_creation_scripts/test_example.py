#!/usr/bin/env python3
"""
Test example for the Mathematical Concept Scraper

This script demonstrates how to use the scraper with sample data.
"""

import os
import tempfile
from concept_scraper import ConceptScraper

def create_sample_files():
    """Create sample files for testing."""
    sample_files = {}
    
    # Sample PDF content (simulated)
    sample_files['sample.txt'] = """
    Mathematics Curriculum: Grade 3
    
    Number and Operations
    
    Students will learn single digit addition as a foundational skill. This involves adding numbers from 0 to 9 without carrying. 
    
    Before learning multi-digit addition with carrying, students must understand place value. Place value understanding helps students recognize that the position of a digit determines its value.
    
    Multi-digit addition with carrying builds upon single digit addition. Students learn to add numbers with more than one digit, including the process of carrying when the sum exceeds 9 in any position.
    
    Number line addition is another method for teaching addition. Students use a number line to visualize the addition process by counting forward from the first number.
    
    Geometry
    
    Students begin with basic shapes recognition, identifying circles, squares, triangles, and rectangles. This foundational knowledge is required before learning about shape properties.
    
    Shape properties include understanding that squares have four equal sides and four right angles, while rectangles have four sides with opposite sides equal and four right angles.
    
    Area calculation requires understanding of shape properties. Students learn to calculate the area of rectangles by multiplying length by width.
    
    Algebra
    
    Pattern recognition is introduced through simple repeating patterns. Students identify and continue patterns using shapes, numbers, or colors.
    
    Simple equations with one variable build upon pattern recognition. Students solve equations like x + 3 = 7 by using inverse operations.
    """
    
    # Sample CSV content
    sample_files['sample.csv'] = """concept,description,prerequisite,strand
single digit addition,Adding numbers 0-9 without carrying,,Number
place value,Understanding digit position determines value,,Number
multi-digit addition,Adding numbers with multiple digits,single digit addition,Number
carrying in addition,Process when sum exceeds 9 in any position,place value,Number
number line addition,Using number line to visualize addition,single digit addition,Number
basic shapes,Recognizing circles squares triangles rectangles,,Geometry
shape properties,Understanding sides angles of shapes,basic shapes,Geometry
area calculation,Calculating area of rectangles,shape properties,Geometry
pattern recognition,Identifying and continuing patterns,,Algebra
simple equations,Solving equations with one variable,pattern recognition,Algebra"""
    
    return sample_files

def run_test():
    """Run a test of the concept scraper."""
    print("=" * 60)
    print("MATHEMATICAL CONCEPT SCRAPER - TEST EXAMPLE")
    print("=" * 60)
    
    # Create sample files
    sample_files = create_sample_files()
    
    # Create temporary directory for test files
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f"Created temporary directory: {temp_dir}")
        
        # Write sample files
        for filename, content in sample_files.items():
            filepath = os.path.join(temp_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created sample file: {filename}")
        
        # Initialize scraper
        print("\nInitializing scraper...")
        scraper = ConceptScraper()
        
        # Show initial statistics
        print("\nInitial statistics:")
        scraper.print_statistics()
        
        # Process sample files
        print(f"\nProcessing sample files in: {temp_dir}")
        results = scraper.process_directory(temp_dir)
        
        # Show final statistics
        print("\nFinal statistics:")
        scraper.print_statistics()
        
        # Show results summary
        print("\nProcessing Results:")
        for result in results:
            if result['success']:
                print(f"✓ {os.path.basename(result['file'])}: "
                      f"{result['concepts_added']} concepts, "
                      f"{result['relationships_added']} relationships")
            else:
                print(f"✗ {os.path.basename(result['file'])}: {result['error']}")
        
        print("\n" + "=" * 60)
        print("Test completed! Check the 'output' directory for CSV files.")
        print("=" * 60)

if __name__ == "__main__":
    # Check if OpenAI API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("ERROR: OPENAI_API_KEY environment variable is not set!")
        print("Please set your OpenAI API key before running this test.")
        print("You can create a .env file with: OPENAI_API_KEY=your_key_here")
        exit(1)
    
    run_test() 