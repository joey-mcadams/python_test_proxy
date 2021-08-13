## Description

This is a simple proxy server to inspect traffic as it goes to [httpbin.org](https://httpbin.org/)

If a request has a JSON payload, and in that payload there's a key value of `{"is_malicious": true}` then the proxy
will intercept the payload and return a 403 error. 

If a request repeats, the proxy will log a warning. 

The proxy is built on Python and uses the [Flask](https://flask.palletsprojects.com/) library

### How to run

#### Prereqs
Install required libraries
```bash
pip install -r .\requirements.txt
```

#### Run the proxy
From the project root:
```bash
python .\proxy_main.py
```

#### Curl Commands to get you going:
Simple curl: 
```bash
curl --location --request GET 'http://0.0.0.0:8080/get'
```

Simple malicious test case
```bash
curl --location --request POST 'http://0.0.0.0:8080/post' \
--header 'Content-Type: application/json' \
--data-raw '{
    "is_malicious":true
}'
```

A slightly more complicated test case
```bash
curl --location --request POST 'http://0.0.0.0:8080/post' \
--header 'Content-Type: application/json' \
--data-raw '{
    "is_malicious":false,
    "hidden": {
        "some_value": {
            "is_malicious": false
        }
    }
}'
```