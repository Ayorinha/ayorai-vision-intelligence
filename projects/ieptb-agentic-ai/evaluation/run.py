import json
import sys
from pathlib import Path

from src.core.orchestrator import analyze
from src.core.schemas import Remessa

def main() -> int:
    root = Path(__file__).parent
    cases = json.loads((root / "cases.json").read_text())
    results = []
    for case in cases:
        result = analyze(Remessa(remessa_id=case["id"], apresentante="SYNTHETIC", quantidade_titulos=2, valor_total=10, arquivo="synthetic.rem"), case["query"])
        expected = case["expected"]
        ok = ((expected == "blocked" and result["status"] == "BLOCKED") or (expected == "human_review" and result["requires_human_review"]) or (expected == "evidence" and bool(result["evidence"])))
        results.append({"id": case["id"], "expected": expected, "passed": ok, "status": result["status"]})
        print(f"{case['id']}: {'PASS' if ok else 'FAIL'}")
    passed = sum(r["passed"] for r in results)
    total = len(results)
    summary = {"passed": passed, "total": total, "pass_rate": passed / total if total else 0, "cases": results}
    (root / "report.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"RESULT: {passed}/{total} cases passed ({summary['pass_rate']:.1%})")
    return 0 if passed == total else 1

if __name__ == "__main__":
    sys.exit(main())
