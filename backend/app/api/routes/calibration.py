"""
Bio-calibration API endpoints.
Handles pH analysis, skin type assessment, and user profile creation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


class PhAnalysisRequest(BaseModel):
    """Request model for pH test strip analysis."""
    ph_value: float = Field(..., ge=3.0, le=9.0, description="Measured pH value from test strip")


class PhAnalysisResponse(BaseModel):
    """Response model for pH analysis."""
    ph_value: float
    category: str  # "acidic", "optimal", "alkaline"
    recommendations: list[str]


class UserProfileRequest(BaseModel):
    """Request model for creating a user physiological profile."""
    ph_value: float = Field(..., ge=3.0, le=9.0)
    skin_type: str = Field(..., pattern="^(Dry|Normal|Oily)$")
    temperature: float = Field(default=36.5, ge=35.0, le=40.0)
    allergies: list[str] = Field(default_factory=list)


class UserProfileResponse(BaseModel):
    """Response model for user profile."""
    profile_id: str
    ph_value: float
    ph_category: str
    skin_type: str
    temperature: float
    temperature_category: str
    allergies: list[str]
    physio_adjustments: dict


def categorize_ph(ph_value: float) -> tuple[str, list[str]]:
    """Categorize pH value and provide recommendations."""
    if ph_value < 4.5:
        return "acidic", [
            "Reduce aldehyde concentration by 15%",
            "Add pH buffer agents",
            "Substitute with acetal derivatives for stability"
        ]
    elif ph_value > 6.0:
        return "alkaline", [
            "Increase floral core concentration by 20%",
            "Add mild acidic modifiers",
            "Monitor for saponification reactions"
        ]
    else:
        return "optimal", [
            "Standard formulation parameters apply",
            "No pH-related adjustments needed"
        ]


def categorize_temperature(temp: float) -> tuple[str, list[str]]:
    """Categorize body temperature and provide recommendations."""
    if temp > 37.2:
        return "warm", [
            "Reduce top note ratio (front-heavy burn-off risk)",
            "Use higher molecular weight substitutes",
            "Increase fixative base proportion"
        ]
    elif temp < 36.0:
        return "cool", [
            "Increase top note volatility",
            "Reduce heavy base notes",
            "Adjust for reduced diffusion"
        ]
    else:
        return "normal", [
            "Standard volatility curve applies"
        ]


@router.post("/analyze-ph", response_model=PhAnalysisResponse)
async def analyze_ph(request: PhAnalysisRequest):
    """
    Analyze pH value from test strip and provide formulation recommendations.

    In production, this would accept an image and use CV for OCR.
    For MVP, accepts direct pH value input.
    """
    category, recommendations = categorize_ph(request.ph_value)

    return PhAnalysisResponse(
        ph_value=request.ph_value,
        category=category,
        recommendations=recommendations
    )


@router.post("/profile", response_model=UserProfileResponse)
async def create_profile(request: UserProfileRequest):
    """
    Create a user physiological profile for personalized formulation.

    Combines pH, skin type, temperature, and allergies to generate
    a comprehensive adjustment profile for the Aether engine.
    """
    import uuid

    ph_category, ph_recommendations = categorize_ph(request.ph_value)
    temp_category, temp_recommendations = categorize_temperature(request.temperature)

    # Build physio adjustments based on all factors
    physio_adjustments = {
        "ph_adjustments": ph_recommendations,
        "temperature_adjustments": temp_recommendations,
        "skin_type_adjustments": []
    }

    # Skin type specific adjustments
    if request.skin_type == "Dry":
        physio_adjustments["skin_type_adjustments"] = [
            "Increase high-LogP fixatives by 25%",
            "Add molecular encapsulation for longevity",
            "Boost base notes proportion"
        ]
    elif request.skin_type == "Oily":
        physio_adjustments["skin_type_adjustments"] = [
            "Increase top note volatility",
            "Reduce heavy base notes",
            "Monitor for terpene oxidation with squalene"
        ]
    else:
        physio_adjustments["skin_type_adjustments"] = [
            "Standard lipid balance formula"
        ]

    return UserProfileResponse(
        profile_id=str(uuid.uuid4()),
        ph_value=request.ph_value,
        ph_category=ph_category,
        skin_type=request.skin_type,
        temperature=request.temperature,
        temperature_category=temp_category,
        allergies=request.allergies,
        physio_adjustments=physio_adjustments
    )
