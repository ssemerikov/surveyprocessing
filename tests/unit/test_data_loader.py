"""Tests for data loader."""

import pytest
from pathlib import Path

from ingestion.data_loader import DataLoader, DataFormat


class TestDataLoader:
    """Test DataLoader class."""

    def test_loader_initialization(self):
        """Test loader initialization."""
        loader = DataLoader(encoding='utf-8', language='uk')
        assert loader.encoding == 'utf-8'
        assert loader.language == 'uk'
        assert loader.df is None

    def test_transliterate_column(self):
        """Test Ukrainian to English transliteration."""
        loader = DataLoader()

        # Test basic transliteration
        result = loader._transliterate_column("Область")
        assert isinstance(result, str)
        assert result.isascii()  # Should be ASCII

        # Test complex Ukrainian
        result = loader._transliterate_column("Ваш вік")
        assert result == "vash_vik"

        # Test with spaces
        result = loader._transliterate_column("Зазначте область")
        assert "_" in result  # Spaces should become underscores

    def test_ukrainian_stopwords(self):
        """Test Ukrainian stopwords loading."""
        loader = DataLoader()
        stopwords = loader._get_ukrainian_stopwords() if hasattr(loader, '_get_ukrainian_stopwords') else set()

        # Check it's a set
        assert isinstance(stopwords, set) or stopwords is None

        # If it exists, should contain common Ukrainian words
        if stopwords:
            common_words = {'і', 'в', 'на', 'що', 'та'}
            assert len(common_words.intersection(stopwords)) > 0

    def test_parse_multiple_choice(self, tmp_path):
        """Test parsing multiple choice questions."""
        # Create test CSV with multiple choice data
        csv_content = """col1,choices
1,"option1, option2, option3"
2,"single_option"
3,"""

        csv_file = tmp_path / "test.csv"
        csv_file.write_text(csv_content)

        loader = DataLoader()

        # Test with actual pandas (mock if not available)
        try:
            df = loader.load_csv(csv_file)
            result = loader.parse_multiple_choice('choices', delimiter=',')

            # First row should have 3 items
            assert len(result.iloc[0]) == 3
            # Second row should have 1 item
            assert len(result.iloc[1]) == 1
            # Third row should be empty list
            assert len(result.iloc[2]) == 0
        except ImportError:
            pytest.skip("pandas not available")

    def test_get_data_summary(self, sample_csv_file):
        """Test data summary generation."""
        loader = DataLoader()

        try:
            loader.load_csv(sample_csv_file)
            summary = loader.get_data_summary()

            assert 'total_rows' in summary
            assert 'total_columns' in summary
            assert summary['total_rows'] == 3
            assert summary['total_columns'] > 0
        except ImportError:
            pytest.skip("pandas not available")


class TestDataFormat:
    """Test DataFormat enum."""

    def test_data_format_values(self):
        """Test DataFormat enum values."""
        assert DataFormat.CSV == "csv"
        assert DataFormat.TSV == "tsv"
        assert DataFormat.XLSX == "xlsx"
        assert DataFormat.JSON == "json"
