import requests
import os

BASE_URL = f"https://api.planet-emu.com"


def test_mirror():
    response = requests.get(f"{BASE_URL}/mirror/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}
