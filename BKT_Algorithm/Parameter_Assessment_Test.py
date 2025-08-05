"""
Simple test for parameter assessment using existing BKT system
"""

import random
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sklearn.mixture import GaussianMixture
from scipy.optimize import minimize

import sys
sys.path.append('./')


# Fix the pyBKT bug before importing
import random

# Monkey patch random.randint to handle the float issue in pyBKT
original_randint = random.randint
def patched_randint(a, b):
    # Convert floats to ints for pyBKT compatibility
    return original_randint(int(a), int(b))

# Apply the patch
random.randint = patched_randint

# Now import pyBKT
from pyBKT.models import Model

# Restore original function after import
random.randint = original_randint

PYBKT_AVAILABLE = True
print("pyBKT imported successfully (bug fixed)")



try:
    from _static.mcq_algorithm_current import (
        KnowledgeGraph, StudentManager, BayesianKnowledgeTracing, 
        MCQScheduler
    )
    SYSTEM_AVAILABLE = True
except ImportError:
    print("Could not import BKT system.")
    SYSTEM_AVAILABLE = False
'''
try:
    from pyBKT.models import Model
    PYBKT_AVAILABLE = True
except ImportError:
    print("pyBKT not installed")
    PYBKT_AVAILABLE = False
'''
def create_realistic_student(student_manager, student_id: str, kg) -> None:
    """Create student with realistic initial mastery distribution"""
    student = student_manager.create_student(student_id)
    
    # Set realistic mastery levels - some topics known, others not
    random.seed(hash(student_id) % 1000)  # Consistent per student
    
# Get topics that actually have MCQs
    topics_with_mcqs = set()
    if hasattr(kg, 'ultra_loader'):
        for mcq_data in kg.ultra_loader.minimal_mcq_data.values():
            topics_with_mcqs.add(mcq_data.main_topic_index)
    
    print(f"Topics with MCQs: {len(topics_with_mcqs)}")
    
    for topic_idx in kg.get_all_indexes():
        if topic_idx in topics_with_mcqs:
            # Only mark topics with MCQs as studied with low mastery
            mastery = random.uniform(0.1, 0.4)  # Low mastery = eligible
            student.studied_topics[topic_idx] = True
        else:
            # High mastery for topics without MCQs (so they're not "due")
            mastery = 0.8
            student.studied_topics[topic_idx] = False
            
        student.mastery_levels[topic_idx] = mastery


def simulate_learning_sessions(kg, student_manager, mcq_scheduler, bkt_system, 
                             student_id: str, num_sessions: int = 10) -> list:
    """Generate realistic learning data using  existing system"""
    #print(f"Simulating {num_sessions} learning sessions for {student_id}")
    
    # Use  optimized preloading
    kg.preload_for_student(student_id, student_manager)
    
    all_attempts = []
    
    # TEMPORARY: Direct MCQ selection for testing parameter fitting
    for session in range(num_sessions):
        if hasattr(kg, 'ultra_loader'):
            available_mcqs = list(kg.ultra_loader.minimal_mcq_data.keys())
            # Repeat first 5 MCQs instead of random sampling
            selected_mcqs = available_mcqs[:5]  # Always same 5 MCQs
        else:
            selected_mcqs = []


        #Below is the original code that uses the algorithm properly
        ''' 
        if hasattr(kg, 'ultra_loader'):
            available_mcqs = list(kg.ultra_loader.minimal_mcq_data.keys())
            selected_mcqs = random.sample(available_mcqs, min(10, len(available_mcqs)))
        else:
            selected_mcqs = []
        
        if not selected_mcqs:
            print(f"No questions available for session {session + 1}")
            continue
        '''

        '''
    for session in range(num_sessions):

        # Use algorithm to select questions
        selected_mcqs = mcq_scheduler.select_optimal_mcqs(student_id, num_questions=5)
        
        if not selected_mcqs:
            print(f"No questions available for session {session + 1}")
            continue
            
    #print(f"Session {session + 1}: {len(selected_mcqs)} questions")
        '''
        for mcq_id in selected_mcqs:
            

            # Get current mastery for realistic response simulation
            if hasattr(kg, 'ultra_loader'):
                minimal_data = kg.ultra_loader.get_minimal_mcq_data(mcq_id)
                main_topic = minimal_data.main_topic_index if minimal_data else 0
            else:
                mcq = kg.mcqs.get(mcq_id)
                main_topic = mcq.main_topic_index if mcq else 0

            student = student_manager.get_student(student_id)
            #student.daily_completed.add(mcq_id)
            current_mastery = student.get_mastery(main_topic)
            
            # Simple realistic ai response: higher mastery = higher success chance
            # we cant use the one from the BKT alg. because then we're just using the parameters directly

            success_prob = 0.15 + (current_mastery * 0.7)  # 15-85% range
            is_correct = random.random() < success_prob
            time_taken = random.uniform(20, 90)
            
            # record the attempt (includes BKT updates)

            
            bkt_updates = student_manager.record_attempt(
                student_id, mcq_id, is_correct, time_taken, kg
            )
            
            # Store for parameter fitting test
            all_attempts.append({
                'mcq_id': mcq_id,
                'topic_index': main_topic,
                'is_correct': is_correct,
                'timestamp': datetime.now() - timedelta(hours=session, minutes=random.randint(0, 59))
            })
    
    #print(f"Generated {len(all_attempts)} attempts across {num_sessions} sessions")
    return all_attempts

#Debug code for pyBKT system which ended up not working
#Later, if we can get this to function it might be worth considering
''' 
def test_parameter_fitting(kg, attempts: list, student_id: str) -> dict:
    """Test Parameter_Assessment.py code with the generated data"""
    if not PYBKT_AVAILABLE:
        return {'error': 'pyBKT not available'}
    
    print(f"DEBUG: Total attempts received: {len(attempts)}")
    
    # Convert to pyBKT format (from Parameter_Assessment.py)
    student_data = []
    for i, attempt in enumerate(attempts):
        topic_name = kg.get_topic_of_index(attempt['topic_index'])
        print(f"DEBUG: Attempt {i}: topic_index={attempt['topic_index']}, topic_name={topic_name}")
        if topic_name:
            student_data.append({
                'user_id': student_id,
                'skill_name': topic_name,
                'correct': 1 if attempt['is_correct'] else 0,
                'order_id': i
            })
    
    print(f"DEBUG: student_data length: {len(student_data)}")
    
    df = pd.DataFrame(student_data)
    skills = df['skill_name'].unique()
    
    print(f"DEBUG: {len(skills)} unique topics: {list(skills)}")
    
    # Apply fitting logic
    fitted_params = {}
    model = Model(seed=42, num_fits=10)
    
    for skill in skills:
        skill_data = df[df['skill_name'] == skill]
        print(f"DEBUG: {skill} has {len(skill_data)} attempts")
        if len(skill_data) < 3:  # minimum data
            print(f"DEBUG: Skipping {skill} - not enough data")
            continue
        
        print(f"DEBUG: Attempting to fit {skill}")
        try:
            model.fit(data=skill_data, skills=[skill])
            params = model.params()[skill]
            print(f"DEBUG: Successfully fitted {skill}")
            
            fitted_params[skill] = {
                'prior': params['prior'],
                'learn': params['learns'][0] if params['learns'] else 0.3,
                'guess': params['guesses'][0] if params['guesses'] else 0.1,
                'slip': params['slips'][0] if params['slips'] else 0.1,
                'attempts': len(skill_data)
            }
            
        except Exception as e:
            print(f"DEBUG: Failed to fit {skill}: {e}")
    
    return fitted_params
'''


def bkt_likelihood(params, responses):
    """
    Calculate likelihood of observing response sequence given BKT parameters
    """
    p_l0, p_t, p_g, p_s = params
    
    # Ensure parameters are in valid range
    if not (0 <= p_l0 <= 1 and 0 <= p_t <= 1 and 0 <= p_g <= 1 and 0 <= p_s <= 1):
        return -np.inf
    
    current_mastery = p_l0
    log_likelihood = 0
    
    for response in responses:
        # P(Correct) = P(L)(1-P(S)) + (1-P(L))P(G)
        p_correct = current_mastery * (1 - p_s) + (1 - current_mastery) * p_g
        p_correct = max(1e-10, min(1-1e-10, p_correct))  # Avoid log(0)
        
        # Add to likelihood
        if response == 1:  # Correct
            log_likelihood += np.log(p_correct)
        else:  # Incorrect
            log_likelihood += np.log(1 - p_correct)
        
        # Update mastery using BKT
        if response == 1:  # Correct response
            numerator = current_mastery * (1 - p_s)
            denominator = current_mastery * (1 - p_s) + (1 - current_mastery) * p_g
        else:  # Incorrect response
            numerator = current_mastery * p_s
            denominator = current_mastery * p_s + (1 - current_mastery) * (1 - p_g)
        
        if denominator > 0:
            conditional_prob = numerator / denominator
        else:
            conditional_prob = current_mastery
            
        # P(L_{t+1}) = P(L_t|evidence) + (1-P(L_t|evidence))P(T)
        current_mastery = conditional_prob + (1 - conditional_prob) * p_t
        current_mastery = max(0, min(1, current_mastery))
    
    return log_likelihood

def fit_bkt_parameters_sklearn(responses, num_restarts=10):
    """
    Fit BKT parameters using scipy optimization (more reliable than pyBKT)
    """
    responses = np.array(responses)
    
    def negative_likelihood(params):
        return -bkt_likelihood(params, responses)
    
    best_params = None
    best_likelihood = -np.inf
    
    # Multiple random restarts to avoid local minima
    for _ in range(num_restarts):
        # Random initial parameters
        initial_params = [
            np.random.uniform(0.01, 0.5),  # p_l0 (prior)
            np.random.uniform(0.1, 0.6),   # p_t (learn)
            np.random.uniform(0.01, 0.3),  # p_g (guess)
            np.random.uniform(0.01, 0.2)   # p_s (slip)
        ]
        
        # Constraints: all parameters between 0 and 1
        bounds = [(0.1, 0.9)] * 4
        
        try:
            result = minimize(
                negative_likelihood,
                initial_params,
                method='L-BFGS-B',
                bounds=bounds
            )
            
            if result.success and result.fun < -best_likelihood:
                best_likelihood = -result.fun
                best_params = result.x
                
        except Exception as e:
            continue
    
    if best_params is not None:
        return {
            'prior': float(best_params[0]),
            'learns': [float(best_params[1])],
            'guesses': [float(best_params[2])],
            'slips': [float(best_params[3])],
            'likelihood': float(best_likelihood)
        }
    else:
        return None

def test_parameter_fitting(kg, attempts: list, student_id: str) -> dict:
    """
    Test BKT parameter fitting using scikit-learn optimization
    """
    print(f"Testing sklearn-based BKT fitting with {len(attempts)} attempts")
    
    # Convert to simple format
    student_data = []
    for i, attempt in enumerate(attempts):
        student_data.append({
            'user_id': student_id,
            'skill_name': f"topic_{attempt['topic_index']}",
            'correct': 1 if attempt['is_correct'] else 0,
            'order_id': i
        })
    
    df = pd.DataFrame(student_data)
    skills = df['skill_name'].unique()
    print(f"📊 {len(skills)} unique topics: {list(skills)}")
    
    fitted_params = {}
    
    for skill in skills:
        skill_data = df[df['skill_name'] == skill]
        responses = skill_data['correct'].values

         # DEBUG INFO:
        print(f"{skill}: {len(responses)} attempts")
        print(f"   Response pattern: {responses}")
        print(f"   Success rate: {np.mean(responses):.1%}")
        
        if len(responses) < 3:
            print(f"   Skipping - need at least 3 attempts")
            continue
        
        print(f"{skill}: {len(responses)} attempts")
        
        if len(responses) < 3:
            print(f"   Skipping - need at least 3 attempts")
            continue
        
        print(f"   🔄 Fitting parameters...")
        
        # Use our sklearn-based fitting
        params = fit_bkt_parameters_sklearn(responses, num_restarts=15)
        
        if params:
            fitted_params[skill] = {
                'prior': params['prior'],
                'learn': params['learns'][0],
                'guess': params['guesses'][0],
                'slip': params['slips'][0],
                'likelihood': params['likelihood'],
                'attempts': len(responses)
            }
            print(f"   Success! P(L0)={params['prior']:.3f}, P(T)={params['learns'][0]:.3f}")
        else:
            print(f"    Failed to converge")
    
    return fitted_params





def run_parameter_test():
    """Main test function"""
    if not SYSTEM_AVAILABLE:
        print("BKT system not available")
        return
    
    #print("Parameter Assessment Test")
    print("=" * 40)
    
    # Initialize system properly (from BKT demo pattern)
    kg = KnowledgeGraph(
        nodes_file='_static/small-graph-kg.json',
        mcqs_file='_static/small-graph-computed_mcqs.json',
        config_file='_static/config.json'
    )
    
    student_manager = StudentManager(kg.config)
    mcq_scheduler = MCQScheduler(kg, student_manager)
    bkt_system = BayesianKnowledgeTracing(kg, student_manager)
    
    # Connect systems (this was missing in my original!)
    mcq_scheduler.set_bkt_system(bkt_system)
    student_manager.set_bkt_system(bkt_system)
    
    print("System initialized")
    
    # Test with multiple students to see parameter differences
    results = {}
    for i in range(3):
        student_id = f"param_test_student_{i}"
        
        # Create realistic student
        create_realistic_student(student_manager, student_id, kg)
        
        # Generate learning data using algorithms
        attempts = simulate_learning_sessions(
            kg, student_manager, mcq_scheduler, bkt_system, 
            student_id, num_sessions=10
        )

        # Test parameter fitting
        if attempts:
            fitted_params = test_parameter_fitting(kg, attempts, student_id)
            results[student_id] = fitted_params
            
            print(f"\n{student_id}: {len(fitted_params)} topics fitted")
            for topic, params in list(fitted_params.items())[:3]:  # Show first 3
                print(f"  {topic}: P(L0)={params['prior']:.3f}, P(T)={params['learn']:.3f}")
    # Quick summary line
    print(f"\n FITTED PARAMETERS SUMMARY: " + " | ".join([f"{student_id}: {len(params)} topics" for student_id, params in results.items()]))
    print(f"\n Test complete! Parameter fitting tested on {len(results)} students")

    #  MINIMAL TEST AT THE END:
    print("Testing pyBKT with minimal data...")

    return results

if __name__ == "__main__":
    run_parameter_test()