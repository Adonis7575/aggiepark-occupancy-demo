"""Single-frame occupancy decisions shared by the camera and PS5 experiment.

Scores are not calibrated probabilities. An unknown state never counts as open.
"""
import math
from numbers import Real


def occupancy_label(score, band=.15):
    """Defer scores inside the band around 0.5, or outside the valid score range.

    Boundary scores are accepted, matching the camera's original rule. A zero
    band gives the original binary baseline: scores >= 0.5 mean occupied.
    """
    if isinstance(band, bool) or not isinstance(band, Real) or not math.isfinite(band) or not 0 <= band < .5:
        raise ValueError('The uncertainty band must be finite and between 0 and 0.5 (exclusive).')
    if isinstance(score, bool) or not isinstance(score, Real) or not math.isfinite(score) or not 0 <= score <= 1:
        return 'unknown'
    if abs(score - .5) < band:
        return 'unknown'
    return 'occupied' if score >= .5 else 'empty'
