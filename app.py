"""QUBO Arena local API and read-only QMS Testnet adapter."""
import os
import time
from datetime import datetime, timezone
from pathlib import Path
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from engine import InputError, energy, receipt, solve, validate_problem, validate_bits, verify_receipt

ROOT = Path(__file__).parent
RPC = "https://rpc.testnet.qms.finance"
EXPECTED_CHAIN = 19480
app = FastAPI(title="QUBO Arena", version="1.0.0")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
_cache = {"at": 0, "data": None}


def example_problem(name, q, description, offset=0):
    return {"id": name.lower().replace(" ", "-"), "name": name, "description": description, "q": q, "offset": offset, "provenance": "REFERENCE FIXTURE"}


PROBLEMS = [
    example_problem("Two choices", [[-2, 3], [0, -1]], "Pick either valuable item. A combined selection carries a penalty."),
    example_problem("Budgeted selection", [[-3, 4, 2, 1], [0, -5, 3, 2], [0, 0, -2, 4], [0, 0, 0, -4]], "Four projects have individual value and pairwise conflicts."),
    example_problem("Graph independent set", [[-1, 3, 0, 0, 3, 0], [0, -1, 3, 0, 0, 0], [0, 0, -1, 3, 0, 0], [0, 0, 0, -1, 3, 0], [0, 0, 0, 0, -1, 3], [0, 0, 0, 0, 0, -1]], "Choose as many vertices as possible without selecting neighbors; a selected edge costs 3."),
    example_problem("Dense 12-variable", [[(-2 if i == j else ((i * 7 + j * 11) % 7 - 3) if j > i else 0) for j in range(12)] for i in range(12)], "A seeded dense interaction matrix for harder, reproducible comparisons."),
]


@app.exception_handler(InputError)
async def input_error(_request: Request, exc: InputError):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code=422, content={"code": "INVALID_INPUT", "message": str(exc)})


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "qubo-arena", "scope": "local-math"}


@app.get("/api/problems")
def problems():
    return {"problems": PROBLEMS}


@app.post("/api/solve")
async def api_solve(body: dict):
    return solve(body.get("problem"), body.get("method"), body.get("seed", 7))


@app.post("/api/verify")
async def api_verify(body: dict):
    p = validate_problem(body.get("problem"))
    bits = validate_bits(body.get("assignment"), len(p["q"]))
    score = energy(p, bits)
    return {"valid": True, "energy": score, "receipt": receipt(p, bits, score), "provenance": "LOCAL COMPUTATION"}


@app.post("/api/receipt/verify")
async def api_verify_receipt(body: dict):
    return verify_receipt(body)


def rpc(method, params):
    error = None
    for _ in range(2):
        try:
            response = requests.post(RPC, json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params}, timeout=3)
            response.raise_for_status()
            data = response.json()
            if "error" in data or "result" not in data:
                raise ValueError(str(data.get("error", "Missing result")))
            return data["result"]
        except (requests.RequestException, ValueError) as exc:
            error = str(exc)
    raise RuntimeError(error)


@app.get("/api/qms/status")
def qms_status():
    now = time.time()
    if _cache["data"] and now - _cache["at"] < 15:
        return {**_cache["data"], "cached": True}
    checked = datetime.now(timezone.utc).isoformat()
    try:
        chain = int(rpc("eth_chainId", []), 16)
        if chain != EXPECTED_CHAIN:
            raise RuntimeError(f"RPC reported chain ID {chain}; expected {EXPECTED_CHAIN}")
        observed_head = int(rpc("eth_blockNumber", []), 16)
        block = rpc("eth_getBlockByNumber", ["latest", False])
        if not isinstance(block, dict) or not block.get("hash"):
            raise RuntimeError("RPC returned no latest block")
        data = {"state": "LIVE QMS DATA", "chain_id": chain, "observed_head": observed_head, "block_number": int(block["number"], 16), "block_hash": block["hash"], "block_timestamp": datetime.fromtimestamp(int(block["timestamp"], 16), timezone.utc).isoformat(), "transaction_count": len(block.get("transactions", [])), "checked_at": checked, "rpc": RPC, "explorer": "https://testnet.qmsscan.io", "block_url": "https://testnet.qmsscan.io/block/" + block["hash"], "cached": False, "proof_data": "UNVERIFIED", "proof_note": "Official explorer displays a QUBO hash, winning solution and Matrix Market download per block. Arena does not yet parse or independently verify that format."}
    except Exception as exc:
        data = {"state": "UNAVAILABLE", "code": "QMS_RPC_UNAVAILABLE", "message": str(exc)[:240], "checked_at": checked, "rpc": RPC, "proof_data": "UNAVAILABLE", "proof_note": "Official explorer has QUBO block pages; no block could be retrieved through RPC in this request."}
    _cache.update(at=now, data=data)
    return data
