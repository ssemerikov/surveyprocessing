"""Metadata models for survey analysis."""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SurveyMetadata(BaseModel):
    """Metadata about the survey and data collection."""

    # Collection information
    collection_start: datetime = Field(..., description="Data collection start date")
    collection_end: datetime = Field(..., description="Data collection end date")
    total_responses: int = Field(0, ge=0, description="Total number of responses")
    valid_responses: int = Field(0, ge=0, description="Number of valid responses")

    # Geographic coverage
    regions_covered: List[str] = Field(default_factory=list, description="List of regions")
    total_regions: int = Field(25, description="Total number of regions (21 + Kyiv)")

    # Sample characteristics
    response_rate: Optional[float] = Field(None, ge=0, le=100, description="Response rate %")
    completion_rate: float = Field(0, ge=0, le=100, description="Completion rate %")

    # Data quality summary
    avg_quality_score: Optional[float] = Field(None, ge=0, le=100, description="Average quality score")
    duplicate_count: int = Field(0, ge=0, description="Number of duplicates identified")
    invalid_count: int = Field(0, ge=0, description="Number of invalid responses")

    # Context
    context_tags: List[str] = Field(default_factory=list, description="Context tags (e.g., 'wartime')")
    collection_method: str = Field("online", description="Data collection method")

    # Processing metadata
    processed_at: Optional[datetime] = Field(None, description="When data was processed")
    processor_version: str = Field("1.0.0", description="Version of processing software")

    class Config:
        use_enum_values = True


class RegionalMetadata(BaseModel):
    """Metadata specific to a geographic region."""

    region_name: str = Field(..., description="Region name (Ukrainian)")
    region_name_en: Optional[str] = Field(None, description="Region name (English)")

    # Regional statistics
    total_responses: int = Field(0, ge=0, description="Responses from this region")
    population: Optional[int] = Field(None, description="Region population")
    schools_count: Optional[int] = Field(None, description="Number of schools in region")

    # War impact indicators
    is_frontline: bool = Field(False, description="Whether region is near frontline")
    is_occupied: bool = Field(False, description="Whether region is partially occupied")
    has_frequent_alerts: bool = Field(False, description="Frequent air raid alerts")

    # Digital infrastructure
    internet_coverage_pct: Optional[float] = Field(None, ge=0, le=100, description="Internet coverage %")
    avg_internet_speed_mbps: Optional[float] = Field(None, ge=0, description="Average internet speed")

    # Educational statistics
    distance_learning_pct: Optional[float] = Field(None, ge=0, le=100, description="% in distance learning")
    mixed_learning_pct: Optional[float] = Field(None, ge=0, le=100, description="% in mixed learning")
    in_person_learning_pct: Optional[float] = Field(None, ge=0, le=100, description="% in in-person learning")

    # Coordinates for mapping
    latitude: Optional[float] = Field(None, ge=-90, le=90, description="Region center latitude")
    longitude: Optional[float] = Field(None, ge=-180, le=180, description="Region center longitude")

    # Additional metadata
    notes: Optional[str] = Field(None, description="Additional notes about region")

    class Config:
        use_enum_values = True


class AnalysisMetadata(BaseModel):
    """Metadata about the analysis performed."""

    analysis_id: str = Field(..., description="Unique analysis identifier")
    analysis_type: str = Field(..., description="Type of analysis")
    performed_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")

    # Analysis parameters
    parameters: Dict[str, any] = Field(default_factory=dict, description="Analysis parameters used")
    filters_applied: List[str] = Field(default_factory=list, description="Data filters applied")

    # Results summary
    records_analyzed: int = Field(0, ge=0, description="Number of records analyzed")
    results_generated: int = Field(0, ge=0, description="Number of results generated")

    # Statistical information
    statistical_methods: List[str] = Field(default_factory=list, description="Statistical methods used")
    significance_level: float = Field(0.05, description="Statistical significance level")

    # Quality indicators
    warnings: List[str] = Field(default_factory=list, description="Warnings generated during analysis")
    errors: List[str] = Field(default_factory=list, description="Errors encountered")

    # Reproducibility
    random_seed: Optional[int] = Field(None, description="Random seed for reproducibility")
    software_version: str = Field("1.0.0", description="Software version used")
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Key dependency versions")

    class Config:
        use_enum_values = True
