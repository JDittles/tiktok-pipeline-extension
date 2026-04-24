import json
import os
import sys
import urllib.request
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

TIKTOK_URL = "https://www.tiktok.com/@hereinhawaiitv/video/7631290061862079757?q=natural%20disaster%20help%20video&t=1776990758219"
PROVIDER = "claude"
URL = "http://localhost:8000/classify"


_KEY_MAP = {
    "gemini": "GOOGLE_API_KEY",
    "openai": "OPENAI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
}

PAYLOAD = {
    "url": TIKTOK_URL,
    "provider": PROVIDER,
    "api_key": os.getenv(_KEY_MAP[PROVIDER]),
}

def main():
    data = json.dumps(PAYLOAD).encode()
    req = urllib.request.Request(URL, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read())
            pprint(body)
    except urllib.error.HTTPError as e:
        body = json.loads(e.read())
        print(f"HTTP {e.code}:", json.dumps(body, indent=2), file=sys.stderr)

if __name__ == "__main__":
    main()
