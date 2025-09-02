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
from typing import Dict, List, Set, Tuple, Optional, Union, Any
from fractions import Fraction
from dataclasses import dataclass, field
from datetime import datetime
import math
import json
import random
import re
from sympy import ( sqrt, Poly, sympify, expand, factor, simplify, collect, symbols, latex, Rational,gcd, lcm, factorial, isprime, factorint, Abs, floor, ceiling, Mod,diff, integrate, limit, series, solve, roots,sin, cos, tan, asin, acos, atan, sec, csc, cot, pi, E, deg, rad, log, exp,cancel, apart, together, nsimplify
)

x, a, b, c, d, r_1, r_2 = symbols('x a b c d r_1 r_2')
local_namespace = {
    'x': x, 'a': a, 'b': b, 'c': c, 'r_1': r_1, 'r_2': r_2,
    'sin': sin, 'cos': cos, 'tan': tan, 'pi': pi, 'sqrt': sqrt,
    'log': log, 'exp': exp, 'E': E, 'gcd':gcd
}


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
    difficulty_breakdown: 'DifficultyBreakdown'
    # Optional: only load if actually needed
    text: Optional[str] = None  # Only for display/debugging
    chapter: Optional[str] = None

    is_parameterized: bool = False #?

    has_breakdown: bool = False
    breakdown_options: List[int] = field(default_factory=list)

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

        self._breakdown_stats = {
            'total_with_breakdown': 0,
            'by_topic': {}
        }

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
                difficulty_breakdown = DifficultyBreakdown.from_dict(mcq_data['difficulty_breakdown'])

                # Use precomputed values directly - no calculations
                minimal_data = MinimalMCQData(
                    id=mcq_id,
                    main_topic_index=mcq_data['main_topic_index'],
                    subtopic_weights=subtopic_weights,
                    difficulty=mcq_data['overall_difficulty'],  # Direct use
                    prerequisites=prerequisites,  # Direct use
                    difficulty_breakdown=difficulty_breakdown,
                    chapter=mcq_data.get('chapter'),
                    is_parameterized=mcq_data.get('is_parameterized', False)
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
class BreakdownStep:
    """Represents a single step in a question breakdown"""
    step_no: int
    step_type: str
    text: str
    options: List[str]
    correctindex: int
    option_explanations: List[str]
    prereq_topics: List[int] = field(default_factory=list)
    subquestion_expression: Optional[str] = None
    calculated_parameters: Optional[Dict[str, str]] = field(default_factory=dict)

    # Inherited from parent MCQ
    parent_mcq: 'MCQ' = None
    parent_generated_parameters: Dict[str, Dict] = field(default_factory=dict)
    parent_calculated_parameters: Dict[str, str] = field(default_factory=dict)
    parent_params: Dict[str, Union[int, float]] = field(default_factory=dict)
    parent_question_expression: Optional[str] = None

    def __post_init__(self):
        """Process step data after initialization"""
        # Merge parent and step-specific calculated parameters
        self.all_calculated_parameters = {
            **self.parent_calculated_parameters,
            **self.calculated_parameters
        }

    @classmethod
    def from_dict(cls, step_data: Dict, parent_mcq: 'MCQ') -> 'BreakdownStep':
        """Create BreakdownStep from dictionary with parent MCQ context"""
        return cls(
            step_no=step_data['step_no'],
            step_type=step_data['step_type'],
            text=step_data['text'],
            options=step_data['options'],
            correctindex=step_data['correctindex'],
            option_explanations=step_data['option_explanations'],
            prereq_topics=step_data.get('prereq_topics', []),
            subquestion_expression=step_data.get('subquestion_expression'),
            calculated_parameters=step_data.get('calculated_parameters', {}),
            parent_generated_parameters=parent_mcq.generated_parameters or {},
            parent_calculated_parameters=parent_mcq.calculated_parameters or {},
            parent_params=parent_mcq.get_current_parameters_safe(),
            parent_question_expression=parent_mcq.question_expression,
            parent_mcq=parent_mcq
        )

    def should_skip(self, student_mastery: Dict[int, float], config: Dict) -> bool:
        """Check if this step should be skipped based on prerequisite mastery"""
        if not self.prereq_topics:
            return False

        mastery_threshold = config.get('prerequisite_skip_threshold', 0.8)

        for topic_id in self.prereq_topics:
            if student_mastery.get(topic_id, 0.0) > mastery_threshold:
                return True

        return False

    def render_step_text(self) -> str:
        """Render step text with parameter substitution using parent MCQ's method"""
        # Get fresh parameters from parent MCQ to ensure consistency
        if self.parent_mcq:
            fresh_parent_params = self.parent_mcq.get_current_parameters_safe()
            print(f"🔄 Using fresh parent params: {fresh_parent_params}")
        else:
            fresh_parent_params = self.parent_params  # Fallback to stored params
            print(f"📦 Using stored params: {fresh_parent_params}")

        return self._generate_step_text_with_substitution(self.text, fresh_parent_params)



    def _generate_step_text_with_substitution(self, text: str, params: Dict) -> str:
        """Generate step text using the SAME logic as generate_question_text"""
        if not params or not text:
            return text

        result_text = text

        # Handle question_expression variants (SAME as generate_question_text)
        if hasattr(self, 'parent_question_expression') and self.parent_question_expression:
            placeholders = [
                ('${question_expression_expanded}', 'expanded'),
                ('${question_expression_factored}', 'factored'),
                ('${question_expression_simplified}', 'simplified'),
                ('${question_expression_collected}', 'collected'),
                ('${question_expression}', 'as_is')
            ]

            for placeholder, format_type in placeholders:
                if placeholder in result_text:
                    try:
                        local_namespace = {'__builtins__': {}}

                        # Create SymPy-safe parameter dictionary
                        # Only include numeric parameters
                        sympy_safe_params = {}
                        for key, value in params.items():
                            try:
                                if isinstance(value, (int, float)):
                                    sympy_safe_params[key] = value
                                elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):  # Fraction
                                    sympy_safe_params[key] = Rational(value.numerator, value.denominator)
                                # Skip strings, complex objects, etc.
                                elif isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                                    # Handle coefficient lists - keep as list for indexing
                                    sympy_safe_params[key] = value
                                elif isinstance(value, str) and not ('\\' in value or callable(value)):  # ✅ ALLOW clean strings but skip LaTeX and function-like strings
                                    sympy_safe_params[key] = value  # Keep string parameters for substitution
                                # Skip problematic types that cause 'subs' errors
                                elif hasattr(value, 'subs') or callable(value):
                                    continue  # Skip SymPy objects and functions
                                elif callable(value):  # Function objects
                                    continue
                                elif hasattr(value, '__call__'):  # More function detection
                                    continue
                                elif str(type(value)).startswith('<function'):  # Function type detection
                                    continue
                                elif isinstance(value, (list, dict, tuple)) and not all(isinstance(x, (int, float)) for x in value):
                                    continue
                                else:
                                    # Try to convert unknown types to float
                                    try:
                                        # Check if it's a numeric type we can safely convert
                                        if hasattr(value, '__float__') and not callable(value):
                                            sympy_safe_params[key] = float(value)
                                        elif hasattr(value, '__int__') and not callable(value):
                                            sympy_safe_params[key] = int(value)
                                    except (ValueError, TypeError, AttributeError):
                                        # Skip if can't convert safely
                                        continue

                            except Exception:
                                # Skip any parameter that causes issues during type checking
                                continue

                        # Debug output to see what's being used
                        if len(sympy_safe_params) != len(params):
                            filtered_out = set(params.keys()) - set(sympy_safe_params.keys())
                            print(f"   Filtered out parameters: {filtered_out}")
                            print(f"   Using safe parameters: {list(sympy_safe_params.keys())}")
                        latex_expr = ""
                        # Handle equations separately
                        if '=' in self.parent_question_expression:
                            left_side, right_side = self.parent_question_expression.split('=', 1)
                            left_expr = sympify(left_side.strip(), locals=local_namespace)
                            right_expr = sympify(right_side.strip(), locals=local_namespace)

                            left_sub = left_expr.subs(sympy_safe_params)
                            right_sub = right_expr.subs(sympy_safe_params)

                            # Apply format
                            if format_type == 'expanded':
                                left_proc = expand(left_sub)
                                right_proc = expand(right_sub)
                            elif format_type == 'factored':
                                left_proc = factor(left_sub)
                                right_proc = factor(right_sub)
                            elif format_type == 'simplified':
                                left_proc = simplify(left_sub)
                                right_proc = simplify(right_sub)
                            elif format_type == 'collected':
                                left_proc = collect(left_sub, symbols('x'))
                                right_proc = collect(right_sub, symbols('x'))
                            else:
                                left_proc = left_sub
                                right_proc = right_sub

                            # Convert both sides to LaTeX
                            left_latex = latex(left_proc)
                            right_latex = latex(right_proc)
                            # Clean signs
                            left_latex = left_latex.replace('+ -', '- ').replace('- -', '+ ')
                            right_latex = right_latex.replace('+ -', '- ').replace('- -', '+ ')

                            latex_expr = f"{left_latex} = {right_latex}"

                        else:
                            if self.parent_question_expression in params:
                                # This is a parameter name that should be substituted
                                expr = symbols(self.parent_question_expression)
                            else:
                                # This is a mathematical expression to be parsed
                                expr = sympify(self.parent_question_expression, locals=local_namespace)
                            substituted = expr.subs(sympy_safe_params)
                            if format_type == 'expanded':
                                processed = expand(substituted)
                            elif format_type == 'factored':
                                processed = factor(substituted)
                            elif format_type == 'simplified':
                                processed = simplify(substituted)
                            elif format_type == 'collected':
                                processed = collect(substituted, symbols('x'))
                            else:
                                processed = substituted

                            latex_expr = latex(processed)
                            latex_expr = latex_expr.replace('+ -', '- ').replace('- -', '+ ')

                        # Replace placeholder with formatted expression wrapped in $...$
                        result_text = result_text.replace(placeholder, f"\\({latex_expr}\\)")

                    except Exception as e:
                        print(f"⚠️ Error processing question_expression: {e}")
                        # Fallback: do naive substitution of parameters
                        fallback_expr = self.parent_question_expression
                        for pname, pvalue in sympy_safe_params.items():
                            if not pname.endswith('_sympy'):  # Skip SymPy objects
                                # Use smart formatting for parameter values
                                formatted_pvalue = MCQ.smart_format_number(pvalue)
                                fallback_expr = fallback_expr.replace(str(pname), formatted_pvalue)
                        fallback_expr = fallback_expr.replace('+ -', '- ').replace('- -', '+ ')
                        result_text = result_text.replace(placeholder, f"\\({fallback_expr}\\)")

            for placeholder, format_type in placeholders:
                if placeholder in result_text:
                    try:
                        # FIXED: Use the same parameter vs expression logic
                        if self.parent_question_expression in params:
                            # This is a parameter name that should be substituted
                            processed = MCQ.smart_format_number(params[self.parent_question_expression])
                        else:
                            # This is a mathematical expression to be processed
                            processed = self._process_expression_with_sympy(
                                self.parent_question_expression, format_type, params
                            )

                        result_text = result_text.replace(placeholder, f"\\({processed}\\)")

                    except Exception as e:
                        print(f"⚠️ Error processing question_expression: {e}")
                        # Use the same fallback as generate_question_text
                        fallback_expr = self.parent_question_expression
                        for pname, pvalue in params.items():
                            if isinstance(pvalue, (int, float)):
                                formatted_pvalue = MCQ.smart_format_number(pvalue)
                                fallback_expr = fallback_expr.replace(str(pname), formatted_pvalue)
                        result_text = result_text.replace(placeholder, f"${fallback_expr}$")

        # Handle subquestion_expression variants (SAME pattern)
        if hasattr(self, 'subquestion_expression') and self.subquestion_expression and self.subquestion_expression.strip():
            subq_placeholders = [
                ('${subquestion_expression_expanded}', 'expanded'),
                ('${subquestion_expression_factored}', 'factored'),
                ('${subquestion_expression_simplified}', 'simplified'),
                ('${subquestion_expression_collected}', 'collected'),
                ('${subquestion_expression}', 'as_is')
                ]

            for placeholder, format_type in subq_placeholders:
                if placeholder in result_text:
                    try:
                        local_namespace = {'__builtins__': {}}

                        # Create SymPy-safe parameter dictionary
                        # Only include numeric parameters
                        sympy_safe_params = {}
                        for key, value in params.items():
                            try:
                                if isinstance(value, (int, float)):
                                    sympy_safe_params[key] = value
                                elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):  # Fraction
                                    sympy_safe_params[key] = Rational(value.numerator, value.denominator)
                                # Skip strings, complex objects, etc.
                                elif isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                                    # Handle coefficient lists - keep as list for indexing
                                    sympy_safe_params[key] = value
                                elif isinstance(value, str) and not ('\\' in value or callable(value)):  # ✅ ALLOW clean strings but skip LaTeX and function-like strings
                                    sympy_safe_params[key] = value  # Keep string parameters for substitution
                                # Skip problematic types that cause 'subs' errors
                                elif hasattr(value, 'subs') or callable(value):
                                    continue  # Skip SymPy objects and functions
                                elif callable(value):  # Function objects
                                    continue
                                elif hasattr(value, '__call__'):  # More function detection
                                    continue
                                elif str(type(value)).startswith('<function'):  # Function type detection
                                    continue
                                elif isinstance(value, (list, dict, tuple)) and not all(isinstance(x, (int, float)) for x in value):
                                    continue
                                else:
                                    # Try to convert unknown types to float
                                    try:
                                        # Check if it's a numeric type we can safely convert
                                        if hasattr(value, '__float__') and not callable(value):
                                            sympy_safe_params[key] = float(value)
                                        elif hasattr(value, '__int__') and not callable(value):
                                            sympy_safe_params[key] = int(value)
                                    except (ValueError, TypeError, AttributeError):
                                        # Skip if can't convert safely
                                        continue

                            except Exception:
                                # Skip any parameter that causes issues during type checking
                                continue

                        # Debug output to see what's being used
                        if len(sympy_safe_params) != len(params):
                            filtered_out = set(params.keys()) - set(sympy_safe_params.keys())
                            print(f"   Filtered out parameters: {filtered_out}")
                            print(f"   Using safe parameters: {list(sympy_safe_params.keys())}")
                        latex_expr = ""
                        # Handle equations separately
                        if '=' in self.subquestion_expression:
                            left_side, right_side = self.subquestion_expression.split('=', 1)
                            left_expr = sympify(left_side.strip(), locals=local_namespace)
                            right_expr = sympify(right_side.strip(), locals=local_namespace)

                            left_sub = left_expr.subs(sympy_safe_params)
                            right_sub = right_expr.subs(sympy_safe_params)

                            # Apply format
                            if format_type == 'expanded':
                                left_proc = expand(left_sub)
                                right_proc = expand(right_sub)
                            elif format_type == 'factored':
                                left_proc = factor(left_sub)
                                right_proc = factor(right_sub)
                            elif format_type == 'simplified':
                                left_proc = simplify(left_sub)
                                right_proc = simplify(right_sub)
                            elif format_type == 'collected':
                                left_proc = collect(left_sub, symbols('x'))
                                right_proc = collect(right_sub, symbols('x'))
                            else:
                                left_proc = left_sub
                                right_proc = right_sub

                            # Convert both sides to LaTeX
                            left_latex = latex(left_proc)
                            right_latex = latex(right_proc)
                            # Clean signs
                            left_latex = left_latex.replace('+ -', '- ').replace('- -', '+ ')
                            right_latex = right_latex.replace('+ -', '- ').replace('- -', '+ ')

                            latex_expr = f"{left_latex} = {right_latex}"

                        else:
                            if self.subquestion_expression in params:
                                # This is a parameter name that should be substituted
                                expr = symbols(self.subquestion_expression)
                            else:
                                # This is a mathematical expression to be parsed
                                expr = sympify(self.subquestion_expression, locals=local_namespace)
                            substituted = expr.subs(sympy_safe_params)
                            if format_type == 'expanded':
                                processed = expand(substituted)
                            elif format_type == 'factored':
                                processed = factor(substituted)
                            elif format_type == 'simplified':
                                processed = simplify(substituted)
                            elif format_type == 'collected':
                                processed = collect(substituted, symbols('x'))
                            else:
                                processed = substituted

                            latex_expr = latex(processed)
                            latex_expr = latex_expr.replace('+ -', '- ').replace('- -', '+ ')

                        # Replace placeholder with formatted expression wrapped in $...$
                        result_text = result_text.replace(placeholder, f"\\({latex_expr}\\)")

                    except Exception as e:
                        print(f"⚠️ Error processing question_expression: {e}")
                        # Fallback: do naive substitution of parameters
                        fallback_expr = self.question_expression
                        for pname, pvalue in sympy_safe_params.items():
                            if not pname.endswith('_sympy'):  # Skip SymPy objects
                                # Use smart formatting for parameter values
                                formatted_pvalue = MCQ.smart_format_number(pvalue)
                                fallback_expr = fallback_expr.replace(str(pname), formatted_pvalue)
                        fallback_expr = fallback_expr.replace('+ -', '- ').replace('- -', '+ ')
                        result_text = result_text.replace(placeholder, f"\\({fallback_expr}\\)")




        # Individual parameter substitutions (SAME as existing code)
        for param_name, param_value in params.items():
            placeholder = f'${{{param_name}}}'
            if placeholder in result_text:
                formatted_value = MCQ.smart_format_number(param_value)
                result_text = result_text.replace(placeholder, formatted_value)

        return result_text

    def _process_expression_with_sympy(self, expression: str, format_type: str, params: Dict) -> str:
        """Process mathematical expressions using SymPy - USING EXISTING LOGIC from generate_question_text"""
        from sympy import sympify, expand, factor, simplify, collect, symbols, latex, Rational

        try:
            local_namespace = {'__builtins__': {}}

            # FIXED: Use the SAME logic as generate_question_text
            # Create SymPy-safe parameters (same as existing code)
            sympy_safe_params = {}
            for key, value in params.items():
                try:
                    if isinstance(value, (int, float)):
                        sympy_safe_params[key] = value
                    elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):  # Fraction
                        sympy_safe_params[key] = Rational(value.numerator, value.denominator)
                    # Skip strings, complex objects, etc.
                except Exception:
                    continue

            #  Use the same parameter vs expression check as generate_question_text
            if expression in params:
                # This is a parameter name that should be substituted
                print(f"🔧 Treating '{expression}' as parameter name")
                expr = symbols(expression)
            else:
                # This is a mathematical expression to be parsed
                print(f"🔧 Parsing '{expression}' as mathematical expression")
                expr = sympify(expression, locals=local_namespace)

            # Apply parameter substitution
            substituted = expr.subs(sympy_safe_params)

            # Apply format transformation (same as existing code)
            if format_type == 'expanded':
                processed = expand(substituted)
            elif format_type == 'factored':
                processed = factor(substituted)
            elif format_type == 'simplified':
                processed = simplify(substituted)
            elif format_type == 'collected':
                processed = collect(substituted, symbols('x'))
            else:  # 'as_is'
                processed = substituted

            # Convert to LaTeX (same as existing code)
            latex_expr = latex(processed)
            latex_expr = latex_expr.replace('+ -', '- ').replace('- -', '+ ')
            return latex_expr

        except Exception as e:
            print(f"⚠️ SymPy processing failed: {e}")
            # FIXED: Use the same fallback as generate_question_text
            fallback_expr = expression
            for pname, pvalue in sympy_safe_params.items():
                if not pname.endswith('_sympy'):  # Skip SymPy objects
                    # Use smart formatting for parameter values
                    formatted_pvalue = MCQ.smart_format_number(pvalue)
                    fallback_expr = fallback_expr.replace(str(pname), formatted_pvalue)
            fallback_expr = fallback_expr.replace('+ -', '- ').replace('- -', '+ ')
            return fallback_expr

    def _simple_parameter_substitution(self, expression: str, params: Dict) -> str:
        """Simple parameter substitution without SymPy"""
        result = expression
        for pname, pvalue in params.items():
            if not isinstance(pvalue, str):
                formatted_pvalue = MCQ.smart_format_number(pvalue)
                result = result.replace(str(pname), formatted_pvalue)

        return result.replace('+ -', '- ').replace('- -', '+ ')

    def render_step_options(self) -> List[str]:
        """Render step options with parameter substitution and calculations"""
        # Calculate step-specific parameters
        calc_params = self._calculate_step_parameters()
        # Use fresh parameters if parent MCQ is available
        if self.parent_mcq:
            fresh_parent_params = self.parent_mcq.get_current_parameters_safe()
        else:
            fresh_parent_params = self.parent_params  # Fallback

        all_params = {**fresh_parent_params, **calc_params}

        rendered_options = []
        for option in self.options:
            rendered = self._render_step_option_sophisticated(option, all_params)
            rendered_options.append(rendered)

        return rendered_options

    def _render_step_option_sophisticated(self, option: str, all_params: Dict) -> str:
        """Render single step option with sophisticated formatting"""
        # Step 1: Parameter substitution
        substituted = self._substitute_parameters(option, all_params)

        # Step 2: Try mathematical evaluation
        try:
            if any(op in substituted for op in ['+', '-', '*', '/', '**', 'sqrt']):
                evaluated = self._evaluate_step_mathematical_expression(substituted, all_params)
                if evaluated is not None:
                    substituted = evaluated
        except:
            pass

        # Step 3:  - Apply math cleaning before LaTeX formatting
        substituted = self.parent_mcq.clean_math_expression(substituted) if self.parent_mcq else substituted

        # Step 4: LaTeX formatting
        if not (substituted.startswith('\\(') and substituted.endswith('\\)')):
            if any(char in substituted for char in ['+', '-', '*', '/', '^', '=', '<', '>', 'sqrt', 'frac']) or '\\' in substituted:
                substituted = f"\\({substituted}\\)"

        return substituted

    def _evaluate_step_mathematical_expression(self, expr: str, params: Dict) -> Optional[str]:
        """Safely evaluate mathematical expressions for steps"""
        try:
            safe_namespace = MCQ.create_safe_math_namespace({
                **params
            })

            result = eval(expr, safe_namespace)
            return MCQ.smart_format_number(result)

        except:
            return None

    def _calculate_step_parameters(self) -> Dict[str, Union[int, float]]:
        """Calculate step-specific parameters"""
        calc_params = {}

        for calc_name, calc_expr in self.all_calculated_parameters.items():
            try:
                if calc_name == calc_expr:
                    continue

                # Create safe namespace with parent parameters
                safe_namespace = MCQ.create_safe_math_namespace({
                    **self.parent_params,
                    **calc_params
                })
                calc_result = eval(calc_expr, safe_namespace)
                calc_params[calc_name] = calc_result

            except Exception as e:
                print(f"⚠️ Failed to calculate step parameter {calc_name}: {e}")
                calc_params[calc_name] = 0

        return calc_params

    def _substitute_parameters(self, text: str, params: Dict) -> str:
        """Substitute parameters using new ${param} format (no double $)"""
        result = text

        # Sort parameters by length to avoid partial matches ???
        sorted_params = sorted(params.items(), key=lambda x: len(x[0]), reverse=True)

        for param_name, param_value in sorted_params:
            # New format: ${param} (single $ for parameter substitution)
            placeholder = f'${{{param_name}}}'
            if placeholder in result:
                formatted_value = MCQ.smart_format_number(param_value)
                result = result.replace(placeholder, formatted_value)

        return result

    def _substitute_and_render_option(self, option: str, all_params: Dict) -> str:
        """Substitute parameters and render option for LaTeX display"""
        # Step 1: Parameter substitution
        substituted = self._substitute_parameters(option, all_params)

        # Step 2: LaTeX formatting (assuming options are already in LaTeX format)
        # Just wrap in LaTeX delimiters if not already wrapped
        if not (substituted.startswith('\\(') and substituted.endswith('\\)')):
            if any(char in substituted for char in ['+', '-', '*', '/', '^', '=', '<', '>']):
                substituted = f"\\({substituted}\\)"

        return substituted


    def render_step_option_explanations(self) -> List[str]:
        """Render step option explanations with parameter substitution and calculations"""
        # Calculate step-specific parameters
        calc_params = self._calculate_step_parameters()
        # Use fresh parameters if parent MCQ is available
        if self.parent_mcq:
            fresh_parent_params = self.parent_mcq.get_current_parameters_safe()
        else:
            fresh_parent_params = self.parent_params  # Fallback

        all_params = {**fresh_parent_params, **calc_params}

        rendered_explanations = []
        for explanation in self.option_explanations:
            rendered = self._render_step_explanation_sophisticated(explanation, all_params)
            rendered_explanations.append(rendered)

        return rendered_explanations


    def _render_step_explanation_sophisticated(self, explanation: str, all_params: Dict) -> str:
        """Render single step explanation with sophisticated formatting and cleaning"""
        # Step 1: Parameter substitution
        substituted = self._substitute_parameters(explanation, all_params)

        # Step 2: Try mathematical evaluation
        try:
            if any(op in substituted for op in ['+', '-', '*', '/', '**', 'sqrt']):
                evaluated = self._evaluate_step_mathematical_expression(substituted, all_params)
                if evaluated is not None:
                    substituted = evaluated
        except:
            pass

        # Step 3: Apply math cleaning (key fix for breakdown steps too)
        substituted = self.parent_mcq.clean_math_expression(substituted) if self.parent_mcq else substituted

        # Step 4: LaTeX formatting
        if not (substituted.startswith('\\(') and substituted.endswith('\\)')):
            if any(char in substituted for char in ['+', '-', '*', '/', '^', '=', '<', '>', 'sqrt', 'frac']) or '\\' in substituted:
                substituted = f"\\({substituted}\\)"

        return substituted


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

    overall_difficulty: float  # Store directly from JSON
    prerequisites: Dict[int, float]

    # optional fields for parameterization
    question_expression: Optional[str] = None
    generated_parameters: Optional[Dict[str, Dict]] = None
    calculated_parameters: Optional[Dict[str, str]] = None

    # Cache for generated parameters (not saved to JSON)
    _current_params: Optional[Dict] = field(default=None, init=False)
    _is_parameterized: Optional[bool] = field(default=None, init=False)

    breakdown: Optional[Dict[str, Dict]] = None

    @staticmethod
    def create_safe_math_namespace(base_params: Dict = None) -> Dict:
        """Create a standardized safe namespace with common math functions"""
        safe_namespace = {
            '__builtins__': {},
            # Math functions
            'sqrt': lambda x: x**0.5,
            'round': round,
            'int': int,
            'float': float,
            'sum': sum,
            'len': len,

        # Basic arithmetic & comparison
        'abs': Abs, 'max': max, 'min': min, 'round': round,

        # Number theory
        'gcd': gcd, 'lcm': lcm, 'factorial': factorial,
        'isprime': isprime, 'factorint': factorint,
        'floor': floor, 'ceiling': ceiling, 'mod': Mod,

        # Calculus
        'diff': diff, 'integrate': integrate, 'limit': limit,
        'solve': solve, 'roots': roots,

        # Trigonometry
        'sin': sin, 'cos': cos, 'tan': tan,
        'asin': asin, 'acos': acos, 'atan': atan,
        'sec': sec, 'csc': csc, 'cot': cot,

        # Constants
        'pi': pi, 'e': E,

        # Logarithms & exponentials
        'log': log, 'ln': log, 'exp': exp,
        'sqrt': sqrt, 'pow': pow,

        # Rational functions
        'cancel': cancel,
        }
        if base_params:
            safe_namespace.update(base_params)

        return safe_namespace

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

        breakdown = data.get('breakdown', None)


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
            prerequisites=prerequisites,
            question_expression=data.get('question_expression'),
            generated_parameters=data.get('generated_parameters', {}),
            calculated_parameters=data.get('calculated_parameters', {}),
            breakdown=breakdown
        )
    def _generate_parameters(self) -> Dict:
        """Generates random parameters for questions based on constraints"""
        if not self.generated_parameters:
            return {}

        for attempt in range(100):  # Try up to 100 times
            params = {}
            success = True

            # generate all parameters, then check constraints
            for param_name, config in self.generated_parameters.items():
                try:
                    if config['type'] == 'int':
                        # VALIDATE: Check for invalid range
                        if config['min'] > config['max']:

                            print(f"Warning: Invalid range for {param_name}: min={config['min']} > max={config['max']}")
                            success = False
                            break
                        min_val = config['min']
                        max_val = config['max']
                        exclude = config.get('exclude', [])

                        # Handle single exclude value
                        if not isinstance(exclude, list):
                            exclude = [exclude]

                        # Generate valid values
                        valid_values = [x for x in range(min_val, max_val + 1) if x not in exclude]

                        if not valid_values:
                            raise ValueError(f"No valid values for parameter {param_name}")

                        params[param_name] = random.choice(valid_values)

                    elif config['type'] == 'float':
                        min_val = config['min']
                        max_val = config['max']
                        params[param_name] = random.uniform(min_val, max_val)

                    elif config['type'] == 'choice':
                        if not config.get('choices'):
                            print(f"Warning: No choices provided for parameter {param_name}")
                            success = False
                            break
                        params[param_name] = random.choice(config['choices'])

                    elif config['type'] == 'fraction':
                        # Fraction type
                        fraction_value = self._generate_fraction_parameter(config)
                        params[param_name] = fraction_value

                        # Store components for easier access
                        params[f"{param_name}_num"] = fraction_value.numerator
                        params[f"{param_name}_den"] = fraction_value.denominator
                        params[f"{param_name}_float"] = float(fraction_value)

                    elif config['type'] == 'decimal':
                        # Decimal type
                        value = self._generate_decimal_parameter(config)
                        params[param_name] = value

                    elif config['type'] == 'angle':
                        # Angle type - returns dict with multiple representations
                        angle_data = self._generate_angle_parameter(config)
                        params[param_name] = angle_data['value'] # Primary value
                        # Add conversion parameters for use in expressions
                        params[f"{param_name}_degrees"] = angle_data['degrees']
                        params[f"{param_name}_radians"] = angle_data['radians']
                        params[f"{param_name}_unit"] = angle_data['unit']

                    elif config['type'] == 'polynomial':
                        poly_data = self._generate_polynomial_parameter(config)
                        params[param_name] = poly_data['expression']  # String expression
                        params[f"{param_name}_coeffs"] = poly_data['coefficients']  # List of numbers
                        params[f"{param_name}_degree"] = poly_data['degree']  # Integer
                        coeffs = poly_data['coefficients']
                        for i, coeff in enumerate(coeffs):
                            params[f"{param_name}_coeff_{i}"] = coeff

                    elif config['type'] == 'function':
                        # Function type - returns dict with function components
                        func_data = self._generate_function_parameter(config)
                        value = func_data['expression']  # Primary expression string
                        params[param_name] = func_data['expression']
                        # Add function parameters for use in calculations
                        for key, val in func_data['parameters'].items():
                            params[f"{param_name}_{key}"] = val
                        params[f"{param_name}_type"] = func_data['function_type']
                    else:
                        print(f"Warning: Unknown parameter type '{config['type']}' for {param_name}")
                        success = False
                        break
                except Exception as e:
                    print(f"Warning: Error generating parameter {param_name}: {e}")
                    success = False
                    break

            if not success:
                continue

            # Now check all exclude constraints
            all_constraints_met = True
            for param_name, config in self.generated_parameters.items():
                exclude_rule = config.get('exclude')
                if exclude_rule is not None:
                    if isinstance(exclude_rule, str):
                        # Reference to another parameter
                        if exclude_rule in params:
                            if params[param_name] == params[exclude_rule]:
                                all_constraints_met = False
                                break
                    elif isinstance(exclude_rule, list):
                        # List of excluded values
                        if params[param_name] in exclude_rule:
                            all_constraints_met = False
                            break
                    elif isinstance(exclude_rule, (int, float)):
                        # Single excluded value
                        if params[param_name] == exclude_rule:
                            all_constraints_met = False
                            break

            if not all_constraints_met:
                continue  # Try again

            # Calculate derived parameters
            try:
                if self.calculated_parameters:
                    for calc_name, calc_expr in self.calculated_parameters.items():
                        try:
                            # Check for self-referential calculated parameters (common bug)
                            if calc_name == calc_expr:
                                print(f"Warning: Self-referential calculated parameter: {calc_name} = {calc_expr}")
                                continue

                            # Create safe evaluation environment
                            local_namespace = {'__builtins__': {}}

                            safe_namespace = MCQ.create_safe_math_namespace({**params})
                            calc_result = eval(calc_expr, {"__builtins__": {}}, safe_namespace)
                            params[calc_name] = calc_result
                        except Exception as e:
                            print(f"Warning: Error calculating parameter {calc_name} with expression '{calc_expr}': {e}")
                            # For debugging: show available parameters
                            if attempt == 0:  # Only show on first attempt to avoid spam
                                print(f"Available parameters: {list(params.keys())}")
                            # Skip this calculated parameter rather than failing entirely
                            continue

                return params

            except Exception as e:
                continue  # Try again if calculation fails

        # If we get here, we failed to generate valid parameters
        print("Warning: Could not generate valid parameters after 100 attempts")
        return self._generate_fallback_parameters()

    def _generate_fraction_parameter(self, config: Dict[str, Any]) -> Fraction:
        """Generate a fraction parameter with specified constraints."""
        # Set defaults
        num_min = config.get('numerator_min', -12)
        num_max = config.get('numerator_max', 12)
        den_min = config.get('denominator_min', 1)
        den_max = config.get('denominator_max', 8)
        exclude_num = config.get('exclude_numerator', [])
        exclude_den = config.get('exclude_denominator', [0])
        reduce_fraction = config.get('reduce', True)
        proper_only = config.get('proper_only', False)

        # Generate valid numerator
        valid_numerators = [n for n in range(num_min, num_max + 1) if n not in exclude_num]
        numerator = random.choice(valid_numerators)

        # Generate valid denominator
        valid_denominators = [d for d in range(den_min, den_max + 1) if d not in exclude_den]
        denominator = random.choice(valid_denominators)

        # Handle proper fraction constraint
        if proper_only and abs(numerator) >= abs(denominator):
            max_num = min(abs(denominator) - 1, num_max)
            min_num = max(-max_num, num_min)
            valid_numerators = [n for n in range(min_num, max_num + 1) if n not in exclude_num]
            if valid_numerators:
                numerator = random.choice(valid_numerators)

        fraction = Fraction(numerator, denominator)
        return fraction if reduce_fraction else Fraction(numerator, denominator)

    def _generate_decimal_parameter(self, config: Dict[str, Any]) -> float:
        """Generate a decimal parameter with controlled precision."""
        min_val = config.get('min', -100.0)
        max_val = config.get('max', 100.0)
        decimal_places = config.get('decimal_places', 2)
        step = config.get('step', 0.01)
        exclude = config.get('exclude', [])

        # Calculate number of steps
        num_steps = int((max_val - min_val) / step)

        # Generate using steps to ensure precise decimal values
        for _ in range(100):  # Max attempts
            step_number = random.randint(0, num_steps)
            value = min_val + step_number * step
            value = round(value, decimal_places)

            if value not in exclude and min_val <= value <= max_val:
                return value

        return round(min_val, decimal_places)  # Fallback

    def _generate_angle_parameter(self, config: Dict[str, Any]) -> Dict[str, float]:
        """Generate an angle parameter with unit handling."""
        angle_type = config.get('type', 'degrees')
        special_angles_only = config.get('special_angles_only', False)
        quadrant = config.get('quadrant', None)  # 1-4, or None for any

        if special_angles_only:
            if angle_type == 'degrees':
                special_angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
            else:  # radians
                special_angles = [0, math.pi/6, math.pi/4, math.pi/3, math.pi/2,
                                2*math.pi/3, 3*math.pi/4, 5*math.pi/6, math.pi,
                                7*math.pi/6, 5*math.pi/4, 4*math.pi/3, 3*math.pi/2,
                                5*math.pi/3, 7*math.pi/4, 11*math.pi/6, 2*math.pi]

            # Filter by quadrant if specified
            if quadrant:
                if angle_type == 'degrees':
                    quadrant_ranges = {
                        1: (0, 90), 2: (90, 180), 3: (180, 270), 4: (270, 360)
                    }
                else:
                    quadrant_ranges = {
                        1: (0, math.pi/2), 2: (math.pi/2, math.pi),
                        3: (math.pi, 3*math.pi/2), 4: (3*math.pi/2, 2*math.pi)
                    }

                min_range, max_range = quadrant_ranges[quadrant]
                special_angles = [a for a in special_angles if min_range <= a <= max_range]

            angle_value = random.choice(special_angles)
        else:
            # Generate any angle
            if angle_type == 'degrees':
                min_angle, max_angle = 0, 360
            else:
                min_angle, max_angle = 0, 2*math.pi

            if quadrant:
                if angle_type == 'degrees':
                    quadrant_ranges = {
                        1: (0, 90), 2: (90, 180), 3: (180, 270), 4: (270, 360)
                    }
                else:
                    quadrant_ranges = {
                        1: (0, math.pi/2), 2: (math.pi/2, math.pi),
                        3: (math.pi, 3*math.pi/2), 4: (3*math.pi/2, 2*math.pi)
                    }
                min_angle, max_angle = quadrant_ranges[quadrant]

            if angle_type == 'degrees':
                angle_value = random.randint(int(min_angle), int(max_angle))
            else:
                angle_value = random.uniform(min_angle, max_angle)

        # Convert to both formats
        if angle_type == 'degrees':
            degrees = angle_value
            radians = math.radians(angle_value)
        else:
            radians = angle_value
            degrees = math.degrees(angle_value)

        return {
            'value': angle_value,
            'degrees': degrees,
            'radians': radians,
            'unit': angle_type
        }


    def _generate_polynomial_parameter(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a polynomial parameter with specified constraints."""
        degree = config.get('degree', 2)
        variable = config.get('variable', 'x')
        coeff_min = config.get('coefficient_min', -5)
        coeff_max = config.get('coefficient_max', 5)
        leading_coeff_exclude = config.get('leading_coefficient_exclude', [0])
        monic = config.get('monic', False)
        integer_coeffs = config.get('integer_coeffs', True)

        coefficients = []

        # Generate leading coefficient (ensure non-zero unless monic)
        if monic:
            coefficients.append(1)
        else:
            valid_leading = [x for x in range(coeff_min, coeff_max + 1) if x not in leading_coeff_exclude]
            coefficients.append(random.choice(valid_leading))

        # Generate remaining coefficients
        for i in range(degree):
            if integer_coeffs:
                coeff = random.randint(coeff_min, coeff_max)
            else:
                coeff = random.uniform(coeff_min, coeff_max)
            coefficients.append(coeff)

        # Build expression string
        terms = []
        for i, coeff in enumerate(coefficients):
            power = degree - i

            if coeff == 0:
                continue

            if power == 0:
                terms.append(str(coeff))
            elif power == 1:
                if coeff == 1:
                    terms.append(variable)
                elif coeff == -1:
                    terms.append(f"-{variable}")
                else:
                    terms.append(f"{coeff}*{variable}")
            else:
                if coeff == 1:
                    terms.append(f"{variable}**{power}")
                elif coeff == -1:
                    terms.append(f"-{variable}**{power}")
                else:
                    terms.append(f"{coeff}*{variable}**{power}")

        expression = " + ".join(terms).replace(" + -", " - ")
        if not expression:
            expression = "0"

        return {
            'expression': expression,
            'coefficients': coefficients,
            'degree': degree,
            'variable': variable
        }

    def _generate_function_parameter(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a mathematical function parameter."""
        func_type = config.get('function_type', 'linear')
        domain_min = config.get('domain_min', -10)
        domain_max = config.get('domain_max', 10)
        param_ranges = config.get('parameter_ranges', {})


        if func_type == 'linear':
            # f(x) = mx + b
            m = random.randint(param_ranges.get('slope_min', -5), param_ranges.get('slope_max', 5))
            b = random.randint(param_ranges.get('intercept_min', -10), param_ranges.get('intercept_max', 10))

            parameters = {'slope': m, 'y_intercept': b}
            expression = f"{m}*x + {b}".replace("+ -", "- ")

        elif func_type == 'quadratic':
            # f(x) = ax² + bx + c
            a = random.randint(param_ranges.get('a_min', -3), param_ranges.get('a_max', 3))
            b = random.randint(param_ranges.get('b_min', -5), param_ranges.get('b_max', 5))
            c = random.randint(param_ranges.get('c_min', -10), param_ranges.get('c_max', 10))

            if a == 0:  # Ensure it's actually quadratic
                a = 1

            expression = f"{a}*x**2 + {b}*x + {c}".replace("+ -", "- ")
            parameters = {'a': a, 'b': b, 'c': c}

        elif func_type == 'exponential':
            # f(x) = a * b^x
            a = random.randint(param_ranges.get('coefficient_min', 1), param_ranges.get('coefficient_max', 5))
            b = random.choice([2, 3, 5, 10] if 'bases' not in param_ranges else param_ranges['bases'])

            expression = f"{a} * {b}**x"
            parameters = {'coefficient': a, 'base': b}

        else:  # Default to linear if unknown type
            m, b = 1, 0
            expression = "x"
            parameters = {'slope': m, 'y_intercept': b}

        return {
            'expression': expression,
            #'sympy_expr': sympy_expr,
            'function_type': func_type,
            'parameters': parameters,
            'domain_min': domain_min,
            'domain_max': domain_max
        }

    def _generate_fallback_parameters(self) -> Dict:
        """ fallback parameter generation"""
        print(f"Generating fallback parameters for question ID: {getattr(self, 'id', 'unknown')}")
        params = {}

        for name, rule in self.generated_parameters.items():
            try:
                if rule['type'] == 'int':
                    # Use minimum value as safe fallback
                    params[name] = rule.get('min', 1)

                elif rule['type'] == 'choice':
                    # Use first choice as fallback
                    choices = rule.get('choices', ['default'])
                    params[name] = choices[0]

                elif rule['type'] == 'fraction':
                    # Create safe fraction fallback
                    from fractions import Fraction
                    fallback_fraction = Fraction(1, 1)  # Default to 1/1
                    params[name] = fallback_fraction
                    params[f"{name}_num"] = fallback_fraction.numerator
                    params[f"{name}_den"] = fallback_fraction.denominator
                    params[f"{name}_float"] = float(fallback_fraction)

                elif rule['type'] == 'decimal':
                    params[name] = rule.get('min', 1.0)

                elif rule['type'] == 'angle':
                    params[name] = 0
                    params[f"{name}_degrees"] = 0
                    params[f"{name}_radians"] = 0
                    params[f"{name}_unit"] = 'degrees'

                elif rule['type'] == 'polynomial':
                    params[name] = 'x'
                    params[f"{name}_coeffs"] = [1, 0]  # x + 0
                    params[f"{name}_degree"] = 1

                    coeffs = [1, 0]  # Default fallback coefficients
                    for i, coeff in enumerate(coeffs):
                        params[f"{name}_coeff_{i}"] = coeff

                elif rule['type'] == 'function':
                    params[name] = 'x'
                    params[f"{name}_m"] = 1
                    params[f"{name}_b"] = 0
                    params[f"{name}_type"] = 'linear'

                else:
                    params[name] = 1  # Generic fallback

            except Exception as e:
                print(f"Warning: Error in fallback for parameter {name}: {e}")
                params[name] = 1

        # Calculate derived parameters for fallback ?????????????????????
        for calc_name, calc_expr in (self.calculated_parameters or {}).items():
            try:


                # Try mathematical evaluation
                local_namespace = {'__builtins__': {}}

                # Convert to SymPy-compatible parameters
                sympy_params = {}
                for key, value in params.items():
                    if isinstance(value, (int, float)):
                        sympy_params[key] = sympify(value)
                    elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):  # Fraction
                        sympy_params[key] = sympify(f"{value.numerator}/{value.denominator}")

                expr = sympify(calc_expr, locals=local_namespace)
                result = expr.subs(sympy_params)

                # Convert result to appropriate type
                if hasattr(result, 'is_number') and result.is_number:
                    if result.is_integer:
                        params[calc_name] = int(result)
                    else:
                        params[calc_name] = float(result)

            except Exception as e:
                print(f"Warning: Error in fallback calculation for {calc_name}: {e}")
                # Store as literal string if mathematical evaluation fails
                params[calc_name] = calc_expr
        return params



    @staticmethod
    def smart_format_number(value: Union[int, float, Fraction]) -> str:
        """
        Smart number formatting that prefers clean representations
        """
        if isinstance(value, str):
            return str(value)

        elif isinstance(value, int):
            return str(value)

        elif isinstance(value, float):
            # Check if it's actually a whole number
            if abs(value - round(value)) < 1e-10:
                return str(int(round(value)))

            # Check if it's a simple fraction
            frac = Fraction(value).limit_denominator(100)  # Max denominator 100

            # Use fraction if it's exact and has a reasonable denominator
            if abs(float(frac) - value) < 1e-10 and frac.denominator <= 50:
                if frac.denominator == 1:
                    return str(frac.numerator)
                else:
                    return f"\\frac{{{frac.numerator}}}{{{frac.denominator}}}"

            # For unavoidable decimals, limit precision
            if abs(value) < 1e-6:
                return "0"  # Very small values become 0
            elif abs(value - round(value, 1)) < 1e-10:
                return str(round(value, 1))  # 1 decimal place if exact
            elif abs(value - round(value, 2)) < 1e-10:
                return str(round(value, 2))  # 2 decimal places if exact
            else:
                return str(round(value, 4))  # Max 4 decimal places

        elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):
            # Already a fraction
            num, den = value.numerator, value.denominator
            if den == 1:
                return str(num)
            else:
                return f"\\frac{{{num}}}{{{den}}}"

        elif hasattr(value, 'p') and hasattr(value, 'q'):  # SymPy Rational
            # Convert SymPy Rational to proper fraction format
            if value.q == 1:
                return str(value.p)
            else:
                return f"\\frac{{{value.p}}}{{{value.q}}}"

        else:
            return str(value)

    def ensure_parameters_cached(self) -> None:
        """Ensure parameters are generated and cached for consistent use"""
        if self.is_parameterized:
            if self._current_params is None:
                self._current_params = self._generate_parameters()
            else:
                print(f"⚡ Parameters already cached for MCQ {self.id}: {self._current_params}")
        else:
            print(f"📝 MCQ {self.id} is not parameterized")

    def generate_question_text(self, text: str, params: Dict) -> str:
        """
        Generate the final question text by substituting parameters and
        evaluating the question expression in different formats.

        Supports:
        - Parameter placeholders like ${a}$, ${b}$
        - Derived/calculated parameters
        - Question expressions in expanded, factored, simplified, collected, or as-is form
        - Proper LaTeX formatting
        """
        if not params or not text:
            return text

        # Start with text to modify
        result_text = text
        # Define question expression placeholders and formats
        placeholders = [
            ('${question_expression_expanded}', 'expanded'),
            ('${question_expression_factored}', 'factored'),
            ('${question_expression_simplified}', 'simplified'),
            ('${question_expression_collected}', 'collected'),
            ('${question_expression}', 'as_is')
        ]

        # If question_expression is defined
        if self.question_expression and self.question_expression.strip():
            for placeholder, format_type in placeholders:
                if placeholder in result_text:
                    try:
                        local_namespace = {'__builtins__': {}}

                        # Create SymPy-safe parameter dictionary
                        # Only include numeric parameters
                        sympy_safe_params = {}
                        for key, value in params.items():
                            try:
                                if isinstance(value, (int, float)):
                                    sympy_safe_params[key] = MCQ.smart_format_number(value)
                                elif hasattr(value, 'numerator') and hasattr(value, 'denominator'):  # Fraction
                                    sympy_safe_params[key] = Rational(value.numerator, value.denominator)
                                # Skip strings, complex objects, etc.
                                elif isinstance(value, list) and all(isinstance(x, (int, float)) for x in value):
                                    # Handle coefficient lists - keep as list for indexing
                                    sympy_safe_params[key] = value
                                elif isinstance(value, str) and not ('\\' in value or callable(value)):  # ✅ ALLOW clean strings but skip LaTeX and function-like strings
                                    sympy_safe_params[key] = value  # Keep string parameters for substitution
                                # Skip problematic types that cause 'subs' errors
                                elif hasattr(value, 'subs') or callable(value):
                                    continue  # Skip SymPy objects and functions
                                elif callable(value):  # Function objects
                                    continue
                                elif hasattr(value, '__call__'):  # More function detection
                                    continue
                                elif str(type(value)).startswith('<function'):  # Function type detection
                                    continue
                                elif isinstance(value, (list, dict, tuple)) and not all(isinstance(x, (int, float)) for x in value):
                                    continue
                                else:
                                    # Try to convert unknown types to float
                                    try:
                                        # Check if it's a numeric type we can safely convert
                                        if hasattr(value, '__float__') and not callable(value):
                                            sympy_safe_params[key] = float(value)
                                        elif hasattr(value, '__int__') and not callable(value):
                                            sympy_safe_params[key] = int(value)
                                    except (ValueError, TypeError, AttributeError):
                                        # Skip if can't convert safely
                                        continue

                            except Exception:
                                # Skip any parameter that causes issues during type checking
                                continue

                        # Debug output to see what's being used
                        if len(sympy_safe_params) != len(params):
                            filtered_out = set(params.keys()) - set(sympy_safe_params.keys())
                            print(f"   Filtered out parameters: {filtered_out}")
                            print(f"   Using safe parameters: {list(sympy_safe_params.keys())}")
                        latex_expr = ""
                        # Handle equations separately
                        if '=' in self.question_expression:
                            left_side, right_side = self.question_expression.split('=', 1)
                            left_expr = sympify(left_side.strip(), locals=local_namespace)
                            right_expr = sympify(right_side.strip(), locals=local_namespace)

                            left_sub = left_expr.subs(sympy_safe_params)
                            right_sub = right_expr.subs(sympy_safe_params)

                            # Apply format
                            if format_type == 'expanded':
                                left_proc = expand(left_sub)
                                right_proc = expand(right_sub)
                            elif format_type == 'factored':
                                left_proc = factor(left_sub)
                                right_proc = factor(right_sub)
                            elif format_type == 'simplified':
                                left_proc = simplify(left_sub)
                                right_proc = simplify(right_sub)
                            elif format_type == 'collected':
                                left_proc = collect(left_sub, symbols('x'))
                                right_proc = collect(right_sub, symbols('x'))
                            else:
                                left_proc = left_sub
                                right_proc = right_sub

                            # Convert both sides to LaTeX
                            left_latex = latex(left_proc)
                            right_latex = latex(right_proc)
                            # Clean signs
                            left_latex = left_latex.replace('+ -', '- ').replace('- -', '+ ')
                            right_latex = right_latex.replace('+ -', '- ').replace('- -', '+ ')

                            latex_expr = f"{left_latex} = {right_latex}"

                        else:
                            if self.question_expression in params:
                                # This is a parameter name that should be substituted
                                expr = symbols(self.question_expression)
                            else:
                                # This is a mathematical expression to be parsed
                                expr = sympify(self.question_expression, locals=local_namespace)
                            substituted = expr.subs(sympy_safe_params)
                            if format_type == 'expanded':
                                processed = expand(substituted)
                            elif format_type == 'factored':
                                processed = factor(substituted)
                            elif format_type == 'simplified':
                                processed = simplify(substituted)
                            elif format_type == 'collected':
                                processed = collect(substituted, symbols('x'))
                            else:
                                processed = substituted

                            latex_expr = latex(processed)
                            latex_expr = latex_expr.replace('+ -', '- ').replace('- -', '+ ')

                        # After getting latex_expr, apply cleaning:
                        latex_expr = self.clean_math_expression(latex_expr)
                        result_text = result_text.replace(placeholder, f"\\({latex_expr}\\)")

                    except Exception as e:
                        print(f"⚠️ Error processing question_expression: {e}")
                        # Fallback: do naive substitution of parameters
                        fallback_expr = self.question_expression
                        for pname, pvalue in sympy_safe_params.items():
                            if not pname.endswith('_sympy'):  # Skip SymPy objects
                                # Use smart formatting for parameter values
                                formatted_pvalue = MCQ.smart_format_number(pvalue)
                                fallback_expr = fallback_expr.replace(str(pname), formatted_pvalue)
                        fallback_expr = self.clean_math_expression(fallback_expr)
                        result_text = result_text.replace(placeholder, f"\\({fallback_expr}\\)")

        # Handle individual parameter substitutions like ${a}$, ${b}$
        for param_name, param_value in params.items():
            placeholder = f'${{{param_name}}}'
            if placeholder in result_text:
                formatted_value = MCQ.smart_format_number(param_value)
                formatted_value = self.clean_math_expression(str(formatted_value))
                result_text = result_text.replace(placeholder, formatted_value)

        return result_text


    def render_options(self, params: Dict) -> List[str]:
        """Render options with sophisticated parameter substitution and centralized calculations"""
        if not self.options:
            return []

        print(f"🔧 Rendering options with params: {params}")

        try:
            # Step 1: Calculate derived parameters
            calc = {}
            if self.calculated_parameters:
                for calc_name, calc_expr in self.calculated_parameters.items():
                    try:
                        if calc_name == calc_expr:
                            continue

                        safe_namespace =MCQ.create_safe_math_namespace({
                            **params,
                            **calc
                        })
                        calc_result = eval(calc_expr, safe_namespace)
                        calc[calc_name] = calc_result
                        print(f"✅ Calculated {calc_name} = {calc_result}")

                    except Exception as e:
                        print(f"⚠️ Failed to calculate {calc_name}: {e}")
                        calc[calc_name] = 0

            all_params = {**params, **calc}
            print(f"🔗 All params: {all_params}")

            # Step 2: Process options with parameter substitution only
            rendered_options = []
            for i, option in enumerate(self.options):
                print(f"🎯 Processing option {i}: '{option}'")

                # Sophisticated parameter substitution and formatting
                result = self._render_option_sophisticated(option, all_params)
                rendered_options.append(result)
                print(f"✅ Result: {result}")

            return rendered_options

        except Exception as e:
            print(f"💥 Error: {e}")
            return [f"\\({opt}\\)" for opt in self.options]

    def _render_option_sophisticated(self, option: str, all_params: Dict) -> str:
        """Render single option with sophisticated parameter substitution and LaTeX formatting"""
        # Step 1: Parameter substitution using new format
        substituted = self._substitute_parameters(option, all_params)

        # Step 2: Evaluate any remaining mathematical expressions
        try:
            # Try to evaluate as math if it looks like an expression
            if any(op in substituted for op in ['+', '-', '*', '/', '**', 'sqrt']):
                evaluated = self._evaluate_mathematical_expression(substituted, all_params)
                if evaluated is not None:
                    substituted = evaluated
        except:
            pass  # Keep original if evaluation fails
        try:
            #  Try to evaluate simple arithmetic in fractions
            substituted = self._evaluate_simple_arithmetic(substituted)
        except:
            pass  # Keep original if evaluation fails

        # Step 3: Apply math cleaning before LaTeX formatting
        substituted = self.clean_math_expression(substituted)

        # Step 4: LaTeX formatting - ensure proper delimiters
        if not (substituted.startswith('\\(') and substituted.endswith('\\)')):
            # Only wrap if it contains mathematical symbols or LaTeX commands
            if any(char in substituted for char in ['+', '-', '*', '/', '^', '=', '<', '>', 'frac']) or '\\' in substituted:
                substituted = f"\\({substituted}\\)"

        return substituted


    def _evaluate_mathematical_expression(self, expr: str, params: Dict) -> Optional[str]:
        """Safely evaluate mathematical expressions and format the result"""
        try:
            # Create safe namespace
            safe_namespace = MCQ.create_safe_math_namespace({
                **params
            })

            # Try to evaluate
            result = eval(expr, safe_namespace)

            # Format the result using smart formatting
            return self.smart_format_number(result)

        except:
            return None  # Return None if evaluation fails


    def _evaluate_simple_arithmetic(self, expression: str) -> str:
        """Evaluate simple arithmetic in expressions like fractions"""
        import re

        # Pattern to match fractions with arithmetic: \frac{a-b}{c+d}
        frac_pattern = r'\\frac\{([^}]+)\}\{([^}]+)\}'

        def evaluate_frac_parts(match):
            numerator = match.group(1)
            denominator = match.group(2)

            try:
                # Evaluate numerator and denominator separately
                num_result = self._safe_arithmetic_eval(numerator)
                den_result = self._safe_arithmetic_eval(denominator)

                # Return simplified fraction
                if den_result != 0:
                    if num_result % den_result == 0:
                        return str(num_result // den_result)  # Whole number
                    else:
                        return f"\\frac{{{num_result}}}{{{den_result}}}"
                else:
                    return f"\\frac{{{num_result}}}{{{den_result}}}"  # Keep original if division by zero

            except:
                # If evaluation fails, return original
                return f"\\frac{{{numerator}}}{{{denominator}}}"

        # Apply evaluation to all fractions in the expression
        result = re.sub(frac_pattern, evaluate_frac_parts, expression)

        return result

    def _safe_arithmetic_eval(self, expr: str) -> int:
        """Safely evaluate simple arithmetic expressions"""
        try:
            # Only allow basic arithmetic - no variables or complex operations
            allowed_chars = set('0123456789+-*/() ')
            if all(c in allowed_chars for c in expr):
                return int(eval(expr, {"__builtins__": {}}))
            else:
                raise ValueError("Complex expression")
        except:
            # If evaluation fails, try to extract just the number
            import re
            numbers = re.findall(r'-?\d+', expr)
            return int(numbers[0]) if numbers else 0


    def _substitute_parameters(self, text: str, params: Dict) -> str:
        """Substitute parameters using new ${param} format"""
        result = text

        # Sort parameters by length to avoid partial matches
        sorted_params = sorted(params.items(), key=lambda x: len(x[0]), reverse=True)

        for param_name, param_value in sorted_params:
            placeholder = f'${{{param_name}}}'
            if placeholder in result:
                formatted_value = self.smart_format_number(param_value)
                result = result.replace(placeholder, formatted_value)

        # Clean up signs
        result = self.clean_math_expression(result)
        return result


    @property
    def rendered_option_explanations(self) -> List[str]:
        """Get option explanations with parameter substitution and LaTeX formatting"""
        if self.is_parameterized:
            if self._current_params is None:
                self._current_params = self._generate_parameters()
            return self.render_option_explanations(self._current_params)
        return self.option_explanations

    def render_option_explanations(self, params: Dict) -> List[str]:
        """Render option explanations with sophisticated parameter substitution and centralized calculations"""
        if not self.option_explanations:
            return []

        print(f"🔧 Rendering option explanations with params: {params}")

        try:
            # Step 1: Calculate derived parameters
            calc = {}
            if self.calculated_parameters:
                for calc_name, calc_expr in self.calculated_parameters.items():
                    try:
                        if calc_name == calc_expr:
                            continue

                        safe_namespace = MCQ.create_safe_math_namespace({
                            **params,
                            **calc
                        })
                        calc_result = eval(calc_expr, safe_namespace)
                        calc[calc_name] = calc_result
                        print(f"✅ Calculated {calc_name} = {calc_result}")

                    except Exception as e:
                        print(f"⚠️ Failed to calculate {calc_name}: {e}")
                        calc[calc_name] = 0

            all_params = {**params, **calc}
            print(f"🔗 All params: {all_params}")

            # Step 2: Process explanations with parameter substitution and cleaning
            rendered_explanations = []
            for i, explanation in enumerate(self.option_explanations):
                print(f"🎯 Processing explanation {i}: '{explanation}'")

                # Parameter substitution and cleaning
                result = self._render_explanation_sophisticated(explanation, all_params)
                rendered_explanations.append(result)
                print(f"✅ Result: {result}")

            return rendered_explanations

        except Exception as e:
            print(f"💥 Error: {e}")
            return self.option_explanations  # Return original on error

    def _render_explanation_sophisticated(self, explanation: str, all_params: Dict) -> str:
        """Render single explanation with sophisticated parameter substitution and math cleaning"""
        # Step 1: Parameter substitution
        substituted = self._substitute_parameters(explanation, all_params)

        # Step 2: Try mathematical evaluation for any embedded math
        try:
            # Try to evaluate simple mathematical expressions
            if any(op in substituted for op in ['+', '-', '*', '/', '**', 'sqrt']):
                evaluated = self._evaluate_mathematical_expression(substituted, all_params)
                if evaluated is not None:
                    substituted = evaluated
        except:
            pass  # Keep original if evaluation fails

        # Step 3: Apply math cleaning (this is the key fix)
        substituted = self.clean_math_expression(substituted)

        # Step 4: LaTeX formatting for any math content
        if not (substituted.startswith('\\(') and substituted.endswith('\\)')):
            # Only wrap if it contains mathematical symbols or LaTeX commands
            if any(char in substituted for char in ['+', '-', '*', '/', '^', '=', '<', '>', 'frac']) or '\\' in substituted:
                substituted = f"\\({substituted}\\)"

        return substituted

    def clean_math_expression(self, expression: str) -> str:
        """Enhanced math expression cleaning - applies all sign fixes consistently"""

        # Pattern: (a)-(b) becomes a+(-b) then a-b
        expression = re.sub(r'\((-?\d+)\)-\((-?\d+)\)',
                        lambda m: f"{m.group(1)}+{m.group(2)[1:] if m.group(2).startswith('-') else '-'+m.group(2)}",
                        expression)

        # Pattern: (-a)+(-b) becomes -a-b
        expression = re.sub(r'\((-?\d+)\)\+\((-?\d+)\)',
                        lambda m: f"{m.group(1)}{m.group(2)}" if m.group(2).startswith('-') else f"{m.group(1)}+{m.group(2)}",
                        expression)

        # Remove unnecessary parentheses around single numbers
        expression = re.sub(r'\((-?\d+)\)', r'\1', expression)

        # Enhanced sign cleaning - apply multiple passes for complex cases
        for _ in range(3):  # Multiple passes to catch nested issues
            # Basic sign fixes
            expression = expression.replace('--', '+')
            expression = expression.replace('+-', '-')
            expression = expression.replace('-+', '-')

            # Space-aware fixes
            expression = expression.replace('+ -', '- ')
            expression = expression.replace('- -', '+ ')
            expression = expression.replace('+ +', '+ ')

            # Handle cases with no spaces
            expression = re.sub(r'\+\s*-', '-', expression)
            expression = re.sub(r'-\s*-', '+', expression)

            # Clean up multiple consecutive spaces
            expression = re.sub(r'\s+', ' ', expression)

            # Clean up spaces around operators
            expression = re.sub(r'\s*([+\-*/=])\s*', r' \1 ', expression)
            expression = expression.strip()

        return expression

    @property
    def question_text(self) -> str:
        """Get question text with parameter substitution"""
        if self.is_parameterized:
            if self._current_params is None:
                self._current_params = self._generate_parameters()
            return self.generate_question_text(self.text, self._current_params)
        return self.text

    @property
    def question_options(self) -> List[str]:
        """Get options with parameter substitution and LaTeX rendering"""
        if self.is_parameterized:
            if self._current_params is None:
                self._current_params = self._generate_parameters()
            return self.render_options(self._current_params)
        return self.options

    @property
    def is_parameterized(self) -> bool:
        """Check if this MCQ uses parameterization"""
        if self._is_parameterized is None:
            self._is_parameterized = bool(self.generated_parameters)
        return self._is_parameterized


    @property
    def has_breakdown(self) -> bool:
        """Check if this MCQ has breakdown steps"""
        return bool(self.breakdown)

    @property
    def breakdown_routes(self) -> List[str]:
        """Get available breakdown routes"""
        return list(self.breakdown.keys()) if self.breakdown else []


    def get_breakdown_route(self, student_answer: int) -> Optional[str]:
        """
        Determine which breakdown route to use based on student answer.

        Args:
            student_answer: Index of the answer the student chose (0-based)

        Returns:
            Route ID for breakdown, or None if no breakdown should be triggered
        """
        if not self.has_breakdown:
            return None

        # Never provide breakdown for correct answers
        if student_answer == self.correctindex:
            return None

        # Look for route that maps to this answer index
        for route_id, route_data in self.breakdown.items():
            # Get answer_mapping list (defaults to empty list if not present)
            answer_mapping = route_data.get('answer_mapping', [])

            # Check if student's answer index is in this route's mapping
            if student_answer in answer_mapping:
                print(f"🎯 Student answer {student_answer} mapped to route '{route_id}'")
                return route_id

        # Fallback: if no mapping found, use first available route
        routes = list(self.breakdown.keys())
        if routes:
            fallback_route = routes[0]
            return fallback_route

        return None

    def should_skip_step(self, prereq_topics: List[int], student_mastery: Dict[int, float], config: Dict) -> bool:
        """Check if a step should be skipped based on prerequisite mastery"""
        if not prereq_topics:
            return False

        mastery_threshold = config.get('prerequisite_skip_threshold', 0.8)

        for topic_id in prereq_topics:
            if student_mastery.get(topic_id, 0.0) > mastery_threshold:
                return True

        return False

    def execute_breakdown_for_student(self, student_answer: int, student_mastery: Dict[int, float], config: Dict) -> Optional[List[BreakdownStep]]:
        """
        Execute breakdown steps for a student who answered incorrectly.
        Updated to use answer mapping.

        Args:
            student_answer: Index of answer student chose (0-based)
            student_mastery: Dictionary of student's mastery levels
            config: Configuration dictionary

        Returns:
            List of BreakdownStep objects or None
        """
        # Only provide breakdown for wrong answers
        if not self.has_breakdown or student_answer == self.correctindex:
            return None

        # Get the appropriate breakdown route using answer mapping
        route = self.get_breakdown_route(student_answer)
        if not route or route not in self.breakdown:
            return None

        # Get steps for this route
        route_data = self.breakdown[route]
        steps_data = route_data.get('steps', [])

        print(f"📚 Executing breakdown route '{route}' with {len(steps_data)} steps")

        # Create BreakdownStep objects
        executable_steps = []
        for step_data in steps_data:
            step = BreakdownStep.from_dict(step_data, self)

            # Check if step should be skipped based on prerequisite mastery
            if not step.should_skip(student_mastery, config):
                executable_steps.append(step)
                print(f"✅ Added step {step.step_no} ({step.step_type})")
            else:
                print(f"⏭️ Skipping step {step.step_no} due to prerequisite mastery")

        return executable_steps






    def regenerate_parameters(self):
        """Force regeneration of parameters"""
        self._current_params = None

    def get_current_parameters_safe(self) -> Dict[str, Union[int, float]]:
        """Get current parameter values with guaranteed consistency"""
        if self.is_parameterized:
            if self._current_params is None:
                print(f"⚠️ WARNING: Parameters were None when they should be cached! Regenerating...")
                self._current_params = self._generate_parameters()
                print(f"🔄 Regenerated parameters: {self._current_params}")
            return self._current_params.copy()  # Return copy to prevent modification
        return {}

    def get_correct_answer_value(self) -> Optional[Union[int, float, str]]:
        """Get the numerical value of the correct answer"""
        if not self.is_parameterized:
            return self.options[self.correctindex]

        if self._current_params is None:
            self._current_params = self._generate_parameters()

        try:
            rendered_options = self.render_options(self._current_params)
            return rendered_options[self.correctindex]
        except:
            return None

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

    def get_breakdown_config(self) -> Dict:
        return self.get('breakdown_config', {
            'prerequisite_skip_threshold': 0.8,
            'step_mastery_weight': 0.3,
            'enable_breakdown_system': True
        })

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

    breakdown_history: List[Dict] = field(default_factory=list)
    breakdown_preferences: Dict[str, float] = field(default_factory=lambda: {
        'breakdown_success_rate': 0.0
    })
    skill_states: Dict[str, 'SkillState'] = field(default_factory=dict)

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
        self._current_breakdown_session = None

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
        ability_levels= {
            'conceptual_understanding': 0.5,
            'procedural_fluency': 0.5,
            'problem_solving': 0.5,
            'mathematical_communication': 0.5,
            'memory': 0.5,
            'spatial_reasoning': 0.5
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

        if hasattr(self, '_current_breakdown_session') and self._current_breakdown_session:
            return self._handle_breakdown_step_completion(
                student_id, mcq_id, is_correct, time_taken, kg
            )

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

    def start_breakdown_session(self, student_id: str, breakdown_steps: List['BreakdownStep']):
        """ Start a breakdown session for a student"""
        self._current_breakdown_session = {
            'student_id': student_id,
            'steps': breakdown_steps,
            'current_step_index': 0,
            'start_time': datetime.now(),
            'step_results': []
        }

    def _handle_breakdown_step_completion(self, student_id: str, step_result: str,
                                        is_correct: bool, time_taken: float, breakdown_step: 'BreakdownStep') -> List[Dict]:
        """NEW METHOD: Handle completion of a breakdown step"""
        if not self._current_breakdown_session:
            return []

        session = self._current_breakdown_session
        session['step_results'].append({
            'step_no': session['current_step_index'],
            'correct': is_correct,
            'time_taken': time_taken,
            'timestamp': datetime.now(),
            'step_type': breakdown_step.step_type
        })
        '''
        # Update mastery based on step completion (lighter weight than full question)
        bkt_updates = []
        if self.bkt_system:
            step = session['steps'][session['current_step_index']]
            bkt_updates = self.bkt_system.process_breakdown_step(
                student_id, step, is_correct
            )
        '''
        bkt_updates = []
        if (self.bkt_system and
            hasattr(self.bkt_system, 'skill_tracker') and
            self.bkt_system.skill_tracker):

            step_difficulty = getattr(breakdown_step, 'difficulty', 0.2)
            skill_result = self.bkt_system.process_breakdown_step_response(
                student_id, breakdown_step.step_type, is_correct, step_difficulty
            )
            if skill_result and skill_result.get('skill_update'):
                bkt_updates.append(skill_result)


        session['current_step_index'] += 1
        return bkt_updates

    def complete_breakdown_session(self, student_id: str) -> Dict:
        """NEW METHOD: Complete breakdown session and analyze results"""
        if not self._current_breakdown_session:
            return {}

        session = self._current_breakdown_session

        # Analyze student performance on breakdown
        total_steps = len(session['step_results'])
        correct_steps = sum(1 for result in session['step_results'] if result['correct'])
        success_rate = correct_steps / total_steps if total_steps > 0 else 0

        # Store breakdown completion in student profile
        student = self.get_student(student_id)
        breakdown_attempt = {
            'timestamp': datetime.now(),
            'total_steps': total_steps,
            'correct_steps': correct_steps,
            'success_rate': success_rate,
            'session_data': session
        }

        # Add breakdown history to student profile
        if not hasattr(student, 'breakdown_history'):
            student.breakdown_history = []
        student.breakdown_history.append(breakdown_attempt)

        self._current_breakdown_session = None
        return breakdown_attempt

    def is_in_breakdown_session(self, student_id: str) -> bool:
        """NEW METHOD: Check if student is currently in a breakdown session"""
        return (self._current_breakdown_session is not None and
                self._current_breakdown_session.get('student_id') == student_id)

    def get_current_breakdown_step(self, student_id: str) -> Optional['BreakdownStep']:
        """NEW METHOD: Get current breakdown step for student"""
        if not self.is_in_breakdown_session(student_id):
            return None

        session = self._current_breakdown_session
        if session['current_step_index'] < len(session['steps']):
            return session['steps'][session['current_step_index']]
        return None


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
    def __init__(self, nodes_file: str = 'kg_new.json',
                 mcqs_file: str = 'computed_mcqs_breakdown.json',
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
        result = []
        for key in self.nodes.keys():
            result.append(key)
        return result

    def get_mcq_safely(self, mcq_id: str, need_full_text: bool = False):
        """
        Helper function to get MCQ data regardless of loading method
        Returns:
            For minimal data: MinimalMCQData object
            For full data: MCQ object
            None if not found
        """
        # Get the MCQ using appropriate loader
        if hasattr(self, 'ultra_loader'):
            if need_full_text:
                mcq = self.ultra_loader.get_full_mcq_if_needed(mcq_id)
            else:
                mcq = self.ultra_loader.get_minimal_mcq_data(mcq_id)
        else:
            mcq = self.mcqs.get(mcq_id)

        # Handle parameter regeneration for parameterized MCQs
        if mcq and hasattr(mcq, 'is_parameterized') and mcq.is_parameterized:
            mcq.regenerate_parameters()

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

    def get_prerequisite_chain_length(self, topic_index: int, max_depth: int = 6, max_nodes: int = 50) -> int:
        """Calculate prerequisite chain length using BFS with depth tracking"""
        visited = set()
        queue = [(topic_index, 0)]  # (node_id, depth)
        max_depth_reached = 0
        nodes_explored = 0

        while queue and nodes_explored < max_nodes:
            current, depth = queue.pop(0)
            if current in visited or depth >= max_depth:
                continue

            visited.add(current)
            nodes_explored += 1
            max_depth_reached = max(max_depth_reached, depth)

            node = self.get_node_by_index(current)
            if node:
                for prereq_id, weight in node.dependencies:
                    if prereq_id not in visited and weight > 0.1:
                        queue.append((prereq_id, depth + 1))

        return max_depth_reached

    def _get_transitive_prerequisites_bfs_limited(self, node_id: int,
                                                 max_depth: int = 4,
                                                 max_nodes: int = 100) -> List[int]:
        """
        BFS traversal with computational limits.
        Stops at max_depth levels or max_nodes explored.
        """
        visited = set()
        queue = [(node_id, 0)]  # (node_id, depth)
        prerequisites = []
        nodes_explored = 0

        while queue and nodes_explored < max_nodes:
            current, depth = queue.pop(0)

            if current in visited or depth >= max_depth:
                continue

            visited.add(current)
            nodes_explored += 1

            # Get direct prerequisites from node dependencies
            node = self.kg.get_node_by_index(current)
            if node:
                for prereq_id, weight in node.dependencies:
                    if prereq_id not in visited and weight > 0.1:  # Only significant dependencies
                        queue.append((prereq_id, depth + 1))
                        prerequisites.append(prereq_id)

        return prerequisites

    def _get_prerequisite_chains_batch(self, target_nodes: List[int],
                                     max_depth: int = 4,
                                     max_nodes: int = 100) -> Dict[int, List[int]]:
        """
        Batch prerequisite calculation to reduce graph traversals and improve performance.
        Processes multiple target nodes in a single operation to minimize redundant work.
        """


        results = {}
        global_visited = set()  # Track globally visited nodes to avoid redundant work

        for target_node in target_nodes:
            if target_node not in results:
                # BFS for this target, reusing global visited state where possible
                prerequisites = self._bfs_single_target_optimized(
                    target_node, max_depth, max_nodes, global_visited
                )
                results[target_node] = prerequisites


        return results
    def _bfs_single_target_optimized(self, target_node: int, max_depth: int,
                                max_nodes: int, global_visited: Set[int]) -> List[int]:
        """
        Optimized BFS for single target that leverages global visited state.
        Helper method for get_prerequisite_chains_batch.
        """
        local_visited = set()
        queue = [(target_node, 0)]  # (node_id, depth)
        prerequisites = []
        nodes_explored = 0

        while queue and nodes_explored < max_nodes:
            current, depth = queue.pop(0)

            if current in local_visited or depth >= max_depth:
                continue

            local_visited.add(current)
            global_visited.add(current)  # Update global state
            nodes_explored += 1

            # Get direct prerequisites from node dependencies
            node = self.get_node_by_index(current)
            if node:
                for prereq_id, weight in node.dependencies:
                    if prereq_id not in local_visited and weight > 0.1:
                        queue.append((prereq_id, depth + 1))
                        prerequisites.append(prereq_id)

        return prerequisites



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
    def difficulty_breakdown(self) -> 'DifficultyBreakdown':
        """Return detailed breakdown in minimal data"""
        return self.minimal_data.difficulty_breakdown

class MCQScheduler:
    """the bit that does the actual mcq algorithm calculations
        Selects optimal questions for students based on:
        - Current mastery levels across topics
        - Prerequisites and dependencies
        - Question difficulty and coverage
        - Learning objectives and priorities
        - orders them

    The greedy algorithm iteratively selects questions that maximize
    coverage-to-cost ratio until learning goals are met.
    """

    def __init__(self, knowledge_graph, student_manager, config_manager=None):
        self.kg = knowledge_graph
        self.student_manager = student_manager
        self.config = config_manager or knowledge_graph.config
        self.mcq_vectors = {}  # {mcq_id: MCQVector}
        self.bkt_system = None  # Will be set after BKT system is created
        self._pedagogy_cache = {
            'chain_lengths': {},      # {topic_index: chain_length}
            'breakdown_scores': {},   # {mcq_id: score}
            'topic_orderings': {}     # {frozenset(topics): sorted_list}
        }
        self._cache_dirty = False  # Track when to invalidate caches


    def _invalidate_pedagogy_caches(self):
        """Invalidate caches when graph or MCQ data changes"""
        self._pedagogy_cache['chain_lengths'].clear()
        self._pedagogy_cache['topic_orderings'].clear()
        # Don't clear breakdown_scores - they're based on MCQ data, not graph structure

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





    def select_optimal_mcqs(self, student_id: str, num_questions: int = 5,
                          use_chapter_weights: bool = False, confidence: float = 1.0) -> List[str]:
        """
        Main greedy algorithm for adaptive MCQ selection.
        Iteratively selects best question, updates virtual mastery, repeats.
        """

        student = self.student_manager.get_student(student_id)
        if not student:
            print(f"❌ Student {student_id} not found")
            return []
        # Get config values
        greedy_max_mcqs_to_evaluate = self.get_config_value('greedy_algorithm.greedy_max_mcqs_to_evaluate', 50)
        greedy_early_stopping = self.get_config_value('greedy_algorithm.greedy_early_stopping', False)
        greedy_convergence_threshold = self.get_config_value('algorithm_config.greedy_convergence_threshold', 0.05)

        # Get MCQs eligible for selection
        eligible_mcqs = self.get_available_questions_for_student(student_id)
        print(f"Eligible MCQs: {eligible_mcqs}")
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

                    coverage_to_cost_ratio, coverage_info = self._calculate_coverage_to_cost_ratio(mcq_id, topic_priorities, simulated_mastery_levels, student, confidence)
                    print(f"   📊 Ratio: {coverage_to_cost_ratio:.3f}")

                    if coverage_to_cost_ratio > best_ratio:
                        best_ratio = coverage_to_cost_ratio
                        best_mcq = mcq_id
                        best_coverage_info = coverage_info
                        print(f"   ✅ New best MCQ: {mcq_id} (ratio: {best_ratio:.3f})")
                    if best_mcq is None:
                        print("✅ No suitable MCQs left — stopping.")
                        break

                except Exception as e:
                    print(f"   ❌ Error evaluating MCQ {mcq_id}: {type(e)} - {e}")
                    import traceback
                    traceback.print_exc()
                    # Continue with next MCQ instead of crashing
                    continue

            if best_mcq is None:
                print(f"No suitable MCQ found for remaining due topics in iteration {iteration + 1}")
                break

            print(f"Best MCQ selected: {best_mcq}, best score: {best_ratio}")
            # Select the best MCQ
            selected_mcqs.append(best_mcq)

            # Update virtual mastery and topic priorities
            try:
                # Update virtual mastery and topic priorities
                total_topic_coverage_score = self._update_simulated_mastery_and_priorities(best_mcq, simulated_mastery_levels, topic_priorities, best_coverage_info, student)

                if iteration % 5 == 0:  # Only print every 5th iteration
                    print(f"✅ Q{iteration}: Coverage {total_topic_coverage_score:.3f}")

            except Exception as e:
                print(f"❌ Error updating virtual mastery: {type(e)} - {e}")
                import traceback
                traceback.print_exc()
                break
            if iteration % 5 == 0:
            #print(f"Selected Q{iteration + 1}: {self.kg.mcqs[best_mcq].text[:50]}...")
                print(f"  Coverage-to-cost ratio: {best_ratio:.3f}")
                print(f"  Total coverage gained: {total_topic_coverage_score:.3f}")
                print(f"  Remaining due topics: {len(topic_priorities)}")

            # Early stopping if improvement is minimal
            if (greedy_early_stopping and abs(total_topic_coverage_score - last_total_coverage) < greedy_convergence_threshold):
                print(f"Early stopping: minimal improvement detected")
                break

            last_total_coverage = total_topic_coverage_score

        print(f"🎯 Greedy selection complete: {selected_mcqs}")

        # apply reordering for better learning outcomes
        pedagogically_ordered_mcqs = self._reorder_mcqs_pedagogically(selected_mcqs)

        print(f"📚 Final pedagogical order: {pedagogically_ordered_mcqs}")
        return pedagogically_ordered_mcqs


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

    def set_bkt_system(self, bkt_system):
        """Set reference to BKT system after initialization"""
        self.bkt_system = bkt_system
        # Also set the reference in student manager
        self.student_manager.bkt_system = bkt_system
    def _update_simulated_mastery_and_priorities(self, mcq_id: str,
                                            simulated_mastery_levels: Dict[int, float],
                                            topic_priorities: Dict[int, float],
                                            coverage_info: Dict,
                                            student: StudentProfile) -> float:
        """
        virtual mastery updates using BKT functions.
        """
        if not self.bkt_system:
            return self._update_simulated_mastery_fallback(
                mcq_id, simulated_mastery_levels, topic_priorities, coverage_info, student)

        # Get config values
        mastery_threshold = self.get_config_value('algorithm_config.mastery_threshold', 0.7)
        greedy_priority_weight = self.get_config_value('greedy_algorithm.greedy_priority_weight', 2.0)

        # Get MCQ data (use existing pattern from process_mcq_response_improved)
        if hasattr(self.kg, 'ultra_loader'):
            minimal_data = self.kg.ultra_loader.get_minimal_mcq_data(mcq_id)
            if not minimal_data:
                return coverage_info['total_topic_coverage_score']
            subtopic_weights = minimal_data.subtopic_weights
            main_topic_index = minimal_data.main_topic_index
        else:
            mcq = self.kg.mcqs.get(mcq_id)
            if not mcq:
                return coverage_info['total_topic_coverage_score']
            subtopic_weights = mcq.subtopic_weights
            main_topic_index = mcq.main_topic_index

        topics_to_remove = []
        total_topic_coverage_score = coverage_info['total_topic_coverage_score']

        # Process each topic using the same logic as process_mcq_response_improved()
        for topic_index, weight in subtopic_weights.items():
            if topic_index not in topic_priorities:
                continue  # Only update due topics

            current_mastery = simulated_mastery_levels.get(topic_index, student.get_mastery(topic_index))

            # Use existing BKT parameter logic (same as process_mcq_response_improved)
            base_params = self.bkt_system.get_topic_parameters(topic_index)
            adjusted_params = {
                'prior_knowledge': base_params['prior_knowledge'],
                'learning_rate': base_params['learning_rate'] * weight,  # Scale by weight
                'slip_rate': base_params['slip_rate'],
                'guess_rate': base_params['guess_rate']
            }

            # Calculate BKT update (same logic as process_student_response but virtual)
            conditional_prob = self.bkt_system.calculate_conditional_probability(
                current_mastery, True, adjusted_params)
            new_mastery = self.bkt_system.update_mastery(conditional_prob, adjusted_params)

            # Update virtual mastery
            simulated_mastery_levels[topic_index] = new_mastery

            # Update topic priorities
            if new_mastery >= mastery_threshold:
                topics_to_remove.append(topic_index)
            else:
                new_priority = (1.0 - new_mastery) ** greedy_priority_weight
                topic_priorities[topic_index] = new_priority

        # Remove topics that reached mastery threshold
        for topic_index in topics_to_remove:
            topic_priorities.pop(topic_index, None)

        # Apply area of effect simulation if enabled
        enable_virtual_area_effects = self.get_config_value('greedy_algorithm.enable_virtual_area_effects', True)
        if (enable_virtual_area_effects and
            self.bkt_system and
            hasattr(self.bkt_system, 'is_area_effect_enabled') and
            self.bkt_system.is_area_effect_enabled()):

            # Calculate mastery changes for area effect
            mastery_changes = {}
            for topic_index in subtopic_weights.keys():
                if topic_index in simulated_mastery_levels:
                    original_mastery = student.get_mastery(topic_index)
                    mastery_change = simulated_mastery_levels[topic_index] - original_mastery
                    if mastery_change > 0:
                        mastery_changes[topic_index] = mastery_change

            # Apply area effects for each topic that had positive mastery changes
            for topic_index, mastery_change in mastery_changes.items():
                area_effect_updates = self._simulate_area_of_effect_single(
                    topic_index, mastery_change, simulated_mastery_levels, topic_priorities, student)

                # Update coverage score based on area effects
                for update in area_effect_updates:
                    total_topic_coverage_score += update.get('coverage_boost', 0)

        return total_topic_coverage_score

    def _simulate_area_of_effect_single(self, center_topic_index: int, mastery_change: float,
                                    simulated_mastery_levels: Dict[int, float],
                                    topic_priorities: Dict[int, float],
                                    student: StudentProfile) -> List[Dict]:
        """
        Simulate area of effect for a single topic using existing area effect logic.
        Based on apply_area_of_effect() but works with virtual mastery levels.
        """
        if mastery_change <= 0:
            return []

        # Get area effect configuration (same as existing function)
        area_config = self.bkt_system.get_area_effect_config()
        max_distance = area_config['max_distance']
        decay_rate = area_config['decay_rate']
        min_effect = area_config['min_effect']
        mastery_threshold = self.get_config_value('algorithm_config.mastery_threshold', 0.7)
        greedy_priority_weight = self.get_config_value('greedy_algorithm.greedy_priority_weight', 2.0)

        # Use NetworkX to find paths (same logic as apply_area_of_effect)
        undirected_graph = self.kg.graph.to_undirected()

        try:
            paths = nx.single_source_shortest_path(undirected_graph, center_topic_index, cutoff=max_distance)
        except Exception:
            return []

        # Remove center node
        paths.pop(center_topic_index, None)

        updates = []
        topics_to_remove = []

        for topic_index, path in paths.items():
            distance = len(path) - 1

            # Calculate path weight (same logic as _calculate_path_weight)
            path_weight = self._calculate_path_weight_safe(path)

            # Calculate effect (same formula as apply_area_of_effect)
            base_effect = mastery_change * (decay_rate ** distance)
            final_effect = base_effect * path_weight

            if final_effect > min_effect:
                current_mastery = simulated_mastery_levels.get(topic_index, student.get_mastery(topic_index))
                new_mastery = min(1.0, current_mastery + final_effect)

                # Update virtual mastery (not real student data)
                simulated_mastery_levels[topic_index] = new_mastery

                # Calculate coverage boost
                coverage_boost = 0.0
                if topic_index in topic_priorities:
                    coverage_boost = topic_priorities[topic_index] * final_effect * 0.3  # Reduced weight for area effects

                # Update topic priorities
                if topic_index in topic_priorities:
                    if new_mastery >= mastery_threshold:
                        topics_to_remove.append(topic_index)
                    else:
                        new_priority = (1.0 - new_mastery) ** greedy_priority_weight
                        topic_priorities[topic_index] = new_priority

                updates.append({
                    'topic_index': topic_index,
                    'center_topic': center_topic_index,
                    'distance': distance,
                    'effect_strength': final_effect,
                    'mastery_change': new_mastery - current_mastery,
                    'coverage_boost': coverage_boost,
                    'update_type': 'area_effect_simulation'
                })

        # Remove topics that reached mastery threshold
        for topic_index in topics_to_remove:
            topic_priorities.pop(topic_index, None)

        return updates

    def _calculate_path_weight_safe(self, path: List[int]) -> float:
        """Calculate path weight with error handling (same as existing _calculate_path_weight)"""
        if len(path) < 2:
            return 1.0

        total_weight = 1.0
        for i in range(len(path) - 1):
            source, target = path[i], path[i + 1]
            edge_weight = 0.5  # Default weight

            try:
                if self.kg.graph.has_edge(source, target):
                    edge_weight = self.kg.graph[source][target].get('weight', 0.5)
                elif self.kg.graph.has_edge(target, source):
                    edge_weight = self.kg.graph[target][source].get('weight', 0.5)
            except Exception:
                edge_weight = 0.5

            total_weight *= edge_weight

        return total_weight


    def _update_simulated_mastery_fallback(self, mcq_id: str,
                                        simulated_mastery_levels: Dict[int, float],
                                        topic_priorities: Dict[int, float],
                                        coverage_info: Dict,
                                        student: StudentProfile) -> float:
        """
        Fallback method using original difficulty-based approach when BKT unavailable.
        """
        # Get config values
        mastery_threshold = self.get_config_value('algorithm_config.mastery_threshold', 0.7)
        greedy_mastery_update_rate = self.get_config_value('greedy_algorithm.greedy_mastery_update_rate', 0.8)
        greedy_priority_weight = self.get_config_value('greedy_algorithm.greedy_priority_weight', 2.0)

        mcq_vector = self.mcq_vectors.get(mcq_id)
        if not mcq_vector:
            return coverage_info['total_topic_coverage_score']

        topics_to_remove = []

        # Update main topic and subtopics (original approach)
        for main_topic_index, topic_weight in mcq_vector.subtopic_weights.items():
            if main_topic_index in topic_priorities:
                current_mastery = simulated_mastery_levels.get(main_topic_index, student.get_mastery(main_topic_index))

                # Original difficulty-based mastery increase
                if main_topic_index == mcq_vector.main_topic_index:
                    mastery_increase = mcq_vector.difficulty * greedy_mastery_update_rate
                else:
                    mastery_increase = (mcq_vector.difficulty * topic_weight * greedy_mastery_update_rate)

                new_mastery = min(1.0, current_mastery + mastery_increase)
                simulated_mastery_levels[main_topic_index] = new_mastery

                # Update priorities
                if new_mastery >= mastery_threshold:
                    topics_to_remove.append(main_topic_index)
                else:
                    new_priority = (1.0 - new_mastery) ** greedy_priority_weight
                    topic_priorities[main_topic_index] = new_priority

        # Update prerequisites (original approach)
        for prereq_index, prereq_weight in mcq_vector.prerequisites.items():
            if prereq_index in topic_priorities:
                current_mastery = simulated_mastery_levels.get(prereq_index, student.get_mastery(prereq_index))
                mastery_increase = (mcq_vector.difficulty * prereq_weight * greedy_mastery_update_rate * 0.5)
                new_mastery = min(1.0, current_mastery + mastery_increase)
                simulated_mastery_levels[prereq_index] = new_mastery

                if new_mastery >= mastery_threshold:
                    topics_to_remove.append(prereq_index)
                else:
                    new_priority = (1.0 - new_mastery) ** greedy_priority_weight
                    topic_priorities[prereq_index] = new_priority

        # Remove topics that are no longer due
        for topic_index in topics_to_remove:
            topic_priorities.pop(topic_index, None)

        return coverage_info['total_topic_coverage_score']



    def _calculate_coverage_to_cost_ratio(self, mcq_id: str, topic_priorities: Dict[int, float],simulated_mastery_levels: Dict[int, float],student: StudentProfile,confidence: float = 1.0) -> Tuple[float, Dict]:
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
        difficulty_cost = self._calculate_difficulty_cost(mcq_vector, student, simulated_mastery_levels, confidence)

        # Calculate importance bonus (reward for important topics)
        importance_bonus = self._calculate_importance_bonus(mcq_vector, topic_priorities)

        # Total cost (lower is better)
        total_cost = max(0.01, difficulty_cost - importance_bonus)  # Prevent division by zero

        # Ratio: coverage/cost (higher is better)
        coverage_to_cost_ratio = coverage_info['total_topic_coverage_score'] / total_cost

        return coverage_to_cost_ratio, coverage_info


    def calculate_skills_difficulty_mismatch(self, mcq_vector: OptimizedMCQVector, student) -> Dict[str, float]:
        """
        FIXED VERSION: Calculate mismatch between student abilities and question difficulty requirements.
        """

        # Handle both StudentProfile objects and dictionaries safely
        if isinstance(student, dict):
            student_id = student.get('student_id')
            if student_id:
                actual_student = self.student_manager.get_student(student_id)
                if actual_student:
                    student = actual_student
                else:
                    print(f"⚠️  Warning: Could not find StudentProfile for {student_id}")
                    # Return default penalties with total_skills_penalty
                    return {
                        'problem_solving': 0.0,
                        'procedural_fluency': 0.0,
                        'conceptual_understanding': 0.0,
                        'mathematical_communication': 0.0,
                        'memory': 0.0,
                        'spatial_reasoning': 0.0,
                        'total_skills_penalty': 0.0
                    }
            else:
                print("⚠️  Warning: Student dict has no student_id")
                return {
                    'problem_solving': 0.0,
                    'procedural_fluency': 0.0,
                    'conceptual_understanding': 0.0,
                    'mathematical_communication': 0.0,
                    'memory': 0.0,
                    'spatial_reasoning': 0.0,
                    'total_skills_penalty': 0.0
                }

        # Ensure student has ability_levels attribute
        if not hasattr(student, 'ability_levels'):
            print(f"⚠️  Warning: Student object missing ability_levels attribute")
            student.ability_levels = {
                'problem_solving': 0.5,
                'procedural_fluency': 0.5,
                'conceptual_understanding': 0.5,
                'mathematical_communication': 0.5,
                'memory': 0.5,
                'spatial_reasoning': 0.5
            }

        # Get configuration weights with defaults
        config_weights = self.config.get('algorithm_config.skill_difficulty_weights', {
            'problem_solving_penalty': 0.2,
            'procedural_penalty': 0.15,
            'conceptual_penalty': 0.15,
            'memory_penalty': 0.1,
            'communication_penalty': 0.1,
            'spatial_penalty': 0.1,
            'student_offset': 0.1
        })

        skill_penalties = {}

        # Problem-solving skills mismatch
        student_problem_solving = student.ability_levels.get('problem_solving', 0.5) + config_weights.get('student_offset', 0.1)
        question_problem_solving = mcq_vector.difficulty_breakdown.problem_solving
        problem_solving_mismatch = student_problem_solving - question_problem_solving
        skill_penalties['problem_solving'] = -config_weights.get('problem_solving_penalty', 0.2) * abs(problem_solving_mismatch)

        # Procedural fluency mismatch
        student_procedural = student.ability_levels.get('procedural_fluency', 0.5) + config_weights.get('student_offset', 0.1)
        question_procedural = mcq_vector.difficulty_breakdown.procedural_fluency
        procedural_mismatch = student_procedural - question_procedural
        skill_penalties['procedural_fluency'] = -config_weights.get('procedural_penalty', 0.15) * abs(procedural_mismatch)

        # Conceptual understanding mismatch
        student_conceptual = student.ability_levels.get('conceptual_understanding', 0.5) + config_weights.get('student_offset', 0.1)
        question_conceptual = mcq_vector.difficulty_breakdown.conceptual_understanding
        conceptual_mismatch = student_conceptual - question_conceptual
        skill_penalties['conceptual_understanding'] = -config_weights.get('conceptual_penalty', 0.15) * abs(conceptual_mismatch)

        # Memory requirement mismatch
        student_memory = student.ability_levels.get('memory', 0.5) + config_weights.get('student_offset', 0.1)
        question_memory = mcq_vector.difficulty_breakdown.memory
        memory_mismatch = student_memory - question_memory
        skill_penalties['memory'] = -config_weights.get('memory_penalty', 0.1) * abs(memory_mismatch)

        # Mathematical communication mismatch
        student_communication = student.ability_levels.get('mathematical_communication', 0.5) + config_weights.get('student_offset', 0.1)
        question_communication = mcq_vector.difficulty_breakdown.mathematical_communication
        communication_mismatch = student_communication - question_communication
        skill_penalties['mathematical_communication'] = -config_weights.get('communication_penalty', 0.1) * abs(communication_mismatch)

        # Spatial reasoning mismatch
        student_spatial = student.ability_levels.get('spatial_reasoning', 0.5) + config_weights.get('student_offset', 0.1)
        question_spatial = mcq_vector.difficulty_breakdown.spatial_reasoning
        spatial_mismatch = student_spatial - question_spatial
        skill_penalties['spatial_reasoning'] = -config_weights.get('spatial_penalty', 0.1) * abs(spatial_mismatch)

        # Calculate and include total_skills_penalty
        total_penalty = sum(skill_penalties.values())
        skill_penalties['total_skills_penalty'] = total_penalty

        return skill_penalties

    def _calculate_difficulty_cost(self, mcq_vector: OptimizedMCQVector,
                                student: StudentProfile,
                                simulated_mastery_levels: Dict[int, float],
                                confidence: float = 1.0) -> float:
        """
        Calculate difficulty mismatch cost with confidence-based reduction.
        Lower confidence = reduced penalties = more exploration.
        """
        # Get config values
        confidence_cap = self.get_config_value('confidence_algorithm.confidence_cap', 0.8)
        difficulty_reduction_factor = self.get_config_value('confidence_algorithm.difficulty_reduction_factor', 0.5)
        min_difficulty_penalty = self.get_config_value('confidence_algorithm.min_difficulty_penalty', 0.1)

        # Calculate base difficulty cost (existing logic)
        base_difficulty_cost = self._calculate_base_difficulty_cost(mcq_vector, simulated_mastery_levels, student)

        # Apply confidence-based reduction only if below cap
        if confidence >= confidence_cap:
            return base_difficulty_cost

        # Calculate reduction factor based on confidence
        confidence_below_cap = confidence_cap - confidence
        max_reduction = confidence_cap  # Maximum possible reduction
        reduction_ratio = confidence_below_cap / max_reduction

        # Apply reduction but maintain minimum penalty
        penalty_multiplier = 1.0 - (reduction_ratio * difficulty_reduction_factor)
        penalty_multiplier = max(penalty_multiplier, min_difficulty_penalty)

        return base_difficulty_cost * penalty_multiplier

    def _calculate_base_difficulty_cost(self, mcq_vector: OptimizedMCQVector, simulated_mastery_levels: Dict[int, float], student: StudentProfile) -> float:
        """
        Calculate cost based on difficulty mismatch.
        Questions too hard or too easy get penalized.
        """
        # Get penalty values from config
        greedy_difficulty_penalty = self.get_config_value('greedy_algorithm.greedy_difficulty_penalty', 1.5)
        greedy_too_easy_penalty = self.get_config_value('greedy_algorithm.greedy_too_easy_penalty', 1.5)

        # Calculate skills-based difficulty mismatch
        skills_analysis = self.calculate_skills_difficulty_mismatch(mcq_vector, student)

        # Use the total skills penalty as the base difficulty cost
        skills_based_cost = abs(skills_analysis['total_skills_penalty'])


        # Calculate weighted student ability for this MCQ
        weighted_mastery = 0.0
        total_weight = 0.0

        for main_topic_index, weight in mcq_vector.subtopic_weights.items():
            mastery = simulated_mastery_levels.get(main_topic_index, student.get_mastery(main_topic_index))
            weighted_mastery += mastery * weight
            total_weight += weight

        if total_weight > 0:
            weighted_mastery /= total_weight

        # Overall difficulty mismatch
        overall_difficulty_diff = abs(mcq_vector.difficulty - weighted_mastery)

        # Apply existing penalties for too easy/too hard
        if mcq_vector.difficulty < weighted_mastery:
            overall_cost = overall_difficulty_diff * greedy_too_easy_penalty
        else:
            overall_cost = overall_difficulty_diff * greedy_difficulty_penalty

        # Combine skills-based cost with overall difficulty cost
        # Weight the skills component higher since it's more granular
        skills_weight = self.get_config_value('greedy_algorithm.skills_breakdown_weight', 2.0)
        overall_weight = self.get_config_value('greedy_algorithm.overall_difficulty_weight', 1.0)

        total_difficulty_cost = (skills_weight * skills_based_cost +
                                overall_weight * overall_cost)

        return total_difficulty_cost

    def _calculate_importance_bonus(self, mcq_vector: OptimizedMCQVector,topic_priorities: Dict[int, float]) -> float:
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

    def _reorder_mcqs_pedagogically(self, selected_mcqs: List[str]) -> List[str]:
        """
        Reorder selected MCQs for optimal pedagogical sequence.
        Groups by main topic, orders topics by prerequisite chain length,
        then uses round-robin with difficulty breakdown ordering within topics.
        Always applied for better learning outcomes.
        """
        if not selected_mcqs:
            return selected_mcqs

        print(f"🎓 Reordering {len(selected_mcqs)} MCQs pedagogically...")

        # Step 1: Group MCQs by main topic
        topic_to_mcqs = self._group_mcqs_by_main_topic(selected_mcqs)

        # Step 2: Calculate prerequisite chain lengths for each topic (with caching)
        topic_chain_lengths = self._get_cached_topic_chain_lengths(topic_to_mcqs.keys())

        # Step 3: Sort topics by prerequisite chain length (fundamental topics first)
        sorted_topics = sorted(topic_to_mcqs.keys(),
                            key=lambda t: topic_chain_lengths[t])

        print(f"📚 Topic ordering by prerequisite chain length:")
        for topic in sorted_topics:
            topic_name = self.kg.get_topic_of_index(topic)
            print(f"   {topic_name} (chain length: {topic_chain_lengths[topic]})")

        # Step 4: Sort MCQs within each topic by difficulty breakdown priority
        for topic in topic_to_mcqs:
            topic_to_mcqs[topic] = self._sort_mcqs_by_difficulty_breakdown(topic_to_mcqs[topic])

        # Step 5: Round-robin through topics (handles unequal distribution)
        reordered_mcqs = self._round_robin_mcq_selection(topic_to_mcqs, sorted_topics)

        print(f"✅ Pedagogical reordering complete: {len(reordered_mcqs)} MCQs")
        return reordered_mcqs


    def _group_mcqs_by_main_topic(self, mcq_ids: List[str]) -> Dict[int, List[str]]:
        """Group MCQ IDs by their main topic index"""
        topic_to_mcqs = {}

        for mcq_id in mcq_ids:
            # Get main topic index from minimal data
            mcq_data = self.kg.ultra_loader.get_minimal_mcq_data(mcq_id)
            if mcq_data:
                main_topic = mcq_data.main_topic_index
                if main_topic not in topic_to_mcqs:
                    topic_to_mcqs[main_topic] = []
                topic_to_mcqs[main_topic].append(mcq_id)

        return topic_to_mcqs


    def _get_cached_topic_chain_lengths(self, topic_indices: Set[int]) -> Dict[int, int]:
        """
        Get prerequisite chain lengths with caching.
        Uses KnowledgeGraph methods and caches results in MCQScheduler.
        """
        # Check if cache needs invalidation based on graph changes
        if self.kg._matrix_dirty:
            self._invalidate_pedagogy_caches()

        chain_lengths = {}
        uncached_topics = []

        # Get cached values first
        for topic_index in topic_indices:
            if topic_index in self._pedagogy_cache['chain_lengths']:
                chain_lengths[topic_index] = self._pedagogy_cache['chain_lengths'][topic_index]
            else:
                uncached_topics.append(topic_index)

        # Calculate missing chain lengths using KnowledgeGraph methods
        if uncached_topics:
            max_depth = self.get_config_value('greedy_algorithm.pedagogy_ordering.max_prereq_depth', 6)
            max_nodes = self.get_config_value('greedy_algorithm.pedagogy_ordering.max_prereq_nodes', 50)

            for topic_index in uncached_topics:
                try:
                    chain_length = self.kg.get_prerequisite_chain_length(topic_index, max_depth, max_nodes)
                    chain_lengths[topic_index] = chain_length
                    self._pedagogy_cache['chain_lengths'][topic_index] = chain_length
                except Exception as e:
                    print(f"⚠️ Error calculating chain length for topic {topic_index}: {e}")
                    chain_lengths[topic_index] = 0
                    self._pedagogy_cache['chain_lengths'][topic_index] = 0

        return chain_lengths


    def _sort_mcqs_by_difficulty_breakdown(self, mcq_ids: List[str]) -> List[str]:
        """
        Sort MCQs within a topic by difficulty breakdown priority.
        Order: memory/conceptual → procedural → communication → problem_solving/spatial
        Uses the skill progression weights from config.
        """
        # Get skill weights from config once
        skill_weights = self.get_config_value('greedy_algorithm.pedagogy_ordering.skill_progression_weights', {
            'memory': 1.0,
            'conceptual_understanding': 1.1,
            'procedural_fluency': 2.0,
            'mathematical_communication': 3.0,
            'problem_solving': 4.0,
            'spatial_reasoning': 4.1
        })

        # Batch get all vectors to avoid repeated calls
        vectors = {}
        for mcq_id in mcq_ids:
            vector = self._get_or_create_optimized_mcq_vector(mcq_id)
            if vector:
                vectors[mcq_id] = vector

        # Pre-calculate all scores with caching
        scores = {}
        for mcq_id in mcq_ids:
            if mcq_id in self._pedagogy_cache['breakdown_scores']:
                scores[mcq_id] = self._pedagogy_cache['breakdown_scores'][mcq_id]
            else:
                if mcq_id in vectors:
                    score = self._get_breakdown_priority_score(vectors[mcq_id], skill_weights)
                    scores[mcq_id] = score
                    self._pedagogy_cache['breakdown_scores'][mcq_id] = score
                else:
                    scores[mcq_id] = 999.0  # Put at end if no vector available

        # Sort by priority score (lower score = higher priority = appears first)
        return sorted(mcq_ids, key=lambda mid: scores[mid])


    def _get_breakdown_priority_score(self, mcq_vector: OptimizedMCQVector, skill_weights: Dict[str, float]) -> float:
        """
        Calculate priority score based on difficulty breakdown.
        Extracted as private method for better testability and reusability.
        """
        if not mcq_vector.difficulty_breakdown:
            return 999.0  # Put at end if no breakdown available

        breakdown = mcq_vector.difficulty_breakdown

        # Calculate weighted average of skill difficulties
        total_weighted_difficulty = 0.0
        total_weight = 0.0

        for skill, weight in skill_weights.items():
            if hasattr(breakdown, skill):
                skill_difficulty = getattr(breakdown, skill, 0.0)
                total_weighted_difficulty += skill_difficulty * weight
                total_weight += weight

        if total_weight > 0:
            return total_weighted_difficulty / total_weight
        else:
            # Fallback to overall difficulty if breakdown not available
            return mcq_vector.difficulty


    def _round_robin_mcq_selection(self, topic_to_mcqs: Dict[int, List[str]],
                                sorted_topics: List[int]) -> List[str]:
        """
        Use round-robin to distribute MCQs across topics.
        Handles topics with different numbers of questions gracefully.
        Takes one MCQ from each topic in turn until all are assigned.
        """
        reordered_mcqs = []
        topic_positions = {topic: 0 for topic in sorted_topics}  # Track position in each topic's list

        # Continue until all MCQs are assigned
        total_remaining = sum(len(topic_to_mcqs.get(topic, [])) for topic in sorted_topics)

        while total_remaining > 0:
            round_assigned = 0

            # Go through topics in prerequisite order
            for topic in sorted_topics:
                if topic not in topic_to_mcqs:
                    continue

                # If this topic still has MCQs to assign
                if topic_positions[topic] < len(topic_to_mcqs[topic]):
                    mcq_id = topic_to_mcqs[topic][topic_positions[topic]]
                    reordered_mcqs.append(mcq_id)
                    topic_positions[topic] += 1
                    round_assigned += 1

                    # Debug output
                    topic_name = self.kg.get_topic_of_index(topic)
                    vector = self._get_or_create_optimized_mcq_vector(mcq_id)
                    difficulty = vector.difficulty if vector else 0.0
                    print(f"   Round-robin: Added {mcq_id} from {topic_name} (difficulty: {difficulty:.3f})")

            # Update remaining count
            total_remaining -= round_assigned

            # Safety check to prevent infinite loops
            if round_assigned == 0:
                print("⚠️ No questions assigned in round - breaking to prevent infinite loop")
                break

        return reordered_mcqs


    def handle_breakdown_question(self, student_id: str, mcq_id: str, wrong_answer: int) -> Optional[List['BreakdownStep']]:
        """Handle breakdown execution for wrong answers"""
        student = self.student_manager.get_student(student_id)
        mcq = self.kg.get_mcq_safely(mcq_id, need_full_text=True)

        if mcq and mcq.has_breakdown:
            config = self.kg.config.config  # Access config dict

            # Use the updated MCQ method that handles answer_mapping
            breakdown_steps = mcq.execute_breakdown_for_student(
                wrong_answer, student.mastery_levels, config
            )

            if breakdown_steps:
                print(f"📚 Generated {len(breakdown_steps)} breakdown steps for answer {wrong_answer}")
                if hasattr(self.student_manager, 'start_breakdown_session'):
                    self.student_manager.start_breakdown_session(student_id, breakdown_steps)
            return breakdown_steps
        return None


    def process_breakdown_step_response(self, student_id: str, step_index: int,
                                    user_answer: int, breakdown_steps: List['BreakdownStep']) -> Dict:
        """
        Process individual breakdown step response with skill tracking
        """
        if step_index >= len(breakdown_steps):
            return {'error': 'Invalid step index'}

        step = breakdown_steps[step_index]
        is_correct = (user_answer == step.correctindex)

        result = {
            'step_index': step_index,
            'is_correct': is_correct,
            'step_type': step.step_type,
            'user_answer': user_answer,
            'correct_answer': step.correctindex
        }


        if (hasattr(self, 'bkt_system') and
            self.bkt_system and
            hasattr(self.bkt_system, 'process_breakdown_step_response')):

            step_difficulty = getattr(step, 'difficulty', 0.2)
            skill_result = self.bkt_system.process_breakdown_step_response(
                student_id, step.step_type, is_correct, step_difficulty
            )
            result.update(skill_result)

        return result


    def get_next_breakdown_step(self, breakdown_steps: List['BreakdownStep'], current_step_index: int) -> Optional['BreakdownStep']:
        """NEW METHOD: Get next step in breakdown sequence"""
        if current_step_index < len(breakdown_steps) - 1:
            return breakdown_steps[current_step_index + 1]
        return None

    def should_trigger_breakdown(self, student_id: str, mcq_id: str, is_correct: bool) -> bool:
        """NEW METHOD: Determine if breakdown should be triggered"""
        if is_correct:
            return False

        mcq = self.kg.get_mcq_safely(mcq_id, need_full_text=True)
        if not mcq or not mcq.has_breakdown:
            return False


        return True
@dataclass
class SkillState:
    """Complete state for a single skill (0-1 scale)"""
    ability_level: float  # 0-1 scale
    alpha: float          # Beta distribution success parameter
    beta: float           # Beta distribution failure parameter
    last_updated: datetime
    total_evidence: float # Total evidence accumulated



class BetaInformedEloSkillTracker:
    """
    Tracks student skills using Beta-informed Elo updates on 0-1 scale
    """

    def __init__(self, config_manager=None):
        self.config = config_manager

        # Get parameters from config with defaults
        self.initial_ability = self.get_config_value('skill_tracking.initial_ability', 0.5)
        self.initial_alpha = self.get_config_value('skill_tracking.initial_alpha', 1.0)
        self.initial_beta = self.get_config_value('skill_tracking.initial_beta', 1.0)
        self.base_learning_rate = self.get_config_value('skill_tracking.base_learning_rate', 0.15)
        self.min_evidence_threshold = self.get_config_value('skill_tracking.min_evidence_threshold', 0.05)

        # Skill-specific learning rates
        self.skill_learning_rates = {
            'problem_solving': self.get_config_value('skill_tracking.skill_learning_rates.problem_solving', 0.12),
            'procedural_fluency': self.get_config_value('skill_tracking.skill_learning_rates.procedural_fluency', 0.18),
            'conceptual_understanding': self.get_config_value('skill_tracking.skill_learning_rates.conceptual_understanding', 0.15),
            'memory': self.get_config_value('skill_tracking.skill_learning_rates.memory', 0.20),
            'mathematical_communication': self.get_config_value('skill_tracking.skill_learning_rates.mathematical_communication', 0.16),
            'spatial_reasoning': self.get_config_value('skill_tracking.skill_learning_rates.spatial_reasoning', 0.17)
        }

        # All valid skill names (matches step_type values)
        self.valid_skills = [
            'problem_solving', 'procedural_fluency', 'conceptual_understanding',
            'memory', 'mathematical_communication', 'spatial_reasoning'
        ]
    def get_skill_summary(self, student: StudentProfile) -> Dict[str, Any]:
        """
        Get comprehensive skill summary for a student.

        Returns:
            Dictionary with current skill levels, confidence, and progress metrics
        """


        if not student:
            print(f"⚠️  Warning: No student provided for skill summary")
            return {}

        # Ensure student has ability_levels
        if not hasattr(student, 'ability_levels') or not student.ability_levels:
            student.ability_levels = {skill: 0.5 for skill in self.skill_categories}

        skill_summary = {}

        for skill_name in self.valid_skills:
            # Get or initialize skill state
            skill_state = self.get_or_initialize_skill_state(student, skill_name)

            # Calculate uncertainty from Beta distribution
            total_samples = skill_state.alpha + skill_state.beta
            uncertainty = 1 / (1 + total_samples * 0.1)

            skill_summary[skill_name] = {
                'ability_level': skill_state.ability_level,
                'uncertainty': uncertainty,
                'total_evidence': skill_state.total_evidence,
                'alpha': skill_state.alpha,
                'beta': skill_state.beta,
                'last_updated': skill_state.last_updated
            }

        return skill_summary


    def get_config_value(self, key: str, default):
        """Get configuration value with fallback to default"""
        if not self.config:
            return default
        try:
            keys = key.split('.')
            value = self.config.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError, AttributeError):
            return default

    def get_or_initialize_skill_state(self, student: 'StudentProfile', skill_name: str) -> SkillState:
        """Get skill state or initialize if doesn't exist"""
        if not hasattr(student, 'skill_states'):
            student.skill_states = {}

        if skill_name not in student.skill_states:
            student.skill_states[skill_name] = SkillState(
                ability_level=self.initial_ability,
                alpha=self.initial_alpha,
                beta=self.initial_beta,
                last_updated=datetime.now(),
                total_evidence=0.0
            )

        return student.skill_states[skill_name]

    def update_skills_from_question(self, student: 'StudentProfile',
                                   mcq_vector: 'OptimizedMCQVector',
                                   is_correct: bool) -> Dict[str, Dict]:
        """
        Update all relevant skills based on question performance
        Skills weighted by their breakdown values in the question
        """
        if not mcq_vector or not mcq_vector.difficulty_breakdown:
            return {}

        skill_updates = {}

        # Update each skill weighted by its breakdown value
        for skill_name in self.valid_skills:
            skill_difficulty = getattr(mcq_vector.difficulty_breakdown, skill_name, 0.0)
            evidence_weight = skill_difficulty #/ 5.0  # Convert 0-5 to 0-1

            if evidence_weight >= self.min_evidence_threshold:
                update_result = self._update_single_skill(
                    student, skill_name, skill_difficulty, is_correct, evidence_weight,
                    source="question"
                )
                if update_result:
                    skill_updates[skill_name] = update_result

        return skill_updates

    def update_skill_from_breakdown_step(self, student: 'StudentProfile',
                                       step_type: str, is_correct: bool,
                                       step_difficulty: float = 0.2) -> Optional[Dict]:
        """
        Update specific skill based on breakdown step performance
        Only updates on incorrect answers (correct answers do nothing)
        """
        if is_correct:
            return None  # Correct breakdown steps don't update skills

        if step_type not in self.valid_skills:
            print(f"Warning: Unknown step_type '{step_type}', skipping skill update")
            return None

        # Breakdown steps provide strong evidence (weight = 1.0)
        evidence_weight = 1.0

        return self._update_single_skill(
            student, step_type, step_difficulty, is_correct, evidence_weight,
            source=f"breakdown_step({step_type})"
        )

    def apply_breakdown_completion_update(self, student: 'StudentProfile',
                                        mcq_vector: 'OptimizedMCQVector') -> Dict[str, Dict]:
        """
        Apply negative updates when all breakdown steps are completed correctly
        (Student needed help, so treat as if they got original question wrong)
        """
        if not mcq_vector or not mcq_vector.difficulty_breakdown:
            return {}

        # Apply negative updates (as if question was answered incorrectly)
        return self.update_skills_from_question(student, mcq_vector, is_correct=False)

    def _update_single_skill(self, student: 'StudentProfile', skill_name: str,
                           question_difficulty: float, is_correct: bool,
                           evidence_weight: float, source: str = "unknown") -> Dict:
        """
        Core skill update logic using Beta-informed Elo approach
        """
        skill_state = self.get_or_initialize_skill_state(student, skill_name)

        # === CALCULATE EXPECTED PERFORMANCE ===
        # Both student ability and question difficulty are on 0-1 scale after normalization
        student_ability = skill_state.ability_level
        normalized_question_difficulty = min(question_difficulty , 1.0)  # Ensure 0-1

        # Calculate expected success probability using logistic function
        difficulty_difference = normalized_question_difficulty - student_ability
        scale_factor = self.get_config_value('skill_tracking.difficulty_scale_factor', 0.5)
        expected_prob = 1 / (1 + math.exp(difficulty_difference / scale_factor))

        # === BETA-INFORMED LEARNING RATE ===
        # Calculate uncertainty from Beta distribution
        total_samples = skill_state.alpha + skill_state.beta
        uncertainty = 1 / (1 + total_samples * 0.1)  # Slower uncertainty decay

        # Get skill-specific learning rate
        base_rate = self.skill_learning_rates.get(skill_name, self.base_learning_rate)

        # Adapt learning rate based on uncertainty and evidence
        uncertainty_multiplier = self.get_config_value('skill_tracking.uncertainty_multiplier', 1.0)
        adaptive_rate = base_rate * evidence_weight * (1 + uncertainty * uncertainty_multiplier)

        # === ELO-STYLE UPDATE ===
        actual_outcome = 1.0 if is_correct else 0.0
        performance_error = actual_outcome - expected_prob

        # Update ability level (keeping in 0-1 range)
        ability_change = adaptive_rate * performance_error
        new_ability = np.clip(skill_state.ability_level + ability_change, 0.0, 1.0)

        # === BETA POSTERIOR UPDATE ===
        # Weight evidence by how "surprising" the outcome was
        surprise_factor = abs(performance_error)
        surprise_amplification = self.get_config_value('skill_tracking.surprise_amplification', 1.5)
        effective_evidence = evidence_weight * (0.5 + surprise_factor * surprise_amplification)

        new_alpha = skill_state.alpha + effective_evidence * actual_outcome
        new_beta = skill_state.beta + effective_evidence * (1 - actual_outcome)

        # === UPDATE STUDENT STATE ===
        old_ability = skill_state.ability_level
        skill_state.ability_level = new_ability
        skill_state.alpha = new_alpha
        skill_state.beta = new_beta
        skill_state.last_updated = datetime.now()
        skill_state.total_evidence += effective_evidence

        # Update the main ability_levels dict (used by greedy algorithm)
        student.ability_levels[skill_name] = new_ability

        return {
            'skill_name': skill_name,
            'source': source,
            'old_ability': old_ability,
            'new_ability': new_ability,
            'ability_change': ability_change,
            'expected_prob': expected_prob,
            'performance_error': performance_error,
            'evidence_weight': evidence_weight,
            'effective_evidence': effective_evidence,
            'uncertainty': uncertainty,
            'question_difficulty': normalized_question_difficulty
        }

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

        self.skill_tracking_enabled = self.get_config_value('skill_tracking.enabled', True)
        if self.skill_tracking_enabled:
            self.skill_tracker = BetaInformedEloSkillTracker(config_manager)
            print("✅ Skill tracking enabled with Beta-informed Elo")
        else:
            self.skill_tracker = None
            print("❌ Skill tracking disabled")

    def set_scheduler(self, scheduler):
        """Set reference to scheduler after initialization"""
        self.scheduler = scheduler

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

    def get_config_value(self, key: str, default):
        """Get configuration value with fallback to default"""
        if not self.config:
            return default
        try:
            keys = key.split('.')
            value = self.config.config
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError, AttributeError):
            return default

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
        Process a student's response and update their mastery using BKT with skill tracking
        FSRS forgetting applied automatically
        """
        student = self.student_manager.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        # Use provided custom parameters or default for topic
        params = custom_params if custom_params else self.get_topic_parameters(topic_index)

        # Get current mastery level
        current_mastery = student.mastery_levels.get(topic_index)
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

        # Update skills if skill tracking is enabled
        skill_updates = {}
        if self.skill_tracking_enabled and self.skill_tracker and mcq_id:
            try:
                mcq_vector = self.scheduler._get_or_create_optimized_mcq_vector(mcq_id)
                if mcq_vector:
                    skill_updates = self.skill_tracker.update_skills_from_question(
                        student, mcq_vector, is_correct
                    )
            except Exception as e:
                print(f"Warning: Skill update failed for {mcq_id}: {e}")

        result['skill_updates'] = skill_updates
        return result



    def process_breakdown_completion(self, student_id: str, mcq_id: str,
                                all_steps_correct: bool) -> Dict:
        """
        Process completion of breakdown sequence
        If all steps correct, apply negative update (student needed help)
        """
        if not self.skill_tracking_enabled or not self.skill_tracker:
            return {'skill_updates': {}}

        if not all_steps_correct:
            return {'skill_updates': {}}  # Individual step failures already handled

        student = self.student_manager.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        try:
            mcq_vector = self.scheduler._get_or_create_optimized_mcq_vector(mcq_id)
            if mcq_vector:
                skill_updates = self.skill_tracker.apply_breakdown_completion_update(
                    student, mcq_vector
                )
                return {'skill_updates': skill_updates}
        except Exception as e:
            print(f"Warning: Breakdown completion update failed for {mcq_id}: {e}")

        return {'skill_updates': {}}

    def complete_breakdown_sequence(self, student_id: str, mcq_id: str,
                                breakdown_results: List[Dict]) -> Dict:
        """
        Complete breakdown sequence and apply final updates
        """
        # Check if all steps were answered correctly
        all_correct = all(result['is_correct'] for result in breakdown_results)
        correct_count = sum(1 for r in breakdown_results if r['is_correct'])
        total_count = len(breakdown_results)
        performance_ratio = correct_count / total_count if total_count > 0 else 0.0

        completion_result = {
            'all_steps_correct': all_correct,
            'total_steps': total_count,
            'correct_steps': correct_count,
            'performance_ratio': performance_ratio
        }

        # Apply skill updates if all steps correct (student needed help)
        if (all_correct and
            hasattr(self, 'bkt_system') and
            hasattr(self.bkt_system, 'skill_tracker') and
            self.bkt_system.skill_tracker):

            skill_completion_updates = self.process_breakdown_completion(
                student_id, mcq_id, all_steps_correct=True
            )
            completion_result['skill_completion_updates'] = skill_completion_updates

        # Add BKT mastery updates based on performance
        # Use record_attempt with performance-weighted result
        is_correct_equivalent = performance_ratio >= 0.8

        # Get the StudentManager to use record_attempt
        if hasattr(self, 'student_manager') and self.student_manager:
            bkt_updates = self.student_manager.record_attempt(
                student_id, mcq_id, is_correct_equivalent, 10.0, self.kg
            )

            # Scale the updates based on performance
            if bkt_updates and performance_ratio < 1.0:
                scale_factor = 0.3 + (0.4 * performance_ratio)  # 0.3 to 0.7 scaling

                # Apply scaling
                for update in bkt_updates:
                    if 'mastery_change' in update:
                        original_change = update['mastery_change']
                        scaled_change = original_change * scale_factor

                        student = self.student_manager.get_student(student_id)
                        if student and 'main_topic_index' in update:
                            topic_index = update['main_topic_index']
                            current_mastery = student.get_mastery(topic_index)
                            adjusted_mastery = current_mastery - original_change + scaled_change
                            student.mastery_levels[topic_index] = max(0.0, min(1.0, adjusted_mastery))
                            update['mastery_change'] = scaled_change
                            update['mastery_after'] = student.mastery_levels[topic_index]

            completion_result['bkt_updates'] = bkt_updates

        return completion_result

    def process_breakdown_step_response(self, student_id: str, step_type: str,
                                    is_correct: bool, step_difficulty: float = 0.2) -> Dict:
        """
        Process breakdown step response and update relevant skill
        Only updates skills on incorrect answers
        """
        if not self.skill_tracking_enabled or not self.skill_tracker:
            return {'skill_update': None}

        student = self.student_manager.get_student(student_id)
        if not student:
            raise ValueError(f"Student {student_id} not found")

        skill_update = self.skill_tracker.update_skill_from_breakdown_step(
            student, step_type, is_correct, step_difficulty
        )

        return {'skill_update': skill_update}

    def process_mcq_response_improved(self, student_id: str, mcq_id: str,is_correct: bool) -> List[Dict]:
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
                current_mastery = student.mastery_levels.get(topic_index)
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

        stored_mastery = student.mastery_levels.get(topic_index)

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


    def get_student_skill_summary(self, student_id: str) -> Dict:
        """Get comprehensive summary of student's skill levels"""
        if not self.skill_tracking_enabled or not self.skill_tracker:
            return {}

        student = self.student_manager.get_student(student_id)
        if not student:
            return {}

        return self.skill_tracker.get_skill_summary(student)

    def reset_student_skills(self, student_id: str):
        """Reset student's skills to initial values (for testing)"""
        if not self.skill_tracking_enabled or not self.skill_tracker:
            return

        student = self.student_manager.get_student(student_id)
        if not student:
            return

        # Reset skill states
        if hasattr(student, 'skill_states'):
            delattr(student, 'skill_states')

        # Reset ability levels to initial values
        for skill_name in self.skill_tracker.valid_skills:
            student.ability_levels[skill_name] = self.skill_tracker.initial_ability

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

# Add these functions to mcq_algorithm_current.py

def get_comprehensive_session_stats(student_manager, student_id: str) -> Dict:
    """
    Get comprehensive session statistics for the demo
    """
    student = student_manager.get_student(student_id)
    if not student:
        return {}

    # Basic statistics
    total_questions = len(student.attempt_history)
    correct_answers = sum(1 for attempt in student.attempt_history if attempt.correct)
    success_rate = (correct_answers / total_questions) if total_questions > 0 else 0.0

    # Time statistics
    total_time = sum(attempt.time_taken for attempt in student.attempt_history)
    avg_time_per_question = (total_time / total_questions) if total_questions > 0 else 0.0

    # Mastery statistics
    mastery_levels = list(student.mastery_levels.values())
    avg_mastery = sum(mastery_levels) / len(mastery_levels) if mastery_levels else 0.0
    mastery_above_threshold = sum(1 for m in mastery_levels if m > 0.7)

    # Topic-specific statistics
    topics_studied = len([m for m in mastery_levels if m > 0.1])

    return {
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'success_rate': success_rate,
        'total_time': total_time,
        'avg_time_per_question': avg_time_per_question,
        'avg_mastery': avg_mastery,
        'topics_studied': topics_studied,
        'mastery_above_threshold': mastery_above_threshold,
        'session_count': student.session_count,
        'total_time_on_system': student.total_time_on_system
    }

def get_skill_progression_for_session(bkt_system, student_id: str) -> Dict:
    """
    Get skill progression information for session summary
    """
    if not bkt_system.skill_tracking_enabled or not bkt_system.skill_tracker:
        return {}

    student = bkt_system.student_manager.get_student(student_id)
    if not student:
        return {}

    skill_summary = bkt_system.skill_tracker.get_skill_summary(student)

    # Calculate improvements (this would ideally track from session start)
    improvements = {}
    for skill_name, current_level in student.ability_levels.items():
        # For demo purposes, assume some improvement
        initial_level = 0.5  # This should be tracked from session start in real implementation
        improvement = current_level - initial_level
        improvements[skill_name] = {
            'initial': initial_level,
            'current': current_level,
            'improvement': improvement,
            'improvement_percentage': (improvement / initial_level) * 100 if initial_level > 0 else 0
        }

    return {
        'current_levels': student.ability_levels.copy(),
        'improvements': improvements,
        'skill_summary': skill_summary
    }

def preview_decay_simulation(bkt_system, student_id: str, days_ahead: int = 7) -> Dict:
    """
    Preview what mastery decay would look like after a certain number of days
    WITHOUT actually applying the decay (for preview purposes)
    """
    student = bkt_system.student_manager.get_student(student_id)
    if not student:
        return {'error': 'Student not found'}

    if not bkt_system.fsrs_forgetting:
        return {'error': 'FSRS forgetting not enabled'}

    # Store original time offset
    original_offset = time_manipulator.get_time_offset()

    # Temporarily simulate time passage
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

            topic_name = bkt_system.kg.get_topic_of_index(topic_index)
            if topic_name:  # Only include topics with valid names
                decay_preview['topics'].append({
                    'topic_index': topic_index,
                    'topic_name': topic_name,
                    'current_mastery': current_mastery,
                    'predicted_mastery': predicted_mastery,
                    'decay_amount': decay_amount,
                    'decay_percentage': decay_percentage,
                    'stability': components.stability,
                    'difficulty': components.difficulty,
                    'retrievability': components.retrievability
                })

    # Restore original time offset (this is just a preview)
    time_manipulator._time_offset = original_offset

    # Sort by decay amount (most decay first)
    decay_preview['topics'].sort(key=lambda x: x['decay_amount'], reverse=True)

    return decay_preview

def get_session_summary_data(bkt_system, student_id: str, session_questions: List[str]) -> Dict:
    """
    Get comprehensive data for session summary display
    """
    student = bkt_system.student_manager.get_student(student_id)
    if not student:
        return {'error': 'Student not found'}

    # Basic session info
    session_stats = get_comprehensive_session_stats(bkt_system.student_manager, student_id)

    # Skill progression
    skill_progression = get_skill_progression_for_session(bkt_system, student_id)

    # Topic coverage in this session
    topics_covered = set()
    questions_by_topic = {}

    for mcq_id in session_questions:
        # Get MCQ topic information
        if hasattr(bkt_system.kg, 'ultra_loader') and bkt_system.kg.ultra_loader:
            minimal_data = bkt_system.kg.ultra_loader.get_minimal_mcq_data(mcq_id)
            if minimal_data:
                topic_idx = minimal_data.main_topic_index
                topic_name = bkt_system.kg.get_topic_of_index(topic_idx)
                if topic_name:
                    topics_covered.add(topic_name)
                    if topic_name not in questions_by_topic:
                        questions_by_topic[topic_name] = []
                    questions_by_topic[topic_name].append(mcq_id)

    # Mastery changes during session (approximate)
    mastery_changes = {}
    for topic_idx, mastery in student.mastery_levels.items():
        topic_name = bkt_system.kg.get_topic_of_index(topic_idx)
        if topic_name in topics_covered:
            mastery_changes[topic_name] = {
                'current_mastery': mastery,
                'estimated_change': 0.05  # This should be tracked properly in real implementation
            }

    return {
        'session_stats': session_stats,
        'skill_progression': skill_progression,
        'topics_covered': list(topics_covered),
        'questions_by_topic': questions_by_topic,
        'mastery_changes': mastery_changes,
        'session_length': len(session_questions)
    }

def initialize_session_tracking(student_manager, student_id: str) -> Dict:
    """
    Initialize session tracking for a student
    """
    student = student_manager.get_student(student_id)
    if not student:
        return {'error': 'Student not found'}

    # Record session start
    student_manager.start_session(student_id)

    # Store initial skill levels for comparison
    if hasattr(student, 'ability_levels'):
        student.session_start_abilities = student.ability_levels.copy()

    # Store initial mastery levels
    student.session_start_mastery = student.mastery_levels.copy()

    return {
        'success': True,
        'session_start_time': datetime.now().isoformat(),
        'student_id': student_id
    }

def finalize_session_tracking(student_manager, student_id: str) -> Dict:
    """
    Finalize session tracking and calculate improvements
    """
    student = student_manager.get_student(student_id)
    if not student:
        return {'error': 'Student not found'}

    # End the session
    student_manager.end_session(student_id)

    # Calculate actual improvements
    improvements = {
        'mastery_improvements': {},
        'skill_improvements': {}
    }

    if hasattr(student, 'session_start_mastery'):
        for topic_idx, start_mastery in student.session_start_mastery.items():
            current_mastery = student.mastery_levels.get(topic_idx, 0.0)
            improvement = current_mastery - start_mastery
            if abs(improvement) > 0.01:  # Only track significant changes
                topic_name = student_manager.bkt_system.kg.get_topic_of_index(topic_idx) if hasattr(student_manager, 'bkt_system') else f"Topic {topic_idx}"
                improvements['mastery_improvements'][topic_name] = {
                    'start': start_mastery,
                    'end': current_mastery,
                    'change': improvement
                }

    if hasattr(student, 'session_start_abilities'):
        for skill_name, start_ability in student.session_start_abilities.items():
            current_ability = student.ability_levels.get(skill_name, 0.5)
            improvement = current_ability - start_ability
            if abs(improvement) > 0.01:  # Only track significant changes
                improvements['skill_improvements'][skill_name] = {
                    'start': start_ability,
                    'end': current_ability,
                    'change': improvement
                }

    return {
        'success': True,
        'session_end_time': datetime.now().isoformat(),
        'improvements': improvements
    }

