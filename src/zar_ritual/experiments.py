"""Run the simulations reported in Table 4 and Figure 3 of the paper."""
from __future__ import annotations

import json
from pathlib import Path

from .model import DEFAULT, POLICIES, summarise

#: Values of q used for the sweep in Figure 3A.
Q_VALUES = (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)


def run_all(n: int = 10000, main_seed: int = 1, sweep_seed: int = 2) -> dict:
    """Compare the four policies at default settings and sweep q for accept and verify."""
    main = [summarise(p, DEFAULT, n, main_seed) for p in POLICIES]
    sweep = []
    for q in Q_VALUES:
        P = dict(DEFAULT, q=q)
        for p in ("accept", "verify"):
            sweep.append(dict(q=q, policy=p, accuracy=summarise(p, P, n, sweep_seed)["accuracy"]))
    return dict(params=DEFAULT, n=n, main=main, sweep=sweep)


def save(results: dict, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(results, indent=1))
    return path


def table4(results: dict) -> str:
    """Format the main results as a plain-text version of Table 4."""
    names = {
        "accept": "Accept first name",
        "verify": "Verify claim, fixed order",
        "epistemic": "Choose songs for information",
        "care": "Care: repeat what worked",
    }
    head = f"{'Policy':<30}{'Correct':>9}{'Songs':>7}{'Revised':>9}{'Order dev.':>12}{'Repeated':>10}{'None':>7}"
    rows = [head, "-" * len(head)]
    for m in results["main"]:
        rows.append(
            f"{names[m['policy']]:<30}{m['accuracy']:>9.1%}{m['songs']:>7.1f}{m['revised']:>9.0%}"
            f"{m['order_deviation']:>12.0%}{m['repeat_share']:>10.0%}{m['unresolved']:>7.0%}"
        )
    return "\n".join(rows)
