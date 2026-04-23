"""Engineering specifications for the Lytica-1 reference material.

The Lytica-1 design is templated on *Arabidopsis thaliana* glutamine
synthetase 2 (GS2, UniProt Q43127), a member of the eukaryotic GSII family.
Eukaryotic GSII enzymes assemble as a **decamer** (two stacked pentameric
rings, D5 symmetry), with ten active sites formed at the interfaces between
adjacent subunits within each ring. This decameric quaternary structure is
the basis of the Lytica-1 design: the shared interfaces carry the catalytic
machinery, so engineered stabilization of the ring-ring and intra-ring
contacts is expected to improve both thermal robustness and operational
durability without disrupting activity.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from Bio import SeqIO

TEMPLATE_FASTA = Path(__file__).parent / "gs2_template.fasta"

# Template accession and catalytic-domain constants for A. thaliana GS2.
# The mature chloroplastic enzyme begins after cleavage of the ~49-aa
# N-terminal chloroplast transit peptide; the catalytic core spans the
# remainder of the chain (UniProt Q43127 feature annotation).
TEMPLATE_ACCESSION = "Q43127"
TEMPLATE_LENGTH_AA = 430
TRANSIT_PEPTIDE_END = 49  # cleavage between residues 49 and 50
CATALYTIC_DOMAIN_START = TRANSIT_PEPTIDE_END + 1
CATALYTIC_DOMAIN_END = TEMPLATE_LENGTH_AA
MATURE_LENGTH_AA = CATALYTIC_DOMAIN_END - CATALYTIC_DOMAIN_START + 1

# Quaternary assembly: eukaryotic GSII decamer (5+5).
OLIGOMERIC_STATE = "decamer"
SUBUNITS_PER_OLIGOMER = 10
SUBUNITS_PER_RING = 5
ACTIVE_SITES_PER_OLIGOMER = 10

# Thermal stability target. Baseline Tm is the terrestrial 37 degC reference,
# expressed in Kelvin for a physically meaningful percent change. A "+10%"
# target in Celsius (40.7 degC) would be trivially close to baseline, so the
# Lytica-1 target is +10% in Kelvin: 310.15 K * 1.10 = 341.17 K (~68 degC).
TM_BASELINE_K = 310.15            # 37 degC terrestrial baseline
TM_TARGET_FRACTION = 1.10         # +10% in absolute (Kelvin) units
TM_TARGET_K = TM_BASELINE_K * TM_TARGET_FRACTION
TM_TARGET_C = TM_TARGET_K - 273.15


@dataclass
class LyticaStandard:
    """Standard Reference Material for the Lytica-1 catalyst.

    Stores environmental variables and structural constants for the
    reference material. The design is based on the decameric eukaryotic
    GSII architecture of *Arabidopsis thaliana* GS2 (UniProt Q43127):
    ten catalytic subunits arranged as two pentameric rings, with active
    sites at subunit interfaces. Placeholder index fields
    (``thermal_stability``, ``durability_index``) are normalized to the
    native GS2 baseline (1.0 = native performance).

    Attributes
    ----------
    name:
        Human-readable identifier for the reference material.
    template_accession:
        UniProt accession of the structural template.
    sequence_length_aa:
        Full precursor length in amino acids.
    mature_length_aa:
        Mature catalytic-chain length after transit-peptide cleavage.
    oligomeric_state:
        Quaternary assembly descriptor (``"decamer"``).
    tm_baseline_k / tm_target_k:
        Melting-temperature baseline and engineering target (Kelvin).
    thermal_stability:
        Dimensionless stability index, normalized to native GS2 (1.0 =
        native Tm; target is ``TM_TARGET_FRACTION`` = 1.10).
    durability_index:
        Dimensionless durability index under cyclic orbital stress
        (1.0 = native baseline).
    """

    name: str = "Lytica-1"
    template_accession: str = TEMPLATE_ACCESSION
    sequence_length_aa: int = TEMPLATE_LENGTH_AA
    mature_length_aa: int = MATURE_LENGTH_AA
    oligomeric_state: str = OLIGOMERIC_STATE
    subunits_per_oligomer: int = SUBUNITS_PER_OLIGOMER
    active_sites_per_oligomer: int = ACTIVE_SITES_PER_OLIGOMER
    tm_baseline_k: float = TM_BASELINE_K
    tm_target_k: float = TM_TARGET_K
    thermal_stability: float = 1.0
    durability_index: float = 1.0
    reference_pressure_kpa: float = 101.325
    notes: str = ""
    metadata: dict = field(default_factory=dict)

    def meets_thermal_target(self) -> bool:
        """True iff the stability index reaches the +10% Tm target."""
        return self.thermal_stability >= TM_TARGET_FRACTION

    def load_template_sequence(self) -> str:
        """Return the template amino-acid sequence from the FASTA file."""
        record = SeqIO.read(TEMPLATE_FASTA, "fasta")
        return str(record.seq)


DEFAULT_STANDARD = LyticaStandard(
    name="Lytica-1",
    template_accession=TEMPLATE_ACCESSION,
    sequence_length_aa=TEMPLATE_LENGTH_AA,
    mature_length_aa=MATURE_LENGTH_AA,
    oligomeric_state=OLIGOMERIC_STATE,
    subunits_per_oligomer=SUBUNITS_PER_OLIGOMER,
    active_sites_per_oligomer=ACTIVE_SITES_PER_OLIGOMER,
    tm_baseline_k=TM_BASELINE_K,
    tm_target_k=TM_TARGET_K,
    thermal_stability=1.0,
    durability_index=1.0,
    notes=(
        "Baseline values reflect native A. thaliana GS2 (Q43127). "
        "Thermal-stability target is +10% Tm in Kelvin (341.17 K / 68.0 C)."
    ),
)


if __name__ == "__main__":
    s = DEFAULT_STANDARD
    print(f"Reference material: {s.name}")
    print(f"  template:          {s.template_accession} ({s.sequence_length_aa} aa precursor)")
    print(f"  mature length:     {s.mature_length_aa} aa (residues {CATALYTIC_DOMAIN_START}-{CATALYTIC_DOMAIN_END})")
    print(f"  quaternary state:  {s.oligomeric_state} ({s.subunits_per_oligomer} subunits, "
          f"{s.active_sites_per_oligomer} active sites)")
    print(f"  Tm baseline:       {s.tm_baseline_k:.2f} K ({s.tm_baseline_k - 273.15:.2f} C)")
    print(f"  Tm target (+10%):  {s.tm_target_k:.2f} K ({s.tm_target_k - 273.15:.2f} C)")
    print(f"  thermal_stability: {s.thermal_stability} (target {TM_TARGET_FRACTION})")
    print(f"  durability_index:  {s.durability_index}")
