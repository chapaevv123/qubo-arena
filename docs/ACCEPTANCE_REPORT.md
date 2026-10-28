# Acceptance report — 28 October 2026

## Verdict

**NOT READY for an externally verifiable QMS Builder submission.** The complete local mathematical user journey passes. Live QMS data could not be observed because this environment blocks outbound sockets (Windows error 10013); the UI correctly reports `UNAVAILABLE`. The workspace policy also makes `.git` read-only, so `git add`/`git commit` failed at `.git/index.lock`. A published GitHub/demo URL is absent. The owner can demonstrate the local product immediately.

## Evidence

- `python -m pytest -q --confcutdir . tests`: 12 passed. The tests cover asymmetric coefficients, exact optima for every fixture, deterministic solver outputs, receipt hashing/tamper detection, malformed input, API journey, and mocked QMS success/failure states.
- `node tests/browser_acceptance.mjs`: passed in headless Microsoft Edge against the running server at `127.0.0.1:8767`. It used a fresh context, traversed overview → two solver runs → export → fixture and custom-matrix verification → receipt export/check/tamper → benchmark selection → changed problem and measured random/greedy comparison (−57/−59) → invalid seed → QMS status → methodology → mobile overview. Zero page exceptions and no horizontal overflow at 390 px.
- Repeated on 28 October 2026 after adding `eth_blockNumber` and `/health`: 12 tests passed, full Edge acceptance passed, `/health` returned HTTP 200, `/api/qms/status` returned `UNAVAILABLE` with WinError 10013 and a UTC timestamp.
- [Desktop overview](screenshots/overview.png), [arena](screenshots/arena.png), [mobile](screenshots/mobile.png) are real browser captures.
- QMS status resolved to `UNAVAILABLE` with `QMS_RPC_UNAVAILABLE`; this is an expected safe failure in the current sandbox, not a successful live-chain test.

## Remaining gaps

- QMS RPC success branch and real latest-block contents need acceptance from a network-enabled environment.
- Explorer `.mtx.gz` data is linked but not parsed or independently verified.
- No GitHub repository or deployment has been published.
- No commit is recorded in the initialized repository because `.git/index.lock` creation is denied by workspace permissions. All source files remain untracked and intact.
- `gh auth status` reports the configured `chapaevv123` token is invalid. [Public release handoff](PUBLIC_RELEASE.md) contains the exact owner actions and free Render configuration.
- The Solver Arena currently uses bundled problems; the Verifier accepts custom matrices as JSON.
