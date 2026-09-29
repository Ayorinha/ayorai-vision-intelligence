# Post-Quantum Migration Guidance

This document is a migration-planning reference. AYORAI AI Shield does not claim post-quantum security.

## Inventory first

Before changing algorithms, inventory:

- RSA signatures and key sizes;
- RSA key transport;
- ECDSA signing;
- ECDH key agreement;
- DH key agreement;
- certificate and trust-store dependencies;
- protocol versions and external interoperability constraints.

The existing crypto-agility inventory can identify candidate algorithms; it does not perform cryptographic migration automatically.

## Migration sequence

1. classify keys and protocols by business impact and data lifetime;
2. identify long-lived confidential data and harvest-now-decrypt-later exposure;
3. confirm approved algorithms with the organization's cryptographic standards owner;
4. establish hybrid interoperability where required by the protocol;
5. rotate and revoke keys under controlled procedures;
6. validate signatures, key agreement and certificate paths in staging;
7. measure compatibility and performance with reproducible tests;
8. document rollback and emergency key-rotation procedures.

Algorithm selection must follow current standards and organizational risk and interoperability requirements. This repository intentionally does not hard-code a universal post-quantum choice.
