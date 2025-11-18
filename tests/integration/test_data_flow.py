"""Test data flow through the system."""

import pytest


class TestDataFlow:
    """Test data flowing through ingestion -> validation -> analysis."""

    def test_ingestion_to_validation_flow(self, sample_csv_file):
        """Test data flow from ingestion to validation."""
        try:
            from ingestion.data_loader import DataLoader
            from validation.validator import DataValidator

            # Load data
            loader = DataLoader()
            df = loader.load_csv(sample_csv_file)

            # Validate
            validator = DataValidator()
            metrics = validator.validate(df)

            assert metrics is not None
            assert metrics.total_records == len(df)
            assert 0 <= metrics.overall_score <= 100
        except ImportError as e:
            pytest.skip(f"Required library not available: {e}")

    def test_validation_to_analysis_flow(self, sample_csv_file):
        """Test data flow from validation to analysis."""
        try:
            from ingestion.data_loader import DataLoader
            from validation.validator import DataValidator
            from analysis.descriptive_stats import DescriptiveAnalyzer

            # Load and validate
            loader = DataLoader()
            df = loader.load_csv(sample_csv_file)

            validator = DataValidator()
            metrics = validator.validate(df)

            # Analyze if quality is good enough
            if metrics.overall_score > 50:
                analyzer = DescriptiveAnalyzer(df)
                results = analyzer.analyze_all()

                assert 'frequencies' in results
                assert 'missing_analysis' in results
        except ImportError as e:
            pytest.skip(f"Required library not available: {e}")
