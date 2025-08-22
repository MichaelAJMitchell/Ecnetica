"""
Configuration for Ontology Builder

This module contains all configuration settings for the ontology builder system.
It centralizes all configurable parameters, making the system easy to adjust
and maintain. Environment variables are loaded for sensitive information.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This allows you to store sensitive information like API keys separately
load_dotenv()

# LLM Configuration
# These settings control which language models are used and in what order
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')  # Your OpenAI API key from environment
DEFAULT_MODEL = "gpt-5-mini"  # Primary model for highest quality extraction
FALLBACK_MODELS = ["gpt-4o-mini", "gpt-4.1-mini"]  # Backup models if primary fails

# Processing Configuration
# These settings control how documents are chunked for LLM processing
CHUNK_SIZE = 1000000  # Maximum characters per chunk (1M characters)
OVERLAP_SIZE = 200000  # Characters to overlap between chunks (200K characters)

# The overlap ensures that concepts at chunk boundaries aren't lost and
# provides context for the LLM to understand relationships between chunks.
# Larger chunks = more context but higher token usage
# Larger overlap = better context preservation but more processing time

# Output Configuration
# This setting controls the default output file name
DEFAULT_OUTPUT_FILE = "graph-data.json"  # Default JSON output filename

# Prompt Templates
# These prompts will be used by the LLM for each extraction step
# You can customize these prompts to improve extraction quality

CONCEPT_EXTRACTION_PROMPT = """
You are a mathematical education expert. Extract mathematical concepts from the given text.

TEXT TO ANALYZE:
{text}

CONTEXT:
- Source: {context[source_file]}
- Position: {context[chunk_position]}
- Existing concepts: {context[existing_concepts_count]} already extracted
- Existing relationships: {context[existing_relationships_count]} already identified

Focus on:
- Specific mathematical concepts (e.g., "single digit addition" not just "addition")
- Mathematical operations, formulas, theorems, and procedures
- Educational concepts that students need to learn

Return as a JSON array of concepts.
"""

RELATIONSHIP_EXTRACTION_PROMPT = """
You are a mathematical education expert. Identify relationships between mathematical concepts.

TEXT TO ANALYZE:
{text}

NEW CONCEPTS TO ANALYZE:
{concepts}

CONTEXT:
- Source: {context[source_file]}
- Position: {context[chunk_position]}
- New concepts: {context[new_concepts_count]} just extracted
- Existing concepts: {context[existing_concepts_count]} total
- Existing relationships: {context[existing_relationships_count]} total

Focus on:
- Prerequisites: What must be learned before what
- Dependencies: How concepts build on each other
- Logical connections: Related concepts that support each other

Return as a JSON array of relationships.
"""

VERIFICATION_PROMPT = """
You are a mathematical education expert. Verify the quality of extracted concepts and relationships.

CONTEXT:
- Source: {context[source_file]}
- Position: {context[chunk_position]}
- New concepts: {context[new_concepts_count]} to verify
- New relationships: {context[new_relationships_count]} to verify

Check for:
- Concept accuracy: Are the concepts correctly identified?
- Relationship validity: Do the relationships make mathematical sense?
- Completeness: Are important concepts or relationships missing?
- Consistency: Do the extractions align with the source text?

Return a JSON object with:
- concepts_valid: boolean (true if concepts are good quality)
- relationships_valid: boolean (true if relationships are good quality)
- quality_score: number (1-10 overall quality)
- feedback: brief explanation of any issues found
""" 