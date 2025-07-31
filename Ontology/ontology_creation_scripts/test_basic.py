#!/usr/bin/env python3
"""
Basic test script for Mathematical Concept Scraper

This script tests the core functionality without requiring the OpenAI API key.
"""

import os
import tempfile
from file_processor import FileProcessor
from data_manager import DataManager

def test_file_processor():
    """Test the file processor functionality."""
    print("Testing File Processor...")
    
    processor = FileProcessor()
    
    # Test supported formats
    assert processor.is_supported_format("test.pdf") == True
    assert processor.is_supported_format("test.csv") == True
    assert processor.is_supported_format("test.txt") == True
    assert processor.is_supported_format("test.tex") == True
    assert processor.is_supported_format("test.docx") == True
    assert processor.is_supported_format("test.xyz") == False
    
    print("✓ File format detection working correctly")
    
    # Test text chunking
    test_text = "This is a test. " * 100  # Create a long text
    chunks = processor.chunk_text(test_text, chunk_size=100, overlap=20)
    
    assert len(chunks) > 1, "Text should be chunked"
    # Allow chunks to exceed size slightly when breaking at sentence boundaries
    assert all(len(chunk) <= 150 for chunk in chunks), "Chunks should not exceed size by too much"
    
    print("✓ Text chunking working correctly")
    
    # Test CSV processing
    csv_content = """concept,description,strand
addition,Adding numbers,Number
subtraction,Subtracting numbers,Number"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(csv_content)
        csv_file = f.name
    
    try:
        processed_text = processor.process_csv(csv_file)
        assert "concept" in processed_text
        assert "addition" in processed_text
        print("✓ CSV processing working correctly")
    finally:
        os.unlink(csv_file)
    
    # Test TXT processing
    txt_content = "This is a test text file with mathematical concepts."
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(txt_content)
        txt_file = f.name
    
    try:
        processed_text = processor.process_txt(txt_file)
        assert processed_text == txt_content
        print("✓ TXT processing working correctly")
    finally:
        os.unlink(txt_file)

def test_data_manager():
    """Test the data manager functionality."""
    print("\nTesting Data Manager...")
    
    # Create a temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Temporarily change the output directory
        original_output_dir = DataManager.OUTPUT_DIR if hasattr(DataManager, 'OUTPUT_DIR') else "output"
        
        # Create a test data manager
        manager = DataManager()
        
        # Test concept addition
        test_concepts = [
            {
                "name": "Single digit addition",
                "explanation": "Adding numbers 0-9",
                "broader_concept": "Addition",
                "strand": "Number",
                "source": "test.txt"
            },
            {
                "name": "Multi-digit addition",
                "explanation": "Adding numbers with multiple digits",
                "broader_concept": "Addition",
                "strand": "Number",
                "source": "test.txt"
            }
        ]
        
        added_concepts, existing_concepts = manager.add_concepts(test_concepts)
        assert len(added_concepts) == 2
        assert len(existing_concepts) == 0
        print("✓ Concept addition working correctly")
        
        # Test duplicate detection
        duplicate_concepts = [
            {
                "name": "Single digit addition",
                "explanation": "Adding numbers 0-9",
                "broader_concept": "Addition",
                "strand": "Number",
                "source": "test2.txt"
            }
        ]
        
        added_concepts, existing_concepts = manager.add_concepts(duplicate_concepts)
        assert len(added_concepts) == 0
        assert len(existing_concepts) == 1
        print("✓ Duplicate detection working correctly")
        
        # Test relationship addition
        test_relationships = [
            {
                "prerequisite": "Single digit addition",
                "dependent": "Multi-digit addition",
                "explanation": "Must know single digit addition before multi-digit",
                "source": "test.txt"
            }
        ]
        
        added_relationships, existing_relationships = manager.add_relationships(test_relationships)
        assert len(added_relationships) == 1
        assert len(existing_relationships) == 0
        print("✓ Relationship addition working correctly")
        
        # Test statistics
        stats = manager.get_statistics()
        assert stats['total_concepts'] == 2
        assert stats['total_relationships'] == 1
        assert stats['unique_sources'] == 1
        print("✓ Statistics working correctly")

def main():
    """Run all basic tests."""
    print("=" * 60)
    print("MATHEMATICAL CONCEPT SCRAPER - BASIC TESTS")
    print("=" * 60)
    
    try:
        test_file_processor()
        test_data_manager()
        
        print("\n" + "=" * 60)
        print("ALL BASIC TESTS PASSED! ✓")
        print("=" * 60)
        print("\nThe core functionality is working correctly.")
        print("To use the full scraper, you'll need to:")
        print("1. Set your OpenAI API key in a .env file")
        print("2. Run: python3 main.py --file your_document.pdf")
        
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 