"""Confusion-matrix metrics and question-level bootstrap."""
import numpy as np

def cm(y, p, k):
    return np.bincount(np.asarray(y, dtype=int) * k + np.asarray(p, dtype=int), minlength=k * k).reshape(k, k)

def macro_f1(C):
    tp = np.diag(C).astype(float)
    den = C.sum(0) + C.sum(1)
    return float(np.mean(np.where(den > 0, 2 * tp / np.maximum(den, 1), 0.0)))

def qwk(C):
    n = C.sum()
    if n == 0:
        return float("nan")
    k = C.shape[0]
    i, j = np.indices((k, k))
    W = (i - j) ** 2 / (k - 1) ** 2
    E = np.outer(C.sum(1), C.sum(0)) / n
    d = (W * E).sum()
    return float(1 - (W * C).sum() / d) if d > 0 else 0.0

def boot(qids, f, B=2000, seed=42):
    """Resample whole questions with replacement. f(idx) returns a vector of statistics."""
    uq, inv = np.unique(np.asarray(qids), return_inverse=True)
    members = [np.where(inv == i)[0] for i in range(len(uq))]
    rng = np.random.RandomState(seed)
    out = []
    for _ in range(B):
        pick = rng.randint(0, len(uq), len(uq))
        out.append(f(np.concatenate([members[i] for i in pick])))
    return np.array(out, dtype=float), len(uq)

def ci(a, lo=2.5, hi=97.5):
    return np.nanpercentile(a, [lo, hi], axis=0)
