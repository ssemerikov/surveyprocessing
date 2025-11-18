"""Ukrainian text analysis module."""

import logging
import re
from collections import Counter
from typing import Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class UkrainianTextAnalyzer:
    """
    Text analysis for Ukrainian language open-ended responses.

    Features:
    - Text preprocessing
    - Word frequency analysis
    - Topic extraction
    - Sentiment analysis (basic)
    - Word clouds
    - Theme categorization
    """

    def __init__(self, texts: pd.Series, min_word_length: int = 3):
        """
        Initialize text analyzer.

        Args:
            texts: Series of text responses
            min_word_length: Minimum word length to consider
        """
        self.texts = texts.dropna()
        self.min_word_length = min_word_length

        # Ukrainian stopwords
        self.stopwords = self._get_ukrainian_stopwords()

        # Processed texts
        self.cleaned_texts = []
        self.all_words = []

    def _get_ukrainian_stopwords(self) -> set:
        """Get Ukrainian stopwords."""
        stopwords = {
            'і', 'в', 'у', 'та', 'на', 'з', 'до', 'не', 'що', 'як',
            'за', 'від', 'по', 'про', 'це', 'або', 'для', 'при', 'із',
            'був', 'була', 'були', 'буде', 'може', 'можна', 'треба',
            'є', 'був', 'була', 'були', 'буде', 'має', 'мають',
            'щоб', 'якщо', 'коли', 'тому', 'але', 'також', 'вже',
            'ще', 'тільки', 'дуже', 'все', 'всі', 'весь', 'свій',
            'який', 'яка', 'які', 'цей', 'ця', 'це', 'ці',
            'мій', 'моя', 'мої', 'твій', 'його', 'її', 'їх',
        }
        return stopwords

    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess Ukrainian text.

        Args:
            text: Raw text string

        Returns:
            List of cleaned words
        """
        # Convert to lowercase
        text = text.lower()

        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text)

        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)

        # Remove numbers (optional - adjust as needed)
        # text = re.sub(r'\d+', '', text)

        # Keep only Ukrainian letters, spaces, and hyphens
        text = re.sub(r'[^а-яіїєґА-ЯІЇЄҐ\s\-]', ' ', text)

        # Split into words
        words = text.split()

        # Filter words
        words = [
            w for w in words
            if len(w) >= self.min_word_length
            and w not in self.stopwords
            and not w.isdigit()
        ]

        return words

    def analyze_all(self) -> Dict:
        """Run complete text analysis."""
        logger.info(f"Analyzing {len(self.texts)} text responses...")

        # Preprocess all texts
        self.cleaned_texts = [self.preprocess_text(text) for text in self.texts]
        self.all_words = [word for text in self.cleaned_texts for word in text]

        results = {
            'word_frequencies': self.get_word_frequencies(),
            'common_phrases': self.extract_common_phrases(),
            'themes': self.categorize_themes(),
            'statistics': self.get_text_statistics(),
        }

        return results

    def get_word_frequencies(self, top_n: int = 50) -> pd.DataFrame:
        """
        Get most frequent words.

        Args:
            top_n: Number of top words to return

        Returns:
            DataFrame with word frequencies
        """
        word_counts = Counter(self.all_words)
        top_words = word_counts.most_common(top_n)

        df = pd.DataFrame(top_words, columns=['word', 'frequency'])
        total = len(self.all_words)
        df['percentage'] = (df['frequency'] / total * 100).round(2)

        return df

    def extract_common_phrases(self, n_gram: int = 2, top_n: int = 30) -> pd.DataFrame:
        """
        Extract common n-grams (phrases).

        Args:
            n_gram: Size of n-gram (2=bigrams, 3=trigrams)
            top_n: Number of top phrases

        Returns:
            DataFrame with common phrases
        """
        n_grams = []

        for words in self.cleaned_texts:
            if len(words) < n_gram:
                continue

            for i in range(len(words) - n_gram + 1):
                phrase = ' '.join(words[i:i + n_gram])
                n_grams.append(phrase)

        phrase_counts = Counter(n_grams)
        top_phrases = phrase_counts.most_common(top_n)

        df = pd.DataFrame(top_phrases, columns=['phrase', 'frequency'])
        return df

    def categorize_themes(self) -> Dict[str, int]:
        """
        Categorize responses into themes.

        Returns:
            Dictionary of themes and their counts
        """
        themes = {
            'технічна_підтримка': [],  # Technical support
            'платформи': [],  # Platforms
            'комунікація': [],  # Communication
            'інтернет': [],  # Internet
            'обладнання': [],  # Equipment/devices
            'навчання': [],  # Training
            'інформація': [],  # Information
            'доступ': [],  # Access
            'якість': [],  # Quality
            'покращення': [],  # Improvements
        }

        # Keywords for each theme
        theme_keywords = {
            'технічна_підтримка': ['підтримка', 'допомога', 'технічн', 'консультац', 'супровід'],
            'платформи': ['платформ', 'сайт', 'систем', 'електронний', 'онлайн'],
            'комунікація': ['комунікац', 'зв\'язок', 'спілкування', 'контакт', 'відповід'],
            'інтернет': ['інтернет', 'мереж', 'інтернету', 'з\'єднання'],
            'обладнання': ['обладнання', 'комп\'ютер', 'планшет', 'телефон', 'пристрій', 'технік'],
            'навчання': ['навчання', 'вчител', 'учн', 'уроки', 'освіт'],
            'інформація': ['інформац', 'дані', 'повідомлення', 'оголошення'],
            'доступ': ['доступ', 'можливість', 'користування'],
            'якість': ['якість', 'якісн', 'ефективн', 'покращ'],
            'покращення': ['покращ', 'вдоскон', 'полі', 'змін', 'розвиток'],
        }

        # Categorize each response
        for text in self.texts:
            text_lower = text.lower()

            for theme, keywords in theme_keywords.items():
                if any(kw in text_lower for kw in keywords):
                    themes[theme].append(text)

        # Count occurrences
        theme_counts = {theme: len(texts) for theme, texts in themes.items()}

        return theme_counts

    def get_text_statistics(self) -> Dict:
        """Get basic text statistics."""
        word_counts = [len(self.preprocess_text(text)) for text in self.texts]

        stats = {
            'total_responses': len(self.texts),
            'total_words': len(self.all_words),
            'unique_words': len(set(self.all_words)),
            'avg_words_per_response': np.mean(word_counts),
            'median_words_per_response': np.median(word_counts),
            'min_words': np.min(word_counts),
            'max_words': np.max(word_counts),
        }

        return stats

    def generate_wordcloud(
        self,
        save_path: Optional[str] = None,
        width: int = 1200,
        height: int = 800,
        max_words: int = 100
    ):
        """
        Generate word cloud visualization.

        Args:
            save_path: Path to save image (None = display only)
            width: Image width
            height: Image height
            max_words: Maximum words to display
        """
        if not self.all_words:
            logger.warning("No words to create word cloud")
            return

        # Create word cloud
        wordcloud = WordCloud(
            width=width,
            height=height,
            background_color='white',
            max_words=max_words,
            font_path=None,  # May need to specify Ukrainian font path
            relative_scaling=0.5,
            min_font_size=10
        ).generate(' '.join(self.all_words))

        # Plot
        plt.figure(figsize=(width/100, height/100), dpi=100)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.tight_layout(pad=0)

        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
            logger.info(f"Word cloud saved to {save_path}")
        else:
            plt.show()

        plt.close()

    def get_sample_responses_by_theme(
        self,
        theme: str,
        n_samples: int = 5
    ) -> List[str]:
        """Get sample responses for a specific theme."""
        theme_keywords = {
            'технічна_підтримка': ['підтримка', 'допомога', 'технічн'],
            'платформи': ['платформ', 'сайт', 'систем'],
            'інтернет': ['інтернет', 'мереж'],
        }

        if theme not in theme_keywords:
            return []

        keywords = theme_keywords[theme]
        matching = []

        for text in self.texts:
            if any(kw in text.lower() for kw in keywords):
                matching.append(text)

        return matching[:n_samples]

    def export_results(self, output_path: str):
        """Export text analysis results to Excel."""
        results = self.analyze_all()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Word frequencies
            results['word_frequencies'].to_excel(
                writer,
                sheet_name='Word_Frequencies',
                index=False
            )

            # Common phrases
            results['common_phrases'].to_excel(
                writer,
                sheet_name='Common_Phrases',
                index=False
            )

            # Themes
            pd.DataFrame(
                list(results['themes'].items()),
                columns=['Theme', 'Count']
            ).to_excel(writer, sheet_name='Themes', index=False)

            # Statistics
            pd.DataFrame(
                [results['statistics']]
            ).T.to_excel(writer, sheet_name='Statistics')

        logger.info(f"Text analysis results exported to {output_path}")
