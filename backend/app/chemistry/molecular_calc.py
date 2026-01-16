"""
Molecular calculation engine using RDKit.
Provides LogP calculations, molecular property analysis, and SMILES validation.
"""

from typing import Optional
from dataclasses import dataclass


@dataclass
class MolecularProperties:
    """Container for calculated molecular properties."""
    smiles: str
    valid: bool
    logp: Optional[float] = None
    molecular_weight: Optional[float] = None
    tpsa: Optional[float] = None  # Topological Polar Surface Area
    num_rotatable_bonds: Optional[int] = None
    num_h_donors: Optional[int] = None
    num_h_acceptors: Optional[int] = None
    estimated_vapor_pressure: Optional[float] = None
    volatility_class: Optional[str] = None  # "high", "medium", "low"
    error_message: Optional[str] = None


def validate_smiles(smiles: str) -> bool:
    """
    Validate a SMILES string using RDKit.

    Args:
        smiles: SMILES string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        from rdkit import Chem
        mol = Chem.MolFromSmiles(smiles)
        return mol is not None
    except ImportError:
        # Fallback if RDKit not installed
        return len(smiles) > 0


def calculate_logp(smiles: str) -> Optional[float]:
    """
    Calculate LogP (octanol-water partition coefficient) using Crippen method.

    LogP is critical for fragrance chemistry:
    - High LogP (>3): Lipophilic, good skin retention, slow evaporation
    - Low LogP (<2): Hydrophilic, poor retention, fast evaporation

    Args:
        smiles: SMILES string of the molecule

    Returns:
        LogP value or None if calculation fails
    """
    try:
        from rdkit import Chem
        from rdkit.Chem import Crippen

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return round(Crippen.MolLogP(mol), 2)
    except ImportError:
        return None
    except Exception:
        return None


def calculate_molecular_weight(smiles: str) -> Optional[float]:
    """
    Calculate molecular weight.

    Molecular weight affects volatility:
    - <150 g/mol: Very volatile (top notes)
    - 150-250 g/mol: Moderate volatility (middle notes)
    - >250 g/mol: Low volatility (base notes)

    Args:
        smiles: SMILES string

    Returns:
        Molecular weight in g/mol
    """
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        return round(Descriptors.MolWt(mol), 2)
    except ImportError:
        return None
    except Exception:
        return None


def estimate_vapor_pressure(smiles: str, temperature_c: float = 25.0) -> Optional[float]:
    """
    Estimate vapor pressure using molecular properties.

    Since RDKit doesn't have built-in vapor pressure calculation,
    we use an empirical correlation based on molecular weight and LogP.

    This is a simplified model; for production, use UNIFAC or other
    thermodynamic models.

    Args:
        smiles: SMILES string
        temperature_c: Temperature in Celsius (default 25)

    Returns:
        Estimated vapor pressure in mmHg
    """
    try:
        mw = calculate_molecular_weight(smiles)
        logp = calculate_logp(smiles)

        if mw is None or logp is None:
            return None

        # Simplified empirical correlation
        # log10(VP) = A - B*MW/1000 - C*LogP
        # Coefficients derived from fragrance compound data
        A = 2.5
        B = 8.0
        C = 0.3

        log_vp = A - B * (mw / 1000) - C * logp

        # Temperature correction using simplified Clausius-Clapeyron
        # VP(T) = VP(25) * exp(dH/R * (1/298 - 1/T))
        temp_k = temperature_c + 273.15
        temp_factor = (temp_k / 298.15) ** 2  # Simplified

        vp = (10 ** log_vp) * temp_factor

        return round(vp, 6)
    except Exception:
        return None


def classify_volatility(smiles: str) -> Optional[str]:
    """
    Classify molecule volatility based on vapor pressure estimate.

    Args:
        smiles: SMILES string

    Returns:
        "high", "medium", or "low"
    """
    vp = estimate_vapor_pressure(smiles)
    mw = calculate_molecular_weight(smiles)

    if vp is None and mw is None:
        return None

    # Use molecular weight as primary indicator if VP unavailable
    if mw is not None:
        if mw < 150:
            return "high"
        elif mw < 250:
            return "medium"
        else:
            return "low"

    if vp is not None:
        if vp > 0.1:
            return "high"
        elif vp > 0.001:
            return "medium"
        else:
            return "low"

    return None


def get_full_properties(smiles: str) -> MolecularProperties:
    """
    Calculate all available molecular properties for a SMILES string.

    Args:
        smiles: SMILES string

    Returns:
        MolecularProperties dataclass with all calculated values
    """
    if not smiles:
        return MolecularProperties(
            smiles=smiles,
            valid=False,
            error_message="Empty SMILES string"
        )

    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors, Crippen, rdMolDescriptors

        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return MolecularProperties(
                smiles=smiles,
                valid=False,
                error_message="Invalid SMILES - could not parse"
            )

        logp = round(Crippen.MolLogP(mol), 2)
        mw = round(Descriptors.MolWt(mol), 2)
        tpsa = round(Descriptors.TPSA(mol), 2)
        rotatable = rdMolDescriptors.CalcNumRotatableBonds(mol)
        h_donors = rdMolDescriptors.CalcNumHBD(mol)
        h_acceptors = rdMolDescriptors.CalcNumHBA(mol)

        vp = estimate_vapor_pressure(smiles)
        volatility = classify_volatility(smiles)

        return MolecularProperties(
            smiles=smiles,
            valid=True,
            logp=logp,
            molecular_weight=mw,
            tpsa=tpsa,
            num_rotatable_bonds=rotatable,
            num_h_donors=h_donors,
            num_h_acceptors=h_acceptors,
            estimated_vapor_pressure=vp,
            volatility_class=volatility
        )

    except ImportError:
        return MolecularProperties(
            smiles=smiles,
            valid=False,
            error_message="RDKit not installed"
        )
    except Exception as e:
        return MolecularProperties(
            smiles=smiles,
            valid=False,
            error_message=str(e)
        )


def filter_by_logp(ingredients: list[dict], min_logp: float, max_logp: float = 10.0) -> list[dict]:
    """
    Filter ingredients by LogP range.

    Useful for selecting fixatives (high LogP) or volatile top notes (low LogP).

    Args:
        ingredients: List of ingredient dicts with 'smiles' key
        min_logp: Minimum LogP threshold
        max_logp: Maximum LogP threshold

    Returns:
        Filtered list of ingredients
    """
    result = []
    for ing in ingredients:
        smiles = ing.get('smiles', '')
        if smiles:
            logp = calculate_logp(smiles)
            if logp is not None and min_logp <= logp <= max_logp:
                ing_copy = ing.copy()
                ing_copy['calculated_logp'] = logp
                result.append(ing_copy)
    return result


def identify_fixatives(ingredients: list[dict], logp_threshold: float = 3.5) -> list[dict]:
    """
    Identify fixative ingredients (high LogP, low volatility).

    Fixatives are essential for dry skin formulations to extend longevity.

    Args:
        ingredients: List of ingredient dicts
        logp_threshold: Minimum LogP for fixative classification

    Returns:
        List of fixative ingredients
    """
    return filter_by_logp(ingredients, min_logp=logp_threshold)
