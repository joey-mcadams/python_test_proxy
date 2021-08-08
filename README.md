# python_test_proxy
A generic proxy server written in python.

This is some scratch / garbage code. It's a really fast implementation of a Flask proxy server I wanted to test out.

This will look for any incoming payload that has: 

```
{
    "test_key":"malicious"
}
```

If that key is found, it will respond with a 451 (Legally unable to respond) error. 

The requirements are pinned due to a bug in the Werkzeug library. If you use the latest versions, you can not 
debug this app in pycharm.

