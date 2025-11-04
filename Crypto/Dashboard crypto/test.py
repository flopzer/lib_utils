import importlib
import pytest

# test.py
# Tests Flask basiques avec pytest. Placez ce fichier à la racine du projet et lancez: pytest -q

def get_app():
    # Essaie d'importer app.create_app or app.app, sinon main.create_app or main.app
    for module_name in ("app", "main"):
        try:
            mod = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        if hasattr(mod, "create_app"):
            return mod.create_app()
        if hasattr(mod, "app"):
            return mod.app
    raise RuntimeError(
        "Impossible d'importer l'application Flask. Créez un module app.py ou main.py "
        "exportant create_app() ou app."
    )

@pytest.fixture
def client():
    app = get_app()
    app.testing = True
    with app.test_client() as client:
        yield client

def test_root_accessible(client):
    """Vérifie que la route '/' répond (200 ou redirection)."""
    resp = client.get("/")
    assert resp.status_code in (200, 302), f"Unexpected status {resp.status_code}"

def test_health_endpoint_if_present(client):
    """Vérifie /health, /ping ou /status si l'une existe; sinon skip."""
    for path in ("/health", "/ping", "/status"):
        resp = client.get(path)
        if resp.status_code == 200:
            ct = resp.headers.get("Content-Type", "")
            assert ("json" in ct) or ("text" in ct) or ("html" in ct)
            return
    pytest.skip("Aucun endpoint de santé (/health, /ping, /status) trouvé")



