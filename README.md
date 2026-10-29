# RTGSClear Gate — offline accounting invariants

This repository currently provides a **bounded, offline diagnostic** for integer-denominated account transfers. It does **not** implement an RTGS payment network, real settlement, durable replay journal, distributed concurrency control, identity/authentication, cryptographic key management, QuickNode RPC, x402, or a FIPS-validated module.

## Run without network access

```bash
python -m unittest discover -s tests -p 'test_*.py' -v
python tests/reality_check_harness.py
cargo fmt --all -- --check
cargo test --offline
cargo run --offline
```

`rtgs_gate.apply_batch` returns new account balances and replay IDs only after validating an entire batch. The caller is responsible for **atomic, durable persistence** of both values, concurrency control, legal settlement finality, and all operational controls. No such caller is included here. The Rust binary is an independent integer-arithmetic smoke test, not an RTGS engine.

## Acceptance status

- Python regression tests and Rust unit tests: run in CI; check the specific commit's GitHub Actions results.
- CodeQL: runs separately; a passing workflow is **not** a security audit.
- Security approval: **NOT GRANTED**.
- Deployment readiness: **NOT GRANTED**.
- Production certification/FIPS validation: **NONE**.

This branch replaces previously fabricated `100/100` and FIPS/RPC status messages with verifiable, narrowly scoped checks. See `SECURITY.md` for the project security policy; no claim in legacy architecture documents is evidence of implementation.
