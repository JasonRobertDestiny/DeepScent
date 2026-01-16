"""
Pydantic data models for user profile.
"""

from pydantic import BaseModel, Field
from typing import Optional


class UserProfileCreate(BaseModel):
    """Request model for creating a user profile."""
    ph_value: float = Field(..., ge=3.0, le=9.0, description="Skin pH value")
    skin_type: str = Field(..., pattern="^(Dry|Normal|Oily)$", description="Skin type")
    temperature: float = Field(default=36.5, ge=35.0, le=40.0, description="Body temperature in Celsius")
    allergies: list[str] = Field(default_factory=list, description="List of known allergens")


class UserProfileResponse(BaseModel):
    """Response model for user profile with computed adjustments."""
    profile_id: str
    ph_value: float
    ph_category: str
    skin_type: str
    temperature: float
    temperature_category: str
    allergies: list[str]
    physio_adjustments: dict

    class Config:
        from_attributes = True
