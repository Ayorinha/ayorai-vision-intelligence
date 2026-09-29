from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac


@dataclass(frozen=True)
class PublisherKey:
    """Trusted publisher verification key for synthetic/reference deployments."""

    key_id: str
    secret: bytes


class ManifestSigner:
    """Small HMAC-SHA256 manifest signer for authenticated reference deployments."""

    def __init__(self, key: PublisherKey) -> None:
        self.key = key

    def sign(self, canonical_manifest: str) -> str:
        return hmac.new(
            self.key.secret,
            canonical_manifest.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

    def verify(self, canonical_manifest: str, signature: str) -> bool:
        expected = self.sign(canonical_manifest)
        return hmac.compare_digest(expected, signature)
