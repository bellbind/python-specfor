import functools
import unittest

class Bundle(object):
    def setUp(its):
        for prepare in its.prepares:
            prepare(its)
            pass
        pass
    def tearDown(its):
        for cleanup in its.cleanups:
            cleanup(its)
            pass
        pass
    pass
class Spec(Bundle, unittest.TestCase):
    
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
            self.spec_type.cleanups.append(cleanup)
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
            behavior_.definition = behavior
            behavior_.description = description
            behavior_.__test__ = True # __test__ for nose
            behavior_.__name__ = description
            
            name = "%s: %s" % (
                unittest.TestLoader.testMethodPrefix, description)
            setattr(self.spec_type, name, behavior_)
            self.spec_type.behaviors.append(name)
            return behavior
        return decorator
    def __getitem__(self, name):
        return self.__call__(name)
    pass

class BundleBehavior(object):
    def __init__(self, bundle, behavior):
        self.bundle = bundle
        self.behavior = behavior
        self.setup = None
        pass
    def to_func(self):
        behavior = self.behavior.definition
        @functools.wraps(behavior)
        def behavior_(its):
            if self.setup: self.setup(its)
            for prepare in self.bundle.prepares:
                prepare(its)
                pass
            try:
                behavior(its)
            finally:
                for cleanup in self.bundle.cleanups:
                    cleanup(its)
                    pass
                pass
            pass
        description = "[%s] %s" % (
            self.bundle.__name__, self.behavior.description)
        behavior_.definition = behavior
        behavior_.description = description
        behavior_.__test__ = True # __test__ for nose
        behavior_.__name__ = description
        return behavior_
    pass

class AddBundle(object):
    def __init__(self, spec_type):
        self.spec_type = spec_type
        self.spec_type.bundles = []
        self.spec_type.bundlebehaviors = []
        pass
    def __call__(self, bundle):
        bundlebehaviors = []
        for name in bundle.behaviors:
            behavior = getattr(bundle, name)
            bb = BundleBehavior(bundle, behavior)
            behavior_ = bb.to_func()
            name = "%s:%s" % (
                unittest.TestLoader.testMethodPrefix, 
                behavior_.description)
            setattr(self.spec_type, name, behavior_)
            bundlebehaviors.append(bb)
            self.spec_type.bundlebehaviors.append(bb)
            pass
        self.spec_type.bundles.append(bundle)
        
        def decorator(setup):
            for bb in bundlebehaviors:
                bb.setup = setup
                pass
            return setup
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
        spec_type.of = AddBundle(spec_type)
        return spec_type
    def __getitem__(self, name):
        return self.__call__(name)
    pass
class MakeBundle(object):
    def __call__(self, name):
        spec_type = type(name, (Bundle,), {})
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
    
    def run(self, spec, result=None):
        result = result or unittest.TestResult()
        for name in [n for n in dir(spec) if n.startswith("test")]:
            test = spec(name)
            test.run(result)
            pass
        return result
    
    of = MakeSpec()
    behaviors_of = MakeBundle()
    pass

spec = Engine()
__all__ = ["spec"]

