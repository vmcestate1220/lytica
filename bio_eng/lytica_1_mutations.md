# Lytica-1 Candidate Mutations — Thermostabilization Panel

**Template:** *Arabidopsis thaliana* GS2, UniProt **Q43127** (precursor, 430 aa)
**Numbering:** Q43127 precursor, 1-based. Mature chain = residues 50–430.
**Objective:** Raise Tm toward the LL-N1 Gold-tier benchmark of **341.17 K
(68.0 °C)** by rigidifying subunit–subunit interfaces and catalytic-loop
regions while preserving decameric assembly and catalytic activity.

---

## Analytical approach

All candidates below were identified by direct scan of the Q43127
sequence for motifs associated with thermal instability in published
protein-engineering literature, then filtered to the N-terminal β-grasp
fold (approximately residues 50–155 of the mature chain) and the
C-terminal catalytic domain's interface loops (approximately residues
155–430). Residue-level assignment of each candidate to a specific
subunit–subunit contact **requires structural validation**: a homology
model of Q43127 aligned to the maize cytosolic GS1a crystal structure
(PDB 2D3A) is the recommended next step before any of these substitutions
is committed to a synthesis order.

Stabilization modalities represented in the panel:

- **Deamidation mitigation** (N–G and tandem N–N motifs) — removes a
  common source of slow, irreversible loss-of-function that dominates
  lifetime at elevated temperatures.
- **Loop rigidification** (G–G motifs, G→P/A substitutions) — reduces the
  conformational entropy of the unfolded state, raising Tm.
- **Electrostatic surface optimization** (K→R at surface-exposed tandem
  Lys) — Arg's delocalized guanidinium provides longer-range, more
  thermally robust ionic interactions.
- **Disulfide engineering** (native Cys survey) — identifies candidate
  cysteine pairs for engineered inter-subunit disulfides.

---

## Panel

### 1. N248A — deamidation mitigation, catalytic domain

- **Context:** `...NISGT | N248-G249 | EVMP...`
- **Rationale:** N–G is the canonical high-risk deamidation motif; under
  sustained thermal load this position converts Asn to isoaspartate with
  loss of local geometry. Ala substitution eliminates the amide side
  chain entirely and preserves backbone geometry (minimal steric
  perturbation).
- **Risk:** Position lies inside the catalytic domain; activity screen
  required.

### 2. N302A — deamidation mitigation, near catalytic-core Cys

- **Context:** `...IEGDW | N302-G303 | AGCHTNY...` (C306 is 4 residues
  downstream)
- **Rationale:** A second N–G deamidation hotspot, adjacent to a native
  cysteine. Oxidation of C306 and deamidation of N302 are two
  independent mechanisms that converge on the same local structure; N302A
  removes one of the two axes of instability.
- **Risk:** Active-site proximity probable; flux must be measured pre-
  and post-mutation.

### 3. N145D — tandem-Asn removal, surface / loop region

- **Context:** `...PFRGG | N144-N145 | ILV...`
- **Rationale:** Tandem N144–N145 pair is unstable and likely surface-
  exposed (follows a G–G hinge, typical of a loop). Converting N145 to
  Asp removes one deamidation site and introduces a negative charge
  capable of forming a stabilizing salt bridge with a nearby basic
  residue (structural model required to confirm pairing partner).
- **Risk:** Low; surface position anticipated.

### 4. G143P — β-grasp / catalytic-domain hinge rigidification

- **Context:** `...RDPFR | G142-G143 | NNILV...`
- **Rationale:** G–G hinge between the β-grasp fold and the N-terminal
  catalytic-domain helices. Proline rigidifies the backbone at this
  junction, shrinking the conformational ensemble of the unfolded state.
  G143 (rather than G142) is proposed to preserve the upstream φ/ψ
  geometry of G142.
- **Risk:** Medium — hinge flexibility may be functional; screen for
  cooperativity loss between domains.

### 5. G86A — β-grasp domain loop rigidification

- **Context:** `...EYIWI | G85-G86 | SGID...`
- **Rationale:** G–G motif in the N-terminal β-grasp fold. Alanine (not
  proline) is chosen here because this position is more likely to lie
  within a β-strand terminus or tight turn where proline is geometrically
  prohibited. Ala reduces backbone entropy modestly without forcing a
  cis-peptide.
- **Risk:** Low–medium; β-grasp is a small, well-packed fold with known
  tolerance to surface substitutions.

### 6. G320P — catalytic-loop rigidification

- **Context:** `...SMREE | G319-G320 | FEVI...`
- **Rationale:** G–G motif in the C-terminal catalytic domain, in a
  region plausibly corresponding to the "Glu-flap" or an adjacent
  catalytic loop (aligned against bacterial/plant GS structures). Pro
  substitution at G320 rigidifies the loop; the upstream E317–E318 pair
  is preserved, maintaining any active-site glutamate coordination.
- **Risk:** Medium–high — this is the highest-confidence catalytic-loop
  candidate in the panel, which also makes it the most likely to
  compromise turnover. Priority candidate for a paired activity/Tm
  screen.

### 7. K175R — surface-Lys electrostatic optimization

- **Context:** `...EIFSN | K175-K176 | VSGE...` (tandem Lys pair in the
  catalytic domain)
- **Rationale:** Surface-exposed tandem lysines are common sites for
  K→R substitution to gain thermostability via the stronger, more
  delocalized charge of the guanidinium. One of the two is proposed
  (whichever is closer to an acidic partner on an adjacent subunit per
  the homology model); default to K175 (the more N-terminal of the
  pair).
- **Risk:** Low.

### 8. A/S → C at a β-grasp interface position paired with native C150
  (engineered inter-subunit disulfide — hypothesis only)

- **Context:** Native C150 in `...NILV | I149-C150 | DTWTP...` sits
  near the β-grasp–catalytic-domain boundary; the other native cysteines
  in the chain (C217, C237, C274, C306, C371) are candidates for
  engineered disulfide partners only if a structural model places a
  suitable Cα–Cα distance (≈ 4.5–7 Å) across an inter-subunit contact.
- **Rationale:** Engineered inter-subunit disulfides are a proven
  thermostabilization route (+5–15 K Tm is typical in successful cases)
  because they covalently lock the decameric assembly against ring-ring
  dissociation.
- **Status:** **Hypothesis — do not synthesize until a homology model
  identifies a specific (position, partner) pair with acceptable
  geometry.** Listed for completeness so that the structural-validation
  step returns with a concrete recommendation.

---

## Screening protocol (pre-certification)

Each candidate (or combination) shall be evaluated against both axes of
LL-N1 compliance before it enters a certification stress test:

1. **Tm shift** — measure by DSF or DSC; target ΔTm ≥ +3 K per
   stabilizing residue (additive combinations preferred to 5–10 K cumulative).
2. **Activity retention** — specific activity in L units, measured at the
   LL-N1 reference conditions (Link Port composition, 22 °C). Retention
   ≥ 80 % of the native template is the minimum bar for a candidate to
   advance; ≥ 95 % is preferred.
3. **Assembly integrity** — confirm decameric assembly by size-exclusion
   chromatography or native mass spectrometry. Loss of the decamer
   **disqualifies** the variant under LL-N1 §4.1 (structural benchmark),
   irrespective of Tm or activity.

Combinations that pass all three axes become candidates for the 24-hour
thermal-hold stress test defined in `docs/compliance_testing.md` §2.

---

## Caveats

- **These are sequence-analysis-derived hypotheses.** Every suggestion
  assumes a role (hinge, interface, surface) inferred from context, not
  from a solved structure of Q43127. Homology modelling against
  PDB 2D3A (maize GS1a) is the blocking next step.
- **Combinatorial effects are not additive in general.** Mutations that
  individually raise Tm can destabilize the decamer when combined;
  quaternary assembly must be verified for each combination.
- **Activity is the gate.** A catalyst that achieves the Tm target but
  fails the LL-N1 ≥ 90 % flux retention test (compliance doc §2) is not
  certifiable at any tier.

*End of document — Lytica-1 thermostabilization mutation panel, v1.*
