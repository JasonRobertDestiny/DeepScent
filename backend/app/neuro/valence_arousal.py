"""
Valence-Arousal model mapping for scent personalization.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ScentMapping:
    """Mapping from VA coordinates to scent characteristics."""
    families: list[str]
    descriptors: list[str]
    note_distribution: dict[str, float]  # top, middle, base ratios
    intensity: str  # "light", "moderate", "intense"
    longevity_preference: str  # "short", "medium", "long"


# VA quadrant mappings based on fragrance psychology research
VA_MAPPINGS = {
    # Quadrant I: High Valence, High Arousal (Happy, Excited)
    "high_valence_high_arousal": ScentMapping(
        families=["citrus", "fresh", "fruity", "aromatic"],
        descriptors=["bright", "sparkling", "energizing", "zesty", "effervescent"],
        note_distribution={"top": 0.35, "middle": 0.40, "base": 0.25},
        intensity="moderate",
        longevity_preference="medium"
    ),

    # Quadrant II: High Valence, Low Arousal (Calm, Content)
    "high_valence_low_arousal": ScentMapping(
        families=["woody", "floral", "musky", "powdery"],
        descriptors=["soft", "warm", "comforting", "cozy", "serene"],
        note_distribution={"top": 0.20, "middle": 0.35, "base": 0.45},
        intensity="light",
        longevity_preference="long"
    ),

    # Quadrant III: Low Valence, Low Arousal (Sad, Depressed)
    "low_valence_low_arousal": ScentMapping(
        families=["resinous", "ambery", "earthy", "leather"],
        descriptors=["grounding", "contemplative", "deep", "meditative"],
        note_distribution={"top": 0.15, "middle": 0.30, "base": 0.55},
        intensity="moderate",
        longevity_preference="long"
    ),

    # Quadrant IV: Low Valence, High Arousal (Anxious, Stressed)
    "low_valence_high_arousal": ScentMapping(
        families=["herbal", "green", "aquatic", "ozonic"],
        descriptors=["clean", "crisp", "refreshing", "calming", "balancing"],
        note_distribution={"top": 0.30, "middle": 0.40, "base": 0.30},
        intensity="light",
        longevity_preference="medium"
    ),

    # Center: Neutral
    "neutral": ScentMapping(
        families=["woody", "aromatic", "floral"],
        descriptors=["balanced", "versatile", "classic", "elegant"],
        note_distribution={"top": 0.25, "middle": 0.40, "base": 0.35},
        intensity="moderate",
        longevity_preference="medium"
    )
}


def get_va_quadrant(valence: float, arousal: float) -> str:
    """
    Determine VA quadrant from coordinates.

    Args:
        valence: -1 to 1 (unpleasant to pleasant)
        arousal: 0 to 1 (calm to excited)

    Returns:
        Quadrant key for VA_MAPPINGS
    """
    arousal_threshold = 0.5
    valence_threshold = 0.15  # Slightly wider neutral zone

    if abs(valence) < valence_threshold:
        return "neutral"

    if valence > valence_threshold:
        if arousal > arousal_threshold:
            return "high_valence_high_arousal"
        else:
            return "high_valence_low_arousal"
    else:
        if arousal > arousal_threshold:
            return "low_valence_high_arousal"
        else:
            return "low_valence_low_arousal"


def get_scent_mapping(valence: float, arousal: float) -> ScentMapping:
    """
    Get scent mapping for given VA coordinates.

    Args:
        valence: -1 to 1
        arousal: 0 to 1

    Returns:
        ScentMapping with recommended characteristics
    """
    quadrant = get_va_quadrant(valence, arousal)
    return VA_MAPPINGS[quadrant]


def blend_mappings(
    primary: ScentMapping,
    secondary: ScentMapping,
    blend_ratio: float = 0.7
) -> ScentMapping:
    """
    Blend two scent mappings for intermediate VA positions.

    Args:
        primary: Primary mapping (higher weight)
        secondary: Secondary mapping
        blend_ratio: Weight of primary (0-1)

    Returns:
        Blended ScentMapping
    """
    # Combine families (unique)
    families = list(set(primary.families[:3] + secondary.families[:2]))

    # Combine descriptors
    descriptors = list(set(primary.descriptors[:3] + secondary.descriptors[:2]))

    # Blend note distribution
    note_dist = {}
    for note in ["top", "middle", "base"]:
        note_dist[note] = (
            primary.note_distribution[note] * blend_ratio +
            secondary.note_distribution[note] * (1 - blend_ratio)
        )

    # Use primary for discrete attributes
    return ScentMapping(
        families=families,
        descriptors=descriptors,
        note_distribution=note_dist,
        intensity=primary.intensity,
        longevity_preference=primary.longevity_preference
    )
