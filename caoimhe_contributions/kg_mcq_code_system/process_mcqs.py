import uuid
import json
from typing import Dict, List, Union
from mcq_algorithm_with_json import DifficultyBreakdown,KnowledgeGraph

def process_mcq_document(mcq_document: Union[List[Dict], Dict], knowledge_graph) -> List[Dict]:
    """
    Process a document of MCQs and return JSON-ready MCQs with:
    - Generated UUIDs
    - Calculated prerequisites using existing kgcode_reduced functions
    - Calculated difficulty using existing kgcode_reduced functions
    
    Args:
        mcq_document: List of MCQ dictionaries OR single MCQ dictionary
        knowledge_graph: KnowledgeGraph instance from kgcode_reduced
        
    Returns:
        List of complete JSON-ready MCQ dictionaries
    """
    with open('mcqs.json', 'r') as f:
        data = json.load(f)
        mcq_document = data['mcqs']

    # Handle single MCQ input
    if isinstance(mcq_document, dict):
        mcq_document = [mcq_document]
    
    processed_mcqs = []
    
    for mcq_input in mcq_document:
        try:
            processed_mcq = _process_single_mcq(mcq_input, knowledge_graph)
            processed_mcqs.append(processed_mcq)
        except Exception as e:
            print(f"Error processing MCQ: {e}")
            continue
    
    return processed_mcqs

def _calculate_prerequisites(subtopic_weights: Dict[int, float], knowledge_graph) -> Dict[str, float]:
    """
    Get all prerequisite topics needed to attempt this question.
    Uses graph traversal to find dependencies of tested topics.
    """
    adjacency_matrix = knowledge_graph.get_adjacency_matrix()
    prerequisites = {}
    
    if adjacency_matrix.size > 0:
        for topic_index, topic_weight in subtopic_weights.items():
            if topic_index < adjacency_matrix.shape[0]:
                topic_prereqs = adjacency_matrix[topic_index, :]
                
                for prereq_index, prereq_strength in enumerate(topic_prereqs):
                    if prereq_strength > 0:
                        weighted_prereq = prereq_strength * topic_weight
                        prereq_key = str(prereq_index)
                        
                        if prereq_key in prerequisites:
                            prerequisites[prereq_key] = max(prerequisites[prereq_key], weighted_prereq)
                        else:
                            prerequisites[prereq_key] = weighted_prereq
    
    return prerequisites



def _extract_difficulty_from_input(mcq_input: Dict):
    """Extract difficulty components from MCQ input and create DifficultyBreakdown."""

    difficulty_data = mcq_input['difficulty_breakdown']
    
    # Extract values from the difficulty_breakdown object
    conceptual = float(difficulty_data.get('conceptual_understanding', 0.0))
    procedural = float(difficulty_data.get('procedural_fluency', 0.0))
    problem_solving = float(difficulty_data.get('problem_solving', 0.0))
    communication = float(difficulty_data.get('mathematical_communication', 0.0))
    memory = float(difficulty_data.get('memory', 0.0))
    spatial = float(difficulty_data.get('spatial_reasoning', 0.0))
    # Create DifficultyBreakdown directly
    difficulty_breakdown = DifficultyBreakdown(
        conceptual_understanding=conceptual,
        procedural_fluency=procedural,
        problem_solving=problem_solving,
        mathematical_communication=communication,
        memory=memory,
        spatial_reasoning=spatial
    )
    
    return difficulty_breakdown

def _process_single_mcq(mcq_input: Dict, knowledge_graph) -> Dict:
    """
    Process a single MCQ using existing kgcode_reduced functions.
    
    Args:
        mcq_input: MCQ dictionary in your format
        knowledge_graph: KnowledgeGraph instance
        
    Returns:
        Complete JSON-ready MCQ dictionary
    """
    
    # Generate UUID
    mcq_id = str(uuid.uuid4())
    difficulty_breakdown = _extract_difficulty_from_input(mcq_input)
    # Get chapter from main topic using existing function
    main_topic_node = knowledge_graph.get_node_by_index(mcq_input['main_topic_index'])
    chapter = main_topic_node.chapter
    
    # Create temporary MCQ object to use existing prerequisite calculation
    # Convert subtopic_weights to have integer keys for existing functions
    subtopic_weights = {int(k) if isinstance(k, str) else k: v 
                       for k, v in mcq_input['subtopic_weights'].items()}
    
    main_topic_index = mcq_input['main_topic_index']
    main_topic_node = knowledge_graph.get_node_by_index(main_topic_index)
    chapter = main_topic_node.chapter
    
    # Calculate prerequisites using existing adjacency matrix function
    prerequisites = _calculate_prerequisites(
        subtopic_weights, knowledge_graph
    )
    overall_difficulty = difficulty_breakdown.calculate_overall()
    # Build complete MCQ dictionary
    complete_mcq = {
        "id": mcq_id,
        "text": str(mcq_input['text']),
        "options": list(mcq_input['options']),
        "correctindex": int(mcq_input['correctindex']),
        "option_explanations": list(mcq_input['option_explanations']),
        "main_topic_index": int(main_topic_index),
        "chapter": str(chapter),
        "subtopic_weights": {str(k): float(v) for k, v in subtopic_weights.items()},
        "difficulty_breakdown": {
            "conceptual_understanding": float(difficulty_breakdown.conceptual_understanding),
            "procedural_fluency": float(difficulty_breakdown.procedural_fluency),
            "problem_solving": float(difficulty_breakdown.problem_solving),
            "mathematical_communication": float(difficulty_breakdown.mathematical_communication),
            "memory": float(difficulty_breakdown.memory),
            "spatial_reasoning": float(difficulty_breakdown.spatial_reasoning)
        },
        "overall_difficulty": float(overall_difficulty),
        "prerequisites": prerequisites
    }
    return complete_mcq



    



def example_usage():
    kg = KnowledgeGraph()
    mcq_document = 'mcqs.json'
    print("\n" + "="*50)
    # Process all MCQs
    processed_mcqs = process_mcq_document(mcq_document, kg)
    with open('computed_mcqs.json', 'w') as f:
        json.dump({"mcqs": processed_mcqs}, f, indent=2)

if __name__ == "__main__":
    example_usage()