import re
from specfor import mock

# [pythonic mock design] 
mockhttp = mock.define("mockhttp")

method = mockhttp.method("request")
@mock.called.at(1)
@method.just(uri="http://example.com", method="GET")
def request(state, uri, method):
    return 200

@mock.called.until(4)
@method.like(uri=str, method=re.compile(r'GET|PUT|POST|DELETE'))
def request(state, uri, method):
    return 201

@mock.called.between(2, 3)
@method.like(uri="http://example.com/foo", 
             method=re.compile(r'GET|PUT|POST|DELETE'))
def request(state, uri, method):
    return 404


method = mockhttp.property("uri")
@method.get.always
def uri(state):
    return "http://localhost"

@method.set.unless(val="http://localhost")
def uri(state, val):
    raise ValueError("invalid")

http = mockhttp("0")
print(http.uri)
try:
    http.uri = "abc"
    pass
except ValueError:
    print("OK: error by resp def")
    pass
try:
    http.uri = "http://localhost"
    pass
except AssertionError:
    print("OK: error by no responsibility")
    pass
try:
    mock.check(http)
except AssertionError:
    print("OK: error by responsibility count not completed")
    pass
print(http.request("http://example.com", "GET"))
for i in range(4):
    print(http.request("http://example.com/foo", "GET"))
    pass
for i in range(2):
    print(http.request("http://example.com/foo", "GET"))
    pass
mock.check(http)
