"""Nitrogen-flux simulator: payload-mass reduction via the L metric.

The efficiency metric **L** (Lyticas) is defined such that::

    1 L = catalytic flux of native (unoptimized) A. thaliana GS2 (Q43127)

i.e. the baseline is the wild-type enzyme's steady-state turnover rate.
A catalyst with L > 1 processes more ammonia per unit enzyme mass per unit
time, which linearly reduces the mass of on-board enzyme (and the mass of
make-up nitrogen carriers) that must be uplifted from Earth for a given
mission duration.

Model (intentionally simple)::

    M_total(L) = M_fixed + (N_daily * days) / L

where
    M_fixed     kg   mass-invariant habitat overhead (structure, plumbing)
    N_daily     kg   daily nitrogen-carrier uplift required at L = 1
    days              mission duration
    L            Lyticas; 1 L = native GS2 baseline

At L = 1 the model reproduces the native-enzyme uplift requirement; at
L = 2 the consumable term halves; and so on.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

# Baseline: 1 L is defined as the native Arabidopsis GS2 catalytic flux.
# Absolute kcat for native GS2 is a literature-sourced placeholder;
# downstream ratios in L are independent of this number, but cross-
# calibration to absolute flux (mol NH3 / s) depends on it.
NATIVE_GS2_KCAT_S = 21.0   # s^-1, placeholder (Ishiyama et al. 2004 range)
LYTICA_DEFINITION_NOTE = (
    "1 L is defined as the catalytic flux of native A. thaliana GS2 "
    "(Q43127). Native kcat ~ 21 s^-1 (placeholder; refine from lab data)."
)

BASELINE_L = 1.0

# --- ATP energy coefficient ------------------------------------------------
# The GS reaction is strictly ATP-coupled:
#
#     glutamate + NH3 + ATP  ->  glutamine + ADP + Pi
#
# Stoichiometry is 1 mol ATP per mol NH3 fixed, so the bulk energy demand
# scales with nitrogen throughput and is *independent of L*. L reduces the
# mass of enzyme required, not the ATP required per turnover.
ATP_PER_NH3 = 1.0                       # mol ATP / mol NH3 fixed
ATP_HYDROLYSIS_KJ_PER_MOL = 30.5        # standard-state |dG|; cellular ~50
NITROGEN_G_PER_MOL = 14.007             # atomic N
SECONDS_PER_DAY = 86400.0

# Electrical-to-chemical efficiency of the ATP-regeneration subsystem
# (placeholder; real systems span ~10-40% depending on the regeneration
# pathway -- photobiological, glucose-driven, electrocatalytic, etc.).
ATP_REGEN_EFFICIENCY = 0.25

# Energy coefficients, expressed per kg of elemental nitrogen processed:
#   THERMO  -- irreducible thermodynamic floor (|dG_ATP|)
#   SYSTEM  -- realistic electrical draw after regeneration losses
_MOL_N_PER_KG = 1000.0 / NITROGEN_G_PER_MOL
ENERGY_COEFFICIENT_THERMO_KJ_PER_KG_N = (
    ATP_PER_NH3 * ATP_HYDROLYSIS_KJ_PER_MOL * _MOL_N_PER_KG
)
ENERGY_COEFFICIENT_SYSTEM_KJ_PER_KG_N = (
    ENERGY_COEFFICIENT_THERMO_KJ_PER_KG_N / ATP_REGEN_EFFICIENCY
)


@dataclass
class MissionProfile:
    """Parameters of a single mission scenario."""

    duration_days: float
    fixed_mass_kg: float            # habitat overhead, L-independent
    nitrogen_kg_per_day: float      # uplift rate at L = 1
    name: str = "mission"


def payload_mass(profile: MissionProfile, L: float) -> float:
    """Total uplift mass (kg) for a given efficiency L.

    Raises ValueError for non-positive L (undefined: division by zero /
    negative flux has no physical meaning).
    """
    if L <= 0:
        raise ValueError(f"L must be positive; got {L}")
    consumable = profile.nitrogen_kg_per_day * profile.duration_days
    return profile.fixed_mass_kg + consumable / L


def mass_savings(profile: MissionProfile, L: float) -> float:
    """Absolute mass saved (kg) vs. the L = 1 baseline."""
    return payload_mass(profile, BASELINE_L) - payload_mass(profile, L)


def power_requirement_w(
    nitrogen_kg_per_day: float,
    regen_efficiency: float = ATP_REGEN_EFFICIENCY,
) -> float:
    """Average electrical power (W) to sustain a given N recycling rate.

    Uses the ATP-coupled stoichiometry of the GS reaction. Power is
    L-independent: improving catalyst efficiency reduces enzyme mass but
    not the per-turnover ATP demand.
    """
    if regen_efficiency <= 0:
        raise ValueError(f"regen_efficiency must be positive; got {regen_efficiency}")
    kj_per_kg_n = ENERGY_COEFFICIENT_THERMO_KJ_PER_KG_N / regen_efficiency
    daily_kj = nitrogen_kg_per_day * kj_per_kg_n
    return daily_kj * 1000.0 / SECONDS_PER_DAY


def mission_energy_kwh(
    profile: MissionProfile,
    regen_efficiency: float = ATP_REGEN_EFFICIENCY,
) -> float:
    """Integrated electrical energy (kWh) for the full mission."""
    power_w = power_requirement_w(profile.nitrogen_kg_per_day, regen_efficiency)
    return power_w * profile.duration_days * SECONDS_PER_DAY / 3_600_000.0


def sweep(profile: MissionProfile, L_values) -> pd.DataFrame:
    """Return a DataFrame of uplift mass and power across an L sweep.

    ``power_w`` is reported once per row for reference but does not vary
    with L (see module docstring).
    """
    L_arr = np.asarray(L_values, dtype=float)
    baseline = payload_mass(profile, BASELINE_L)
    total = np.array([payload_mass(profile, L) for L in L_arr])
    power_w = power_requirement_w(profile.nitrogen_kg_per_day)
    return pd.DataFrame(
        {
            "L": L_arr,
            "total_mass_kg": total,
            "savings_kg": baseline - total,
            "savings_pct": 100.0 * (baseline - total) / baseline,
            "power_w": np.full_like(L_arr, power_w),
        }
    )


if __name__ == "__main__":
    # Illustrative scenario: 2-year lunar habitat, 6 crew, coarse numbers.
    demo = MissionProfile(
        duration_days=730,
        fixed_mass_kg=500.0,
        nitrogen_kg_per_day=1.2,
        name="Lunar-2yr-6crew (illustrative)",
    )
    L_sweep = [1.0, 1.25, 1.5, 2.0, 3.0, 5.0]
    df = sweep(demo, L_sweep)
    print(LYTICA_DEFINITION_NOTE)
    print(f"\nScenario: {demo.name}")
    print(f"  duration = {demo.duration_days} d, "
          f"fixed = {demo.fixed_mass_kg} kg, "
          f"N rate at L=1 = {demo.nitrogen_kg_per_day} kg/d")
    print()
    print(f"Energy coefficient (thermodynamic floor): "
          f"{ENERGY_COEFFICIENT_THERMO_KJ_PER_KG_N:.1f} kJ per kg N")
    print(f"Energy coefficient (at {ATP_REGEN_EFFICIENCY:.0%} regen efficiency): "
          f"{ENERGY_COEFFICIENT_SYSTEM_KJ_PER_KG_N:.1f} kJ per kg N")
    print(f"Sustained power draw:    {power_requirement_w(demo.nitrogen_kg_per_day):.2f} W")
    print(f"Mission energy total:    {mission_energy_kwh(demo):.1f} kWh")
    print()
    print(df.to_string(index=False, float_format=lambda x: f"{x:8.2f}"))
