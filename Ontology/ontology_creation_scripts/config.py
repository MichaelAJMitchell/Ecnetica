import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DEFAULT_MODEL = "gpt-5-mini"
FALLBACK_MODELS = ["gpt-4o-mini", "gpt-4.1-mini", "gpt-3.5-turbo", "gpt-4-turbo-preview"]

# Retry Configuration
MAX_RETRIES = 5
BASE_DELAY = 1.0
MAX_DELAY = 60.0
BACKOFF_FACTOR = 2.0

# File Processing Configuration
CHUNK_SIZE = 1000000  # Characters per chunk for processing (increased to 1M for better efficiency)
OVERLAP_SIZE = 200000  # Overlap between chunks (increased proportionally)

# Output Configuration
OUTPUT_DIR = "../"  # Changed to Ontology directory (parent of ontology_creation_scripts)
CONCEPTS_FILE = os.path.join(OUTPUT_DIR, "concepts.csv")
RELATIONSHIPS_FILE = os.path.join(OUTPUT_DIR, "relationships.csv")

# Archive Configuration
ARCHIVE_DIR = os.path.join(OUTPUT_DIR, "ontology_archive")

# Supported file formats
SUPPORTED_FORMATS = ['.csv', '.pdf', '.txt', '.tex', '.docx', '.md']

# Prompts for Multi-Stage Extraction
STAGE1_BROAD_CONCEPT_PROMPT = """You are a mathematical education expert tasked with identifying broad mathematical topics and themes from educational documents.

Your task is to identify the main mathematical areas present in the text. Focus on broad categories like:
- Number Systems (Natural numbers, Integers, Rational numbers, Real numbers, Complex numbers)
- Operations (Addition, Subtraction, Multiplication, Division, Powers, Roots)
- Algebraic Concepts (Variables, Equations, Functions, Expressions)
- Geometric Concepts (Shapes, Measurements, Transformations, Coordinate Geometry)
- Data Analysis (Statistics, Probability, Graphing, Data Interpretation)
- Calculus Concepts (Limits, Derivatives, Integrals, Applications)

{context_part}

TEXT TO ANALYZE:
{text_chunk}

Identify ONLY the broadest, most fundamental mathematical areas present. Do not extract specific concepts yet.

Respond with a JSON array of broad topics:
[
    {{
        "broad_topic": "topic name",
        "description": "brief description of this mathematical area",
        "subtopics": ["list of main subtopics within this area"]
    }}
]

Be comprehensive but focus on the highest level mathematical domains."""

STAGE2_GRANULAR_CONCEPT_PROMPT = """You are a mathematical education expert tasked with extracting granular mathematical concepts within specific topic areas.

Given the broad topic "{broad_topic}" and its description "{topic_description}", extract all specific, granular concepts mentioned in the text.

For each concept, provide:
1. A specific name (be very granular, e.g., "single digit addition" not just "addition")
2. A clear explanation of what this concept is
3. The broader concept it falls under
4. The mathematical strand or topic

{context_part}

TEXT TO ANALYZE:
{text_chunk}

Extract concepts that are:
- Specific and teachable (not too broad)
- Clearly mathematical in nature
- Mentioned explicitly or strongly implied in the text
- Properly categorized under the given broad topic

Respond with a JSON array:
[
    {{
        "name": "specific concept name",
        "explanation": "brief explanation of what this concept is",
        "broader_concept": "{broad_topic}",
        "strand": "mathematical strand/topic",
        "grade_level": "",
        "difficulty": ""
    }}
]

Be extremely specific and granular. Each concept should be a distinct, teachable unit."""

STAGE3_CROSS_REFERENCE_PROMPT = """You are a mathematical education expert tasked with validating and cross-referencing extracted concepts.

Review the concepts extracted so far and identify:
1. Any concepts mentioned in the text but not yet extracted
2. Any concepts that should be merged (too similar)
3. Any concepts that should be split (too broad)
4. Any concepts that are not truly mathematical
5. Missing prerequisite relationships between concepts

EXISTING CONCEPTS:
{existing_concepts}

{context_part}

TEXT TO ANALYZE:
{text_chunk}

Focus on:
- Concepts mentioned in examples or exercises
- Implicit concepts (e.g., 'solving equations' implies 'equation manipulation')
- Cross-references between different sections
- Concepts that span multiple broad topics

Respond with a JSON array of any additional concepts found:
[
    {{
        "name": "concept name",
        "explanation": "brief explanation",
        "broader_concept": "broader concept",
        "strand": "mathematical strand/topic",
        "grade_level": "",
        "difficulty": ""
    }}
]

Only include concepts that were genuinely missed in previous stages."""

# Enhanced relationship extraction prompt
ENHANCED_RELATIONSHIP_EXTRACTION_PROMPT = """You are a mathematical education expert tasked with identifying prerequisite relationships between mathematical concepts.

Analyze the following text and identify which concepts are prerequisites for other concepts. A prerequisite is a concept that must be understood before learning another concept.

AVAILABLE CONCEPTS:
{concept_info}

{context_part}

TEXT TO ANALYZE:
{text_chunk}

For each prerequisite relationship you identify, provide:
1. The prerequisite concept (the concept that must be learned first)
2. The dependent concept (the concept that depends on the prerequisite)
3. A brief explanation of why this prerequisite relationship exists
4. The strength of the relationship (strong/moderate/weak)

Consider:
- Mathematical complexity (simpler concepts are prerequisites for more complex ones)
- Logical dependencies (concepts that build upon others)
- Educational progression (typical learning order)
- Explicit mentions in the text

It is ESSENTIAL to provide the response as a JSON array of objects with the following structure:
[
    {{
        "prerequisite": "name of prerequisite concept",
        "dependent": "name of dependent concept",
        "explanation": "brief explanation of the relationship",
        "strength": "strong/moderate/weak",
        "source": "{source}"
    }}
]

Only include relationships that are clearly supported by the text. Be conservative - only include relationships that are explicitly mentioned or strongly implied."""

# Original prompts (kept for backward compatibility)
CONCEPT_EXTRACTION_PROMPT = """You are a mathematical education expert tasked with extracting very granular micro-concepts from mathematics curriculum documents and textbooks.
        
Analyze the following text and extract all mathematical concepts mentioned, with a VERY HIGH level of granularity. 
For example, instead of just "addition", identify specific types like "single digit addition", "multi-digit addition", "addition with carrying", etc.

For each concept, provide:
1. A brief name of the micro-concept (be very specific)
2. A brief explanation of what this concept is (1-2 sentences)
3. A broader concept it falls under
4. The mathematical strand or topic (e.g., Algebra, Number, Geometry)
 
{context_part}

IMPORTANT: When extracting concepts, be consistent with existing concepts when possible. If you find a concept that is similar to an existing one, use similar naming conventions and categorization.

TEXT TO ANALYZE:
{text_chunk}

It is ESSENTIAL to provide the response as a JSON array of objects with the following structure:
[
    {{
        "name": "concept name",
        "explanation": "brief explanation of what this concept is",
        "broader_concept": "broader concept",
        "strand": "mathematical strand/topic",
        "grade_level": "",
        "difficulty": ""
    }}
]

Only include concepts that are clearly mathematics-related. Be as specific and granular as possible.
Always leave grade_level and difficulty as empty strings.
Provide clear, concise explanations that would help someone understand what the concept is.

You MUST respond with the JSON array and nothing else."""

RELATIONSHIP_EXTRACTION_PROMPT = """You are a mathematical education expert tasked with identifying prerequisite relationships between mathematical concepts.
        
Analyze the following text and identify which concepts are prerequisites for other concepts. A prerequisite is a concept that must be understood before learning another concept.

AVAILABLE CONCEPTS:
{concept_info}

{context_part}

IMPORTANT: When identifying relationships, be consistent with existing relationships when possible. If you find a relationship that is similar to an existing one, use similar explanation patterns and reasoning.

TEXT TO ANALYZE:
{text_chunk}

For each prerequisite relationship you identify, provide:
1. The prerequisite concept (the concept that must be learned first)
2. The dependent concept (the concept that depends on the prerequisite)
3. A brief explanation of why this prerequisite relationship exists

It is ESSENTIAL to provide the response as a JSON array of objects with the following structure:
[
    {{
        "prerequisite": "name of prerequisite concept",
        "dependent": "name of dependent concept",
        "explanation": "brief explanation of the relationship",
        "source": "{source}"
    }}
]

Only include relationships that are clearly supported by the text. Be conservative - only include relationships that are explicitly mentioned or strongly implied.""" 