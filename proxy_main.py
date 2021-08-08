import flask
from flask import Flask, request, Response
from requests import get
import json

app = Flask(__name__)


def pre_process_request(request_: flask.Request) -> bool:
    # noinspection PyBroadException

    try:
        payload_string = request_.data.decode()
        payload = json.loads(payload_string)
        if "test_key" in payload.keys():
            if payload.get("test_key", None) == "malicious":
                return False

    # This is terrible practice, to broad exception.
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
        return Response("Malicious JSON", 451)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    # app.run(host='0.0.0.0', port=8080)
