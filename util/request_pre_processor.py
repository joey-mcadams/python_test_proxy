import json
from config.config import BAD_KEY
import flask


def is_repeat_request(request_: flask.Request, last_request: flask.Request) -> bool:
    """
    Look to see if the incoming request is a repeat of the last request

    If it is a repeat return True
    If it is not a repeat return False
    """

    # I'm making an assumption here:
    # if the last request has the same url, from the same origin, with the same data
    # it's the same request.

    # TODO: Another cheaty thing I'm doing here:
    #       google.com should equal www.google.com
    if last_request:
        if last_request.base_url == request_.base_url \
           and last_request.data == request_.data \
           and last_request.remote_addr == request_.remote_addr:
            return True

    return False


def is_invalid_key_present(request_: flask.Request) -> bool:
    """
    This simply looks at the payload of a request and returns True or False
    depending on if the payload is JSON, and includes
    "test_key":"malicious"
    """

    if not request_.data:  # We don't have data, it's good
        return False

    # noinspection PyBroadException

    # Walk through our incoming payload and see if the malicious key and value
    # is present
    try:
        payload_string = request_.data.decode()

        # This is faster than walking the JSON for the key, this will speed up
        # performance on things we're not interested in.
        if BAD_KEY in payload_string:

            # We found a potential match, lets go through the JSON and look for it.
            return _walk_json_for_bad_key(json.loads(payload_string))

    # This is terrible practice, too broad exception.
    # However, I didn't want to deal with the all the exceptions that can happen
    # if the payload isn't actually JSON or even text
    except Exception as e:
        print(e)

    return False


def _walk_json_for_bad_key(node: dict) -> bool:
    """
    Given a dict, walk through it's contents and see if it has a bad_key
    and the bad_key's value is True

    return: boolean
    """
    if isinstance(node, list):
        return _walk_list(node)

    for key, item in node.items():
        if isinstance(item, dict):
            return _walk_json_for_bad_key(item)
        if isinstance(item, list):
            return _walk_list(item)
        else:
            if key == BAD_KEY and item == True:
                return True

    return False


def _walk_list(node):
    """
    Given a list, walk through it's contents and see if contains any dicts. If it does
    then walk that dict to find if it contains the BAD_KEY

    return: boolean
    """
    for item in node:
        if isinstance(item, dict):
            return _walk_json_for_bad_key(item)

    return False

