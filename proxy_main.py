import flask
from flask import Flask, request, Response
from requests import get
import json

app = Flask(__name__)

HOST = '0.0.0.0'
PORT = 8080


def pre_process_request(request_: flask.Request) -> bool:
    """
    This simply looks at the payload of a request and returns True or False
    depending on if the payload is JSON, and includes
    "test_key":"malicious"
    """

    # noinspection PyBroadException
    try:
        payload_string = request_.data.decode()
        payload = json.loads(payload_string)
        if "test_key" in payload.keys():
            if payload.get("test_key", None) == "malicious":
                return False

    # This is terrible practice, too broad exception.
    # However, I didn't want to deal with the all the exceptions that can happen
    # if the payload isn't actually JSON or even text
    except Exception as e:
        pass

    return True


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    if pre_process_request(request):
        return get(request.url).content
    else:
        return Response("Malicious JSON", 403)


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)