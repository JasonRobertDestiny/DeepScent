"""
Ingredient database interface.
Provides access to fragrance ingredient data with sustainability and safety information.
"""

import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

from app.config import settings


@dataclass
class Ingredient:
    """Fragrance ingredient with full metadata."""
    id: str
    name: str
    smiles: str
    note_type: str  # "top", "middle", "base"
    family: str
    logp: float
    molecular_weight: float
    is_sustainable: bool
    source: str
    sustainability_score: int
    ifra_restricted: bool
    allergen: bool
    max_concentration: Optional[float] = None
    descriptors: list[str] = None
    origin: Optional[str] = None

    def __post_init__(self):
        if self.descriptors is None:
            self.descriptors = []


class IngredientDatabase:
    """
    Singleton database for fragrance ingredients.
    Loads from JSON and provides query methods.
    """

    _instance = None
    _ingredients: dict[str, Ingredient] = {}
    _loaded = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._loaded:
            self._load_ingredients()

    def _load_ingredients(self):
        """Load ingredients from JSON file."""
        data_path = settings.data_dir / "ingredients.json"

        if not data_path.exists():
            # Create minimal fallback
            self._ingredients = {}
            self._loaded = True
            return

        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for ing_data in data.get('ingredients', []):
            ingredient = Ingredient(
                id=ing_data['id'],
                name=ing_data['name'],
                smiles=ing_data['smiles'],
                note_type=ing_data['note_type'],
                family=ing_data['family'],
                logp=ing_data['logp'],
                molecular_weight=ing_data['molecular_weight'],
                is_sustainable=ing_data['is_sustainable'],
                source=ing_data['source'],
                sustainability_score=ing_data['sustainability_score'],
                ifra_restricted=ing_data.get('ifra_restricted', False),
                allergen=ing_data.get('allergen', False),
                max_concentration=ing_data.get('max_concentration'),
                descriptors=ing_data.get('descriptors', []),
                origin=ing_data.get('origin')
            )
            self._ingredients[ingredient.id] = ingredient

        self._loaded = True

    def get_all(self) -> list[Ingredient]:
        """Get all ingredients."""
        return list(self._ingredients.values())

    def get_by_id(self, ingredient_id: str) -> Optional[Ingredient]:
        """Get ingredient by ID."""
        return self._ingredients.get(ingredient_id)

    def get_by_note_type(self, note_type: str) -> list[Ingredient]:
        """Get ingredients by note type (top, middle, base)."""
        return [ing for ing in self._ingredients.values() if ing.note_type == note_type]

    def get_by_family(self, family: str) -> list[Ingredient]:
        """Get ingredients by fragrance family."""
        return [ing for ing in self._ingredients.values() if ing.family == family]

    def get_sustainable(self, min_score: int = 8) -> list[Ingredient]:
        """Get sustainable ingredients above a minimum score."""
        return [ing for ing in self._ingredients.values()
                if ing.is_sustainable and ing.sustainability_score >= min_score]

    def get_upcycled(self) -> list[Ingredient]:
        """Get upcycled ingredients (highest sustainability tier)."""
        return [ing for ing in self._ingredients.values() if ing.source == "upcycled"]

    def get_non_allergenic(self) -> list[Ingredient]:
        """Get ingredients that are not known allergens."""
        return [ing for ing in self._ingredients.values() if not ing.allergen]

    def get_fixatives(self, min_logp: float = 3.5) -> list[Ingredient]:
        """Get fixative ingredients based on LogP threshold."""
        return [ing for ing in self._ingredients.values() if ing.logp >= min_logp]

    def search_by_descriptor(self, descriptor: str) -> list[Ingredient]:
        """Search ingredients by scent descriptor."""
        descriptor_lower = descriptor.lower()
        return [ing for ing in self._ingredients.values()
                if any(descriptor_lower in d.lower() for d in ing.descriptors)]

    def get_safe_for_allergies(self, allergies: list[str]) -> list[Ingredient]:
        """
        Get ingredients safe for a user with specific allergies.

        Args:
            allergies: List of allergen names to exclude

        Returns:
            List of safe ingredients
        """
        allergies_lower = [a.lower() for a in allergies]
        safe = []
        for ing in self._ingredients.values():
            # Check if ingredient name contains any allergen
            ing_name_lower = ing.name.lower()
            is_safe = not any(allergen in ing_name_lower for allergen in allergies_lower)

            # Also check if it's a declared allergen and user is sensitive
            if ing.allergen:
                for allergen in allergies_lower:
                    if allergen in ing_name_lower:
                        is_safe = False
                        break

            if is_safe:
                safe.append(ing)

        return safe


# Singleton instance
ingredient_db = IngredientDatabase()
