"""Exporta o OpenAPI gerado pelo FastAPI (usado pelo GitHub Pages)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app  # noqa: E402

destino = Path(sys.argv[1] if len(sys.argv) > 1 else "openapi.json")
destino.parent.mkdir(parents=True, exist_ok=True)
doc = app.openapi()
doc.setdefault("servers", [{"url": "http://localhost:8000", "description": "Ambiente local"}])
for metodos in doc["paths"].values():
    for operacao in metodos.values():
        operacao.setdefault("security", [])  # rotas sem token explícito ficam marcadas como públicas
destino.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OpenAPI exportado em {destino}")
