import copy
import itertools
import pytest
from fastapi.testclient import TestClient
from app import app, PROBLEMS
import app as api_module
from engine import InputError, energy, solve, receipt, verify_receipt

client = TestClient(app)


def test_asymmetric_convention():
    p = {"q": [[-2, 3], [4, -1]], "offset": 0.5}
    assert energy(p, [1, 1]) == 4.5
    assert energy(p, [1, 0]) == -1.5


@pytest.mark.parametrize("p", PROBLEMS)
def test_exact_is_minimum(p):
    result = solve(p, "exact", 7)
    assert result["energy"] == min(energy(p, list(x)) for x in itertools.product((0, 1), repeat=len(p["q"])))
    assert result["status"] == "certified optimal"
    assert verify_receipt(result["receipt"])["valid"]


@pytest.mark.parametrize("method", ["random", "greedy", "anneal", "exact"])
def test_reproducible_and_correct(method):
    p = PROBLEMS[1]
    a, b = solve(p, method, 101), solve(p, method, 101)
    assert a["assignment"] == b["assignment"]
    assert a["energy"] == b["energy"] == energy(p, a["assignment"])
    assert a["receipt"]["sha256"] == b["receipt"]["sha256"]


def test_reject_malformed_and_tampered():
    with pytest.raises(InputError):
        energy({"q": [[float("nan")]]}, [1])
    with pytest.raises(InputError):
        energy({"q": [[1]]}, [True])
    with pytest.raises(InputError):
        solve({"q": [[0]*21 for _ in range(21)]}, "exact")
    r = receipt(PROBLEMS[0], [1, 0], -2)
    r["energy"] = 99
    assert not verify_receipt(r)["valid"]


def test_api_journey():
    p = client.get("/api/problems").json()["problems"][0]
    run = client.post("/api/solve", json={"problem": p, "method": "exact", "seed": 4}).json()
    check = client.post("/api/verify", json={"problem": p, "assignment": run["assignment"]}).json()
    assert check["energy"] == run["energy"]
    assert client.post("/api/receipt/verify", json=check["receipt"]).json()["valid"]
    assert client.post("/api/verify", json={"problem": p, "assignment": [2, 1]}).status_code == 422


def test_qms_success_and_failure_states(monkeypatch):
    api_module._cache.update(at=0, data=None)
    block = {"number": "0xa", "hash": "0x" + "a" * 64, "timestamp": "0x1", "transactions": ["0xabc"]}
    monkeypatch.setattr(api_module, "rpc", lambda method, params: "0x4c18" if method == "eth_chainId" else "0xa" if method == "eth_blockNumber" else block)
    good = client.get("/api/qms/status").json()
    assert good["state"] == "LIVE QMS DATA" and good["block_number"] == 10 and good["observed_head"] == 10
    assert good["block_url"].endswith(block["hash"])
    api_module._cache.update(at=0, data=None)
    monkeypatch.setattr(api_module, "rpc", lambda method, params: "0x1")
    bad = client.get("/api/qms/status").json()
    assert bad["state"] == "UNAVAILABLE" and bad["code"] == "QMS_RPC_UNAVAILABLE"
