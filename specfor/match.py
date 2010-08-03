import difflib
import functools

class MatchActions(object):
    def __init__(self, expectation):
        self.expectation = expectation
        pass
    pass


def register(name, match_func):
    setattr(MatchActions, name, match_func)
    pass

# expectation actions
class MatchAction(object):
    def __init__(self, expectation):
        self.expectation = expectation
        pass
    def __getitem__(self, expected):
        return self.__call__(expected)
    pass

class Match(MatchAction):
    def __call__(self, expected):
        message = "it[%s] should be %s" % (
            repr(self.expectation.value), repr(expected))
        assert self.expectation.value == expected, message
        pass
    pass
register("__eq__", lambda self, expected: Match(self.expectation)(expected))
register("be", property(lambda self: Match(self.expectation)))

class MatchNot(MatchAction):
    def __call__(self, expected):
        message = "it should not be %s" % (repr(self.expectation.value))
        assert self.expectation.value != expected, message
        pass
    pass
register("__ne__", lambda self, expected: MatchNot(self.expectation)(expected))
register("not_be", property(lambda self: MatchNot(self.expectation)))

class MatchInstance(MatchAction):
    def __call__(self, expected):
        message = "it[%s] should not be instance of %s" % (
            repr(self.expectation.value), repr(expected))
        assert isinstance(self.expectation.value, expected), message
        pass
    pass
register("be_instance_of", 
         property(lambda self: MatchInstance(self.expectation)))


class MatchExist(MatchAction):
    def __call__(self):
        message = "it[%s] does not exist" % (self.expectation.value)
        assert self.expectation.value is not None, message
        pass
    pass
register("exist", property(lambda self: MatchExist(self.expectation)()))

class MatchIn(MatchAction):
    def __call__(self, expected):
        message = "it[%s] does not exist in %s" % (
            self.expectation.value, expected)
        assert self.expectation.value in expected, message
        pass
    pass
register("be_in", property(lambda self: MatchIn(self.expectation)))

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
register("be_each_of", property(lambda self: MatchEach(self.expectation)))

class MatchTrue(MatchAction):
    def __call__(self):
        message = "it[%s] should be True" % (self.expectation.value)
        assert self.expectation.value, message
        pass
    pass
register("be_true", property(lambda self: MatchTrue(self.expectation)()))

class MatchFalse(MatchAction):
    def __call__(self):
        message = "it[%s] should be False" % (self.expectation.value)
        assert not self.expectation.value, message
        pass
    pass
register("be_false", property(lambda self: MatchTrue(self.expectation)()))

