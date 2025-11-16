import pytest
import requests
import threading
import time
from app import app

@pytest.fixture(scope="module")
def server_url():
    # Start server in background
    thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=8081, debug=False)
    )
    thread.daemon = True
    thread.start()
    time.sleep(1)
    return "http://127.0.0.1:8081"

def test_octocat_gists(server_url):
    response = requests.get(f"{server_url}/octocat")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "id" in data[0]
    assert "html_url" in data[0]