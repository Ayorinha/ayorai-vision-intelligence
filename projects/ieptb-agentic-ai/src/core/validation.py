from typing import Any

def validate_remessa(data: dict[str, Any]) -> list[str]:
    issues=[]
    if data.get("quantidade_titulos", 0) < 0: issues.append("quantity_negative")
    if data.get("valor_total", 0) < 0: issues.append("value_negative")
    if not data.get("arquivo"): issues.append("file_missing")
    if data.get("quantidade_titulos", 0) == 0 and data.get("valor_total", 0) > 0: issues.append("value_without_titles")
    return issues
