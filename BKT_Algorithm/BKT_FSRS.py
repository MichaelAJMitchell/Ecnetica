from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import math
import networkx as nx
# This will interface with the knowledge graph in the full code file
#but for now just making some updates to the bkt class seperately to add functionalities


# FSRS Memory Components 
@dataclass
class FSRSMemoryComponents:
    """FSRS-inspired memory components for modeling different types of forgetting"""
    stability: float = 1.0
    difficulty: float = 0.5
    retrievability: float = 1.0
    last_review: Optional[datetime] = None
    review_count: int = 0
    recent_success_rate: float = 0.5

@dataclass
class FSRSForgettingConfig:
    """Configuration for FSRS-inspired forgetting model"""
    stability_power_factor: float = -0.5
    difficulty_power_factor: float = 0.3
    retrievability_power_factor: float = -0.8
    stability_weight: float = 0.4
    difficulty_weight: float = 0.3
    retrievability_weight: float = 0.3
    success_stability_boost: float = 1.2
    failure_stability_penalty: float = 0.8
    difficulty_adaptation_rate: float = 0.1
    base_forgetting_time: float = 1.0
    max_stability: float = 365.0
    min_stability: float = 0.1
    retrievability_threshold: float = 0.9
    min_retrievability: float = 0.1

class FSRSForgettingModel:
    """FSRS-inspired forgetting model using power functions"""
    
    def __init__(self, config: FSRSForgettingConfig = None):
        self.config = config or FSRSForgettingConfig()
        self.memory_components: Dict[str, Dict[int, FSRSMemoryComponents]] = {}
    
    def get_memory_components(self, student_id: str, topic_index: int) -> FSRSMemoryComponents:
        """Get or initialize memory components for a student-topic pair"""
        if student_id not in self.memory_components:
            self.memory_components[student_id] = {}
        
        if topic_index not in self.memory_components[student_id]:
            # Initialize with default values
            self.memory_components[student_id][topic_index] = FSRSMemoryComponents(
                stability=1.0,
                difficulty=0.5,
                retrievability=1.0,
                last_review=datetime.now(),
                review_count=0,
                recent_success_rate=0.5
            )
        
        return self.memory_components[student_id][topic_index]
    
    def apply_forgetting(self, student_id: str, topic_index: int, current_mastery: float) -> float:
        """Apply FSRS-inspired forgetting to current mastery level"""
        components = self.get_memory_components(student_id, topic_index)
        
        if components.last_review is None:
            components.last_review = datetime.now()
            return current_mastery
        
        # Calculate time since last review in days
        time_elapsed = (datetime.now() - components.last_review).total_seconds() / (24 * 3600)
        
        if time_elapsed <= 0:
            return current_mastery
        
        # FSRS-inspired forgetting formula using power functions
        stability_factor = math.pow(time_elapsed, self.config.stability_power_factor) * components.stability
        difficulty_factor = math.pow(components.difficulty, self.config.difficulty_power_factor)
        retrievability_factor = math.pow(components.retrievability, self.config.retrievability_power_factor)
        
        # Combine factors with weights
        forgetting_multiplier = (
            self.config.stability_weight * stability_factor +
            self.config.difficulty_weight * difficulty_factor +
            self.config.retrievability_weight * retrievability_factor
        )
        
        # Apply forgetting with exponential decay
        forgetting_rate = math.exp(-time_elapsed / (self.config.base_forgetting_time * forgetting_multiplier))
        
        # Ensure forgetting doesn't go below minimum threshold
        forgotten_mastery = max(0.01, current_mastery * forgetting_rate)
        
        # Update last access time for retrievability calculations
        components.last_review = datetime.now()
        
        return forgotten_mastery
    
    def update_memory_components(self, student_id: str, topic_index: int, 
                               is_correct: bool, new_mastery: float):
        """Update FSRS memory components based on learning event"""
        components = self.get_memory_components(student_id, topic_index)
        
        # Update review count
        components.review_count += 1
        
        # Update success rate with exponential moving average
        alpha = 0.3  # Learning rate for moving average
        success_value = 1.0 if is_correct else 0.0
        components.recent_success_rate = (
            alpha * success_value + 
            (1 - alpha) * components.recent_success_rate
        )
        
        # Update stability based on performance
        if is_correct:
            components.stability = min(
                self.config.max_stability,
                components.stability * self.config.success_stability_boost
            )
        else:
            components.stability = max(
                self.config.min_stability,
                components.stability * self.config.failure_stability_penalty
            )
        # may change this
        # Update difficulty based on performance and mastery
        if is_correct and new_mastery > 0.7:
            components.difficulty = max(0.1, components.difficulty - self.config.difficulty_adaptation_rate)
        elif not is_correct and new_mastery < 0.5:
            components.difficulty = min(1.0, components.difficulty + self.config.difficulty_adaptation_rate)
        
        # Update retrievability
        if is_correct:
            components.retrievability = min(1.0, components.retrievability + 0.2)
        else:
            components.retrievability = max(0.1, components.retrievability - 0.1)

@dataclass
class BKTConfig:
    """Configuration for BKT algorithm behavior"""
    enable_forgetting: bool = True
    enable_difficulty_adaptation: bool = True
    enable_time_decay: bool = True
    time_decay_lambda: float = 0.1
    forgetting_halflife_days: float = 30.0
    difficulty_learning_scaling: bool = True
    prerequisite_propagation: bool = True
    propagation_decay: float = 0.3
    # Area of Effect parameters
    area_effect_enabled: bool = True
    area_effect_max_distance: int = 2      # Maximum graph distance for effect spread
    area_effect_decay_rate: float = 0.6    # How much effect decays per hop
    area_effect_min_effect: float = 0.01   # Minimum effect to apply
    
    # NEW: FSRS forgetting parameters
    enable_fsrs_forgetting: bool = True
    fsrs_stability_power: float = -0.5
    fsrs_difficulty_power: float = 0.3
    fsrs_retrievability_power: float = -0.8
    fsrs_stability_weight: float = 0.4
    fsrs_difficulty_weight: float = 0.3
    fsrs_retrievability_weight: float = 0.3
    fsrs_success_stability_boost: float = 1.2
    fsrs_failure_stability_penalty: float = 0.8
    fsrs_difficulty_adaptation_rate: float = 0.1

@dataclass
class BKTParameters:
    """BKT model parameters for a specific skill/topic"""
    prior_knowledge: float = 0.1  # P(L_0) - probability student knows skill beforehand
    learning_rate: float = 0.3    # P(T) - probability student learns skill after question
    slip_rate: float = 0.05       # P(S) - probability student knows but gets wrong
    guess_rate: float = 0.15      # P(G) - probability student doesn't know but gets right

    def __post_init__(self):
        """Validate parameters are in valid ranges"""
        if not (0 <= self.prior_knowledge <= 1):
            raise ValueError("Prior knowledge must be between 0 and 1")
        if not (0 <= self.learning_rate <= 1):
            raise ValueError("Learning rate must be between 0 and 1")
        if not (0 <= self.slip_rate <= 0.3):  # Following Corbett & Anderson constraint
            raise ValueError("Slip rate should be between 0 and 0.3")
        if not (0 <= self.guess_rate <= 0.3):  # Following Corbett & Anderson constraint
            raise ValueError("Guess rate should be between 0 and 0.3")

class BayesianKnowledgeTracing:
    """
    Enhanced Bayesian Knowledge Tracing with FSRS forgetting
    Drop-in replacement for the original BKT class
    """
    
    def __init__(self, knowledge_graph, student_manager, 
                 default_params: BKTParameters = None, 
                 config: BKTConfig = None, 
                 scheduler: Optional['MCQScheduler'] = None):
        """
        Initialize BKT with knowledge graph and student manager

        Args:
            knowledge_graph: The KnowledgeGraph instance
            student_manager: The StudentManager instance
            default_params: Default BKT parameters for all topics
            config: BKT configuration object
            scheduler: Optional MCQScheduler instance
        """
        self.kg = knowledge_graph
        self.student_manager = student_manager
        self.default_params = default_params or BKTParameters()
        self.config = config or BKTConfig()
        self.scheduler = scheduler

        # Topic-specific parameters (can be customized per topic)
        self.topic_parameters: Dict[int, BKTParameters] = {}

        # Initialize default parameters for all topics
        self._initialize_topic_parameters()
        
        # Initialize FSRS forgetting model if enabled
        if self.config.enable_fsrs_forgetting:
            fsrs_config = FSRSForgettingConfig(
                stability_power_factor=self.config.fsrs_stability_power,
                difficulty_power_factor=self.config.fsrs_difficulty_power,
                retrievability_power_factor=self.config.fsrs_retrievability_power,
                stability_weight=self.config.fsrs_stability_weight,
                difficulty_weight=self.config.fsrs_difficulty_weight,
                retrievability_weight=self.config.fsrs_retrievability_weight,
                success_stability_boost=self.config.fsrs_success_stability_boost,
                failure_stability_penalty=self.config.fsrs_failure_stability_penalty,
                difficulty_adaptation_rate=self.config.fsrs_difficulty_adaptation_rate
            )
            self.fsrs_forgetting = FSRSForgettingModel(fsrs_config)
        else:
            self.fsrs_forgetting = None

    def _initialize_topic_parameters(self):
        """Initialize BKT parameters for all topics in the knowledge graph"""
        for node_index in self.kg.get_all_indexes():
            if node_index not in self.topic_parameters:
                self.topic_parameters[node_index] = BKTParameters(
                    prior_knowledge=0.1,
                    learning_rate=0.3,
                    slip_rate=0.05,
                    guess_rate=0.15
                )

    def set_topic_parameters(self, main_topic_index: int, params: BKTParameters):
        """Set custom BKT parameters for a specific topic"""
        self.topic_parameters[main_topic_index] = params

    def get_topic_parameters(self, main_topic_index: int) -> BKTParameters:
        """Get BKT parameters for a specific topic"""
        return self.topic_parameters.get(main_topic_index, self.default_params)

    def _get_effective_parameters(self, main_topic_index: int, mcq_id: str = None) -> BKTParameters:
        """
        Get effective parameters for a topic, potentially adjusted for difficulty

        Args:
            main_topic_index: Index of the topic
            mcq_id: Optional MCQ ID for difficulty-based adjustments

        Returns:
            BKTParameters (potentially adjusted)
        """
        base_params = self.get_topic_parameters(main_topic_index)

        if not self.config.enable_difficulty_adaptation or not mcq_id:
            return base_params

        # Get MCQ difficulty if available
        mcq = self.kg.mcqs.get(mcq_id)
        if not mcq:
            return base_params

        difficulty = mcq.difficulty
        current_params = base_params

        # Adjust learning rate based on difficulty
        # Harder questions should have higher learning rewards
        difficulty_factor = 1.0 + (difficulty - 0.5) * 0.4
        adjusted_learning = min(0.8, current_params.learning_rate * difficulty_factor)

        # Adjust slip rate based on difficulty
        # Harder questions might have higher slip rates
        slip_factor = 1.0 + (difficulty - 0.5) * 0.2
        adjusted_slip = min(0.3, current_params.slip_rate * slip_factor)

        return BKTParameters(
            prior_knowledge=current_params.prior_knowledge,
            learning_rate=adjusted_learning,
            slip_rate=max(0.01, min(0.3, adjusted_slip)),
            guess_rate=current_params.guess_rate
        )

    def initialize_student_mastery(self, student_id: str, main_topic_index: int = None):
        """
        Initialize student's mastery level for a topic or all topics using P(L_0)

        Args:
            student_id: Student identifier
            main_topic_index: Specific topic index, or None for all topics
        """
        student = self.student_manager.get_student(student_id)
        if not student:
            return

        if main_topic_index is not None:
            # Initialize specific topic
            params = self.get_topic_parameters(main_topic_index)
            student.mastery_levels[main_topic_index] = params.prior_knowledge
        else:
            # Initialize all topics
            for node_index in self.kg.get_all_indexes():
                if node_index not in student.mastery_levels:
                    params = self.get_topic_parameters(node_index)
                    student.mastery_levels[node_index] = params.prior_knowledge

    def calculate_conditional_probability(self, current_mastery: float, is_correct: bool, 
                                        params: BKTParameters) -> float:
        """Calculate P(L_t | Result) using Bayes' theorem"""
        if is_correct:
            numerator = current_mastery * (1 - params.slip_rate)
            denominator = (current_mastery * (1 - params.slip_rate) +
                          (1 - current_mastery) * params.guess_rate)
        else:
            numerator = current_mastery * params.slip_rate
            denominator = (current_mastery * params.slip_rate +
                          (1 - current_mastery) * (1 - params.guess_rate))

        if denominator == 0:
            return current_mastery
        return numerator / denominator

    def update_mastery(self, conditional_prob: float, params: BKTParameters) -> float:
        """Update mastery using learning rate: P(L_{t+1}) = P(L_t|Result) + (1-P(L_t|Result))P(T)"""
        return conditional_prob + (1 - conditional_prob) * params.learning_rate

    def predict_correctness(self, mastery: float, params: BKTParameters) -> float:
        """Predict probability of correct answer: P(Correct) = P(L_t)(1-P(S)) + (1-P(L_t))P(G)"""
        return mastery * (1 - params.slip_rate) + (1 - mastery) * params.guess_rate

    def process_student_response(self, student_id: str, main_topic_index: int,
                                is_correct: bool, mcq_id: str = None,
                                custom_params: Optional[BKTParameters] = None) -> Dict:
        """
        Process a student's response and update their mastery using BKT
        FSRS forgetting applied automatically
        """
        student = self.student_manager.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Use provided custom parameters or default for topic
        params = custom_params if custom_params else self.get_topic_parameters(main_topic_index)

        # Get current mastery level
        current_mastery = student.get_mastery(main_topic_index)
        mastery_before_forgetting = current_mastery

        # If this is the first time seeing this topic, initialize with prior
        if main_topic_index not in student.mastery_levels:
            current_mastery = params.prior_knowledge
            student.mastery_levels[main_topic_index] = current_mastery
            mastery_before_forgetting = current_mastery

        # Apply FSRS forgetting if enabled
        if self.config.enable_fsrs_forgetting and self.fsrs_forgetting:
            forgotten_mastery = self.fsrs_forgetting.apply_forgetting(
                student_id, main_topic_index, current_mastery)
            student.mastery_levels[main_topic_index] = forgotten_mastery
            current_mastery = forgotten_mastery
        else:
            forgotten_mastery = current_mastery

        # Calculate prediction before update (for validation)
        prediction_before = self.predict_correctness(current_mastery, params)

        # Apply BKT update
        conditional_prob = self.calculate_conditional_probability(current_mastery, is_correct, params)
        new_mastery = self.update_mastery(conditional_prob, params)

        # Update student's mastery level
        student.mastery_levels[main_topic_index] = new_mastery

        # Update FSRS memory components after BKT update
        if self.config.enable_fsrs_forgetting and self.fsrs_forgetting:
            self.fsrs_forgetting.update_memory_components(
                student_id, main_topic_index, is_correct, new_mastery)

        # Calculate new prediction
        prediction_after = self.predict_correctness(new_mastery, params)

        # Return detailed information about the update (enhanced with FSRS info)
        result = {
            'student_id': student_id,
            'main_topic_index': main_topic_index,
            'topic_name': self.kg.get_topic_of_index(main_topic_index),
            'mcq_id': mcq_id,
            'is_correct': is_correct,
            'mastery_before': mastery_before_forgetting,
            'mastery_after': new_mastery,
            'mastery_change': new_mastery - current_mastery,
            'conditional_probability': conditional_prob,
            'prediction_before': prediction_before,
            'prediction_after': prediction_after,
            'parameters_used': {
                'prior_knowledge': params.prior_knowledge,
                'learning_rate': params.learning_rate,
                'slip_rate': params.slip_rate,
                'guess_rate': params.guess_rate
            }
        }

        # Add FSRS information if enabled
        if self.config.enable_fsrs_forgetting and self.fsrs_forgetting:
            components = self.fsrs_forgetting.get_memory_components(student_id, main_topic_index)
            result['fsrs_components'] = {
                'stability': components.stability,
                'difficulty': components.difficulty,
                'retrievability': components.retrievability,
                'review_count': components.review_count,
                'recent_success_rate': components.recent_success_rate
            }
            result['mastery_after_forgetting'] = forgotten_mastery
            result['forgetting_applied'] = mastery_before_forgetting - forgotten_mastery
            result['total_change'] = new_mastery - mastery_before_forgetting

        return result

    def process_mcq_response_improved(self, student_id: str, mcq_id: str,
                                    is_correct: bool) -> List[Dict]:
        """
        Enhanced version that uses explicit topic weights from the MCQ
        with FSRS forgetting applied automatically
        """
        mcq = self.kg.mcqs.get(mcq_id)
        if not mcq:
            raise ValueError(f"MCQ {mcq_id} not found")

        # FIXED: Import MCQScheduler properly to avoid circular imports 
        try:
            from mcq_algorithm_full_python import MCQScheduler
            scheduler = MCQScheduler(self.kg, self.student_manager)
            scheduler._precompute_prerequisites()
            mcq_vector = scheduler.mcq_vectors.get(mcq_id)
        except ImportError:
            # Fallback if import fails - just use the MCQ directly
            mcq_vector = None

        updates = []

        # Use the MCQ's explicit topic weights directly 
        for main_topic_index, weight in mcq.subtopic_weights.items():
            # Get base parameters for this topic
            base_params = self._get_effective_parameters(main_topic_index, mcq_id)

            # Create adjusted parameters with scaled learning rate
            adjusted_params = BKTParameters(
                prior_knowledge=base_params.prior_knowledge,
                learning_rate=base_params.learning_rate * weight,  # Scale by weight
                slip_rate=base_params.slip_rate,
                guess_rate=base_params.guess_rate
            )

            # Process with enhanced method (includes FSRS forgetting)
            update = self.process_student_response(
                student_id, main_topic_index, is_correct, mcq_id, custom_params=adjusted_params)
            
            update['topic_weight'] = weight
            update['is_primary_topic'] = (main_topic_index == mcq.main_topic_index)

            updates.append(update)

        return updates

    def apply_area_of_effect(self, student_id: str, center_main_topic_index: int,
                           mastery_change: float, max_distance: int = 3,
                           decay_rate: float = 0.5) -> List[Dict]:
        """
        Area of effect that uses actual path weights between topics.
        """
        if mastery_change <= 0:
            return []

        student = self.student_manager.get_student(student_id)
        if not student:
            return []

        # Use NetworkX to find all shortest paths within distance
        undirected_graph = self.kg.graph.to_undirected()

        try:
            # Get all shortest paths to nodes within max_distance
            paths = nx.single_source_shortest_path(undirected_graph, center_main_topic_index, cutoff=max_distance)
        except Exception:  # Catch any NetworkX errors
            return []

        # Remove center node (path to itself)
        paths.pop(center_main_topic_index, None)

        updates = []

        for main_topic_index, path in paths.items():
            distance = len(path) - 1  # Number of edges in path

            # Calculate path weight by multiplying all edge weights along the path
            path_weight = self._calculate_path_weight(path)

            # Calculate effect: decay^distance * mastery_change * path_weight
            base_effect = mastery_change * (decay_rate ** distance)
            final_effect = base_effect * path_weight

            # Only apply significant effects
            if final_effect > 0.01:
                current_mastery = student.get_mastery(main_topic_index)
                new_mastery = min(1.0, current_mastery + final_effect)

                # Update student mastery
                student.mastery_levels[main_topic_index] = new_mastery

                # Record the update
                updates.append({
                    'main_topic_index': main_topic_index,
                    'topic_name': self.kg.get_topic_of_index(main_topic_index),
                    'mastery_before': current_mastery,
                    'mastery_after': new_mastery,
                    'mastery_change': new_mastery - current_mastery,
                    'distance': distance,
                    'path_weight': path_weight,
                    'effect_strength': final_effect,
                    'path': [self.kg.get_topic_of_index(idx) for idx in path],
                    'update_type': 'area_effect'
                })

        return updates

    def _calculate_path_weight(self, path: List[int]) -> float:
        """
        Calculate the combined weight along a path by multiplying edge weights.
        """
        if len(path) < 2:
            return 1.0

        total_weight = 1.0
        for i in range(len(path) - 1):
            source, target = path[i], path[i + 1]
            
            # Get edge weight (check both directions since we're using undirected)
            edge_weight = 0.5  # Default weight
            
            if self.kg.graph.has_edge(source, target):
                edge_weight = self.kg.graph[source][target].get('weight', 0.5)
            elif self.kg.graph.has_edge(target, source):
                edge_weight = self.kg.graph[target][source].get('weight', 0.5)
            
            # Multiply weights along the path
            total_weight *= edge_weight

        return total_weight

    def process_mcq_response_simple(self, student_id: str, mcq_id: str, is_correct: bool) -> List[Dict]:
        """
        Simple wrapper that adds area of effect to improved response processing.
        FSRS forgetting applied automatically
        """
        # Do normal MCQ processing first (now includes FSRS forgetting)
        primary_updates = self.process_mcq_response_improved(student_id, mcq_id, is_correct)

        if not is_correct:  # Only spread effects on correct answers
            return primary_updates

        all_updates = primary_updates.copy()

        # Add area effects for primary topics that had positive mastery changes
        for update in primary_updates:
            if update.get('is_primary_topic', False) and update['mastery_change'] > 0:
                area_updates = self.apply_area_of_effect(
                    student_id, update['main_topic_index'], update['mastery_change'])
                all_updates.extend(area_updates)

        return all_updates

    def process_mcq_with_area_effect(self, student_id: str, mcq_id: str, is_correct: bool) -> List[Dict]:
        """
        Simplified MCQ processing with area effects.
        Replaces the longer process_mcq_response_with_area_effect method.
        """
        # Do normal MCQ processing first
        primary_updates = self.process_mcq_response_improved(student_id, mcq_id, is_correct)

        if not is_correct:  # Only spread effects on correct answers
            return primary_updates

        all_updates = primary_updates.copy()

        # Add area effects for primary topics that had positive mastery changes
        for update in primary_updates:
            if update.get('is_primary_topic', False) and update['mastery_change'] > 0:
                area_updates = self.apply_area_of_effect(
                    student_id, update['main_topic_index'], update['mastery_change'])
                all_updates.extend(area_updates)

        return all_updates

    def calibrate_parameters(self, student_id: str, main_topic_index: int,
                           attempt_history: List[Tuple[bool, datetime]]) -> BKTParameters:
        """
        Simple parameter calibration based on student's attempt history
        This is a basic implementation - more sophisticated methods exist

        Args:
            student_id: Student identifier
            main_topic_index: Topic to calibrate for
            attempt_history: List of (is_correct, timestamp) tuples

        Returns:
            Calibrated BKT parameters
        """
        if not attempt_history:
            return self.get_topic_parameters(main_topic_index)

        # Calculate basic statistics
        total_attempts = len(attempt_history)
        correct_attempts = sum(1 for is_correct, _ in attempt_history if is_correct)
        success_rate = correct_attempts / total_attempts

        # Simple heuristic calibration
        current_params = self.get_topic_parameters(main_topic_index)

        # Adjust guess rate based on early performance
        early_attempts = attempt_history[:min(3, total_attempts)]
        early_success = sum(1 for is_correct, _ in early_attempts if is_correct)
        early_rate = early_success / len(early_attempts)

        # If student does well early, they might have higher prior knowledge
        adjusted_prior = min(0.8, current_params.prior_knowledge + early_rate * 0.3)

        # If overall success rate is very high, reduce slip rate
        adjusted_slip = max(0.01, current_params.slip_rate - (success_rate - 0.7) * 0.1)

        # If success rate is low but attempts are many, increase learning rate
        adjusted_learning = min(0.8, current_params.learning_rate +
                              (0.1 if success_rate < 0.5 and total_attempts > 5 else 0))

        return BKTParameters(
            prior_knowledge=adjusted_prior,
            learning_rate=adjusted_learning,
            slip_rate=max(0.01, min(0.3, adjusted_slip)),
            guess_rate=current_params.guess_rate
        )

    # NEW METHODS FOR FSRS FUNCTIONALITY
    def get_current_mastery_with_decay(self, student_id: str, topic_index: int) -> float:
        """Get current mastery level with forgetting applied, without updating stored values"""
        student = self.student_manager.get_student(student_id)
        if not student:
            return 0.0

        stored_mastery = student.get_mastery(topic_index)

        if self.config.enable_fsrs_forgetting and self.fsrs_forgetting:
            return self.fsrs_forgetting.apply_forgetting(student_id, topic_index, stored_mastery)
        else:
            return stored_mastery

    def get_review_recommendations(self, student_id: str, 
                                 target_retention: float = 0.9) -> List[Dict]:
        """Get review recommendations based on FSRS forgetting predictions"""
        if not self.config.enable_fsrs_forgetting or not self.fsrs_forgetting:
            return []

        student = self.student_manager.get_student(student_id)
        if not student:
            return []

        recommendations = []

        for topic_index, mastery in student.mastery_levels.items():
            if mastery > 0.05:  # Only consider topics with minimal mastery
                components = self.fsrs_forgetting.get_memory_components(student_id, topic_index)
                
                if components.review_count > 0:
                    # Calculate current retention
                    current_mastery = self.get_current_mastery_with_decay(student_id, topic_index)
                    retention_ratio = current_mastery / mastery if mastery > 0 else 0
                    
                    # Calculate priority score based on retention drop and importance
                    retention_drop = 1.0 - retention_ratio
                    importance_score = mastery  # Higher mastery = more important to maintain
                    
                    priority_score = retention_drop * importance_score
                    
                    if retention_ratio < target_retention:
                        recommendations.append({
                            'topic_index': topic_index,
                            'topic_name': self.kg.get_topic_of_index(topic_index),
                            'current_mastery': current_mastery,
                            'original_mastery': mastery,
                            'retention_ratio': retention_ratio,
                            'priority_score': priority_score,
                            'review_count': components.review_count,
                            'stability': components.stability,
                            'difficulty': components.difficulty
                        })

        # Sort by priority score (descending)
        recommendations.sort(key=lambda x: x['priority_score'], reverse=True)
        return recommendations

    def get_fsrs_diagnostics(self, student_id: str) -> Dict:
        """Get diagnostic information about FSRS forgetting state for a student"""
        if not self.config.enable_fsrs_forgetting or not self.fsrs_forgetting:
            return {'fsrs_enabled': False}

        student = self.student_manager.get_student(student_id)
        if not student:
            return {'error': 'Student not found'}

        diagnostics = {
            'fsrs_enabled': True,
            'total_topics': len(student.mastery_levels),
            'topics_with_memory_components': 0,
            'average_stability': 0.0,
            'average_difficulty': 0.0,
            'average_retrievability': 0.0,
            'topics_needing_review': 0
        }

        stability_sum = 0.0
        difficulty_sum = 0.0
        retrievability_sum = 0.0
        component_count = 0

        for topic_index, mastery in student.mastery_levels.items():
            if mastery > 0.05:  # Only consider topics with minimal mastery
                components = self.fsrs_forgetting.get_memory_components(student_id, topic_index)
                
                if components.review_count > 0:
                    component_count += 1
                    stability_sum += components.stability
                    difficulty_sum += components.difficulty
                    retrievability_sum += components.retrievability
        
                    # Check if needs review (retention < 90%)
                    current_retention = self.fsrs_forgetting.apply_forgetting(
                        student_id, topic_index, mastery) / mastery
                    if current_retention < 0.9:
                        diagnostics['topics_needing_review'] += 1

        diagnostics['topics_with_memory_components'] = component_count
        if component_count > 0:
            diagnostics['average_stability'] = stability_sum / component_count
            diagnostics['average_difficulty'] = difficulty_sum / component_count
            diagnostics['average_retrievability'] = retrievability_sum / component_count

        return diagnostics


# UTILITY FUNCTIONS (from full Python file)
def analyze_area_of_effect(bkt_updates: List[Dict], kg) -> Dict:
    """
    Analyze BKT updates to categorize primary vs area-of-effect changes.
    """
    if not bkt_updates:
        return {'primary_count': 0, 'area_effect_count': 0, 'total_updates': 0,
                'primary_updates': [], 'area_effect_updates': []}

    primary_updates = [u for u in bkt_updates if u.get('is_primary_topic', False)]
    area_effect_updates = [u for u in bkt_updates if not u.get('is_primary_topic', False)]

    return {
        'primary_count': len(primary_updates),
        'area_effect_count': len(area_effect_updates),
        'total_updates': len(bkt_updates),
        'primary_updates': primary_updates,
        'area_effect_updates': area_effect_updates
    }


def visualize_knowledge_graph(kg, student_manager, student_id: str,
                             before_masteries: Dict[int, float] = None,
                             after_masteries: Dict[int, float] = None,
                             title_suffix: str = ""):
    """
    Create knowledge graph visualization showing mastery levels.
    """
    student = student_manager.get_student(student_id)
    if not student:
        print(f"Student {student_id} not found!")
        return
    
    try:
        import matplotlib.pyplot as plt
        import networkx as nx
        import numpy as np
    except ImportError:
        print("Visualization requires matplotlib and networkx")
        return

    # Use current masteries if before/after not provided
    if before_masteries is None:
        before_masteries = student.mastery_levels.copy()
    if after_masteries is None:
        after_masteries = student.mastery_levels.copy()

    # Create figure with subplots if we have before/after
    if before_masteries != after_masteries:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        axes = [ax1, ax2]
        masteries_list = [before_masteries, after_masteries]
        titles = [f"Before{title_suffix}", f"After{title_suffix}"]
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        axes = [ax]
        masteries_list = [before_masteries]
        titles = [f"Current Mastery{title_suffix}"]

    for i, (ax, masteries, title) in enumerate(zip(axes, masteries_list, titles)):
        # Get positions using spring layout
        pos = nx.spring_layout(kg.graph, k=2, iterations=50, seed=42)

        # Color nodes based on mastery levels
        node_colors = []
        node_sizes = []
        for node in kg.graph.nodes():
            mastery = masteries.get(node, 0.0)
            # Color: red (low) -> yellow (medium) -> green (high)
            if mastery < 0.3:
                color = 'red'
            elif mastery < 0.7:
                color = 'orange'
            else:
                color = 'green'
            node_colors.append(color)
            node_sizes.append(300 + mastery * 700)  # Size based on mastery

        # Draw the graph
        nx.draw_networkx_nodes(kg.graph, pos, node_color=node_colors, 
                              node_size=node_sizes, alpha=0.8, ax=ax)

        # Draw edges with weights
        edges = kg.graph.edges()
        if edges:
            weights = [kg.graph[u][v].get('weight', 0.5) for u, v in edges]
            nx.draw_networkx_edges(kg.graph, pos, edge_color='gray',
                                  width=[w*3 for w in weights], alpha=0.6,
                                  arrows=True, arrowsize=15, ax=ax)

        # Draw labels
        labels = {}
        for node in kg.graph.nodes():
            topic_name = kg.get_topic_of_index(node)
            mastery = masteries.get(node, 0.0)
            labels[node] = f"{topic_name[:10]}...\n({mastery:.2f})"

        nx.draw_networkx_labels(kg.graph, pos, labels, font_size=8, ax=ax)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                   markersize=10, label='Low Mastery (< 0.3)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', 
                   markersize=10, label='Medium Mastery (0.3-0.7)'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='green', 
                   markersize=10, label='High Mastery (> 0.7)')
    ]
    
    if len(axes) == 1:
        axes[0].legend(handles=legend_elements, loc='upper right')
    else:
        fig.legend(handles=legend_elements, loc='upper center', 
                  bbox_to_anchor=(0.5, 0.02), ncol=3)

    plt.tight_layout()
    plt.show()