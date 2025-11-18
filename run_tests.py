#!/usr/bin/env python3
"""
Simple test runner that works without pytest.
Runs basic tests to verify module functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Test results
passed = 0
failed = 0
skipped = 0


def test_result(name, success, message=""):
    """Record test result."""
    global passed, failed
    if success:
        passed += 1
        print(f"  ✓ {name}")
    else:
        failed += 1
        print(f"  ✗ {name}")
        if message:
            print(f"    {message}")


def test_imports():
    """Test that all modules can be imported."""
    print("\n1. Testing Module Imports...")

    try:
        from models.survey import Survey, Question, QuestionType
        test_result("Import models.survey", True)
    except Exception as e:
        test_result("Import models.survey", False, str(e))

    try:
        from models.response import Response, Answer, ResponseStatus
        test_result("Import models.response", True)
    except Exception as e:
        test_result("Import models.response", False, str(e))

    try:
        from models.quality import DataQualityMetrics, QualityDimension
        test_result("Import models.quality", True)
    except Exception as e:
        test_result("Import models.quality", False, str(e))

    try:
        from models.metadata import SurveyMetadata, RegionalMetadata
        test_result("Import models.metadata", True)
    except Exception as e:
        test_result("Import models.metadata", False, str(e))

    try:
        from ingestion.data_loader import DataLoader
        test_result("Import ingestion.data_loader", True)
    except Exception as e:
        test_result("Import ingestion.data_loader", False, str(e))

    try:
        from validation.validator import DataValidator
        test_result("Import validation.validator", True)
    except Exception as e:
        test_result("Import validation.validator", False, str(e))

    try:
        from analysis.descriptive_stats import DescriptiveAnalyzer
        test_result("Import analysis.descriptive_stats", True)
    except Exception as e:
        test_result("Import analysis.descriptive_stats", False, str(e))

    try:
        from analysis.text_analysis import UkrainianTextAnalyzer
        test_result("Import analysis.text_analysis", True)
    except Exception as e:
        test_result("Import analysis.text_analysis", False, str(e))

    try:
        from pipeline import SurveyAnalysisPipeline
        test_result("Import pipeline", True)
    except Exception as e:
        test_result("Import pipeline", False, str(e))


def test_data_models():
    """Test data models."""
    print("\n2. Testing Data Models...")

    try:
        from datetime import datetime
        from models.survey import Survey, Question, QuestionType

        # Test Survey creation
        survey = Survey(
            survey_id="test_001",
            title_uk="Тест",
            title_en="Test",
            start_date=datetime(2024, 10, 7),
            end_date=datetime(2024, 10, 18)
        )
        test_result("Create Survey model", True)
        test_result("Survey has 22 questions default", survey.total_questions == 22)

        # Test Question creation
        question = Question(
            question_id=1,
            survey_id="test_001",
            question_number=1,
            text_uk="Тест?",
            text_en="Test?",
            question_type=QuestionType.SINGLE_CHOICE,
            category="test",
            order=1
        )
        test_result("Create Question model", True)

    except Exception as e:
        test_result("Data models tests", False, str(e))

    try:
        from models.response import Response, Answer

        # Test Response creation
        response = Response(survey_id="test_001")
        test_result("Create Response model", True)

        # Test Answer creation
        answer = Answer(
            response_id=response.response_id,
            question_id=1,
            value_raw="Test value"
        )
        response.add_answer(answer)
        test_result("Add answer to response", len(response.answers) == 1)

    except Exception as e:
        test_result("Response/Answer models", False, str(e))


def test_data_loader():
    """Test data loader."""
    print("\n3. Testing Data Loader...")

    try:
        from ingestion.data_loader import DataLoader

        loader = DataLoader(encoding='utf-8', language='uk')
        test_result("Create DataLoader", True)
        test_result("DataLoader encoding set", loader.encoding == 'utf-8')
        test_result("DataLoader language set", loader.language == 'uk')

        # Test transliteration
        result = loader._transliterate_column("Область")
        test_result("Transliterate Ukrainian text", result and result.isascii())

    except Exception as e:
        test_result("DataLoader tests", False, str(e))


def test_validation():
    """Test validation."""
    print("\n4. Testing Validation...")

    try:
        from validation.validator import DataValidator, ValidationRule
        from models.quality import QualityDimension

        validator = DataValidator()
        test_result("Create DataValidator", True)
        test_result("Validator has default rules", len(validator.rules) > 0)

        # Test rule creation
        rule = ValidationRule(
            rule_id="TEST_001",
            name="Test Rule",
            description="Test",
            dimension=QualityDimension.VALIDITY,
            severity="warning"
        )
        test_result("Create ValidationRule", True)

    except Exception as e:
        test_result("Validation tests", False, str(e))


def test_text_analyzer():
    """Test text analyzer."""
    print("\n5. Testing Text Analyzer...")

    try:
        from analysis.text_analysis import UkrainianTextAnalyzer
        import pandas as pd

        texts = pd.Series([
            "Потрібно покращити якість",
            "Технічна підтримка добра"
        ])

        analyzer = UkrainianTextAnalyzer(texts, min_word_length=3)
        test_result("Create UkrainianTextAnalyzer", True)
        test_result("Analyzer has stopwords", len(analyzer.stopwords) > 0)

        # Test preprocessing
        words = analyzer.preprocess_text("Тестовий текст для аналізу")
        test_result("Preprocess Ukrainian text", len(words) > 0)

    except ImportError:
        global skipped
        skipped += 1
        print(f"  ⊘ Text analyzer tests (pandas not available)")
    except Exception as e:
        test_result("Text analyzer tests", False, str(e))


def test_real_data():
    """Test with real data if available."""
    print("\n6. Testing with Real Data...")

    data_file = Path("/home/user/surveyprocessing/data/raw/answers.csv")

    if not data_file.exists():
        global skipped
        skipped += 1
        print("  ⊘ Real data tests (data file not found)")
        return

    try:
        from ingestion.data_loader import DataLoader

        loader = DataLoader()
        df = loader.load_csv(data_file)

        test_result("Load real CSV data", df is not None)
        test_result("Data has rows", len(df) > 5000)
        test_result("Data has columns", len(df.columns) > 30)

        # Get summary
        summary = loader.get_data_summary()
        test_result("Generate data summary", 'total_rows' in summary)

    except ImportError:
        skipped += 1
        print("  ⊘ Real data tests (pandas not available)")
    except Exception as e:
        test_result("Real data tests", False, str(e))


def test_pipeline():
    """Test pipeline."""
    print("\n7. Testing Pipeline...")

    try:
        from pipeline import SurveyAnalysisPipeline

        pipeline = SurveyAnalysisPipeline()
        test_result("Create SurveyAnalysisPipeline", True)
        test_result("Pipeline has data_loader", pipeline.data_loader is not None)
        test_result("Pipeline has validator", pipeline.validator is not None)

    except Exception as e:
        test_result("Pipeline tests", False, str(e))


def main():
    """Run all tests."""
    print("=" * 80)
    print("UKRAINIAN EDUCATION SURVEY ANALYSIS - TEST SUITE")
    print("=" * 80)

    test_imports()
    test_data_models()
    test_data_loader()
    test_validation()
    test_text_analyzer()
    test_real_data()
    test_pipeline()

    # Print summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"  Passed:  {passed}")
    print(f"  Failed:  {failed}")
    print(f"  Skipped: {skipped}")
    print(f"  Total:   {passed + failed + skipped}")

    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n✗ {failed} TESTS FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
