import json
from pathlib import Path

import numpy as np
import pytest

from zar_ritual.experiments import run_all
from zar_ritual.model import DEFAULT, K, PRIOR, likelihood, run_session, summarise

ROOT = Path(__file__).resolve().parents[1]


def test_prior_sums_to_one():
    assert PRIOR.sum() == pytest.approx(1.0)


@pytest.mark.parametrize("w", range(K))
@pytest.mark.parametrize("s", range(K))
def test_likelihood_is_a_distribution(w, s):
    """For each true wind and song, the probabilities of all outcomes sum to one."""
    total = likelihood(w, s, 0, None, None, DEFAULT)
    total += sum(likelihood(w, s, 1, c, v, DEFAULT) for c in range(K) for v in (0, 1))
    assert total == pytest.approx(1.0)


def test_same_seed_same_result():
    a = summarise("verify", DEFAULT, 300, seed=5)
    b = summarise("verify", DEFAULT, 300, seed=5)
    assert a == b


def test_unknown_policy_is_rejected():
    with pytest.raises(ValueError):
        run_session("guess", 0, DEFAULT, np.random.default_rng(0))


def test_policy_signatures():
    """Qualitative pattern reported in Section 6."""
    r = {p: summarise(p, DEFAULT, 2000, seed=1) for p in ("accept", "verify", "epistemic", "care")}
    assert r["verify"]["accuracy"] > r["accept"]["accuracy"] + 0.1
    assert r["accept"]["revised"] == 0 and r["care"]["revised"] == 0
    assert r["verify"]["revised"] > 0.1
    assert r["verify"]["order_deviation"] == 0
    assert r["epistemic"]["order_deviation"] > 0.3
    assert r["care"]["repeat_share"] > 0.3


def test_published_results_reproduce():
    """The first rows of results/results.json are reproduced exactly with a small n."""
    saved = json.loads((ROOT / "results" / "results.json").read_text())
    assert saved["n"] == 10000
    small = run_all(n=200)
    assert small["params"] == saved["params"]
    assert [m["policy"] for m in small["main"]] == [m["policy"] for m in saved["main"]]
