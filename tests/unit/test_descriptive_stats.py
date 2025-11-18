"""Tests for descriptive statistics."""

import pytest


class TestDescriptiveAnalyzer:
    """Test DescriptiveAnalyzer class."""

    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        try:
            import pandas as pd
            from analysis.descriptive_stats import DescriptiveAnalyzer

            df = pd.DataFrame({
                'region': ['Київська', 'Львівська', 'Харківська'],
                'grade': [9, 10, 11],
                'satisfaction': ['Так', 'Ні', 'Так']
            })

            analyzer = DescriptiveAnalyzer(df)
            assert analyzer.df is not None
            assert len(analyzer.df) == 3
        except ImportError:
            pytest.skip("pandas not available")

    def test_calculate_frequencies(self):
        """Test frequency calculation."""
        try:
            import pandas as pd
            from analysis.descriptive_stats import DescriptiveAnalyzer

            df = pd.DataFrame({
                'region': ['Київська', 'Львівська', 'Київська', 'Харківська'],
                'satisfaction': ['Так', 'Так', 'Ні', 'Так']
            })

            analyzer = DescriptiveAnalyzer(df)
            frequencies = analyzer.calculate_frequencies(['region'])

            assert 'region' in frequencies
            assert len(frequencies['region']) > 0
        except ImportError:
            pytest.skip("pandas not available")

    def test_find_column(self):
        """Test column finding by keywords."""
        try:
            import pandas as pd
            from analysis.descriptive_stats import DescriptiveAnalyzer

            df = pd.DataFrame({
                'Область проживання': ['Київська'],
                'Клас': [9],
                'Задоволені': ['Так']
            })

            analyzer = DescriptiveAnalyzer(df)

            # Should find region column
            region_col = analyzer._find_column(['област', 'region'])
            assert region_col == 'Область проживання'

            # Should find grade column
            grade_col = analyzer._find_column(['клас', 'grade'])
            assert grade_col == 'Клас'
        except ImportError:
            pytest.skip("pandas not available")
