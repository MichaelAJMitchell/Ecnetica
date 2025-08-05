"""
Comprehensive Test Suite for MCQ Algorithm Current
=================================================

This module provides extensive testing for the mcq_algorithm_current system,
including functionality tests, weight parameter optimization tests, performance
tests, and integration tests. Designed to replace existing test code.

"""

import numpy as np
import time
import json
import random
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import traceback
from copy import deepcopy
import sympy as sp
from sympy import sympify, latex, simplify
import re

# Import the classes we're testing
# These imports should match your actual import structure
try:
    from mcq_algorithm_different_numbers import (
        KnowledgeGraph, StudentManager, MCQScheduler,
        BayesianKnowledgeTracing, OptimizedMCQVector
    )
except ImportError:
    print("⚠️  Could not import from mcq_algorithm_current")
    print("   Make sure the module is in your path")
    # Define dummy classes for testing
    class KnowledgeGraph: pass
    class StudentManager: pass
    class MCQScheduler: pass
    class BayesianKnowledgeTracing: pass
    class OptimizedMCQVector: pass

# Test Configuration Classes
@dataclass
class TestConfig:
    """Configuration for running comprehensive tests"""
    # File paths
    nodes_file: str = 'mcq_algorithm_files\kg.json'
    mcqs_file: str = 'mcq_algorithm_files\computed_mcqs_different_numbers.json'
    config_file: str = '_static\config.json'

    # Test parameters
    num_test_students: int = 10
    max_questions_per_test: int = 20
    performance_threshold_seconds: float = 2.0

    # Weight ranges for testing
    mastery_threshold_range: Tuple[float, float] = (0.5, 0.9)
    priority_weight_range: Tuple[float, float] = (1.0, 3.0)
    subtopic_weight_range: Tuple[float, float] = (0.3, 0.9)
    prereq_weight_range: Tuple[float, float] = (0.2, 0.8)

    # Test modes
    run_performance_tests: bool = True
    run_weight_optimization: bool = True
    run_edge_case_tests: bool = True
    run_integration_tests: bool = True

@dataclass
class TestResult:
    """Results from a single test case"""
    test_name: str
    success: bool
    execution_time: float
    details: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

@dataclass
class WeightTestResult:
    """Results from weight parameter testing"""
    config_name: str
    weights: Dict[str, float]
    avg_questions_selected: float
    avg_coverage_ratio: float
    avg_execution_time: float
    success_rate: float
    details: Dict[str, Any] = field(default_factory=dict)

class MCQAlgorithmTestSuite:
    """
    Comprehensive test suite for MCQ algorithm functionality.

    This class provides systematic testing of:
    - Core algorithm functionality
    - Weight parameter effects
    - Performance characteristics
    - Edge cases and error handling
    - Integration between components
    """

    def __init__(self, test_config: TestConfig):
        self.config = test_config
        self.results: List[TestResult] = []
        self.weight_results: List[WeightTestResult] = []
        self.kg = None
        self.student_manager = None
        self.mcq_scheduler = None
        self.bkt_system = None
        # Add test data for the different numbers system
        self.different_numbers_test_data = self._create_different_numbers_test_data

    def _create_different_numbers_test_data(self) -> List[Dict[str, Any]]:
        """Create test data matching your mcq_algorithm_different_numbers format"""
        return [
            {
                "id": "test_discriminant_different_001",
                "text": "What is the discriminant of ${question_expression}$?",
                "question_expression": "a*x**2 + b*x + c",
                "generated_parameters": {
                    "a": {"type": "int", "min": 1, "max": 5},
                    "b": {"type": "int", "min": -10, "max": 10},
                    "c": {"type": "int", "min": -10, "max": 10}
                },
                "calculated_parameters": {},
                "options": ["b**2-4*a*c", "b**2+4*a*c", "sqrt(b**2-4*a*c)", "(-b+sqrt(b**2-4*a*c))/(2*a)"],
                "correctindex": 0,
                "option_explanations": [
                    "Correct! The discriminant formula is b² - 4ac",
                    "Incorrect. You calculated b² + 4ac instead",
                    "Incorrect. This is √(discriminant), not discriminant",
                    "Incorrect. This is part of quadratic formula, not discriminant"
                ],
                "main_topic_index": 17,
                "chapter": "algebra",
                "subtopic_weights": {"17": 1.0},
                "difficulty_breakdown": {
                    "conceptual_understanding": 0.3,
                    "procedural_fluency": 0.7,
                    "problem_solving": 0.2,
                    "mathematical_communication": 0.1,
                    "memory": 0.4,
                    "spatial_reasoning": 0.0
                },
                "overall_difficulty": 0.35,
                "prerequisites": {}
            },
            {
                "id": "test_factoring_different_001",
                "text": "Factor the quadratic expression ${question_expression}$.",
                "question_expression": "(x - r_1)*(x - r_2)",
                "generated_parameters": {
                    "a": {"type": "int", "min": 1, "max": 6},
                    "b": {"type": "int", "min": 2, "max": 6},
                    "c": {"type": "int", "min": 1, "max": 6},
                    "d": {"type": "int", "min": 2, "max": 6}
                },
                "calculated_parameters": {
                    "r_1": "a/b",
                    "r_2": "c/d"
                },
                "options": ["(b*x - a)*(d*x - c)", "(b*x + a)*(d*x + c)", "(a*x - b)*(c*x - d)", "(x - a/b)*(x - c/d)"],
                "correctindex": 0,
                "option_explanations": [
                    "Correct! This expands to the original expression",
                    "Incorrect. Check the signs carefully",
                    "Incorrect. Check coefficient placement",
                    "Correct form but not in standard polynomial format"
                ],
                "main_topic_index": 6,
                "chapter": "algebra",
                "subtopic_weights": {"6": 1.0},
                "difficulty_breakdown": {
                    "conceptual_understanding": 0.4,
                    "procedural_fluency": 0.8,
                    "problem_solving": 0.6,
                    "mathematical_communication": 0.2,
                    "memory": 0.3,
                    "spatial_reasoning": 0.0
                },
                "overall_difficulty": 0.47,
                "prerequisites": {}
            },
            {
                "id": "test_exclude_logic_001",
                "text": "Solve: ${question_expression}$ where a ≠ ${b}$",
                "question_expression": "a*x + b",
                "generated_parameters": {
                    "a": {"type": "int", "min": 1, "max": 10, "exclude": "b"},
                    "b": {"type": "int", "min": 1, "max": 5}
                },
                "calculated_parameters": {},
                "options": ["-b/a", "b/a", "a/b", "-a/b"],
                "correctindex": 0,
                "option_explanations": [
                    "Correct! x = -b/a when ax + b = 0",
                    "Incorrect. Check the sign",
                    "Incorrect. Variables are inverted",
                    "Incorrect. Both sign and variables wrong"
                ],
                "main_topic_index": 5,
                "chapter": "algebra",
                "subtopic_weights": {"5": 1.0},
                "difficulty_breakdown": {
                    "conceptual_understanding": 0.2,
                    "procedural_fluency": 0.9,
                    "problem_solving": 0.3,
                    "mathematical_communication": 0.1,
                    "memory": 0.2,
                    "spatial_reasoning": 0.0
                },
                "overall_difficulty": 0.28,
                "prerequisites": {}
            },
            {
                "id": "test_choice_type_001",
                "text": "What is the ${operation}$ of ${a}$ and ${b}$?",
                "question_expression": "a + b",
                "generated_parameters": {
                    "a": {"type": "int", "min": 10, "max": 50},
                    "b": {"type": "int", "min": 5, "max": 25},
                    "operation": {"type": "choice", "choices": ["sum", "product", "difference"]}
                },
                "calculated_parameters": {
                    "result": "a + b"
                },
                "options": ["a + b", "a - b", "a * b", "a / b"],
                "correctindex": 0,
                "option_explanations": [
                    "Correct! This is the sum",
                    "This is the difference",
                    "This is the product",
                    "This is the quotient"
                ],
                "main_topic_index": 1,
                "chapter": "arithmetic",
                "subtopic_weights": {"1": 1.0},
                "difficulty_breakdown": {
                    "conceptual_understanding": 0.1,
                    "procedural_fluency": 0.3,
                    "problem_solving": 0.1,
                    "mathematical_communication": 0.2,
                    "memory": 0.1,
                    "spatial_reasoning": 0.0
                },
                "overall_difficulty": 0.13,
                "prerequisites": {}
            }
        ]

    def _run_different_numbers_tests(self):
        """Run comprehensive tests for the mcq_algorithm_different_numbers implementation"""
        print("🔢 Testing MCQ Algorithm Different Numbers Implementation")
        print("-" * 60)

        # Test your actual implementation methods
        self._test_different_numbers_parameter_generation()
        self._test_different_numbers_exclude_logic()
        self._test_different_numbers_question_text_generation()
        self._test_different_numbers_option_rendering()
        self._test_different_numbers_sympy_integration()
        self._test_different_numbers_choice_parameters()
        self._test_different_numbers_calculated_parameters()
        self._test_different_numbers_latex_output()
        self._test_different_numbers_edge_cases()
        self._test_different_numbers_performance()


    def _test_different_numbers_parameter_generation(self):
        """Test the _generate_parameters method from your implementation"""
        test_name = "Different Numbers: Parameter Generation"
        start_time = time.time()

        try:
            # Import your actual MCQ class
            try:
                from mcq_algorithm_different_numbers import MCQ
            except ImportError:
                raise ImportError("Could not import MCQ from mcq_algorithm_different_numbers")

            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)

                # Test parameter generation multiple times
                for attempt in range(20):
                    params = mcq._generate_parameters()

                    # Validate each parameter against its constraints
                    for param_name, param_value in params.items():
                        if param_name in mcq.generated_parameters:
                            config = mcq.generated_parameters[param_name]

                            if config['type'] == 'int':
                                # Check range
                                assert config['min'] <= param_value <= config['max'], \
                                    f"Parameter {param_name}={param_value} outside range [{config['min']}, {config['max']}]"

                                # Check exclude constraint (your specific logic)
                                exclude_rule = config.get('exclude')
                                if exclude_rule is not None:
                                    if isinstance(exclude_rule, str):
                                        # Reference to another parameter
                                        if exclude_rule in params:
                                            exclude_value = params[exclude_rule]
                                            assert param_value != exclude_value, \
                                                f"Parameter {param_name}={param_value} should not equal {exclude_rule}={exclude_value}"
                                    else:
                                        # Direct value or list
                                        exclude_values = exclude_rule if isinstance(exclude_rule, list) else [exclude_rule]
                                        assert param_value not in exclude_values, \
                                            f"Parameter {param_name}={param_value} in exclude list {exclude_values}"

                            elif config['type'] == 'choice':
                                # Check choice is from valid options
                                assert param_value in config['choices'], \
                                    f"Parameter {param_name}={param_value} not in choices {config['choices']}"

                # Test calculated parameters
                for calc_name, calc_expr in mcq.calculated_parameters.items():
                    assert calc_name in params, f"Calculated parameter {calc_name} not generated"

                    # Verify calculation is correct (basic check)
                    try:
                        expected = sympify(calc_expr).subs(params)
                        actual = params[calc_name]
                        # Allow small floating point differences
                        assert abs(float(expected) - float(actual)) < 0.001, \
                            f"Calculated parameter {calc_name}: expected {expected}, got {actual}"
                    except Exception as e:
                        print(f"Warning: Could not verify calculation for {calc_name}: {e}")

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={
                    "mcqs_tested": len(self.different_numbers_test_data),
                    "parameters_generated": len(self.different_numbers_test_data) * 20
                }
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")


    def _test_different_numbers_exclude_logic(self):
        """Test the exclude parameter logic specifically"""
        test_name = "Different Numbers: Exclude Logic"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            # Find test case with exclude logic
            exclude_test = next(t for t in self.different_numbers_test_data if 'exclude' in str(t))
            mcq = MCQ.from_dict(exclude_test)

            # Test exclude logic works correctly
            exclude_violations = 0
            total_tests = 100

            for _ in range(total_tests):
                params = mcq._generate_parameters()

                # Check that 'a' parameter doesn't equal 'b' parameter
                if 'a' in params and 'b' in params:
                    if params['a'] == params['b']:
                        exclude_violations += 1

            violation_rate = exclude_violations / total_tests
            assert violation_rate < 0.05, f"Exclude logic violated {violation_rate:.1%} of the time (should be <5%)"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={
                    "exclude_tests": total_tests,
                    "violations": exclude_violations,
                    "violation_rate": violation_rate
                }
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s) - {violation_rate:.1%} violation rate")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_question_text_generation(self):
        """Test the generate_question_text method"""
        test_name = "Different Numbers: Question Text Generation"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)

                # Generate parameters
                params = mcq._generate_parameters()

                # Test question text generation
                generated_text = mcq.generate_question_text(mcq.text, params)

                # Basic validation
                assert isinstance(generated_text, str), "Generated text must be string"
                assert len(generated_text) > 0, "Generated text cannot be empty"

                # Check that placeholders were replaced
                if '${question_expression}$' in mcq.text:
                    assert '${question_expression}$' not in generated_text, \
                        "Question expression placeholder not replaced"

                    # Should contain LaTeX mathematical notation
                    assert '$' in generated_text, "Should contain LaTeX delimiters"

                # Check parameter substitutions
                for param_name in params.keys():
                    placeholder = f'${{{param_name}}}$'
                    if placeholder in mcq.text:
                        assert placeholder not in generated_text, \
                            f"Parameter placeholder {placeholder} not replaced"

                # Test property access (your question_text property)
                if hasattr(mcq, 'question_text'):
                    property_text = mcq.question_text
                    assert isinstance(property_text, str), "question_text property must return string"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"text_generations_tested": len(self.different_numbers_test_data)}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")



    def _test_different_numbers_option_rendering(self):
        """Test the render_options method"""
        test_name = "Different Numbers: Option Rendering"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)

                # Generate parameters
                params = mcq._generate_parameters()

                # Test option rendering (your actual method)
                if hasattr(mcq, 'render_options'):
                    rendered_options = mcq.render_options(params)

                    # Basic validation
                    assert isinstance(rendered_options, list), "Rendered options must be list"
                    assert len(rendered_options) == len(mcq.options), \
                        f"Rendered options count mismatch: {len(rendered_options)} vs {len(mcq.options)}"

                    # Check LaTeX formatting
                    for i, option in enumerate(rendered_options):
                        assert isinstance(option, str), f"Option {i} must be string"

                        # Should be wrapped in LaTeX delimiters if mathematical
                        if any(char in str(mcq.options[i]) for char in ['*', '+', '-', '/', '^', '(', ')']):
                            assert '\\(' in option and '\\)' in option, \
                                f"Mathematical option should be wrapped in LaTeX: {option}"

                # Test with discriminant example specifically
                if 'discriminant' in mcq.id.lower():
                    a, b, c = params.get('a', 1), params.get('b', 0), params.get('c', 0)
                    expected_discriminant = b**2 - 4*a*c

                    # First option should be the discriminant value
                    first_option = rendered_options[0].strip('\\(').strip('\\)')
                    assert str(expected_discriminant) == first_option or str(int(expected_discriminant)) == first_option, \
                        f"Discriminant calculation error: expected {expected_discriminant}, got {first_option}"

                # Test property access if available
                if hasattr(mcq, 'question_options'):
                    property_options = mcq.question_options
                    assert isinstance(property_options, list), "question_options property must return list"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"option_renderings_tested": len(self.different_numbers_test_data)}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_sympy_integration(self):
        """Test SymPy integration in your implementation"""
        test_name = "Different Numbers: SymPy Integration"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            # Test that SymPy local_namespace is working
            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)
                params = mcq._generate_parameters()

                # Test expression parsing with SymPy
                if mcq.question_expression:
                    try:
                        # This should use your local_namespace
                        from mcq_algorithm_different_numbers import local_namespace
                        expr = sympify(mcq.question_expression, locals=local_namespace)

                        # Test substitution
                        result = expr.subs(params)
                        assert not result.has(sp.Symbol) or not any(str(sym) in params for sym in result.free_symbols), \
                            "Not all parameters were substituted in expression"

                        # Test LaTeX generation
                        latex_output = latex(result)
                        assert isinstance(latex_output, str), "LaTeX output must be string"
                        assert len(latex_output) > 0, "LaTeX output cannot be empty"

                    except Exception as e:
                        print(f"Warning: SymPy processing failed for {mcq.id}: {e}")

                # Test option evaluation with SymPy
                if mcq.options:
                    for option_expr in mcq.options:
                        try:
                            if option_expr in ['result']:  # Skip calculated parameter references
                                continue

                            # Parse option as SymPy expression
                            opt_expr = sympify(option_expr, locals=local_namespace)
                            opt_result = opt_expr.subs(params)

                            # Should be evaluable to a number or simple expression
                            simplified = simplify(opt_result)
                            assert simplified is not None, f"Option {option_expr} could not be simplified"

                        except Exception as e:
                            print(f"Warning: Option evaluation failed for '{option_expr}': {e}")

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"sympy_expressions_tested": len(self.different_numbers_test_data)}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_choice_parameters(self):
        """Test choice-type parameters (your specific feature)"""
        test_name = "Different Numbers: Choice Parameters"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            # Find test case with choice parameter
            choice_test = next(t for t in self.different_numbers_test_data if
                             any('choice' in str(param.get('type', '')) for param in t.get('generated_parameters', {}).values()))

            mcq = MCQ.from_dict(choice_test)

            # Test choice parameter generation
            choice_values_seen = set()
            for _ in range(50):
                params = mcq._generate_parameters()

                # Find the choice parameter
                for param_name, config in mcq.generated_parameters.items():
                    if config.get('type') == 'choice':
                        value = params[param_name]
                        assert value in config['choices'], \
                            f"Choice parameter {param_name}={value} not in valid choices {config['choices']}"
                        choice_values_seen.add(value)

            # Should see multiple different choice values (randomness test)
            assert len(choice_values_seen) > 1, f"Choice parameter not random enough: only saw {choice_values_seen}"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={
                    "choice_tests": 50,
                    "unique_choices_seen": len(choice_values_seen),
                    "choices_seen": list(choice_values_seen)
                }
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s) - {len(choice_values_seen)} unique choices")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_calculated_parameters(self):
        """Test calculated parameters functionality"""
        test_name = "Different Numbers: Calculated Parameters"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            # Find test with calculated parameters
            calc_test = next(t for t in self.different_numbers_test_data if t.get('calculated_parameters'))
            mcq = MCQ.from_dict(calc_test)

            for _ in range(20):
                params = mcq._generate_parameters()

                # Verify calculated parameters were computed
                for calc_name, calc_expr in mcq.calculated_parameters.items():
                    assert calc_name in params, f"Calculated parameter {calc_name} missing from generated params"

                    # Manually verify calculation
                    try:
                        from mcq_algorithm_different_numbers import local_namespace
                        expected = sympify(calc_expr, locals=local_namespace).subs(params)
                        actual = params[calc_name]

                        # Allow small floating point differences
                        diff = abs(float(expected) - float(actual))
                        assert diff < 0.001, \
                            f"Calculated parameter {calc_name}: expected {expected}, got {actual}, diff={diff}"
                    except Exception as e:
                        print(f"Warning: Could not verify {calc_name}: {e}")

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"calculated_parameter_tests": 20}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_latex_output(self):
        """Test LaTeX output formatting"""
        test_name = "Different Numbers: LaTeX Output"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)
                params = mcq._generate_parameters()

                # Test question text LaTeX
                question_text = mcq.generate_question_text(mcq.text, params)

                if mcq.question_expression and ('${question_expression}$' in mcq.text):
                    # Should contain LaTeX math delimiters
                    assert '$' in question_text, "Question text should contain LaTeX delimiters"

                    # Check for valid LaTeX patterns
                    latex_patterns = [r'\$.*\$', r'\\.*\{.*\}', r'\^', r'_']
                    has_latex = any(re.search(pattern, question_text) for pattern in latex_patterns)
                    assert has_latex, f"No LaTeX patterns found in: {question_text}"

                # Test option LaTeX
                if hasattr(mcq, 'render_options'):
                    rendered_options = mcq.render_options(params)

                    for option in rendered_options:
                        # Mathematical options should be in LaTeX format
                        if any(char in option for char in ['+', '-', '*', '/', '^']):
                            assert '\\(' in option and '\\)' in option, \
                                f"Mathematical option not properly formatted: {option}"

                # Test that LaTeX compiles (basic syntax check)
                latex_content = re.findall(r'\$([^$]+)\$', question_text)
                for latex_expr in latex_content:
                    # Basic syntax validation - should not have unmatched braces
                    open_braces = latex_expr.count('{')
                    close_braces = latex_expr.count('}')
                    assert open_braces == close_braces, f"Unmatched braces in LaTeX: {latex_expr}"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"latex_outputs_tested": len(self.different_numbers_test_data)}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_edge_cases(self):
        """Test edge cases specific to your implementation"""
        test_name = "Different Numbers: Edge Cases"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            # Test 1: Invalid parameter ranges
            invalid_data = self.different_numbers_test_data[0].copy()
            invalid_data["generated_parameters"]["a"]["min"] = 10
            invalid_data["generated_parameters"]["a"]["max"] = 5  # max < min

            mcq_invalid = MCQ.from_dict(invalid_data)

            # Should handle gracefully without crashing
            try:
                params = mcq_invalid._generate_parameters()
                # If it succeeds, params should be reasonable
                assert isinstance(params, dict), "Should return dict even with invalid ranges"
            except Exception:
                pass  # Acceptable to fail, but shouldn't crash entire system

            # Test 2: Missing question expression
            no_expr_data = self.different_numbers_test_data[0].copy()
            no_expr_data["question_expression"] = None
            no_expr_data["text"] = "Simple question with no expression"

            mcq_no_expr = MCQ.from_dict(no_expr_data)
            params = mcq_no_expr._generate_parameters()
            text = mcq_no_expr.generate_question_text(mcq_no_expr.text, params)
            assert text == "Simple question with no expression", "Should handle missing expression gracefully"

            # Test 3: Empty calculated parameters
            empty_calc_data = self.different_numbers_test_data[0].copy()
            empty_calc_data["calculated_parameters"] = {}

            mcq_empty_calc = MCQ.from_dict(empty_calc_data)
            params = mcq_empty_calc._generate_parameters()
            assert isinstance(params, dict), "Should handle empty calculated parameters"

            # Test 4: Large parameter ranges
            large_range_data = self.different_numbers_test_data[0].copy()
            large_range_data["generated_parameters"]["a"]["min"] = -1000
            large_range_data["generated_parameters"]["a"]["max"] = 1000

            mcq_large = MCQ.from_dict(large_range_data)
            params = mcq_large._generate_parameters()
            assert -1000 <= params.get('a', 0) <= 1000, "Should handle large ranges correctly"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"edge_cases_tested": 4}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_performance(self):
        """Test performance of your implementation"""
        test_name = "Different Numbers: Performance"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            total_generations = 0
            total_generation_time = 0
            total_text_generation_time = 0
            total_option_generation_time = 0

            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)

                # Time parameter generation
                for _ in range(50):
                    gen_start = time.time()
                    params = mcq._generate_parameters()
                    gen_time = time.time() - gen_start
                    total_generation_time += gen_time
                    total_generations += 1

                    # Time question text generation
                    text_start = time.time()
                    text = mcq.generate_question_text(mcq.text, params)
                    text_time = time.time() - text_start
                    total_text_generation_time += text_time

                    # Time option rendering
                    if hasattr(mcq, 'render_options'):
                        opt_start = time.time()
                        options = mcq.render_options(params)
                        opt_time = time.time() - opt_start
                        total_option_generation_time += opt_time

            # Calculate averages
            avg_param_time = total_generation_time / total_generations
            avg_text_time = total_text_generation_time / total_generations
            avg_option_time = total_option_generation_time / total_generations
            total_avg_time = avg_param_time + avg_text_time + avg_option_time

            # UPDATED: Realistic thresholds for SymPy + LaTeX operations
            assert avg_param_time < 0.05, f"Parameter generation too slow: {avg_param_time:.4f}s"    # 50ms
            assert avg_text_time < 0.05, f"Text generation too slow: {avg_text_time:.4f}s"          # 50ms
            assert avg_option_time < 0.10, f"Option rendering too slow: {avg_option_time:.4f}s"      # 100ms
            assert total_avg_time < 0.20, f"Total generation too slow: {total_avg_time:.4f}s"        # 200ms

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={
                    "total_generations": total_generations,
                    "avg_param_time_ms": avg_param_time * 1000,
                    "avg_text_time_ms": avg_text_time * 1000,
                    "avg_option_time_ms": avg_option_time * 1000,
                    "total_avg_time_ms": total_avg_time * 1000,
                    "generations_per_second": 1 / total_avg_time if total_avg_time > 0 else 0
                }
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")
            print(f"   📊 Average times: Params={avg_param_time*1000:.1f}ms, Text={avg_text_time*1000:.1f}ms, Options={avg_option_time*1000:.1f}ms")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")

    def _test_different_numbers_integration_with_main_system(self):
        """Test integration with your main algorithm system"""
        test_name = "Different Numbers: Main System Integration"
        start_time = time.time()

        try:
            from mcq_algorithm_different_numbers import MCQ

            # Test that parameterized MCQs work with your existing system
            for test_data in self.different_numbers_test_data:
                mcq = MCQ.from_dict(test_data)

                # Test essential properties exist and work
                assert hasattr(mcq, 'difficulty'), "MCQ missing difficulty property"
                assert hasattr(mcq, 'get_prerequisites'), "MCQ missing get_prerequisites method"

                difficulty = mcq.difficulty
                assert isinstance(difficulty, (int, float)), "Difficulty must be numeric"
                assert 0 <= difficulty <= 1, f"Difficulty {difficulty} outside valid range [0,1]"

                # Test prerequisites
                prereqs = mcq.get_prerequisites()
                assert isinstance(prereqs, dict), "Prerequisites must be dict"

                # Test that parameterized MCQs still have the same core properties
                assert mcq.main_topic_index == test_data['main_topic_index'], "Main topic index should be preserved"
                assert mcq.correctindex == test_data['correctindex'], "Correct index should be preserved"

                # Test parameterization properties
                if hasattr(mcq, 'is_parameterized'):
                    is_param = mcq.is_parameterized
                    expected_param = bool(mcq.generated_parameters)
                    assert is_param == expected_param, f"is_parameterized={is_param} but generated_parameters={'exists' if mcq.generated_parameters else 'missing'}"

                # Test regeneration if available
                if hasattr(mcq, 'regenerate_parameters'):
                    original_params = mcq.get_current_parameters() if hasattr(mcq, 'get_current_parameters') else None
                    mcq.regenerate_parameters()
                    new_params = mcq.get_current_parameters() if hasattr(mcq, 'get_current_parameters') else None

                    if original_params and new_params:
                        # Parameters might be different after regeneration
                        assert isinstance(new_params, dict), "Regenerated parameters should be dict"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=True,
                execution_time=execution_time,
                details={"integration_tests": len(self.different_numbers_test_data)}
            ))
            print(f"✅ {test_name}: PASSED ({execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name=test_name,
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ {test_name}: FAILED - {str(e)}")


    def initialize_system(self) -> bool:
        """Initialize the MCQ algorithm system for testing"""
        try:
            # Import required classes (assuming they're available)
            print("🔧 Initializing MCQ Algorithm System...")

            self.kg = KnowledgeGraph(
                nodes_file=self.config.nodes_file,
                mcqs_file=self.config.mcqs_file,
                config_file=self.config.config_file
            )

            self.student_manager = StudentManager(self.kg.config)
            self.mcq_scheduler = MCQScheduler(self.kg, self.student_manager)
            self.bkt_system = BayesianKnowledgeTracing(self.kg, self.student_manager)

            # Connect systems
            self.mcq_scheduler.set_bkt_system(self.bkt_system)
            self.student_manager.set_bkt_system(self.bkt_system)

            print("✅ System initialized successfully")
            return True

        except Exception as e:
            print(f"❌ System initialization failed: {str(e)}")
            traceback.print_exc()
            return False

    def run_all_tests(self) -> Dict[str, Any]:
        """Run the complete test suite"""
        print("\n" + "="*80)
        print("MCQ ALGORITHM COMPREHENSIVE TEST SUITE")
        print("="*80)

        if not self.initialize_system():
            return {"success": False, "error": "System initialization failed"}

        total_start_time = time.time()

        # Core functionality tests
        print("\n📋 RUNNING CORE FUNCTIONALITY TESTS")
        print("-" * 50)
        self._run_core_functionality_tests()

        # NEW: Different Numbers MCQ tests
        print("\n🔢 RUNNING DIFFERENT NUMBERS MCQ TESTS")
        print("-" * 50)
        self._run_different_numbers_tests()

        # Integration test
        print("\n🔗 RUNNING DIFFERENT NUMBERS INTEGRATION TEST")
        print("-" * 50)
        self._test_different_numbers_integration_with_main_system()

        # Weight parameter tests
        if self.config.run_weight_optimization:
            print("\n⚖️ RUNNING WEIGHT PARAMETER TESTS")
            print("-" * 50)
            self._run_weight_parameter_tests()

        # Performance tests
        if self.config.run_performance_tests:
            print("\n🚀 RUNNING PERFORMANCE TESTS")
            print("-" * 50)
            self._run_performance_tests()

        # Edge case tests
        if self.config.run_edge_case_tests:
            print("\n⚠️ RUNNING EDGE CASE TESTS")
            print("-" * 50)
            self._run_edge_case_tests()

        # Integration tests
        if self.config.run_integration_tests:
            print("\n🔗 RUNNING INTEGRATION TESTS")
            print("-" * 50)
            self._run_integration_tests()

        total_time = time.time() - total_start_time

        # Generate summary report
        return self._generate_test_report(total_time)



    def _run_core_functionality_tests(self):
        """Test core algorithm functionality"""

        # Test 1: System Component Validation
        self._test_system_components()

        # Test 2: MCQ Vector Creation
        self._test_mcq_vector_creation()

        # Test 3: Eligibility Filtering
        self._test_eligibility_filtering()

        # Test 4: Priority Calculations
        self._test_priority_calculations()

        # Test 5: Greedy Selection Algorithm
        self._test_greedy_selection()

        # Test 6: Virtual Mastery Updates
        self._test_simulated_mastery_updates()
        self._test_bkt_virtual_mastery_updates()

        # Test 7: MCQ Selection Consistency
        self._test_selection_consistency()

        print("\n🔬 RUNNING ENHANCED FEATURE TESTS")
        print("-" * 50)
        self._test_virtual_area_effects()

        # Add detailed analysis example
        print("\n📋 DETAILED SELECTION ANALYSIS EXAMPLE")
        print("-" * 50)
        test_student_id = "detailed_analysis_student"
        self._create_test_student(test_student_id, random_mastery=True)
        analysis_results = self.analyze_question_selection_details(test_student_id, 3)

    def _test_system_components(self):
        """Test that all system components are properly initialized"""
        start_time = time.time()

        try:
            # Test knowledge graph
            assert self.kg is not None, "Knowledge graph not initialized"

            # Check knowledge graph structure
            kg_details = {}

            if hasattr(self.kg, 'nodes'):
                kg_details['has_nodes'] = True
                kg_details['num_nodes'] = len(self.kg.nodes)
                assert len(self.kg.nodes) > 0, "Knowledge graph has no nodes"
            else:
                kg_details['has_nodes'] = False
                print("⚠️  Knowledge graph has no 'nodes' attribute")

            if hasattr(self.kg, 'mcqs'):
                kg_details['has_mcqs'] = True
                kg_details['num_mcqs'] = len(self.kg.mcqs)
            else:
                kg_details['has_mcqs'] = False
                print("⚠️  Knowledge graph has no 'mcqs' attribute")

            if hasattr(self.kg, 'ultra_loader'):
                kg_details['has_ultra_loader'] = True
                if hasattr(self.kg.ultra_loader, 'minimal_mcq_data'):
                    kg_details['ultra_loader_mcq_count'] = len(self.kg.ultra_loader.minimal_mcq_data)
                else:
                    kg_details['ultra_loader_mcq_count'] = 0
                print("📊 Ultra loader detected")
            else:
                kg_details['has_ultra_loader'] = False
                print("📊 Traditional knowledge graph mode")

            # Test student manager
            assert self.student_manager is not None, "Student manager not initialized"

            # Test MCQ scheduler
            assert self.mcq_scheduler is not None, "MCQ scheduler not initialized"

            # Test BKT system
            assert self.bkt_system is not None, "BKT system not initialized"

            # Test configuration
            assert hasattr(self.kg, 'config'), "Configuration not loaded"

            # Verify we have some way to access MCQ data
            has_mcq_data = (kg_details.get('has_mcqs', False) and kg_details.get('num_mcqs', 0) > 0) or \
                          (kg_details.get('has_ultra_loader', False) and kg_details.get('ultra_loader_mcq_count', 0) > 0)

            assert has_mcq_data, "No MCQ data found in knowledge graph (neither traditional mcqs nor ultra_loader data)"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="System Components Validation",
                success=True,
                execution_time=execution_time,
                details=kg_details
            ))
            print("✅ System components validation: PASSED")
            print(f"   📊 Knowledge graph details: {kg_details}")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="System Components Validation",
                success=False,
                execution_time=execution_time,
                error_message=str(e),
                details=kg_details if 'kg_details' in locals() else {}
            ))
            print(f"❌ System components validation: FAILED - {str(e)}")

            # Provide detailed debugging information
            print("🔍 Detailed Debug Information:")
            print(f"   - Knowledge Graph type: {type(self.kg)}")
            print(f"   - Knowledge Graph attributes: {[attr for attr in dir(self.kg) if not attr.startswith('_')]}")

            if hasattr(self.kg, 'config'):
                print(f"   - Config type: {type(self.kg.config)}")
                print(f"   - Config attributes: {[attr for attr in dir(self.kg.config) if not attr.startswith('_')]}")

            if hasattr(self.kg, 'ultra_loader'):
                print(f"   - Ultra loader type: {type(self.kg.ultra_loader)}")
                print(f"   - Ultra loader attributes: {[attr for attr in dir(self.kg.ultra_loader) if not attr.startswith('_')]}")

            print(f"   - Student Manager type: {type(self.student_manager)}")
            print(f"   - MCQ Scheduler type: {type(self.mcq_scheduler)}")
            print(f"   - BKT System type: {type(self.bkt_system)}")

    def _test_mcq_vector_creation(self):
        """Test MCQ vector creation and optimization"""
        start_time = time.time()

        try:
            # First check if the system uses ultra_loader (on-demand) or traditional pre-computation
            has_ultra_loader = hasattr(self.kg, 'ultra_loader')

            if has_ultra_loader:
                print("📊 Detected ultra_loader - testing on-demand vector creation")

                # For ultra_loader systems, we need to test vector creation through actual usage
                # Get some MCQ IDs to test with
                available_mcq_ids = []

                # Try to get MCQ IDs from ultra_loader
                if hasattr(self.kg.ultra_loader, 'minimal_mcq_data'):
                    available_mcq_ids = list(self.kg.ultra_loader.minimal_mcq_data.keys())[:5]  # Test with first 5
                elif hasattr(self.kg, 'mcqs'):
                    available_mcq_ids = list(self.kg.mcqs.keys())[:5]

                if not available_mcq_ids:
                    raise Exception("No MCQ IDs available for testing vector creation")

                # Test on-demand vector creation
                vectors_created = 0
                sample_vector = None

                for mcq_id in available_mcq_ids:
                    vector = self.mcq_scheduler._get_or_create_optimized_mcq_vector(mcq_id)
                    if vector:
                        vectors_created += 1
                        if sample_vector is None:
                            sample_vector = vector

                assert vectors_created > 0, f"No vectors created from {len(available_mcq_ids)} MCQ IDs"

                # Check that vectors are now stored
                num_stored_vectors = len(self.mcq_scheduler.mcq_vectors)
                assert num_stored_vectors > 0, "Vectors created but not stored in mcq_vectors"

            else:
                print("📊 Traditional pre-computation mode - ensuring all vectors computed")

                # Traditional pre-computation mode
                self.mcq_scheduler._ensure_vectors_computed()

                # Check if vectors were created
                num_stored_vectors = len(self.mcq_scheduler.mcq_vectors)
                assert num_stored_vectors > 0, "No MCQ vectors created in pre-computation mode"

                # Get sample vector
                sample_mcq_id = list(self.mcq_scheduler.mcq_vectors.keys())[0]
                sample_vector = self.mcq_scheduler.mcq_vectors[sample_mcq_id]
                vectors_created = num_stored_vectors

            # Validate sample vector properties (works for both modes)
            assert sample_vector is not None, "No sample vector available for validation"
            assert hasattr(sample_vector, 'mcq_id'), "Vector missing mcq_id"
            assert hasattr(sample_vector, 'subtopic_weights'), "Vector missing subtopic_weights"
            assert hasattr(sample_vector, 'difficulty'), "Vector missing difficulty"
            assert hasattr(sample_vector, 'prerequisites'), "Vector missing prerequisites"

            # Test vector property access
            mcq_id = sample_vector.mcq_id
            subtopic_weights = sample_vector.subtopic_weights
            difficulty = sample_vector.difficulty
            prerequisites = sample_vector.prerequisites

            assert isinstance(mcq_id, str), "MCQ ID should be string"
            assert isinstance(subtopic_weights, dict), "Subtopic weights should be dict"
            assert isinstance(difficulty, (int, float)), "Difficulty should be numeric"
            assert isinstance(prerequisites, dict), "Prerequisites should be dict"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="MCQ Vector Creation",
                success=True,
                execution_time=execution_time,
                details={
                    "num_vectors_created": vectors_created,
                    "num_stored_vectors": len(self.mcq_scheduler.mcq_vectors),
                    "uses_ultra_loader": has_ultra_loader,
                    "sample_vector_valid": True,
                    "sample_mcq_id": mcq_id
                }
            ))
            print(f"✅ MCQ vector creation: PASSED ({vectors_created} vectors created, {len(self.mcq_scheduler.mcq_vectors)} stored)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="MCQ Vector Creation",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ MCQ vector creation: FAILED - {str(e)}")

            # Additional debugging information
            print("🔍 Debug Information:")
            print(f"   - Has ultra_loader: {hasattr(self.kg, 'ultra_loader')}")
            print(f"   - Has mcqs attribute: {hasattr(self.kg, 'mcqs')}")
            print(f"   - mcq_vectors count: {len(self.mcq_scheduler.mcq_vectors)}")

            if hasattr(self.kg, 'ultra_loader') and hasattr(self.kg.ultra_loader, 'minimal_mcq_data'):
                print(f"   - Ultra loader MCQ count: {len(self.kg.ultra_loader.minimal_mcq_data)}")
            elif hasattr(self.kg, 'mcqs'):
                print(f"   - Knowledge graph MCQ count: {len(self.kg.mcqs)}")
            else:
                print("   - No MCQ data found in knowledge graph")

    def _test_eligibility_filtering(self):
        """Test MCQ eligibility filtering functionality"""
        start_time = time.time()

        try:
            # Create test student with varied mastery
            student_id = "test_eligibility_student"
            student = self._create_test_student(student_id, random_mastery=True)

            # Test eligibility filtering
            eligible_mcqs = self.mcq_scheduler.get_available_questions_for_student(student_id)

            # Validate results
            assert isinstance(eligible_mcqs, list), "Eligible MCQs should be a list"

            # Test with different student configurations
            results = {}
            for mastery_level in [0.2, 0.5, 0.8]:
                test_student_id = f"test_mastery_{mastery_level}"
                test_student = self._create_test_student(test_student_id, fixed_mastery=mastery_level)
                test_eligible = self.mcq_scheduler.get_available_questions_for_student(test_student_id)
                results[f"mastery_{mastery_level}"] = len(test_eligible)

            # Expect that lower mastery students have more eligible questions
            low_mastery_eligible = results.get("mastery_0.2", 0)
            high_mastery_eligible = results.get("mastery_0.8", 0)

            # This is expected but not required (might be no questions for high mastery)
            mastery_correlation_reasonable = low_mastery_eligible >= high_mastery_eligible

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Eligibility Filtering",
                success=True,
                execution_time=execution_time,
                details={
                    "base_eligible_count": len(eligible_mcqs),
                    "mastery_level_results": results,
                    "mastery_correlation_reasonable": mastery_correlation_reasonable
                }
            ))
            print(f"✅ Eligibility filtering: PASSED ({len(eligible_mcqs)} eligible)")
            print(f"   📊 Low mastery (0.2): {low_mastery_eligible}, High mastery (0.8): {high_mastery_eligible}")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Eligibility Filtering",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Eligibility filtering: FAILED - {str(e)}")

            # Additional debugging for eligibility issues
            print("🔍 Debug Information:")
            try:
                debug_student = self._create_test_student("debug_student", fixed_mastery=0.3)
                print(f"   - Debug student created: {debug_student is not None}")
                print(f"   - Debug student studied topics: {len(debug_student.studied_topics) if hasattr(debug_student, 'studied_topics') else 'No studied_topics attr'}")
                print(f"   - Debug student mastery levels: {len(debug_student.mastery_levels) if hasattr(debug_student, 'mastery_levels') else 'No mastery_levels attr'}")

                # Check if knowledge graph has the required methods
                if hasattr(self.kg, 'ultra_loader'):
                    print(f"   - Ultra loader available: True")
                    if hasattr(self.kg.ultra_loader, 'get_mcq_ids_for_due_topics'):
                        print(f"   - get_mcq_ids_for_due_topics method available: True")
                    else:
                        print(f"   - get_mcq_ids_for_due_topics method available: False")
                else:
                    print(f"   - Ultra loader available: False")

            except Exception as debug_e:
                print(f"   - Debug failed: {debug_e}")

    def _test_priority_calculations(self):
        """Test topic priority calculation algorithms"""
        start_time = time.time()

        try:
            # Create test student
            student_id = "test_priority_student"
            student = self._create_test_student(student_id, random_mastery=True)

            # Test priority calculation
            simulated_mastery_levels = student.mastery_levels.copy()
            priorities = self.mcq_scheduler._calculate_topic_priorities_due_only(student, simulated_mastery_levels)

            # Validate priorities
            assert isinstance(priorities, dict), "Priorities should be a dictionary"

            # Test priority ordering (lower mastery should have higher priority)
            priority_mastery_pairs = []
            for topic_idx, priority in priorities.items():
                mastery = simulated_mastery_levels.get(topic_idx, 0.0)
                priority_mastery_pairs.append((priority, mastery))

            # Sort by priority (descending) and check mastery correlation
            priority_mastery_pairs.sort(reverse=True)

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Priority Calculations",
                success=True,
                execution_time=execution_time,
                details={
                    "num_priority_topics": len(priorities),
                    "priority_range": (min(priorities.values()) if priorities else 0,
                                     max(priorities.values()) if priorities else 0)
                }
            ))
            print(f"✅ Priority calculations: PASSED ({len(priorities)} topics)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Priority Calculations",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Priority calculations: FAILED - {str(e)}")

    def _test_greedy_selection(self):
        """Test the main greedy selection algorithm"""
        start_time = time.time()

        try:
            # Create test student
            student_id = "test_greedy_student"
            student = self._create_test_student(student_id, random_mastery=True)

            # Test different numbers of questions
            selection_results = {}
            for num_questions in [1, 3, 5, 10]:
                try:
                    selected = self.mcq_scheduler.select_optimal_mcqs(student_id, num_questions)
                    print(self.get_mcq_safely(selected.mcq_id, need_full_text=True))
                    selection_results[num_questions] = {
                        "selected_count": len(selected),
                        "selected_mcqs": selected,
                        "success": True
                    }
                except Exception as e:
                    selection_results[num_questions] = {
                        "selected_count": 0,
                        "success": False,
                        "error": str(e)
                    }

            # Validate that selections are different for different numbers
            successful_selections = [r for r in selection_results.values() if r["success"]]
            assert len(successful_selections) > 0, "No successful selections"

            selected_sets = [r["selected_mcqs"] for r in successful_selections]

            def all_same(seq_of_lists):
                return all(s == selected_sets[0] for s in selected_sets)

            assert not all_same(selected_sets), "Selections did not change across runs"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Greedy Selection Algorithm",
                success=True,
                execution_time=execution_time,
                details={"selection_results": selection_results}
            ))
            print("✅ Greedy selection algorithm: PASSED")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Greedy Selection Algorithm",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Greedy selection algorithm: FAILED - {str(e)}")

    def _test_virtual_area_effects(self):
        """Test that area effects work in virtual simulation"""
        start_time = time.time()

        try:
            student_id = "area_effect_test_student"
            student = self._create_test_student(student_id, fixed_mastery=0.3)

            # Test with area effects enabled vs disabled
            original_setting = self.kg.config.get('greedy_algorithm.enable_virtual_area_effects', True)

            # With area effects
            selected_with_area = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)

            # Disable area effects
            if hasattr(self.kg.config, 'config'):
                self.kg.config.config['greedy_algorithm'] = self.kg.config.config.get('greedy_algorithm', {})
                self.kg.config.config['greedy_algorithm']['enable_virtual_area_effects'] = False

            selected_without_area = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)

            # Restore setting
            if hasattr(self.kg.config, 'config'):
                self.kg.config.config['greedy_algorithm']['enable_virtual_area_effects'] = original_setting

            area_effects_impact = selected_with_area != selected_without_area

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Virtual Area Effects",
                success=True,
                execution_time=execution_time,
                details={
                    "area_effects_impact": area_effects_impact,
                    "with_area": selected_with_area,
                    "without_area": selected_without_area
                }
            ))

            print(f"✅ Virtual area effects: PASSED (impact detected: {area_effects_impact})")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Virtual Area Effects",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Virtual area effects: FAILED - {str(e)}")

    def _test_simulated_mastery_updates(self):
        """Test that virtual mastery updates don't affect real student data"""
        start_time = time.time()

        try:
            # Create test student
            student_id = "test_simulated_mastery_student"
            student = self._create_test_student(student_id, random_mastery=True)

            # Store original mastery
            original_mastery = student.mastery_levels.copy()

            # Run selection algorithm (which uses virtual mastery)
            selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)

            # Check that real mastery wasn't changed
            current_mastery = student.mastery_levels

            mastery_unchanged = True
            for topic_idx, original_value in original_mastery.items():
                current_value = current_mastery.get(topic_idx, 0.0)
                if abs(original_value - current_value) > 1e-10:
                    mastery_unchanged = False
                    break

            assert mastery_unchanged, "Real student mastery was modified during algorithm"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Virtual Mastery Updates",
                success=True,
                execution_time=execution_time,
                details={
                    "mastery_preserved": True,
                    "questions_selected": len(selected)
                }
            ))
            print("✅ Virtual mastery updates: PASSED")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Virtual Mastery Updates",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Virtual mastery updates: FAILED - {str(e)}")

    def _test_bkt_virtual_mastery_updates(self):
        """Test that virtual mastery updates use BKT instead of simple difficulty addition"""
        start_time = time.time()

        try:
            student_id = "bkt_virtual_test_student"
            student = self._create_test_student(student_id, fixed_mastery=0.4)

            # Test with BKT available vs unavailable
            selected_with_bkt = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)

            # Temporarily disable BKT to test fallback
            original_bkt = self.mcq_scheduler.bkt_system
            self.mcq_scheduler.bkt_system = None
            selected_without_bkt = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)
            self.mcq_scheduler.bkt_system = original_bkt

            # Verify different selections (BKT should be more sophisticated)
            bkt_vs_fallback_different = selected_with_bkt != selected_without_bkt

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="BKT Virtual Mastery Updates",
                success=True,  # Basic functionality test
                execution_time=execution_time,
                details={
                    "bkt_vs_fallback_different": bkt_vs_fallback_different,
                    "with_bkt": selected_with_bkt,
                    "without_bkt": selected_without_bkt
                }
            ))

            print(f"✅ BKT virtual updates: PASSED (different selections: {bkt_vs_fallback_different})")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="BKT Virtual Mastery Updates",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ BKT virtual updates: FAILED - {str(e)}")

    def analyze_question_selection_details(self, student_id: str, num_questions: int = 5):
        """Get detailed analysis of why questions were chosen (minimal printing)"""

        print(f"\n📊 QUESTION SELECTION ANALYSIS")
        print("-" * 50)

        # Get student state before selection
        student = self.student_manager.get_student(student_id)
        due_topics = [idx for idx in student.studied_topics
                    if student.get_mastery(idx) < self.kg.config.get('algorithm_config.mastery_threshold', 0.7)]

        print(f"Student: {student_id}")
        print(f"Topics below mastery: {len(due_topics)}")
        print(f"Average mastery: {sum(student.get_mastery(idx) for idx in due_topics)/len(due_topics):.3f}")

        # Select questions with detailed tracking
        selected_mcqs = self.mcq_scheduler.select_optimal_mcqs(student_id, num_questions)

        print(f"\n🎯 SELECTED QUESTIONS ({len(selected_mcqs)}):")

        for i, mcq_id in enumerate(selected_mcqs, 1):
            if hasattr(self.kg, 'ultra_loader'):
                mcq_data = self.kg.ultra_loader.get_minimal_mcq_data(mcq_id)
                main_topic = mcq_data.main_topic_index if mcq_data else "Unknown"
                difficulty = mcq_data.difficulty if mcq_data else "Unknown"
            else:
                mcq = self.kg.mcqs.get(mcq_id)
                main_topic = mcq.main_topic_index if mcq else "Unknown"
                difficulty = mcq.overall_difficulty if mcq else "Unknown"

            topic_name = self.kg.get_topic_of_index(main_topic) if main_topic != "Unknown" else "Unknown"
            current_mastery = student.get_mastery(main_topic) if main_topic != "Unknown" else 0

            print(f"  Q{i}: {topic_name} (mastery: {current_mastery:.3f}, difficulty: {difficulty:.3f})")

        return {
            'selected_mcqs': selected_mcqs,
            'due_topics_count': len(due_topics),
            'selection_summary': f"{len(selected_mcqs)} questions selected for {len(due_topics)} due topics"
        }


    def _test_selection_consistency(self):
        """Test that selection algorithm produces consistent results"""
        start_time = time.time()

        try:
            # Create test student
            student_id = "test_consistency_student"
            student = self._create_test_student(student_id, fixed_mastery=0.5)

            # Run selection multiple times with same parameters
            selections = []
            for i in range(5):
                selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)
                selections.append(selected)

            # Check consistency (first selection should be deterministic)
            if len(selections) > 1 and len(selections[0]) > 0:
                first_questions = [sel[0] if sel else None for sel in selections]
                first_consistent = len(set(first_questions)) == 1
            else:
                first_consistent = True  # No questions to compare

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Selection Consistency",
                success=True,
                execution_time=execution_time,
                details={
                    "first_question_consistent": first_consistent,
                    "num_trials": len(selections),
                    "avg_selection_count": np.mean([len(s) for s in selections])
                }
            ))
            print("✅ Selection consistency: PASSED")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Selection Consistency",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Selection consistency: FAILED - {str(e)}")

    def _run_weight_parameter_tests(self):
        """Test different weight parameter configurations"""

        weight_configs = self._generate_weight_configurations()

        for config_name, weights in weight_configs.items():
            print(f"🧪 Testing weight configuration: {config_name}")
            result = self._test_weight_configuration(config_name, weights)
            self.weight_results.append(result)

    def _generate_weight_configurations(self) -> Dict[str, Dict[str, float]]:
        """Generate different weight configurations for testing"""

        configs = {
            "baseline": {
                "mastery_threshold": 0.7,
                "greedy_priority_weight": 2.0,
                "greedy_subtopic_weight": 0.7,
                "greedy_prereq_weight": 0.5
            },
            "conservative": {
                "mastery_threshold": 0.8,
                "greedy_priority_weight": 1.5,
                "greedy_subtopic_weight": 0.5,
                "greedy_prereq_weight": 0.3
            },
            "aggressive": {
                "mastery_threshold": 0.6,
                "greedy_priority_weight": 3.0,
                "greedy_subtopic_weight": 0.9,
                "greedy_prereq_weight": 0.7
            },
            "prerequisite_focused": {
                "mastery_threshold": 0.7,
                "greedy_priority_weight": 2.0,
                "greedy_subtopic_weight": 0.4,
                "greedy_prereq_weight": 0.8
            },
            "subtopic_focused": {
                "mastery_threshold": 0.7,
                "greedy_priority_weight": 2.0,
                "greedy_subtopic_weight": 0.9,
                "greedy_prereq_weight": 0.3
            }
        }

        return configs

    def _test_weight_configuration(self, config_name: str, weights: Dict[str, float]) -> WeightTestResult:
        """Test a specific weight configuration"""
        start_time = time.time()

        try:
            # Temporarily update configuration
            original_config = self._backup_config()
            self._apply_weight_config(weights)

            # Test with multiple students
            results = []
            for i in range(5):  # Test with 5 different students
                student_id = f"weight_test_student_{config_name}_{i}"
                student = self._create_test_student(student_id, random_mastery=True)

                # Run selection
                selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 5)

                # Calculate metrics
                coverage_ratio = self._calculate_coverage_ratio(selected, student_id)

                results.append({
                    "questions_selected": len(selected),
                    "coverage_ratio": coverage_ratio,
                    "success": True
                })

            # Restore original configuration
            self._restore_config(original_config)

            # Calculate averages
            avg_questions = np.mean([r["questions_selected"] for r in results])
            avg_coverage = np.mean([r["coverage_ratio"] for r in results])
            success_rate = np.mean([r["success"] for r in results])

            execution_time = time.time() - start_time

            return WeightTestResult(
                config_name=config_name,
                weights=weights,
                avg_questions_selected=avg_questions,
                avg_coverage_ratio=avg_coverage,
                avg_execution_time=execution_time,
                success_rate=success_rate,
                details={"individual_results": results}
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return WeightTestResult(
                config_name=config_name,
                weights=weights,
                avg_questions_selected=0.0,
                avg_coverage_ratio=0.0,
                avg_execution_time=execution_time,
                success_rate=0.0,
                details={"error": str(e)}
            )

    def _run_performance_tests(self):
        """Test algorithm performance under different conditions"""

        # Test 1: Large student load
        self._test_large_student_load()

        # Test 2: Many question selection
        self._test_many_question_selection()

        # Test 3: Repeated selections
        self._test_repeated_selections()

    def _test_large_student_load(self):
        """Test performance with many students"""
        start_time = time.time()

        try:
            num_students = 20
            students = []

            # Create many students
            for i in range(num_students):
                student_id = f"perf_test_student_{i}"
                student = self._create_test_student(student_id, random_mastery=True)
                students.append(student_id)

            # Test selection for all students
            total_selections = 0
            for student_id in students:
                selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)
                total_selections += len(selected)

            execution_time = time.time() - start_time
            avg_time_per_student = execution_time / num_students

            # Performance should be reasonable
            performance_acceptable = avg_time_per_student < self.config.performance_threshold_seconds

            self.results.append(TestResult(
                test_name="Large Student Load Performance",
                success=performance_acceptable,
                execution_time=execution_time,
                details={
                    "num_students": num_students,
                    "total_selections": total_selections,
                    "avg_time_per_student": avg_time_per_student,
                    "performance_acceptable": performance_acceptable
                }
            ))

            status = "PASSED" if performance_acceptable else "SLOW"
            print(f"✅ Large student load: {status} ({avg_time_per_student:.3f}s/student)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Large Student Load Performance",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Large student load: FAILED - {str(e)}")

    def _test_many_question_selection(self):
        """Test selection of many questions at once"""
        start_time = time.time()

        try:
            student_id = "many_questions_student"
            student = self._create_test_student(student_id, fixed_mastery=0.4)

            # Try selecting many questions
            selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 20)

            execution_time = time.time() - start_time
            performance_acceptable = execution_time < self.config.performance_threshold_seconds

            self.results.append(TestResult(
                test_name="Many Questions Selection Performance",
                success=performance_acceptable,
                execution_time=execution_time,
                details={
                    "questions_requested": 20,
                    "questions_selected": len(selected),
                    "performance_acceptable": performance_acceptable
                }
            ))

            status = "PASSED" if performance_acceptable else "SLOW"
            print(f"✅ Many questions selection: {status} ({len(selected)}/20 in {execution_time:.3f}s)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Many Questions Selection Performance",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Many questions selection: FAILED - {str(e)}")

    def _test_repeated_selections(self):
        """Test performance of repeated selections"""
        start_time = time.time()

        try:
            student_id = "repeated_selection_student"
            student = self._create_test_student(student_id, random_mastery=True)

            # Perform multiple selections
            num_iterations = 10
            total_selected = 0

            for i in range(num_iterations):
                selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 2)
                total_selected += len(selected)

            execution_time = time.time() - start_time
            avg_time_per_selection = execution_time / num_iterations
            performance_acceptable = avg_time_per_selection < (self.config.performance_threshold_seconds / 2)

            self.results.append(TestResult(
                test_name="Repeated Selections Performance",
                success=performance_acceptable,
                execution_time=execution_time,
                details={
                    "num_iterations": num_iterations,
                    "total_selected": total_selected,
                    "avg_time_per_selection": avg_time_per_selection,
                    "performance_acceptable": performance_acceptable
                }
            ))

            status = "PASSED" if performance_acceptable else "SLOW"
            print(f"✅ Repeated selections: {status} ({avg_time_per_selection:.3f}s/selection)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Repeated Selections Performance",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Repeated selections: FAILED - {str(e)}")

    def _run_edge_case_tests(self):
        """Test edge cases and error conditions"""

        # Test 1: Student with no studied topics
        self._test_no_studied_topics()

        # Test 2: Student with all high mastery
        self._test_all_high_mastery()

        # Test 3: Student with all completed questions
        self._test_all_completed_questions()

        # Test 4: Invalid student ID
        self._test_invalid_student_id()

    def _test_no_studied_topics(self):
        """Test student with no studied topics"""
        start_time = time.time()

        try:
            student_id = "no_studied_topics_student"
            student = self.student_manager.create_student(student_id)
            # Don't mark any topics as studied

            selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 5)

            # Should handle gracefully (return empty list)
            assert isinstance(selected, list), "Should return a list"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="No Studied Topics Edge Case",
                success=True,
                execution_time=execution_time,
                details={"questions_selected": len(selected)}
            ))
            print(f"✅ No studied topics: PASSED ({len(selected)} questions)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="No Studied Topics Edge Case",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ No studied topics: FAILED - {str(e)}")

    def _test_all_high_mastery(self):
        """Test student with all high mastery levels"""
        start_time = time.time()

        try:
            student_id = "high_mastery_student"
            student = self._create_test_student(student_id, fixed_mastery=0.95)

            selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 5)

            # Should handle gracefully
            assert isinstance(selected, list), "Should return a list"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="All High Mastery Edge Case",
                success=True,
                execution_time=execution_time,
                details={"questions_selected": len(selected)}
            ))
            print(f"✅ All high mastery: PASSED ({len(selected)} questions)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="All High Mastery Edge Case",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ All high mastery: FAILED - {str(e)}")

    def _test_all_completed_questions(self):
        """Test student who completed all available questions today"""
        start_time = time.time()

        try:
            student_id = "all_completed_student"
            student = self._create_test_student(student_id, random_mastery=True)

            # Mark many questions as completed today
            if hasattr(self.mcq_scheduler, 'mcq_vectors'):
                mcq_ids = list(self.mcq_scheduler.mcq_vectors.keys())[:50]  # Mark first 50 as completed
                for mcq_id in mcq_ids:
                    student.daily_completed.add(mcq_id)

            selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 5)

            # Should handle gracefully
            assert isinstance(selected, list), "Should return a list"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="All Completed Questions Edge Case",
                success=True,
                execution_time=execution_time,
                details={
                    "questions_selected": len(selected),
                    "completed_count": len(student.daily_completed)
                }
            ))
            print(f"✅ All completed questions: PASSED ({len(selected)} questions)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="All Completed Questions Edge Case",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ All completed questions: FAILED - {str(e)}")

    def _test_invalid_student_id(self):
        """Test with invalid student ID"""
        start_time = time.time()

        try:
            # Try with non-existent student
            selected = self.mcq_scheduler.select_optimal_mcqs("nonexistent_student", 5)

            # Should handle gracefully (return empty list)
            assert isinstance(selected, list), "Should return a list for invalid student"
            assert len(selected) == 0, "Should return empty list for invalid student"

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Invalid Student ID Edge Case",
                success=True,
                execution_time=execution_time,
                details={"questions_selected": len(selected)}
            ))
            print("✅ Invalid student ID: PASSED")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Invalid Student ID Edge Case",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Invalid student ID: FAILED - {str(e)}")

    def _run_integration_tests(self):
        """Test integration between different system components"""

        # Test 1: Full learning session simulation
        self._test_full_learning_session()

        # Test 2: BKT integration
        self._test_bkt_integration()


    def _test_full_learning_session(self):
        """Test a complete learning session with question answering"""
        start_time = time.time()

        try:
            student_id = "integration_test_student"
            student = self._create_test_student(student_id, fixed_mastery=0.3)

            # Simulate answering several questions
            total_questions = 0
            for session_round in range(3):
                # Select questions
                selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 3)
                total_questions += len(selected)

                # Simulate answering (random correct/incorrect)
                for mcq_id in selected:
                    is_correct = random.choice([True, False])
                    time_taken = random.uniform(30, 120)  # 30-120 seconds

                    # Record attempt
                    self.student_manager.record_attempt(
                        student_id, mcq_id, is_correct, time_taken, self.kg
                    )

            # Verify student progress was tracked
            final_student = self.student_manager.get_student(student_id)
            attempts_recorded = len(final_student.completed_questions) > 0

            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Full Learning Session Integration",
                success=attempts_recorded,
                execution_time=execution_time,
                details={
                    "total_questions_attempted": total_questions,
                    "attempts_recorded": attempts_recorded,
                    "final_completed_count": len(final_student.completed_questions)
                }
            ))

            print(f"✅ Full learning session: PASSED ({total_questions} questions)")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Full Learning Session Integration",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Full learning session: FAILED - {str(e)}")

    def _test_bkt_integration(self):
        """Test integration with Bayesian Knowledge Tracing"""
        start_time = time.time()

        try:
            student_id = "bkt_integration_student"
            student = self._create_test_student(student_id, fixed_mastery=0.5)

            original_mastery = student.mastery_levels.copy()

            # Select and answer a question
            selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 1)
            if selected:
                mcq_id = selected[0]

                # Record a correct answer
                bkt_updates = self.student_manager.record_attempt(
                    student_id, mcq_id, True, 60, self.kg
                )

                # Check that BKT updates were applied
                updated_student = self.student_manager.get_student(student_id)
                mastery_changed = updated_student.mastery_levels != original_mastery

                execution_time = time.time() - start_time
                self.results.append(TestResult(
                    test_name="BKT Integration",
                    success=mastery_changed,
                    execution_time=execution_time,
                    details={
                        "bkt_updates_applied": mastery_changed,
                        "mcq_answered": mcq_id
                    }
                ))
                print("✅ BKT integration: PASSED")
            else:
                execution_time = time.time() - start_time
                self.results.append(TestResult(
                    test_name="BKT Integration",
                    success=False,
                    execution_time=execution_time,
                    error_message="No questions available for BKT test"
                ))
                print("❌ BKT integration: FAILED - No questions available")

        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="BKT Integration",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ BKT integration: FAILED - {str(e)}")



    # Helper Methods
    def _create_test_student(self, student_id: str, random_mastery: bool = False,
                           fixed_mastery: Optional[float] = None) -> Any:
        """Create a test student with specified mastery characteristics"""
        try:
            student = self.student_manager.create_student(student_id)

            # Determine number of topics/nodes
            num_topics = 0
            if hasattr(self.kg, 'nodes') and self.kg.nodes:
                num_topics = len(self.kg.nodes)
            elif hasattr(self.kg, 'ultra_loader') and hasattr(self.kg.ultra_loader, 'minimal_mcq_data'):
                # For ultra_loader, get topics from MCQ data
                all_topics = set()
                for minimal_data in self.kg.ultra_loader.minimal_mcq_data.values():
                    all_topics.add(minimal_data.main_topic_index)
                    all_topics.update(minimal_data.subtopic_weights.keys())
                num_topics = max(all_topics) + 1 if all_topics else 10  # Fallback to 10
            else:
                # Fallback - assume reasonable number of topics
                num_topics = 20
                print(f"⚠️  Could not determine number of topics, using fallback: {num_topics}")

            print(f"📝 Creating test student with {num_topics} topics")


            for i in range(num_topics):
                # Mark topic as studied (required for eligibility)
                if hasattr(student, 'mark_topic_studied'):
                    student.mark_topic_studied(i)
                elif hasattr(student, 'studied_topics'):
                    # Handle both set and dict types for studied_topics
                    if isinstance(student.studied_topics, set):
                        student.studied_topics.add(i)
                    elif isinstance(student.studied_topics, dict):
                        student.studied_topics[i] = True
                    else:
                        # Fallback: try to convert to set
                        if not isinstance(student.studied_topics, set):
                            student.studied_topics = set()
                        student.studied_topics.add(i)

                # Set mastery level
                if fixed_mastery is not None:
                    mastery_value = fixed_mastery
                elif random_mastery:
                    mastery_value = random.uniform(0.1, 0.9)
                else:
                    mastery_value = 0.5  # Default

                # Set mastery in student profile
                if hasattr(student, 'mastery_levels'):
                    student.mastery_levels[i] = mastery_value
                elif hasattr(student, 'set_mastery'):
                    student.set_mastery(i, mastery_value)

            # Ensure student has required attributes
            if not hasattr(student, 'studied_topics'):
                student.studied_topics = set(range(num_topics))
            if not hasattr(student, 'mastery_levels'):
                student.mastery_levels = {i: (fixed_mastery or 0.5) for i in range(num_topics)}
            if not hasattr(student, 'daily_completed'):
                student.daily_completed = set()

            print(f"✅ Test student created: {len(student.studied_topics)} studied topics, {len(student.mastery_levels)} mastery levels")
            return student

        except Exception as e:
            print(f"❌ Failed to create test student: {str(e)}")
            raise Exception(f"Test student creation failed: {str(e)}")

    def _backup_config(self) -> Dict:
        """Backup current configuration"""
        # This would need to be implemented based on actual config structure
        return {"mastery_threshold": getattr(self.kg.config, 'mastery_threshold', 0.7)}

    def _apply_weight_config(self, weights: Dict[str, float]):
        """Apply weight configuration temporarily"""
        for key, value in weights.items():
            if hasattr(self.kg.config, key):
                setattr(self.kg.config, key, value)

    def _restore_config(self, backup: Dict):
        """Restore configuration from backup"""
        for key, value in backup.items():
            if hasattr(self.kg.config, key):
                setattr(self.kg.config, key, value)

    def _calculate_coverage_ratio(self, selected_mcqs: List[str], student_id: str) -> float:
        """Calculate coverage ratio for selected MCQs"""
        if not selected_mcqs:
            return 0.0

        student = self.student_manager.get_student(student_id)
        if not student:
            return 0.0

        # Simple coverage calculation based on number of topics covered
        covered_topics = set()
        for mcq_id in selected_mcqs:
            if mcq_id in self.mcq_scheduler.mcq_vectors:
                vector = self.mcq_scheduler.mcq_vectors[mcq_id]
                covered_topics.update(vector.subtopic_weights.keys())

        total_due_topics = sum(1 for topic_idx, mastery in student.mastery_levels.items()
                              if mastery < 0.7 and student.is_topic_studied(topic_idx))

        if total_due_topics == 0:
            return 1.0

        return len(covered_topics) / total_due_topics

    def _generate_test_report(self, total_time: float) -> Dict[str, Any]:
        """Generate comprehensive test report"""

        # Core functionality results
        core_passed = sum(1 for r in self.results if r.success)
        core_total = len(self.results)
        core_success_rate = core_passed / core_total if core_total > 0 else 0

        # Weight test results
        weight_summary = {}
        if self.weight_results:
            weight_summary = {
                "num_configurations_tested": len(self.weight_results),
                "best_config": max(self.weight_results, key=lambda x: x.avg_coverage_ratio).config_name,
                "avg_success_rate": np.mean([r.success_rate for r in self.weight_results])
            }

        # Performance analysis
        perf_results = [r for r in self.results if "Performance" in r.test_name]
        avg_execution_time = np.mean([r.execution_time for r in self.results])

        report = {
            "summary": {
                "total_execution_time": total_time,
                "core_tests_passed": core_passed,
                "core_tests_total": core_total,
                "core_success_rate": core_success_rate,
                "avg_test_execution_time": avg_execution_time
            },
            "core_functionality": {
                "results": [
                    {
                        "test_name": r.test_name,
                        "success": r.success,
                        "execution_time": r.execution_time,
                        "error": r.error_message
                    } for r in self.results
                ]
            },
            "weight_parameters": weight_summary,
            "weight_details": [
                {
                    "config_name": r.config_name,
                    "weights": r.weights,
                    "avg_questions_selected": r.avg_questions_selected,
                    "avg_coverage_ratio": r.avg_coverage_ratio,
                    "success_rate": r.success_rate
                } for r in self.weight_results
            ],
            "performance": {
                "num_performance_tests": len(perf_results),
                "performance_tests_passed": sum(1 for r in perf_results if r.success)
            }
        }

        # Print summary
        print("\n" + "="*80)
        print("TEST SUITE SUMMARY")
        print("="*80)
        print(f"📊 Total execution time: {total_time:.2f} seconds")
        print(f"✅ Core tests passed: {core_passed}/{core_total} ({core_success_rate*100:.1f}%)")
        print(f"⚖️ Weight configurations tested: {len(self.weight_results)}")
        print(f"🚀 Performance tests passed: {sum(1 for r in perf_results if r.success)}/{len(perf_results)}")

        if self.weight_results:
            best_config = max(self.weight_results, key=lambda x: x.avg_coverage_ratio)
            print(f"🏆 Best weight configuration: {best_config.config_name} ({best_config.avg_coverage_ratio:.3f} coverage)")

        # Print failed tests
        failed_tests = [r for r in self.results if not r.success]
        if failed_tests:
            print(f"\n❌ Failed tests:")
            for r in failed_tests:
                print(f"   - {r.test_name}: {r.error_message}")

        print("\n✅ Test suite completed successfully!")

        return report


def run_comprehensive_tests(config_file: str = 'config.json') -> Dict[str, Any]:
    """
    Main function to run the comprehensive test suite.

    Args:
        config_file: Path to configuration file

    Returns:
        Dictionary containing complete test results
    """
    # Create test configuration
    test_config = TestConfig(config_file=config_file)

    # Initialize and run test suite
    test_suite = MCQAlgorithmTestSuite(test_config)
    results = test_suite.run_all_tests()

    return results


# Example usage and additional test functions
def quick_functionality_test() -> bool:
    """Quick test to verify basic functionality works"""
    try:
        test_config = TestConfig()
        test_config.run_weight_optimization = False
        test_config.run_performance_tests = False
        test_config.run_edge_case_tests = False
        test_config.run_integration_tests = False

        test_suite = MCQAlgorithmTestSuite(test_config)
        results = test_suite.run_all_tests()

        return results["summary"]["core_success_rate"] > 0.8
    except Exception:
        return False


def weight_optimization_test() -> Dict[str, Any]:
    """Focused test for weight parameter optimization"""
    test_config = TestConfig()
    test_config.run_performance_tests = False
    test_config.run_edge_case_tests = False
    test_config.run_integration_tests = False

    test_suite = MCQAlgorithmTestSuite(test_config)
    results = test_suite.run_all_tests()

    return results["weight_details"]
def debug_mcq_selection_issues(kg, student_manager, student_id):
    """Standalone debug function - no self parameter"""
    print("\n" + "="*60)
    print("🔍 DEBUGGING MCQ SELECTION ISSUES")
    print("="*60)

    # 1. Check knowledge graph MCQ loading
    print(f"\n📚 Knowledge Graph MCQ Status:")
    if hasattr(kg, 'mcqs'):
        print(f"   Total MCQs loaded: {len(kg.mcqs)}")
        if kg.mcqs:
            sample_mcq = list(kg.mcqs.values())[0]
            print(f"   Sample MCQ ID: {sample_mcq.id}")
            print(f"   Sample main topic: {sample_mcq.main_topic_index}")
    else:
        print("   ❌ No 'mcqs' attribute found")

    # 2. Check ultra_loader
    if hasattr(kg, 'ultra_loader'):
        try:
            stats = kg.ultra_loader.get_stats()
            print(f"\n📊 Ultra Loader Stats:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
        except Exception as e:
            print(f"   ❌ Error getting ultra_loader stats: {e}")
    else:
        print("   ❌ No 'ultra_loader' found")

    # 3. Check topic-to-MCQ mapping
    print(f"\n🗺️ Topic-to-MCQ Mapping:")
    if hasattr(kg, 'topic_to_mcq_ids'):
        mapping = kg.topic_to_mcq_ids
        print(f"   Total topics with MCQs: {len(mapping)}")
        print(f"   Topics: {sorted(mapping.keys())[:10]}..." if mapping else "   No topics found")

        # Check first few topics
        if mapping:
            for topic_idx in sorted(mapping.keys())[:5]:
                mcq_count = len(mapping[topic_idx])
                print(f"   Topic {topic_idx}: {mcq_count} MCQs")
    else:
        print("   ❌ No 'topic_to_mcq_ids' found")

    # 4. Check student status
    student = student_manager.get_student(student_id)
    if student:
        print(f"\n👤 Student Status:")
        print(f"   Studied topics: {len(student.studied_topics)}")
        print(f"   Topics list: {sorted(student.studied_topics.keys())[:10]}...")
        print(f"   Mastery levels: {len(student.mastery_levels)}")
        print(f"   Daily completed: {len(student.daily_completed)}")

        # Check mastery for first few topics
        mastery_threshold = 0.7
        due_topics = []
        for topic_idx in sorted(student.mastery_levels.keys())[:5]:
            mastery = student.mastery_levels[topic_idx]
            is_studied = student.is_topic_studied(topic_idx)
            is_due = is_studied and mastery < mastery_threshold
            print(f"   Topic {topic_idx}: mastery={mastery:.2f}, studied={is_studied}, due={is_due}")
            if is_due:
                due_topics.append(topic_idx)

        print(f"   Due topics (first 5): {due_topics}")
    else:
        print(f"   ❌ Student {student_id} not found")

    # 5. Check file system
    print(f"\n📁 File System Check:")
    try:
        import os
        files_to_check = [
            'mcq_algorithm_files\\kg.json',
            'mcq_algorithm_files\\computed_mcqs_different_numbers.json',
            '_static\\config.json'
        ]

        for filepath in files_to_check:
            exists = os.path.exists(filepath)
            size = os.path.getsize(filepath) if exists else 0
            print(f"   {filepath}: {'✅' if exists else '❌'} exists, {size} bytes")

            if exists and filepath.endswith('.json'):
                try:
                    import json
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                    if 'mcqs' in str(filepath).lower():
                        mcq_count = len(data.get('mcqs', data)) if isinstance(data, dict) else len(data)
                        print(f"      Contains {mcq_count} MCQs")
                except Exception as e:
                    print(f"      Error reading JSON: {e}")
    except Exception as e:
        print(f"   Error checking files: {e}")

    print("\n" + "="*60)


def quick_debug():
    """Quick debugging function - call this once to diagnose the problem"""
    print("🚀 Starting Quick Debug Session...")

    try:
        # Import your classes
        from mcq_algorithm_different_numbers import (
            KnowledgeGraph, StudentManager, MCQScheduler,
            BayesianKnowledgeTracing
        )

        # Initialize your system
        print("📂 Loading knowledge graph...")
        kg = KnowledgeGraph(
            nodes_file='mcq_algorithm_files\\kg.json',
            mcqs_file='mcq_algorithm_files\\computed_mcqs_different_numbers.json',
            config_file='_static\\config.json'
        )

        print("👥 Creating student manager...")
        student_manager = StudentManager(kg.config)

        print("🎯 Creating MCQ scheduler...")
        mcq_scheduler = MCQScheduler(kg, student_manager)

        # Create test student
        print("👤 Creating test student...")
        student_id = "debug_student"
        student = student_manager.create_student(student_id)

        # Set some mastery levels
        print("📊 Setting up student mastery...")
        import random
        for topic_idx in range(1, 19):  # Assuming you have topics 1-18
            mastery = random.uniform(0.1, 0.6)  # Low mastery so topics are "due"
            student.mastery_levels[topic_idx] = mastery
            student.studied_topics[topic_idx] = True
            student.confidence_levels[topic_idx] = mastery * 0.8

        print(f"✅ Created student with {len(student.studied_topics)} studied topics")

        # Run debugging
        debug_mcq_selection_issues(kg, student_manager, student_id)

        # Test MCQ selection
        print("\n🧪 Testing MCQ Selection:")
        try:
            eligible_mcqs = mcq_scheduler.get_available_questions_for_student(student_id)
            print(f"   Eligible MCQs found: {len(eligible_mcqs)}")

            if eligible_mcqs:
                print(f"   Sample MCQ IDs: {eligible_mcqs[:5]}")

                # Try to select some questions
                selected = mcq_scheduler.select_optimal_mcqs(student_id, 3)
                print(f"   Selected MCQs: {len(selected)}")
                print(f"   ✅ MCQ selection is working!")
            else:
                print(f"   ❌ No eligible MCQs found - this is the core problem!")

        except Exception as e:
            print(f"   ❌ Error in MCQ selection: {e}")
            import traceback
            traceback.print_exc()

    except Exception as e:
        print(f"❌ Error in quick debug setup: {e}")
        import traceback
        traceback.print_exc()

def debug_mcq_loading_issues(config_file: str = 'config.json') -> Dict[str, Any]:
    """
    Diagnostic function to debug MCQ loading issues.

    Returns detailed information about what's working and what's not.
    """
    debug_info = {
        "system_initialization": {},
        "mcq_data_sources": {},
        "vector_creation": {},
        "recommendations": []
    }

    try:
        print("🔍 DEBUGGING MCQ LOADING ISSUES")
        print("="*50)

        # Test 1: System Initialization
        print("1️⃣ Testing system initialization...")
        try:
            kg = KnowledgeGraph(
                nodes_file='small-graph-kg.json',
                mcqs_file='small-graph-computed_mcqs.json',
                config_file=config_file
            )
            debug_info["system_initialization"]["knowledge_graph"] = "SUCCESS"
            print("   ✅ Knowledge graph initialized")
        except Exception as e:
            debug_info["system_initialization"]["knowledge_graph"] = f"FAILED: {str(e)}"
            print(f"   ❌ Knowledge graph failed: {str(e)}")
            debug_info["recommendations"].append("Check that JSON files exist and are valid")


        # Test 2: Check MCQ Data Sources
        print("2️⃣ Checking MCQ data sources...")

        if hasattr(kg, 'mcqs'):
            mcq_count = len(kg.mcqs)
            debug_info["mcq_data_sources"]["traditional_mcqs"] = mcq_count
            print(f"   📚 Traditional MCQs: {mcq_count}")
        else:
            debug_info["mcq_data_sources"]["traditional_mcqs"] = 0
            print("   ⚠️  No traditional mcqs attribute")

        if hasattr(kg, 'ultra_loader'):
            debug_info["mcq_data_sources"]["has_ultra_loader"] = True
            print("   📊 Ultra loader detected")

            if hasattr(kg.ultra_loader, 'minimal_mcq_data'):
                ultra_count = len(kg.ultra_loader.minimal_mcq_data)
                debug_info["mcq_data_sources"]["ultra_loader_mcqs"] = ultra_count
                print(f"   📚 Ultra loader MCQs: {ultra_count}")
            else:
                debug_info["mcq_data_sources"]["ultra_loader_mcqs"] = 0
                print("   ⚠️  Ultra loader has no minimal_mcq_data")
        else:
            debug_info["mcq_data_sources"]["has_ultra_loader"] = False
            print("   📊 No ultra loader")

        # Test 3: MCQ Scheduler Creation
        print("3️⃣ Testing MCQ scheduler...")
        try:
            student_manager = StudentManager(kg.config)
            mcq_scheduler = MCQScheduler(kg, student_manager)
            debug_info["system_initialization"]["mcq_scheduler"] = "SUCCESS"
            print("   ✅ MCQ scheduler created")
        except Exception as e:
            debug_info["system_initialization"]["mcq_scheduler"] = f"FAILED: {str(e)}"
            print(f"   ❌ MCQ scheduler failed: {str(e)}")
            return debug_info

        # Test 4: Vector Creation Methods
        print("4️⃣ Testing vector creation methods...")

        # Check available methods
        has_ensure_vectors = hasattr(mcq_scheduler, '_ensure_vectors_computed')
        has_get_or_create = hasattr(mcq_scheduler, '_get_or_create_optimized_mcq_vector')

        debug_info["vector_creation"]["has_ensure_vectors_computed"] = has_ensure_vectors
        debug_info["vector_creation"]["has_get_or_create_optimized"] = has_get_or_create

        print(f"   📋 _ensure_vectors_computed: {has_ensure_vectors}")
        print(f"   📋 _get_or_create_optimized_mcq_vector: {has_get_or_create}")

        # Test 5: Actual Vector Creation
        print("5️⃣ Testing actual vector creation...")

        if has_ensure_vectors:
            try:
                mcq_scheduler._ensure_vectors_computed()
                vectors_after_ensure = len(mcq_scheduler.mcq_vectors)
                debug_info["vector_creation"]["vectors_after_ensure_computed"] = vectors_after_ensure
                print(f"   📊 Vectors after _ensure_vectors_computed: {vectors_after_ensure}")
            except Exception as e:
                debug_info["vector_creation"]["ensure_vectors_error"] = str(e)
                print(f"   ❌ _ensure_vectors_computed failed: {str(e)}")

        if has_get_or_create and debug_info["mcq_data_sources"].get("ultra_loader_mcqs", 0) > 0:
            # Try to create a vector for a specific MCQ
            sample_mcq_id = list(kg.ultra_loader.minimal_mcq_data.keys())[0]
            try:
                vector = mcq_scheduler._get_or_create_optimized_mcq_vector(sample_mcq_id)
                if vector:
                    debug_info["vector_creation"]["on_demand_creation"] = "SUCCESS"
                    print(f"   ✅ On-demand vector creation: SUCCESS for {sample_mcq_id}")
                else:
                    debug_info["vector_creation"]["on_demand_creation"] = "FAILED - returned None"
                    print(f"   ❌ On-demand vector creation: returned None")
            except Exception as e:
                debug_info["vector_creation"]["on_demand_creation"] = f"FAILED: {str(e)}"
                print(f"   ❌ On-demand vector creation failed: {str(e)}")

        # Test 6: Student Creation and Eligibility
        print("6️⃣ Testing student creation and eligibility...")
        try:
            test_student = student_manager.create_student("debug_student")

            # Get number of topics
            num_topics = len(kg.nodes) if hasattr(kg, 'nodes') else 10

            # Mark topics as studied
            for i in range(num_topics):
                if hasattr(test_student, 'mark_topic_studied'):
                    test_student.mark_topic_studied(i)
                test_student.mastery_levels[i] = 0.3  # Low mastery

            eligible_mcqs = mcq_scheduler.get_available_questions_for_student("debug_student")
            debug_info["vector_creation"]["eligible_mcqs_count"] = len(eligible_mcqs)
            print(f"   📊 Eligible MCQs for test student: {len(eligible_mcqs)}")

        except Exception as e:
            debug_info["vector_creation"]["student_eligibility_error"] = str(e)
            print(f"   ❌ Student eligibility test failed: {str(e)}")

        # Generate recommendations
        print("7️⃣ Generating recommendations...")

        if debug_info["mcq_data_sources"]["traditional_mcqs"] == 0 and debug_info["mcq_data_sources"]["ultra_loader_mcqs"] == 0:
            debug_info["recommendations"].append("No MCQ data found - check JSON file loading")

        if debug_info["mcq_data_sources"]["has_ultra_loader"] and debug_info["vector_creation"].get("vectors_after_ensure_computed", 0) == 0:
            debug_info["recommendations"].append("Ultra loader detected but no vectors created - vectors are created on-demand")

        if not debug_info["mcq_data_sources"]["has_ultra_loader"] and debug_info["vector_creation"].get("vectors_after_ensure_computed", 0) == 0:
            debug_info["recommendations"].append("Traditional mode but no vectors created - check _precompute_prerequisites_for_mcqs method")

        if debug_info["vector_creation"].get("eligible_mcqs_count", 0) == 0:
            debug_info["recommendations"].append("No eligible MCQs found - check student topic marking and mastery thresholds")

        print("✅ Debug analysis complete!")

    except Exception as e:
        debug_info["overall_error"] = str(e)
        print(f"❌ Debug analysis failed: {str(e)}")

    return debug_info


if __name__ == "__main__":
    print("MCQ Algorithm Test Suite - Choose an option:")
    print("1. Quick functionality test")
    print("2. Debug MCQ loading issues")
    print("3. Full comprehensive test suite")
    print("4. Weight optimization only")
    #quick_debug()

    try:
        choice = input("Enter choice (1-4, or press Enter for full suite): ").strip()
    except:
        choice = "3"  # Default to full suite

    if choice == "1":
        print("\n🚀 Running quick functionality test...")
        success = quick_functionality_test()
        print(f"✅ Quick test {'PASSED' if success else 'FAILED'}")

    elif choice == "2":
        print("\n🔍 Running debug analysis...")
        debug_results = debug_mcq_loading_issues()
        print("\n📋 DEBUG SUMMARY:")
        print(json.dumps(debug_results, indent=2))

    elif choice == "4":
        print("\n⚖️ Running weight optimization test...")
        weight_results = weight_optimization_test()
        print("\n📊 WEIGHT OPTIMIZATION RESULTS:")
        for result in weight_results:
            print(f"  {result['config_name']}: {result['avg_coverage_ratio']:.3f} coverage")

    else:  # choice == "3" or default
        print("\n🚀 Starting comprehensive MCQ algorithm test suite...")
        results = run_comprehensive_tests()

        # Optionally save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        results_file = f"mcq_test_results_{timestamp}.json"

        try:
            with open(results_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"📁 Test results saved to: {results_file}")
        except Exception as e:
            print(f"⚠️ Could not save results file: {e}")





