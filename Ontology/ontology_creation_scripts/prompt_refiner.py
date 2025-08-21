import json
import os
from typing import Dict, List, Any, Tuple
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd
from config import DEFAULT_MODEL, FALLBACK_MODELS

class PromptRefiner:
    """
    AI-powered prompt refinement system that improves extraction prompts based on quality feedback.
    """
    
    def __init__(self, api_key: str = None):
        """Initialize the prompt refiner with OpenAI client."""
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key)
        self.prompt_versions = []
        self.performance_history = []
        
    def refine_prompt(self, 
                     current_prompt: str, 
                     quality_feedback: Dict[str, Any],
                     extraction_results: Dict[str, Any],
                     prompt_type: str) -> str:
        """
        Use quality feedback to refine a prompt.
        
        Args:
            current_prompt: The current prompt to refine
            quality_feedback: Quality assessment results
            extraction_results: Results from the extraction
            prompt_type: Type of prompt (e.g., 'concept_extraction', 'relationship_extraction')
            
        Returns:
            Refined prompt string
        """
        
        refinement_prompt = self._build_refinement_prompt(
            current_prompt, quality_feedback, extraction_results, prompt_type
        )
        
        try:
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "You are an expert prompt engineer specializing in AI knowledge extraction."},
                    {"role": "user", "content": refinement_prompt}
                ],
                temperature=0.2,
                max_tokens=1500
            )
            
            refined_prompt = response.choices[0].message.content
            
            # Store the refinement
            self._store_prompt_refinement(
                prompt_type, current_prompt, refined_prompt, quality_feedback
            )
            
            return refined_prompt
            
        except Exception as e:
            print(f"Prompt refinement failed: {e}")
            return current_prompt
    
    def _build_refinement_prompt(self, 
                                current_prompt: str, 
                                quality_feedback: Dict[str, Any],
                                extraction_results: Dict[str, Any],
                                prompt_type: str) -> str:
        """Build the prompt refinement prompt."""
        
        # Extract key quality metrics
        quality_summary = self._extract_quality_summary(quality_feedback)
        
        prompt = f"""
You are an expert prompt engineer. Based on the quality assessment below, suggest improvements to our {prompt_type} prompt.

QUALITY ASSESSMENT:
{quality_summary}

CURRENT PROMPT:
{current_prompt}

EXTRACTION RESULTS SUMMARY:
- Concepts extracted: {extraction_results.get('concepts_count', 'Unknown')}
- Relationships extracted: {extraction_results.get('relationships_count', 'Unknown')}
- Source file: {extraction_results.get('source_file', 'Unknown')}

IMPROVEMENT SUGGESTIONS FROM QUALITY ASSESSMENT:
{json.dumps(quality_feedback.get('improvement_suggestions', []), indent=2)}

Your task is to improve the prompt to address the quality issues identified. Focus on:

1. **Clarity and Specificity**: Make instructions clearer and more specific
2. **Example Formatting**: Improve example structure and clarity
3. **Context Utilization**: Better use of available context
4. **Output Format**: Clearer output format requirements
5. **Constraints**: Add specific constraints to avoid common issues

Provide ONLY the improved prompt - no explanations or additional text. The prompt should be ready to use immediately.
"""
        return prompt
    
    def _extract_quality_summary(self, quality_feedback: Dict[str, Any]) -> str:
        """Extract a readable summary of quality feedback."""
        summary_parts = []
        
        metrics = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                  'relationship_completeness', 'overall_quality']
        
        for metric in metrics:
            if metric in quality_feedback:
                metric_data = quality_feedback[metric]
                if isinstance(metric_data, dict) and 'score' in metric_data:
                    score = metric_data['score']
                    feedback = metric_data.get('feedback', 'No feedback provided')
                    summary_parts.append(f"{metric.replace('_', ' ').title()}: {score}/10 - {feedback}")
        
        return "\n".join(summary_parts)
    
    def _store_prompt_refinement(self, 
                                prompt_type: str, 
                                old_prompt: str, 
                                new_prompt: str, 
                                quality_feedback: Dict[str, Any]):
        """Store information about the prompt refinement."""
        
        refinement_record = {
            "timestamp": pd.Timestamp.now().isoformat(),
            "prompt_type": prompt_type,
            "old_prompt": old_prompt,
            "new_prompt": new_prompt,
            "quality_feedback": quality_feedback,
            "overall_score": self._calculate_overall_score(quality_feedback)
        }
        
        self.prompt_versions.append(refinement_record)
    
    def _calculate_overall_score(self, quality_feedback: Dict[str, Any]) -> float:
        """Calculate overall quality score from feedback."""
        scores = []
        
        metrics = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                  'relationship_completeness', 'overall_quality']
        
        for metric in metrics:
            if metric in quality_feedback:
                metric_data = quality_feedback[metric]
                if isinstance(metric_data, dict) and 'score' in metric_data:
                    scores.append(metric_data['score'])
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_prompt_performance_history(self, prompt_type: str = None) -> List[Dict[str, Any]]:
        """Get performance history for prompts."""
        if prompt_type:
            return [v for v in self.prompt_versions if v['prompt_type'] == prompt_type]
        return self.prompt_versions
    
    def get_best_prompt_version(self, prompt_type: str) -> str:
        """Get the best performing prompt version for a given type."""
        type_versions = [v for v in self.prompt_versions if v['prompt_type'] == prompt_type]
        
        if not type_versions:
            return None
        
        # Sort by overall score (descending)
        type_versions.sort(key=lambda x: x['overall_score'], reverse=True)
        return type_versions[0]['new_prompt']
    
    def analyze_prompt_effectiveness(self, prompt_type: str) -> Dict[str, Any]:
        """Analyze how effective prompt refinements have been."""
        type_versions = [v for v in self.prompt_versions if v['prompt_type'] == prompt_type]
        
        if not type_versions:
            return {"message": f"No refinements found for {prompt_type}"}
        
        # Calculate improvement trends
        initial_scores = []
        final_scores = []
        
        for i, version in enumerate(type_versions):
            if i == 0:
                initial_scores.append(version['overall_score'])
            else:
                initial_scores.append(type_versions[i-1]['overall_score'])
            final_scores.append(version['overall_score'])
        
        improvements = [final - initial for final, initial in zip(final_scores, initial_scores)]
        
        analysis = {
            "total_refinements": len(type_versions),
            "average_improvement": sum(improvements) / len(improvements) if improvements else 0,
            "best_score": max(final_scores) if final_scores else 0,
            "improvement_trend": "positive" if sum(improvements) > 0 else "negative",
            "refinement_history": type_versions
        }
        
        return analysis
    
    def save_prompt_history(self, filepath: str):
        """Save prompt refinement history to a JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.prompt_versions, f, indent=2)
    
    def load_prompt_history(self, filepath: str):
        """Load prompt refinement history from a JSON file."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.prompt_versions = json.load(f) 