# Architecture

Browser → FastAPI (`app.py`) → deterministic engine (`engine.py`). The browser displays results and exports JSON; all scoring and hashing are server-side. The QMS adapter is a separate read-only path to the official RPC. Failure there does not affect mathematical endpoints.

## API

`GET /api/problems` returns reference fixtures. `POST /api/solve` accepts `{problem,method,seed}`. `POST /api/verify` accepts `{problem,assignment}`. `POST /api/receipt/verify` checks canonical hash and recomputed energy. `GET /api/qms/status` requests `eth_chainId`, `eth_blockNumber` and the latest block, then returns `LIVE QMS DATA` or `UNAVAILABLE` with source, timestamp and diagnostic. `GET /health` verifies only the local service, without depending on QMS RPC.

## Limits and precision

Square matrices contain 1–32 variables; finite numeric coefficients and offset are bounded to ±1e6. Boolean values are rejected as coefficients and bits. Exact search is limited to 16 variables (65,536 assignments). Seeds are unsigned 32-bit integers. The objective uses Python binary floating point and `math.fsum`; results should not be represented as decimal-exact proofs for arbitrary fractional inputs. Receipt canonicalization is Python `json.dumps(sort_keys=True,separators=(',', ':'),ensure_ascii=False,allow_nan=False)` encoded as UTF-8. Version `qubo-arena-receipt-v1` binds the normalized problem, assignment and energy.

## Security and reliability

The RPC destination is fixed server-side; users cannot supply arbitrary URLs. Requests time out after 3 seconds and retry once. Status is cached 15 seconds to limit shared-RPC pressure. No credentials, writes or transactions are used. UI inserts external data with HTML escaping and opens explorer links with `rel=noopener`. API input validation returns structured `INVALID_INPUT` 422 errors. QMS failures return `QMS_RPC_UNAVAILABLE` while local math remains usable.

## Provenance vocabulary

`REFERENCE FIXTURE`: bundled problem data. `LOCAL COMPUTATION`: solver result or receipt computed here. `LIVE QMS DATA`: chain ID verified against 19480 and latest block retrieved. `UNAVAILABLE`: RPC request failed. `UNVERIFIED`: explorer PoUW data exists but Arena has not independently validated it.
