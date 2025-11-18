"""Data loading module with Ukrainian text support."""

import logging
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import pandas as pd
import numpy as np
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class DataFormat(str, Enum):
    """Supported data formats."""

    CSV = "csv"
    TSV = "tsv"
    XLSX = "xlsx"
    JSON = "json"


class ColumnMapping(BaseModel):
    """Mapping between Ukrainian and English column names."""

    ukrainian: str = Field(..., description="Ukrainian column name")
    english: str = Field(..., description="English column name")
    question_number: Optional[int] = Field(None, description="Question number if applicable")
    data_type: str = Field("string", description="Expected data type")
    category: Optional[str] = Field(None, description="Question category")


class DataLoader:
    """
    Comprehensive data loader for Ukrainian education survey data.

    Handles:
    - Multi-format loading (CSV, TSV, XLSX)
    - Proper UTF-8 encoding for Ukrainian text
    - Column name translation
    - Data type standardization
    - Multiple-choice question parsing
    - Timestamp parsing
    - Missing data handling
    """

    def __init__(
        self,
        encoding: str = 'utf-8',
        language: str = 'uk',
        create_translations: bool = True,
        validate_on_load: bool = True
    ):
        """
        Initialize DataLoader.

        Args:
            encoding: Character encoding (default: utf-8)
            language: Primary language code (default: uk for Ukrainian)
            create_translations: Whether to create English column names
            validate_on_load: Whether to validate data during loading
        """
        self.encoding = encoding
        self.language = language
        self.create_translations = create_translations
        self.validate_on_load = validate_on_load

        self.df: Optional[pd.DataFrame] = None
        self.column_mappings: List[ColumnMapping] = []
        self.metadata: Dict = {}

        # Initialize column mappings
        self._init_column_mappings()

    def _init_column_mappings(self):
        """Initialize Ukrainian to English column mappings."""
        # This will be populated based on actual survey structure
        # For now, creating template structure
        self.default_mappings = {
            'Позначка часу': 'timestamp',
            'Область': 'region',
            'Тип населеного пункту': 'settlement_type',
            'Тип закладу освіти': 'school_type',
            'Клас': 'grade',
            'Кількість дітей': 'children_count',
        }

    def load_csv(
        self,
        file_path: Union[str, Path],
        delimiter: str = ',',
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from CSV file.

        Args:
            file_path: Path to CSV file
            delimiter: CSV delimiter (default: comma)
            **kwargs: Additional arguments for pd.read_csv

        Returns:
            Loaded DataFrame
        """
        logger.info(f"Loading CSV file: {file_path}")

        try:
            self.df = pd.read_csv(
                file_path,
                encoding=self.encoding,
                delimiter=delimiter,
                **kwargs
            )
            logger.info(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")

            self._post_load_processing()
            return self.df

        except UnicodeDecodeError as e:
            logger.error(f"Encoding error: {e}. Trying alternative encoding...")
            # Try cp1251 (common in Ukrainian Windows systems)
            self.df = pd.read_csv(
                file_path,
                encoding='cp1251',
                delimiter=delimiter,
                **kwargs
            )
            self._post_load_processing()
            return self.df

    def load_tsv(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """Load data from TSV file."""
        logger.info(f"Loading TSV file: {file_path}")
        return self.load_csv(file_path, delimiter='\t', **kwargs)

    def load_xlsx(
        self,
        file_path: Union[str, Path],
        sheet_name: Union[str, int] = 0,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load data from Excel file.

        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name or index
            **kwargs: Additional arguments for pd.read_excel

        Returns:
            Loaded DataFrame
        """
        logger.info(f"Loading Excel file: {file_path}, sheet: {sheet_name}")

        self.df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            engine='openpyxl',
            **kwargs
        )

        logger.info(f"Loaded {len(self.df)} rows, {len(self.df.columns)} columns")
        self._post_load_processing()
        return self.df

    def load_auto(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        Auto-detect format and load data.

        Args:
            file_path: Path to data file
            **kwargs: Additional loading arguments

        Returns:
            Loaded DataFrame
        """
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == '.csv':
            return self.load_csv(file_path, **kwargs)
        elif suffix == '.tsv':
            return self.load_tsv(file_path, **kwargs)
        elif suffix in ['.xlsx', '.xls']:
            return self.load_xlsx(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    def _post_load_processing(self):
        """Perform post-load processing."""
        if self.df is None:
            return

        # Clean column names
        self.df.columns = self.df.columns.str.strip()

        # Create English column names if requested
        if self.create_translations:
            self._create_english_columns()

        # Parse timestamps
        self._parse_timestamps()

        # Handle missing data
        self._handle_missing_data()

        # Standardize data types
        self._standardize_types()

        # Create metadata
        self._create_metadata()

        # Validate if requested
        if self.validate_on_load:
            self._validate_data()

    def _create_english_columns(self):
        """Create English column name mappings."""
        logger.info("Creating English column names...")

        # Create mapping dictionary
        self.column_map_dict = {}

        for uk_col in self.df.columns:
            # Check if we have a predefined mapping
            if uk_col in self.default_mappings:
                en_col = self.default_mappings[uk_col]
            else:
                # Create transliterated version
                en_col = self._transliterate_column(uk_col)

            self.column_map_dict[uk_col] = en_col

            # Store mapping
            self.column_mappings.append(
                ColumnMapping(ukrainian=uk_col, english=en_col)
            )

        # Store original columns
        self.df.attrs['original_columns'] = self.df.columns.tolist()

    def _transliterate_column(self, col_name: str) -> str:
        """
        Transliterate Ukrainian column name to English.

        Args:
            col_name: Ukrainian column name

        Returns:
            English transliterated name
        """
        # Simple transliteration map
        translit_map = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g',
            'д': 'd', 'е': 'e', 'є': 'ye', 'ж': 'zh', 'з': 'z',
            'и': 'y', 'і': 'i', 'ї': 'yi', 'й': 'y', 'к': 'k',
            'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
            'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
            'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ь': '', 'ю': 'yu', 'я': 'ya',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G',
            'Д': 'D', 'Е': 'E', 'Є': 'Ye', 'Ж': 'Zh', 'З': 'Z',
            'И': 'Y', 'І': 'I', 'Ї': 'Yi', 'Й': 'Y', 'К': 'K',
            'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
            'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
            'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
            'Ь': '', 'Ю': 'Yu', 'Я': 'Ya'
        }

        result = []
        for char in col_name:
            if char in translit_map:
                result.append(translit_map[char])
            elif char.isalnum() or char in ['_', '-']:
                result.append(char)
            else:
                result.append('_')

        # Clean up the result
        transliterated = ''.join(result)
        transliterated = transliterated.strip('_').lower()
        transliterated = '_'.join(transliterated.split())  # Replace spaces with underscores

        return transliterated

    def _parse_timestamps(self):
        """Parse timestamp columns."""
        timestamp_cols = [col for col in self.df.columns if 'час' in col.lower() or 'timestamp' in col.lower()]

        for col in timestamp_cols:
            try:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                logger.info(f"Parsed timestamp column: {col}")
            except Exception as e:
                logger.warning(f"Could not parse {col} as timestamp: {e}")

    def _handle_missing_data(self):
        """Handle missing data appropriately."""
        # Calculate missing percentages
        missing_pct = (self.df.isna().sum() / len(self.df)) * 100
        self.metadata['missing_percentages'] = missing_pct.to_dict()

        # Log columns with high missing rates
        high_missing = missing_pct[missing_pct > 20]
        if len(high_missing) > 0:
            logger.warning(f"Columns with >20% missing: {high_missing.to_dict()}")

    def _standardize_types(self):
        """Standardize data types."""
        # Try to convert numeric columns
        for col in self.df.columns:
            if self.df[col].dtype == 'object':
                # Try numeric conversion
                try:
                    numeric_col = pd.to_numeric(self.df[col], errors='coerce')
                    if numeric_col.notna().sum() / len(self.df) > 0.9:  # If >90% converts
                        self.df[col] = numeric_col
                except:
                    pass

    def _create_metadata(self):
        """Create metadata about the dataset."""
        self.metadata.update({
            'rows': len(self.df),
            'columns': len(self.df.columns),
            'column_names': self.df.columns.tolist(),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'loaded_at': datetime.now().isoformat(),
            'memory_usage_mb': self.df.memory_usage(deep=True).sum() / 1024**2,
        })

    def _validate_data(self):
        """Perform basic validation."""
        logger.info("Validating data...")

        # Check for completely empty rows
        empty_rows = self.df.isna().all(axis=1).sum()
        if empty_rows > 0:
            logger.warning(f"Found {empty_rows} completely empty rows")

        # Check for duplicate rows
        duplicates = self.df.duplicated().sum()
        if duplicates > 0:
            logger.warning(f"Found {duplicates} duplicate rows")
            self.metadata['duplicates'] = int(duplicates)

    def parse_multiple_choice(
        self,
        column: str,
        delimiter: str = ',',
        strip: bool = True
    ) -> pd.Series:
        """
        Parse multiple-choice responses that are concatenated strings.

        Args:
            column: Column name to parse
            delimiter: Delimiter used to separate choices
            strip: Whether to strip whitespace from choices

        Returns:
            Series with lists of choices
        """
        if column not in self.df.columns:
            raise ValueError(f"Column {column} not found")

        def parse_row(value):
            if pd.isna(value):
                return []
            choices = str(value).split(delimiter)
            if strip:
                choices = [c.strip() for c in choices]
            return [c for c in choices if c]  # Remove empty strings

        return self.df[column].apply(parse_row)

    def create_derived_variables(self):
        """Create derived variables for analysis."""
        logger.info("Creating derived variables...")

        # Age groups (if applicable)
        if 'age' in self.df.columns:
            self.df['age_group'] = pd.cut(
                self.df['age'],
                bins=[0, 6, 10, 14, 18, 100],
                labels=['1-6', '7-10', '11-14', '15-18', '18+']
            )

        # School level from grade
        if any('клас' in col.lower() or 'grade' in col.lower() for col in self.df.columns):
            grade_col = [col for col in self.df.columns if 'клас' in col.lower() or 'grade' in col.lower()][0]

            def get_school_level(grade):
                if pd.isna(grade):
                    return None
                grade_num = int(grade) if isinstance(grade, (int, float)) else None
                if grade_num is None:
                    return None
                if 1 <= grade_num <= 4:
                    return 'початкова'  # elementary
                elif 5 <= grade_num <= 9:
                    return 'базова'  # middle
                elif 10 <= grade_num <= 11:
                    return 'профільна'  # high
                return None

            self.df['school_level'] = self.df[grade_col].apply(get_school_level)

    def get_data_summary(self) -> Dict:
        """Get summary of loaded data."""
        if self.df is None:
            return {}

        summary = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage_mb': round(self.df.memory_usage(deep=True).sum() / 1024**2, 2),
            'columns': self.df.columns.tolist(),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'missing_data': self.df.isna().sum().to_dict(),
            'duplicates': int(self.df.duplicated().sum()),
        }

        return summary

    def get_data_dictionary(self) -> pd.DataFrame:
        """Create a data dictionary with column information."""
        if self.df is None:
            return pd.DataFrame()

        dictionary = []
        for col in self.df.columns:
            info = {
                'column_name': col,
                'data_type': str(self.df[col].dtype),
                'non_null_count': int(self.df[col].notna().sum()),
                'null_count': int(self.df[col].isna().sum()),
                'null_percentage': round((self.df[col].isna().sum() / len(self.df)) * 100, 2),
                'unique_values': int(self.df[col].nunique()),
                'sample_values': self.df[col].dropna().head(3).tolist()
            }
            dictionary.append(info)

        return pd.DataFrame(dictionary)

    def export_data(
        self,
        output_path: Union[str, Path],
        format: Optional[DataFormat] = None,
        **kwargs
    ):
        """Export loaded data to file."""
        if self.df is None:
            raise ValueError("No data loaded to export")

        path = Path(output_path)

        if format is None:
            # Auto-detect from extension
            suffix = path.suffix.lower()
            if suffix == '.csv':
                format = DataFormat.CSV
            elif suffix == '.xlsx':
                format = DataFormat.XLSX
            elif suffix == '.json':
                format = DataFormat.JSON
            else:
                raise ValueError(f"Cannot determine format from extension: {suffix}")

        if format == DataFormat.CSV:
            self.df.to_csv(path, encoding=self.encoding, index=False, **kwargs)
        elif format == DataFormat.XLSX:
            self.df.to_excel(path, engine='openpyxl', index=False, **kwargs)
        elif format == DataFormat.JSON:
            self.df.to_json(path, orient='records', force_ascii=False, indent=2, **kwargs)

        logger.info(f"Data exported to: {path}")
