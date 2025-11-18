"""Tests for validation module."""

import pytest
from datetime import datetime

from validation.validator import DataValidator, ValidationRule
from models.quality import QualityDimension


class TestDataValidator:
    """Test DataValidator class."""

    def test_validator_initialization(self):
        """Test validator initialization."""
        config = {'min_response_completeness': 0.7}
        validator = DataValidator(config=config)

        assert validator.config == config
        assert isinstance(validator.rules, list)
        assert len(validator.rules) > 0  # Should have default rules

    def test_add_rule(self):
        """Test adding validation rule."""
        validator = DataValidator()
        initial_count = len(validator.rules)

        rule = ValidationRule(
            rule_id="TEST_001",
            name="Test Rule",
            description="Test description",
            dimension=QualityDimension.VALIDITY,
            severity="warning"
        )

        def test_func(df, rule):
            return []

        validator.add_rule(rule, test_func)
        assert len(validator.rules) == initial_count + 1

    def test_dimension_weight(self):
        """Test dimension weight calculation."""
        validator = DataValidator()

        # Test known dimensions
        completeness_weight = validator._get_dimension_weight(QualityDimension.COMPLETENESS)
        assert completeness_weight == 0.25

        accuracy_weight = validator._get_dimension_weight(QualityDimension.ACCURACY)
        assert accuracy_weight == 0.30

        # Weights should sum to ~1.0
        total_weight = sum([
            validator._get_dimension_weight(dim)
            for dim in QualityDimension
        ])
        assert 0.9 <= total_weight <= 1.1


class TestValidationRule:
    """Test ValidationRule model."""

    def test_rule_creation(self):
        """Test creating validation rule."""
        rule = ValidationRule(
            rule_id="COMP_001",
            name="Completeness Check",
            description="Check minimum completeness",
            dimension=QualityDimension.COMPLETENESS,
            severity="warning"
        )

        assert rule.rule_id == "COMP_001"
        assert rule.dimension == QualityDimension.COMPLETENESS
        assert rule.severity == "warning"
