from pathlib import Path
import sys

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app import create_app
from app.services import user_service


@pytest.fixture(autouse=True)
def reset_user_state():
    user_service.reset_state()


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()
