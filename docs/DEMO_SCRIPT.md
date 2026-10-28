# 2–3 minute demo script

**0:00–0:25** Open the overview. “QUBO Arena makes optimization results inspectable. A wallet is unnecessary for its core workflow.” Show the three steps and the QMS boundary.

**0:25–1:15** Enter Solver arena. Select *Dense 12-variable* with seed 7. Explain `E(x)=xᵀQx+c` and run seeded random, then greedy. In the tested build, their actual scores were −57 and −59. Explain that heuristic improvements are observed, not guaranteed. Run exact if time permits and point out its certified status. Export the run JSON.

**1:15–1:55** Select the exact row and verify it. Show the recomputed energy and SHA-256. Export its receipt; paste it into Receipts and see `VALID`. Alter the energy and show `INVALID`.

**1:55–2:30** Open Benchmarks, switch to Graph independent set, and explain the selected-vertex/edge-penalty model. Open QMS Devnet. If RPC is reachable, show verified chain ID, block, timestamp and explorer link. If unavailable, show the explicit error and point out that local solving still works.

**2:30–2:45** Open Methodology. Explain local receipts versus on-chain proof evidence and the planned QMS explorer-format integration.
