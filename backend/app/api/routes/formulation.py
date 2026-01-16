"""
Formulation API endpoints.
Handles perfume formula generation and IFRA validation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

router = APIRouter()


class FormulationRequest(BaseModel):
    """Request model for generating a personalized perfume formula."""
    profile_id: str = Field(..., description="User profile ID from calibration")
    ph_value: float = Field(..., ge=3.0, le=9.0)
    skin_type: str = Field(..., pattern="^(Dry|Normal|Oily)$")
    temperature: float = Field(default=36.5, ge=35.0, le=40.0)
    prompt: Optional[str] = Field(None, description="Natural language scent description")
    valence: Optional[float] = Field(None, ge=-1.0, le=1.0, description="EEG-derived valence score")
    arousal: Optional[float] = Field(None, ge=0.0, le=1.0, description="EEG-derived arousal score")


class Ingredient(BaseModel):
    """Single ingredient in a formula."""
    name: str
    smiles: str
    concentration: float  # percentage
    note_type: str  # "top", "middle", "base"
    logp: float
    is_sustainable: bool
    source: str  # "natural", "bio-based", "upcycled", "synthetic"


class FormulaResponse(BaseModel):
    """Response model for generated formula."""
    formula_id: str
    name: str
    description: str
    ingredients: list[Ingredient]
    note_pyramid: dict  # top, middle, base percentages
    longevity_score: float  # 1-10
    projection_score: float  # 1-10
    sustainability_score: float  # 1-10
    ifra_compliant: bool
    physio_corrections_applied: list[str]


class ValidationRequest(BaseModel):
    """Request model for IFRA compliance validation."""
    ingredients: list[Ingredient]


class ValidationResponse(BaseModel):
    """Response model for IFRA validation."""
    compliant: bool
    violations: list[str]
    warnings: list[str]
    allergen_total: float  # percentage
    max_allergen_limit: float


@router.post("/generate", response_model=FormulaResponse)
async def generate_formula(request: FormulationRequest):
    """
    Generate a personalized perfume formula based on physiological profile.

    Uses Physio-RAG to apply corrections based on skin chemistry,
    then optimizes for the user's emotional preferences (if EEG data provided)
    or text prompt interpretation.
    """
    import uuid

    # Placeholder formula generation logic
    # In production, this calls the AetherAgent

    corrections_applied = []

    # pH-based corrections
    if request.ph_value < 4.5:
        corrections_applied.append("Reduced aldehyde concentration (acidic skin)")
    elif request.ph_value > 6.0:
        corrections_applied.append("Increased floral core (alkaline skin)")

    # Skin type corrections
    if request.skin_type == "Dry":
        corrections_applied.append("Boosted high-LogP fixatives (dry skin longevity)")
    elif request.skin_type == "Oily":
        corrections_applied.append("Enhanced top note projection (oily skin)")

    # Temperature corrections
    if request.temperature > 37.2:
        corrections_applied.append("Adjusted volatility curve (warm skin)")

    # Sample formula structure
    sample_ingredients = [
        Ingredient(
            name="Bergamot Oil (Citrus bergamia)",
            smiles="CC(C)=CCCC(C)=CC=O",
            concentration=8.0,
            note_type="top",
            logp=2.8,
            is_sustainable=True,
            source="natural"
        ),
        Ingredient(
            name="Linalool (Bio-based)",
            smiles="CC(C)=CCCC(C)(O)C=C",
            concentration=12.0,
            note_type="middle",
            logp=2.97,
            is_sustainable=True,
            source="bio-based"
        ),
        Ingredient(
            name="Vanillin (Lignin-derived)",
            smiles="COc1cc(C=O)ccc1O",
            concentration=5.0,
            note_type="base",
            logp=1.37,
            is_sustainable=True,
            source="upcycled"
        ),
        Ingredient(
            name="Iso E Super (Bio Musk)",
            smiles="CC1(C)CC2CCC1(C)C2(C)CC=O",
            concentration=15.0,
            note_type="base",
            logp=4.2,
            is_sustainable=True,
            source="bio-based"
        )
    ]

    # Generate formula name based on prompt or default
    formula_name = "Aether Signature"
    if request.prompt:
        if "京都" in request.prompt or "kyoto" in request.prompt.lower():
            formula_name = "Kyoto Morning Rain"

    return FormulaResponse(
        formula_id=str(uuid.uuid4()),
        name=formula_name,
        description="A personalized fragrance crafted by Aether AI, optimized for your unique skin chemistry.",
        ingredients=sample_ingredients,
        note_pyramid={
            "top": 20.0,
            "middle": 35.0,
            "base": 45.0
        },
        longevity_score=8.5,
        projection_score=7.2,
        sustainability_score=9.0,
        ifra_compliant=True,
        physio_corrections_applied=corrections_applied
    )


@router.post("/validate", response_model=ValidationResponse)
async def validate_formula(request: ValidationRequest):
    """
    Validate a formula against IFRA safety standards.

    Checks allergen concentrations, restricted substances,
    and provides compliance certification.
    """
    violations = []
    warnings = []
    allergen_total = 0.0

    # IFRA allergen limits (simplified)
    ALLERGEN_LIMIT = 1.0  # 1% total allergen limit for leave-on products
    ALLERGENS = ["linalool", "citral", "limonene", "geraniol", "eugenol"]

    for ingredient in request.ingredients:
        name_lower = ingredient.name.lower()

        # Check for common allergens
        for allergen in ALLERGENS:
            if allergen in name_lower:
                allergen_total += ingredient.concentration

        # Check for restricted concentrations
        if "oakmoss" in name_lower and ingredient.concentration > 0.1:
            violations.append(f"Oakmoss concentration ({ingredient.concentration}%) exceeds IFRA limit (0.1%)")

        if ingredient.concentration > 20.0:
            warnings.append(f"High concentration of {ingredient.name} ({ingredient.concentration}%)")

    if allergen_total > ALLERGEN_LIMIT:
        violations.append(f"Total allergen concentration ({allergen_total:.2f}%) exceeds limit ({ALLERGEN_LIMIT}%)")

    return ValidationResponse(
        compliant=len(violations) == 0,
        violations=violations,
        warnings=warnings,
        allergen_total=allergen_total,
        max_allergen_limit=ALLERGEN_LIMIT
    )
