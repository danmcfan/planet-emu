import requests
import os

API_UID = os.getenv("API_UID")
REGION = os.getenv("REGION")
STAGE = os.getenv("STAGE")
PATH = f"https://{API_UID}.execute-api.{REGION}.amazonaws.com/{STAGE}"

def test_mirror():
    response = requests.get(f"{PATH}/mirror/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}