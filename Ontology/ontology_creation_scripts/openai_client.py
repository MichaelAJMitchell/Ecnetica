import openai
import json
import time
import random
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import (
    OPENAI_API_KEY, DEFAULT_MODEL, FALLBACK_MODELS,
    MAX_RETRIES, BASE_DELAY, MAX_DELAY, BACKOFF_FACTOR
)

class OpenAIClient:
    """Handles OpenAI API calls with retry logic and model fallbacks."""
    
    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = openai.OpenAI(api_key=OPENAI_API_KEY)
        self.models = [DEFAULT_MODEL] + FALLBACK_MODELS
    
    def _calculate_delay(self, attempt: int) -> float:
        """Calculate delay for exponential backoff with jitter."""
        delay = min(BASE_DELAY * (BACKOFF_FACTOR ** attempt), MAX_DELAY)
        # Add jitter to prevent thundering herd
        jitter = random.uniform(0, 0.1 * delay)
        return delay + jitter
    
    @retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=BASE_DELAY, max=MAX_DELAY),
        retry=retry_if_exception_type((openai.RateLimitError, openai.APITimeoutError, openai.APIConnectionError))
    )
    def _make_api_call(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Make an API call with retry logic."""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                **kwargs
            )
            return response
        except openai.RateLimitError as e:
            print(f"Rate limit hit for model {model}, retrying...")
            time.sleep(self._calculate_delay(0))
            raise
        except openai.APITimeoutError as e:
            print(f"Timeout for model {model}, retrying...")
            time.sleep(self._calculate_delay(0))
            raise
        except openai.APIConnectionError as e:
            print(f"Connection error for model {model}, retrying...")
            time.sleep(self._calculate_delay(0))
            raise
        except Exception as e:
            print(f"Unexpected error with model {model}: {str(e)}")
            raise
    
    def _log_malformed_response(self, model: str, content: str, task_type: str):
        """Log malformed responses to a file for debugging."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/malformed_response_{task_type}_{model}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Model: {model}\n")
                f.write(f"Task: {task_type}\n")
                f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                f.write(f"{'='*50}\n")
                f.write(content)
            print(f"Logged malformed response to: {filename}")
        except Exception as e:
            print(f"Failed to log malformed response: {str(e)}")

    def _reformat_json_response(self, model: str, malformed_content: str, task_type: str) -> Optional[List[Dict[str, Any]]]:
        """Attempt to reformat a malformed JSON response using the same model."""
        reformat_prompt = f"""Your previous response was not in valid JSON format. Please reformat it as a proper JSON array.

ORIGINAL TASK: {task_type}

MALFORMED RESPONSE:
{malformed_content}

Please extract the relevant information from the malformed response above and format it as a valid JSON array. If the malformed response contains mathematical concepts, format them as:

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

If the malformed response contains relationships, format them as:

[
    {{
        "prerequisite": "prerequisite concept name",
        "dependent": "dependent concept name", 
        "explanation": "relationship explanation",
        "source": "source"
    }}
]

Return ONLY the JSON array, no other text."""

        messages = [
            {"role": "system", "content": "You are a JSON formatting expert."},
            {"role": "user", "content": reformat_prompt}
        ]
        
        try:
            print(f"Attempting to reformat JSON response using {model}")
            response = self._make_api_call(
                model=model,
                messages=messages,
                temperature=0.1  # Lower temperature for more consistent formatting
            )
            
            content = response.choices[0].message.content.strip()
            
            # Try to parse the reformatted JSON
            try:
                # Find JSON array in the response
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                
                if start_idx != -1 and end_idx != 0:
                    json_str = content[start_idx:end_idx]
                    result = json.loads(json_str)
                    print(f"Successfully reformatted JSON using {model}")
                    return result
                else:
                    print(f"Reformatted response still contains no JSON array from {model}")
                    return None
                    
            except json.JSONDecodeError as e:
                print(f"Failed to parse reformatted JSON from {model}: {str(e)}")
                return None
                
        except Exception as e:
            print(f"Error reformatting JSON with {model}: {str(e)}")
            return None

    def extract_concepts(self, text_chunk: str, existing_concepts: List[Dict[str, Any]], source: str) -> List[Dict[str, Any]]:
        """Extract mathematical concepts from text using OpenAI API."""
        from config import CONCEPT_EXTRACTION_PROMPT
        
        # Prepare context from existing concepts
        context_part = ""
        if existing_concepts:
            context_examples = existing_concepts[:5]  # Use first 5 as examples
            context_part = f"EXISTING CONCEPTS (for reference):\n"
            for concept in context_examples:
                context_part += f"- {concept['name']}: {concept['explanation']} (Strand: {concept['strand']})\n"
        
        prompt = CONCEPT_EXTRACTION_PROMPT.format(
            context_part=context_part,
            text_chunk=text_chunk
        )
        
        messages = [
            {"role": "system", "content": "You are a mathematical education expert."},
            {"role": "user", "content": prompt}
        ]
        
        for model in self.models:
            try:
                print(f"Attempting concept extraction with model: {model}")
                response = self._make_api_call(
                    model=model,
                    messages=messages,
                    temperature=0.3
                )
                
                content = response.choices[0].message.content.strip()
                
                # Try to parse JSON response
                try:
                    # Find JSON array in the response
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    
                    if start_idx != -1 and end_idx != 0:
                        json_str = content[start_idx:end_idx]
                        concepts = json.loads(json_str)
                        
                        # Add source to each concept
                        for concept in concepts:
                            concept['source'] = source
                        
                        print(f"Successfully extracted {len(concepts)} concepts using {model}")
                        return concepts
                    else:
                        print(f"No JSON array found in response from {model}")
                        # Log the malformed response
                        self._log_malformed_response(model, content, "concept_extraction")
                        # Try to reformat the response
                        reformatted_concepts = self._reformat_json_response(model, content, "concept extraction")
                        if reformatted_concepts:
                            # Add source to each concept
                            for concept in reformatted_concepts:
                                concept['source'] = source
                            print(f"Successfully extracted {len(reformatted_concepts)} concepts using reformatted response from {model}")
                            return reformatted_concepts
                        continue
                        
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON from {model}: {str(e)}")
                    # Log the malformed response
                    self._log_malformed_response(model, content, "concept_extraction")
                    # Try to reformat the response
                    reformatted_concepts = self._reformat_json_response(model, content, "concept extraction")
                    if reformatted_concepts:
                        # Add source to each concept
                        for concept in reformatted_concepts:
                            concept['source'] = source
                        print(f"Successfully extracted {len(reformatted_concepts)} concepts using reformatted response from {model}")
                        return reformatted_concepts
                    continue
                    
            except Exception as e:
                print(f"Error with model {model}: {str(e)}")
                if model == self.models[-1]:  # Last model
                    raise Exception(f"All models failed for concept extraction: {str(e)}")
                continue
        
        return []
    
    def extract_relationships(self, text_chunk: str, concepts: List[Dict[str, Any]], 
                           existing_relationships: List[Dict[str, Any]], source: str) -> List[Dict[str, Any]]:
        """Extract prerequisite relationships from text using OpenAI API."""
        from config import RELATIONSHIP_EXTRACTION_PROMPT
        
        # Filter concepts to only include those that actually exist in the database
        # This prevents the "Could not find concept IDs" warnings
        available_concepts = []
        for concept in concepts:
            if 'id' in concept:  # Only include concepts that have been added to the database
                available_concepts.append(concept)
        
        # Prepare concept info for the prompt
        concept_info = []
        for concept in available_concepts:
            concept_info.append(f"{concept['name']}: {concept['explanation']}")
        
        # Prepare context from existing relationships
        context_part = ""
        if existing_relationships:
            context_examples = existing_relationships[:3]  # Use first 3 as examples
            context_part = f"EXISTING RELATIONSHIPS (for reference):\n"
            for rel in context_examples:
                context_part += f"- {rel['prerequisite_name']} → {rel['dependent_name']}: {rel['explanation']}\n"
        
        prompt = RELATIONSHIP_EXTRACTION_PROMPT.format(
            concept_info=', '.join(concept_info),
            context_part=context_part,
            text_chunk=text_chunk,
            source=source
        )
        
        messages = [
            {"role": "system", "content": "You are a mathematical education expert."},
            {"role": "user", "content": prompt}
        ]
        
        for model in self.models:
            try:
                print(f"Attempting relationship extraction with model: {model}")
                response = self._make_api_call(
                    model=model,
                    messages=messages,
                    temperature=0.3
                )
                
                content = response.choices[0].message.content.strip()
                
                # Try to parse JSON response
                try:
                    # Find JSON array in the response
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    
                    if start_idx != -1 and end_idx != 0:
                        json_str = content[start_idx:end_idx]
                        relationships = json.loads(json_str)
                        
                        # Add source to each relationship if not already present
                        for rel in relationships:
                            if 'source' not in rel:
                                rel['source'] = source
                        
                        print(f"Successfully extracted {len(relationships)} relationships using {model}")
                        return relationships
                    else:
                        print(f"No JSON array found in response from {model}")
                        # Log the malformed response
                        self._log_malformed_response(model, content, "relationship_extraction")
                        # Try to reformat the response
                        reformatted_relationships = self._reformat_json_response(model, content, "relationship extraction")
                        if reformatted_relationships:
                            # Add source to each relationship if not already present
                            for rel in reformatted_relationships:
                                if 'source' not in rel:
                                    rel['source'] = source
                            print(f"Successfully extracted {len(reformatted_relationships)} relationships using reformatted response from {model}")
                            return reformatted_relationships
                        continue
                        
                except json.JSONDecodeError as e:
                    print(f"Failed to parse JSON from {model}: {str(e)}")
                    # Log the malformed response
                    self._log_malformed_response(model, content, "relationship_extraction")
                    # Try to reformat the response
                    reformatted_relationships = self._reformat_json_response(model, content, "relationship extraction")
                    if reformatted_relationships:
                        # Add source to each relationship if not already present
                        for rel in reformatted_relationships:
                            if 'source' not in rel:
                                rel['source'] = source
                        print(f"Successfully extracted {len(reformatted_relationships)} relationships using reformatted response from {model}")
                        return reformatted_relationships
                    continue
                    
            except Exception as e:
                print(f"Error with model {model}: {str(e)}")
                if model == self.models[-1]:  # Last model
                    raise Exception(f"All models failed for relationship extraction: {str(e)}")
                continue
        
        return [] 