"""Data validation framework."""

import logging
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

import pandas as pd
import numpy as np
from pydantic import BaseModel, Field

from ..models.quality import (
    QualityRule,
    QualityViolation,
    QualityDimension,
    DataQualityMetrics,
    DimensionScore
)

logger = logging.getLogger(__name__)


class ValidationRule(BaseModel):
    """A validation rule for survey data."""

    rule_id: str = Field(..., description="Unique rule identifier")
    name: str = Field(..., description="Rule name")
    description: str = Field(..., description="Rule description")
    dimension: QualityDimension = Field(..., description="Quality dimension")
    severity: str = Field("warning", description="Severity level")

    # Rule function (not serializable, set separately)
    validator_func: Optional[Callable] = Field(None, exclude=True)

    class Config:
        arbitrary_types_allowed = True


class DataValidator:
    """
    Comprehensive data validator for survey responses.

    Performs validation across multiple quality dimensions:
    - Completeness
    - Accuracy
    - Consistency
    - Validity
    - Uniqueness
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize DataValidator.

        Args:
            config: Configuration dictionary with validation parameters
        """
        self.config = config or {}
        self.rules: List[ValidationRule] = []
        self.violations: List[QualityViolation] = []

        # Initialize default rules
        self._init_default_rules()

    def _init_default_rules(self):
        """Initialize default validation rules."""
        # Completeness rules
        self.add_rule(
            ValidationRule(
                rule_id="COMP_001",
                name="Minimum Completeness",
                description="Response must have minimum completeness threshold",
                dimension=QualityDimension.COMPLETENESS,
                severity="warning"
            ),
            self._check_min_completeness
        )

        # Validity rules
        self.add_rule(
            ValidationRule(
                rule_id="VALID_001",
                name="Region Validity",
                description="Region must be a valid Ukrainian region",
                dimension=QualityDimension.VALIDITY,
                severity="error"
            ),
            self._check_valid_region
        )

        self.add_rule(
            ValidationRule(
                rule_id="VALID_002",
                name="Grade Range",
                description="Grade must be between 1 and 11",
                dimension=QualityDimension.VALIDITY,
                severity="error"
            ),
            self._check_valid_grade
        )

        # Uniqueness rules
        self.add_rule(
            ValidationRule(
                rule_id="UNIQ_001",
                name="Duplicate Detection",
                description="Detect duplicate responses",
                dimension=QualityDimension.UNIQUENESS,
                severity="warning"
            ),
            self._check_duplicates
        )

        # Consistency rules
        self.add_rule(
            ValidationRule(
                rule_id="CONS_001",
                name="Timestamp Consistency",
                description="Timestamp must be within survey period",
                dimension=QualityDimension.CONSISTENCY,
                severity="warning"
            ),
            self._check_timestamp_range
        )

    def add_rule(self, rule: ValidationRule, validator_func: Callable):
        """
        Add a validation rule.

        Args:
            rule: ValidationRule instance
            validator_func: Function that performs validation
        """
        rule.validator_func = validator_func
        self.rules.append(rule)

    def validate(self, df: pd.DataFrame) -> DataQualityMetrics:
        """
        Validate entire dataset.

        Args:
            df: DataFrame to validate

        Returns:
            DataQualityMetrics with results
        """
        logger.info(f"Validating dataset with {len(df)} rows...")

        self.violations = []
        dimension_scores = {}

        # Group rules by dimension
        for dimension in QualityDimension:
            dimension_rules = [r for r in self.rules if r.dimension == dimension]

            if not dimension_rules:
                continue

            dimension_violations = []
            passed_checks = 0
            total_checks = len(dimension_rules) * len(df)

            # Run each rule
            for rule in dimension_rules:
                try:
                    rule_violations = rule.validator_func(df, rule)
                    dimension_violations.extend(rule_violations)
                    passed_checks += (len(df) - len(rule_violations))
                except Exception as e:
                    logger.error(f"Error running rule {rule.rule_id}: {e}")

            # Calculate dimension score
            score = (passed_checks / total_checks * 100) if total_checks > 0 else 100

            dimension_scores[dimension] = DimensionScore(
                dimension=dimension,
                score=score,
                weight=self._get_dimension_weight(dimension),
                total_checks=total_checks,
                passed_checks=passed_checks,
                failed_checks=total_checks - passed_checks,
                violations=dimension_violations
            )

            self.violations.extend(dimension_violations)

        # Create quality metrics
        metrics = self._create_quality_metrics(df, list(dimension_scores.values()))

        logger.info(f"Validation complete. Overall score: {metrics.overall_score:.2f}")
        return metrics

    def _get_dimension_weight(self, dimension: QualityDimension) -> float:
        """Get weight for a quality dimension."""
        weights = {
            QualityDimension.COMPLETENESS: 0.25,
            QualityDimension.ACCURACY: 0.30,
            QualityDimension.CONSISTENCY: 0.20,
            QualityDimension.TIMELINESS: 0.10,
            QualityDimension.VALIDITY: 0.15,
        }
        return weights.get(dimension, 0.10)

    def _create_quality_metrics(
        self,
        df: pd.DataFrame,
        dimension_scores: List[DimensionScore]
    ) -> DataQualityMetrics:
        """Create comprehensive quality metrics."""
        metrics = DataQualityMetrics(
            dimension_scores=dimension_scores,
            all_violations=self.violations,
            total_records=len(df)
        )

        # Calculate completeness
        completeness_by_field = ((df.notna().sum() / len(df)) * 100).to_dict()
        metrics.completeness = completeness_by_field
        metrics.overall_completeness = sum(completeness_by_field.values()) / len(completeness_by_field)

        # Calculate validity
        valid_records = len(df) - len([v for v in self.violations if v.severity in ['error', 'critical']])
        metrics.valid_records = max(0, valid_records)
        metrics.invalid_records = len(df) - metrics.valid_records
        metrics.accuracy_rate = (metrics.valid_records / len(df) * 100) if len(df) > 0 else 0

        # Calculate uniqueness
        duplicates = df.duplicated().sum()
        metrics.duplicate_records = int(duplicates)
        metrics.uniqueness_rate = ((len(df) - duplicates) / len(df) * 100) if len(df) > 0 else 100

        # Calculate overall score
        metrics.calculate_overall_score()

        return metrics

    # Validation rule implementations

    def _check_min_completeness(
        self,
        df: pd.DataFrame,
        rule: ValidationRule
    ) -> List[QualityViolation]:
        """Check minimum completeness threshold."""
        violations = []
        min_threshold = self.config.get('min_response_completeness', 0.7)

        for idx, row in df.iterrows():
            completeness = row.notna().sum() / len(row)
            if completeness < min_threshold:
                violations.append(QualityViolation(
                    violation_id=f"{rule.rule_id}_{idx}",
                    rule_id=rule.rule_id,
                    record_id=str(idx),
                    actual_value=completeness,
                    expected_value=min_threshold,
                    severity=rule.severity,
                    message=f"Response completeness ({completeness:.2%}) below threshold ({min_threshold:.2%})"
                ))

        return violations

    def _check_valid_region(
        self,
        df: pd.DataFrame,
        rule: ValidationRule
    ) -> List[QualityViolation]:
        """Check if region is valid."""
        violations = []

        valid_regions = {
            "Вінницька", "Волинська", "Дніпропетровська", "Донецька",
            "Житомирська", "Закарпатська", "Запорізька", "Івано-Франківська",
            "Київська", "Кіровоградська", "Луганська", "Львівська",
            "Миколаївська", "Одеська", "Полтавська", "Рівненська",
            "Сумська", "Тернопільська", "Харківська", "Херсонська",
            "Хмельницька", "Черкаська", "Чернівецька", "Чернігівська",
            "м. Київ"
        }

        # Find region column
        region_cols = [col for col in df.columns if 'област' in col.lower() or 'region' in col.lower()]

        if not region_cols:
            return violations

        region_col = region_cols[0]

        for idx, value in df[region_col].items():
            if pd.notna(value) and value not in valid_regions:
                violations.append(QualityViolation(
                    violation_id=f"{rule.rule_id}_{idx}",
                    rule_id=rule.rule_id,
                    record_id=str(idx),
                    field_name=region_col,
                    actual_value=value,
                    expected_value="Valid Ukrainian region",
                    severity=rule.severity,
                    message=f"Invalid region: {value}"
                ))

        return violations

    def _check_valid_grade(
        self,
        df: pd.DataFrame,
        rule: ValidationRule
    ) -> List[QualityViolation]:
        """Check if grade is within valid range."""
        violations = []

        # Find grade column
        grade_cols = [col for col in df.columns if 'клас' in col.lower() or 'grade' in col.lower()]

        if not grade_cols:
            return violations

        grade_col = grade_cols[0]

        for idx, value in df[grade_col].items():
            if pd.notna(value):
                try:
                    grade = int(value)
                    if grade < 1 or grade > 11:
                        violations.append(QualityViolation(
                            violation_id=f"{rule.rule_id}_{idx}",
                            rule_id=rule.rule_id,
                            record_id=str(idx),
                            field_name=grade_col,
                            actual_value=grade,
                            expected_value="1-11",
                            severity=rule.severity,
                            message=f"Grade {grade} out of valid range (1-11)"
                        ))
                except (ValueError, TypeError):
                    violations.append(QualityViolation(
                        violation_id=f"{rule.rule_id}_{idx}",
                        rule_id=rule.rule_id,
                        record_id=str(idx),
                        field_name=grade_col,
                        actual_value=value,
                        expected_value="Numeric 1-11",
                        severity=rule.severity,
                        message=f"Grade must be numeric: {value}"
                    ))

        return violations

    def _check_duplicates(
        self,
        df: pd.DataFrame,
        rule: ValidationRule
    ) -> List[QualityViolation]:
        """Check for duplicate responses."""
        violations = []

        duplicates = df[df.duplicated(keep=False)]

        for idx in duplicates.index:
            violations.append(QualityViolation(
                violation_id=f"{rule.rule_id}_{idx}",
                rule_id=rule.rule_id,
                record_id=str(idx),
                severity=rule.severity,
                message=f"Duplicate response detected"
            ))

        return violations

    def _check_timestamp_range(
        self,
        df: pd.DataFrame,
        rule: ValidationRule
    ) -> List[QualityViolation]:
        """Check if timestamps are within survey period."""
        violations = []

        # Survey period: October 7-18, 2024
        survey_start = pd.Timestamp('2024-10-07')
        survey_end = pd.Timestamp('2024-10-18 23:59:59')

        # Find timestamp column
        timestamp_cols = [col for col in df.columns if 'час' in col.lower() or 'timestamp' in col.lower()]

        if not timestamp_cols:
            return violations

        timestamp_col = timestamp_cols[0]

        for idx, value in df[timestamp_col].items():
            if pd.notna(value):
                try:
                    ts = pd.Timestamp(value)
                    if ts < survey_start or ts > survey_end:
                        violations.append(QualityViolation(
                            violation_id=f"{rule.rule_id}_{idx}",
                            rule_id=rule.rule_id,
                            record_id=str(idx),
                            field_name=timestamp_col,
                            actual_value=str(ts),
                            expected_value=f"{survey_start} to {survey_end}",
                            severity=rule.severity,
                            message=f"Timestamp outside survey period"
                        ))
                except:
                    pass

        return violations

    def get_violations_summary(self) -> pd.DataFrame:
        """Get summary of violations."""
        if not self.violations:
            return pd.DataFrame()

        summary_data = []
        for v in self.violations:
            summary_data.append({
                'rule_id': v.rule_id,
                'record_id': v.record_id,
                'field': v.field_name,
                'severity': v.severity,
                'message': v.message,
                'actual': v.actual_value,
                'expected': v.expected_value
            })

        return pd.DataFrame(summary_data)
