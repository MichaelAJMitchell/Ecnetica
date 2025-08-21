import json
import os
from typing import Dict, List, Any, Optional
import pandas as pd
from quality_assessor import QualityAssessor
from prompt_refiner import PromptRefiner
from config import STAGE1_BROAD_CONCEPT_PROMPT, STAGE2_GRANULAR_CONCEPT_PROMPT, STAGE3_CROSS_REFERENCE_PROMPT, ENHANCED_RELATIONSHIP_EXTRACTION_PROMPT

class AdaptivePromptManager:
    """
    Manages prompt versions and automatically selects the best performing prompts
    based on quality assessment and performance tracking.
    """
    
    def __init__(self, quality_assessor: QualityAssessor, prompt_refiner: PromptRefiner):
        """Initialize the adaptive prompt manager."""
        self.quality_assessor = quality_assessor
        self.prompt_refiner = prompt_refiner
        self.prompt_registry = self._initialize_prompt_registry()
        self.performance_tracker = {}
        
    def _initialize_prompt_registry(self) -> Dict[str, Dict[str, Any]]:
        """Initialize the registry with current prompts."""
        return {
            'stage1_broad_concept': {
                'current': STAGE1_BROAD_CONCEPT_PROMPT,
                'versions': [],
                'performance_history': [],
                'best_score': 0.0,
                'last_refined': None
            },
            'stage2_granular_concept': {
                'current': STAGE2_GRANULAR_CONCEPT_PROMPT,
                'versions': [],
                'performance_history': [],
                'best_score': 0.0,
                'last_refined': None
            },
            'stage3_cross_reference': {
                'current': STAGE3_CROSS_REFERENCE_PROMPT,
                'versions': [],
                'performance_history': [],
                'best_score': 0.0,
                'last_refined': None
            },
            'relationship_extraction': {
                'current': ENHANCED_RELATIONSHIP_EXTRACTION_PROMPT,
                'versions': [],
                'performance_history': [],
                'best_score': 0.0,
                'last_refined': None
            }
        }
    
    def get_current_prompt(self, prompt_type: str) -> str:
        """Get the current best prompt for a given type."""
        if prompt_type in self.prompt_registry:
            return self.prompt_registry[prompt_type]['current']
        else:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
    
    def record_extraction_performance(self, 
                                    prompt_type: str, 
                                    quality_assessment: Dict[str, Any],
                                    extraction_metadata: Dict[str, Any]):
        """
        Record the performance of an extraction using a specific prompt.
        
        Args:
            prompt_type: Type of prompt used
            quality_assessment: Quality assessment results
            extraction_metadata: Metadata about the extraction
        """
        
        if prompt_type not in self.prompt_registry:
            return
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(quality_assessment)
        
        # Record performance
        performance_record = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'prompt_version': self.prompt_registry[prompt_type]['current'][:100] + "...",  # Truncate for storage
            'overall_score': overall_score,
            'quality_assessment': quality_assessment,
            'extraction_metadata': extraction_metadata
        }
        
        self.prompt_registry[prompt_type]['performance_history'].append(performance_record)
        
        # Update best score if this is better
        if overall_score > self.prompt_registry[prompt_type]['best_score']:
            self.prompt_registry[prompt_type]['best_score'] = overall_score
        
        # Check if refinement is needed
        self._check_refinement_needed(prompt_type, overall_score)
    
    def _calculate_overall_score(self, quality_assessment: Dict[str, Any]) -> float:
        """Calculate overall quality score from assessment."""
        scores = []
        
        metrics = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                  'relationship_completeness', 'overall_quality']
        
        for metric in metrics:
            if metric in quality_assessment:
                metric_data = quality_assessment[metric]
                if isinstance(metric_data, dict) and 'score' in metric_data:
                    scores.append(metric_data['score'])
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _check_refinement_needed(self, prompt_type: str, current_score: float):
        """Check if prompt refinement is needed based on performance."""
        registry = self.prompt_registry[prompt_type]
        
        # Get recent performance (last 5 extractions)
        recent_performance = registry['performance_history'][-5:] if len(registry['performance_history']) >= 5 else registry['performance_history']
        
        if not recent_performance:
            return
        
        # Calculate average recent score
        recent_scores = [p['overall_score'] for p in recent_performance]
        avg_recent_score = sum(recent_scores) / len(recent_scores)
        
        # Refine if:
        # 1. Recent performance is consistently low (< 6.0)
        # 2. Performance has declined significantly
        # 3. We haven't refined recently
        
        should_refine = False
        refinement_reason = ""
        
        if avg_recent_score < 6.0:
            should_refine = True
            refinement_reason = f"Low recent performance: {avg_recent_score:.2f}"
        elif len(recent_performance) >= 3 and current_score < (avg_recent_score - 1.0):
            should_refine = True
            refinement_reason = f"Performance decline: {current_score:.2f} vs avg {avg_recent_score:.2f}"
        
        if should_refine:
            self._trigger_prompt_refinement(prompt_type, refinement_reason)
    
    def _trigger_prompt_refinement(self, prompt_type: str, reason: str):
        """Trigger automatic prompt refinement."""
        print(f"Triggering refinement for {prompt_type}: {reason}")
        
        # Get recent quality assessments for this prompt type
        recent_assessments = []
        for record in self.prompt_registry[prompt_type]['performance_history'][-3:]:
            if 'quality_assessment' in record:
                recent_assessments.append(record['quality_assessment'])
        
        if not recent_assessments:
            return
        
        # Use the most recent assessment for refinement
        latest_assessment = recent_assessments[-1]
        
        # Get extraction metadata
        latest_metadata = self.prompt_registry[prompt_type]['performance_history'][-1].get('extraction_metadata', {})
        
        # Refine the prompt
        current_prompt = self.prompt_registry[prompt_type]['current']
        refined_prompt = self.prompt_refiner.refine_prompt(
            current_prompt, 
            latest_assessment, 
            latest_metadata, 
            prompt_type
        )
        
        # Update the prompt registry
        if refined_prompt != current_prompt:
            self._update_prompt_version(prompt_type, current_prompt, refined_prompt)
    
    def _update_prompt_version(self, prompt_type: str, old_prompt: str, new_prompt: str):
        """Update to a new prompt version."""
        registry = self.prompt_registry[prompt_type]
        
        # Store the old version
        version_record = {
            'timestamp': pd.Timestamp.now().isoformat(),
            'prompt': old_prompt,
            'performance_score': registry['best_score'],
            'reason': 'Automated refinement'
        }
        
        registry['versions'].append(version_record)
        registry['current'] = new_prompt
        registry['last_refined'] = pd.Timestamp.now().isoformat()
        
        print(f"Updated {prompt_type} prompt to new version")
    
    def get_performance_summary(self, prompt_type: str = None) -> Dict[str, Any]:
        """Get performance summary for prompts."""
        if prompt_type:
            return self._get_prompt_performance_summary(prompt_type)
        
        # Overall summary
        summary = {
            'total_prompts': len(self.prompt_registry),
            'prompt_performance': {}
        }
        
        for prompt_type in self.prompt_registry:
            summary['prompt_performance'][prompt_type] = self._get_prompt_performance_summary(prompt_type)
        
        return summary
    
    def _get_prompt_performance_summary(self, prompt_type: str) -> Dict[str, Any]:
        """Get performance summary for a specific prompt type."""
        registry = self.prompt_registry[prompt_type]
        
        if not registry['performance_history']:
            return {"message": "No performance data available"}
        
        # Calculate performance metrics
        scores = [p['overall_score'] for p in registry['performance_history']]
        
        summary = {
            'total_extractions': len(registry['performance_history']),
            'current_score': scores[-1] if scores else 0,
            'best_score': registry['best_score'],
            'average_score': sum(scores) / len(scores) if scores else 0,
            'score_trend': self._calculate_score_trend(scores),
            'last_refined': registry['last_refined'],
            'total_versions': len(registry['versions'])
        }
        
        return summary
    
    def _calculate_score_trend(self, scores: List[float]) -> str:
        """Calculate the trend of scores over time."""
        if len(scores) < 3:
            return "insufficient_data"
        
        # Calculate trend using simple linear regression
        recent_scores = scores[-5:]  # Last 5 scores
        
        if len(recent_scores) < 2:
            return "stable"
        
        # Simple trend calculation
        first_half = recent_scores[:len(recent_scores)//2]
        second_half = recent_scores[len(recent_scores)//2:]
        
        if not first_half or not second_half:
            return "stable"
        
        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)
        
        diff = second_avg - first_avg
        
        if diff > 0.5:
            return "improving"
        elif diff < -0.5:
            return "declining"
        else:
            return "stable"
    
    def save_prompt_registry(self, filepath: str):
        """Save the prompt registry to a JSON file."""
        # Convert timestamps to strings for JSON serialization
        registry_copy = {}
        for prompt_type, data in self.prompt_registry.items():
            registry_copy[prompt_type] = data.copy()
            if 'last_refined' in registry_copy[prompt_type] and registry_copy[prompt_type]['last_refined'] is not None:
                registry_copy[prompt_type]['last_refined'] = registry_copy[prompt_type]['last_refined'].isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(registry_copy, f, indent=2)
    
    def load_prompt_registry(self, filepath: str):
        """Load the prompt registry from a JSON file."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                loaded_registry = json.load(f)
            
            # Convert string timestamps back to pandas Timestamps
            for prompt_type, data in loaded_registry.items():
                if prompt_type in self.prompt_registry:
                    self.prompt_registry[prompt_type].update(data)
                    
                    # Convert timestamp back
                    if 'last_refined' in self.prompt_registry[prompt_type] and self.prompt_registry[prompt_type]['last_refined']:
                        self.prompt_registry[prompt_type]['last_refined'] = pd.Timestamp(self.prompt_registry[prompt_type]['last_refined']) 