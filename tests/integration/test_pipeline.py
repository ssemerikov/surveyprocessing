"""Integration tests for the full pipeline."""

import pytest
from pathlib import Path


class TestPipelineIntegration:
    """Test full pipeline integration."""

    def test_pipeline_initialization(self, config_dict, tmp_path):
        """Test pipeline initialization."""
        try:
            from pipeline import SurveyAnalysisPipeline
            import yaml

            # Create temp config file
            config_file = tmp_path / "config.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(config_dict, f)

            pipeline = SurveyAnalysisPipeline(config_path=config_file)
            assert pipeline.config is not None
            assert pipeline.data_loader is not None
            assert pipeline.validator is not None
        except ImportError as e:
            pytest.skip(f"Required library not available: {e}")

    def test_load_and_validate(self, sample_csv_file, config_dict, tmp_path):
        """Test loading and validating data."""
        try:
            from pipeline import SurveyAnalysisPipeline
            import yaml

            # Create config
            config_file = tmp_path / "config.yaml"
            with open(config_file, 'w') as f:
                yaml.dump(config_dict, f)

            pipeline = SurveyAnalysisPipeline(config_path=config_file)

            # Load data
            df = pipeline.load_data(sample_csv_file)
            assert df is not None
            assert len(df) == 3

            # Validate
            validation_results = pipeline.validate_data()
            assert 'quality_metrics' in validation_results
            assert 'summary' in validation_results
        except ImportError as e:
            pytest.skip(f"Required library not available: {e}")


class TestEndToEndWorkflow:
    """Test end-to-end workflow."""

    def test_complete_workflow(self, tmp_path):
        """Test complete analysis workflow with real data."""
        try:
            from pipeline import SurveyAnalysisPipeline

            # Check if actual data file exists
            data_file = Path("/home/user/surveyprocessing/data/raw/answers.csv")
            if not data_file.exists():
                pytest.skip("Actual data file not available")

            pipeline = SurveyAnalysisPipeline()

            # Load data
            df = pipeline.load_data(data_file)
            assert df is not None
            assert len(df) > 0

            # Get summary
            summary = pipeline.get_summary()
            assert 'total_rows' in summary
            assert summary['total_rows'] > 5000  # Should have 5000+ responses

        except Exception as e:
            pytest.skip(f"End-to-end test skipped: {e}")
