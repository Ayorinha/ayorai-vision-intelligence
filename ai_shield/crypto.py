from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CryptoUse:
    component: str
    algorithm: str
    purpose: str


@dataclass
class CryptoInventory:
    """Algorithm inventory enabling crypto-agility and migration planning."""

    uses: list[CryptoUse] = field(default_factory=list)

    def register(self, component: str, algorithm: str, purpose: str) -> None:
        self.uses.append(CryptoUse(component, algorithm, purpose))

    def algorithms(self) -> set[str]:
        return {item.algorithm for item in self.uses}

    def migration_candidates(self) -> tuple[CryptoUse, ...]:
        return tuple(
            item for item in self.uses
            if item.algorithm.upper() in {"RSA", "RSA-PSS", "ECDSA", "ECDH", "DH"}
        )
