# Pulse builder lessons for later review

- **Make provenance visible at the point of use.** `static/index.html` and `app.py` label reference fixtures, local computation, live data, unavailable data and unverified explorer proofs. The browser flow exercises the unavailable state.
- **Pin mathematical conventions before writing solvers.** `engine.energy` evaluates the full supplied matrix exactly once per ordered pair. `test_asymmetric_convention` catches accidental symmetrization.
- **Treat receipts as consistency evidence.** `engine.receipt` hashes canonical inputs and score; `verify_receipt` recalculates. The browser test alters energy and observes `INVALID`.
- **Keep network adapters isolated.** `/api/qms/status` has bounded retry/cache and cannot block `/api/solve`; the browser flow succeeds while RPC is unavailable.
- **Accept only demonstrated claims.** `docs/PROTOCOL_EVIDENCE.md` distinguishes official v0.1 features from v2 plans and records the socket failure.
