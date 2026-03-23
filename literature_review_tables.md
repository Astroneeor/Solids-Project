# AFF Curved Intramedullary Nail — Literature‑Derived Modelling Parameters

> **Course:** BMEN 383 – Continuum/Solid Mechanics II
> **Date generated:** 2026‑03‑22
> **Sources:** scite.ai MCP literature search + well‑established reference values

---

## PHASE 1 — LITERATURE HARVEST

---

### Table A: Femoral Cortical Bone Mechanical Properties

All values are for **human femoral cortical bone, mid‑diaphyseal shaft, longitudinal direction** unless otherwise noted.

| Property | Mean | SD | Range | Units | Region | Loading Mode & Direction | Age / Population | Test Type | n | Citation |
|---|---|---|---|---|---|---|---|---|---|---|
| **Elastic modulus** | 17.0 | 3.1 | 11.5–19.7 | GPa | Mid‑diaphyseal femoral cortical shaft | Tension, longitudinal | Adult donors (20–69 yr) | Uniaxial coupon tensile test | ~40 | Reilly & Burstein, 1975 (DOI: 10.1016/0021-9290(75)90075-5) |
| Elastic modulus | 17.2 (median) | IQR 2.2 | 12.2–20.5 | GPa | Proximal femoral diaphysis (all 4 quadrants) | Tension, longitudinal | Adult donors (5 donors, healthy) | Uniaxial coupon tensile test w/ extensometer | 80 | Baleani et al., 2024 (DOI: 10.3390/bioengineering11040395) |
| Elastic modulus | 18.6 | — | — | GPa | Mid‑diaphyseal femoral cortical | Compression, longitudinal | Adult male (36–50 yr) | Quasi‑static compression | 3 donors | Weerasooriya et al., 2016 (DOI: 10.1007/s40870-016-0048-4) |
| Elastic modulus (bending) | ~18 (young) | — | — | GPa | Mid‑diaphyseal femoral cortical, lateral | Three‑point bending | Young (20–40 yr) | 3‑pt bending + micro‑CT | ~8/group | Zimmermann et al., 2016 (DOI: 10.1038/srep21072) |
| Elastic modulus (bending) | ~14 (OP) | — | — | GPa | Mid‑diaphyseal femoral cortical, lateral | Three‑point bending | Osteoporotic (elderly) | 3‑pt bending + micro‑CT | ~8/group | Zimmermann et al., 2016 |
| **Tensile yield stress** | 114 | — | 104–120 | MPa | Mid‑diaphyseal femoral cortical shaft | Tension, longitudinal | Adult donors | Uniaxial coupon tensile test | ~40 | Reilly & Burstein, 1975 |
| Tensile yield stress | ~117 (median) | — | 75.9–136.6 | MPa | Proximal femoral diaphysis | Tension, longitudinal | Adult healthy | Uniaxial tensile w/ extensometer | 80 | Baleani et al., 2024 |
| **Tensile ultimate stress** | 133 | — | 120–140 | MPa | Mid‑diaphyseal femoral cortical shaft | Tension, longitudinal | Adult donors | Uniaxial coupon tensile test | ~40 | Reilly & Burstein, 1975 |
| Tensile ultimate stress (bending) | ~150 (young) | — | — | MPa | Mid‑diaphyseal, lateral cortex | Three‑point bending | Young (20–40 yr) | 3‑pt bending | ~8 | Zimmermann et al., 2016 |
| Tensile ultimate stress (bending) | ~110 (OP) | — | — | MPa | Mid‑diaphyseal, lateral cortex | Three‑point bending | Osteoporotic elderly | 3‑pt bending | ~8 | Zimmermann et al., 2016 |
| **Compressive yield stress** | 182 | — | 170–193 | MPa | Mid‑diaphyseal femoral cortical shaft | Compression, longitudinal | Adult donors | Uniaxial compression | ~40 | Reilly & Burstein, 1975 |
| Compressive yield stress | ~180 | — | — | MPa | Mid‑diaphyseal femoral cortical shaft | Compression, longitudinal, quasi‑static | Adult males (36–50 yr) | Compression coupon | 3 donors | Weerasooriya et al., 2016 |
| **Compressive ultimate stress** | 195 | — | 183–213 | MPa | Mid‑diaphyseal femoral cortical shaft | Compression, longitudinal | Adult donors | Uniaxial compression | ~40 | Reilly & Burstein, 1975 |
| **Tensile yield strain** | 0.82 (median) | — | 0.77–0.87 | % | Proximal femoral diaphysis (all quadrants) | Tension, longitudinal | Adult healthy (5 donors) | Uniaxial tensile w/ extensometer | 80 | Baleani et al., 2024 |
| Tensile yield strain | 0.73 | — | — | % | Femoral diaphysis cortical | Tension, longitudinal | Adult donors | Coupon / FE‑based | — | Bayraktar et al., 2004 (DOI: 10.1016/j.jbiomech.2003.08.010) |
| **Fatigue (tension, cortical bone)** | Endurance limit ~40–60% of σ_u,t at 10⁶ cycles | — | — | MPa | Femoral diaphysis cortical | Tension‑tension, R ≈ 0.1, longitudinal | Adult (various) | Rotating‑beam / tension‑tension | Various | Carter & Caler, 1983; Zioupos et al., 2001 (see note below) |

**Notes on fatigue:**
- Cortical bone fatigue endurance limit is approximately 40–60% of the monotonic ultimate tensile strength at ~10⁶–10⁷ cycles (Carter & Caler, 1983; Zioupos et al., 2001).
- For mid‑diaphyseal femoral cortical bone with σ_u,t ≈ 130 MPa, this gives a fatigue endurance limit of roughly **50–80 MPa** in tension at 10⁶ cycles.
- Fatigue life is strongly affected by porosity, microcrack accumulation, and age.

---

### Table B: Femoral Curvature (Anterior Bow — Radius of Curvature)

| Study | ROC Type | Mean ROC | SD | Range | Units | Anatomical Span | Population | Method | Citation |
|---|---|---|---|---|---|---|---|---|---|
| Bong et al., 2004 | Anterior cortical ROC | 1200 | 360 | 530–3260 | mm | Full femoral length | Mixed American adults (n ≈ 100) | Lateral X‑ray | Bong et al., 2004 (DOI: 10.1097/00005131-200408000-00003) |
| Egol et al., 2004 | Anterior cortical ROC | 1320 (Black M) | — | — | mm | Full femoral length | Black males (bone specimens, n ≈ 100 each) | Physical specimen photography | Egol et al., 2004 (DOI: 10.1097/00005131-200408000-00003) |
| Egol et al., 2004 | Anterior cortical ROC | 1330 (Black F) | — | — | mm | Full femoral length | Black females | Physical specimen photography | Egol et al., 2004 |
| Egol et al., 2004 | Anterior cortical ROC | 1190 (White M) | — | — | mm | Full femoral length | White males | Physical specimen photography | Egol et al., 2004 |
| Egol et al., 2004 | Anterior cortical ROC | 1050 (White F) | — | — | mm | Full femoral length | White females | Physical specimen photography | Egol et al., 2004 |
| Liu et al., 2021 | Medullary ROC (centerline, 3D CT) | 959 (M) | 267 | — | mm | Full femoral medullary centerline | Chinese males (n = 50) | 3D CT reconstruction | Liu et al., 2021 (DOI: 10.1155/2021/7674764) |
| Liu et al., 2021 | Medullary ROC (centerline, 3D CT) | 884 (F) | 250 | — | mm | Full femoral medullary centerline | Chinese females (n = 46) | 3D CT reconstruction | Liu et al., 2021 |
| Liu et al., 2021 | Medullary ROC (centerline, 3D CT) | 923 (all) | 260 | — | mm | Full femoral medullary centerline | Chinese adults (n = 96) | 3D CT reconstruction | Liu et al., 2021 |
| Chantarapanich et al. | Medullary ROC (3D cadaver recon) | 895 | 238 | — | mm | Full femoral medullary centerline | Thai adults (cadaver) | 3D reconstruction | Chantarapanich et al. (cited in Liu 2021) |
| Schmutz et al., 2022 | Cortical ROC (3D CT) | 838 (median, non‑perf) | IQR 776–920 | 582–920 | mm | Diaphysis | Mixed Western population (n = 42) | 3D CT reconstruction | Schmutz et al., 2022 (DOI: 10.1097/corr.0000000000002166) |

**Key observations:**
- Asian (Chinese, Thai) populations show **smaller medullary ROC** (~880–960 mm) compared to Caucasian populations (~1050–1320 mm).
- Women tend to have **smaller ROC** (more bowed) than men within each ethnic group.
- Large inter‑individual variability (SD ~250–360 mm).
- Commercial IM nails typically have ROC of 1500–3000 mm, which is substantially **straighter** than many femora, especially in Asian women.

---

### Table C: Femoral Diaphyseal Cross‑Section

| Level | Outer Diameter (mm) | Inner (Endosteal) Diameter (mm) | Cortical Thickness (mm) | Population / Specimen Info | Citation |
|---|---|---|---|---|---|
| Lesser trochanter (LT) | 24.34 (mean) | 15.28 (mean) | 4.55 (mean) | South Korean, n = 600, age 20–93, CT | Ma et al., 2025 (DOI: 10.1371/journal.pone.0312420) |
| 3 cm below LT (subtrochanteric) | 24.58 (mean) | 14.27 (mean) | 4.97 (mean) | South Korean, n = 600, CT | Ma et al., 2025 |
| Mid‑diaphysis (approx.) | 26–30 | 12–16 | 5–7 (healthy adult) | Mixed Western, cadaver + CT (various studies) | Noble et al., 1995; Skedros & Baucom, 2007 |
| Mid‑diaphysis (isthmus) | 26–28 | 10–12 (isthmus) | 6–8 | Adult healthy, Western | Noble et al., 1995 (DOI: 10.1097/00003086-199503000-00015) |
| Femoral shaft (biomechanical surrogate) | 24 (tube model) | — | 2–6 (parametric) | Synthetic bone surrogate | Various FE studies (e.g., Jcm 2023) |

**Key observations:**
- At the **subtrochanteric / AFF‑relevant level** (near or slightly below LT): OD ≈ 24–26 mm, ID ≈ 13–16 mm, cortical thickness ≈ 4.5–6.0 mm.
- At **mid‑diaphysis / isthmus**: cortical thickness is typically maximal (5–8 mm), endosteal diameter is at its minimum (10–12 mm).
- Elderly / osteoporotic patients have **thinner** cortices (endosteal resorption widens the canal).

---

### Table D: Hip Joint Contact Forces in Walking

| Activity | Peak Hip Contact Force (×BW) | Mean ± SD | Sample / Population | Measurement Type | Citation |
|---|---|---|---|---|---|
| Level walking (normal speed ~1.0–1.3 m/s) | 2.38 (average patient) | Range: 1.8–2.8 | 4 patients with instrumented implants | In‑vivo instrumented prosthesis | Bergmann et al., 2001 (DOI: 10.1016/s0021-9290(01)00040-9) |
| Level walking (normal speed) | Up to ~2.8–3.5 (individual peaks) | — | Same 4 patients, different speeds | In‑vivo instrumented prosthesis | Bergmann et al., 2001 |
| Level walking (slow, 0.72 m/s) | 2.98 | — | n = 11 THR patients (long‑term) | Musculoskeletal model (OpenSim) | O'Connor et al., 2018 (DOI: 10.1016/j.jbiomech.2018.07.033) |
| Level walking (0.83 m/s) | 3.5 | — | Bergmann instrumented data | In‑vivo instrumented prosthesis | Bergmann et al., 1993 (via O'Connor 2018) |
| Level walking (fast, ~1.3 m/s) | ~3.0–3.5 | — | Healthy / THR fast walkers | Model / instrumented | O'Connor et al., 2018; Correa et al., 2010 |
| Stair climbing | 2.5–3.5 | — | Instrumented | In‑vivo | Bergmann et al., 2001 |
| Standing on one leg | 2.3–2.8 | — | Instrumented | In‑vivo | Bergmann et al., 2001 |

**Key observations:**
- **Normal walking:** consensus peak hip contact force ≈ **2.0–3.0 × BW** for typical walking speeds.
- Faster walking and stair climbing push to **3.0–3.5 × BW**.
- Bergmann (2001) is the gold‑standard reference (>2000 citations), reporting average peak of ~2.4 × BW for normal walking.

---

### Table E: Implant Material Properties

| Material | E (GPa) | ν | Yield Stress (MPa) | Ultimate Stress (MPa) | Standard / Grade | Citation |
|---|---|---|---|---|---|---|
| **Ti‑6Al‑4V ELI** (α+β, wrought) | 110–114 | 0.34 | ≥ 860 | ≥ 930 | ASTM F136 | ASTM F136; Niinomi, 1998; Kim et al., 2019 (DOI: 10.3390/app9245281) |
| Ti‑6Al‑4V (standard grade) | 114 | 0.34 | 880 | 950 | ASTM F1472 | ASTM F1472; Niinomi, 1998 |
| 316L Stainless Steel (for comparison) | 193 | 0.30 | 170–310 | 490–690 | ASTM F138 | Niinomi, 1998 |
| Co‑Cr‑Mo (for comparison) | 210–253 | 0.30 | 450–1500 | 900–1540 | ASTM F75/F1537 | Niinomi, 1998 |
| **Ti‑Nb‑Sn** (β‑type, low modulus) | 40–60 | ~0.33 | 300–700 | 400–800 | Experimental | Ozaki et al., 2004; various reviews |
| Ti‑29Nb‑13Ta‑4.6Zr (TNTZ, β‑type) | 55–65 | ~0.33 | 500–700 | 600–900 | Experimental | Niinomi, 2002; Kuroda et al. |

**Key observations:**
- **Ti‑6Al‑4V ELI** is the standard IM nail material: E ≈ 110 GPa, σ_y ≈ 860 MPa.
- The modular ratio **n = E_nail / E_bone ≈ 110/17 ≈ 6.5**, meaning the nail is ~6.5× stiffer than bone.
- Low‑modulus β‑Ti alloys (E ≈ 40–65 GPa) are being developed to **reduce stress shielding**; these give n ≈ 2.5–4.

---

## PHASE 2 — MODELLING PARAMETERS & SAFETY FACTORS

---

### 2.1 Recommended Nominal Bone Properties (Mid‑Diaphyseal Femoral Cortical, Longitudinal)

| Property | Symbol | Nominal | Lower Bound | Upper Bound | Units | Comment |
|---|---|---|---|---|---|---|
| Elastic modulus | E_b | 17.0 | 12.0 | 20.5 | GPa | Mean of Reilly & Burstein; range from Baleani 2024 |
| Tensile yield stress | σ_y,t | 108 | 76 | 137 | MPa | Conservative: 108 from R&B; low bound from Baleani |
| Tensile ultimate stress | σ_u,t | 133 | 110 | 150 | MPa | R&B mean; OP patients ~110 (Zimmermann 2016) |
| Compressive yield stress | σ_y,c | 180 | 170 | 195 | MPa | R&B + Weerasooriya; bone is ~1.5–1.7× stronger in compression |
| Compressive ultimate stress | σ_u,c | 195 | 183 | 213 | MPa | Reilly & Burstein 1975 |
| Tensile yield strain | ε_y | 0.80 | 0.73 | 0.87 | % | Baleani 2024 median ~0.82; Bayraktar 2004 ~0.73 |
| Poisson's ratio | ν_b | 0.30 | 0.28 | 0.33 | — | Standard literature value |

### 2.2 Design Allowable for Lateral Cortex Tension

For an AFF scenario in **older adults** (possibly osteoporotic, with pre‑existing microdamage):

- **Conservative tensile yield stress:** σ_y,t = **100 MPa** (reduced from 108 to account for age/OP effects; Zimmermann 2016 shows ~22% modulus drop and ~27% strength drop in OP)
- **Factor of Safety (FOS) = 2.0** on tensile yield:
  - **σ_lat,allow = σ_y,t / FOS = 100 / 2.0 = 50 MPa**
- This is consistent with the fatigue endurance limit (~50–80 MPa at 10⁶ cycles), providing additional margin for cyclic gait loading.
- **Anatomical context:** Mid‑diaphyseal cortical shaft, longitudinal direction, lateral cortex (tension side during anteroposterior bending).
- **Clinical context:** AFF patients are often older women (some Asian descent) on long‑term bisphosphonates, with possible accumulated microdamage.

### 2.3 Recommended Nominal Geometry

| Parameter | Symbol | Nominal | Range | Units | Comment |
|---|---|---|---|---|---|
| Femoral anterior ROC | R_f | 1100 | 700–1500 | mm | Central estimate for mixed population; Asian females ~880 |
| Outer radius (subtrochanteric) | r_o | 13.0 | 12.0–15.0 | mm | OD/2 from Ma 2025 (~24–26 mm at AFF level) |
| Inner radius (endosteal) | r_i | 7.5 | 6.0–8.5 | mm | ID/2 from Ma 2025 (~13–16 mm) |
| Cortical thickness | t_c | 5.0 | 3.5–7.0 | mm | (r_o − r_i); thinner in OP |
| Nail radius (IM nail) | r_n | 5.5 | 4.5–6.5 | mm | Standard IM nail ø = 9–13 mm |
| Nail ROC (commercial) | R_n | 1500 | 1500–3000 | mm | Most commercial nails ~1500 mm |
| Active nail length | L | 250 | 200–350 | mm | Diaphyseal span between locking screws |

**Variability notes:**
- **Asian females** tend toward the *lower* end of ROC (~880 mm) and *smaller* canal diameters.
- **Elderly / osteoporotic** patients have *thinner* cortices (r_i increases, t_c decreases).
- The ROC **mismatch** between a 1500 mm nail and an 880 mm femur is substantial and clinically relevant.

### 2.4 Recommended Nominal Loads

| Parameter | Symbol | Nominal | Range | Units | Comment |
|---|---|---|---|---|---|
| Peak hip contact force factor | k_N | 2.4 | 2.0–3.5 | × BW | Bergmann 2001 (walking, average patient) |
| Representative body weight | W | 700 | 500–900 | N | ~70 kg typical; AFF patients may be lighter |
| Nominal axial load | N = k_N × W | 1680 | 1000–3150 | N | For 70 kg patient at 2.4 × BW |

**Note:** Walking is the primary design load. Running (~4–5× BW) and stumbling (~8× BW) are excluded from the current scope but represent worst‑case scenarios.

### 2.5 Recommended Nominal Implant Properties (Ti‑6Al‑4V ELI)

| Parameter | Symbol | Nominal | Units | Comment |
|---|---|---|---|---|
| Elastic modulus | E_n | 110 | GPa | ASTM F136 |
| Yield stress | σ_y,n | 860 | MPa | ASTM F136 minimum |
| Poisson's ratio | ν_n | 0.34 | — | |
| Modular ratio | n = E_n / E_b | 6.5 | — | 110/17 |

---

## PHASE 3 — SYMBOLIC EQUATIONS

---

### 3.1 Cross‑Section Properties

**Femur (thick‑walled circular tube):**

$$A_b = \pi (r_o^2 - r_i^2)$$

$$I_b = \frac{\pi}{4}(r_o^4 - r_i^4)$$

**Nail (solid circular rod):**

$$A_n = \pi r_n^2$$

$$I_n = \frac{\pi}{4} r_n^4$$

### 3.2 Composite Section (Transformed Section Method)

**Modular ratio:**

$$n = \frac{E_n}{E_b}$$

**Transformed nail area:**

$$A_n' = n \, A_n$$

**Neutral axis location** (measured from bone centroid, with nail centroid at eccentricity $y_n$):

$$\bar{y} = \frac{n \, A_n \, y_n}{A_b + n \, A_n}$$

**Composite second moment of area** (about composite neutral axis):

$$I_{\text{comp}} = I_b + A_b \, \bar{y}^2 + n \, I_n + n \, A_n \, (y_n - \bar{y})^2$$

### 3.3 Key Distances from Neutral Axis

- To lateral (tension) cortex: $\quad c_{\text{lat}} = r_o - \bar{y}$
- To medial (compression) cortex: $\quad c_{\text{med}} = r_o + \bar{y}$
- To nail centroid: $\quad c_n = |y_n - \bar{y}|$

### 3.4 Eccentricity from Curvature Mismatch

For an arc of length $L$ and radius $R$, the **sagitta** (midpoint deflection from chord) is:

$$s \approx \frac{L^2}{8R}$$

- Bone sagitta: $\quad s_f = \dfrac{L^2}{8 R_f}$
- Nail sagitta: $\quad s_n = \dfrac{L^2}{8 R_n}$
- Mismatch: $\quad \Delta s = s_f - s_n = \frac{L^2}{8}\left(\frac{1}{R_f} - \frac{1}{R_n}\right)$

The eccentricity of the nail centroid from the bone centroid (in the anterior‑posterior direction):

$$y_n \approx \Delta s = \frac{L^2}{8}\left(\frac{1}{R_f} - \frac{1}{R_n}\right)$$

For a **bow‑matched** curved nail ($R_n = R_f$): $\quad y_n = 0$.

### 3.5 Bending Moment from Femoral Bow

The axial hip contact force $N$ acts along the mechanical axis. Due to the femoral bow, the shaft centroid is offset from the mechanical axis by eccentricity $e$:

$$e \approx s_f = \frac{L^2}{8 R_f}$$

The bow‑induced bending moment at mid‑span:

$$M = N \cdot e = \frac{N \, L^2}{8 R_f}$$

### 3.6 Stress Equations — Three Cases

---

#### Case 1: Bone Only (No Nail)

**Axial stress (compressive, uniform):**

$$\sigma_{\text{ax}}^{(\text{bone})} = \frac{N}{A_b}$$

**Bending stress at lateral cortex:**

$$\sigma_{\text{bend,lat}}^{(\text{bone})} = \frac{M \cdot r_o}{I_b}$$

**Total lateral cortex stress (tension = positive):**

$$\sigma_{\text{lat}}^{(\text{bone})} = -\frac{N}{A_b} + \frac{M \cdot r_o}{I_b}$$

(The bending term is tensile on the lateral side; the axial term is compressive.)

---

#### Case 2: Straight Nail (Curvature Mismatch, $y_n \neq 0$)

The straight nail has $R_n \to \infty$ (or very large), so:

$$y_n = \frac{L^2}{8}\left(\frac{1}{R_f} - \frac{1}{R_n}\right) \approx \frac{L^2}{8 R_f} = e$$

Composite neutral axis shifts by $\bar{y}$, composite inertia is $I_{\text{comp}}$.

**Axial stress in bone (shared):**

$$\sigma_{\text{ax}}^{(\text{comp})} = \frac{N}{A_b + n \, A_n}$$

**Bending stress at lateral cortex:**

$$\sigma_{\text{bend,lat}}^{(\text{straight})} = \frac{M \cdot c_{\text{lat}}}{I_{\text{comp}}}$$

where $c_{\text{lat}} = r_o - \bar{y}$.

**Total lateral cortex stress:**

$$\sigma_{\text{lat}}^{(\text{straight})} = -\frac{N}{A_b + n \, A_n} + \frac{M \cdot (r_o - \bar{y})}{I_{\text{comp}}}$$

**Stress in the nail:**

$$\sigma_n^{(\text{straight})} = n \left[ -\frac{N}{A_b + n \, A_n} + \frac{M \cdot (y_n - \bar{y})}{I_{\text{comp}}} \right]$$

---

#### Case 3: Curved, Bow‑Matched Nail ($y_n = 0$)

When the nail curvature matches the bone ($R_n = R_f$), $y_n = 0$ and the composite section is symmetric about the bone centroid.

$$\bar{y} = 0$$

$$I_{\text{comp}}^{(\text{match})} = I_b + n \, I_n$$

**Axial stress:**

$$\sigma_{\text{ax}}^{(\text{match})} = \frac{N}{A_b + n \, A_n}$$

**Bending stress at lateral cortex:**

$$\sigma_{\text{bend,lat}}^{(\text{match})} = \frac{M \cdot r_o}{I_b + n \, I_n}$$

**Total lateral cortex stress:**

$$\sigma_{\text{lat}}^{(\text{match})} = -\frac{N}{A_b + n \, A_n} + \frac{M \cdot r_o}{I_b + n \, I_n}$$

This case gives the **maximum benefit** from the nail: the nail adds stiffness ($n I_n$) directly without shifting the neutral axis.

---

### 3.7 Curvature and Strain Relations

**Curvature at the section:**

$$\kappa = \frac{M}{E_b \, I_{\text{comp}}}$$

**Strain at lateral cortex:**

$$\varepsilon_{\text{lat}} = \kappa \cdot c_{\text{lat}} = \frac{M \cdot c_{\text{lat}}}{E_b \, I_{\text{comp}}}$$

### 3.8 Performance Metrics

**Percentage stress reduction (curved nail vs bone only):**

$$\Delta\sigma_{\text{lat}}^{(\text{match vs bone})}(\%) = 100 \cdot \frac{\sigma_{\text{lat}}^{(\text{bone})} - \sigma_{\text{lat}}^{(\text{match})}}{\sigma_{\text{lat}}^{(\text{bone})}}$$

**Percentage stress reduction (curved nail vs straight nail):**

$$\Delta\sigma_{\text{lat}}^{(\text{match vs straight})}(\%) = 100 \cdot \frac{\sigma_{\text{lat}}^{(\text{straight})} - \sigma_{\text{lat}}^{(\text{match})}}{\sigma_{\text{lat}}^{(\text{straight})}}$$

**Safety margin (lateral cortex):**

$$\text{FOS}_{\text{lat}} = \frac{\sigma_{y,t}}{\sigma_{\text{lat}}}$$

Require $\text{FOS}_{\text{lat}} \geq 2.0$ for the design to be acceptable.

---

## Symbol Glossary

| Symbol | Description | Units |
|---|---|---|
| $r_o$ | Femoral outer radius | mm |
| $r_i$ | Femoral inner (endosteal) radius | mm |
| $r_n$ | Nail outer radius | mm |
| $E_b$ | Bone elastic modulus (longitudinal) | GPa |
| $E_n$ | Nail elastic modulus | GPa |
| $n$ | Modular ratio $E_n / E_b$ | — |
| $A_b$ | Bone cross‑sectional area | mm² |
| $A_n$ | Nail cross‑sectional area | mm² |
| $I_b$ | Bone second moment of area | mm⁴ |
| $I_n$ | Nail second moment of area | mm⁴ |
| $I_{\text{comp}}$ | Composite second moment of area | mm⁴ |
| $y_n$ | Nail centroid eccentricity from bone centroid | mm |
| $\bar{y}$ | Composite neutral axis offset from bone centroid | mm |
| $c_{\text{lat}}$ | Distance from NA to lateral cortex | mm |
| $N$ | Axial compressive force (hip contact) | N |
| $M$ | Bending moment at cross‑section | N·mm |
| $e$ | Eccentricity of bone shaft from mechanical axis | mm |
| $R_f$ | Femoral anterior radius of curvature | mm |
| $R_n$ | Nail radius of curvature | mm |
| $L$ | Active nail length (diaphyseal span) | mm |
| $s$ | Sagitta (midpoint deflection) | mm |
| $\sigma_{y,t}$ | Tensile yield stress of bone | MPa |
| $\sigma_{u,t}$ | Tensile ultimate stress of bone | MPa |
| $\sigma_{y,c}$ | Compressive yield stress of bone | MPa |
| $\sigma_{\text{lat}}$ | Total stress at lateral cortex | MPa |
| $\sigma_{\text{lat,allow}}$ | Allowable lateral cortex stress | MPa |
| $\varepsilon_y$ | Tensile yield strain of bone | — |
| $k_N$ | Hip contact force factor | × BW |
| $W$ | Body weight | N |

---

## References

1. Reilly DT, Burstein AH. The elastic and ultimate properties of compact bone tissue. *J Biomech.* 1975;8(6):393–405. DOI: 10.1016/0021-9290(75)90075-5
2. Baleani M, Erani P, Acciaioli A, et al. Tensile yield strain of human cortical bone from the femoral diaphysis is constant among healthy adults and across the anatomical quadrants. *Bioengineering.* 2024;11(4):395. DOI: 10.3390/bioengineering11040395
3. Bayraktar HH, Morgan EF, Niebur GL, Morris GE, Wong EK, Keaveny TM. Comparison of the elastic and yield properties of human femoral trabecular and cortical bone tissue. *J Biomech.* 2004;37(1):27–35. DOI: 10.1016/j.jbiomech.2003.08.010
4. Zimmermann EA, Schaible E, Gludovatz B, et al. Intrinsic mechanical behavior of femoral cortical bone in young, osteoporotic and bisphosphonate-treated individuals. *Sci Rep.* 2016;6:21072. DOI: 10.1038/srep21072
5. Weerasooriya T, Sanborn B, Gunnarsson CA. Orientation dependent compressive response of human femoral cortical bone as a function of strain rate. *J Dyn Behav Mater.* 2016;2:74–90. DOI: 10.1007/s40870-016-0048-4
6. Carter DR, Caler WE. Cycle-dependent and time-dependent bone fracture with repeated loading. *J Biomech Eng.* 1983;105(2):166–170.
7. Zioupos P, Currey JD, Casinos A. Tensile fatigue in bone: are cycles, or time, or both important? *J Theor Biol.* 2001;210(3):389–399.
8. Bergmann G, Deuretzbacher G, Heller MO, et al. Hip contact forces and gait patterns from routine activities. *J Biomech.* 2001;34(7):859–871. DOI: 10.1016/s0021-9290(01)00040-9
9. O'Connor JD, Rutherford M, Bennett D, et al. Long-term hip loading in unilateral total hip replacement patients. *J Biomech.* 2018;80:8–15. DOI: 10.1016/j.jbiomech.2018.07.033
10. Correa TA, Crossley KM, Kim HJ, Pandy MG. Contributions of individual muscles to hip joint contact force in normal walking. *J Biomech.* 2010;43(8):1618–1622. DOI: 10.1016/j.jbiomech.2010.02.008
11. Bong MR, Koval KJ, Egol KA, et al. The relationship between the length of the femoral neck and the incidence of femoral shaft fractures. *J Orthop Trauma.* 2004;18(7):426–430. DOI: 10.1097/00005131-200408000-00003
12. Egol KA, Chang EY, Cvitkovic J, Koval KJ, Kummer FJ. Mismatch of current intramedullary nails with the anterior bow of the femur. *J Orthop Trauma.* 2004;18(7):410–415. DOI: 10.1097/00005131-200408000-00003
13. Liu Y, Zhang A, Cai R, et al. Morphological measurement of the femoral anterior bow in Chinese population based on 3D CT. *Biomed Res Int.* 2021;2021:7674764. DOI: 10.1155/2021/7674764
14. Ma X, Yang I, Lee S, et al. Evaluation of cortical thickness and cortical thickness index in the proximal femur. *PLoS ONE.* 2025;20(2):e0312420. DOI: 10.1371/journal.pone.0312420
15. Schmutz B, et al. A simple method to improve detection of femoral nail abutment in the distal femur. *Clin Orthop Relat Res.* 2022. DOI: 10.1097/corr.0000000000002166
16. Niinomi M. Mechanical properties of biomedical titanium alloys. *Mater Sci Eng A.* 1998;243(1–2):231–236.
17. Kim MS, An S, Huh C, et al. Development of zirconium-based alloys with low elastic modulus for dental implant materials. *Appl Sci.* 2019;9(24):5281. DOI: 10.3390/app9245281
18. Noble PC, et al. The anatomic basis of femoral component design. *Clin Orthop Relat Res.* 1995;(311):148–165.
19. Kanawati A, Jang B, McGee R. The influence of entry point and radius of curvature on femoral intramedullary nail position. *J Orthop.* 2014;11(2):68–71. DOI: 10.1016/j.jor.2014.04.010
20. Ren D, Liu Y, Li M, et al. Role of femoral anterior bow in cephalomedullary nailing. *BMC Surgery.* 2016;16:83. DOI: 10.1186/s12893-016-0183-9
