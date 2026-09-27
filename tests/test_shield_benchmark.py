from benchmarks.shield_benchmark import build_cases, run


def test_benchmark_cases_are_synthetic_and_have_expected_decisions():
    cases = build_cases()
    assert cases
    assert all(case.request.resource.startswith("synthetic/") for case in cases)
    assert all(case.expected.value in {"allow", "review", "block", "isolate"} for case in cases)


def test_benchmark_runs_against_real_shield_engine():
    result = run()
    assert result["synthetic_only"] is True
    assert result["total_cases"] == len(build_cases())
    assert result["failed_cases"] == 0
    assert result["pass_rate"] == 1.0
