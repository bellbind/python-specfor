import difflib
import functools

# expectation actions
class MatchAction(object):
    def __init__(self, expectation):
        self.expectation = expectation
        pass
    def __getitem__(self, expected):
        return self.__call__(expected)

class Match(MatchAction):
    def __call__(self, expected):
        message = "it[%s] should be %s" % (
            repr(self.expectation.value), repr(expected))
        assert self.expectation.value == expected, message
        pass
    pass

class MatchNot(MatchAction):
    def __call__(self, expected):
        message = "it should not be %s" % (repr(self.expectation.value))
        assert self.expectation.value != expected, message
        pass
    pass

class MatchInstance(MatchAction):
    def __call__(self, expected):
        message = "it[%s] should not be instance of %s" % (
            repr(self.expectation.value), repr(expected))
        assert isinstance(self.expectation.value, expected), message
        pass
    pass

class MatchExist(MatchAction):
    def __call__(self):
        message = "it[%s] does not exist" % (self.expectation.value)
        assert self.expectation.value is not None, message
        pass
    pass

class MatchIn(MatchAction):
    def __call__(self, expected):
        message = "it[%s] does not exist in %s" % (
            self.expectation.value, expected)
        assert self.expectation.value in expected, message
        pass
    pass

class MatchEach(MatchAction):
    def __call__(self, expected):
        value = list(sorted(self.expectation.value))
        exp = list(sorted(expected))
        
        diff = difflib.SequenceMatcher(None, value, exp)
        matches = diff.get_matching_blocks()
        vindex = 0
        eindex = 0
        lefts = []
        not_founds = []
        for match in matches:
            lefts.extend(value[vindex:match.a])
            not_founds.extend(exp[eindex:match.b])
            vindex = match.a + match.size
            eindex = match.b + match.size
            pass
        
        message = ""
        message += "%s should not be in it" % lefts if lefts else ""
        message += ", and " if lefts and not_founds else ""
        message += "%s should be in it" % not_founds if not_founds else ""
        
        assert value != exp, message
        pass
    pass

class MatchTrue(MatchAction):
    def __call__(self):
        message = "it[%s] should be False" % (self.expectation.value)
        assert self.expectation.value, message
        pass
    pass

class MatchActions(object):
    def __init__(self, expectation):
        self.expectation = expectation
        pass
    def __eq__(self, expected):
        Match(self.expectation)(expected)
        pass
    def __ne__(self, expected):
        MatchNot(self.expectation)(expected)
        pass
    @property
    def be(self):
        return Match(self.expectation)
    @property
    def not_be(self):
        return MatchNot(self.expectation)
    @property
    def exist(self):
        return MatchExist(self.expectation)()
    @property
    def be_true(self):
        return MatchTrue(self.expectation)()
    @property
    def be_in(self):
        return MatchIn(self.expectation)
    @property
    def be_instance_of(self):
        return MatchInstance(self.expectation)
    pass

class ValueExpectation(object):
    def __init__(self, value):
        self.value = value
        pass
    def __getattr__(self, name):
        value = getattr(self.value, name)
        if not hasattr(value, "__call__"): return ValueExpectation(value)
        @functools.wraps(value)
        def proxy(*args, **kwargs):
            return ValueExpectation(value(*args, **kwargs))
        return proxy
    def __call__(self, affect):
        return ValueExpectation(affect(self.value))
    def __enter__(self):
        return self
    def __exit__(self, type, exc, traceback):
        return type is None
    @property
    def should(self):
        return MatchActions(self)
    pass

class ErrorExpectation(object):
    def __init__(self, exc_type):
        self.exc_type = exc_type
        pass
    def __enter__(self):
        return self
    def __exit__(self, type, exc, traceback):
        if type == self.exc_type:
            self.exc = exc
            self.traceback = traceback
            return True
        if type is None:
            assert False, "Nothing is raised expected to raise %s" % (
                repr(self.exc_type))
            pass
        else:
            assert False, "%s is raised, but expected to raise %s" % (
                exc, repr(self.exc_type))
            pass
        return False
    pass

# DSL
class The(object):
    def __getitem__(self, value):
        return ValueExpectation(value)
    pass
class Expected(object):
    def __getitem__(self, value):
        return ErrorExpectation(value)
    pass


the = The()
expected = Expected()
__all__ = ["the", "expected"]

