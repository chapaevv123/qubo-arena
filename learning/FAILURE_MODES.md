# Failure modes observed

| Failure | Evidence | Fix or containment |
|---|---|---|
| Outbound QMS RPC blocked by Windows socket policy | Direct `requests.post` failed with WinError 10013. | `app.py` returns `QMS_RPC_UNAVAILABLE`; browser flow confirms mathematical work remains available. |
| Port 8765 already occupied | First Uvicorn start failed with address-in-use. | Documented and tested port 8767. |
| Parent Pulse pytest hook attempted write outside workspace | Initial pytest run showed 11 passes then failed in parent `conftest.py`. | Run `pytest --confcutdir . tests`; final run exits successfully. |
| QMS documentation reveals explorer QUBO evidence after initial research | [Official network guide](https://docs.qms.finance/for-developers/network-and-rpc). | Updated UI, evidence and application copy to identify Matrix Market downloads; parser remains a stated gap. |
| Switching Solver Arena problem left the previous matrix active | Expanded Playwright flow measured the old two-choice energy after selecting dense-12. | Added `problemSelect.onchange=selectProblem` in `static/app.js`; full browser flow then measured −57/−59 on dense-12. |
| Git metadata is read-only under the workspace policy | `git add` failed creating `.git/index.lock` with Permission denied. | Preserved all files, documented the blocker, and left publishing/commit for an environment with writable `.git`. |
| GitHub CLI identity is configured but its token is invalid | `gh auth status` returned login failure for `chapaevv123` on 28 October 2026. | No repository or URL was fabricated; `docs/PUBLIC_RELEASE.md` gives the owner's authentication and publication steps. |
| Live QMS RPC cannot be reached from the sandbox | Repeat request to `eth_chainId` returned WinError 10013 before any chain data. | Adapter displays `UNAVAILABLE` with UTC freshness and keeps local math online; `test_qms_success_and_failure_states` covers parsed success and mismatch failure. |
