# zar-ritual-inference

Simulation code and figures for the paper:

> Baselizadeh, A., & Gharasou, M. (2026). *Whose inference? A critical review of predictive-processing accounts of spirit possession, with zar rituals in Hormozgan as a test case* [Manuscript in preparation].

The paper argues that predictive-processing accounts of spirit possession model the inference of the possessed person, but not the public inference that ritual specialists make about which spirit is present. Section 6 of the paper uses a small simulation to show which traces different ritual policies would leave in a session record. This repository contains that simulation and the code for Figures 1 to 3.

The parameters are illustrative. The model is not fitted to any data.

## The model

The hidden variable is the wind (spirit) that afflicts a person. There are six winds:

| Wind | Class | Prior probability |
|---|---|---|
| 0, 1, 2 | Non-Muslim winds, addressed by zar songs | 0.25, 0.20, 0.15 |
| 3, 4 | Mashayekh winds | 0.15, 0.15 |
| 5 | Nuban wind | 0.10 |

Each night follows a fixed order: zar songs first, then mashayekh songs. The third night plays the nuban song.

| Parameter | Meaning | Default |
|---|---|---|
| `p_hit` | Probability of a response when the song of the true wind is played | 0.70 |
| `p_fa` | Probability of a response to any other song | 0.15 |
| `q` | Probability that a responding wind gives its true name | 0.70 |
| `s_true` | Probability that the coded signs fit the claimed name, if the name is true | 0.85 |
| `s_false` | Probability that the coded signs fit the claimed name, if the name is false | 0.20 |
| `stop` | Posterior probability at which the Verify and Choose policies stop | 0.90 |

When a wind gives a false name, the name usually echoes the song being played.

Four ritual policies are compared:

| Policy | Code name | What it does |
|---|---|---|
| Accept first name | `accept` | Takes the first name spoken |
| Verify claim, fixed order | `verify` | Keeps the fixed order, updates a probability for each wind after every song, and stops when one wind reaches `stop` |
| Choose songs for information | `epistemic` | Uses the same probabilities, but picks each next song for its expected information gain, within the rule that mashayekh songs end the zar part of a night |
| Care: repeat what worked | `care` | Replays the first song that drew a response and takes the first name spoken |

## Installation

You need Python 3.9 or later.

```bash
git clone https://github.com/AliBaselizadeh/zar-ritual-inference.git
cd zar-ritual-inference
python -m venv .venv
source .venv/bin/activate          # on Windows: .venv\Scripts\activate
pip install -e .
```

## Usage

Reproduce Table 4 and Figures 1 to 3 of the paper (about 20 seconds):

```bash
zar-ritual
```

This writes `results/results.json` and the figures in `results/figures/` (PNG at 300 dpi and PDF).

Other options:

```bash
zar-ritual -n 2000                                   # fewer simulated persons, quicker
zar-ritual --no-figures                              # numbers only
zar-ritual --from-results results/results.json       # redraw figures without re-running
python -m zar_ritual --help
```

From Python:

```python
from zar_ritual import DEFAULT, summarise

summarise("verify", DEFAULT, n=10000, seed=1)
summarise("accept", dict(DEFAULT, q=0.3), n=10000, seed=2)
```

## Results

With 10,000 simulated persons per policy (seed 1), the output matches Table 4 of the paper:

| Policy | Correct identification | Songs played (mean) | First name later replaced | Departs from fixed order | Share of songs repeated | No identification |
|---|---|---|---|---|---|---|
| Accept first name | 68% | 3.4 | 0% | 0% | 0% | 3% |
| Verify claim, fixed order | 89.5% | 5.6 | 26% | 0% | 0% | 4% |
| Choose songs for information | 87.5% | 5.0 | 24% | 47% | 0% | 6% |
| Care: repeat what worked | 68.4% | 11.0 | 0% | 96% | 52% | 3% |

The sweep over `q` (seed 2) gives Figure 3A. At `q` = 0.3, Accept identifies 29% of winds correctly and Verify 84%.

The random seeds are fixed, so a run with the default settings reproduces `results/results.json` exactly.

## Repository structure

```
zar-ritual-inference/
├── src/zar_ritual/
│   ├── model.py         the simulation: likelihood, Bayesian update, policies, summaries
│   ├── experiments.py   runs Table 4 and the q sweep, writes results.json
│   ├── figures.py       Figures 1 to 3
│   └── cli.py           command-line entry point (zar-ritual)
├── tests/test_model.py  checks that the likelihood is a probability distribution,
│                        that runs are reproducible, and the qualitative pattern
├── results/             results.json and figures from the default run
├── pyproject.toml
├── requirements.txt
├── CITATION.cff
└── LICENSE
```

Figure 1 (search and selection of records) and Figure 2 (three inferential problems) are diagrams. Their numbers and labels are fixed values taken from the review, not computed by the model.

## Tests

```bash
pip install -e ".[test]"
pytest
```

## Citation

If you use this code, please cite the paper above. Citation metadata is in `CITATION.cff`.

## License

MIT. See `LICENSE`.
