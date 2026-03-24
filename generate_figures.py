"""
AFF Curved IM Nail — Report Figures (v2, cleaned up)
BMEN 383 — Continuum / Solid Mechanics II

Generates 4 publication-quality figures from numerical_results.md
and extended_analysis_readme.md data.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
from pathlib import Path
import os

os.chdir(Path(__file__).parent)

# ── Global style ──
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 300,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

# Colour palette (colorblind-friendly)
C_BONE     = "#4E89A0"
C_STRAIGHT = "#D07830"
C_CURVED   = "#5A9E58"
C_ALLOW    = "#C0392B"
C_FATIGUE  = "#7D5BA6"
COLORS3    = [C_BONE, C_STRAIGHT, C_CURVED]

BONE_FILL  = "#F2E0C8"
BONE_EDGE  = "#8B7355"
CANAL_EDGE = "#A09080"
NAIL_S_FILL = "#E8A050"
NAIL_S_EDGE = "#B07020"
NAIL_C_FILL = "#6BBF6B"
NAIL_C_EDGE = "#3D8B3D"


# ================================================================
# FIGURE 1 — Vertical sagittal schematic: straight vs curved nail
# ================================================================
def fig1_schematic():
    fig, axes = plt.subplots(1, 2, figsize=(8, 9),
                             gridspec_kw={"wspace": 0.45})

    for ax_idx, (ax, title, nail_type) in enumerate(zip(
            axes,
            ["(a)  Straight nail", "(b)  Curvature-matched nail"],
            ["straight", "curved"])):

        ax.set_aspect("equal")
        ax.axis("off")

        # ── Bowed femur using a parabolic canal centreline ──
        # Proximal = top (t=0), distal = bottom (t=1)
        # Canal bows to the RIGHT (anterior) at mid-shaft
        n_pts = 300
        t = np.linspace(0, 1, n_pts)
        bone_height = 18.0
        bow_amplitude = 2.2  # max lateral bow at midspan (exaggerated)

        # Canal centreline: vertical + parabolic bow
        xm = bow_amplitude * 4 * t * (1 - t)   # peaks at t=0.5
        ym = bone_height * (1 - t)               # top to bottom

        # Perpendicular normals (to the right = anterior)
        dx = np.gradient(xm)
        dy = np.gradient(ym)
        mag = np.sqrt(dx**2 + dy**2)
        # Normal pointing to the right (anterior)
        nx_u = -dy / mag
        ny_u = dx / mag

        bone_hw = 2.2    # bone half-width
        canal_hw = 1.3   # canal half-width

        # Cortex walls
        xa = xm + bone_hw * nx_u;  ya = ym + bone_hw * ny_u
        xp = xm - bone_hw * nx_u;  yp = ym - bone_hw * ny_u
        # Canal walls
        xca = xm + canal_hw * nx_u; yca = ym + canal_hw * ny_u
        xcp = xm - canal_hw * nx_u; ycp = ym - canal_hw * ny_u

        # Draw cortical bone (filled polygon)
        verts_outer = list(zip(xa, ya)) + list(zip(xp[::-1], yp[::-1]))
        ax.add_patch(plt.Polygon(verts_outer, closed=True,
                                 facecolor=BONE_FILL, edgecolor=BONE_EDGE,
                                 linewidth=1.8, zorder=1))

        # Canal interior (white)
        verts_canal = list(zip(xca, yca)) + list(zip(xcp[::-1], ycp[::-1]))
        ax.add_patch(plt.Polygon(verts_canal, closed=True,
                                 facecolor="white", edgecolor=CANAL_EDGE,
                                 linewidth=0.8, linestyle="--", zorder=2))

        # ── Nail ──
        nail_hw = 0.85
        if nail_type == "straight":
            # Straight line from proximal entry to distal entry
            xn_c = np.linspace(xm[0], xm[-1], n_pts)
            yn_c = np.linspace(ym[0], ym[-1], n_pts)
            nfill, nedge = NAIL_S_FILL, NAIL_S_EDGE
        else:
            xn_c, yn_c = xm.copy(), ym.copy()
            nfill, nedge = NAIL_C_FILL, NAIL_C_EDGE

        # Nail perpendicular offsets
        dnx = np.gradient(xn_c); dny = np.gradient(yn_c)
        nmag = np.sqrt(dnx**2 + dny**2)
        nnx = -dny / nmag; nny = dnx / nmag

        xna = xn_c + nail_hw * nnx; yna = yn_c + nail_hw * nny
        xnp = xn_c - nail_hw * nnx; ynp = yn_c - nail_hw * nny

        verts_nail = list(zip(xna, yna)) + list(zip(xnp[::-1], ynp[::-1]))
        ax.add_patch(plt.Polygon(verts_nail, closed=True,
                                 facecolor=nfill, edgecolor=nedge,
                                 linewidth=1.2, alpha=0.88, zorder=3))

        # ── Force arrow at proximal end ──
        ax.annotate("",
                    xy=(xm[0], ym[0] + 0.2),
                    xytext=(xm[0], ym[0] + 3.5),
                    arrowprops=dict(arrowstyle="->,head_width=0.35,"
                                   "head_length=0.25",
                                   color="black", lw=2.2), zorder=5)
        ax.text(xm[0] + 0.5, ym[0] + 3.0, r"$N$", fontsize=15,
                fontweight="bold", ha="left", va="center")

        # ── Side labels (rotated along the bone axis) ──
        mid = n_pts // 2
        # Place "Anterior" at 25% from top (above impingement zone)
        q1 = int(0.20 * n_pts)
        ax.text(xa[q1] + 1.3, ya[q1], "Anterior", fontsize=10,
                ha="left", va="center", color="#555", fontstyle="italic",
                rotation=-5)
        ax.text(xp[q1] - 1.3, yp[q1], "Posterior", fontsize=10,
                ha="right", va="center", color="#555", fontstyle="italic",
                rotation=-5)

        # ── Proximal / Distal ──
        ax.text(xm[0] - 3.0, ym[0] + 0.3, "Proximal", fontsize=9,
                ha="center", color="#777")
        ax.text(xm[-1] - 3.0, ym[-1] - 0.3, "Distal", fontsize=9,
                ha="center", color="#777")

        # ── Annotations for each nail type ──
        if nail_type == "straight":
            # y_n double-arrow at ~65% along bone
            idx = int(0.65 * n_pts)
            ax.annotate("",
                        xy=(xn_c[idx], yn_c[idx]),
                        xytext=(xm[idx], ym[idx]),
                        arrowprops=dict(arrowstyle="<->", color="#333",
                                        lw=1.3, shrinkA=1, shrinkB=1),
                        zorder=6)
            lx = max(xn_c[idx], xm[idx]) + 0.6
            ly = (yn_c[idx] + ym[idx]) / 2
            ax.text(lx, ly, r"$y_n$", fontsize=13, fontweight="bold",
                    ha="left", va="center", color="#333")

            # Impingement X markers along anterior cortex
            for frac in [0.45, 0.55, 0.65, 0.75, 0.85]:
                i2 = int(frac * n_pts)
                ax.plot(xa[i2], ya[i2], "x", color=C_ALLOW,
                        markersize=7, markeredgewidth=2.0, zorder=6)

            # Impingement label
            i_imp = int(0.55 * n_pts)
            ax.annotate("Impingement\nrisk zone",
                        xy=(xa[i_imp] + 0.1, ya[i_imp]),
                        xytext=(xa[i_imp] + 3.0, ya[i_imp] + 1.5),
                        fontsize=9, color=C_ALLOW, fontweight="bold",
                        ha="left", va="center",
                        arrowprops=dict(arrowstyle="->", color=C_ALLOW,
                                        lw=1.5,
                                        connectionstyle="arc3,rad=-0.15"),
                        zorder=6)
        else:
            # y_n = 0 label
            ax.text(xm[mid] + 2.0, ym[mid], r"$y_n = 0$",
                    fontsize=12, ha="left", va="center",
                    color=NAIL_C_EDGE, fontweight="bold",
                    bbox=dict(facecolor="white", edgecolor=NAIL_C_EDGE,
                              boxstyle="round,pad=0.3", alpha=0.85))

        # Auto-set axis limits with padding
        all_x = np.concatenate([xa, xp])
        all_y = np.concatenate([ya, yp])
        pad_x, pad_y = 6.5, 4.5
        ax.set_xlim(all_x.min() - pad_x, all_x.max() + pad_x + 1.5)
        ax.set_ylim(all_y.min() - pad_y, all_y.max() + pad_y)

        ax.set_title(title, fontsize=13, fontweight="bold", pad=10)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=BONE_FILL, edgecolor=BONE_EDGE,
                       lw=1.5, label="Cortical bone"),
        mpatches.Patch(facecolor=NAIL_S_FILL, edgecolor=NAIL_S_EDGE,
                       lw=1.2, label="Straight nail"),
        mpatches.Patch(facecolor=NAIL_C_FILL, edgecolor=NAIL_C_EDGE,
                       lw=1.2, label="Curved nail"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=3,
              frameon=True, fontsize=10, bbox_to_anchor=(0.5, 0.01),
              edgecolor="#ccc")

    fig.suptitle(
        "Figure 1.  Sagittal-plane schematic: straight vs. curvature-matched nail",
        fontsize=12, fontweight="bold", y=0.97)
    fig.savefig("fig1_bowed_femur_schematic.png", facecolor="white")
    plt.close(fig)
    print("  Saved fig1_bowed_femur_schematic.png")


# ================================================================
# FIGURE 2 — Bar chart: lateral cortex stress (combined sag+frontal)
# ================================================================
def fig2_stress_bars():
    # Data from extended_analysis_readme.md §3.5
    cases       = ["Bone only", "Straight nail", "Curved nail"]
    sigma_sag   = np.array([15.16, 12.45, 14.41])
    sigma_front = np.array([52.56, 42.62, 42.62])
    sigma_total = sigma_sag + sigma_front  # 67.72, 55.07, 57.03
    fos_total   = np.array([1.48, 1.82, 1.75])

    sigma_yt    = 100.0
    sigma_end   = 59.9

    x = np.arange(len(cases))
    width = 0.52

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Bottom portion: sagittal (lighter, hatched)
    bars_sag = ax.bar(x, sigma_sag, width,
                      color=COLORS3, alpha=0.45, edgecolor="white", lw=0.8,
                      zorder=3)
    # Top portion: frontal (full colour)
    bars_front = ax.bar(x, sigma_front, width, bottom=sigma_sag,
                        color=COLORS3, alpha=0.92, edgecolor="white", lw=0.8,
                        zorder=3)
    # Add hatching to sagittal portion for distinction
    for bar in bars_sag:
        bar.set_hatch("///")
        bar.set_edgecolor("#ffffff88")

    # Reference lines
    ax.axhline(sigma_yt, color=C_ALLOW, linestyle="--", linewidth=1.6, zorder=2,
               label=r"$\sigma_{y,t}^{\,\mathrm{cons}}$ = 100 MPa")
    ax.axhline(sigma_end, color=C_FATIGUE, linestyle=":", linewidth=1.6, zorder=2,
               label=r"$\sigma_{\mathrm{endurance}}$ = 59.9 MPa")

    # Value labels inside each bar segment
    for i in range(3):
        # Sagittal label
        ax.text(i, sigma_sag[i] / 2, f"{sigma_sag[i]:.1f}",
                ha="center", va="center", fontsize=9.5,
                color="white", fontweight="bold", zorder=4)
        # Frontal label
        ax.text(i, sigma_sag[i] + sigma_front[i] / 2,
                f"{sigma_front[i]:.1f}",
                ha="center", va="center", fontsize=9.5,
                color="white", fontweight="bold", zorder=4)

    # FOS labels ABOVE bars (offset higher to avoid endurance line)
    for i, (s, f) in enumerate(zip(sigma_total, fos_total)):
        y_label = max(s, sigma_end) + 4.5
        ax.annotate(f"FOS = {f:.2f}",
                    xy=(i, s), xytext=(i, y_label),
                    ha="center", va="bottom", fontsize=10.5,
                    fontweight="bold", color="#222",
                    arrowprops=dict(arrowstyle="-", color="#aaa",
                                    lw=0.8, shrinkB=2),
                    zorder=5)

    ax.set_xticks(x)
    ax.set_xticklabels(cases, fontsize=11, fontweight="bold")
    ax.set_ylabel(r"Lateral cortex stress  $\sigma_{\mathrm{lat,total}}$  (MPa)",
                  fontsize=12)
    ax.set_ylim(0, 118)

    # Custom legend
    legend_handles = [
        mpatches.Patch(facecolor="#888", alpha=0.45, hatch="///",
                       edgecolor="#fff", label="Sagittal (bow-induced)"),
        mpatches.Patch(facecolor="#888", alpha=0.92,
                       label="Frontal (hip offset)"),
        Line2D([0], [0], color=C_ALLOW, ls="--", lw=1.6,
               label=r"$\sigma_{y,t}^{\,\mathrm{cons}}$ = 100 MPa"),
        Line2D([0], [0], color=C_FATIGUE, ls=":", lw=1.6,
               label=r"$\sigma_{\mathrm{endurance}}$ = 59.9 MPa"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", framealpha=0.92,
              edgecolor="#ccc", fontsize=9.5)

    ax.set_title("Figure 2.  Combined lateral cortex stress under walking loads",
                 fontweight="bold", fontsize=12, pad=14)
    fig.tight_layout()
    fig.savefig("fig2_lateral_stress_bars.png", facecolor="white")
    plt.close(fig)
    print("  Saved fig2_lateral_stress_bars.png")


# ================================================================
# FIGURE 3 — Compatibility index vs. stress (scatter)
# ================================================================
def fig3_compatibility():
    # Data from extended_analysis_readme.md §4.2
    # fmt: (C, sigma_total, label, color, marker, filled)
    points = [
        # Nominal
        (0.000, 67.72, "Bone only\n(no nail)", C_BONE,     "s", True),
        (0.146, 55.07, "Straight nail",        C_STRAIGHT, "D", True),
        (0.000, 57.03, "Curved nail",          C_CURVED,   "o", True),
        # Asian female
        (0.282, 42.04, "Straight\n(Asian)",    C_STRAIGHT, "D", False),
        (0.000, 45.69, "Curved\n(Asian)",      C_CURVED,   "o", False),
    ]

    fig, ax = plt.subplots(figsize=(7.5, 5.5))

    # Shaded risk zone
    ax.axvspan(0.14, 0.36, alpha=0.07, color=C_ALLOW, zorder=0)
    ax.text(0.245, 52, "Higher\nimpingement\nrisk", fontsize=8.5,
            ha="center", va="center", color=C_ALLOW, fontstyle="italic",
            fontweight="bold", alpha=0.7)

    # Endurance line
    ax.axhline(59.9, color=C_FATIGUE, ls=":", lw=1.4, zorder=1)
    ax.text(0.345, 60.8, r"$\sigma_{\mathrm{endurance}}$", fontsize=9,
            color=C_FATIGUE, ha="right", va="bottom")

    # Plot points
    for C, sigma, label, color, marker, filled in points:
        fc = color if filled else "none"
        s = 180 if filled else 140
        lw = 0.9 if filled else 2.0
        ax.scatter(C, sigma, s=s, color=fc, marker=marker,
                   edgecolors=color, linewidths=lw, zorder=5)

    # ── Labels with manual positioning to avoid overlap ──
    # Bone only (top-left)
    ax.annotate("Bone only\n67.7 MPa", xy=(0.000, 67.72),
                xytext=(0.04, 71.5), fontsize=9, fontweight="bold",
                color=C_BONE, ha="left",
                arrowprops=dict(arrowstyle="-", color=C_BONE, lw=0.8))
    # Curved nail (below bone-only on C=0 axis)
    ax.annotate("Curved nail\n57.0 MPa", xy=(0.000, 57.03),
                xytext=(0.04, 53.0), fontsize=9, fontweight="bold",
                color=C_CURVED, ha="left",
                arrowprops=dict(arrowstyle="-", color=C_CURVED, lw=0.8))
    # Straight nail
    ax.annotate("Straight nail\n55.1 MPa", xy=(0.146, 55.07),
                xytext=(0.19, 55.07), fontsize=9, fontweight="bold",
                color=C_STRAIGHT, ha="left")
    # Asian curved (open)
    ax.annotate("Curved, Asian\n45.7 MPa", xy=(0.000, 45.69),
                xytext=(0.04, 42.5), fontsize=8.5, color=C_CURVED,
                ha="left", fontstyle="italic",
                arrowprops=dict(arrowstyle="-", color=C_CURVED, lw=0.6))
    # Asian straight (open)
    ax.annotate("Straight, Asian\n42.0 MPa", xy=(0.282, 42.04),
                xytext=(0.21, 38.5), fontsize=8.5, color=C_STRAIGHT,
                ha="left", fontstyle="italic",
                arrowprops=dict(arrowstyle="-", color=C_STRAIGHT, lw=0.6))

    # Dashed line connecting straight nail scenarios
    ax.plot([0.146, 0.282], [55.07, 42.04], ls="--", color=C_STRAIGHT,
            alpha=0.4, lw=1.3, zorder=2)
    # Dashed line connecting curved nail scenarios
    ax.plot([0.000, 0.000], [57.03, 45.69], ls="--", color=C_CURVED,
            alpha=0.4, lw=1.3, zorder=2)

    # Custom legend
    legend_handles = [
        Line2D([0], [0], marker="s", color="w", markerfacecolor=C_BONE,
               markersize=9, markeredgecolor="k", markeredgewidth=0.5,
               label="Bone only"),
        Line2D([0], [0], marker="D", color="w", markerfacecolor=C_STRAIGHT,
               markersize=9, markeredgecolor="k", markeredgewidth=0.5,
               label="Straight nail"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=C_CURVED,
               markersize=9, markeredgecolor="k", markeredgewidth=0.5,
               label="Curved nail"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="none",
               markersize=9, markeredgecolor="#666", markeredgewidth=1.5,
               label="Asian female scenario"),
    ]
    ax.legend(handles=legend_handles, loc="upper right", framealpha=0.92,
              edgecolor="#ccc")

    ax.set_xlabel(r"Compatibility index  $C = |y_n| \,/\, r_o$", fontsize=12)
    ax.set_ylabel(r"$\sigma_{\mathrm{lat,total}}$  (MPa)", fontsize=12)
    ax.set_xlim(-0.025, 0.36)
    ax.set_ylim(35, 76)

    ax.set_title("Figure 3.  Compatibility index vs. lateral cortex stress",
                 fontweight="bold", fontsize=12, pad=14)
    fig.tight_layout()
    fig.savefig("fig3_compatibility_vs_stress.png", facecolor="white")
    plt.close(fig)
    print("  Saved fig3_compatibility_vs_stress.png")


# ================================================================
# FIGURE 4 — Two-segment EI schematic (taller, clearer)
# ================================================================
def fig4_tip_EI():
    fig, axes = plt.subplots(1, 2, figsize=(11, 6),
                             gridspec_kw={"wspace": 0.30})

    configs = [
        ("(a)  Short / mid-length nail", 0.42, 1.0, "100%"),
        ("(b)  Long, curvature-matched nail", 0.72, 0.6, "60%"),
    ]

    for ax, (title, nail_frac, m_frac, m_label) in zip(axes, configs):
        ax.set_xlim(-1, 13)
        ax.set_ylim(-5.5, 7)
        ax.set_aspect("equal")
        ax.axis("off")

        beam_len = 11.0
        beam_hh = 0.8  # beam half-height
        r1_end = beam_len * nail_frac

        # ── Region 1: bone + nail ──
        rect1 = Rectangle((0, -beam_hh), r1_end, 2 * beam_hh,
                           facecolor="#B8D4E3", edgecolor="#3A6B8C",
                           linewidth=2.0, zorder=2)
        ax.add_patch(rect1)

        # Nail bar inside
        nail_hh = 0.35
        nail_rect = Rectangle((0.1, -nail_hh), r1_end - 0.2, 2 * nail_hh,
                               facecolor=NAIL_S_FILL, edgecolor=NAIL_S_EDGE,
                               linewidth=1.2, alpha=0.85, zorder=3)
        ax.add_patch(nail_rect)

        # ── Region 2: bone only ──
        rect2 = Rectangle((r1_end, -beam_hh), beam_len - r1_end, 2 * beam_hh,
                           facecolor=BONE_FILL, edgecolor=BONE_EDGE,
                           linewidth=2.0, zorder=2)
        ax.add_patch(rect2)

        # ── Transition line ──
        ax.plot([r1_end, r1_end], [-beam_hh - 0.6, beam_hh + 0.6],
                color=C_ALLOW, linewidth=3.0, zorder=4)
        ax.text(r1_end, beam_hh + 1.0, "Nail tip",
                fontsize=10, ha="center", va="bottom",
                color=C_ALLOW, fontweight="bold")

        # ── EI labels below beam ──
        ax.text(r1_end / 2, -beam_hh - 1.0,
                r"$EI_1$  (bone + nail)",
                fontsize=10, ha="center", va="top",
                color="#3A6B8C", fontweight="bold")
        ax.text((r1_end + beam_len) / 2, -beam_hh - 1.0,
                r"$EI_2$  (bone only)",
                fontsize=10, ha="center", va="top",
                color=BONE_EDGE, fontweight="bold")

        # ── Bending moment diagram above beam ──
        M_peak = 3.0
        x_bmd = np.array([0, r1_end, beam_len])
        y_bmd = np.array([M_peak,
                          M_peak * (1 - nail_frac * 0.55),
                          M_peak * 0.08])
        y_bmd_plot = y_bmd + beam_hh + 1.6

        ax.fill_between(x_bmd, beam_hh + 1.6, y_bmd_plot,
                        alpha=0.18, color=C_FATIGUE, zorder=1)
        ax.plot(x_bmd, y_bmd_plot, color=C_FATIGUE, lw=1.8, zorder=1)
        ax.text(0.5, y_bmd_plot[0] + 0.25, "$M(x)$", fontsize=10,
                color=C_FATIGUE, fontweight="bold")

        # ── Curvature arrows at transition ──
        arrow_y_start = -beam_hh - 1.8
        k1_len = 1.2
        k2_len = k1_len * 1.23

        # kappa_1 (left of transition)
        ax.annotate("",
                    xy=(r1_end - 0.5, arrow_y_start - k1_len),
                    xytext=(r1_end - 0.5, arrow_y_start),
                    arrowprops=dict(arrowstyle="->,head_width=0.25",
                                   color="#3A6B8C", lw=2.0))
        ax.text(r1_end - 1.2, arrow_y_start - k1_len / 2,
                r"$\kappa_1$", fontsize=11, ha="right", va="center",
                color="#3A6B8C", fontweight="bold")

        # kappa_2 (right of transition)
        ax.annotate("",
                    xy=(r1_end + 0.5, arrow_y_start - k2_len),
                    xytext=(r1_end + 0.5, arrow_y_start),
                    arrowprops=dict(arrowstyle="->,head_width=0.25",
                                   color=BONE_EDGE, lw=2.0))
        ax.text(r1_end + 1.2, arrow_y_start - k2_len / 2,
                r"$\kappa_2$", fontsize=11, ha="left", va="center",
                color=BONE_EDGE, fontweight="bold")

        # Delta-kappa label
        ax.text(r1_end, arrow_y_start - max(k1_len, k2_len) - 0.7,
                fr"$\Delta\kappa$  ({m_label})",
                fontsize=11, ha="center", va="top",
                color=C_ALLOW, fontweight="bold")

        # ── Proximal / Distal ──
        ax.text(0, beam_hh + 0.5, "Proximal", fontsize=9, ha="left",
                color="#777")
        ax.text(beam_len, beam_hh + 0.5, "Distal", fontsize=9, ha="right",
                color="#777")

        ax.set_title(title, fontsize=12, fontweight="bold", pad=8)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor="#B8D4E3", edgecolor="#3A6B8C", lw=1.5,
                       label="Region 1: bone + nail"),
        mpatches.Patch(facecolor=BONE_FILL, edgecolor=BONE_EDGE, lw=1.5,
                       label="Region 2: bone only"),
        mpatches.Patch(facecolor=NAIL_S_FILL, edgecolor=NAIL_S_EDGE, lw=1.0,
                       alpha=0.85, label="IM nail"),
        Line2D([0], [0], color=C_ALLOW, lw=3.0,
               label="Transition (nail tip)"),
        mpatches.Patch(facecolor=C_FATIGUE, alpha=0.18, edgecolor=C_FATIGUE,
                       label="Bending moment $M(x)$"),
    ]
    fig.legend(handles=legend_elements, loc="lower center", ncol=5,
              frameon=True, fontsize=9.5, bbox_to_anchor=(0.5, -0.03),
              edgecolor="#ccc")

    fig.suptitle(
        "Figure 4.  Two-segment EI model: nail tip stiffness discontinuity",
        fontsize=12, fontweight="bold", y=0.99)
    fig.subplots_adjust(bottom=0.08, top=0.92, left=0.02, right=0.98)
    fig.savefig("fig4_tip_EI_schematic.png", facecolor="white")
    plt.close(fig)
    print("  Saved fig4_tip_EI_schematic.png")


# ================================================================
# RUN ALL
# ================================================================
if __name__ == "__main__":
    print("Generating figures (v2)...")
    fig1_schematic()
    fig2_stress_bars()
    fig3_compatibility()
    fig4_tip_EI()
    print("\nAll figures saved.")
