#!/usr/bin/env python3
"""
Test script for enhanced extraction features:
- Multi-stage concept extraction
- Semantic chunking
- Context-aware processing
"""

import os
import sys
from file_processor import FileProcessor
from openai_client import OpenAIClient
from data_manager import DataManager

def test_semantic_chunking():
    """Test semantic chunking with sample text."""
    print("Testing semantic chunking...")
    
    # Sample text with semantic boundaries
    sample_text = """
# Chapter 1: Introduction to Numbers

## Section 1.1: Natural Numbers
Natural numbers are the counting numbers: 1, 2, 3, 4, 5, and so on.
We use natural numbers for counting objects.

## Section 1.2: Addition
Addition is combining two or more numbers to find their sum.
For example, 2 + 3 = 5.

# Chapter 2: Basic Operations

## Section 2.1: Subtraction
Subtraction is taking away one number from another.
For example, 5 - 3 = 2.

## Section 2.2: Multiplication
Multiplication is repeated addition.
For example, 3 × 4 = 12.
"""
    
    # Test semantic chunking
    chunks = FileProcessor.semantic_chunk_text(sample_text, chunk_size=500, overlap=50)
    
    print(f"Created {len(chunks)} semantic chunks:")
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i+1}:")
        print(f"Length: {len(chunk)} characters")
        print(f"Content: {chunk[:100]}...")
    
    return chunks

def test_context_aware_chunks():
    """Test context-aware chunk creation."""
    print("\nTesting context-aware chunks...")
    
    sample_text = """
# Chapter 1: Introduction to Numbers

Natural numbers are the counting numbers: 1, 2, 3, 4, 5, and so on.
We use natural numbers for counting objects.

Addition is combining two or more numbers to find their sum.
For example, 2 + 3 = 5.

Subtraction is taking away one number from another.
For example, 5 - 3 = 2.
"""
    
    # Test context-aware chunking
    context_chunks = FileProcessor.create_context_aware_chunks(sample_text, chunk_size=300, overlap=50)
    
    print(f"Created {len(context_chunks)} context-aware chunks:")
    for i, chunk_info in enumerate(context_chunks):
        print(f"\nChunk {i+1}:")
        print(f"Document context: {chunk_info['document_context']}")
        print(f"Content length: {len(chunk_info['chunk_content'])} characters")
        if chunk_info['previous_context']:
            print(f"Previous context: {chunk_info['previous_context'][:50]}...")
        if chunk_info['next_context']:
            print(f"Next context: {chunk_info['next_context'][:50]}...")
    
    return context_chunks

def test_multi_stage_extraction():
    """Test multi-stage concept extraction with sample text."""
    print("\nTesting multi-stage concept extraction...")
    
    # Initialize components
    openai_client = OpenAIClient()
    data_manager = DataManager()
    
    # Sample text for testing
    sample_text = """
    In this chapter, we explore the fundamental concepts of arithmetic.
    
    We begin with natural numbers, which are the counting numbers: 1, 2, 3, 4, 5, and so on.
    Students learn to count objects using natural numbers.
    
    Next, we introduce addition, which is combining two or more numbers to find their sum.
    For example, when we add 2 and 3, we get 5. This is written as 2 + 3 = 5.
    
    We also cover subtraction, which is taking away one number from another.
    For example, 5 - 3 = 2 means we take away 3 from 5 and get 2.
    
    Finally, we learn about multiplication, which is repeated addition.
    For example, 3 × 4 = 12 means we add 3 four times: 3 + 3 + 3 + 3 = 12.
    """
    
    # Get existing concepts for context
    existing_concepts = data_manager.get_concepts_for_context()
    
    # Test multi-stage extraction
    try:
        concepts = openai_client.extract_concepts_multi_stage(
            sample_text, existing_concepts, "test_source"
        )
        
        print(f"Extracted {len(concepts)} concepts using multi-stage approach:")
        for concept in concepts:
            print(f"  - {concept.get('name', 'Unknown')}: {concept.get('explanation', '')}")
        
        return concepts
        
    except Exception as e:
        print(f"Error in multi-stage extraction: {str(e)}")
        return []

def main():
    """Run all tests."""
    print("Enhanced Extraction Test Suite")
    print("=" * 50)
    
    # Test 1: Semantic chunking
    test_semantic_chunking()
    
    # Test 2: Context-aware chunks
    test_context_aware_chunks()
    
    # Test 3: Multi-stage extraction (requires API key)
    print("\nNote: Multi-stage extraction test requires valid OpenAI API key")
    try:
        test_multi_stage_extraction()
    except Exception as e:
        print(f"Multi-stage extraction test failed: {str(e)}")
        print("This is expected if no API key is configured")
    
    print("\nTest suite completed!")

if __name__ == "__main__":
    main() 