"""Tests for data models."""

from datetime import datetime
import pytest

from models.survey import Survey, Question, QuestionType
from models.response import Response, Answer, ResponseStatus
from models.quality import DataQualityMetrics, QualityDimension, DimensionScore


class TestSurveyModel:
    """Test Survey model."""

    def test_survey_creation(self):
        """Test creating a survey."""
        survey = Survey(
            survey_id="test_survey_001",
            title_uk="Тестове опитування",
            title_en="Test Survey",
            start_date=datetime(2024, 10, 7),
            end_date=datetime(2024, 10, 18)
        )
        assert survey.survey_id == "test_survey_001"
        assert survey.title_uk == "Тестове опитування"
        assert survey.total_questions == 22

    def test_survey_date_validation(self):
        """Test that end_date must be after start_date."""
        with pytest.raises(ValueError):
            Survey(
                survey_id="test_survey_002",
                title_uk="Test",
                title_en="Test",
                start_date=datetime(2024, 10, 18),
                end_date=datetime(2024, 10, 7)  # Before start_date
            )


class TestQuestionModel:
    """Test Question model."""

    def test_question_creation(self):
        """Test creating a question."""
        question = Question(
            question_id=1,
            survey_id="test_survey_001",
            question_number=1,
            text_uk="Ваш вік?",
            text_en="Your age?",
            question_type=QuestionType.SINGLE_CHOICE,
            category="demographic",
            order=1
        )
        assert question.question_number == 1
        assert question.question_type == QuestionType.SINGLE_CHOICE

    def test_question_number_range(self):
        """Test question number validation."""
        with pytest.raises(ValueError):
            Question(
                question_id=1,
                survey_id="test_survey_001",
                question_number=25,  # Out of range (1-22)
                text_uk="Test",
                text_en="Test",
                question_type=QuestionType.TEXT,
                category="test",
                order=1
            )


class TestResponseModel:
    """Test Response model."""

    def test_response_creation(self):
        """Test creating a response."""
        response = Response(
            survey_id="test_survey_001"
        )
        assert response.status == ResponseStatus.PARTIAL
        assert response.completion_percentage == 0.0

    def test_add_answer(self):
        """Test adding answer to response."""
        response = Response(survey_id="test_survey_001")
        answer = Answer(
            response_id=response.response_id,
            question_id=1,
            value_raw="від 35 до 44"
        )
        response.add_answer(answer)
        assert len(response.answers) == 1
        assert response.get_answer(1) is not None

    def test_quality_score_calculation(self):
        """Test quality score calculation."""
        response = Response(survey_id="test_survey_001")

        # Add some answers
        for i in range(1, 20):  # Add 19 answers (>85% completion)
            answer = Answer(
                response_id=response.response_id,
                question_id=i,
                value_raw="test_value"
            )
            response.add_answer(answer)

        score = response.calculate_quality_score()
        assert 0 <= score <= 100
        assert score > 50  # Should be decent with high completion


class TestAnswerModel:
    """Test Answer model."""

    def test_answer_creation(self):
        """Test creating an answer."""
        answer = Answer(
            response_id="resp_001",
            question_id=1,
            value_raw="Жінка"
        )
        assert answer.value_raw == "Жінка"
        assert answer.is_valid is True

    def test_answer_normalization(self):
        """Test answer normalization."""
        answer = Answer(
            response_id="resp_001",
            question_id=1,
            value_raw="  Жінка  "  # With whitespace
        )
        answer.normalize_value()
        assert answer.value_normalized == "Жінка"


class TestQualityMetrics:
    """Test quality metrics."""

    def test_dimension_score_creation(self):
        """Test creating dimension score."""
        dim_score = DimensionScore(
            dimension=QualityDimension.COMPLETENESS,
            score=95.5,
            weight=0.25,
            total_checks=100,
            passed_checks=95,
            failed_checks=5
        )
        assert dim_score.score == 95.5
        assert dim_score.dimension == QualityDimension.COMPLETENESS

    def test_quality_metrics_overall_score(self):
        """Test overall quality score calculation."""
        metrics = DataQualityMetrics(total_records=100)

        # Add dimension scores
        metrics.dimension_scores = [
            DimensionScore(
                dimension=QualityDimension.COMPLETENESS,
                score=90.0,
                weight=0.25,
                total_checks=100,
                passed_checks=90,
                failed_checks=10
            ),
            DimensionScore(
                dimension=QualityDimension.ACCURACY,
                score=85.0,
                weight=0.30,
                total_checks=100,
                passed_checks=85,
                failed_checks=15
            )
        ]

        overall = metrics.calculate_overall_score()
        assert 80 <= overall <= 95
        assert metrics.quality_grade in ['A', 'B', 'C']
