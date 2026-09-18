from pathlib import Path
from src.core.database import init_db
from src.core.repository import upsert_knowledge

init_db()
source=Path("knowledge/demo_operations.md")
upsert_knowledge("demo_operations",source.read_text(encoding="utf-8"))
print("Demo knowledge loaded.")
