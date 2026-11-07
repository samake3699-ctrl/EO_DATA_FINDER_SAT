
import os
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from dotenv import load_dotenv

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/"
    "auth/realms/CDSE/protocol/openid-connect/token"
)


def get_access_token():
    load_dotenv(Path(__file__).with_name(".env"))

    client_id = os.getenv("COPERNICUS_CLIENT_ID")
    client_secret = os.getenv("COPERNICUS_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Missing Copernicus credentials in .env")

    data = urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")

    request = Request(
        TOKEN_URL,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )

    with urlopen(request, timeout=30) as response:
        result = json.load(response)

    return result["access_token"]


if __name__ == "__main__":
    get_access_token()
    print("OAuth authentication OK")
