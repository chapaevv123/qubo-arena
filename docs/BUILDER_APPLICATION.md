# QMS Builder Program application draft

**Project:** QUBO Arena  
**Category:** Developer tooling / optimization verification  
**Repository:** local project; GitHub URL to be added after owner publication  
**Demo:** local Windows application; no public deployment claimed

QUBO Arena turns the optimization concept behind QMS proof of useful work into an inspectable developer workbench. A user can select a reference QUBO, run four real deterministic solver methods, compare measured energies, recompute a submitted solution independently, and export a canonical SHA-256 receipt. It needs no wallet or paid service.

The project already includes a responsive product interface, bounded exact search, reproducible fixtures, a read-only QMS Testnet RPC adapter, 12 passing mathematical/API tests, and a real Edge browser acceptance flow covering export, tamper detection, custom matrix verification, errors and mobile layout. On the dense 12-variable fixture with seed 7, random sampling scored −57 and greedy local search scored −59. The adapter checks chain ID 19480 and requests `eth_blockNumber` plus the latest block before displaying network data. It handles outages without disabling the core product. Official QMS documentation says block pages expose a QUBO hash, winning solution/objective and Matrix Market instance download; Arena links to block pages but does not yet independently validate those proof artifacts. A live RPC response remains unobserved from this sandbox due to Windows socket policy.

**Value to QMS:** A clear verification and benchmarking experience can help developers understand optimization quality, reproduce solver claims, and prepare for richer QMS PoUW integrations. The current product is deliberately honest about the boundary between local calculations and consensus evidence.

**Next with builder access:** Obtain the documented QMS-specific proof schema and sample `.mtx.gz` files, implement safe Matrix Market parsing and independent objective checks, add provenance-preserving block import, then validate against live explorer examples. If a supported protocol API emerges, integrate it without assuming marketplace features exist in v0.1.

**Why this team merits access:** The submitted code demonstrates working verification, conservative protocol claims, browser-tested UX, and a concrete path from reference problems to QMS block evidence. No token rewards, grants, whitelist status, or approval are claimed.

The owner should review the live application form at <https://qms.finance/builders-program/apply>, add team/contact details and actual published repository/demo URLs, and submit personally. The form could not be inspected from the build environment. [Release handoff](PUBLIC_RELEASE.md) records the steps to obtain those URLs.
