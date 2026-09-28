from pathlib import Path

from src.api.main import app


def test_release_version_contract():
    pyproject = Path("pyproject.toml").read_text(encoding="utf-8")
    assert 'version = "3.0.0"' in pyproject
    assert app.version == "3.0.0"
