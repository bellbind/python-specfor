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
        message = "it[%s] should be %s"
        assert self.expectation.value == expected, message % (
            repr(self.expectation.value), repr(expected))
        pass
    pass
register("__eq__", lambda self, expected: Match(self.expectation)(expected))
register("be", property(lambda self: Match(self.expectation)))

class MatchNot(MatchAction):
    def __call__(self, expected):
        message = "it[%s] should not be %s"
        assert self.expectation.value != expected, message % (
            repr(self.expectation.value), expected)
        pass
    pass
register("__ne__", lambda self, expected: MatchNot(self.expectation)(expected))
register("not_be", property(lambda self: MatchNot(self.expectation)))

class MatchTrue(MatchAction):
    def __call__(self):
        message = "it should be True"
        assert self.expectation.value, message
        pass
    pass
register("be_true", property(lambda self: MatchTrue(self.expectation)()))
register("be_ok", property(lambda self: MatchTrue(self.expectation)()))

class MatchFalse(MatchAction):
    def __call__(self):
        message = "it should be False"
        assert not self.expectation.value, message
        pass
    pass
register("be_false", property(lambda self: MatchFalse(self.expectation)()))
register("be_no", property(lambda self: MatchFalse(self.expectation)()))



class MatchExist(MatchAction):
    def __call__(self):
        message = "it[%s] does not exist"
        assert self.expectation.value is not None, message % (
            self.expectation.value)
        pass
    pass
register("exist", property(lambda self: MatchExist(self.expectation)()))

class MatchNotExist(MatchAction):
    def __call__(self):
        message = "it[%s] exists"
        assert self.expectation.value is None, message % (
            self.expectation.value)
        pass
    pass
register("not_exist", property(lambda self: MatchNotExist(self.expectation)()))

class MatchIn(MatchAction):
    def __call__(self, expected):
        message = "it[%s] does not exist in %s"
        assert self.expectation.value in expected, message % (
            self.expectation.value, expected)
        pass
    pass
register("be_in", property(lambda self: MatchIn(self.expectation)))

class MatchNotIn(MatchAction):
    def __call__(self, expected):
        message = "it[%s] exists in %s"
        assert self.expectation.value not in expected, message % (
            self.expectation.value, expected)
        pass
    pass
register("not_be_in", property(lambda self: MatchNotIn(self.expectation)))

class MatchInstance(MatchAction):
    def __call__(self, expected):
        message = "it[%s] should be instance of %s"
        assert isinstance(self.expectation.value, expected), message % (
            repr(self.expectation.value), repr(expected))
        pass
    pass
register("be_instance_of", 
         property(lambda self: MatchInstance(self.expectation)))

class MatchSame(MatchAction):
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
        
        assert not lefts and not not_founds, "".join(
            ["%s should not be in it" % lefts if lefts else "",
             ", and " if lefts and not_founds else "",
             "%s should be in it" % not_founds if not_founds else ""])
        pass
    pass
register("be_same_as", property(lambda self: MatchSame(self.expectation)))


class MatchSameOrder(MatchAction):
    def __call__(self, expected):
        value = list(self.expectation.value)
        exp = list(expected)
        assert value == exp, "diff:\n%s" % (
            "\n".join(difflib.ndiff(
                    [repr(v) for v in value],
                    [repr(v) for v in exp])))
        pass
    pass
register("be_same_order_as", 
         property(lambda self: MatchSameOrder(self.expectation)))


