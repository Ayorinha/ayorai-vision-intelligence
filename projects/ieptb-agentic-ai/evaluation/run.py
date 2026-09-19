import json
import sys
from pathlib import Path

from src.core.orchestrator import analyze
from src.core.schemas import Remessa

def main() -> int:
    cases=json.loads(Path(__file__).with_name("cases.json").read_text())
    passed=0
    for case in cases:
        result=analyze(
            Remessa(
                remessa_id=case["id"],
                apresentante="SYNTHETIC",
                quantidade_titulos=2,
                valor_total=10,
                arquivo="synthetic.rem",
            ),
            case["query"],
        )
        ok=(
            (case["expected"]=="blocked" and result["status"]=="BLOCKED")
            or (case["expected"]=="human_review" and result["requires_human_review"])
            or (case["expected"]=="evidence" and bool(result["evidence"]))
        )
        passed += int(ok)
        print(f"{case['id']}: {'PASS' if ok else 'FAIL'}")
    total=len(cases)
    rate=passed/total if total else 0
    print(f"RESULT: {passed}/{total} cases passed ({rate:.1%})")
    return 0 if passed == total else 1

if __name__=="__main__":
    sys.exit(main())
