from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class RuntimeDescriptor:
    artifact_digest: str
    runtime_version: str
    policy_digest: str


@dataclass(frozen=True)
class AttestationResult:
    verified: bool
    reason: str


class RuntimeAttestor(Protocol):
    def verify(self, runtime: RuntimeDescriptor) -> AttestationResult:
        ...


class StaticRuntimeAttestor:
    """Reference interface; real TEE/attestation providers can implement the protocol."""

    def __init__(self, trusted_artifacts: set[str]) -> None:
        self.trusted_artifacts = set(trusted_artifacts)

    def verify(self, runtime: RuntimeDescriptor) -> AttestationResult:
        if runtime.artifact_digest not in self.trusted_artifacts:
            return AttestationResult(False, "runtime_artifact_not_trusted")
        if not runtime.policy_digest:
            return AttestationResult(False, "policy_digest_missing")
        return AttestationResult(True, "runtime_attestation_satisfied")
