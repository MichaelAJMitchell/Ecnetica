import json
import os
from typing import Dict, List, Any, Tuple
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd
from config import DEFAULT_MODEL, FALLBACK_MODELS

class QualityAssessor:
    """
    AI-powered quality assessment system for knowledge graph extractions.
    Evaluates concepts and relationships for quality, completeness, and accuracy.
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the quality assessor with OpenAI client."""
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key)
        self.quality_metrics = []
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def assess_extraction_quality(self, 
                                concepts: List[Dict], 
                                relationships: List[Dict], 
                                source_chunk: str,
                                source_file: str) -> Dict[str, Any]:
        """
        Assess the quality of extracted concepts and relationships.
        
        Args:
            concepts: List of extracted concepts
            relationships: List of extracted relationships  
            source_chunk: The source text chunk that was processed
            source_file: Name of the source file
            
        Returns:
            Dictionary containing quality scores and feedback
        """
        
        prompt = self._build_quality_assessment_prompt(concepts, relationships, source_chunk)
        
        try:
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a knowledge graph quality expert specializing in mathematical education."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            # Parse the response
            assessment_text = response.choices[0].message.content
            assessment = self._parse_quality_assessment(assessment_text)
            
            # Add metadata
            assessment['source_file'] = source_file
            assessment['timestamp'] = pd.Timestamp.now().isoformat()
            assessment['concepts_count'] = len(concepts)
            assessment['relationships_count'] = len(relationships)
            
            # Store for analysis
            self.quality_metrics.append(assessment)
            
            return assessment
            
        except Exception as e:
            # Fallback to basic assessment if AI fails
            return self._fallback_assessment(concepts, relationships, source_file)
    
    def _build_quality_assessment_prompt(self, concepts: List[Dict], relationships: List[Dict], source_chunk: str) -> str:
        """Build the quality assessment prompt."""
        
        concepts_text = json.dumps(concepts, indent=2) if concepts else "[]"
        relationships_text = json.dumps(relationships, indent=2) if relationships else "[]"
        
        prompt = f"""
You are a knowledge graph quality expert. Evaluate the following extracted concepts and relationships:

EXTRACTED CONCEPTS:
{concepts_text}

EXTRACTED RELATIONSHIPS:
{relationships_text}

SOURCE TEXT CHUNK:
{source_chunk[:1000]}...

Rate each aspect on a scale of 1-10 and provide specific feedback:

1. CONCEPT GRANULARITY (1-10): Are concepts specific enough and at the right level of detail?
2. CONCEPT COMPLETENESS (1-10): Are important concepts missing from the source text?
3. RELATIONSHIP ACCURACY (1-10): Are prerequisite relationships logical and mathematically sound?
4. RELATIONSHIP COMPLETENESS (1-10): Are key relationships between concepts missing?
5. OVERALL QUALITY (1-10): How well does this extraction represent the mathematical content?

Provide your response in this exact JSON format:
{{
    "concept_granularity": {{"score": X, "feedback": "..."}},
    "concept_completeness": {{"score": X, "feedback": "..."}},
    "relationship_accuracy": {{"score": X, "feedback": "..."}},
    "relationship_completeness": {{"score": X, "feedback": "..."}},
    "overall_quality": {{"score": X, "feedback": "..."}},
    "improvement_suggestions": ["suggestion1", "suggestion2", ...]
}}
"""
        return prompt
    
    def _parse_quality_assessment(self, assessment_text: str) -> Dict[str, Any]:
        """Parse the AI response into structured assessment data."""
        try:
            # Try to extract JSON from the response
            start_idx = assessment_text.find('{')
            end_idx = assessment_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = assessment_text[start_idx:end_idx]
                assessment = json.loads(json_str)
                return assessment
            else:
                raise ValueError("No JSON found in response")
                
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback parsing for malformed responses
            return self._parse_fallback_assessment(assessment_text)
    
    def _parse_fallback_assessment(self, assessment_text: str) -> Dict[str, Any]:
        """Fallback parsing for malformed AI responses."""
        # Extract scores using regex patterns
        import re
        
        scores = {}
        feedback = {}
        
        # Look for score patterns like "score: X" or "X/10"
        score_patterns = [
            r'concept_granularity.*?(\d+)/10',
            r'concept_completeness.*?(\d+)/10', 
            r'relationship_accuracy.*?(\d+)/10',
            r'relationship_completeness.*?(\d+)/10',
            r'overall_quality.*?(\d+)/10'
        ]
        
        metric_names = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                       'relationship_completeness', 'overall_quality']
        
        for i, pattern in enumerate(score_patterns):
            match = re.search(pattern, assessment_text, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                scores[metric_names[i]] = {"score": score, "feedback": "AI response parsing required manual intervention"}
            else:
                scores[metric_names[i]] = {"score": 5, "feedback": "Unable to parse score from AI response"}
        
        return {
            **scores,
            "improvement_suggestions": ["AI response parsing failed - manual review needed"],
            "parsing_error": True
        }
    
    def _fallback_assessment(self, concepts: List[Dict], relationships: List[Dict], source_file: str) -> Dict[str, Any]:
        """Basic fallback assessment when AI fails."""
        return {
            "concept_granularity": {"score": 5, "feedback": "AI assessment failed - using fallback"},
            "concept_completeness": {"score": 5, "feedback": "AI assessment failed - using fallback"},
            "relationship_accuracy": {"score": 5, "feedback": "AI assessment failed - using fallback"},
            "relationship_completeness": {"score": 5, "feedback": "AI assessment failed - using fallback"},
            "overall_quality": {"score": 5, "feedback": "AI assessment failed - using fallback"},
            "improvement_suggestions": ["AI assessment system needs investigation"],
            "source_file": source_file,
            "timestamp": pd.Timestamp.now().isoformat(),
            "concepts_count": len(concepts),
            "relationships_count": len(relationships),
            "ai_failure": True
        }
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """Get summary statistics of all quality assessments."""
        if not self.quality_metrics:
            return {"message": "No quality assessments available"}
        
        df = pd.DataFrame(self.quality_metrics)
        
        summary = {
            "total_assessments": len(self.quality_metrics),
            "average_scores": {},
            "quality_trends": {},
            "common_issues": []
        }
        
        # Calculate average scores for each metric
        for metric in ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                      'relationship_completeness', 'overall_quality']:
            if metric in df.columns:
                scores = []
                for item in df[metric]:
                    if isinstance(item, dict) and 'score' in item:
                        scores.append(item['score'])
                
                if scores:
                    summary["average_scores"][metric] = {
                        "mean": sum(scores) / len(scores),
                        "min": min(scores),
                        "max": max(scores)
                    }
        
        return summary
    
    def save_quality_metrics(self, filepath: str):
        """Save quality metrics to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.quality_metrics, f, indent=2)
    
    def load_quality_metrics(self, filepath: str):
        """Load quality metrics from a JSON file."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.quality_metrics = json.load(f) 