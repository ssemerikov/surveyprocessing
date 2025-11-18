"""Survey and Question data models."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, validator


class QuestionType(str, Enum):
    """Types of survey questions."""

    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"
    TEXT = "text"
    RATING = "rating"
    MATRIX = "matrix"
    RANKING = "ranking"
    DEMOGRAPHIC = "demographic"
    ORDINAL = "ordinal"
    NUMERIC = "numeric"
    DATE = "date"
    OPEN_ENDED = "open_ended"


class Question(BaseModel):
    """Model for a survey question."""

    question_id: int = Field(..., description="Unique question identifier")
    survey_id: str = Field(..., description="Parent survey identifier")
    question_number: int = Field(..., ge=1, le=22, description="Question number (1-22)")

    # Question text
    text_uk: str = Field(..., description="Question text in Ukrainian")
    text_en: Optional[str] = Field(None, description="Question text in English")

    # Question metadata
    question_type: QuestionType = Field(..., description="Type of question")
    category: str = Field(..., description="Question category")

    # Options for choice-based questions
    options: Optional[List[str]] = Field(None, description="Answer options")
    options_uk: Optional[List[str]] = Field(None, description="Options in Ukrainian")
    options_en: Optional[List[str]] = Field(None, description="Options in English")

    # Validation rules
    is_required: bool = Field(True, description="Whether question is required")
    min_selections: Optional[int] = Field(None, description="Minimum selections (multiple choice)")
    max_selections: Optional[int] = Field(None, description="Maximum selections (multiple choice)")

    # Metadata
    order: int = Field(..., description="Display order")
    section: Optional[str] = Field(None, description="Section/group")

    @validator('question_type', pre=True)
    def validate_question_type(cls, v):
        """Validate and convert question type."""
        if isinstance(v, str):
            return QuestionType(v)
        return v

    class Config:
        use_enum_values = True


class Survey(BaseModel):
    """Model for the entire survey."""

    survey_id: str = Field(..., description="Unique survey identifier")
    title_uk: str = Field(..., description="Survey title in Ukrainian")
    title_en: str = Field(..., description="Survey title in English")

    # Metadata
    description: Optional[str] = Field(None, description="Survey description")
    version: str = Field("1.0.0", description="Survey version")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    modified_at: datetime = Field(default_factory=datetime.utcnow)

    # Survey period
    start_date: datetime = Field(..., description="Survey start date")
    end_date: datetime = Field(..., description="Survey end date")

    # Questions
    questions: List[Question] = Field(default_factory=list, description="Survey questions")
    total_questions: int = Field(22, description="Total number of questions")

    # Configuration
    language: str = Field("uk", description="Primary language")
    target_audience: str = Field("parents", description="Target respondent group")
    geographic_scope: str = Field("Ukraine", description="Geographic coverage")

    # Context
    context: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context (e.g., wartime conditions)"
    )

    @validator('end_date')
    def end_after_start(cls, v, values):
        """Validate that end_date is after start_date."""
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('end_date must be after start_date')
        return v

    def get_question_by_number(self, number: int) -> Optional[Question]:
        """Get question by its number."""
        for q in self.questions:
            if q.question_number == number:
                return q
        return None

    def get_questions_by_category(self, category: str) -> List[Question]:
        """Get all questions in a category."""
        return [q for q in self.questions if q.category == category]

    def get_questions_by_type(self, qtype: QuestionType) -> List[Question]:
        """Get all questions of a specific type."""
        return [q for q in self.questions if q.question_type == qtype]

    class Config:
        use_enum_values = True
