#!/usr/bin/env python3
"""
Test script for the meta-prompting system components.

This script tests:
1. Quality assessment functionality
2. Prompt refinement capabilities
3. Adaptive prompt management
4. Dashboard functionality
"""

import os
import json
from quality_assessor import QualityAssessor
from prompt_refiner import PromptRefiner
from adaptive_prompt_manager import AdaptivePromptManager
from meta_prompting_dashboard import MetaPromptingDashboard

def test_quality_assessor():
    """Test the quality assessor functionality."""
    print("🧪 Testing Quality Assessor...")
    
    # Mock data for testing
    mock_concepts = [
        {
            "name": "Quadratic Equation",
            "description": "An equation of the form ax² + bx + c = 0",
            "grade_level": "High School",
            "difficulty": "Intermediate"
        },
        {
            "name": "Discriminant",
            "description": "b² - 4ac, determines nature of roots",
            "grade_level": "High School", 
            "difficulty": "Intermediate"
        }
    ]
    
    mock_relationships = [
        {
            "prerequisite_name": "Quadratic Equation",
            "dependent_name": "Discriminant",
            "relationship_type": "prerequisite",
            "strength": "strong"
        }
    ]
    
    mock_source_chunk = """
    A quadratic equation is an equation of the form ax² + bx + c = 0, where a, b, and c are constants.
    The discriminant, given by b² - 4ac, determines the nature of the roots of the equation.
    """
    
    # Initialize quality assessor
    assessor = QualityAssessor()
    
    # Test quality assessment
    try:
        assessment = assessor.assess_extraction_quality(
            mock_concepts, mock_relationships, mock_source_chunk, "test_file.md"
        )
        
        print("✅ Quality assessment completed successfully")
        print(f"   Overall quality score: {assessment.get('overall_quality', {}).get('score', 'N/A')}/10")
        
        return True
        
    except Exception as e:
        print(f"❌ Quality assessment failed: {e}")
        return False

def test_prompt_refiner():
    """Test the prompt refiner functionality."""
    print("\n🧪 Testing Prompt Refiner...")
    
    # Mock quality feedback
    mock_quality_feedback = {
        "concept_granularity": {"score": 6, "feedback": "Concepts could be more specific"},
        "concept_completeness": {"score": 7, "feedback": "Most concepts captured"},
        "relationship_accuracy": {"score": 8, "feedback": "Relationships are logical"},
        "relationship_completeness": {"score": 5, "feedback": "Missing some key relationships"},
        "overall_quality": {"score": 6.5, "feedback": "Good but room for improvement"},
        "improvement_suggestions": ["Add more specific concept definitions", "Include more relationship types"]
    }
    
    mock_extraction_results = {
        "concepts_count": 2,
        "relationships_count": 1,
        "source_file": "test_file.md"
    }
    
    # Initialize prompt refiner
    refiner = PromptRefiner()
    
    # Test prompt refinement
    try:
        current_prompt = "Extract mathematical concepts from the text."
        refined_prompt = refiner.refine_prompt(
            current_prompt, 
            mock_quality_feedback, 
            mock_extraction_results, 
            "concept_extraction"
        )
        
        print("✅ Prompt refinement completed successfully")
        print(f"   Original prompt length: {len(current_prompt)}")
        print(f"   Refined prompt length: {len(refined_prompt)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Prompt refinement failed: {e}")
        return False

def test_adaptive_prompt_manager():
    """Test the adaptive prompt manager functionality."""
    print("\n🧪 Testing Adaptive Prompt Manager...")
    
    # Initialize components
    assessor = QualityAssessor()
    refiner = PromptRefiner()
    manager = AdaptivePromptManager(assessor, refiner)
    
    # Test prompt registry
    try:
        # Check if prompts are loaded
        stage1_prompt = manager.get_current_prompt('stage1_broad_concept')
        print("✅ Prompt registry initialized successfully")
        print(f"   Stage 1 prompt length: {len(stage1_prompt)}")
        
        # Test performance recording
        mock_quality = {
            "concept_granularity": {"score": 7, "feedback": "Good"},
            "concept_completeness": {"score": 6, "feedback": "Fair"},
            "relationship_accuracy": {"score": 8, "feedback": "Excellent"},
            "relationship_completeness": {"score": 5, "feedback": "Needs improvement"},
            "overall_quality": {"score": 6.5, "feedback": "Good overall"}
        }
        
        mock_metadata = {
            "source_file": "test.md",
            "chunk_number": 1,
            "concepts_count": 3,
            "relationships_count": 2
        }
        
        manager.record_extraction_performance('stage1_broad_concept', mock_quality, mock_metadata)
        print("✅ Performance recording completed successfully")
        
        # Test performance summary
        summary = manager.get_performance_summary('stage1_broad_concept')
        print("✅ Performance summary generated successfully")
        print(f"   Total extractions: {summary.get('total_extractions', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Adaptive prompt manager test failed: {e}")
        return False

def test_dashboard():
    """Test the dashboard functionality."""
    print("\n🧪 Testing Meta-Prompting Dashboard...")
    
    try:
        # Initialize dashboard
        dashboard = MetaPromptingDashboard()
        
        # Test dashboard initialization
        print("✅ Dashboard initialized successfully")
        
        # Test summary generation
        dashboard.display_overall_summary()
        print("✅ Dashboard summary display completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Dashboard test failed: {e}")
        return False

def test_data_persistence():
    """Test data persistence functionality."""
    print("\n🧪 Testing Data Persistence...")
    
    try:
        # Initialize components
        assessor = QualityAssessor()
        refiner = PromptRefiner()
        manager = AdaptivePromptManager(assessor, refiner)
        
        # Add some test data
        test_quality = {
            "concept_granularity": {"score": 8, "feedback": "Test feedback"},
            "concept_completeness": {"score": 7, "feedback": "Test feedback"},
            "relationship_accuracy": {"score": 9, "feedback": "Test feedback"},
            "relationship_completeness": {"score": 6, "feedback": "Test feedback"},
            "overall_quality": {"score": 7.5, "feedback": "Test feedback"}
        }
        
        assessor.quality_metrics.append(test_quality)
        
        # Test saving
        assessor.save_quality_metrics("test_quality_metrics.json")
        manager.save_prompt_registry("test_prompt_registry.json")
        
        print("✅ Data persistence test completed successfully")
        
        # Clean up test files
        if os.path.exists("test_quality_metrics.json"):
            os.remove("test_quality_metrics.json")
        if os.path.exists("test_prompt_registry.json"):
            os.remove("test_prompt_registry.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Data persistence test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Starting Meta-Prompting System Tests...")
    print("=" * 60)
    
    tests = [
        ("Quality Assessor", test_quality_assessor),
        ("Prompt Refiner", test_prompt_refiner),
        ("Adaptive Prompt Manager", test_adaptive_prompt_manager),
        ("Dashboard", test_dashboard),
        ("Data Persistence", test_data_persistence)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"⚠️  {test_name} test had issues")
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Meta-prompting system is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    main() 