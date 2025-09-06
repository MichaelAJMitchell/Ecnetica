"""
This python file provides the integration layer that connects:
1. BKT parameter optimization (Parameter_Assessment_Test.py)
2. FSRS parameter optimization (FSRS_Parameter_Assessment.py)  
3. Main MCQ algorithm with optimized parameters (mcq_algorithm_current.py)
"""

import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import asdict
import copy
import sys
sys.path.append('./')


# Import optimization modules
try:
    from BKT_Algorithm.FSRS_Parameter_Assessment import EfficientFSRSOptimizer, run_efficient_fsrs_optimization
    FSRS_OPTIMIZER_AVAILABLE = True
except ImportError:
    FSRS_OPTIMIZER_AVAILABLE = False
    print(" FSRS optimizer not available")

try:
    from BKT_Algorithm.Parameter_Assessment_Test import fit_bkt_parameters_sklearn, test_parameter_fitting
    BKT_OPTIMIZER_AVAILABLE = True
except ImportError:
    BKT_OPTIMIZER_AVAILABLE = False
    print(" BKT optimizer not available")

try:
    from _static.mcq_algorithm import (
        KnowledgeGraph, StudentManager, BayesianKnowledgeTracing, MCQScheduler,
        FSRSForgettingConfig, ConfigurationManager
    )
    MAIN_SYSTEM_AVAILABLE = True
except ImportError:
    MAIN_SYSTEM_AVAILABLE = False
    print("⚠️ Main MCQ system not available")

class IntegratedParameterOptimizer:
    """
    Unified parameter optimization for BKT-FSRS system
    """
    
    def __init__(self, kg, student_manager):
        self.kg = kg
        self.student_manager = student_manager
        self.optimization_results = {}
        
    def run_complete_optimization(self, 
                                min_attempts_per_topic: int = 5,
                                train_test_split: float = 0.8,
                                save_results: bool = True) -> Dict:
        """
        Run complete parameter optimization for both BKT and FSRS
        """
        print(" INTEGRATED BKT-FSRS PARAMETER OPTIMIZATION")
        print("="*60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'bkt_optimization': None,
            'fsrs_optimization': None,
            'integration_config': None,
            'validation_metrics': None
        }
        
        # Step 1: BKT Parameter Optimization
        if BKT_OPTIMIZER_AVAILABLE:
            print("\n  1: BKT Parameter Optimization")
            print("-" * 40)
            bkt_results = self._optimize_bkt_parameters(min_attempts_per_topic)
            results['bkt_optimization'] = bkt_results
            print(f" BKT optimization complete: {len(bkt_results)} topics fitted")
        else:
            print(" Skipping BKT optimization - module not available")
        
        # Step 2: FSRS Parameter Optimization  
        if FSRS_OPTIMIZER_AVAILABLE:
            print("\n  2: FSRS Parameter Optimization")
            print("-" * 40)
            fsrs_results = self._optimize_fsrs_parameters(train_test_split)
            results['fsrs_optimization'] = fsrs_results
            if fsrs_results.get('optimization', {}).get('optimization_success'):
                print(" FSRS optimization complete")
            else:
                print(" FSRS optimization failed")
        else:
            print(" Skipping FSRS optimization - module not available")
        
        # Step 3: Create integrated configuration
        print("\n  3: Integration Configuration")
        print("-" * 40)
        integration_config = self._create_integrated_config(
            results['bkt_optimization'],
            results['fsrs_optimization']
        )
        results['integration_config'] = integration_config
        print("✅ Integration configuration created")
        
        # Step 4: Validation
        print("\n 4: Validation")
        print("-" * 40)
        validation_metrics = self._validate_integrated_system(integration_config)
        results['validation_metrics'] = validation_metrics
        print("✅ Validation complete")
        
        # Step 5: Save results
        if save_results:
            self._save_optimization_results(results)
        
        # Final summary
        self._print_optimization_summary(results)
        
        return results
    
    def _optimize_bkt_parameters(self, min_attempts_per_topic: int) -> Dict:
        """Optimize BKT parameters using existing student data"""
        bkt_results = {}
        
        # Extract attempts data grouped by topic
        topic_attempts = {}
        for student_id, student in self.student_manager.students.items():
            for attempt in student.attempt_history:
                # Get topic index
                if hasattr(self.kg, 'ultra_loader'):
                    minimal_data = self.kg.ultra_loader.get_minimal_mcq_data(attempt.mcq_id)
                    topic_idx = minimal_data.main_topic_index if minimal_data else None
                else:
                    mcq = self.kg.mcqs.get(attempt.mcq_id)
                    topic_idx = mcq.main_topic_index if mcq else None
                
                if topic_idx is None:
                    continue
                
                topic_name = self.kg.get_topic_of_index(topic_idx)
                if topic_name not in topic_attempts:
                    topic_attempts[topic_name] = []
                
                topic_attempts[topic_name].append({
                    'student_id': student_id,
                    'correct': 1 if attempt.correct else 0,
                    'timestamp': attempt.timestamp
                })
        
        # Fit BKT parameters for each topic with sufficient data
        for topic_name, attempts in topic_attempts.items():
            if len(attempts) >= min_attempts_per_topic:
                print(f"   Fitting BKT for {topic_name}: {len(attempts)} attempts")
                
                # Convert to response sequence
                responses = [attempt['correct'] for attempt in attempts]
                
                # Fit parameters
                fitted_params = fit_bkt_parameters_sklearn(responses, num_restarts=5)
                
                if fitted_params:
                    bkt_results[topic_name] = {
                        'prior': fitted_params['prior'],
                        'learn': fitted_params['learns'][0],
                        'guess': fitted_params['guesses'][0],
                        'slip': fitted_params['slips'][0],
                        'likelihood': fitted_params['likelihood'],
                        'n_attempts': len(attempts),
                        'success_rate': np.mean(responses)
                    }
                    print(f"       Success: P(L0)={fitted_params['prior']:.3f}")
                else:
                    print(f"       Failed to fit")
        
        return bkt_results
    
    def _optimize_fsrs_parameters(self, train_test_split: float) -> Dict:
        """Optimize FSRS parameters using efficient official libraries"""
        if not FSRS_OPTIMIZER_AVAILABLE:
            return {'error': 'Efficient FSRS optimizer not available'}
        
        # Use the efficient optimization with official libraries
        return run_efficient_fsrs_optimization(
            self.kg, 
            self.student_manager, 
            validate=True,
            save_results=False  # We'll save everything together
        )
    
    def _create_integrated_config(self, bkt_results: Optional[Dict], 
                                fsrs_results: Optional[Dict]) -> Dict:
        """Create integrated configuration file with optimized parameters"""
        
        # Start with current config as base
        base_config = self.kg.config.config if hasattr(self.kg, 'config') else {}
        integrated_config = copy.deepcopy(base_config)
        
        # Add BKT optimizations
        if bkt_results:
            # Create topic-specific BKT parameters section
            if 'bkt_parameters' not in integrated_config:
                integrated_config['bkt_parameters'] = {'default': {}, 'topic_specific': {}}
            
            # Calculate average parameters for default
            if bkt_results:
                avg_prior = np.mean([p['prior'] for p in bkt_results.values()])
                avg_learn = np.mean([p['learn'] for p in bkt_results.values()])
                avg_guess = np.mean([p['guess'] for p in bkt_results.values()])
                avg_slip = np.mean([p['slip'] for p in bkt_results.values()])
                
                integrated_config['bkt_parameters']['default'] = {
                    'prior_knowledge': float(avg_prior),
                    'learning_rate': float(avg_learn),
                    'slip_rate': float(avg_slip),
                    'guess_rate': float(avg_guess)
                }
            
            # Add topic-specific parameters
            for topic_name, params in bkt_results.items():
                # Get topic index for key
                topic_idx = None
                for idx in self.kg.get_all_indexes():
                    if self.kg.get_topic_of_index(idx) == topic_name:
                        topic_idx = idx
                        break
                
                if topic_idx is not None:
                    integrated_config['bkt_parameters']['topic_specific'][str(topic_idx)] = {
                        'prior_knowledge': float(params['prior']),
                        'learning_rate': float(params['learn']),
                        'slip_rate': float(params['slip']),
                        'guess_rate': float(params['guess']),
                        'description': f"Optimized for {topic_name}",
                        'n_attempts': params['n_attempts'],
                        'likelihood': float(params['likelihood'])
                    }
        
        # Add FSRS optimizations
        if fsrs_results and fsrs_results.get('optimization', {}).get('optimization_success'):
            fsrs_params = fsrs_results['optimization']['optimized_parameters']
            
            # Update FSRS config section
            if 'bkt_config' not in integrated_config:
                integrated_config['bkt_config'] = {}
            
            # Map optimized parameters to config structure
            integrated_config['bkt_config'].update({
                'enable_fsrs_forgetting': True,
                'fsrs_stability_power': float(fsrs_params['stability_power_factor']),
                'fsrs_difficulty_power': float(fsrs_params['difficulty_power_factor']),
                'fsrs_retrievability_power': float(fsrs_params['retrievability_power_factor']),
                'fsrs_stability_weight': float(fsrs_params['stability_weight']),
                'fsrs_difficulty_weight': float(fsrs_params['difficulty_weight']),
                'fsrs_retrievability_weight': float(fsrs_params['retrievability_weight']),
                'fsrs_success_stability_boost': float(fsrs_params['success_stability_boost']),
                'fsrs_failure_stability_penalty': float(fsrs_params['failure_stability_penalty']),
                'fsrs_difficulty_adaptation_rate': float(fsrs_params['difficulty_adaptation_rate']),
                'fsrs_base_forgetting_time': float(fsrs_params['base_forgetting_time']),
                'fsrs_max_stability': float(fsrs_params['max_stability']),
                'fsrs_min_stability': float(fsrs_params['min_stability'])
            })
            
            # Add optimization metadata
            integrated_config['optimization_metadata'] = {
                'fsrs_log_likelihood': float(fsrs_results['optimization']['log_likelihood']),
                'fsrs_optimization_method': fsrs_results['optimization']['method'],
                'fsrs_validation_improvement': fsrs_results.get('validation', {}).get('improvement_percent', 0.0)
            }
        
        # Add metadata about optimization
        integrated_config['metadata'] = integrated_config.get('metadata', {})
        integrated_config['metadata'].update({
            'config_version': '2.0_optimized',
            'optimization_timestamp': datetime.now().isoformat(),
            'bkt_topics_optimized': len(bkt_results) if bkt_results else 0,
            'fsrs_optimized': fsrs_results is not None and fsrs_results.get('optimization', {}).get('optimization_success', False),
            'description': 'Integrated BKT-FSRS configuration with optimized parameters'
        })
        
        return integrated_config
    
    def _validate_integrated_system(self, integrated_config: Dict) -> Dict:
        """Validate the integrated system with optimized parameters"""
        validation_results = {
            'config_validation': self._validate_config_structure(integrated_config),
            'parameter_sanity_check': self._validate_parameter_ranges(integrated_config),
            'system_compatibility': self._test_system_compatibility(integrated_config)
        }
        
        return validation_results
    
    def _validate_config_structure(self, config: Dict) -> Dict:
        """Validate that the config has proper structure"""
        required_sections = ['bkt_parameters', 'bkt_config', 'algorithm_config']
        missing_sections = [section for section in required_sections if section not in config]
        
        return {
            'required_sections_present': len(missing_sections) == 0,
            'missing_sections': missing_sections,
            'has_optimization_metadata': 'optimization_metadata' in config
        }
    
    def _validate_parameter_ranges(self, config: Dict) -> Dict:
        """Validate that optimized parameters are in reasonable ranges"""
        validation_results = {'valid_parameters': [], 'invalid_parameters': []}
        
        # Validate BKT parameters
        if 'bkt_parameters' in config:
            default_bkt = config['bkt_parameters'].get('default', {})
            for param, value in default_bkt.items():
                if param in ['prior_knowledge', 'learning_rate', 'slip_rate', 'guess_rate']:
                    if 0.0 <= value <= 1.0:
                        validation_results['valid_parameters'].append(f"BKT {param}: {value:.3f}")
                    else:
                        validation_results['invalid_parameters'].append(f"BKT {param}: {value:.3f} (out of range)")
        
        # Validate FSRS parameters
        if 'bkt_config' in config:
            fsrs_params = {k: v for k, v in config['bkt_config'].items() if k.startswith('fsrs_')}
            for param, value in fsrs_params.items():
                # Basic sanity checks for FSRS parameters
                if 'weight' in param and not (0.0 <= value <= 1.0):
                    validation_results['invalid_parameters'].append(f"FSRS {param}: {value:.3f} (weight out of range)")
                elif 'stability' in param and value <= 0:
                    validation_results['invalid_parameters'].append(f"FSRS {param}: {value:.3f} (should be positive)")
                else:
                    validation_results['valid_parameters'].append(f"FSRS {param}: {value:.3f}")
        
        return validation_results
    
    def _test_system_compatibility(self, config: Dict) -> Dict:
        """Test that the optimized config works with the main system"""
        try:
            # Try to create a temporary config manager with optimized parameters
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(config, f, indent=2)
                temp_config_path = f.name
            
            try:
                # Test if ConfigurationManager can load the optimized config
                temp_config_manager = ConfigurationManager(temp_config_path)
                
                # Test basic operations
                default_bkt = temp_config_manager.get_bkt_parameters()
                fsrs_enabled = temp_config_manager.get('bkt_config.enable_fsrs_forgetting', False)
                
                compatibility_result = {
                    'config_loads': True,
                    'bkt_parameters_accessible': default_bkt is not None,
                    'fsrs_enabled': fsrs_enabled,
                    'error': None
                }
                
            finally:
                os.unlink(temp_config_path)
                
        except Exception as e:
            compatibility_result = {
                'config_loads': False,
                'bkt_parameters_accessible': False,
                'fsrs_enabled': False,
                'error': str(e)
            }
        
        return compatibility_result
    
    def _save_optimization_results(self, results: Dict):
        """Save complete optimization results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save integrated config
        config_filename = f'optimized_config_{timestamp}.json'
        with open(config_filename, 'w') as f:
            json.dump(results['integration_config'], f, indent=2, default=str)
        print(f"💾 Saved optimized config: {config_filename}")
        
        # Save full results
        results_filename = f'optimization_results_{timestamp}.json'
        with open(results_filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Saved full results: {results_filename}")
        
        # Save summary report
        summary_filename = f'optimization_summary_{timestamp}.txt'
        with open(summary_filename, 'w') as f:
            f.write(self._generate_summary_report(results))
        print(f"📄 Saved summary report: {summary_filename}")
    
    def _generate_summary_report(self, results: Dict) -> str:
        """Generate human-readable summary report"""
        lines = [
            "INTEGRATED BKT-FSRS OPTIMIZATION SUMMARY",
            "=" * 50,
            f"Optimization completed: {results['timestamp']}",
            ""
        ]
        
        # BKT Results
        bkt_results = results.get('bkt_optimization', {})
        if bkt_results:
            lines.extend([
                "BKT PARAMETER OPTIMIZATION:",
                f"  Topics optimized: {len(bkt_results)}",
                f"  Average prior knowledge: {np.mean([p['prior'] for p in bkt_results.values()]):.3f}",
                f"  Average learning rate: {np.mean([p['learn'] for p in bkt_results.values()]):.3f}",
                ""
            ])
        
        # FSRS Results
        fsrs_results = results.get('fsrs_optimization', {})
        if fsrs_results and fsrs_results.get('optimization', {}).get('optimization_success'):
            validation = fsrs_results.get('validation', {})
            lines.extend([
                "FSRS PARAMETER OPTIMIZATION:",
                f"  Optimization successful: Yes",
                f"  Log likelihood: {fsrs_results['optimization']['log_likelihood']:.6f}",
                f"  Validation improvement: {validation.get('improvement_percent', 0):.2f}%",
                ""
            ])
        
        # Validation
        validation = results.get('validation_metrics', {})
        if validation:
            config_valid = validation.get('config_validation', {})
            param_valid = validation.get('parameter_sanity_check', {})
            compat = validation.get('system_compatibility', {})
            
            lines.extend([
                "VALIDATION RESULTS:",
                f"  Config structure valid: {config_valid.get('required_sections_present', False)}",
                f"  Valid parameters: {len(param_valid.get('valid_parameters', []))}",
                f"  Invalid parameters: {len(param_valid.get('invalid_parameters', []))}",
                f"  System compatibility: {compat.get('config_loads', False)}",
                ""
            ])
        
        lines.extend([
            "NEXT STEPS:",
            "1. Review the optimized_config_*.json file",
            "2. Update your main system to use the optimized config",
            "3. Monitor system performance with new parameters",
            "4. Consider re-optimization as more data becomes available"
        ])
        
        return "\n".join(lines)
    
    def _print_optimization_summary(self, results: Dict):
        """Print final optimization summary"""
        print("\n" + "=" * 60)
        print(" INTEGRATED OPTIMIZATION COMPLETE")
        print("=" * 60)
        
        bkt_count = len(results.get('bkt_optimization', {}))
        fsrs_success = results.get('fsrs_optimization', {}).get('optimization', {}).get('optimization_success', False)
        
        print(f" BKT Topics Optimized: {bkt_count}")
        print(f" FSRS Optimization: {'Success' if fsrs_success else ' Failed'}")
        
        if fsrs_success:
            improvement = results.get('fsrs_optimization', {}).get('validation', {}).get('improvement_percent', 0)
            print(f" FSRS Improvement: {improvement:+.2f}%")
        
        validation = results.get('validation_metrics', {})
        if validation:
            valid_params = len(validation.get('parameter_sanity_check', {}).get('valid_parameters', []))
            invalid_params = len(validation.get('parameter_sanity_check', {}).get('invalid_parameters', []))
            print(f" Parameter Validation: {valid_params} valid, {invalid_params} invalid")
        
        print("\n System is now ready with optimized parameters")

class OptimizedSystemFactory:
    """
    Factory class to create system instances with optimized parameters
    """
    
    @staticmethod
    def create_optimized_system(optimized_config_path: str, 
                              nodes_file: str = 'small-graph-kg.json',
                              mcqs_file: str = 'small-graph-computed_mcqs.json') -> Tuple[Any, Any, Any, Any]:
        """
        Create a complete system using optimized parameters
        Returns: (kg, student_manager, mcq_scheduler, bkt_system)
        """
        if not MAIN_SYSTEM_AVAILABLE:
            raise ImportError("Main MCQ system not available")
        
        print(f" Creating optimized system from {optimized_config_path}")
        
        # Initialize with optimized config
        kg = KnowledgeGraph(
            nodes_file=nodes_file,
            mcqs_file=mcqs_file,
            config_file=optimized_config_path
        )
        
        student_manager = StudentManager(kg.config)
        mcq_scheduler = MCQScheduler(kg, student_manager)
        bkt_system = BayesianKnowledgeTracing(kg, student_manager)
        
        # Connect systems
        mcq_scheduler.set_bkt_system(bkt_system)
        student_manager.set_bkt_system(bkt_system)
        
        print("✅ Optimized system created successfully")
        
        return kg, student_manager, mcq_scheduler, bkt_system

# Main execution function
def run_complete_optimization_pipeline(nodes_file: str = 'small-graph-kg.json',
                                     mcqs_file: str = 'small-graph-computed_mcqs.json',
                                     config_file: str = 'config.json',
                                     simulate_data: bool = True,
                                     n_simulation_students: int = 10) -> Dict:
    """
    Run the complete optimization pipeline from scratch
    """
    if not MAIN_SYSTEM_AVAILABLE:
        return {'error': 'Main system not available'}
    
    print(" COMPLETE BKT-FSRS OPTIMIZATION PIPELINE")
    print("=" * 60)
    
    # Initialize base system
    kg = KnowledgeGraph(nodes_file, mcqs_file, config_file)
    student_manager = StudentManager(kg.config)
    mcq_scheduler = MCQScheduler(kg, student_manager)
    bkt_system = BayesianKnowledgeTracing(kg, student_manager)
    
    # Connect systems
    mcq_scheduler.set_bkt_system(bkt_system)
    student_manager.set_bkt_system(bkt_system)
    
    # Generate simulation data if requested
    if simulate_data:
        print(f"\n Generating simulation data for {n_simulation_students} students...")
        try:
            from Parameter_Assessment_Test import create_realistic_student, simulate_learning_sessions
            
            for i in range(n_simulation_students):
                student_id = f"optimization_student_{i}"
                create_realistic_student(student_manager, student_id, kg)
                
                attempts = simulate_learning_sessions(
                    kg, student_manager, mcq_scheduler, bkt_system,
                    student_id, num_sessions=15
                )
                print(f"   Generated {len(attempts)} attempts for {student_id}")
                
        except ImportError:
            print(" Simulation functions not available - using existing data only")
    
    # Run optimization
    optimizer = IntegratedParameterOptimizer(kg, student_manager)
    results = optimizer.run_complete_optimization(save_results=True)
    
    return results

# Example usage and testing
if __name__ == "__main__":
    print("Integrated BKT-FSRS System")
    print("This module provides complete parameter optimization for your learning system")
    print("\nQuick start:")
    print("  results = run_complete_optimization_pipeline()")
    print("  kg, sm, sched, bkt = OptimizedSystemFactory.create_optimized_system('optimized_config_*.json')")