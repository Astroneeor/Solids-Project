"""
AFF Curved IM Nail — Numerical Calculations with Uncertainty Propagation
BMEN 383 – Continuum/Solid Mechanics II

Computes stresses for 3 cases (bone only, straight nail, curved nail)
using nominal values and propagates uncertainty via Monte Carlo sampling.
Outputs results to numerical_results.md
"""

import numpy as np
import json
from pathlib import Path

np.random.seed(42)
N_MC = 50_000  # Monte Carlo samples

# ──────────────────────────────────────────────
# 1. LOAD PARAMETERS
# ──────────────────────────────────────────────
with open(Path(__file__).parent / "model_parameters.json") as f:
    params = json.load(f)

# --- Nominal values ---
E_b  = 17.0e3    # MPa (= 17.0 GPa)
E_n  = 110.0e3   # MPa (= 110 GPa)
r_o  = 13.0      # mm
r_i  = 7.5       # mm
r_n  = 5.5       # mm
R_f  = 1100.0    # mm
R_n  = 1500.0    # mm (commercial straight nail)
L    = 250.0     # mm  (nail segment length, for mismatch y_n)
L_diaph = 400.0  # mm  (full diaphyseal arc length, GT to supracondylar, for bow eccentricity e)
k_N  = 2.4       # x BW
W    = 700.0     # N (70 kg)
sigma_y_t = 108.0  # MPa (tensile yield, bone)
sigma_y_t_conservative = 100.0  # MPa (for FOS calc)
FOS_required = 2.0

# ──────────────────────────────────────────────
# 2. DETERMINISTIC CALCULATIONS (NOMINAL)
# ──────────────────────────────────────────────

def compute_all(E_b, E_n, r_o, r_i, r_n, R_f, R_n, L, N, L_diaph=400.0):
    """Compute stresses for all 3 cases. Returns dict of results.

    Key distinction:
      - e (bow eccentricity) uses L_diaph: the offset of the mid-shaft
        from the hip-knee mechanical axis, due to the full femoral arc.
      - y_n (nail mismatch) uses L: the mismatch between the nail and
        bone curvature over the nail segment only.
    """
    # Modular ratio
    n = E_n / E_b

    # Section properties
    A_b = np.pi * (r_o**2 - r_i**2)
    I_b = (np.pi / 4) * (r_o**4 - r_i**4)
    A_n = np.pi * r_n**2
    I_n = (np.pi / 4) * r_n**4

    # Bow eccentricity: offset of mid-diaphysis from mechanical axis
    # Uses full diaphyseal arc length
    e = L_diaph**2 / (8 * R_f)
    M = N * e                    # bending moment at mid-span

    # Nail eccentricity (curvature mismatch over nail segment)
    y_n_straight = (L**2 / 8) * (1/R_f - 1/R_n)

    # ── Case 1: Bone only ──
    sigma_ax_bone = N / A_b
    sigma_bend_bone = M * r_o / I_b
    sigma_lat_bone = -sigma_ax_bone + sigma_bend_bone

    # ── Case 2: Straight nail (y_n != 0) ──
    y_n = y_n_straight
    y_bar = (n * A_n * y_n) / (A_b + n * A_n)
    I_comp = (I_b + A_b * y_bar**2
              + n * I_n + n * A_n * (y_n - y_bar)**2)
    c_lat_straight = r_o - y_bar

    sigma_ax_straight = N / (A_b + n * A_n)
    sigma_bend_straight = M * c_lat_straight / I_comp
    sigma_lat_straight = -sigma_ax_straight + sigma_bend_straight

    # Nail stress
    sigma_nail_straight = n * (-N / (A_b + n * A_n)
                               + M * (y_n - y_bar) / I_comp)

    # ── Case 3: Curved (bow-matched) nail (y_n = 0) ──
    I_comp_match = I_b + n * I_n
    sigma_ax_match = N / (A_b + n * A_n)
    sigma_bend_match = M * r_o / I_comp_match
    sigma_lat_match = -sigma_ax_match + sigma_bend_match

    # Nail stress (curved)
    sigma_nail_match = n * (-N / (A_b + n * A_n))  # bending term = 0 at centroid

    # ── Performance metrics ──
    pct_reduce_match_vs_bone = 100 * (sigma_lat_bone - sigma_lat_match) / sigma_lat_bone
    pct_reduce_match_vs_straight = 100 * (sigma_lat_straight - sigma_lat_match) / sigma_lat_straight

    # ── Strains ──
    eps_lat_bone = sigma_lat_bone / E_b  # unitless
    eps_lat_straight = sigma_lat_straight / E_b
    eps_lat_match = sigma_lat_match / E_b

    return {
        "n": n,
        "A_b": A_b, "I_b": I_b, "A_n": A_n, "I_n": I_n,
        "e": e, "M": M, "y_n": y_n,
        "y_bar": y_bar, "I_comp": I_comp, "I_comp_match": I_comp_match,
        # Case 1
        "sigma_ax_bone": sigma_ax_bone,
        "sigma_bend_bone": sigma_bend_bone,
        "sigma_lat_bone": sigma_lat_bone,
        "eps_lat_bone": eps_lat_bone,
        # Case 2
        "sigma_ax_straight": sigma_ax_straight,
        "sigma_bend_straight": sigma_bend_straight,
        "sigma_lat_straight": sigma_lat_straight,
        "sigma_nail_straight": sigma_nail_straight,
        "eps_lat_straight": eps_lat_straight,
        # Case 3
        "sigma_ax_match": sigma_ax_match,
        "sigma_bend_match": sigma_bend_match,
        "sigma_lat_match": sigma_lat_match,
        "sigma_nail_match": sigma_nail_match,
        "eps_lat_match": eps_lat_match,
        # Metrics
        "pct_reduce_match_vs_bone": pct_reduce_match_vs_bone,
        "pct_reduce_match_vs_straight": pct_reduce_match_vs_straight,
    }

N_load = k_N * W
nom = compute_all(E_b, E_n, r_o, r_i, r_n, R_f, R_n, L, N_load, L_diaph)

# FOS calculations
FOS_bone = sigma_y_t_conservative / nom["sigma_lat_bone"] if nom["sigma_lat_bone"] > 0 else float('inf')
FOS_straight = sigma_y_t_conservative / nom["sigma_lat_straight"] if nom["sigma_lat_straight"] > 0 else float('inf')
FOS_match = sigma_y_t_conservative / nom["sigma_lat_match"] if nom["sigma_lat_match"] > 0 else float('inf')

# ──────────────────────────────────────────────
# 3. MONTE CARLO UNCERTAINTY PROPAGATION
# ──────────────────────────────────────────────
# Define parameter distributions (truncated normals approximated via clipping)
def trunc_normal(mean, sd, lo, hi, n):
    samples = np.random.normal(mean, sd, n)
    return np.clip(samples, lo, hi)

# Parameter uncertainties (from literature ranges → approximate SD)
E_b_mc  = trunc_normal(17.0e3, 2.5e3, 12.0e3, 20.5e3, N_MC)   # MPa
r_o_mc  = trunc_normal(13.0, 0.75, 12.0, 15.0, N_MC)            # mm
r_i_mc  = trunc_normal(7.5, 0.6, 6.0, 8.5, N_MC)                # mm
r_n_mc  = np.full(N_MC, 5.5)                                     # fixed (nail design)
R_f_mc  = trunc_normal(1100.0, 200.0, 700.0, 1500.0, N_MC)      # mm
R_n_mc  = np.full(N_MC, 1500.0)                                  # fixed (commercial)
L_mc    = trunc_normal(250.0, 25.0, 200.0, 350.0, N_MC)          # mm (nail segment)
L_diaph_mc = trunc_normal(400.0, 30.0, 340.0, 460.0, N_MC)      # mm (full diaphysis)
k_N_mc  = trunc_normal(2.4, 0.3, 2.0, 3.5, N_MC)                # xBW
W_mc    = trunc_normal(700.0, 75.0, 500.0, 900.0, N_MC)          # N
E_n_mc  = np.full(N_MC, 110.0e3)                                 # fixed (implant spec)
sigma_y_t_mc = trunc_normal(100.0, 12.0, 70.0, 137.0, N_MC)     # MPa (conservative)

# Run MC
mc_lat_bone = np.zeros(N_MC)
mc_lat_straight = np.zeros(N_MC)
mc_lat_match = np.zeros(N_MC)
mc_fos_bone = np.zeros(N_MC)
mc_fos_straight = np.zeros(N_MC)
mc_fos_match = np.zeros(N_MC)

for i in range(N_MC):
    N_i = k_N_mc[i] * W_mc[i]
    res = compute_all(E_b_mc[i], E_n_mc[i], r_o_mc[i], r_i_mc[i],
                      r_n_mc[i], R_f_mc[i], R_n_mc[i], L_mc[i], N_i,
                      L_diaph_mc[i])
    mc_lat_bone[i] = res["sigma_lat_bone"]
    mc_lat_straight[i] = res["sigma_lat_straight"]
    mc_lat_match[i] = res["sigma_lat_match"]
    syt = sigma_y_t_mc[i]
    mc_fos_bone[i] = syt / res["sigma_lat_bone"] if res["sigma_lat_bone"] > 0 else 99.0
    mc_fos_straight[i] = syt / res["sigma_lat_straight"] if res["sigma_lat_straight"] > 0 else 99.0
    mc_fos_match[i] = syt / res["sigma_lat_match"] if res["sigma_lat_match"] > 0 else 99.0

def stats(arr):
    return {"mean": np.mean(arr), "std": np.std(arr),
            "p5": np.percentile(arr, 5), "p50": np.percentile(arr, 50),
            "p95": np.percentile(arr, 95), "min": np.min(arr), "max": np.max(arr)}

mc_bone_stats = stats(mc_lat_bone)
mc_straight_stats = stats(mc_lat_straight)
mc_match_stats = stats(mc_lat_match)
mc_fos_bone_stats = stats(mc_fos_bone)
mc_fos_straight_stats = stats(mc_fos_straight)
mc_fos_match_stats = stats(mc_fos_match)

# Probability of exceeding allowable
sigma_allow = 50.0  # MPa
prob_exceed_bone = np.mean(mc_lat_bone > sigma_allow) * 100
prob_exceed_straight = np.mean(mc_lat_straight > sigma_allow) * 100
prob_exceed_match = np.mean(mc_lat_match > sigma_allow) * 100

# ──────────────────────────────────────────────
# 4. ASIAN FEMALE SCENARIO (R_f = 880 mm)
# ──────────────────────────────────────────────
R_f_asian = 880.0
L_diaph_asian = 370.0  # shorter femur
N_load_light = 2.4 * 550  # lighter patient, 55 kg
nom_asian = compute_all(E_b, E_n, r_o, r_i, r_n, R_f_asian, R_n, L, N_load_light, L_diaph_asian)
FOS_bone_asian = sigma_y_t_conservative / nom_asian["sigma_lat_bone"] if nom_asian["sigma_lat_bone"] > 0 else float('inf')
FOS_straight_asian = sigma_y_t_conservative / nom_asian["sigma_lat_straight"] if nom_asian["sigma_lat_straight"] > 0 else float('inf')
FOS_match_asian = sigma_y_t_conservative / nom_asian["sigma_lat_match"] if nom_asian["sigma_lat_match"] > 0 else float('inf')

# ──────────────────────────────────────────────
# 5. GENERATE MARKDOWN OUTPUT
# ──────────────────────────────────────────────
md = []
md.append("# AFF Curved IM Nail — Numerical Results")
md.append("")
md.append("> Auto-generated by `run_calculations.py`")
md.append(f"> Monte Carlo samples: {N_MC:,}")
md.append("> All stresses in MPa, lengths in mm, forces in N")
md.append("")
md.append("---")
md.append("")

# Section 1: Input summary
md.append("## 1. Input Parameters (Nominal)")
md.append("")
md.append("| Parameter | Symbol | Value | Units |")
md.append("|---|---|---|---|")
md.append(f"| Bone elastic modulus | E_b | {E_b/1e3:.1f} | GPa |")
md.append(f"| Nail elastic modulus | E_n | {E_n/1e3:.1f} | GPa |")
md.append(f"| Modular ratio | n | {nom['n']:.2f} | — |")
md.append(f"| Outer radius | r_o | {r_o:.1f} | mm |")
md.append(f"| Inner radius | r_i | {r_i:.1f} | mm |")
md.append(f"| Nail radius | r_n | {r_n:.1f} | mm |")
md.append(f"| Femoral ROC | R_f | {R_f:.0f} | mm |")
md.append(f"| Nail ROC (commercial) | R_n | {R_n:.0f} | mm |")
md.append(f"| Nail segment length | L | {L:.0f} | mm |")
md.append(f"| Diaphyseal arc length | L_diaph | {L_diaph:.0f} | mm |")
md.append(f"| Hip contact force factor | k_N | {k_N:.1f} | ×BW |")
md.append(f"| Body weight | W | {W:.0f} | N |")
md.append(f"| Axial load | N | {N_load:.0f} | N |")
md.append(f"| Conservative tensile yield | σ_y,t | {sigma_y_t_conservative:.0f} | MPa |")
md.append(f"| Allowable lateral stress | σ_allow | {sigma_allow:.0f} | MPa (FOS = {FOS_required:.1f}) |")
md.append("")

# Section 2: Cross-section properties
md.append("## 2. Cross-Section Properties")
md.append("")
md.append("| Property | Value | Units |")
md.append("|---|---|---|")
md.append(f"| Bone area (A_b) | {nom['A_b']:.1f} | mm² |")
md.append(f"| Bone 2nd moment (I_b) | {nom['I_b']:.0f} | mm⁴ |")
md.append(f"| Nail area (A_n) | {nom['A_n']:.1f} | mm² |")
md.append(f"| Nail 2nd moment (I_n) | {nom['I_n']:.0f} | mm⁴ |")
md.append(f"| Bow eccentricity (e = s_f) | {nom['e']:.2f} | mm |")
md.append(f"| Bending moment (M = N·e) | {nom['M']:.0f} | N·mm |")
md.append(f"| Nail-bone mismatch (y_n) | {nom['y_n']:.2f} | mm |")
md.append(f"| NA shift (ȳ, straight nail) | {nom['y_bar']:.2f} | mm |")
md.append(f"| I_comp (straight nail) | {nom['I_comp']:.0f} | mm⁴ |")
md.append(f"| I_comp (curved nail) | {nom['I_comp_match']:.0f} | mm⁴ |")
md.append("")

# Section 3: Stress results
md.append("## 3. Lateral Cortex Stress Results (Nominal)")
md.append("")
md.append("| Quantity | Case 1: Bone Only | Case 2: Straight Nail | Case 3: Curved Nail | Units |")
md.append("|---|---|---|---|---|")
md.append(f"| Axial stress (σ_ax) | {nom['sigma_ax_bone']:.2f} | {nom['sigma_ax_straight']:.2f} | {nom['sigma_ax_match']:.2f} | MPa |")
md.append(f"| Bending stress (σ_bend,lat) | {nom['sigma_bend_bone']:.2f} | {nom['sigma_bend_straight']:.2f} | {nom['sigma_bend_match']:.2f} | MPa |")
md.append(f"| **Total lateral stress (σ_lat)** | **{nom['sigma_lat_bone']:.2f}** | **{nom['sigma_lat_straight']:.2f}** | **{nom['sigma_lat_match']:.2f}** | **MPa** |")
md.append(f"| Lateral strain (ε_lat) | {nom['eps_lat_bone']*100:.4f} | {nom['eps_lat_straight']*100:.4f} | {nom['eps_lat_match']*100:.4f} | % |")
md.append(f"| Nail stress (σ_nail) | — | {nom['sigma_nail_straight']:.2f} | {nom['sigma_nail_match']:.2f} | MPa |")
md.append(f"| **FOS (σ_y,t / σ_lat)** | **{FOS_bone:.2f}** | **{FOS_straight:.2f}** | **{FOS_match:.2f}** | — |")
md.append(f"| Meets FOS ≥ 2.0? | {'Yes' if FOS_bone >= 2.0 else '**NO**'} | {'Yes' if FOS_straight >= 2.0 else '**NO**'} | {'Yes' if FOS_match >= 2.0 else '**NO**'} | — |")
md.append("")

# Performance metrics
md.append("### Performance Comparison")
md.append("")
md.append(f"- Curved nail reduces lateral cortex stress by **{nom['pct_reduce_match_vs_bone']:.1f}%** vs bone only")
md.append(f"- Curved nail reduces lateral cortex stress by **{nom['pct_reduce_match_vs_straight']:.1f}%** vs straight nail")
md.append("")

# Section 4: MC results
md.append("## 4. Uncertainty Analysis (Monte Carlo, n = {:,})".format(N_MC))
md.append("")
md.append("Input parameters sampled from truncated normal distributions based on literature ranges.")
md.append("")
md.append("### Lateral Cortex Stress Distribution (σ_lat, MPa)")
md.append("")
md.append("| Statistic | Bone Only | Straight Nail | Curved Nail |")
md.append("|---|---|---|---|")
md.append(f"| Mean | {mc_bone_stats['mean']:.2f} | {mc_straight_stats['mean']:.2f} | {mc_match_stats['mean']:.2f} |")
md.append(f"| Std Dev | {mc_bone_stats['std']:.2f} | {mc_straight_stats['std']:.2f} | {mc_match_stats['std']:.2f} |")
md.append(f"| 5th percentile | {mc_bone_stats['p5']:.2f} | {mc_straight_stats['p5']:.2f} | {mc_match_stats['p5']:.2f} |")
md.append(f"| Median (50th) | {mc_bone_stats['p50']:.2f} | {mc_straight_stats['p50']:.2f} | {mc_match_stats['p50']:.2f} |")
md.append(f"| 95th percentile | {mc_bone_stats['p95']:.2f} | {mc_straight_stats['p95']:.2f} | {mc_match_stats['p95']:.2f} |")
md.append(f"| Min | {mc_bone_stats['min']:.2f} | {mc_straight_stats['min']:.2f} | {mc_match_stats['min']:.2f} |")
md.append(f"| Max | {mc_bone_stats['max']:.2f} | {mc_straight_stats['max']:.2f} | {mc_match_stats['max']:.2f} |")
md.append("")

md.append("### Factor of Safety Distribution")
md.append("")
md.append("| Statistic | Bone Only | Straight Nail | Curved Nail |")
md.append("|---|---|---|---|")
md.append(f"| Mean FOS | {mc_fos_bone_stats['mean']:.2f} | {mc_fos_straight_stats['mean']:.2f} | {mc_fos_match_stats['mean']:.2f} |")
md.append(f"| Std Dev | {mc_fos_bone_stats['std']:.2f} | {mc_fos_straight_stats['std']:.2f} | {mc_fos_match_stats['std']:.2f} |")
md.append(f"| 5th percentile | {mc_fos_bone_stats['p5']:.2f} | {mc_fos_straight_stats['p5']:.2f} | {mc_fos_match_stats['p5']:.2f} |")
md.append(f"| Median (50th) | {mc_fos_bone_stats['p50']:.2f} | {mc_fos_straight_stats['p50']:.2f} | {mc_fos_match_stats['p50']:.2f} |")
md.append(f"| 95th percentile | {mc_fos_bone_stats['p95']:.2f} | {mc_fos_straight_stats['p95']:.2f} | {mc_fos_match_stats['p95']:.2f} |")
md.append("")

md.append("### Probability of Exceeding Allowable Stress (σ_lat > 50 MPa)")
md.append("")
md.append("| Case | P(σ_lat > 50 MPa) |")
md.append("|---|---|")
md.append(f"| Bone only | {prob_exceed_bone:.1f}% |")
md.append(f"| Straight nail | {prob_exceed_straight:.1f}% |")
md.append(f"| Curved nail | {prob_exceed_match:.1f}% |")
md.append("")

# Section 5: Asian female scenario
md.append("## 5. Clinical Scenario: Asian Female (R_f = 880 mm, W = 550 N)")
md.append("")
md.append("This scenario represents a higher-risk patient: smaller, more bowed femur.")
md.append("")
md.append(f"- R_f = {R_f_asian:.0f} mm, W = 550 N (55 kg), k_N = 2.4, N = {N_load_light:.0f} N")
md.append(f"- Bow eccentricity: e = {nom_asian['e']:.2f} mm")
md.append(f"- Bending moment: M = {nom_asian['M']:.0f} N·mm")
md.append(f"- Nail mismatch (y_n): {nom_asian['y_n']:.2f} mm")
md.append("")
md.append("| Quantity | Bone Only | Straight Nail | Curved Nail | Units |")
md.append("|---|---|---|---|---|")
md.append(f"| σ_lat | {nom_asian['sigma_lat_bone']:.2f} | {nom_asian['sigma_lat_straight']:.2f} | {nom_asian['sigma_lat_match']:.2f} | MPa |")
md.append(f"| FOS | {FOS_bone_asian:.2f} | {FOS_straight_asian:.2f} | {FOS_match_asian:.2f} | — |")
md.append(f"| Meets FOS ≥ 2.0? | {'Yes' if FOS_bone_asian >= 2.0 else '**NO**'} | {'Yes' if FOS_straight_asian >= 2.0 else '**NO**'} | {'Yes' if FOS_match_asian >= 2.0 else '**NO**'} | — |")
md.append(f"| Curved vs bone reduction | — | — | {nom_asian['pct_reduce_match_vs_bone']:.1f}% | — |")
md.append(f"| Curved vs straight reduction | — | — | {nom_asian['pct_reduce_match_vs_straight']:.1f}% | — |")
md.append("")

# Section 6: Key takeaways
md.append("## 6. Key Takeaways")
md.append("")
md.append("1. **Bone only** has the highest lateral cortex tensile stress — bow-induced bending dominates over axial compression.")
md.append(f"2. Both nailed cases reduce the axial compression in the bone (from {nom['sigma_ax_bone']:.1f} to {nom['sigma_ax_straight']:.1f} MPa) by sharing load with the stiffer nail.")
md.append(f"3. The **straight nail** shifts the composite NA by ȳ = {nom['y_bar']:.2f} mm toward the tension side, which *reduces* c_lat and thus lowers the beam-level bending stress at the lateral cortex. This gives the straight nail the lowest σ_lat in this simplified model.")
md.append(f"4. The **curved nail** keeps the NA centered (ȳ = 0) and adds pure bending stiffness (I_comp = {nom['I_comp_match']:.0f} vs I_b = {nom['I_b']:.0f} mm⁴), reducing σ_lat by **{nom['pct_reduce_match_vs_bone']:.1f}%** relative to bone only.")
md.append(f"5. All cases have comfortable FOS: bone = {FOS_bone:.2f}, straight = {FOS_straight:.2f}, curved = {FOS_match:.2f}.")
md.append(f"6. Monte Carlo 95th-percentile stresses: bone = {mc_bone_stats['p95']:.1f}, straight = {mc_straight_stats['p95']:.1f}, curved = {mc_match_stats['p95']:.1f} MPa — all well below σ_allow = 50 MPa for walking loads.")
md.append("")
md.append("## 7. Important Model Limitations")
md.append("")
md.append("This is a **simplified 2D composite-beam model** capturing only bow-induced eccentric compression. It does **not** capture:")
md.append("")
md.append("1. **Anterior cortex contact/impingement forces**: a straight nail in a curved bone creates point contact at the anterior cortex, which is the primary clinical concern with nail-bone mismatch [12], [15], [19], [20]. These localized stresses can exceed cortical bone strength and cause perforation.")
md.append("2. **Coronal-plane (medial-lateral) bending**: the hip joint moment arm (~50–60 mm medial offset) produces the dominant bending moment at the subtrochanteric level, causing much higher lateral cortex tensions than the sagittal bow alone.")
md.append("3. **Muscle forces and 3D loading**: abductor muscles, IT band, and other soft tissues significantly alter the stress state.")
md.append("4. **Stress concentrations**: at screw holes, nail tip, and nail-bone contact points.")
md.append("5. **Fatigue and microdamage accumulation**: AFF is a stress fracture that develops over millions of gait cycles, not a single overload event.")
md.append("")
md.append("**The curved nail's primary clinical advantage** is in eliminating the **anterior cortex perforation risk** and distributing contact forces along the nail length — benefits that this beam-level model does not quantify. A full 3D FEA with contact modeling would be needed to capture these effects.")
md.append("")

# Write
out_path = Path(__file__).parent / "numerical_results.md"
out_path.write_text("\n".join(md), encoding="utf-8")
print(f"Results written to {out_path}")
print(f"\nQuick summary:")
print(f"  sigma_lat (bone only):    {nom['sigma_lat_bone']:.2f} MPa  (FOS = {FOS_bone:.2f})")
print(f"  sigma_lat (straight nail): {nom['sigma_lat_straight']:.2f} MPa  (FOS = {FOS_straight:.2f})")
print(f"  sigma_lat (curved nail):   {nom['sigma_lat_match']:.2f} MPa  (FOS = {FOS_match:.2f})")
print(f"  Curved vs bone:  -{nom['pct_reduce_match_vs_bone']:.1f}%")
print(f"  Curved vs straight: -{nom['pct_reduce_match_vs_straight']:.1f}%")
print(f"  P(exceed 50 MPa): bone {prob_exceed_bone:.1f}%, straight {prob_exceed_straight:.1f}%, curved {prob_exceed_match:.1f}%")
