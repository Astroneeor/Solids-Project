# AFF Curved Intramedullary Nail — Solid Mechanics Design Project

**BMEN 383 — Continuum / Solid Mechanics II**

## Overview

This project evaluates whether a **patient-specific, bow-matched curved intramedullary (IM) nail** reduces lateral cortex stress and fracture risk in **atypical femoral fractures (AFF)** compared to conventional straight nails.

All analyses use Euler-Bernoulli composite beam theory (transformed section method) — no FEA required.

## Key Findings

| Metric | Straight Nail | Curved Nail |
|---|---|---|
| Combined stress (sag + frontal) | 55.1 MPa | 57.0 MPa |
| Compatibility index C | 0.146 | **0.000** |
| Anterior cortex contact risk | High | **None** |
| Tip stiffness discontinuity | Standard | **Reduced (~40%)** |
| Fatigue FOS | 1.09 | 1.05 |

The straight nail wins marginally on beam-level stress, but the curved nail wins on **curvature mismatch**, **tip strain**, and **anterior impingement risk** — the clinically dominant factors in AFF.

## Repository Contents

| File | Description |
|---|---|
| `literature_review_tables.md` | Literature-derived parameter tables (Tables A-E), modeling parameters, symbolic equations, and 25 IEEE references |
| `model_parameters.json` | Machine-readable nominal values, ranges, and units for all parameters |
| `run_calculations.py` | Baseline 2D sagittal model with Monte Carlo uncertainty (50k samples) |
| `numerical_results.md` | Baseline results: 3-case stress comparison, MC statistics, Asian female scenario |
| `run_extended_analysis.py` | Extended analysis: frontal bending, compatibility index, EI model, fatigue |
| `extended_analysis_readme.md` | Full write-up of the five extended analyses with tables and interpretation |

## How to Run

```bash
pip install numpy
python run_calculations.py           # generates numerical_results.md
python run_extended_analysis.py      # generates extended_analysis_readme.md
```

## Three Structural Cases

1. **Bone only** — intact femur, no implant
2. **Straight nail** — conventional IM nail (R_n = 1500 mm vs R_f = 1100 mm femur)
3. **Curved nail** — bow-matched nail (R_n = R_f), eliminating curvature mismatch

## Nominal Parameters

- Bone: E_b = 17 GPa, sigma_y,t = 108 MPa (mid-diaphyseal femoral cortical, longitudinal)
- Nail: Ti-6Al-4V ELI, E_n = 110 GPa, sigma_y,n = 860 MPa
- Geometry: r_o = 13 mm, r_i = 7.5 mm, r_n = 5.5 mm
- Loading: N = 2.4 x 700 N = 1680 N (walking)
- Femoral ROC: R_f = 1100 mm (nominal), 880 mm (Asian female)
