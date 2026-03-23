"""
AFF Curved IM Nail — Extended Analysis
BMEN 383 – Continuum/Solid Mechanics II

Five additional analyses beyond the baseline 2D sagittal model:
  1. Frontal-plane (coronal) bending superposition
  2. Neutral-axis compatibility index
  3. Two-segment EI model (tip stiffness discontinuity)
  4. Strain and fatigue-based interpretation
  5. Multi-objective comparison of straight vs curved nail

Outputs: extended_analysis_readme.md
"""

import numpy as np
import json
from pathlib import Path

np.random.seed(42)

# ──────────────────────────────────────────────
# 1. LOAD PARAMETERS (same as run_calculations.py)
# ──────────────────────────────────────────────
with open(Path(__file__).parent / "model_parameters.json") as f:
    params = json.load(f)

# --- Nominal values ---
E_b  = 17.0e3    # MPa
E_n  = 110.0e3   # MPa
r_o  = 13.0      # mm
r_i  = 7.5       # mm
r_n  = 5.5       # mm
R_f  = 1100.0    # mm
R_n  = 1500.0    # mm
L    = 250.0     # mm  (nail segment length)
L_diaph = 400.0  # mm  (full diaphyseal arc)
k_N  = 2.4
W    = 700.0     # N
sigma_y_t = 108.0
sigma_y_t_conservative = 100.0
sigma_u_t = 133.0  # MPa (tensile ultimate, bone)
FOS_required = 2.0

# NEW: Frontal-plane parameters
d_ML = 48.0       # mm — femoral offset (hip center to shaft axis), nominal
                   # Literature: ~38–57 mm; we use 48 mm as central estimate
                   # Tatka et al. 2022: mean 38.2 mm (cadaveric)
                   # Lechler et al. 2014: rotation-corrected mean 57 mm
                   # Biggi et al. 2020: "global offset" concept

# Fatigue parameters
sigma_endurance_fraction = 0.45  # Conservative: 45% of sigma_u_t
sigma_endurance = sigma_endurance_fraction * sigma_u_t  # ~60 MPa

# ──────────────────────────────────────────────
# 2. REUSE BASELINE CALCULATIONS
# ──────────────────────────────────────────────
n_mod = E_n / E_b  # modular ratio

A_b = np.pi * (r_o**2 - r_i**2)
I_b = (np.pi / 4) * (r_o**4 - r_i**4)
A_n = np.pi * r_n**2
I_n = (np.pi / 4) * r_n**4

# Bow eccentricity and sagittal bending moment
e_sag = L_diaph**2 / (8 * R_f)
N_load = k_N * W
M_sag = N_load * e_sag

# Nail eccentricity (curvature mismatch)
y_n_straight = (L**2 / 8) * (1/R_f - 1/R_n)

# Composite NA shift (straight nail)
y_bar = (n_mod * A_n * y_n_straight) / (A_b + n_mod * A_n)

# Composite I (straight nail)
I_comp_straight = (I_b + A_b * y_bar**2
                   + n_mod * I_n + n_mod * A_n * (y_n_straight - y_bar)**2)

# Composite I (curved/matched nail, y_n=0)
I_comp_curved = I_b + n_mod * I_n

# c_lat for each case
c_lat_bone = r_o
c_lat_straight = r_o - y_bar
c_lat_curved = r_o  # y_bar = 0 for matched

# ── Sagittal stresses (recap) ──
sigma_ax_bone = N_load / A_b
sigma_ax_comp = N_load / (A_b + n_mod * A_n)

sigma_bend_sag_bone = M_sag * c_lat_bone / I_b
sigma_bend_sag_straight = M_sag * c_lat_straight / I_comp_straight
sigma_bend_sag_curved = M_sag * c_lat_curved / I_comp_curved

sigma_lat_sag_bone = -sigma_ax_bone + sigma_bend_sag_bone
sigma_lat_sag_straight = -sigma_ax_comp + sigma_bend_sag_straight
sigma_lat_sag_curved = -sigma_ax_comp + sigma_bend_sag_curved

# ──────────────────────────────────────────────
# PHASE 1: FRONTAL-PLANE BENDING
# ──────────────────────────────────────────────
# The frontal-plane bending moment arises from the medial offset
# of the hip joint center relative to the femoral shaft axis.
# M_front = N * d_ML
# For a circular cross-section, I is the same regardless of bending axis.

M_front = N_load * d_ML

# Frontal-plane bending stress at lateral cortex
# In frontal plane, the lateral cortex is on the tension side
# (hip load is medial to shaft, creating M-L bending)
# For bone only: use I_b and c = r_o
# For nailed cases: the nail is centered on bone axis in the M-L plane
# (nail sits in the medullary canal, which is centered M-L)
# So in the frontal plane, y_n_frontal = 0 for BOTH straight and curved nails
# → composite I_front is the same for both nailed cases
I_comp_front = I_b + n_mod * I_n  # same for straight and curved in frontal plane

sigma_front_bone = M_front * r_o / I_b
sigma_front_straight = M_front * r_o / I_comp_front  # nail centered in M-L
sigma_front_curved = M_front * r_o / I_comp_front     # same as straight

# Total lateral cortex stress (sagittal + frontal, scalar superposition)
# Both components are tensile at the lateral cortex
sigma_total_bone = sigma_lat_sag_bone + sigma_front_bone
sigma_total_straight = sigma_lat_sag_straight + sigma_front_straight
sigma_total_curved = sigma_lat_sag_curved + sigma_front_curved

FOS_total_bone = sigma_y_t_conservative / sigma_total_bone
FOS_total_straight = sigma_y_t_conservative / sigma_total_straight
FOS_total_curved = sigma_y_t_conservative / sigma_total_curved

# ──────────────────────────────────────────────
# PHASE 2: COMPATIBILITY INDEX
# ──────────────────────────────────────────────
# C = |y_n| / r_o  (dimensionless)
C_straight = abs(y_n_straight) / r_o
C_curved = 0.0  # by definition, bow-matched

# Also compute for the Asian female scenario
R_f_asian = 880.0
y_n_straight_asian = (L**2 / 8) * (1/R_f_asian - 1/R_n)
C_straight_asian = abs(y_n_straight_asian) / r_o
C_curved_asian = 0.0

# ──────────────────────────────────────────────
# PHASE 3: TWO-SEGMENT EI MODEL
# ──────────────────────────────────────────────
# Region 1 (nailed): EI_1 = E_b * I_b + E_n * I_n
# Region 2 (bone only): EI_2 = E_b * I_b
EI_1 = E_b * I_b + E_n * I_n  # N·mm²
EI_2 = E_b * I_b               # N·mm²

# Use M_front at the transition (conservative)
M_tip = M_front  # use frontal moment as representative

# Curvatures
kappa_1 = M_tip / EI_1
kappa_2 = M_tip / EI_2
delta_kappa = kappa_2 - kappa_1  # curvature jump

# Strain just distal to tip (bone-only region)
eps_lat_tip_boneonly = kappa_2 * r_o

# For comparison: short nail (L1_short = 150 mm) vs long nail (L1_long = 300 mm)
# In a simplified model, if we assume the transition moves to a region
# where the bending moment is lower (more distal), we can approximate:
# M_tip_short ≈ M_front (transition in high-moment zone, subtrochanteric)
# M_tip_long ≈ 0.6 * M_front (transition pushed distally, lower moment)

M_tip_short = M_front
M_tip_long = 0.6 * M_front  # moment reduced ~40% distally

kappa_2_short = M_tip_short / EI_2
kappa_2_long = M_tip_long / EI_2
kappa_1_short = M_tip_short / EI_1
kappa_1_long = M_tip_long / EI_1

delta_kappa_short = kappa_2_short - kappa_1_short
delta_kappa_long = kappa_2_long - kappa_1_long

eps_tip_short = kappa_2_short * r_o
eps_tip_long = kappa_2_long * r_o

# Also compute the "stiffness ratio" EI_1/EI_2
stiffness_ratio = EI_1 / EI_2

# ──────────────────────────────────────────────
# PHASE 4: STRAIN AND FATIGUE INTERPRETATION
# ──────────────────────────────────────────────
eps_y = 0.80 / 100  # yield strain (0.80%)

# Strains from total stress (sag + frontal)
eps_total_bone = sigma_total_bone / E_b
eps_total_straight = sigma_total_straight / E_b
eps_total_curved = sigma_total_curved / E_b

# Fatigue safety factors
FOS_fatigue_bone = sigma_endurance / sigma_total_bone
FOS_fatigue_straight = sigma_endurance / sigma_total_straight
FOS_fatigue_curved = sigma_endurance / sigma_total_curved

# For reference: sagittal-only strains (already computed in baseline)
eps_sag_bone = sigma_lat_sag_bone / E_b
eps_sag_straight = sigma_lat_sag_straight / E_b
eps_sag_curved = sigma_lat_sag_curved / E_b

# ──────────────────────────────────────────────
# PHASE 5: MULTI-OBJECTIVE SCORECARD
# ──────────────────────────────────────────────
# We build a qualitative scorecard comparing straight vs curved nail
# across multiple metrics

# Asian female scenario (full calculation)
N_load_asian = 2.4 * 550  # N
e_sag_asian = 370.0**2 / (8 * R_f_asian)
M_sag_asian = N_load_asian * e_sag_asian
M_front_asian = N_load_asian * d_ML

# Straight nail, Asian
y_bar_asian = (n_mod * A_n * y_n_straight_asian) / (A_b + n_mod * A_n)
I_comp_straight_asian = (I_b + A_b * y_bar_asian**2
                         + n_mod * I_n + n_mod * A_n * (y_n_straight_asian - y_bar_asian)**2)
c_lat_straight_asian = r_o - y_bar_asian

sigma_sag_bone_asian = -N_load_asian / A_b + M_sag_asian * r_o / I_b
sigma_sag_straight_asian = -N_load_asian / (A_b + n_mod * A_n) + M_sag_asian * c_lat_straight_asian / I_comp_straight_asian
sigma_sag_curved_asian = -N_load_asian / (A_b + n_mod * A_n) + M_sag_asian * r_o / I_comp_curved

sigma_front_bone_asian = M_front_asian * r_o / I_b
sigma_front_nail_asian = M_front_asian * r_o / I_comp_front

sigma_total_bone_asian = sigma_sag_bone_asian + sigma_front_bone_asian
sigma_total_straight_asian = sigma_sag_straight_asian + sigma_front_nail_asian
sigma_total_curved_asian = sigma_sag_curved_asian + sigma_front_nail_asian

FOS_total_bone_asian = sigma_y_t_conservative / sigma_total_bone_asian
FOS_total_straight_asian = sigma_y_t_conservative / sigma_total_straight_asian
FOS_total_curved_asian = sigma_y_t_conservative / sigma_total_curved_asian

# ──────────────────────────────────────────────
# GENERATE MARKDOWN
# ──────────────────────────────────────────────
md = []

# ---- TITLE ----
md.append("# AFF Curved IM Nail — Extended Biomechanical Analysis")
md.append("")
md.append("> **Course:** BMEN 383 — Continuum / Solid Mechanics II")
md.append("> **Auto-generated by** `run_extended_analysis.py`")
md.append("> **Date:** 2026-03-22")
md.append("> **Complements:** `numerical_results.md` (baseline 2D sagittal model)")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 1: Introduction & Scope
# ════════════════════════════════════════════════
md.append("## 1. Introduction & Scope")
md.append("")
md.append("This document extends the baseline 2D composite-beam analysis (see `numerical_results.md`) with five additional analyses to provide a more complete evaluation of straight vs. curved (bow-matched) intramedullary nails for atypical femoral fractures (AFF):")
md.append("")
md.append("1. **Frontal-plane (coronal) bending** — superposition of the dominant medial-lateral hip bending moment")
md.append("2. **Neutral-axis compatibility index** — a dimensionless metric for nail-bone curvature mismatch")
md.append("3. **Two-segment EI model** — stiffness discontinuity at the nail tip and its effect on local curvature")
md.append("4. **Strain and fatigue interpretation** — relating stresses to yield strain and fatigue endurance limit")
md.append("5. **Multi-objective comparison** — synthesizing all metrics to compare straight vs. curved nail designs")
md.append("")
md.append("**Key limitations:** All analyses remain within Euler-Bernoulli beam theory and simple superposition. No explicit contact mechanics, muscle forces, or 3D FEA are used. The model captures load-sharing and section-level stress/strain but not localized contact stresses, stress concentrations at screw holes, or anterior cortex impingement.")
md.append("")
md.append("**Parameter verification:** All key input parameters (E_b = 17 GPa, sigma_y,t = 108 MPa, R_f = 1100 mm, k_N = 2.4x BW, E_n = 110 GPa) were re-validated against peer-reviewed literature via scite.ai and remain consistent with the values reported in `literature_review_tables.md` [1]-[25]. No changes to nominal values were warranted.")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 2: Baseline Recap
# ════════════════════════════════════════════════
md.append("## 2. Baseline 2D Sagittal Model Recap")
md.append("")
md.append("The baseline model (detailed in `numerical_results.md`) considers three structural cases under axial hip contact load N = k_N * W transmitted through the bowed femur:")
md.append("")
md.append("| Parameter | Value | Units |")
md.append("|---|---|---|")
md.append(f"| Axial load N = k_N * W | {N_load:.0f} | N |")
md.append(f"| Bow eccentricity e = L_diaph^2 / (8 R_f) | {e_sag:.2f} | mm |")
md.append(f"| Sagittal bending moment M_sag = N * e | {M_sag:.0f} | N*mm |")
md.append(f"| Bone I_b | {I_b:.0f} | mm^4 |")
md.append(f"| Composite I (straight nail) | {I_comp_straight:.0f} | mm^4 |")
md.append(f"| Composite I (curved nail) | {I_comp_curved:.0f} | mm^4 |")
md.append(f"| NA shift y_bar (straight) | {y_bar:.2f} | mm |")
md.append("")
md.append("**Sagittal-only lateral cortex stress:**")
md.append("")
md.append("| Case | sigma_lat,sag (MPa) | FOS_sag |")
md.append("|---|---|---|")
md.append(f"| Bone only | {sigma_lat_sag_bone:.2f} | {sigma_y_t_conservative/sigma_lat_sag_bone:.2f} |")
md.append(f"| Straight nail | {sigma_lat_sag_straight:.2f} | {sigma_y_t_conservative/sigma_lat_sag_straight:.2f} |")
md.append(f"| Curved nail | {sigma_lat_sag_curved:.2f} | {sigma_y_t_conservative/sigma_lat_sag_curved:.2f} |")
md.append("")
md.append("The straight nail shows the lowest sagittal stress because the NA shift (y_bar > 0) reduces c_lat. However, this simplified model does not capture the anterior cortex contact forces caused by curvature mismatch.")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 3: Frontal-Plane Bending
# ════════════════════════════════════════════════
md.append("## 3. Frontal-Plane (Coronal) Bending and Superposition")
md.append("")
md.append("### 3.1 Rationale")
md.append("")
md.append("The hip joint contact force acts through the femoral head, which is medially offset from the femoral shaft axis by the **femoral offset** d_ML. This creates a frontal-plane bending moment at the subtrochanteric / mid-diaphyseal level that is typically *larger* than the sagittal bow-induced moment [8], [9].")
md.append("")
md.append("**Femoral offset (d_ML):**")
md.append("")
md.append("| Parameter | Nominal | Range | Units | Sources |")
md.append("|---|---|---|---|---|")
md.append(f"| d_ML (hip center to shaft axis) | {d_ML:.0f} | 35-65 | mm | Tatka et al. 2022 (mean 38 mm, cadaveric); Lechler et al. 2014 (rotation-corrected mean 57 mm); Biggi et al. 2020 |")
md.append("")
md.append("### 3.2 Frontal-Plane Bending Moment")
md.append("")
md.append("$$M_{\\text{front}} = N \\cdot d_{ML}$$")
md.append("")
md.append(f"M_front = {N_load:.0f} x {d_ML:.0f} = **{M_front:.0f} N*mm**")
md.append("")
md.append(f"Compare to sagittal moment: M_sag = {M_sag:.0f} N*mm")
md.append("")
md.append(f"**Ratio M_front / M_sag = {M_front/M_sag:.2f}** — the frontal-plane moment is {M_front/M_sag:.1f}x larger than the sagittal bow-induced moment.")
md.append("")
md.append("### 3.3 Frontal-Plane Section Properties")
md.append("")
md.append("For a circular cross-section, I is identical regardless of bending axis. In the frontal plane, the nail sits centrally within the medullary canal (y_n = 0 in the M-L direction) for **both** straight and curved nails. Therefore:")
md.append("")
md.append(f"- I_comp,front (both nailed cases) = I_b + n * I_n = {I_comp_front:.0f} mm^4")
md.append(f"- c_lat,front = r_o = {r_o:.1f} mm (lateral cortex is outermost in M-L)")
md.append("")
md.append("### 3.4 Frontal-Plane Stresses")
md.append("")
md.append("| Case | sigma_front (MPa) | I used (mm^4) |")
md.append("|---|---|---|")
md.append(f"| Bone only | {sigma_front_bone:.2f} | {I_b:.0f} (I_b) |")
md.append(f"| Straight nail | {sigma_front_straight:.2f} | {I_comp_front:.0f} (I_comp,front) |")
md.append(f"| Curved nail | {sigma_front_curved:.2f} | {I_comp_front:.0f} (I_comp,front) |")
md.append("")
md.append("**Key insight:** In the frontal plane, both nail types produce identical bending stress because the nail is centered (no mismatch). The straight nail's sagittal advantage (lower sigma_sag due to NA shift) does *not* carry over to the frontal plane.")
md.append("")
md.append("### 3.5 Combined Stress (Sagittal + Frontal)")
md.append("")
md.append("Both sagittal and frontal bending produce tension at the lateral cortex. Using scalar superposition (conservative upper bound):")
md.append("")
md.append("$$\\sigma_{\\text{lat,total}} = \\sigma_{\\text{lat,sag}} + \\sigma_{\\text{front}}$$")
md.append("")
md.append("| Case | sigma_sag (MPa) | sigma_front (MPa) | **sigma_total (MPa)** | **FOS_total** |")
md.append("|---|---|---|---|---|")
md.append(f"| Bone only | {sigma_lat_sag_bone:.2f} | {sigma_front_bone:.2f} | **{sigma_total_bone:.2f}** | **{FOS_total_bone:.2f}** |")
md.append(f"| Straight nail | {sigma_lat_sag_straight:.2f} | {sigma_front_straight:.2f} | **{sigma_total_straight:.2f}** | **{FOS_total_straight:.2f}** |")
md.append(f"| Curved nail | {sigma_lat_sag_curved:.2f} | {sigma_front_curved:.2f} | **{sigma_total_curved:.2f}** | **{FOS_total_curved:.2f}** |")
md.append("")
md.append(f"**Observations:**")
md.append(f"- Frontal-plane bending dominates: it contributes {sigma_front_bone:.1f} MPa (bone) vs {sigma_lat_sag_bone:.1f} MPa (sagittal) — **{sigma_front_bone/sigma_total_bone*100:.0f}%** of total stress for bone only.")
md.append(f"- The straight and curved nails now show **nearly identical** total stress ({sigma_total_straight:.2f} vs {sigma_total_curved:.2f} MPa), because the frontal component dominates and is the same for both.")
md.append(f"- The straight nail's sagittal advantage is diluted: it was {(sigma_lat_sag_bone - sigma_lat_sag_straight)/sigma_lat_sag_bone*100:.1f}% lower in sagittal-only, but only {(sigma_total_bone - sigma_total_straight)/sigma_total_bone*100:.1f}% lower in the combined stress.")
md.append(f"- **Bone only** (FOS = {FOS_total_bone:.2f}) now falls **below** FOS = 2.0, highlighting why a nail is biomechanically necessary. Both nailed cases maintain FOS > 1.5.")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 4: Compatibility Index
# ════════════════════════════════════════════════
md.append("## 4. Neutral-Axis Compatibility Index")
md.append("")
md.append("### 4.1 Definition")
md.append("")
md.append("The **compatibility index** C quantifies how eccentric the nail centroid is within the medullary canal, as a fraction of the bone radius:")
md.append("")
md.append("$$C = \\frac{|y_n|}{r_o}$$")
md.append("")
md.append("where y_n is the nail centroid offset from the bone centroid (in the sagittal plane) due to curvature mismatch.")
md.append("")
md.append("- C = 0: nail perfectly follows the bone curvature (ideal)")
md.append("- C > 0: nail deviates from the canal centerline, increasing anterior cortex contact risk")
md.append("")
md.append("### 4.2 Results")
md.append("")
md.append("| Scenario | Nail Type | y_n (mm) | C = |y_n|/r_o | sigma_total (MPa) | Interpretation |")
md.append("|---|---|---|---|---|---|")
md.append(f"| Nominal (R_f=1100) | Straight | {y_n_straight:.2f} | {C_straight:.3f} | {sigma_total_straight:.2f} | Moderate mismatch |")
md.append(f"| Nominal (R_f=1100) | Curved | 0.00 | {C_curved:.3f} | {sigma_total_curved:.2f} | Perfect match |")
md.append(f"| Asian female (R_f=880) | Straight | {y_n_straight_asian:.2f} | {C_straight_asian:.3f} | {sigma_total_straight_asian:.2f} | Larger mismatch |")
md.append(f"| Asian female (R_f=880) | Curved | 0.00 | {C_curved_asian:.3f} | {sigma_total_curved_asian:.2f} | Perfect match |")
md.append("")
md.append("### 4.3 Interpretation")
md.append("")
md.append(f"- For the nominal population, C_straight = {C_straight:.3f} — the nail centroid sits **{y_n_straight:.1f} mm** anterior to the bone centroid.")
md.append(f"- For Asian females with R_f = 880 mm, C_straight = {C_straight_asian:.3f} — the mismatch grows to **{y_n_straight_asian:.1f} mm**, nearly {C_straight_asian/C_straight:.1f}x worse.")
md.append(f"- A non-zero C means the straight nail presses against the anterior cortex, creating **localized contact stresses** not captured by beam theory.")
md.append(f"- The curved nail has C = 0 by design, eliminating this mismatch-driven cortical contact.")
md.append(f"- Even though the straight nail has marginally lower sigma_total in the beam model, **the compatibility index reveals the hidden risk**: anterior cortex impingement, which is the primary clinical mechanism of nail-related AFF [12], [15], [19], [20].")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 5: Two-Segment EI Model
# ════════════════════════════════════════════════
md.append("## 5. Tip Stiffness Discontinuity (Two-Segment EI Model)")
md.append("")
md.append("### 5.1 Concept")
md.append("")
md.append("An intramedullary nail creates two distinct flexural regions along the femoral shaft:")
md.append("")
md.append("- **Region 1 (nailed):** bone + nail composite, flexural rigidity EI_1 = E_b * I_b + E_n * I_n")
md.append("- **Region 2 (bone only):** distal to the nail tip, flexural rigidity EI_2 = E_b * I_b")
md.append("")
md.append("At the transition (nail tip), there is a **stiffness discontinuity**: the curvature must jump to maintain moment equilibrium across the interface.")
md.append("")
md.append("### 5.2 Stiffness Values")
md.append("")
md.append(f"| Region | EI (N*mm^2) | Description |")
md.append(f"|---|---|---|")
md.append(f"| Region 1 (nailed) | {EI_1:.3e} | E_b * I_b + E_n * I_n |")
md.append(f"| Region 2 (bone only) | {EI_2:.3e} | E_b * I_b |")
md.append(f"| **Stiffness ratio EI_1/EI_2** | **{stiffness_ratio:.2f}** | Nailed region is {stiffness_ratio:.1f}x stiffer |")
md.append("")
md.append("### 5.3 Curvature Jump at Nail Tip")
md.append("")
md.append("Under a representative bending moment M at the transition:")
md.append("")
md.append("$$\\kappa_1 = \\frac{M}{EI_1}, \\quad \\kappa_2 = \\frac{M}{EI_2}$$")
md.append("")
md.append("$$\\Delta\\kappa = \\kappa_2 - \\kappa_1 = M\\left(\\frac{1}{EI_2} - \\frac{1}{EI_1}\\right)$$")
md.append("")
md.append("### 5.4 Short vs. Long Nail Comparison")
md.append("")
md.append("A **short/mid-length nail** places the transition in a high-moment region (subtrochanteric). A **long, curved nail** pushes the transition distally where the bending moment is lower.")
md.append("")
md.append("| Scenario | M at tip (N*mm) | kappa_1 (1/mm) | kappa_2 (1/mm) | Delta_kappa (1/mm) | eps_lat,tip (%) |")
md.append("|---|---|---|---|---|---|")
md.append(f"| Short nail (tip in high-M zone) | {M_tip_short:.0f} | {kappa_1_short:.2e} | {kappa_2_short:.2e} | {delta_kappa_short:.2e} | {eps_tip_short*100:.4f} |")
md.append(f"| Long curved nail (tip in low-M zone) | {M_tip_long:.0f} | {kappa_1_long:.2e} | {kappa_2_long:.2e} | {delta_kappa_long:.2e} | {eps_tip_long*100:.4f} |")
md.append("")
md.append(f"**Key finding:** The long curved nail reduces the curvature jump by **{(1 - delta_kappa_long/delta_kappa_short)*100:.0f}%** and the distal-tip strain by the same proportion, simply by moving the transition to a region of lower bending moment.")
md.append("")
md.append("### 5.5 Clinical Significance")
md.append("")
md.append("- The curvature jump Delta_kappa creates a **stress riser** at the nail tip, which is a recognized site of peri-prosthetic fracture [15], [19].")
md.append(f"- The stiffness ratio of {stiffness_ratio:.1f}x means the bone-only region must bend {stiffness_ratio:.1f}x more per unit moment than the nailed region.")
md.append("- A **longer, bow-matched nail** mitigates this by:")
md.append("  - Moving the transition distally (lower M).")
md.append("  - Matching the bone curvature (no anterior contact stress along the nail length).")
md.append("  - Reducing the effective Delta_kappa at the tip.")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 6: Strain and Fatigue
# ════════════════════════════════════════════════
md.append("## 6. Strain and Fatigue Perspective")
md.append("")
md.append("### 6.1 Strain Calculation")
md.append("")
md.append("Lateral cortex strain from the combined (sag + frontal) stress:")
md.append("")
md.append("$$\\varepsilon_{\\text{lat}} = \\frac{\\sigma_{\\text{lat,total}}}{E_b}$$")
md.append("")
md.append(f"Yield strain (literature): epsilon_y = {eps_y*100:.2f}%")
md.append("")
md.append("### 6.2 Fatigue Endurance Limit")
md.append("")
md.append(f"For mid-diaphyseal femoral cortical bone, the fatigue endurance limit at ~10^6 cycles is approximately 40-60% of sigma_u,t [6], [7].")
md.append("")
md.append(f"Using a conservative 45% of sigma_u,t = {sigma_u_t:.0f} MPa:")
md.append("")
md.append(f"**sigma_endurance = {sigma_endurance_fraction:.0%} x {sigma_u_t:.0f} = {sigma_endurance:.1f} MPa**")
md.append("")
md.append("### 6.3 Results")
md.append("")
md.append("| Case | sigma_total (MPa) | epsilon_lat (%) | FOS_yield | FOS_fatigue | epsilon_lat / epsilon_y |")
md.append("|---|---|---|---|---|---|")
md.append(f"| Bone only | {sigma_total_bone:.2f} | {eps_total_bone*100:.4f} | {FOS_total_bone:.2f} | {FOS_fatigue_bone:.2f} | {eps_total_bone/eps_y:.3f} |")
md.append(f"| Straight nail | {sigma_total_straight:.2f} | {eps_total_straight*100:.4f} | {FOS_total_straight:.2f} | {FOS_fatigue_straight:.2f} | {eps_total_straight/eps_y:.3f} |")
md.append(f"| Curved nail | {sigma_total_curved:.2f} | {eps_total_curved*100:.4f} | {FOS_total_curved:.2f} | {FOS_fatigue_curved:.2f} | {eps_total_curved/eps_y:.3f} |")
md.append("")
md.append("### 6.4 Interpretation")
md.append("")
md.append(f"- All strains are well below the yield strain ({eps_y*100:.2f}%), with epsilon_lat / epsilon_y ratios of {eps_total_bone/eps_y:.1%} – {max(eps_total_straight, eps_total_curved)/eps_y:.1%}.")
md.append(f"- **Bone only** has FOS_fatigue = {FOS_fatigue_bone:.2f} (< 1.0), meaning the un-nailed femur is already at risk of fatigue failure under combined loading — consistent with AFF occurring in intact bone. Both nailed cases achieve FOS_fatigue > 1.0.")
md.append(f"- However, in AFF patients with **bisphosphonate-suppressed remodeling** and accumulated microdamage, the effective fatigue endurance limit may be substantially lower, potentially reducing these safety margins.")
md.append(f"- The key insight is that **even modest stress reductions translate into meaningful fatigue life extensions**, because the S-N curve for cortical bone follows an inverse power law: small decreases in stress amplitude produce disproportionately large increases in cycles to failure [6], [7].")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 7: Synthesis
# ════════════════════════════════════════════════
md.append("## 7. Synthesis and Design Implications")
md.append("")
md.append("### 7.1 Multi-Objective Scorecard")
md.append("")
md.append("| Metric | Straight Nail | Curved Nail | Winner | Notes |")
md.append("|---|---|---|---|---|")
md.append(f"| sigma_lat,sag (MPa) | {sigma_lat_sag_straight:.2f} | {sigma_lat_sag_curved:.2f} | Straight | NA shift reduces c_lat |")
md.append(f"| sigma_lat,total (sag+front, MPa) | {sigma_total_straight:.2f} | {sigma_total_curved:.2f} | {'Straight' if sigma_total_straight < sigma_total_curved else 'Curved' if sigma_total_curved < sigma_total_straight else 'Tied'} | Frontal plane equalizes |")
winner_compat = "Curved" if C_curved < C_straight else "Tied"
md.append(f"| Compatibility index C | {C_straight:.3f} | {C_curved:.3f} | {winner_compat} | C = 0 is ideal |")
md.append(f"| Tip curvature jump | Same (geometry-dependent) | Reduced (longer nail) | Curved | Lower M at distal tip |")
md.append(f"| FOS_fatigue | {FOS_fatigue_straight:.2f} | {FOS_fatigue_curved:.2f} | {'Straight' if FOS_fatigue_straight > FOS_fatigue_curved else 'Curved'} | Both > 1.0 |")
md.append(f"| Anterior cortex contact risk | High (C >> 0) | None (C = 0) | Curved | Primary clinical concern |")
md.append(f"| Asian female safety | C = {C_straight_asian:.3f} | C = 0.000 | Curved | Mismatch amplified |")
md.append("")
md.append("### 7.2 Key Takeaways")
md.append("")
md.append("1. **Frontal-plane bending dominates.** The coronal moment from hip offset is ~{:.1f}x the sagittal bow moment. Once frontal bending is included, the straight nail's beam-level advantage over the curved nail is marginal ({:.1f} vs {:.1f} MPa total).".format(M_front/M_sag, sigma_total_straight, sigma_total_curved))
md.append("")
md.append("2. **The compatibility index reveals the true risk.** The straight nail has C = {:.3f} (nominal) to {:.3f} (Asian female), meaning the nail centroid sits {:.1f}–{:.1f} mm off the canal centerline. This drives anterior cortex contact and localized stress concentrations that beam theory cannot capture.".format(C_straight, C_straight_asian, y_n_straight, y_n_straight_asian))
md.append("")
md.append("3. **Stiffness discontinuity at the nail tip** creates a curvature jump of {:.2e} 1/mm. A longer, curved nail pushes this transition to a lower-moment region, reducing tip strain by ~40%.".format(delta_kappa_short))
md.append("")
md.append("4. **Un-nailed bone fails the fatigue criterion** (FOS_fatigue = {:.2f} < 1.0) under combined loading, which is consistent with AFF occurring in intact femora. Both nailed cases bring FOS_fatigue above 1.0, but margins are thin — especially relevant for AFF patients with bisphosphonate-suppressed remodeling and reduced effective endurance limits.".format(FOS_fatigue_bone))
md.append("")
md.append("5. **Design recommendation:** A **long, patient-specific curved nail** matching the individual femoral ROC offers:")
md.append("   - C = 0 (no curvature mismatch, no anterior impingement)")
md.append("   - Comparable beam-level stress performance")
md.append("   - Reduced stiffness discontinuity at the tip")
md.append("   - Greatest benefit for high-risk patients (Asian females, excessive bow)")
md.append("")
md.append("### 7.3 What This Model Does and Does Not Capture")
md.append("")
md.append("| Captured (BMEN 383 level) | Not captured (beyond scope) |")
md.append("|---|---|")
md.append("| Composite beam bending (transformed section) | 3D FEA with contact |")
md.append("| Sagittal + frontal superposition | Muscle forces (abductors, IT band) |")
md.append("| Stiffness discontinuity (EI jump) | Stress concentrations at screw holes |")
md.append("| Compatibility index (curvature mismatch) | Anterior cortex contact pressure |")
md.append("| Strain and fatigue safety factors | Microdamage accumulation over time |")
md.append("| Monte Carlo uncertainty (see baseline) | Patient-specific geometry from CT |")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# Section 8: Asian Female Scenario (Extended)
# ════════════════════════════════════════════════
md.append("## 8. Clinical Scenario: Asian Female (Extended)")
md.append("")
md.append("Higher-risk patient: R_f = 880 mm, W = 550 N (55 kg), L_diaph = 370 mm.")
md.append("")
md.append("| Metric | Bone Only | Straight Nail | Curved Nail | Units |")
md.append("|---|---|---|---|---|")
md.append(f"| sigma_total (sag + front) | {sigma_total_bone_asian:.2f} | {sigma_total_straight_asian:.2f} | {sigma_total_curved_asian:.2f} | MPa |")
md.append(f"| FOS_total | {FOS_total_bone_asian:.2f} | {FOS_total_straight_asian:.2f} | {FOS_total_curved_asian:.2f} | -- |")
md.append(f"| Compatibility index C | -- | {C_straight_asian:.3f} | 0.000 | -- |")
md.append(f"| y_n (nail offset) | -- | {y_n_straight_asian:.2f} | 0.00 | mm |")
md.append("")
md.append(f"In the Asian female scenario, the curvature mismatch is amplified (C = {C_straight_asian:.3f} vs {C_straight:.3f} nominal), making the case for a bow-matched curved nail even stronger.")
md.append("")
md.append("---")
md.append("")

# ════════════════════════════════════════════════
# References note
# ════════════════════════════════════════════════
md.append("## References")
md.append("")
md.append("All references [1]–[25] are as listed in `literature_review_tables.md`. Additional sources for the frontal-plane lever arm (d_ML):")
md.append("")
md.append("- [26] Tatka, J., Delagrammaticas, D.E., Kemler, B.R. (2022). A new understanding of radiographic landmarks of the greater trochanter that indicate correct femoral rotation for measurement of femoral offset. *Arthroplasty*, 4(1). https://doi.org/10.1186/s42836-022-00121-y")
md.append("- [27] Lechler, P., Frink, M., Gulati, A. (2014). The influence of hip rotation on femoral offset in plain radiographs. *Acta Orthopaedica*, 85(4), 389-395. https://doi.org/10.3109/17453674.2014.931196")
md.append("- [28] Biggi, S., Banci, L., Tedino, R. (2020). Restoring global offset and lower limb length with a 3 offset option double-tapered stem. *BMC Musculoskelet Disord*, 21(1). https://doi.org/10.1186/s12891-020-03674-8")
md.append("- [29] Kanawati, A., Jang, B., McGee, R. (2014). The influence of entry point and radius of curvature on femoral intramedullary nail position in the distal femur. *Journal of Orthopaedics*, 11(2), 68-71. https://doi.org/10.1016/j.jor.2014.04.010")
md.append("- [30] Shetty, A., Shenoy, P., Swaminathan, T.R. (2019). Mismatch of long Gamma intramedullary nail with bow of the femur. *J Clin Orthop Trauma*, 10(2), 302-304. https://doi.org/10.1016/j.jcot.2017.12.006")
md.append("")

# Write
out_path = Path(__file__).parent / "extended_analysis_readme.md"
out_path.write_text("\n".join(md), encoding="utf-8")
print(f"Extended analysis written to {out_path}")
print(f"\nQuick summary:")
print(f"  M_front / M_sag = {M_front/M_sag:.2f}")
print(f"  sigma_total: bone={sigma_total_bone:.2f}, straight={sigma_total_straight:.2f}, curved={sigma_total_curved:.2f} MPa")
print(f"  FOS_total:   bone={FOS_total_bone:.2f}, straight={FOS_total_straight:.2f}, curved={FOS_total_curved:.2f}")
print(f"  Compatibility: C_straight={C_straight:.3f}, C_curved={C_curved:.3f}")
print(f"  Stiffness ratio EI_1/EI_2 = {stiffness_ratio:.2f}")
print(f"  FOS_fatigue: bone={FOS_fatigue_bone:.2f}, straight={FOS_fatigue_straight:.2f}, curved={FOS_fatigue_curved:.2f}")
