"""Deterministic QUBO calculations. Energy = offset + sum(Q[i][j]*x[i]*x[j])."""
import hashlib
import json
import math
import random
import time

MAX_N = 32
EXACT_N = 16


class InputError(ValueError):
    pass


def validate_problem(problem):
    if not isinstance(problem, dict):
        raise InputError("Problem must be a JSON object")
    q = problem.get("q")
    if not isinstance(q, list) or not 1 <= len(q) <= MAX_N:
        raise InputError(f"Q must be a square matrix with 1–{MAX_N} rows")
    n = len(q)
    if any(not isinstance(row, list) or len(row) != n for row in q):
        raise InputError("Q must be square")
    for row in q:
        for value in row:
            if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or abs(value) > 1e6:
                raise InputError("Q coefficients must be finite numbers within ±1,000,000")
    offset = problem.get("offset", 0)
    if isinstance(offset, bool) or not isinstance(offset, (int, float)) or not math.isfinite(offset) or abs(offset) > 1e6:
        raise InputError("Offset must be a finite number within ±1,000,000")
    return {"q": q, "offset": offset}


def validate_bits(bits, n):
    if not isinstance(bits, list) or len(bits) != n or any(type(v) is not int or v not in (0, 1) for v in bits):
        raise InputError(f"Assignment must contain exactly {n} binary integers")
    return bits


def energy(problem, bits):
    p = validate_problem(problem)
    x = validate_bits(bits, len(p["q"]))
    return math.fsum([p["offset"]] + [p["q"][i][j] * x[i] * x[j] for i in range(len(x)) for j in range(len(x))])


def receipt(problem, bits, score):
    payload = {"schema": "qubo-arena-receipt-v1", "problem": validate_problem(problem), "assignment": validate_bits(bits, len(problem["q"])), "energy": score}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return {**payload, "sha256": hashlib.sha256(canonical.encode()).hexdigest(), "provenance": "LOCAL COMPUTATION"}


def verify_receipt(data):
    if not isinstance(data, dict) or data.get("schema") != "qubo-arena-receipt-v1":
        raise InputError("Unsupported receipt schema")
    score = energy(data.get("problem"), data.get("assignment"))
    expected = receipt(data["problem"], data["assignment"], score)
    return {"valid": data.get("sha256") == expected["sha256"] and data.get("energy") == score, "computed_energy": score, "computed_sha256": expected["sha256"]}


def solve(problem, method, seed=7):
    p = validate_problem(problem)
    n = len(p["q"])
    if type(seed) is not int or not 0 <= seed <= 2**32-1:
        raise InputError("Seed must be an integer from 0 to 4,294,967,295")
    if method not in ("random", "greedy", "anneal", "exact"):
        raise InputError("Unknown solver")
    if method == "exact" and n > EXACT_N:
        raise InputError(f"Exact solver is limited to {EXACT_N} variables")
    rng = random.Random(seed)
    started = time.perf_counter()
    evaluated = 0
    def score(x):
        nonlocal evaluated
        evaluated += 1
        return energy(p, x)
    if method == "exact":
        best, best_e = None, math.inf
        for mask in range(1 << n):
            x = [(mask >> i) & 1 for i in range(n)]
            e = score(x)
            if e < best_e:
                best, best_e = x, e
    elif method == "random":
        best, best_e = None, math.inf
        for _ in range(max(64, n * 16)):
            x = [rng.randrange(2) for _ in range(n)]
            e = score(x)
            if e < best_e:
                best, best_e = x, e
    elif method == "greedy":
        best = [rng.randrange(2) for _ in range(n)]
        best_e = score(best)
        for _ in range(8):
            x = [rng.randrange(2) for _ in range(n)]
            e = score(x)
            while True:
                candidates = []
                for i in range(n):
                    y = x.copy(); y[i] ^= 1
                    candidates.append((score(y), i))
                candidate_e, i = min(candidates)
                if candidate_e >= e:
                    break
                x[i] ^= 1; e = candidate_e
            if e < best_e:
                best, best_e = x.copy(), e
    else:
        best = [rng.randrange(2) for _ in range(n)]
        best_e = score(best)
        x, e = best.copy(), best_e
        steps = max(800, n * 160)
        for t in range(steps):
            temperature = 4.0 * (0.02 / 4.0) ** (t / max(1, steps - 1))
            i = rng.randrange(n)
            y = x.copy(); y[i] ^= 1
            ey = score(y)
            if ey <= e or rng.random() < math.exp((e - ey) / temperature):
                x, e = y, ey
                if e < best_e:
                    best, best_e = x.copy(), e
    return {"method": method, "seed": seed, "assignment": best, "energy": best_e, "runtime_ms": round((time.perf_counter()-started)*1000, 3), "evaluations": evaluated, "status": "certified optimal" if method == "exact" else "best known in this run", "receipt": receipt(p, best, best_e), "provenance": "LOCAL COMPUTATION"}
