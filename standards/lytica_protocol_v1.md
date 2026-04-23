# The Lytica Link Standard

**Specification for Nitrogen Upcycling Efficiency in Closed-Loop Lunar Habitats**

| Field | Value |
| --- | --- |
| Designation | **LL-N1** (Lytica Link — Nitrogen 1) |
| Revision | v1 |
| Status | Draft technical white paper |
| Reference template | *Arabidopsis thaliana* GS2, UniProt Q43127 |

---

## 1. Scope

This document establishes the **Lytica Link** as the governing protocol for
the chemical interface between metabolic waste recovery and
bio-manufacturing inputs in closed-loop extraterrestrial life-support
systems. The Link defines the standardized handoff by which ammonia (NH₃)
generated as a metabolic byproduct is converted, under controlled
conditions, into stable amino-acid precursors suitable for downstream
biomass and nutrient synthesis.

**Applicability.** The standard applies to pressurized extraterrestrial
environments operating at the Lytica Link reference conditions:

| Parameter | Reference value |
| --- | --- |
| Pressure | 10.2 psi (70.3 kPa) |
| Temperature | 22 °C (295.15 K) |

Deployments outside these reference conditions are permitted but require an
equivalence declaration demonstrating that the chemical interface remains
within the tolerances defined in Section 4.

## 2. Terminology and Taxonomy

**Lytica-1.** The primary engineered catalytic agent specified by this
standard. Lytica-1 is templated on the decameric GSII architecture of
*Arabidopsis thaliana* glutamine synthetase (UniProt **Q43127**): two
pentameric rings arranged with D5 symmetry, yielding ten active sites at
the inter-subunit interfaces. Mature chain length is 381 aa following
cleavage of the native 49-aa chloroplast transit peptide.

**L (Lyticas).** The unit of catalytic flux efficiency. By definition,

> **1 L ≡ the native catalytic flux of the Q43127 template**

expressed as turnover per unit enzyme mass per unit time. A catalyst rated
at *n* L sustains *n* times the nitrogen-fixation throughput per gram of
enzyme relative to the native template, under reference conditions.

**The Link.** The biochemical junction at which the NH₃ → amino-acid
conversion is standardized for module interoperability. The Link specifies
the chemical form, flux envelope, and thermodynamic conditions at the
boundary between any upstream recovery module (waste, respiration,
greywater processing) and any downstream bio-manufacturing module
(nutrient synthesis, biomass growth). Compliance with the Link allows
modules from independent suppliers to be composed without bespoke
adapters.

## 3. System Impact (Significance and Use)

### 3.1 The Biochemical Catalytic Converter analogy

The Lytica Link functions, at a system level, as a **Biochemical Catalytic
Converter**: metabolic NH₃ enters the Link as an unstable, mass-inefficient
waste stream, and exits as a stable, high-value biochemical input
(glutamine, and thereby the amino-acid pool). Just as an automotive
catalytic converter converts toxic combustion products into benign exhaust
via controlled catalysis, the Lytica Link converts nitrogenous metabolic
byproducts into directly reusable inputs for habitat biomass production,
closing the nitrogen loop without the need to uplift fresh nitrogen
carriers from Earth for each cycle.

### 3.2 Operational Mass vs. Sustained Power

Two distinct system costs must be tracked independently:

- **Operational Mass** — the enzyme, consumable nitrogen-carrier, and
  associated handling mass that must be delivered from Earth to the Moon.
  Operational Mass **scales inversely with L**: higher-efficiency catalysts
  process more nitrogen per gram, which proportionally reduces the
  consumable uplift term.
- **Sustained Power** — the continuous electrical draw required to
  regenerate the ATP consumed by the GS reaction. The reaction is strictly
  coupled (**1 ATP per NH₃ fixed**), so Sustained Power scales with
  nitrogen throughput and is **stoichiometrically constant with respect to
  L**. Improving L reduces enzyme mass, not the per-turnover energy debt.

The Link explicitly separates these two quantities to prevent a common
design error in which catalyst improvements are over-credited with power
savings they do not provide.

### 3.3 Simulator evidence

Reference simulations (see `sys_model/flux_simulator.py`) for the
illustrative two-year, six-crew lunar scenario yield the following uplift
reductions relative to the L = 1 baseline:

| L rating | Total uplift mass | Savings vs. baseline |
| ---: | ---: | ---: |
| 1.00 | 1376.0 kg | — |
| 2.00 | 938.0 kg | 31.8 % |
| 3.00 | 792.0 kg | 42.4 % |
| **5.00** | **675.2 kg** | **50.9 %** |

A rating of **5 L thus yields approximately a 50 % reduction in
Earth-to-Moon uplift mass** for the modeled scenario, while Sustained Power
remains fixed at the stoichiometric ATP floor (~121 W average draw at 25 %
ATP-regeneration efficiency). This result constitutes the primary
quantitative justification for targeting an L ≥ 5 rating in the Lytica-1
program.

## 4. Technical Benchmarks

The following benchmarks are **mandatory** for any catalyst presented for
certification under the Lytica Link.

### 4.1 Structural benchmark

**Conservation of the decameric quaternary assembly is mandatory.**

Certified catalysts shall retain the eukaryotic GSII decameric architecture
(10 subunits arranged as two pentameric rings, D5 symmetry, 10 active
sites at inter-subunit interfaces). Deviations from the decameric state
(e.g. tetrameric, octameric, or dodecameric variants) are not certifiable
under LL-N1 regardless of observed catalytic performance, because the
active-site geometry of the eukaryotic GSII family is defined by the
inter-subunit interfaces of the decamer.

### 4.2 Thermal benchmark

**Target melting temperature:** `Tm ≥ 341.17 K (68.0 °C)`.

This target corresponds to a 10 % increase in absolute (Kelvin) melting
temperature relative to the terrestrial physiological reference of
37 °C (310.15 K). The Kelvin basis is specified deliberately: a
Celsius-basis percentage is physically meaningless because the Celsius
zero is arbitrary.

Space-grade certification under LL-N1 requires demonstration of the Tm
target by a validated thermal-denaturation assay, under the reference
pressure and atmospheric composition of Section 1.

### 4.3 Efficiency benchmark (informative)

The L metric is not, of itself, a pass/fail benchmark: the Link certifies
catalytic compliance, and the program separately targets L ≥ 5 for
first-generation deployment based on the uplift-mass analysis in
Section 3.3. Higher L ratings remain compatible with the Link provided the
structural and thermal benchmarks are met.

---

*End of document — Lytica Link LL-N1, v1 draft.*
