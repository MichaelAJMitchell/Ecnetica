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
You are a physics education expert specializing in curriculum design and concept mapping.
Your job is to extract **atomic physics learning concepts** from the input text.  
Follow the rules and output exactly in the required format (no extra text).
First, **think step by step**:
1. Identify candidate physics ideas (operations, theorems, definitions, procedures, skills).
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
- Specific physics concepts (e.g., "potential energy" not just "energy")
- Physics definitions, formulas, experiments, and procedures
- Educational concepts that students need to learn

### OUTPUT FORMAT
Return exactly a JSON **array** of concept objects (no additional commentary), where each concept has this exact structure:  
[
  {{
    "name": "concept_name_here",
    "explanation": "brief_description_of_the_concept",
    "broader_concept": "higher_level_category_or_parent_concept",
    "strand": "physics_strand_e.g._Mechanics",
    "grade_level": "educational_level_e.g._Elementary_Middle_High_College",
    "difficulty": "complexity_level_e.g._Basic_Intermediate_Advanced"
    (Optional) "confidence_score": a number between 0 and 1 indicating your confidence  
  }}
]

Strand should be one of the following:
- Heat & Temperature
- Waves, Light & Sound
- Mechanics
- Electricity
- Modern Physics
- Particle Physics
- Applied Electricity

Broader_concept should encapsulate a number of smaller concepts or  individual learning steps, while still being a quite specific problem or concept.

Examples of broader concepts:
- Linear Motion
- Circular Motion
- Specific Heat Capacity
- Wave Nature of Light
- Current Electricity
- The Electron

Rules:
- If a candidate is vague or covers multiple distinct ideas, **omit it** rather than produce a low-quality entry.  
- Do not output duplicates — only one object per concept name.  
- Ensure each object is valid JSON, no trailing commas, consistent types.

IMPORTANT: Every concept MUST have a "name" field. All other fields are optional but recommended.

ADDITIONAL REQUESTS
Rank the concepts in descending priority (most central first).
If confident, include a "confidence_score" field (0 = low, 1 = high).
Do not output any prose outside the JSON array.
"""

RELATIONSHIP_EXTRACTION_PROMPT = """
### INSTRUCTION
You are a physics education expert specializing in curriculum structure and concept dependency mapping.
Your task is to identify **relationships between physics concepts** within the provided text and concept list.
Follow these steps carefully:
1. Identify all possible pairs of concepts that are connected by learning dependencies or logical relationships.
2. Determine the *type* and *direction* of each relationship.
3. Exclude relationships that are vague, uncertain, or unsupported by the text.
4. Return only high-quality, interpretable links.

---
### INPUT

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

You also have access to a concept ID mapping for existing concepts (use these IDs when possible).
For newly extracted concepts, use the concept name as a placeholder until the system assigns IDs.
---
### RELATIONSHIP TYPES
Use one of the following relationship types:
- "prerequisite": Concept A must be understood before Concept B.
- "builds_on": Concept B extends or elaborates Concept A.
- "related": Concepts A and B are closely connected but not dependent.
- "supports": Concept A provides a foundation or tool used in Concept B.


---
### OUTPUT FORMAT
Return exactly one JSON array of relationship objects, where each relationship has this exact structure:
[
  {{
    "prerequisite_concept_id": "uuid_of_prerequisite_concept",
    "dependent_concept_id": "uuid_of_dependent_concept", 
    "relationship_type": "prerequisite_builds_on_related_supports",
    "strength": 0.8
  }}
]

Rules:
- Use existing concept IDs when available; for new ones, use names as placeholders.
- The system will resolve these placeholders to proper IDs later
- Exclude any uncertain or generic relationships.
- Ensure directionality is correct (A → B).
- Ensure the relationship is not a duplicate.
- Strength should be 0.0 to 1.0
"""

VERIFICATION_PROMPT = """
You are a physics education expert. Verify the quality of extracted concepts and relationships.

CONTEXT:
- Source: {context[source_file]}
- Position: {context[chunk_position]}
- New concepts: {context[new_concepts_count]} to verify
- New relationships: {context[new_relationships_count]} to verify

Check for:
- Concept accuracy: Are the concepts correctly identified?
- Relationship validity: Do the relationships make physics sense?
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