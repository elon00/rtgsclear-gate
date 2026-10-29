# RTGSClear Gate — concept and implementation boundaries

**Status: research / offline diagnostic; not a deployed payment network.**

## Purpose
Explore accounting invariants relevant to a possible real-time gross settlement (RTGS) architecture, without asserting that funds can be moved or finality achieved.

## What is implemented
The Python `rtgs_gate.apply_batch` function validates a batch of transfers using exact integer minor units and returns a new balance map plus replay-ID set. It rejects malformed input, duplicate IDs, insufficient funds, overflow, and cross-currency balance leakage. The Rust binary independently checks a bounded pairwise integer transfer.

## What remains a proposal
Authenticated settlement participants, durable transaction journaling, serializable concurrency, crash/restart safety, settlement finality, banking interfaces, multi-currency FX, regulatory controls, independent audit, operational monitoring, and disaster recovery. These are **not implemented** in this repository.

## Verification
Run `python -m unittest discover -s tests -p 'test_*.py' -v`, `cargo test --offline`, and inspect CodeQL/CI results for the exact commit SHA. A passing unit test does not establish end-to-end RTGS functionality, cryptographic certification, or security approval.

## Release policy
No production, public testnet/mainnet, paid cloud, gas, cycles, or secret-key operation is authorized by this project. Independent security review and evidence-based acceptance gates remain mandatory.
