"""Tests for Ukrainian text analysis."""

import pytest

from analysis.text_analysis import UkrainianTextAnalyzer


class TestUkrainianTextAnalyzer:
    """Test UkrainianTextAnalyzer class."""

    def test_analyzer_initialization(self, sample_text_data):
        """Test analyzer initialization."""
        try:
            import pandas as pd
            texts = pd.Series(sample_text_data)
            analyzer = UkrainianTextAnalyzer(texts, min_word_length=3)

            assert analyzer.min_word_length == 3
            assert len(analyzer.texts) == 5
            assert len(analyzer.stopwords) > 0
        except ImportError:
            pytest.skip("pandas not available")

    def test_ukrainian_stopwords(self):
        """Test Ukrainian stopwords."""
        try:
            import pandas as pd
            analyzer = UkrainianTextAnalyzer(pd.Series([]))
            stopwords = analyzer._get_ukrainian_stopwords()

            assert isinstance(stopwords, set)
            assert 'і' in stopwords
            assert 'в' in stopwords
            assert 'на' in stopwords
            assert len(stopwords) > 20  # Should have reasonable number
        except ImportError:
            pytest.skip("pandas not available")

    def test_preprocess_text(self, sample_text_data):
        """Test text preprocessing."""
        try:
            import pandas as pd
            texts = pd.Series(sample_text_data)
            analyzer = UkrainianTextAnalyzer(texts)

            # Test preprocessing
            text = "Потрібно покращити якість інтернету в школі"
            words = analyzer.preprocess_text(text)

            assert isinstance(words, list)
            assert len(words) > 0
            # Stopwords should be removed
            assert 'в' not in words
            # Content words should remain
            assert 'якість' in words or 'інтернету' in words
        except ImportError:
            pytest.skip("pandas not available")

    def test_categorize_themes(self, sample_text_data):
        """Test theme categorization."""
        try:
            import pandas as pd
            texts = pd.Series(sample_text_data)
            analyzer = UkrainianTextAnalyzer(texts)

            themes = analyzer.categorize_themes()

            assert isinstance(themes, dict)
            assert 'технічна_підтримка' in themes
            assert 'платформи' in themes
            assert 'інтернет' in themes

            # Should find internet theme in sample data
            assert themes['інтернет'] > 0
        except ImportError:
            pytest.skip("pandas not available")

    def test_get_text_statistics(self, sample_text_data):
        """Test text statistics."""
        try:
            import pandas as pd
            texts = pd.Series(sample_text_data)
            analyzer = UkrainianTextAnalyzer(texts)
            analyzer.cleaned_texts = [analyzer.preprocess_text(t) for t in texts]
            analyzer.all_words = [w for t in analyzer.cleaned_texts for w in t]

            stats = analyzer.get_text_statistics()

            assert 'total_responses' in stats
            assert 'total_words' in stats
            assert 'unique_words' in stats
            assert stats['total_responses'] == 5
            assert stats['total_words'] > 0
        except ImportError:
            pytest.skip("pandas not available")


class TestTextPreprocessing:
    """Test text preprocessing functions."""

    def test_lowercase_conversion(self):
        """Test that text is converted to lowercase."""
        try:
            import pandas as pd
            analyzer = UkrainianTextAnalyzer(pd.Series([]))
            text = "УКРАЇНА Україна україна"
            words = analyzer.preprocess_text(text)

            # All words should be lowercase
            for word in words:
                assert word == word.lower()
        except ImportError:
            pytest.skip("pandas not available")

    def test_url_removal(self):
        """Test URL removal."""
        try:
            import pandas as pd
            analyzer = UkrainianTextAnalyzer(pd.Series([]))
            text = "Відвідайте http://example.com для інформації"
            words = analyzer.preprocess_text(text)

            # URL should be removed
            assert 'http://example.com' not in ' '.join(words)
        except ImportError:
            pytest.skip("pandas not available")

    def test_min_word_length_filter(self):
        """Test minimum word length filtering."""
        try:
            import pandas as pd
            analyzer = UkrainianTextAnalyzer(pd.Series([]), min_word_length=4)
            text = "я є ми вони школа"
            words = analyzer.preprocess_text(text)

            # Short words should be filtered
            for word in words:
                assert len(word) >= 4
        except ImportError:
            pytest.skip("pandas not available")
