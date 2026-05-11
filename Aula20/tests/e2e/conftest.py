import os
import shutil
import threading
import time
import urllib.request

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from werkzeug.serving import make_server

from app import create_app


def _wait_for_server(base_url, timeout=5):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base_url, timeout=1) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.1)

    raise RuntimeError("Server did not start")


def _find_chrome_binary():
    env_path = os.environ.get("CHROME_BIN")
    if env_path and os.path.exists(env_path):
        return env_path

    for candidate in (
        "google-chrome",
        "google-chrome-stable",
        "chromium",
        "chromium-browser",
    ):
        path = shutil.which(candidate)
        if path:
            return path

    return None


@pytest.fixture(scope="session")
def live_server():
    app = create_app()
    server = make_server("127.0.0.1", 5000, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    _wait_for_server("http://127.0.0.1:5000")
    yield "http://127.0.0.1:5000"

    server.shutdown()
    thread.join()


@pytest.fixture
def driver():
    chrome_binary = _find_chrome_binary()
    if not chrome_binary:
        pytest.skip("Chrome not available for E2E tests")

    options = Options()
    options.binary_location = chrome_binary
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1280,720")

    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as exc:
        pytest.skip(f"Chrome not available for E2E tests: {exc}")
    yield driver
    driver.quit()
