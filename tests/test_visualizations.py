#!/usr/bin/env python3
"""
Test Suite for Visualization Modules
Tests visualization generation without requiring external dependencies
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_visualization_files_exist():
    """Test that visualization PDFs were generated."""

    q22_viz_dir = Path('reports/visualizations')
    all_q_viz_dir = Path('reports/visualizations/all_questions')

    # Check Q22 visualizations
    q22_files = [
        'response_types.pdf',
        'sentiment_distribution.pdf',
        'theme_distribution.pdf',
        'top_words.pdf',
        'top_bigrams.pdf',
        'wordcloud.pdf',
        'text_length_distribution.pdf',
        'regional_distribution.pdf',
        'theme_network.pdf',
        'priority_matrix.pdf',
        'wartime_context.pdf',
        'communication_themes.pdf',
        'infrastructure_needs.pdf',
        'dashboard_summary.pdf'
    ]

    print("\n" + "=" * 80)
    print("TEST: Q22 Visualization Files")
    print("=" * 80)

    q22_found = 0
    for filename in q22_files:
        filepath = q22_viz_dir / filename
        exists = filepath.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {filename}")
        if exists:
            q22_found += 1

    print(f"\nQ22 Visualizations: {q22_found}/{len(q22_files)} found")

    # Check comprehensive survey visualizations
    all_q_count = len(list(all_q_viz_dir.glob('*.pdf'))) if all_q_viz_dir.exists() else 0

    print("\n" + "=" * 80)
    print("TEST: Comprehensive Survey Visualizations")
    print("=" * 80)
    print(f"  Total PDF files found: {all_q_count}")

    expected_files = [
        'q1_age_distribution.pdf',
        'q2_gender_distribution.pdf',
        'q4_regional_distribution.pdf',
        'q16_communication_channels.pdf',
        'complete_survey_dashboard.pdf'
    ]

    for filename in expected_files:
        filepath = all_q_viz_dir / filename
        exists = filepath.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {filename}")

    # Overall assessment
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    total_found = q22_found + all_q_count
    total_expected = len(q22_files) + 20  # Approximate

    if total_found >= 30:
        print(f"  ✓ PASS: {total_found} visualizations generated (>= 30 expected)")
        return True
    else:
        print(f"  ✗ FAIL: Only {total_found} visualizations generated (< 30 expected)")
        return False


def test_latex_report_exists():
    """Test that LaTeX report file exists."""

    print("\n" + "=" * 80)
    print("TEST: LaTeX Report File")
    print("=" * 80)

    latex_file = Path('reports/latex_report/main.tex')

    if latex_file.exists():
        file_size = latex_file.stat().st_size
        line_count = len(latex_file.read_text(encoding='utf-8').splitlines())

        print(f"  ✓ LaTeX report exists: {latex_file}")
        print(f"  File size: {file_size:,} bytes")
        print(f"  Line count: {line_count:,} lines")

        if line_count > 500:
            print(f"  ✓ PASS: LaTeX report is comprehensive ({line_count} lines)")
            return True
        else:
            print(f"  ✗ FAIL: LaTeX report is too short ({line_count} lines < 500)")
            return False
    else:
        print(f"  ✗ FAIL: LaTeX report not found at {latex_file}")
        return False


def test_strategic_insights_exist():
    """Test that strategic insights reports exist."""

    print("\n" + "=" * 80)
    print("TEST: Strategic Insights Reports")
    print("=" * 80)

    files_to_check = [
        'reports/strategic_insights/q22_strategic_insights.txt',
        'reports/strategic_insights/q22_policy_brief.txt',
        'reports/strategic_insights/q22_data_export.json',
        'reports/text_analysis/q22_comprehensive_analysis.txt',
        'reports/text_analysis/q22_detailed_analysis.xlsx'
    ]

    found_count = 0
    for filepath_str in files_to_check:
        filepath = Path(filepath_str)
        exists = filepath.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {filepath}")
        if exists:
            found_count += 1

    if found_count == len(files_to_check):
        print(f"\n  ✓ PASS: All {found_count} strategic insight files found")
        return True
    else:
        print(f"\n  ✗ FAIL: Only {found_count}/{len(files_to_check)} files found")
        return False


def test_source_code_exists():
    """Test that source code modules exist."""

    print("\n" + "=" * 80)
    print("TEST: Source Code Modules")
    print("=" * 80)

    modules = [
        'enhanced_text_analysis.py',
        'strategic_insights_q22.py',
        'generate_visualizations.py',
        'comprehensive_survey_visualizations.py',
        'run_analysis.py',
        'generate_comprehensive_report.py'
    ]

    found_count = 0
    for module in modules:
        filepath = Path(module)
        exists = filepath.exists()
        status = "✓" if exists else "✗"

        if exists:
            line_count = len(filepath.read_text(encoding='utf-8').splitlines())
            print(f"  {status} {module} ({line_count} lines)")
            found_count += 1
        else:
            print(f"  {status} {module}")

    if found_count == len(modules):
        print(f"\n  ✓ PASS: All {found_count} source modules found")
        return True
    else:
        print(f"\n  ✗ FAIL: Only {found_count}/{len(modules)} modules found")
        return False


def run_all_tests():
    """Run all tests and report results."""

    print("\n" + "=" * 80)
    print("COMPREHENSIVE VISUALIZATION TEST SUITE")
    print("=" * 80)

    tests = [
        ("Visualization Files", test_visualization_files_exist),
        ("LaTeX Report", test_latex_report_exists),
        ("Strategic Insights", test_strategic_insights_exist),
        ("Source Code", test_source_code_exists)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n  ✗ ERROR in {test_name}: {e}")
            results.append((test_name, False))

    # Final summary
    print("\n" + "=" * 80)
    print("FINAL TEST RESULTS")
    print("=" * 80)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {test_name}")

    print()
    print(f"  Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n  ✓✓✓ ALL TESTS PASSED ✓✓✓")
        return 0
    else:
        print(f"\n  ✗✗✗ {total - passed} TEST(S) FAILED ✗✗✗")
        return 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
