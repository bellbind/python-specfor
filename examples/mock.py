import re
from specfor.mockings import mock

# [decorator based mock design] 
# not yet implemented
mockhttp = mock.define("mockhttp")

method = mockhttp.method("request")
@method.define(at=1, just=dict(uri="http://example.com", method="GET"))
def request(state, uri, method):
    return 200

@method.define(
    until=4, like=dict(uri=str, method=re.compile(r'GET|PUT|POST|DELETE')))
def request(state, uri, method):
    return 201

@method.define(
    between=(2,3),
    like=dict(uri="http://example.com/foo", 
              method=re.compile(r'GET|PUT|POST|DELETE')))
def request(state, uri, method):
    return 404


prop = mockhttp.property("uri")
@prop.get.always
def uri(state):
    return "http://localhost"

@prop.set.define(unless=dict(val="http://localhost"))
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
