import re

INJECTION_PATTERNS = [
    r"ignore\s+(all|any|previous|prior)\s+instructions",
    r"reveal\s+(the\s+)?system\s+prompt",
    r"export\s+all\s+(records|data)",
    r"send\s+.*\s+credentials",
    r"disable\s+(security|audit|policy)",
    r"bypass\s+(security|policy|approval)",
]

PII_PATTERNS = {
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "cpf_like": re.compile(r"\b\d{3}[.]?\d{3}[.]?\d{3}[-]?\d{2}\b"),
    "phone": re.compile(r"\b(?:\+?55\s?)?(?:\(?\d{2}\)?\s?)?9?\d{4}[-\s]?\d{4}\b"),
}

def detect_prompt_injection(text: str) -> list[str]:
    return [p for p in INJECTION_PATTERNS if re.search(p, text, re.I)]

def redact_pii(text: str) -> tuple[str, list[str]]:
    found=[]
    redacted=text
    for kind, pattern in PII_PATTERNS.items():
        if pattern.search(redacted):
            found.append(kind)
            redacted=pattern.sub(f"[REDACTED_{kind.upper()}]", redacted)
    return redacted, found
