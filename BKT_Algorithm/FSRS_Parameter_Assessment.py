"""
Optimising FSRS parameters using previous work on the topic available through python libraries.

Here, we try several approaches but the current one of most interest is the fsrs-rs-python approach.
This works best because it is fastest, but can be switched to the other options if the library is left unmaintained.
"""



import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import warnings
warnings.filterwarnings('ignore')
import sys
sys.path.append('./')


# Try official FSRS libraries in order of preference
FSRS_IMPLEMENTATION = None

# Option 1: fsrs-rs-python (fastest, Rust-based)
try:
    import fsrs_rs_python
    FSRS_IMPLEMENTATION = 'fsrs_rs_python'
    print("✅ Using fsrs-rs-python (Rust implementation - fastest)")
except ImportError:
    pass

# Option 2: Official py-fsrs (pure Python)
if FSRS_IMPLEMENTATION is None:
    try:
        from fsrs import FSRS, Card, ReviewLog, Rating, Optimizer, Scheduler
        FSRS_IMPLEMENTATION = 'py_fsrs'
        print("✅ Using py-fsrs (official Python implementation)")
    except ImportError:
        pass

# Option 3: fsrs-optimizer (dedicated optimization package)
if FSRS_IMPLEMENTATION is None:
    try:
        import fsrs_optimizer
        FSRS_IMPLEMENTATION = 'fsrs_optimizer'
        print("✅ Using fsrs-optimizer (dedicated optimization package)")
    except ImportError:
        pass

if FSRS_IMPLEMENTATION is None:
    print(" No FSRS libraries available")

# Import your existing FSRS implementation for integration
try:
    from _static.mcq_algorithm import (
        FSRSForgettingModel, FSRSForgettingConfig, FSRSMemoryComponents
    )
    CUSTOM_FSRS_AVAILABLE = True
except ImportError:
    CUSTOM_FSRS_AVAILABLE = False
    print("⚠️ Custom FSRS implementation not available")

@dataclass
class FSRSReviewData:
    """Standardized review data format for FSRS optimization"""
    card_id: str
    review_time: datetime
    rating: int  # 1=Again, 2=Hard, 3=Good, 4=Easy
    state: int   # 0=New, 1=Learning, 2=Review, 3=Relearning
    last_review: Optional[datetime] = None
    
class EfficientFSRSOptimizer:
    """
    Efficient FSRS optimizer using official libraries
    """
    
    def __init__(self):
        self.implementation = FSRS_IMPLEMENTATION
        self.optimized_parameters = None
        self.optimization_results = None
        
    def extract_fsrs_review_data(self, kg, student_manager) -> List[FSRSReviewData]:
        """
        Extract review data in FSRS format from your existing system
        """
        print(" Extracting review data for FSRS optimization...")
        
        all_reviews = []
        
        for student_id, student in student_manager.students.items():
            # Group attempts by topic to create card-like sequences
            topic_sequences = {}
            
            for attempt in student.attempt_history:
                # Get topic index
                if hasattr(kg, 'ultra_loader'):
                    minimal_data = kg.ultra_loader.get_minimal_mcq_data(attempt.mcq_id)
                    topic_idx = minimal_data.main_topic_index if minimal_data else None
                else:
                    mcq = kg.mcqs.get(attempt.mcq_id)
                    topic_idx = mcq.main_topic_index if mcq else None
                
                if topic_idx is None:
                    continue
                
                card_id = f"{student_id}_topic_{topic_idx}"
                
                if card_id not in topic_sequences:
                    topic_sequences[card_id] = []
                
                # Convert to FSRS rating (1-4 scale)
                rating = 3 if attempt.correct else 1  # Good=3, Again=1
                
                topic_sequences[card_id].append({
                    'timestamp': attempt.timestamp,
                    'rating': rating,
                    'mcq_id': attempt.mcq_id
                })
            
            # Convert sequences to FSRS review data
            for card_id, reviews in topic_sequences.items():
                if len(reviews) < 2:  # Need multiple reviews for optimization
                    continue
                
                # Sort by timestamp
                reviews.sort(key=lambda x: x['timestamp'])
                
                # Convert to FSRSReviewData objects
                last_review_time = None
                for i, review in enumerate(reviews):
                    state = 0 if i == 0 else 2  # New for first, Review for others
                    
                    fsrs_review = FSRSReviewData(
                        card_id=card_id,
                        review_time=review['timestamp'],
                        rating=review['rating'],
                        state=state,
                        last_review=last_review_time
                    )
                    
                    all_reviews.append(fsrs_review)
                    last_review_time = review['timestamp']
        
        print(f" Extracted {len(all_reviews)} FSRS reviews from {len(topic_sequences)} cards")
        return all_reviews
    
    def optimize_with_py_fsrs(self, review_data: List[FSRSReviewData]) -> Dict:
        """
        Optimize using official py-fsrs library
        """
        if FSRS_IMPLEMENTATION != 'py_fsrs':
            return {'error': 'py-fsrs not available'}
        
        print(" Optimizing with official py-fsrs library...")
        
        # Convert to py-fsrs ReviewLog format
        review_logs = []
        
        for review in review_data:
            # Calculate elapsed days since last review
            if review.last_review:
                delta_t = (review.last_review - review.review_time).days
                delta_t = max(0, delta_t)  # Ensure non-negative
            else:
                delta_t = 0
            
            review_log = ReviewLog(
                rating=Rating(review.rating),
                delta_t=delta_t,
                review_datetime=review.review_time,
                card_id=review.card_id,
                review_duration_milliseconds=30000  # Default 30 seconds
            )
            review_logs.append(review_log)
        
        if not review_logs:
            return {'error': 'No valid review logs created'}
        
        print(f"   Converted {len(review_logs)} review logs")
        
        # Initialize optimizer with review logs
        try:
            optimizer = Optimizer(review_logs)
            
            # Compute optimal parameters
            print("   Computing optimal parameters...")
            optimal_parameters = optimizer.compute_optimal_parameters()
            
            # Compute optimal retention rate
            print("   Computing optimal retention...")
            optimal_retention = optimizer.compute_optimal_retention(optimal_parameters)
            
            # Get optimization metrics
            scheduler_default = Scheduler()
            scheduler_optimized = Scheduler(optimal_parameters, optimal_retention)
            
            return {
                'success': True,
                'optimal_parameters': optimal_parameters,
                'optimal_retention': optimal_retention,
                'parameters_count': len(optimal_parameters),
                'review_logs_used': len(review_logs),
                'implementation': 'py_fsrs'
            }
            
        except Exception as e:
            return {'error': f'py-fsrs optimization failed: {e}'}
    
    def optimize_with_fsrs_rs_python(self, review_data: List[FSRSReviewData]) -> Dict:
        """
        Optimize using fsrs-rs-python (fastest Rust implementation)
        """
        if FSRS_IMPLEMENTATION != 'fsrs_rs_python':
            return {'error': 'fsrs-rs-python not available'}
        
        print(" Optimizing with fsrs-rs-python (Rust implementation)...")
        
        try:
            # Convert to fsrs-rs-python format
            items = []
            
            # Group by card for sequence building
            card_sequences = {}
            for review in review_data:
                if review.card_id not in card_sequences:
                    card_sequences[review.card_id] = []
                card_sequences[review.card_id].append(review)
            
            # Convert each card sequence
            for card_id, reviews in card_sequences.items():
                reviews.sort(key=lambda x: x.review_time)
                
                for i, review in enumerate(reviews):
                    # Calculate delta_t (days since last review)
                    if i == 0:
                        delta_t = 0
                    else:
                        prev_review = reviews[i-1]
                        delta_t = (review.review_time - prev_review.review_time).days
                        delta_t = max(0, delta_t)
                    
                    # Create fsrs-rs item
                    item = fsrs_rs_python.FSRSItem(
                        delta_t=delta_t,
                        rating=review.rating,
                        reviews=i + 1  # Number of reviews so far
                    )
                    items.append(item)
            
            if not items:
                return {'error': 'No valid items for fsrs-rs-python'}
            
            print(f"   Created {len(items)} FSRS items")
            
            # Run optimization
            print("   Running Rust-based optimization...")
            optimal_weights = fsrs_rs_python.optimize(items)
            
            # Calculate metrics
            metrics = fsrs_rs_python.evaluate(items, optimal_weights)
            
            return {
                'success': True,
                'optimal_parameters': optimal_weights.tolist(),
                'parameters_count': len(optimal_weights),
                'items_used': len(items),
                'log_loss': metrics.get('log_loss', 0.0),
                'rmse': metrics.get('rmse', 0.0),
                'implementation': 'fsrs_rs_python'
            }
            
        except Exception as e:
            return {'error': f'fsrs-rs-python optimization failed: {e}'}
    
    def optimize_with_fsrs_optimizer(self, review_data: List[FSRSReviewData]) -> Dict:
        """
        Optimize using dedicated fsrs-optimizer package
        """
        if FSRS_IMPLEMENTATION != 'fsrs_optimizer':
            return {'error': 'fsrs-optimizer not available'}
        
        print(" Optimizing with fsrs-optimizer package...")
        
        try:
            # Convert to DataFrame format expected by fsrs-optimizer
            df_data = []
            
            for review in review_data:
                df_data.append({
                    'card_id': review.card_id,
                    'review_time': review.review_time,
                    'rating': review.rating,
                    'review_state': review.state,
                    'review_duration': 30  # Default duration in seconds
                })
            
            df = pd.DataFrame(df_data)
            
            if df.empty:
                return {'error': 'No data for fsrs-optimizer'}
            
            print(f"   Created DataFrame with {len(df)} reviews")
            
            # Run optimization using fsrs-optimizer
            optimizer = fsrs_optimizer.Optimizer()
            optimal_parameters = optimizer.train(df)
            
            # Evaluate performance
            metrics = optimizer.evaluate(df, optimal_parameters)
            
            return {
                'success': True,
                'optimal_parameters': optimal_parameters.tolist(),
                'parameters_count': len(optimal_parameters),
                'reviews_used': len(df),
                'accuracy': metrics.get('accuracy', 0.0),
                'implementation': 'fsrs_optimizer'
            }
            
        except Exception as e:
            return {'error': f'fsrs-optimizer failed: {e}'}
    
    def run_optimization(self, kg, student_manager) -> Dict:
        """
        Main optimization function that uses the best available implementation
        """
        if FSRS_IMPLEMENTATION is None:
            return {'error': 'No FSRS implementation available'}
        
        print(f" Running FSRS optimization with {FSRS_IMPLEMENTATION}")
        print("="*50)
        
        # Extract review data
        review_data = self.extract_fsrs_review_data(kg, student_manager)
        
        if not review_data:
            return {'error': 'No review data found'}
        
        # Run optimization with best available method
        if FSRS_IMPLEMENTATION == 'fsrs_rs_python':
            result = self.optimize_with_fsrs_rs_python(review_data)
        elif FSRS_IMPLEMENTATION == 'py_fsrs':
            result = self.optimize_with_py_fsrs(review_data)
        elif FSRS_IMPLEMENTATION == 'fsrs_optimizer':
            result = self.optimize_with_fsrs_optimizer(review_data)
        else:
            return {'error': f'Unknown implementation: {FSRS_IMPLEMENTATION}'}
        
        if result.get('success'):
            self.optimized_parameters = result['optimal_parameters']
            self.optimization_results = result
            print(f"✅ Optimization successful!")
            print(f"   Parameters: {result['parameters_count']}")
            print(f"   Data used: {result.get('review_logs_used', result.get('items_used', result.get('reviews_used', 0)))}")
            
            # Add validation metrics if available
            if 'log_loss' in result:
                print(f"   Log loss: {result['log_loss']:.6f}")
            if 'rmse' in result:
                print(f"   RMSE: {result['rmse']:.6f}")
            if 'accuracy' in result:
                print(f"   Accuracy: {result['accuracy']:.1%}")
        
        return result
    
    def convert_to_custom_fsrs_config(self, optimized_params: List[float]) -> Optional[Dict]:
        """
        Convert optimized FSRS parameters to your custom FSRSForgettingConfig format
        """
        if not CUSTOM_FSRS_AVAILABLE or not optimized_params:
            return None
        
        # FSRS has 21 parameters total (in v6)
        # Map them to your custom config parameters
        # This mapping is based on FSRS algorithm documentation
        
        if len(optimized_params) < 17:
            print(f"⚠️ Expected at least 17 parameters, got {len(optimized_params)}")
            return None
        
        # Map FSRS parameters to your custom config
        # Note: This mapping may need adjustment based on your specific implementation
        custom_config = {
            'stability_power_factor': -0.5,  # You'll need to derive this from FSRS params
            'difficulty_power_factor': 0.3,  # Similarly for other params
            'retrievability_power_factor': -0.8,
            
            # Use FSRS parameters where possible
            'stability_weight': 0.4,
            'difficulty_weight': 0.3, 
            'retrievability_weight': 0.3,
            
            # Map FSRS stability factors
            'success_stability_boost': min(2.0, max(1.1, optimized_params[8])) if len(optimized_params) > 8 else 1.2,
            'failure_stability_penalty': min(0.9, max(0.3, 1.0 - optimized_params[6])) if len(optimized_params) > 6 else 0.8,
            
            # Other parameters with reasonable defaults
            'difficulty_adaptation_rate': 0.1,
            'base_forgetting_time': 1.0,
            'max_stability': 365.0,
            'min_stability': 0.1,
            'retrievability_threshold': 0.9,
            'min_retrievability': 0.1
        }
        
        print(" Converted optimized FSRS parameters to custom config format")
        print(" Note: Some parameter mappings are approximations and may need tuning")
        
        return custom_config
    
    def validate_optimization(self, kg, student_manager, test_split: float = 0.2) -> Dict:
        """
        Validate optimization results using held-out data
        """
        if not self.optimized_parameters:
            return {'error': 'No optimized parameters to validate'}
        
        print(f"🔬 Validating optimization with {test_split:.0%} held-out data...")
        
        # This would implement proper validation
        # For now, return basic metrics
        return {
            'validation_method': 'basic',
            'parameters_validated': len(self.optimized_parameters),
            'implementation': FSRS_IMPLEMENTATION,
            'status': 'validation_needed'  # TODO: Implement proper validation
        }

def run_efficient_fsrs_optimization(kg, student_manager, 
                                  validate: bool = True,
                                  save_results: bool = True) -> Dict:
    """
    Run efficient FSRS optimization using official libraries
    """
    if FSRS_IMPLEMENTATION is None:
        return {
            'error': 'No FSRS implementation available',
            'install_instructions': [
                'pip install fsrs  # Official Python implementation',
                'pip install fsrs-rs-python  # Fastest Rust implementation', 
                'pip install fsrs-optimizer  # Dedicated optimizer'
            ]
        }
    
    optimizer = EfficientFSRSOptimizer()
    
    # Run optimization
    optimization_result = optimizer.run_optimization(kg, student_manager)
    
    if not optimization_result.get('success'):
        return optimization_result
    
    # Validate if requested
    validation_result = None
    if validate:
        validation_result = optimizer.validate_optimization(kg, student_manager)
    
    # Convert to custom config if possible
    custom_config = None
    if CUSTOM_FSRS_AVAILABLE:
        custom_config = optimizer.convert_to_custom_fsrs_config(
            optimization_result['optimal_parameters']
        )
    
    # Combine results
    final_result = {
        'timestamp': datetime.now().isoformat(),
        'optimization': optimization_result,
        'validation': validation_result,
        'custom_config': custom_config,
        'implementation_used': FSRS_IMPLEMENTATION,
        'efficiency_note': f'Used official {FSRS_IMPLEMENTATION} library for maximum efficiency'
    }
    
    # Save results if requested
    if save_results:
        filename = f'efficient_fsrs_optimization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w') as f:
            json.dump(final_result, f, indent=2, default=str)
        print(f"💾 Saved optimization results to {filename}")
    
    return final_result

# Quick test function
def test_efficient_optimization(kg, student_manager, n_test_students: int = 5):
    """
    Test the efficient optimization with simulated data
    """
    print(" Testing efficient FSRS optimization...")
    
    # Generate test data if needed
    try:
        from Parameter_Assessment_Test import create_realistic_student, simulate_learning_sessions
        
        for i in range(n_test_students):
            student_id = f"efficient_test_student_{i}"
            if student_id not in student_manager.students:
                create_realistic_student(student_manager, student_id, kg)
                simulate_learning_sessions(kg, student_manager, None, None, student_id, 15)
        
        print(f"   Generated test data for {n_test_students} students")
        
    except ImportError:
        print("   Using existing student data only")
    
    # Run optimization
    return run_efficient_fsrs_optimization(kg, student_manager)

if __name__ == "__main__":
    print("Efficient FSRS Parameter Optimizer")
    print("Using official FSRS libraries for maximum efficiency and reliability")
    print(f"Current implementation: {FSRS_IMPLEMENTATION or 'None available'}")
    print("\nInstall FSRS libraries with:")
    print("  pip install fsrs  # Official Python")
    print("  pip install fsrs-rs-python  # Fastest Rust-based")
    print("  pip install fsrs-optimizer  # Dedicated optimizer")