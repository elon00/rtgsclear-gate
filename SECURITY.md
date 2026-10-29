# Security scope — RTGSClear Gate

This repository is **not** a production RTGS system. It contains bounded offline accounting invariant checks. There is no persistent journal, multi-process locking, authenticated participant identity, banking settlement integration, or independently certified cryptographic implementation.

## Implemented safeguards
- Exact integer minor-unit accounting with range and overflow checks.
- Reject duplicate/replayed transfer IDs in the caller-supplied in-memory set.
- All-or-nothing batch validation in a new in-memory state; caller inputs remain unchanged on failure.
- Adversarial unit tests and static analysis workflows.

## Known unresolved risks / release blockers
- No durable, serializable, atomic persistence of balances and replay IDs.
- No crash recovery, multi-writer concurrency protection, or multi-host coordination.
- No authenticated authorization, finality, reconciliation, audit trail, key management, or banking rail.
- No FIPS 203/204/205 implementation or validation; no QuickNode, x402, or live-chain integration.

**Security approval: NOT GRANTED. Deployment readiness: NOT GRANTED.** No claim of 100/100, FIPS validation, or a bug bounty is authorized by this document.

## Reporting
Use the repository's GitHub Security tab and private vulnerability reporting if available. Do not post exploit details or secrets in public issues. No external security mailbox or reward program has been independently verified.
