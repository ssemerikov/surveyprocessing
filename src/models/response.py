"""Response and Answer data models."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator
from uuid import UUID, uuid4


class ResponseStatus(str, Enum):
    """Status of a survey response."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    ABANDONED = "abandoned"
    INVALID = "invalid"
    VALIDATED = "validated"


class Answer(BaseModel):
    """Model for a single answer to a question."""

    answer_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique answer ID")
    response_id: str = Field(..., description="Parent response ID")
    question_id: int = Field(..., description="Question number (1-22)")

    # Answer value (polymorphic - supports multiple types)
    value_raw: Union[str, int, float, List[str], None] = Field(
        None, description="Raw answer value"
    )
    value_normalized: Union[str, int, float, List[str], None] = Field(
        None, description="Normalized answer value"
    )

    # Metadata
    answered_at: Optional[datetime] = Field(None, description="When answered")
    time_spent_seconds: Optional[float] = Field(None, description="Time spent on question")
    is_skipped: bool = Field(False, description="Whether question was skipped")
    edit_count: int = Field(0, description="Number of times edited")

    # Data quality indicators
    is_valid: bool = Field(True, description="Whether answer passes validation")
    validation_errors: List[str] = Field(default_factory=list, description="Validation errors")

    def normalize_value(self, normalization_func=None):
        """Normalize the answer value."""
        if normalization_func:
            self.value_normalized = normalization_func(self.value_raw)
        else:
            # Default normalization
            if isinstance(self.value_raw, str):
                self.value_normalized = self.value_raw.strip()
            else:
                self.value_normalized = self.value_raw

    class Config:
        use_enum_values = True


class Response(BaseModel):
    """Model for a complete survey response."""

    response_id: str = Field(default_factory=lambda: str(uuid4()), description="Unique response ID")
    survey_id: str = Field(..., description="Parent survey ID")

    # Respondent information (anonymized)
    respondent_id: Optional[str] = Field(None, description="Pseudonymized respondent ID")

    # Timing information
    submitted_at: datetime = Field(default_factory=datetime.utcnow, description="Submission timestamp")
    started_at: Optional[datetime] = Field(None, description="When response started")
    duration_seconds: Optional[float] = Field(None, description="Total response duration")

    # Status
    status: ResponseStatus = Field(
        ResponseStatus.PARTIAL, description="Response completion status"
    )
    completion_percentage: float = Field(0.0, ge=0.0, le=100.0, description="% of questions answered")

    # Answers
    answers: List[Answer] = Field(default_factory=list, description="All answers in this response")

    # Metadata
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata (device, location, IP hash, etc.)"
    )

    # Quality metrics
    quality_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="Overall quality score")
    quality_flags: List[str] = Field(default_factory=list, description="Data quality warnings")

    # Regional/demographic cache (for faster filtering)
    region: Optional[str] = Field(None, description="Respondent's region")
    settlement_type: Optional[str] = Field(None, description="Settlement type")
    school_type: Optional[str] = Field(None, description="School type")
    child_grade: Optional[int] = Field(None, description="Child's grade level")

    @validator('completion_percentage', always=True)
    def calculate_completion(cls, v, values):
        """Calculate completion percentage based on answered questions."""
        if 'answers' in values:
            answered = sum(1 for a in values['answers'] if not a.is_skipped)
            total = 22  # Total questions
            return (answered / total) * 100
        return v

    @validator('status', always=True)
    def determine_status(cls, v, values):
        """Automatically determine status based on completion."""
        if 'completion_percentage' in values:
            completion = values['completion_percentage']
            if completion >= 95:
                return ResponseStatus.COMPLETE
            elif completion >= 30:
                return ResponseStatus.PARTIAL
            else:
                return ResponseStatus.ABANDONED
        return v

    def get_answer(self, question_id: int) -> Optional[Answer]:
        """Get answer for a specific question."""
        for answer in self.answers:
            if answer.question_id == question_id:
                return answer
        return None

    def add_answer(self, answer: Answer) -> None:
        """Add an answer to this response."""
        # Remove existing answer for this question if any
        self.answers = [a for a in self.answers if a.question_id != answer.question_id]
        self.answers.append(answer)

    def get_demographic_summary(self) -> Dict[str, Any]:
        """Get summary of demographic information."""
        return {
            'region': self.region,
            'settlement_type': self.settlement_type,
            'school_type': self.school_type,
            'child_grade': self.child_grade,
        }

    def calculate_quality_score(self) -> float:
        """Calculate overall quality score for this response."""
        scores = []

        # Completeness score (40%)
        completeness = self.completion_percentage / 100
        scores.append(completeness * 0.4)

        # Validity score (30%)
        valid_answers = sum(1 for a in self.answers if a.is_valid)
        total_answers = len(self.answers)
        validity = valid_answers / total_answers if total_answers > 0 else 0
        scores.append(validity * 0.3)

        # Timing score (15%) - not too fast (bot) or too slow (abandoned)
        if self.duration_seconds:
            # Assume reasonable range: 5-60 minutes for full survey
            if 300 <= self.duration_seconds <= 3600:
                timing_score = 1.0
            elif self.duration_seconds < 300:
                timing_score = self.duration_seconds / 300
            else:
                timing_score = max(0, 1 - (self.duration_seconds - 3600) / 3600)
            scores.append(timing_score * 0.15)

        # Consistency score (15%) - no excessive editing
        avg_edits = sum(a.edit_count for a in self.answers) / len(self.answers) if self.answers else 0
        consistency = max(0, 1 - (avg_edits / 5))  # Penalize > 5 edits per question
        scores.append(consistency * 0.15)

        self.quality_score = sum(scores) * 100
        return self.quality_score

    class Config:
        use_enum_values = True
