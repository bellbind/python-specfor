import re
from specfor.mockings import mock

# [Example of decorator based mocking] 

# [Define mock] 
mockhttp = mock.define("mockhttp")
# define mock method with multiple input patterns and returns
# - at, until, over, between: count restriction
# - just, like, unless: parameter pattern
method = mockhttp.method("request")
@method.define(at=1, just=dict(uri="http://example.com", method="GET"))
def request(state, uri, method):
    return 200

@method.define(
    until=4, like=dict(uri=str, method=re.compile(r'PUT')))
def request(state, uri, method):
    return 201

@method.define(
    between=(2,3),
    like=dict(uri="http://example.com/foo", 
              method=lambda m:m == "GET"))
def request(state, uri, method):
    return 404

# define property: define get/set as same style with mock method
prop = mockhttp.property("uri")
@prop.get.always
def uri(state):
    return "http://localhost"

@prop.set.define(unless=dict(val="http://localhost"))
def uri(state, val):
    raise ValueError("invalid")


# [Use mock]
# Build mock instance with neat id
http = mockhttp("0")

# Access the property with expected behavior
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


# Check mock instance. 
# AssertionError because of count restrection is not filled
try:
    mock.check(http)
except AssertionError:
    print("OK: error by responsibility count not completed")
    pass

# Call method for completing count restrictions 
print(http.request("http://example.com", "GET"))
for i in range(4):
    print(http.request("http://example.com/foo", "PUT"))
    pass
for i in range(2):
    print(http.request("http://example.com/foo", "GET"))
    pass

# Check mock instance with no errors
mock.check(http)
