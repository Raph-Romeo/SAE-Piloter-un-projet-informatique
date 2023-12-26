import json
import datetime


def test(request) -> bytes:
    return json.dumps({"message": "Response from url /test"}).encode()
