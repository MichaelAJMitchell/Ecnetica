import numpy as np
import uuid
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
import random
import json

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
    _prerequisites: Optional[Dict[int, float]] = field(default=None, init=False)  # Cached prerequisites
    _difficulty: Optional[float] = field(default=None, init=False)

    def get_prerequisites(self, kg) -> Dict[int, float]:
        """Cache prerequisite calculation"""
        if self._prerequisites is None:
            self._prerequisites = self._calculate_prerequisites(kg)
        return self._prerequisites



    @classmethod
    def from_dict(cls, data: Dict):
        """Create MCQ from JSON dictionary"""
        # Validate core required fields
        required_fields = ['text', 'options', 'correctindex', 'option_explanations',
                          'main_topic_index', 'subtopic_weights']

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field '{field}' in MCQ data")

        mcq_id = data.get('id')

        # Validate options and explanations match
        if len(data['options']) != len(data['option_explanations']):
            raise ValueError("Number of options must match number of option explanations")

        # Validate correct index
        if not (0 <= data['correctindex'] < len(data['options'])):
            raise ValueError(f"correctindex {data['correctindex']} is out of range for {len(data['options'])} options")

        # Convert string keys in subtopic_weights to integers
        try:
            subtopic_weights = {int(k): v for k, v in data['subtopic_weights'].items()}
        except ValueError as e:
            raise ValueError(f"Invalid subtopic_weights format - keys must be convertible to integers: {e}")

        # Validate subtopic weights sum to 1.0 (with tolerance)
        weight_sum = sum(subtopic_weights.values())
        if abs(weight_sum - 1.0) > 0.001:
            raise ValueError(f"Subtopic weights must sum to 1.0, got {weight_sum}")

        # Handle chapter - use provided or default
        chapter = data.get('chapter', 'unknown')

        difficulty_breakdown = DifficultyBreakdown.from_dict(data['difficulty_breakdown'])


        return cls(
            text=data['text'],
            options=data['options'],
            correctindex=data['correctindex'],
            option_explanations=data['option_explanations'],
            main_topic_index=data['main_topic_index'],
            chapter=chapter,
            subtopic_weights=subtopic_weights,
            difficulty_breakdown=difficulty_breakdown,
            id=mcq_id  # Use generated or provided ID
        )

    def _calculate_prerequisites(self, kg) -> Dict[int, float]:
        """
        Get all prerequisite topics needed to attempt this question.
        Uses graph traversal to find dependencies of tested topics.
        """
        adjacency_matrix = kg.get_adjacency_matrix()
        prerequisites = {}

        if adjacency_matrix.size > 0:
            for topic_index, topic_weight in self.explicit_topic_weights.items():
                if topic_index < adjacency_matrix.shape[0]:
                    topic_prereqs = adjacency_matrix[topic_index, :]
                    for prereq_index, prereq_strength in enumerate(topic_prereqs):
                        if prereq_strength > 0:
                            weighted_prereq = prereq_strength * topic_weight
                            if prereq_index in prerequisites:
                                prerequisites[prereq_index] = max(prerequisites[prereq_index], weighted_prereq)
                            else:
                                prerequisites[prereq_index] = weighted_prereq
        return prerequisites

    @property
    def difficulty(self) -> float:
        """Cache difficulty calculation"""
        if self._difficulty is None:
            self._difficulty = self.difficulty_breakdown.calculate_overall()
        return self._difficulty


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
            with open(self.config_file, 'r') as f:
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
        """Get all attempts for a specific topic"""
        topic_name = kg.get_topic_of_index(node_index)
        if not topic_name:
            return []

        return [attempt for attempt in self.attempt_history
                if kg.mcqs.get(attempt.mcq_id) and
                kg.mcqs[attempt.mcq_id].main_topic_index == node_index]

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
        mcq = kg.mcqs.get(mcq_id)
        if mcq:
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
    """
    def __init__(self, nodes_file: str = 'kg.json',
                 mcqs_file: str = 'computed_mcqs.json',
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
        self._build_graph()

        # Create NetworkX graph
        self._build_graph()

    def _load_nodes_from_json(self, nodes_file: str):
        """Load knowledge graph nodes from JSON file"""
        try:
            with open(nodes_file, 'r') as f:
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
                if 'target' not in dep or 'weight' not in dep:
                    raise ValueError(f"Invalid dependency format in node {node_id}: {dep}")
                dependencies.append((dep['target'], dep['weight']))

            # Create and store node
            node = Node(topic, chapter, dependencies)
            self.nodes[node_id] = node

            # Update next index
            self._next_index = max(self._next_index, node_id + 1)

        print(f"✅ Successfully loaded {len(self.nodes)} nodes from {nodes_file}")

    def _initialize_nodes(self):
        # nodes with (topic, chapter, dependencies[destination node, weight])
        node_data = [
            ('solving linear equations', 'algebra', [(6,0.5), (14,0.8), (15,0.6)]),
            ('linear equations in standard form', 'algebra', [(0,0.3), (2,0.4)]),
            ('form of quadratic equations', 'algebra', [(5,0.9), (6,0.7), (9,0.6), (10,0.8), (12,0.6), (14,0.7), (15,0.8), (17,0.6)]),
            ('expanding brackets', 'algebra', [(0,0.7), (9,0.8), (14,0.2)]),
            ('substitution', 'algebra', [(5,0.9), (11,0.3), (12,0.3), (13,0.4), (15,0.9), (17,0.8)]),
            ('using substitution to make equations in quadratic equations', 'algebra', [(9,0.5), (11,0.6), (12,0.7), (13,0.5)]),
            ('factorisation by inspection for a=1', 'algebra', [(7,0.8), (12,0.9)]),
            ('factorisation by inspection for a ne 1', 'algebra', [(12,0.9)]),
            ('basic coordinate geometry', 'geometry', [(10,0.8), (11,0.6), (13,0.7)]),
            ('writing quadratics in completed square form', 'algebra', [(11,0.9), (13,0.8)]),
            ('graph of quadratics', 'algebra', [(11,0.7), (12,0.5), (13,0.6)]),
            ('vertex of parabola', 'algebra', []),
            ('x-intercept/roots', 'algebra', [(15,0.4), (16,0.6), (17,0.5)]),
            ('interpreting completed square form', 'algebra', []),
            ('quadratic formula derivation', 'algebra', [(15,0.9)]),
            ('using quadratic formula', 'algebra', [(16,0.8), (17,0.7)]),
            ('nature of roots', 'algebra', []),
            ('discriminant', 'algebra', [(16,0.7)])
        ]

        for topic, chapter, dependencies in node_data:
            self._add_node_internal(topic, chapter, dependencies)

    def _load_mcqs_from_json(self, mcqs_file: str):
        """Load MCQs from JSON file with detailed diagnostic information"""
        try:
            with open(mcqs_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Required MCQs file '{mcqs_file}' not found. Please ensure the MCQs JSON file exists.")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in MCQs file '{mcqs_file}': {e}")

        # Validate JSON structure
        if 'mcqs' not in data:
            raise ValueError(f"Invalid JSON structure in '{mcqs_file}': missing 'mcqs' key")


        # Clear existing MCQs
        self.mcqs.clear()

        # Load each MCQ with detailed error reporting
        successfully_loaded = 0

        for i, mcq_data in enumerate(data['mcqs']):

            try:

                # Check for required fields
                required_fields = ['text', 'options', 'correctindex', 'option_explanations',
                                'main_topic_index', 'subtopic_weights']

                missing_fields = []
                for field in required_fields:
                    if field not in mcq_data:
                        missing_fields.append(field)

                if missing_fields:
                    print(f"   ❌ Missing required fields: {missing_fields}")
                    continue

                mcq = MCQ.from_dict(mcq_data)

                # Check for duplicate IDs
                if mcq.id in self.mcqs:
                    raise ValueError(f"Duplicate MCQ ID '{mcq.id}' found. IDs must be unique.")

                # Store the MCQ
                self.mcqs[mcq.id] = mcq
                successfully_loaded += 1
            except Exception as e:
                print(f"   ❌ Error loading MCQ #{i+1}: {e}")
        print(f"✅ Successfully loaded {successfully_loaded} MCQs from {mcqs_file}")
        return successfully_loaded

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

    def export_to_json(self, nodes_file: str = None, mcqs_file: str = None):
        """Export current state back to JSON files"""

        if nodes_file:
            # Export nodes
            nodes_data = {
                "nodes": [],
                "metadata": {
                    "total_nodes": len(self.nodes),
                    "chapters": list(set(node.chapter for node in self.nodes.values())),
                    "description": "Knowledge graph for adaptive learning system"
                }
            }

            for node_id, node in self.nodes.items():
                node_data = {
                    "id": node_id,
                    "topic": node.topic,
                    "chapter": node.chapter,
                    "dependencies": [
                        {"target": target, "weight": weight}
                        for target, weight in node.dependencies
                    ]
                }
                nodes_data["nodes"].append(node_data)

            with open(nodes_file, 'w') as f:
                json.dump(nodes_data, f, indent=2)
            print(f"Exported {len(self.nodes)} nodes to {nodes_file}")

        if mcqs_file:
            # Export MCQs
            mcqs_data = {
                "mcqs": [],
                "metadata": {
                    "total_mcqs": len(self.mcqs),
                    "chapters_covered": list(set(mcq.chapter for mcq in self.mcqs.values())),
                    "topics_covered": list(set(mcq.main_topic_index for mcq in self.mcqs.values())),
                    "description": "MCQ bank for adaptive learning system"
                }
            }

            for mcq in self.mcqs.values():
                mcq_data = {
                    "id": mcq.id,
                    "text": mcq.text,
                    "options": mcq.options,
                    "correctindex": mcq.correctindex,
                    "option_explanations": mcq.option_explanations,
                    "main_topic_index": mcq.main_topic_index,
                    "chapter": mcq.chapter,
                    "subtopic_weights": {str(k): v for k, v in mcq.subtopic_weights.items()},
                    "difficulty_breakdown": {
                        "conceptual_understanding": mcq.difficulty_breakdown.conceptual_understanding,
                        "procedural_fluency": mcq.difficulty_breakdown.procedural_fluency,
                        "problem_solving": mcq.difficulty_breakdown.problem_solving,
                        "mathematical_communication": mcq.difficulty_breakdown.mathematical_communication,
                        "memory": mcq.difficulty_breakdown.memory,
                        "spatial_reasoning": mcq.difficulty_breakdown.spatial_reasoning
                    }
                }
                mcqs_data["mcqs"].append(mcq_data)

            with open(mcqs_file, 'w') as f:
                json.dump(mcqs_data, f, indent=2)
            print(f"Exported {len(self.mcqs)} MCQs to {mcqs_file}")


    def _add_node_internal(self, topic: str, chapter: str, dependencies: List[Tuple[int, float]]):
        """Internal method to add a node with automatic index assignment"""
        index = self._next_index
        self._next_index += 1

        node = Node(topic, chapter, dependencies)
        self.nodes[index] = node
        self.topic_to_index[topic] = index
        self._matrix_dirty = True  # Invalidate cache
        return index

    def add_node(self, topic: str, chapter: str, dependencies: List[Tuple[int, float]] = None):
        """Public method to add a new node with automatic indexing
        Validates dependencies exist before adding.
        """
        if dependencies is None:
            dependencies = []

        # Check if topic already exists
        if topic in self.topic_to_index:
            raise ValueError(f"Topic '{topic}' already exists in the knowledge graph")

        # Add the node
        index = self._add_node_internal(topic, chapter, dependencies)

        # Update NetworkX graph
        self.graph.add_node(index, topic=topic, chapter=chapter)

        # Add edges for dependencies
        for dest, weight in dependencies:
            if dest not in self.nodes:
                print(f"Warning: Dependency index {dest} does not exist, skipping edge")
                continue
            self.graph.add_edge(index, dest, weight=weight)
        self._matrix_dirty = True  # Invalidate cache
        return index

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

    def create_mcqs(self, text: str, options: List[str], correctindex: int, option_explanations: List[str], main_topic_index: int,
                                       subtopic_weights: Dict[int, float],conceptual=0.0, procedural=0.0, problem_solving=0.0,communication=0.0, memory=0.0, spatial=0.0) -> MCQ:
        """
        Create a new MCQ and add it to the question bank.
        Validates all referenced topics exist and weights sum to 1.0.
        """

        # Validate ALL topics in subtopic_weights

        for topic_idx in subtopic_weights.keys():
            if topic_idx not in self.nodes:
                raise ValueError(f"Topic index {topic_idx} not found in knowledge graph")

        # Validate that explicit weights sum to 1.0 (with small tolerance for floating point)
        weight_sum = sum(subtopic_weights.values())
        if abs(weight_sum - 1.0) > 0.001:
            raise ValueError(f"Topic weights must sum to 1.0, got {weight_sum}")

        mcq_id = str(uuid.uuid4())
        # Get node for chapter info
        node = self.get_node_by_index(main_topic_index)

        difficulty_breakdown = DifficultyBreakdown.create(conceptual, procedural, problem_solving, communication, memory, spatial)

        mcq = MCQ(text=text,options=options,correctindex=correctindex,option_explanations=option_explanations,main_topic_index=main_topic_index,chapter=node.chapter,subtopic_weights=subtopic_weights,difficulty_breakdown=difficulty_breakdown,id=mcq_id
        )

        # Store MCQ in the graph
        self.mcqs[mcq.id] = mcq

        return mcq


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


    def visualize_graph(self, figsize=(12, 8), node_size=1000, font_size=8):
        """Visualize the knowledge graph"""
        fig, ax = plt.subplots(figsize=figsize)

        # Use spring layout for natural clustering
        pos = nx.spring_layout(self.graph, k=2, iterations=50)

        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos,
                              node_color='lightblue',
                              node_size=node_size,
                              ax=ax)

        # Draw edges with weight-based thickness
        edges = self.graph.edges()
        weights = [self.graph[u][v]['weight'] for u, v in edges]

        nx.draw_networkx_edges(self.graph, pos,
                              edge_color='gray',
                              width=[w*3 for w in weights],
                              alpha=0.6,
                              arrows=True,
                              arrowsize=20,
                              ax=ax)

        # Draw labels
        labels = {node: f"{node}\n{self.graph.nodes[node]['topic'][:15]}..." for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, labels, font_size=font_size, ax=ax)

        plt.title("Knowledge Graph Visualization")
        plt.axis('off')
        plt.tight_layout()
        plt.show()

@dataclass
class MCQVector:
    """
    Vectorized representation of an MCQ for efficient algorithm processing.
    Caches computed values like prerequisites for performance.
    """
    mcq_id: str
    mcq_ref: MCQ # Reference to full MCQ object
    prerequisites: Dict[int, float]  # computed prerequisites with weights

    @property
    def subtopic_weights(self):
        return self.mcq_ref.subtopic_weights

    @property
    def difficulty(self):
        """Overall difficulty level"""
        return self.mcq_ref.difficulty

    @property
    def primary_main_topic_index(self):
        """Main topic being tested"""
        return self.mcq_ref.main_topic_index

    @property
    def difficulty_breakdown(self) -> Dict[str, float]:
        difficulty_breakdown = self.mcq_ref.difficulty_breakdown.to_dict()
        return difficulty_breakdown

class MCQScheduler:
    """the bit that does the actual mcq algorithm calculations"""

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

    def _precompute_prerequisites(self):
        """Precompute prerequisites for all MCQs using explicit weights and adjacency matrix"""
        adjacency_matrix = self.kg.get_adjacency_matrix()

        for mcq_id, mcq in self.kg.mcqs.items():
            # Use the MCQ's explicit topic weights directly
            subtopic_weights = mcq.subtopic_weights

            # Calculate weighted prerequisites
            prerequisites = {}

            if adjacency_matrix.size > 0:
                # For each topic in the MCQ, find its prerequisites
                for main_topic_index, topic_weight in subtopic_weights.items():
                    if main_topic_index < adjacency_matrix.shape[0]:
                        # Get direct prerequisites for this topic
                        topic_prereqs = adjacency_matrix[main_topic_index, :]

                        # Weight the prerequisites by the topic's explicit weight in the MCQ
                        for prereq_index, prereq_strength in enumerate(topic_prereqs):
                            if prereq_strength > 0:
                                weighted_prereq = prereq_strength * topic_weight
                                if prereq_index in prerequisites:
                                    prerequisites[prereq_index] = max(prerequisites[prereq_index], weighted_prereq)
                                else:
                                    prerequisites[prereq_index] = weighted_prereq

            # Create MCQ vector
            mcq_vector = MCQVector(mcq_id=mcq_id,mcq_ref=mcq,prerequisites=prerequisites
        )

            self.mcq_vectors[mcq_id] = mcq_vector

    def _ensure_vectors_computed(self):
        """Ensure MCQ vectors are computed when needed"""
        if not self.mcq_vectors and self.kg.mcqs:
            self._precompute_prerequisites()

    def get_eligible_mcqs_for_greedy_selection(self, student_id: str) -> List[str]:
        """
        Get MCQ IDs eligible for greedy selection:
        1. All topics and subtopics must be studied
        2. Main topic must be 'due' (below mastery threshold)
        3. Not completed today
        """
        self._ensure_vectors_computed()
        student = self.student_manager.get_student(student_id)
        if not student:
            return []
        # Get mastery threshold from config
        mastery_threshold = self.get_config_value('algorithm_config.mastery_threshold', 0.7)

        eligible_mcqs = []

        for mcq_id, mcq_vector in self.mcq_vectors.items():
            # Skip if completed today
            if mcq_id in student.daily_completed:
                continue

            # Check if main topic is due (below mastery threshold)
            main_topic_mastery = student.get_mastery(mcq_vector.primary_main_topic_index)
            if main_topic_mastery >= mastery_threshold:
                continue  # Main topic not due

            # Check if all topics in the MCQ's explicit weights are studied
            all_explicit_topics_studied = True
            for main_topic_index in mcq_vector.subtopic_weights.keys():
                if not student.is_topic_studied(main_topic_index):
                    all_explicit_topics_studied = False
                    break

            if all_explicit_topics_studied:
                eligible_mcqs.append(mcq_id)

        return eligible_mcqs


    def get_eligible_mcqs_for_student(self, student_id: str) -> List[str]:
        """
        Get MCQ IDs that contain only studied topics for the student.
        """
        self._ensure_vectors_computed()
        student = self.student_manager.get_student(student_id)
        if not student:
            return []

        eligible_mcqs = []

        for mcq_id, mcq_vector in self.mcq_vectors.items():
            # Check if all topics in the MCQ's explicit weights are studied
            all_explicit_topics_studied = True
            for main_topic_index in mcq_vector.subtopic_weights.keys():
                if not student.is_topic_studied(main_topic_index):
                    all_explicit_topics_studied = False
                    break

            if all_explicit_topics_studied:
                eligible_mcqs.append(mcq_id)

        return eligible_mcqs




    def select_mcqs_greedy(self, student_id: str, num_questions: int = 1,
                          use_chapter_weights: bool = False) -> List[str]:
        """
        Main greedy algorithm for adaptive MCQ selection.
        Iteratively selects best question, updates virtual mastery, repeats.
        """
        self._ensure_vectors_computed()
        # Get config values
        greedy_max_mcqs_to_evaluate = self.get_config_value('greedy_algorithm.greedy_max_mcqs_to_evaluate', 50)
        greedy_early_stopping = self.get_config_value('greedy_algorithm.greedy_early_stopping', False)
        greedy_convergence_threshold = self.get_config_value('algorithm_config.greedy_convergence_threshold', 0.05)

        # Get MCQs eligible for selection
        eligible_mcqs = self.get_eligible_mcqs_for_greedy_selection(student_id)

        if not eligible_mcqs:
            print(f"No eligible MCQs found for greedy selection (no due main topics with all studied subtopics)")
            return []

        student = self.student_manager.get_student(student_id)

        # Performance optimization: limit MCQs evaluated if too many
        if len(eligible_mcqs) > greedy_max_mcqs_to_evaluate:
            # Sort by a quick priority score and take top candidates
            quick_scores = [(mcq_id, self._quick_priority_score(mcq_id, student))
                          for mcq_id in eligible_mcqs]
            quick_scores.sort(key=lambda x: x[1], reverse=True)
            eligible_mcqs = [mcq_id for mcq_id, _ in quick_scores[:self.config.greedy_max_mcqs_to_evaluate]]

        # Create working copy of mastery levels for algorithm (not real mastery updates)
        virtual_mastery = student.mastery_levels.copy()

        # Get prioritized topics (only those below mastery threshold)
        topic_priorities = self._calculate_topic_priorities_due_only(student, virtual_mastery)

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

                coverage_to_cost_ratio, coverage_info = self._calculate_coverage_to_cost_ratio(mcq_id, topic_priorities, virtual_mastery, student)

                if coverage_to_cost_ratio > best_ratio:
                    best_ratio = coverage_to_cost_ratio
                    best_mcq = mcq_id
                    best_coverage_info = coverage_info

            if best_mcq is None:
                print(f"No suitable MCQ found for remaining due topics in iteration {iteration + 1}")
                break

            # Select the best MCQ
            selected_mcqs.append(best_mcq)

            # Update virtual mastery and topic priorities
            total_coverage = self._update_virtual_mastery_and_priorities(best_mcq, virtual_mastery, topic_priorities, best_coverage_info, student)

            print(f"Selected Q{iteration + 1}: {self.kg.mcqs[best_mcq].text[:50]}...")
            print(f"  Coverage-to-cost ratio: {best_ratio:.3f}")
            print(f"  Total coverage gained: {total_coverage:.3f}")
            print(f"  Remaining due topics: {len(topic_priorities)}")

            # Early stopping if improvement is minimal
            if (greedy_early_stopping and abs(total_coverage - last_total_coverage) < greedy_convergence_threshold):
                print(f"Early stopping: minimal improvement detected")
                break

            last_total_coverage = total_coverage

        return selected_mcqs


    def _quick_priority_score(self, mcq_id: str, student: StudentProfile) -> float:
        """Quick scoring for performance optimization when too many MCQs available"""
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
                                            virtual_mastery: Dict[int, float]) -> Dict[int, float]:
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
                mastery = virtual_mastery.get(main_topic_index, student.get_mastery(main_topic_index))

                #  Only include topics below mastery threshold
                if mastery < mastery_threshold:
                    # topics with lower mastery get higher priority
                    priority = (1.0 - mastery) * greedy_priority_weight
                    topic_priorities[main_topic_index] = priority

        return topic_priorities

    def _calculate_weighted_coverage(self, mcq_vector: MCQVector,topic_priorities: Dict[int, float],virtual_mastery: Dict[int, float]) -> Dict:
        """
        Calculate how well an MCQ covers priority topics.
        Returns coverage score and breakdown.
        """
        # Get config values
        greedy_subtopic_weight = self.get_config_value('greedy_algorithm.greedy_subtopic_weight', 0.7)
        greedy_prereq_weight = self.get_config_value('greedy_algorithm.greedy_prereq_weight', 0.5)

        total_coverage = 0.0
        coverage_details = {'main_topic_coverage': 0.0,'subtopic_coverage': 0.0,'prereq_coverage': 0.0}

        # Main topic and subtopic coverage - for due topics
        for main_topic_index, mcq_weight in mcq_vector.subtopic_weights.items():
            if main_topic_index in topic_priorities:
                topic_priority = topic_priorities[main_topic_index]

                # Coverage = MCQ weight × topic priority × type weight factor
                if main_topic_index == mcq_vector.primary_main_topic_index:
                    coverage = mcq_weight * topic_priority
                    coverage_details['main_topic_coverage'] += coverage
                else:
                    coverage = mcq_weight * topic_priority * greedy_subtopic_weight
                    coverage_details['subtopic_coverage'] += coverage

                total_coverage += coverage

        # Prerequisite coverage - for due prerequisites
        for prereq_index, prereq_weight in mcq_vector.prerequisites.items():
            if prereq_index in topic_priorities:
                topic_priority = topic_priorities[prereq_index]
                coverage = prereq_weight * topic_priority * greedy_prereq_weight
                coverage_details['prereq_coverage'] += coverage
                total_coverage += coverage

        coverage_details['total_coverage'] = total_coverage
        return coverage_details

    def _update_virtual_mastery_and_priorities(self, mcq_id: str,
                                            virtual_mastery: Dict[int, float],
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

        mcq = self.kg.mcqs.get(mcq_id)
        mcq_vector = self.mcq_vectors.get(mcq_id)

        if not mcq or not mcq_vector:
            return 0.0

        topics_to_remove = []
        total_coverage = coverage_info['total_coverage']

        # Update main topic and subtopics
        for main_topic_index, topic_weight in mcq_vector.subtopic_weights.items():
            if main_topic_index in topic_priorities:  # Only update due topics
                current_mastery = virtual_mastery.get(main_topic_index, student.get_mastery(main_topic_index))

                # Mastery increase based on question difficulty and weight
                if main_topic_index == mcq_vector.primary_main_topic_index:
                    # Main topic gets full difficulty boost
                    mastery_increase = mcq_vector.difficulty * greedy_mastery_update_rate
                else:
                    # Subtopics get weighted boost
                    mastery_increase = (mcq_vector.difficulty * topic_weight * greedy_mastery_update_rate)

                new_mastery = min(1.0, current_mastery + mastery_increase)
                virtual_mastery[main_topic_index] = new_mastery

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
                current_mastery = virtual_mastery.get(prereq_index, student.get_mastery(prereq_index))

                # Prerequisites get smaller, weighted boost
                mastery_increase = (mcq_vector.difficulty * prereq_weight * greedy_mastery_update_rate * 0.5)

                new_mastery = min(1.0, current_mastery + mastery_increase)
                virtual_mastery[prereq_index] = new_mastery

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


        return total_coverage
    def _calculate_coverage_to_cost_ratio(self, mcq_id: str, topic_priorities: Dict[int, float],virtual_mastery: Dict[int, float],student: StudentProfile) -> Tuple[float, Dict]:
        """
        Calculate coverage-to-cost ratio
        Higher ratio = better choice (more benefit, less cost)
        Coverage is weighted by topic priorities and question weights.
        """
        mcq = self.kg.mcqs.get(mcq_id)
        mcq_vector = self.mcq_vectors.get(mcq_id)

        if not mcq or not mcq_vector:
            return 0.0, {'total_coverage': 0.0}

        # Calculate weighted coverage
        coverage_info = self._calculate_weighted_coverage( mcq_vector, topic_priorities, virtual_mastery)

        if coverage_info['total_coverage'] == 0:
            return 0.0, coverage_info

        # Calculate difficulty cost (penalty for poor match)
        difficulty_cost = self._calculate_difficulty_cost_enhanced(mcq_vector, virtual_mastery, student)

        # Calculate importance bonus (reward for important topics)
        importance_bonus = self._calculate_importance_bonus_enhanced(mcq_vector, topic_priorities)

        # Total cost (lower is better)
        total_cost = max(0.01, difficulty_cost - importance_bonus)  # Prevent division by zero

        # Ratio: coverage/cost (higher is better)
        coverage_to_cost_ratio = coverage_info['total_coverage'] / total_cost

        return coverage_to_cost_ratio, coverage_info


    def _calculate_difficulty_cost_enhanced(self, mcq_vector: MCQVector,virtual_mastery: Dict[int, float],student: StudentProfile) -> float:
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
            mastery = virtual_mastery.get(main_topic_index, student.get_mastery(main_topic_index))
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

    def _calculate_importance_bonus_enhanced(self, mcq_vector: MCQVector,topic_priorities: Dict[int, float]) -> float:
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



class BayesianKnowledgeTracing:
    """Bayesian Knowledge Tracing implementation for the education knowledge graph."""

    def __init__(self, knowledge_graph, student_manager,config_manager=None,scheduler: Optional[MCQScheduler] = None):
        """
        Initialize BKT with knowledge graph and student manager

        Args:
            knowledge_graph: The KnowledgeGraph instance
            student_manager: The StudentManager instance
            default_params: Default BKT parameters for all topics
            config: BKT configuration object
        """
        self.kg = knowledge_graph
        self.student_manager = student_manager
        self.config = config_manager or knowledge_graph.config
        self.scheduler = scheduler


    def get_topic_parameters(self, main_topic_index: int):
        """Get BKT parameters for a topic using direct config values"""
        params = self.config.get_bkt_parameters(main_topic_index)

        # Return a simple dict instead of a complex object
        return {
            'prior_knowledge': params.get('prior_knowledge', 0.1),
            'learning_rate': params.get('learning_rate', 0.3),
            'slip_rate': params.get('slip_rate', 0.05),
            'guess_rate': params.get('guess_rate', 0.15)
        }
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
    '''
    def _initialize_topic_parameters(self):
        """Initialize BKT parameters for all topics in the knowledge graph"""
        for node_index in self.kg.get_all_indexes():
            if node_index not in self.topic_parameters:
                # customize parameters based on topic difficulty/properties here
                self.topic_parameters[node_index] = BKTParameters(prior_knowledge=0.1,    learning_rate=0.3,  slip_rate=0.05,  guess_rate=0.15       )

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
            BKTParameters object (may be modified copy)
        """
        base_params = self.get_topic_parameters(main_topic_index)

        # If difficulty adaptation is disabled, return base parameters
        if not self.config.enable_difficulty_adaptation:
            return base_params

        # For now, return base parameters - can be extended later
        # to adjust based on MCQ difficulty
        return base_params
    '''
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
            student.mastery_levels[main_topic_index] = params['prior_knowledge']
        else:
            # Initialize all topics
            for node_index in self.kg.get_all_indexes():
                if node_index not in student.mastery_levels:
                    params = self.get_topic_parameters(node_index)
                    student.mastery_levels[node_index] = params['prior_knowledge']

    def calculate_conditional_probability(self, current_mastery: float, is_correct: bool, params: Dict) -> float:
        """
        Calculate P(L_t | Result) using Bayes' theorem

        Args:
            current_mastery: Current P(L_t)
            is_correct: Whether the student answered correctly
            params: BKT parameters for this topic

        Returns:
            Updated probability that student knows the skill
        """
        if is_correct:
            # P(L_t | Correct) = P(L_t)(1-P(S)) / [P(L_t)(1-P(S)) + (1-P(L_t))P(G)]
            numerator = current_mastery * (1 - params['slip_rate'])
            denominator = (current_mastery * (1 - params['slip_rate']) +
                          (1 - current_mastery) * params['guess_rate'])
        else:
            # P(L_t | Incorrect) = P(L_t)P(S) / [P(L_t)P(S) + (1-P(L_t))(1-P(G))]
            numerator = current_mastery * params['slip_rate']
            denominator = (current_mastery *  params['slip_rate'] +
                          (1 - current_mastery) * (1 - params['guess_rate']))

        # Avoid division by zero
        if denominator == 0:
            return current_mastery

        return numerator / denominator

    def update_mastery(self, conditional_prob: float, params: Dict) -> float:
        """
        Update mastery using learning rate: P(L_{t+1}) = P(L_t|Result) + (1-P(L_t|Result))P(T)

        Args:
            conditional_prob: P(L_t | Result) from calculate_conditional_probability
            params: BKT parameters for this topic

        Returns:
            Updated mastery level P(L_{t+1})
        """
        return conditional_prob + (1 - conditional_prob) * params['learning_rate']

    def predict_correctness(self, mastery: float, params: Dict) -> float:
        """
        Predict probability of correct answer: P(Correct) = P(L_t)(1-P(S)) + (1-P(L_t))P(G)

        Args:
            mastery: Current mastery level P(L_t)
            params: BKT parameters for this topic

        Returns:
            Probability of answering correctly
        """
        return mastery * (1 - params['slip_rate']) + (1 - mastery) * params['guess_rate']

    def process_student_response(self, student_id: str, main_topic_index: int,
                                is_correct: bool, mcq_id: str = None,
                                custom_params: Optional[Dict] = None) -> Dict:
      """
      Process a student's response and update their mastery using BKT

      Args:
          student_id: Student identifier
          main_topic_index: Index of the topic being tested
          is_correct: Whether the student answered correctly
          mcq_id: Optional MCQ identifier for logging

      Returns:
          Dictionary with before/after mastery and prediction info
      """
      student = self.student_manager.get_student(student_id)
      if not student:
          raise ValueError(f"Student {student_id} not found")
      # Use provided custom parameters or default for topic
      params = custom_params if custom_params else self.get_topic_parameters(main_topic_index)

      # Get current mastery level
      current_mastery = student.get_mastery(main_topic_index)


      # If this is the first time seeing this topic, initialize with prior
      if main_topic_index not in student.mastery_levels:
          current_mastery = params['prior_knowledge']
          student.mastery_levels[main_topic_index] = current_mastery

      # Calculate prediction before update (for validation)
      prediction_before = self.predict_correctness(current_mastery, params)

      # Apply BKT update
      conditional_prob = self.calculate_conditional_probability(current_mastery, is_correct, params)
      new_mastery = self.update_mastery(conditional_prob, params)

      # Update student's mastery level
      student.mastery_levels[main_topic_index] = new_mastery

      # Calculate new prediction
      prediction_after = self.predict_correctness(new_mastery, params)

      # Return detailed information about the update
      return {
                                'student_id': student_id,
                                'main_topic_index': main_topic_index,
                                'topic_name': self.kg.get_topic_of_index(main_topic_index),
                                'mcq_id': mcq_id,
                                'is_correct': is_correct,
                                'mastery_before': current_mastery,
                                'mastery_after': new_mastery,
                                'mastery_change': new_mastery - current_mastery,
                                'conditional_probability': conditional_prob,
                                'prediction_before': prediction_before,
                                'prediction_after': prediction_after,
                                'parameters_used': params.copy()
                                }

    def process_mcq_response_improved(self, student_id: str, mcq_id: str,
                                    is_correct: bool) -> List[Dict]:
        """
        Enhanced version that uses explicit topic weights from the MCQ (ive chaned this a bit)
        """
        mcq = self.kg.mcqs.get(mcq_id)
        if not mcq:
            raise ValueError(f"MCQ {mcq_id} not found")

        updates = []

        # Use the MCQ's explicit topic weights directly
        for main_topic_index, weight in mcq.subtopic_weights.items():
            # Get base parameters for this topic
            base_params = self.get_topic_parameters(main_topic_index)

            # Create adjusted parameters with scaled learning rate
            adjusted_params = {
                'prior_knowledge': base_params['prior_knowledge'],
                'learning_rate': base_params['learning_rate'] * weight,  # Scale by weight
                'slip_rate': base_params['slip_rate'],
                'guess_rate': base_params['guess_rate']
            }
            update = self.process_student_response(student_id, main_topic_index, is_correct, mcq_id, custom_params=adjusted_params)
            update['topic_weight'] = weight
            update['is_primary_topic'] = (main_topic_index == mcq.main_topic_index)

            updates.append(update)

        return updates

    def apply_area_of_effect(self, student_id: str, center_main_topic_index: int,mastery_change: float) -> List[Dict]:
        """
        Area of effect that uses actual path weights between topics.

        Args:
            student_id: Student identifier
            center_main_topic_index: Topic that was updated
            mastery_change: How much the center topic changed
            max_distance: Maximum hops to propagate (default 3)
            decay_rate: How much effect decays per hop (default 0.5)

        Returns:
            List of update dictionaries for affected topics
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

        Args:
            path: List of topic indices representing the path

        Returns:
            Combined weight (product of all edge weights in path)
        """
        if len(path) < 2:
            return 1.0

        total_weight = 1.0

        for i in range(len(path) - 1):
            source = path[i]
            target = path[i + 1]

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
        # Do normal MCQ processing first
        primary_updates = self.process_mcq_response_improved(student_id, mcq_id, is_correct)

        if not is_correct:  # Only spread effects on correct answers
            return primary_updates

        all_updates = primary_updates.copy()

        # Add area effects for primary topics that had positive mastery changes
        for update in primary_updates:
            if update.get('is_primary_topic', False) and update['mastery_change'] > 0:
                area_updates = self.apply_area_of_effect(student_id,update['main_topic_index'],update['mastery_change'])
                all_updates.extend(area_updates)

        return all_updates

    def calibrate_parameters(self, student_id: str, main_topic_index: int,attempt_history: List[Tuple[bool, datetime]]) -> Dict:
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
        adjusted_prior = min(0.8, current_params['prior_knowledge'] + early_rate * 0.3)

        # If overall success rate is very high, reduce slip rate
        adjusted_slip = max(0.01, current_params['slip_rate'] - (success_rate - 0.7) * 0.1)

        # If success rate is low but attempts are many, increase learning rate
        adjusted_learning = min(0.8, current_params['learning_rate'] +(0.1 if success_rate < 0.5 and total_attempts > 5 else 0))

        return {
            'prior_knowledge': adjusted_prior,
            'learning_rate': adjusted_learning,
            'slip_rate': max(0.01, min(0.3, adjusted_slip)),
            'guess_rate': current_params['guess_rate']
        }



def create_realistic_student(student_manager, kg, bkt_system, student_name: str) -> str:
    """
    Create a student with realistic mastery and confidence distributions.
    """
    student_id = f"student_{student_name.lower().replace(' ', '_')}"
    student = student_manager.create_student(student_id)

    all_indices = kg.get_all_indexes()
    #bkt_system.initialize_student_mastery(student_id)

    # Create varied mastery and confidence levels
    for main_topic_index in all_indices:
        if main_topic_index in [0, 1, 14, 15]:  # Basic topics
            mastery = random.uniform(0.4, 0.8)
        elif main_topic_index in [2, 3, 5, 6]:  # Intermediate topics
            mastery = random.uniform(0.2, 0.6)
        else:  # Advanced topics
            mastery = random.uniform(0.1, 0.4)

        # Add randomness and ensure bounds
        mastery = max(0.0, min(1.0, mastery + random.gauss(0, 0.05)))

        student.mastery_levels[main_topic_index] = mastery

        # Mark topics as studied if they have reasonable mastery
        if mastery > 0.15:
            student.studied_topics[main_topic_index] = True

    # Set realistic usage statistics
    student.total_questions_attempted = random.randint(10, 50)
    student.total_time_on_system = random.uniform(60.0, 300.0)
    student.session_count = random.randint(3, 15)

    return student_id


def ask_question(kg, mcq_id: str) -> Tuple[bool, float]:
    """
    Present a question and get user response.
    """
    mcq = kg.mcqs.get(mcq_id)
    if not mcq:
        print(f"Question {mcq_id} not found!")
        return False, 0.0

    print(f"\n{'-'*70}")
    print("QUESTION:")
    print(f"{mcq.text}")
    print("\nOptions:")

    for i, option in enumerate(mcq.options):
        print(f"  {chr(65+i)}. {option}")

    start_time = datetime.now()
    valid_options = [chr(65+i) for i in range(len(mcq.options))]
    user_choice = None

    while user_choice is None:
        user_input = input(f"\nEnter your answer ({'/'.join(valid_options)}): ").strip().upper()
        if user_input in valid_options:
            user_choice = ord(user_input) - ord('A')
            print(f"You selected: {user_input}")
        else:
            print(f"Invalid input. Please enter one of: {'/'.join(valid_options)}")


    end_time = datetime.now()
    time_taken = (end_time - start_time).total_seconds()

    is_correct = user_choice == mcq.correctindex
    correct_option = chr(65 + mcq.correctindex)

    print(f"\n{'CORRECT!' if is_correct else 'INCORRECT!'}")
    print(f"The correct answer is: {correct_option}. {mcq.options[mcq.correctindex]}")
    print(f"Explanation of your answer: {mcq.option_explanations[user_choice]}")
    print(f"Time taken: {time_taken:.1f} seconds")

    return is_correct, time_taken

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

    show_comparison = before_masteries is not None and after_masteries is not None

    if show_comparison:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
        axes = [ax1, ax2]
        titles = ["MASTERY - Before", "MASTERY - After"]
        data_sets = [before_masteries, after_masteries]
    else:
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        axes = [ax]
        titles = [f"Knowledge Mastery {title_suffix}"]
        data_sets = [student.mastery_levels]

    pos = nx.spring_layout(kg.graph, k=3, iterations=100, seed=42)

    def get_mastery_color(value):
        if value < 0.2:
            return '#d32f2f'  # Dark red
        elif value < 0.4:
            return '#f57c00'  # Orange
        elif value < 0.6:
            return '#fbc02d'  # Yellow
        elif value < 0.8:
            return '#689f38'  # Light green
        else:
            return '#388e3c'  # Dark green

    for ax, title, data in zip(axes, titles, data_sets):
        node_colors = []
        node_sizes = []
        edge_colors = []
        edge_widths = []

        for node_index in kg.graph.nodes():
            value = data.get(node_index, 0.0)
            node_colors.append(get_mastery_color(value))
            node_sizes.append(300 + (value * 900))

        for u, v in kg.graph.edges():
            weight = kg.graph[u][v].get('weight', 0.5)
            if weight > 0.7:
                edge_colors.append('#2e7d32')
            elif weight > 0.4:
                edge_colors.append('#1976d2')
            else:
                edge_colors.append('#757575')
            edge_widths.append(1 + (weight * 4))

        nx.draw_networkx_nodes(kg.graph, pos, node_color=node_colors, node_size=node_sizes,
                              alpha=0.9, linewidths=2, edgecolors='white', ax=ax)
        nx.draw_networkx_edges(kg.graph, pos, edge_color=edge_colors, width=edge_widths,
                              alpha=0.7, arrows=True, arrowsize=25, ax=ax)

        labels = {}
        for node_index in kg.graph.nodes():
            topic_name = kg.get_topic_of_index(node_index)
            value = data.get(node_index, 0.0)
            short_name = topic_name[:15] + "..." if len(topic_name) > 15 else topic_name
            labels[node_index] = f"{node_index}\n{short_name}\n{value:.2f}"

        nx.draw_networkx_labels(kg.graph, pos, labels, font_size=8, font_weight='bold',
                               font_color='black', ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')

    # Add legend
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#d32f2f',
                   markersize=10, label='Very Low (0.0-0.2)', markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#f57c00',
                   markersize=10, label='Low (0.2-0.4)', markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#fbc02d',
                   markersize=10, label='Medium-Low (0.4-0.6)', markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#689f38',
                   markersize=10, label='Medium-High (0.6-0.8)', markeredgecolor='black'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#388e3c',
                   markersize=10, label='High (0.8-1.0)', markeredgecolor='black')
    ]

    if show_comparison:
        fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.08),
                  ncol=5, fontsize=9, title="Mastery Levels")
        plt.suptitle(f"Knowledge Graph Comparison - {student_id} {title_suffix}",
                     fontsize=16, fontweight='bold')
    else:
        ax.legend(handles=legend_elements, loc='center left', bbox_to_anchor=(1.02, 0.5),
                 fontsize=9, title="Legend")
        plt.title(f"Knowledge Graph - {student_id} {title_suffix}", fontsize=16, fontweight='bold')

    plt.tight_layout()
    plt.show()


def test_greedy_algorithm_functionality():
    """
    Comprehensive test to demonstrate and validate the new greedy MCQ selection algorithm.
    Tests eligibility filtering, priority calculation, and iterative selection behavior.
    """
    print("\n" + "="*80)
    print("GREEDY ALGORITHM FUNCTIONALITY TEST")
    print("="*80)

    try:


        kg = KnowledgeGraph(
            nodes_file='kg.json',
            mcqs_file='computed_mcqs.json',
            config_file='config.json'
        )
        student_manager = StudentManager(kg.config)
        mcq_scheduler = MCQScheduler(kg, student_manager)
        bkt_system = BayesianKnowledgeTracing(kg, student_manager)

        # Connect systems
        mcq_scheduler.set_bkt_system(bkt_system)
        student_manager.set_bkt_system(bkt_system)


        # Create test student with mixed mastery levels
        student_id = "test_student_greedy"
        student = create_test_student_with_varied_mastery(student_manager, kg, bkt_system, student_id)

        print(f"\n📊 TEST STUDENT PROFILE: {student_id}")
        print("-" * 50)

        # Display student's current state
        #display_student_mastery_summary(student, kg, config_manager)

        # Test 1: MCQ Eligibility Filtering
        print(f"\n🔍 TEST 1: MCQ ELIGIBILITY FILTERING")
        print("-" * 40)
        test_mcq_eligibility_filtering(mcq_scheduler, student_id, kg)

        # Test 2: Topic Priority Calculation
        print(f"\n📈 TEST 2: TOPIC PRIORITY CALCULATION")
        print("-" * 40)
        test_topic_priority_calculation(mcq_scheduler, student_id, kg)

        # Test 3: Iterative Selection Process
        print(f"\n🎯 TEST 3: ITERATIVE SELECTION PROCESS")
        print("-" * 40)
        test_iterative_selection_process(mcq_scheduler, student_id, kg, num_questions=5)

        # Test 4: Virtual Mastery Updates
        print(f"\n🔄 TEST 4: VIRTUAL MASTERY UPDATE BEHAVIOR")
        print("-" * 40)
        test_virtual_mastery_updates(mcq_scheduler, student_id, kg)


        print(f"\n✅ ALL GREEDY ALGORITHM TESTS COMPLETED SUCCESSFULLY")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        print("Please check the implementation and try again.")

def create_test_student_with_varied_mastery(student_manager, kg, bkt_system, student_id):
    """Create a test student with strategically varied mastery levels for testing"""
    student = student_manager.create_student(student_id)

    # Get all topic indices
    all_topics = kg.get_all_indexes()

    # Create varied mastery levels for testing
    mastery_distribution = {
        'very_low': (0.1, 0.3),    # Due topics (below 0.7 threshold)
        'low': (0.3, 0.4),         # Due topics
        'medium': (0.4, 0.5),      # Due topics (just below threshold)
        'high': (0.5, 0.6),        # Not due (above threshold)
        'very_high': (0.6, 0.7)    # Not due
    }

    # Distribute topics across mastery levels
    topics_per_category = len(all_topics) // 5
    topic_categories = {
        'very_low': all_topics[:topics_per_category],
        'low': all_topics[topics_per_category:2*topics_per_category],
        'medium': all_topics[2*topics_per_category:3*topics_per_category],
        'high': all_topics[3*topics_per_category:4*topics_per_category],
        'very_high': all_topics[4*topics_per_category:]
    }

    # Set mastery levels and mark all topics as studied
    import random
    for category, topics in topic_categories.items():
        min_mastery, max_mastery = mastery_distribution[category]
        for main_topic_index in topics:
            mastery = random.uniform(min_mastery, max_mastery)
            student.mastery_levels[main_topic_index] = mastery
            student.confidence_levels[main_topic_index] = mastery * 0.8  # Confidence slightly lower
            student.studied_topics[main_topic_index] = True  # Mark as studied

    return student

def display_student_mastery_summary(student, kg, config_manager):
    """Display a summary of student's mastery levels categorized by due status"""
    mastery_threshold = config_manager.get('algorithm_config.mastery_threshold', 0.7)
    due_topics = []
    not_due_topics = []

    for main_topic_index, mastery in student.mastery_levels.items():
        topic_name = kg.get_topic_of_index(main_topic_index)
        if mastery < mastery_threshold:
            due_topics.append((main_topic_index, topic_name, mastery))
        else:
            not_due_topics.append((main_topic_index, topic_name, mastery))

    # Sort by mastery level
    due_topics.sort(key=lambda x: x[2])
    not_due_topics.sort(key=lambda x: x[2])

    print(f"📚 Studied Topics: {len(student.studied_topics)}")
    print(f"🔴 Due Topics (below {mastery_threshold}): {len(due_topics)}")
    print(f"🟢 Not Due Topics (above {mastery_threshold}): {len(not_due_topics)}")

    # Show a few examples of each
    print(f"\nLowest mastery topics (most due):")
    for i, (idx, name, mastery) in enumerate(due_topics[:5]):
        print(f"  {i+1}. {name[:30]:<30} (mastery: {mastery:.3f})")

    print(f"\nHighest mastery topics (not due):")
    for i, (idx, name, mastery) in enumerate(not_due_topics[-3:]):
        print(f"  {i+1}. {name[:30]:<30} (mastery: {mastery:.3f})")

def test_mcq_eligibility_filtering(mcq_scheduler, student_id, kg):
    """Test that MCQ eligibility filtering works correctly"""
    # Test standard eligibility (all studied topics)
    all_eligible = mcq_scheduler.get_eligible_mcqs_for_student(student_id)

    # Test greedy eligibility (due main topics + all studied)
    greedy_eligible = mcq_scheduler.get_eligible_mcqs_for_greedy_selection(student_id)

    print(f"📋 All eligible MCQs (studied topics only): {len(all_eligible)}")
    print(f"🎯 Greedy eligible MCQs (due main topic + studied): {len(greedy_eligible)}")
    print(f"📉 Filtered out {len(all_eligible) - len(greedy_eligible)} MCQs with non-due main topics")

    # Analyze why MCQs were filtered out
    filtered_out = set(all_eligible) - set(greedy_eligible)
    if filtered_out:
        print(f"\nExample filtered MCQs (non-due main topics):")
        student = mcq_scheduler.student_manager.get_student(student_id)
        for i, mcq_id in enumerate(list(filtered_out)[:3]):
            mcq_vector = mcq_scheduler.mcq_vectors.get(mcq_id)
            if mcq_vector:
                main_topic = mcq_vector.primary_main_topic_index
                mastery = student.get_mastery(main_topic)
                topic_name = kg.get_topic_of_index(main_topic)
                print(f"  {i+1}. {topic_name[:40]:<40} (mastery: {mastery:.3f} >= {mcq_scheduler.config.mastery_threshold})")

    return greedy_eligible

def test_topic_priority_calculation(mcq_scheduler, student_id, kg):
    """Test that topic priority calculation only includes due topics"""
    student = mcq_scheduler.student_manager.get_student(student_id)
    virtual_mastery = student.mastery_levels.copy()

    # Calculate priorities using the new method
    topic_priorities = mcq_scheduler._calculate_topic_priorities_due_only(student, virtual_mastery)

    print(f"🎯 Topics with calculated priorities: {len(topic_priorities)}")
    # Get mastery threshold from config
    mastery_threshold = mcq_scheduler.get_config_value('algorithm_config.mastery_threshold', 0.7)

    # Verify all prioritized topics are below threshold
    all_below_threshold = True
    above_threshold_count = 0

    for main_topic_index, priority in topic_priorities.items():
        mastery = student.get_mastery(main_topic_index)
        if mastery >= mastery_threshold:
            all_below_threshold = False
            above_threshold_count += 1

    if all_below_threshold:
        print(f"✅ All prioritized topics are below mastery threshold ({mcq_scheduler.config.mastery_threshold})")
    else:
        print(f"❌ {above_threshold_count} prioritized topics are above mastery threshold")

    # Show priority distribution
    priorities = list(topic_priorities.values())
    if priorities:
        print(f"📊 Priority range: {min(priorities):.3f} to {max(priorities):.3f}")
        print(f"📈 Average priority: {sum(priorities)/len(priorities):.3f}")

        # Show top priority topics
        sorted_priorities = sorted(topic_priorities.items(), key=lambda x: x[1], reverse=True)
        print(f"\nTop 5 priority topics (lowest mastery):")
        for i, (topic_idx, priority) in enumerate(sorted_priorities[:5]):
            topic_name = kg.get_topic_of_index(topic_idx)
            mastery = student.get_mastery(topic_idx)
            print(f"  {i+1}. {topic_name[:35]:<35} (mastery: {mastery:.3f}, priority: {priority:.3f})")

    return topic_priorities

def test_iterative_selection_process(mcq_scheduler, student_id, kg, num_questions=5):
    """Test the iterative selection process and virtual mastery updates"""
    print(f"🔄 Running greedy selection for {num_questions} questions...")

    # Get initial state
    student = mcq_scheduler.student_manager.get_student(student_id)
    initial_due_count = len([t for t, m in student.mastery_levels.items()
                           if m < mcq_scheduler.config.mastery_threshold and student.is_topic_studied(t)])

    print(f"📊 Initial due topics: {initial_due_count}")

    # Run greedy selection with detailed output
    selected_mcqs = mcq_scheduler.select_mcqs_greedy(student_id, num_questions)

    print(f"\n📋 SELECTION RESULTS:")
    print(f"🎯 Questions selected: {len(selected_mcqs)}")

    # Analyze selected questions
    if selected_mcqs:
        print(f"\nSelected question analysis:")
        for i, mcq_id in enumerate(selected_mcqs):
            mcq = kg.mcqs.get(mcq_id)
            mcq_vector = mcq_scheduler.mcq_vectors.get(mcq_id)
            if mcq and mcq_vector:
                main_topic_name = kg.get_topic_of_index(mcq_vector.primary_main_topic_index)
                main_mastery = student.get_mastery(mcq_vector.primary_main_topic_index)
                print(f"  Q{i+1}: {main_topic_name[:40]:<40} (difficulty: {mcq_vector.difficulty:.2f}, mastery: {main_mastery:.3f})")

                # Show topic coverage
                topic_count = len(mcq_vector.subtopic_weights)
                prereq_count = len(mcq_vector.prerequisites)
                print(f"       Topics covered: {topic_count}, Prerequisites: {prereq_count}")

    return selected_mcqs

def test_virtual_mastery_updates(mcq_scheduler, student_id, kg):
    """Test that virtual mastery updates work correctly without affecting real mastery"""
    student = mcq_scheduler.student_manager.get_student(student_id)

    # Save original mastery levels
    original_mastery = student.mastery_levels.copy()

    # Get eligible MCQs and select one for testing
    eligible_mcqs = mcq_scheduler.get_eligible_mcqs_for_greedy_selection(student_id)

    if not eligible_mcqs:
        print("❌ No eligible MCQs for virtual mastery testing")
        return

    test_mcq_id = eligible_mcqs[0]
    mcq_vector = mcq_scheduler.mcq_vectors.get(test_mcq_id)

    if not mcq_vector:
        print("❌ No MCQ vector found for testing")
        return

    print(f"🧪 Testing virtual mastery updates with MCQ: {kg.mcqs[test_mcq_id].text[:50]}...")

    # Create virtual mastery copy
    virtual_mastery = student.mastery_levels.copy()

    # Calculate initial priorities
    initial_priorities = mcq_scheduler._calculate_topic_priorities_due_only(student, virtual_mastery)
    initial_due_count = len(initial_priorities)

    # Simulate MCQ selection and virtual updates
    coverage_info = mcq_scheduler._calculate_weighted_coverage(mcq_vector, initial_priorities, virtual_mastery)

    print(f"📊 Before virtual update:")
    print(f"   Due topics: {initial_due_count}")
    print(f"   Coverage calculated: {coverage_info['total_coverage']:.3f}")

    # Apply virtual mastery update
    mcq_scheduler._update_virtual_mastery_and_priorities(
        test_mcq_id, virtual_mastery, initial_priorities, coverage_info, student
    )

    final_due_count = len(initial_priorities)
    topics_covered = initial_due_count - final_due_count

    print(f"📊 After virtual update:")
    print(f"   Due topics remaining: {final_due_count}")
    print(f"   Topics covered: {topics_covered}")

    # Verify real mastery unchanged
    mastery_unchanged = all(
        original_mastery[topic_idx] == student.mastery_levels[topic_idx]
        for topic_idx in original_mastery
    )

    if mastery_unchanged:
        print("✅ Real student mastery levels unchanged (virtual-only updates)")
    else:
        print("❌ Real student mastery was modified (should be virtual-only)")

    # Show example virtual vs real mastery
    main_topic = mcq_vector.primary_main_topic_index
    original_main_mastery = original_mastery[main_topic]
    virtual_main_mastery = virtual_mastery[main_topic]
    real_main_mastery = student.mastery_levels[main_topic]

    print(f"\nExample mastery changes (main topic):")
    print(f"   Original: {original_main_mastery:.3f}")
    print(f"   Virtual:  {virtual_main_mastery:.3f} (change: +{virtual_main_mastery - original_main_mastery:.3f})")
    print(f"   Real:     {real_main_mastery:.3f} (should be unchanged)")



def run_knowledge_graph_test():
    """
    Main test system combining all functionalities.
    """
    print("KNOWLEDGE GRAPH LEARNING SYSTEM")
    print("Demonstrating Confidence-Based Selection & Area of Effect Updates")
    print("=" * 70)

    try:
        # Initialize system
        kg = KnowledgeGraph(
            nodes_file='kg.json',
            mcqs_file='computed_mcqs.json',
            config_file='config.json'
        )
        student_manager = StudentManager(kg.config)
        mcq_scheduler = MCQScheduler(kg, student_manager)
        bkt_system = BayesianKnowledgeTracing(kg, student_manager)

        # Connect systems
        mcq_scheduler.set_bkt_system(bkt_system)
        student_manager.set_bkt_system(bkt_system)


        # Load MCQs

        #loaded_mcq_ids = load_comprehensive_mcqs(kg)

        # Get student information
        print("\nSTUDENT REGISTRATION")
        print("-" * 25)
        student_name = input("Enter your name: ").strip()
        if not student_name:
            student_name = "Test Student"
            print(f"Using default name: {student_name}")

        # Create student profile
        print(f"\nCreating learning profile for {student_name}...")
        student_id = create_realistic_student(student_manager, kg, bkt_system, student_name)

        student = student_manager.get_student(student_id)

        # Show initial mastery levels
        print(f"\n INITIAL MASTERY LEVELS")
        print("-" * 30)
        print(f"{'Index':<6} {'Topic Name':<35} {'Mastery':<8} {'Level':<7} {'Confidence':<10} {'Studied'}")
        print("-" * 95)

        for main_topic_index in sorted(student.mastery_levels.keys()):
            topic_name = kg.get_topic_of_index(main_topic_index)
            mastery = student.get_mastery(main_topic_index)
            confidence = student.get_confidence(main_topic_index)
            studied = "✅ Yes" if student.is_topic_studied(main_topic_index) else "❌ No"

            short_name = topic_name[:30] + "..." if len(topic_name) > 30 else topic_name
            # Color-code mastery levels
            if mastery >= 0.7:
                level_emoji = "🟢"
            elif mastery >= 0.4:
                level_emoji = "🟡"
            else:
                level_emoji = "🔴"

            short_name = topic_name[:30] + "..." if len(topic_name) > 30 else topic_name
            print(f"{main_topic_index:<6} {short_name:<35} {mastery:<8.3f} {level_emoji:<7} {confidence:<10.3f} {studied}")


        # Select questions for practice
        print(f"\nQUESTION SELECTION PROCESS")
        print("-" * 30)
        eligible_mcqs = mcq_scheduler.get_eligible_mcqs_for_greedy_selection(student_id)
        print(f"Found {len(eligible_mcqs)} eligible questions (topics student has studied):")

        for mcq_id in eligible_mcqs:
            mcq = kg.mcqs.get(mcq_id)
            if mcq:
                topic_name = kg.get_topic_of_index(mcq.main_topic_index)
                difficulty = mcq.difficulty
                mastery = student.get_mastery(mcq.main_topic_index)

                # Color-code mastery levels
                if mastery >= 0.7:
                    mastery_emoji = "🟢"
                elif mastery >= 0.4:
                    mastery_emoji = "🟡"
                else:
                    mastery_emoji = "🔴"

                print(f"  {topic_name[:40]:<40} (Difficulty: {difficulty:.2f}, Mastery: {mastery_emoji} {mastery:.3f})")

        if not eligible_mcqs:
            print("No questions available for your current study topics.")
            return

        selected_mcqs = mcq_scheduler.select_mcqs_greedy(student_id, num_questions=1)
        print(f"\nSelected {len(selected_mcqs)} questions using greedy algorithm:")

        for i, mcq_id in enumerate(selected_mcqs, 1):
            mcq = kg.mcqs.get(mcq_id)
            if mcq:
                topic_name = kg.get_topic_of_index(mcq.main_topic_index)
                difficulty = mcq.difficulty
                mastery = student.get_mastery(mcq.main_topic_index)
                confidence = student.get_confidence(mcq.main_topic_index)
                # Color-code mastery and confidence levels
                if mastery >= 0.7:
                    mastery_emoji = "🟢"
                elif mastery >= 0.4:
                    mastery_emoji = "🟡"
                else:
                    mastery_emoji = "🔴"

                if confidence >= 0.7:
                    confidence_emoji = "🟢"
                elif confidence >= 0.4:
                    confidence_emoji = "🟡"
                else:
                    confidence_emoji = "🔴"

                # Calculate overall MCQ score for this question

                print(f"  {i}.  {topic_name}")
                print(f"     Difficulty: {difficulty:.2f}, Mastery: {mastery_emoji} {mastery:.3f}, Confidence: {confidence_emoji} {confidence:.3f}")
                print(f"     Question: {mcq.text[:60]}...")
                print()


        # Store initial state
        before_masteries = student.mastery_levels.copy()

        # Question session
        print(f"\nQUESTION SESSION")
        print("-" * 25)
        print(f"You will answer {len(selected_mcqs)} questions.")
        print("Your responses will update the knowledge model using Bayesian Knowledge Tracing.")

        session_results = []
        for i, mcq_id in enumerate(selected_mcqs, 1):
            print(f"\n--- Question {i} of {len(selected_mcqs)} ---")

            # Show question context
            mcq = kg.mcqs.get(mcq_id)
            if mcq:
                topic_name = kg.get_topic_of_index(mcq.main_topic_index)
                mastery = student.get_mastery(mcq.main_topic_index)
                confidence = student.get_confidence(mcq.main_topic_index)
                print(f"Topic: {topic_name}")
                print(f"Current mastery: {mastery:.3f}, confidence: {confidence:.3f}")

            # Ask question and record response
            is_correct, time_taken = ask_question(kg, mcq_id)


            bkt_updates = student_manager.record_attempt(student_id, mcq_id, is_correct, time_taken, kg)

            # Analyze updates
            area_analysis = analyze_area_of_effect(bkt_updates, kg)

            if bkt_updates:
                print(f"Knowledge updates: {area_analysis['total_updates']} topics affected")
                print(f"  Primary updates: {area_analysis['primary_count']}")
                print(f"  Area of effect: {area_analysis['area_effect_count']}")

                # Show detailed update information
                if area_analysis['primary_updates']:
                    print(f"\n  PRIMARY TOPIC UPDATES:")
                    for update in area_analysis['primary_updates']:
                        change = update['mastery_change']
                        if change > 0:
                            change_emoji = "📈"
                        elif change < 0:
                            change_emoji = "📉"
                        else:
                            change_emoji = "➡️"

                        print(f"    • {update['topic_name']}")
                        print(f"      📊 Before: {update['mastery_before']:.3f} → After: {update['mastery_after']:.3f}")
                        print(f"      {change_emoji} Change: {update['mastery_change']:+.3f}")

                if area_analysis['area_effect_updates']:
                    print(f"\n  AREA OF EFFECT UPDATES:")
                    for update in area_analysis['area_effect_updates'][:5]:  # Show first 5
                        change = update['mastery_change']
                        if change > 0:
                            change_emoji = "📈"
                        elif change < 0:
                            change_emoji = "📉"
                        else:
                            change_emoji = "➡️"

                        print(f"    • {update['topic_name']}")
                        print(f"      📊 Before: {update['mastery_before']:.3f} → After: {update['mastery_after']:.3f}")
                        print(f"      {change_emoji} Change: {update['mastery_change']:+.3f}")

                    if len(area_analysis['area_effect_updates']) > 5:
                        print(f"    ... and {len(area_analysis['area_effect_updates']) - 5} more area effect updates")

            session_results.append({
                'mcq_id': mcq_id,
                'is_correct': is_correct,
                'time_taken': time_taken,
                'area_analysis': area_analysis
            })

        # Store final state
        after_masteries = student.mastery_levels.copy()

        # Post-session analysis
        print(f"\nSESSION COMPLETE - ANALYSIS")
        print("=" * 40)

        # Basic statistics
        correct_count = sum(1 for result in session_results if result['is_correct'])
        total_primary_updates = sum(r['area_analysis']['primary_count'] for r in session_results)
        total_area_updates = sum(r['area_analysis']['area_effect_count'] for r in session_results)

        print(f"\n Session Summary:")
        print(f"   Questions answered: {len(session_results)}")
        print(f"   Correct answers: {correct_count}")
        print(f"   Accuracy: {correct_count/len(session_results)*100:.1f}%")
        print(f"  Total knowledge updates: {total_primary_updates + total_area_updates}")
        print(f"    Primary topic updates: {total_primary_updates}")
        print(f"    Area of effect updates: {total_area_updates}")

        # Analyze knowledge changes
        print(f"\nCOMPREHENSIVE KNOWLEDGE CHANGES")
        print("-" * 40)

        # Collect all changes (both primary and area effect)
        all_changes = []
        for main_topic_index in before_masteries:
            before = before_masteries.get(main_topic_index, 0.0)
            after = after_masteries.get(main_topic_index, 0.0)
            change = after - before
            if abs(change) > 0.001:  # Show even small changes
                topic_name = kg.get_topic_of_index(main_topic_index)
                confidence = student.get_confidence(main_topic_index)
                all_changes.append((main_topic_index, topic_name, before, after, change, confidence))

        # Sort by magnitude of change
        all_changes.sort(key=lambda x: abs(x[4]), reverse=True)

        print(f"Total topics with mastery changes: {len(all_changes)}")
        print(f"\n{'Index':<6} {'Topic Name':<35} {'Before':<8} {'After':<8} {'Change':<9} {'Type'}")
        print("-" * 95)

        # Determine which changes were primary vs area effect
        primary_topic_indices = set()
        area_effect_indices = set()

        for result in session_results:
            for update in result['area_analysis']['primary_updates']:
                primary_topic_indices.add(update['main_topic_index'])
            for update in result['area_analysis']['area_effect_updates']:
                area_effect_indices.add(update['main_topic_index'])

        for main_topic_index, topic_name, before, after, change, confidence in all_changes:
            if main_topic_index in primary_topic_indices:
                update_type = "Primary"
            elif main_topic_index in area_effect_indices:
                update_type = "Area Effect"
            else:
                update_type = "Other"
            # Use trending emojis for changes
            if change > 0:
                change_emoji = "📈"
            elif change < 0:
                change_emoji = "📉"
            else:
                change_emoji = "➡️"

            short_name = topic_name[:30] + "..." if len(topic_name) > 30 else topic_name
            print(f"{main_topic_index:<6} {short_name:<35} {before:<8.3f} {after:<8.3f} {change_emoji}{change:+.3f} {update_type}")
            direction = "+" if change > 0 else ""


        # Summary statistics for changes#
        primary_changes = [x[4] for x in all_changes if x[0] in primary_topic_indices]
        area_effect_changes = [x[4] for x in all_changes if x[0] in area_effect_indices]

        print(f"\nChange Statistics:")
        if primary_changes:
            print(f"  Primary topic changes: {len(primary_changes)} topics")
            print(f"    Average change: {np.mean(primary_changes):+.3f}")
            print(f"    Largest change: {max(primary_changes, key=abs):+.3f}")

        if area_effect_changes:
            print(f"  Area effect changes: {len(area_effect_changes)} topics")
            print(f"    Average change: {np.mean(area_effect_changes):+.3f}")
            print(f"    Largest change: {max(area_effect_changes, key=abs):+.3f}")
        # Area of effect analysis
        if total_area_updates > 0:
            max_spread = max(r['area_analysis']['area_effect_count'] for r in session_results)
            avg_spread = total_area_updates / len(session_results)

            print(f"\nArea of Effect Analysis:")
            print(f"  Total propagated updates: {total_area_updates}")
            print(f"  Average spread per question: {avg_spread:.1f} topics")
            print(f"  Maximum spread: {max_spread} topics")

            print(f"\nKnowledge propagation patterns:")
            for i, result in enumerate(session_results, 1):
                if result['area_analysis']['area_effect_count'] > 0:
                    mcq = kg.mcqs.get(result['mcq_id'])
                    primary_topic = kg.get_topic_of_index(mcq.main_topic_index)
                    spread_count = result['area_analysis']['area_effect_count']
                    accuracy = "✅ Correct" if result['is_correct'] else "❌ Incorrect"
                    print(f"  Q{i} ({accuracy}): {primary_topic[:25]}... → {spread_count} connected topics")

        # Final student statistics
        stats = student_manager.get_student_statistics(student_id)
        print(f"\nFinal Learning Profile:")
        print(f"  Overall success rate: {stats['success_rate']*100:.1f}%")
        print(f"  Total questions attempted: {stats['total_questions']}")
        print(f"  Average mastery level: {stats['average_mastery']:.3f}")
        print(f"  Topics with high mastery (>0.6): {sum(1 for m in after_masteries.values() if m > 0.6)}")

        # Confidence-mastery correlation
        mastery_values = list(after_masteries.values())
        confidence_values = list(student.confidence_levels.values())
        if len(mastery_values) > 0 and len(confidence_values) > 0:
            correlation = np.corrcoef(mastery_values, confidence_values)[0, 1]
            print(f"  Mastery-Confidence correlation: {correlation:.3f}")
        # Generate visualization
        '''
        visualize_knowledge_graph(kg, student_manager, student_id,
                                 before_masteries=before_masteries,
                                 after_masteries=after_masteries,
                                 title_suffix="(Session Results)")
        '''

        #test_greedy_algorithm_functionality()
    except NameError as e:
        print(f"Error: Required classes not found - {e}")
        print("Please ensure the following classes are imported:")
        print("KnowledgeGraph, StudentManager, MCQScheduler, BayesianKnowledgeTracing")
        print("\nImport with:")
        print("from kg_code_withameila import KnowledgeGraph, StudentManager, MCQScheduler, BayesianKnowledgeTracing")

    except Exception as e:
        print(f"Error during system execution: {e}")
        print("Please check your system configuration and try again.")



if __name__ == "__main__":
    # Run the main test system
    run_knowledge_graph_test()
