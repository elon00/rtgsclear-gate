# RTGSClear Gate — architecture roadmap (not production evidence)

## Current code boundary
- `rtgs_gate.py`: in-memory, offline exact-integer accounting invariant checker.
- `tests/test_rtgs_gate.py`: adversarial Python regressions for replay IDs, amount bounds, overflow, insufficient funds, and batch atomicity.
- `src/main.rs`: independent Rust checked-arithmetic smoke test.
- GitHub Actions: Python/Rust tests and separate Python CodeQL analysis.

## Future architecture (NOT implemented)
1. Authenticated participants and least-privilege authorization.
2. Durable, transactional balance/replay journal with serializable multi-worker locking.
3. Idempotent crash/restart recovery and tamper-evident audit logs.
4. Multi-currency settlement, reconciliation, external bank integration and finality.
5. Independent cryptographic and security review, disaster recovery, operational controls.
6. Optional QuickNode, x402, PQC, and Conway/Raven research integrations **only if justified and verified**.

## Acceptance gates
A real settlement system must prove cross-process and cross-host exactly-once processing, concurrency isolation, crash safety, legal settlement finality, and security review. None of these is established by this offline checker.

**No FIPS certification, no production readiness, no 100/100 score.** See `SECURITY.md` and the exact-SHA CI results.
