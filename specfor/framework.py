import functools
import unittest

class Spec(unittest.TestCase):
    def setUp(self):
        for prepare in self.prepares:
            prepare(self)
            pass
        pass
    def tearDown(self):
        for cleanup in self.cleanups:
            cleanup(self)
            pass
        pass
    pass

# spec TestCase creator

class AddPrepare(object):
    def __init__(self, spec_type):
        self.spec_type = spec_type
        self.spec_type.prepares = []
        pass
    def __call__(self):
        def decorator(prepare):
            self.spec_type.prepares.append(prepare)
            return prepare
        return decorator
    pass

class AddCleanUp(object):
    def __init__(self, spec_type):
        self.spec_type = spec_type
        self.spec_type.cleanups = []
        pass
    def __call__(self):
        def decorator(cleanup):
            self.spec_type.cleanuos.append(cleanup)
            return cleanup
        return decorator
    pass

class AddBehavior(object):
    def __init__(self, spec_type):
        self.spec_type = spec_type
        self.spec_type.behaviors = []
        pass
    def __call__(self, description):
        def decorator(behavior):
            @functools.wraps(behavior)
            def behavior_(its):
                return behavior(its)
            # prefix is for unittest
            name = "%s: %s" % (
                unittest.TestLoader.testMethodPrefix, description)
            setattr(self.spec_type, name, behavior_)
            behavior_.definition = behavior
            behavior_.description = description
            behavior_.__test__ = True # __test__ for nose
            behavior_.__name__ = description
            self.spec_type.behaviors.append(name)
            return behavior
        return decorator
    def __getitem__(self, name):
        return self.__call__(name)
    pass

class MakeSpec(object):
    def __call__(self, name):
        spec_type = type(name, (Spec,), {})
        spec_type.before = AddPrepare(spec_type)
        spec_type.after = AddCleanUp(spec_type)
        spec_type.that = AddBehavior(spec_type)
        return spec_type
    def __getitem__(self, name):
        return self.__call__(name)
    pass

# DSL
class Engine(object):
    def publish(self, globals_):
        if globals_["__name__"] == "__main__": 
            return unittest.main()
        return
    pass

spec = Engine()
spec.of = MakeSpec()
__all__ = ["spec"]

