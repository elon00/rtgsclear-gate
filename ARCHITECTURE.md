# RTGSClear Gate — evidence-based architecture

- **Canonical ID:** QMOOSA-0960; **component role:** TESTS.
- **Implemented:** Python `rtgs_gate.py` offline exact-integer transfer validation with batch atomicity in memory, per-currency isolation, duplicate/replay ID rejection, and checked account limits; Rust `src/main.rs` bounded arithmetic smoke test.
- **Not implemented:** a persistent ledger, multi-process consensus/locking, RTGS finality, real-bank rails, identity/KYC, QuickNode, x402, Conway, Raven/REA, PQC, FIPS certification, or deployment.
- **CI:** `ci-cd-pipeline.yml` runs genuine Python and Rust tests; `codeql.yml` initializes and analyzes Python. Evidence is only valid for the specific tested SHA.
- **Threat model:** hostile input, duplicate transfer IDs, negative/overflow amounts, insufficient funds, partial batch failure. A process crash or concurrent writers can still cause duplicate processing without an external durable atomic store. The module must not be used as a production settlement engine.
- **Security gate:** fail closed; no production approval until authenticated authorization, durable serializable transaction journal, reconciliation, audit, independent review, and adversarial concurrency/crash tests are independently verified.
