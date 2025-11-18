"""Data quality models and metrics."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class QualityDimension(str, Enum):
    """Dimensions of data quality."""

    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    TIMELINESS = "timeliness"
    VALIDITY = "validity"
    UNIQUENESS = "uniqueness"


class QualityRule(BaseModel):
    """A data quality validation rule."""

    rule_id: str = Field(..., description="Unique rule identifier")
    rule_name: str = Field(..., description="Human-readable rule name")
    dimension: QualityDimension = Field(..., description="Quality dimension")

    # Rule definition
    description: str = Field(..., description="Rule description")
    severity: str = Field("warning", description="Severity: info, warning, error, critical")

    # Rule parameters
    threshold: Optional[float] = Field(None, description="Threshold value")
    expected_value: Optional[any] = Field(None, description="Expected value")

    # Rule status
    is_active: bool = Field(True, description="Whether rule is active")

    class Config:
        use_enum_values = True


class QualityViolation(BaseModel):
    """A violation of a quality rule."""

    violation_id: str = Field(..., description="Unique violation identifier")
    rule_id: str = Field(..., description="Rule that was violated")

    # Violation details
    record_id: Optional[str] = Field(None, description="ID of record with violation")
    field_name: Optional[str] = Field(None, description="Field with violation")

    actual_value: Optional[any] = Field(None, description="Actual value found")
    expected_value: Optional[any] = Field(None, description="Expected value")

    # Metadata
    detected_at: datetime = Field(default_factory=datetime.utcnow, description="When detected")
    severity: str = Field("warning", description="Severity level")
    message: str = Field(..., description="Violation message")

    class Config:
        use_enum_values = True


class DimensionScore(BaseModel):
    """Score for a single quality dimension."""

    dimension: QualityDimension = Field(..., description="Quality dimension")
    score: float = Field(..., ge=0.0, le=100.0, description="Score 0-100")
    weight: float = Field(1.0, ge=0.0, le=1.0, description="Weight in overall score")

    # Details
    total_checks: int = Field(0, ge=0, description="Total checks performed")
    passed_checks: int = Field(0, ge=0, description="Checks that passed")
    failed_checks: int = Field(0, ge=0, description="Checks that failed")

    # Violations
    violations: List[QualityViolation] = Field(default_factory=list, description="Quality violations")

    class Config:
        use_enum_values = True


class DataQualityMetrics(BaseModel):
    """Comprehensive data quality metrics for the dataset."""

    # Overall quality
    overall_score: float = Field(0.0, ge=0.0, le=100.0, description="Overall quality score")
    quality_grade: str = Field("N/A", description="Quality grade (A-F)")

    # Dimension scores
    dimension_scores: List[DimensionScore] = Field(
        default_factory=list,
        description="Scores by dimension"
    )

    # Completeness metrics
    completeness: Dict[str, float] = Field(
        default_factory=dict,
        description="Completeness by field"
    )
    overall_completeness: float = Field(0.0, ge=0.0, le=100.0, description="Overall completeness")

    # Accuracy metrics
    valid_records: int = Field(0, ge=0, description="Number of valid records")
    invalid_records: int = Field(0, ge=0, description="Number of invalid records")
    accuracy_rate: float = Field(0.0, ge=0.0, le=100.0, description="Accuracy rate")

    # Consistency metrics
    consistency_violations: int = Field(0, ge=0, description="Consistency violations found")
    cross_field_errors: int = Field(0, ge=0, description="Cross-field validation errors")

    # Timeliness metrics
    on_time_responses: int = Field(0, ge=0, description="Responses within time window")
    late_responses: int = Field(0, ge=0, description="Responses outside time window")

    # Validity metrics
    schema_violations: int = Field(0, ge=0, description="Schema violations")
    business_rule_violations: int = Field(0, ge=0, description="Business rule violations")

    # Uniqueness metrics
    duplicate_records: int = Field(0, ge=0, description="Duplicate records found")
    uniqueness_rate: float = Field(100.0, ge=0.0, le=100.0, description="Uniqueness rate")

    # Anomalies
    statistical_outliers: int = Field(0, ge=0, description="Statistical outliers detected")
    suspicious_patterns: int = Field(0, ge=0, description="Suspicious response patterns")

    # All violations
    all_violations: List[QualityViolation] = Field(
        default_factory=list,
        description="All quality violations"
    )

    # Metadata
    assessed_at: datetime = Field(default_factory=datetime.utcnow, description="Assessment timestamp")
    total_records: int = Field(0, ge=0, description="Total records assessed")

    def calculate_overall_score(self) -> float:
        """Calculate weighted overall quality score."""
        if not self.dimension_scores:
            return 0.0

        total_weight = sum(ds.weight for ds in self.dimension_scores)
        if total_weight == 0:
            return 0.0

        weighted_sum = sum(ds.score * ds.weight for ds in self.dimension_scores)
        self.overall_score = weighted_sum / total_weight

        # Assign grade
        if self.overall_score >= 90:
            self.quality_grade = "A"
        elif self.overall_score >= 80:
            self.quality_grade = "B"
        elif self.overall_score >= 70:
            self.quality_grade = "C"
        elif self.overall_score >= 60:
            self.quality_grade = "D"
        else:
            self.quality_grade = "F"

        return self.overall_score

    def get_dimension_score(self, dimension: QualityDimension) -> Optional[DimensionScore]:
        """Get score for a specific dimension."""
        for ds in self.dimension_scores:
            if ds.dimension == dimension:
                return ds
        return None

    def get_critical_violations(self) -> List[QualityViolation]:
        """Get all critical violations."""
        return [v for v in self.all_violations if v.severity == "critical"]

    def get_summary(self) -> Dict[str, any]:
        """Get a summary of quality metrics."""
        return {
            'overall_score': self.overall_score,
            'quality_grade': self.quality_grade,
            'completeness': self.overall_completeness,
            'accuracy_rate': self.accuracy_rate,
            'uniqueness_rate': self.uniqueness_rate,
            'total_violations': len(self.all_violations),
            'critical_violations': len(self.get_critical_violations()),
            'total_records': self.total_records,
        }

    class Config:
        use_enum_values = True
