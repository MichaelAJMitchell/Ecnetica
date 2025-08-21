#!/usr/bin/env python3
"""
Mathematical Concept Scraper with Meta-Prompting

This script extracts mathematical concepts and relationships from various document formats
using AI-powered extraction with continuous quality assessment and prompt refinement.
"""

import os
import sys
import argparse
import json
from concept_scraper import ConceptScraper

def main():
    """Main function for the concept scraper."""
    parser = argparse.ArgumentParser(
        description='Extract mathematical concepts and relationships from documents using AI with meta-prompting.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --file ../ontology_source_materials/textbook.md
  python main.py --input-folder ../ontology_source_materials/
  python main.py --files ../ontology_source_materials/*.md ../ontology_source_materials/*.pdf
  python main.py --stats
  python main.py --quality-report
  python main.py --prompt-analysis
  python main.py --dashboard
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Process a single file'
    )
    
    parser.add_argument(
        '--directory', '-d',
        type=str,
        help='Process all supported files in a specific directory'
    )
    
    parser.add_argument(
        '--input-folder', '-i',
        type=str,
        default='../ontology_source_materials/',
        help='Process all supported files in an input folder (default: ../ontology_source_materials/)'
    )
    
    parser.add_argument(
        '--files', '-F',
        nargs='+',
        type=str,
        help='Process multiple specific files'
    )
    
    parser.add_argument(
        '--stats', '-s',
        action='store_true',
        help='Show current knowledge graph statistics'
    )
    
    parser.add_argument(
        '--quality-report', '-q',
        action='store_true',
        help='Generate quality assessment report for recent extractions'
    )
    
    parser.add_argument(
        '--prompt-analysis', '-p',
        action='store_true',
        help='Analyze prompt performance and refinement history'
    )
    
    parser.add_argument(
        '--dashboard', '-D',
        action='store_true',
        help='Launch interactive meta-prompting dashboard'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='../',
        help='Output directory for CSV files (default: ../ - Ontology directory)'
    )
    
    parser.add_argument(
        '--save-quality-metrics',
        type=str,
        help='Save quality metrics to specified file'
    )
    
    parser.add_argument(
        '--save-prompt-performance',
        type=str,
        help='Save prompt performance data to specified file'
    )
    
    args = parser.parse_args()
    
    # Check if any action is specified
    if not any([args.file, args.directory, args.input_folder, args.files, args.stats, 
                args.quality_report, args.prompt_analysis, args.dashboard]):
        parser.print_help()
        sys.exit(1)
    
    try:
        # Initialize the scraper
        print("Initializing Mathematical Concept Scraper with Meta-Prompting...")
        scraper = ConceptScraper()
        
        # Show statistics if requested
        if args.stats:
            scraper.print_statistics()
            return
        
        # Generate quality report if requested
        if args.quality_report:
            print("\n📊 Generating Quality Assessment Report...")
            quality_summary = scraper.get_session_quality_summary()
            print(json.dumps(quality_summary, indent=2))
            return
        
        # Analyze prompt performance if requested
        if args.prompt_analysis:
            print("\n🤖 Analyzing Prompt Performance...")
            # This would require access to the prompt manager
            print("Prompt analysis functionality requires running extractions first.")
            return
        
        # Launch dashboard if requested
        if args.dashboard:
            print("\n🚀 Launching Meta-Prompting Dashboard...")
            from meta_prompting_dashboard import MetaPromptingDashboard
            dashboard = MetaPromptingDashboard()
            dashboard.run_interactive_dashboard()
            return
        
        results = []
        
        # Process single file
        if args.file:
            print(f"Processing single file: {args.file}")
            result = scraper.process_single_file(args.file)
            results.append(result)
        
        # Process directory
        elif args.directory:
            print(f"Processing directory: {args.directory}")
            results = scraper.process_directory(args.directory)
        
        # Process input folder
        elif args.input_folder:
            print(f"Processing input folder: {args.input_folder}")
            results = scraper.process_directory(args.input_folder)
        
        # Process multiple files
        elif args.files:
            print(f"Processing {len(args.files)} files")
            results = scraper.process_files(args.files)
        
        # Print summary
        if results:
            print(f"\n{'='*60}")
            print("PROCESSING SUMMARY")
            print(f"{'='*60}")
            
            successful = 0
            total_concepts = 0
            total_relationships = 0
            
            for result in results:
                if result['success']:
                    successful += 1
                    total_concepts += result['concepts_added']
                    total_relationships += result['relationships_added']
                    print(f"✓ {os.path.basename(result['file'])}: "
                          f"{result['concepts_added']} concepts, "
                          f"{result['relationships_added']} relationships")
                    
                    # Show quality summary if available
                    if 'quality_summary' in result:
                        quality = result['quality_summary']
                        if 'quality_scores' in quality and 'overall_quality' in quality['quality_scores']:
                            avg_score = quality['quality_scores']['overall_quality']['average']
                            print(f"  Quality Score: {avg_score:.2f}/10")
                    
                else:
                    print(f"✗ {os.path.basename(result['file'])}: {result['error']}")
            
            print(f"\nSuccessfully processed: {successful}/{len(results)} files")
            print(f"Total new concepts: {total_concepts}")
            print(f"Total new relationships: {total_relationships}")
            
            # Show final statistics
            scraper.print_statistics()
            
            # Show quality summary for the session
            print(f"\n{'='*60}")
            print("QUALITY ASSESSMENT SUMMARY")
            print(f"{'='*60}")
            session_quality = scraper.get_session_quality_summary()
            if 'message' not in session_quality:
                print(f"Total quality assessments: {session_quality.get('total_assessments', 0)}")
                if 'average_scores' in session_quality:
                    print("\nAverage Quality Scores:")
                    for metric, scores in session_quality['average_scores'].items():
                        metric_name = metric.replace('_', ' ').title()
                        print(f"  {metric_name}: {scores['mean']:.2f}/10")
            
            # Save quality metrics if requested
            if args.save_quality_metrics:
                scraper.save_quality_metrics(args.save_quality_metrics)
                print(f"\n✅ Quality metrics saved to {args.save_quality_metrics}")
            
            # Save prompt performance if requested
            if args.save_prompt_performance:
                scraper.save_prompt_performance(args.save_prompt_performance)
                print(f"✅ Prompt performance data saved to {args.save_prompt_performance}")
        
    except KeyboardInterrupt:
        print("\n\nProcess interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 