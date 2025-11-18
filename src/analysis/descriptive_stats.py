"""Descriptive statistics module for survey analysis."""

import logging
from typing import Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
from scipy import stats

logger = logging.getLogger(__name__)


class DescriptiveAnalyzer:
    """
    Comprehensive descriptive statistics analyzer.

    Provides:
    - Frequency distributions
    - Cross-tabulations
    - Summary statistics
    - Missing data analysis
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize analyzer.

        Args:
            df: DataFrame with survey data
        """
        self.df = df
        self.results = {}

    def analyze_all(self) -> Dict:
        """Run all descriptive analyses."""
        logger.info("Running comprehensive descriptive analysis...")

        self.results = {
            'frequencies': self.calculate_frequencies(),
            'crosstabs': self.calculate_crosstabs(),
            'summary_stats': self.calculate_summary_stats(),
            'missing_analysis': self.analyze_missing_data(),
        }

        return self.results

    def calculate_frequencies(self, columns: Optional[List[str]] = None) -> Dict:
        """
        Calculate frequency distributions for categorical variables.

        Args:
            columns: Specific columns to analyze (None = all categorical)

        Returns:
            Dictionary of frequency tables
        """
        if columns is None:
            # Auto-detect categorical columns
            columns = self.df.select_dtypes(include=['object', 'category']).columns.tolist()

        frequencies = {}

        for col in columns:
            if col not in self.df.columns:
                continue

            freq_table = self.df[col].value_counts()
            freq_pct = self.df[col].value_counts(normalize=True) * 100

            frequencies[col] = pd.DataFrame({
                'count': freq_table,
                'percentage': freq_pct
            }).round(2)

        logger.info(f"Calculated frequencies for {len(frequencies)} columns")
        return frequencies

    def calculate_crosstabs(self) -> Dict:
        """
        Calculate key cross-tabulations.

        Returns:
            Dictionary of cross-tabulation tables
        """
        crosstabs = {}

        # Find relevant columns
        region_col = self._find_column(['област', 'region'])
        settlement_col = self._find_column(['населен', 'settlement'])
        school_col = self._find_column(['заклад', 'school', 'тип'])
        grade_col = self._find_column(['клас', 'grade'])
        format_col = self._find_column(['формат', 'format', 'навчання', 'learning'])

        # Region × Educational format
        if region_col and format_col:
            ct = pd.crosstab(
                self.df[region_col],
                self.df[format_col],
                margins=True,
                normalize='index'
            ) * 100
            crosstabs['region_x_format'] = ct.round(2)

        # School type × Grade
        if school_col and grade_col:
            ct = pd.crosstab(
                self.df[school_col],
                self.df[grade_col],
                margins=True
            )
            crosstabs['school_x_grade'] = ct

        # Settlement type × School type
        if settlement_col and school_col:
            ct = pd.crosstab(
                self.df[settlement_col],
                self.df[school_col],
                margins=True,
                normalize='index'
            ) * 100
            crosstabs['settlement_x_school'] = ct.round(2)

        logger.info(f"Calculated {len(crosstabs)} cross-tabulations")
        return crosstabs

    def calculate_summary_stats(self) -> Dict:
        """
        Calculate summary statistics for numeric variables.

        Returns:
            Dictionary of summary statistics
        """
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()

        if not numeric_cols:
            return {}

        summary = {}

        for col in numeric_cols:
            summary[col] = {
                'count': int(self.df[col].count()),
                'mean': float(self.df[col].mean()),
                'std': float(self.df[col].std()),
                'min': float(self.df[col].min()),
                'q25': float(self.df[col].quantile(0.25)),
                'median': float(self.df[col].median()),
                'q75': float(self.df[col].quantile(0.75)),
                'max': float(self.df[col].max()),
                'skewness': float(stats.skew(self.df[col].dropna())),
                'kurtosis': float(stats.kurtosis(self.df[col].dropna())),
            }

        return summary

    def analyze_missing_data(self) -> Dict:
        """
        Analyze missing data patterns.

        Returns:
            Dictionary with missing data analysis
        """
        missing_count = self.df.isna().sum()
        missing_pct = (missing_count / len(self.df)) * 100

        analysis = {
            'missing_by_column': pd.DataFrame({
                'missing_count': missing_count,
                'missing_percentage': missing_pct
            }).round(2),
            'total_missing': int(missing_count.sum()),
            'rows_with_missing': int(self.df.isna().any(axis=1).sum()),
            'complete_rows': int(self.df.notna().all(axis=1).sum()),
        }

        return analysis

    def get_response_rate_by_region(self) -> pd.DataFrame:
        """Calculate response rates by region."""
        region_col = self._find_column(['област', 'region'])

        if not region_col:
            return pd.DataFrame()

        region_counts = self.df[region_col].value_counts()
        region_pct = (region_counts / region_counts.sum()) * 100

        return pd.DataFrame({
            'responses': region_counts,
            'percentage': region_pct.round(2)
        }).sort_values('responses', ascending=False)

    def _find_column(self, keywords: List[str]) -> Optional[str]:
        """Find column matching keywords."""
        for col in self.df.columns:
            col_lower = col.lower()
            if any(kw in col_lower for kw in keywords):
                return col
        return None

    def export_results(self, output_path: str):
        """Export results to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Write frequencies
            for col, freq_table in self.results.get('frequencies', {}).items():
                sheet_name = f"Freq_{col[:25]}"
                freq_table.to_excel(writer, sheet_name=sheet_name)

            # Write crosstabs
            for name, crosstab in self.results.get('crosstabs', {}).items():
                crosstab.to_excel(writer, sheet_name=name[:31])

            # Write summary stats
            if self.results.get('summary_stats'):
                pd.DataFrame(self.results['summary_stats']).T.to_excel(
                    writer,
                    sheet_name='Summary_Statistics'
                )

            # Write missing analysis
            if self.results.get('missing_analysis'):
                self.results['missing_analysis']['missing_by_column'].to_excel(
                    writer,
                    sheet_name='Missing_Data'
                )

        logger.info(f"Results exported to {output_path}")
