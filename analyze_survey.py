#!/usr/bin/env python3
"""
Main script to analyze Ukrainian Education Survey data.

Usage:
    python analyze_survey.py
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pipeline import SurveyAnalysisPipeline


def main():
    """Run complete survey analysis."""
    print("=" * 80)
    print("UKRAINIAN EDUCATION SURVEY - COMPREHENSIVE ANALYSIS")
    print("Data: Parents' Assessment of Digital Education Environments")
    print("Period: October 7-18, 2024 (Wartime Conditions)")
    print("Sample: 5,224 responses from 25 regions of Ukraine")
    print("=" * 80)
    print()

    # Initialize pipeline
    pipeline = SurveyAnalysisPipeline(config_path='config/config.yaml')

    # Load data
    print("Loading data...")
    data_path = 'data/raw/answers.csv'
    pipeline.load_data(data_path)

    print(f"✓ Data loaded: {len(pipeline.df)} responses\n")

    # Get data summary
    summary = pipeline.get_summary()
    print("DATA SUMMARY:")
    print(f"  Total Rows: {summary['total_rows']}")
    print(f"  Total Columns: {summary['total_columns']}")
    print(f"  Memory Usage: {summary['memory_usage_mb']:.2f} MB")
    print(f"  Duplicates: {summary['duplicates']}")
    print()

    # Run complete analysis
    print("Running comprehensive analysis (this may take a few minutes)...")
    results = pipeline.run_analysis()

    print("\nKEY FINDINGS:")
    print(f"  Quality Grade: {results['validation']['summary']['quality_grade']}")
    print(f"  Overall Quality Score: {results['validation']['summary']['overall_score']:.2f}/100")
    print(f"  Data Completeness: {results['validation']['summary']['completeness']:.2f}%")
    print(f"  Accuracy Rate: {results['validation']['summary']['accuracy_rate']:.2f}%")
    print()

    # Generate reports
    print("Generating reports...")
    output_dir = Path('reports')
    output_dir.mkdir(exist_ok=True)

    pipeline.generate_reports(output_dir, formats=['excel'])

    print(f"\n✓ Reports generated in: {output_dir}/")
    print("  - analysis_results.xlsx")
    print("  - summary.txt")
    print()

    # Export processed data
    print("Exporting processed data...")
    pipeline.export_data('data/processed/survey_data_processed.csv')
    print("✓ Processed data exported to: data/processed/survey_data_processed.csv")
    print()

    print("=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print()
    print("Next steps:")
    print("  1. Review reports in the 'reports/' directory")
    print("  2. Examine analysis_results.xlsx for detailed statistics")
    print("  3. Check summary.txt for key findings")
    print()


if __name__ == '__main__':
    main()
