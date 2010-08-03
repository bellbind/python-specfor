import difflib
import functools

from . import match


class ValueExpectation(object):
    def __init__(self, lazy):
        self.lazy = lazy
        pass
    def __getattr__(self, name):
        lazy = lambda: getattr(self.value, name)
        lazy.__name__ = name
        return ValueExpectation(lazy=lazy)
    def __call__(self, *args, **kwargs):
        lazy = lambda: self.value.__call__(*args, **kwargs)
        lazy.__name__ = "__call__"
        return ValueExpectation(lazy=lazy)
    def __enter__(self):
        return self
    def __exit__(self, type, exc, traceback):
        return type is None
    @property
    def value(self):
        return self.lazy()
    @property
    def should(self):
        return match.MatchActions(self)
    def applying(self, func):
        lazy = functools.wraps(func)(lambda: func(self.value))
        return ValueExpectation(lazy)
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
class Raising(object):
    def __getitem__(self, value):
        return ErrorExpectation(value)
    pass
class The(object):
    raising = Raising()
    def __getitem__(self, value):
        return ValueExpectation(lambda:value)
    pass


the = The()
__all__ = ["the"]

