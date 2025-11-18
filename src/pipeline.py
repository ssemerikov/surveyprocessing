"""Main analysis pipeline for Ukrainian Education Survey."""

import logging
from pathlib import Path
from typing import Dict, Optional, Union
from datetime import datetime

import pandas as pd
import yaml

from .ingestion.data_loader import DataLoader
from .validation.validator import DataValidator
from .analysis.descriptive_stats import DescriptiveAnalyzer
from .analysis.text_analysis import UkrainianTextAnalyzer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class SurveyAnalysisPipeline:
    """
    Comprehensive analysis pipeline for Ukrainian education survey data.

    This pipeline orchestrates the entire analysis workflow:
    1. Data loading with Ukrainian text support
    2. Data validation and quality assessment
    3. Descriptive statistics analysis
    4. Regional analysis
    5. Digital environment analysis
    6. Text analysis of open-ended responses
    7. Statistical testing
    8. Report generation
    9. Dashboard creation
    """

    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the analysis pipeline.

        Args:
            config_path: Path to YAML configuration file
        """
        self.config_path = config_path or 'config/config.yaml'
        self.config = self._load_config()

        # Pipeline components
        self.data_loader: Optional[DataLoader] = None
        self.validator: Optional[DataValidator] = None
        self.df: Optional[pd.DataFrame] = None

        # Analysis results
        self.results = {}
        self.quality_metrics = None

        # Initialize data loader
        self.data_loader = DataLoader(
            encoding=self.config['data']['input']['encoding'],
            language=self.config['data']['input']['language'],
            create_translations=True,
            validate_on_load=True
        )

        # Initialize validator
        self.validator = DataValidator(config=self.config['data']['validation'])

        logger.info("Survey Analysis Pipeline initialized")

    def _load_config(self) -> Dict:
        """Load configuration from YAML file."""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file not found: {self.config_path}. Using defaults.")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Get default configuration."""
        return {
            'data': {
                'input': {
                    'encoding': 'utf-8',
                    'language': 'uk'
                },
                'validation': {
                    'min_response_completeness': 0.7
                }
            },
            'analysis': {
                'text_analysis': {
                    'min_word_length': 3,
                    'n_topics': 10
                }
            }
        }

    def load_data(
        self,
        file_path: Union[str, Path],
        file_type: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load survey data from file.

        Args:
            file_path: Path to data file (CSV, TSV, or XLSX)
            file_type: File type ('csv', 'tsv', 'xlsx', or None for auto-detect)

        Returns:
            Loaded DataFrame
        """
        logger.info(f"Loading data from {file_path}")

        if file_type:
            if file_type.lower() == 'csv':
                self.df = self.data_loader.load_csv(file_path)
            elif file_type.lower() == 'tsv':
                self.df = self.data_loader.load_tsv(file_path)
            elif file_type.lower() == 'xlsx':
                self.df = self.data_loader.load_xlsx(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
        else:
            self.df = self.data_loader.load_auto(file_path)

        logger.info(f"Data loaded: {len(self.df)} rows, {len(self.df.columns)} columns")

        # Create derived variables
        self.data_loader.create_derived_variables()

        return self.df

    def validate_data(self) -> Dict:
        """
        Validate loaded data and assess quality.

        Returns:
            Dictionary with validation results
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        logger.info("Validating data...")

        self.quality_metrics = self.validator.validate(self.df)

        validation_results = {
            'quality_metrics': self.quality_metrics,
            'violations': self.validator.get_violations_summary(),
            'summary': self.quality_metrics.get_summary()
        }

        logger.info(f"Validation complete. Quality grade: {self.quality_metrics.quality_grade}")

        return validation_results

    def run_descriptive_analysis(self) -> Dict:
        """
        Run descriptive statistics analysis.

        Returns:
            Dictionary with descriptive analysis results
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        logger.info("Running descriptive analysis...")

        analyzer = DescriptiveAnalyzer(self.df)
        results = analyzer.analyze_all()

        # Add response rate by region
        results['response_rate_by_region'] = analyzer.get_response_rate_by_region()

        self.results['descriptive'] = results

        logger.info("Descriptive analysis complete")
        return results

    def run_text_analysis(self, text_column: Optional[str] = None) -> Dict:
        """
        Run text analysis on open-ended responses.

        Args:
            text_column: Column name with text responses (auto-detected if None)

        Returns:
            Dictionary with text analysis results
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        # Find text column if not specified
        if text_column is None:
            # Look for column with suggestions/comments
            text_cols = [col for col in self.df.columns if
                        'пропозиц' in col.lower() or
                        'коментар' in col.lower() or
                        'suggest' in col.lower()]

            if not text_cols:
                logger.warning("No text column found for analysis")
                return {}

            text_column = text_cols[0]

        logger.info(f"Running text analysis on column: {text_column}")

        analyzer = UkrainianTextAnalyzer(
            self.df[text_column],
            min_word_length=self.config['analysis'].get('text_analysis', {}).get('min_word_length', 3)
        )

        results = analyzer.analyze_all()

        self.results['text_analysis'] = results

        logger.info("Text analysis complete")
        return results

    def run_analysis(self) -> Dict:
        """
        Run complete analysis pipeline.

        Returns:
            Dictionary with all analysis results
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_data() first.")

        logger.info("=" * 80)
        logger.info("RUNNING COMPREHENSIVE SURVEY ANALYSIS")
        logger.info("=" * 80)

        # 1. Data validation
        logger.info("\n[1/3] Validating data...")
        validation_results = self.validate_data()

        # 2. Descriptive analysis
        logger.info("\n[2/3] Running descriptive analysis...")
        descriptive_results = self.run_descriptive_analysis()

        # 3. Text analysis
        logger.info("\n[3/3] Running text analysis...")
        text_results = self.run_text_analysis()

        # Compile all results
        all_results = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_responses': len(self.df),
                'columns': len(self.df.columns),
            },
            'validation': validation_results,
            'descriptive': descriptive_results,
            'text_analysis': text_results,
        }

        self.results = all_results

        logger.info("\n" + "=" * 80)
        logger.info("ANALYSIS COMPLETE")
        logger.info("=" * 80)
        logger.info(f"Total responses analyzed: {len(self.df)}")
        logger.info(f"Data quality grade: {validation_results['summary']['quality_grade']}")
        logger.info("=" * 80 + "\n")

        return all_results

    def generate_reports(
        self,
        output_dir: Union[str, Path],
        formats: Optional[list] = None
    ):
        """
        Generate analysis reports.

        Args:
            output_dir: Directory to save reports
            formats: List of formats ('excel', 'pdf', 'html')
        """
        if not self.results:
            raise ValueError("No results available. Run run_analysis() first.")

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        formats = formats or ['excel']

        logger.info(f"Generating reports in {output_path}")

        # Generate Excel reports
        if 'excel' in formats:
            self._generate_excel_report(output_path / 'analysis_results.xlsx')

        # Generate summary report
        self._generate_summary_report(output_path / 'summary.txt')

        logger.info("Reports generated successfully")

    def _generate_excel_report(self, output_path: Path):
        """Generate comprehensive Excel report."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Overview
            overview_data = {
                'Metric': ['Total Responses', 'Quality Grade', 'Completeness', 'Analysis Date'],
                'Value': [
                    self.results['metadata']['total_responses'],
                    self.results['validation']['summary']['quality_grade'],
                    f"{self.results['validation']['summary']['completeness']:.2f}%",
                    self.results['metadata']['analysis_date']
                ]
            }
            pd.DataFrame(overview_data).to_excel(writer, sheet_name='Overview', index=False)

            # Descriptive stats - frequencies
            freq_data = []
            for col, freq_table in self.results['descriptive'].get('frequencies', {}).items():
                freq_table_copy = freq_table.copy()
                freq_table_copy['column'] = col
                freq_data.append(freq_table_copy)

            if freq_data:
                pd.concat(freq_data).to_excel(writer, sheet_name='Frequencies')

            # Text analysis
            if 'text_analysis' in self.results and self.results['text_analysis']:
                # Word frequencies
                if 'word_frequencies' in self.results['text_analysis']:
                    self.results['text_analysis']['word_frequencies'].to_excel(
                        writer,
                        sheet_name='Word_Frequencies',
                        index=False
                    )

                # Themes
                if 'themes' in self.results['text_analysis']:
                    pd.DataFrame(
                        list(self.results['text_analysis']['themes'].items()),
                        columns=['Theme', 'Count']
                    ).to_excel(writer, sheet_name='Themes', index=False)

        logger.info(f"Excel report saved to {output_path}")

    def _generate_summary_report(self, output_path: Path):
        """Generate text summary report."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("UKRAINIAN EDUCATION SURVEY - ANALYSIS SUMMARY\n")
            f.write("=" * 80 + "\n\n")

            # Metadata
            f.write(f"Analysis Date: {self.results['metadata']['analysis_date']}\n")
            f.write(f"Total Responses: {self.results['metadata']['total_responses']}\n")
            f.write(f"Data Quality Grade: {self.results['validation']['summary']['quality_grade']}\n")
            f.write(f"Overall Quality Score: {self.results['validation']['summary']['overall_score']:.2f}/100\n")
            f.write("\n" + "-" * 80 + "\n\n")

            # Quality metrics
            f.write("DATA QUALITY METRICS:\n")
            f.write(f"  Completeness: {self.results['validation']['summary']['completeness']:.2f}%\n")
            f.write(f"  Accuracy Rate: {self.results['validation']['summary']['accuracy_rate']:.2f}%\n")
            f.write(f"  Uniqueness Rate: {self.results['validation']['summary']['uniqueness_rate']:.2f}%\n")
            f.write(f"  Total Violations: {self.results['validation']['summary']['total_violations']}\n")
            f.write("\n" + "-" * 80 + "\n\n")

            # Text analysis summary
            if 'text_analysis' in self.results and self.results['text_analysis']:
                stats = self.results['text_analysis'].get('statistics', {})
                f.write("TEXT ANALYSIS SUMMARY:\n")
                f.write(f"  Total Responses: {stats.get('total_responses', 0)}\n")
                f.write(f"  Total Words: {stats.get('total_words', 0)}\n")
                f.write(f"  Unique Words: {stats.get('unique_words', 0)}\n")
                f.write(f"  Avg Words/Response: {stats.get('avg_words_per_response', 0):.2f}\n")

                # Top themes
                if 'themes' in self.results['text_analysis']:
                    f.write("\n  Top Themes:\n")
                    themes = sorted(
                        self.results['text_analysis']['themes'].items(),
                        key=lambda x: x[1],
                        reverse=True
                    )
                    for theme, count in themes[:10]:
                        f.write(f"    - {theme}: {count} responses\n")

            f.write("\n" + "=" * 80 + "\n")

        logger.info(f"Summary report saved to {output_path}")

    def export_data(self, output_path: Union[str, Path]):
        """Export processed data."""
        if self.df is None:
            raise ValueError("No data loaded.")

        self.data_loader.export_data(output_path)

    def get_summary(self) -> Dict:
        """Get quick summary of dataset."""
        if self.df is None:
            raise ValueError("No data loaded.")

        return self.data_loader.get_data_summary()
