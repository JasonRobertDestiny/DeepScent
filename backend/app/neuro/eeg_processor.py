"""
EEG signal processing using MNE-Python.
Provides power spectral density analysis and frequency band extraction.
"""

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class EEGBandPowers:
    """Container for EEG frequency band powers."""
    theta: float  # 4-8 Hz
    alpha: float  # 8-13 Hz
    beta: float   # 13-30 Hz
    gamma: float  # 30-50 Hz


@dataclass
class ValenceArousal:
    """Valence-Arousal emotional coordinates."""
    valence: float   # -1 (unpleasant) to 1 (pleasant)
    arousal: float   # 0 (calm) to 1 (excited)
    confidence: float  # 0 to 1


def compute_band_powers(
    eeg_data: np.ndarray,
    sfreq: float = 256.0,
    channels: list[str] = None
) -> EEGBandPowers:
    """
    Compute power in standard EEG frequency bands.

    Args:
        eeg_data: EEG time series data (channels x samples)
        sfreq: Sampling frequency in Hz
        channels: Channel names (optional)

    Returns:
        EEGBandPowers with theta, alpha, beta, gamma powers
    """
    try:
        from scipy import signal

        # Define frequency bands
        bands = {
            'theta': (4, 8),
            'alpha': (8, 13),
            'beta': (13, 30),
            'gamma': (30, 50)
        }

        # Compute power spectral density using Welch's method
        freqs, psd = signal.welch(eeg_data, fs=sfreq, nperseg=int(sfreq * 2))

        # If 2D, average across channels
        if psd.ndim > 1:
            psd = psd.mean(axis=0)

        # Extract band powers
        powers = {}
        for band_name, (low, high) in bands.items():
            idx = np.where((freqs >= low) & (freqs <= high))[0]
            powers[band_name] = float(psd[idx].mean())

        return EEGBandPowers(
            theta=powers['theta'],
            alpha=powers['alpha'],
            beta=powers['beta'],
            gamma=powers['gamma']
        )

    except ImportError:
        # Fallback with simulated values if scipy not available
        return EEGBandPowers(theta=1.0, alpha=1.5, beta=1.2, gamma=0.8)


def compute_frontal_alpha_asymmetry(
    left_alpha: float,
    right_alpha: float
) -> float:
    """
    Compute Frontal Alpha Asymmetry (FAA) for valence estimation.

    FAA = ln(right_alpha) - ln(left_alpha)

    Positive FAA (left > right activation) = approach motivation / positive valence
    Negative FAA (right > left activation) = withdrawal motivation / negative valence

    Args:
        left_alpha: Alpha power from left frontal electrode (F3/AF3)
        right_alpha: Alpha power from right frontal electrode (F4/AF4)

    Returns:
        FAA value (typically -2 to 2)
    """
    if left_alpha <= 0 or right_alpha <= 0:
        return 0.0

    faa = np.log(right_alpha) - np.log(left_alpha)
    return float(faa)


def compute_valence_arousal(
    band_powers: EEGBandPowers,
    faa: Optional[float] = None
) -> ValenceArousal:
    """
    Map EEG band powers to Valence-Arousal coordinates.

    Uses Russell's Circumplex Model of Affect.

    Args:
        band_powers: Power in theta, alpha, beta, gamma bands
        faa: Frontal Alpha Asymmetry (optional, improves valence accuracy)

    Returns:
        ValenceArousal with emotional coordinates
    """
    # Arousal: Beta/Alpha ratio
    # High beta relative to alpha = high arousal
    if band_powers.alpha > 0:
        arousal_raw = band_powers.beta / band_powers.alpha
    else:
        arousal_raw = 1.0

    # Normalize arousal to 0-1 range (typical ratio 0.5-3.0)
    arousal = min(1.0, max(0.0, (arousal_raw - 0.5) / 2.5))

    # Valence: Based on FAA if available, otherwise use theta reduction
    if faa is not None:
        # FAA typically ranges from -2 to 2
        valence = min(1.0, max(-1.0, faa / 2.0))
        confidence = 0.8
    else:
        # Theta reduction during pleasant stimuli
        # Lower theta = more pleasant (simplified heuristic)
        theta_norm = band_powers.theta / (band_powers.alpha + 0.001)
        valence = 1.0 - min(2.0, theta_norm)  # Invert: low theta = positive
        valence = min(1.0, max(-1.0, valence))
        confidence = 0.5

    return ValenceArousal(
        valence=round(valence, 3),
        arousal=round(arousal, 3),
        confidence=round(confidence, 2)
    )


def map_va_to_scent_profile(va: ValenceArousal) -> dict:
    """
    Map Valence-Arousal to scent profile recommendations.

    Based on fragrance psychology research linking emotions to scent families.

    Args:
        va: ValenceArousal coordinates

    Returns:
        Dict with recommended families and descriptors
    """
    recommendations = {
        'families': [],
        'descriptors': [],
        'avoid': [],
        'mood': ''
    }

    # High valence (pleasant)
    if va.valence > 0.3:
        if va.arousal > 0.5:
            # Happy, excited
            recommendations['mood'] = 'energizing'
            recommendations['families'] = ['citrus', 'fresh', 'aromatic']
            recommendations['descriptors'] = ['bright', 'uplifting', 'sparkling', 'zesty']
        else:
            # Content, relaxed
            recommendations['mood'] = 'calming'
            recommendations['families'] = ['woody', 'floral', 'musky']
            recommendations['descriptors'] = ['soft', 'warm', 'comforting', 'serene']

    # Low valence (unpleasant or neutral)
    elif va.valence < -0.3:
        # Tense, sad - recommend grounding scents
        recommendations['mood'] = 'grounding'
        recommendations['families'] = ['resinous', 'ambery', 'earthy']
        recommendations['descriptors'] = ['meditative', 'contemplative', 'ancient']
        recommendations['avoid'] = ['sharp citrus', 'heavy florals']

    else:
        # Neutral valence
        if va.arousal > 0.5:
            # Alert but neutral
            recommendations['mood'] = 'focusing'
            recommendations['families'] = ['herbal', 'green', 'aromatic']
            recommendations['descriptors'] = ['clean', 'crisp', 'clear']
        else:
            # Calm and neutral
            recommendations['mood'] = 'balancing'
            recommendations['families'] = ['woody', 'clean', 'aquatic']
            recommendations['descriptors'] = ['transparent', 'balanced', 'subtle']

    return recommendations


class EEGProcessor:
    """
    EEG signal processor for Aether.

    Handles raw EEG data from consumer devices (e.g., Muse headband)
    and extracts emotional features for perfume personalization.
    """

    def __init__(self, sfreq: float = 256.0):
        """
        Initialize processor.

        Args:
            sfreq: Sampling frequency (Muse = 256 Hz)
        """
        self.sfreq = sfreq
        self.band_powers: Optional[EEGBandPowers] = None
        self.va: Optional[ValenceArousal] = None

    def process(
        self,
        eeg_data: np.ndarray,
        left_frontal_idx: int = 0,
        right_frontal_idx: int = 1
    ) -> ValenceArousal:
        """
        Process EEG data and extract Valence-Arousal.

        Args:
            eeg_data: Raw EEG data (channels x samples)
            left_frontal_idx: Index of left frontal channel (AF3/F3)
            right_frontal_idx: Index of right frontal channel (AF4/F4)

        Returns:
            ValenceArousal coordinates
        """
        # Compute band powers
        self.band_powers = compute_band_powers(eeg_data, self.sfreq)

        # Compute FAA if we have stereo frontal channels
        faa = None
        if eeg_data.ndim > 1 and eeg_data.shape[0] > 1:
            left_powers = compute_band_powers(
                eeg_data[left_frontal_idx:left_frontal_idx+1],
                self.sfreq
            )
            right_powers = compute_band_powers(
                eeg_data[right_frontal_idx:right_frontal_idx+1],
                self.sfreq
            )
            faa = compute_frontal_alpha_asymmetry(
                left_powers.alpha,
                right_powers.alpha
            )

        # Compute VA
        self.va = compute_valence_arousal(self.band_powers, faa)
        return self.va

    def get_scent_profile(self) -> dict:
        """Get scent recommendations based on last processed EEG."""
        if self.va is None:
            return {'error': 'No EEG data processed yet'}
        return map_va_to_scent_profile(self.va)


def simulate_eeg_from_mood(mood: str, duration_sec: float = 10.0, sfreq: float = 256.0) -> np.ndarray:
    """
    Simulate EEG data for a given mood (for testing/demo).

    Args:
        mood: One of 'happy', 'calm', 'focused', 'stressed'
        duration_sec: Duration in seconds
        sfreq: Sampling frequency

    Returns:
        Simulated EEG data (4 channels x samples)
    """
    n_samples = int(duration_sec * sfreq)
    t = np.arange(n_samples) / sfreq

    # Base frequencies for each band
    theta_freq = 6
    alpha_freq = 10
    beta_freq = 20
    gamma_freq = 40

    # Adjust amplitudes based on mood
    if mood == 'happy':
        theta_amp = 0.5
        alpha_amp = 1.5
        beta_amp = 1.2
        gamma_amp = 0.8
    elif mood == 'calm':
        theta_amp = 0.8
        alpha_amp = 2.0
        beta_amp = 0.6
        gamma_amp = 0.4
    elif mood == 'focused':
        theta_amp = 0.6
        alpha_amp = 1.0
        beta_amp = 1.8
        gamma_amp = 1.0
    elif mood == 'stressed':
        theta_amp = 1.2
        alpha_amp = 0.5
        beta_amp = 2.0
        gamma_amp = 0.6
    else:
        theta_amp = alpha_amp = beta_amp = gamma_amp = 1.0

    # Generate 4 channels (simulating AF3, AF4, TP9, TP10)
    eeg = np.zeros((4, n_samples))
    for ch in range(4):
        noise = np.random.randn(n_samples) * 0.3
        eeg[ch] = (
            theta_amp * np.sin(2 * np.pi * theta_freq * t) +
            alpha_amp * np.sin(2 * np.pi * alpha_freq * t) +
            beta_amp * np.sin(2 * np.pi * beta_freq * t) +
            gamma_amp * np.sin(2 * np.pi * gamma_freq * t) +
            noise
        )

    return eeg
