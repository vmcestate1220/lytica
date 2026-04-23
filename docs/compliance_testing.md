# Lytica Link — Compliance and Testing Protocol

**Companion document to:** `standards/lytica_protocol_v1.md` (LL-N1, v1)

This document defines the conformance, testing, and metadata requirements
a candidate catalytic agent must satisfy to be certified under the Lytica
Link standard (LL-N1). It is normative for LL-N1 v1 certification.

---

## 1. Certification Tiers

Tiers are assigned on the basis of the catalyst's measured efficiency
rating in Lyticas (L), where 1 L ≡ the native catalytic flux of the
Q43127 template (see `standards/lytica_protocol_v1.md` §2).

| Tier | Minimum rating | Intended use |
| --- | ---: | --- |
| **Bronze** | ≥ 1 L | Reference / native-equivalent; used for calibration and as the floor of certifiability. |
| **Silver** | ≥ 2 L | Standard-grade habitat deployment. |
| **Gold** | ≥ 5 L | Mass-optimized deployments; corresponds to the ~50 % uplift reduction reported in `sys_model/flux_simulator.py` (see white paper §3.3). |
| **Diamond** | ≥ 10 L | Long-duration, fusion-powered colonies. Provided for forward compatibility with power-unconstrained architectures where the per-turnover ATP cost is no longer the dominant system variable and catalyst mass dominates the logistics budget. |

All tiers additionally require the **structural** and **thermal**
benchmarks of LL-N1 §4 (decameric quaternary assembly; Tm ≥ 341.17 K) to
be met. A catalyst that exceeds the L threshold of a given tier but fails
either of these benchmarks is **not** certifiable at that tier.

The tier ladder is intentionally extensible: future revisions of LL-N1 may
add higher tiers without breaking backward compatibility.

## 2. Mandatory Stress-Test Protocol

### 2.1 Objective

Demonstrate that a candidate agent retains its rated catalytic flux under
sustained thermal load at the LL-N1 thermal benchmark.

### 2.2 Procedure

1. **Pre-stress measurement.** Measure steady-state catalytic flux (in
   Lyticas) under the LL-N1 reference conditions (70.3 kPa, 22 °C, Link
   Port composition per §4). Record as `L_pre`.
2. **Thermal hold.** Hold the agent at **341.17 K (68.0 °C)** — the Tm
   target — for **24 hours continuous**, at the LL-N1 reference pressure.
3. **Post-stress measurement.** Return the agent to reference conditions
   (22 °C) and re-measure steady-state flux under identical Link Port
   composition to step 1. Record as `L_post`.
4. **Retention calculation.** Compute

   ```
   flux_retention = L_post / L_pre
   ```

### 2.3 Pass criterion

`flux_retention ≥ 0.90`

A candidate that fails the retention threshold is **not** certifiable
under LL-N1 at any tier, regardless of its pre-stress L rating.

### 2.4 Reporting

The stress-test record shall include `L_pre`, `L_post`,
`flux_retention`, the temperature trace for the 24-hour hold, and the
measurement uncertainty (95 % CI) on `L_pre` and `L_post`. These values
are incorporated into the Lytica Link Certificate (§3).

## 3. Metadata Compliance — the Lytica Link Certificate

Every certified catalyst shipment shall be accompanied by a machine-
readable **Lytica Link Certificate** conforming to the JSON Schema below.
The certificate is the canonical compliance artifact; habitat integration
systems are entitled to refuse any agent that does not present a
conforming certificate.

### 3.1 JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lytica.link/schemas/certificate/v1.json",
  "title": "Lytica Link Certificate",
  "description": "Machine-readable compliance artifact for LL-N1 v1 catalysts.",
  "type": "object",
  "required": [
    "certificate_id",
    "standard",
    "tier",
    "manufacturer",
    "manufacture_date",
    "certified_L",
    "Tm_observed",
    "sequence_identity_to_Q43127",
    "stress_test"
  ],
  "properties": {
    "certificate_id": {
      "type": "string",
      "description": "Globally unique identifier for this certificate.",
      "pattern": "^LL-N1-[A-Z0-9-]{6,}$"
    },
    "standard": {
      "type": "string",
      "const": "LL-N1",
      "description": "Lytica Link standard designation."
    },
    "standard_revision": {
      "type": "string",
      "const": "v1"
    },
    "tier": {
      "type": "string",
      "enum": ["Bronze", "Silver", "Gold", "Diamond"]
    },
    "manufacturer": {
      "type": "object",
      "required": ["name"],
      "properties": {
        "name": { "type": "string" },
        "identifier": { "type": "string" },
        "contact": { "type": "string", "format": "email" }
      }
    },
    "manufacture_date": {
      "type": "string",
      "format": "date"
    },
    "certified_L": {
      "type": "number",
      "minimum": 1.0,
      "description": "Rated catalytic flux in Lyticas. 1 L = native Q43127 flux."
    },
    "Tm_observed": {
      "type": "number",
      "minimum": 341.17,
      "description": "Observed melting temperature in Kelvin. Must meet or exceed the LL-N1 thermal benchmark of 341.17 K."
    },
    "sequence_identity_to_Q43127": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 100.0,
      "description": "Percent amino-acid sequence identity of the catalytic chain to UniProt Q43127 (mature, residues 50-430)."
    },
    "quaternary_structure": {
      "type": "string",
      "const": "decamer",
      "description": "Mandatory eukaryotic GSII decameric (2x5) assembly."
    },
    "stress_test": {
      "type": "object",
      "required": ["L_pre", "L_post", "flux_retention", "hold_temperature_K", "hold_duration_hours"],
      "properties": {
        "L_pre": { "type": "number", "minimum": 1.0 },
        "L_post": { "type": "number", "minimum": 0.0 },
        "flux_retention": {
          "type": "number",
          "minimum": 0.90,
          "maximum": 1.0,
          "description": "L_post / L_pre; must be >= 0.90 for certification."
        },
        "hold_temperature_K": {
          "type": "number",
          "const": 341.17
        },
        "hold_duration_hours": {
          "type": "number",
          "const": 24
        }
      }
    }
  }
}
```

### 3.2 Tier–L consistency

The `tier` field must be consistent with `certified_L`:

- `tier == "Bronze"`   →  `certified_L >= 1`
- `tier == "Silver"`   →  `certified_L >= 2`
- `tier == "Gold"`     →  `certified_L >= 5`
- `tier == "Diamond"`  →  `certified_L >= 10`

Certificates that declare a tier inconsistent with `certified_L` are
invalid and shall be rejected.

### 3.3 Example

```json
{
  "certificate_id": "LL-N1-ACME-000042",
  "standard": "LL-N1",
  "standard_revision": "v1",
  "tier": "Gold",
  "manufacturer": {
    "name": "Acme Astrobio Ltd.",
    "identifier": "ACME",
    "contact": "compliance@acme.example"
  },
  "manufacture_date": "2026-04-15",
  "certified_L": 5.2,
  "Tm_observed": 342.05,
  "sequence_identity_to_Q43127": 96.8,
  "quaternary_structure": "decamer",
  "stress_test": {
    "L_pre": 5.20,
    "L_post": 4.85,
    "flux_retention": 0.933,
    "hold_temperature_K": 341.17,
    "hold_duration_hours": 24
  }
}
```

## 4. Interface Interoperability — the Link Port

The **Link Port** is the physical/chemical boundary across which NH₃
crosses from an upstream recovery module into a Lytica-1-compatible
bio-manufacturing module. To guarantee that any LL-N1-certified catalyst
can be driven by any LL-N1-compliant module, the Port specifies the
feed composition within narrow tolerances.

| Port parameter | Specification | Tolerance |
| --- | --- | --- |
| Feed pH | 7.5 | ± 0.3 |
| Buffer capacity (β) | ≥ 30 mmol·L⁻¹·pH⁻¹ | — |
| Total ammoniacal nitrogen (NH₃ + NH₄⁺) | 5 mM | 1 mM – 10 mM |
| Co-substrate glutamate | 10 mM | ≥ 5 mM |
| ATP (steady-state) | 3 mM | 2 mM – 5 mM |
| Mg²⁺ (cofactor) | 5 mM | ≥ 2 mM |
| Operating temperature | 22 °C | ± 2 °C |
| Operating pressure | 70.3 kPa | ± 2 kPa |

**Rationale.** The GS reaction
(`glutamate + NH₃ + ATP → glutamine + ADP + Pi`) requires divalent
cation (Mg²⁺ or Mn²⁺) coordination at the active site and is strongly
pH-dependent; plant GSII shows optimum activity in the mildly alkaline
range around pH 7.5. The ammoniacal-N window is chosen to remain well
above the native Km while below concentrations that promote substrate
inhibition or non-productive chemistry. Glutamate and ATP tolerances
are specified at steady state; transient excursions during startup and
shutdown are governed by a separate transient-operation annex
(out-of-scope for v1).

### 4.1 High-radiation operation (lunar surface)

Lunar surface deployment imposes continuous exposure to galactic cosmic
rays (GCR), solar-particle-event (SPE) protons, and secondary neutrons
generated by interaction of primary cosmic rays with regolith and
hardware. Two compounding effects on a Lytica-1 Link Port must be
mitigated:

1. **Radiolytic pH drift.** Water radiolysis produces H⁺, OH⁻, and
   short-lived radical species (·OH, e⁻_aq, ·H). In a poorly buffered
   feed, steady radiolysis creates a pH drift that exits the 7.5 ± 0.3
   envelope within hours.
2. **Direct radiation damage to the catalyst.** Primary and secondary
   particles cleave backbone peptide bonds, oxidize Cys/Met/Trp side
   chains, and accelerate deamidation of Asn/Gln. Shielding of the
   catalytic housing is mandatory.

The following supplemental specifications apply to any LL-N1 deployment
outside a radiation-shielded pressure vessel (i.e. anywhere on the
lunar surface, in cis-lunar transit, or in a partially shielded
subsurface habitat):

| Parameter | Standard (indoor) | High-radiation (surface) |
| --- | --- | --- |
| Buffer capacity (β) | ≥ 30 mmol·L⁻¹·pH⁻¹ | **≥ 100 mmol·L⁻¹·pH⁻¹** |
| Buffer species (recommended) | HEPES or phosphate, 20 mM | **HEPES + phosphate, ≥ 50 mM each** |
| Catalyst housing shielding | not required | **See §4.1.1** |

#### 4.1.1 Catalytic-housing shielding

The Lytica-1 housing shall be enclosed by a composite shield with both
a hydrogenous layer (for neutron moderation and SPE-proton attenuation)
and a high-Z layer (for gamma and secondary-photon attenuation):

| Layer | Material | Minimum thickness | Function |
| --- | --- | --- | --- |
| Inner | High-density polyethylene (HDPE) | **5 cm** | Moderates secondary neutrons; attenuates SPE protons; low-Z minimizes bremsstrahlung secondaries. |
| Outer | Lead (or equivalent areal density) | **2 mm** | Attenuates gammas and X-rays from solar flares and from neutron-capture secondaries in the HDPE. |

The stack above corresponds to approximately **5 g·cm⁻²**
water-equivalent, sufficient to bring acute SPE doses at the catalyst
within the operational envelope while holding GCR dose rate below
thresholds at which direct backbone cleavage dominates thermal
denaturation as the lifetime-limiting mode. Deployments at higher
latitudes, on prolonged surface missions, or in regolith-tower
configurations without regolith overburden may require increased
thicknesses; radiation-transport modelling (OLTARIS or equivalent)
against the mission's actual GCR/SPE spectrum is required before the
shielding specification is treated as sufficient.

Equivalent shielding by water, regolith, or an aluminum–HDPE layered
design is acceptable provided the total areal density and hydrogenous
fraction match or exceed the table above.

### 4.2 Non-compliance

A module whose Link Port deviates from §4 (or, where applicable, §4.1)
may not claim LL-N1 compatibility, even if it nominally hosts a
certified catalyst. The catalyst certificate (§3) is not sufficient on
its own; the Port specification is the obligation of the hosting
hardware.

---

*End of document — LL-N1 compliance and testing protocol, v1.*
