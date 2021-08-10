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


## Original Requirements
Rust is preferred but not required.  You may also implement it in C++, Java, Scala, Python, Node.js, or Deno.  If you are more comfortable in one of these other options, then please use it.  We would rather see an accurate representation of who you are as an engineer than a Rust implementation.  If you don’t see your favorite language on this list please ask us about it.  Feel free to use any technologies, libraries, or services you need to help accomplish your goal.

Our interest isn’t in if you can solve this exercise, but how you solve it.  We value quality software engineering practices and well-documented, understandable, maintainable, and tested code bases.  These priorities are what we will be looking for out of the homework assignment.  

The goal is to develop a simple HTTP service that will stand in front of another HTTP server and accept requests and proxy them back to some back end.  This will act in some ways like a very simple web application firewall.  It should accept these requests, inspect them, and then make some action.


   • The location of the back-end service must be configurable in some way.

   • First, we want to look to see if the request is malicious.  In this exercise, we will make it easy and assume the attack will announce itself in the request.  If there is a request with a JSON body with a key named is_malicious and set to true then the request should be blocked.  Blocked requests should not be proxied to the back-end and the client should be return an HTTP 403 response. This value might be at the root of the JSON object or nested in a child object.  For example: Both `{ "is_malicious": true }` and `{ "hidden": { "is_malicious": true } }` should be blocked while `{ "is_malicious": false }` and `{ “data” : null }` should not.

   • If a request isn’t blocked, then it should be passed on to the back-end without any changes.  The response from the back-end should then be forwarded on to the client without any changes.

   • If we see two identical requests in a row, then we need to log this in some kind of an audit trail, so if an analyst needs to follow up on it, we have a record on it.
      

The final deliverable should be in the form of a pull request against this repo.  The pull request should include all required documentation to help us set up the program and use it.  You should also include any tools or scripts you used to test it.  

If you have any questions, please don’t hesitate to ask.  In software engineering, requirements gathering can be just as important as the coding itself.
