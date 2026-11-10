"""Figures 1 to 3 of the paper.

Figure 1  search and selection of records (counts are fixed values from the review)
Figure 2  three inferential problems in a possession ritual (diagram)
Figure 3  simulation results, drawn from the results produced by experiments.run_all
"""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

BLUE = "#1f5a96"
GREY = "#7a7a7a"
TINT = "#eef3f9"


def _save(fig, outdir: Path, stem: str, tight: bool = True) -> list[Path]:
    outdir.mkdir(parents=True, exist_ok=True)
    kw = dict(bbox_inches="tight") if tight else {}
    paths = [outdir / f"{stem}.png", outdir / f"{stem}.pdf"]
    fig.savefig(paths[0], dpi=300, **kw)
    fig.savefig(paths[1], **kw)
    plt.close(fig)
    return paths


def figure1(outdir: Path) -> list[Path]:
    """Search and selection of records."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.6})
    fig, ax = plt.subplots(figsize=(7.2, 6.4))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def box(x, y, w, h, t, fc="white", bold=False):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="square,pad=0", fc=fc, ec="#333333", lw=0.8))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center",
                fontweight="bold" if bold else "normal", linespacing=1.35)

    def arr(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=0.8, color="#333333", shrinkA=0, shrinkB=0))

    box(1, 92, 47, 7, "Core search", fc=TINT, bold=True)
    box(52, 92, 47, 7, "Context search and citation tracking", fc=TINT, bold=True)
    box(1, 74, 47, 16, "Scopus n = 79\nWeb of Science n = 1,986\n(40 after local filter on both blocks)\n"
                       "PubMed n = 20; Embase n = 25\nEBSCO, incl. APA PsycInfo, n = 15")
    box(52, 74, 47, 16, "Context search: Scopus n = 87;\nWeb of Science n = 68\n"
                        "Forward citations of four anchor papers\nRILM search for zar in Iran\n"
                        "Unique records not screened before n = 489")
    arr(24.5, 74, 24.5, 68)
    arr(75.5, 74, 75.5, 68)
    box(1, 59, 47, 9, "Unique records screened on\ntitle and abstract n = 110")
    box(52, 59, 47, 9, "Matched both concept blocks or cited\nFischer & Tasananukorn (2018) n = 35")
    arr(24.5, 59, 24.5, 53)
    arr(75.5, 59, 75.5, 53)
    box(1, 40, 47, 13, "Excluded n = 102\n(off topic, trance as metaphor,\n"
                       "clinical hypnosis, virtual-reality presence)")
    box(52, 40, 47, 13, "Excluded n = 22\n(religion or spirituality without possession,\n"
                        "or empirical work without an account)")
    arr(24.5, 40, 24.5, 34)
    arr(75.5, 40, 75.5, 34)
    box(1, 22, 47, 12, "Retained n = 8\nAccounts of possession, trance or shamanism: 6\n"
                       "Comparison records, not appraised: 2")
    box(52, 22, 47, 12, "Retained n = 13\nAccounts: 3; published critique: 1\n"
                        "Comparison records, not appraised: 3\nSources on zar in Iran: 6")
    box(1, 4, 47, 12, "Other sources\nPublished exchange on\nRigoli & Lennon (2025a): 4\n"
                      "Related models added by the authors: 2")
    arr(24.5, 22, 58, 16)
    arr(75.5, 22, 75.5, 16)
    box(52, 4, 47, 12, "Appraised in Table 1\n9 accounts and 2 related models", fc=TINT, bold=True)
    arr(48, 10, 52, 10)
    return _save(fig, outdir, "Figure1_search_flow")


def figure2(outdir: Path) -> list[Path]:
    """Three inferential problems in a possession ritual."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7.4})
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    def box(x, y, w, h, t, fc="white", ec="#333333", bold=False, lw=0.8):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=1.2", fc=fc, ec=ec, lw=lw))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center",
                fontweight="bold" if bold else "normal", linespacing=1.3)

    def arr(x1, y1, x2, y2, c="#333333", ls="-"):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="-|>", lw=0.9, color=c, ls=ls, shrinkA=0, shrinkB=0))

    for t, x, w in [("Who infers", 2, 16), ("Hidden variable", 21, 22),
                    ("What is observed", 46, 26), ("Actions available", 75, 23)]:
        ax.text(x + w / 2, 96, t, ha="center", fontweight="bold")
    rows = [
        (70, "1  Possessed\nperson", "Source of own\nmovements and\nsensations",
         "Body signals, the music,\nothers' reactions", "Yield, resist,\nmove, speak", "white", "#333333"),
        (40, "2  Ritual\nspecialist\n(baba, mama)", "Which wind is\npresent and\nwhat it wants",
         "Response to each song,\nthe name spoken,\ncoded signs",
         "Choose songs, question\nthe wind, call other\nspecialists, confirm", TINT, BLUE),
        (10, "3  Kin and\ncommunity", "Is the possession\ngenuine; has the\nperson improved",
         "The performance,\nthe verdict, later\nconduct", "Fund sessions, accept\nthe person as a\nmember",
         "white", "#333333"),
    ]
    for y, a, b, c, d, fc, ec in rows:
        lw = 1.4 if ec == BLUE else 0.8
        box(2, y, 16, 20, a, fc=fc, ec=ec, bold=True, lw=lw)
        box(21, y, 22, 20, b, fc=fc, ec=ec, lw=lw)
        box(46, y, 26, 20, c, fc=fc, ec=ec, lw=lw)
        box(75, y, 23, 20, d, fc=fc, ec=ec, lw=lw)
    arr(59, 70, 59, 60.5, c=BLUE)
    ax.text(57.5, 65, "response\nand name", color=BLUE, fontsize=6.8, va="center", ha="right")
    arr(80, 60, 69, 69.5, c=BLUE, ls="--")
    ax.text(76.5, 66.5, "songs and questions\nreach the person", color=BLUE, fontsize=6.8, va="center", ha="left")
    arr(59, 40, 59, 30.5)
    ax.text(60.5, 35, "verdict and performance", fontsize=6.8, va="center")
    return _save(fig, outdir, "Figure2_three_problems")


def figure3(results: dict, outdir: Path) -> list[Path]:
    """Simulation results: (A) accuracy against q, (B) revisions and order deviations."""
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.linewidth": 0.8,
                         "xtick.major.width": 0.8, "ytick.major.width": 0.8})
    qs = sorted({s["q"] for s in results["sweep"]})
    acc = {p: [next(s["accuracy"] for s in results["sweep"] if s["q"] == q and s["policy"] == p) * 100
               for q in qs] for p in ("accept", "verify")}
    main = {m["policy"]: m for m in results["main"]}
    default_q = results["params"]["q"]

    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw={"width_ratios": [1.15, 1]})
    a.plot(qs, acc["verify"], "-o", color=BLUE, ms=4, lw=1.6, label="Verify claim against coded signs")
    a.plot(qs, acc["accept"], "-s", color=GREY, ms=4, lw=1.6, label="Accept first name")
    a.axvline(default_q, color="#bbbbbb", lw=0.8, ls="--")
    a.text(default_q - 0.005, 97, "default q", color="#777777", fontsize=7.5, ha="right")
    a.set_xlabel("Probability that a wind names itself correctly (q)")
    a.set_ylabel("Correct identification (%)")
    a.set_ylim(20, 100)
    a.set_xticks(qs)
    a.legend(frameon=False, fontsize=7.5, loc="lower right")
    a.set_title("A", loc="left", fontweight="bold")

    pol = ["accept", "verify", "epistemic", "care"]
    lab = ["Accept", "Verify", "Choose for\ninformation", "Care"]
    x = range(4)
    w = 0.38
    rev = [main[p]["revised"] * 100 for p in pol]
    dev = [main[p]["order_deviation"] * 100 for p in pol]
    b.bar([i - w / 2 for i in x], rev, w, color=BLUE, label="First name later replaced")
    b.bar([i + w / 2 for i in x], dev, w, color="#c8c8c8", edgecolor=GREY, lw=0.6,
          label="Departs from fixed song order")
    for i in x:
        b.text(i - w / 2, rev[i] + 1.5, f"{rev[i]:.0f}", ha="center", fontsize=7)
        b.text(i + w / 2, dev[i] + 1.5, f"{dev[i]:.0f}", ha="center", fontsize=7)
    b.set_xticks(list(x))
    b.set_xticklabels(lab, fontsize=7.5)
    b.set_ylabel("Runs (%)")
    b.set_ylim(0, 110)
    b.legend(frameon=False, fontsize=7.5, loc="upper left")
    b.set_title("B", loc="left", fontweight="bold")
    fig.tight_layout()
    return _save(fig, outdir, "Figure3_model", tight=False)
