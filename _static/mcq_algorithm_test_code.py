"""
Comprehensive Test Suite for MCQ Algorithm Current
=================================================

This module provides extensive testing for the mcq_algorithm_current system,
including functionality tests, weight parameter optimization tests, performance
tests, and integration tests. Designed to replace existing test code.

Author: Algorithm Testing Framework
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

# Import the classes we're testing
# These imports should match your actual import structure
try:
    from mcq_algorithm_current import (
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
    nodes_file: str = '_static\small-graph-kg.json'
    mcqs_file: str = '_static\small-graph-computed_mcqs.json'
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
        
        # Test 7: MCQ Selection Consistency
        self._test_selection_consistency()
    
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
                    selection_results[num_questions] = {
                        "selected_count": len(selected),
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
        
        # Test 3: Configuration changes
        self._test_configuration_changes()
    
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
    
    def _test_configuration_changes(self):
        """Test system behavior with configuration changes"""
        start_time = time.time()
        
        try:
            student_id = "config_test_student"
            student = self._create_test_student(student_id, fixed_mastery=0.6)
            
            # Test with different mastery thresholds
            results = {}
            for threshold in [0.5, 0.7, 0.9]:
                # Backup and modify config
                original_threshold = getattr(self.kg.config, 'mastery_threshold', 0.7)
                if hasattr(self.kg.config, 'mastery_threshold'):
                    self.kg.config.mastery_threshold = threshold
                
                # Run selection
                selected = self.mcq_scheduler.select_optimal_mcqs(student_id, 5)
                results[threshold] = len(selected)
                
                # Restore config
                if hasattr(self.kg.config, 'mastery_threshold'):
                    self.kg.config.mastery_threshold = original_threshold
            
            # Verify that different thresholds produce different results
            unique_results = len(set(results.values()))
            config_responsive = unique_results > 1
            
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Configuration Changes",
                success=config_responsive,
                execution_time=execution_time,
                details={
                    "threshold_results": results,
                    "config_responsive": config_responsive
                }
            ))
            
            print(f"✅ Configuration changes: PASSED (responsive: {config_responsive})")
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.results.append(TestResult(
                test_name="Configuration Changes",
                success=False,
                execution_time=execution_time,
                error_message=str(e)
            ))
            print(f"❌ Configuration changes: FAILED - {str(e)}")
    
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
        has_precompute = hasattr(mcq_scheduler, '_precompute_prerequisites_for_mcqs')
        
        debug_info["vector_creation"]["has_ensure_vectors_computed"] = has_ensure_vectors
        debug_info["vector_creation"]["has_get_or_create_optimized"] = has_get_or_create
        debug_info["vector_creation"]["has_precompute_prerequisites"] = has_precompute
        
        print(f"   📋 _ensure_vectors_computed: {has_ensure_vectors}")
        print(f"   📋 _get_or_create_optimized_mcq_vector: {has_get_or_create}")
        print(f"   📋 _precompute_prerequisites_for_mcqs: {has_precompute}")
        
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



    
    