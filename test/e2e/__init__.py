from fastapi.testclient import TestClient
from test.config.database import override_get_db
from src.config.database import get_db
from main import app

client = TestClient(app)

app.dependency_overrides[get_db] = override_get_db
