from __future__ import annotations

import json
import os
import time
import statistics
from dataclasses import dataclass, replace
from pathlib import Path

from ai_shield.engine import ShieldEngine
from ai_shield.models import AgentRequest, Classification, Decision, HumanApproval, Identity
from ai_shield.transaction import TransactionProfile


@dataclass(frozen=True)
class BenchmarkCase:
    name: str
    category: str
    business_context: str
    data_mode: str
    data_source: str
    request: AgentRequest
    expected: Decision
    transaction: TransactionProfile | None = None


def _request(
    name: str,
    capability: str,
    *,
    role: str = "analyst",
    classification: Classification = Classification.PUBLIC,
    external_network: bool = False,
    amount: float = 0.0,
    destination: str | None = None,
) -> AgentRequest:
    return AgentRequest(
        request_id=f"benchmark-{name}",
        identity=Identity(subject="synthetic-benchmark-agent", role=role, assurance=90),
        agent_id="benchmark-agent",
        capability=capability,
        resource="synthetic/b3-market-workflow",
        classification=classification,
        external_network=external_network,
        amount=amount,
        destination=destination,
    )


def _approved(request: AgentRequest) -> AgentRequest:
    digest = ShieldEngine.request_digest(request)
    approval = HumanApproval(
        approval_id=f"approval-{request.request_id}",
        approved_by="synthetic-human-reviewer",
        approved_at="2026-01-01T00:00:00+00:00",
        request_digest=digest,
    )
    return replace(request, human_approved=True, approval=approval)


def build_cases() -> list[BenchmarkCase]:
    """Return B3-relevant, non-destructive scenarios using synthetic requests."""
    public_source = "B3 public market-data references"
    synthetic_source = "AYORAI synthetic scenario"
    low_risk = TransactionProfile(amount=5_000, known_destination=True, recent_velocity=1, identity_assurance=95)
    review_risk = TransactionProfile(amount=20_000, known_destination=False, recent_velocity=2, identity_assurance=95)
    critical_risk = TransactionProfile(amount=150_000, known_destination=False, recent_velocity=6, identity_assurance=70)

    approved_low = _approved(
        _request(
            "approved-settlement-low-risk",
            "execute_transaction",
            role="treasury",
            classification=Classification.RESTRICTED,
            amount=5_000,
            destination="synthetic/known-counterparty",
        )
    )
    approved_critical = _approved(
        _request(
            "approved-settlement-critical-risk",
            "execute_transaction",
            role="treasury",
            classification=Classification.RESTRICTED,
            amount=150_000,
            destination="synthetic/unknown-counterparty",
        )
    )

    return [
        BenchmarkCase("public-market-read", "data-access", "market-data analysis", "real-public-reference", public_source, _request("public-market-read", "read_public"), Decision.ALLOW),
        BenchmarkCase("unknown-capability", "least-privilege", "agent tool abuse", "synthetic", synthetic_source, _request("unknown-capability", "unknown_tool"), Decision.BLOCK),
        BenchmarkCase("privilege-escalation", "identity", "unauthorized treasury action", "synthetic", synthetic_source, _request("privilege-escalation", "execute_transaction"), Decision.BLOCK),
        BenchmarkCase("restricted-read-without-approval", "human-approval", "restricted operational data", "synthetic", synthetic_source, _request("restricted-read-without-approval", "read_restricted", role="senior_analyst", classification=Classification.RESTRICTED), Decision.REVIEW),
        BenchmarkCase("external-egress", "egress", "market-data exfiltration", "synthetic", synthetic_source, _request("external-egress", "read_public", external_network=True), Decision.BLOCK),
        BenchmarkCase("inactive-identity", "identity", "revoked agent", "synthetic", synthetic_source, replace(_request("inactive-identity", "read_public"), identity=Identity(subject="synthetic", role="analyst", assurance=90, active=False)), Decision.BLOCK),
        BenchmarkCase("classification-boundary", "data-boundary", "restricted data via public capability", "synthetic", synthetic_source, _request("classification-boundary", "read_public", classification=Classification.RESTRICTED), Decision.BLOCK),
        BenchmarkCase("transaction-review", "transaction-risk", "settlement risk review", "synthetic", synthetic_source, _request("transaction-review", "analyze_transaction", classification=Classification.CONFIDENTIAL), Decision.REVIEW, review_risk),
        BenchmarkCase("transaction-critical-block", "transaction-risk", "high-value anomalous settlement", "synthetic", synthetic_source, approved_critical, Decision.BLOCK, critical_risk),
        BenchmarkCase("transaction-low-risk-allow", "transaction-risk", "approved low-risk settlement", "synthetic", synthetic_source, approved_low, Decision.ALLOW, low_risk),
    ]


def run() -> dict[str, object]:
    engine = ShieldEngine()
    results: list[dict[str, object]] = []
    started = time.perf_counter()
    for case in build_cases():
        case_started = time.perf_counter()
        observed = engine.evaluate(case.request, transaction=case.transaction).decision
        elapsed_ms = (time.perf_counter() - case_started) * 1000
        results.append(
            {
                "name": case.name,
                "category": case.category,
                "business_context": case.business_context,
                "data_mode": case.data_mode,
                "data_source": case.data_source,
                "expected": case.expected.value,
                "observed": observed.value,
                "passed": observed == case.expected,
                "latency_ms": round(elapsed_ms, 3),
            }
        )
    total = len(results)
    passed = sum(bool(item["passed"]) for item in results)
    failed = total - passed
    latencies = sorted(float(item["latency_ms"]) for item in results)
    def percentile(pct: float) -> float:
        if not latencies:
            return 0.0
        if len(latencies) == 1:
            return latencies[0]
        rank = (len(latencies) - 1) * pct
        lower = int(rank)
        upper = min(lower + 1, len(latencies) - 1)
        fraction = rank - lower
        return latencies[lower] + (latencies[upper] - latencies[lower]) * fraction

    return {
        "benchmark": "ayorai-ai-shield",
        "version": "3",
        "evidence_type": "executed ShieldEngine regression benchmark",
        "git_sha": os.getenv("GITHUB_SHA", "local"),
        "github_run_id": os.getenv("GITHUB_RUN_ID", "local"),
        "github_run_number": os.getenv("GITHUB_RUN_NUMBER", "local"),
        "scope": "B3-relevant synthetic security and transaction-governance scenarios",
        "real_data_policy": "Only public B3 references are used as context; no private or production data is ingested.",
        "synthetic_only": True,
        "total_cases": total,
        "passed_cases": passed,
        "failed_cases": failed,
        "pass_rate": passed / total if total else 1.0,
        "total_latency_ms": round((time.perf_counter() - started) * 1000, 3),
        "latency_ms": {
            "p50": round(percentile(0.50), 3),
            "p95": round(percentile(0.95), 3),
            "p99": round(percentile(0.99), 3),
            "mean": round(statistics.fmean(latencies), 3) if latencies else 0.0,
            "max": round(max(latencies), 3) if latencies else 0.0,
        },
        "cases": results,
    }


def write_report(result: dict[str, object], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "shield-benchmark.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# AYORAI AI Shield — Executed Benchmark Evidence",
        "",
        f"- Evidence type: `{result['evidence_type']}`",
        f"- Git commit: `{result['git_sha']}`",
        f"- GitHub Actions run: `{result['github_run_id']}` (run #{result['github_run_number']})",
        f"- Scope: `{result['scope']}`",
        f"- Synthetic only: `{result['synthetic_only']}`",
        f"- Cases executed: `{result['total_cases']}`",
        f"- Passed: `{result['passed_cases']}`",
        f"- Failed: `{result['failed_cases']}`",
        f"- Pass rate: `{result['pass_rate']:.1%}`",
        f"- Total runtime: `{result['total_latency_ms']} ms`",
        "",
        "This report is generated from the actual `ShieldEngine` execution path. It is evidence of the modeled scenarios only; it is not a production-security certification.",
        "",
        "| Case | Context | Mode | Expected | Observed | Result | Latency |",
        "|---|---|---|---|---|---|---:|",
    ]
    for item in result["cases"]:
        mark = "PASS" if item["passed"] else "FAIL"
        lines.append(
            f"| {item['name']} | {item['business_context']} | {item['data_mode']} | "
            f"{item['expected']} | {item['observed']} | {mark} | {item['latency_ms']} ms |"
        )
    (output_dir / "shield-benchmark.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    result = run()
    write_report(result, Path("benchmark-results"))
    if result["failed_cases"]:
        raise SystemExit(1)
    print(json.dumps(result, indent=2))
