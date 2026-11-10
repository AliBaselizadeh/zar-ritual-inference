"""Command-line entry point.

Examples
--------
    zar-ritual                      # 10,000 persons per policy, write results/ and figures
    zar-ritual -n 2000              # quicker run
    zar-ritual --no-figures         # numbers only
    zar-ritual --from-results results/results.json   # redraw figures without re-running
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from . import __version__
from .experiments import run_all, save, table4


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="zar-ritual", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("-n", type=int, default=10000, help="simulated persons per policy (default 10000)")
    ap.add_argument("-o", "--outdir", default="results", help="output folder (default: results)")
    ap.add_argument("--no-figures", action="store_true", help="do not draw figures")
    ap.add_argument("--from-results", metavar="JSON", help="redraw figures from an existing results file")
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = ap.parse_args(argv)
    outdir = Path(args.outdir)

    if args.from_results:
        results = json.loads(Path(args.from_results).read_text())
    else:
        t0 = time.time()
        print(f"Running {args.n} simulated persons per policy ...")
        results = run_all(n=args.n)
        path = save(results, outdir / "results.json")
        print(f"Saved {path} ({time.time() - t0:.0f} s)\n")
    print(table4(results))
    print("\nAccuracy against q (accept / verify):")
    for q in sorted({s["q"] for s in results["sweep"]}):
        a = next(s["accuracy"] for s in results["sweep"] if s["q"] == q and s["policy"] == "accept")
        v = next(s["accuracy"] for s in results["sweep"] if s["q"] == q and s["policy"] == "verify")
        print(f"  q = {q:.1f}:  {a:6.1%}  /  {v:6.1%}")

    if not args.no_figures:
        from .figures import figure1, figure2, figure3

        figdir = outdir / "figures"
        for p in figure1(figdir) + figure2(figdir) + figure3(results, figdir):
            print(f"Saved {p}")


if __name__ == "__main__":
    main()
