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
DEFAULT_MODEL = "gpt-5" # Primary model for highest quality extraction
FALLBACK_MODELS = ["gpt-4.1", "gpt-5-mini", "gpt-4.1-mini", "gpt-5", "gpt-4o-mini"]  # Backup models if primary fails

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
### INSTRUCTION
You are a mathematics education expert specializing in curriculum design and concept mapping.
Your job is to extract **atomic mathematical learning concepts** from the input text.  
Follow the rules and output exactly in the required format (no extra text).
First, **think step by step**:
1. Identify candidate mathematical ideas (operations, theorems, definitions, procedures, skills).
2. Filter out those that are too broad, vague, or duplicative (only keep clear, teachable units).
3. For each remaining concept, generate the fields with consistency and internal validation.

### INPUT
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

### OUTPUT FORMAT
Return exactly a JSON **array** of concept objects (no additional commentary), where each concept has this exact structure:  
[
  {{
    "name": "concept_name_here",
    "explanation": "brief_description_of_the_concept",
    "broader_concept": "higher_level_category_or_parent_concept",
    "strand": "mathematical_strand_e.g._Algebra_Geometry_Number_Theory",
    "grade_level": "educational_level_e.g._Elementary_Middle_High_College",
    "difficulty": "complexity_level_e.g._Basic_Intermediate_Advanced"
    (Optional) "confidence_score": a number between 0 and 1 indicating your confidence  
  }}
]

Rules:
- If a candidate is vague or covers multiple distinct ideas, **omit it** rather than produce a low-quality entry.  
- Do not output duplicates — only one object per concept name.  
- Ensure each object is valid JSON, no trailing commas, consistent types.

IMPORTANT: Every concept MUST have a "name" field. All other fields are optional but recommended.

### EXAMPLES  
The following are **good examples** tio be used as inspiration for what should be extracted:

Example 1:
  "name": "Circle Construction with Given Radius",
  "strand": "Geometry",
  "explanation": "Drawing a circle with a specified radius using a compass.",
  "broader_concept": "Geometric Constructions",
  "grade_level": "Middle_High",
  "difficulty": "Basic"

Example 2:
  "name": "Internal Division of a Line Segment",
  "strand": "Geometry",
  "explanation": "Dividing a line segment into a given ratio m:n internally, and finding the coordinates of the dividing point.",
  "broader_concept": "Coordinate Geometry",
  "grade_level": "High",
  "difficulty": "Intermediate"

Bad examples (and why):
Bad Example 1:
  "name": "theorems 7, 8, 11, 12, 13, 16, 17, 18, 20, 21",
  "strand": "Geometry",
  "explanation": "Specific geometric theorems outlined in the curriculum…",
  "broader_concept": "Theorem",
  "grade_level": "High",
  "difficulty": "Intermediate"

Reason: Too broad and non-descriptive.

Bad Example 2:
  "name": "Contextual problem solving with numbers",
  "strand": "Number",
  "explanation": "Applying arithmetic operations to real-life situations and interpreting results.",
  "broader_concept": "Problem solving",
  "grade_level": "Elementary",
  "difficulty": "Basic"

Reason: Too general; not a discrete concept.

ADDITIONAL REQUESTS
Rank the concepts in descending priority (most central first).
If confident, include a "confidence_score" field (0 = low, 1 = high).
Do not output any prose outside the JSON array.
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