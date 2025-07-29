"""
Adaptive Question Selection Algorithm

This implements an intelligent question selection system that:
- Analyzes student mastery across knowledge topics
- Selects questions optimally based on learning needs
- Uses prerequisite relationships and difficulty matching
- Optimizes for maximum learning efficiency

Main Classes:
    MCQScheduler: Core algorithm for adaptive question 
    OptimizedMCQVector: Efficient question representation
    MinimalMCQData: Memory-optimized question data
"""




import numpy as np
import networkx as nx
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import math 
import json



@dataclass
class MinimalMCQData:
    """
    Contains ONLY the data needed for select_optimal_mcqs algorithm
    """
    id: str
    main_topic_index: int
    subtopic_weights: Dict[int, float]  # For coverage calculation
    difficulty: float  # For cost calculation
    prerequisites: Dict[int, float]  # For prerequisite coverage
    
    # Optional: only load if actually needed
    text: Optional[str] = None  # Only for display/debugging
    chapter: Optional[str] = None

class MCQLoader:
    """
    Loads only the minimal data needed for select_optimal_mcqs algorithm to save memory
    """
    
    def __init__(self, mcqs_file: str):
        self.mcqs_file = mcqs_file
        
        # Core data structures (minimal memory)
        self.minimal_mcq_data: Dict[str, MinimalMCQData] = {}
        self.topic_to_mcq_ids: Dict[int, Set[str]] = {}
        
        # Lazy loading for full MCQ objects (only when absolutely needed)
        self._full_mcq_cache: Dict[str, 'MCQ'] = {}
        self._raw_mcq_data: Dict[str, dict] = {}
        
        # Build the minimal index
        self._build_minimal_index()
    
    def _build_minimal_index(self):
        """Build index with only essential data for the algorithm"""
        print(f"🔍 Building optimized MCQ index from {self.mcqs_file}...")
        
        try:
            with open(self.mcqs_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            mcqs_data = data.get('mcqs', data) if isinstance(data, dict) else data
            
            for mcq_data in mcqs_data:
                mcq_id = mcq_data['id']
                
                # Convert string keys to integers (only conversion needed)
                subtopic_weights = {int(k): v for k, v in mcq_data['subtopic_weights'].items()}
                prerequisites = {int(k): v for k, v in mcq_data['prerequisites'].items()}
                
                # Use precomputed values directly - no calculations!
                minimal_data = MinimalMCQData(
                    id=mcq_id,
                    main_topic_index=mcq_data['main_topic_index'],
                    subtopic_weights=subtopic_weights,
                    difficulty=mcq_data['overall_difficulty'],  # Direct use
                    prerequisites=prerequisites,  # Direct use
                    chapter=mcq_data.get('chapter')
                )
                
                self.minimal_mcq_data[mcq_id] = minimal_data
                
                # Index by main topic
                main_topic = mcq_data['main_topic_index']
                if main_topic not in self.topic_to_mcq_ids:
                    self.topic_to_mcq_ids[main_topic] = set()
                self.topic_to_mcq_ids[main_topic].add(mcq_id)
                
                # Store raw data for full MCQ creation
                self._raw_mcq_data[mcq_id] = mcq_data
                
        except Exception as e:
            print(f"❌ Error building minimal index: {e}")
            raise
    
        print(f"✅  optimized index complete:")
        print(f"   📊 {len(self.minimal_mcq_data)} MCQs indexed")
        print(f"   📂 {len(self.topic_to_mcq_ids)} topics") 
    

    def get_mcqs_for_due_topics_minimal(self, due_topic_indices: List[int]) -> List[MinimalMCQData]:
        """
        Get minimal MCQ data for due topics
        This is what select_optimal_mcqs actually needs
        """
        relevant_mcqs = []
        
        for topic_index in due_topic_indices:
            if topic_index in self.topic_to_mcq_ids:
                for mcq_id in self.topic_to_mcq_ids[topic_index]:
                    minimal_data = self.minimal_mcq_data[mcq_id]
                    relevant_mcqs.append(minimal_data)
        
        return relevant_mcqs
    
    def get_mcq_ids_for_due_topics(self, due_topic_indices: List[int]) -> List[str]:
        """Get just the MCQ IDs for due topics """
        mcq_ids = []
        for topic_index in due_topic_indices:
            if topic_index in self.topic_to_mcq_ids:
                mcq_ids.extend(self.topic_to_mcq_ids[topic_index])
        return mcq_ids
    
    def get_minimal_mcq_data(self, mcq_id: str) -> Optional[MinimalMCQData]:
        """Get minimal data for a specific MCQ"""
        return self.minimal_mcq_data.get(mcq_id)
    
    def get_full_mcq_if_needed(self, mcq_id: str) -> Optional['MCQ']:
        """
        Load full MCQ object when necessary
        (e.g., for display text, detailed analysis)
        """
        if mcq_id in self._full_mcq_cache:
            return self._full_mcq_cache[mcq_id]
        
        if mcq_id in self._raw_mcq_data:
            try:
                mcq = MCQ.from_dict(self._raw_mcq_data[mcq_id])
                self._full_mcq_cache[mcq_id] = mcq
                return mcq
            except Exception as e:
                print(f"❌ Failed to create full MCQ {mcq_id}: {e}")
                return None
        
        return None
    
    def get_stats(self) -> Dict:
        """Get loader statistics"""
        minimal_memory = len(self.minimal_mcq_data) * 0.5  # Estimate KB
        full_memory = len(self._full_mcq_cache) * 5  # Estimate KB
        
        return {
            'total_indexed': len(self.minimal_mcq_data),
            'minimal_data_loaded': len(self.minimal_mcq_data),
            'full_mcqs_cached': len(self._full_mcq_cache),
            'topics_indexed': len(self.topic_to_mcq_ids),
            'estimated_minimal_memory_kb': minimal_memory,
            'estimated_full_memory_kb': full_memory,
            'memory_savings_percent': (1 - (minimal_memory + full_memory) / (len(self.minimal_mcq_data) * 5)) * 100
        }


@dataclass
class Node:
    """
    Represents a learning topic/concept in the educational knowledge graph.
    Each node is a skill or concept that students need to master.
    """
    topic: str  # Name of the topic (e.g., "solving linear equations")
    chapter: str  # Course chapter this topic belongs to
    dependencies: List[Tuple[int, float]]  # Prerequisites: [(topic_index, importance_weight)]
    _in_degree: Optional[int] = field(default=None, init=False)  # Cached incoming connections
    _out_degree: Optional[int] = field(default=None, init=False)  # Cached outgoing connections

@dataclass
class DifficultyBreakdown:
    """
    Breaks down question difficulty across different cognitive skills.
    Helps match questions to student abilities in specific areas.
    """
    conceptual_understanding: float = 0.0
    procedural_fluency: float = 0.0
    problem_solving: float = 0.0
    mathematical_communication: float = 0.0
    memory: float = 0.0
    spatial_reasoning: float = 0.0

    def calculate_overall(self) -> float:
        """Calculate average difficulty across all cognitive skills, 
        as this is what we take as difficulty for each mcq
        """
        return (self.conceptual_understanding +
                self.procedural_fluency +
                self.problem_solving +
                self.mathematical_communication +
                self.memory +
                self.spatial_reasoning) / 6

    @classmethod
    def from_dict(cls, data: Dict[str, float]):
        """Create DifficultyBreakdown from JSON dictionary"""
        return cls(
            conceptual_understanding=data.get('conceptual_understanding', 0.0),
            procedural_fluency=data.get('procedural_fluency', 0.0),
            problem_solving=data.get('problem_solving', 0.0),
            mathematical_communication=data.get('mathematical_communication', 0.0),
            memory=data.get('memory', 0.0),
            spatial_reasoning=data.get('spatial_reasoning', 0.0)
        )
    
    @classmethod
    def create(cls, conceptual=0.0, procedural=0.0, problem_solving=0.0,
               communication=0.0, memory=0.0, spatial=0.0):
        """Factory method for easier instantiation"""
        return cls(conceptual, procedural, problem_solving, communication, memory, spatial)

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for MCQVector compatibility"""
        return {
            'problem_solving': self.problem_solving,
            'memory': self.memory,
            'notation': self.notation,
            'algebra': self.algebra,
            'interconnected': self.interconnected
        }

@dataclass
class MCQ:
    text: str  # Question text (may include LaTeX math)
    options: List[str]  # Answer choices
    correctindex: int  # Index of correct answer (0-based)
    option_explanations: List[str]  # Why each option is correct/incorrect
    main_topic_index: int  # Primary topic being tested
    chapter: str  # Course chapter
    subtopic_weights: Dict[int, float]  # Topics tested: {topic_index: importance_weight}
    difficulty_breakdown: DifficultyBreakdown  # Cognitive skill requirements
    id: str  # Unique identifier

    overall_difficulty: float  # NEW: Store directly from JSON
    prerequisites: Dict[int, float] 

    


    @classmethod
    def from_dict(cls, data: Dict):
        """Create MCQ from JSON dictionary"""
        # Validate core required fields 
        required_fields = ['text', 'options', 'correctindex', 'option_explanations', 
                        'main_topic_index', 'subtopic_weights', 'difficulty_breakdown',
                        'overall_difficulty', 'prerequisites'] 
        
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field '{field}' in MCQ data")
        
        mcq_id = data.get('id')

        # Validate options and explanations match
        if len(data['options']) != len(data['option_explanations']):
            raise ValueError("Number of options must match number of option explanations")
        
        # Validate correct index
        if not (0 <= data['correctindex'] < len(data['options'])):
            raise ValueError(f"Question answer index {data['correctindex']} is invalid. Must be between 0 and {len(data['options'])-1} for {len(data['options'])} answer choices.")
        
        # Convert string keys in subtopic_weights to integers
        try:
            subtopic_weights = {int(k): v for k, v in data['subtopic_weights'].items()}
        except ValueError as e:
            raise ValueError(f"Invalid subtopic_weights format - keys must be convertible to integers: {e}")

        # Convert string keys to integers for prerequisites
        try:
            prerequisites = {int(k): v for k, v in data['prerequisites'].items()}
        except ValueError as e:
            raise ValueError(f"Invalid prerequisites format - keys must be convertible to integers: {e}")
        
        # Validate subtopic weights sum to 1.0 (with tolerance)
        weight_sum = sum(subtopic_weights.values())
        if abs(weight_sum - 1.0) > 0.001:
            raise ValueError(f"Subtopic weights must sum to 1.0, got {weight_sum}")
        
        # Handle chapter - use provided or default
        chapter = data.get('chapter', 'unknown')
        
        difficulty_breakdown = DifficultyBreakdown.from_dict(data['difficulty_breakdown'])

        overall_difficulty = data['overall_difficulty']

        
        return cls(
            text=data['text'],
            options=data['options'],
            correctindex=data['correctindex'],
            option_explanations=data['option_explanations'],
            main_topic_index=data['main_topic_index'],
            chapter=chapter,
            subtopic_weights=subtopic_weights,
            difficulty_breakdown=difficulty_breakdown,
            id=mcq_id,  
            overall_difficulty=overall_difficulty,  
            prerequisites=prerequisites
        )
    
    #for backwards compatibility for now
    @property
    def difficulty(self) -> float:
        """Direct access to precomputed overall difficulty"""
        return self.overall_difficulty

    def get_prerequisites(self, kg=None) -> Dict[int, float]:
        """Direct access to precomputed prerequisites (kg parameter kept for compatibility)"""
        return self.prerequisites

    def get_difficulty(self) -> float:
        """Direct access to precomputed overall difficulty"""
        return self.overall_difficulty


    def __post_init__(self):
        # Validate that explicit weights sum to 1.0
        weight_sum = sum(self.subtopic_weights.values())
        if abs(weight_sum - 1.0) > 0.001:
            raise ValueError(f"Topic weights must sum to 1.0, got {weight_sum}")

@dataclass
class StudentAttempt:
    """Record of a student's attempt at an MCQ"""
    mcq_id: str
    timestamp: datetime
    correct: bool
    time_taken: float  # seconds


class ConfigurationManager:
    """Simple configuration manager that uses JSON values directly"""
    
    def __init__(self, config_file: str = 'config.json'):
        self.config_file = config_file
        self.config = self._load_config_file()
        
    def _load_config_file(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{self.config_file}' not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in configuration file '{self.config_file}': {e}")
    
    def get(self, path: str, default=None):
        """
        Get configuration value using dot notation path
        Example: get('bkt_parameters.default.prior_knowledge')
        """
        keys = path.split('.')
        value = self.config
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_bkt_parameters(self, topic_index: int = None):
        """Get BKT parameters for topic, with fallback to default"""
        if topic_index is not None:
            # Try topic-specific first
            topic_params = self.get(f'bkt_parameters.topic_specific.{topic_index}')
            if topic_params:
                return topic_params
        
        # Fallback to default
        return self.get('bkt_parameters.default')
    
    def reload(self):
        """Reload configuration from file"""
        self.config = self._load_config_file()


@dataclass
class StudentProfile:
    """
    Complete profile tracking a student's learning progress.
    Includes mastery levels, confidence, and attempt history.
    """
    student_id: str
    mastery_levels: Dict[int, float]  # {node_index: mastery_level}
    confidence_levels: Dict[int, float]  # {node_index: confidence_level}
    studied_topics: Dict[int, bool]  #  {node_index: is_studied} this is to take into account topics they havent covered yet
    completed_questions: Set[str]  # set of completed MCQ IDs (this might be something to remove)
    daily_completed: Set[str]  # questions completed today


    ability_levels: Dict[str, float] = field(default_factory=lambda: {
        'conceptual_understanding': 0.5,
        'procedural_fluency': 0.5,
        'problem_solving': 0.5,
        'mathematical_communication': 0.5,
        'memory': 0.5,
        'spatial_reasoning': 0.5
    })
    # Learning history and statistics
    total_questions_attempted: int = 0
    total_time_on_system: float = 0.0  # minutes
    session_count: int = 0
    last_active: Optional[datetime] = None
    registration_date: Optional[datetime] = None
    attempt_history: List[StudentAttempt] = field(default_factory=list)


    def __post_init__(self):
        """Initialize default values if not provided"""
        if self.registration_date is None:
            self.registration_date = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()

    
    def get_mastery(self, node_index: int) -> float:
        """Get mastery level for a topic, defaulting to 0.1 if not set"""
        return self.mastery_levels.get(node_index, 0.1)
    

    def get_confidence(self, node_index: int) -> float:
        """Get confidence level for a topic, defaulting to 0.1 if not set"""
        return self.confidence_levels.get(node_index, 0.1)

    def is_topic_studied(self, node_index: int) -> bool:
        """Check if a topic has been studied by the student"""
        return self.studied_topics.get(node_index, False)

    def mark_topic_as_studied(self, node_index: int):
        """Mark a topic as studied"""
        self.studied_topics[node_index] = True

    def mark_topic_as_not_studied(self, node_index: int):
        """Mark a topic as not studied"""
        self.studied_topics[node_index] = False

    def get_studied_topics(self) -> Set[int]:
        """Get all studied topic indices"""
        return {idx for idx, studied in self.studied_topics.items() if studied}

    def calculate_base_confidence(self, config_manager) -> float:
        """Calculate base confidence based on system usage"""
        # Get confidence parameters from config
        min_confidence = config_manager.get('algorithm_config.min_confidence', 0.1)
        max_confidence = config_manager.get('algorithm_config.max_confidence', 0.95)
        questions_for_full_factor = config_manager.get('algorithm_config.questions_for_full_factor', 100)
        hours_for_full_factor = config_manager.get('algorithm_config.hours_for_full_factor', 20.0)
        confidence_question_weight = config_manager.get('algorithm_config.confidence_question_weight', 0.3)
        confidence_time_weight = config_manager.get('algorithm_config.confidence_time_weight', 0.3)
        confidence_consistency_weight = config_manager.get('algorithm_config.confidence_consistency_weight', 0.2)

        # Confidence grows with:
        # 1. Number of questions attempted
        # 2. Time spent on system
        # 4. Consistency of usage (last active vs registration)

        # Question factor (0 to 1)
        question_factor = min(1.0, self.total_questions_attempted / questions_for_full_factor)

        # Time factor (0 to 1)
        time_factor = min(1.0, (self.total_time_on_system / 60.0) / hours_for_full_factor)

        # Consistency factor (based on days active vs days registered)
        days_registered = max(1, (datetime.now() - self.registration_date).days)
        days_since_last_active = (datetime.now() - self.last_active).days
        consistency_factor = max(0.1, 1.0 - (days_since_last_active / max(days_registered, 7)))

        # Weighted combination
        base_confidence = (
            confidence_question_weight * question_factor +
            confidence_time_weight * time_factor +
            confidence_consistency_weight * consistency_factor
        )

        # Scale to confidence range
        return self.min_confidence + base_confidence * (self.max_confidence - self.min_confidence)

    def calculate_topic_confidence(self, node_index: int, kg, config_manager) -> float:
        """Calculate confidence for a specific topic"""
        min_confidence = config_manager.get('algorithm_config.min_confidence', 0.1)
        max_confidence = config_manager.get('algorithm_config.max_confidence', 0.95)
        attempts_for_full_confidence = config_manager.get('algorithm_config.attempts_for_full_confidence', 10)
        confidence_decay_halflife = config_manager.get('algorithm_config.confidence_decay_halflife', 30.0)
        topic_attempt_weight = config_manager.get('algorithm_config.topic_attempt_weight', 0.7)
        topic_decay_weight = config_manager.get('algorithm_config.topic_decay_weight', 0.3)

        base_confidence = self.calculate_base_confidence(config_manager)

        # Get attempts for this topic
        attempts = self.get_topic_attempts(node_index, kg)

        if not attempts:
            return base_confidence

        # Attempt-based factor
        attempt_factor = min(1.0, len(attempts) / attempts_for_full_confidence)

        # Time decay factor (confidence decreases with time since last attempt)
        last_attempt = max(attempts, key=lambda x: x.timestamp)
        days_since_attempt = (datetime.now() - last_attempt.timestamp).days
        decay_factor = 0.5 ** (days_since_attempt / confidence_decay_halflife)

        # Combine factors
        topic_confidence = (
            topic_attempt_weight * attempt_factor +
            topic_decay_weight * decay_factor
        )

        # Blend with base confidence
        final_confidence = base_confidence + topic_confidence * (self.max_confidence - base_confidence)

        return min(max_confidence, max(min_confidence, final_confidence))


    def get_topic_attempts(self, node_index: int, kg) -> List[StudentAttempt]:
        """Get all attempts for a specific topic - OPTIMIZED"""
        topic_name = kg.get_topic_of_index(node_index)
        if not topic_name:
            return []

        topic_attempts = []
        for attempt in self.attempt_history:
            # For  optimized loading, we only need minimal data
            if hasattr(kg, 'ultra_loader'):
                minimal_data = kg.ultra_loader.get_minimal_mcq_data(attempt.mcq_id)
                if minimal_data and minimal_data.main_topic_index == node_index:
                    topic_attempts.append(attempt)
            else:
                # Fallback for regular loading
                mcq = kg.mcqs.get(attempt.mcq_id)
                if mcq and mcq.main_topic_index == node_index:
                    topic_attempts.append(attempt)
        
        return topic_attempts

    def get_topic_success_rate(self, node_index: int, kg) -> float:
        """Calculate success rate for a specific topic"""
        attempts = self.get_topic_attempts(node_index, kg)
        if not attempts:
            return 0.0

        correct_attempts = sum(1 for attempt in attempts if attempt.correct)
        return correct_attempts / len(attempts)

    def set_ability_level(self, ability_name: str, level: float):
        """Set ability level for a specific skill (between 0.0 and 1.0)"""
        if not 0.0 <= level <= 1.0:
            raise ValueError(f"Ability level must be between 0.0 and 1.0, got {level}")
        
        # Updated valid ability names to match your config structure
        valid_abilities = [
            'conceptual_understanding', 'procedural_fluency', 'problem_solving',
            'mathematical_communication', 'memory', 'spatial_reasoning'
        ]
        
        if ability_name not in valid_abilities:
            raise ValueError(f"Invalid ability name: {ability_name}. Valid names: {valid_abilities}")
        
        self.ability_levels[ability_name] = level

    def get_all_ability_levels(self) -> Dict[str, float]:
        """Get a copy of all ability levels"""
        return self.ability_levels.copy()

    def get_ability_summary(self) -> str:
        """Get a formatted summary of student abilities"""
        abilities = self.get_all_ability_levels()
        summary_lines = ["Student Ability Levels:"]
        for ability, level in abilities.items():
            formatted_name = ability.replace('_', ' ').title()
            percentage = level * 100
            summary_lines.append(f"  {formatted_name}: {percentage:.1f}%")
        return '\n'.join(summary_lines)


class StudentManager:
    """Manager class for handling multiple students
    Handles profile creation, session tracking, and statistics.
    """

    def __init__(self, config_manager=None):
        self.students: Dict[str, StudentProfile] = {}
        self.active_sessions: Dict[str, datetime] = {}
        self.config = config_manager
        self.bkt_system = None  # Reference to BKT system
    def get_mastery_threshold(self):
        """Get mastery threshold from config"""
        return self.config.get('algorithm_config.mastery_threshold', 0.7) if self.config else 0.7
    
    def get_confidence_params(self):
        """Get confidence calculation parameters"""
        if not self.config:
            return {'min_confidence': 0.1, 'max_confidence': 0.95, 'growth_rate': 0.02}
        
        return {
            'min_confidence': self.config.get('algorithm_config.min_confidence', 0.1),
            'max_confidence': self.config.get('algorithm_config.max_confidence', 0.95),
            'growth_rate': self.config.get('algorithm_config.confidence_growth_rate', 0.02),
            'question_weight': self.config.get('algorithm_config.confidence_question_weight', 0.3),
            'time_weight': self.config.get('algorithm_config.confidence_time_weight', 0.3),
            'consistency_weight': self.config.get('algorithm_config.confidence_consistency_weight', 0.2)
        }
    
    def create_student(self, student_id: str) -> StudentProfile:
        """Create a new student profile"""
        if student_id in self.students:
            raise ValueError(f"Student {student_id} already exists")

        student = StudentProfile(
            student_id=student_id,
            mastery_levels={},
            confidence_levels={},
            studied_topics={},
        ability_levels={
            'problem_solving': 0.5,
            'memory': 0.5,
            'notation': 0.5,
            'algebra': 0.5,
            'interconnectedness': 0.5
        },
            completed_questions=set(),
            daily_completed=set()
        )
        self.students[student_id] = student
        return student

    def get_student(self, student_id: str) -> Optional[StudentProfile]:
        """Get student profile by ID"""
        return self.students.get(student_id)

    def set_bkt_system(self, bkt_system):
        """Set reference to BKT system after initialization"""
        self.bkt_system = bkt_system

    def record_attempt(self, student_id: str, mcq_id: str, is_correct: bool,
                      time_taken: float, kg):
        """Attempt recording that triggers BKT updates"""
        student = self.get_student(student_id)
        if not student:
            return []

        # Record the attempt normally
        if hasattr(kg, 'ultra_loader'):
            # don't need full MCQ object for recording attempts, just verify the MCQ exists
            minimal_data = kg.ultra_loader.get_minimal_mcq_data(mcq_id)
            if not minimal_data:
                print(f"❌ MCQ {mcq_id} not found")
                return []
            mcq_exists = True
        else:
            # Fallback to original method
            mcq = kg.mcqs.get(mcq_id)
            mcq_exists = mcq is not None
        if mcq_exists:
            attempt = StudentAttempt(
                mcq_id=mcq_id,
                timestamp=datetime.now(),
                correct=is_correct,
                time_taken=time_taken,
            )

            student.attempt_history.append(attempt)
            student.completed_questions.add(mcq_id)
            student.daily_completed.add(mcq_id)
            student.total_questions_attempted += 1
            student.last_active = attempt.timestamp

            # Trigger BKT update if system is available
            if self.bkt_system:
                bkt_updates = self.bkt_system.process_mcq_with_area_effect(
                    student_id, mcq_id, is_correct)
                return bkt_updates

        return []
    def start_session(self, student_id: str):
        """Start a new session for a student"""
        student = self.get_student(student_id)
        if student:
            self.active_sessions[student_id] = datetime.now()
            student.session_count += 1

    def end_session(self, student_id: str):
        """End a session and update time tracking"""
        if student_id in self.active_sessions:
            student = self.get_student(student_id)
            if student:
                session_duration = (datetime.now() - self.active_sessions[student_id]).total_seconds() / 60.0
                student.total_time_on_system += session_duration
                student.last_active = datetime.now()
            del self.active_sessions[student_id]

    def reset_daily_progress(self, student_id: str):
        """Reset daily completed questions"""
        student = self.get_student(student_id)
        if student:
            student.daily_completed.clear()

    def get_student_statistics(self, student_id: str) -> Dict:
        """Get comprehensive statistics for a student"""
        student = self.get_student(student_id)
        if not student:
            return {}

        total_questions = len(student.attempt_history)
        if total_questions == 0:
            success_rate = 0.0
            avg_time = 0.0
        else:
            correct_attempts = sum(1 for attempt in student.attempt_history if attempt.correct)
            success_rate = correct_attempts / total_questions
            avg_time = sum(attempt.time_taken for attempt in student.attempt_history) / total_questions

        mastery_levels = list(student.mastery_levels.values())
        avg_mastery = sum(mastery_levels) / len(mastery_levels) if mastery_levels else 0.0

        return {
            'total_questions': total_questions,
            'success_rate': success_rate,
            'average_time': avg_time,
            'average_mastery': avg_mastery,
            'total_time_on_system': student.total_time_on_system,
            'session_count': student.session_count,
            'last_active': student.last_active,
            'registration_date': student.registration_date,
        }


    
class KnowledgeGraph:
    """
    Core knowledge structure representing relationships between learning topics.
    Uses a directed graph where edges represent prerequisite relationships.
    This class stores a lot of things
    """
    def __init__(self, nodes_file: str = 'small-graph-kg.json',
                 mcqs_file: str = 'small-graph-computed_mcqs.json',
                 config_file: str = 'config.json'):
        
        self.nodes = {}  # {index: Node}
        self.topic_to_index = {}  # Maps topic names to indexes: {topic_name: index} for quick lookup
        self.mcqs = {}
        self.graph = nx.DiGraph()
        self._next_index = 0  # Auto-incrementing index counter for making new topics 
        self._adjacency_matrix = None  # Cache the matrix
        self._matrix_dirty = False     # Track if matrix needs recalculation

        # Initialize nodes with the original data
        #self._initialize_nodes()
        self.config = ConfigurationManager(config_file)
        # Load static data from JSON files
        self._load_nodes_from_json(nodes_file)
        self._load_mcqs_from_json(mcqs_file)

        # Create NetworkX graph
        self._build_graph()
    
    def _load_nodes_from_json(self, nodes_file: str):
        """Load knowledge graph nodes from JSON file"""
        try:
            with open(nodes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Required nodes file '{nodes_file}' not found. Please ensure the knowledge graph JSON file exists.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in nodes file '{nodes_file}': {e}")
        
        # Validate JSON structure
        if 'nodes' not in data:
            raise ValueError(f"Invalid JSON structure in '{nodes_file}': missing 'nodes' key")
        
        # Clear existing nodes
        self.nodes.clear()
        
        # Load each node
        for node_data in data['nodes']:
            # Validate required fields
            required_fields = ['id', 'topic', 'chapter', 'dependencies']
            for field in required_fields:
                if field not in node_data:
                    raise ValueError(f"Missing required field '{field}' in node data: {node_data}")
            
            node_id = node_data['id']
            topic = node_data['topic']
            chapter = node_data['chapter']
            
            # Convert dependencies format
            dependencies = []
            for dep in node_data['dependencies']:
                if not isinstance(dep, list) or len(dep) != 2:
                    raise ValueError(f"Invalid dependency format in node {node_id}: expected [target, weight], got {dep}")
                target, weight = dep
                if not isinstance(target, int) or not isinstance(weight, (int, float)):
                    raise ValueError(f"Invalid dependency types in node {node_id}: target must be int, weight must be number")
                dependencies.append((target, weight))
            
            # Create and store node
            node = Node(topic, chapter, dependencies)
            self.nodes[node_id] = node
            
            # Update next index
            self._next_index = max(self._next_index, node_id + 1)
        
        print(f"✅ Successfully loaded {len(self.nodes)} nodes from {nodes_file}")

    def _load_mcqs_from_json(self, mcqs_file: str):
        """optimized loading for select_optimal_mcqs algorithm"""
        print(f"📥 Setting up optimized loading for {mcqs_file}...")
        self.ultra_loader = MCQLoader(mcqs_file)
        print(f"✅  optimized loader ready")
        
        # Show memory savings
        stats = self.ultra_loader.get_stats()
        print(f"   📊 {stats['total_indexed']} MCQs indexed with minimal data")

    def preload_for_student(self, student_id: str, student_manager) -> List[str]:
        """Preload minimal data for student's due topics"""
        if not hasattr(self, 'ultra_loader'):
            return []
        
        student = student_manager.get_student(student_id)
        if not student:
            return []
        
        # Get due topics
        due_topics = []
        mastery_threshold = getattr(self.config, 'mastery_threshold', 0.7)
        
        for topic_index, mastery in student.mastery_levels.items():
            if student.is_topic_studied(topic_index) and mastery < mastery_threshold:
                due_topics.append(topic_index)
        
         # Get MCQ IDs for due topics
        relevant_mcq_ids = self.ultra_loader.get_mcq_ids_for_due_topics(due_topics)

        print(f"👤 Preloaded minimal data for {len(relevant_mcq_ids)} MCQs across {len(due_topics)} due topics for student {student_id}")
        
        return relevant_mcq_ids

    def _build_graph(self):
        # Add nodes with their attributes
        for index, node in self.nodes.items():
            self.graph.add_node(index,
                              topic=node.topic,
                              chapter=node.chapter)

        # Add weighted edges based on dependencies
        for index, node in self.nodes.items():
            for dest, weight in node.dependencies:
                self.graph.add_edge(index, dest, weight=weight)


    def get_node_by_index(self, index: int) -> Optional[Node]:
        """Get node by index"""
        return self.nodes.get(index)

    def get_topic_of_index(self, index: int) -> Optional[str]:
        """Get the topic name of an index"""
        node = self.nodes.get(index)
        return node.topic if node else None

    def get_all_indexes(self) -> List[int]:
        """Get all node indexes in the graph"""
        return list(self.nodes.keys())

    def get_mcq_safely(self, mcq_id: str, need_full_text: bool = False):
        """
        Helper function to get MCQ data regardless of loading method
        Returns:
            For minimal data: MinimalMCQData object
            For full data: MCQ object
            None if not found
        """
        if hasattr(self, 'ultra_loader'):
            if need_full_text:
                return self.ultra_loader.get_full_mcq_if_needed(mcq_id)
            else:
                return self.ultra_loader.get_minimal_mcq_data(mcq_id)
        else:
            return self.mcqs.get(mcq_id)


    def get_node_degree(self, node_index: int) -> Dict[str, int]:
        """
        Get number of incoming/outgoing connections for a topic.
        Uses caching to avoid recalculation.
        """
        node = self.nodes.get(node_index)
        if not node:
            return {'in_degree': 0, 'out_degree': 0}

        # Check if cached values exist and graph hasn't changed
        if node._in_degree is None or self._matrix_dirty:
            node._in_degree = self.graph.in_degree(node_index)
            node._out_degree = self.graph.out_degree(node_index)

        return {
            'in_degree': node._in_degree,
            'out_degree': node._out_degree
        }


    def get_adjacency_matrix(self) -> np.ndarray:
        """ Cached adjacency matrix until graph changes"""
        if self._adjacency_matrix is None or self._matrix_dirty:
            self._adjacency_matrix = self._calculate_adjacency_matrix()
            self._matrix_dirty = False
        return self._adjacency_matrix

    def _calculate_adjacency_matrix(self) -> np.ndarray:
        """Private method to actually calculate the matrix"""
        if not self.nodes:
            return np.array([])

        max_index = max(self.nodes.keys())
        n = max_index + 1
        matrix = np.zeros((n, n), dtype=float)

        for source_index, node in self.nodes.items():
            for dest_index, weight in node.dependencies:
                if dest_index < n:
                    matrix[source_index, dest_index] = weight
        return matrix



@dataclass
class OptimizedMCQVector:
    """
    Vectorized representation of an MCQ with minimal datafor efficient algorithm processing.
    Caches computed values like prerequisites for performance
    """
    mcq_id: str
    minimal_data: MinimalMCQData  # Instead of full MCQ reference
    prerequisites: Dict[int, float]
    
    @property
    def subtopic_weights(self):
        return self.minimal_data.subtopic_weights
    
    @property
    def difficulty(self):
        return self.minimal_data.difficulty
    
    @property
    def main_topic_index(self):
        return self.minimal_data.main_topic_index
    
    @property
    def difficulty_breakdown(self) -> Dict[str, float]:
        """Return detailed breakdown if available, otherwise synthesize from overall"""
        if self.minimal_data.difficulty_breakdown:
            return self.minimal_data.difficulty_breakdown
        else:
            print('no difficuty breakdown')
            return []

class MCQScheduler:
    """the bit that does the actual mcq algorithm calculations
        Selects optimal questions for students based on:
        - Current mastery levels across topics
        - Prerequisites and dependencies 
        - Question difficulty and coverage
        - Learning objectives and priorities
    
    The greedy algorithm iteratively selects questions that maximize
    coverage-to-cost ratio until learning goals are met.
    """

    def __init__(self, knowledge_graph, student_manager, config_manager=None):
        self.kg = knowledge_graph
        self.student_manager = student_manager
        self.config = config_manager or knowledge_graph.config
        self.mcq_vectors = {}  # {mcq_id: MCQVector}
        self.bkt_system = None  # Will be set after BKT system is created

    def get_config_value(self, path: str, default=None):
        """Get configuration value using dot notation"""
        return self.config.get(path, default)
    
    def set_bkt_system(self, bkt_system):
        """Set reference to BKT system after initialization"""
        self.bkt_system = bkt_system
        # Also set the reference in student manager
        self.student_manager.bkt_system = bkt_system

 

    def _get_or_create_optimized_mcq_vector(self, mcq_id: str) -> Optional[OptimizedMCQVector]:
        """Get or create MCQ vector using minimal data"""
        if mcq_id in self.mcq_vectors:
            return self.mcq_vectors[mcq_id]
        
        if hasattr(self.kg, 'ultra_loader'):
            minimal_data = self.kg.ultra_loader.get_minimal_mcq_data(mcq_id)
            if minimal_data:

                
                # Create optimized vector
                vector = OptimizedMCQVector(
                    mcq_id=mcq_id,
                    minimal_data=minimal_data,
                    prerequisites=minimal_data.prerequisites
                )
                self.mcq_vectors[mcq_id] = vector
                return vector
            else:
                print(f"❌ No minimal data found for MCQ {mcq_id}")
                return None
    
        else:
            print(f"❌ ultra_loader not initialized")
            return None


    def get_available_questions_for_student(self, student_id: str) -> List[str]:
        """
         optimized eligibility check using minimal data
        """
        student = self.student_manager.get_student(student_id)
        if not student:
            return []
        
        if hasattr(self.kg, 'ultra_loader'):
            # Get due topics first
            due_topics = []
            mastery_threshold = getattr(self.config, 'mastery_threshold', 0.7)
            
            for topic_index, mastery in student.mastery_levels.items():
                if student.is_topic_studied(topic_index) and mastery < mastery_threshold:
                    due_topics.append(topic_index)
            
            if not due_topics:
                return []
            
            # Get MCQ IDs for due topics only
            eligible_mcqs = self.kg.ultra_loader.get_mcq_ids_for_due_topics(due_topics)
            
            # Filter out completed today
            eligible_mcqs = [mcq_id for mcq_id in eligible_mcqs if mcq_id not in student.daily_completed]
            
            print(f"🎯 Found {len(eligible_mcqs)} eligible MCQs for {len(due_topics)} due topics")
     
            
            return eligible_mcqs
        else:
            print("⚠️ No fallback method defined; returning empty list")
            return []


   


    def select_optimal_mcqs(self, student_id: str, num_questions: int = 1,
                          use_chapter_weights: bool = False) -> List[str]:
        """
        Main greedy algorithm for adaptive MCQ selection.
        Iteratively selects best question, updates virtual mastery, repeats.
        """
        # Get config values
        greedy_max_mcqs_to_evaluate = self.get_config_value('greedy_algorithm.greedy_max_mcqs_to_evaluate', 50)
        greedy_early_stopping = self.get_config_value('greedy_algorithm.greedy_early_stopping', False)
        greedy_convergence_threshold = self.get_config_value('algorithm_config.greedy_convergence_threshold', 0.05)
        
        # Get MCQs eligible for selection
        eligible_mcqs = self.get_available_questions_for_student(student_id)

        if not eligible_mcqs:
            print(f"No eligible MCQs found for greedy selection (no due main topics with all studied subtopics)")
            return []

        vectors_created = 0
        for mcq_id in eligible_mcqs:
            vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if vector:
                vectors_created += 1
            else:
                print(f"❌ Failed to create vector for MCQ {mcq_id}")
        
        print(f"✅ Created {vectors_created}/{len(eligible_mcqs)} MCQ vectors")
        
        if vectors_created == 0:
            print("❌ No MCQ vectors could be created - cannot run algorithm")
            return []
        
        student = self.student_manager.get_student(student_id)

        # Performance optimization: limit MCQs evaluated if too many
        if len(eligible_mcqs) > greedy_max_mcqs_to_evaluate:
            # Sort by a quick priority score and take top candidates
            quick_scores = [(mcq_id, self._calculate_quick_priority_score(mcq_id, student))
                          for mcq_id in eligible_mcqs]
            quick_scores.sort(key=lambda x: x[1], reverse=True)
            eligible_mcqs = [mcq_id for mcq_id, _ in quick_scores[:self.config.greedy_max_mcqs_to_evaluate]]

        # Create working copy of mastery levels for algorithm (not real mastery updates)
        simulated_mastery_levels = student.mastery_levels.copy()

        # Get prioritized topics (only those below mastery threshold)
        topic_priorities = self._calculate_topic_priorities_due_only(student, simulated_mastery_levels)

        if not topic_priorities:
            print(f"No due topics found for student {student_id}")
            return []

        selected_mcqs = []
        last_total_coverage = 0.0

        print(f"Initial due topics: {len(topic_priorities)} topics")
        print(f"Topic priorities range: {min(topic_priorities.values()):.3f} to {max(topic_priorities.values()):.3f}")
        print(f"Eligible MCQs with due main topics: {len(eligible_mcqs)}")

        # Greedy selection loop
        for iteration in range(num_questions):
            if not topic_priorities:
                print(f"All due topics covered after {iteration} questions")
                break

            # Calculate coverage-to-cost ratio for each available MCQ
            best_mcq = None
            best_ratio = 0.0
            best_coverage_info = None

            for mcq_id in eligible_mcqs:
                if mcq_id in selected_mcqs:  # Skip already selected
                    continue

            try:
                # Ensure vector exists before calculation
                vector = self._get_or_create_optimized_mcq_vector(mcq_id)
                if not vector:
                    print(f"   ⚠️  Skipping MCQ {mcq_id} - no vector available")
                    continue
                
                coverage_to_cost_ratio, coverage_info = self._calculate_coverage_to_cost_ratio(mcq_id, topic_priorities, simulated_mastery_levels, student)
                print(f"   📊 Ratio: {coverage_to_cost_ratio:.3f}")
                
                if coverage_to_cost_ratio > best_ratio:
                    best_ratio = coverage_to_cost_ratio
                    best_mcq = mcq_id
                    best_coverage_info = coverage_info
                    print(f"   ✅ New best MCQ: {mcq_id} (ratio: {best_ratio:.3f})")
                
            except Exception as e:
                print(f"   ❌ Error evaluating MCQ {mcq_id}: {type(e)} - {e}")
                import traceback
                traceback.print_exc()
                # Continue with next MCQ instead of crashing
                continue

            if best_mcq is None:
                print(f"No suitable MCQ found for remaining due topics in iteration {iteration + 1}")
                break

            # Select the best MCQ
            selected_mcqs.append(best_mcq)

            # Update virtual mastery and topic priorities
            try:
                # Update virtual mastery and topic priorities
                total_topic_coverage_score = self._update_simulated_mastery_and_priorities(best_mcq, simulated_mastery_levels, topic_priorities, best_coverage_info, student)
                
                print(f"✅ Updated virtual mastery- Coverage: {total_topic_coverage_score:.3f}, Remaining topics: {len(topic_priorities)}")
                
            except Exception as e:
                print(f"❌ Error updating virtual mastery: {type(e)} - {e}")
                import traceback
                traceback.print_exc()
                break

            #print(f"Selected Q{iteration + 1}: {self.kg.mcqs[best_mcq].text[:50]}...")
            print(f"  Coverage-to-cost ratio: {best_ratio:.3f}")
            print(f"  Total coverage gained: {total_topic_coverage_score:.3f}")
            print(f"  Remaining due topics: {len(topic_priorities)}")

            # Early stopping if improvement is minimal
            if (greedy_early_stopping and abs(total_topic_coverage_score - last_total_coverage) < greedy_convergence_threshold):
                print(f"Early stopping: minimal improvement detected")
                break

            last_total_coverage = total_topic_coverage_score

        return selected_mcqs


    def _calculate_quick_priority_score(self, mcq_id: str, student: StudentProfile) -> float:
        """Quick scoring for performance optimization when too many MCQs available
        This is a fast approximation. Full scoring uses _calculate_coverage_to_cost_ratio()"""
        mcq_vector = self.mcq_vectors.get(mcq_id)
        if not mcq_vector:
            return 0.0
        # Get greedy priority weight from config
        greedy_priority_weight = self.get_config_value('greedy_algorithm.greedy_priority_weight', 2.0)

        # Simple score based on average topic need
        total_need = 0.0
        for main_topic_index, weight in mcq_vector.subtopic_weights.items():
            mastery = student.get_mastery(main_topic_index)
            topic_need = (1.0 - mastery) ** greedy_priority_weight
            total_need += weight * topic_need

        return total_need

    def _calculate_topic_priorities_due_only(self, student: StudentProfile,
                                            simulated_mastery_levels: Dict[int, float]) -> Dict[int, float]:
        """
        Calculate continuous priority scores for topics below mastery threshold.
        Lower mastery = higher priority 
        """
        # Get config values
        mastery_threshold = self.get_config_value('algorithm_config.mastery_threshold', 0.7)
        greedy_priority_weight = self.get_config_value('greedy_algorithm.greedy_priority_weight', 2.0)
        
        topic_priorities = {}

        for main_topic_index in student.studied_topics:
            if student.is_topic_studied(main_topic_index):
                mastery = simulated_mastery_levels.get(main_topic_index, student.get_mastery(main_topic_index))

                #  Only include topics below mastery threshold
                if mastery < mastery_threshold:
                    # topics with lower mastery get higher priority
                    priority = (1.0 - mastery) * greedy_priority_weight
                    topic_priorities[main_topic_index] = priority

        return topic_priorities

    def _calculate_weighted_coverage(self, mcq_vector: OptimizedMCQVector,topic_priorities: Dict[int, float],simulated_mastery_levels: Dict[int, float]) -> Dict:
        """
        Calculate how well an MCQ covers priority topics.
        Returns coverage score and breakdown.
        """
        # Get config values
        greedy_subtopic_weight = self.get_config_value('greedy_algorithm.greedy_subtopic_weight', 0.7)
        greedy_prereq_weight = self.get_config_value('greedy_algorithm.greedy_prereq_weight', 0.5)
        
        total_topic_coverage_score = 0.0
        coverage_details = {'main_topic_coverage': 0.0,'subtopic_coverage': 0.0,'prereq_coverage': 0.0}

        # Main topic and subtopic coverage - for due topics
        for main_topic_index, mcq_weight in mcq_vector.subtopic_weights.items():
            if main_topic_index in topic_priorities: 
                topic_priority = topic_priorities[main_topic_index]

                # Coverage = MCQ weight × topic priority × type weight factor
                if main_topic_index == mcq_vector.main_topic_index:
                    coverage = mcq_weight * topic_priority
                    coverage_details['main_topic_coverage'] += coverage
                else:
                    coverage = mcq_weight * topic_priority * greedy_subtopic_weight
                    coverage_details['subtopic_coverage'] += coverage

                total_topic_coverage_score += coverage

        # Prerequisite coverage - for due prerequisites
        for prereq_index, prereq_weight in mcq_vector.prerequisites.items():
            if prereq_index in topic_priorities: 
                topic_priority = topic_priorities[prereq_index]
                coverage = prereq_weight * topic_priority * greedy_prereq_weight
                coverage_details['prereq_coverage'] += coverage
                total_topic_coverage_score += coverage

        coverage_details['total_topic_coverage_score'] = total_topic_coverage_score
        return coverage_details

    def _update_simulated_mastery_and_priorities(self, mcq_id: str,
                                            simulated_mastery_levels: Dict[int, float],
                                            topic_priorities: Dict[int, float],
                                            coverage_info: Dict,
                                            student: StudentProfile) -> float:
        """
        Simulate mastery updates from answering an MCQ correctly, by adding on question difficulty (probably will change eventually)
        Updates virtual mastery and recalculates priorities.
        """
        # Get config values
        mastery_threshold = self.get_config_value('algorithm_config.mastery_threshold', 0.7)
        greedy_mastery_update_rate = self.get_config_value('greedy_algorithm.greedy_mastery_update_rate', 0.8)
        greedy_priority_weight = self.get_config_value('greedy_algorithm.greedy_priority_weight', 2.0)
        
        mcq_vector = self.mcq_vectors.get(mcq_id)

        if not mcq_vector:
            return 0.0

        topics_to_remove = []
        total_topic_coverage_score = coverage_info['total_topic_coverage_score']

        # Update main topic and subtopics
        for main_topic_index, topic_weight in mcq_vector.subtopic_weights.items():
            if main_topic_index in topic_priorities:  # Only update due topics
                current_mastery = simulated_mastery_levels.get(main_topic_index, student.get_mastery(main_topic_index))

                # Mastery increase based on question difficulty and weight
                if main_topic_index == mcq_vector.main_topic_index:
                    # Main topic gets full difficulty boost
                    mastery_increase = mcq_vector.difficulty * greedy_mastery_update_rate
                else:
                    # Subtopics get weighted boost
                    mastery_increase = (mcq_vector.difficulty * topic_weight * greedy_mastery_update_rate)

                new_mastery = min(1.0, current_mastery + mastery_increase)
                simulated_mastery_levels[main_topic_index] = new_mastery

                # Remove topics that reach mastery threshold
                if new_mastery >= mastery_threshold:
                    topics_to_remove.append(main_topic_index)
                else:
                    # Recalculate priority for topics still below threshold
                    new_priority = (1.0 - new_mastery) ** greedy_priority_weight
                    topic_priorities[main_topic_index] = new_priority

        # Update prerequisites with reduced effect
        for prereq_index, prereq_weight in mcq_vector.prerequisites.items():
            if prereq_index in topic_priorities:  # Only update due prerequisites
                current_mastery = simulated_mastery_levels.get(prereq_index, student.get_mastery(prereq_index))

                # Prerequisites get smaller, weighted boost
                mastery_increase = (mcq_vector.difficulty * prereq_weight * greedy_mastery_update_rate * 0.5)

                new_mastery = min(1.0, current_mastery + mastery_increase)
                simulated_mastery_levels[prereq_index] = new_mastery

                # Remove prerequisites that reach mastery threshold
                if new_mastery >= mastery_threshold:
                    topics_to_remove.append(prereq_index)
                else:
                    # Recalculate priority for prerequisites still below threshold
                    new_priority = (1.0 - new_mastery) ** greedy_priority_weight
                    topic_priorities[prereq_index] = new_priority

        # Remove topics that are no longer due
        for main_topic_index in topics_to_remove:
            topic_priorities.pop(main_topic_index, None)


        return total_topic_coverage_score
    def _calculate_coverage_to_cost_ratio(self, mcq_id: str, topic_priorities: Dict[int, float],simulated_mastery_levels: Dict[int, float],student: StudentProfile) -> Tuple[float, Dict]:
        """
        Calculate coverage-to-cost ratio 
        Higher ratio = better choice (more benefit, less cost)
        Coverage is weighted by topic priorities and question weights.
        """
        if hasattr(self.kg, 'ultra_loader'):
            # For optimized loading, work with mcq_vector
            mcq_vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if not mcq_vector:
                return 0.0, {'total_topic_coverage_score': 0.0}
            # No need for full MCQ object in coverage calculation
            mcq = None  
        else:
            # Fallback to original method
            mcq = self.kg.mcqs.get(mcq_id)
            mcq_vector = self.mcq_vectors.get(mcq_id)
            if not mcq or not mcq_vector:
                return 0.0, {'total_topic_coverage_score': 0.0}

        # Calculate weighted coverage
        coverage_info = self._calculate_weighted_coverage( mcq_vector, topic_priorities, simulated_mastery_levels)

        if coverage_info['total_topic_coverage_score'] == 0:
            return 0.0, coverage_info

        # Calculate difficulty cost (penalty for poor match)
        difficulty_cost = self._calculate_difficulty_cost_enhanced(mcq_vector, simulated_mastery_levels, student)

        # Calculate importance bonus (reward for important topics)
        importance_bonus = self._calculate_importance_bonus_enhanced(mcq_vector, topic_priorities)

        # Total cost (lower is better)
        total_cost = max(0.01, difficulty_cost - importance_bonus)  # Prevent division by zero

        # Ratio: coverage/cost (higher is better)
        coverage_to_cost_ratio = coverage_info['total_topic_coverage_score'] / total_cost

        return coverage_to_cost_ratio, coverage_info
 


    def _calculate_difficulty_cost_enhanced(self, mcq_vector: OptimizedMCQVector,simulated_mastery_levels: Dict[int, float],student: StudentProfile) -> float:
        """
        Calculate cost based on difficulty mismatch.
        Questions too hard or too easy get penalized.
        """
        # Get penalty values from config
        greedy_difficulty_penalty = self.get_config_value('greedy_algorithm.greedy_difficulty_penalty', 1.5)
        greedy_too_easy_penalty = self.get_config_value('greedy_algorithm.greedy_too_easy_penalty', 1.5)
        
        # Calculate weighted student ability for this MCQ
        weighted_mastery = 0.0
        total_weight = 0.0

        for main_topic_index, weight in mcq_vector.subtopic_weights.items():
            mastery = simulated_mastery_levels.get(main_topic_index, student.get_mastery(main_topic_index))
            weighted_mastery += mastery * weight
            total_weight += weight

        if total_weight > 0:
            weighted_mastery /= total_weight

        # Base difficulty mismatch
        difficulty_diff = abs(mcq_vector.difficulty - weighted_mastery)

        # Apply configurable penalties
        if mcq_vector.difficulty < weighted_mastery:
            # Extra penalty for too-easy questions
            difficulty_cost = difficulty_diff * greedy_too_easy_penalty
        else:
            # penalty for difficulty mismatch
            difficulty_cost = difficulty_diff * greedy_difficulty_penalty

        return difficulty_cost

    def _calculate_importance_bonus_enhanced(self, mcq_vector: OptimizedMCQVector,topic_priorities: Dict[int, float]) -> float:
        """
        Calculate bonus for covering important topics.
        Topics with many dependencies are more important.
        """
        # Get importance weight from config
        greedy_importance_weight = self.get_config_value('greedy_algorithm.greedy_importance_weight', 0.3)
        
        importance_bonus = 0.0

        # Check importance of all topics in the MCQ
        for main_topic_index, mcq_weight in mcq_vector.subtopic_weights.items():
            if main_topic_index in topic_priorities:
                # Node degree importance from graph
                node_degree_info = self.kg.get_node_degree(main_topic_index)
                out_degree = node_degree_info.get('out_degree', 0)

                # Weighted importance bonus
                topic_importance = out_degree * mcq_weight * greedy_importance_weight
                importance_bonus += topic_importance

        return importance_bonus
    

@dataclass
class FSRSMemoryComponents:
    """FSRS-inspired memory components for modeling different types of forgetting"""
    stability: float = 1.0
    difficulty: float = 0.5
    retrievability: float = 1.0
    last_review: Optional[datetime] = None
    review_count: int = 0
    recent_success_rate: float = 0.5


#i think i put this in the config, will check

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



class BayesianKnowledgeTracing:
    """
    Enhanced Bayesian Knowledge Tracing with FSRS forgetting
    """
    
    def __init__(self, knowledge_graph, student_manager, config_manager=None, scheduler=None):
        """
        Initialize BKT with knowledge graph and student manager
        """
        self.kg = knowledge_graph
        self.student_manager = student_manager
        self.config = config_manager or knowledge_graph.config
        self.scheduler = scheduler

        # Use config manager to get BKT parameters instead of hardcoded defaults
        self.default_params = self._get_default_params_from_config()
        
        # Topic-specific parameters (loaded from config)
        self.topic_parameters: Dict[int, Dict] = {}
        self._initialize_topic_parameters()
        
        # Initialize FSRS forgetting model if enabled
        if self.config.get('bkt_config.enable_fsrs_forgetting', True):
            fsrs_config = self._create_fsrs_config_from_config()
            self.fsrs_forgetting = FSRSForgettingModel(fsrs_config)
        else:
            self.fsrs_forgetting = None

    def _get_default_params_from_config(self) -> Dict:
        """Get default BKT parameters from config manager"""
        return self.config.get('bkt_parameters.default', {
            'prior_knowledge': 0.1,
            'learning_rate': 0.3,
            'slip_rate': 0.03,
            'guess_rate': 0.1
        })

    def _create_fsrs_config_from_config(self) -> FSRSForgettingConfig:
        """Create FSRS config from the main config manager"""
        return FSRSForgettingConfig(
            stability_power_factor=self.config.get('bkt_config.fsrs_stability_power', -0.5),
            difficulty_power_factor=self.config.get('bkt_config.fsrs_difficulty_power', 0.3),
            retrievability_power_factor=self.config.get('bkt_config.fsrs_retrievability_power', -0.8),
            stability_weight=self.config.get('bkt_config.fsrs_stability_weight', 0.4),
            difficulty_weight=self.config.get('bkt_config.fsrs_difficulty_weight', 0.3),
            retrievability_weight=self.config.get('bkt_config.fsrs_retrievability_weight', 0.3),
            success_stability_boost=self.config.get('bkt_config.fsrs_success_stability_boost', 1.2),
            failure_stability_penalty=self.config.get('bkt_config.fsrs_failure_stability_penalty', 0.8),
            difficulty_adaptation_rate=self.config.get('bkt_config.fsrs_difficulty_adaptation_rate', 0.1),
            base_forgetting_time=self.config.get('bkt_config.fsrs_base_forgetting_time', 1.0),
            max_stability=self.config.get('bkt_config.fsrs_max_stability', 365.0),
            min_stability=self.config.get('bkt_config.fsrs_min_stability', 0.1),
            retrievability_threshold=self.config.get('bkt_config.fsrs_retrievability_threshold', 0.9),
            min_retrievability=self.config.get('bkt_config.fsrs_min_retrievability', 0.1)
        )

    def _initialize_topic_parameters(self):
        """Initialize BKT parameters for all topics from config"""
        for node_index in self.kg.get_all_indexes():
            self.topic_parameters[node_index] = self.get_topic_parameters(node_index)

    def get_topic_parameters(self, topic_index: int) -> Dict:
        """Get BKT parameters for a topic using config manager (matches original signature)"""
        # Try to get topic-specific parameters first
        topic_params = self.config.get_bkt_parameters(topic_index)
        
        if topic_params:
            return topic_params
        else:
            # Fall back to default parameters
            return self.default_params

    def is_area_effect_enabled(self):
        """Check if area effect is enabled"""
        return self.config.get('bkt_config.area_effect_enabled', True)
    
    def get_area_effect_config(self):
        """Get area effect configuration"""
        return {
            'max_distance': self.config.get('bkt_config.area_effect_max_distance', 2),
            'decay_rate': self.config.get('bkt_config.area_effect_decay_rate', 0.6),
            'min_effect': self.config.get('bkt_config.area_effect_min_effect', 0.01)
        }

    def initialize_student_mastery(self, student_id: str, topic_index: int = None):
        """Initialize student's mastery level for a topic or all topics using P(L_0)"""
        student = self.student_manager.get_student(student_id)
        if not student:
            return

        if topic_index is not None:
            # Initialize specific topic
            params = self.get_topic_parameters(topic_index)
            student.mastery_levels[topic_index] = params['prior_knowledge']
        else:
            # Initialize all topics
            for node_index in self.kg.get_all_indexes():
                if node_index not in student.mastery_levels:
                    params = self.get_topic_parameters(node_index)
                    student.mastery_levels[node_index] = params['prior_knowledge']

    def calculate_conditional_probability(self, current_mastery: float, is_correct: bool, params: Dict) -> float:
        """Calculate P(L_t | Result) using Bayes' theorem"""
        if is_correct:
            numerator = current_mastery * (1 - params['slip_rate'])
            denominator = (current_mastery * (1 - params['slip_rate']) +
                          (1 - current_mastery) * params['guess_rate'])
        else:
            numerator = current_mastery * params['slip_rate']
            denominator = (current_mastery * params['slip_rate'] +
                          (1 - current_mastery) * (1 - params['guess_rate']))

        if denominator == 0:
            return current_mastery
        return numerator / denominator

    def update_mastery(self, conditional_prob: float, params: Dict) -> float:
        """Update mastery using learning rate: P(L_{t+1}) = P(L_t|Result) + (1-P(L_t|Result))P(T)"""
        return conditional_prob + (1 - conditional_prob) * params['learning_rate']

    def predict_correctness(self, mastery: float, params: Dict) -> float:
        """Predict probability of correct answer: P(Correct) = P(L_t)(1-P(S)) + (1-P(L_t))P(G)"""
        return mastery * (1 - params['slip_rate']) + (1 - mastery) * params['guess_rate']

    def process_student_response(self, student_id: str, topic_index: int,
                                is_correct: bool, mcq_id: str = None,
                                custom_params: Optional[Dict] = None) -> Dict:
        """
        Process a student's response and update their mastery using BKT
        FSRS forgetting applied automatically
        """
        student = self.student_manager.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Use provided custom parameters or default for topic
        params = custom_params if custom_params else self.get_topic_parameters(topic_index)

        # Get current mastery level
        current_mastery = student.get_mastery(topic_index)
        mastery_before_forgetting = current_mastery

        # If this is the first time seeing this topic, initialize with prior
        if topic_index not in student.mastery_levels:
            current_mastery = params['prior_knowledge']
            student.mastery_levels[topic_index] = current_mastery
            mastery_before_forgetting = current_mastery

        # Apply FSRS forgetting if enabled
        if self.config.get('bkt_config.enable_fsrs_forgetting', True) and self.fsrs_forgetting:
            forgotten_mastery = self.fsrs_forgetting.apply_forgetting(
                student_id, topic_index, current_mastery)
            student.mastery_levels[topic_index] = forgotten_mastery
            current_mastery = forgotten_mastery
        else:
            forgotten_mastery = current_mastery

        # Calculate prediction before update (for validation)
        prediction_before = self.predict_correctness(current_mastery, params)

        # Apply BKT update
        conditional_prob = self.calculate_conditional_probability(current_mastery, is_correct, params)
        new_mastery = self.update_mastery(conditional_prob, params)

        # Update student's mastery level
        student.mastery_levels[topic_index] = new_mastery

        # Update FSRS memory components after BKT update
        if self.config.get('bkt_config.enable_fsrs_forgetting', True) and self.fsrs_forgetting:
            self.fsrs_forgetting.update_memory_components(
                student_id, topic_index, is_correct, new_mastery)

        # Calculate new prediction
        prediction_after = self.predict_correctness(new_mastery, params)

        # Return detailed information about the update (enhanced with FSRS info)
        result = {
            'student_id': student_id,
            'main_topic_index': topic_index,
            'topic_name': self.kg.get_topic_of_index(topic_index),
            'mcq_id': mcq_id,
            'is_correct': is_correct,
            'mastery_before': mastery_before_forgetting,
            'mastery_after': new_mastery,
            'mastery_change': new_mastery - current_mastery,
            'conditional_probability': conditional_prob,
            'prediction_before': prediction_before,
            'prediction_after': prediction_after,
            'parameters_used': params.copy()
        }

        # Add FSRS information if enabled
        if self.config.get('bkt_config.enable_fsrs_forgetting', True) and self.fsrs_forgetting:
            components = self.fsrs_forgetting.get_memory_components(student_id, topic_index)
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
        if hasattr(self.kg, 'ultra_loader'):
            # For  optimized loading, get minimal data
            minimal_data = self.kg.ultra_loader.get_minimal_mcq_data(mcq_id)
            if not minimal_data:
                raise ValueError(f"MCQ {mcq_id} not found")
            
            # Use minimal data attributes
            subtopic_weights = minimal_data.subtopic_weights
            main_topic_index = minimal_data.main_topic_index
        else:
            # For regular loading, get full MCQ
            mcq = self.kg.mcqs.get(mcq_id)
            if not mcq:
                raise ValueError(f"MCQ {mcq_id} not found")
            
            # Use full MCQ attributes
            subtopic_weights = mcq.subtopic_weights
            main_topic_index = mcq.main_topic_index

        updates = []

        # Use the MCQ's explicit topic weights directly 
        for topic_index, weight in subtopic_weights.items():
            # Get base parameters for this topic
            base_params = self.get_topic_parameters(topic_index)

            # Create adjusted parameters with scaled learning rate
            adjusted_params = {
                'prior_knowledge': base_params['prior_knowledge'],
                'learning_rate': base_params['learning_rate'] * weight,  # Scale by weight
                'slip_rate': base_params['slip_rate'],
                'guess_rate': base_params['guess_rate']
            }

            # Process with enhanced method (includes FSRS forgetting)
            update = self.process_student_response(
                student_id, topic_index, is_correct, mcq_id, custom_params=adjusted_params)
            
            update['topic_weight'] = weight
            update['is_primary_topic'] = (topic_index == main_topic_index)

            updates.append(update)

        return updates

    def apply_area_of_effect(self, student_id: str, center_topic_index: int, mastery_change: float) -> List[Dict]:
        """
        Area of effect that uses actual path weights between topics.
        """
        if not self.is_area_effect_enabled() or mastery_change <= 0:
            return []
        
        # Get area effect configuration
        area_config = self.get_area_effect_config()
        max_distance = area_config['max_distance']
        decay_rate = area_config['decay_rate']
        min_effect = area_config['min_effect']

        student = self.student_manager.get_student(student_id)
        if not student:
            return []

        # Use NetworkX to find all shortest paths within distance
        undirected_graph = self.kg.graph.to_undirected()

        try:
            # Get all shortest paths to nodes within max_distance
            paths = nx.single_source_shortest_path(undirected_graph, center_topic_index, cutoff=max_distance)
        except Exception:  # Catch any NetworkX errors
            return []

        # Remove center node (path to itself)
        paths.pop(center_topic_index, None)

        updates = []

        for topic_index, path in paths.items():
            distance = len(path) - 1  # Number of edges in path

            # Calculate path weight by multiplying all edge weights along the path
            path_weight = self._calculate_path_weight(path)

            # Calculate effect: decay^distance * mastery_change * path_weight
            base_effect = mastery_change * (decay_rate ** distance)
            final_effect = base_effect * path_weight

            # Only apply significant effects
            if final_effect > min_effect:
                current_mastery = student.get_mastery(topic_index)
                new_mastery = min(1.0, current_mastery + final_effect)

                # Update student mastery
                student.mastery_levels[topic_index] = new_mastery

                # Record the update
                updates.append({
                    'main_topic_index': topic_index,
                    'topic_name': self.kg.get_topic_of_index(topic_index),
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
        """Calculate the combined weight along a path by multiplying edge weights."""
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

    def process_mcq_with_area_effect(self, student_id: str, mcq_id: str, is_correct: bool) -> List[Dict]:
        """
        Simplified MCQ processing with area effects.
        Replaces the longer process_mcq_response_with_area_effect method.
        """
        try:
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
    
        except Exception as e:
            print(f"❌ Error in BKT processing: {type(e)} - {e}")
            import traceback
            traceback.print_exc()
            return []


    def calibrate_parameters(self, student_id: str, topic_index: int,
                           attempt_history: List[Tuple[bool, datetime]]) -> Dict:
        """
        Simple parameter calibration based on student's attempt history
        """
        if not attempt_history:
            return self.get_topic_parameters(topic_index)

        # Calculate basic statistics
        total_attempts = len(attempt_history)
        correct_attempts = sum(1 for is_correct, _ in attempt_history if is_correct)
        success_rate = correct_attempts / total_attempts

        # Simple heuristic calibration
        current_params = self.get_topic_parameters(topic_index)

        # Adjust guess rate based on early performance
        early_attempts = attempt_history[:min(3, total_attempts)]
        early_success = sum(1 for is_correct, _ in early_attempts if is_correct)
        early_rate = early_success / len(early_attempts)

        # If student does well early, they might have higher prior knowledge
        adjusted_prior = min(0.8, current_params['prior_knowledge'] + early_rate * 0.3)

        # If overall success rate is very high, reduce slip rate
        adjusted_slip = max(0.01, current_params['slip_rate'] - (success_rate - 0.7) * 0.1)

        # If success rate is low but attempts are many, increase learning rate
        adjusted_learning = min(0.8, current_params['learning_rate'] +
                              (0.1 if success_rate < 0.5 and total_attempts > 5 else 0))

        return {
            'prior_knowledge': adjusted_prior,
            'learning_rate': adjusted_learning,
            'slip_rate': max(0.01, min(0.3, adjusted_slip)),
            'guess_rate': current_params['guess_rate']
        }

    # NEW METHODS FOR FSRS FUNCTIONALITY
    def get_current_mastery_with_decay(self, student_id: str, topic_index: int) -> float:
        """Get current mastery level with forgetting applied, without updating stored values"""
        student = self.student_manager.get_student(student_id)
        if not student:
            return 0.0

        stored_mastery = student.get_mastery(topic_index)

        if self.config.get('bkt_config.enable_fsrs_forgetting', True) and self.fsrs_forgetting:
            return self.fsrs_forgetting.apply_forgetting(student_id, topic_index, stored_mastery)
        else:
            return stored_mastery

    def get_review_recommendations(self, student_id: str, 
                                 target_retention: float = 0.9) -> List[Dict]:
        """Get review recommendations based on FSRS forgetting predictions"""
        if not self.config.get('bkt_config.enable_fsrs_forgetting', True) or not self.fsrs_forgetting:
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
        if not self.config.get('bkt_config.enable_fsrs_forgetting', True) or not self.fsrs_forgetting:
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
    
##############  FSRS TIME TESTING   ##################

from datetime import datetime, timedelta
import math

class TimeManipulator:
    """
    Time manipulation utility for testing FSRS forgetting curves
    Allows simulating the passage of time without actually waiting
    """
    
    def __init__(self):
        self._time_offset = timedelta(0)  # How much time we've "fast-forwarded"
        self._original_now = datetime.now  # Store original datetime.now function
        
    def get_current_time(self) -> datetime:
        """Get the current "simulated" time"""
        return self._original_now() + self._time_offset
    
    def fast_forward(self, days: int = 0, hours: int = 0, minutes: int = 0) -> datetime:
        """
        Fast forward time by the specified amount
        
        Args:
            days: Number of days to advance
            hours: Number of hours to advance  
            minutes: Number of minutes to advance
            
        Returns:
            New current time after fast forwarding
        """
        time_delta = timedelta(days=days, hours=hours, minutes=minutes)
        self._time_offset += time_delta
        new_time = self.get_current_time()
        
        print(f"⏰ Time fast-forwarded by {days} days, {hours} hours, {minutes} minutes")
        print(f"📅 Current simulated time: {new_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return new_time
    
    def reset_time(self) -> datetime:
        """Reset time manipulation back to real time"""
        self._time_offset = timedelta(0)
        real_time = self._original_now()
        print(f"🔄 Time reset to real time: {real_time.strftime('%Y-%m-%d %H:%M:%S')}")
        return real_time
    
    def get_time_offset(self) -> timedelta:
        """Get current time offset"""
        return self._time_offset
    
    def get_time_info(self) -> dict:
        """Get time manipulation info for display"""
        real_time = self._original_now()
        sim_time = self.get_current_time()
        
        return {
            'real_time': real_time.strftime('%Y-%m-%d %H:%M:%S'),
            'simulated_time': sim_time.strftime('%Y-%m-%d %H:%M:%S'),
            'offset_days': self._time_offset.days,
            'offset_hours': self._time_offset.seconds // 3600,
            'offset_minutes': (self._time_offset.seconds % 3600) // 60,
            'time_manipulation_active': self._time_offset != timedelta(0)
        }

# Global time manipulator instance
time_manipulator = TimeManipulator()

# Monkey patch the FSRSForgettingModel to use simulated time
def patch_fsrs_for_time_manipulation():
    """Patch the existing FSRSForgettingModel to use simulated time"""
    
    # Store original methods
    original_get_memory_components = FSRSForgettingModel.get_memory_components
    original_apply_forgetting = FSRSForgettingModel.apply_forgetting
    original_update_memory_components = FSRSForgettingModel.update_memory_components
    
    def patched_get_memory_components(self, student_id: str, topic_index: int) -> FSRSMemoryComponents:
        """Patched version that uses simulated time for initialization"""
        if student_id not in self.memory_components:
            self.memory_components[student_id] = {}
        
        if topic_index not in self.memory_components[student_id]:
            # Initialize with simulated time
            self.memory_components[student_id][topic_index] = FSRSMemoryComponents(
                stability=1.0,
                difficulty=0.5,
                retrievability=1.0,
                last_review=time_manipulator.get_current_time(),  # Use simulated time
                review_count=0,
                recent_success_rate=0.5
            )
        
        return self.memory_components[student_id][topic_index]
    
    def patched_apply_forgetting(self, student_id: str, topic_index: int, current_mastery: float) -> float:
        """Patched version that uses simulated time for forgetting calculations"""
        components = self.get_memory_components(student_id, topic_index)
        
        if components.last_review is None:
            components.last_review = time_manipulator.get_current_time()
            return current_mastery
        
        # Calculate time since last review using simulated time
        current_time = time_manipulator.get_current_time()
        time_elapsed = (current_time - components.last_review).total_seconds() / (24 * 3600)
        
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
        
        # Update last access time using simulated time
        components.last_review = current_time
        
        return forgotten_mastery
    
    def patched_update_memory_components(self, student_id: str, topic_index: int, 
                                       is_correct: bool, new_mastery: float):
        """Patched version that uses simulated time for updates"""
        components = self.get_memory_components(student_id, topic_index)
        
        # Update review count
        components.review_count += 1
        
        # Update last review time to simulated time
        components.last_review = time_manipulator.get_current_time()
        
        # Update success rate with exponential moving average
        alpha = 0.3
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
    
    # Apply the patches
    FSRSForgettingModel.get_memory_components = patched_get_memory_components
    FSRSForgettingModel.apply_forgetting = patched_apply_forgetting
    FSRSForgettingModel.update_memory_components = patched_update_memory_components

# Apply the patches when this module is imported
patch_fsrs_for_time_manipulation()

# Utility functions for testing
def simulate_time_passage(bkt_system, student_id: str, days: int = 0, hours: int = 0, minutes: int = 0) -> dict:
    """
    Fast-forward time and apply forgetting to student's mastery levels
    
    Args:
        bkt_system: The BayesianKnowledgeTracing instance
        student_id: Student identifier
        days: Days to fast forward
        hours: Hours to fast forward
        minutes: Minutes to fast forward
        
    Returns:
        Dictionary with before/after mastery levels and decay statistics
    """
    if not bkt_system.config.get('bkt_config.enable_fsrs_forgetting', True) or not bkt_system.fsrs_forgetting:
        return {'error': 'FSRS forgetting not enabled'}
    
    student = bkt_system.student_manager.get_student(student_id)
    if not student:
        return {'error': 'Student not found'}
    
    # Store mastery levels before time passage
    mastery_before = student.mastery_levels.copy()
    
    # Fast forward time
    new_time = time_manipulator.fast_forward(days=days, hours=hours, minutes=minutes)
    
    # Apply forgetting to all topics
    decay_results = []
    total_decay = 0
    topics_affected = 0
    
    for topic_index, original_mastery in mastery_before.items():
        if original_mastery > 0.05:  # Only apply forgetting to topics with some mastery
            # Apply forgetting and update student's mastery
            new_mastery = bkt_system.fsrs_forgetting.apply_forgetting(student_id, topic_index, original_mastery)
            student.mastery_levels[topic_index] = new_mastery
            
            decay_amount = original_mastery - new_mastery
            if decay_amount > 0.001:  # Only track significant decay
                decay_results.append({
                    'topic_index': topic_index,
                    'topic_name': bkt_system.kg.get_topic_of_index(topic_index),
                    'mastery_before': original_mastery,
                    'mastery_after': new_mastery,
                    'decay_amount': decay_amount,
                    'decay_percentage': (decay_amount / original_mastery) * 100
                })
                total_decay += decay_amount
                topics_affected += 1
    
    # Sort by decay amount
    decay_results.sort(key=lambda x: x['decay_amount'], reverse=True)
    
    return {
        'time_advanced': {
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'new_current_time': new_time.strftime('%Y-%m-%d %H:%M:%S')
        },
        'decay_summary': {
            'total_decay': total_decay,
            'topics_affected': topics_affected,
            'average_decay': total_decay / topics_affected if topics_affected > 0 else 0
        },
        'topic_changes': decay_results
    }

def preview_mastery_decay(bkt_system, student_id: str, days_ahead: int = 30) -> dict:
    """
    Preview how mastery levels will decay over time without actually fast-forwarding
    
    Args:
        bkt_system: The BayesianKnowledgeTracing instance
        student_id: Student identifier
        days_ahead: How many days ahead to simulate
        
    Returns:
        Dictionary with current mastery, predicted mastery, and decay info
    """
    if not bkt_system.config.get('bkt_config.enable_fsrs_forgetting', True) or not bkt_system.fsrs_forgetting:
        return {'error': 'FSRS forgetting not enabled'}
    
    student = bkt_system.student_manager.get_student(student_id)
    if not student:
        return {'error': 'Student not found'}
    
    # Store original time offset
    original_offset = time_manipulator.get_time_offset()
    
    # Simulate time passage
    time_manipulator.fast_forward(days=days_ahead)
    
    decay_preview = {
        'days_simulated': days_ahead,
        'topics': []
    }
    
    for topic_index, current_mastery in student.mastery_levels.items():
        if current_mastery > 0.05:  # Only preview topics with some mastery
            # Calculate predicted mastery after time passage
            predicted_mastery = bkt_system.fsrs_forgetting.apply_forgetting(
                student_id, topic_index, current_mastery)
            
            decay_amount = current_mastery - predicted_mastery
            decay_percentage = (decay_amount / current_mastery) * 100 if current_mastery > 0 else 0
            
            # Get memory components for additional info
            components = bkt_system.fsrs_forgetting.get_memory_components(student_id, topic_index)
            
            decay_preview['topics'].append({
                'topic_index': topic_index,
                'topic_name': bkt_system.kg.get_topic_of_index(topic_index),
                'current_mastery': current_mastery,
                'predicted_mastery': predicted_mastery,
                'decay_amount': decay_amount,
                'decay_percentage': decay_percentage,
                'stability': components.stability,
                'difficulty': components.difficulty,
                'retrievability': components.retrievability
            })
    
    # Restore original time offset
    time_manipulator._time_offset = original_offset
    
    # Sort by decay amount (most decay first)
    decay_preview['topics'].sort(key=lambda x: x['decay_amount'], reverse=True)
    
    return decay_preview

def reset_time_to_real() -> dict:
    """Reset time manipulation back to real time"""
    old_offset = time_manipulator.get_time_offset()
    real_time = time_manipulator.reset_time()
    
    return {
        'time_offset_was': str(old_offset),
        'real_time_now': real_time.strftime('%Y-%m-%d %H:%M:%S'),
        'reset_successful': True
    }

def get_time_status() -> dict:
    """Get current time manipulation status"""
    return time_manipulator.get_time_info()

################################


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

def refresh_student_mastery(bkt_system, student_id: str):
    """
    Simple function to refresh one student's mastery with current decay
    """
    student = bkt_system.student_manager.get_student(student_id)
    if not student or not bkt_system.fsrs_forgetting:
        return
    
    print(f"🔄 Refreshing mastery for {student_id}...")
    
    updates = []
    for topic_index, stored_mastery in list(student.mastery_levels.items()):
        if stored_mastery > 0.05:
            decayed_mastery = bkt_system.fsrs_forgetting.apply_forgetting(
                student_id, topic_index, stored_mastery)
            
            decay_amount = stored_mastery - decayed_mastery
            if decay_amount > 0.001:
                student.mastery_levels[topic_index] = decayed_mastery
                topic_name = bkt_system.kg.get_topic_of_index(topic_index)
                updates.append(f"   {topic_name}: {stored_mastery:.3f} → {decayed_mastery:.3f} (-{decay_amount:.3f})")
    
    if updates:
        print(f"📉 Applied decay to {len(updates)} topics:")
        for update in updates[:5]:  # Show first 5
            print(update)
        if len(updates) > 5:
            print(f"   ... and {len(updates)-5} more")
    else:
        print("   No significant decay to apply")
    
    student._last_decay_update = time_manipulator.get_current_time()
