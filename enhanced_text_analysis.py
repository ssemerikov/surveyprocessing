#!/usr/bin/env python3
"""
Enhanced Text Analysis for Q22 - Parent Suggestions
Deep NLP analysis of free-text responses from 5,223 parents
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict
import re
from typing import Dict, List, Tuple, Set

# NLP Libraries
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation


class UkrainianTextAnalyzer:
    """Advanced Ukrainian text analysis for survey suggestions."""

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.suggestions_col = df.columns[25]  # Q22
        self.region_col = df.columns[4]  # Q4: Region
        self.tech_support_col = df.columns[14]  # Q12: Tech support
        self.website_quality_col = df.columns[16]  # Q14: Website quality
        self.device_access_col = df.columns[24]  # Q21: Device access
        self.format_col = df.columns[8]  # Q8: Educational format

        # Ukrainian stopwords (expanded)
        self.stopwords = self._get_ukrainian_stopwords()

        # Theme keywords (comprehensive)
        self.theme_keywords = self._get_theme_keywords()

        # Satisfaction indicators
        self.satisfaction_positive = {'влаштовує', 'добре', 'чудово', 'відмінно', 'гарно',
                                     'задоволений', 'задоволена', 'супер', 'прекрасно',
                                     'ідеально', 'достатньо', 'нормально'}
        self.satisfaction_negative = {'погано', 'жахливо', 'недостатньо', 'слабо', 'немає',
                                     'відсутнє', 'відсутній', 'проблема', 'важко'}

    def _get_ukrainian_stopwords(self) -> Set[str]:
        """Expanded Ukrainian stopwords."""
        return {
            # Basic
            'і', 'в', 'у', 'та', 'на', 'з', 'до', 'не', 'що', 'як', 'від', 'за',
            'по', 'при', 'це', 'є', 'був', 'була', 'було', 'були', 'буде', 'будуть',
            # Pronouns
            'я', 'ти', 'він', 'вона', 'воно', 'ми', 'ви', 'вони', 'мій', 'моя', 'моє',
            'твій', 'твоя', 'наш', 'наша', 'ваш', 'ваша', 'їх', 'його', 'її',
            # Common words
            'або', 'але', 'якщо', 'тому', 'для', 'про', 'під', 'над', 'між', 'через',
            'також', 'можна', 'треба', 'потрібно', 'все', 'всі', 'весь', 'вся', 'таке',
            'такий', 'така', 'так', 'ні', 'ще', 'вже', 'тільки', 'лише', 'навіть',
            # Question-specific noise
            'думку', 'вашу', 'вашого', 'закладу', 'освіти', 'опишіть', 'ласка', 'пропозиції'
        }

    def _get_theme_keywords(self) -> Dict[str, List[str]]:
        """Comprehensive theme classification keywords."""
        return {
            'технічна_підтримка': [
                'підтримка', 'техпідтримка', 'технічний', 'технічна', 'допомога',
                'консультація', 'фахівець', 'спеціаліст', 'сервіс', 'обслуговування'
            ],
            'інтернет': [
                'інтернет', 'інтернету', 'швидкість', 'зв\'язок', "зв'язку", 'wi-fi',
                'wifi', 'вайфай', 'підключення', 'мережа', 'мережі', 'онлайн',
                'он-лайн', 'он лайн', 'offline', 'офлайн'
            ],
            'обладнання': [
                'комп\'ютер', "комп'ютери", 'ноутбук', 'планшет', 'техніка',
                'обладнання', 'пристрій', 'пристрої', 'девайс', 'гаджет',
                'монітор', 'клавіатура', 'миша', 'принтер', 'сканер'
            ],
            'платформи': [
                'платформа', 'платформи', 'система', 'системи', 'додаток', 'додатки',
                'програма', 'програми', 'софт', 'зум', 'zoom', 'teams', 'тімс',
                'classroom', 'клас', 'moodle', 'мудл', 'електронний журнал'
            ],
            'комунікація': [
                'комунікація', 'звязок', 'спілкування', 'інформування',
                'повідомлення', 'оповіщення', 'чат', 'месенджер', 'viber', 'вайбер',
                'telegram', 'телеграм', 'email', 'пошта', 'sms', 'смс'
            ],
            'навчання_контент': [
                'урок', 'уроки', 'заняття', 'матеріал', 'матеріали', 'контент',
                'відео', 'відеоурок', 'презентація', 'лекція', 'завдання',
                'домашнє', 'дз', 'тест', 'тести', 'підручник', 'посібник'
            ],
            'електронний_журнал': [
                'журнал', 'щоденник', 'оцінки', 'оцінювання', 'бали', 'відвідування',
                'відвідуваність', 'успішність', 'дневник', 'е-журнал'
            ],
            'сайт_школи': [
                'сайт', 'веб-сайт', 'вебсайт', 'портал', 'сторінка', 'вебсторінка',
                'інтерфейс', 'дизайн', 'навігація', 'розділ', 'розділи'
            ],
            'навчання_вчителів': [
                'навчання', 'тренінг', 'курс', 'курси', 'підготовка', 'підвищення',
                'кваліфікація', 'семінар', 'вебінар', 'освоєння', 'вміння', 'навички',
                'вчителі', 'педагоги', 'викладачі'
            ],
            'доступ': [
                'доступ', 'доступність', 'доступний', 'доступна', 'вхід', 'логін',
                'пароль', 'реєстрація', 'авторизація', 'права', 'дозвіл'
            ],
            'безпека': [
                'безпека', 'захист', 'конфіденційність', 'персональні', 'дані',
                'приватність', 'безпечний', 'небезпечно', 'вірус', 'хакер'
            ],
            'військовий_контекст': [
                'тривога', 'тривоги', 'повітряна', 'укриття', 'війна', 'бомбосховище',
                'евакуація', 'безпека', 'сирена', 'сирени', 'обстріл', 'ворог'
            ],
            'фінансування': [
                'фінансування', 'кошти', 'гроші', 'бюджет', 'платно', 'безкоштовно',
                'оплата', 'ціна', 'вартість', 'дорого', 'дешево'
            ],
            'інформаційна_грамотність': [
                'цифрова', 'цифрові', 'компетентність', 'компетенція', 'грамотність',
                'навички', 'вміння', 'знання', 'уміння', 'освоїти', 'вчитися'
            ],
            'батьківський_контроль': [
                'контроль', 'моніторинг', 'відстеження', 'слідкування', 'перевірка',
                'батьки', 'батьківський', 'батьківська', 'сімя', 'родина'
            ]
        }

    def preprocess_text(self, text: str) -> List[str]:
        """Preprocess Ukrainian text."""
        if pd.isna(text):
            return []

        text = str(text).lower()

        # Remove URLs, emails, special chars
        text = re.sub(r'http\S+|www\.\S+', '', text)
        text = re.sub(r'\S+@\S+', '', text)
        text = re.sub(r'[^\w\s\'-]', ' ', text)

        # Tokenize
        words = text.split()

        # Remove stopwords and short words
        words = [w for w in words if w not in self.stopwords and len(w) > 2]

        return words

    def classify_response_type(self, text: str) -> str:
        """Classify response as satisfied/substantive/minimal."""
        if pd.isna(text):
            return 'empty'

        text = str(text).strip().lower()

        # Empty or minimal
        if len(text) < 3 or text in {'-', '...', '.', '—', '–', 'немає', 'нема'}:
            return 'minimal'

        # Satisfied (everything is fine)
        if any(word in text for word in ['все влаштовує', 'всё устраивает', 'все добре',
                                          'все гаразд', 'все нормально', 'усе влаштовує',
                                          'все влаштує', 'все добре', 'усе добре']):
            return 'satisfied'

        # Very brief
        if len(text) < 10:
            return 'brief'

        # Substantive
        return 'substantive'

    def extract_themes(self, text: str) -> List[str]:
        """Extract themes from text based on keywords."""
        if pd.isna(text):
            return []

        text = str(text).lower()
        themes = []

        for theme, keywords in self.theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                themes.append(theme)

        return themes if themes else ['інше']

    def analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis for Ukrainian text."""
        if pd.isna(text):
            return 'neutral'

        text = str(text).lower()

        positive_count = sum(1 for word in self.satisfaction_positive if word in text)
        negative_count = sum(1 for word in self.satisfaction_negative if word in text)

        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        else:
            return 'neutral'

    def run_comprehensive_analysis(self) -> Dict:
        """Run complete text analysis pipeline."""

        suggestions = self.df[self.suggestions_col].copy()

        results = {
            'total_responses': len(suggestions),
            'non_empty': suggestions.notna().sum(),
            'response_types': {},
            'themes': defaultdict(int),
            'theme_cooccurrence': defaultdict(int),
            'sentiment': defaultdict(int),
            'length_stats': {},
            'word_frequency': {},
            'bigram_frequency': {},
            'trigram_frequency': {},
            'tfidf_keywords': [],
            'topics': {},
            'regional_themes': {},
            'cross_analysis': {},
            'examples': defaultdict(list)
        }

        # 1. RESPONSE TYPE CLASSIFICATION
        print("1. Classifying response types...")
        response_types = suggestions.apply(self.classify_response_type)
        results['response_types'] = response_types.value_counts().to_dict()

        # Filter for substantive responses
        substantive_mask = response_types == 'substantive'
        substantive_texts = suggestions[substantive_mask]
        print(f"   Substantive responses: {len(substantive_texts)} ({len(substantive_texts)/len(suggestions)*100:.1f}%)")

        # 2. THEME EXTRACTION
        print("2. Extracting themes...")
        all_themes = []
        for idx, text in suggestions.items():
            themes = self.extract_themes(text)
            all_themes.extend(themes)

            # Theme co-occurrence
            if len(themes) > 1:
                for i, theme1 in enumerate(themes):
                    for theme2 in themes[i+1:]:
                        pair = tuple(sorted([theme1, theme2]))
                        results['theme_cooccurrence'][pair] += 1

            # Store examples
            for theme in themes:
                if len(results['examples'][theme]) < 5:
                    results['examples'][theme].append(text)

        results['themes'] = Counter(all_themes)

        # 3. SENTIMENT ANALYSIS
        print("3. Analyzing sentiment...")
        sentiments = suggestions.apply(self.analyze_sentiment)
        results['sentiment'] = sentiments.value_counts().to_dict()

        # 4. TEXT LENGTH STATISTICS
        print("4. Computing length statistics...")
        lengths = suggestions.str.len()
        results['length_stats'] = {
            'mean': lengths.mean(),
            'median': lengths.median(),
            'std': lengths.std(),
            'min': lengths.min(),
            'max': lengths.max(),
            'quartiles': lengths.quantile([0.25, 0.5, 0.75]).to_dict()
        }

        # 5. WORD FREQUENCY (substantive only)
        print("5. Analyzing word frequencies...")
        all_words = []
        all_bigrams = []
        all_trigrams = []

        for text in substantive_texts:
            words = self.preprocess_text(text)
            all_words.extend(words)

            # Bigrams
            if len(words) >= 2:
                bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words)-1)]
                all_bigrams.extend(bigrams)

            # Trigrams
            if len(words) >= 3:
                trigrams = [f"{words[i]} {words[i+1]} {words[i+2]}" for i in range(len(words)-2)]
                all_trigrams.extend(trigrams)

        results['word_frequency'] = Counter(all_words).most_common(100)
        results['bigram_frequency'] = Counter(all_bigrams).most_common(50)
        results['trigram_frequency'] = Counter(all_trigrams).most_common(30)

        # 6. TF-IDF ANALYSIS
        print("6. Running TF-IDF analysis...")
        if len(substantive_texts) > 10:
            tfidf = TfidfVectorizer(
                max_features=50,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.8
            )

            try:
                tfidf_matrix = tfidf.fit_transform(substantive_texts.fillna(''))
                feature_names = tfidf.get_feature_names_out()

                # Get average TF-IDF score for each term
                avg_scores = tfidf_matrix.mean(axis=0).A1
                results['tfidf_keywords'] = [
                    (feature_names[i], float(avg_scores[i]))
                    for i in avg_scores.argsort()[-30:][::-1]
                ]
            except Exception as e:
                print(f"   TF-IDF failed: {e}")

        # 7. TOPIC MODELING (LDA)
        print("7. Discovering topics...")
        if len(substantive_texts) > 20:
            try:
                vectorizer = CountVectorizer(max_features=100, min_df=2, max_df=0.8)
                doc_term_matrix = vectorizer.fit_transform(substantive_texts.fillna(''))

                lda = LatentDirichletAllocation(n_components=5, random_state=42, max_iter=20)
                lda.fit(doc_term_matrix)

                feature_names = vectorizer.get_feature_names_out()

                for topic_idx, topic in enumerate(lda.components_):
                    top_words_idx = topic.argsort()[-10:][::-1]
                    top_words = [feature_names[i] for i in top_words_idx]
                    results['topics'][f'topic_{topic_idx+1}'] = top_words
            except Exception as e:
                print(f"   Topic modeling failed: {e}")

        # 8. REGIONAL THEME ANALYSIS
        print("8. Analyzing regional patterns...")
        regional_data = defaultdict(lambda: defaultdict(int))

        for idx, row in self.df.iterrows():
            region = row[self.region_col]
            text = row[self.suggestions_col]
            themes = self.extract_themes(text)

            for theme in themes:
                regional_data[region][theme] += 1

        results['regional_themes'] = dict(regional_data)

        # 9. CROSS-ANALYSIS WITH QUANTITATIVE QUESTIONS
        print("9. Cross-analyzing with quantitative data...")

        # Tech support satisfaction vs themes
        tech_support_themes = defaultdict(lambda: defaultdict(int))
        for idx, row in self.df.iterrows():
            satisfaction = row[self.tech_support_col]
            text = row[self.suggestions_col]
            themes = self.extract_themes(text)

            for theme in themes:
                tech_support_themes[satisfaction][theme] += 1

        results['cross_analysis']['tech_support_vs_themes'] = dict(tech_support_themes)

        # Educational format vs themes
        format_themes = defaultdict(lambda: defaultdict(int))
        for idx, row in self.df.iterrows():
            edu_format = row[self.format_col]
            text = row[self.suggestions_col]
            themes = self.extract_themes(text)

            for theme in themes:
                format_themes[edu_format][theme] += 1

        results['cross_analysis']['format_vs_themes'] = dict(format_themes)

        print("\n✓ Comprehensive analysis complete!")
        return results


def generate_comprehensive_report(results: Dict, output_path: str):
    """Generate detailed text analysis report."""

    lines = []

    def add_header(title):
        lines.append("")
        lines.append("=" * 100)
        lines.append(title.center(100))
        lines.append("=" * 100)
        lines.append("")

    def add_section(title):
        lines.append("")
        lines.append("-" * 100)
        lines.append(title)
        lines.append("-" * 100)

    # HEADER
    add_header("COMPREHENSIVE TEXT ANALYSIS - QUESTION 22")
    add_header("Parent Suggestions for Digital Education Environment Improvement")

    lines.append(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Total Responses: {results['total_responses']:,}")
    lines.append(f"Non-Empty Responses: {results['non_empty']:,} ({results['non_empty']/results['total_responses']*100:.1f}%)")

    # 1. RESPONSE TYPE DISTRIBUTION
    add_section("1. RESPONSE TYPE CLASSIFICATION")
    lines.append("")
    total = sum(results['response_types'].values())
    for resp_type, count in sorted(results['response_types'].items(), key=lambda x: x[1], reverse=True):
        pct = count / total * 100
        lines.append(f"  {resp_type:<20} {count:>5} ({pct:>5.1f}%)")

    # 2. LENGTH STATISTICS
    add_section("2. TEXT LENGTH STATISTICS")
    lines.append("")
    stats = results['length_stats']
    lines.append(f"  Mean length:       {stats['mean']:>6.1f} characters")
    lines.append(f"  Median length:     {stats['median']:>6.1f} characters")
    lines.append(f"  Std deviation:     {stats['std']:>6.1f} characters")
    lines.append(f"  Min length:        {stats['min']:>6.0f} characters")
    lines.append(f"  Max length:        {stats['max']:>6.0f} characters")

    # 3. SENTIMENT DISTRIBUTION
    add_section("3. SENTIMENT ANALYSIS")
    lines.append("")
    total_sent = sum(results['sentiment'].values())
    for sentiment, count in sorted(results['sentiment'].items(), key=lambda x: x[1], reverse=True):
        pct = count / total_sent * 100
        lines.append(f"  {sentiment:<20} {count:>5} ({pct:>5.1f}%)")

    # 4. THEME DISTRIBUTION
    add_section("4. THEME DISTRIBUTION (Top 20)")
    lines.append("")
    for theme, count in results['themes'].most_common(20):
        pct = count / results['total_responses'] * 100
        lines.append(f"  {theme:<40} {count:>5} ({pct:>5.1f}%)")

    # 5. WORD FREQUENCY
    add_section("5. MOST FREQUENT WORDS (Top 50)")
    lines.append("")
    for i, (word, count) in enumerate(results['word_frequency'][:50], 1):
        lines.append(f"  {i:>2}. {word:<30} {count:>5}")

    # 6. BIGRAMS
    add_section("6. MOST FREQUENT BIGRAMS (Top 30)")
    lines.append("")
    for i, (bigram, count) in enumerate(results['bigram_frequency'][:30], 1):
        lines.append(f"  {i:>2}. {bigram:<50} {count:>5}")

    # 7. TRIGRAMS
    add_section("7. MOST FREQUENT TRIGRAMS (Top 20)")
    lines.append("")
    for i, (trigram, count) in enumerate(results['trigram_frequency'][:20], 1):
        lines.append(f"  {i:>2}. {trigram:<60} {count:>5}")

    # 8. TF-IDF KEYWORDS
    if results['tfidf_keywords']:
        add_section("8. TF-IDF KEYWORDS (Top 30)")
        lines.append("")
        for i, (keyword, score) in enumerate(results['tfidf_keywords'], 1):
            lines.append(f"  {i:>2}. {keyword:<40} {score:>8.4f}")

    # 9. DISCOVERED TOPICS
    if results['topics']:
        add_section("9. DISCOVERED TOPICS (LDA)")
        for topic_name, words in results['topics'].items():
            lines.append("")
            lines.append(f"  {topic_name.upper()}:")
            lines.append(f"    {', '.join(words)}")

    # 10. THEME CO-OCCURRENCE
    add_section("10. THEME CO-OCCURRENCE (Top 20 Pairs)")
    lines.append("")
    sorted_pairs = sorted(results['theme_cooccurrence'].items(), key=lambda x: x[1], reverse=True)[:20]
    for i, (pair, count) in enumerate(sorted_pairs, 1):
        lines.append(f"  {i:>2}. {pair[0]} + {pair[1]:<40} {count:>5}")

    # 11. EXAMPLES BY THEME
    add_section("11. EXAMPLE RESPONSES BY THEME")
    for theme in sorted(results['examples'].keys()):
        if theme != 'інше' and results['examples'][theme]:
            lines.append("")
            lines.append(f"  THEME: {theme.upper()}")
            for i, example in enumerate(results['examples'][theme][:3], 1):
                example_text = str(example)[:150]
                lines.append(f"    {i}. {example_text}...")

    # Save report
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n✓ Report generated: {output_path}")
    print(f"  Total lines: {len(lines)}")


def main():
    """Run enhanced text analysis."""

    print("=" * 100)
    print("ENHANCED TEXT ANALYSIS - Q22 PARENT SUGGESTIONS".center(100))
    print("=" * 100)
    print()

    # Load data
    print("Loading data...")
    df = pd.read_csv('data/raw/answers.csv', encoding='utf-8')
    print(f"✓ Loaded {len(df):,} responses")
    print()

    # Run analysis
    analyzer = UkrainianTextAnalyzer(df)
    results = analyzer.run_comprehensive_analysis()

    # Generate reports
    Path("reports/text_analysis").mkdir(parents=True, exist_ok=True)

    # Main report
    generate_comprehensive_report(
        results,
        'reports/text_analysis/q22_comprehensive_analysis.txt'
    )

    # Export to Excel
    print("\nGenerating Excel report...")
    with pd.ExcelWriter('reports/text_analysis/q22_detailed_analysis.xlsx', engine='openpyxl') as writer:

        # Sheet 1: Overview
        overview = pd.DataFrame({
            'Metric': [
                'Total Responses',
                'Non-Empty Responses',
                'Substantive Responses',
                'Satisfied Responses',
                'Mean Length (chars)',
                'Median Length (chars)'
            ],
            'Value': [
                results['total_responses'],
                results['non_empty'],
                results['response_types'].get('substantive', 0),
                results['response_types'].get('satisfied', 0),
                f"{results['length_stats']['mean']:.1f}",
                f"{results['length_stats']['median']:.1f}"
            ]
        })
        overview.to_excel(writer, sheet_name='Overview', index=False)

        # Sheet 2: Response Types
        resp_types_df = pd.DataFrame([
            {'Type': k, 'Count': v, 'Percentage': f"{v/sum(results['response_types'].values())*100:.1f}%"}
            for k, v in results['response_types'].items()
        ])
        resp_types_df.to_excel(writer, sheet_name='Response_Types', index=False)

        # Sheet 3: Themes
        themes_df = pd.DataFrame([
            {'Theme': k, 'Count': v, 'Percentage': f"{v/results['total_responses']*100:.1f}%"}
            for k, v in results['themes'].most_common()
        ])
        themes_df.to_excel(writer, sheet_name='Themes', index=False)

        # Sheet 4: Word Frequency
        words_df = pd.DataFrame(results['word_frequency'], columns=['Word', 'Count'])
        words_df.to_excel(writer, sheet_name='Word_Frequency', index=False)

        # Sheet 5: Bigrams
        bigrams_df = pd.DataFrame(results['bigram_frequency'], columns=['Bigram', 'Count'])
        bigrams_df.to_excel(writer, sheet_name='Bigrams', index=False)

        # Sheet 6: Sentiment
        sentiment_df = pd.DataFrame([
            {'Sentiment': k, 'Count': v, 'Percentage': f"{v/sum(results['sentiment'].values())*100:.1f}%"}
            for k, v in results['sentiment'].items()
        ])
        sentiment_df.to_excel(writer, sheet_name='Sentiment', index=False)

        # Sheet 7: TF-IDF
        if results['tfidf_keywords']:
            tfidf_df = pd.DataFrame(results['tfidf_keywords'], columns=['Keyword', 'TF-IDF Score'])
            tfidf_df.to_excel(writer, sheet_name='TFIDF_Keywords', index=False)

    print(f"✓ Excel report: reports/text_analysis/q22_detailed_analysis.xlsx")

    print()
    print("=" * 100)
    print("ENHANCED TEXT ANALYSIS COMPLETE".center(100))
    print("=" * 100)


if __name__ == '__main__':
    main()
