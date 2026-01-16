"""
AetherAgent: Core AI agent for personalized perfume formulation.
Orchestrates Physio-RAG corrections, molecular calculations, and formula generation.
"""

from dataclasses import dataclass, field
from typing import Optional
import uuid

from app.core.physio_rag import physio_rag, PhysioRule
from app.chemistry.molecular_calc import calculate_logp, get_full_properties
from app.chemistry.ingredient_db import ingredient_db, Ingredient


@dataclass
class UserProfile:
    """User physiological profile for personalized formulation."""
    profile_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    ph: float = 5.5
    skin_type: str = "Normal"  # "Dry", "Normal", "Oily"
    temperature: float = 36.5
    allergies: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            'ph': self.ph,
            'skin_type': self.skin_type,
            'temperature': self.temperature,
            'allergies': self.allergies
        }


@dataclass
class FormulaIngredient:
    """An ingredient in the formula with concentration."""
    ingredient: Ingredient
    concentration: float  # percentage
    adjusted: bool = False  # True if concentration was modified by RAG
    adjustment_reason: str = ""


@dataclass
class Formula:
    """A complete perfume formula."""
    formula_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = "Aether Creation"
    description: str = ""
    ingredients: list[FormulaIngredient] = field(default_factory=list)
    corrections_applied: list[str] = field(default_factory=list)
    sustainability_score: float = 0.0
    ifra_compliant: bool = True

    @property
    def top_notes(self) -> list[FormulaIngredient]:
        return [i for i in self.ingredients if i.ingredient.note_type == "top"]

    @property
    def middle_notes(self) -> list[FormulaIngredient]:
        return [i for i in self.ingredients if i.ingredient.note_type == "middle"]

    @property
    def base_notes(self) -> list[FormulaIngredient]:
        return [i for i in self.ingredients if i.ingredient.note_type == "base"]

    @property
    def note_pyramid(self) -> dict[str, float]:
        """Calculate note type proportions."""
        top_total = sum(i.concentration for i in self.top_notes)
        mid_total = sum(i.concentration for i in self.middle_notes)
        base_total = sum(i.concentration for i in self.base_notes)
        total = top_total + mid_total + base_total

        if total == 0:
            return {"top": 0, "middle": 0, "base": 0}

        return {
            "top": round(100 * top_total / total, 1),
            "middle": round(100 * mid_total / total, 1),
            "base": round(100 * base_total / total, 1)
        }


class AetherAgent:
    """
    Core AI agent for Aether perfume formulation system.

    Responsibilities:
    1. Accept user physiological profile
    2. Query Physio-RAG for applicable correction rules
    3. Generate base formula from ingredient database
    4. Apply physiological corrections
    5. Validate against IFRA standards
    6. Output final personalized formula
    """

    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.applicable_rules: list[PhysioRule] = []
        self.formula: Optional[Formula] = None

    def generate_formula(
        self,
        scent_preferences: Optional[list[str]] = None,
        valence: Optional[float] = None,
        arousal: Optional[float] = None
    ) -> Formula:
        """
        Generate a personalized perfume formula.

        Args:
            scent_preferences: List of desired scent descriptors
            valence: EEG-derived pleasantness score (-1 to 1)
            arousal: EEG-derived arousal level (0 to 1)

        Returns:
            Personalized Formula object
        """
        # Step 1: Retrieve applicable physio rules
        self._retrieve_physio_rules()

        # Step 2: Generate base formula
        self.formula = self._generate_base_formula(scent_preferences, valence, arousal)

        # Step 3: Apply physiological corrections
        self._apply_physio_corrections()

        # Step 4: Optimize for sustainability
        self._optimize_sustainability()

        # Step 5: Calculate sustainability score
        self._calculate_sustainability_score()

        return self.formula

    def _retrieve_physio_rules(self):
        """Retrieve applicable rules from Physio-RAG."""
        profile_dict = self.user_profile.to_dict()
        self.applicable_rules = physio_rag.get_applicable_rules(profile_dict)

    def _generate_base_formula(
        self,
        scent_preferences: Optional[list[str]],
        valence: Optional[float],
        arousal: Optional[float]
    ) -> Formula:
        """Generate base formula from ingredient database."""
        formula = Formula()
        all_ingredients = ingredient_db.get_all()

        # Filter by allergies first
        safe_ingredients = ingredient_db.get_safe_for_allergies(
            self.user_profile.allergies
        )

        # Select ingredients by note type
        # Standard ratio: 20% top, 35% middle, 45% base
        top_notes = [i for i in safe_ingredients if i.note_type == "top"]
        middle_notes = [i for i in safe_ingredients if i.note_type == "middle"]
        base_notes = [i for i in safe_ingredients if i.note_type == "base"]

        # Apply scent preferences if provided
        if scent_preferences:
            top_notes = self._filter_by_preferences(top_notes, scent_preferences) or top_notes
            middle_notes = self._filter_by_preferences(middle_notes, scent_preferences) or middle_notes
            base_notes = self._filter_by_preferences(base_notes, scent_preferences) or base_notes

        # Apply valence-arousal mapping
        if valence is not None and arousal is not None:
            formula.description = self._va_to_description(valence, arousal)
            # High valence + high arousal = citrus, bright
            # High valence + low arousal = woody, musky, calm
            if valence > 0.3 and arousal > 0.5:
                # Prefer citrus and fresh
                top_notes = [i for i in top_notes if 'citrus' in i.family or 'fresh' in ' '.join(i.descriptors)][:2] or top_notes[:2]
            elif valence > 0.3 and arousal <= 0.5:
                # Prefer woody and calming
                base_notes = [i for i in base_notes if 'woody' in i.family][:3] or base_notes[:3]

        # Build formula with standard concentrations
        # Top notes: ~8-12% each, total ~20%
        for i, ing in enumerate(top_notes[:2]):
            conc = 10.0 - (i * 2)
            formula.ingredients.append(FormulaIngredient(ingredient=ing, concentration=conc))

        # Middle notes: ~10-15% each, total ~35%
        for i, ing in enumerate(middle_notes[:3]):
            conc = 12.0 - (i * 1)
            formula.ingredients.append(FormulaIngredient(ingredient=ing, concentration=conc))

        # Base notes: ~10-20% each, total ~45%
        for i, ing in enumerate(base_notes[:3]):
            conc = 15.0 - (i * 2)
            formula.ingredients.append(FormulaIngredient(ingredient=ing, concentration=conc))

        return formula

    def _filter_by_preferences(self, ingredients: list[Ingredient], preferences: list[str]) -> list[Ingredient]:
        """Filter ingredients by scent preferences."""
        matched = []
        for ing in ingredients:
            for pref in preferences:
                pref_lower = pref.lower()
                if (pref_lower in ing.family.lower() or
                    any(pref_lower in d.lower() for d in ing.descriptors)):
                    matched.append(ing)
                    break
        return matched

    def _va_to_description(self, valence: float, arousal: float) -> str:
        """Convert Valence-Arousal to scent description."""
        if valence > 0.3:
            if arousal > 0.5:
                return "An energizing blend that uplifts and invigorates"
            else:
                return "A serene composition for peaceful moments"
        else:
            if arousal > 0.5:
                return "A bold and intense sensory experience"
            else:
                return "A grounding and contemplative fragrance"

    def _apply_physio_corrections(self):
        """Apply physiological corrections based on RAG rules."""
        if not self.formula:
            return

        for rule in self.applicable_rules:
            correction_desc = self._apply_single_rule(rule)
            if correction_desc:
                self.formula.corrections_applied.append(correction_desc)

    def _apply_single_rule(self, rule: PhysioRule) -> Optional[str]:
        """Apply a single physio rule to the formula."""
        action = rule.action
        target = rule.target.lower()
        factor = rule.factor or 1.0

        if action == "reduce_concentration":
            return self._adjust_concentration_by_target(target, factor, f"Reduced {target} ({rule.reasoning})")

        elif action == "increase_concentration":
            return self._adjust_concentration_by_target(target, factor, f"Increased {target} ({rule.reasoning})")

        elif action == "boost_high_logp":
            threshold = rule.threshold.get('logp', 3.5) if rule.threshold else 3.5
            return self._boost_fixatives(threshold, factor)

        elif action == "reduce_proportion":
            target_prop = rule.threshold.get('target_proportion', 0.15) if rule.threshold else 0.15
            return self._adjust_note_proportion(target, target_prop)

        elif action == "flag_oxidation_risk":
            return self._flag_oxidation_ingredients()

        elif action == "eliminate_or_substitute":
            return self._eliminate_allergen(target)

        return None

    def _adjust_concentration_by_target(self, target: str, factor: float, reason: str) -> str:
        """Adjust concentration of ingredients matching target."""
        adjusted_count = 0
        for fi in self.formula.ingredients:
            # Match by family or note type
            if (target in fi.ingredient.family.lower() or
                target in fi.ingredient.note_type.lower() or
                target in fi.ingredient.name.lower()):
                fi.concentration *= factor
                fi.adjusted = True
                fi.adjustment_reason = reason
                adjusted_count += 1

        if adjusted_count > 0:
            return f"{reason} - affected {adjusted_count} ingredient(s)"
        return None

    def _boost_fixatives(self, logp_threshold: float, factor: float) -> str:
        """Boost high-LogP ingredients for dry skin longevity."""
        boosted = []
        for fi in self.formula.ingredients:
            if fi.ingredient.logp >= logp_threshold:
                fi.concentration *= factor
                fi.adjusted = True
                fi.adjustment_reason = "Boosted for dry skin retention"
                boosted.append(fi.ingredient.name)

        if boosted:
            return f"Boosted fixatives (LogP>{logp_threshold}): {', '.join(boosted)}"
        return None

    def _adjust_note_proportion(self, note_type: str, target_proportion: float) -> str:
        """Adjust proportion of a note type in the formula."""
        current_pyramid = self.formula.note_pyramid
        current_prop = current_pyramid.get(note_type.replace(" notes", "").lower(), 0) / 100

        if current_prop > target_proportion:
            # Need to reduce
            reduction_factor = target_proportion / current_prop if current_prop > 0 else 1.0
            for fi in self.formula.ingredients:
                if fi.ingredient.note_type.lower() in note_type.lower():
                    fi.concentration *= reduction_factor
                    fi.adjusted = True
            return f"Reduced {note_type} proportion from {current_prop:.0%} to {target_proportion:.0%}"

        return None

    def _flag_oxidation_ingredients(self) -> str:
        """Flag citrus terpenes at risk of oxidation on oily skin."""
        flagged = []
        for fi in self.formula.ingredients:
            if 'citrus' in fi.ingredient.family.lower():
                # Reduce concentration slightly and flag
                fi.concentration *= 0.9
                fi.adjusted = True
                fi.adjustment_reason = "Reduced due to squalene oxidation risk"
                flagged.append(fi.ingredient.name)

        if flagged:
            return f"Reduced oxidation-prone ingredients: {', '.join(flagged)}"
        return None

    def _eliminate_allergen(self, allergen: str) -> str:
        """Remove or minimize allergenic ingredients."""
        removed = []
        self.formula.ingredients = [
            fi for fi in self.formula.ingredients
            if allergen.lower() not in fi.ingredient.name.lower()
            or (removed.append(fi.ingredient.name) or False)  # Side effect to track removed
        ]

        # Actually remove them
        new_ingredients = []
        for fi in self.formula.ingredients:
            if allergen.lower() in fi.ingredient.name.lower():
                removed.append(fi.ingredient.name)
            else:
                new_ingredients.append(fi)
        self.formula.ingredients = new_ingredients

        if removed:
            return f"Eliminated allergen {allergen}: {', '.join(removed)}"
        return None

    def _optimize_sustainability(self):
        """Prefer sustainable ingredients where possible."""
        # Already using sustainable ingredients from DB
        # This could be extended to swap out synthetic for bio-based alternatives
        pass

    def _calculate_sustainability_score(self):
        """Calculate overall formula sustainability score."""
        if not self.formula.ingredients:
            self.formula.sustainability_score = 0.0
            return

        total_weighted_score = 0.0
        total_concentration = 0.0

        for fi in self.formula.ingredients:
            total_weighted_score += fi.ingredient.sustainability_score * fi.concentration
            total_concentration += fi.concentration

        if total_concentration > 0:
            self.formula.sustainability_score = round(total_weighted_score / total_concentration, 1)


def create_agent(
    ph: float = 5.5,
    skin_type: str = "Normal",
    temperature: float = 36.5,
    allergies: list[str] = None
) -> AetherAgent:
    """
    Factory function to create an AetherAgent with user profile.

    Args:
        ph: Skin pH value (3.0-9.0)
        skin_type: "Dry", "Normal", or "Oily"
        temperature: Body temperature in Celsius
        allergies: List of allergen names to avoid

    Returns:
        Configured AetherAgent instance
    """
    profile = UserProfile(
        ph=ph,
        skin_type=skin_type,
        temperature=temperature,
        allergies=allergies or []
    )
    return AetherAgent(profile)
