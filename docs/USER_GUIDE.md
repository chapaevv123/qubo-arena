# User guide

1. Open `http://127.0.0.1:8767` and choose **Start solving**.
2. Select a reference problem. The matrix and plain-language explanation are shown.
3. Run **Seeded random** with seed 7. Change to **Exact exhaustive** and run again. Lower energy is better. A star marks certified optimal results.
4. Select a row, choose **Verify selected result**, and inspect the independently recalculated energy and SHA-256 receipt.
5. Export the receipt. In **Receipts**, paste its JSON and choose **Check receipt**. Changing the energy or vector makes it invalid.
6. Export a full run from the Arena for reproducibility. The JSON contains the problem, method, seed, assignment, score and receipt.
7. Open **QMS Devnet**. `LIVE QMS DATA` requires a successful chain ID and latest block read; `UNAVAILABLE` includes a diagnostic. The local solver works in either state.

The verifier also accepts a custom JSON problem such as `{"q":[[-2,3],[0,-1]],"offset":0}`. Each matrix entry is counted once, including both off-diagonal entries of an asymmetric matrix. Only exact search certifies global optimality, and only up to 16 variables.
