from benchmarks.shield_benchmark import build_cases, run


def test_benchmark_cases_are_safe_and_typed():
    cases = build_cases()
    assert cases
    assert all(case.request.resource.startswith("synthetic/") for case in cases)
    assert all(case.expected.value in {"allow", "review", "block", "isolate"} for case in cases)
    assert any(case.data_mode == "real-public-reference" for case in cases)
    assert any(case.data_mode == "synthetic" for case in cases)


def test_benchmark_runs_against_real_shield_engine():
    result = run()
    assert result["evidence_type"] == "executed ShieldEngine regression benchmark"
    assert result["git_sha"]
    assert result["github_run_id"]
    assert result["total_cases"] == len(build_cases())
    assert result["failed_cases"] == 0
    assert result["pass_rate"] == 1.0
    assert all(item["passed"] for item in result["cases"])
    assert all(item["latency_ms"] >= 0 for item in result["cases"])


def test_benchmark_covers_core_b3_relevant_controls():
    categories = {case.category for case in build_cases()}
    assert {"data-access", "least-privilege", "human-approval", "egress", "transaction-risk"} <= categories
