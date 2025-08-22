"""
LLM Client - Handles interactions with multiple LLM providers with fallback

This module manages all communication with Large Language Models, providing
a unified interface for concept and relationship extraction. It implements
intelligent fallback mechanisms and retry logic to ensure reliable operation.
"""

import openai
import json
import re
import time
import random
from typing import List, Dict, Any, Optional
from config import OPENAI_API_KEY, DEFAULT_MODEL, FALLBACK_MODELS

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
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.models = [DEFAULT_MODEL] + FALLBACK_MODELS
        self.current_model_index = 0
    
    def extract_concepts(self, text: str, context: dict, prompt: str) -> list:
        """
        Extract mathematical concepts from text using the current LLM model.
        
        This method sends text chunks to the LLM with carefully crafted prompts
        to identify mathematical concepts. It uses the context information to
        help the LLM understand the broader document structure.
        
        Args:
            text: The text chunk to analyze for mathematical concepts
            context: Metadata about the chunk's position and surrounding content
            prompt: The prompt template to use for extraction
            
        Returns:
            list: List of extracted concepts, each containing:
                - name: The concept name
                - explanation: Brief description of the concept
                - broader_concept: Higher-level category
                - strand: Mathematical strand (Algebra, Geometry, etc.)
                - grade_level: Educational level (if determinable)
                - difficulty: Complexity assessment (if determinable)
        """
        return self._retry_with_fallback(
            self._extract_concepts_single_model, text, context, prompt
        )
    
    def extract_relationships(self, text: str, concepts: list, context: dict, prompt: str) -> list:
        """
        Extract relationships between mathematical concepts using the current LLM model.
        
        This method analyzes how concepts relate to each other, identifying
        prerequisites, dependencies, and conceptual connections. It uses the
        list of concepts to guide the relationship extraction process.
        
        Args:
            text: The text chunk containing the concepts
            concepts: List of concepts found in this chunk
            context: Metadata about the chunk and document structure
            prompt: The prompt template to use for extraction
            
        Returns:
            list: List of relationships, each containing:
                - prerequisite_name: ID of the prerequisite concept
                - dependent_name: ID of the concept that depends on the prerequisite
                - relationship_type: Nature of the relationship (prerequisite, builds_on, etc.)
                - strength: Confidence level of the relationship (0.0 to 1.0)
        """
        return self._retry_with_fallback(
            self._extract_relationships_single_model, text, concepts, context, prompt
        )
    
    def verify_extraction(self, context: dict, prompt: str) -> dict:
        """
        Verify the quality of extracted concepts and relationships.
        
        Args:
            context: Original text content and extracted data
            prompt: The verification prompt template
            
        Returns:
            dict: Verification results with validity flags
        """
        return self._retry_with_fallback(
            self._verify_extraction_single_model, context, prompt
        )
    
    def _retry_with_fallback(self, func, *args, **kwargs):
        """
        Retry a function with exponential backoff and automatic model fallback.
        
        This is the core reliability mechanism that:
        1. Attempts the operation with the current model
        2. If it fails, waits with exponential backoff before retrying
        3. If retries are exhausted, falls back to the next model
        4. Continues until all models are exhausted or operation succeeds
        
        Args:
            func: The function to retry (extract_concepts, extract_relationships, or verify_extraction)
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            The result of the successful function call
            
        Raises:
            Exception: If all models fail after exhausting retries
        """
        max_retries = 3
        base_delay = 1.0
        max_delay = 30.0
        
        for model_index in range(len(self.models)):
            self.current_model_index = model_index
            current_model = self.models[model_index]
            
            for attempt in range(max_retries):
                try:
                    print(f"Attempting with model: {current_model} (attempt {attempt + 1})")
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                    raise Exception("Function returned None")
                    
                except Exception as e:
                    print(f"Error with {current_model} (attempt {attempt + 1}): {str(e)}")
                    
                    if attempt < max_retries - 1:
                        # Calculate delay with exponential backoff
                        delay = min(base_delay * (2 ** attempt), max_delay)
                        delay += random.uniform(0, 0.1 * delay)  # Add jitter
                        print(f"Waiting {delay:.1f} seconds before retry...")
                        time.sleep(delay)
                    else:
                        print(f"Model {current_model} failed after {max_retries} attempts")
                        if model_index < len(self.models) - 1:
                            print(f"Falling back to next model...")
                            break
                        else:
                            raise Exception(f"All models failed: {str(e)}")
        
        raise Exception("All models and retries exhausted")
    
    def _extract_concepts_single_model(self, text: str, context: dict, prompt: str) -> list:
        """Extract concepts using a single model with JSON fallback."""
        try:
            response = self.client.chat.completions.create(
                model=self.models[self.current_model_index],
                messages=[
                    {"role": "system", "content": "You are a mathematical education expert."},
                    {"role": "user", "content": prompt.format(text=text, context=context)}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            result = self._extract_json_from_response(content)
            
            if result:
                return result
            
            # Fallback: reformat the response
            print("JSON parsing failed, attempting reformat...")
            result = self._reformat_json_response(
                content, 
                "JSON array of mathematical concepts with fields: name, explanation, broader_concept, strand, grade_level, difficulty"
            )
            
            return result if result else []
            
        except Exception as e:
            print(f"Concept extraction failed: {str(e)}")
            raise
    
    def _extract_relationships_single_model(self, text: str, concepts: list, context: dict, prompt: str) -> list:
        """Extract relationships using a single model with JSON fallback."""
        try:
            response = self.client.chat.completions.create(
                model=self.models[self.current_model_index],
                messages=[
                    {"role": "system", "content": "You are a mathematical education expert."},
                    {"role": "user", "content": prompt.format(text=text, concepts=concepts, context=context)}
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            result = self._extract_json_from_response(content)
            
            if result:
                return result
            
            # Fallback: reformat the response
            print("JSON parsing failed, attempting reformat...")
            result = self._reformat_json_response(
                content, 
                "JSON array of relationships with fields: prerequisite_name, dependent_name, relationship_type, strength"
            )
            
            return result if result else []
            
        except Exception as e:
            print(f"Relationship extraction failed: {str(e)}")
            raise
    
    def _verify_extraction_single_model(self, context: dict, prompt: str) -> dict:
        """Verify extraction using a single model with JSON fallback."""
        try:
            response = self.client.chat.completions.create(
                model=self.models[self.current_model_index],
                messages=[
                    {"role": "system", "content": "You are a mathematical education expert."},
                    {"role": "user", "content": prompt.format(context=context)}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            result = self._extract_json_from_response(content)
            
            if result:
                return result
            
            # Fallback: reformat the response
            print("JSON parsing failed, attempting reformat...")
            result = self._reformat_json_response(
                content, 
                "JSON object with fields: concepts_valid (boolean), relationships_valid (boolean), quality_score (number), feedback (string)"
            )
            
            return result if result else {"concepts_valid": False, "relationships_valid": False, "quality_score": 0, "feedback": "Verification failed"}
            
        except Exception as e:
            print(f"Verification failed: {str(e)}")
            raise
    
    def _extract_json_from_response(self, content: str) -> Optional[dict]:
        """Extract JSON from response, handling common formatting issues."""
        # Try direct parsing first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass
        
        # Look for JSON array/object in the response
        json_patterns = [
            r'\[.*\]',  # Array pattern
            r'\{.*\}',  # Object pattern
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group())
                except json.JSONDecodeError:
                    continue
        
        return None
    
    def _reformat_json_response(self, malformed_content: str, expected_format: str) -> Optional[dict]:
        """Ask the same model to reformat its response."""
        reformat_prompt = f"""
Your previous response was not valid JSON. Please reformat it as:

{expected_format}

ORIGINAL RESPONSE:
{malformed_content}

Return ONLY the valid JSON, no other text.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.models[self.current_model_index],
                messages=[
                    {"role": "system", "content": "You are a JSON formatting expert."},
                    {"role": "user", "content": reformat_prompt}
                ],
                temperature=0.1,  # Low temperature for consistent formatting
                max_tokens=2000
            )
            
            content = response.choices[0].message.content.strip()
            return self._extract_json_from_response(content)
            
        except Exception as e:
            print(f"JSON reformatting failed: {str(e)}")
            return None 