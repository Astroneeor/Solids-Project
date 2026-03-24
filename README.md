# AFF Curved Intramedullary Nail — Biomechanical Analysis

**BMEN 383 — Continuum / Solid Mechanics II, University of Calgary, Winter 2026**

## Overview

This repository contains the computational analysis supporting our design project on **atypical femoral fractures (AFF)**. We evaluate whether a **patient-specific, bow-matched curved intramedullary (IM) nail** reduces lateral cortex stress and fracture risk compared to conventional straight nails.

All analyses use Euler-Bernoulli composite beam theory with the transformed section method.

## Key Findings

| Metric | Bone Only | Straight Nail | Curved Nail |
|---|---|---|---|
| Combined lateral stress (MPa) | 67.7 | 55.1 | 57.0 |
| FOS (yield) | 1.48 | 1.82 | 1.75 |
| FOS (fatigue) | 0.88 | 1.09 | 1.05 |
| Compatibility index C | — | 0.146 | **0.000** |
| Anterior cortex contact risk | — | High | **None** |

The straight nail has a marginal beam-level stress advantage, but the curved nail eliminates curvature mismatch (C = 0), reduces tip stiffness discontinuity by ~40%, and removes anterior cortex impingement risk — the clinically dominant factors in AFF.

## Three Structural Cases

1. **Bone only** — intact bowed femur, no implant
2. **Straight nail** — conventional IM nail (R_n = 1500 mm vs R_f = 1100 mm femur)
3. **Curved nail** — bow-matched nail (R_n = R_f), eliminating curvature mismatch

## Repository Contents

| File | Description |
|---|---|
| `literature_review_tables.md` | Literature-derived parameter tables (A–E), symbolic equations, 25+ IEEE references |
| `model_parameters.json` | Machine-readable nominal values, ranges, and units for all parameters |
| `run_calculations.py` | Baseline 2D sagittal composite beam model with Monte Carlo uncertainty (50k samples) |
| `numerical_results.md` | Baseline results: 3-case stress comparison, MC statistics, Asian female scenario |
| `run_extended_analysis.py` | Extended analysis: frontal bending, compatibility index, EI model, fatigue |
| `extended_analysis_readme.md` | Full write-up of the five extended analyses with interpretation |
| `generate_figures.py` | Script to generate all four publication-quality figures |
| `fig1_bowed_femur_schematic.png` | Bowed femur schematic: straight vs curved nail geometry |
| `fig2_lateral_stress_bars.png` | Stacked stress bar chart (sagittal + frontal) with yield/fatigue thresholds |
| `fig3_compatibility_vs_stress.png` | Compatibility index vs total stress (nominal + Asian female scenarios) |
| `fig4_tip_EI_schematic.png` | Two-segment EI model with bending moment diagram |

## Nominal Parameters

- **Bone:** E_b = 17 GPa, sigma_y,t = 108 MPa (mid-diaphyseal femoral cortical bone)
- **Nail:** Ti-6Al-4V ELI (ASTM F136), E_n = 110 GPa
- **Geometry:** r_o = 13 mm, r_i = 7.5 mm, r_n = 5.5 mm
- **Loading:** N = 2.4 × 700 N = 1680 N (walking), d_ML = 48 mm (femoral offset)
- **Femoral ROC:** R_f = 1100 mm (nominal), 880 mm (Asian female)

## How to Run

```bash
pip install numpy matplotlib
python run_calculations.py           # generates numerical_results.md
python run_extended_analysis.py      # generates extended_analysis_readme.md
python generate_figures.py           # generates fig1–fig4 PNG files
```

## Acknowledgments

Computational modeling scripts and analysis were developed with assistance from Claude (Anthropic, 2025), a large language model. All equations, parameter selections, interpretations, and design decisions were verified independently by the authors.
