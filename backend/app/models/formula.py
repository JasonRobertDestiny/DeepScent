"""
Pydantic data models for perfume formula.
"""

from pydantic import BaseModel, Field
from typing import Optional


class IngredientModel(BaseModel):
    """Single ingredient in a formula."""
    id: str
    name: str
    smiles: str
    concentration: float = Field(..., ge=0, le=100, description="Concentration percentage")
    note_type: str = Field(..., pattern="^(top|middle|base)$")
    logp: float
    is_sustainable: bool
    source: str
    sustainability_score: int = Field(..., ge=0, le=10)
    adjusted: bool = False
    adjustment_reason: str = ""


class FormulaRequest(BaseModel):
    """Request model for generating a formula."""
    profile_id: str
    ph_value: float = Field(..., ge=3.0, le=9.0)
    skin_type: str = Field(..., pattern="^(Dry|Normal|Oily)$")
    temperature: float = Field(default=36.5, ge=35.0, le=40.0)
    allergies: list[str] = Field(default_factory=list)
    prompt: Optional[str] = Field(None, description="Natural language scent description")
    valence: Optional[float] = Field(None, ge=-1.0, le=1.0, description="EEG valence score")
    arousal: Optional[float] = Field(None, ge=0.0, le=1.0, description="EEG arousal score")
    preferences: list[str] = Field(default_factory=list, description="Scent preferences")


class FormulaResponse(BaseModel):
    """Response model for generated formula."""
    formula_id: str
    name: str
    description: str
    ingredients: list[IngredientModel]
    note_pyramid: dict  # {"top": float, "middle": float, "base": float}
    longevity_score: float = Field(..., ge=0, le=10)
    projection_score: float = Field(..., ge=0, le=10)
    sustainability_score: float = Field(..., ge=0, le=10)
    ifra_compliant: bool
    corrections_applied: list[str]

    class Config:
        from_attributes = True


class IFRAValidationRequest(BaseModel):
    """Request for IFRA compliance validation."""
    ingredients: list[IngredientModel]


class IFRAValidationResponse(BaseModel):
    """Response for IFRA validation."""
    compliant: bool
    violations: list[str]
    warnings: list[str]
    allergen_total: float
    max_allergen_limit: float
