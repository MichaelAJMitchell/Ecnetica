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
DEFAULT_MODEL = "gpt-4.1"  # Primary model for highest quality extraction
FALLBACK_MODELS = ["gpt-5-mini", "gpt-4.1-mini", "gpt-5", "gpt-4o-mini"]  # Backup models if primary fails

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

Return as a JSON array of concepts, where each concept has this exact structure:
[
  {{
    "name": "concept_name_here",
    "explanation": "brief_description_of_the_concept",
    "broader_concept": "higher_level_category_or_parent_concept",
    "strand": "mathematical_strand_e.g._Algebra_Geometry_Number_Theory",
    "grade_level": "educational_level_e.g._Elementary_Middle_High_College",
    "difficulty": "complexity_level_e.g._Basic_Intermediate_Advanced"
  }}
]

IMPORTANT: Every concept MUST have a "name" field. All other fields are optional but recommended.
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

Return as a JSON array of relationships, where each relationship has this exact structure:
[
  {{
    "prerequisite_concept_id": "uuid_of_prerequisite_concept",
    "dependent_concept_id": "uuid_of_dependent_concept", 
    "relationship_type": "prerequisite_builds_on_related_supports",
    "strength": 0.8
  }}
]

IMPORTANT: 
- Use the concept IDs from the concept_ids mapping in the context for EXISTING concepts
- For NEW concepts (those just extracted), use the concept name as a placeholder
- The system will resolve these placeholders to proper IDs later
- Strength should be 0.0 to 1.0
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

Return a JSON object with this exact structure:
{{
  "concepts_valid": true,
  "relationships_valid": true,
  "quality_score": 8,
  "feedback": "brief_explanation_of_any_issues_found"
}}

IMPORTANT: concepts_valid and relationships_valid must be boolean values. quality_score must be 1-10.
""" 