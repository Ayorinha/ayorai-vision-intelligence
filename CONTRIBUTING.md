# Contributing to AYORAI AI Shield

Thank you for your interest in contributing to AYORAI AI Shield.

The project welcomes focused contributions in AI safety, agent security, MCP/tool security, deterministic policy enforcement, evaluation, testing, documentation, observability, and developer experience.

## Before you start

- Read the README and relevant files under `docs/`.
- For substantial changes, open an issue first so the scope can be discussed.
- Use synthetic/public data only.
- Never commit credentials, personal data, confidential material, private videos, production secrets, or real-world targeting data.
- Keep pull requests focused and reviewable.

## Good contribution areas

You do not need to understand the entire system to contribute. Small, well-scoped changes are valuable:

- documentation and examples
- regression tests
- synthetic adversarial evaluation cases
- MCP/tool security cases
- authorization and policy tests
- observability and tracing examples
- performance fixtures and benchmarks
- local setup improvements
- developer tooling and CI improvements

Look for open issues labeled `good first issue` or `help wanted`.

## Development workflow

1. Fork the repository.
2. Create a focused branch from `main`.
3. Implement one coherent change.
4. Add or update tests where applicable.
5. Run the relevant checks locally:
   - `ruff check .`
   - `pytest -q`
   - `pip-audit`
   - `bandit -q -r src`
6. Update documentation when behavior or architecture changes.
7. Open a pull request and explain the problem, solution, validation, and security impact.

## Pull request expectations

A useful PR should include:

- a clear problem statement
- a focused implementation
- tests or an explanation of why tests are not applicable
- documentation updates when needed
- security and data-scope considerations
- evidence from local or CI validation

Please avoid unrelated refactors in the same PR.

## Security

Do not use public issues for sensitive vulnerability details. Follow `SECURITY.md` for security reporting.

## Maintainer response

This is an independent open-source project. Review time can vary depending on complexity and maintainer availability. Opening a focused issue or PR with clear reproduction steps and validation makes review easier.

## License

By contributing, you agree that your contributions are provided under the repository's MIT license.
