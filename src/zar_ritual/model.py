"""Minimal model of wind identification in Hormozgan zar rituals.

The hidden state is the wind (one of K) that afflicts a person. Each song
played in a session addresses one wind. After each song the specialist may
observe three things:

    r   a response (trance or dance), or none
    c   the name the wind claims when it speaks (only if r = 1)
    v   whether the coded signs shown fit the claimed name (only if r = 1)

Four ritual policies are compared:

    accept      take the first name spoken
    verify      keep the fixed song order, update a probability for each wind
                after every song, stop when one wind reaches the threshold
    epistemic   use the same probabilities, but choose each next song for its
                expected information gain, within the rule that mashayekh
                songs end the zar part of a night
    care        replay the first song that drew a response and take the
                first name spoken

The parameters are illustrative. The model is not fitted to any data; it
shows which traces each policy would leave in a session record.

See Section 6 and Box 1 of Baselizadeh & Gharasou, "Whose inference? A
critical review of predictive-processing accounts of spirit possession, with
zar rituals in Hormozgan as a test case".
"""
from __future__ import annotations

from typing import Optional

import numpy as np

#: Number of winds.
K = 6

#: Class of each wind: 0 = non-Muslim winds addressed by zar songs,
#: 1 = mashayekh winds, 2 = nuban wind.
GROUP = np.array([0, 0, 0, 1, 1, 2])

#: Fixed song order for each night: zar songs, then mashayekh songs;
#: the third night plays the nuban song.
NIGHTS = [[0, 1, 2, 3, 4], [0, 1, 2, 3, 4], [5]]

#: Prior probability of each wind.
PRIOR = np.array([0.25, 0.20, 0.15, 0.15, 0.15, 0.10])

#: Default parameters.
#:   p_hit    P(response | the song of the true wind is played)
#:   p_fa     P(response | another song is played)
#:   q        P(a responding wind gives its true name)
#:   s_true   P(coded signs fit the claimed name | the name is true)
#:   s_false  P(coded signs fit the claimed name | the name is false)
#:   stop     posterior threshold at which verify and epistemic stop
DEFAULT = dict(p_hit=0.7, p_fa=0.15, q=0.7, s_true=0.85, s_false=0.2, stop=0.9)

POLICIES = ("accept", "verify", "epistemic", "care")


def likelihood(w: int, s: int, r: int, c: Optional[int], v: Optional[int], P: dict) -> float:
    """Return P(r, c, v | true wind w, song s)."""
    pr = P["p_hit"] if s == w else P["p_fa"]
    if r == 0:
        return 1 - pr
    if c == w:  # the wind names itself correctly
        pc = P["q"]
    elif s != w and c == s:  # a false name echoes the song being played
        pc = 1 - P["q"]
    elif s == w:  # a false name, spread over the other winds
        pc = (1 - P["q"]) / (K - 1)
    else:
        pc = 0.0
    pv = P["s_true"] if c == w else P["s_false"]
    return pr * pc * (pv if v else 1 - pv)


def observe(w: int, s: int, P: dict, rng: np.random.Generator):
    """Sample one observation (r, c, v) for true wind w and song s."""
    if rng.random() >= (P["p_hit"] if s == w else P["p_fa"]):
        return 0, None, None
    if rng.random() < P["q"]:
        c = w
    else:
        c = s if s != w else rng.choice([k for k in range(K) if k != w])
    v = int(rng.random() < (P["s_true"] if c == w else P["s_false"]))
    return 1, c, v


def update(post: np.ndarray, s: int, r: int, c, v, P: dict) -> np.ndarray:
    """Bayesian update of the probability of each wind after one song."""
    post = post * np.array([likelihood(w, s, r, c, v, P) for w in range(K)])
    return post / post.sum()


def entropy(p: np.ndarray) -> float:
    """Shannon entropy in bits."""
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def expected_information_gain(post: np.ndarray, s: int, P: dict) -> float:
    """Expected reduction in uncertainty about the wind from playing song s."""
    outcomes = [(0, None, None)] + [(1, c, v) for c in range(K) for v in (0, 1)]
    h, gain = entropy(post), 0.0
    for r, c, v in outcomes:
        pw = post * np.array([likelihood(w, s, r, c, v, P) for w in range(K)])
        po = pw.sum()
        if po > 0:
            gain += po * (h - entropy(pw / po))
    return gain


def run_session(policy: str, w: int, P: dict, rng: np.random.Generator) -> dict:
    """Simulate the sessions held for one person whose true wind is w.

    Returns a dict with the final identification (``answer``, or None if no
    wind is identified), the songs played as (night, song) pairs, and the
    names claimed in order.
    """
    if policy not in POLICIES:
        raise ValueError(f"unknown policy {policy!r}; choose from {POLICIES}")
    post, played, claims, stuck = PRIOR.copy(), [], [], None
    for ni, night in enumerate(NIGHTS):
        left = list(night)
        while left:
            if policy == "epistemic":
                # free choice of the most informative song,
                # keeping the zar-before-mashayekh rule
                s = max(left, key=lambda k: expected_information_gain(post, k, P))
                left = [k for k in left if k != s and GROUP[k] >= GROUP[s]]
            elif policy == "care" and stuck is not None:
                s = stuck  # keep replaying the song that worked
                left = left[1:]
            else:
                s = left.pop(0)  # fixed ritual order
            played.append((ni, s))
            r, c, v = observe(w, s, P, rng)
            post = update(post, s, r, c, v, P)
            if r:
                claims.append(c)
                if policy == "accept":
                    return dict(answer=c, played=played, claims=claims)
                if policy == "care":
                    stuck = stuck if stuck is not None else s
            if policy in ("verify", "epistemic") and post.max() >= P["stop"]:
                return dict(answer=int(post.argmax()), played=played, claims=claims)
    if policy == "care" and claims:
        answer = claims[0]
    else:
        answer = int(post.argmax()) if post.max() >= 0.5 else None
    return dict(answer=answer, played=played, claims=claims)


def summarise(policy: str, P: dict = DEFAULT, n: int = 10000, seed: int = 1) -> dict:
    """Run n simulated persons under one policy and return summary rates.

    accuracy         share of persons whose wind is identified correctly
    songs            mean number of songs played
    revised          share of persons whose first spoken name was later replaced
    order_deviation  share of persons whose song sequence departs from the fixed order
    repeat_share     share of all songs played that repeat an earlier (night, song)
    unresolved       share of persons with no identification
    """
    rng = np.random.default_rng(seed)
    canon = [s for night in NIGHTS for s in night]
    acc = songs = revised = deviates = repeats = plays = unresolved = 0
    for _ in range(n):
        w = int(rng.choice(K, p=PRIOR))
        out = run_session(policy, w, P, rng)
        acc += out["answer"] == w
        unresolved += out["answer"] is None
        seq = [s for _, s in out["played"]]
        songs += len(seq)
        revised += bool(out["claims"]) and out["answer"] is not None and out["answer"] != out["claims"][0]
        deviates += seq != canon[: len(seq)]
        repeats += len(out["played"]) - len(set(out["played"]))
        plays += len(out["played"])
    return dict(
        policy=policy,
        accuracy=acc / n,
        songs=songs / n,
        revised=revised / n,
        order_deviation=deviates / n,
        repeat_share=repeats / max(plays, 1),
        unresolved=unresolved / n,
    )
