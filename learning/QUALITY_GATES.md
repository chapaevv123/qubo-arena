# Reusable quality gates

1. **Source evidence:** every protocol field needs an official URL and the implemented behavior in `docs/PROTOCOL_EVIDENCE.md`.
2. **Math contract:** objective convention, input limits, exact limit and precision policy must be explicit in `engine.py` and `docs/ARCHITECTURE.md`.
3. **Independent check:** `tests/test_engine.py` must compare exact solutions to enumeration, reject malformed inputs and detect receipt tampering.
4. **Browser journey:** `tests/browser_acceptance.mjs` must traverse the full core path from a fresh context, test export and a failure case, check console and mobile width.
5. **Integration honesty:** `app.py:qms_status` must only show `LIVE QMS DATA` after chain ID verification and a real block; outage must resolve to a diagnostic state.
6. **Submission gate:** do not claim a public demo or QMS proof verification until external URL and live proof evidence are tested.
7. **Public release gate:** verify Git write access and GitHub authentication, deploy from a committed repository, then run browser acceptance against the actual public URL. `docs/PUBLIC_RELEASE.md` records the current blockers.
