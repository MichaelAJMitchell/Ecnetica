
"""
Complete BKT-FSRS System Integration Test

This test demonstrates the entire system working together:
1. Initialize knowledge graph and MCQ system
2. Create students with realistic data
3. Run BKT parameter optimization
4. Run FSRS parameter optimization (using official libraries)
5. Create integrated optimized configuration
6. Test the optimized system with new students
7. Compare performance vs baseline

"""

import sys
import os
from datetime import datetime
import json

sys.path.append('./')


def main():
    print(" COMPLETE BKT-FSRS SYSTEM INTEGRATION TEST")
    print("=" * 60)
    
    # Check if we can import all required modules
    missing_modules = check_dependencies()
    if missing_modules:
        print(" Missing required modules:")
        for module in missing_modules:
            print(f"   - {module}")
        print("\nInstall missing modules and try again.")
        return False
    
    try:
        # Step 1: Initialize Core System
        print("\n  1: Initializing Core System")
        print("-" * 40)
        kg, student_manager, mcq_scheduler, bkt_system = initialize_core_system()
        print("✅ Core system initialized successfully")
        
        # Step 2: Generate Test Data
        print("\n 2: Generating Test Data")
        print("-" * 40)
        training_students = generate_training_data(kg, student_manager, mcq_scheduler, bkt_system)
        print(f"✅ Generated training data for {len(training_students)} students")
        
        # Step 3: Run Integrated Optimization
        print("\n 3: Running Integrated Parameter Optimization")
        print("-" * 40)
        optimization_results = run_integrated_optimization(kg, student_manager)
        
        if not optimization_results.get('integration_config'):
            print(" Optimization failed - cannot continue")
            return False
        
        print("✅ Parameter optimization completed successfully")
        
        # Step 4: Create Optimized System
        print("\n STEP 4: Creating Optimized System")
        print("-" * 40)
        optimized_kg, optimized_student_manager, optimized_mcq_scheduler, optimized_bkt_system = create_optimized_system(optimization_results)
        print(" Optimized system created successfully")
        
        # Step 5: Test Performance Comparison
        print("\n 5: Performance Comparison Test")
        print("-" * 40)
        comparison_results = test_performance_comparison(
            (kg, student_manager, mcq_scheduler, bkt_system),
            (optimized_kg, optimized_student_manager, optimized_mcq_scheduler, optimized_bkt_system)
        )
        print(" Performance comparison completed")
        
        # Step 6: Display Results
        print("\n STEP 6: Test Results Summary")
        print("-" * 40)
        display_final_results(optimization_results, comparison_results)
        
        print("\n" + "=" * 60)
        print(" ALL TESTS PASSED")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n TEST FAILED: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_dependencies():
    """Check if all required modules are available"""
    missing = []
    
    # Core system modules
    try:
        from _static.mcq_algorithm_current import (
            KnowledgeGraph, StudentManager, BayesianKnowledgeTracing, MCQScheduler
        )
    except ImportError as e:
        missing.append(f"_static.mcq_algorithm_current.py - {e}")
    
    # BKT parameter optimization
    try:
        from BKT_Algorithm.Parameter_Assessment_Test import (
            create_realistic_student, simulate_learning_sessions, fit_bkt_parameters_sklearn
        )
    except ImportError as e:
        missing.append(f"Parameter_Assessment_Test.py - {e}")
    
    # FSRS optimization (try efficient version first)
    fsrs_available = False
    try:
        from BKT_Algorithm.FSRS_Parameter_Assessment import run_efficient_fsrs_optimization
        fsrs_available = True
    except ImportError:
        try:
            from BKT_Algorithm.FSRS_Parameter_Assessment import run_fsrs_optimization_pipeline
            fsrs_available = True
        except ImportError as e:
            missing.append(f"FSRS optimizer - {e}")
    
    # Integration system
    try:
        from BKT_Algorithm.Optimisation_System_Integration import (
            IntegratedParameterOptimizer, OptimizedSystemFactory
        )
    except ImportError as e:
        missing.append(f"BKT_Algorithm.Optimisation_System_Integration.py - {e}")
    
    # Required JSON files
    required_files = [
        '_static/small-graph-kg.json',
        '_static/small-graph-computed_mcqs.json', 
        '_static/config.json'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            missing.append(f"Required file: {file}")
    
    return missing

def initialize_core_system():
    """Initialize the core BKT-FSRS system"""
    from _static.mcq_algorithm_current import (
        KnowledgeGraph, StudentManager, BayesianKnowledgeTracing, MCQScheduler
    )
    
    # Initialize with default config
    kg = KnowledgeGraph(
        nodes_file='_static/small-graph-kg.json',
        mcqs_file='_static/small-graph-computed_mcqs.json',
        config_file='_static/config.json'
    )
    
    student_manager = StudentManager(kg.config)
    mcq_scheduler = MCQScheduler(kg, student_manager)
    bkt_system = BayesianKnowledgeTracing(kg, student_manager)
    
    # Connect systems
    mcq_scheduler.set_bkt_system(bkt_system)
    student_manager.set_bkt_system(bkt_system)
    
    print(f"   📚 Knowledge Graph: {len(kg.get_all_indexes())} topics")
    if hasattr(kg, 'ultra_loader'):
        print(f"   📝 MCQs: {len(kg.ultra_loader.minimal_mcq_data)} questions")
    print(f"   ⚙️ BKT System: {len(kg.config.get('bkt_parameters', {}).get('topic_specific', {}))} topic-specific parameters")
    
    return kg, student_manager, mcq_scheduler, bkt_system

def generate_training_data(kg, student_manager, mcq_scheduler, bkt_system, n_students=8):
    """Generate realistic training data for optimization"""
    from Parameter_Assessment_Test import create_realistic_student, simulate_learning_sessions
    
    training_students = []
    
    for i in range(n_students):
        student_id = f"training_student_{i:02d}"
        
        # Create student with realistic initial mastery
        create_realistic_student(student_manager, student_id, kg)
        
        # Generate varied learning sessions (different amounts per student)
        n_sessions = 10 + (i * 2)  # 10-24 sessions per student
        attempts = simulate_learning_sessions(
            kg, student_manager, mcq_scheduler, bkt_system,
            student_id, num_sessions=n_sessions
        )
        
        training_students.append(student_id)
        print(f"   👤 {student_id}: {len(attempts)} attempts across {n_sessions} sessions")
    
    # Display summary statistics
    total_attempts = sum(len(student.attempt_history) for student in student_manager.students.values())
    print(f"\n   📊 Training Data Summary:")
    print(f"      Students: {len(training_students)}")
    print(f"      Total attempts: {total_attempts}")
    print(f"      Avg attempts per student: {total_attempts / len(training_students):.1f}")
    
    return training_students

def run_integrated_optimization(kg, student_manager):
    """Run the complete integrated optimization pipeline"""
    from BKT_Algorithm.Optimisation_System_Integration import IntegratedParameterOptimizer
    
    optimizer = IntegratedParameterOptimizer(kg, student_manager)
    
    # Run complete optimization with reasonable settings for test
    results = optimizer.run_complete_optimization(
        min_attempts_per_topic=3,  # Lower threshold for test data
        train_test_split=0.8,
        save_results=True
    )
    
    # Display optimization summary
    bkt_count = len(results.get('bkt_optimization', {}))
    fsrs_success = False
    
    if 'fsrs_optimization' in results:
        fsrs_opt = results['fsrs_optimization']
        if isinstance(fsrs_opt, dict):
            fsrs_success = fsrs_opt.get('optimization', {}).get('success', False) or fsrs_opt.get('success', False)
    
    print(f"   📊 BKT Optimization: {bkt_count} topics fitted")
    print(f"   🧠 FSRS Optimization: {'✅ Success' if fsrs_success else '❌ Failed'}")
    
    if fsrs_success:
        if 'validation' in results.get('fsrs_optimization', {}):
            improvement = results['fsrs_optimization']['validation'].get('improvement_percent', 0)
            print(f"   📈 FSRS Improvement: {improvement:+.2f}%")
    
    return results

def create_optimized_system(optimization_results):
    """Create a new system instance using optimized parameters"""
    from BKT_Algorithm.Optimisation_System_Integration import OptimizedSystemFactory
    
    # Save the integrated config to a temporary file
    config_filename = f"test_optimized_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    with open(config_filename, 'w') as f:
        json.dump(optimization_results['integration_config'], f, indent=2, default=str)
    
    print(f"   💾 Saved optimized config: {config_filename}")
    
    # Create optimized system
    optimized_kg, optimized_student_manager, optimized_mcq_scheduler, optimized_bkt_system = OptimizedSystemFactory.create_optimized_system(
        config_filename,
        nodes_file='_static/small-graph-kg.json',
        mcqs_file='_static/small-graph-computed_mcqs.json'
    )
    
    print(f"   ⚙️ Optimized system uses {len(optimized_kg.config.get('bkt_parameters', {}).get('topic_specific', {}))} topic-specific BKT parameters")
    
    return optimized_kg, optimized_student_manager, optimized_mcq_scheduler, optimized_bkt_system

def test_performance_comparison(baseline_system, optimized_system):
    """Compare performance between baseline and optimized systems"""
    from Parameter_Assessment_Test import create_realistic_student, simulate_learning_sessions
    
    baseline_kg, baseline_sm, baseline_sched, baseline_bkt = baseline_system
    optimized_kg, optimized_sm, optimized_sched, optimized_bkt = optimized_system
    
    # Test with 3 new students on each system
    test_results = {
        'baseline': {'students': [], 'total_attempts': 0, 'avg_mastery_gain': 0},
        'optimized': {'students': [], 'total_attempts': 0, 'avg_mastery_gain': 0}
    }
    
    for system_name, (kg, sm, sched, bkt) in [('baseline', baseline_system), ('optimized', optimized_system)]:
        mastery_gains = []
        
        for i in range(3):
            student_id = f"test_{system_name}_{i}"
            
            # Create student
            create_realistic_student(sm, student_id, kg)
            student = sm.get_student(student_id)
            
            # Record initial mastery
            initial_mastery = {idx: student.get_mastery(idx) for idx in kg.get_all_indexes()}
            
            # Run learning sessions
            attempts = simulate_learning_sessions(kg, sm, sched, bkt, student_id, num_sessions=5)
            
            # Calculate mastery gain
            final_mastery = {idx: student.get_mastery(idx) for idx in kg.get_all_indexes()}
            avg_gain = sum(final_mastery[idx] - initial_mastery[idx] for idx in initial_mastery) / len(initial_mastery)
            
            mastery_gains.append(avg_gain)
            test_results[system_name]['students'].append(student_id)
            test_results[system_name]['total_attempts'] += len(attempts)
        
        test_results[system_name]['avg_mastery_gain'] = sum(mastery_gains) / len(mastery_gains)
        
        print(f"   {system_name.title()}: {len(mastery_gains)} students, avg mastery gain: {test_results[system_name]['avg_mastery_gain']:.3f}")
    
    return test_results

def display_final_results(optimization_results, comparison_results):
    """Display comprehensive test results"""
    
    print("\n📊 OPTIMIZATION RESULTS:")
    
    # BKT Results
    bkt_results = optimization_results.get('bkt_optimization', {})
    if bkt_results:
        print(f"   📚 BKT Topics Optimized: {len(bkt_results)}")
        avg_prior = sum(p['prior'] for p in bkt_results.values()) / len(bkt_results)
        avg_learn = sum(p['learn'] for p in bkt_results.values()) / len(bkt_results)
        print(f"      Average prior knowledge: {avg_prior:.3f}")
        print(f"      Average learning rate: {avg_learn:.3f}")
    
    # FSRS Results
    fsrs_results = optimization_results.get('fsrs_optimization', {})
    if fsrs_results and fsrs_results.get('success'):
        print(f"   🧠 FSRS Optimization: ✅ Success")
        if 'optimal_parameters' in fsrs_results:
            print(f"      Parameters optimized: {len(fsrs_results['optimal_parameters'])}")
        if 'validation' in fsrs_results:
            improvement = fsrs_results['validation'].get('improvement_percent', 0)
            print(f"      Validation improvement: {improvement:+.2f}%")
    
    # Performance Comparison
    print(f"\n📈 PERFORMANCE COMPARISON:")
    baseline_gain = comparison_results['baseline']['avg_mastery_gain']
    optimized_gain = comparison_results['optimized']['avg_mastery_gain']
    improvement = ((optimized_gain - baseline_gain) / abs(baseline_gain)) * 100 if baseline_gain != 0 else 0
    
    print(f"   Baseline system: {baseline_gain:.3f} avg mastery gain")
    print(f"   Optimized system: {optimized_gain:.3f} avg mastery gain")
    print(f"   Performance improvement: {improvement:+.1f}%")
    
    # Validation
    validation = optimization_results.get('validation_metrics', {})
    if validation:
        config_valid = validation.get('config_validation', {}).get('required_sections_present', False)
        param_valid = validation.get('parameter_sanity_check', {})
        compat = validation.get('system_compatibility', {}).get('config_loads', False)
        
        print(f"\n✅ VALIDATION:")
        print(f"   Config structure: {'✅ Valid' if config_valid else '❌ Invalid'}")
        print(f"   Parameters: {len(param_valid.get('valid_parameters', []))} valid, {len(param_valid.get('invalid_parameters', []))} invalid")
        print(f"   System compatibility: {'✅ Compatible' if compat else '❌ Incompatible'}")

        save_optimization_files_to_bkt_folder(optimization_results, comparison_results)

    

def save_optimization_files_to_bkt_folder(optimization_results, comparison_results):
    """Save optimization files to BKT_Algorithm/JSON_Files folder"""
    
    folder = "BKT_Algorithm/JSON_Files"
    #os.makedirs(folder, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Save optimized config
    config_filename = os.path.join(folder, f"optimized_config_{timestamp}.json")
    with open(config_filename, 'w') as f:
        json.dump(optimization_results['integration_config'], f, indent=2, default=str)
    
    # Save full results
    results_filename = os.path.join(folder, f"optimization_results_{timestamp}.json")
    full_results = {
        'optimization_results': optimization_results,
        'comparison_results': comparison_results,
        'timestamp': datetime.now().isoformat()
    }
    with open(results_filename, 'w') as f:
        json.dump(full_results, f, indent=2, default=str)
    
    # Save summary text file
    summary_filename = os.path.join(folder, f"optimization_summary_{timestamp}.txt")
    with open(summary_filename, 'w') as f:
        f.write("BKT-FSRS OPTIMIZATION SUMMARY\n")
        f.write("=" * 40 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # BKT results
        bkt_results = optimization_results.get('bkt_optimization', {})
        if bkt_results:
            f.write(f"BKT Topics Optimized: {len(bkt_results)}\n")
        
        # FSRS results
        fsrs_results = optimization_results.get('fsrs_optimization', {})
        if fsrs_results and fsrs_results.get('success'):
            f.write("FSRS Optimization: Success\n")
        
        # Performance comparison
        baseline_gain = comparison_results['baseline']['avg_mastery_gain']
        optimized_gain = comparison_results['optimized']['avg_mastery_gain']
        improvement = ((optimized_gain - baseline_gain) / abs(baseline_gain)) * 100 if baseline_gain != 0 else 0
        f.write(f"\nPerformance Improvement: {improvement:+.1f}%\n")
    
    print(f"\n💾 FILES SAVED TO {folder}:")
    print(f"   📄 {config_filename}")
    print(f"   📊 {results_filename}")  
    print(f"   📋 {summary_filename}")
    
    return [config_filename, results_filename, summary_filename]

def run_quick_test():
    """Quick test version with minimal data"""
    print("🧪 RUNNING QUICK INTEGRATION TEST")
    print("=" * 50)
    
    try:
        # Just test imports and basic functionality
        print(" Testing imports...")
        from _static.mcq_algorithm_current import KnowledgeGraph, StudentManager
        from BKT_Algorithm.Optimisation_System_Integration import IntegratedParameterOptimizer
        print("✅ All imports successful")
        
        print("📊 Testing system initialization...")
        kg = KnowledgeGraph('_static/small-graph-kg.json', '_static/small-graph-computed_mcqs.json', '_static/config.json')
        student_manager = StudentManager(kg.config)
        print("✅ System initialization successful")
        
        print("👤 Testing student creation...")
        from Parameter_Assessment_Test import create_realistic_student
        create_realistic_student(student_manager, "test_student", kg)
        print("✅ Student creation successful")
        
        print("🎉 QUICK TEST PASSED! Run main() for full integration test.")
        return True
        
    except Exception as e:
        print(f"❌ QUICK TEST FAILED: {e}")
        return False

if __name__ == "__main__":
    print("BKT-FSRS Integration Test")
    print("Choose test mode:")
    print("1. Full integration test (recommended)")
    print("2. Quick test (imports and basic functionality)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "2":
        success = run_quick_test()
    else:
        print("Running full integration test...\n")
        success = main()
    
    if success:
        print("\n🎉 Integration test completed successfully!")
    else:
        print("\n❌ Integration test failed. Check error messages above.")