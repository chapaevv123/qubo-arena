# QMS protocol evidence — 28 October 2026

| Claim | Official evidence | Arena behavior |
|---|---|---|
| Testnet chain ID 19480, HTTPS RPC, explorer | [Network and RPC](https://docs.qms.finance/for-developers/network-and-rpc) | `app.py` pins endpoint and rejects a mismatched chain ID. |
| Public `eth`, `net`, `web3` RPC; rate limit 50 req/s/client | [Network and RPC](https://docs.qms.finance/for-developers/network-and-rpc) | Read-only `eth_chainId` and `eth_getBlockByNumber`, 15-second cache. |
| v0.1 uses randomly generated PoUW problems; explorer shows solved problem and solution | [Releases](https://docs.qms.finance/overview/releases) | QMS panel links to latest block when RPC works. |
| Block page shows QUBO instance hash, winning solution/objective, `.mtx.gz` download | [Network and RPC](https://docs.qms.finance/for-developers/network-and-rpc) | Marked `UNVERIFIED`; no inference that a local receipt is a chain proof. |
| Client-submitted QUBO marketplace belongs to v2 roadmap | [Releases](https://docs.qms.finance/overview/releases) | No marketplace submission or reward claim. |
| Early testnet may reset | [Official testnet notice](https://qms.finance/news/welcome-to-qms-testnet) | No persistent on-chain assumption. |
| v0.1 miners are operated by QMS and solve randomly generated problems; client marketplace follows later | [Official AMA recap](https://qms.finance/news/qms-ama-recap-the-vision-the-testnet-the-road-ahead) | No claim of participating in mining or marketplace settlement. |

The public RPC was attempted again on 28 October 2026 and Windows returned socket permission error 10013. Thus the adapter's live-success branch has not been observed against the real endpoint here. The adapter requests `eth_chainId`, `eth_blockNumber`, and `eth_getBlockByNumber("latest", false)`, validates the chain ID, and timestamps the result. The explorer API advertises standard Blockscout block endpoints at [QMSScan API docs](https://testnet.qmsscan.io/api-docs), but a QMS-specific proof schema was not confirmed in that API. The official Matrix Market download is visible via block pages. Parsing it and verifying consensus objectives require a documented mapping and live sample, so Arena does not present that as completed.

No official QMS GitHub implementation or contract ABI was confirmed for the PoUW verification path during this research. A direct Builder application page fetch was unavailable; application copy must be reviewed against the form by the owner.
