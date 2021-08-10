import copy

from flask import Flask, request, Response

import proxy_main
from util.request_pre_processor import is_invalid_key_present, is_repeat_request

import requests
import urllib
import logging

from config import *

app = Flask(__name__)

LAST_REQUEST = None

@app.route('/', methods=HTTP_METHODS)
@app.route('/<path:path>', methods=HTTP_METHODS)
def proxy(path):
    # Check for malicous key
    if is_invalid_key_present(request):
        return Response("Malicious JSON", 403)

    # Check for repeats
    result = is_repeat_request(request, proxy_main.LAST_REQUEST)
    if result:
        logging.warning("Repeat request found!")
        logging.warning(request)
    proxy_main.LAST_REQUEST = copy.copy(request)

    # Good request, send it
    return requests.request(method=request.method,
                            url=urllib.parse.urljoin(URL_BASE, path),
                            headers=request.headers,
                            data=request.data
                            ).content


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)