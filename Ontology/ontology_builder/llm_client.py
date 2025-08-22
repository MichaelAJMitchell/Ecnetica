"""
LLM Client - Handles interactions with multiple LLM providers with fallback

This module manages all communication with Large Language Models, providing
a unified interface for concept and relationship extraction. It implements
intelligent fallback mechanisms and retry logic to ensure reliable operation.
"""

class LLMClient:
    """
    Manages interactions with multiple LLM providers with automatic fallback.
    
    This class provides a robust interface to LLM APIs, automatically switching
    between different models if one fails. It implements exponential backoff
    retry logic to handle temporary API issues gracefully.
    """
    
    def __init__(self):
        """
        Initialize the LLM client with a prioritized list of models.
        
        Models are tried in order of preference:
        1. gpt-5-mini: Primary model (highest quality)
        2. gpt-4o-mini: First fallback (good quality, lower cost)
        3. gpt-4.1-mini: Second fallback (reliable, lower cost)
        
        The system automatically falls back to the next model if the current
        one fails or hits rate limits.
        """
        self.models = ["gpt-5-mini", "gpt-4o-mini", "gpt-4.1-mini"]
        self.current_model_index = 0
    
    def extract_concepts(self, text: str, context: dict) -> list:
        """
        Extract mathematical concepts from text using the current LLM model.
        
        This method sends text chunks to the LLM with carefully crafted prompts
        to identify mathematical concepts. It uses the context information to
        help the LLM understand the broader document structure.
        
        Args:
            text: The text chunk to analyze for mathematical concepts
            context: Metadata about the chunk's position and surrounding content
            
        Returns:
            list: List of extracted concepts, each containing:
                - name: The concept name
                - explanation: Brief description of the concept
                - broader_concept: Higher-level category
                - strand: Mathematical strand (Algebra, Geometry, etc.)
                - grade_level: Educational level (if determinable)
                - difficulty: Complexity assessment (if determinable)
        """
        pass
    
    def extract_relationships(self, text: str, concepts: list, context: dict) -> list:
        """
        Extract relationships between mathematical concepts using the current LLM model.
        
        This method analyzes how concepts relate to each other, identifying
        prerequisites, dependencies, and conceptual connections. It uses the
        list of concepts to guide the relationship extraction process.
        
        Args:
            text: The text chunk containing the concepts
            concepts: List of concepts found in this chunk
            context: Metadata about the chunk and document structure
            
        Returns:
            list: List of relationships, each containing:
                - prerequisite_id: ID of the prerequisite concept
                - dependent_id: ID of the concept that depends on the prerequisite
                - relationship_type: Nature of the relationship (prerequisite, builds_on, etc.)
                - strength: Confidence level of the relationship (0.0 to 1.0)
        """
        pass
    
    def _retry_with_fallback(self, func, *args, **kwargs):
        """
        Retry a function with exponential backoff and automatic model fallback.
        
        This is the core reliability mechanism that:
        1. Attempts the operation with the current model
        2. If it fails, waits with exponential backoff before retrying
        3. If retries are exhausted, falls back to the next model
        4. Continues until all models are exhausted or operation succeeds
        
        Args:
            func: The function to retry (extract_concepts or extract_relationships)
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of the successful function call
            
        Raises:
            Exception: If all models fail after exhausting retries
        """
        pass 