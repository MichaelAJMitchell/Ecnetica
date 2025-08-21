#!/usr/bin/env python3
"""
Meta-Prompting Dashboard for Knowledge Graph Extraction System

This dashboard provides insights into:
- Quality assessment results
- Prompt performance tracking
- Prompt refinement history
- System improvement trends
"""

import json
import os
import pandas as pd
from datetime import datetime
from typing import Dict, List, Any
from quality_assessor import QualityAssessor
from adaptive_prompt_manager import AdaptivePromptManager
from prompt_refiner import PromptRefiner

class MetaPromptingDashboard:
    """Dashboard for monitoring and analyzing meta-prompting system performance."""
    
    def __init__(self, quality_metrics_file: str = None, prompt_registry_file: str = None):
        """Initialize the dashboard with data files."""
        self.quality_assessor = QualityAssessor()
        self.prompt_refiner = PromptRefiner()
        self.prompt_manager = AdaptivePromptManager(self.quality_assessor, self.prompt_refiner)
        
        # Load existing data if available
        if quality_metrics_file and os.path.exists(quality_metrics_file):
            self.quality_assessor.load_quality_metrics(quality_metrics_file)
        
        if prompt_registry_file and os.path.exists(prompt_registry_file):
            self.prompt_manager.load_prompt_registry(prompt_registry_file)
    
    def display_overall_summary(self):
        """Display overall system performance summary."""
        print("=" * 80)
        print("META-PROMPTING SYSTEM PERFORMANCE DASHBOARD")
        print("=" * 80)
        print()
        
        # Quality Assessment Summary
        quality_summary = self.quality_assessor.get_quality_summary()
        print("📊 QUALITY ASSESSMENT OVERVIEW")
        print("-" * 40)
        
        if 'message' in quality_summary:
            print(f"Status: {quality_summary['message']}")
        else:
            print(f"Total Assessments: {quality_summary.get('total_assessments', 0)}")
            
            if 'average_scores' in quality_summary:
                print("\nAverage Quality Scores:")
                for metric, scores in quality_summary['average_scores'].items():
                    metric_name = metric.replace('_', ' ').title()
                    print(f"  {metric_name}: {scores['mean']:.2f}/10 (min: {scores['min']}, max: {scores['max']})")
        
        print()
        
        # Prompt Performance Summary
        prompt_summary = self.prompt_manager.get_performance_summary()
        print("🤖 PROMPT PERFORMANCE OVERVIEW")
        print("-" * 40)
        print(f"Total Prompt Types: {prompt_summary.get('total_prompts', 0)}")
        
        if 'prompt_performance' in prompt_summary:
            for prompt_type, performance in prompt_summary['prompt_performance'].items():
                if 'message' not in performance:
                    print(f"\n  {prompt_type.replace('_', ' ').title()}:")
                    print(f"    Total Extractions: {performance.get('total_extractions', 0)}")
                    print(f"    Current Score: {performance.get('current_score', 0):.2f}/10")
                    print(f"    Best Score: {performance.get('best_score', 0):.2f}/10")
                    print(f"    Average Score: {performance.get('average_score', 0):.2f}/10")
                    print(f"    Trend: {performance.get('score_trend', 'unknown')}")
                    print(f"    Total Versions: {performance.get('total_versions', 0)}")
        
        print()
    
    def display_quality_trends(self, days: int = 30):
        """Display quality trends over time."""
        print("📈 QUALITY TRENDS OVER TIME")
        print("-" * 40)
        
        if not self.quality_assessor.quality_metrics:
            print("No quality metrics available for trend analysis.")
            return
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(self.quality_assessor.quality_metrics)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Filter by date range
        cutoff_date = datetime.now() - pd.Timedelta(days=days)
        recent_df = df[df['timestamp'] > cutoff_date]
        
        if recent_df.empty:
            print(f"No quality metrics found in the last {days} days.")
            return
        
        print(f"Analyzing trends for the last {days} days...")
        print(f"Total assessments in period: {len(recent_df)}")
        
        # Calculate trends for each metric
        metrics = ['concept_granularity', 'concept_completeness', 'relationship_accuracy', 
                  'relationship_completeness', 'overall_quality']
        
        for metric in metrics:
            scores = []
            for record in recent_df[metric]:
                if isinstance(record, dict) and 'score' in record:
                    scores.append(record['score'])
            
            if scores:
                # Simple trend calculation
                first_half = scores[:len(scores)//2] if len(scores) >= 2 else scores
                second_half = scores[len(scores)//2:] if len(scores) >= 2 else scores
                
                if first_half and second_half:
                    first_avg = sum(first_half) / len(first_half)
                    second_avg = sum(second_half) / len(second_half)
                    change = second_avg - first_avg
                    
                    trend_symbol = "↗️" if change > 0.1 else "↘️" if change < -0.1 else "→"
                    trend_desc = "improving" if change > 0.1 else "declining" if change < -0.1 else "stable"
                    
                    metric_name = metric.replace('_', ' ').title()
                    print(f"  {metric_name}: {trend_symbol} {trend_desc} (change: {change:+.2f})")
        
        print()
    
    def display_prompt_refinement_history(self, prompt_type: str = None):
        """Display history of prompt refinements."""
        print("🔄 PROMPT REFINEMENT HISTORY")
        print("-" * 40)
        
        if prompt_type:
            prompt_types = [prompt_type]
        else:
            prompt_types = ['stage1_broad_concept', 'stage2_granular_concept', 
                          'stage3_cross_reference', 'relationship_extraction']
        
        for pt in prompt_types:
            print(f"\n{pt.replace('_', ' ').title()}:")
            
            # Get refinement history from prompt refiner
            history = self.prompt_refiner.get_prompt_performance_history(pt)
            
            if not history:
                print("  No refinements recorded yet.")
                continue
            
            print(f"  Total refinements: {len(history)}")
            
            # Show recent refinements
            for i, refinement in enumerate(history[-3:]):  # Last 3 refinements
                timestamp = refinement.get('timestamp', 'Unknown')
                overall_score = refinement.get('overall_score', 0)
                print(f"    {i+1}. {timestamp[:10]} - Score: {overall_score:.2f}/10")
        
        print()
    
    def display_improvement_suggestions(self):
        """Display recent improvement suggestions from quality assessments."""
        print("💡 RECENT IMPROVEMENT SUGGESTIONS")
        print("-" * 40)
        
        if not self.quality_assessor.quality_metrics:
            print("No quality metrics available for improvement suggestions.")
            return
        
        # Get recent assessments
        recent_metrics = self.quality_assessor.quality_metrics[-10:]  # Last 10 assessments
        
        suggestions = []
        for metric in recent_metrics:
            if 'improvement_suggestions' in metric:
                for suggestion in metric['improvement_suggestions']:
                    suggestions.append({
                        'suggestion': suggestion,
                        'source_file': metric.get('source_file', 'Unknown'),
                        'timestamp': metric.get('timestamp', 'Unknown')
                    })
        
        if not suggestions:
            print("No improvement suggestions found in recent assessments.")
            return
        
        print(f"Found {len(suggestions)} recent improvement suggestions:")
        
        # Group by suggestion type
        suggestion_counts = {}
        for suggestion in suggestions:
            key = suggestion['suggestion'][:50] + "..." if len(suggestion['suggestion']) > 50 else suggestion['suggestion']
            suggestion_counts[key] = suggestion_counts.get(key, 0) + 1
        
        # Display most common suggestions
        for suggestion, count in sorted(suggestion_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {suggestion} (mentioned {count} times)")
        
        print()
    
    def export_performance_report(self, output_file: str):
        """Export a comprehensive performance report to JSON."""
        print(f"📋 Exporting performance report to {output_file}...")
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'quality_summary': self.quality_assessor.get_quality_summary(),
            'prompt_performance': self.prompt_manager.get_performance_summary(),
            'recent_quality_metrics': self.quality_assessor.quality_metrics[-50:],  # Last 50 metrics
            'prompt_refinement_history': self.prompt_refiner.prompt_versions
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"✅ Performance report exported to {output_file}")
    
    def run_interactive_dashboard(self):
        """Run an interactive dashboard session."""
        while True:
            print("\n" + "=" * 60)
            print("META-PROMPTING DASHBOARD MENU")
            print("=" * 60)
            print("1. Overall Summary")
            print("2. Quality Trends (Last 30 days)")
            print("3. Prompt Refinement History")
            print("4. Improvement Suggestions")
            print("5. Export Performance Report")
            print("6. Exit")
            print("-" * 60)
            
            choice = input("Select an option (1-6): ").strip()
            
            if choice == '1':
                self.display_overall_summary()
            elif choice == '2':
                self.display_quality_trends()
            elif choice == '3':
                self.display_prompt_refinement_history()
            elif choice == '4':
                self.display_improvement_suggestions()
            elif choice == '5':
                output_file = input("Enter output filename (e.g., performance_report.json): ").strip()
                if output_file:
                    self.export_performance_report(output_file)
            elif choice == '6':
                print("Exiting dashboard...")
                break
            else:
                print("Invalid choice. Please select 1-6.")
            
            input("\nPress Enter to continue...")

def main():
    """Main function to run the dashboard."""
    # Default file paths
    quality_file = "quality_metrics.json"
    prompt_file = "prompt_registry.json"
    
    # Check if files exist in current directory
    if not os.path.exists(quality_file):
        quality_file = None
    if not os.path.exists(prompt_file):
        prompt_file = None
    
    dashboard = MetaPromptingDashboard(quality_file, prompt_file)
    
    if quality_file is None and prompt_file is None:
        print("⚠️  No existing data files found. Dashboard will start with empty data.")
        print("   Run the concept scraper first to generate quality metrics and prompt data.")
        print()
    
    dashboard.run_interactive_dashboard()

if __name__ == "__main__":
    main() 